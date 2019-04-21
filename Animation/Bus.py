import tkinter


class Bus:
    def __init__(self, canvas: tkinter.Canvas, x, y, width, height, x_speed, y_speed):
        self.canvas = canvas
        self.image = canvas.create_oval(x, y, x+width, y+height, outline="yellow", fill="yellow")
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.width = width
        self.height = height

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.canvas.delete(self.image)
        self.image = self.canvas.create_oval(round(self.x), round(self.y), round(self.x) + self.width, round(self.y) + self.height, outline="yellow", fill="yellow")
        self.canvas.pack()
        self.canvas.update()
