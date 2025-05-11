# Elementary Sorting Techniques

Below are all Elementary Sorting Techniques for Educational Purposes only, These are rarely used in production.

## Selection Sort

* Exchanges : $N-1$
* Comparisons : $N^2$
* Comparisons dominate runtime
* Not Stable
* Takes same time irrespective of already sorted array
* outperforms more sophisticated methods in one important application; it is the method for sorting files with huge item and small keys. `(cost of moving > cost of making comparisons)`

````c++
void selection(vector<int> arr, int l , int r){
    for(int i = l ; i <r ; i++){
        int min  = i;
        for(int j = i+1 ; j <=r ; j++)
            if(arr[j] < arr[min]) min = j ;
        swap(arr[i], arr[min]);
    }
}
````

## Bubble Sort

* Exchanges : Upto $N^2$
* Comparison: $N^2$
* Stable
* **Inefficient for large datasets** due to high number of swaps, rarely used in practice
* Not Memory Efficient, but in-place
* Adaptive : Useful In scenarios where data is almost already sorted.

````c++
// compexch: compare and exchange if necessary
template <typename T>
void compexch(T& a, T& b) {
    if (b < a) {
        std::swap(a, b);
    }
}
````

````c++
// assuming compexch is implemented
void bubble(vector<int> arr , int l , int r){
    for(int i = l; i < r; i++)
        for(int j = r ; j > i; j--)
            compexch(arr[j-1], arr[j]);
}
````

## Insertion Sort

* Exchanges: Upto $N^2$
* Comparison: $N^2$
* Stable
* Adaptive
* Efficient for small datasets or partially sorted data
* Used in practice for small data and as a final stage in more complex sorts like TimSort or Hybrid sorts
* The **sentinel optimization** ensures that the inner loop never checks bounds `(j > l)`, improving efficiency.

````c++
void insertion(vector<int> a, int l, int r) {
    // Sentinel placement: move the smallest item to the beginning
    for (int i = r; i > l; --i) compexch(a[i - 1], a[i]);

    // Insertion sort with sentinel
    for (int i = l + 2; i <= r; ++i) {
        Item v = a[i];
        int j = i;
        while (v < a[j - 1]) {
            a[j] = a[j - 1];
            --j;
        }
        a[j] = v;
    }
}
````

## Shell Sort

* Not Stable
* More on Shell Sort : [Link](https://algo.minetest.in/3-Sorting/6-Elementary_Sorting_Methods/6-Shell_sort/)

````c++
template <typename Item>
void shellsort(Item a[], int l, int r) {
    int h;

    // Generate initial maximum gap (using Knuth's sequence: 1, 4, 13, 40, ...)
    for (h = 1; h <= (r - l) / 9; h = 3 * h + 1);

    // Decrease the gap and perform gapped insertion sort
    for (; h > 0; h /= 3) {
        for (int i = l + h; i <= r; ++i) {
            Item v = a[i];
            int j = i;

            // Gapped insertion sort
            while (j >= l + h && v < a[j - h]) {
                a[j] = a[j - h];
                j -= h;
            }

            a[j] = v;
        }
    }
}
````

