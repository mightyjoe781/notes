# Subsets & Knapsack

## Subsets

### Subset Sum equal to S

Given an array with N positive integers, Find if any of the subset of the array sums equal to K.

```python
def main(arr, k):
    n = len(arr)

    @cache
    def solve(i, curr):
        if curr == k:
            return True

        if i >= n or curr > k:
            return False

        return solve(i + 1, curr + arr[i]) or solve(i + 1, curr)

    return solve(0, 0)
```

Above solution builds up the `curr` sum to be equal to target.

### Partition Equal Subset Sum

Problem 416 : [Link]https://leetcode.com/problems/partition-equal-subset-sum/description/

if We can partition the array into two subsets such that the sum of the elements in both subsets is equal.

This problem is quite simple if we know the sum of the array. then problem reduces to above problem, finding the Subset where sum is exactly half of the total sum.

```python

def canPartition(nums):
    s = sum(nums)

    if s%2: # odd sum, its not possible to partition
        return False

    k = s//2
    n = len(nums)

    dp = [[False] * (s+1) for _ in range(n+1)]
    dp[0][0] = True
    
    for i in range(1, n+1):
        for s in range(k+1):
            dp[i][s] = dp[i-1][s]
            if s >= nums[i-1]:
                dp[i][s] = dp[i][s] or dp[i-1][s-nums[i-1]]
    

    return dp[n][k]
```

### Partition Array into Two Arrays to Minimize the Sum Difference

Problem Link 2035 - [Link](https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/)

Consider that we have two partitions of the original array with $n$ length each $p_1$ and $p_2$

Problem : $\text{minimize } [abs(sum(p_1) - sum(p_2))]$

NOTE: We can't optimize this problem using simple Dynamic Programming, We will require to use special technique like MITM with min-max p (thanks to generous n = 40).

```python
def minimumDifference(self, nums: List[int]) -> int:
    n = len(nums)
    half = n // 2
    total = sum(nums)

    A = nums[:half]
    B = nums[half:]

    def gen(arr):
        n = len(arr)
        res = [[] for _ in range(n+1)]
        for mask in range(1 << n):
            s = 0
            cnt = 0
            for i in range(n):
                if mask & (1 << i):
                    s += arr[i]
                    cnt += 1
            res[cnt].append(s)
        return res

    sumA = gen(A)
    sumB = gen(B)

    for k in range(half+1):
        sumB[k].sort()

    ans = float('inf')

    for k in range(half+1):
        for sa in sumA[k]:
            need = total/2 - sa
            arr = sumB[half - k]
            idx = bisect_left(arr, need)

            if idx < len(arr):
                s = sa + arr[idx]
                ans = min(ans, abs(total - 2*s))

            if idx > 0:
                s = sa + arr[idx-1]
                ans = min(ans, abs(total - 2*s))

    return ans
```

NOTE: Solve the same problem if given $p1-p2 = D$, where $D$ is difference given. Now its doable using DP because we know $p_1 + p_2 = S$ 
### Count Subsets with Sum K

Same as above problem, but rather than checking its a counting problem

```python

def main(arr, k):
    n = len(arr)

    @cache
    def solve(i, curr):
        if curr == k:
            return 1

        if i >= n or curr > k:
            return 0

        return solve(i + 1, curr + arr[i]) + solve(i + 1, curr)

    return solve(0, 0)
```

## Bounded Knapsack

### Coin Change

NOTE: if coins are replaceable infinitely then this is unbounded knapsack, else its bounded.

* Very Famous & Standard Problem
* Trying to solve this problem greedily fails, Proof by contradiction
    * Example - `[1, 15, 25]` coins, to get a total sum of 30, we will need 1 denomination of 25, and 6 denomination of `1`, A total of 6 coins
    * But optimal solution is to use 2 denomination of 15.
* Split Criteria is we can divide the problem into two subproblems where we take `0` denomination of first coin, other solution is we take more than zero denomination of the first coin
    * $s_1$ : Excluding first coin : $P(A, 1, target)$
    * $s_2$ : Including first coin : $P(A, 0, target-A[0])$ 
* Recurrence : $P(A, 0, target) = min {P(A, 1, target), 1 + P(A, 0, target - A[0])}$
* Clearly its a 2-dimensional DP with a size of `n * (target + 1)`
* Base Case
    * `dp[n][0] = 0`
    * `dp[n][1...target] = INT_MAX` (NOTE: since we are taking min at each step, `INT_MAX` will eventually be replaced)


**Recursive Solution**

