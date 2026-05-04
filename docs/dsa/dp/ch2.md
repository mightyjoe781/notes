# 2D/3D DP

## Grid Unique Paths

Problem Link 62 - [Link](https://leetcode.com/problems/unique-paths/)

Problem is Simple Grid traversal, and count ways you can reach to final tile.

```python

def uniquePaths(self, m: int, n: int) -> int:

    # dp = [[0] * (n+1) for _ in range(m+1)]
    # dp[m-1][n-1] = 1

    # for i in range(m-1, -1, -1):
    #     for j in range(n-1, -1, -1):
    #         dp[i][j] += dp[i+1][j] + dp[i][j+1]
        
    # return dp[0][0]

    @cache
    def solve(i, j):
        
        if i >= m or j >= n: # invalid point
            return 0
        
        if i == m-1 and j == n-1:
            return 1

        return solve(i+1, j) + solve(i, j+1)


    return solve(0, 0)

```

## Unique Paths II

Problem Link 63 - [Link](https://leetcode.com/problems/unique-paths-ii/)

Problem is similar to above problem, except we now early terminate impossible grid points,

```python
def uniquePathsWithObstacles(grid):
    m, n = len(grid), len(grid[0])
    
    @cache
    def solve(i, j):
        if i >= m or j >= n or grid[i][j]:
            return 0
            
        if i == m-1 and j == n-1:
            return 1
        
        return solve(i+1, j) + solve(i, j+1)
    
    return solve(0, 0)
```


## Minimum Path Sum

Problem Link 64 - [Link](https://leetcode.com/problems/minimum-path-sum/)

```python

def minPathSum(grid):
    n, m = len(grid), len(grid[0])
    
    @cache
    def solve(i, j):

        if i >= n or j >= m: # impossible path, stop traversal
            return float('inf')

        if i == n-1 and j == m-1:
            return grid[i][j]

        return grid[i][j] + min(solve(i+1, j), solve(i, j+1))
    
    return solve(0, 0)
```


## Triangle

```python

def minimumTotal(triangle):
    
    n = len(triangle)

    @cache
    def solve(i, j):
        if i >= n or j >= n:
            return float('inf')

        if i == n-1:
            return triangle[i][j]

        return triangle[i][j] + min(solve(i+1, j), solve(i+1, j+1))

    return solve(0, 0)
    
    # dp = [row[:] for row in triangle]  # copy triangle

    # for i in range(n-2, -1, -1):
    #     for j in range(i+1):
    #         dp[i][j] = triangle[i][j] + min(
    #             dp[i+1][j],
    #             dp[i+1][j+1]
    #         )

    # return dp[0][0]

```

## Minimum Falling Path Sum

Problem Link 931 - [Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/)

```python

def minFallingPathSum(matrix):

    n = len(matrix)

    dp = [[0] * n for _ in range(n)]

    # Base case: last row
    for j in range(n):
        dp[n-1][j] = matrix[n-1][j]

    # Build bottom-up
    for i in range(n-2, -1, -1):
        for j in range(n):
            dp[i][j] = matrix[i][j] + min(
                dp[i+1][j],
                dp[i+1][j-1] if j > 0 else float('inf'),
                dp[i+1][j+1] if j < n-1 else float('inf')
            )

    return min(dp[0])
```


## Best Time to Buy & Sell Stocks with Txn Fee

* [Best Time to Buy and Sell Stocks with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) : might look like above problems but its not because we can sell at will.
* Cue to DP : Maximize profit (try DP!)
* DnC criteria : think about all possible txn, so we can buy on 6th day and sell on 1st day $(b_6, s_1)$, like that there could be many element of the set. Now problem is finding subproblem which provide us mutually exclusive & exhaustive sets.
* We could purchase on first day and don’t buy on first day. Let’s try to related the subproblem to original problem
* Purchase on 0th day
    * $s_1$ : max profit you can make from $D[1... n-1]$, assuming first thing we do is sell $[S_i, (B_j S_k), (B_iS_m)....]$
* Don’t purchase on 0th day
    * $s_2$ : max profit that you can make from $D[1...n-1]$, assuming you start with a buy
* Here we can notice that that there are two degree of freedom making this problem 2D DP

* We will need 2 variable, 1 representing suffix sum & second represent the operation (buy/sell)
* Representation: $f(D, 0, 1, fee)$
    * $s_1$ : $f(D, 1, 0, fee)$
    * $s_2$ : $f(D,1, 1, fee)$
* NOTE: purchase can be represented as negative profit.
* $f(D, 0, 1) = max(-D[0] + f(D,1, 0), f(D, 1, 1))$
* but here there is no way to solve $f(D, 1, 0)$ ? We will need to write another recurrence for it
* $f(D, 0, 0) = max(D[0] + f(D, 1, 1) - fee, f(D, 1, 0))$
* We will have two arrays tracking
    * `n(buy)` : all suffix arrays
    * `n(sell)` : all prefix arrays

```python
def maxProfit(prices, fee):
    n = len(prices)

    @cache
    def solve(i, holding):
        if i == n:
            return 0
        if holding:  # have stock, can sell or hold
            return max(prices[i] - fee + solve(i+1, False), solve(i+1, True))
        else:  # no stock, can buy or skip
            return max(-prices[i] + solve(i+1, True), solve(i+1, False))

    return solve(0, False)
```

**Tabulation**

```python
def maxProfit(prices, fee):
    n = len(prices)
    # hold[i] = max profit from day i onward when holding stock
    # cash[i] = max profit from day i onward when not holding
    hold = [0] * (n + 1)
    cash = [0] * (n + 1)

    for i in range(n - 1, -1, -1):
        hold[i] = max(prices[i] - fee + cash[i+1], hold[i+1])
        cash[i] = max(-prices[i] + hold[i+1], cash[i+1])

    return cash[0]
```

## Longest Arithmetic Subsequence

* Nested, 2D DP
* [Problem Link](https://leetcode.com/problems/longest-arithmetic-subsequence/)

1. Modelling the Problem: We have to find $res = max\{s_i\}$, where $s_i$ : length or largest Arithmetic Subsequence ending at $i$
2. Now to find $s_i$ : Assume $j$ for every $j < i$ s.t. common difference `d = A[i] - A[j]` is same.
3. Notice how this requires us to track common difference as well, converting this problem into a 2 DP Problem
4. Dimensions - Prefix Array, Common Difference
5. Data Structure -> use `unordered_map<int,int> `: key -> cd , value -> length of longest chain.

```python
def longestArithSeqLength(nums):
    n = len(nums)
    dp = [dict() for _ in range(n)]  # dp[i][diff] = length ending at i with common diff
    res = 0

    for i in range(n):
        for j in range(i):
            d = nums[i] - nums[j]
            dp[i][d] = dp[j].get(d, 1) + 1
            res = max(res, dp[i][d])

    return res
```

## Target Sum

* [Problem Link](https://leetcode.com/problems/target-sum/description/)
* Subset DP, 2 D DP, Counting Problem
* DnC Criteria : Split the set into 2 components, set $s_1$ contains the sum with $A[0]$ in positive sign while another set $s_2$ with $A[0]$ in negative sign
    * $s_1$ : number of ways to make `target-A[0]` from `A[1...n]`
    * $s_2$ : number of ways to make `target+A[0]` from `A[1...n]`

* Recurrence : $P(A, 0, target) = P(A, 1, target-A[0]) + P(A, 1, target + A[0])$
* Size of DP Array : $n(2 + (\Sigma{A[i] + 1}))$
* To understand the order of filling the table, try to put some value on above recurrence
* Base Case : `n-1` row where the `1` where `target == A[n-1]` otherwise `0`, or using n

```python
def findTargetSumWays(nums, target):
    n = len(nums)

    @cache
    def solve(i, curr):
        if i == n:
            return 1 if curr == target else 0
        return solve(i+1, curr + nums[i]) + solve(i+1, curr - nums[i])

    return solve(0, 0)
```

**Tabulation**

```python
def findTargetSumWays(nums, target):
    from collections import defaultdict
    dp = defaultdict(int)
    dp[0] = 1

    for num in nums:
        next_dp = defaultdict(int)
        for curr, ways in dp.items():
            next_dp[curr + num] += ways
            next_dp[curr - num] += ways
        dp = next_dp

    return dp[target]
```

## Edit Distance

* [Problem Link](https://leetcode.com/problems/edit-distance/)
* Famous Problem Commonly Asked in Interviews
* Here, `dp[i][j]` refers to minimum operation needed to convert `s1[0...i]` into `s2[0...j]`
* Given the operations
    * If `s1[i] == s2[j]` then `dp[i][j] = dp[i-1][j-1]`
    * If `s1[i] != s2[j]`
        * `dp[i][j] = dp[i-1][j-1] + 1` : replace operation
        * `dp[i][j] = dp[i][j-1]+1 ` : insertion operation
        * `dp[i][j] = dp[i-1][j]+1 ` : delete operation
        * `dp[i][j]` is minimum of above operation.
* order of filling from top to down and left to right
* Base Case : to  transform [a] into [ab….] if there is a in second word then $n-1$ deletion otherwise $n$. Simpler base case is by shifting everything by one. :)
* we add a row above the table and column of left side too. just to make the base case simpler.

```python
def minDistance(word1, word2):
    m, n = len(word1), len(word2)

    @cache
    def solve(i, j):
        if i == m: return n - j
        if j == n: return m - i
        if word1[i] == word2[j]:
            return solve(i+1, j+1)
        return 1 + min(solve(i+1, j), solve(i, j+1), solve(i+1, j+1))

    return solve(0, 0)
```

**Tabulation**

```python
def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    return dp[m][n]
```
