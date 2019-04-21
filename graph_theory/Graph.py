import sys
import time
from typing import Dict, Optional, List

from graph_theory.HeapEntry import HeapEntry
from graph_theory.PriorityQueue import PriorityQueue
from graph_theory.Node import Node
from graph_theory.Edge import Edge
from helper_functions_aufgabe1 import measure_distance
import heapq

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
        if edge not in self.edges:
            self.edges.add(edge)
            node1.add_edge(edge)
            node2.add_edge(edge)

    def add_node(self, node_position: List[int]):
        assert len(node_position) == 2, "length of the node_position must be two!"
        if str(node_position) not in self.nodes:
            self.nodes[str(node_position)] = Node(*node_position)

    def shortest_path(self, from_node_position: List[int], to_node_position: List[int]):
        assert str(from_node_position) in self.nodes.keys() and str(to_node_position) in self.nodes.keys(), "Nodes have to be in the graph !"
        from_node: Node = self.nodes[str(from_node_position)]
        to_node: Node = self.nodes[str(to_node_position)]
        if self.came_from is None:  # from_node make sure djikstra was made for the right start node.
            self.came_from, self.distances = self.djikstra(from_node)
        return get_path_and_cost(self.came_from, self.distances, from_node, to_node)

    def djikstra(self, from_node: Node):
        print(f"Djikstra Algorithm on {len(self.nodes)} Nodes and {len(self.edges)} Edges")
        seen: set = set([])
        nodes: List = []
        distances: Dict[Node, int] = {}
        for node in self.nodes.values():
            if node is from_node:
                distances[node] = 0
                heap_entry = HeapEntry(0, node)
                heapq.heappush(nodes, heap_entry)
            else:
                distances[node] = sys.maxsize
                heap_entry = HeapEntry(sys.maxsize, node)
                nodes.append(heap_entry)

        came_from: Dict[Node, Node] = {}
        while len(nodes) > 0:
            current_node: Node = heapq.heappop(nodes).node
            current_node_cost: int = distances[current_node]
            seen.add(current_node)
            for edge in current_node.edges:
                connected_node: Node = edge.get_other_node(current_node)
                if connected_node in seen:
                    continue
                connected_node_cost: int = current_node_cost + edge.cost
                if connected_node_cost < distances[connected_node]:
                    distances[connected_node] = connected_node_cost
                    heapq.heappush(nodes, HeapEntry(connected_node_cost, connected_node))
                    came_from[connected_node] = current_node
        return came_from, distances


def get_path_and_cost(came_from: Dict[Node, Node], distances: Dict[Node, int], from_node: Node, to_node: Node):
    path: List[Node] = [to_node]  # could be a set
    while path[0] is not from_node:
        path.insert(0, came_from[path[0]])
    return path, distances[to_node]


if __name__ == '__main__':
    graph = Graph()
    graph.add_node([0, 0])
    graph.add_node([10, 0])
    graph.add_node([10, 10])
    graph.add_node([20, 20])
    graph.add_edge([0, 0], [10, 0], 10)
    graph.add_edge([10, 10], [0, 0], 5)
    graph.add_edge([10, 10], [20, 20], 20)
    print(graph.shortest_path([0, 0], [20, 20]))
    pass
