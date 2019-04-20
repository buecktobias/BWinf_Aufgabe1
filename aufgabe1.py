import sys
from typing import List
from time import time_ns
from graph_theory.Graph import Graph
import tkinter as tk
from math import tan
from helper_functions_aufgabe1 import *
from graph_theory.Node import Node
from itertools import combinations


def measure_time(t_distance, speed_kmh):
    speed_ms = speed_kmh / 3.6
    time = t_distance / speed_ms
    return time


def time_needed_minus_bus_time(t_distance, to_cords):
    time_to_road = measure_time(t_distance, 15)
    bus_time = measure_time(to_cords[1], 30)
    return time_to_road - bus_time


def add(ls: list, element):
    if element not in ls:
        ls.append(element)


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


if __name__ == '__main__':
    start_time = time_ns()

    start_point, test_polygons = get_polygons_from_file("input/lisarennt3.txt")
    shapely_polygons: List[LinearRing] = [LinearRing(poly) for poly in test_polygons]
    root: tk.Tk = tk.Tk()
    canvas_width: int = 800
    canvas_height: int = 800
    canvas: tk.Canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    create_polygons(canvas, test_polygons)
    canvas.create_oval(start_point[0] - 10, start_point[1] - 10, start_point[0] + 10, start_point[1] + 10)
    canvas.pack()
    canvas.update()
    graph: Graph = Graph()
    open_nodes: list = [start_point]

    already_checked: set = set([])
    graph.add_node(start_point)

    street_points = [[0, y] for y in range(0, canvas_height, 10)]
    all_important_points = street_points

    all_polygon_edges: list = [start_point]
    for polygon in test_polygons:
        for point in polygon:
            all_polygon_edges.append(point)

    optimal_targets_list: list = []
    while len(open_nodes) > 0:
        current_node = open_nodes.pop()
        all_polygon_edges.remove(current_node)
        graph.add_node(current_node)
        for point in all_polygon_edges:
            if is_line_segment_free(current_node, point, shapely_polygons):
                graph.add_node(point)
                graph.add_edge(current_node, point, measure_distance(current_node, point))
                add(open_nodes, point)
        y__ = current_node[1] + tan(0.523599) * current_node[0]  # 0.523599 is about 30 degrees in radians
        optimal_target: list = [0, y__]
        if is_line_segment_free(current_node, optimal_target, shapely_polygons):
            graph.add_node(optimal_target)
            graph.add_edge(current_node, optimal_target, measure_distance(current_node, optimal_target))
            add(optimal_targets_list, optimal_target)

    smallest_time = sys.maxsize
    for street_point in optimal_targets_list:
        path, distance = graph.shortest_path(start_point, street_point)
        time = time_needed_minus_bus_time(distance, street_point)
        if time < smallest_time:
            smallest_time = time
            best_path = path
    print(best_path)
    for i in range(1, len(best_path)):
        canvas.create_line(best_path[i-1].x, best_path[i-1].y, best_path[i].x, best_path[i].y)
    canvas.pack()
    canvas.update()
    end_time = time_ns()
    measured_time = end_time - start_time
    print(f"It needed " + str(measured_time) + "nanoseconds ," + str(measured_time / 1000000) + " milliseconds ," + str(measured_time / 1000000000) + " seconds")
    canvas.mainloop()
