from random import *

class Map:
    def __init__(self, largeur, hauteur):
        self.hauteur = hauteur
        self.largeur = largeur
        self.heat_map = []
        self.map = [["."] * hauteur] * largeur
        self.list_heat_points_visited = []

    def cursor(self, x, y, layer):
        print("------\n", layer, x, y, "\n------")
        voisins = [(x + 1, y + 1), (x, y + 1), (x - 1, y + 1),
                   (x + 1, y + 0), (x - 1, y + 0),
                   (x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]
        for case in voisins:
            if 0 <= case[0] <= self.largeur - 1 and 0 <= case[1] <= self.hauteur - 1:
                if not ((case[0], case[1]) in self.list_heat_points_visited[layer]):
                    self.list_heat_points_visited[layer].append((case[0], case[1]))
                    self.cursor(case[0], case[1], layer)
                    print(case)

    def generate_heat_map_layer(self):

        self.heat_map.append([])
        self.list_heat_points_visited.append([])
        x = randint(0, self.hauteur - 1)
        y = randint(0, self.largeur - 1)
        self.cursor(x, y, len(self.heat_map) - 1)

    def make_heat_map(self, nb_points):
        for point in [None] * nb_points :
            self.generate_heat_map_layer()

    def display(self):
        """affiche la map"""
        for y in self.list_heat_points_visited:
            print("| ", end="")
            for x in y:
                print(x, "| ", end="")
            print("")


def main():
    """teste la generation de map"""
    map_de_test = Map(20, 20)
    map_de_test.make_heat_map(3)
    map_de_test.display()


if __name__ == "__main__" :
    main()
