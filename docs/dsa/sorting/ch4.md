# Special Sorting Techniques

NOTE: Its good to know these techniques rather than understanding in great detail.

## Batcher’s Odd-Even Mergesort

Batcher’s Odd-Even Mergesort is a comparison-based parallel sorting algorithm, known for its deterministic structure and regular data access patterns, making it highly suitable for hardware implementation like on GPUs, FPGAs, and sorting networks.

Implementation - [Link](https://algo.minetest.in/3-Sorting/11-Special_purpose_sorting_methods/1-Batchers_OddEven/)

## External Sorting

External sorting is a class of sorting algorithms that can handle massive amounts of data. External sorting is required when the data being sorted do not fit into the main memory of a computing device (usually RAM) and instead they must reside in the slower external memory, usually a disk drive. Thus, external sorting algorithms are external memory algorithms and thus applicable in the external memory model of computation. 

More - [Algo Site](https://algo.minetest.in/3-Sorting/11-Special_purpose_sorting_methods/3-External_Sorting/)  [Wiki Article](https://en.wikipedia.org/wiki/External_sorting)

## Parallel MergeSort

Paper - [Parallel Merge Sort](https://www.sjsu.edu/people/robert.chun/courses/cs159/s3/T.pdf)

## Counting Sort

Counting Sort is a non-comparison-based linear-time sorting algorithm suitable for integers in a fixed range. It works by counting the frequency of each unique element, then calculating prefix sums to determine positions in the output array.

* No Comparisons
* Time Complexity : $O(n+k)$ where n is the number of elements, and k is the range of input.
* Space : $O(k)$
* Ideal for **bucket-based grouping**, **radix sort**, or **histogram generation**.

## Radix Sort

**Radix Sort** is a **non-comparison** sorting algorithm that sorts numbers digit by digit, starting either from the least significant digit (**LSD**) or most significant digit (**MSD**), using a **stable sort** (like Counting Sort) at each digit level.

[Full Chapter in Detail](https://algo.minetest.in/3-Sorting/10-Radix_Sorting/)

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
