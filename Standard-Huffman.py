import heapq
from collections import Counter, namedtuple
import json


class Node(namedtuple("Node", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanTree:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = self._read_file_text()
        self.root = None
        self.codes = {}  # store generated codes in a dictionary

    # -------------------------------------------------------------
    #               read file & build tree
    # -------------------------------------------------------------
    def _read_file_text(self) -> str:
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _calculate_frequencies(self) -> dict:
        return dict(Counter(self.text))

    def build_huffman_tree(self):
        freq = self._calculate_frequencies()
        heap = [Node(char, f, None, None) for char, f in freq.items()]
        heapq.heapify(heap)
        if len(heap) == 0:
            self.root = None
            return None

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

    # -------------------------------------------------------------
    #               code generation & compression
    # -------------------------------------------------------------

    def generate_codes(self, node=None, current_code=""):
        """Recursively generate Huffman codes for each character."""
        if node is None:
            node = self.root
        # Base case: empty tree
        if node is None:
            return
        # Base case: leaf node (contains a character)
        if node.char is not None:
            self.codes[node.char] = current_code or "0"  # handle single char case
            return

        # Recursive case : traverse left and right
        if node.left:
            self.generate_codes(node.left, current_code + "0")
        if node.right:
            self.generate_codes(node.right, current_code + "1")

    def encode_data(self) -> str:
        """Convert original text into a string of bits using Huffman codes."""
        return "".join(self.codes[ch] for ch in self.text)

    def pad_bit_string(self, bit_string: str) -> str:
        """Pad the bit string so its length is a multiple of 8 (for bytes)."""
        extra_padding = 8 - len(bit_string) % 8
        if extra_padding == 8:
            extra_padding = 0

        # Add padding info at the beginning
        padded_info = f"{extra_padding:08b}"  # telling the decompressor how many zeros to remove later
        bit_string = padded_info + bit_string + ("0" * extra_padding)
        return bit_string

    def bit_string_to_Actual_bytes(self, bit_string: str) -> bytes:
        """Convert '010101...' string into actual bytes."""
        return bytes(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))

    def write_compressed_file(self, output_path: str):
        """Write compressed file with header (freq table) and binary data."""
        # Build tree and generate codes
        self.build_huffman_tree()
        self.generate_codes()

        # Get frequency table
        freq_table = self._calculate_frequencies()

        # Encode text into bits
        bit_string = self.encode_data()
        padded_bits = self.pad_bit_string(bit_string)
        byte_data = self.bit_string_to_Actual_bytes(padded_bits)

        # Write compressed file
        with open(output_path, "wb") as file:
            # --- Write header: frequency table as JSON---
            header = json.dumps(freq_table).encode("utf-8")
            file.write(len(header).to_bytes(4, "big"))  # first 4 bytes = header size
            file.write(header)
            # --- Write compressed binary data ---
            file.write(byte_data)

        print(f"File compressed successfully: {output_path}")

def display_compressed_data_bits(file_path: str):
    """Show only the bitstream part (skip header)."""
    with open(file_path, "rb") as file:
        header_size = int.from_bytes(file.read(4), "big")
        header = file.read(header_size)  # skip JSON freq table
        byte_data = file.read()  # this is only the compressed bits

        bit_string = ''.join(f'{byte:08b}' for byte in byte_data) # convert bytes to bit string

        # remove padding bits (based on first 8 bits)
        padding_info = int(bit_string[:8], 2)
        actual_bits = bit_string[8:len(bit_string) - padding_info]

        print(f"Actual encoded bit length (msg length): {len(actual_bits)} bits")
        print(f"Padding bits removed: {padding_info}")
        print(f"Displayed first 128 bits: {actual_bits[:128]}")

# -------------------------------------------------------------
#                           main
# -------------------------------------------------------------
if __name__ == "__main__":
    input_path = "Standard-Huffman-Testing.txt"
    output_path = "Compressed.bin"

    huffman = HuffmanTree(input_path)
    huffman.write_compressed_file(output_path)
    print("-------------------------------------")
    # Display generated codes
    print("Generated Huffman Codes:")
    for char, code in huffman.codes.items():
        print(repr(char), ":", code)
    print("-------------------------------------")
    # Display binary content of compressed file
    display_compressed_data_bits(output_path)
