# Graph Traversal

## DFS

- Traverses graph in a depth-first manner.
- Time Complexity
    - $O(V+E)$: Adjacency List
    - $O(V^2)$: Adjacency Matrix

```python
def dfs(u, adj, visited):
    visited[u] = True
    for v in adj[u]:
        if not visited[v]:
            dfs(v, adj, visited)
```

[GFG DFS Problem](https://www.geeksforgeeks.org/problems/depth-first-traversal-for-a-graph/1)

[Clone Graph](https://leetcode.com/problems/clone-graph/)

## BFS

- Traverses graph in a breadth-first manner.
- Time Complexity
    - $O(V+E)$: Adjacency List
    - $O(V^2)$: Adjacency Matrix

```python
from collections import deque

def bfs(s, adj, n):
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

[GFG BFS Problem](https://www.geeksforgeeks.org/problems/bfs-traversal-of-graph/1)

## Multi-Source BFS

Standard BFS finds shortest distances from **one** source. Multi-source BFS seeds the queue with **multiple sources at distance 0** and expands outward simultaneously. Every cell gets the distance to its *nearest* source.

**When to use:** "distance to nearest X", "minimum steps to spread from all starting points", "walls that enclose all reachable cells".

```python
from collections import deque

def multi_source_bfs(grid, sources):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    q = deque()

    for r, c in sources:
        dist[r][c] = 0
        q.append((r, c))

    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))

    return dist
```

**Classic problems:**

*Rotting Oranges* - seed all rotten oranges (value 2) at t=0, BFS spreads to fresh (value 1). Answer is max distance reached; if any fresh remains at distance -1 → return -1.

*01 Matrix* - seed all 0-cells at distance 0, BFS gives nearest 0 for every cell.

*Walls and Gates* - seed all gates (0) at distance 0, BFS fills each empty room with minimum steps to nearest gate.

```python
def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1

    time = 0
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while q:
        r, c, t = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                time = t + 1
                q.append((nr, nc, t + 1))

    return time if fresh == 0 else -1
```

## Connected Components

Can be done using Union-Find or BFS as well.

```python
def count_components(adj, n):
    visited = [False] * n
    num_cc = 0

    for i in range(n):
        if not visited[i]:
            dfs(i, adj, visited)
            num_cc += 1

    return num_cc
```

https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/description/

## Flood Fill - Labeling/Coloring the Connected Components

This version counts the size of each component and recolors it.

```python
def flood_fill(grid, r, c, old_color, new_color):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return 0
    if grid[r][c] != old_color:
        return 0
    grid[r][c] = new_color
    count = 1
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
        count += flood_fill(grid, r + dr, c + dc, old_color, new_color)
    return count
```

## Cycle Detection

Approach depends on graph type:

* Undirected Graph — *DFS with parent tracking*, *Union-Find*
* Directed Graph — *Kahn's Algorithm*, *DFS with recursion stack*

### DFS on Undirected Graph

**Key Idea:** During DFS, if you encounter a visited vertex that is not the parent of the current vertex (back-edge), a cycle exists.

```python
def has_cycle_undirected(adj, n):
    visited = [False] * n

    def dfs(v, parent):
        visited[v] = True
        for neighbor in adj[v]:
            if not visited[neighbor]:
                if dfs(neighbor, v):
                    return True
            elif neighbor != parent:  # back-edge
                return True
        return False

    for i in range(n):
        if not visited[i]:
            if dfs(i, -1):
                return True
    return False
