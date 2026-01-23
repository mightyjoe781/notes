# Binary Search on Answers & 2D Search

## Problems on Searching an Answer

This is a very common type of pattern which used with Binary Search, Let's say solving a problem requires simulation on a range of input.

But If the input is a range, and response to that input is monotonic in nature, then practiv


### Find the SquareRoot of a Number

**Problem Statement:** You are given a positive integer n. Your task is to find and return its square root. If ‘n’ is not a perfect square, then return the floor value of `sqrt(n)`.

Root of a Number lies between `0-n` inclusive (A better bound would be `1-n//2`, To calculate for floor value of `sqrt` we can use following algorithm.

Predicate : `mid * mid <= n`, `T*F*` last T

```python

def floor_sqrt(n):

    if n < 2:
        return n

    lo, hi = 1, n // 2
    ans = 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if mid * mid <= n:
            ans = mid          # mid is a candidate
            lo = mid + 1       # try bigger
        else:
            hi = mid - 1       # try smaller

    return ans

```

For precision in floating point number, we can use following variant.

```python

def sqrt(n):
    lo, hi = 0, n
    while hi - lo > 1e-8:
        # don't use +1, as it moves the float way too ahead
        mid = lo + (hi - lo) / 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo
```

### Find the Nth root of a number using Binary Search

**Problem Statement:** Given two numbers N and M, find the Nth root of M. The nth root of a number M is defined as a number X when raised to the power N equals M. If the 'nth root is not an integer, return -1.

Its quite similar above integer variant only, `mid` calculation is change a bit for comparisons.

```python

# Store result of mid^n
ans = 1
for _ in range(n):
    ans *= mid
    if ans > m:
        break

```

### Kako Eating Bananas

Here Kako can eat at rate of 1 banana or `max(piles)` according to constraint.

```python

from math import ceil
def minEatingSpeed(piles: List[int], h: int) -> int:
    l, r = 1, max(piles)

    def pred(rate):
        return sum((pile + rate - 1) // rate for pile in piles) <= h

    while l < r:
        m = l + (r - l)//2
        if pred(m): # FFFFTTTTT, first T
            r = m
        else:
            l = m + 1
    
    return l

```

### Minimum Number of Days to Make `m` Bouquets

You are given an integer array `bloomDay`, an integer `m` and an integer `k`.

You want to make `m` bouquets. To make a bouquet, you need to use `k` **adjacent flowers** from the garden.

The garden consists of `n` flowers, the `ith` flower will bloom in the `bloomDay[i]` and then can be used in **exactly one** bouquet.

Return _the minimum number of days you need to wait to be able to make_ `m` _bouquets from the garden_. If it is impossible to make m bouquets return `-1`.

Making bouquets part is simulated here

```python

def minDays(A, m, k):
    if m * k > len(A): return -1
    left, right = 1, max(A)
    while left < right:
        mid = (left + right) // 2
        flow = bouq = 0
        for a in A:
            flow = 0 if a > mid else flow + 1
            if flow >= k:
                flow = 0
                bouq += 1
                if bouq == m: break
        if bouq == m:
            right = mid
        else:
            left = mid + 1
    return left

```

### Find the Smallest Divisors

Exactly Similar to Koko Eating Banana's

```python
l, r = 1, int(1e6)

def pred(div):
    return sum(math.ceil(num/div) for num in nums) <= threshold
```

### Capacity To Ship Packages Within D Days

A conveyor belt has packages that must be shipped from one port to another within `days` days.

The `ith` package on the conveyor belt has a weight of `weights[i]`. Each day, we load the ship with packages on the conveyor belt (in the order given by `weights`). We may not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within `days` days.

```python

def shipWithinDays(weights: List[int], days: int) -> int:
    l, r = max(weights), sum(weights)

    def pred(W):
        days_used = 1
        current = 0

        for wt in weights:
            if current + wt > W:
                days_used += 1
                current = 0
            current += wt
        return days_used <= days

    while l < r:
        m = l + (r - l)//2
        if pred(m):
            r = m
        else:
            l = m + 1

    return l

```

### Aggressive Cows

**Problem Statement:** You are given an array **'arr'** of size **'n'** which denotes the position of stalls. You are also given an integer **'k'** which denotes the number of aggressive cows.  
You are given the task of assigning stalls to **'k'** cows such that the minimum distance between any two of them is the maximum possible. Find the maximum possible minimum distance.

```python

def aggressive_cows(arr, cows):
    n = len(arr)

    # sort stalls
    arr.sort()

    def can_place(dist):
        # first cow at stall-1
        cnt, prev = 1, arr[0]

        for i in range(1, n):
            if arr[i] - prev >= dist:
                cnt += 1
                prev = arr[i]

        return cnt >= cows

    # dist(1, max - min)
    l, r = 1, arr[-1] - arr[0]
    while l < r:
        mid = l + (r - l + 1) // 2
        print(l, mid, r)
        if can_place(mid):  # TTTTFFF, last T
            l = mid
        else:
            r = mid - 1

    return l

```

### Kth Missing Number ⭐

**Problem Statement:** You are given a strictly increasing array ‘vec’ and a positive integer 'k'. Find the 'kth' positive integer missing from 'vec'.

```
Input Format: vec[]={4,7,9,10}, k = 1
Result: 1
Explanation: The missing numbers are 1, 2, 3, 5, 6, 8, 11, 12, ……, and so on. Since 'k' is 1, the first missing element is 1.
```

In this problem we cannot directly apply binary search on the answer space, as we cannot assure which missing number has the possibility of being the `kth` missing number.

Its more like a combination of two pointer and binary search, So set `l` and `r` to be boundaries of `arr` and try to find `mid`

```
Acutal : 4 7 9 10
Index  : 0 1 2 3
Correct: 1 2 3 4

Let say mid point to 7, then numbers missing till 7 ~ 7 - 2 = 5
for 9 ~ 9 - 3 = 6
for 10 - 4 = 6

Notice this difference is monotonically increasing

```

```python

def main(nums, k):
    l, r = 0, len(nums)

    while l < r:
        mid = l + (r - l) // 2
        missing = nums[mid] - (mid + 1)

        if missing < k:
            l = mid + 1
        else:
            r = mid

    # l is number of elements before kth missing
    return k + l

```

### Book Allocation Problem


Here `l=max(arr)` ~ because atleast 1 book needs to be assigned to a student, and `r=sum(arr)`, giving all books to 1 student,


```python

def allocateBooks(self, pages, m):
    n = len(pages)
    if m > n:
        return -1   # not enough books

    def can_allocate(max_pages):
        students = 1
        curr_pages = 0

        for p in pages:
            if curr_pages + p <= max_pages:
                curr_pages += p
            else:
                students += 1
                curr_pages = p

        return students <= m

    l, r = max(pages), sum(pages)

    while l < r:
        mid = l + (r - l) // 2
        if can_allocate(mid):
            r = mid
        else:
            l = mid + 1

    return l


```

### Split Array Largest Sum

So this problem is similar to previous one where we guessed the answer for possible division of books for students, here instead of book with pages its an array with values.

```python

def splitArray(nums: List[int], k: int) -> int:

    def can_split(max_sum):
        groups = 1
        curr = 0
        for num in nums:
            if curr + num <= max_sum:
                curr += num
            else:
                groups += 1
                curr = num
        return groups <= k   # valid if we can split into k or fewer groups

    l, r = max(nums), sum(nums)

    while l < r:
        mid = l + (r - l) // 2
        if can_split(mid):  #### FFFFFTTTT, first T
            r = mid          # try smaller max sum
        else:
            l = mid + 1      # need larger max sum

    return l

```

### Painters Partition Problem

**Problem Statement:** Given an array/list of length ‘N’, where the array/list represents the boards and each element of the given array/list represents the length of each board. Some ‘K’ numbers of painters are available to paint these boards. Consider that each unit of a board takes 1 unit of time to paint. You are supposed to return the area of the minimum time to get this job done of painting all the ‘N’ boards under the constraint that any painter will only paint the continuous sections of boards.

Exactly Same Code as Above for solution

### Minimize Maximum Distance between Gas Station

**Problem Statement:** You are given a sorted array ‘arr’ of length ‘n’, which contains positive integer positions of ‘n’ gas stations on the X-axis. You are also given an integer ‘k’. You have to place 'k' new gas stations on the X-axis. You can place them anywhere on the non-negative side of the X-axis, even on non-integer positions. Let 'dist' be the maximum value of the distance between adjacent gas stations after adding k new gas stations. Find the minimum value of ‘dist’.

```
Input Format: N = 5, arr[] = {1,2,3,4,5}, k = 4
Result: 0.5
Explanation: One of the possible ways to place 4 gas stations is {1,1.5,2,2.5,3,3.5,4,4.5,5}. Thus the maximum difference between adjacent gas stations is 0.5. Hence, the value of ‘dist’ is 0.5. It can be shown that there is no possible way to add 4 gas stations in such a way that the value of ‘dist’ is lower than this.
```

So We can place *gastations* between `0-n` anywhere, even fractional points. This will be binary search over this range.

```python

def main(nums, k):
    def can_place(D):
        needed = 0
        for i in range(len(nums) - 1):
            gap = nums[i + 1] - nums[i]
            needed += int(gap / D)
        return needed <= k

    l, r = 0.0, nums[-1] - nums[0]

    while r - l > 1e-6:
        m = l + (r - l) / 2
        if can_place(m):
            r = m  # try smaller max distance
        else:
            l = m  # need larger distance

    return r

```


### Median of Two Sorted Arrays of Different Size ⭐

Given two sorted arrays arr1 and arr2 of size m and n respectively, return the median of the two sorted arrays. The median is defined as the middle value of a sorted list of numbers. In case the length of the list is even, the median is the average of the two middle elements.

Instead of merging arrays, we **partition** them such that:

```
Left half contains exactly half the elements
All elements in left half ≤ all elements in right half
```

If total length is

- odd - median ~ Max(left side)
- even - median ~ average(max(left), min(right))

![](assets/Pasted%20image%2020260122231556.png)

```python

def findMedianSortedArrays(A, B):
    # ensure A is smaller
    if len(A) > len(B):
        A, B = B, A

    n, m = len(A), len(B)
    low, high = 0, n

    while low <= high:
        i = (low + high) // 2
        j = (n + m + 1) // 2 - i

        A_left  = A[i-1] if i > 0 else float('-inf')
        A_right = A[i]   if i < n else float('inf')
        B_left  = B[j-1] if j > 0 else float('-inf')
        B_right = B[j]   if j < m else float('inf')

        if A_left <= B_right and B_left <= A_right:
            # correct partition
            if (n + m) % 2 == 0:
                return (max(A_left, B_left) + min(A_right, B_right)) / 2
            else:
                return max(A_left, B_left)

        elif A_left > B_right:
            high = i - 1
        else:
            low = i + 1

```

### Kth Element in Two Sorted Arrays

Similar to above question but asks for `kth` largest number, rather than median

Change Bounds to following,

```python
    # Apply binary search
    low = max(0, k - n)
    high = min(k, m)
```

## Binary Search in 2D Grids

### Find the row with maximum number of 1's

**Problem Statement:** You have been given a non-empty grid ‘mat’ with 'n' rows and 'm' columns consisting of only 0s and 1s. All the rows are sorted in ascending order. Your task is to find the index of the row with the maximum number of ones. Note: If two rows have the same number of ones, consider the one with a smaller index. If there's no row with at least 1 zero, return -1

Simple straightforward questions

```python

from bisect import bisect_left
def main(mat):
    n, m = len(mat), len(mat[0])

    ans, max_cnt = 0, 0
    for i in range(n):
        cnt = m - bisect_left(mat[i], 1)
        if cnt > max_cnt:
            ans = i
            max_cnt = cnt

    if max_cnt == 0:
        return -1
    return ans

```

### Search in a Sorted 2D Matrix

**Problem Statement:** You have been given a 2-D array **'mat'** of size **'N x M'** where **'N'** and **'M'** denote the number of rows and columns, respectively. The elements of each row are sorted in non-decreasing order. Moreover, the first element of a row is greater than the last element of the previous row (if it exists). You are given an integer **‘target’**, and your task is to find if it exists in the given 'mat' or not.

So this of this as a single long array, where

```python

def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1

    while lo <= hi:
        mid = (lo + hi)//2

        r, c = mid//n, mid%n
        if matrix[r][c] == target: ## TTTTFFFF, last T
            return True
        elif matrix[r][c] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return False

```

### Search in row & column sorted Matrix

**Problem Statement:** You have been given a 2-D array 'mat' of size 'N x M' where 'N' and 'M' denote the number of rows and columns, respectively. The elements of each row and each column are sorted in non-decreasing order. But, the first element of a row is not necessarily greater than the last element of the previous row (if it exists). You are given an integer ‘target’, and your task is to find if it exists in the given 'mat' or not.

One naive approach is to do binary search in both array

```python

def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
    
    m, n = len(matrix), len(matrix[0])

    i, j = 0, n - 1

    while i < m and j >= 0:
        if matrix[i][j] == target:
            return True
        if matrix[i][j] > target:
            j -= 1
        else:
            i += 1

    return False

```

### Median of Row Wise Sorted Matrix

Given a row-wise sorted matrix of size `M*N`, where M is no. of rows and N is no. of columns, find the median in the given matrix.  
Note: `M*N` is odd.

We can solve this problem using searching the answer technique

![](assets/Pasted%20image%2020260122235023.png)


```python

import bisect

def main(matrix):
    n, m = len(matrix), len(matrix[0])

    def count_le(x):
        cnt = 0
        for row in matrix:
            cnt += bisect.bisect_right(row, x)
        return cnt

    lo = min(row[0] for row in matrix)
    hi = max(row[-1] for row in matrix)

    need = (n * m + 1) // 2   # position of median

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if count_le(mid) < need:
            lo = mid + 1
        else:
            hi = mid

    return lo

```

### Find a Peak Element II

A **peak** element in a 2D grid is an element that is **strictly greater** than all of its **adjacent** neighbors to the left, right, top, and bottom.

Given a **0-indexed** `m x n` matrix `mat` where **no two adjacent cells are equal**, find **any** peak element `mat[i][j]` and return _the length 2 array_ `[i,j]`.

You may assume that the entire matrix is surrounded by an **outer perimeter** with the value `-1` in each cell.

You must write an algorithm that runs in `O(m log(n))` or `O(n log(m))` time.

![](assets/Pasted%20image%2020260122235135.png)

Instead of check every cell $O(mn)$ we can binary search on columns or rows. In each chosen column, we need to find row index of the maximum element

Compare element with its left and right neighbors.
Move the search direction based on where a bigger neighbor exists, Having a bigger neighbor guarantees peak exists in that direction.

```python

def findPeakGrid(mat):
    m, n = len(mat), len(mat[0])
    l, r = 0, n - 1

    while l <= r:
        mid = (l + r) // 2

        # find row index of max element in mid column
        max_row = 0
        for i in range(m):
            if mat[i][mid] > mat[max_row][mid]:
                max_row = i

        mid_val = mat[max_row][mid]
        left = mat[max_row][mid - 1] if mid - 1 >= 0 else -1
        right = mat[max_row][mid + 1] if mid + 1 < n else -1

        if mid_val > left and mid_val > right:
            return [max_row, mid]
        elif left > mid_val:
            r = mid - 1
        else:
            l = mid + 1

```

Notice how movement is towards a strictly larger neighbor always, Since grid is surrounded by -1, you won't move forever, eventually landing on a cell grater than all 4 neighbors

Same Idea as 1D Peak Element, Optimization over Monotonic Direction.