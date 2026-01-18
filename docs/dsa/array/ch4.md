# Subarrays & Subsequences

* core concepts in problems related to array and string problems
* Its important to understand the difference between them

## Subarrays

* A **subarray** is a contiguous part of an array.
* Formed by selecting a continuous segment `(A[l..r])` where `(0 <= l <= r < n)`

* number of subarrays in an array of `n` size : `n(n+1)/2`
* order of element is preserved and contiguous
* sliding window & prefix sums are important tools to solve subarray related problems

### Common Problems

* Maximum Sum Subarray (Kadane’s Algorithm)
* Counting Subarrays with Certain sum or property
* Longest Subarray with Constraint

### Examples

```c++
// Kadane's Algorithm
int maxSubArray(vector<int>& nums) {
	int n = nums.size(), i ,res = INT_MIN;
	int prev = 0, curr;
  for(i = 1; i <= n; i++){
      curr = max(prev + nums[i-1], nums[i-1]);
      res = max(res,curr);
      prev = curr;
  }
  return res; 
}

// Alternate Implementation
int maxSubArray(vector<int>& nums) {
	int n = nums.size(), i ,res = INT_MIN;
	int sum = 0;
  for(i = 0; i <= n; i++){
		sum += nums[i];
    res = max(res, sum);
    if(sum < 0) sum = 0; 
    // when sum drops negative we will not find better solution by adding more numbers, better to reset
  }
  return res; 
}

// NOTE: Both Implementation works regardless of negative numbers
```


## Subsequences

* sequence derived from the array by deleting zero or more elements without changing the order of remaining elements
* not necessarily contiguous

* number of subsequences in an array of size `n` is `2^n`
* usually these problems are optimally solvable by using DP

### Common Problems

* Longest Increasing Subsquence (LIS)
* Counting subsequences with certain properties
* Subsequences sum problems

```c++
// Example with DP
int lengthOfLIS(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, 1);
    int maxLength = 1;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[i] > nums[j]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
        maxLength = max(maxLength, dp[i]);
    }
    return maxLength;
}
```



## Problems

Subarrays

Pre-requisite : Prefix and Sliding Window

* Longest Subarray with Given Sum
* Count of Subarrays with Given Sum
* Subarray with Max Product
* Subarray with `k` Distinct Elements
* Longest Ascending(or Descending) Subarray
* Longest Palindromic Subarray
* Fixed-Length Max/Min Subarray

Subsequences

Prerequisite : Recursion, DP

* LIS (Longest Increasing Subsequence)
* LCS (longest common Subsequences)
* Count Subsequences with Given Property
* Subsequence Matching
* Distinct Subsequences


## Solution to Some Problems

### Maximum Product Subarray

[Link]([Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/))

Given an integer array `nums`, find a that has the largest product, and return _the product_.

Its a variant of Kadane's algorithm.

```python

def maxProduct(nums: List[int]) -> int:
    prefix, suffix, max_so_far = 0, 0, float('-inf')
    for i in range(len(nums)):
        prefix = (prefix or 1) * nums[i]
        # The expression ~i is equivalent to -i - 1
        suffix = (suffix or 1) * nums[~i]
        max_so_far = max(max_so_far, prefix, suffix)
    return max_so_far

```