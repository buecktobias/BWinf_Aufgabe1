import tkinter
from PIL import Image, ImageTk
from PIL import *


class Bus:
    def __init__(self, canvas: tkinter.Canvas, x, y, width, height, x_speed, y_speed):
        self._canvas = canvas
        self._x = x
        self._y = y
        self._x_speed = x_speed
        self._y_speed = y_speed
        self._width = width
        self._height = height
        self._canvas_image = None
        pil_image: Image = Image.open("Bus.jpg")
        pil_image = pil_image.resize((30, 30))
        self._image = ImageTk.PhotoImage(pil_image)
        self.show()

    def update(self):
        self._x += self._x_speed
        self._y += self._y_speed
        self._canvas.delete(self._canvas_image)
        self.show()

    def show(self):
        self._canvas_image = self._canvas.create_image(self._x, self._y, image=self._image, anchor="nw")
        self._canvas.pack()
        self._canvas.update()

