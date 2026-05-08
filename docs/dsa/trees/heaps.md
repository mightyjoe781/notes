# Heap

> for detailed description on this topic refer to Heaps Section specifically.

## Simple Max-Heap Implementation

```python

class MaxHeap:
    def __init__(self, arr=None):
        self.heap = list(arr or [])
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sink(i)

    def _parent(self, i): return (i - 1) // 2
    def _left(self, i):   return 2 * i + 1
    def _right(self, i):  return 2 * i + 2

    def _swim(self, i):
        while i > 0 and self.heap[self._parent(i)] < self.heap[i]:
            p = self._parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def _sink(self, i):
        n = len(self.heap)
        while self._left(i) < n:
            j = self._left(i)
            if self._right(i) < n and self.heap[self._right(i)] > self.heap[j]:
                j = self._right(i)
            if self.heap[i] >= self.heap[j]:
                break
            self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
            i = j

    def insert(self, val):
        self.heap.append(val)
        self._swim(len(self.heap) - 1)

    def get_max(self):
        return self.heap[0] if self.heap else -1

    def remove_max(self):
        if not self.heap: return -1
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._sink(0)
        return self.heap[0] if self.heap else -1

```

### Summary of Operations

| **Operation**       | **Method**   | **Complexity** |
| ------------------- | ------------ | -------------- |
| Insert item         | insert(val)  | O(log n)       |
| Remove max          | removeMax()  | O(log n)       |
| Peek max            | getMax()     | O(1)           |
| Build heap from arr | MaxHeap(arr) | O(n)           |

### Min-Heap Implementation

To convert Max-Heap into a Min-Heap:

* In `_swim()` : change `<` to `>`
* In `_sink()` : change `>` to `<`

In practice, Python's `heapq` module is a min-heap by default. For a max-heap, negate values on push/pop.