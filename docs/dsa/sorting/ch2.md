# Quicksort

* Quicksort is most widely used sorting algorithm than any other algorithm.

* Invented in 1960 by C.A.R. Hoare.

  - easy to implement
  - resource efficient in many cases

* features

  - in-place
  - $N \log{N}$ on avg case

* drawbacks

  - Not stable

  - $N^2$ in worst case
  - fragile ( any small mistake in implementation can go un-noticed and cause bad performance)

* STL library uses `qsort` function.

* Performance of the quicksort is highly dependent on the input.

![image-20201020142048564](https://algo.minetest.in/1-The_Basic_Algorithm.assets/image-20201020142048564.png)

````c++
// Partition function
template <typename Item>
int partition(Item a[], int l, int r) {
    int i = l - 1, j = r;
    Item v = a[r];
    for (;;) {
        while (a[++i] < v);         // move i right
        while (v < a[--j]) if (j == l) break; // move j left
        if (i >= j) break;
        swap(a[i], a[j]);           // swap a[i] and a[j]
    }
    swap(a[i], a[r]);               // place pivot at its final position
    return i;                       // return pivot index
}

// Quicksort main function
template <typename Item>
void quicksort(Item a[], int l, int r) {
    if (r <= l) return;
    int i = partition(a, l, r);
    quicksort(a, l, i - 1);
    quicksort(a, i + 1, r);
}
````

* Dynamic Characterstics
  * Nearly ordered files perform worst.
  * Because they have many partitions.

## Quick-Select

* Finding `k-th` smallest number in a set of numbers
* Can be used to find median without sorting
* Time Complexity : $O(N)$ in avg case, $O(N^2)$ in worst case

````c++
// Recursive
template <typename Item>
void quickselect(Item a[], int l, int r, int k) {
    if (r <= l) return;
    int i = partition(a, l, r);
    if (i > k) quickselect(a, l, i - 1, k);
    else if (i < k) quickselect(a, i + 1, r, k);
}
````

````c++
// Iterative Approach
template <typename Item>
void quickselect(Item a[], int l, int r, int k) {
    while (r > l) {
        int i = partition(a, l, r);
        if (i > k) r = i - 1;
        else if (i < k) l = i + 1;
        else break;
    }
}
````

