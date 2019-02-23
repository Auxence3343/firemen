from random import *
from math import *
from classes_images import *
from time import *


def afficher_carte(carte):
    """affiche la carte"""
    for y in carte:
        print("| ", end="")
        for x in y:
            print(x, "| ", end="")
        print("")


class Arbre:
    """ représente un arbre"""
    def __init__(self, x, y, espece, image_vivant, image_en_feu, image_mort, canvas, pos_matrice_x, pos_matrice_y,
                 abscisse_de_l_arbre_dans_la_matrice, ordonne_de_l_arbre_dans_la_matrice):
        self.etat = "vivant"
        self.espece = espece  # le type d'arbre ( herbe, arbre, buisson )
        self.canvas = canvas
        self.date_de_mise_a_feu = 0

        # position de la case de l'arbre dans la matrice
        self.x_matrice_arbre = abscisse_de_l_arbre_dans_la_matrice
        self.y_matrice_arbre = ordonne_de_l_arbre_dans_la_matrice

        if self.espece == "arbre":
            self.temps_avant_la_mort = 0.5
        elif self.espece == "buisson":
            self.temps_avant_la_mort = 0.5
        else:
            self.temps_avant_la_mort = 0.5
        self.temps_avant_la_mort *= randint(6, 14) / 10
        self.image_vivant = image_vivant
        self.image_en_feu = image_en_feu
        self.image_mort = image_mort

        self.image = Image(x, y, self.image_vivant, self.canvas,
                           origine_ecran_x=pos_matrice_x, origine_ecran_y=pos_matrice_y)

    def faire_bruler(self):
        """ met le feu a l'arbre"""
        if self.etat == "vivant":
            self.etat = "en feu"
            self.date_de_mise_a_feu = time()
            self.image.change_image(self.image_en_feu)

    def tuer(self):
        """ tue la plante"""
        self.etat = "mort"
        self.image.change_image(self.image_mort)

    def actualiser_la_combustion(self):
        """ regarde ou la plante en est dans sa combustion"""
        if self.etat == "en feu" or self.etat == "propage le feu":
            heure_actuelle = time()
            temps_depuis_la_mise_a_feu = heure_actuelle - self.date_de_mise_a_feu
            if temps_depuis_la_mise_a_feu > self.temps_avant_la_mort:
                self.tuer()
            elif self.etat == "en feu" and temps_depuis_la_mise_a_feu > self.temps_avant_la_mort / 2:
                self.etat = "propage le feu"

    def shift(self, delta_x, delta_y):
        """ déplace l'arbre"""
        self.image.deplacer_vers(delta_x, delta_y)


class GenerateurDeForet:
    """ cette classe sert a générer la carte sous la forme de caractères ascii, la veritable carte avec les instances
    d'arbres se trouve dans la classe matrix"""
    def __init__(self, largeur, hauteur):
        """ crée la carte"""
        self.hauteur = hauteur
        self.largeur = largeur
        self.Couche_de_la_heat_map = []
        self.liste_des_points_chauds = []
        self.liste_des_points_chauds_visites = []
        self.heat_map = []
        self.map = []

        self.generer_carte("/\\", "##", "..")

        del self.liste_des_points_chauds
        del self.liste_des_points_chauds_visites
        del self.heat_map
        del self.Couche_de_la_heat_map

    def generer_couche_de_heat_map(self):
        """ crée une couche de la heat carte (voir ci dessous)"""

        self.Couche_de_la_heat_map.append([])
        self.liste_des_points_chauds_visites.append([])
        self.liste_des_points_chauds.append([])
        index_de_la_couche_actuelle = len(self.Couche_de_la_heat_map) - 1
        x = randint(0, self.largeur - 1)
        y = randint(0, self.hauteur - 1)

        for y_list in range(self.hauteur):
            self.Couche_de_la_heat_map[index_de_la_couche_actuelle].append([])
            for x_list in range(self.largeur):
                valeur_de_la_case = ceil(sqrt((x - x_list) ** 2 + (y - y_list) ** 2))
                self.Couche_de_la_heat_map[index_de_la_couche_actuelle][y_list].append(valeur_de_la_case)

    def assembler_heat_map(self, nb_points):
        """ génère une matrice contenant la probabilité d'apparition d'un arbre pour chaque case"""
        for point in [None] * nb_points:
            self.generer_couche_de_heat_map()

        # addition des couches de la heat_map
        self.heat_map = []

        for y in range(0, self.hauteur):  # passe par toutes les cases de la carte
            self.heat_map.append([])
            for x in range(0, self.largeur):
                point = self.hauteur * self.largeur  # pour être sûr que les résultats ne sont pas faussés

                for couche in range(nb_points):  # additionne les différentes couches
                    if self.Couche_de_la_heat_map[couche][y][x] < point:
                        point = self.Couche_de_la_heat_map[couche][y][x]
                point = ceil(sqrt(point))  # uniformise les valeurs des points
                self.heat_map[y].append(point)

    def generer_carte(self, arbre, buisson, herbe):
        """ construit une version ascii de la carte"""
        nb_bosquets = ceil(sqrt(self.hauteur * self.largeur) / 10)
        self.assembler_heat_map(nb_bosquets)
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

        #  afficher_carte(self.heat_map)
        #  afficher_carte(self.carte)


