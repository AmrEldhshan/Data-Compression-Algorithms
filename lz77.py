from typing import List, Tuple


Tag = Tuple[int, int, str]

def compress(text: str , window_size: int =10 , lookahead_size: int = 10 ) -> List[Tag]:
    i=0 
    text_lenght=len(text) 
    tags: List[Tag] = []

    while i<text_lenght :
        start_window  = max(0,i-window_size)
        end_lookahead  = min(text_lenght,i+lookahead_size)

        best_offset = 0
        best_length = 0

        for j in range(start_window , i):
            length = 0 

            while (i + length < text_lenght) and (text[j + length] == text[i + length]):
                length += 1
                if length >= lookahead_size:
                    break
                if j + length >= i:
                    break

            length = 0
            while (i + length < text_lenght) and (text[j + length] == text[i + length]):
                length += 1
                if length >= lookahead_size:
                    break

            if length > best_length:
                best_length = length
                best_offset = i - j  

        if best_length == 0:
            tags.append((0, 0, text[i]))
            i += 1
        else:
            next_char = text[i + best_length] if (i + best_length) < text_lenght else ''
            tags.append((best_offset, best_length, next_char))
            i += best_length + (1 if next_char else 0)
        
    return tags

def decompress(tags: List[Tag]) -> str:
    original_string: List[str] = []

    for offset, length, next_char in tags:

        if offset == 0 and length == 0:
            original_string.append(next_char)
        else:
            start = len(original_string) - offset
            for i in range(length):
                original_string.append(original_string[start + i])
            if next_char:
                original_string.append(next_char)

    return ''.join(original_string)



