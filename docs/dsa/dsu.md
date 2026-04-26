# DSU

## Union-Find (Simple)

````c++
class UnionFind {
private:
  vector<int> p;
public:
  UnionFind(int N) {
    p.assign(N, 0); 
    for (int i = 0; i < N; ++i) 
      p[i] = i;
  }

  int findSet(int i) { return (p[i] == i) ? i : (p[i] = findSet(p[i])); }
  bool unionSet(int i, int j) {
    int x = findSet(i), y = findSet(j);
    if(x == y) return false;
    p[x] = y;
    return true;
  }
};
````



## Union-Find (Fastest Implementation)

````c++
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

class UnionFind {                                // OOP style
private:
  vi p, rank, setSize;                           // vi p is the key part
  int numSets;
public:
  UnionFind(int N) {
    p.assign(N, 0); for (int i = 0; i < N; ++i) p[i] = i;
    rank.assign(N, 0);                           // optional speedup
    setSize.assign(N, 1);                        // optional feature
    numSets = N;                                 // optional feature
  }

  int findSet(int i) { return (p[i] == i) ? i : (p[i] = findSet(p[i])); }
  bool isSameSet(int i, int j) { return findSet(i) == findSet(j); }

  int numDisjointSets() { return numSets; }      // optional
  int sizeOfSet(int i) { return setSize[findSet(i)]; } // optional

  bool unionSet(int i, int j) {
    if (isSameSet(i, j)) return false;           // i and j are in same set
    int x = findSet(i), y = findSet(j);          // find both rep items
    if (rank[x] > rank[y]) swap(x, y);           // keep x 'shorter' than y
    p[x] = y;                                    // set x under y
    if (rank[x] == rank[y]) ++rank[y];           // optional speedup
    setSize[y] += setSize[x];                    // combine set sizes at y
    --numSets;                                   // a union reduces numSets
    return true;
  }
};
````

## Python Implementation

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

```python
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.num_sets
```

### Largest Component Size

```python
def largest_component(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return max(uf.set_size(i) for i in range(n))
```

More graph applications (Kruskal's MST) are in the [Graph Section](graphs/ch5.md).