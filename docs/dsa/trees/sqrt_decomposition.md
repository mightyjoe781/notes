# Sqrt Decomposition

* Divides the array into blocks of size roughly $\sqrt{n}$.
* Each block stores the minimum value of that block.
* Lazy array stores pending updates for each block.

Range Updates

* If the update range is within a single block, apply updates directly to elements and rebuild that block
* If the update range spans multiple blocks:
    * Update partial blocks at the edges directly.
    * For full blocks in between, store lazy updates and update block minimum directly.

Range Minimum Query

* If query range is within a single block, check elements directly.
* Otherwise, check partial blocks at edges and use stored block minimum or lazy values for full blocks in between.
* Using `float('inf')` as sentinel for "no update" can cause problems if `inf` is a valid value - prefer `None` to distinguish "no pending update".

```python

from math import isqrt

class SqrtDecomposition:
    def __init__(self, A):
        self.n = len(A)
        self.block_size = isqrt(self.n) or 1
        self.num_blocks = (self.n + self.block_size - 1) // self.block_size
        self.A = A[:]
        self.blocks = [float('inf')] * self.num_blocks
        self.lazy = [None] * self.num_blocks
        for b in range(self.num_blocks):
            self._rebuild(b)

    def _apply_lazy(self, b):
        if self.lazy[b] is not None:
            start = b * self.block_size
            end = min(self.n, start + self.block_size)
            for i in range(start, end):
                self.A[i] = self.lazy[b]
            self.blocks[b] = self.lazy[b]
            self.lazy[b] = None

    def _rebuild(self, b):
        start = b * self.block_size
        end = min(self.n, start + self.block_size)
        self.blocks[b] = min(self.A[start:end])

    def range_update(self, l, r, val):
        sb, eb = l // self.block_size, r // self.block_size

        if sb == eb:
            self._apply_lazy(sb)
            for i in range(l, r + 1):
                self.A[i] = val
            self._rebuild(sb)
        else:
            self._apply_lazy(sb)
            for i in range(l, (sb + 1) * self.block_size):
                self.A[i] = val
            self._rebuild(sb)

            for b in range(sb + 1, eb):
                self.lazy[b] = val
                self.blocks[b] = val

            self._apply_lazy(eb)
            for i in range(eb * self.block_size, r + 1):
                self.A[i] = val
            self._rebuild(eb)

    def range_min(self, l, r):
        sb, eb = l // self.block_size, r // self.block_size

        if sb == eb:
            self._apply_lazy(sb)
            return min(self.A[l:r + 1])

        self._apply_lazy(sb)
        mn = min(self.A[l:(sb + 1) * self.block_size])

        for b in range(sb + 1, eb):
            mn = min(mn, self.lazy[b] if self.lazy[b] is not None else self.blocks[b])

        self._apply_lazy(eb)
        mn = min(mn, min(self.A[eb * self.block_size:r + 1]))
        return mn

```

