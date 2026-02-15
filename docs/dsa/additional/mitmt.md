# Meet-in-the-Middle Technique

- Meet in the Middle is a divide-and-conquer technique, used to reduce complexity of exponential search problems
- Typically when n < 40, where brute force is $O(2^n)$ but we can reduce it by $O(2^{\frac{n}{2}})$
- Especially useful in subset problems, Knapsack, XOR-sum
- We split the input into two halves, solving independently, and combining results
- When to Apply MITM ?
    - While dealing with subset or permutation problems where n is too large for brute force
    - There is **no polynomial-time algorithm**, but a smarter brute-force can be done
    - Splitting data leads to **independent subproblems**

- Steps
    - Split the problem in two halves
    - Enumerate all solution for both halves
    - Combine both using binary search, hashing or two-pointer techniques

A classic example of MITM is solving a 3x3 Rubik's Cube. It can be solved in at least 20 moves (https://cube20.org/)

Simulating the solution for searching for solution is just finding the shortest distance between both the configuration as shown.

![](assets/Pasted%20image%2020260215005428.png)

In worst our algorithm might take 4 quintillion moves to solve the rubik's cube, $\approx 10^{20}$ states

A regular computer can explore about $10^6$ states/seconds. This would take $\approx 10 ^{14} s \approx 3 \cdot 10 ^ 6 \text{years}$. We could try to solve from both direction and combine the results in about $\approx 10^{10} \text{moves}$

This obviously trades off speed for storage.

![](assets/Pasted%20image%2020260215005909.png)

