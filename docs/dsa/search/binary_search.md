# Binary Search

Binary search is a powerful algorithm for locating an element or solving optimization problems within a search space where the data meets specific criteria. The following is a concise summary and framework for applying binary search effectively:

Key Concepts

1. **Search Space:** 
   * A set of elements, such as indices, numbers, or a conceptual range, that can be ordered or partitioned. Examples include sorted arrays, monotonic functions, and intervals.

2. **Predicate (p(x))**: 
   * A boolean function (true/false) applied to items in the search space.
   * The predicate determines the behavior of the elements:
     * `F*T*`: false, false, false, true, true (transition from F to T).
     * `T*F*`: true, true, true, false, false (transition from T to F).
3. Applicability of Binary Search:
   * Binary Search is applicable if:
     * The search space is monotonic w.r.t. the predicate.
     * For `F*T*`: All F precede T.
     * For `T*F*`: All T precede F.
4. Goals of Binary Search:
   * Find the last F or the first T in `F*T*`.
   * Find the last T or the first F in `T*F*`.

## Framework to Solve Binary Search Problem

1. **Define the Search Space:**
   * Decide whether it is a range ([lo, hi]) or a collection (like an array).

2. **Define the Predicate (p(x)):**
   * Write a condition that transitions at a key point.

Example: For a sorted array and a target x, use p(x) = (arr[mid] >= target) for ``F*T*`.

3. **Decide the Goal:**
   * Find **first T**, **last F**, **last T**, or **first F** based on the problem.

4. **Write Binary Search:**
   * Use the appropriate loop (while(lo < hi) or while(lo <= hi)) and mid-point calculation:
     * low_mid: mid = lo + (hi - lo) / 2 (default).
     * high_mid: mid = lo + (hi - lo + 1) / 2 (if focusing on higher mid).

## Pseudo Codes for C++

### For `F*T*` (Find Last F/First T)

````c++
int lastF(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;  // Use high_mid
        if (p(mid))
            hi = mid - 1;  // Move left
        else
            lo = mid;      // Move right
    }
    return (!p(lo)) ? lo : -1;  // Check and return
}
````

````c++
int firstT(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;  // Use low_mid
        if (p(mid))
            hi = mid;      // Move left
        else
            lo = mid + 1;  // Move right
    }
    return (p(lo)) ? lo : -1;  // Check and return
}
````

### For `T*F*` (Find Last T/First F)

````c++
int lastT(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;  // Use high_mid
        if (p(mid))
            lo = mid;      // Move right
        else
            hi = mid - 1;  // Move left
    }
    return (p(lo)) ? lo : -1;  // Check and return
}
````

````c++
int firstF(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;  // Use low_mid
        if (p(mid))
            lo = mid + 1;  // Move right
        else
            hi = mid;      // Move left
    }
    return (!p(lo)) ? lo : -1;  // Check and return
}
````

### **Tips to Remember**

1. **Predicate**: Design it to divide the search space into `F*T*` or `T*F*`.

2. **Mid Calculation**:
   * **low_mid**: lo + (hi - lo) / 2 (default for most cases).
   * **high_mid**: lo + (hi - lo + 1) / 2 (if skipping mid element is required).

3. **Focus**: Adjust lo or hi based on whether you move left or right.

4. **Post-Loop Check**: Always verify the result before returning to avoid off-by-one errors.

Binary Search simplifies problems when you clearly define the search space and the predicate.

### Overflow Safe Binary Search Template

````c++
int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;  // Overflow-safe
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
````

## Pseudo Code For Python Bisect

Python offers two function : *bisect.bisect_left* and *bisect.bisect_right* (same as *bisect.bisect*)

### bisect.bisect_left

```python

bisect.bisect_left(a, x, lo=0, hi=len(a), *, key=None)

```

Locates the insertion point of x in a to maintain sorted order. If x is already present then it returns insertion point (*before to left*) of existing entries for the number x.

`ip : insertion point`

Array is divided into two parts, `all(elem < x for elem in a[lo : ip])` is true, and `all(elem >= x for elem in a[ip: hi])`

key function can be used to extract a comparison key from each element in the array.

### bisect.bisect_right

```python

bisect.bisect_right(a, x, lo=0, hi=len(a), *, key=None)

```

Locates the insertion point of x in a to maintain sorted. If x is already present then it return the insertion point (*after to right*) of existing entries for x

Array is divided into two slices such that, `all(elem <= x for elem in a[lo:ip])` is true, and `all(elem > x for elem in a[ip: hi])` is true for right slice.

Other useful python functions

- `bisect.insort_left` : Insert x in a in sorted manner, using `bisect.bisect_left`
- `bisect.insort_right` : Insert x in a in sorted manner, using `bisect.bisect_right`

```python

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

```

### Overflow Safe implementation

```python

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        # Use safer mid calculation to prevent overflow in other languages
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


