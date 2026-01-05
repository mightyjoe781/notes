# Matrix Chain Multiplication

Often known as Matrix Chain Ordering Problem, is an optimization problem concerning most efficient way to multiply a sequence of matrices.
NOTE: Problem is about the order not the actual multiplication

This problem sets stage for *interval DP problems*

Consider 4 matrices : A, B, C and D. Then there are 5 ways to multiply them :

$$
((AB)C)D = (A(BC))D) = (AB)(CD) = A((BC)D) = A(B(CD))
$$

Although order doesn't affect the final result, but multiplication complexity varies for each parenthesized term.

Example for matrices of $X \times Y$ and $Y \times Z$ requires $XYZ$ ordinary multiplications and $X(Y-1)Z$ additions.

Example : A is 10x30, B is 30 x 5, C is 5x 60

$$
\begin{align}
(AB)C &= (10\times 30\times 5) + (10 \times 5 \times 60) = 4500 \text{ operations} \\
A(BC) &= (30\times 5\times 60) + (10 \times 30 \times 60) = 27000 \text{ operations}
\end{align}
$$

The number of possible parenthesization of a product of matrices can be calculated using *Catalan Number*, but that would be very large to brute-force.

This problem has property of Overlapping Subproblems, so we can use dynamic programming to optimize the calculation.

In general, we can find the minimum cost using the following recursive algorithm:

- Take the sequence of matrices and separate it into two subsequences.
- Find the minimum cost of multiplying out each subsequence.
- Add these costs together, and add in the cost of multiplying the two result matrices.
- Do this for each possible position at which the sequence of matrices can be split, and take the minimum over all of them.

```python
def matrix_chain_order(dims: list[int]) -> int:
    n = len(dims)

    @cache
    def solve(i, j):
        # base case: one matrix or no matrix
        if j - i <= 1:
            return 0

        ans = float('inf')

        for k in range(i + 1, j):
            cost = (
                solve(i, k) +
                dims[i] * dims[k] * dims[j] +
                solve(k, j)
            )
            ans = min(ans, cost)

        return ans

    return solve(0, n - 1)
```


A more compressed version taken from Wiki : Interesting approach to write the recursive function and using defaults to yield invalid values.

```python
def matrix_chain_order(dims: list[int]) -> int:

    @cache
    def a(i, j):
        return min(
            (a(i, k) + dims[i] * dims[k] * dims[j] + a(k, j) for k in range(i + 1, j)),
            default=0,
        )

    return a(0, len(dims) - 1)
```

### Bottom Up MCM

State Represents : `dp[i][j] = minimum cost to multiply matrices from i to j-1`

Base Case : `dp[i][i+1] = 0     # single matrix => no cost`

```python
def matrixChainMultiplication(dims):
    n = len(dims)
    
    dp = [[0] * n for _ in range(n)]

    # length = gap between i and j
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            dp[i][j] = float('inf')

            for k in range(i + 1, j):
                cost = (
                    dp[i][k] +
                    dims[i] * dims[k] * dims[j] +
                    dp[k][j]
                )
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]
```

### Key TakeAway

This is a classical Interval DP Example, where are trying all the possible splits, and answer is all the possible partition points

Template is always in this format : 

```python
solve(l, r):
    if base case:
        return 0

    ans = INF
    for mid in range(l+1, r):
        ans = min/max(
            solve(l, mid) + cost(l, mid, r) + solve(mid, r)
        )
    return ans
```

Quite Famous Problems Related to This are :

- MCM
- Burst Balloons
- Palindrome Partitioning
- Optimal BST

## Cut Sticks

Problem Link - 1547 : [Link](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/submissions/1874820137/)

This could be converted into Interval DP simply by adding sentinals to the cuts,

```python
def minCost(self, n: int, cuts: List[int]) -> int:
    
    cuts = [0] + sorted(cuts) + [n]
    m = len(cuts)

    # dp = [[0] * m for _ in range(m)]

    # for length in range(2, m):
    #     for i in range(m - length):
    #         j = i + length
    #         dp[i][j] = float('inf')

    #         for k in range(i + 1, j):
    #             cost = dp[i][k] + dp[k][j] + (cuts[j] - cuts[i])
    #             dp[i][j] = min(dp[i][j], cost)

    # return dp[0][m - 1]

    @cache
    def solve(i, j):
        if j - i <= 1:
            return 0

        res = float('inf')
        for k in range(i+1, j):
            cost = (
                solve(i, k) +
                (cuts[j] - cuts[i]) + # cost we gain for cutting at k
                solve(k, j)
            )
            res = min(res, cost)
        return res

    return solve(0, m-1)
```

## Burst Balloons

Problem Link - 312 : [Link](https://leetcode.com/problems/burst-balloons/description/)
This problem should be trivial, just add virtual boundary of `nums = [1] + nums + [1]`

## Palindrome Partitioning II

Although this problem looks like interval DP but it is not. Reason for that is that cuts that you do on the array will accumulate as we move forward, there is no *meaningful merge cost* between two halves here.

Correct Recursion would be :

`solve(i) = min cuts needed for s[i:]`

This problem is more akin to *Prefix DP*

```python
def minCut(self, s: str) -> int:
    n = len(s)

    def is_pal(i, j):
        return s[i:j] == s[i:j][::-1]

    @cache
    def solve(i):
        if i == n:
            return -1  # important trick

        res = float('inf')
        for j in range(i + 1, n + 1):
            if is_pal(i, j):
                res = min(res, 1 + solve(j))
        return res

    return solve(0)
```

## Partition Array for Maximum Sum

Problem Link - 1043 : [Link](https://leetcode.com/problems/partition-array-for-maximum-sum/)

Its also a *Prefix DP*

```python
def maxSumAfterPartitioning(self, arr: List[int], k: int) -> int:
    n = len(arr)

    @cache
    def solve(i):
        if i >= n:
            return 0
        
        res = 0
        curr_max = 0
        for j in range(i, min(n, i+k)):
            curr_max = max(curr_max, arr[j])
            length = j - i + 1
            res = max(res, curr_max * length + solve(j+1))
        return res
        
    return solve(0)
```