# Grid DP

### Minimum Path Sum

* [Problem Link](https://leetcode.com/problems/minimum-path-sum/)
* Direction Constraint : down, right only
* We have to minimize the sum along a valid path from `(0,0)` to `(m-1, n-1)`
* Split criteria: Two sets of problems, where we can either take the down or right cell
  * $s_1$ : Min. Path Sum given first step is right step, then solving problem for $P(0, 1)$
  * $s_2$ : Min. Path Sum given first step is right step, then solving problem for $P(1, 0)$
* All matrices are suffix matrix for the original matrix
* Recurrence: $P(0, 0) = min\{P(0, 1), P(1, 0)\} + A[0][0]$
* Its a two dimensional DP, $m*n$
* Base Cases : declare extra column & row with the value `INT_MAX`
* Order to fill the table, bottom to top & right to left

````c++
int minPathSum(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size() ,i ,j ;
    vector< vector<int>> dp(m+1,vector<int>(n+1,INT_MAX));
    dp[m][n-1] = dp[m-1][n] = 0;
    // bottom to top , R to L
    for(i = m-1; i>=0; i--)
        for(j = n-1; j>=0; j--)
            dp[i][j] = grid[i][j] + min(dp[i+1][j],dp[i][j+1]);
    return dp[0][0]; 
}
````

**Space State Optimization**

````c++
int minPathSum(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size() ,i ,j ;
    vector<int> dp(n+1,INT_MAX);
    dp[n-1] = 0;
    // bottom to top , R to L
    for(i = m-1; i>=0; i--)
        for(j = n-1; j>=0; j--)
            dp[j] = grid[i][j] + min(dp[j+1],dp[j]);
    return dp[0]; 
}
````

### Dungeon Game

* [Problem Link](https://leetcode.com/problems/dungeon-game/description/)
* Find a path where the health of knight doesn’t go below zero, 
* Split Criteria
  * $H_1$ : Initial min. Health of knight for rescuing in the box `(0, 1)` to `(m-1, n-1)`
  * $H_2$ : Initial min. Health of knight for rescuing in the box `(1, 0)` to `(m-1, n-1)`
* By definition $H_1 > 0$ & $H_2 > 0$, so `dp[0][0] = val`, so both subproblems will become `H1` is `-6` & `H2` is `-5`, assuming initial health as `val-6` and `val-5` respectively, and it is guaranteed that one path will lead to solution by problem constraint
* Base Case
  * bottom row : $H_1 = \max(H_1 - val, 1)$
  * right column : $H_2 = \max(H_2 - val, 1)$
* Order of filling : B to L & R to L

````c++
int calculateMinimumHP(vector<vector<int>>& dungeon) {
    int m = dungeon.size(), n = dungeon[0].size(), i , j;
    vector<vector<int>> dp(m,vector<int> (n,INT_MAX));
    
    dp[m-1][n-1] = max(1-dungeon[m-1][n-1],1);
    
    for( i = m-1; i >= 0; i--){
        for(j = n-1; j >= 0; j--){
            if(i+1 < m)
                dp[i][j] = min(dp[i][j],
                               dp[i+1][j] - dungeon[i][j]);
            if(j+1 < n)
                dp[i][j] = min(dp[i][j],
                               dp[i][j+1] - dungeon[i][j]);
            dp[i][j] = max(1,dp[i][j]);
        }
    }    
  	return dp[0][0];
}
````

### Unique Paths

* https://leetcode.com/problems/unique-paths/description/

### Frog Jump

* [Problem Link](https://leetcode.com/problems/frog-jump/)
* Split Criteria: at each step we could jump to `k` , `k+1`, `k-1`
* Representation : $P(S_i,k)$ : can we reach the last stone starting from $s_i$ assuming the last jump made was `k`
* Recurrence : $P(s_i, k) = P(s_j, k-1) || P(s_l, k) || P(s_m, k+1)$
* where $s_j = s_i + k - 1$, $s_l = s_i + k$ , $s_m = s_i +k+1$, s : represents the indices
* Size : nxn, max possible jump is `n+1`, order of filling : bottom to top

**TLE Solution**

````c++
bool canCross(vector<int>& stones) {
    if(stones[1]!=1)
        return false;
    int n = stones.size(), i ,j;
    unordered_map<int,int> m;
    vector<vector<bool>> dp(n,vector<bool>(n+1,false));
    // populate the map
    for(i = 0; i <n; i++){
        m[stones[i]] = i;
        dp[n-1][i+1] = true;
    }
    // DP table
    for(i = n-2; i >= 1; i--){
        for(j = 1; j <= n; j++){
            // 3 casese
            if(j > 1 && m.find(stones[i]+j-1) != m.end())
                dp[i][j] = dp[i][j] || dp[m[stones[i]+j-1]][j-1];
            // j
            if(m.find(stones[i]+j) != m.end())
                dp[i][j] = dp[i][j] || dp[m[stones[i]+j]][j];

            // j+1
            if(m.find(stones[i]+j+1) != m.end())
                dp[i][j] = dp[i][j] || dp[m[stones[i]+j+1]][j+1];
        }
    }     
  	return dp[1][1]; 
}
````

* Above solution can be improved by observing that for all the `k` stones we don’t need to store last possible sum
* we need only few `k` values:
* Bottom Up -> always computing all subproblems, Top-Down -> computes only the needed subproblem

**Top-Down Solution Passes**

````c++
bool canCrossHelper(unordered_map<int,int>& m, vector<vector<int>> &dp ,int i, int j , vector<int>& stones){
    int n = stones.size();
    // base case
    if( i == n-1) return true;
    // dp step 
    if(dp[i][j]!= -1) return dp[i][j];
    int t1 = 0, t2=0, t3 = 0;
    // 3 casese
    if(j > 1 && m.find(stones[i]+j-1) != m.end())
        t1 = canCrossHelper(m,dp,m[stones[i]+j-1],j-1,stones);
    // j
    if(m.find(stones[i]+j) != m.end())
        t2 = canCrossHelper(m,dp,m[stones[i]+j],j,stones);
    // j+1
    if(m.find(stones[i]+j+1) != m.end())
        t3 = canCrossHelper(m,dp,m[stones[i]+j+1],j+1,stones);

    dp[i][j] = t1 || t2 || t3;
    return dp[i][j];
}
bool canCross(vector<int>& stones) {
    if(stones[1]!=1)
        return false;
    int n = stones.size(), i ,j;
    unordered_map<int,int> m;
    vector<vector<int>> dp(n,vector<int>(n+1,-1));
    // populate the map
    for(i = 0; i <n; i++){
        m[stones[i]] = i;
    }    
  	return canCrossHelper(m,dp,1,1,stones);
}
````

## Palindrome DP

### Longest Palindromic Subsequences

* [Problem Link](https://leetcode.com/problems/longest-palindromic-subsequence/)
* Check Stone Game Problem : [Link](ch5.md)
* Hint : Recurrence : 
  * Equal : $P(0, n-1) = 2 + P(1, n-2)$
  * Not Equal : $P(0, n-1) = max\{P(1, n-1), P(0, n-2)\}$


````c++
int longestPalindromeSubseq(string s) {
    int n = s.size(), len, i;
    vector<vector<int>> dp(n,vector<int>(n,0));

    // length wise
    for(len = 1; len <= n; len++)
        for(i = 0; i+len-1 < n; i++)
            if(len == 1)
                dp[i][i] = 1;
    		else {
        	// s[i][i+len-1]
        if(s[i] == s[i+len-1])
            dp[i][i+len-1] = 2+(i+1> i+len-2?0:dp[i+1][i+len-2]);
        else
            dp[i][i+len-1] = max(dp[i+1][i+len-1],dp[i][i+len-2]);
    }  
  	return dp[0][n-1]; 
}
````

### Min Cuts for Pal

* [Link](https://leetcode.com/problems/palindrome-partitioning-ii/description/)
