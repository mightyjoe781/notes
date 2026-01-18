# Prefix Sums & Difference Arrays

Prefix sums and difference arrays are fundamental tools to efficiently handle range queries and range updates on arrays. They help reduce time complexity from $(O(n \times q))$ to $(O(n + q))$ for many problems involving cumulative computations.

## Prefix Sums

### Concept

* Prefix sum array stores cumulative sums of elements up to each index
* For an array `A` of length `n`, prefix sums array `P` is defined as

```python
P[0] = A[0]
for i in range(1, n):
  P[i] = P[i-1] + A[i]
```

* To calculate sum in range `A[l...r]`

```python
def range_sum(P, l, r):
  if l == 0: return P[r]
  return P[r] - P[l-1]
```

* Applications
    * Efficient Range Sum Queries
    * Counting Elements satisfying conditions in ranges
    * Solving problems involving sum of subarrays

## Difference Arrays

### Concept

* A difference array *D* for an array A stores the difference between consecutive elements
* Allows efficient Range Updates: increment all elements in range `[l..r]` by a value `val` in O(1)
* After all updates, original array can be reconstructed by prefix sum of *D*

````python
D[0] = A[0]
for i in range(1, n):
  D[i] = A[i] - A[i-1]
````

### Range Update

* To add a `val` to `A[l...r]`
    * increment `D[l]` by `val`
    * decrement `D[r+1]` by `val` if `r + 1 < n`

```python
D[l] += val
if r + 1 < D.size():
  D[r+1] -= val
```

* Reconstruction
    * Prefix sum array of difference array is exactly same as original array

## Problems

Prefix Sum

* Subarray Sum Equals K (560)
* Range Sum Queries (303)
* [Equilibrium Index](https://www.geeksforgeeks.org/problems/equilibrium-point-1587115620/1)
* Maximum Subarray Sum : Kadane’s Algorithm
* Minimum Size Subarray Sum: Prefix sum with sliding window/binary search
* Counting Zero-Sum Subarrays (325) : Track occurrences of prefix sums using hash maps to count subarrays summing to zero

Difference Array

* Range Updates with Add/Subtract
* **Car Pooling Problem** (1094) : Model pickups/drop-offs using difference arrays
* **Corporate Flight Bookings** (1109) : Apply seat reservations to flight segments and output final seat counts. Difference arrays handle bulk updates efficiently
* Range Addition (370)
* Meeting Room II 

Hybrid Problems

* Product of Array Except Self (238)
* Longest Turbulent Subarray (978)
* Find Pivot Index (724)


## Prefix Sum Problems

### Counting Zero-Sum Subarrays

Give a subarray : 

$(a[i] + a[i+1] ... a[j]) = \Sigma_{k \in 0 \le i < j < n} a[k] = \Sigma_{k \in [0, j]} a[k] - \Sigma_{k \in [0, i-1]} a[k] = prefix[j] - prefix[i] = 0$

So we have to find how many times we have encountered the specific prefix - 1 (for the current prefix)

```python

from collections import defaultdict
def findSubarray(arr):
    
    mp = defaultdict(lambda: 0)
    mp[0] = 1
    
    res = 0
    s = 0
    
    for v in arr:
        s += v # prefix sum
        mp[s] += 1
        res += mp[s] - 1 # this is subarray counting trick during enumeration
        # quite common in window operations
    
    return res
```

NOTE: Repeat above problem, but now find longest subarray where sum is zero.
### Subarray Sum Equals K

**Problem Statement:** Given an array nums of size n and an integer k, find the length of the longest sub-array that sums to k. If no such sub-array exists, return 0.

Solved Using Sliding Window if length of longest subarray is asked, but here it is asking subarray sum equals k, and their count.

Similar to above problem, now we search `mp[s-target] - 1` in the map

```python

from collections import defaultdict
def subarraySum(nums: List[int], k: int) -> int:

    mp = defaultdict(lambda: 0)
    mp[0] = 1
    
    res = 0
    s = 0
    
    for v in nums:
        s += v # prefix sum
        if s - k in mp:
            res += mp[s - k]
        mp[s] += 1
    return res

```

### Count the number of subarrays with given xor K

**Problem Statement:** Given an array of integers A and an integer B. Find the total number of subarrays having bitwise XOR of all elements equal to k.

A prefix XOR at index `i`, represents the XOR of all elements up to `i`

```
subarray_xor(i, j) = prefix_xor(j) - prefix_xor(j)

```

We can store its frequency in a map, and solve using above code in Linear Time.

## Difference Array



## Hybrid Problems

### Product of Array Except Self

This is more like prefix product problem, 

A naive approach to this problem would be to just directly multiplying all numbers of the array, then dividing the current number, but that would work only if array doesn't contain any zeroes at all.

![](assets/Pasted%20image%2020260117173824.png)

```python
def productExceptSelf(self, nums: List[int]) -> List[int]:
    n = len(nums)

    prefix = [1] * len(nums)
    suffix = [1] * len(nums)

    prefix[0] = nums[0]
    suffix[n-1] = nums[n-1]

    for i in range(1, n):
        prefix[i] = nums[i] * prefix[i-1]

    for i in range(n-2, -1, -1):
        suffix[i] = nums[i] * suffix[i+1]
    
    res = [1] * len(nums)
    res[0] = suffix[1]
    res[n-1] = prefix[n-2]

    for i in range(1, n-1):
        res[i] = prefix[i-1] * suffix[i+1]
    
    return res

```

A further optimization can be storing suffix product information into the array itself.




