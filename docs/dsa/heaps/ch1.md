# Priority Queue & HeapSort

*A priority queue is a data structure of items with keys that supports two basic operation*

* insert a new item
* remove the item with the largest key

Applications

* Simulation Systems (keys ~ event times)
* Job scheduling (keys ~ priority)
* Numerical computation ( keys ~ computation errors )

NOTE: [Linear Implementation](https://algo.minetest.in/3-Sorting/9-Priority_Queues_and_Heapsort/2-Heap_Data_Structure/) , [Tree Implementation](https://algo.minetest.in/3-Sorting/9-Priority_Queues_and_Heapsort/3-Algorithms_on_heap/)

The PQ algorithms on heaps all work by first making a simple  modification that could violate the heap condition and them traversing  the and restoring the heap condition everywhere. This is known as ***Heapifying*** or ***fixing*** the heap.

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

### Problems

* Implement a Priority Queue using Heap
* Heap Sort (Concept)
* Build a Max Heap from an Array