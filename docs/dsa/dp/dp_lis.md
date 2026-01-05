# DP on LIS


LIS refers to Longest Increasing Subsequence, This special problem type is covered in detail here because it sets up a larger pattern where we keep track of previous states.

Problem Link - 300 : [Link](https://leetcode.com/problems/longest-increasing-subsequence/)

```python

def lis(arr):
    n = len(arr)

    @cache
    def solve(i, prev):
        if i == n:
            return 0

        # option 1: skip current element
        res = solve(i + 1, prev)

        # option 2: take current element (if valid)
        if prev == -1 or arr[i] > arr[prev]:
            res = max(res, 1 + solve(i + 1, i))

        return res

    return solve(0, -1)
```


But above solution may not work correctly and give MLE due to State Explosion and $O(n^2)$ complexity. But if you notice the recurrence, we can compress states saving us MLE problem.

```python

def lengthOfLIS(nums):
    n = len(nums)
    dp = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
```

There is an optimized solution for LIS which uses $O(n \log n)$ complexity, its based on tracking the current sequence.

Principle :  `tails[k] = smallest possible tail of an increasing subsequence of length k+1`

```python
from bisect import bisect_left
def lengthOfLIS(nums):
    tails = []

    for num in nums:
        idx = bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num

    return len(tails)
```


Pattern to notice here is that: At this stage, the solution is no longer reducible to a simple start–end DP state. Instead, it requires evaluating and maximizing over several concurrent propagation states.


## Largest Divisible Subset

Here core problem is similar to longest increasing subset, but sorting the `nums` helps in the order we solve the problem

If `nums[i] % nums[j] == 0` and $j < i$, then `nums[j]` can come before` nums[i]`
Exactly like `nums[j] < nums[i]` in LIS.

```python

def largestDivisibleSubset(nums):
    nums.sort()
    n = len(nums)

    @cache
    def solve(i, prev):
        if i == n:
            return 0

        # option 1: skip
        res = solve(i + 1, prev)

        # option 2: take (if divisible)
        if prev == -1 or nums[i] % nums[prev] == 0:
            res = max(res, 1 + solve(i + 1, i))

        return res


    ans = []
    i, prev = 0, -1

    while i < n:
        # if taking nums[i] gives optimal answer, take it
        if (prev == -1 or nums[i] % nums[prev] == 0) and \
           1 + solve(i + 1, i) >= solve(i + 1, prev):
            ans.append(nums[i])
            prev = i
        i += 1

    return ans
```

Bottom Up Version

```python

def largestDivisibleSubset(nums):
    nums.sort()
    n = len(nums)
    dp = [1] * n
    parent = [-1] * n

    max_idx = 0
    for i in range(n):
        for j in range(i):
            if nums[i] % nums[j] == 0 and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
        if dp[i] > dp[max_idx]:
            max_idx = i

    res = []
    while max_idx != -1:
        res.append(nums[max_idx])
        max_idx = parent[max_idx]

    return res[::-1]
```

NOTE: LIS has an $O(n \log n)$ solution because “increasing” induces a total order that supports binary search; divisibility does not.

## Largest String Chain

Problem Link - 1048 : [Link](https://leetcode.com/problems/longest-string-chain/description/)

You are given words. A word A can come before word B if: B can be formed by inserting exactly one character into A.
Find the longest possible chain

`words.sort(key=len)` : This helps induce order of processing.

Maximum chain length starting from index i, given that the last chosen word index is prev.

```python
def longestStrChain(words):
    words.sort(key=len)
    n = len(words)

    def is_pred(a, b):
        if len(b) != len(a) + 1:
            return False
        i = j = 0
        mismatch = 0
        while i < len(a) and j < len(b):
            if a[i] == b[j]:
                i += 1
            else:
                mismatch += 1
                if mismatch > 1:
                    return False
            j += 1
        return True

    @cache
    def solve(i, prev):
        if i == n:
            return 0

        # skip current word
        res = solve(i + 1, prev)

        # take current word if valid
        if prev == -1 or is_pred(words[prev], words[i]):
            res = max(res, 1 + solve(i + 1, i))

        return res

    return solve(0, -1)
```


Bottom Up Version

```python
def longestStrChain(self, words):
    words.sort(key=len)
    dp = {}

    for w in words:
        dp[w] = 1
        for i in range(len(w)):
            prev = w[:i] + w[i+1:]
            if prev in dp:
                dp[w] = max(dp[w], dp[prev] + 1)

    return max(dp.values())
```


## Longest Biotonic Subsequence

What is Biotonic Subsequence : strictly increases → reaches a peak → strictly decreases
`A bitonic subsequence is just: LIS ending at i + LDS starting at i − 1`

```python

def longestBitonicSubsequence(nums):
    n = len(nums)

    inc = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                inc[i] = max(inc[i], inc[j] + 1)

    dec = [1] * n
    for i in range(n-1, -1, -1):
        for j in range(n-1, i, -1):
            if nums[j] < nums[i]:
                dec[i] = max(dec[i], dec[j] + 1)

    ans = 0
    for i in range(n):
        ans = max(ans, inc[i] + dec[i] - 1)

    return ans
```

## Number of LIS

```python
def findNumberOfLIS(self, nums):
    n = len(nums)
    dp = [1] * n
    cnt = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    cnt[i] = cnt[j]
                elif dp[j] + 1 == dp[i]:
                    cnt[i] += cnt[j]

    longest = max(dp)
    return sum(cnt[i] for i in range(n) if dp[i] == longest)
```