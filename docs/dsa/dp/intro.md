# Dynamic Programming

Key skill to master DP is ability to determine the problem *states* and to determine the relationship or *transitions* between current problems and their sub-problems.

Identify problems related to Dynamic Programming by determining whether the problem can be solved by counting solutions rather than enumeration or involve Optimization. Often, pruning is necessary to obtain the answer within time limits.

If the problem cannot be solved using another technique, dynamic programming must be applied. Only when problem is still hard due to enumeration, DP fails and methods like MITM come saving.

### Types of DP Problems

| **Type**               | **Dimension** | **Core Idea / State**                 | **Common Examples**                          | **Techniques**                        |
| ---------------------- | ------------- | ------------------------------------- | -------------------------------------------- | ------------------------------------- |
| **1D DP**              | 1             | Linear state (i)                      | Fibonacci, Climbing Stairs, House Robber     | Simple recurrence, prefix/suffix      |
| **2D DP**              | 2             | Two indices (i, j)                    | LCS, Edit Distance, 0/1 Knapsack             | Nested loops, memo/table              |
| **Grid DP**            | 2 (grid)      | Grid position (i, j) with movement    | Unique Paths, Min Path Sum                   | Directional traversal (right/down)    |
| **Subset DP**          | 2             | Subsets + indices                     | Subset Sum, Target Sum, Count Subsets        | Choose/Skip, Include/Exclude          |
| **Unbounded Knapsack** | 2             | Repeat items, unlimited use           | Coin Change (ways/least), Rod Cutting        | Iterate items, inner loop on total    |
| **Bounded Knapsack**   | 2             | Use each item once                    | 0/1 Knapsack, Equal Partition                | Reverse loops to avoid reuse          |
| **Bitmask DP**         | ≥2            | Set of visited items (mask, pos)      | TSP, Count Valid Words, Assignment Problem   | Bitmasking, memoization               |
| **Tree DP**            | Varies        | DP on tree nodes, subtree aggregation | Tree Diameter, Max Weight Independent Set    | DFS, post-order, rerooting            |
| **Interval DP**        | 2             | Range-based (i to j)                  | Matrix Chain Multiplication, Burst Balloons  | Nested intervals, greedy partition    |
| **Palindrome DP**      | 2             | String substrings                     | Longest Palindromic Subseq, Min Cuts for Pal | Expand from center / DP on substrings |
| **Digit DP**           | Varies        | Positional digits with constraints    | Count ≤ N with X digits, Sum of digits       | pos, tight, leading_zero, memo        |
| **Game DP / Minimax**  | 2+            | Optimal moves between players         | Stone Game, Predict Winner, Nim Game         | Minimax, turn-based state             |
| **Memoization**        | Any           | Recursion + Caching                   | Decode Ways, Unique Paths, Partition Memo    | Top-down recursion + unordered_map    |
| **Tabulation**         | Any           | Bottom-up DP table                    | Most DP problems (as iterative solutions)    | Fill from base cases up               |
