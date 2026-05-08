# Segment Trees

* **Segment Tree** with **lazy propagation** is used to efficiently handle range updates and range minimum queries (RMQ).
* A segment tree stores **answers for ranges**, so queries can be answered by **combining a few precomputed segments**.
* For array of size $n$
    * Root -> entire range `[0,n-1]`
    * Each node would split its range into two halves
    * Leaves will represent single elements
* Segment trees provide fast $O(\log n)$ queries and updates, making them ideal for dynamic array problems.
* to get RSQ (Range Sum Query) in Segment Tree
    * In build function replace : `st[p] = min(st[2*p], st[2*p+1]);` with `st[p] = st[2*p] + st[2*p+1];`
    * In query function : `min(query(...), query(...));`  with `query(...left...) + query(...right...);`
    * In update function : `st[p] = st[2*p] + st[2*p+1];`

![](assets/Pasted%20image%2020260114085402.png)

| **Operation**    | **Fenwick Tree** | **Segment Tree** |
| ---------------- | ---------------- | ---------------- |
| **Point Update** | ✅ O(log n)       | ✅ O(log n)       |
| **Range Query**  | ✅ O(log n)       | ✅ O(log n)       |
| **Range Update** | Not Supported    | ✅ (needs lazy)   |
| **Point Query**  | Not Supported    | ✅                |

NOTE: Think of segment tree like a framework, not as an algorithm.

Key Idea :

- If a node covers a single element store that element
- otherwise split range into two halves
    - build left and right
    - combine results

Usually when we are pushing updates to the tree then it needs to be propagated to leaves, but in case we don't wanna do it right away, we can store it intermediate and evaluate only when required (Lazy Propagation).

## Segment Tree (without Lazy Propagation)

* Only Point Updates are available

```python

class SegmentTree:
    def __init__(self, A):
        self.n = len(A)
        self.st = [0] * (4 * self.n)
        self._build(A, 1, 0, self.n - 1)

    def _l(self, p):
        return p << 1

    def _r(self, p):
        return (p << 1) + 1

    def _build(self, A, p, L, R):
        if L == R:
            self.st[p] = A[L]
        else:
            m = (L + R) // 2
            self._build(A, self._l(p), L, m)
            self._build(A, self._r(p), m + 1, R)
            self.st[p] = min(self.st[self._l(p)], self.st[self._r(p)])

    def _query(self, p, L, R, i, j):
        if j < L or i > R:
            return float("inf")
        if i <= L and R <= j:
            return self.st[p]
        m = (L + R) // 2
        return min(
            self._query(self._l(p), L, m, i, j),
            self._query(self._r(p), m + 1, R, i, j)
        )

    def _update(self, p, L, R, idx, val):
        if L == R:
            self.st[p] = val
        else:
            m = (L + R) // 2
            if idx <= m:
                self._update(self._l(p), L, m, idx, val)
            else:
                self._update(self._r(p), m + 1, R, idx, val)
            self.st[p] = min(self.st[self._l(p)], self.st[self._r(p)])

    # public API
    def query(self, i, j):
        return self._query(1, 0, self.n - 1, i, j)

    def update(self, idx, val):
        if 0 <= idx < self.n:
            self._update(1, 0, self.n - 1, idx, val)

```

## Segment Tree with Lazy Propagation (Optimal)

```python

class SegmentTreeLazy:
    def __init__(self, A):
        self.n = len(A)
        self.A = A[:]
        self.st = [0] * (4 * self.n)
        self.lazy = [-1] * (4 * self.n)
        self._build(1, 0, self.n - 1)

    def _l(self, p):
        return p << 1

    def _r(self, p):
        return (p << 1) + 1

    def _conquer(self, a, b):
        if a == -1:
            return b
        if b == -1:
            return a
        return min(a, b)

    def _build(self, p, L, R):
        if L == R:
            self.st[p] = self.A[L]
        else:
            m = (L + R) // 2
            self._build(self._l(p), L, m)
            self._build(self._r(p), m + 1, R)
            self.st[p] = self._conquer(
                self.st[self._l(p)], self.st[self._r(p)]
            )

    def _propagate(self, p, L, R):
        if self.lazy[p] != -1:
            self.st[p] = self.lazy[p]
            if L != R:
                self.lazy[self._l(p)] = self.lazy[p]
                self.lazy[self._r(p)] = self.lazy[p]
            else:
                self.A[L] = self.lazy[p]
            self.lazy[p] = -1

    def _rmq(self, p, L, R, i, j):
        self._propagate(p, L, R)
        if i > j:
            return -1
        if i <= L and R <= j:
            return self.st[p]

        m = (L + R) // 2
        return self._conquer(
            self._rmq(self._l(p), L, m, i, min(m, j)),
            self._rmq(self._r(p), m + 1, R, max(i, m + 1), j)
        )

    def _update(self, p, L, R, i, j, val):
        self._propagate(p, L, R)
        if i > j:
            return
        if i <= L and R <= j:
            self.lazy[p] = val
            self._propagate(p, L, R)
        else:
            m = (L + R) // 2
            self._update(self._l(p), L, m, i, min(m, j), val)
            self._update(self._r(p), m + 1, R, max(i, m + 1), j, val)

            left_val = (
                self.lazy[self._l(p)]
                if self.lazy[self._l(p)] != -1
                else self.st[self._l(p)]
            )
            right_val = (
                self.lazy[self._r(p)]
                if self.lazy[self._r(p)] != -1
                else self.st[self._r(p)]
            )

            self.st[p] = (
                self.st[self._l(p)]
                if left_val <= right_val
                else self.st[self._r(p)]
            )

    # public API
    def RMQ(self, i, j):
        return self._rmq(1, 0, self.n - 1, i, j)

    def update(self, i, j, val):
        self._update(1, 0, self.n - 1, i, j, val)

```

## Sweep Line Segment Tree


```python

class SegmentTree:
    def __init__(self, xs):
        self.xs = xs
        self.n = len(xs) - 1
        self.covered = [0] * (4 * self.n)
        self.count = [0] * (4 * self.n)

    def _update(self, p, L, R, i, j, val):
        # no overlap
        if self.xs[R + 1] <= i or self.xs[L] >= j:
            return

        # total cover
        if i <= self.xs[L] and self.xs[R + 1] <= j:
            self.count[p] += val
        else:
            m = (L + R) // 2
            self._update(p * 2, L, m, i, j, val)
            self._update(p * 2 + 1, m + 1, R, i, j, val)

        # pull up
        if self.count[p] > 0:
            self.covered[p] = self.xs[R + 1] - self.xs[L]
        elif L == R:
            self.covered[p] = 0
        else:
            self.covered[p] = (
                self.covered[p * 2] + self.covered[p * 2 + 1]
            )

    def update(self, i, j, val):
        self._update(1, 0, self.n - 1, i, j, val)

    def query(self):
        return self.covered[1]

```

