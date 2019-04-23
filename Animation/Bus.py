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
        self.canvas_image = None
        pil_image: Image = Image.open("Bus.jpg")
        pil_image = pil_image.resize((30, 30))
        self.image = ImageTk.PhotoImage(pil_image)
        self.show()

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.canvas.delete(self.canvas_image)
        self.show()

    def show(self):
        self.canvas_image = self.canvas.create_image(self.x, self.y, image=self.image, anchor="nw")
        self.canvas.pack()
        self.canvas.update()

