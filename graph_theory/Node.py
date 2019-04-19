from graph_theory.Edge import Edge


class Node:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.name = f"({self.x}, {self.y})"
        self.edges: set = set([])

    def add_edge(self, edge: Edge):
        self.edges.add(edge)

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    pass
