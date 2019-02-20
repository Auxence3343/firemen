from random import *
from math import *
from classes_images import *
from time import *


def display(carte):
    """affiche la map"""
    for y in carte:
        print("| ", end="")
        for x in y:
            print(x, "| ", end="")
        print("")


class Arbre:
    """ représente un arbre"""
    def __init__(self, x, y, espece, alive, burning, dead, canvas, pos_matrix_x, pos_matrix_y,
                 x_matrix_arbre, y_matrix_arbre):
        self.state = "alive"
        self.espece = espece  # le type d'arbre ( herbe, arbre, buisson )
        self.canvas = canvas
        self.date_de_mise_a_feu = 0
        # position de la case de l'arbre dans la matrice
        self.x_matrix_arbre = x_matrix_arbre
        self.y_matrix_arbre = y_matrix_arbre

        if self.espece == "arbre":
            self.time_before_death = 6
        elif self.espece == "buisson":
            self.time_before_death = 4
        else:
            self.time_before_death = 2
        self.time_before_death *= randint(6, 14)/10
        self.alive = alive
        self.burning = burning
        self.dead = dead

        self.image = Image(x, y, self.alive, self.canvas, screen_origin_x=pos_matrix_x, screen_origin_y=pos_matrix_y)

    def make_burn(self):
        """ met le feu a l'arbre"""
        if self.state == "alive":
            self.state = "burning"
            self.date_de_mise_a_feu = time()
            self.image.change_image(self.burning)

    def kill(self):
        """ tue la plante"""
        self.state = "dead"
        self.image.change_image(self.dead)

    def check_combustion_stage(self):
        """ regarde ou la plante en est dans sa combustion"""
        if self.state == "burning" or self.state == "propagating fire":
            heure_actuelle = time()
            temps_depuis_la_mise_a_feu = heure_actuelle - self.date_de_mise_a_feu
            if temps_depuis_la_mise_a_feu > self.time_before_death:
                self.kill()
            elif self.state == "burning" and temps_depuis_la_mise_a_feu > self.time_before_death / 2:
                self.state = "propagating fire"

    def shift(self, delta_x, delta_y):
        """ déplace l'arbre"""
        self.image.move_to(delta_x, delta_y)


class Map:
    """ cette classe sert a générer la map sous la forme de caractères ascii, la veritable carte avec les instances
    d'arbres se trouve dans la classe matrix"""
    def __init__(self, largeur, hauteur):
        """ crée la map"""
        self.hauteur = hauteur
        self.largeur = largeur
        self.heat_map_layer = []
        self.list_heat_points = []
        self.list_heat_points_visited = []
        self.heat_map = []
        self.map = []

        self.make_map("/\\", "##", "..")

        del self.list_heat_points
        del self.list_heat_points_visited
        del self.heat_map
        del self.heat_map_layer

    def generate_heat_map_layer(self):
        """ crée une couche de la heat map (voir ci dessous)"""

        self.heat_map_layer.append([])
        self.list_heat_points_visited.append([])
        self.list_heat_points.append([])
        layer = len(self.heat_map_layer) - 1
        x = randint(0, self.largeur - 1)
        y = randint(0, self.hauteur - 1)

        for y_list in range(self.hauteur):
            self.heat_map_layer[layer].append([])
            for x_list in range(self.largeur):
                value = ceil(sqrt((x - x_list) ** 2 + (y - y_list) ** 2))
                self.heat_map_layer[layer][y_list].append(value)

    def make_heat_map(self, nb_points):
        """ génère une matrice contenant la probabilité d'apparition d'un arbre pour chaque case"""
        for point in [None] * nb_points:
            self.generate_heat_map_layer()

        # addition des couches de la heat_map
        self.heat_map = []

        for y in range(0, self.hauteur):  # passe par toutes les cases de la map
            self.heat_map.append([])
            for x in range(0, self.largeur):
                point = self.hauteur * self.largeur  # pour être sûr que les résultats ne sont pas faussés

                for couche in range(nb_points):  # additionne les différentes couches
                    if self.heat_map_layer[couche][y][x] < point:
                        point = self.heat_map_layer[couche][y][x]
                point = ceil(sqrt(point))  # uniformise les valeurs des points
                self.heat_map[y].append(point)

    def make_map(self, arbre, buisson, herbe):
        """ construit une version ascii de la map"""
        nb_bosquets = ceil(sqrt(self.hauteur * self.largeur) / 10)
        self.make_heat_map(nb_bosquets)
        self.map = []
        for y in range(0, self.hauteur):
            self.map.append([])
            for x in range(0, self.largeur):
                if self.heat_map[y][x] <= 2:  # haute densité
                    proba_grand_arbre = 0.9
                    proba_herbe = 0.1

                elif self.heat_map[y][x] == 3:  # moyenne densité
                    proba_grand_arbre = 0.2
                    proba_herbe = 0.2

                else:  # basse densité
                    proba_grand_arbre = 0.1
                    proba_herbe = 0.8

                valeur_aleatoire = randint(0, 100) / 100

                if valeur_aleatoire < proba_grand_arbre:
                    self.map[y].append(arbre)
                elif valeur_aleatoire > (1 - proba_herbe):
                    self.map[y].append(herbe)
                else:
                    self.map[y].append(buisson)

        #  display(self.heat_map)
        #  display(self.map)


