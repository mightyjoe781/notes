# Grid DP

### Minimum Path Sum

* [Problem Link](https://leetcode.com/problems/minimum-path-sum/)
* Direction Constraint : down, right only
* We have to minimize the sum along a valid path from `(0,0)` to `(m-1, n-1)`
* Split criteria: Two sets of problems, where we can either take the down or right cell
    * $s_1$ : Min. Path Sum given first step is right step, then solving problem for $P(0, 1)$
    * $s_2$ : Min. Path Sum given first step is right step, then solving problem for $P(1, 0)$
* All matrices are suffix matrix for the original matrix
* Recurrence: $P(0, 0) = min\{P(0, 1), P(1, 0)\} + A[0][0]$
* Its a two dimensional DP, $m*n$
* Base Cases : declare extra column & row with the value `INT_MAX`
* Order to fill the table, bottom to top & right to left

```python
def minPathSum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
    dp[m-1][n] = dp[m][n-1] = 0

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            dp[i][j] = grid[i][j] + min(dp[i+1][j], dp[i][j+1])

    return dp[0][0]
```

### Dungeon Game

* [Problem Link](https://leetcode.com/problems/dungeon-game/description/)
* Find a path where the health of knight doesn’t go below zero, 
* Split Criteria
    * $H_1$ : Initial min. Health of knight for rescuing in the box `(0, 1)` to `(m-1, n-1)`
    * $H_2$ : Initial min. Health of knight for rescuing in the box `(1, 0)` to `(m-1, n-1)`
* By definition $H_1 > 0$ & $H_2 > 0$, so `dp[0][0] = val`, so both subproblems will become `H1` is `-6` & `H2` is `-5`, assuming initial health as `val-6` and `val-5` respectively, and it is guaranteed that one path will lead to solution by problem constraint
* Base Case
    * bottom row : $H_1 = \max(H_1 - val, 1)$
    * right column : $H_2 = \max(H_2 - val, 1)$
* Order of filling : B to L & R to L

```python
def calculateMinimumHP(dungeon):
    m, n = len(dungeon), len(dungeon[0])

    @cache
    def solve(i, j):
        if i == m or j == n:
            return float('inf')
        if i == m-1 and j == n-1:
            return max(1 - dungeon[i][j], 1)
        min_next = min(solve(i+1, j), solve(i, j+1))
        return max(min_next - dungeon[i][j], 1)

    return solve(0, 0)
```

**Tabulation**

```python
def calculateMinimumHP(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [[float('inf')] * n for _ in range(m)]

    dp[m-1][n-1] = max(1 - dungeon[m-1][n-1], 1)

    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            if i == m-1 and j == n-1:
                continue
            min_next = min(
                dp[i+1][j] if i+1 < m else float('inf'),
                dp[i][j+1] if j+1 < n else float('inf')
            )
            dp[i][j] = max(min_next - dungeon[i][j], 1)

    return dp[0][0]
```

### Unique Paths

* https://leetcode.com/problems/unique-paths/description/

### Frog Jump

* [Problem Link](https://leetcode.com/problems/frog-jump/)
* Split Criteria: at each step we could jump to `k` , `k+1`, `k-1`
* Representation : $P(S_i,k)$ : can we reach the last stone starting from $s_i$ assuming the last jump made was `k`
* Recurrence : $P(s_i, k) = P(s_j, k-1) || P(s_l, k) || P(s_m, k+1)$
* where $s_j = s_i + k - 1$, $s_l = s_i + k$ , $s_m = s_i +k+1$, s : represents the indices
* Size : nxn, max possible jump is `n+1`, order of filling : bottom to top

* Bottom-up always computes all subproblems; top-down computes only the needed ones - prefer top-down here.

**Top-Down Solution**

```python
def canCross(stones):
    if stones[1] != 1:
        return False

    stone_set = set(stones)
    last = stones[-1]

    @cache
    def solve(pos, k):
        if pos == last:
            return True
        for jump in [k-1, k, k+1]:
            if jump > 0 and pos + jump in stone_set:
                if solve(pos + jump, jump):
                    return True
        return False

    return solve(1, 1)
```

## Palindrome DP

### Longest Palindromic Subsequences

* [Problem Link](https://leetcode.com/problems/longest-palindromic-subsequence/)
* Check Stone Game Problem : [Link](ch5.md)
* Hint : Recurrence : 
    * Equal : $P(0, n-1) = 2 + P(1, n-2)$
    * Not Equal : $P(0, n-1) = max\{P(1, n-1), P(0, n-2)\}$


```python
def longestPalindromeSubseq(s):
    n = len(s)

    @cache
    def solve(l, r):
        if l > r: return 0
        if l == r: return 1
        if s[l] == s[r]:
            return 2 + solve(l+1, r-1)
        return max(solve(l+1, r), solve(l, r-1))

    return solve(0, n-1)
```

**Tabulation**

```python
def longestPalindromeSubseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    for length in range(1, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 1:
                dp[i][j] = 1
            elif s[i] == s[j]:
                dp[i][j] = 2 + (dp[i+1][j-1] if i+1 <= j-1 else 0)
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])

    return dp[0][n-1]
```

### Min Cuts for Pal

* [Link](https://leetcode.com/problems/palindrome-partitioning-ii/description/)
