# Combinatorics & Permutations

* Note that all problems listed here are enumeration problems requiring the generation of all possible solution combinations. If the problems involved calculating a single value instead of actual solutions, they would become dynamic programming problems. In such cases, optimizations like memoization can reduce complexity.

## Subsets

* NOTE: Subsets don’t have any specific order
* To solve this problems lets divide the solution set using some criteria where both solutions are
  * Disjoint ($c_1 \text{ and } c_2 = \phi $)
  * Universal ($c_1 \text{ or } c_2 = U$)
* we can interpret solution set as : $c_1$ solution that includes first element in the subset, $c_2$ solution that doesn’t include the first element
* Solution for `[2, 3, 5]` becomes
  * $c_1$ : number of subset of `[3, 5]`
  * $c_2$ : any subsets of `[3, 5]` and append `2` to it
* Solution is based on Suffix Array
* Recurrence : `f(arr, 0, n-1) = f(arr, 1, n-1)` $\text{ or }$ `f(arr, 1, n-1) + {arr[0]}`
* Base Case: `f(arr, n-1, n-1) = { {}, {arr[n-1]}}`

````c++
vector<vector<int>> f(vector<int>& nums, int i, int r) {
  // Base Case
  if(i == r) {
    return {{}, {nums[r]}}
  }
  // Recursive Step
  // Get C2
  vector<vector<int>> c1 = f(nums, i+1, r);
  
  // Get C1
  vector<vector<int>> c2 = c1;
  for(int j = 0; j < c2.size(); j++)
    	c1[j].push_back(nums[i]);
  
  // combine both solution
  vector<vector<int>> res = c2;
  for(int j = 0; j < c1.size(); j++) {
    res.push_back(c1[j]);
  }
  return res;
}

vector<vector<int>> subsets(vector<int>& nums) {
  return f(nums, 0, nums.size() - 1);
}
````

* more space optimal approach is to track current recursion calls using `contribution` arr.

````c++
void f(vector<int>& nums, int i, int end, vector<int> contri, vector<vector<int>> & res){
    if(i == end){
        res.push_back(contri);
        
        contri.push_back(nums[end]);
        res.push_back(contri);
        return;
    }
    
    // Recursive
    // C2.
    f(nums,i+1,end, contri,res);
    
    // C1.
    // Contribution at this step is nums[i], ideally should be passed as reference
   	contri.push_back(nums[i]);
    f(nums,i+1,end, contri, res);
}
vector<vector<int>> subsets(vector<int>& nums){
    vector<vector<int>> res;
    
    // Implicit return
    f(nums, 0, nums.size()-1, {}, res);
    return res;
}
````

## Combination

Given an array = `[1, 2, 3, 4]` and `k=2`

Solution Set would be : `{[1,2] , [2,3], [3,4], [1,4] , [2,4], [1,3] }`

- Divide : Above problem can be divided into two chunks such that they contain `1` in c_1 and doesn’t contain `1` in c_2
- Represent : Suffix Array
- $c_2$ : all possible `k` sized subsets of `P(A[1...n-1], k)`
- $c_1$ : all possible `k-1` sized subsets of `P(A[l...n-1]) + [A[0]]` (`A[0]` is appended to solution)
- Recursion: `P(A, 0, n-1, k) = P(A, 1, n-1, k) + (P(A, 1, n-1, k-1)..A[0])`
- Base Case
  - `s > e`
    - `k = 0` : `{{}}`
    - `k > 0` : no solution
  - `s <= e`
    - `k = 0` : `{{}}`

````c++
vector<vector<int>> f(int start, int end, int k){
    // Base Case.
    if(k == 0)
        return {{}};
    if(start > end)
        return {};
    
    // Recursive Step
    // C2
    // Doesn't include the first element
    vector<vector<int>> c2 = f(start+1,end,k);

    // C1
    // Include the first element
    vector<vector<int>> temp = f(start+1, end, k-1);

    // Append the first element
    vector<vector<int>> c1 = temp;
    for(int i = 0; i < temp.size(); i++)
        c1[i].push_back(start+1);

    // Merge
    // Res is c1 U c2
    vector<vector<int>> res = c2;
    for(int i = 0 ; i < c1.size(); i++)
        res.push_back(c1[i]);
    return res;
}
vector<vector<int>> combine(int n, int k) {
    return f(0,n-1,k);
}
````

