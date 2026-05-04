# 1D DP

## Climbing Stairs

[Problem Link](https://leetcode.com/problems/climbing-stairs/)

* If a person stands at the bottom, he has choice of taking 1 or 2 steps, and he wants to reach to the top (`n th` stairs)
* This problem can easily be modeled using following recursion: `f(n) = f(n-1) + f(n-2)` , which is coincidently fibonacci sequence.
* Solving the above recursion using traditional recursion will result in a time limit exceeded error on any sufficiently capable platform. This problem requires determining the number of ways to solve it, not the specific ways themselves.
* But for solving above problem efficiently we might need to Memoization to store already calculated answers, 

* Splits
    * $x_1$ : ways to reach top floor using 1st floor
    * $x_2$ : ways to reach top floor using 2nd floor
* Recursion : `f(n) = f(n-1) + f(n-2)`
* Base cases: `f(1) = 1, f(2) = 2`

```python
from functools import cache

def climbStairs(n):
    @cache
    def solve(i):
        if i <= 1:
            return 1
        return solve(i-1) + solve(i-2)
    return solve(n)
```

Recurrence: $O(n^2)$, Memoization: $O(n)$

Now we could have solved same problem from smallest solution to largest then, we don’t even have to check anything. `dp[n]` would simply be the answer

```python
def climbStairs(n):
    if n == 1:
        return 1
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

Further Optimization can be done upon recognizing that we are using only 2 variables to store states. (State Compression)

## Frog Jump

Problem Link : [Link](https://takeuforward.org/data-structure/dynamic-programming-frog-jump-dp-3)

So this problem is similar to model as previous problem but now there is a cost for a jump that needs to be minimized.

Python Solution : 

```python

def frog_jump(heights):
    n = len(heights)
    heights.append(float("inf"))  # sentinel value
    
    # dp = [float("inf")] * (n + 1)
    # dp[n - 1] = 0

    # for i in range(n-1, -1, -1):
    #     dp[i] = min(
    #         dp[i + 1] + abs(heights[i] - heights[i + 1]),
    #         dp[i + 2] + abs(heights[i] - heights[i + 2]),
    #     )
    # return dp[0]

    @cache
    def jump(i):
        if i >= n:
            return float("inf") # invalid states

        if i == n - 1: # no need to jump
            return 0

        e1 = jump(i + 1) + abs(heights[i] - heights[i + 1])
        e2 = jump(i + 2) + abs(heights[i] - heights[i + 2])

        return min(e1, e2)

    return jump(0)
```


NOTE: How indexing problem can be solved using using sentinels, but be careful using these techniques.

## Frog Jump with `k` Distances

Problem Link - [Link](https://takeuforward.org/data-structure/dynamic-programming-frog-jump-with-k-distances-dp-4)

```python

def frog_jump(heights, k):
    n = len(heights)
    heights.extend([float("inf")] * k)  # sentinel value
    
    @cache
    def jump(i):
        if i >= n - 1: # no need to jump
            return 0
        
        res = float('inf')
        for j in range(1, k + 1):
            res = min(res, jump(i + j) + abs(heights[i] - heights[i + j]))
        return res

    return jump(0)

```

## House Robber

- [Problem Link](https://leetcode.com/problems/house-robber/)
- Notice how robber can’t rob two adjacent houses. Determing houses he will rob to get maximum money
- Now problem is no longer enumeration (where we could do choice of picking/leaving elements). Here we are given optimization problem and answer is one final answer.
- We can state the problem as, optimal solution either contains $x$ or it does not.
- Say optimal solution is $[H_i, H_j, H_k...]$ we can see that if $H_1$ is part of solution or it is not. dividing problem into two sets.
- Original Problem : $P(A, 0, n-1)$
- Subproblems
    - $p_1$ : $M(H_1) + P(A, 2, n-1)$  // including the H1
    - $p2$ : $P(A, 1, n-1)$ // doesn’t include H1
- Recurrence : $P(A, 0, n-1) = [M(H_1) + P(A, 2, n-1)] + [P(A, 1, n-1)]$
- Above Recurrence, in correct dimensions : $P(A, 0) = max{A(0) + P(A, 2), P(A, 1)}$
- Base Cases: while solving for last 2 elements its nothing but $max{A(n-1), A(n-2)}$ or we can last element `A(n-2)`
- Order of filling could be either direction, problem just flips to prefix in that case.

```python
def rob(nums):
    n = len(nums)

    @cache
    def solve(i):
        if i >= n:
            return 0
        return max(nums[i] + solve(i+2), solve(i+1))

    return solve(0)
```

**Tabulation**

```python
def rob(nums):
    n = len(nums)
    dp = [0] * (n + 2)
    dp[n-1] = nums[n-1]

    for i in range(n-2, -1, -1):
        dp[i] = max(nums[i] + dp[i+2], dp[i+1])

    return dp[0]
```

### Problems

* [House Robber II](https://leetcode.com/problems/house-robber-ii/) : Try similar problem with constraint changed.

## Decode Ways

[Problem Link](https://leetcode.com/problems/decode-ways/description/)

* Clearly problem is a counting problem, and we don’t want to enumerate
* DnC Criteria should make solution mutually exclusive and exhaustive
    * $s_1$ : set of all words made by considering only 1st character
    * $s_2$ : set of all words made by considering first 2 characters
* Let’s connect with original subproblem, hint: Suffix Array
* Original Problem: $P(S, 0)$
    * $s_1$ : $P(S, 1)$
    * $s_2$ : $P(S, 2)$
* Recurrence Relation: $P(s, 0) = P(s, 1) + P(s, 2)$
* NOTE: $s_2$ can be pruned while solving the problem as numbers greater than 26 are invalid.

```python

def numDecodings(s: str) -> int:
    n = len(s)

    @cache
    def solve(i):
        # reached end successfully
        if i == n:
            return 1

        # leading zero is invalid
        if s[i] == '0':
            return 0

        # take one digit
        res = solve(i + 1)

        # take two digits if valid
        if (
            i + 1 < n and
            (s[i] == '1' or (s[i] == '2' and s[i + 1] <= '6'))
        ):
            res += solve(i + 2)

        return res

    return solve(0)

```

**Tabulation**

```python
def numDecodings(s):
    n = len(s)
    dp = [0] * (n + 1)
    dp[n] = 1
    dp[n-1] = 0 if s[n-1] == '0' else 1

    for i in range(n-2, -1, -1):
        if s[i] != '0':
            dp[i] += dp[i+1]
        if s[i] == '1' or (s[i] == '2' and s[i+1] <= '6'):
            dp[i] += dp[i+2]

    return dp[0]
```

## Advanced 1D DP Problems

* These problems either have Nested Loops, or more than 1 degree of freedom but in a limited capacity (second dimension is small enough to enumerate) 

### Longest Increasing Subsequence (LIS)

- [Problem Link](https://leetcode.com/problems/longest-increasing-subsequence/)

Up until we have looked at subarrays, subsequences are different that subarray, they follow the order they appear in, but not necessarily contagious

1. Modeling the Problem: We have to find $res = max\{s_i\}$, where $s_i$ : Length of LIS ending at $i$
2. Now to find $s_i$ : Length of LIS ending at $i$, we assume that at any $j$, (where $j < i$) If $A[i] > A[j]$ we can extend the subsequence by 1
3. Recurrence : $S_i = 1 + max_{j \le i} S_j$ and $A[i] > A[j]$
4. Checking DP, Prefix Array with dimension 1, size <- n
5. Base case : `dp[0] = 1`

```python
def lengthOfLIS(nums):
    n = len(nums)
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], 1 + dp[j])

    return max(dp)
