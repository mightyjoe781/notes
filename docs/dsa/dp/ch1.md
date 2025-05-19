# 1D DP

### Climbing Stairs

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

````c++
int climbStairsHelper(int n, vector<int>& dp){
    // base case
    if(n == 1) return 1;
    if(n == 2) return 2;

    // recursive step
    // check the table
    if(dp[n] != -1)
        return dp[n];

    // if not solved
    // solve now and store in table
    dp[n] = climbStairsHelper(n-1,dp) + climbStairsHelper(n-2,dp);
    return dp[n];
}
int climbStairs(int n) {
    vector<int> dp(n+1,-1);
    return climbStairsHelper(n,dp); 
}
````

Recurrence: $O(n^2)$, Memoization: $O(n)$

Now we could have solved same problem from smallest solution to largest then, we don’t even have to check anything. `dp[n]` would simply be the answer

````c++
int climbStairs(int n) {
    if(n == 1) return 1;
    vector<int> dp(n+1,-1);
    dp[1] = 1;
    dp[2] = 2;
    for(int i = 3; i < n+1; i++)
        dp[i] = dp[i-1]+dp[i-2];
    return dp[n];
}
````

Further Optimization can be done upon recognising that we are using only 2 variables to store states. (State Compression)

### House Robber

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

````c++
//<data-type of ans> f(<Subproblem representation>,<DP table>)
int robHelper(vector<int>& nums,int start,vector<int>& dp){
    int n = nums.size();
    // base cases
    if(start == n-1)
        return nums[n-1];
    if(start == n)
        return 0;
    // check the dp table
    if(dp[start] != -1)
        return dp[start];
    // recursive call
    dp[start] = max(nums[start]+robHelper(nums,start+2,dp),
                    robHelper(nums,start+1,dp));
    return dp[start];  }
int rob(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n+1,-1);
    return robHelper(nums,0,dp); }

````

**Second Approach**

````c++
int rob(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n+1,-1);
    dp[n] = 0, dp[n-1] = nums[n-1];
    for(int i = n-2; i >= 0; i--)
        dp[i] = max(nums[i]+dp[i+2], dp[i+1]);
    return dp[0]; 
}
````

**Second Approach (State Space Optimization)**

````c++
int rob(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(2,-1);
    
    dp[n%2] = 0, dp[(n-1)%2] = nums[n-1];
    for(int i = n-2; i >= 0; i--)
        dp[i%2] = max(nums[i]+dp[(i+2)%2], dp[(i+1)%2]);
    return dp[0%2];
}
````

Solution of Climbing Stairs using this approach : http://p.ip.fi/a6qS

### Problems

* [House Robber II](https://leetcode.com/problems/house-robber-ii/) : Try similar problem with constraint changed.

### Decode Ways

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

**Bottom Up Solution**

````c++
int numDecodings(string s) {
    int n = s.size();
    vector<int> dp(n);
    dp[n-1] = (s[n-1] == '0') ? 0 : 1;

    for(int i = n-2; i >= 0; i--){
        dp[i] = 0;
        // 2 cases
        // single digit
        if(s[i] != '0')
            dp[i] += dp[i+1];

        // double digit
        if(s[i] =='1' || (s[i] == '2' && s[i+1] <= '6')){
            if(i == n-2)
                dp[i] += 1;
            else 
                dp[i] += dp[i+2];
        }
    }
    return dp[0]; 
}
````

**Simplified Code**

````c++
int numDecodings(string s) {
    int n = s.size();
    vector<int> dp(n+1, 0);
    dp[n] = 1;
    dp[n-1] = (s[n-1] == '0') ? 0 : 1;

    for(int i = n-2; i >= 0; i--){
        if(s[i] != '0')
            dp[i] += dp[i+1];
        if(s[i] =='1' || (s[i] == '2' && s[i+1] <= '6'))
            dp[i] += dp[i+2];
    }
    return dp[0];
}
````

## Advanced 1D DP Problems

* These problems either have Nested Loops, or more than 1 degree of freedom but in a limited capacity (second dimension is small enough to enumerate) 

### Longest Increasing Subsequence (LIS)

- [Problem Link](https://leetcode.com/problems/longest-increasing-subsequence/)

Up until we have looked at subarrays, subsequences are different that subarray, they follow the order they appear in, but not necessarily contigous

1. Modelling the Problem: We have to find $res = max\{s_i\}$, where $s_i$ : Length of LIS ending at $i$
2. Now to find $s_i$ : Length of LIS ending at $i$, we assume that at any $j$, (where $j < i$) If $A[i] > A[j]$ we can extend teh subsequence by 1
3. Recurrence : $S_i = 1 + max_{j \le i} S_j$ and $A[i] > A[j]$
4. Checking DP, Prefix Array with dimension 1, size <- n
5. Base case : `dp[0] = 1`

````c++
int lengthOfLIS(vector<int>& nums) {
    int n = nums.size(),i,j, res = 1;
    vector<int> dp(n,1);

    for(i = 1; i < n; i++){
        // compute dp[i]
        for(j = i-1; j >= 0; j--)
            if(nums[i] > nums[j])
                dp[i] = max(dp[i],1+dp[j]);
        res = max(res,dp[i]);
    }     return res;  
}
````

* Solve Longest Arithmetic Subsequence After this problem

### Word Break

- [Problem Link](https://leetcode.com/problems/word-break/)

All possible splits can be calculated and some will be valid, and some will not be valid. We can have splits at `0, 1, 2, ..., n-1` giving $s_1, s_2, ..., s_n$

given : `catsanddog`, we could split at `[1, 4, 7]` or `[3, 6, 8]` and more...

- Model Problem: $S$ : set of all possible splits
- DnC Criteria: we can mark first split at `0, 1, 2...`, split at some position is i would be $s_i$ , these splits will be mutually exclusive and exhaustive in nature
- We can prune the solution and validate each subproblem as
  - $s_1$ : $A[1...n-1]$ s.t. all words are in dictionary
  - $s_2$ : A[2 ... n-1]
  - Suffix Strings
- We should have split s.t. all words `[0 ... i-1]` for $s_i$ are in dictionary
- Representation : $res = OR\{w[0 ..i-1] \in D \text{ \& } S_i\}$
- $S = w_1 | w_2 | w_3 | ...$
- $D = \{w_1, w_2, w_1w_2\}$
- Order to fill : in backwards, for $j < i$

````c++
bool wordBreak(string s, vector<string>& wordDict) {
    unordered_set<string> dict(wordDict.begin(), wordDict.end());
    int i, j, n = s.size();
    vector<bool> dp(n+1,false);
    dp[n] = true;
    string temp = "";
    for(i = n-1; i >= 0 ; i--){
        //compute s_i
        temp = "";
        for(j = i; j <n; j++){
            temp += s[j];
            if(dict.find(temp) == dict.end())
                continue;
            dp[i] = dp[i] || dp[j+1];

            if(dp[i])
                break;
        }
    }     return dp[0]; 
}
````

* Word - Break II 
