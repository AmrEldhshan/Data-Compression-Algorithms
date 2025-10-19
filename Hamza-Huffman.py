import heapq
import os
import json

# ------------------------------------------------------------
# Huffman Node
# ------------------------------------------------------------
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Comparison for priority queue
    def __lt__(self, other):
        return self.freq < other.freq


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def build_frequency_table(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def build_huffman_tree(freq_table):
    heap = [Node(ch, freq) for ch, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2

        heapq.heappush(heap, merged)

    return heap[0] if heap else None


def generate_codes(node, current_code="", codes={}):
    if node is None:
        return

    if node.char is not None:  # leaf node
        codes[node.char] = current_code
        return

    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)
    return codes


# ------------------------------------------------------------
# Compression
# ------------------------------------------------------------
def compress(input_file, output_file, codes_file):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    if not text:
        print("Input file is empty.")
        return

    freq_table = build_frequency_table(text)
    tree = build_huffman_tree(freq_table)
    codes = generate_codes(tree)

    print("Generated Huffman Codes:", codes)

    # Encode text
    encoded_text = "".join(codes[ch] for ch in text)

    # Pad encoded text to make its length multiple of 8
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text += "0" * extra_padding

    # Add info about padding in the first byte
    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text

    # Convert to bytes
    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        b.append(int(byte, 2))

    # Write binary file
    with open(output_file, "wb") as out:
        out.write(bytes(b))

    # Save codes for decompression
    with open(codes_file, "w", encoding="utf-8") as cfile:
        json.dump(codes, cfile)

    print(f"Compression done! Saved to {output_file}")


# ------------------------------------------------------------
# Decompression
# ------------------------------------------------------------
def decompress(input_file, output_file, codes_file):
    with open(codes_file, "r", encoding="utf-8") as cfile:
        codes = json.load(cfile)

    # Reverse codes: bits → character
    reverse_codes = {v: k for k, v in codes.items()}

    with open(input_file, "rb") as f:
        bit_string = ""
        byte = f.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, "0")
            bit_string += bits
            byte = f.read(1)

    # Remove padding
    padding_info = bit_string[:8]
    extra_padding = int(padding_info, 2)
    bit_string = bit_string[8:]  # actual data
    encoded_text = bit_string[:-extra_padding] if extra_padding > 0 else bit_string

    # Decode text
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""

    with open(output_file, "w", encoding="utf-8") as out:
        out.write(decoded_text)

    print(f"Decompression done! Saved to {output_file}")


# ------------------------------------------------------------
# Main Menu
# ------------------------------------------------------------
if __name__ == "__main__":
    print("Huffman Coding Tool")
    print("1. Compress")
    print("2. Decompress")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        compress("Standard-Huffman-Testing.txt", "compressed.bin", "codes.json")
    elif choice == "2":
        decompress("compressed.bin", "decompressed.txt", "codes.json")
    else:
        print("Invalid choice.")