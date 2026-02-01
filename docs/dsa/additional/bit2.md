# Bitmask DP

Bitmask DP is useful when the state of a problem involves subsets (e.g. selected elements, visited nodes). Since subsets of n elements can be represented using integers from 0 to 2ⁿ - 1, we can model states with bitmasks.

## Subset Generation

To iterate over **all subsets** of a set of size n:

````python

for mask in range(1 << n):
# for mask in range(1 << n - 1, -1, -1): # use: to avoid reverse order,
    # mask represents a subset
    for j in range(n):
        # check set bits in mask (in reverse)
        if mask & (1 << j):
            # j-th element is in the subset

````

Example -

```
arr = [1, 2, 3]
masks = [000, 001, 010, 011, 100, 101, 110, 111]
subset = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]
```

To iterate over all subset of a specific mask

````python

arr = ["a", "b", "c", "d"]
n = len(arr)

# notice its reverse mask, side effect of using 1 << j
mask = int("1101", 2)   # {a, c, d}
sub = mask

while sub:
    subset = []

    for j in range(n):
        if sub & (1 << j):
            subset.append(arr[j])

    print(subset)
    sub = (sub - 1) & mask
        
````

Example -

```
arr = [a, b, c, d]
mask = [1101] ~ [a, c, d] # NOTICE its reverse,
submask of given mask = [1011, 1010, 1001, 1000, 0011, 0010, 0001, 0000]
all submask ~ [[a, c, d], [a, c], [a, d], [a], [c, d], [c], [d], []]

```


Very useful in optimization problems with subsets (e.g., TSP, Set Cover).

## Bitmask DP Template

````python
INF = float('inf')

dp = [INF] * (1 << N)
dp[0] = 0  # base case

for mask in range(1 << N):
    for i in range(N):
        if mask & (1 << i):
            continue  # i already chosen

        new_mask = mask | (1 << i)
        dp[new_mask] = min(
            dp[new_mask],
            dp[mask] + cost[mask][i]
        )
````

## Example Problems

### Traveling Salesman Problem (TSP)

- Problem: Find the minimum cost path that visits every city once and returns to the origin.

![](assets/Pasted%20image%2020260201153708.png)

- There could be many *Hamiltonian Path* in a graph, basically paths which travel each node. We want to find the min. cost Hamiltonian Path
- NOTE: *TSP* is a *NP* Hard Problem, for large ($n > 32$) problem cannot be solved using BitMask DP within time limits.
- A naive solution is to try every such path, time complexity would be $O(n!)$ but BitMask DP solves it in $O(n^2 \times 2^n)$  time.
- Try to prove mathematically, BitMask DP is better solution of TSP that naively trying all combination.

![](assets/Pasted%20image%2020260201154649.png)


- State:
    - mask = cities visited so far
    - i = current city
- Recurrence: `dp[mask][i] = min(dp[mask][i], dp[mask ^ (1 << i)][j] + dist[j][i]) // for all j != i`
- Base case: `dp[1 << i][i] = cost from 0 to i`
- Space Complexity : $O(n \times 2^n)$


````c++
n = 4
INF = float('inf')
dp = [[INF] * n for _ in range(1 << n)]
dp[1][0] = 0  # Start at city 0

for mask in range(1 << n):
    for u in range(n):
        # u is not present in mask
        if not (mask & (1 << u)):
            continue
        
        for v in range(n):
            # v is already visited
            if mask & (1 << v):
                continue
            
            # relax edges from u-v
            new_mask = mask | (1 << v)
            dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + cost[u][v])

# Final answer: return to city 0
res = INF
for u in range(1, n):
    res = min(res, dp[(1 << n) - 1][u] + cost[u][0])

print(res)
````

### Shortest Path Visiting All Nodes

Now try to solve [Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)

You have an undirected, connected graph of `n` nodes labeled from `0` to `n - 1`. You are given an array `graph` where `graph[i]` is a list of all the nodes connected with node `i` by an edge.

Return _the length of the shortest path that visits every node_. You may start and stop at any node, you may revisit nodes multiple times, and you may reuse edges.

Above problem is not TSP!!!

Conditions for TSP Problem

- Complete Graph
- Known Cost Between Every Pair of cities
- Want **minimum Hamiltonian cycle**
- Must return to Start

Now in above question :

