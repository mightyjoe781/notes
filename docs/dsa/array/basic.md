# Array Problems


## 1D Array Problems

### Second Smallest and Second Largest Element

Brute Force Approach : Sort and return `arr[1]` or `arr[-2]`
Optimal Approach : Keep Track of the of both results

```python

def secondLargest(nums):

    if n < 2:
        return -1
    
    largest = float('-inf')
    second_largest = float('-inf')
    for num in nums:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num
    
    return second_largest

```

### Check If Array is Sorted & Rotated

Given an array `nums`, return `true` _if the array was originally sorted in non-decreasing order, then rotated **some** number of positions (including zero)_. Otherwise, return `false`.

```
Input: nums = [3,4,5,1,2]
Output: true
Explanation: [1,2,3,4,5] is the original sorted array.
```

Brute Force Approach is just to consider rotating all possible configuration for this and then finding if array is sorted.

Another approach is sort the copy of the array and then compare with all offsets.

Optimal Approach :

If sorted array is rotated, so at some point in the array where minimum of the array exists, is the rotation point, and from there we can assume everything is gonna be sorted.

![](assets/Pasted%20image%2020260117141217.png)

Result is that in a sorted and rotated array number of inversions is *at-max* 1 in a cyclic traversal of the array (n elements).

```python

def check(self, nums: List[int]) -> bool:
    n = len(nums)
    if n <= 1:
        return True
    
    inv_cnt = 0

    for i in range(1, n):
        if nums[i] < nums[i-1]:
            inv_cnt += 1
    
    # wrap around check
    if nums[0] < nums[n-1]:
        inv_cnt += 1
    
    return inv_cnt <= 1

```

### Rotate An Array

A very simple approach is to use `deque`, and move items around. `Deque` already has a built-in function for this.

```python

from collections import deuqe
def rotate(self, nums: List[int], k: int) -> None:
    dq = deque(nums)
    dq.rotate(k)
    nums[:] = list(dq) # notice we modify nums in-place

```

Another Approach is find the rotation point, and create a new array. Space : $O(n)$ and Time : $O(n)$

To avoid using Extra Space We can use following techniques, Reverse the Entire Array and then reverse both parts separated by `k` boundary.

```
# 1, 2, 3, 4, 5, 6
# k = 2
# 5, 6, 1, 2, 3, 4

# reverse the array
# 6, 5, 4, 3, 2, 1
#       k
# reverse two groups
# 5, 6, 1, 2, 3, 4
```

```python

def rotate(self, nums: List[int], k: int) -> None:
    nums[:] = list(reversed(nums))
    n = len(nums)
    k = k % n

    def reverse(i, j):
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1
    
    reverse(0, k-1)
    reverse(k, n-1)

```


### Union of Two Sorted Array

**Problem Statement:** Given two sorted arrays, **arr1,** and **arr2** of size **n** and **m**. Find the union of two sorted arrays. The union of two arrays can be defined as the common and distinct elements in the two arrays.

A simple straightforward solution would be to convert into sets and take union and convert back to list.

Optimal Approach is to create an extra array, and track both lists.

```python

def findUnion(nums1, nums2, n, m):
    res = []
    i = j = 0

    while i < n and j < m:
        if nums1[i] < nums2[j]:
            if not res or res[-1] != nums1[i]:
                res.append(nums1[i])
            i += 1

        elif nums1[i] > nums2[j]:
            if not res or res[-1] != nums2[j]:
                res.append(nums2[j])
            j += 1

        else:
            if not res or res[-1] != nums1[i]:
                res.append(nums1[i])
            i += 1
            j += 1

    while i < n:
        # if nums, were individually distinct
        # then we can do, res.extend(nums1[i:])
        if not res or res[-1] != nums1[i]:
            res.append(nums1[i])
        i += 1

    while j < m:
        if not res or res[-1] != nums2[j]:
            res.append(nums2[j])
        j += 1

    return res

```


### Find the Number that appears once, other appears Twice

This is an application of `xor` property. XOR of two identical numbers is zero, so xor for rest of the array would be 0 except leaving the number intact.

### Maximum Consecutive Ones

```python

def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
    
    res = 0
    curr = 0
    for num in nums:
        if num == 1:
            curr += 1
        else:
            # reset count
            curr = 0
        res = max(res, curr)
    
    return res

```


## Medium Problems

### 2 Sum (Unsorted)

Given an array of integers `nums` and an integer `target`, return _indices of the two numbers such that they add up to `target`_.

You may assume that each input would have **_exactly_ one solution**, and you may not use the _same_ element twice.

One Approach is to simply try out every pair of numbers, which would $O(n^2)$ in time.

