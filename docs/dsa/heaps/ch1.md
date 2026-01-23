# Priority Queue & HeapSort

*A priority queue is a data structure of items with keys that supports two basic operation*

* insert a new item
* remove the item with the largest key

Applications

* Simulation Systems (keys ~ event times)
* Job scheduling (keys ~ priority)
* Numerical computation ( keys ~ computation errors )

NOTE: [Linear Implementation](https://algo.minetest.in/3-Sorting/9-Priority_Queues_and_Heapsort/2-Heap_Data_Structure/) , [Tree Implementation](https://algo.minetest.in/3-Sorting/9-Priority_Queues_and_Heapsort/3-Algorithms_on_heap/)

The PQ algorithms on heaps all work by first making a simple modification that could violate the heap condition and them traversing  the and restoring the heap condition everywhere. This is known as ***Heapifying*** or ***fixing*** the heap.

There are 2 possibilities

1. Priority of some node is increased : To fix it node should swim up the tree
2. Priority of some node in decreased : To fix it node should swim down the tree

## STL & Python Usage

### Python (heapq) — Min-Heap by Default

| **Operation**          | **Function**                  | **Notes**                       |
| ---------------------- | ----------------------------- | ------------------------------- |
| Create heap            | heapq.heapify(list)           | Converts a list into a heap     |
| Insert item            | heapq.heappush(heap, item)    | Adds an item                    |
| Remove min             | heapq.heappop(heap)           | Pops the smallest item          |
| Peek min               | heap[0]                       | Doesn’t remove                  |
| Replace                | heapq.heapreplace(heap, item) | Pops min & pushes item (faster) |
| Push-Pop               | heapq.heappushpop(heap, item) | Push then pop (more efficient)  |
| Merge sorted iterables | heapq.merge(*iterables)       | Useful for external sorting     |

* heapq is a **min-heap** → use **negative values** for max-heap behavior
* No built-in support for 
    * Updating/removing arbitrary elements (requires rebuild)
    * Custom comparators (use Tuple Keys)
* Not thread-safe (`queue.PriorityQueue` is used for threading)

### C++ (std::priority_queue) — Max-Heap by Default

| **Operation** | **Function**      | **Notes**             |
| ------------- | ----------------- | --------------------- |
| Create heap   | priority_queue<T> | Max-heap by default   |
| Insert item   | pq.push(item)     | Adds an item          |
| Remove max    | pq.pop()          | Pops the largest item |
| Peek max      | pq.top()          | Doesn’t remove        |
| Check empty   | pq.empty()        |                       |
| Size          | pq.size()         |                       |

* for min-heap : `priority_queue<int, vector<int>, greater<int>> minHeap;`

````c++
// custom comparator
struct Task {
    int priority;
    string name;
    bool operator<(const Task& other) const {
        return priority < other.priority;  // max-heap
    }
};
priority_queue<Task> pq;
````

* use locks if needed for threading

## Problems

### Implement a Priority Queue using Binary Heap

A Binary Heap is a Binary Tree that satisfies the following conditions

- It should be Complete Binary Tree ~ A tree in which all levels are completely filled except last level and last level is filled in such a way that all keys are as left as possible.
- It should satisfy Heap Property

Min-Heap Property : For every node in Binary Heap, the node values are less than its right and left child's value.

As a Result Root is always the minimum Element in the Array.

![](assets/Pasted%20image%2020260119210935.png)

### Heap Sort (Concept)

**Heap Sort** is a **comparison-based, in-place sorting algorithm** that uses a **binary heap** data structure to sort elements in **O(n log n)** time.

Repeatedly extract the maximum (or minimum) element from a heap and place it in its correct position.

Building a Heap will take : $O(n)$ time using heapify operations
Additionally Popping n elements will take :  $O(n \log n)$

| Case        | Time            |
| ----------- | --------------- |
| Best        | O(n log n)      |
| Average     | O(n log n)      |
| Worst       | O(n log n)      |
| Extra Space | O(1) (in-place) |

NOTE: It is not a stable algorithm, and works in-place. Worst Case is guaranteed.
### Check if an array represents a min-heap or not

So left and right child should always be greater than the elements !

```python

def isHeap(nums):
    n = len(nums)

    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and nums[left] < nums[i]:
            return False

        if right < n and nums[right] < nums[i]:
            return False

    return True

```

### Convert min Heap to max Heap

Often Known as floyd's heap construction : $O(n)$ time.

Min Heap -> Max Heap

```python

def build_max_heap(nums):
    n = len(nums)

    def heapify(i):
        largest = i
        l = 2*i + 1
        r = 2*i + 2

        if l < n and nums[l] > nums[largest]:
            largest = l
        if r < n and nums[r] > nums[largest]:
            largest = r

        if largest != i:
            nums[i], nums[largest] = nums[largest], nums[i]
            heapify(largest)

    for i in range(n//2 - 1, -1, -1):
        heapify(i)

```

Max Heap -> Min Heap

```python

def build_min_heap(nums):
    n = len(nums)

    def heapify(i):
        smallest = i
        l = 2*i + 1
        r = 2*i + 2

        if l < n and nums[l] < nums[smallest]:
            smallest = l
        if r < n and nums[r] < nums[smallest]:
            smallest = r

        if smallest != i:
            nums[i], nums[smallest] = nums[smallest], nums[i]
            heapify(smallest)

    for i in range(n//2 - 1, -1, -1):
        heapify(i)

```

You only need to know one of above methods, you could negate elements and apply the heapify operations again and then negate elements to restore signs.