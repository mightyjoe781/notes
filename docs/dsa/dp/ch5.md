# Game DP

### Stone Game

- [Problem Link](https://leetcode.com/problems/stone-game/)
- NOTE: Game’s Outcome is Deterministic !
- The problem's constraints state that both players play optimally. Alex, starting the game, can lock a particular index set (odd or even). Therefore, she knows which index set has the greater sum. Conclude that Alex always wins.
- Solution : `return true;`
- Split Criteria:
    - Original Subproblem : Alex goes first, whether Alex Wins/Losses given `A[0...n-1]`
    - Subsets : Lee goes first, whether Alex wins/losses given `A[1, ... n-1]`
    - If Alex chooses `A[n-1]` , then second config becomes Lee goes first, whether Alex wins/losses given `A[0...n-2]`

- There are 3 dimension to this DP, Its of general subarray type
- 2D Subproblems
- Representation :
    - $p_1$ : $P1(A, i, j)$ Assuming alex goes first
    - $p_2$ : $P2(A, i, j)$ Assuming lee goes first
    - Actual Problem will Alex win if P1 or P2
    - $P1(A, i, j) = P2(A, i+1, j) || P2(A, i, j-1)$

- Problem statement needs to expanded as wee need to keeps score to decide who wins
    - $P1(A,i,j)$ <- Alex - lee score for A[i….j] Assuming Alex goes first
    - $P2(A,i,j)$ <- Alex - lee score for A[i…j] Assuming lee goes first
    - $P1(A,i,j) = max \{A[i] + p_2(A,i+1,j) , A[j] + p2(A,i,j-1) \}$
    - $P2(A,i,j) = max \{  p_1(A,i+1,j)-A[i] , p(A,i,j+1)-A[j] \}$
    - $P(A,i,j)$ : whoever is going first <- $max(S_1 - S_2)$;

- Difference between scores of P1 and P2 assuming P1 goes first.
    - $P(A,i,j) = max \{A[i] - P(A,i+1,j) , A[j] - P(A,i,j-1) \}$

- Repeated Subproblems
- Order to Fill Table
    - Top to Down & left to right, since `i<=j`, we just populate lower triangular matrix

- Base Case: We can fill principle diagonal before using `i=j` we can do `A[i]`

````c++
bool stoneGame(vector<int>& piles) {
    int n = piles.size(), i, j;
    vector<vector<int>> dp(n,vector<int>(n,0));
    // diagonal
    for(i = 0; i <n ; i++) dp[i][i] = piles[i];

    for(i = n-2; i >= 0; i--)
        for( j = i+1; j <n; j++)
            dp[i][j] = max(piles[i]-dp[i+1][j],
                           piles[j] - dp[i][j-1]);
    return dp[0][n-1] > 0; 
}
````

- NOTE : this table can be filled diagonally as well :)

### Predict Winner

### Nim Game

## Interval DP

### Burst Balloons

* [Problem Link](https://leetcode.com/problems/burst-balloons/)
* From the problem we can understand clearly there is an order of popping balloons, which will given you most sum. This is similar to there are multiple path but only 1 is optimal (could be more),
* Problem Space : All permutations of bursting balloons
* Subproblem : $s_1$ : the permutation in which balloon $B_1$ is burst at the end
    * Similarly for $s_2$ , $s_3$, .. $s_n$

* Do not burst the balloon in the middle, as it will remove information about nearby balloons, preventing further query resolution. The balloons are not independent. Select the last balloon to ensure that a balloon exists on the left side.
* Let’s say we burst $B_i$ last
    * then solution becomes : $(B_0 ...B_{i-1}) + (B_{j+1} ... B_{n-1}) + 1 *B_i * 1$

* Recurrence : $dp(i, j) = max_{i \le k \le j} dp(i, k-1) + dp(k-1, j) + A[k]$
* Note: Solution is $O(n^3)$

````c++
int maxCoins(vector<int>& nums) {
    int n = nums.size(), len, i, k, left=1, right=1, left_term, right_term;
    vector<vector<int>> dp(n,vector<int> (n,0));
    // dp
    for(len = 1; len <= n; len++){
        for(i = 0; i+len-1 < n; i++){
            // nums[i][i+len-1]
            for(k = i; k <= i+len-1; k++){
                left = right = 1;
                if(i-1 >= 0) left = nums[i-1];
                if(i+len-1+1 < n) right = nums[i+len-1+1];
                left_term = right_term = 0;
                if(k-1 >= 0) left_term = dp[i][k-1];
                if(k+1 < n) right_term = dp[k+1][i+len-1];
                dp[i][i+len-1] = max(dp[i][i+len-1],
                                     left_term+right_term+
                                     left*nums[k]*right);
            }
        }
    }     
  	return dp[0][n-1]; 
}
````

### Minimum Deletions to make Palindrome

- Problem: Find the minimum number of deletions required to make string palindrome
- Key Insight: The problem could be formulated as a range DP over substrings, where goal is to minimize deletions in the substring `s[i...j]`
- Subproblem: `dp[i][j]` : represents the min deletions required to make substring `s[i...j]` a palindrome
- Base Case
    - If `i == j`, substring of lenght 1 is already a palindrome, return 0
    - if `i > j`, empty substring, so shoudl be zero
    - Transition : if `s[i] == s[j]` then problem is same as solving `dp[i+1][j-1]`
- There are two possibilities to get answer, either delete left character or right character & get minimum

````c++
def minDeletions(s):
    n = len(s)
    dp = [[0]*n for _ in range(n)]

    for i in range(n-1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] if i+1 <= j-1 else 0
            else:
                dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])

    return dp[0][n-1]The question of whether machines can think is about as relevant as the question of whether submarines can swim" Edsger Dijkstra
````

### Matrix Chain Multiplication
