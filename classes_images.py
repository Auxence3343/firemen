from tkinter import *


class Image:
    """ cette classe regroupe touts le code destiné a la manipulation d'images
     afin de simplifier la gestion de celles ci"""
    def __init__(self, x, y, file, canvas, origine_ecran_x, origine_ecran_y):

        self.x = x
        self.y = y
        self.canvas = canvas

        self.fichier = PhotoImage(file=file)
        if origine_ecran_x <= x <= origine_ecran_x + self.canvas.winfo_width() and \
           origine_ecran_y <= y <= origine_ecran_y + self.canvas.winfo_height():
            self.image = self.canvas.create_image(x, y, image=self.fichier)
        else:
            self.image = 0

    def deplacer(self, delta_x, delta_y):
        """ déplace l'image relativement a sa position precedente """
        self.canvas.deplacer(self.image, delta_x, delta_y)
        self.x += delta_x
        self.y += delta_y
        self.canvas.update()

    def deplacer_vers(self, x, y):
        """ déplace l'image a une position absolue du canvas"""
        delta_x = self.x + x
        delta_y = self.y + y

        self.deplacer(delta_x, delta_y)

    def change_image(self, nouvelle_image):
        """ change l'image """
        del self.image
        self.fichier = PhotoImage(file=nouvelle_image)
        self.image = self.canvas.create_image(self.x, self.y, image=self.fichier)
