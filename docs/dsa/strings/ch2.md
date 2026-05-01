# String Matching

## Library Solution

Python's built-in string methods handle most basic matching needs efficiently.

* `str.find(sub)` - returns the index of the first occurrence, or `-1` if not found.
* `sub in s` - O(n) membership test; clearest way to check presence.
* `str.index(sub)` - like `find()` but raises `ValueError` on miss.

```python
text = "hello world"
pattern = "world"
if pattern in text:
    print(f"Pattern found at index {text.find(pattern)}")
else:
    print("Pattern not found")
```

## String Hashing

String hashing is a preprocessing technique that converts a string into a numeric value (hash). This value allows efficient comparisons of substrings.

Algorithm

* Choose a **base** (e.g., 31) and a **modulus** (e.g., $10^9+7$).

* Compute the hash of the string using the formula:

  $$H[i] = (H[i-1] \cdot \text{base} + \text{char}[i]) \mod \text{modulus}$$

* Use **prefix hashes** to compute substring hashes efficiently.

```python
def compute_hash(s: str, base: int = 31, mod: int = 10**9 + 7) -> list[int]:
    h = [0] * (len(s) + 1)
    for i, c in enumerate(s):
        h[i + 1] = (h[i] * base + (ord(c) - ord('a') + 1)) % mod
    return h

# Substring hash: hash(s[l..r]) in O(1) using prefix hashes + powers
def get_substring_hash(h: list[int], powers: list[int], l: int, r: int, mod: int) -> int:
    return (h[r + 1] - h[l] * powers[r - l + 1]) % mod
```

## Rabin-Karp

[Best Explanation of Rabin Karp](https://www.youtube.com/watch?v=4qEZned9qWM)

The Rabin-Karp algorithm uses hashing to find all occurrences of a pattern in a text.

Algorithm

* Precompute the hash of the pattern and the initial substring of the text of the same length.
* Slide over the text:
    * If the hashes match, verify the strings.
    * Recompute the hash for the next substring in O(1)
* Complexity: O(N + M) on average.
* Things to consider while implementation
    * Always verify with string comparison after hash match
    * Consider double hashing for critical applications
    * Birthday Paradox - The **Birthday Paradox** refers to the counterintuitive probability result that in a group of just 23 people, there is about a 50% chance that at least two people share the same birthday. Shows the vulnerability of hash functions to collisions, leading to the "birthday attack" where finding two inputs that hash to the same output is easier than expected.


```python
def rabin_karp(text: str, pattern: str) -> bool:
    n, m = len(text), len(pattern)
    if m > n:
        return False

    base, mod = 31, 10**9 + 7
    char_val = lambda c: ord(c) - ord('a') + 1
    power = pow(base, m - 1, mod)

    p_hash = t_hash = 0
    for i in range(m):
        p_hash = (p_hash * base + char_val(pattern[i])) % mod
        t_hash = (t_hash * base + char_val(text[i])) % mod

    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i + m] == pattern:
            return True
        if i < n - m:
            t_hash = (t_hash - char_val(text[i]) * power) % mod
            t_hash = (t_hash * base + char_val(text[i + m])) % mod
    return False
```

## Z-Function

The Z-function computes an array where Z[i] is the length of the longest substring starting from i that matches the prefix of the string.

Applications

* Pattern Matching (Exact Match) : concatenate P and T : `P + '$' + T`, compute Z-function for such string. If $Z[i] \geq \text{length of } P$ , the pattern occurs starting at $i - (\text{length of } P + 1$) 
* Finding Periods in Strings
* Counting Unique Substrings
* String Compression

Algorithm

* Initialize Z[0] = 0 .
* Maintain a window [L, R] that matches the prefix.
* For each i :
    * If $i \leq R$, use previously computed values.
    * Otherwise, compute Z[i] directly
* Complexity: O(N)

```python
def compute_z(s: str) -> list[int]:
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z
```

## Prefix Function (KMP) Algorithm

Very Good Explanation : [Link](https://www.youtube.com/watch?v=M9azY7YyMqI&list=PL3edoBgC7ScV9WPytQ2dtso21YrTuUSBd)

The Knuth-Morris-Pratt (KMP) algorithm avoids redundant comparisons by precomputing a prefix function(lps).

Algorithm

* Compute the prefix function:
    *  $\text{pi}[i]$ is the length of the longest prefix that is also a suffix for the substring ending at i .
* Use $\text{pi}[]$ to skip unnecessary comparisons
* Complexity: O(N + M).

```python
def compute_prefix_function(pattern: str) -> list[int]:
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi
```

```python
def str_str(haystack: str, needle: str) -> int:
    n = len(needle)
    if n == 0:
        return 0
    lps = compute_prefix_function(needle)
    i = j = 0
    while i < len(haystack):
        if haystack[i] == needle[j]:
            i += 1
            j += 1
        if j == n:
            return i - n
        elif i < len(haystack) and haystack[i] != needle[j]:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1
```

