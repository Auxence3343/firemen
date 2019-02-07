from tkinter import *


class App:
    def __init__(self, hauteur, largeur):
        self.root = Tk()
        self.root.title = "Firemen"
        self.hauteur = hauteur
        self.largeur = largeur
        self.canvas = Canvas(self.root,\
                             width=self.largeur,\
                             height=self.hauteur)

        self.root.mainloop()

    def refresh(self):
        pass


def main():
    firemen = App(hauteur=640, largeur=400)


if __name__ == "__main__":
    main()
