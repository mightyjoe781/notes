# Knapsack

## Bounded Knapsack

### Coin Change

* Very Famous & Standard Problem
* Trying to solve this problem greedily fails, Proof by contradiction
  * Example - `[1, 15, 25]` coins, to get a total sum of 30, we will need 1 denomination of 25, and 6 denomination of `1`, A total of 6 coins
  * But optimal solution is to use 2 denomination of 15.
* Split Criteria is we can divide the problem into two subproblems where we take `0` denomination of first coin, other solution is we take more than zero denomination of the first coin
  * $s_1$ : Excluding first coin : $P(A, 1, target)$
  * $s_2$ : Including first coin : $P(A, 0, target-A[0])$ 
* Recurrence : $P(A, 0, target) = min {P(A, 1, target), 1 + P(A, 0, target - A[0])} $
* Clearly its a 2-dimensional DP with a size of `n * (target + 1)`
* Base Case
  * `dp[n][0] = 0`
  * `dp[n][1...target] = INT_MAX` (NOTE: since we are taking min at each step, `INT_MAX` will eventually be replaced)


**Recursive Solution**

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

### Rod Cutting

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

**Tabulation Strategy**

Fill the DP table from the bottom-up:

- Start from i = n-1 down to 0
- Iterate through cap = 0 to W

Order of filling table looks like:

````
Item ⬇️ vs Capacity ➡️ (0...W)
````

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
  - A list of task sizes: tasks[i] (integers)
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
  * Maximize total weight ≤ capacity C

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

### Equal Partition