from graph_theory.Graph import Graph
import tkinter as tk
from helper_functions_aufgabe1 import *
from graph_theory.Node import Node
from itertools import combinations


def get_polygons_from_file(file_name: str):
    file = open(file_name)
    lines = file.readlines()
    start_point = [int(x) for x in lines[-1].split(" ")]
    print("start Point " + str(start_point))
    polygons = []
    for line in lines[1:-1]:
        polygon = [int(x) for x in line.split(" ")[1:]]
        polygon = [[polygon[i - 1], polygon[i]] for i in range(1, len(polygon), 2)]
        polygons.append(polygon)
        # print("polygon " + str(polygon))
    return start_point, polygons


def create_polygons(canvas: tk.Canvas, polygons: list):
    for polygon in polygons:
        canvas.create_polygon(polygon, fill="gray")
        canvas.pack()
        canvas.update()


start_point, test_polygons = get_polygons_from_file("input/lisarennt3.txt")
root: tk.Tk = tk.Tk()
canvas_width: int = 800
canvas_height: int = 800
canvas: tk.Canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
create_polygons(canvas, test_polygons)
canvas.create_oval(start_point[0] - 10, start_point[1] - 10, start_point[0] + 10, start_point[1] + 10)
canvas.pack()
graph: Graph = Graph()
open_nodes: list = [start_point]
start_node: Node = Node(start_point[0], start_point[1])
graph.add_node(start_node)

street_points = [[0, y] for y in range(0, canvas_height, 10)]
all_important_points = street_points
for polygon in test_polygons:
    all_important_points.extend([point for point in polygon])

all_important_lines = combinations(all_important_points, 2)
while len(open_nodes) > 0:
    current_node = open_nodes.pop()




