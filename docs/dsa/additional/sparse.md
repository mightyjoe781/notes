# Sparse Tables & Range Queries

- A **Sparse Table (ST)** is a **static data structure** used to answer **idempotent range queries** (like min, max, GCD, LCM, XOR, etc.) in **O(1)** time after **O(n log n)** preprocessing.
- Use Cases
    - RMQ
    - Range GCD/LCM
    - Range XOR/AND/OR
    - LCA (Lowest Common Ancestor)
    - Binary Lifting/kth ancestor queries
- This topic is very crucial for competitive coding. Interviews often prefer Segment Trees over these due to their dynamic nature.
- Time Complexity
    - Preprocessing : $O(n \log n)$
    - Query: $O(1)$ for idempotent functions
- Concept:
    - Precompute answers for all intervals of length $2^j$ for all positions.
    - For a function `f` (idempotent) e.g. min, gcd : ` s[i][j] = f(st[i][j-1], st[i + 2^(j-1)][j-1])`
    - Query over the range `[L, R]` becomes

````python
j = log2(R - L + 1)
answer = f(st[L][j], st[R - 2^j + 1][j])
````

### RMQ Example

````python
def build_sparse_table(arr):
    from math import log2, floor
    n = len(arr)
    k = floor(log2(n)) + 1
    st = [[0] * k for _ in range(n)]

    for i in range(n):
        st[i][0] = arr[i]

    j = 1
    while (1 << j) <= n:
        i = 0
        while i + (1 << j) <= n:
            st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])
            i += 1
        j += 1
    return st

def query(st, L, R):
    from math import log2, floor
    j = floor(log2(R - L + 1))
    return min(st[L][j], st[R - (1 << j) + 1][j])
````

### Min/Max Example

````python
import math

def build_sparse_table_max(arr):
    n = len(arr)
    max_log = math.floor(math.log2(n)) + 1
    st = [[0] * max_log for _ in range(n)]

    for i in range(n):
        st[i][0] = arr[i]

    for j in range(1, max_log):
        for i in range(n - (1 << j) + 1):
            st[i][j] = max(st[i][j-1], st[i + (1 << (j-1))][j-1])

    return st

def query_max(l, r, st):
    j = math.floor(math.log2(r - l + 1))
    return max(st[l][j], st[r - (1 << j) + 1][j])
  
arr = [1, 3, 2, 7, 9, 11, 3, 5]

st = build_sparse_table_max(arr)

print(query_max(2, 5, st))  # Output: 11
print(query_max(0, 3, st))  # Output: 7
print(query_max(4, 7, st))  # Output: 11
````

### Binary Lifting & Sparse Tables

- Binary lifting is used in tree problems to quickly jump $2^k$ levels in $O(\log N)$
- Preprocess `parent[node][k] = parent[parent[node[k-1]][k-1]`
- Usage
    - Kth Ancestor Query
    - Lowest Common Ancestor (LCA)

### LCA using Sparse Tables (Euler Tour)

- Flatten tree using Euler Tour
- Store depth and first occurrence
- Use RMQ on depth over the Euler array using Sparse Table

````python
import math

class LCA_SparseTable:
    def __init__(self, n, tree):
        self.n = n
        self.tree = tree
        self.euler = []
        self.depth = []
        self.first_occurrence = [-1] * n
        self.visited = [False] * n

        self._dfs(0, 0)  # Root at 0
        self._build_sparse_table()

    def _dfs(self, node, d):
        self.visited[node] = True
        self.first_occurrence[node] = len(self.euler)
        self.euler.append(node)
        self.depth.append(d)

        for neighbor in self.tree[node]:
            if not self.visited[neighbor]:
                self._dfs(neighbor, d + 1)
                self.euler.append(node)
                self.depth.append(d)

    def _build_sparse_table(self):
        m = len(self.depth)
        k = math.floor(math.log2(m)) + 1
        self.st = [[0] * k for _ in range(m)]

        for i in range(m):
            self.st[i][0] = i  # Store index in depth[]

        for j in range(1, k):
            for i in range(m - (1 << j) + 1):
                left = self.st[i][j - 1]
                right = self.st[i + (1 << (j - 1))][j - 1]
                self.st[i][j] = left if self.depth[left] < self.depth[right] else right

    def lca(self, u, v):
        left = self.first_occurrence[u]
        right = self.first_occurrence[v]
        if left > right:
            left, right = right, left

        j = math.floor(math.log2(right - left + 1))
        left_index = self.st[left][j]
        right_index = self.st[right - (1 << j) + 1][j]
        return self.euler[left_index if self.depth[left_index] < self.depth[right_index] else right_index]
````



## Idempotent Function & Their Stability

Only idempotent function work efficiently
$$
f(f(a, b), b) = f(a, b)
$$

- Examples :
    - `min` , `max`
    - `gcd` , `lcm`
    - `XOR`, `AND`, `OR` (XOR is associative but not idempotent, it works)



### Comparison with Segment Tree

| **Feature**       | **Sparse Table**   | **Segment Tree**   |
| ----------------- | ------------------ | ------------------ |
| Query Time        | O(1) (idempotent)  | O(log n)           |
| Update Time       | ❌ (static only)    | ✅ O(log n)         |
| Space             | O(n log n)         | O(4n)              |
| Suitable for      | Static arrays      | Dynamic updates    |
| Common Operations | min, max, GCD, etc | All (with updates) |



### NOTE

**Hybrid Approaches**

- For large inputs, use block partitioning ($\sqrt n$ blocks) combined with Sparse Table for fast queries
- Examples : sqrt decomposition + ST for fast preprocessing & quick queries

**Offline Queries with Sparse Table**

- Useful in offline query prolems (given queries beforehand)
- Sort queries and answer with Sparse Table in O(1)
- Common Usecases
    - Mo’s Algorithm
    - Offline RMQ queries