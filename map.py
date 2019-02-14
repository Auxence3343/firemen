from random import *
from math import *
from classes_images import *


def display(carte):
    """affiche la map"""
    for y in carte:
        print("| ", end="")
        for x in y:
            print(x, "| ", end="")
        print("")


class Arbre:
    def __init__(self, x, y, espece, alive, burning, dead, canvas):
        self.state = "alive"
        self.espece = espece  # le type d'arbre ( herbe, arbre, buisson )
        self.canvas = canvas

        if self.type == "arbre":
            self.time_before_death = 6
        elif self.type == "buisson":
            self.time_before_death = 4
        else:
            self.time_before_death = 2

        self.alive = PhotoImage(file=alive)
        self.burning = PhotoImage(file=burning)
        self.dead = PhotoImage(file=dead)

        self.image = Image(x, y, self.alive, self.canvas)

    def burn(self):
        self.state = "burning"
        self.image.image['file'] = self.burning

    def is_burnt(self):
        if self.state == "burning" :
            if self.time_before_death > 0:
                self.time_before_death -= 1
            else:
                self.state = "burnt"
                self.image.image['file'] = self.burnin



class Map:
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

    def generate_heat_map_layer(self):
        """ crée une couche de la heat map """

        self.heat_map_layer.append([])
        self.list_heat_points_visited.append([])
        self.list_heat_points.append([])
        layer = len(self.heat_map_layer) - 1
        x = randint(0, self.hauteur - 1)
        y = randint(0, self.largeur - 1)

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
        display(self.map)


def main():
    """teste la generation de map"""
    map_de_test = Map(50, 50)
    map_de_test.make_map("/\\", "##", "..")


if __name__ == "__main__":
    main()