```

* Solve Longest Arithmetic Subsequence After this problem

### Word Break

- [Problem Link](https://leetcode.com/problems/word-break/)

All possible splits can be calculated and some will be valid, and some will not be valid. We can have splits at `0, 1, 2, ..., n-1` giving $s_1, s_2, ..., s_n$

given : `catsanddog`, we could split at `[1, 4, 7]` or `[3, 6, 8]` and more...

- Model Problem: $S$ : set of all possible splits
- DnC Criteria: we can mark first split at `0, 1, 2...`, split at some position is i would be $s_i$ , these splits will be mutually exclusive and exhaustive in nature
- We can prune the solution and validate each subproblem as
    - $s_1$ : $A[1...n-1]$ s.t. all words are in dictionary
    - $s_2$ : `A[2 ... n-1]`
    - Suffix Strings
- We should have split s.t. all words `[0 ... i-1]` for $s_i$ are in dictionary
- Representation : $res = OR\{w[0 ..i-1] \in D \text{ \& } S_i\}$
- $S = w_1 | w_2 | w_3 | ...$
- $D = \{w_1, w_2, w_1w_2\}$
- Order to fill : in backwards, for $j < i$

```python
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    n = len(s)

    @cache
    def solve(i):
        if i == n:
            return True
        for j in range(i + 1, n + 1):
            if s[i:j] in word_set and solve(j):
                return True
        return False

    return solve(0)
```

**Tabulation**

```python
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[n] = True

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            if s[i:j] in word_set and dp[j]:
                dp[i] = True
                break

    return dp[0]
```

* Word - Break II 
