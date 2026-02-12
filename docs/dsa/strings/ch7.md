# Compression & Encoding Techniques

These are used in both practical applications (like ZIP files, web protocols) and algorithm problems (e.g. Run-Length Encoding, Huffman Coding).

## Run-Length Encoding

- Replace repeating characters with a count.

````python
Input: "aaabbc"
Output: "a3b2c1"
````

````python
def rle(s):
    res = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        res.append(s[i] + str(j - i))
        i = j
    return ''.join(res)
````

Using Python in-built function

```python
from itertools import groupby

def rle_encode(iterable):
    return [(key, sum(1 for _ in group))
            for key, group in groupby(iterable)]
            
# "AAAABBBCCDAA"
# A4 B3 C2 D1 A2

from itertools import chain, repeat
def rle_decode(pairs):
    return ''.join(chain.from_iterable(repeat(k, n) for k, n in pairs))

```
## Huffman Coding

**Idea:**

- Variable-length encoding based on character frequency (used in compression algorithms like ZIP, JPEG).

**Steps:**

1. Count frequency of each character.
2. Build a **min-heap** to construct a **binary tree**.
3. Traverse the tree to assign binary codes.

**Properties:**

- Prefix-free codes (no code is prefix of another).
- Greedy algorithm.

Useful in:

- Data compression
- Encoding tasks

## Trie-Based Compression

- Tries (prefix trees) efficiently store sets of strings with common prefixes.
- Space-efficient for autocomplete, spell-checkers, or dictionary encoding.

## Burrows-Wheeler Transform (BWT)

Used in compression (e.g. bzip2) and bioinformatics.

- Rearranges the string into a form more amenable to compression.
- Requires suffix array or rotations.

## Dictionary Encoding (LZW)

- Replaces repeating substrings with dictionary indices.
- Used in image compression (GIF) and data formats.