```python
# this calculates the number of fewest coins that you can use,
def coinChange(self, coins: List[int], amount: int) -> int:
    n = len(coins)

    @cache
    def solve(i, amt):
        if amt == 0: # a solution
            return 0
        if i >= n or amt < 0: # invalid state
            return float('inf')

        return min(
            1 + solve(i, amt - coins[i]),  # take coin i (unbounded)
            solve(i + 1, amt)               # skip coin i
        )

    res = solve(0, amount)
    return -1 if res == float('inf') else res

```

````c++
// recursive solution
#include <vector>
#include <climits>
using namespace std;

int coinChangeHelper(const vector<int>& coins, int i, int target, vector<vector<int>>& dp) {
    // base cases
    if (target == 0) return 0;
    if (target < 0 || i >= coins.size()) return INT_MAX;

    if (dp[i][target] != -1)
        return dp[i][target];

    int skip = coinChangeHelper(coins, i + 1, target, dp);
    int take = coinChangeHelper(coins, i, target - coins[i], dp);
    if (take != INT_MAX) take += 1;

    return dp[i][target] = min(skip, take);
}

int coinChange(const vector<int>& coins, int target) {
    int n = coins.size();
    vector<vector<int>> dp(n, vector<int>(target + 1, -1));
    int res = coinChangeHelper(coins, 0, target, dp);
    return (res == INT_MAX ? -1 : res); // -1 if not possible
}
````

**Tabulation Solution**

- From the recurrence we can observe that we can fill 2D Table by filling bottom row, and a column somewhere behind the current element. Bottom to Top & Left to Right.

````c++
int coinChange(vector<int>& coins, int amount) {
    int n = coins.size(), i, j;
    vector<vector<int>> dp(n+1, vector<int>(amount+1,INT_MAX));

    dp[n][0] = 0;
    for(i = n-1; i>= 0; i--){
        for(j = 0; j <= amount; j++){
            dp[i][j] = dp[i+1][j];
            if(j-coins[i] >= 0 && dp[i][j-coins[i]] != INT_MAX)
                dp[i][j] = min(dp[i][j], 1+dp[i][j-coins[i]]);
        }
    }    
  	return dp[0][amount] == INT_MAX ? -1: dp[0][amount];
}
````

* Notice how, `[i]` in the recurrence doesn’t change, that means that it can be state optimized, because we only need one previous row not the entire table.
* [Example Solution](https://algo.minetest.in/Practice_DP/DP_4/)

Further Optimization on Space State could be done using only 1 dimensional table, since states does not depend on some far away row.

````c++
int coinChange(vector<int>& coins, int amount) {
    int n = coins.size(), i, j;
    vector<int> dp(amount+1,INT_MAX);
    dp[0] = 0;
    for(i = n-1; i>= 0; i--)
        for(j = 0; j <= amount; j++)
            if(j-coins[i] >= 0 && dp[j-coins[i]] != INT_MAX)
                dp[j] = min(dp[j], 1+dp[j-coins[i]]);
    return dp[amount] == INT_MAX ? -1: dp[amount];
}
````

**Follow Up**

- Now Try to solve the same problem using following split criteria

    * $s_1$ : picking 1st coin & finding solution

    * $s_2$ : picking 2nd coin & finding solution

    * ...

    * $s_n$

- Recurrence : $P(target) = 1 + \min_{0 \le i \le n}{P(target - A[i])}$
- Base Case:
    - P(0) = 0 (No coins needed to make amount 0)
    - If target < 0, return INT_MAX to signify impossible state

````c++
int coinChangeHelper(const vector<int>& coins, int target, vector<int>& dp) {
    // base cases
    if (target == 0) return 0;
    if (target < 0) return INT_MAX;

    if (dp[target] != -1)
        return dp[target];

    int ans = INT_MAX;
    for (int i = 0; i < coins.size(); ++i) {
        int res = coinChangeHelper(coins, target - coins[i], dp);
        if (res != INT_MAX)
            ans = min(ans, 1 + res);
    }
    return dp[target] = ans;
}

int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, -1);
    int res = coinChangeHelper(coins, amount, dp);
    return res == INT_MAX ? -1 : res;
}
````

Tabulation of Above Method

````c++
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;

    for (int j = 1; j <= amount; ++j) {
        for (int i = 0; i < coins.size(); ++i) {
            if (j - coins[i] >= 0 && dp[j - coins[i]] != INT_MAX)
                dp[j] = min(dp[j], 1 + dp[j - coins[i]]);
        }
    }
    return dp[amount] == INT_MAX ? -1 : dp[amount];
}
````