```

## Problems on Binary Search

Problem on Binary Search can be divided into two types,

- Binary Search on some sorted list
- Binary Search on the Answers to brute force them : Best Example ~ Aggressive Cows Problem, Gas Tank Problem

## Basic Problems

### Implement Lower and Upper Bound

```python

def lower_bound(self, arr, x):
    low, high = 0, len(arr) - 1     # Search range
    ans = len(arr)                  # Default value if not found

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] >= x:
            ans = mid               # Store possible answer
            high = mid - 1          # Move to the left
        else:
            low = mid + 1           # Move to the right
    return ans
    
# Binary search to find upper bound
def upper_bound(self, arr, x):
    low, high = 0, len(arr) - 1
    ans = len(arr)  # Default to length if no element > x

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] > x:
            ans = mid      # Store current mid as answer
            high = mid - 1 # Search left
        else:
            low = mid + 1  # Search right
    return ans

```

### Search in Rotated Sorted Array

There is an integer array `nums` sorted in ascending order (with **distinct** values).

Prior to being passed to your function, `nums` is **possibly left rotated** at an unknown index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (**0-indexed**). For example, `[0,1,2,4,5,6,7]` might be left rotated by `3` indices and become `[4,5,6,7,0,1,2]`.

Given the array `nums` **after** the possible rotation and an integer `target`, return _the index of_ `target` _if it is in_ `nums`_, or_ `-1` _if it is not in_ `nums`.

A naive approach is to directly find the pivot point and then run two binary search on each partition, this can be done in $O(\log n)$. But this approach is not clean.

This shows how we can do binary search in single loop.

```python

def search(nums: List[int], target: int) -> int:

    l, r = 0, len(nums) - 1

    while l <= r:
        mid = (l + r)//2

        if nums[mid] == target:
            return mid

        # left sorted array 
        if nums[l] <= nums[mid]:
            if target > nums[mid] or target < nums[l]:
                l = mid + 1
            else:
                r = mid - 1
        
        # right sorted array
        else:
            if target < nums[mid] or target > nums[r]:
                r = mid - 1
            else:
                l = mid + 1
        
    return -1

```

Solution for second part where, we are allowed to have duplicates

```python

def search(nums: List[int], target: int) -> bool:

    l, r = 0, len(nums) - 1

    while l < r:
        mid = (l + r)//2

        if nums[mid] == target:
            return True

        if nums[mid] > nums[r]: # decreasing edge
            if nums[mid] > target and nums[l] <= target:
                r = mid
            else:
                l = mid + 1
        elif nums[mid] < nums[r]: # increasing edge
            if nums[mid] < target and nums[r] >= target:
                l = mid + 1
            else:
                r = mid
        else:
            r -= 1
    
    return nums[l] == target
```


### Find Minimum in Rotated Sorted Array

![](assets/Pasted%20image%2020260121093234.png)

Given the sorted rotated array `nums` of **unique** elements, return _the minimum element of this array_.

```python


def findMin(self, nums: List[int]) -> int:
    if not nums: return 0

    l, r = 0, len(nums) - 1
    while l < r:

        mid = l + (r - l)//2
        if nums[0] > nums[mid]:
            r = mid
        else:
            l = mid + 1

    if nums[0] < nums[l]:
        return nums[0]

    return nums[l]
    

```

NOTICE how its different than above scenarios.
### Find Rotation applied to Array

**Problem Statement:** Given an integer array arr of size N, sorted in ascending order (with distinct values). Now the array is rotated between 1 to N times which is unknown. Find how many times the array has been rotated.

Solution : Find the minimum element, and if its not in place, then the distance away from 0-index is the rotation applied on the array.

### Single Element on Sorted Array

You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once.

Return _the single element that appears only once_.

Although a straightforward solution is to xor all numbers, but we are supposed to write $O(\log n)$ solution as input is already sorted.

Suppose array is `[1, 1, 2, 2, 3, 3, 4, 5, 5]`

each element's duplicate and itself takes even and odd place, in order before the single number, as soon as single number occurs rest of the numbers occur in reverse order i.e. odd place first and even place later.

```python

def singleNonDuplicate(nums: List[int]) -> int:

    # if mid ~ even, then its duplicate should be next index
    # if mid ~ odd, then its duplicate should be prev index

    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if (
            (mid%2 == 0 and nums[mid] == nums[mid+1]) or 
            (mid%2 == 1 and nums[mid] == nums[mid-1])
        ):
            l = mid + 1
        else:
            r = mid

    return nums[l]

```

### Find Peak Element

```python

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r) >> 1

            # arr[m] < arr[m+1] # peak guaranteed
            # TTTTFFF ~ first F
            if nums[mid] < nums[mid+1]: # rising the peak
                l = mid + 1
            else:
                r = mid

        return l

```

