# Mergesort

* Biggest advantage is guaranteed runtime : $O(N \log{N})$ (independent of input)
* Requires additional space : $O(N)$ (disadvantage)
* Guaranteed runtime can become a liability. Some linear sorts can take advantage of array properties.
* Stable (NOTE: Quicksort & Heapsort are not)
* Choice for sorting linked lists
* Proper example of Divide & Conquer

## Two-Way Merging

Given two sorted arrays `a` and `b`, merge them into a single sorted array.

```python
def merge_ab(a, b):
    c = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            c.append(a[i]); i += 1
        else:
            c.append(b[j]); j += 1
    c.extend(a[i:])
    c.extend(b[j:])
    return c
```

## Inplace Merge

* Stable
* Copies second half in reverse back-to-back with the first, creating a bitonic sequence - so two pointers from both ends always converge correctly without sentinel checks.

```python
def merge(arr, l, m, r):
    # left half forward + right half reversed = bitonic sequence
    aux = arr[l:m+1] + arr[m+1:r+1][::-1]
    i, j = 0, len(aux) - 1
    for k in range(l, r + 1):
        if aux[j] < aux[i]:
            arr[k] = aux[j]; j -= 1
        else:
            arr[k] = aux[i]; i += 1
```

```python
# top-down merge sort
def mergesort(arr, l, r):
    if r <= l:
        return
    m = (l + r) // 2
    mergesort(arr, l, m)
    mergesort(arr, m + 1, r)
    merge(arr, l, m, r)
```

```python
# bottom-up merge sort
def mergesort_bu(arr, l, r):
    m = 1
    while m <= r - l:
        i = l
        while i <= r - m:
            merge(arr, i, i + m - 1, min(i + m + m - 1, r))
            i += m + m
        m += m
```

* NOTE: MergeSort can be improved by adding an additional check to sort smaller partitions using *insertion sort*.

## Linked List Merge Sort

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_lists(a, b):
    dummy = ListNode(0)
    c = dummy
    while a and b:
        if a.val < b.val:
            c.next = a; c = a; a = a.next
        else:
            c.next = b; c = b; b = b.next
    c.next = a if a else b
    return dummy.next
```

```python
# bottom-up
from collections import deque

def mergesort_list_bu(head):
    if not head or not head.next:
        return head
    q = deque()
    node = head
    while node:
        nxt = node.next
        node.next = None
        q.append(node)
        node = nxt
    t = q.popleft()
    while q:
        q.append(t)
        t = merge_lists(q.popleft(), q.popleft())
    return t
```

```python
# top-down: split list into two halves using slow/fast pointer, sort recursively, then merge
def mergesort_list_td(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    return merge_lists(mergesort_list_td(head), mergesort_list_td(mid))
```

### Count Inversions in an Array

**Problem:** Given an array of N integers, count the number of inversions. An inversion is a pair `(i, j)` where `i < j` but `arr[i] > arr[j]`.

A $O(n^2)$ strategy would be to count inversions for each element, but we can do this optimally using merge-sort.

During merge sort, when we merge two sorted halves, if an element from the right half is smaller than an element from the left half, then it forms inversions with all remaining elements in the left half.

```python
def count_inversions(arr):
    def merge_sort(nums):
        if len(nums) <= 1:
            return nums, 0

        mid = len(nums) // 2
        left, inv_left = merge_sort(nums[:mid])
        right, inv_right = merge_sort(nums[mid:])

        merged = []
        i = j = 0
        inv_count = inv_left + inv_right

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inv_count += len(left) - i
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged, inv_count

    _, count = merge_sort(arr)
    return count
```