````c++
// space optimized solution
void f(int start, int end, int k, vector<int>& contri, vector<vector<int>> & res ){
    // Base Case.
    if(k == 0){
        res.push_back(contri);
        return ;
    }
    if(start > end)
        return ;

    // Recursive Step
    // C2. Doesn't include the first element
    f(start+1,end,k, contri, res);

    // C1. Include the first element
    contri.push_back(start+1);
    f(start+1, end, k-1,contri, res);
  	// restore recursion stack
  	contri.pop_back();		// notice now its even better then previous solutions
}
vector<vector<int>> combine(int n, int k) {
    vector<vector<int>> res;
    f(0,n-1,k,{},res);
    return res;
}
````

## Combination Sum

Representation : Suffix Array

* Divide
  * $c_1$ : not including first element :
  * $c_2$ : contains atleast one instance of first element
* Subproblems
  * $c_1$ : `P(A, 1, n-1, sum)`
  * $c_2$ : `P(A, 0, n-1, sum - A[0])` , same as original problem with one copy consumed
* Recurrence: `P(A, 0, n-1, sum)  = P(A, 1, n-1, sum) & P(A, 0, n-1, sum - A[0])`
* Base Cases
  * if `A` becomes empty
    * `sum > 0` : `{}`
    * `sum = 0` : `{{}}` | result
    * `sum < 0` : `{}`
  * `sum <= 0`
    * `sum == 0`: `{{}}` | result
    * `sum < 0` : `{}`

````c++
void f(vector<int>& arr, int start, int end, int target, vector<int>& contri, vector<vector<int>>& res){
    //Base Setps
    if(target == 0) {
        res.push_back(contri);
        return;
    }
    if(target < 0 || start > end)
        return;
    
    //solve c2
    //not including first element
    f(arr,start+1,end,target,contri,res);
    //solve c1 include first element atleast once
    contri.push_back(arr[start]);
    f(arr,start, end, target-arr[start],contri, res);
    contri.pop_back();
}
vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    vector<vector<int>> res;
    vector<int> contri;
    f(candidates, 0, candidates.size()-1,target, contri, res);
    return res;
}
````

* Above solution can be pruned further: `if (rem < k) return;` i.e. `if(end-start+1 < k) return;`

### Combination Sum - II

[LeetCode Link](https://leetcode.com/problems/combination-sum-ii/description/)

* NOTE: Only change is finite consumption of numbers. So out $c_2$ from previous solution changes as follows.

````c++
void f(vector<int>& candidates, int start, int end, int target,vector<int>& contri, vector<vector<int>>& res){
    //base step
    if(target == 0) {
        res.push_back(contri);
        return;
    }

    if( target < 0 || start > end) return;
    //recursive step

    //Not include the smallest ele. at all
    //find the first occurence of number > ar[start]
    int j = start + 1;
    while(j <= end && candidates[j] == candidates[start]) j++;

    f(candidates, j, end, target , contri , res);
    contri.push_back(candidates[start]);
    f(candidates,start + 1, end, target - candidates[start], contri, res);
    contri.pop_back();
}
vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
    vector<int> contri;
    vector<vector<int>> res;
    vector<int> suffix(candidates.size(),0);
    sort(candidates.begin(), candidates.end());
    f(candidates, 0 , candidates.size() -1 , target, contri, res);
    return res;
}
````

## Permutation

* This is somewhat what represent a `1D` DP. Representation of Solution using Suffix Array usually leads to constraint in 1 dimension.
* Ex - `[1, 2, 3]` Split Criteria : ?
  * `n` chunks of solutions, as
  * begins with 1 `{[1,3,2], [1,2,3]}`
  * begins with 2 `{[2,1,3], [2,3,1]}`
  * begins with 3 `{[3,1,2], [3,2,1]}`
