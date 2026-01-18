# Two Pointer

* Useful for handling sorted data or searching for pairs, triplets, or subarrays that meet specific conditions
* The core idea is to use two indices that move through the data structure at different speeds or in different directions to narrow the search space.

| Problem Type                        | Description                                                   | Movement Strategy                          |
| ----------------------------------- | ------------------------------------------------------------- | ------------------------------------------ |
| Pair with target sum                | Find two elements summing to a target value in a sorted array | Move left/right pointers inward            |
| Remove duplicates from sorted array | Remove duplicates in-place and return new length              | Slow and fast pointer moving forward       |
| Partition array                     | Rearrange elements based on a pivot                           | Left and right pointers moving inward      |
| Check palindrome                    | Check if a string is palindrome                               | Left and right pointers moving inward      |
| Triplets with zero sum              | Find all unique triplets that sum to zero                     | Fix one pointer, use two pointers for rest |

## Framework to Solve Problems

- Determine if the two-pointer technique applies.

    - Is the array or string sorted? Can it be sorted without violating constraints?
    - Are pairs, triplets, or subarrays required?
    - Can two loops be replaced by two pointers? NOTE: Extra Information by sorted constraint allows us to skip every pair check.

- Initialize the pointers
    - Usually, `l = 0` and `r = n-1` for pairs
    - For windows, `l` and `r` start at `0`

- Pointer moving conditions
    - If `sum` or `constraint` is more, move `r` to reduce it
    - If `sum` or `constraint` is less, move `l` to reduce it
    - For partitioning problems, swap elements and move pointers accordingly

- Stop Conditions : When pointers cross or meet, terminate

## Examples

* Partition Array Around a Pivot

````c++
void partitionArray(vector<int>& nums, int pivot, int n) {
    int l = 0, r = n - 1;
    while (l <= r) {
        if (nums[l] < pivot) {
            l++;
        } else {
            swap(nums[l], nums[r]);
            r--;
        }
    }
}
````

Sample Problems

* [2 Sum with sorted Input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)
* [3 Sum](https://leetcode.com/problems/3sum/description/) : we can sort without violating constraint
* [(125) Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)

## Problems

### 3-Sum Problem

Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j, i != k, and j != k`, and `nums[i] + nums[j] + nums[k] == 0`

Notice that the solution set must not contain duplicate triplets.

Problem is simple, sorting costs $O(n\log n)$ which is still less than $O(n^2)$ which is the best you can do here.

```python

def threeSum(nums: List[int]) -> List[List[int]]:
    res = set()
    n = len(nums)

    nums.sort()
    
    for i in range(n):
        j, k = i+1, n-1
        while j < k:
            if nums[j] + nums[k] < -nums[i]:
                j += 1
            elif nums[j] + nums[k] > -nums[i]:
                k -= 1
            else:
                res.add((nums[i], nums[j], nums[k]))
                j += 1
                k -= 1
    
    return [list(v) for v in res]

```

### Remove Duplicates from Sorted Array (in-place)

A Naive Approach is to convert list to set or use a dictionary for tracking,
Most optimal approach is to use, fast and slow pointer, slow pointer tracking the unique array.

```python

def removeDuplicates(self, nums: List[int]) -> int:
    # in-place

    slow, fast = 0, 1

    for fast in range(len(nums)):
        if nums[slow] == nums[fast]:
            fast += 1
        else:
            nums[slow+1] = nums[fast]
            fast += 1
            slow += 1
    
    return slow + 1

```

### Move Zeroes to the End

Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

```python

def moveZeroes(self, nums: List[int]) -> None:
    # similar to above problem, in-place duplicate removal
    l, r = 0, 0

    while l < len(nums) and nums[l] != 0:
        l += 1

    while r < len(nums) and nums[r] == 0:
        r += 1

    while r < len(nums):
        if nums[r] != 0:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r += 1
        else:
            r += 1

```


### Sort an Array of 0s, 1s, 2s

This is famous problem often known as Dutch National Flag Problem. With any sorting algorithm it will take $O(n\log n)$ time, but with tracking three-pointer it can be done in $O(n)$

Here, `l-tracks the zeroes, m-tracks the end of ones, r-tracks the 2s`

```c++

void sortColors(vector<int>& nums) {
    // dutch national flag problem
    int l = 0, m = 0, r = nums.size()-1;

    while(m <= r) {
        switch(nums[m]) {
            case 0: swap(nums[l++], nums[m++]);
                break;
            # increment m
            case 1: m++;
                break;
            # could be (2, 0) swap, so we don't increment m
            case 2: swap(nums[m], nums[r--]);
                break;
        }
    }
}

```

### Rearrange Array Elements by Sign

A straightforward approach is to have additional array where we can put element by taking two pointers, 1 tracking positive and 1 for tracking negative numbers.

A little more complicated variant of the problem is performing the operation *in-place*, But *in-place* doesn't exist if you want to preserve the order.

Assumptions : Numbers always appear in pair, and Preserve Order

```python

# doesn't preserve order, in-place rearrangement

def rearrangeArray(self, nums: List[int]) -> List[int]:

    l, r = 0, len(nums) - 1
    while l < r:
        if nums[l] < 0:
            l += 1
        if nums[r] > 0:
            r -= 1
        if nums[l] > nums[r] and nums[l] > 0:
            nums[l], nums[r] = nums[r], nums[l]
    
    sz = len(nums)
    i = int(nums[sz//2] < 0)
    j = sz//2 + i

    while i < sz and j < sz:
        nums[i], nums[j] = nums[j], nums[i]
        i += 2
        j += 1
    
    return nums

```

NOTE: you can't have both of the constraint applicable.

### Merge Two Sorted Arrays without Extra Space

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and two integers m and n, representing the number of elements in `nums1` and `nums2` respectively.

Merge `nums1` and `nums2` into a single array sorted in non-decreasing order.

```
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.
```

A naive approach is to put all elements in num1 and sort it.

Hint : Take two pointer `i` and `j` as the ends for `nums1` and `nums2`, `k = len(nums1)` and try to fill the array backwards. $O(n+m)$ at max.
