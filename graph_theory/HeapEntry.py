from graph_theory import Node


class HeapEntry:
    def __init__(self, priority: int, node: Node):
        self.priority = priority
        self.node = node

    def __lt__(self, other):
        return self.priority < other.priority
