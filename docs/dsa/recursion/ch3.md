# String Recursion

## Palindrome Partitioning

[Leetcode Link](https://leetcode.com/problems/palindrome-partitioning/)

* Given a string `s`, partition `s` such that every substring of the partition is a substring, Enumerate all such solutions

Split Strategy

* divide into `n` chunks
* set of solution where first partition `a` : `a | a | b`
* set of solution where first partition `aa` : `a a | b`
* set of solution where first partition `aab` : $\phi$ // prefix is not a palindrome

Subproblem

* $c_i$ : All the palindrome partition of elements of array after $i$ and then append palindrome before $c_i$

* 1 D Subproblem, its a suffix array problem

Python Solution :

```python

def partition(s):

    n = len(s)
    res = []

    def dfs(i, curr):

        if i == n:
            res.append(curr[:])
            return
        
        for j in range(i, n):
            part = s[i:j + 1]
            if part == part[::-1]: # check palindrome
                dfs(j+1, curr + [part])


    dfs(0, [])
    return res

```

## Word Search

[Leetcode Link](https://leetcode.com/problems/word-search/description/)

* Problem based on 2D Matrix DFS, standard backtracking pattern - see [ch4 Backtracking](ch4.md#word-search) for full solution.


## Word Break

Problem Link 139 - [Link](https://leetcode.com/problems/word-break/)

Although this a DP problem but shows how recursion can be used to this problem.

Python Solution :

```python
def wordBreak(s, wordDict):

    dt = set(wordDict)
    @cache
    def dfs(i):
        if i == len(s): return True

        word = ""
        ans = False
        for j in range(i, len(s)):
            word += s[j]
            if word in dt:
                ans |= dfs(j+1)
        return ans

    return dfs(0)
```


## Rat in a Maze

**Problem Statement:** Given a grid of dimensions n x n. A rat is placed at coordinates (0, 0) and wants to reach at coordinates (n-1, n-1). Find all possible paths that rat can take to travel from (0, 0) to (n-1, n-1). The directions in which rat can move are 'U' (up) , 'D' (down) , 'L' (left) , 'R' (right).  
The value 0 in grid denotes that the cell is blocked and rat cannot use that cell for traveling, whereas value 1 represents that rat can travel through the cell. If the cell (0, 0) has 0 value, then mouse cannot move to any other cell.

NOTE: instead of using visited array, reused the grid. Generally its bad practice mutate the inputs.

```python

def main(n, grid):
    res = []
    dirs = [(0, 1, "R"), (1, 0, "D"), (-1, 0, "L"), (0, -1, "U")]

    def dfs(i, j, path):
        if i == n - 1 and j == n - 1:
            res.append(path)
            return

        if i < 0 or j < 0 or i >= n or j >= n:
            return

        if grid[i][j] == 0:
            return

        # block back travel
        grid[i][j] = 0

        for dx, dy, name in dirs:
            dfs(i + dx, j + dy, path + name)

        # reset grid
        grid[i][j] = 1

    dfs(0, 0, "")
    return res


```

## Valid Parenthesis

### Number of Valid Parenthesis

```
n = 2 => possible ~ [(), )(]
res = 1
```

A simple python solution

```python

def ways(n):
    # invalid scenario
    if n & 1:
        return 0
    
    @cache 
    def count(op, close):
        # invalid scenario, too many open
        if close < op:
            return 0
        
        if not op:
            return 1
        
        return count(op - 1, close) + count(op, close - 1)
    
    return count(n//2, n//2)
        
```

If $n$ is odd then there no possible answer, but if $n$ is even, then is just arranging $n//2$ pairs of open close brackets,

Arranging all $n//2$ pairs in all possible ways. We can use *Catalan Number* to calculate arrangements which are valid.

$$
C_n = \frac{1}{n+1} \binom{2n}{n} = \frac{(2n)!}{(n+1)!n!}
$$

```python

def findWays(self, n):
    
    if n & 1:
        return 0
    
    k = n//2 # pairs
    
    
    res = 1
    for i in range(k):
        res = res * (2 * k - i)//(i+1)
    
    return res // (k + 1)

```

Read more on Catalan Number and its Application : [Link](https://www.geeksforgeeks.org/maths/catalan-numbers/)
### Generate all Valid Parenthesis

```python

def generate_parentheses(n):
    if n & 1:
        return []

    k = n // 2
    res = []

    def dfs(open, close, path):
        # invalid: more ')' than '(' used
        if close < open:
            return
        
        # finished building
        if open == 0 and close == 0:
            res.append(path)
            return
        
        # place '(' if available
        if open > 0:
            dfs(open - 1, close, path + "(")
        
        # place ')' if valid
        if close > 0:
            dfs(open, close - 1, path + ")")

    dfs(k, k, "")
    return res

```