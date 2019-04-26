import tkinter as tk
import random
import math


def generate_polygons(numberOfPolygons, width, height, size, maxEcken=4):
    polygons = []
    for i in range(numberOfPolygons):
        ecken = random.randint(3, maxEcken)
        x = random.randint(0+size, width-size)
        y = random.randint(0+size, height-size)
        xn = x
        yn = y
        polygon = []
        for ii in range(ecken):
            if ii == 0:
                xn = x + random.randint(math.ceil(size/2), size)
                yn = y
            if ii == 1:
                yn = y + random.randint(math.ceil(size / 2), size)
                xn = x
            if ii == 2:
                xn = x - random.randint(math.ceil(size/2), size)
                yn = y
            if ii == 3:
                yn = y - random.randint(math.ceil(size / 2), size)
                xn = x
            ecke = [xn, yn]
            polygon.append(ecke)
        polygons.append(polygon)
    return polygons
