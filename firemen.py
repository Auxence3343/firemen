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

        test = Image(50, 50, "arbre.gif", self.canvas)
        sleep(1)
        test.move_to(100, 100)
        self.root.mainloop()

    def get_canvas(self):
        return self.canvas

    def refresh(self):
        self.canvas.update()
        self.root.after(0, self.refresh)


def main():
    firemen = App(hauteur=400, largeur=640)


if __name__ == "__main__":
    main()
