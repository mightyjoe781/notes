# Dynamic Programming

Key skill to master DP is ability to determine the problem *states* and to determine the relationship or *transitions* between current problems and their sub-problems.

Identify problems related to Dynamic Programming by determining whether the problem can be solved by counting solutions rather than enumeration or involve Optimization. Often, pruning is necessary to obtain the answer within time limits.

If the problem cannot be solved using another technique, dynamic programming must be applied. Only when problem is still hard due to enumeration, DP fails and methods like MITM come saving.

## How to Approach a DP Problem

Follow these steps every time. The bottleneck is always step 2 - everything else is mechanical once the state is clear.

**Step 1 - Verify DP applies**
Does the problem ask for a count, max/min, or yes/no over a combinatorial space? Can the problem be broken into overlapping sub-problems? If yes, DP likely applies.

**Step 2 - Define the state**
Ask: *"What information do I need to fully describe a sub-problem?"*
This becomes your function signature / dp table indices. Keep the state minimal - every extra dimension multiplies time and space.

**Step 3 - Write the recurrence**
Express `dp[state]` in terms of smaller states. Think about the last decision made before reaching this state (last element picked, last step taken).

**Step 4 - Identify base cases**
Smallest valid states that can be answered directly without recursion (empty array, index out of bounds, target = 0).

**Step 5 - Choose implementation order**
Top-down (memoization): write recursion + `@cache`, easier to reason about.
Bottom-up (tabulation): fill a table iteratively, usually faster in practice.

### Worked Example - House Robber

*"Given houses with values, rob non-adjacent houses for max total."*

**Step 2** - What info do I need? Only the current index `i` (which house I'm deciding on). State: `dp(i)` = max money from house `i` to end.

**Step 3** - At house `i`, either rob it (skip `i+1`) or skip it:
```
dp(i) = max(nums[i] + dp(i+2),  dp(i+1))
```

**Step 4** - `dp(n) = 0`, `dp(n-1) = nums[n-1]`

**Step 5** - Top-down:
```python
from functools import cache

def rob(nums):
    n = len(nums)

    @cache
    def dp(i):
        if i >= n:
            return 0
        return max(nums[i] + dp(i + 2), dp(i + 1))

    return dp(0)
```

Bottom-up (space-optimised - only need last two values):
```python
def rob(nums):
    prev2, prev1 = 0, 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1
```

### Common State Identification Patterns

| What varies between sub-problems | State to use |
|---|---|
| Position in 1D array | `i` |
| Two strings / two arrays | `(i, j)` |
| Remaining capacity / budget | `(i, remaining)` |
| Set of visited items | `(i, bitmask)` |
| Range of array | `(l, r)` |
| Digit position + tight constraint | `(pos, tight, ...)` |

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
