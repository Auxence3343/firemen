from tkinter import *


def routine(root):
    """ la fonction qui s'execute en boucle
    a chaque rendu d'image"""

    root.after(0, routine, root)


def main():
    root = Tk()
    root.title = "Firemen"
    canvas = Canvas(root, width=640, height=400)
    canvas.pack()

    #routine(root)

    root.mainloop()


if __name__ == "__main__" :
    main()
