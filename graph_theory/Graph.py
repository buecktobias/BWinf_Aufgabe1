import sys
import time
from typing import Dict, Optional, List, Set

from graph_theory.HeapEntry import HeapEntry
from graph_theory.PriorityQueue import PriorityQueue
from graph_theory.Node import Node
from graph_theory.Edge import Edge
from helper_functions_aufgabe1 import measure_distance
import heapq


class Graph:
    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}
        self._edges: set = set([])
        self._came_from: Optional[Dict[Node, Node]] = None
        self._distances: Optional[Dict[Node, int]] = None

    def add_edge(self, node1_position: List[int], node2_position: List[int], cost):
        node1 = self._nodes[str(node1_position)]
        node2 = self._nodes[str(node2_position)]
        edge: Edge = Edge(node1, node2, cost)
        if edge not in self._edges:
            self._edges.add(edge)
            node1.add_edge(edge)
            node2.add_edge(edge)

    def add_node(self, node_position: List[int]):
        assert len(node_position) == 2, "length of the node_position must be two!"
        if str(node_position) not in self._nodes:
            self._nodes[str(node_position)] = Node(*node_position)

    def shortest_path(self, from_node_position: List[int], to_node_position: List[int]):
        assert str(from_node_position) in self._nodes.keys() and str(to_node_position) in self._nodes.keys(), "Nodes have to be in the graph !"
        from_node: Node = self._nodes[str(from_node_position)]
        to_node: Node = self._nodes[str(to_node_position)]
        if self._came_from is None:
            self._came_from, self._distances = self._djikstra(from_node)
        return _reconstruct_path(self._came_from, from_node, to_node), self._distances[to_node]



    def _djikstra(self, from_node: Node):
        assert from_node in self._nodes.values(), "Node has to be in the Graph!"
        print(f"Djikstra Algorithm on {len(self._nodes)} Nodes and {len(self._edges)} Edges")
        seen: Set[Node] = set([])  # Alle Nodes,die schon gesehen wurden
        nodes_heap = []  # Die Priority Queue implementiert in form eines Heaps
        distances: Dict[Node, int] = {}  # distances speichert die Distanzen zu allen Nodes
        for node in self._nodes.values():
            if node is from_node:
                distances[node] = 0  # die Distanz zur Startnode ist 0
                heap_entry = HeapEntry(0, node)
                heapq.heappush(nodes_heap, heap_entry)  # heap entry wird in die heap gepusht.
            else:
                distances[node] = sys.maxsize  # zu allen anderen nodes ist die Entfernung unendlich, sys.massize ist der größte Integer wert
                heap_entry = HeapEntry(sys.maxsize, node)
                nodes_heap.append(heap_entry)  # heap Eintrag mit unendlich als priorität

        came_from: Dict[Node, Node] = {}  # speichert zu einer Node immer von welcher parent Node man am schnellsten zu dieser Node kommt,so lässt sich der Weg rekostruiren
        while len(nodes_heap) > 0:  # while Schleife bis keine Einträge mehr in der Heap sind.
            current_node: Node = heapq.heappop(nodes_heap).node  # kleinster Eintrag aus der Heap
            current_node_cost: int = distances[current_node]  # Die Kosten der jetzigen Node
            seen.add(current_node)  # die aktuelle Node wird zu seen hinzugefügt.
            for edge in current_node.edges:  # alle Kanten der aktuellen Node werden durchgegangen
                connected_node: Node = edge.get_other_node(current_node)
                if connected_node in seen:  # Wenn der Knotenpunkt bereits durchgegangen wurde wir dieser übersprungnen
                    continue
                connected_node_cost: int = current_node_cost + edge.cost
                if connected_node_cost < distances[connected_node]:
                    distances[connected_node] = connected_node_cost
                    heapq.heappush(nodes_heap, HeapEntry(connected_node_cost, connected_node))  # der neue Wert wird in die Heap gepusht
                    came_from[connected_node] = current_node
        return came_from, distances


def _reconstruct_path(came_from: Dict[Node, Node], from_node: Node, to_node: Node):
    path: List[Node] = [to_node]  # could be a set
    while path[0] is not from_node:
        path.insert(0, came_from[path[0]])
    return path


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
