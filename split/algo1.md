# Algo Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: algo
This is part 1 of 1 parts

---

## File: algo/cp/index.md

## Competitive Programming Basics



1. ### Data Structures Revisited

   - Space Time Complexity Analysis
   - Data Structures & STL Containers
   - Bitmanipulation

2. ### Mathematics

3. ### Number Theory

4. ### Algoritms

5. ### Range Queries

6. ### Game Theory

7. ### Graph Theory

8. ### Dynamic Programming

9. ### Pattern Matching

10. ### Advanced Topics

---

## File: algo/graph/index.md

## Graph Algorithms

- ### [Graph Search](search.md)

- ### Digraphs and DAGs

- ### MSTs

- ### Shortest Paths

- ### Network Flows



---

## File: algo/graph/search.md

## Graph Search

### DFS



```c++
const UNVISITED = -1;
const VISITED = 1;

vector<int> dfs_num;				// initially all set to unvisited

void dfs(int u) {
  dfs_num[u] = VISITED;
  for(auto v:adj[u]) {
    if(dfs_num[v] == UNVISITED)
       dfs(v);
  } }

```

### BFS

````c++
// inside int main() -- no recursion
  vi d(V,INF); d[s] = 0;					// distance from source s to s is 0
  queue<int> q; q.push(s);

  while(!q.empty()) {
    int u = q.front(); q.pop();
    for(auto v:adj[u]) {
      if(d[v] == INF) {
        d[v] = d[u] + 1;
        q.push(v);
 } } }
````



---

## File: algo/index.md

# Algorithms

1. **[Data Structures]()**

   - Elementary Data Structures

   - Abstract Data Structures

   - Recursion & Trees

2. **[Sorting]()**
   - Elementary Sorting Strategies
   
   - Quicksort
   
   - Mergesort
   
   - Priority Queues & Heapsort
   
   - Radix Sort
   
3. **[Searching]()**
   - Binary Search

   - BSTs

   - Hashing

   - Radix Search
4. **[Graph Algorithms](graph/index.md)**
- [Graph Search]()


   - [Digraphs and DAGs]()

   - [MSTs]()

   - [Shortest Paths]()

   - [Network Flows]()


5. **Problem Solving Paradigm**

   - [Complete Search]()

   - [Divide & Conquer]()

   - [Greedy]()

   - [Dynamic Programming]()

[Problems](problems/index.md)

// ---> main page content is theory to learn everything

// ---> Notes from classes

## Advanced Algorithms

- GeoHash
- Quadtree
- Consistent Hashing
- Token Bucket
- Trie
- Rsync
- Raft/Paxos
- Bloomfilter
- Merkle Tree
- HyperLogLog
- Count-min Sketch
- Hiearchical timing wheels
- Operational Transformation



---

## File: algo/problems/index.md

## Problems on DSA

[Max Sum Rectangle no larger than k](max_sum_rectangle_no_larger_than_k.md)

---

## File: algo/problems/max_sum_rectangle_no_larger_than_k.md

### Max Sum Rectangle No Larger than K

Problem Statement : *Given a m x n matrix and an integer k, return the max sum of a rectangle in the matrix such that its sum is no larger than k*.

To approach this problem, we first understand that last condition seems like a constraint on much general problem. So maybe solving the problem of finding max sum rectangle is the correct way to proceed.

Now if you are a novice programmer and still stuck and cannot this of a solution then don’t worry, as you are not the only one stuck in this problem. This problem was proposed by *Ulf Grenander* in 1977 as a simplified model for *maximal likelihood* estimation of patterns in digitized images.

Initially he came up with an $O(n^6)$ solution to problem, So as a result Grenander thought of exploring much simpler version of this problem, let’s try to find the max sum rectangle (subarray) in 1 dimensional array. Eventually he solved the problem with $O(n^2)$ complexity and solving the original problem with $O(n^3)$ complexity.