Reference Video : [Polylog Video](https://www.youtube.com/watch?v=wL3uWO-KLUE)
## Subset Sum Problem

- given $n \le40$ elements and target sum $S$
- Naive approach of enumeration $2^n$ is too slow
- MITM
    - split into two halves A and B
    - Generate subset sums of both halves : sumA , sumB
    - for each sum in sumA, check if `target-sum` exists in sumB (using binary_search or hashing)
- Time : $O(2^{\frac{n}{2}}) * \log(2^{\frac{n}{2}})$

````python
from bisect import bisect_left

def subset_sum(arr, target):
    n = len(arr)
    half = n // 2
    A, B = arr[:half], arr[half:]

    def get_sums(sub):
        sums = []
        for i in range(1 << len(sub)):
            s = 0
            for j in range(len(sub)):
                if i & (1 << j):
                    s += sub[j]
            sums.append(s)
        return sums

    sa = get_sums(A)
    sb = get_sums(B)
    sb.sort()

    for x in sa:
        if bisect_left(sb, target - x) < len(sb) and sb[bisect_left(sb, target - x)] == target - x:
            return True
    return False
````

## Equal Sum Partition

* Given an array `arr`, determine if it can be partitioned into two subsets with equal sum
* MITM
    * total sum must be even
    * split array into two halves
    * Generate all subset sums for each half
    * Use hashing/binary search to check if any combination sums to `total_sum//2`

````python
def can_partition(arr):
    total = sum(arr)
    if total % 2 != 0:
        return False
    target = total // 2

    n = len(arr)
    half = n // 2
    A = arr[:half]
    B = arr[half:]

    def gen_sums(nums):
        sums = []
        for i in range(1 << len(nums)):
            s = 0
            for j in range(len(nums)):
                if i & (1 << j):
                    s += nums[j]
            sums.append(s)
        return sums

    sumA = gen_sums(A)
    sumB = gen_sums(B)
    setB = set(sumB)

    for sa in sumA:
        if (target - sa) in setB:
            return True
    return False
````

## XOR-based problems (split approach)

- MITM works well for XOR Problems where DP or naive recursion is too slow
- Problem: Count number of subsets where XOR = target
- Steps
    - Split Array
    - Generate all XORs of subsets in both halves
    - Count how many `a xor b == target` using hashmap for one side

````python
from collections import Counter

def count_subsets_xor(arr, target):
    def gen_xors(nums):
        res = []
        for i in range(1 << len(nums)):
            xor = 0
            for j in range(len(nums)):
                if i & (1 << j):
                    xor ^= nums[j]
            res.append(xor)
        return res

    half = len(arr) // 2
    A, B = arr[:half], arr[half:]
    xorsA = gen_xors(A)
    xorsB = gen_xors(B)
    counterB = Counter(xorsB)

    count = 0
    for xa in xorsA:
        count += counterB[xa ^ target]
    return count
````

## 0-1 Knapsack

- Given n items (where n is large) each with a weight `w[i]` and value `v[i]`, and a total capacity `W`, find the max total value we can obtain without exceeding the weight `W`
- Standard DP : $O(n*W)$, which could be quite large when either W or `n` is large
- MITM Steps
    - Split into two halves A and B
    - Generate all subsets of each half with
        - total weight `w`
        - total value `v`
    - For one half, **prune dominated pairs**  (where a subset has both higher weight and lower value)
    - For each subset in one half, find best possible complement in other (with total weight <= W) using binary search

````python
from bisect import bisect_right

def knapsack_mitm(weights, values, max_weight):
    n = len(weights)
    half = n // 2
    A = list(zip(weights[:half], values[:half]))
    B = list(zip(weights[half:], values[half:]))

    def generate_subsets(items):
        subsets = []
        for i in range(1 << len(items)):
            tw = tv = 0
            for j in range(len(items)):
                if i & (1 << j):
                    tw += items[j][0]
                    tv += items[j][1]
            if tw <= max_weight:
                subsets.append((tw, tv))
        return subsets

    sa = generate_subsets(A)
    sb = generate_subsets(B)

    # Prune dominated pairs in sb
    sb.sort()
    pruned_sb = []
    max_val = -1
    for w, v in sb:
        if v > max_val:
            pruned_sb.append((w, v))
            max_val = v

    sb_weights = [w for w, v in pruned_sb]
    sb_values = [v for w, v in pruned_sb]

    ans = 0
    for wa, va in sa:
        remaining = max_weight - wa
        idx = bisect_right(sb_weights, remaining) - 1
        if idx >= 0:
            ans = max(ans, va + sb_values[idx])

    return ans
````

## Double Binary Search

Double Binary Search is used when the **search space is 2D**, or when we must binary search on **both the answer** and **some parameter/condition** inside a decision function. It’s common in optimization problems where:

- The answer isn’t directly numeric, but depends on a function.
- You need to search in a matrix-like domain.

Classical Problems

* Minimum Maximum Distance : Given n points, place k stations such that the **maximum distance** from any point to a station is minimized. 
    * Involves two Binary Search, one of the distance `D`
    * for each `D`, binary search or greedy check if `k` police station can be placed
* Binary Search in Sorted Matrix : Binary Search in two dimensions, could be reduced to one dimension
* Aggressive Cows/Router Placement

## A* Optimization Variant

A* Search is an optimization over Dijkstra’s Algorithm using **heuristics** to guide search. It is used to **speed up shortest-path search** (like in pathfinding).

- `f(n) = g(n) + h(n)`
    - `g(n)` = cost from start to node `n`
    - `h(n)` = estimated cost from node n to goal (heuristic)
    - A* selects the node with smallest `f(n)`

- When using MITM in **graph traversal** or **state space search**, especially when both forward and backward searches are possible, **bidirectional A\*** is a powerful optimization.

- You can simulate A* from both **start and goal** simultaneously, and **meet in the middle**.

````python
# template code
# Pseudocode sketch
A_star_forward(start, goal)
A_star_backward(goal, start)

# Combine states where forward and backward searches meet
for state in visited_forward:
    if state in visited_backward:
        update answer with g1(state) + g2(state)
````

- This helps **cut the search space from exponential to square root** of total size — classic MITM optimization.