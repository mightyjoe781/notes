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

### Absolute Diff less than or Equal to Limit

Given an array of integers `nums` and an integer `limit`, return the size of the longest **non-empty** subarray such that the absolute difference between any two elements of this subarray is less than or equal to `limit`

```

Input: nums = [8,2,4,7], limit = 4
Output: 2 
Explanation: All subarrays are: 
[8] with maximum absolute diff |8-8| = 0 <= 4.
[8,2] with maximum absolute diff |8-2| = 6 > 4. 
[8,2,4] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4,7] with maximum absolute diff |8-2| = 6 > 4.
[2] with maximum absolute diff |2-2| = 0 <= 4.
[2,4] with maximum absolute diff |2-4| = 2 <= 4.
[2,4,7] with maximum absolute diff |2-7| = 5 > 4.
[4] with maximum absolute diff |4-4| = 0 <= 4.
[4,7] with maximum absolute diff |4-7| = 3 <= 4.
[7] with maximum absolute diff |7-7| = 0 <= 4. 
Therefore, the size of the longest subarray is 2.

```

A simple brute force solution will be to generate all subarrays, which will be quadratic time.
A simpler solution is to run a sliding window over the array keeping track of the minimum and maximum numbers in this window.

A Simpler solution using Priority Queue (Heaps) : Time : $O(n\log n)$

```python

import heapq
def longestSubarray(nums: List[int], limit: int):
    maxq, minq = [], []
    res = i = 0

    for j, a in enumerate(nums):
        heapq.heappush(maxq, [-a, j])
        heapq.heappush(minq, [a, j])

        # shrink the window
        while -maxq[0][0] - minq[0][0] > limit:
            i = min(maxq[0][1], minq[0][1]) + 1
            while maxq[0][1] < i: heapq.heappop(maxq)
            while minq[0][1] < i: heapq.heappop(minq)
        
        res = max(res, j - i + 1)
    
    return res

```

A more simpler optimization is to use Monotonic Queue & Sliding Window to keep track of the Maximum and Minimum both in the same window.

```python

from collections import deque

def longestSubarray(nums: List[int], limit: int):
    maxd, mind = deque(), deque()
    l = 0

    for r in range(len(nums)):
        v = nums[r]

        # maintain decreasing max deque
        while maxd and v > maxd[-1]:
            maxd.pop()

        # maintain increasing min deque
        while mind and v < mind[-1]:
            mind.pop()

        maxd.append(v)
        mind.append(v)

        # shrink window if invalid
        if maxd[0] - mind[0] > limit:
            if maxd[0] == nums[l]:
                maxd.popleft()
            if mind[0] == nums[l]:
                mind.popleft()
            l += 1

    return len(nums) - l

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

Pre-requsite : Recursion, DP

* LIS (Longest Increasing Subsequence)
* LCS (longest common Subsequences)
* Count Subsequences with Given Property
* Subsequence Matching
* Distinct Subsequences
