# Shortest Path

**Definition:** *A **shortest path** between two vertices s and t in a weighted digraph is a directed simple path from s to t with the property that no other such path has a lower weight.*

**Source-sink shortest path:** Given a start vertex s and finish vertex t, find a shortest path from s to t.

**Single-source shortest path:** Given a start vertex s, find the shortest path from s to each other vertex in the graph.

**All-pairs shortest path:** Find the shortest path connecting each pair of vertices in the graph.

## Underlying Principle

Two core operations are applied repeatedly:

*Edge relaxation* — test whether traveling along a given edge gives a new shortest path to its destination vertex.

*Path relaxation* — test whether traveling through a given vertex gives a new shortest path connecting two other vertices.

**Property:** *If vertex x is on a shortest path from s to t, then that path consists of a shortest path from s to x followed by a shortest path from x to t.*

### Dijkstra's Algorithm (Single-Source)

**Property:** *Dijkstra's algorithm solves the single-source shortest-paths problem in graphs that have **non-negative weights**.*

Uses a min-heap priority queue. At each step, greedily picks the unvisited vertex with the smallest known distance and relaxes its edges.

- Time: $O((V + E) \log V)$ with a binary heap.

```python
import heapq

def dijkstra(n, edges, src):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]  # (distance, vertex)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist
```

To also track and reconstruct the path:

```python
def dijkstra_with_path(n, edges, src):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    parent = [-1] * n
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, parent

def restore_path(src, dst, parent):
    path = []
    v = dst
    while v != src:
        path.append(v)
        v = parent[v]
    path.append(src)
    return path[::-1]
```

## Floyd-Warshall Algorithm (All-Pairs)

Finds shortest paths between all pairs of vertices. Handles negative edge weights but not negative cycles.

- Time: $O(V^3)$, Space: $O(V^2)$

```python
def floyd_warshall(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):
        for u in range(n):
            for v in range(n):
                if dist[u][k] + dist[k][v] < dist[u][v]:
                    dist[u][v] = dist[u][k] + dist[k][v]

    return dist
```

To also print shortest paths, maintain a parent matrix:

```python
def floyd_warshall_with_path(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    parent = [[i] * n for i in range(n)]

    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):
        for u in range(n):
            for v in range(n):
                if dist[u][k] + dist[k][v] < dist[u][v]:
                    dist[u][v] = dist[u][k] + dist[k][v]
                    parent[u][v] = parent[k][v]

    return dist, parent

def print_path(u, v, parent):
    if u == v:
        print(u, end=" ")
        return
    print_path(u, parent[u][v], parent)
    print(v, end=" ")
```

## Bellman-Ford Algorithm

Used to find shortest paths from a source node to all others, even with negative edge weights.

* Works for both directed and undirected graphs.
* Handles **negative edge weights**, unlike Dijkstra's.
* Detects **negative weight cycles**.
* Time: $O(V \times E)$

```python
def bellman_ford(n, edges, src):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # check for negative weight cycles
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return []  # negative cycle detected

    return dist
```

### Other Applications of Floyd-Warshall

#### Transitive Closure (Warshall's Algorithm)

Determine if vertex i can reach vertex j, directly or indirectly. Use bitwise OR instead of arithmetic for speed.

```python
def warshall(adj, n):
    # adj[i][j] = 1 if edge i->j exists, else 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                adj[i][j] |= adj[i][k] & adj[k][j]
    return adj
```

#### Minimax and Maximin

Find the path from i to j that minimizes the maximum edge weight along the path.

```python
def minimax(dist, n):
    # initialize dist[i][j] to edge weight, INF if no direct edge
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], max(dist[i][k], dist[k][j]))
    return dist
```

NOTE: Works only for $V \le 400$ due to $O(V^3)$ complexity.

#### Finding the Cheapest/Negative Cycle

Initialize `dist[i][i] = INF` (diagonal), then run Floyd-Warshall. If `dist[i][i]` is no longer INF for any $i$, a cycle exists. The smallest non-negative `dist[i][i]` is the cheapest cycle. If `dist[i][i] < 0`, a negative cycle exists.