Follow Up : Could you count number of such combinations.
### Target Sum

Problem Link 494 - [Link](https://leetcode.com/problems/target-sum/description/)

The problem is quite simple, for every place we have two choice, either take `+` or `-`

```python

def findTargetSumWays(nums, target):

    s = sum(nums)
    if abs(target) > s:
        return 0

    @cache
    def solve(i: int, curr: int) -> int:
        # base case
        if i == len(nums):
            return 1 if curr == target else 0

        # choose + or -
        plus = solve(i + 1, curr + nums[i])
        minus = solve(i + 1, curr - nums[i])

        return plus + minus

    return solve(0, 0)
```

## UnBounded Knapsack

### Integer Knapsack (0/1)

* Its quite similar to coin change, but we have to take items such that we get maximum value and capacity less than the max capacity
* Given
    * Items : $I_1 I_2 ...I_n$
    * Value : $v_1, v_2...v_n$
    * Capacity: $c_1, c_2...c_n$
* Criteria: Solving the problem based on whether we get max capacity by including or excluding the first element in the set.
    * $s_1$ : solving knapsack including the item1
    * $s_2$ : solving knapsack including the item2
* Recurrence : $P(A, i, cap) = \max\{v_i + P(A, i+1, cap-c_i), P(A, i+1, cap)\}$

Example Problem : A thief wants to rob a store. He is carrying a bag of capacity W. The store has ‘n’ items of infinite supply. Its weight is given by the ‘wt’ array and its value by the ‘val’ array. He can either include an item in its knapsack or exclude it but can’t partially have it as a fraction. We need to find the maximum value of items that the thief can steal. He can take a single item any number of times he wants and put it in his knapsack.

A pythonic Solution

```python
# Unbounded Knapsack
def main(n, W, wt, val):
    @cache
    def solve(i, curr):
        if curr > W:
            return float("-inf")

        if i >= n:
            return 0

        return max(
            val[i] + solve(i, curr + wt[i]), # replacable items,
            solve(i + 1, curr)
        )

    return solve(0, 0)
```

### Fractional Knapsack

* Only difference as compared to above problem is that we are now allowed to take fractional parts of an item. We have to maximize the value given total capacity
* Given
    * Items: Each with `value[i], weight[i]`
    * Partial Items can be taken
    * Capacity : `W`
* This is not a DP Problem, Here greedy will work because we can calculate `value[i]/weight[i]` for each item, giving us the optimal choice to pick items.
* Sort the above transformed array and take as much as till `W` is reached.

### Server Problem (0/1) Knapsack

- You have:
    - A list of task sizes: `tasks[i]` (integers)
    - A **single integer capacity**: C (capacity of **server 0**)
- You need to:
    - **Generate all possible subsets** of tasks (tasks cannot be split).
    - For each subset, compute the **sum of its tasks**.
    - Find the **maximum total task size ≤ C** (that is, the most work server 0 can process **without exceeding** its capacity).
- You’re not required to assign the rest of the tasks or consider other servers.

* Converting to Knapsack
    * Items = tasks
    * Weight = task size
    * Value = same as weight
    * Maximize total weight <= capacity C

````c++
int maxSubsetSumWithinLimit(const vector<int>& tasks, int capacity) {
    vector<bool> dp(capacity + 1, false);
    dp[0] = true;  // zero sum is always achievable

    for (int task : tasks) {
        for (int c = capacity; c >= task; --c) {
            dp[c] = dp[c] || dp[c - task];
        }
    }

    for (int i = capacity; i >= 0; --i) {
        if (dp[i]) return i;
    }

    return 0; // no subset possible (should not happen with dp[0] = true)
}
````

- If n is up to **40** and capacity can be up to **1e9 or more**, use **meet-in-the-middle**

### Rod Cutting

Given a Rod of Length N : `price[i] = price of rod of length i + 1`
We can cut rod into any number of pieces, and since cuts could be overlapping subproblem, we can use Dynamic Programming.

- Converting to Knapsack
    - Capacity = Rod Length N
    - Item Weights = Piece Length
    - Item Value = `price[i]`
    - Unlimited Items = Can cut same length many times
    - Maximize Values <= C

```python

def cutRod(prices, n):

    @cache
    def solve(rem):
        if rem == 0:
            return 0

        res = 0
        for cut in range(1, rem + 1):
            res = max(res, price[cut - 1] + solve(rem - cut))

        return res

    return solve(n)
```