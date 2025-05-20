# String Tasks

String tasks involve manipulation, analysis, and transformation of strings. These are frequently encountered in contests and technical interviews.

### Character Counting & Frequency Maps

- Useful for **anagrams**, **palindromes**, or finding **most/least frequent characters**.
- Use Counter (Python) or arrays (int[26] for lowercase letters).

````python
from collections import Counter
freq = Counter(s)
````

### Prefix / Suffix Processing

- Compute **prefix sums**, **hashes**, or match substrings from the start or end.
- s.startswith("abc"), s.endswith("xyz") (Python methods)

### Palindrome Checks

- Reverse and compare: s == s[::-1]
- Efficient check for substrings using 2 pointers or dynamic programming.

### Lexicographical Comparisons

- Compare strings as numbers or words: "abc" < "abd" → True
- Useful for finding minimal/maximal rotations or rearrangements.

### Sliding Window on Strings

- For substring problems like finding the smallest/biggest/first substring with some property.
- Time: O(n) with hashmap or frequency arrays.

Example: Longest substring without repeating characters.

### String Hashing (Rabin-Karp)

- Compute hash of substrings in O(1) using prefix hash arrays.
- Useful for **duplicate substrings**, **pattern matching**, or **string equality checks**.

### Z-Algorithm / Prefix Function (KMP)

- Efficient pattern matching.
- Find all occurrences of a pattern in a text in O(n + m).

### Minimum / Maximum Operations

- Turn string to palindrome, make all chars equal, reduce to one character, etc.
- Usually involves DP or greedy strategies.

````python
s.split(), s.replace(), re.findall()
````

### String Rewriting / Parsing

- Tokenize by space, delimiter, regex.
- Replace substrings, compress sequences, etc.