Optimal Approach:
Keep track numbers found so far, by adding them to set or a map.

```python

# we can't use two-pointer here since its not sorted array
def twoSum(self, nums: List[int], target: int) -> List[int]:
    mp = {}

    for i, v in enumerate(nums):
        if target - v not in mp:
            mp[v] = i
        else:
            return [i, mp[target-v]]

    return None

```

### Majority Element

The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.

A naive approach is to store all the numbers in a map and count the frequency of most frequent number.

But optimal approach is to track a counter which increments whenever a number is same as majority element or else decreases, if it reaches we reset majority number. Idea is if some number appear more than half time then for counter to be positive all half same numbers will try to increment the counter and rest all will try to decrement the number, leaving atleast one number extra to be majority element.

This is often known as Boyer Moore Voting Algorithm.

```python

def majorityElement(nums):

    cnt, maj = 0, None

    for num in nums:
        if cnt == 0:
            maj = num
        cnt += 1 if num == maj else -1

    return maj

```

### Maximum Subarray Sum

There are multiple ways to solve this problem, but most optimal approach is to use *Kadane's Algorithm*.
This is a very important question.

Principle : If a prefix sum is negative, keeping it will only make any future subarray worse, so optimal solution should restart at current number.

```
Recurrence : optimal ending at i = max(nums[i], optimal ending at i-1 + nums[i])
```

```c++

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        // Kadane's Algorithm
        int sum = 0, ans = INT_MIN;
        for(int i = 0; i < nums.size(); i++) {
            sum += nums[i];         // greedily extend this running sums
            ans = max(ans, sum);    // we keep the maximum RSQ
            if(sum < 0) sum = 0;    // reset running sum, when it dips below zero
        }
        return ans;
    }
};

```

### Stock Buy and Sell

You are given an array `prices` where `prices[i]` is the price of a given stock on the `ith` day.
You want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.
Return _the maximum profit you can achieve from this transaction_. If you cannot achieve any profit, return `0`.

An advanced solution of this question is to use `dp` states like this. (Ignore if not read DP)

```python

@cache
def solve(i, can_buy):
    
    if i >= n:
        return 0

    if can_buy:
        return max(
            -prices[i] + solve(i+1, False), # profit - upon buying
            solve(i+1, True)                # don't purchase
        )
    else:
        return max(
            prices[i],                      # sell, gain profit
            solve(i+1, False)               # don't sell
        )

return solve(0, True)

```

Idea : Track minimum price we have seen so far and what would be the profit if sold today.

```python

def solve(prices):
    min_price = float('inf')
    
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        else:
            # if sold today!
            max_profit = max(max_profit, price - min_price)
    
    return max_profit
    

```

But simpler version of above statement could be solved using simple kadane's algorithm.
How Kadane's algorithm fits here, 

Suppose original array is : `[a0, a1, a2, a3, a4, a5, a6]`

What we are given here according to explanation is difference array :  `[b0, b1, b2, b3, b4, b5, b6]`
where : `b[i] = 0` if `i == 0` (we can't sell before buying)
and : `b[i] = a[i]-a[i-1]` when `i != 0`.

Let's find max profit or difference we get is : `a2, a6` : is

$$
\begin{align}
b3 &= a3 - a2 \\
b4 &= a4 - a3 \\
b5 &= a5 - a4 \\
b6 &= a6 - a5
\end{align}
$$

$$
subarry(b3 + b4 + b5 + b6) = a6 - a2
$$

Original Problem : $\max_{0 \le i < j < n} (a[j] - a[i])$

Transformation to Difference Array :

$$
b[i] =
\begin{cases}
0, & \text{if } i = 0 \\
a[i] - a[i-1], & \text{if } i > 0
\end{cases}
$$

$$
\begin{aligned}
a[j] - a[i]
&= (a[i+1] - a[i]) + (a[i+2] - a[i+1]) + \dots + (a[j] - a[j-1]) \\
&= \sum_{k=i+1}^{j} b[k]
\end{aligned}
$$

Or Problem Transforms to Subarray Sum problem, and we sought out to find maximum sub array sum of the array.

Finding Largest Subarray Sum in an array is equivalent to finding the maximum difference between two elements of an array

```c++

public int maxProfit(int[] prices) {
    int maxCur = 0, maxSoFar = 0;
    for(int i = 1; i < prices.length; i++) {
        maxCur = Math.max(0, maxCur += prices[i] - prices[i-1]);
        maxSoFar = Math.max(maxCur, maxSoFar);
    }
    return maxSoFar;
}

```

### Next Permutation

A **permutation** of an array of integers is an arrangement of its members into a sequence or linear order.

For example, for `arr = [1,2,3]`, the following are all the permutations of `arr`: `[1,2,3], [1,3,2], [2, 1, 3], [2, 3, 1], [3,1,2], [3,2,1]`.

In python at-least you can use in-built functions to solve this quickly :). But optimal solution doesn't require generation of the all permutations.

