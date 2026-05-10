# Elementary Sorting Techniques

Below are all Elementary Sorting Techniques for Educational Purposes only. These are rarely used in production.

## Selection Sort

* Exchanges : $N-1$
* Comparisons : $N^2$
* Comparisons dominate runtime
* Not Stable
* Takes same time irrespective of already sorted array
* Outperforms more sophisticated methods in one important application - it is the method for sorting files with huge items and small keys. `(cost of moving > cost of making comparisons)`

```python
def selection_sort(arr, l, r):
    for i in range(l, r):
        min_idx = i
        for j in range(i + 1, r + 1):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
```

## Bubble Sort

* Exchanges : Upto $N^2$
* Comparison: $N^2$
* Stable
* **Inefficient for large datasets** due to high number of swaps, rarely used in practice
* Not Memory Efficient, but in-place
* Adaptive : Useful in scenarios where data is almost already sorted.

```python
def bubble_sort(arr, l, r):
    for i in range(l, r):
        for j in range(r, i, -1):
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
```

## Insertion Sort

* Exchanges: Upto $N^2$
* Comparison: $N^2$
* Stable
* Adaptive
* Efficient for small datasets or partially sorted data
* Used in practice for small data and as a final stage in more complex sorts like TimSort or Hybrid sorts
* The **sentinel optimization** ensures that the inner loop never checks bounds `(j > l)`, improving efficiency.

```python
def insertion_sort(arr, l, r):
    # sentinel: move smallest to front so inner loop never goes out of bounds
    for i in range(r, l, -1):
        if arr[i] < arr[i - 1]:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]

    for i in range(l + 2, r + 1):
        v = arr[i]
        j = i
        while v < arr[j - 1]:
            arr[j] = arr[j - 1]
            j -= 1
        arr[j] = v
```

## Shell Sort

* Not Stable
* More on Shell Sort : [Link](https://algo.minetest.in/3-Sorting/6-Elementary_Sorting_Methods/6-Shell_sort/)

```python
def shell_sort(arr, l, r):
    h = 1
    while h <= (r - l) // 9:
        h = 3 * h + 1   # Knuth's sequence: 1, 4, 13, 40, ...

    while h > 0:
        for i in range(l + h, r + 1):
            v = arr[i]
            j = i
            while j >= l + h and v < arr[j - h]:
                arr[j] = arr[j - h]
                j -= h
            arr[j] = v
        h //= 3
```
