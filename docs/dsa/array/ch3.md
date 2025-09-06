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

