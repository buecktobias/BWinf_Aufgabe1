import sys
import time
from typing import Dict, Optional, List

from graph_theory.PriorityQueue import PriorityQueue
from graph_theory.Node import Node
from graph_theory.Edge import Edge


class Graph:
    def __init__(self) -> None:
        self.nodes: set = set([])
        self.edges: set = set([])
        self.came_from: Optional[Dict[Node, Node]] = None
        self.distances: Optional[Dict[Node, int]] = None

    def add_edge(self, node1: Node, node2: Node, cost):
        assert node1 in self.nodes and node2 in self.nodes, "Nodes have to be in the Graph!"
        edge: Edge = Edge(node1, node2, cost)
        node1.add_edge(edge)
        node2.add_edge(edge)

    def add_node(self, node: Node):
        self.nodes.add(node)

    def shortest_path(self, from_node: Node, to_node: Node):
        if self.came_from is None:  # from_node make sure djikstra was made for the right start node.
            self.came_from, self.distances = self.djikstra(from_node)
        return get_path_and_cost(self.came_from, self.distances, from_node, to_node)

    def min_node_in_nodes(self, nodes, distances):
        min_node = None
        min_cost = sys.maxsize
        for node in nodes:
            if distances[node] < min_cost:
                min_node = node
                min_cost = distances[node]
        return min_node

    def djikstra(self, from_node: Node):
        seen: set = set([])
        priority_queue: PriorityQueue = PriorityQueue()
        distances: Dict[Node, int] = {}
        for node in self.nodes:
            distances[node] = sys.maxsize
        distances[from_node] = 0
        priority_queue.push(0, from_node)
        came_from: Dict[Node, Node] = {}
        while len(priority_queue.heap) > 0:
            current_node: Node = priority_queue.pop()  # use a heap
            current_node_cost: int = distances[current_node]
            seen.add(current_node)
            for edge in current_node.edges:
                connected_node: Node = edge.get_other_node(current_node)
                if connected_node in seen:
                    continue
                connected_node_cost: int = current_node_cost + edge.cost
                priority_queue.push(connected_node_cost, connected_node)
                if connected_node_cost < distances[connected_node]:
                    distances[connected_node] = connected_node_cost
                    came_from[connected_node] = current_node
        return came_from, distances


def get_path_and_cost(came_from: Dict[Node, Node], distances: Dict[Node, int], from_node: Node, to_node: Node):
    path: List[Node] = [to_node]  # could be a set
    while path[0] is not from_node:
        path.insert(0, came_from[path[0]])
    return path, distances[to_node]


if __name__ == '__main__':
    graph = Graph()
    a = Node(10, 10)
    b = Node(20, 20)
    c = Node(10, 39)
    d = Node(2, 15)
    e = Node(8, 23)
    f = Node(4, 5)
    g = Node(9, 9)
    h = Node(1, 5)
    i = Node(0, 0)
    graph.add_node(a)
    graph.add_node(b)
    graph.add_node(c)
    graph.add_node(d)
    graph.add_node(e)
    graph.add_node(f)
    graph.add_node(g)
    graph.add_node(h)
    graph.add_node(i)
    graph.add_edge(h, i, 3)
    graph.add_edge(i, a, 12)
    graph.add_edge(f, g, 11)
    graph.add_edge(g, d, 3)
    graph.add_edge(a, b, 8)
    graph.add_edge(b, d, 1)
    graph.add_edge(a, d, 5)
    graph.add_edge(a, c, 21)
    graph.add_edge(c, e, 14)
    graph.add_edge(a, e, 3)
    start = time.time_ns()
    print(graph.shortest_path(a, h))
    end = time.time_ns()
    first_shortest_path = end - start

    start2 = time.time_ns()
    print(graph.shortest_path(a, d))
    end2 = time.time_ns()
    second_shortest_path = end2 - start2
    print(f"first {first_shortest_path} second {second_shortest_path}")
