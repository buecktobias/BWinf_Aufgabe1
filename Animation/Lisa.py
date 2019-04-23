import math
import tkinter

from PIL import Image, ImageTk


class Lisa:
    def __init__(self, canvas, x, y, velocity):
        self.velocity = velocity
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        pil_image: Image = Image.open("Lisa.png")
        pil_image = pil_image.resize((20, 30))
        self.image = ImageTk.PhotoImage(pil_image)
        self.canvas_image = None
        self.canvas: tkinter.Canvas = canvas
        self.to_x = x
        self.to_y = y

    def move_to(self, to_x, to_y):
        x_difference = to_x - self.x
        y_difference = to_y - self.y
        angle = math.atan2(y_difference, x_difference)
        self.x_speed = math.cos(angle) * self.velocity
        self.y_speed = math.sin(angle) * self.velocity
        self.to_x = to_x
        self.to_y = to_y

    def update(self):
        if round(self.x) == self.to_x and round(self.y) == self.to_y:
            self.x_speed = 0
            self.y_speed = 0
        self.x += self.x_speed
        self.y += self.y_speed
        self.canvas.delete(self.canvas_image)
        self.show()

    def show(self):
        self.canvas_image = self.canvas.create_image(self.x, self.y, image=self.image)
        self.canvas.pack()
        self.canvas.update()
