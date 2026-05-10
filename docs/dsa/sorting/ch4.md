# Special Sorting Techniques

NOTE: It's good to know these techniques rather than understanding in great detail.

## Batcher’s Odd-Even Mergesort

Batcher’s Odd-Even Mergesort is a comparison-based parallel sorting algorithm, known for its deterministic structure and regular data access patterns, making it highly suitable for hardware implementation like on GPUs, FPGAs, and sorting networks.

Implementation - [Link](https://algo.sudomoon.com/3-Sorting/11-Special_purpose_sorting_methods/1-Batchers_OddEven/)

## External Sorting

External sorting is a class of sorting algorithms that can handle massive amounts of data. External sorting is required when the data being sorted do not fit into the main memory of a computing device (usually RAM) and instead they must reside in the slower external memory, usually a disk drive. Thus, external sorting algorithms are external memory algorithms and thus applicable in the external memory model of computation. 

More - [Algo Site](https://algo.sudomoon.com/3-Sorting/11-Special_purpose_sorting_methods/3-External_Sorting/)  [Wiki Article](https://en.wikipedia.org/wiki/External_sorting)

## Parallel MergeSort

Paper - [Parallel Merge Sort](https://www.sjsu.edu/people/robert.chun/courses/cs159/s3/T.pdf)

## Counting Sort

Counting Sort is a non-comparison-based linear-time sorting algorithm suitable for integers in a fixed range. It works by counting the frequency of each unique element, then calculating prefix sums to determine positions in the output array.

* No Comparisons
* Time Complexity : $O(n+k)$ where n is the number of elements, and k is the range of input.
* Space : $O(k)$
* Ideal for **bucket-based grouping**, **radix sort**, or **histogram generation**.

```python
def counting_sort(arr, max_val=None):
    if not arr:
        return arr
    k = (max_val or max(arr)) + 1
    count = [0] * k

    for x in arr:
        count[x] += 1

    # prefix sums: count[i] now = number of elements <= i
    for i in range(1, k):
        count[i] += count[i - 1]

    out = [0] * len(arr)
    for x in reversed(arr):    # reversed keeps sort stable
        count[x] -= 1
        out[count[x]] = x

    return out
```

## Radix Sort

**Radix Sort** is a **non-comparison** sorting algorithm that sorts numbers digit by digit, starting either from the least significant digit (**LSD**) or most significant digit (**MSD**), using a **stable sort** (like Counting Sort) at each digit level.

* Time Complexity: $O(d \cdot (n + b))$ where d = digits, b = base (usually 10)
* Stable
* Best when keys are integers with a known, bounded number of digits

```python
def radix_sort(arr):
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1       # current digit place (1, 10, 100, ...)

    while max_val // exp > 0:
        # counting sort by digit at position `exp`
        buckets = [[] for _ in range(10)]
        for num in arr:
            digit = (num // exp) % 10
            buckets[digit].append(num)
        arr = [num for bucket in buckets for num in bucket]
        exp *= 10

    return arr
```

## Bucket Sort

**Bucket Sort** distributes elements into several buckets, then sorts each bucket (typically using **insertion sort**) and concatenates them.

* Use it when Inputs are **uniformly distributed floating-point numbers in [0, 1)**
* You want **average-case linear time**
* Data is spread out over a range and simple sorting within chunks is faster

````python
def bucket_sort(arr):
    n = len(arr)
    buckets = [[] for _ in range(n)]

    for num in arr:
        index = int(num * n)
        buckets[index].append(num)

    for i in range(n):
        buckets[i].sort()

    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result
````

---

## Cyclic Sort

Cyclic sort is a special in-place O(n) sort for arrays containing integers in a known range `[1..n]` (or `[0..n-1]`). Each number is placed at its correct index by swapping, not by comparison.

**When to use:** the problem involves an array of size `n` containing integers in range `[1..n]` and asks to find missing/duplicate/misplaced numbers.

```python
def cyclic_sort(nums):
    i = 0
    while i < len(nums):
        correct = nums[i] - 1      # where nums[i] belongs (1-indexed)
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1
    return nums
```

### Find the Missing Number

**Problem:** Given an array of size `n` containing numbers in range `[0, n]` (one number missing), find the missing number.

After cyclic sort, any index where `nums[i] != i + 1` is the missing number.

```python
def findMissingNumber(nums):
    n = len(nums)
    i = 0
    while i < n:
        j = nums[i]
        if j < n and nums[i] != nums[j]:
            nums[i], nums[j] = nums[j], nums[i]
        else:
            i += 1

    for i in range(n):
        if nums[i] != i:
            return i
    return n
```

### Find All Duplicates / All Missing Numbers

**Problem:** Given an array of size `n` containing numbers in range `[1, n]`, find all numbers that appear twice (or all numbers missing from the array).

Same cyclic sort pass, then scan for mismatches:

```python
def findAllDuplicates(nums):
    i = 0
    while i < len(nums):
        j = nums[i] - 1
        if nums[i] != nums[j]:
            nums[i], nums[j] = nums[j], nums[i]
        else:
            i += 1
    return [nums[i] for i in range(len(nums)) if nums[i] != i + 1]
```
