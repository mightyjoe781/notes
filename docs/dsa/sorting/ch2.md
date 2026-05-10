# Quicksort

* Quicksort is the most widely used sorting algorithm.
* Invented in 1960 by C.A.R. Hoare.
    - easy to implement
    - resource efficient in many cases

* Features
    - in-place
    - $N \log{N}$ on avg case

* Drawbacks
    - Not stable
    - $N^2$ in worst case
    - fragile ( any small mistake in implementation can go un-noticed and cause bad performance)

* Python's built-in `sorted()` uses Timsort, a hybrid of merge sort and insertion sort.
* Performance of quicksort is highly dependent on the input.

![](assets/Pasted%20image%2020260510152630.png)

```python
def partition(arr, l, r):
    i, j = l - 1, r
    v = arr[r]
    while True:
        i += 1
        while arr[i] < v:
            i += 1
        j -= 1
        while v < arr[j]:
            if j == l:
                break
            j -= 1
        if i >= j:
            break
        arr[i], arr[j] = arr[j], arr[i]
    arr[i], arr[r] = arr[r], arr[i]
    return i

def quicksort(arr, l, r):
    if r <= l:
        return
    i = partition(arr, l, r)
    quicksort(arr, l, i - 1)
    quicksort(arr, i + 1, r)
```

* Dynamic Characteristics
    * Nearly ordered arrays perform worst.
    * Because they have many partitions.

## Quick-Select

* Finding `k-th` smallest number in a set of numbers
* Can be used to find median without sorting
* Time Complexity : $O(N)$ in avg case, $O(N^2)$ in worst case

```python
# recursive
def quickselect(arr, l, r, k):
    if r <= l:
        return
    i = partition(arr, l, r)
    if i > k:
        quickselect(arr, l, i - 1, k)
    elif i < k:
        quickselect(arr, i + 1, r, k)
```

```python
# iterative
def quickselect(arr, l, r, k):
    while r > l:
        i = partition(arr, l, r)
        if i > k:
            r = i - 1
        elif i < k:
            l = i + 1
        else:
            break
```
