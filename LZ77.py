# ------------------------------------------------------------
#  LZ77 Compression / Decompression Tool for input string
#
#  Simple CLI-based implementation of LZ77 algorithm.
#  - Supports compression and decompression
#  - Customizable sliding window size
#
#  Date: October 2025
# ------------------------------------------------------------

class LZ77:
    def __init__(self, window_size=20):
        """Initialize compressor with a given window size."""
        self.window_size = window_size

    def compress(self, data):
        """
        Compress input text using LZ77.
        Returns a list of (offset, length, next_char) tuples.
        Time Complexity: O(n * w) — n = input length, w = window size.
        Space Complexity: O(n + w)
        """
        compressed = []
        i = 0
        n = len(data)

        while i < n:
            best_length = 0
            best_offset = 0

            # Sliding window range
            start = max(0, i - self.window_size)
            window = data[start:i]
            lookahead = data[i:i + self.window_size]

            # Try to find the longest match in the window
            for length in range(1, len(lookahead) + 1):
                substring = lookahead[:length]
                pos = window.rfind(substring)

                if pos != -1:
                    best_offset = i - (start + pos)
                    best_length = length
                else:
                    break

            # Next character after the match
            next_char = data[i + best_length] if i + best_length < n else ''
            compressed.append((best_offset, best_length, next_char))
            i += best_length + 1

        return compressed

    def decompress(self, compressed_data):
        """
        Rebuild original text from list of (offset, length, next_char).
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        output = []

        for offset, length, next_char in compressed_data:
            if offset == 0 and length == 0:
                # Literal character, no match
                output.append(next_char)
            else:
                # Copy 'length' characters starting 'offset' back
                start = len(output) - offset
                for i in range(length):
                    output.append(output[start + i])
                output.append(next_char)

        return ''.join(output)

    def safe_parse_list(self, raw):
        """
        Parse a manual list of tuples entered by the user safely.
        Example input:
            (0,0,'A'), (0,0,'B'), (2,1,'A')
        Returns:
            [(0,0,'A'), (0,0,'B'), (2,1,'A')]

        Parse user input into a list of tuples safely (no eval).
        Time Complexity: O(m)
        Space Complexity: O(m)
        """
        try:
            raw = raw.strip()
            if raw.startswith("[") and raw.endswith("]"):
                raw = raw[1:-1]

            tuples = []
            chunks = []
            buf = ""
            in_paren = False

            for ch in raw:
                if ch == '(':
                    in_paren = True
                    buf = ""
                buf += ch
                if ch == ')':
                    in_paren = False
                    chunks.append(buf)
                    buf = ""

            for chunk in chunks:
                parts = chunk.strip("() ").split(",")
                if len(parts) == 3:
                    offset = int(parts[0])
                    length = int(parts[1])
                    char = parts[2].strip().strip("'\"")
                    tuples.append((offset, length, char))

            return tuples
        except Exception:
            print("Couldn’t parse compressed data properly.")
            return []

    def menu(self):
        """CLI menu for compressing and decompressing text."""
        print("===== LZ77 Compression Tool =====")
        print("1. Compress text")
        print("2. Decompress data")

        choice = input("Choose (1 or 2): ").strip()
        print()

        if choice == "1":
            # --- Compression ---
            try:
                text = input("Enter text to compress: ").strip()
                if not text:
                    print(" Input text cannot be empty.")
                    return

                w = input("Enter window size: ").strip()
                if not w.isdigit() or int(w) <= 0:
                    print("Invalid window size.")
                    return

                self.window_size = int(w)
                compressed = self.compress(text)

                print("\nCompressed Output:")
                for t in compressed:
                    print(t)
                print("\nCopy this list for decompression later.")

            except Exception as e:
                print("Compression error:", e)

        elif choice == "2":
            # --- Decompression ---
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
                data = self.safe_parse_list(raw)

                if not data:
                    print("Could not parse the input data.")
                    return

                decompressed = self.decompress(data)
                print("\nDecompressed text:\n", decompressed)

            except Exception as e:
                print("Decompression error:", e)

        else:
            print("Invalid choice. Enter 1 or 2.")



if __name__ == "__main__":
    try:
        LZ77().menu()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
