# Combinatorics & Permutations

* Note that all problems listed here are enumeration problems requiring the generation of all possible solution combinations. If the problems involved calculating a single value instead of actual solutions, they would become dynamic programming problems. In such cases, optimizations like memoization can reduce complexity.

## Subsets

* NOTE: Subsets don’t have any specific order
* To solve this problems lets divide the solution set using some criteria where both solutions are
    * Disjoint ($c_1 \text{ and } c_2 = \phi$)
    * Universal ($c_1 \text{ or } c_2 = U$)
* we can interpret solution set as : $c_1$ solution that includes first element in the subset, $c_2$ solution that doesn’t include the first element
* Solution for `[2, 3, 5]` becomes
    * $c_1$ : number of subset of `[3, 5]`
    * $c_2$ : any subsets of `[3, 5]` and append `2` to it
* Solution is based on Suffix Array
* Recurrence : `f(arr, 0, n-1) = f(arr, 1, n-1)` $\text{ or }$ `f(arr, 1, n-1) + {arr[0]}`
* Base Case: `f(arr, n-1, n-1) = { {}, {arr[n-1]}}`

Below are two quite interesting approach to above problem.

NOTE: Python never copies objects automatically, 

For lists:

- Function parameters receive a reference to the same list object
- Mutating it (append, pop, clear) affects everyone holding that reference
- Rebinding `(x = [])` does not affect the caller


Using Pythonic Recursion

```python

def subsets(nums):
    res = []

    def dfs(i, contri): # don't use defaults, as they are init during declaration
        # Base case
        if i == len(nums):
            res.append(contri[:])  # copy current subset # very important
            return

        # Exclude nums[i]
        dfs(i + 1, contri)

        # Include nums[i]
        contri.append(nums[i])
        dfs(i + 1, contri)
        contri.pop()  # backtrack
        
        # or use this for include
        # dfs(i + 1, contri + [nums[i]]) # this is copy of the arr being passed

    dfs(0, []) # explicit shared list reference
    return res
```


```python
def subsets(nums):
    res = []

    def dfs(i, contri):
        if i == len(nums):
            res.append(contri)
            return

        dfs(i + 1, contri)
        dfs(i + 1, contri + [nums[i]]) # this is copy of the arr being passed

    dfs(0, [])
    return res
```

Using BitMasks

```python

def subsets(nums):

    n = len(nums)
    
    # for 2 elements : Mask 00, 01, 10, 11
    res = []
    for mask in range(1 << n):
        curr = []
        for j in range(n):
            if mask & (1 << j):
                curr.append(nums[j])
        res.append(curr)

    return res

```

## Combination

Given an array = `[1, 2, 3, 4]` and `k=2`

Solution Set would be : `{[1,2] , [2,3], [3,4], [1,4] , [2,4], [1,3] }`

- Divide : Above problem can be divided into two chunks such that they contain `1` in c_1 and doesn’t contain `1` in c_2
- Represent : Suffix Array
- $c_2$ : all possible `k` sized subsets of `P(A[1...n-1], k)`
- $c_1$ : all possible `k-1` sized subsets of `P(A[l...n-1]) + [A[0]]` (`A[0]` is appended to solution)
- Recursion: `P(A, 0, n-1, k) = P(A, 1, n-1, k) + (P(A, 1, n-1, k-1)..A[0])`
- Base Case
    - `s > e`
        - `k = 0` : `{{}}`
        - `k > 0` : no solution
    - `s <= e`
        - `k = 0` : `{{}}`

```python
def combine(n, k):
    res = []

    def dfs(start, path):
        if len(path) == k:
            res.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            dfs(i + 1, path)
            path.pop()

    dfs(1, [])
    return res
```

* Pruning: `if n - start + 1 < k: return` (not enough elements left to form a combination of size k)

## Combination Sum

Representation : Suffix Array

* Divide
    * $c_1$ : not including first element :
    * $c_2$ : contains atleast one instance of first element
* Subproblems
    * $c_1$ : `P(A, 1, n-1, sum)`
    * $c_2$ : `P(A, 0, n-1, sum - A[0])` , same as original problem with one copy consumed
* Recurrence: `P(A, 0, n-1, sum)  = P(A, 1, n-1, sum) & P(A, 0, n-1, sum - A[0])`
* Base Cases
    * if `A` becomes empty
        * `sum > 0` : `{}`
        * `sum = 0` : `{{}}` | result
        * `sum < 0` : `{}`
    * `sum <= 0`
        * `sum == 0`: `{{}}` | result
        * `sum < 0` : `{}`

