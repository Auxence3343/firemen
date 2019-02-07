from tkinter import *


def routine(root):
    """ la fonction qui s'execute en boucle
    a chaque rendu d'image"""

    root.after(0, routine, root)


def main():
    root = Tk()
    root.title = "Firemen"

    routine(root)

    root.mainloop()


if __name__ == "__main__" :
    main()
