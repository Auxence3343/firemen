from tkinter import *


class Image:
    """ cette classe regroupe touts le code destiné a la manipulation d'images
     afin de simplifier la gestion de celles ci"""
    def __init__(self, x, y, file, canvas, screen_origin_x, screen_origin_y):
        __slots__ = 'canvas'

        self.x = x
        self.y = y
        self.canvas = canvas

        self.file = PhotoImage(file=file)
        if screen_origin_x <= x <= screen_origin_x + self.canvas.winfo_width() and \
           screen_origin_y <= y <= screen_origin_y + self.canvas.winfo_height():
            self.image = self.canvas.create_image(x, y, image=self.file)
        else:
            self.image = 0

    def move(self, delta_x, delta_y):
        """ déplace l'image relativement a sa position precedente """
        self.canvas.move(self.image, delta_x, delta_y)
        self.x += delta_x
        self.y += delta_y
        self.canvas.update()

    def move_to(self, x, y):
        """ déplace l'image a une position absolue du canvas"""
        delta_x = self.x + x
        delta_y = self.y + y

        self.move(delta_x, delta_y)

    def change_image(self, nouvelle_image):
        """ change l'image """
        del self.image
        self.file = PhotoImage(file=nouvelle_image)
        self.image = self.canvas.create_image(self.x, self.y, image=self.file)
