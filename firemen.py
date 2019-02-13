from time import *
from tkinter import *
from classes_images import *


class App:
    def __init__(self, hauteur, largeur):
        """ initialise les variables 'globales' de l'application et lance le jeu"""
        self.root = Tk()
        self.root.title("Firemen")
        self.hauteur = hauteur
        self.largeur = largeur
        self.canvas = Canvas(self.root, width=self.largeur, height=self.hauteur, background="#000")
        self.canvas.pack()

        self.compte = 40
        self.refresh()
        self.root.mainloop()

    def refresh(self):
        """ fonction qui se relance a chaque 'tick' du jeu"""
        self.canvas.update()
        test = Image(8, 8, "arbre.gif", self.canvas)
        self.compte += 1
        test.move_to(self.compte % 37 * 16, 0)
        sleep(0.2)
        self.root.after(0, self.refresh)


def main():
    App(hauteur=400, largeur=640)


if __name__ == "__main__":
    main()
