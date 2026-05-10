# DSU

Disjoint Set Union (DSU), also called Union-Find, is a data structure that tracks elements partitioned into disjoint (non-overlapping) sets. Supports two operations:

- **find(x)** - find the representative (root) of the set containing x
- **union(x, y)** - merge the sets containing x and y

## Union-Find (Simple)

Path compression only. $O(\log N)$ amortized per operation.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        self.parent[px] = py
        return True
```

## Union-Find (Full)

Path compression + union by rank + set size tracking. Near $O(\alpha(N))$ amortized per operation (inverse Ackermann - effectively constant).

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.num_sets = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.num_sets -= 1
        return True

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def set_size(self, x):
        return self.size[self.find(x)]
```

## Applications

### Cycle Detection in Undirected Graph

**Problem:** Given n nodes and a list of edges, determine if the graph contains a cycle.

If `union(u, v)` returns `False`, the edge `(u, v)` creates a cycle (both endpoints already in the same set).

```python
def has_cycle(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return True
    return False
```

### Count Connected Components

**Problem:** Given n nodes and a list of undirected edges, return the number of connected components.

```python
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.num_sets
```

### Largest Component Size

**Problem:** Given n nodes and a list of undirected edges, return the size of the largest connected component.

```python
def largest_component(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return max(uf.set_size(i) for i in range(n))
```

More graph applications (Kruskal's MST) are in the [Graph Section](graphs/ch5.md).