Notice the last permutation in above example : `[3 2 1]` ~ all numbers are decreasing, and first one ~ all numbers are increasing.

Example : `[9, 5, 4, 3, 1]` doesn't have a solution since its decreasing monotonically !

Another example : `[4 3 1 2] -> [4 3 2 1]`  Notice that the prefix is same but the rest of the suffix portion was not decreasing in nature, 

We are supposed to find point where monotonically decreasing property is violated !. `a[i] < a[i-1]`. Since we need next permutation, we will replace `a[i-1]` with number just greater than itself say `a[j]`. Graphically.


![](assets/Pasted%20image%2020260117163443.png)

But problem is not solved yet ! We have to put remaining numbers in ascending order.


```python

def nextPermutation(self, nums: List[int]) -> None:

    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i+1] <= nums[i]:
        i -= 1
    
    # i not points to swapping point
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        
        # j now points to number just greater than nums[i]
        # swap
        nums[i], nums[j] = nums[j], nums[i]


    def reverse(start, end=n-1):
        i, j = start, end
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1

    # reverse remaining elements
    reverse(i+1)


```

### Leaders in an Array

Given an array `nums` all the element for which there is max element present to their right is called as leaders in an array.

```

Input: arr = [4, 7, 1, 0]  
Output: 7 1 0  
Explanation: The rightmost element (0) is always a leader. 7 and 1 are greater than the elements to their right, making them leaders as well.

```

At first glance, this problem may seem similar to tracking the maximum element to the right using a monotonic queue. However, since we are asked to **identify and store the elements themselves** (the leaders), a monotonic queue is unnecessary.

A simpler and optimal approach is to **traverse the array from right to left** while maintaining a variable max_seen_so_far. The rightmost element is always a leader. As we move leftward, if the current element is **greater than max_seen_so_far**, it is a leader; we append it to the result and update max_seen_so_far. This approach ensures all leaders are identified in a single pass

### Longest Consecutive Sequence

[Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)

Given an unsorted array of integers `nums`, return _the length of the longest consecutive elements sequence._

You must write an algorithm that runs in `O(n)` time.

A naive approach would be create a map storing existence of numbers and check generating all possible sequence at each number which will be $O(n . ans)$

```
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

```

Optimal Approach :

First turn the input into a _set_ of numbers. That takes O(n) and then we can ask in O(1) whether we have a certain number.

Then go through the numbers. If the number x is the start of a streak (i.e., x-1 is not in the set), then test y = x+1, x+2, x+3, ... and stop at the first number y _not_ in the set. The length of the streak is then simply y-x and we update our global best with that. Since we check each streak only once, this is overall O(n).

```python

def longestConsecutive(self, nums):
    nums = set(nums)
    best = 0
    for x in nums:
        # validates this is start of streak, not continuation
        if x - 1 not in nums:
            y = x + 1
            while y in nums:
                y += 1
            best = max(best, y - x)
    return best

```

## Problems on Matrix (2D Array)
### Set Matrix Zeroes

[Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/)

