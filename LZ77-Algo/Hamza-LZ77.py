"""---------------------------- Menu ----------------------------"""
def menue(message, options):
    print(message)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True: # loop until valid choice
        choice = input("Enter your choice (number): ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return choice
        else:
            print("Invalid choice. Please try again.")


""""----------------------------  LZ77 Compression Algorithm ----------------------------"""
def matchesBehind(text, currentIndex, searchWindow):
  searchStart = max(0, currentIndex - searchWindow)
  searchText = text[searchStart:currentIndex]
  match = (0, 0, text[currentIndex]) # default no match found
  # find the longest match 
  for j in range(len(searchText)):
    length = 0
    while (length < len(text) - currentIndex and
           searchText[j:j+length + 1] == text[currentIndex:currentIndex+length + 1]):
      length += 1
    if length > match[1]: # if Found a longer match
      pos = len(searchText) - j
      nextChar = text[currentIndex + length] if (currentIndex + length) < len(text) else ''
      match = (pos, length, nextChar)
  return match

def compressLZ77(text, searchWindow=20):
  if len(text) == 0:
    return []
  currentIndex = 1
  dataCompressed = [(0, 0, text[0])] # default (no match found)  
  while currentIndex < len(text):
    match = matchesBehind(text, currentIndex, searchWindow)
    dataCompressed.append(match)
    currentIndex += match[1] + 1
  return dataCompressed


""""----------------------------  LZ77 Decompression Algorithm ----------------------------"""
def decompressLZ77(compressedData):
  decompressedData = ""
  for pos, length, nextChar in compressedData:
    if pos == 0 and length == 0:
      decompressedData += nextChar
    else:
      start = len(decompressedData) - pos
      decompressedData += decompressedData[start:start+length] + nextChar
  return decompressedData

""""---------------------------- Example usage ----------------------------"""
def main():
    test_cases = [
        ("AAAAAA", 5),
        ("ABABABAB", 4),
        ("A B A B A B", 6),
        ("HELLO WORLD", 5),
        ("ABCABCABCABC", 6),
        ("123123123123", 6),
        ("THIS IS A TEST", 7),
        ("!@#$!@#$!@#", 5),
        ("abcdefghijklmnopqrstuvwxyz", 10),
        ("111222333444", 6),
        ("ABCDABCDABCDABCD", 8),
        ("THE QUICK BROWN FOX", 10),
        ("ZZZZZZZZZZ", 5),
        ("Lorem ipsum dolor sit amet", 10),
        ("Python3.10.5 is cool!", 8),
        ("AAAAAAAAAABBBBBBBBBB", 10),
        ("DATA123DATA123", 6),
        ("A1B2C3D4E5F6", 5),
        ("No repeats here!", 10),
        ("Edge cases: 0123456789", 12),
    ]
    choice = menue("Choose an option:", ["Compress text", "Decompress text", "Run test cases"])
    if choice.startswith("1"):
        text = input("Please enter the text you want to compress: ")
        compressed = compressLZ77(text)
        print("\nCompressed:", compressed)
    elif choice.startswith("2"):
        compressed_input = input("Please enter the compressed data (as a list of tuples): ")
        try:
            compressed_data = eval(compressed_input)
            if all(isinstance(t, tuple) and len(t) == 3 for t in compressed_data):
                decompressed = decompressLZ77(compressed_data)
                print("Decompressed:", decompressed)
            else:
                print("Invalid format. Please enter a list of tuples like [(0, 0, 'A'), (1, 2, 'B')].")
        except:
            print("Invalid input. Please ensure it's a valid Python list of tuples.")
    else:
        for text, window in test_cases:
            compressed = compressLZ77(text, window)
            decompressed = decompressLZ77(compressed)
            print(f"Test passed for input: {text} | Compressed: {compressed} | Decompressed: {decompressed}")

main()