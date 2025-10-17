import heapq
from collections import Counter, namedtuple

class Node(namedtuple("Node", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanTree:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = self._read_file_text()
        self.root = None

    def _read_file_text(self) -> str:
        with open(self.file_path) as file:
            return file.read()
  

    def _calculate_frequencies(self) -> dict:
        return dict(Counter(self.text))

    def build_huffman_tree(self):
        freq = self._calculate_frequencies()

        heap = [Node(char, f, None, None) for char, f in freq.items()]
        heapq.heapify(heap)

        if len(heap) == 1:
            only = heap[0]
            self.root = Node(None, only.freq, only, None)
            return self.root

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(None, left.freq + right.freq, left, right)
            heapq.heappush(heap, merged)

        self.root = heap[0]
        return self.root


if __name__ == "__main__":
    input_path = "input.txt"  
    huffman = HuffmanTree(input_path)

    root = huffman.build_huffman_tree()
    print(root)
