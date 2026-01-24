# Heap

> for detailed description n this topic refer to Heaps Section specifically.

## Simple Max-Heap Implementation

````c++
#include <vector>
#include <iostream>
using namespace std;

class MaxHeap {
private:
    vector<int> heap;

    int parent(int i) { return (i - 1) / 2; }
    int left(int i)   { return 2 * i + 1; }
    int right(int i)  { return 2 * i + 2; }

    // Swim Up (Heapify Up)
    void swim(int i) {
        while (i > 0 && heap[parent(i)] < heap[i]) {
            swap(heap[i], heap[parent(i)]);
            i = parent(i);
        }
    }

    // Sink Down (Heapify Down)
    void sink(int i) {
        int n = heap.size();
        while (left(i) < n) {
            int j = left(i);
            if (right(i) < n && heap[right(i)] > heap[j])
                j = right(i); // pick the larger child
            if (heap[i] >= heap[j])
                break;
            swap(heap[i], heap[j]);
            i = j;
        }
    }

public:
    MaxHeap() {}

    MaxHeap(const vector<int>& arr) {
        heap = arr;
        for (int i = (int)heap.size() / 2 - 1; i >= 0; --i)
            sink(i); // heapify
    }

    void insert(int val) {
        heap.push_back(val);
        swim((int)heap.size() - 1);
    }

    int getMax() {
        return heap.empty() ? -1 : heap[0];
    }

    void removeMax() {
        if (heap.empty()) return;
        heap[0] = heap.back();
        heap.pop_back();
        sink(0);
    }

    void printHeap() {
        for (int x : heap)
            cout << x << ' ';
        cout << '\n';
    }
};
````

### Summary of Operations

| **Operation**       | **Method**   | **Complexity** |
| ------------------- | ------------ | -------------- |
| Insert item         | insert(val)  | O(log n)       |
| Remove max          | removeMax()  | O(log n)       |
| Peek max            | getMax()     | O(1)           |
| Build heap from arr | MaxHeap(arr) | O(n)           |

### Min - Heap Implementation

To convert Max-Heap Implementation into a Min-Heap one

* In `swim()` : change `<` to `>`
* In `sink()` : change `>` to `<`