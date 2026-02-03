# Range Updates & Queries

## Fenwick Tree (Binary Indexed Trees)

- Supports efficient prefix sums (range sum queries from index 1 to \(j\)) and point updates.
- Internally stores cumulative frequencies in a vector ⁠ft.
- Memory Efficient Alternative to Segment Tree

Operations

- Point Update : $O(\log n)$
- Prefix Sum Query : $O(\log n)$
- Range Sum Query : $O(\log n)$

In Fenwick Tree, each index stores a sum of range of numbers : `[i - LSB(i) + 1, i]`, where `LSB(i) = i & -i`.

Above property allows logarithmic traversal up/down.

## Simple Implementation

* Here we have assumed that `n` would be a perfect power of two, if thats not the case, then make it.

````c++
#include <vector>
using namespace std;

class FenwickTree {
private:
    vector<long long> ft;

    int LSOne(int s) { return s & -s; }

public:
    FenwickTree(int n) {
        ft.assign(n + 1, 0); // 1-based indexing
    }

    // Point update: add v to index i
    void update(int i, long long v) {
        while (i < (int)ft.size()) {
            ft[i] += v;
            i += LSOne(i);
        }
    }

    // Prefix sum query: sum[1..i]
    long long rsq(int i) {
        long long sum = 0;
        while (i > 0) {
            sum += ft[i];
            i -= LSOne(i);
        }
        return sum;
    }

    // Range sum query: sum[i..j]
    long long rsq(int i, int j) {
        return rsq(j) - rsq(i - 1);
    }
};
````

Python Implementation

```python

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.ft = [0] * (n + 1)   # 1-based indexing

    def _lsb(self, i):
        return i & -i

    def update(self, i, v):
        while i <= self.n:
            self.ft[i] += v
            i += self._lsb(i)

    def prefix_sum(self, i):
        s = 0
        while i > 0:
            s += self.ft[i]
            i -= self._lsb(i)
        return s

    def range_sum(self, l, r):
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

```

Building Fenwick Tree in $O(n)$.

Instead of calling update repeatedly $O(n \log n)$, we propagate values upwards

```python

class FenwickTree:
    def __init__(self, arr):
        self.n = len(arr) - 1  # arr must be 1-indexed
        self.ft = arr[:]

        for i in range(1, self.n + 1):
            j = i + (i & -i)
            if j <= self.n:
                self.ft[j] += self.ft[i]

```

Select `k-th` Element (Prefix Sum $\ge$ k)

Used in

- Order Statistics
- Finding `k-th` smallest frequency

```python

def select(self, k):
    idx = 0
    bit_mask = 1 << (self.n.bit_length() - 1)

    while bit_mask:
        nxt = idx + bit_mask
        if nxt <= self.n and self.ft[nxt] < k:
            k -= self.ft[nxt]
            idx = nxt
        bit_mask >>= 1

    return idx + 1

```

## Range Update Point Query & Range Query

* Supports **range updates** & **point queries**
* Uses a Fenwick Tree internally but updates the Fenwick Tree in a way that a range update is simulated by two point updates.

Usually representing updates as difference array, and prefix sum restores the actual values. Fenwick Array Represents the `diff`

```
diff[l] += v
diff[r+1] -= v
```


```python

# fenwick tree store diff
class RUPQ:
    def __init__(self, n):
        self.ft = FenwickTree(n)

    def range_update(self, l, r, v):
        self.ft.update(l, v)
        self.ft.update(r + 1, -v)

    def point_query(self, i):
        return self.ft.prefix_sum(i)
        
# to support Range Query, we use second Fenwick Tree, storing count
class RURQ:
    def __init__(self, n):
        self.n = n
        self.ft1 = FenwickTree(n)
        self.ft2 = FenwickTree(n)

    def _update(self, ft, i, v):
        while i <= self.n:
            ft.ft[i] += v
            i += i & -i

    def range_update(self, l, r, v):
        self._update(self.ft1, l, v)
        self._update(self.ft1, r + 1, -v)

        self._update(self.ft2, l, v * (l - 1))
        self._update(self.ft2, r + 1, -v * r)

    def prefix_sum(self, x):
        return (
            x * self.ft1.prefix_sum(x)
            - self.ft2.prefix_sum(x)
        )

    def range_sum(self, l, r):
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

```

## Problems

### Range Sum Query - Mutable

*Above Implementation already solves this problem*

### Count of Smaller Numbers after Self

LeetCode : 315
For each element, count how many numbers to its right are smaller than it.

Topics it covers

- Fenwick Tree as a frequency table
- Co-ordinate Compression
- Offline Queries

```python
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.ft = [0] * (n + 1)

    def update(self, i, v):
        while i <= self.n:
            self.ft[i] += v
            i += i & -i

    def query(self, i):
        s = 0
        while i > 0:
            s += self.ft[i]
            i -= i & -i
        return s

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        n = len(nums)
        
        # Step 1: coordinate compression
        sorted_vals = sorted(set(nums))
        rank = {v: i + 1 for i, v in enumerate(sorted_vals)}

        # Fenwick Tree over frequencies
        ft = FenwickTree(len(sorted_vals))
        res = [0] * n

        # Step 2: traverse from right to left
        for i in range(n - 1, -1, -1):
            r = rank[nums[i]]
            res[i] = ft.query(r - 1)   # count smaller elements
            ft.update(r, 1)            # mark current number

        return res
```

### K-th Order Statistics

*Already solved above*

