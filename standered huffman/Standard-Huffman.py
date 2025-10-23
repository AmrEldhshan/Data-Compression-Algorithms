import heapq
from collections import Counter, namedtuple
import json


class Node(namedtuple("Node", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanTree:
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.text = ""
        self.root = None
        self.codes = {}
        if file_path:
            self.text = self._read_file_text()


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



    # -------------------------------------------------------------
    #                   Decompression Section
    # -------------------------------------------------------------
def decompress_file(self, compressed_path: str, output_path: str = "Decompressed.txt"):
    """Decompress a Huffman-compressed file back into its original content."""

    # --- Step 1: Make sure the compressed file exists ---
    if not os.path.exists(compressed_path):
        print(f"The file '{compressed_path}' does not exist. Please check the name and try again.")
        return

    try:
        with open(compressed_path, "rb") as file:
            # Read header size (first 4 bytes)
            header_size = int.from_bytes(file.read(4), "big")

            # Read and decode the frequency table (JSON format)
            header_data = file.read(header_size)
            freq_table = json.loads(header_data.decode("utf-8"))

            # Remaining bytes are the actual compressed data
            compressed_bytes = file.read()

    except Exception as e:
        print(f"Failed to read compressed file '{compressed_path}': {e}")
        return

    # --- Step 2: Rebuild the Huffman Tree using the frequency table ---
    try:
        self.text = "".join(char * freq for char, freq in freq_table.items())
        self.build_huffman_tree()
        self.generate_codes()
    except Exception as e:
        print(f"Error rebuilding Huffman tree: {e}")
        return

    # --- Step 3: Convert byte data back to bit string ---
    try:
        bit_string = ''.join(f'{byte:08b}' for byte in compressed_bytes)
        padding_info = int(bit_string[:8], 2)
        actual_bits = bit_string[8:len(bit_string) - padding_info]
    except Exception as e:
        print(f"Error decoding bit stream: {e}")
        return

    # --- Step 4: Decode bits back into characters ---
    try:
        reverse_codes = {v: k for k, v in self.codes.items()}
        decoded_text = []
        current_bits = ""

        for bit in actual_bits:
            current_bits += bit
            if current_bits in reverse_codes:
                decoded_text.append(reverse_codes[current_bits])
                current_bits = ""

        decoded_output = ''.join(decoded_text)

        # Write the decompressed text to file
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(decoded_output)

        print(f"File decompressed successfully: {output_path}")

    except Exception as e:
        print(f"Error during decompression process: {e}")



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


# -------------------------------------------------------------
#                       Menu System
# -------------------------------------------------------------
import os
import traceback

def main_menu():
    print("\n=== Huffman Compression Menu ===")
    print("1. Compress a file")
    print("2. Decompress a file")
    print("3. Exit")
    print("--------------------------------")

    choice = input("Enter your choice (default = 1): ").strip() or "1"

    if choice == "1":
        input_path = input("Enter input file path (default = Standard-Huffman-Testing.txt): ").strip() or "Standard-Huffman-Testing.txt"
        output_path = input("Enter output compressed file path (default = Compressed.bin): ").strip() or "Compressed.bin"

        # Defensive check: file must exist
        if not os.path.exists(input_path):
            print(f"Error: The file '{input_path}' does not exist.")
            return main_menu()

        try:
            huffman = HuffmanTree(input_path)
            huffman.write_compressed_file(output_path)
            print("-------------------------------------")
            print("Generated Huffman Codes:")
            for char, code in huffman.codes.items():
                print(repr(char), ":", code)
            print("-------------------------------------")
            display_compressed_data_bits(output_path)
        except Exception as e:
            print("Compression failed:")
            print(traceback.format_exc())

    elif choice == "2":
        compressed_path = input("Enter compressed file path (default = Compressed.bin): ").strip() or "Compressed.bin"
        output_path = input("Enter output decompressed file path (default = Decompressed.txt): ").strip() or "Decompressed.txt"

        # Defensive check: compressed file must exist
        if not os.path.exists(compressed_path):
            print(f"Error: The file '{compressed_path}' does not exist.")
            return main_menu()

        try:
            huffman = HuffmanTree()
            huffman.decompress_file(compressed_path, output_path)
        except Exception as e:
            print("Decompression failed:")
            print(traceback.format_exc())

    elif choice == "3":
        print("Exiting program.")
        return

    else:
        print("Invalid choice! Please enter 1, 2, or 3.")

    # Restart menu after operation
    main_menu()

if __name__ == "__main__":
    main_menu()

    # input_path = "Standard-Huffman-Testing.txt"
    # output_path = "Compressed.bin"

    # huffman = HuffmanTree(input_path)
    # huffman.write_compressed_file(output_path)
    # print("-------------------------------------")
    # # Display generated codes
    # print("Generated Huffman Codes:")
    # for char, code in huffman.codes.items():
    #     print(repr(char), ":", code)
    # print("-------------------------------------")
    # # Display binary content of compressed file
    # display_compressed_data_bits(output_path)
