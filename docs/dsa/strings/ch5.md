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

