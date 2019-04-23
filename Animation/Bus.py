import tkinter
from PIL import Image, ImageTk
from PIL import *

class Bus:
    def __init__(self, canvas: tkinter.Canvas, x, y, width, height, x_speed, y_speed):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.width = width
        self.height = height
        self.image = None
        self.show()

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.canvas.delete(self.image)
        self.show()

    def show(self):
        pil_image: Image = Image.open("Bus.jpg")
        pil_image = pil_image.resize((20, 20))
        img = ImageTk.PhotoImage(pil_image)
        self.image = self.canvas.create_image(self.x, self.y, image=img, anchor="nw")
        self.canvas.pack()
        self.canvas.update()