Micheal Shamos solved the problem in $O(n \log n)$ using Divide and Conquer (DnC) and when he was giving a talk about this solution in CMU (*Carnegie Mellon University*) seminar attended by Jay Kadane who solved it within few minutes $O(n)$ runtime. Eventually there were more interesting solution involving *Dijkstra’s Strategy* applied by David Gries and Pure alzebric manipulation based solution using Bird-Meertens Formalism.

That was a nice history trivia but how do we solve the problem ! At least we got in a correct direction on which we can build up our solution.

Statement : Find the subarray with maximum sum ?

#### A DnC Based Solution (Kadane’s Formulae)

Step 1 : DnC criteria

We wanna find out for every $j$ -> max sum($S_j$) subarray ending at $j$

Step 2 : compute $S_j$

Subarray ends at $j^{th}$ element and it includes $A[j]$. So now there are two possibilities, either we include that element or we do not include the element (which implies, subarray is not continous anymore so we reset subarray value).

Step 3 : So problem concludes to be 1D table with prefix array. $dp[j] = S_j$

Base Case : $dp[0] = nums[0]$ // taken care while declaring the dp vector we explicitly set it to zero.

````c++
int maxSubArray(vector<int>& nums) {
  int n = nums.size(), i, res = INT_MIN;
  vector<int> dp(n+1,0);
  
  for( i = 1; i <= n; i++) {
    dp[i] = max(dp[i-1] + nums[i-1], nums[i-1]);
    res = max( res, dp[i]);
  }
  return res;
}
````

#### Kadane’s Algorithm

Kadane’s Formulation is more simpler implementation of above DnC formulation.

````c++
int maxSubArray(vector<int>& nums) {
  int n = nums.size(), i, res = INT_MIN;
  int prev = 0, curr;
  for(i = 1; i <= n; i++) {
    curr = max(prev + nums[i-1], nums[i-1]);
    res = max(res, curr);
    prev = curr;
  }
  return res;
}
````

Lets try to put in the constraint of finding the maximum sum less than k in 1D array. Best approach is $O(n log(n))$, lets say we want to find the $S_j$ which is nothing but for some $i$ ($i < j$) , the difference between cummulative sum from start till $i$ and $j$, i.e. $cum[j]-cum[i]$.

To solve this problem, traverse from left to right. Put $cum[i]$ values you have encountered till now in a set. While processing $cum[j]$, what you need to retrieve from the set is the smallest number in set such which is bigger than $cum[j]-k$. This lookup can be done in O(log n) using upper_bound function.

````c++
int bestCummulativeSum(int arr[], int N, int K) {
  set<int> cs;
  cs.insert(0);
  
  int best = 0, cum = 0;
  for( int i = 0; i < N; i++) {
    cum += arr[i];
    auto sit = cs.upper_bound(cum-K);
    if(sit != cs.end()) best = max(best, cum - *sit);
    cs.insert(cum);
  }
  return best;
}
````



Now having solved 1D version of our original problem efficiently, lets move on to the second portion of the problem of solving 2D version of the same problem.

This video explains well the approach of the solution for finding maximum area rectangle in a matrix : [Tushar Roy Video](https://www.youtube.com/watch?v=yCQN096CwWM).

Utilising above concepts we can easily solve the problem as follows.



````c++
int maxSumSubmatrix(vector<vector<int>>& matrix, int k) {
  if(matrix.empty()) return 0;
  int r = matrix.size(), c = matrix[0].size(), res = INT_MIN;
  for(int l = 0, l < c; ++l) {
    vector<int> sum(r, 0)
      for(int r = l, r < c; ++r) {
        for(int i = 0; i < r; ++r) {
          sums[i] += matrix[i][r];
        }
        // find the max subarray no more than k     
        set<int> accuSet;
        accuSet.insert(0);
        int curSum = 0, curMax = INT_MIN;
        for(int sum : sums ) {
          curSum += sum;
          auto it = accuSet.lower_bound(curSum - k);
          if(it != accuSet.end()) curMax = std::max(curMax, curSum - *it);
          accuSet.insert(curSum);
        }
        res = std::max(res,curMax);
      }
  }
  return res;
}
````



---