* Subproblem : permutation calculation of the subarray removing that item. These are subsequences not suffix array problem.
* Representation:
  * Keeping a visited array will be helpful to represent the subproblems.
  * Or we can always send the element not to be included to be swapped with  the first element and that way we have a continuous suffix array as a subproblem

##### Keeping visited array (Optimized) 

````c++
void f(vector<int>& nums, vector<bool>& visited, vector<int>& contri, vector<vector<int>>& res){
    //Base Step
    //When everything is visited
    int i;
    for(i=0; i <nums.size(); i++){
        if(!visited[i])
            break;
    }
    if(i == nums.size()){
        res.push_back(contri);
        return;
    }
    //Recursive Step
    //Iterate over all possibilities for current position
    for( i = 0; i< nums.size(); i++)
    {
        //consider the ones that aren't visited
        if(!visited[i]) {
            //Passdown the contri
            //Try for this elt at the current position
            contri.push_back(nums[i]);
            visited[i] = true;
            f(nums,visited,contri, res);
            contri.pop_back(); // important step
            visited[i] = false;
        } 
    }
}
vector<vector<int>> permute(vector<int>& nums) {
    vector<bool> visited(nums.size(),false);
    vector<vector<int>> res;
    vector<int> contri;
    f(nums, visited, contri, res);
    return res;
}
````

Base Case Pruning

````c++
if(contri.size() == nums.size()){
    res.push_back(contri);
    return;
}
````

##### Swapping based solution (creates explicit suffix array)

````c++
void f(vector<int>& nums,int j, vector<int>& contri, vector<vector<int>>& res){
    //Base Step
    //When everything is visited
    if(j == nums.size()){
        res.push_back(contri);
        return;
    }

    //Recursive Step
    //Iterate over all possibilities for current position
    for(int i = j; i< nums.size(); i++)
    {
        //consider the ones that aren't visited
        //Passdown the contri
        //Try for this elt at the current position
        contri.push_back(nums[i]);
        swap(nums[j],nums[i]);
        f(nums,j+1,contri, res);
        //undo operation to maintain tree validity
        contri.pop_back();
        swap(nums[j],nums[i]);
    }
}
vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> res;
    vector<int> contri;
    f(nums, 0, contri, res);
    return res;
}
````

### Permutation Sequence

[k-th Permutation Sequence](https://leetcode.com/problems/permutation-sequence/description/)

* Naively Listing all permutations and then finding `kth` will give TLE in this case.
* We will perform DFS, and try to search that solution
* Ex - `[1, 2, 3]`
* Possibilities = `(123, 132,213, 231, 312,321)` and we have to give `kth` solution.
* There are 3 chunks, chunks including 1, 2, 3 as first number respectively
* now say its a ordered list, then we can easily say chunk size and the chunk in which this `k-th` number will lie would be

$$
\text{chunk id} = \frac{k-1}{(n-1)!}
$$

* then calculate offset how far this item is away from that `chunk_id`
* hmmm can we do that recursively ! yes :D

````c++
int fact(int n){
    int i, res = 1;
    for(i = 1; i<= n; i++)
        res = res * i;
    return res;
}
//Return the pos and unvisited number
int getNumber(vector<int>& visited, int pos){
    int count = 0;
    for(int i = 1; i<= 9; i++){
        if(visited[i]) continue;
        count++;
        if(count == pos)
            return i;
    }
    //NF-won't reach here
    return -1;
}
string getPermutation(int n, int k) {
    int i,chunk_id, pos, curr_digit;
    int copy_n = n;
    vector<int> visited(10,0); 
    string res = "";
    for( i = 1; i <= copy_n; i++){
        chunk_id = (k-1)/fact(n-1); 
        // get corresponding digit
        pos = chunk_id +1;
        curr_digit = getNumber(visited, pos);
        res = res + to_string(curr_digit);

        // mark visited
        visited[curr_digit] = 1;
        // update k and n;
        k = k - (chunk_id*fact(n-1));
        n--;
    }
    return res;
}
````