Given an `m x n` integer matrix `matrix`, if an element is `0`, set its entire row and column to `0`'s.
You must do it [in place](https://en.wikipedia.org/wiki/In-place_algorithm).

A correct solution is to track zeroes seen for each row and column, requiring two arrays of `1xm` and `1xn` dimensions.

But We can just reuse the matrix to store this information, especially at first row !

```python

def setZeroes(self, matrix: List[List[int]]) -> None:
    """
    Do not return anything, modify matrix in-place instead.
    """
    m, n = len(matrix), len(matrix[0])

    # Flags to mark if first row or first column have zeros
    # as this information is lost once we use these !!
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))

    # Use first row and column as markers for zero rows and cols
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # Set zeroes based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    # Zero the first row if needed
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0

    # Zero the first column if needed
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0


```


### Rotate the Matrix

You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.

A general method to rotate an matrix !

```
/*
 * clockwise rotate
 * first reverse up to down, then swap the symmetry 
 * 1 2 3     7 8 9     7 4 1
 * 4 5 6  => 4 5 6  => 8 5 2
 * 7 8 9     1 2 3     9 6 3
*/

/*
 * anticlockwise rotate
 * first reverse left to right, then swap the symmetry
 * 1 2 3     3 2 1     3 6 9
 * 4 5 6  => 6 5 4  => 2 5 8
 * 7 8 9     9 8 7     1 4 7
*/

```

In Python We can Use something Like `zip` operator to do it in one line.

```python

class Solution:
    def rotate(self, A):
        A[:] = zip(*A[::-1])
        
# zip combines a list of iterables taking 1 elment from each
# A = ((a, b, c), (d, e, f), (g, h, i))
# A[::-1] ((g, h, i), (d, e, f), (a, b, c)) # reverse operation
# *A ~ opens into (iterable1, iterable2, ....)
# zip(*A[::-1]) ~ zip(iterable1, iterable2, iterable3)
# zip((g, h, i), (d, e, f), (a, b, c)) # transponse operation
# A = [(g, d, a), (h, e, b), (i, f, c)]

```

```python

def rotate(self, A):
    A.reverse()
    for i in range(len(A)):
        for j in range(i):
            A[i][j], A[j][i] = A[j][i], A[i][j]

```

### Spiral Matrix

Given an `m x n` `matrix`, return _all elements of the_ `matrix` _in spiral order_.

A Simple python solution is to extract each first layer and then rotate the matrix, again take one layers and rotate the matrix.

```python

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        return matrix and [*matrix.pop(0)] + self.spiralOrder([*zip(*matrix)][::-1])

```

A Complete Solution would be like following

```python

def spiralOrder(matrix: List[List[int]]) -> List[int]:
    l, r = 0, len(matrix[0]) - 1
    u, d = 0, len(matrix) - 1
    res = []
    step = 0
    while l <= r and u <= d:
        match (step % 4):
            case 0:
                for i in range(l, r+1):
                    res.append(matrix[u][i])
                u += 1
            case 1:
                for i in range(u, d+1):
                    res.append(matrix[i][r])
                r -= 1
            case 2:
                for i in range(r, l-1, -1):
                    res.append(matrix[d][i])
                d -= 1
            case 3:
                for i in range(d, u-1, -1):
                    res.append(matrix[i][l])
                l += 1
        step += 1
    return res

```


## Misc. Questions

### Pascal's Triangle

```python

def generate(self, numRows: int) -> List[List[int]]:
    if numRows == 0:
        return []
    
    triangle = []

    for i in range(numRows):
        row = [1] * (i+1)

        for j in range(1, i):
            row[j] = triangle[-1][j-1] + triangle[-1][j]
        triangle.append(row)
    
    return triangle

```


### Majority Element II

Given an integer array of size `n`, find all elements that appear more than `⌊ n/3 ⌋` times.

### Count Number of Inversions

Pre-requisite : Sorting : Merge - Sort

[Solution Link](../sorting/ch3.md)

### Shuffle Array in Linear Time

*Fisher Yates Algorithm*

[Video Explanation](https://www.youtube.com/watch?v=4zx5bM2OcvA&list=PL3edoBgC7ScV9WPytQ2dtso21YrTuUSBd&index=14)

```python
import random

# Solution 1: Fisher-Yates algorithm (old version)
# Time complexity: O(n²)
# Space complexity: O(n)
def shuffle(arr):
  shuffled = []
  while len(arr) > 0:
    rand_index = random.randrange(0, len(arr))
    shuffled.append(arr[rand_index])
    arr.pop(rand_index)
  arr = shuffled

# Solution 2: Sorting assigned random values
# Time complexity: O(nlogn)
# Space complexity: O(n)
def shuffle(arr):
  rand_values = [random.random() for i in range(len(arr))]
  rand_indexes = [i for i in range(len(arr))]
  rand_indexes.sort(key=lambda i: rand_values[i])
  arr = [arr[i] for i in rand_indexes]

# Solution 3: Fisher-Yates algorithm (modern version)
# Time complexity: O(n)
# Space complexity: O(1)
def shuffle(arr):
  last_index = len(arr)-1
  while last_index > 0:
    rand_index = random.randint(0, last_index)
    temp = arr[last_index]
    arr[last_index] = arr[rand_index]
    arr[rand_index] = temp
    last_index -= 1
```
### Reverse Pair

Given an integer array `nums`, return _the number of **reverse pairs** in the array_.

A **reverse pair** is a pair `(i, j)` where:

- `0 <= i < j < nums.length` and
- `nums[i] > 2 * nums[j]`

Pre-requisite : Merge Sort

```python

def reversePairs(nums: List[int]) -> int:

    def ms(l, r):
        if l >= r: return 0
        mid = (l + r) // 2
        count = ms(l, mid) + ms(mid + 1, r)

        j = mid + 1
        for i in range(l, mid+1):
            while j <= r and nums[i] > 2 * nums[j]:
                j += 1
            count += j - mid - 1

        nums[l:r+1] = sorted(nums[l:r+1])
        return count

    return ms(0, len(nums) - 1)

```

