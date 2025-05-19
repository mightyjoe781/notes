# Bitmask DP

Bitmask DP is useful when the state of a problem involves subsets (e.g. selected elements, visited nodes). Since subsets of n elements can be represented using integers from 0 to 2ⁿ - 1, we can model states with bitmasks.

## Subset Generation

To iterate over **all subsets** of a set of size n:

````c++
for (int mask = 0; mask < (1 << n); ++mask) {
    // mask represents a subset
    for (int i = 0; i < n; ++i) {
        if (mask & (1 << i)) {
            // i-th element is in the subset
        }
    }
}
````

To iterate over all subset of a specific mask

````c++
int mask = ...;
for (int sub = mask; sub; sub = (sub - 1) & mask) {
    // sub is a subset of mask
}
````

Very useful in optimization problems with subsets (e.g., TSP, Set Cover).

## Bitmask DP Template

````c++
int dp[1 << N]; // Stores answers for all subsets

for (int mask = 0; mask < (1 << N); ++mask) {
    for (int i = 0; i < N; ++i) {
        if ((mask >> i) & 1) continue; // skip if i already in mask
        int newMask = mask | (1 << i);
        dp[newMask] = min(dp[newMask], dp[mask] + cost[mask][i]); // Update based on problem
    }
}
````

## Example Problems

### Traveling Salesman Problem (TSP)

- Problem: Find the minimum cost path that visits every city once and returns to the origin.
- State:
  - mask = cities visited so far
  - i = current city
- Recurrence: `dp[mask][i] = min(dp[mask][i], dp[mask ^ (1 << i)][j] + dist[j][i]) // for all j ≠ i`
- Base case: `dp[1 << i][i] = cost from 0 to i`

### Count Number of Ways to Partition into K Subsets

- Problem: Partition a set of n elements into exactly k non-empty subsets
- Use Bell numbers or bitmask DP with memoization over (mask, k) where:
  - mask = unpicked elements
  - k = subsets left

### Minimum Incompatibility

- [Problem Link](https://leetcode.com/problems/minimum-incompatibility/)
- Need to partition array into k subsets of size n / k, minimizing incompatibility (max - min of each subset)
- Precompute all valid subsets of size n/k and their incompatibility
- Use Bitmask DP:
  - dp[mask] = min incompatibility for subset mask
  - Transition: combine valid group with remaining mask

### Max AND Sum of Array

- [Problem Link](https://leetcode.com/problems/maximum-and-sum-of-array/)
- You are given a list of nums and you have k slots, each can take up to 2 numbers.
- Use Bitmask DP:
  - State: mask of which numbers used
  - Value: max AND sum you can get
  - Transition: try placing a number in each slot (0..k-1) with 2 capacity

## Bitmask Utility Tricks

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

| **Problem**                                                  | **Key Idea**                         |
| ------------------------------------------------------------ | ------------------------------------ |
| [Leetcode 847 - Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | Bitmask BFS on visited nodes         |
| [Leetcode 1349 - Maximum Students Taking Exam](https://leetcode.com/problems/maximum-students-taking-exam/) | Bitmask DP with row states           |
| [Leetcode 1659 - Maximize Grid Happiness](https://leetcode.com/problems/maximize-grid-happiness/) | DP + Bitmask Compression             |
| [AtCoder DP Contest - Problem O “Matching”](https://atcoder.jp/contests/dp/tasks/dp_o) | Count perfect matchings with bitmask |
| [Leetcode 689 - Maximum Sum of 3 Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/) | Sliding window + bitmask dp          |