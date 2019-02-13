from random import *
from math import *


def display(carte):
    """affiche la map"""
    for y in carte:
        print("| ", end="")
        for x in y:
            if x < 10:
                print("0" + str(x), "| ", end="")
            else:
                print(x, "| ", end="")
        print("")

class Map:
    def __init__(self, largeur, hauteur):
        """ crée la map"""
        self.hauteur = hauteur
        self.largeur = largeur
        self.heat_map = []
        self.map = [["."] * hauteur] * largeur
        self.list_heat_points = []
        self.list_heat_points_visited = []

    def cursor(self, x, y, layer, distance):
        """ méthode recursive qui passe par toute les cases du terrain"""
        # print("------\n", layer, x, y, "\n------")
        voisins = [(x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)]
        for case in voisins:
            if 0 <= case[0] <= self.largeur - 1 and 0 <= case[1] <= self.hauteur - 1:
                if not ((case[0], case[1]) in self.list_heat_points_visited[layer]):
                    self.list_heat_points_visited[layer].append((case[0], case[1]))
                    self.list_heat_points[layer].append((case[0], case[1], distance))
                    self.cursor(case[0], case[1], layer, distance + 1)
                    # print(case)

    def generate_heat_map_layer(self):
        """ crée une couche de la heat map """

        self.heat_map.append([])
        self.list_heat_points_visited.append([])
        self.list_heat_points.append([])
        layer = len(self.heat_map) - 1
        x = randint(0, self.hauteur - 1)
        y = randint(0, self.largeur - 1)

        self.cursor(x, y, layer, 0)

        for y_list in range(self.hauteur):
            self.heat_map[layer].append([])
            for x_list in range(self.largeur):
                value = ceil(sqrt((x - x_list) ** 2 + (y - y_list) ** 2))
                self.heat_map[layer][y_list].append(value)

    def make_heat_map(self, nb_points):
        """ génère une matrice contenant la probabilité d'apparition d'un arbre pour chaque case"""
        for point in [None] * nb_points:
            self.generate_heat_map_layer()


def main():
    """teste la generation de map"""
    map_de_test = Map(5, 5)
    map_de_test.make_heat_map(3)
    display(map_de_test.heat_map[0])


if __name__ == "__main__":
    main()
