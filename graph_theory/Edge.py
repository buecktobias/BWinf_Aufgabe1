from graph_theory import Node


class Edge:
    def __init__(self, node1: Node, node2: Node, cost: float):
        self.node1: Node = node1
        self.node2: Node = node2
        self.cost: float = cost

    def get_other_node(self, node):  # used to get the node, a node is connected to through this edge
        if node == self.node1:
            return self.node2
        else:
            return self.node1

    @property
    def cost(self):
        return self._cost

    @cost.getter
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, new_cost: float):
        assert new_cost >= 0, "Cost of Edge must be greater than 0"
        self._cost = new_cost
