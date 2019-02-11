from time import *
from tkinter import *
from classes_images import *

class App:
    def __init__(self, hauteur, largeur):
        self.root = Tk()
        self.root.title = "Firemen"
        self.hauteur = hauteur
        self.largeur = largeur
        self.canvas = Canvas(self.root, width=self.largeur, height=self.hauteur, background="#000")
        self.canvas.pack()

        self.compte = 40
        self.refresh()
        self.root.mainloop()

    def get_canvas(self):
        return self.canvas

    def refresh(self):
        sleep(1)
        test = Image(50, 50, "arbre.gif", self.canvas)
        self.compte += 1
        test.move_to((self.compte % (600 / 16)) * 16, 100)
        self.canvas.update()
        self.root.after(0, self.refresh)


def main():
    firemen = App(hauteur=400, largeur=640)
    del firemen


if __name__ == "__main__":
    main()