- Graph is not Complete
- You don't need to return to start
- Cost is always +1 per edge, 
- You can move along edges only !

Solving it using multi-source BFS, but not TSP !!!! but using BitMasking DP

NOTE: !! why can't we just start multi-source BFS normally without using BitMasks ? We could if problem asked *shortest path to reach a node* but here questions asks *shortest path to reach all nodes*

We could have used, *(node, visited_set)* and a normal BFS but BitMask is optimal choice for implemented visited_set and efficiently handles state transitions.


```python

def shortestPathLength(graph: List[List[int]]) -> int:

    n = len(graph)
    full_mask = (1 << n) - 1

    # dist[mask][u] = shortest steps to reach state (mask, u)
    dist = [[float('inf')] * n for _ in range(1 << n)]
    q = deque()

    # start from every node
    for i in range(n):
        # mask : [001, 010, 100] ~ n = 3
        mask = 1 << i
        dist[mask][i] = 0
        q.append((mask, i))

    while q:
        mask, u = q.popleft()
        d = dist[mask][u]

        if mask == full_mask: # all nodes are visited
            return d

        for v in graph[u]:
            new_mask = mask | (1 << v)
            if dist[new_mask][v] > d + 1:
                # relax the v edge !!
                dist[new_mask][v] = d + 1
                q.append((new_mask, v))

    return -1

```


### Count Number of Ways to Partition into K Subsets

Hint :

- Problem: Partition a set of n elements into exactly k non-empty subsets
- Use Bell numbers or bitmask DP with memoization over (mask, k) where:
    - mask = unpicked elements
    - k = subsets left

The number of ways to partition a set of $n$ elements into $k$ non-empty subsets is given by the Stirling numbers of the second kind.

$$
S(n, k) = k \cdot S(n-1, k) + S(n-1, k-1)
$$

Logic is Simple either $n^{th}$ element joins the existing subset, or forms a new subset, reducing $k$ in second term.

Base Cases

- $S(n, n)$ = 1
- $S(n, 1) = 1$
- $S(n, 0) = 0$ if $n > 0$


Bell Numbers : The total number of ways to partition $n$ elements into any number of non-empty subsets is the sum of Stirling numbers

$$
B(n) = \Sigma_{i=1}^{n} S(n, i)
$$

```python

def stirling(n, k):
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    dp[0][0] = 1

    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]

    return dp[n][k]

def bell_number(n):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1

    for i in range(1, n + 1):
        for j in range(1, i + 1):
            dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]

    return sum(dp[n][1:])

```

Using Bit Mask DP

Since we already found optimal Solution why do we even need BitMask DP ? Above question didn't ask the configurations, what if I want the *subsets compositions* or other *constraints* are imposed on problem, or *elements are not identical*

- Mask ~ elements already placed
- k ~ subsets remaining
- NOTE: Time Complexity is : $O(3^n)$

```
dp(mask, k) = number of ways to partition elements in `mask`
              into exactly `k` non-empty subsets
```


```python

from functools import lru_cache

def count_partitions(n, K):
    FULL = (1 << n) - 1

    @lru_cache(None)
    def dp(mask, k):
        # base cases
        if mask == 0 and k == 0:
            return 1
        if mask == 0 or k == 0:
            return 0

        # pick smallest element
        p = mask & -mask
        rest = mask ^ p

        ans = 0
        sub = rest
        while True:
            subset = p | sub
            remaining = mask ^ subset
            ans += dp(remaining, k - 1)

            if sub == 0:
                break
            sub = (sub - 1) & rest

        return ans

    return dp(FULL, K)

```


### Minimum Incompatibility

