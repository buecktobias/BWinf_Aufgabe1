from heapq import *


class PriorityQueue:
    def __init__(self):
        self.dictionary: dict = {}
        self.heap = []

    def push(self, key, value):
        self.dictionary[key] = value
        heappush(self.heap, key)

    def pop(self):
        smallest_element = heappop(self.heap)
        return self.dictionary[smallest_element]