class Matrix:
    """ gère la 'vraie' carte une fois qu'elle a ete générée par la classe Map
    Matrix s'occupe de :
        - l'affichage de la carte
        - la simulation de la propagation du feu
        - le déplacement de la vue du joueur ( en réalité, on 'déplace' juste la carte dans le sens inverse au
         déplacement de la camera"""
    def __init__(self, hauteur, largeur, canvas):

        self.hauteur_image = 16
        self.largeur_image = 16

        self.pos_matrix_x = 0
        self.pos_matrix_y = 0

        self.map_in_ascii = Map(hauteur=hauteur, largeur=largeur).map  # recupere la carte generee par Map
        #  display(self.map_in_ascii)
        self.canvas = canvas
        self.map = []

        # le code ci dessous "traduit" l'ascii en classes 'Arbre'
        canvas.update()
        for ligne in range(len(self.map_in_ascii)):
            self.map.append([])
            canvas.update()
            for colonne in range(len(self.map_in_ascii[ligne])):

                symbole_ascii = self.map_in_ascii[ligne][colonne]

                pos_arbre_x = self.largeur_image * colonne
                pos_arbre_y = self.hauteur_image * ligne

                if symbole_ascii == "/\\":
                    espece = "arbre"
                    image_vivant = "arbre.gif"
                    image_en_feu = "feu.gif"
                    image_mort = "cendres.gif"
                elif symbole_ascii == "##":
                    espece = "buisson"
                    image_vivant = "buisson.gif"
                    image_en_feu = "feu.gif"
                    image_mort = "cendres.gif"
                else:
                    espece = "herbe"
                    image_vivant = "herbe.gif"
                    image_en_feu = "feu.gif"
                    image_mort = "cendres.gif"

                self.map[ligne].append(Arbre(x=pos_arbre_x + self.largeur_image/2, y=pos_arbre_y + self.hauteur_image/2,
                                             espece=espece, alive=image_vivant, pos_matrix_x=self.pos_matrix_x,
                                             pos_matrix_y=self.pos_matrix_y, burning=image_en_feu, dead=image_mort,
                                             canvas=canvas, x_matrix_arbre=colonne, y_matrix_arbre=ligne))

        self.map[randint(0, len(self.map) - 1)][randint(0, len(self.map) - 1)].make_burn()

    def strafe(self, x, y):
        pass

    def update_fire(self):
        """ met a jour la propagation du feu"""
        x_min_matrix = 0
        y_min_matrix = 0

        y_max_matrix = len(self.map) - 1
        for ligne in range(len(self.map)):

            x_max_matrix = len(self.map[ligne]) - 1
            for colonne in range(len(self.map[ligne])):

                arbre = self.map[ligne][colonne]
                arbre.check_combustion_stage()

                if arbre.state == "propagating fire":
                    voisins = [[arbre.x_matrix_arbre + 1, arbre.y_matrix_arbre],
                               [arbre.x_matrix_arbre, arbre.y_matrix_arbre + 1],
                               [arbre.x_matrix_arbre - 1, arbre.y_matrix_arbre],
                               [arbre.x_matrix_arbre, arbre.y_matrix_arbre - 1]]

                    for case in voisins:
                        #  print(case)
                        if x_min_matrix <= case[0] <= x_max_matrix and y_min_matrix <= case[1] <= y_max_matrix:
                            self.map[case[1]][case[0]].make_burn()


def main():
    """teste la generation de map"""
    display(Map(50, 50).map)


if __name__ == "__main__":
    main()
