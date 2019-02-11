class Image:
    def __init__(self, x, y, file, canvas):

        self.x = x
        self.y = y
        self.canvas = canvas
        self.image = self.canvas.create_image(x, y, image=file)
        self.canvas.update()

    def move(self, delta_x, delta_y):

        self.canvas.move(self.image, delta_x, delta_y)
        self.x += delta_x
        self.y += delta_y
        self.canvas.update()

    def move_to(self, x, y):

        delta_x = self.x - x
        delta_y = self.y - y

        self.move(delta_x, delta_y)

