# ------------------------------------------------------------
#  LZ77 Compression / Decompression Tool
#
#  A simple and readable Python implementation of the LZ77 algorithm.#
#  Date: 10 October 2025 
#  Version 2 
# ------------------------------------------------------------

class LZ77:
    def __init__(self, window_size=20):
        """Set up the compressor with a specific sliding window size."""
        self.window_size = window_size

    # ------------------------------------------------------------



    def compress(self, data):
        """
        Exact equivalent of your first LZ77 implementation,
        rewritten inside the class structure.
        """
        compressed = []
        i = 0
        text_length = len(data)

        while i < text_length:
            start_window = max(0, i - self.window_size)
            end_lookahead = min(text_length, i + self.window_size)

            best_offset = 0
            best_length = 0

            # Check all possible starting points in the window
            for j in range(start_window, i):
                length = 0

                # First matching loop
                while (i + length < text_length) and (data[j + length] == data[i + length]):
                    length += 1
                    if length >= self.window_size:
                        break
                    if j + length >= i:
                        break

                # Reset and check again (this double-check matters!)
                length = 0
                while (i + length < text_length) and (data[j + length] == data[i + length]):
                    length += 1
                    if length >= self.window_size:
                        break

                # Update if better match
                if length > best_length:
                    best_length = length
                    best_offset = i - j

            # Emit token
            if best_length == 0:
                compressed.append((0, 0, data[i]))
                i += 1
            else:
                next_char = data[i + best_length] if (i + best_length) < text_length else ''
                compressed.append((best_offset, best_length, next_char))
                i += best_length + (1 if next_char else 0)

        return compressed
    # ------------------------------------------------------------
    def decompress(self, compressed_data):
        """
        Reconstruct the original text from the compressed tuples.

        Each tuple is (offset, length, next_char), where 'offset' and 'length'
        define how many characters to copy from previously decompressed text.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        output = []

        for offset, length, next_char in compressed_data:
            if offset == 0 and length == 0:
                # Literal character, nothing to copy
                output.append(next_char)
            else:
                # Copy substring from previously decompressed text
                start = len(output) - offset
                for j in range(length):
                    output.append(output[start + j])
                output.append(next_char)

        return ''.join(output)







    # ------------------------------------------------------------
    def safe_parse_list(self, raw):
        """
        Parse user input like:
            (0,0,'A'), (0,0,'B'), (2,1,'A')
        into:
            [(0,0,'A'), (0,0,'B'), (2,1,'A')]

        Does not use eval(), so it’s safe to take direct input.

        Time Complexity: O(m)
        Space Complexity: O(m)
        """
        try:
            raw = raw.strip()
            if raw.startswith("[") and raw.endswith("]"):
                raw = raw[1:-1]

            tuples, chunk, inside = [], "", False

            for ch in raw:
                if ch == '(':
                    inside = True
                    chunk = ""
                chunk += ch
                if ch == ')':
                    inside = False
                    tuples.append(chunk)
                    chunk = ""

            result = []
            for t in tuples:
                parts = t.strip("() ").split(",")
                if len(parts) == 3:
                    offset = int(parts[0])
                    length = int(parts[1])
                    char = parts[2].strip().strip("'\"")
                    result.append((offset, length, char))
            return result
        except Exception:
            print("Couldn’t parse compressed data correctly.")
            return []







    # ------------------------------------------------------------
    def menu(self):
        """
        Command-line interface.
        Lets you pick between compression and decompression modes.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        print("===== LZ77 Compression Tool =====")
        print("1. Compress text")
        print("2. Decompress data")
        print()

        choice = input("Choose (1 or 2): ").strip()
        print()

        if choice == "1":
            # ---------------- Compression ----------------
            try:
                text = input("Enter text to compress: ").strip()
                if not text:
                    print("Input text cannot be empty.")
                    return

                w = input("Enter window size: ").strip()
                if not w.isdigit() or int(w) <= 0:
                    print("Invalid window size.")
                    return

                self.window_size = int(w)
                compressed = self.compress(text)

                print("\nCompressed output:")
                for t in compressed:
                    print(t)
                print("\nCopy this list for decompression later.")

            except Exception as e:
                print("Compression failed:", e)

        elif choice == "2":
            # ---------------- Decompression ----------------
            try:
                print("Enter compressed data as tuples:")
                print("Example: (0,0,'A'), (0,0,'B'), (2,1,'A'), (3,2,'B')\n")
                raw = input("Compressed data: ").strip()

                if not raw:
                    print("You must enter compressed data.")
                    return

                w = input("Enter window size used during compression: ").strip()
                if not w.isdigit() or int(w) <= 0:
                    print("Invalid window size.")
                    return

                self.window_size = int(w)
                parsed = self.safe_parse_list(raw)

                if not parsed:
                    print("Could not parse the input data.")
                    return

                decompressed = self.decompress(parsed)
                print("\nDecompressed text:\n", decompressed)

            except Exception as e:
                print("Decompression failed:", e)

        else:
            print("Invalid choice. Please enter 1 or 2.")

# ---------------- Run program ----------------
if __name__ == "__main__":
    try:
        LZ77().menu()
    except KeyboardInterrupt:
        print("\nStopped by user.")
