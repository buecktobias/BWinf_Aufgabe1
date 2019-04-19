import sys
import time
from typing import Dict, Optional, List

from graph_theory.PriorityQueue import PriorityQueue
from graph_theory.Node import Node
from graph_theory.Edge import Edge


class Graph:
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.edges: set = set([])
        self.came_from: Optional[Dict[Node, Node]] = None
        self.distances: Optional[Dict[Node, int]] = None

    def add_edge(self, node1_position: List[int], node2_position: List[int], cost):
        node1 = self.nodes[str(node1_position)]
        node2 = self.nodes[str(node2_position)]
        edge: Edge = Edge(node1, node2, cost)
        node1.add_edge(edge)
        node2.add_edge(edge)

    def add_node(self, node_position: List[int]):
        self.nodes[str(node_position)] = Node(*node_position)

    def shortest_path(self, from_node_position: List[int], to_node_position: List[int]):
        from_node: Node = self.nodes[str(from_node_position)]
        to_node: Node = self.nodes[str(to_node_position)]
        if self.came_from is None:  # from_node make sure djikstra was made for the right start node.
            self.came_from, self.distances = self.djikstra(from_node)
        return get_path_and_cost(self.came_from, self.distances, from_node, to_node)

    def djikstra(self, from_node: Node):
        seen: set = set([])
        priority_queue: PriorityQueue = PriorityQueue()
        distances: Dict[Node, int] = {}
        for node in self.nodes.values():
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
    graph.add_node([10, 10])
    graph.add_node([20, 20])
    graph.add_node([30, 30])

    graph.add_edge([10, 10], [20, 20], 3)
    graph.add_edge([30, 30], [20, 20], 5)

    start = time.time_ns()
    print(graph.shortest_path([10, 10], [20, 20]))
    end = time.time_ns()
    first_shortest_path = end - start
