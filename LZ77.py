# ------------------------------------------------------------
#  LZ77 Compression / Decompression Tool
#
#  A simple and readable Python implementation of the LZ77 algorithm.#
#  Date: October 2025
# ------------------------------------------------------------

class LZ77:
    def __init__(self, window_size=20):
        """Set up the compressor with a specific sliding window size."""
        self.window_size = window_size

    # ------------------------------------------------------------


    
    def compress(self, data):
        """
        Compress the given text using a basic LZ77 algorithm.
        It searches the previous 'window_size' characters for the
        longest possible match, then encodes it as (offset, length, next_char).

        Time Complexity: O(n * w)
        Space Complexity: O(n + w)
        """
        compressed = []
        i = 0
        n = len(data)

        while i < n:
            match_len = 0
            match_dist = 0

            # Define the sliding window
            start = max(0, i - self.window_size)
            window = data[start:i]
            lookahead = data[i:i + self.window_size]

            # Try to find the longest substring match
            for length in range(1, len(lookahead) + 1):
                substring = lookahead[:length]
                pos = window.rfind(substring)
                if pos != -1:
                    match_dist = i - (start + pos)
                    match_len = length
                else:
                    break

            next_char = data[i + match_len] if i + match_len < n else ''
            compressed.append((match_dist, match_len, next_char))
            i += match_len + 1

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
