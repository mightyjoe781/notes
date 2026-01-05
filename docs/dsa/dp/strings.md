# DP on Strings

## LCS

A **common subsequence** of two strings is a subsequence that is common to both strings.
For e.g. `ace` is a subsequence of `abcde`

We are supposed to find the Longest Common Subsequence between two strings.

Problem Link 1143 : [Link](https://leetcode.com/problems/longest-common-subsequence/description/)

This is clearly a 2D DP problem, as both `(i, j)` define the state of problem at any moment in time.

Recurrence Relation

$$
\begin{align}
P(i, j) &= 1 + P(i+1, j+1), \text{ when } s[i] == s[j] \\
P(i, j) &= max(P(i, j+1), P(i+1, j))
\end{align}
$$

Solution : 

```python
def main(s1, s2):
    n, m = len(s1), len(s2)

    @cache
    def lcs(i, j):
        
        if i >= n or j >= m:
            return 0
        
        if s1[i] == s2[j]:
            return 1 + lcs(i+1, j+1)
        
        return max(lcs(i, j+1), lcs(i+1, j))
        
    return lcs(0, 0)
    
```

TODO : convert this to Tabulation DP and then find the subsequence that is maximum length.

## LPS (Longest Palindromic Subsequence)

Problem Link 583 : [Link](https://leetcode.com/problems/longest-palindromic-subsequence/description/)

A very simple solution of this problem is : 

$$
lps = lcs(s1, s1[::-1], 0, 0)
$$

calculate *lcs* possible between s and its reverse.

Other solution involves using the two pointers in recursion.

```python

def main(s):
    
    @cache
    def solve(l, r):
        if l > r:
            return 0
        
        # handles the odd case
        if l == r:
            return 1
            
        if s[l] == s[r]:
            return 2 + solve(l + 1, r - 1)
        
        return max(solve(l+1, r), solve(l, r - 1))
        
    return solve(0, len(s) - 1)

```

## Minimum Insertions to make String Palindrome

Problem Link 1312 : [Link](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/description/)

This is little confusing at first but ultimately its just find the `lps` and then find how many characters didn't match, that many insertions will be required `n - lps(s)`

$$
ans = n - lps(0, 0)
$$

## Minimum Insertions/Deletion to Convert String

Problem Link 583 : [Link](https://leetcode.com/problems/delete-operation-for-two-strings/description/)

It has similar concept to above DP states, when the characters match we got a valid state but only difference is in base case.
If either of string ends before the other, rest all characters must be deleted.

```python

def minDistance(word1, word2):
    n, m = len(word1), len(word2)
    
    @cache
    def solve(i, j):
        if i == n and j == m: return 0

        if i >= n or j >= m: 
            return max(n-i, m-j)
        
        if word1[i] == word2[j]:
            return solve(i+1, j+1)

        return 1 + min(solve(i+1, j), solve(i, j+1))
    
    return solve(0, 0)
```


## Longest Common SuperSequence

Problem Link : [Link](https://leetcode.com/problems/shortest-common-supersequence/)

In this problem we can concat both strings and find LCS (Longest Common Subsequence) for resulting string.

Explanation about how to rebuild the state for example of `groot` and `brute` : [Link](https://takeuforward.org/data-structure/shortest-common-supersequence-dp-31)

![](assets/Pasted%20image%2020260104193028.png)


```python

def main(s1, s2):
        # use lcs code from above

        lcs_n = n + m - lcs(0, 0)

        i = j = 0
        res = []

        while i < n and j < m:
            if str1[i] == str2[j]:
                res.append(str1[i])
                i += 1
                j += 1
            else:
                if lcs(i+1, j) >= lcs(i, j+1): # key criteria
                    res.append(str1[i])
                    i += 1
                else:
                    res.append(str2[j])
                    j += 1

        # append remaining characters
        res.append(str1[i:])
        res.append(str2[j:])

        return "".join(res)
```

NOTE: if you are not able to rebuild it here refer to LCS state building from the same site.

## Distinct Subsequences

Problem Link - 115 : [Link](https://leetcode.com/problems/distinct-subsequences/)

Statement : Return _the number of distinct_ **_subsequences_** _of_ s _which equals_ t.


So the recursion below describes the case where a character is matching in both `s` and `t`, then we have two choice, either we take it or don't take it.

If characters are not same then subsequence will not be matched.


```python
def main(s, t):
    n, m = len(s), len(t)

    @cache
    def solve(i, j):

        if j == m:
            return 1 # return 1 for valid counting
        if i >= n:
            return 0 # impossible to count it as a solution
        if s[i] == t[j]:
            return solve(i+1, j) + solve(i+1, j+1)

        return solve(i+1, j)
    
    return solve(0, 0)
```

## Edit Distance

Problem Link 72 : [Link](https://leetcode.com/problems/edit-distance/)

Its similar to question above: Minimum Insertions/Deletion to Convert String.
Only recursion is different this time and requires three possibilities.

$$
\begin{align}
P(i, j) &= P(i+1, j+1), \text{ when } s[i] == s[j] \\
P(i, j) &= 1 + min(P(i, j+1) , P(i+1, j), P(i+1, j+1))
\end{align}
$$

Try to approach the problem.

## WildCard Matching

Problem Link - 44 : [Link](https://leetcode.com/problems/wildcard-matching/description/)

This problem is little tricky mostly due to a corner base cases :

- First condition here means we are able to match both `pattern` and `string` successfully
- If pattern is exhausted but string still has characters then we return `False`
- If string is exhausted but rest of pattern is `*` : Tricky Base Case

Example : 

```
s = "abc"
p = "abc*"
```

- Another tricky part is recursion let's say pattern is `*` there we could match up any number of characters, which is represented by taking two scenarios where we match current character but still try to match same `*` with next character `solve(i+1,j)`, and another scenario where we don't match anything with `*`. Allowing us to match `*` with 0 or more characters.

```
s = "acdcb"
p = "a*c?b"
```

Solution :

```python
def isMatch(self, s: str, p: str) -> bool:
    n, m = len(s), len(p)

    @cache
    def solve(i, j):
        # both exhausted
        if i == n and j == m:
            return True

        # pattern exhausted
        if j == m:
            return False

        # string exhausted
        if i == n:
            return all(c == '*' for c in p[j:])

        if p[j] == s[i] or p[j] == '?':
            return solve(i+1, j+1)

        if p[j] == '*':
            return solve(i, j+1) or solve(i+1, j)

        return False

    return solve(0, 0)
```

Cache might fail here to a special case where a single character is repeated multiple times, better use a dp table for that case.