```

### Union-Find to Detect Cycles

* NOTE: Refer to [Union-Find](../dsu.md) for the full implementation.

```python
def has_cycle_union_find(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return True
    return False
```

### Kahn's Algorithm

* NOTE: Same algorithm with minor changes can produce a topological order.

```python
from collections import deque

def has_cycle_kahn(adj, n):
    indegree = [0] * n
    for u in range(n):
        for v in adj[u]:
            indegree[v] += 1

    q = deque(i for i in range(n) if indegree[i] == 0)
    count = 0

    while q:
        u = q.popleft()
        count += 1
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    return count != n  # cycle exists if not all vertices are processed
```

### DFS on Directed Graph

We need to track the path used to reach a node during DFS. Without a recursion stack (`rec_stack`), the algorithm cannot properly identify **back edges**, which are key indicators of cycles in a directed graph.

In a directed graph, a **back edge** points from a node to one of its ancestors in the current DFS path.

The `visited` array only tracks nodes explored at any point. If we encounter a visited node, it does **not** necessarily mean a cycle exists — it could have been visited from a different path. The recursion stack tracks nodes in the current call stack (the current path), allowing detection of back edges.

```
1 → 2 → 3 → 4
    ↘   ↗
      5
```

* Suppose DFS traverses 1 → 2 → 3 → 4 → 5, marking all nodes visited.
* When DFS branches again from node 2, it encounters node 3 which is marked visited.
* This does **not** imply a cycle unless node 3 is still in the current recursion stack.

```python
def has_cycle_directed(adj, n):
    visited = [False] * n
    rec_stack = [False] * n

    def dfs(v):
        visited[v] = True
        rec_stack[v] = True
        for neighbor in adj[v]:
            if not visited[neighbor]:
                if dfs(neighbor):
                    return True
            elif rec_stack[neighbor]:  # back edge found
                return True
        rec_stack[v] = False
        return False

    for i in range(n):
        if not visited[i]:
            if dfs(i):
                return True
    return False
```

### Bipartite (2-colorable) Graph Check

```python
from collections import deque

def is_bipartite(adj, n):
    color = [-1] * n

    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False

    return True
```

### K-Colorable Problem

* The general k-colorable problem is NP-hard.
* DFS/BFS backtracking can work for graphs up to ~25 nodes.
* If a problem can be expressed as a digital circuit or logic gates, it can be reduced to **SAT (Boolean satisfiability)**, which can often be transformed into a **graph k-coloring** problem.

## Problems on DFS/BFS

| **Problem**                                                                                      | **Concept**                     | **Approach**                                                                                                                                                                                                                          |
|--------------------------------------------------------------------------------------------------|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Number of Provinces](https://leetcode.com/problems/number-of-provinces/)                        | DFS on adjacency matrix         | Calculate connected components using a custom DFS implementation. Iterate through unvisited nodes, recursively traverse neighbors via adjacency matrix.                                                                              |
| [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/)                    | BFS for shortest path           | Use BFS starting from all rotten oranges simultaneously. Simulate the rotting process and track total and rotten orange counts to determine if any fresh oranges remain disconnected.                                               |
| [Flood Fill](https://leetcode.com/problems/flood-fill/)                                          | BFS / Flood Fill                | Perform BFS to change connected cells to the new color. Use the original color to track visited cells instead of a separate array.                                                                                                  |
| [Course Schedule](https://leetcode.com/problems/course-schedule/description/)                   | Topological Sort (Kahn's Algo)  | Use Kahn's Algorithm for topological sorting. Challenge: Solve using a DFS approach by detecting cycles in the graph.                                                                                                               |
| [01 Matrix](https://leetcode.com/problems/01-matrix/description/)                                | Modified BFS                    | Initialize BFS from all 0-value cells with a queue storing `(i, j, distance)`. Increment distances during BFS traversal.                                                                                                            |
| [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/description/)              | Boundary DFS/BFS                | Traverse the board boundary and mark connected `O` regions. Any unmarked `O` regions are captured.                                                                                                                                   |
| [Number of Enclaves](https://leetcode.com/problems/number-of-enclaves/description/)              | Boundary BFS/DFS                | Start BFS from boundary `1`s, marking reachable land cells. Count unmarked `1`s for enclosed regions.                                                                                                                              |
| [Word Ladder](https://leetcode.com/problems/word-ladder/)                                        | BFS with transformation         | Generate all possible transformations of each word in BFS. Use a set to check validity and track visited words.                                                                                                                     |
| [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/)                                  | BFS with path reconstruction    | Use BFS for shortest path. Use parent tracking for reconstructing paths. Avoid DFS as it explores all paths and may result in TLE.                                                                                                 |
| [Is Graph Bipartite](https://leetcode.com/problems/is-graph-bipartite/description/)              | BFS/DFS with color assignment   | Check bipartiteness using BFS/DFS. Assign colors alternately and ensure there are no conflicts. Handle disconnected components by applying the algorithm to all nodes.                                                              |

#### Number of Distinct Islands

This problem requires identifying the shapes of encountered islands. The approach is creating a **canonical hash** for the DFS traversal path on each island.

Problem: https://leetcode.com/problems/number-of-distinct-islands/

Given a 2D grid of 0s and 1s, an island is a group of 1s connected by 4-neighbors. Count the number of distinct islands. An island is considered the same as another if one can be **translated** (not rotated or reflected) to equal the other.

The key insight: serialize each island into a string by recording the DFS traversal directions (DRLU), then store unique strings in a set.

```python
def num_distinct_islands(grid):
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    islands = set()

    dirs = [(0, 1, 'R'), (1, 0, 'D'), (0, -1, 'L'), (-1, 0, 'U')]

    def dfs(r, c, path):
        visited[r][c] = True
        for dr, dc, d in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == 1:
                path.append(d)
                dfs(nr, nc, path)
        path.append('#')  # backtrack marker to distinguish shapes

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1 and not visited[i][j]:
                path = []
                dfs(i, j, path)
                islands.add(tuple(path))

    return len(islands)
```