#### Finding the Diameter of a Graph

After running Floyd-Warshall, the diameter is the maximum finite value in the distance matrix.

#### Finding SCCs of a Directed Graph

For small graphs ($O(V^3)$): if `dist[i][j] > 0 and dist[j][i] > 0`, then vertices i and j belong to the same SCC. For larger graphs, use Tarjan's or Kosaraju's algorithm.

## Summary

| Algorithm      | Graph Type          | Complexity            | Special Features                         |
| -------------- | ------------------- | --------------------- | ---------------------------------------- |
| BFS            | Unweighted          | $O(V + E)$            | Layer-by-layer exploration               |
| Dijkstra       | Weighted (Non-Neg.) | $O((V + E) \log V)$   | Priority queue-based; greedy approach    |
| Bellman-Ford   | Weighted (Neg.)     | $O(V \times E)$       | Handles negative weights; detects cycles |
| Floyd-Warshall | All-Pairs / Small   | $O(V^3)$              | Solves all-pairs shortest paths          |

## Problems

1. https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1 — No need to track visited since BFS on an unweighted graph processes layer by layer.
2. https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph/1 — A visited array is needed here for safety and efficiency.
3. https://www.geeksforgeeks.org/problems/implementing-dijkstra-set-1-adjacency-matrix/1 — Try implementing using a `set` instead of a priority queue.

| **Aspect**               | **Priority Queue**                              | **Set**                                                                 |
|--------------------------|-------------------------------------------------|-------------------------------------------------------------------------|
| **Insertion Time**        | $O(\log N)$                                    | $O(\log N)$                                                            |
| **Update Time**           | Not supported directly; push new value instead | $O(\log N)$: Remove old value, insert new value                        |
| **Deletion Time**         | $O(\log N)$                                    | $O(\log N)$                                                            |
| **Ease of Implementation**| Simple (standard `heapq`)                      | More complex, as updates require additional operations                 |
| **Duplicates**            | Allows duplicates                               | Does not allow duplicates                                              |
| **Space Usage**           | May grow larger due to duplicate entries        | Minimal, keeps only one instance of each node                          |
| **Efficiency in Practice**| Generally faster due to less overhead           | Slightly slower due to extra bookkeeping                               |

4. https://leetcode.com/problems/shortest-path-in-binary-matrix/ — The question only asks for a specific target, so optimize space by not storing all distances.
5. https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/ — Keep a `ways` array alongside `dist` and increment it each time an equal-cost path is found.

6. https://leetcode.com/problems/path-with-minimum-effort/ — Modify Dijkstra's priority function to minimize the maximum absolute difference along the path.

7. https://leetcode.com/problems/network-delay-time/ — Straightforward: find all distances, return the maximum.

8. https://www.geeksforgeeks.org/problems/minimum-multiplications-to-reach-end/1 — No explicit graph needed. Think of it as a BFS over 1e5 states connected by multiplication rules.

9. https://leetcode.com/problems/cheapest-flights-within-k-stops/ — Cheapest flight within K stops. This is **not** a standard Dijkstra problem because optimal cost may require more than k stops.

```python
from collections import defaultdict
from functools import cache

def findCheapestPrice(n, flights, src, dst, k):
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))

    @cache
    def dfs(i, stops):
        if i == dst:
            return 0
        if stops < 0:
            return float('inf')
        cost = float('inf')
        for v, w in graph[i]:
            cost = min(cost, w + dfs(v, stops - 1))
        return cost

    res = dfs(src, k)
    return -1 if res == float('inf') else res
```

10. https://www.geeksforgeeks.org/problems/distance-from-the-source-bellman-ford-algorithm/1 — Use Bellman-Ford.
11. https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/description/ — Use Floyd-Warshall and post-process the resulting matrix per the problem conditions.
12. https://leetcode.com/problems/swim-in-rising-water/ — Use Dijkstra to find the path that minimizes the maximum element encountered.
