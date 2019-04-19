import math
from shapely.geometry.polygon import LinearRing, LineString
from shapely.geometry import MultiLineString

def measure_distance(cords1, cords2):
    x_distance = abs(cords1[0] - cords2[0])
    y_distance = abs(cords1[1] - cords2[1])
    return math.sqrt(x_distance*x_distance + y_distance*y_distance)


def intersects_with_polygons(s_poly: LinearRing, s_line: LineString):
    intersection = s_poly.intersection(s_line)
    #print(intersection)
    if intersection.geom_type == "MultiPoint":
        return True
    return False

def is_line_segment_free(from_cords, to_cords, shapely_polygons, canvas_width, canvas_height):
    from_cords = [round(x) for x in from_cords]
    to_cords = [round(x) for x in to_cords]
    s_line = LineString([from_cords, to_cords])
    for polygon in shapely_polygons:
        if intersects_with_polygons(polygon, s_line):
            return False
    return True
