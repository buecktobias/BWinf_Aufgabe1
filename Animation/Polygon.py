import tkinter
from shapely.geometry.polygon import Polygon as ShapelyPolygon


class Polygon:
    def __init__(self, edges: list):
        self._edges = edges
        self.shapely_polygon: ShapelyPolygon = ShapelyPolygon(edges)

    def show(self, canvas: tkinter.Canvas):
        canvas.create_polygon(self._edges)
        canvas.pack()
        canvas.update()