```python
def combinationSum(candidates, target):
    res = []

    def dfs(start, path, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # pruning: candidates sorted, rest are larger
            path.append(candidates[i])
            dfs(i, path, remaining - candidates[i])  # i not i+1, reuse allowed
            path.pop()

    candidates.sort()
    dfs(0, [], target)
    return res
```

### Combination Sum - II

[LeetCode Link](https://leetcode.com/problems/combination-sum-ii/description/)

* NOTE: Only change is finite consumption of numbers. So out $c_2$ from previous solution changes as follows.

```python
def combinationSum2(candidates, target):

    candidates.sort()
    res = []
    n = len(candidates)

    def dfs(start, remaining, path):
        if remaining == 0:
            res.append(path[:])
            return

        for i in range(start, n):
            # Skip duplicates at the same recursion depth
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            if candidates[i] > remaining:
                break  # pruning

            path.append(candidates[i])
            dfs(i + 1, remaining - candidates[i], path)
            path.pop()

    dfs(0, target, [])
    return res
```

### Letter Combination of a Phone Number

[Leetcode Link](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

Given string digit from `2-9`, return all possible letter combination that could represent the numbers.

* So for a digit `3`: there could be 3 possibility `d, e, f`
* Problem reduces to precisely same as suffix array.

```python

def letterCombinations(digits):

    mp = {
        "2" : "abc",
        "3" : "def",
        "4" : "ghi",
        "5" : "jkl",
        "6" : "mno",
        "7" : "pqrs",
        "8" : "tuv",
        "9" : "wxyz",
    }
    n = len(digits)
    res = []

    def solve(i, curr):

        if i == n:
            res.append(curr)
            return

        for c in mp[digits[i]]:
            solve(i+1, curr + c)

    
    solve(0, "")
    return res
```

## Permutation

* This is somewhat what represent a `1D` DP. Representation of Solution using Suffix Array usually leads to constraint in 1 dimension.
* Ex - `[1, 2, 3]` Split Criteria : ?
    * `n` chunks of solutions, as
    * begins with 1 `{[1,3,2], [1,2,3]}`
    * begins with 2 `{[2,1,3], [2,3,1]}`
    * begins with 3 `{[3,1,2], [3,2,1]}`
* Subproblem : permutation calculation of the subarray removing that item. These are subsequences not suffix array problem.
* Representation:
    * Keeping a visited array will be helpful to represent the subproblems.
    * Or we can always send the element not to be included to be swapped with  the first element and that way we have a continuous suffix array as a subproblem

#### Keeping visited array

```python
def permute(nums):
    n = len(nums)
    res = []
    visited = [False] * n

    def dfs(path):
        if len(path) == n:
            res.append(path[:])
            return
        for i in range(n):
            if not visited[i]:
                visited[i] = True
                path.append(nums[i])
                dfs(path)
                path.pop()
                visited[i] = False

    dfs([])
    return res
```

#### Swapping based solution (creates explicit suffix array)

Swap in place - no need for a separate `curr` array

```python
def permutations(arr):
    n = len(arr)
    res = []

    def solve(i):
        if i == n:
            res.append(arr[:]) # copy and append
            return

        for j in range(i, n):
            arr[i], arr[j] = arr[j], arr[i]
            solve(i + 1)
            arr[i], arr[j] = arr[j], arr[i]

    solve(0)
    return res
```

### Permutation Sequence

[k-th Permutation Sequence](https://leetcode.com/problems/permutation-sequence/description/)

* Naively Listing all permutations and then finding `kth` will give TLE in this case.
* We will perform DFS, and try to search that solution
* Ex - `[1, 2, 3]`
* Possibilities = `(123, 132, 213, 231, 312, 321)` and we have to give `kth` solution.
* There are 3 chunks, chunks including 1, 2, 3 as first number respectively
* now say its a ordered list, then we can easily say chunk size and the chunk in which this `k-th` number will lie would be

$$
\text{chunk id} = \frac{k-1}{(n-1)!}
$$

* then calculate offset how far this item is away from that `chunk_id`
* hmmm can we do that recursively ! yes :D

```python
from math import factorial

def getPermutation(n, k):
    digits = list(range(1, n + 1))
    res = ""
    k -= 1  # convert to 0-indexed

    while digits:
        f = factorial(len(digits) - 1)
        chunk_id = k // f
        res += str(digits[chunk_id])
        digits.pop(chunk_id)
        k %= f

    return res
```

