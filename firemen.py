from time import *
from tkinter import *
from classes_images import *
from map import *
from pompiers import *


class App:
    def __init__(self, hauteur, largeur):
        """ initialise les variables 'globales' de l'application et lance le jeu"""
        self.root = Tk()
        self.root.title("Firemen")
        self.hauteur = hauteur
        self.largeur = largeur
        self.canvas = Canvas(self.root, width=self.largeur, height=self.hauteur, background="#000")
        self.canvas.pack()

        self.carte = Matrice(hauteur=720 // 16 + 1, largeur=1080 // 16 + 1, canvas=self.canvas)
        self.pompier = ToutLesPompiers(Matrice)
        self.routine()
        self.root.mainloop()

    def routine(self):
        """ fonction qui se relance a chaque 'tick' du jeu"""
        self.canvas.update()
        self.carte.actualiser_l_incendie("mode_normal")

        self.root.after(0, self.routine)


def main():
    """ une fonction 'main' au cas ou le jeu est appelé depuis un autre fichier sous ce nom là"""
    App(hauteur=720, largeur=1080)


if __name__ == "__main__":
    App(hauteur=720, largeur=1080)