class Matrice:
    """ gère la 'vraie' carte une fois qu'elle a ete générée par la classe GenerateurDeForet
    Matrice s'occupe de :
        - l'affichage de la carte
        - la simulation de la propagation du feu
        - le déplacement de la vue du joueur ( en réalité, on 'déplace' juste la carte dans le sens inverse au
         déplacement de la camera"""
    def __init__(self, hauteur, largeur, canvas):

        self.hauteur_image = 16
        self.largeur_image = 16

        # la position du coin en haut a gauche de l'ecran
        self.origine_ecran_x = 0
        self.origine_ecran_y = 0

        # "carte en ascii" récupère la carte générée par GenerateurDeForet
        self.carte_en_ascii = GenerateurDeForet(hauteur=hauteur, largeur=largeur).map

        self.canvas = canvas
        self.map = []

        # le code ci dessous "traduit" l'ascii en classes 'Arbre'
        canvas.update()
        for ligne in range(len(self.carte_en_ascii)):
            self.map.append([])
            canvas.update()
            for colonne in range(len(self.carte_en_ascii[ligne])):

                symbole_ascii = self.carte_en_ascii[ligne][colonne]

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
                                             espece=espece,
                                             pos_matrice_x=self.origine_ecran_x, pos_matrice_y=self.origine_ecran_y,
                                             image_vivant=image_vivant,
                                             image_en_feu=image_en_feu,
                                             image_mort=image_mort,
                                             canvas=canvas,
                                             abscisse_de_l_arbre_dans_la_matrice=colonne,
                                             ordonne_de_l_arbre_dans_la_matrice=ligne))

        self.map[randint(0, len(self.map) - 1)][randint(0, len(self.map) - 1)].faire_bruler()

    def deplacer_matrice(self, x, y):
        pass

    def actualiser_l_incendie(self):
        """ met a jour la propagation du feu"""
        x_min_matrice = 0
        y_min_matrice = 0

        y_max_matrice = len(self.map) - 1
        for ligne in range(len(self.map)):

            x_max_matrice = len(self.map[ligne]) - 1
            for colonne in range(len(self.map[ligne])):

                arbre = self.map[ligne][colonne]
                arbre.actualiser_la_combustion()

                if arbre.etat == "propage le feu":
                    voisins = [[arbre.x_matrice_arbre + 1, arbre.y_matrice_arbre],
                               [arbre.x_matrice_arbre, arbre.y_matrice_arbre + 1],
                               [arbre.x_matrice_arbre - 1, arbre.y_matrice_arbre],
                               [arbre.x_matrice_arbre, arbre.y_matrice_arbre - 1]]

                    for case in voisins:
                        if x_min_matrice <= case[0] <= x_max_matrice and y_min_matrice <= case[1] <= y_max_matrice:
                            self.map[case[1]][case[0]].faire_bruler()


def main():
    """teste la generation de carte"""
    afficher_carte(GenerateurDeForet(50, 50).map)


if __name__ == "__main__":
    main()
