# Basic String Processing

### Application of String Processing

- Information Processing
- Genomics
- Communication Systems
- Programming Systems

**Rules of the Game**

For clarity there are several assumptions and definitions that we will make use of ahead.

- *Characters* : A `String` is a sequence of characters. Characters are of type `char`.
- *Immutability* : String objects are immutable. Their values don't change during assignment, or when passed as arguments and return values.
- *Indexing* : Operation to extract a specified character from a string.
- *Length* : Size of the string
- *Substring* : extract a specified substring operation. We expect a constant time implementation of this.
- *Concatenation* : Creating a new string by appending one string to another.
- *Character Arrays* : We can alternately use an array of character as direct abstraction for string.

Main point to focus here is understanding the efficiency of each operation.

Not all languages provide same implementation of String for e.g. in C it may take linear time to determine the length of String.

## Basic Problem Categorization in String Processing

* Searching and Matching
    * Pattern Matching
    * Exact Match
    * Approximate Match
* Transformation
    * Reversal
    * Substitution
* Parsing and Tokenization
    * Splitting
    * Parsing
* Dynamic String Construction
    * Concatenation
    * Building Substrings
* Structural Analysis

## Python Strings

| Feature                  | Python                               | Notes                                              |
| ------------------------ | ------------------------------------ | -------------------------------------------------- |
| **String Mutability**    | Immutable (must create new string)   | Use `list` + `''.join()` for in-place-style edits. |
| **Indexing**             | 0-based; supports negative indexing  | `s[-1]` is the last character.                     |
| **Length**               | O(1) via `len(s)`                    | Cached at object creation.                         |
| **Substring Extraction** | O(k) slicing `s[start:end]`          | k = slice length; very ergonomic.                  |
| **Concatenation**        | O(n) due to creation of new strings  | Prefer `''.join(parts)` inside loops.              |
| **Character Arrays**     | Use `list(s)` for mutable char array | Convert back with `''.join(chars)`.                |

## Common String Operations

### Checking Palindrome

```python
s == s[::-1]          # whole string
s[l:r+1] == s[l:r+1][::-1]  # substring s[l..r]
```

### Converting Case

```python
s.upper()   # "hello" → "HELLO"
s.lower()   # "HELLO" → "hello"
```

### Sorting Characters

```python
sorted(s)          # returns a list of chars
''.join(sorted(s)) # back to a string
```

### Counting Frequency

```python
from collections import Counter
freq = Counter(s)       # Counter({'a': 3, 'b': 2, ...})
s.count('a')            # count single character
```

### String Efficiency Notes

* **Avoid concatenation in loops** - use `''.join(parts)` instead of `result += char`.
* **Slicing is O(k)** (k = slice length), not O(1); avoid inside tight loops when possible.
* **Precompute `len(s)`** outside loops if called repeatedly - although Python's `len()` is O(1), it avoids attribute lookups inside hot paths.

## Problems

1. [Roman to Integer](https://leetcode.com/problems/roman-to-integer/description/) - Convert a Roman numeral string to its integer value using symbol-to-value mapping and handle the subtraction rule (e.g. IV = 4).
2. [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/) - Parse a string into a 32-bit signed integer, handling leading whitespace, optional sign, non-digit characters, and overflow. Painful to process :)
3. [Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/description/) - Design an algorithm to encode a list of strings into a single string and decode it back, handling edge cases like empty strings and strings containing delimiters.
4. [String Compression](https://leetcode.com/problems/string-compression/description/) - Compress a character array in-place by replacing consecutive repeated characters with the character followed by its count. Modify the array in-place and return the new length.
