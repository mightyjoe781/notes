# String Processing with DP

- String DP problems usually involve breaking a string into smaller parts and solving subproblems based on those. It includes:
    - Subsequence & substring analysis
    - Palindromes
    - Pattern matching
    - Partitioning
    - Edit distances

### Core Concepts

- Substrings vs Subsequences
    - **Substring**: Continuous sequence (e.g. "abc" in "abcd").
    - **Subsequence**: Can skip characters but maintain order (e.g. "acd" in "abcd").
- State Design
    - Most problems are defined using:
    - `dp[i][j]` → answer for the substring `s[i..j]`
    - `dp[i][j]` → answer for prefixes/suffixes
    - `dp[i]` → answer for prefix of length `i`
- Recurrence Patterns
    - Try partitioning the string at every k, solving for `i..k` and `k+1..j`.
    - Use memoization to avoid recomputing overlapping subproblems.

### Classic Patterns

- Longest Common Subsequence (LCS)

````c++
if s1[i-1] == s2[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
````

- Longest Palindromic Subsequence

````c++
if s[i] == s[j]:
    dp[i][j] = 2 + dp[i+1][j-1]
else:
    dp[i][j] = max(dp[i+1][j], dp[i][j-1])
````

- Longest Palindromic Substring

````c++
dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]
````

- Edit Distance

````c++
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1]
else:
    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
````

### Advance Patterns

- Palindrome Partitioning
- State
    - `is_pal[i][j]` = True/False for checking palindromes
    - `dp[i]` = min cuts for `s[0..i]`

````c++
if is_pal[j][i]:
    dp[i] = min(dp[i], 1 + dp[j-1])
````

- Count Distinct Subsequences
    - **Problem**: Count how many times t occurs as a subsequence of s
    - State: `dp[i][j]` = ways to form `t[0..j-1]` using `s[0..i-1]`

````c++
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
else:
    dp[i][j] = dp[i-1][j]
````

### Longest Palindromic Subarray

Given a string `s`, return the longest substring of `s` that is a _palindrome_.

A **palindrome** is a string that reads the same forward and backward.

This is *two-pointer* approach to problem.

```python

def longestPalindrome(s: str) -> str:

    n = len(s)
    if n == 0:
        return ""

    start = 0
    max_len = 1

    def expand(l, r):
        nonlocal start, max_len
        while l >= 0 and r < n and s[l] == s[r]:
            if r - l + 1 > max_len:
                start = l
                max_len = r - l + 1
            l -= 1
            r += 1

    for i in range(n):
        expand(i, i)     # odd length
        expand(i, i + 1) # even length

    return s[start:start + max_len]

```

This is a $O(n^2)$ solution, There is a better approach to solve this problem using *Manacher's Algorithm* in $O(n)$ time.

Key Idea

- Unify odd and even length palindromes by inserting a special character like (`#`) between characters. Example : `abba`, `#a#b#b#a#`
- Use previous palindrome information to avoid rechecking characters
- Maintain a current Rightmost Palindrome and mirror indices to reuse results.

Instead of expanding from center independently, Manacher's algorithm *reuses* symmetry

```python

def longestPalindrome(s: str) -> str:

    def manacher(s):
        t = '#' + '#'.join(s) + '#'
        n = len(t)

        p = [0] * n

        l, r = 0, 0
        for i in range(n):
            p[i] = min(r - i, p[l + (r - i)]) if i < r else 0
            while (i + p[i] + 1 < n and i - p[i] - 1 >= 0
                    and t[i + p[i] + 1] == t[i - p[i] - 1]):
                p[i] += 1
            
            if i + p[i] > r:
                l, r = i - p[i], i + p[i]
        
        return p
    
    p = manacher(s)

    resLen, center_idx = max((v, i) for i, v in enumerate(p))
    resIdx = (center_idx - resLen) // 2

    return s[resIdx: resIdx + resLen]

```



