# Network Flow

Network flow models movement of a commodity (data, water, traffic) through a directed graph from a **source** `s` to a **sink** `t`. Each edge has a **capacity** - the max amount of flow it can carry.

**Goal:** Find the maximum amount of flow that can be pushed from `s` to `t`.

![Max Flow](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Pets_flow.svg/960px-Pets_flow.svg.png)
## Key Concepts

* **Residual Graph:** For each edge `(u, v)` with capacity `c` and current flow `f`:
    - forward edge `(u, v)` with remaining capacity `c - f`
    - backward edge `(v, u)` with capacity `f` (allows undoing flow)

* **Augmenting Path:** Any path from `s` to `t` in the residual graph with available capacity. Keep pushing flow along augmenting paths until none exist.

* **Max-Flow Min-Cut Theorem:** Maximum flow = minimum cut capacity. A cut partitions vertices into two sets S (containing s) and T (containing t); the cut capacity is the sum of capacities of edges going from S to T.

## Algorithms

| Algorithm | Path Finding | Time Complexity |
|---|---|---|
| Ford-Fulkerson | DFS (any path) | $O(E \cdot maxFlow)$ - not polynomial |
| Edmonds-Karp | BFS (shortest path) | $O(VE^2)$ |
| Dinic's | BFS level graph + DFS | $O(V^2E)$ |

> For interviews: know Edmonds-Karp. It's Ford-Fulkerson with BFS, which guarantees polynomial time.

## Edmonds-Karp

Uses BFS to always find the shortest augmenting path (fewest edges). This bounds the number of augmentations to $O(VE)$.

```python
from collections import deque

def edmonds_karp(graph, source, sink, n):
    # graph[u][v] = residual capacity of edge u -> v
    max_flow = 0

    while True:
        parent = [-1] * n
        parent[source] = source
        q = deque([source])
        while q and parent[sink] == -1:
            u = q.popleft()
            for v in range(n):
                if parent[v] == -1 and graph[u][v] > 0:
                    parent[v] = u
                    q.append(v)

        if parent[sink] == -1:     # no augmenting path
            break

        # bottleneck = min capacity along the path
        flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            flow = min(flow, graph[u][v])
            v = u

        # update residual graph
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= flow
            graph[v][u] += flow
            v = u

        max_flow += flow

    return max_flow
```

## Bipartite Matching

The most common interview-relevant application. Given two disjoint sets L and R, find the maximum number of pairs `(l, r)` where an edge exists between them.

Model as flow: `source → each L node (cap 1) → edges → each R node (cap 1) → sink`. Run max flow = max matching.

![Bipartite Matching](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Simple_bipartite_graph%3B_two_layers.svg/3840px-Simple_bipartite_graph%3B_two_layers.svg.png)

![Bipartite Graph Flat](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Simple_bipartite_graph%3B_no_crossings.svg/3840px-Simple_bipartite_graph%3B_no_crossings.svg.png)

```python
def bipartite_matching(n, m, edges):
    # n = |L|, m = |R|, edges = [(l, r), ...] (0-indexed)
    # node layout: 0 = source, 1..n = L, n+1..n+m = R, n+m+1 = sink
    total = n + m + 2
    source, sink = 0, total - 1
    graph = [[0] * total for _ in range(total)]

    for i in range(1, n + 1):
        graph[source][i] = 1
    for l, r in edges:
        graph[l + 1][n + r + 1] = 1
    for j in range(n + 1, n + m + 1):
        graph[j][sink] = 1

    return edmonds_karp(graph, source, sink, total)
```

## References

* [Max-flow - Wikipedia](https://en.wikipedia.org/wiki/Maximum_flow_problem)
* [Ford-Fulkerson - Wikipedia](https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm)
* [Edmonds-Karp - cp-algorithms](https://cp-algorithms.com/graph/edmonds_karp.html)
* [Dinic's Algorithm - cp-algorithms](https://cp-algorithms.com/graph/dinic.html)
