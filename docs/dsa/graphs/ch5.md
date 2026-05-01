# Minimum Spanning Trees

Given a connected, undirected, weighted graph G, select a subset $E' \subseteq G$ such that the graph G is still connected and the total weight of selected edges $E'$ is minimal.

To satisfy the connectivity requirement:

- We need at least V-1 edges that form a tree spanning all $V$ vertices.

MST can be solved with several well-known algorithms:
- Prim's
- Kruskal's

Applications of MSTs:

* **Network Design:** Minimize cost of laying cable networks.
* **Clustering and Machine Learning:** Remove expensive edges in a tree structure.
* **TSP (Travelling Salesman Problem):** Used for approximation solutions.
* **Pathfinding Algorithms in Games:** Often use MST-based approaches.

## Prim's Algorithm

Start from any vertex, flag it as visited, and push its adjacent edges into a min-heap. Greedily pick the minimum-weight edge whose destination hasn't been visited (to prevent cycles), add its weight to the MST, and enqueue the new vertex's edges.

- Time: $O(E \log E) = O(E \log V)$

```python
import heapq

def prims_mst(n, adj):
    # adj[u] = [(v, weight), ...]
    visited = [False] * n
    pq = [(0, 0)]  # (weight, vertex), start from vertex 0
    mst_weight = 0

    while pq:
        w, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        mst_weight += w
        for v, wt in adj[u]:
            if not visited[v]:
                heapq.heappush(pq, (wt, v))

    return mst_weight
```

## Kruskal's Algorithm

Sort all edges by weight in non-decreasing order. Greedily add each edge to the MST as long as it doesn't form a cycle (checked via Union-Find).

- Time: $O(E \log E + E \cdot \alpha(V)) \approx O(E \log V)$

```python
def kruskals_mst(n, edges):
    # edges = [(weight, u, v), ...]
    uf = UnionFind(n)
    edges.sort()
    mst_weight = 0

    for w, u, v in edges:
        if uf.union(u, v):
            mst_weight += w

    return mst_weight
```

## Union-Find

See [Union-Find](../dsu.md) for the full Python implementation with path compression and union by rank.

Quick reference for MST use:

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

## Famous Variants of MST Applications

#### Maximum Spanning Tree

Modify Kruskal's: sort edges in **non-increasing** weight order instead.

#### Minimum Spanning Subgraph

Some edges are already fixed and must be included. Add the fixed edges first (and their costs), then continue running Kruskal's on the remaining free edges until the graph is connected. The result may not be a tree, hence "subgraph" rather than "tree".

#### Minimum Spanning Forest

Build a forest of exactly K connected components at minimum cost. Run Kruskal's normally, but terminate as soon as the number of connected components equals K.

#### Second Best Spanning Tree

1. Sort edges in $O(E \log V)$.
2. Find the MST using Kruskal's in $O(E)$.
3. For each edge in the MST, temporarily exclude it and find the best spanning tree without it in $O(E)$.
4. The best result across all exclusions is the second-best ST.

Total: $O(E \log V + E + VE) = O(EV)$

#### Minimax (and Maximin)

The minimax path problem: find the path from i to j that minimizes the maximum edge weight along the path.

This maps directly to an MST problem. The MST already captures paths with low individual edge weights. The minimax path between any two vertices i and j is the maximum edge weight on the unique path between them in the MST.

Total complexity: $O(E \log V + V) = O(E \log V)$

## Problems

1. https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1 — Implement Prim's algorithm.
2. https://www.geeksforgeeks.org/problems/disjoint-set-union-find/1 — Recursive Find implementation.
3. https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1 — Same problem, use Kruskal's. Unpack the adjacency graph into edges, using each undirected edge only once.
4. https://leetcode.com/problems/number-of-operations-to-make-network-connected/ — Use Union-Find to count components; rest is arithmetic.
5. https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/ — Complex; recommended to read discussion.
6. https://leetcode.com/problems/accounts-merge/description/ — Track owners separately, build union-find on email strings, then reconstruct with owner names.
7. https://leetcode.com/problems/number-of-islands-ii/ — Treat the 2D array as a flattened 1D array to simplify the Union-Find implementation.
8. https://leetcode.com/problems/swim-in-rising-water/ — Solvable with MST (Kruskal's) as an alternative to Dijkstra.
