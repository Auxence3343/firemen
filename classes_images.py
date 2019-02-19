from tkinter import *


class Image:
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
            print(x, y, screen_origin_x, screen_origin_y,
                  screen_origin_x <= x <= screen_origin_x + self.canvas.winfo_width(),
                  screen_origin_x + self.canvas.winfo_width())
        self.canvas.update()

    def move(self, delta_x, delta_y):

        self.canvas.move(self.image, delta_x, delta_y)
        self.x += delta_x
        self.y += delta_y
        self.canvas.update()

    def move_to(self, x, y):

        delta_x = self.x + x
        delta_y = self.y + y

        self.move(delta_x, delta_y)

    def change_image(self, nouvelle_image):
        self.image['file'] = nouvelle_image
