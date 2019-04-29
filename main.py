import datetime
import sys
import tkinter
from typing import List
from Animation.Polygon import Polygon
from graph_theory.Graph import Graph
import tkinter as tk
from math import tan
from helper_functions_aufgabe1 import *


def measure_time(t_distance, speed_kmh):
    speed_ms = speed_kmh / 3.6   # kmh to ms
    time = t_distance / speed_ms
    return time


def time_needed_minus_bus_time(t_distance, to_cords):
    time_to_road = measure_time(t_distance, LISA_SPEED)
    bus_time = measure_time(to_cords[1], BUS_SPEED)
    return time_to_road - bus_time


def add(ls: list, element):
    if element not in ls:
        ls.append(element)


def get_polygons_from_file(file_name: str):
    file = open(file_name)
    lines = file.readlines()
    start_point = [int(x) for x in lines[-1].split(" ")]
    #print("start Point " + str(start_point))
    polygons = []
    for line in lines[1:-1]:
        polygon = [int(x) for x in line.split(" ")[1:]]
        polygon = [[polygon[i - 1], polygon[i]] for i in range(1, len(polygon), 2)]
        polygons.append(polygon)
        # print("polygon " + str(polygon))
    return start_point, polygons


def create_polygons(canvas: tkinter.Canvas, polygons: List[Polygon]):
    for polygon in polygons:
        polygon.show(canvas)


def calculate_lisas_start_time(time_lisa_meets_bus, best_distance):
    time_lisa_needs = measure_time(best_distance, LISA_SPEED)
    time_difference_lisa_and_bus = datetime.timedelta(seconds=time_lisa_needs)  # day and year does not matter
    time_lisa_needs_to_start = time_lisa_meets_bus - time_difference_lisa_and_bus
    return time_lisa_needs_to_start


def calculate_time_lisa_meets_bus(position_lisa_meets_bus):
    time_bus_needs_to_lisa = measure_time(position_lisa_meets_bus[1], 30)
    time_difference_bus_and_bus_meets_lisa = datetime.timedelta(seconds=time_bus_needs_to_lisa)
    bus_driving_time = datetime.datetime(year=2019, month=4, day=15, hour=7, minute=30, second=0)  # day and year does not matter
    time_bus_meets_lisa = bus_driving_time + time_difference_bus_and_bus_meets_lisa
    return time_bus_meets_lisa


def find_polygon_with_this_point(polygons: List[Polygon], point: List[int]):
    for polygon in polygons:
        for edge in polygon.edges:
            if list(point) == list(edge):
                return polygon
    raise ValueError("point is not in polygon edges" + str(point))


def main(filename, visualize=True):
    canvas_width: int = 1000
    canvas_height: int = 800
    start_point, test_polygons = get_polygons_from_file(filename)
    polygons: List[Polygon] = [Polygon(poly, "P" + str(counter+1)) for counter, poly in enumerate(test_polygons)]  # erstellt Polygone mit den Ids "P1", "P2" ...
    shapely_polygons = [polygon.shapely_polygon for polygon in polygons]

    if visualize:
        root: tk.Tk = tk.Tk()
        canvas: tk.Canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        create_polygons(canvas, polygons)
        canvas.create_oval(start_point[0] - 10, start_point[1] - 10, start_point[0] + 10, start_point[1] + 10, fill="yellow")
    graph: Graph = Graph()  # leerer Graph wird erstellt
    open_nodes: list = [start_point]
    all_polygon_edges: list = [start_point]  # alle Polygon Ecken und der Startpunkt
    for polygon in test_polygons:
        for point in polygon:
            all_polygon_edges.append(point)

    optimal_targets_list: list = []
    while len(open_nodes) > 0:
        current_node = open_nodes.pop()
        graph.add_node(current_node)

        # street point
        y__ = current_node[1] + tan(0.5235988) * current_node[0]  # 0.523599 is about 30 degrees in radians
        optimal_target: list = [0, y__]
        if is_line_segment_free(current_node, optimal_target, shapely_polygons):
            graph.add_node(optimal_target)
            graph.add_edge(current_node, optimal_target, measure_distance(current_node, optimal_target))
            add(optimal_targets_list, optimal_target)  # wird nicht hinzugefügt wenn es schon in der Liste ist

        # polygon edges
        else:
            all_polygon_edges.remove(current_node)
            for point in all_polygon_edges:
                if is_line_segment_free(current_node, point, shapely_polygons):
                    graph.add_node(point)
                    graph.add_edge(current_node, point, measure_distance(current_node, point))
                    add(open_nodes, point)

    smallest_time = sys.maxsize  # unendlich
    best_distance = sys.maxsize
    best_path = []
    for street_point in optimal_targets_list:  # alle Straßenpunkte werden durchgegangen
        path, distance = graph.shortest_path(start_point, street_point)
        time = time_needed_minus_bus_time(distance, street_point)
        if time < smallest_time:
            smallest_time = time
            best_path = path
            best_distance = distance

    for i in range(1, len(best_path)):  # Der beste Weg wird eingezeichnet
        canvas.create_line(best_path[i-1].x, best_path[i-1].y, best_path[i].x, best_path[i].y)

    polygons_lisa_goes_to = ["L"]  # Lisa startet immer bei Lisa
    for node in best_path[1:-1]:  # first one is Lisas start point
        polygons_lisa_goes_to.append(find_polygon_with_this_point(polygons, [node.x, node.y]).name)

    position_lisa_meets_bus = [best_path[-1].x, best_path[-1].y]
    time_bus_meets_lisa = calculate_time_lisa_meets_bus(position_lisa_meets_bus)
    str_time_bus_meets_lisa = f"{ time_bus_meets_lisa.hour}:{ time_bus_meets_lisa.minute}:{ time_bus_meets_lisa.second}"
    lisas_latest_start_time = calculate_lisas_start_time(time_bus_meets_lisa, best_distance)
    str_lisas_start_time: str = f"{lisas_latest_start_time.hour}:{lisas_latest_start_time.minute}:{lisas_latest_start_time.second}"

    time_lisa_needs = measure_time(best_distance, LISA_SPEED)
    smallest_time_converted = datetime.timedelta(seconds=round(time_lisa_needs))
    str_smallest_time = str(smallest_time_converted)
    if visualize:
        canvas.mainloop()
    polygons_lisa_goes_to.append("Straße")
    str_best_path_polygons = list(zip(best_path, polygons_lisa_goes_to))
    return str_lisas_start_time, str_time_bus_meets_lisa, str_smallest_time, round(best_distance), str_best_path_polygons


if __name__ == '__main__':
    LISA_SPEED = 15
    BUS_SPEED = 30
    print(main("input/lisarennt1.txt"))