- [Problem Link](https://leetcode.com/problems/minimum-incompatibility/)
- Need to partition array into k subsets of size n / k, minimizing incompatibility (max - min of each subset)
- Precompute all valid subsets of size n/k and their incompatibility
- Use Bitmask DP:
    - `dp[mask]` = min incompatibility for subset mask
    - Transition: combine valid group with remaining mask

Problem Statement : You are given an integer array `nums`​​​ and an integer `k`. You are asked to distribute this array into `k` subsets of **equal size** such that there are no two equal elements in the same subset.

A subset's **incompatibility** is the difference between the maximum and minimum elements in that array.

Return _the **minimum possible sum of incompatibilities** of the_ `k` _subsets after distributing the array optimally, or return_ `-1` _if it is not possible._

Each subset will be of size $m = n//k$. If any appears more than $k$ times, answer would be -1. Using Pigeonhole principle.

Order inside that subset doesn't matter, Subsets are unlabelled so avoid permutation,

Strategy

Step 1

- Precompute all valid subsets
    - A valid subset is of size $m$
    - all elements are distinct
    - compute its incompatibility = max - min

```
valid[mask] = incompatibility
```

Step 2 

```
dp[mask] = min. incompatibility to cover elements in `mask`
```

- DP Transition to avoid overcounting, 
- Always pick the first unused element p
- Only Consider subsets that
    - include p
    - are disjoin from *mask*

```
dp[mask | subset] = min(dp[mask | subset], dp[mask] + valid[subset])
```

This enforces *canonical ordering*


```python

def minimumIncompatibility(nums: List[int], k: int) -> int:
    n = len(nums)
    m = n // k
    FULL = (1 << n) - 1
    INF = float('inf')

    # Frequency check, pigeonhole principle
    cnt = Counter(nums)
    if any(v > k for v in cnt.values()):
        return -1

    # Precompute valid subsets
    valid = {}
    for mask in range(1 << n):
        if bin(mask).count('1') != m:
            continue

        seen = set()
        mn, mx = float('inf'), float('-inf')
        ok = True

        for i in range(n):
            if mask & (1 << i):
                if nums[i] in seen:
                    ok = False
                    break
                seen.add(nums[i])
                mn = min(mn, nums[i])
                mx = max(mx, nums[i])

        if ok:
            valid[mask] = mx - mn

    # DP
    dp = [INF] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        if dp[mask] == INF:
            continue

        # find first unused element
        for i in range(n):
            if not (mask & (1 << i)):
                first = i
                break

        for sub, cost in valid.items():
            if (sub & (1 << first)) == 0:
                continue
            if (mask & sub) != 0:
                continue

            new_mask = mask | sub
            dp[new_mask] = min(dp[new_mask], dp[mask] + cost)

    return dp[FULL] if dp[FULL] != INF else -1

```

Fixing the first unused element prevents:

```
[A,B] + [C,D]
[C,D] + [A,B]
```

Space Complexity : $O(2^n \cdot n)$
Time Complexity : $O(2^n \cdot \text{number of valid subsets}) \approx O(3^n)$

This is manageable under $n \le 16$
### Max AND Sum of Array

- [Problem Link](https://leetcode.com/problems/maximum-and-sum-of-array/)
- You are given a list of nums and you have k slots, each can take up to 2 numbers.
- Use Bitmask DP:
    - State: mask of which numbers used
    - Value: max AND sum you can get
    - Transition: try placing a number in each slot (0..k-1) with 2 capacity

You are given an integer array `nums` of length `n` and an integer `numSlots` such that `2 * numSlots >= n`. There are `numSlots` slots numbered from `1` to `numSlots`.

You have to place all `n` integers into the slots such that each slot contains at **most** two numbers. The **AND sum** of a given placement is the sum of the **bitwise** `AND` of every number with its respective slot number.

- For example, the **AND sum** of placing the numbers `[1, 3]` into slot `1` and `[4, 6]` into slot `2` is equal to `(1 AND 1) + (3 AND 1) + (4 AND 2) + (6 AND 2) = 1 + 1 + 0 + 2 = 4`.

Return _the maximum possible **AND sum** of_ `nums` _given_ `numSlots` _slots._

Core Trick : Instead of tracking slots directly, we track how many numbers have been placed.

Why this works ?

- If `cnt = number of bits set in mask`
- Then the next number will go into

```
slot = cnt // 2 + 1
```

Because

- Slot 1 takes indices 0, 1
- Slot 2 takes indices 2, 3
- Slot 3 takes indices 4, 5


DP State

```
dp[mask] = maximum AND sum using numbers represented by mask

  mask is over indices of nums
  mask size = 2 ^ n
  Final Answer = dp[(1 << n)-1]

```


```python

def maximumANDSum(nums, numSlots):
    n = len(nums)
    N = 1 << n

    dp = [0] * N

    for mask in range(N):
        cnt = bin(mask).count("1")
        slot = cnt // 2 + 1
        if slot > numSlots:
            continue

        for i in range(n):
            if not (mask & (1 << i)):
                new_mask = mask | (1 << i)
                dp[new_mask] = max(
                    dp[new_mask],
                    dp[mask] + (nums[i] & slot)
                )

    return dp[N - 1]

```

- Here each mask represents a partial assignment
- Slot is uniquely determined by how many numbers are already placed
- Capacity is enforced implicitly (2 per slot)
- Order doesn’t matter - DP explores all valid assignments


- Time : $O(n \cdot 2^n)$
- Space : $O(2 ^ n)$

Works fine for $n \le 14$

### Maximum Students Taking Exam

Given a `m * n` matrix `seats`  that represent seats distributions in a classroom. If a seat is broken, it is denoted by `'#'` character otherwise it is denoted by a `'.'` character.

Students can see the answers of those sitting next to the left, right, upper left and upper right, but he cannot see the answers of the student sitting directly in front or behind him. Return the **maximum** number of students that can take the exam together without any cheating being possible.

Students must be placed in seats in good condition.


```
Input: seats = [["#",".","#","#",".","#"],
                [".","#","#","#","#","."],
                ["#",".","#","#",".","#"]]
Output: 4
Explanation: Teacher can place 4 students in available seats so they don't cheat on the exam. 
```

Idea : Model who can see whom and convert it into bitmask compatibility checks.

Approach

- Convert Each row into a bitmask
- Enumerate valid seating states for one row
    - Students can sit on usable seats : `state & row_mask == state`
    - No left/right cheating in same row : `(state & (state << 1)) == 0`
- DP Definition

```
dp[row][state] = max students up to this row if current row uses `state`

```


```python

def maxStudents(seats):
    m, n = len(seats), len(seats[0])

    row_masks = []
    for row in seats:
        mask = 0
        for j in range(n):
            if row[j] == '.':
                mask |= (1 << j)
        row_masks.append(mask)

    valid_states = []
    for mask in range(1 << n):
        if (mask & (mask << 1)) == 0:
            valid_states.append(mask)

    dp = [{} for _ in range(m)]

    for state in valid_states:
        if (state & row_masks[0]) == state:
            dp[0][state] = bin(state).count("1")

    for i in range(1, m):
        for curr in valid_states:
            if (curr & row_masks[i]) != curr:
                continue
            for prev in dp[i - 1]:
            # upper-left conflict and upper right conflict
                if (curr & (prev << 1)) == 0 and (curr & (prev >> 1)) == 0:
                    dp[i][curr] = max(
                        dp[i].get(curr, 0),
                        dp[i - 1][prev] + bin(curr).count("1")
                    )

    # max(dp[last_row][state] for state in all_valid_states)
    return max(dp[m - 1].values(), default=0)

```

## BitMask Utility Tricks

- Set/Unset/Toggle Bit

````c++
mask | (1 << i)    // set i-th bit
mask & ~(1 << i)   // unset i-th bit
mask ^ (1 << i)    // toggle i-th bit
````

- Count Set Bits

````c++
__builtin_popcount(mask)    // Count 1's in binary (GCC/Clang)
````

- Iterate Subsets of a Mask

````c++
for (int sub = mask; sub; sub = (sub - 1) & mask)
````

## Common Scenarios to Use Bitmask DP

- Permutation with cost (e.g., assignment, TSP)
- Subset selection with constraints (e.g., compatibility, minimal sum)
- Dynamic Programming on graph states (e.g., Hamiltonian path)
- Partitioning problems where sets are mutually exclusive

### Practice Problems

| **Problem**                                                                                                                            | **Key Idea**                         |
| -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| [Leetcode 847 - Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)                     | Bitmask BFS on visited nodes         |
| [Leetcode 1349 - Maximum Students Taking Exam](https://leetcode.com/problems/maximum-students-taking-exam/)                            | Bitmask DP with row states           |
| [Leetcode 1659 - Maximize Grid Happiness](https://leetcode.com/problems/maximize-grid-happiness/)                                      | DP + Bitmask Compression             |
| [AtCoder DP Contest - Problem O “Matching”](https://atcoder.jp/contests/dp/tasks/dp_o)                                                 | Count perfect matchings with bitmask |
| [Leetcode 689 - Maximum Sum of 3 Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/) | Sliding window + bitmask dp          |
