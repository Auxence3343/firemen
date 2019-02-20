from time import *
from tkinter import *
from classes_images import *
from map import *


class App:
    def __init__(self, hauteur, largeur):
        """ initialise les variables 'globales' de l'application et lance le jeu"""
        self.root = Tk()
        self.root.title("Firemen")
        self.hauteur = hauteur
        self.largeur = largeur
        self.canvas = Canvas(self.root, width=self.largeur, height=self.hauteur, background="#000")
        self.canvas.pack()

        self.map = Matrix(hauteur=720//16 + 1, largeur=1080//16 + 1, canvas=self.canvas)

        self.refresh()
        self.root.mainloop()

    def refresh(self):
        """ fonction qui se relance a chaque 'tick' du jeu"""
        self.canvas.update()
        self.map.update_fire()

        self.root.after(0, self.refresh)


def main():
    """ une fonction 'main' au cas ou le jeu est appelé depuis un autre fichier sous ce nom là"""
    App(hauteur=720, largeur=1080)


if __name__ == "__main__":
    App(hauteur=720, largeur=1080)
