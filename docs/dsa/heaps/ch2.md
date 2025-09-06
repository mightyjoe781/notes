# Applications

## Real-time Top-K Elements

### Concept

* Maintain the top `K` largest or smallest elements from a stream or dataset in real-time
* Use a *min-heap* of size `K` to track top `K` largest elements

### Use Cases

* Streaming data analytics
* Real-time Leaderboards
* Online Recommendation System

### Complexity

* Each insertion/deletion operation takes $O(\log K)$
* Efficient for large data streams where $K << N$

### Problems

* Kth Largest Element in an Array
* Top K Frequent Elements
* K Closest Points to Origin

## Median Maintenance

* Maintain the median of a dynamic data stream efficiently
* Use two-heaps
    * A max-heap for the lower half of the numbers
    * A min-heap for the upper half of the numbers
* Balancing the heaps ensures
    * The max-heap size is equal to or one more than the min-heap size
    * Median is either the top of the max-heap (odd cnt) or average of tops of both heaps (even cnt)

### Use Cases

* Real-time Statistics
* Running median in Sensor Data
* Financial Analytics

## Heap-based Sorting & Merging

### HeapSort

* Use a *max-heap* to sort an array in-place
* Steps
    * Build a *max-heap* from input array
    * Repeatedly extract the maximum element and place it at the end
    * Heapify the reduced heap
* Time Complexity: $O(n \log n)$
* Space Complexity: $O(1)$ (in-place)

### Merge K Sorted Lists/Array

* Use a *min-heap* to efficiently merge K sorted list
* Steps
    * Insert the first element of each list into the min-heap
    * Extract the smallest element from the heap and add it to the merged output.
    * Insert the next element from the extracted element’s list into the heap.
    * Repeat until all elements are processed.
* Time Complexity: $O(N \log K)$

### Problems

* Meeting Rooms II (Minimum Number of Meeting Rooms) : (253)

### Use Cases

* External Sorting
* Merging logs or streams
* Database Query Language