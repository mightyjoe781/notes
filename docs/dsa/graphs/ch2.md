# Graph Traversal

## DFS

- traverses graph in 'depth-first' manner
- Time Complexity
    - $O(V+E)$ : Adjacency List
    - $O(V^2)$ : Adjacency Matrix

```c++
const UNVISITED = -1;
const VISITED = 1;

vector<int> dfs_num;				// initially all set to unvisited

void dfs(int u) {
  dfs_num[u] = VISITED;
  for(auto v:adj[u]) {
    if(dfs_num[v] == UNVISITED)
       dfs(v);
  } }
```

[GFG DFS Problem](https://www.geeksforgeeks.org/problems/depth-first-traversal-for-a-graph/1)

[Clone Graph](https://leetcode.com/problems/clone-graph/)

## BFS

- traverses graph in 'breadth-first' manner
- Time Complexity
    - $O(V+E)$ : Adjacency List
    - $O(V^2)$ : Adjacency Matrix

````c++
// inside int main() -- no recursion
  vi d(V,INF); d[s] = 0;					// distance from source s to s is 0
  queue<int> q; q.push(s);

  while(!q.empty()) {
    int u = q.front(); q.pop();
    for(auto v:adj[u]) {
      if(d[v] == INF) {
        d[v] = d[u] + 1;
        q.push(v);
 } } }
````

[GFG BFS Problem](https://www.geeksforgeeks.org/problems/bfs-traversal-of-graph/1)

## Connected Components

- Can be done using Union-Find and BFS also.

````c++
// inside int main()---this is the DFS solution
numCC = 0;
  dfs_num.assign(V, UNVISITED); // sets all vertices’ state to UNVISITED
  for (int i = 0; i < V; i++) // for each vertex i in [0..V-1]
  	if (dfs_num[i] == UNVISITED) // if vertex i is not visited yet
  	printf("CC %d:", ++numCC), dfs(i), printf("\n"); // 3 lines here!
````

https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/description/

## Flood Fill - Labeling/Coloring the Connected Components

This version actually counts the size of each component and colors it.

````c++
int dr[] = {1,1,0,-1,-1,-1, 0, 1}; // trick to explore an implicit 2D grid
int dc[] = {0,1,1, 1, 0,-1,-1,-1}; // S,SE,E,NE,N,NW,W,SW neighbors
int floodfill(int r, int c, char c1, char c2) { // returns the size of CC
  if (r < 0 || r >= R || c < 0 || c >= C) return 0; // outside grid
  if (grid[r][c] != c1) return 0; // does not have color c1
  int ans = 1; // adds 1 to ans because vertex (r, c) has c1 as its color
  grid[r][c] = c2; // now recolors vertex (r, c) to c2 to avoid cycling!
  for (int d = 0; d < 8; d++)
    ans += floodfill(r + dr[d], c + dc[d], c1, c2);
  return ans; // the code is neat due to dr[] and dc[]
}
````

NOTE: this direction traversal can be simple using `vector<vector<int>> dirs` to represent directions to traverse in.

## Cycle Detection
Approach should be based on Graph Type:

* Undirected Graph - *DFS with parent tracking*, *Union-Find*
* Directed Graph - Kahn’s Algorithm, *DFS with recursion Stack*

### DFS on Undirected Graph

**Key Idea**: During DFS, if you encounter a visited vertex that is not the parent of the current vertex (back-edge), a cycle exists.

````c++
bool dfs(int v, int parent, vector<vector<int>> &adj, vector<bool> &visited) {
    visited[v] = true;
    for (int neighbor : adj[v]) {
        if (!visited[neighbor]) {
            if (dfs(neighbor, v, adj, visited))
                return true;
        } else if (neighbor != parent) // back-edge
            return true; // Cycle detected
    }
    return false;
}

bool hasCycleUndirected(vector<vector<int>> &adj, int n) {
    vector<bool> visited(n, false);
    for (int i = 0; i < n; ++i)
        if (!visited[i])
            if (dfs(i, -1, adj, visited))
                return true;
    return false;
}
````

### UNION-FIND TO Detect CyCLES

* NOTE: This is a simplified implementation of Union-Find. Refer [Better Union-Find](ch5.md)

````c++
class UnionFind {
    
public:
    vector<int> p;
    UnionFind(int n) {
        p.resize(n);
        for(int i = 0; i < n; i++)
            p[i] = i;
    }
    int find(int x) {
        if(p[x] != x)
            return p[x] = find(p[x]);	// path compression
        return x;
    }
    bool unite(int x, int y) {
        int px = find(x);
        int py = find(y);
        if(px == py)
            return false;
        p[px] = py;
        return true;
    }
};

// inside main function
bool isCycle(int n, vector<vector<int>>& edges) {
    UnionFind uf(n);
    for(auto e: edges) {
        if(!uf.unite(e[0], e[1]))
            return true;
    }
    return false;
}
````



### Kahn’s Algorithm

* NOTE: Same algorithm with minor changes, can be used to give Topological Order.

````c++
bool hasCycleKahn(vector<vector<int>> &adj, int n) {
    vector<int> inDegree(n, 0);

    // Calculate in-degree
    for (int i = 0; i < n; ++i)
        for (int neighbor : adj[i])
            inDegree[neighbor]++;

  	// put zero-indegree nodes in on queue
    queue<int> q;
    for (int i = 0; i < n; ++i)
        if (inDegree[i] == 0)
            q.push(i);

    int count = 0; // Number of processed nodes
    while (!q.empty()) {
        int v = q.front(); q.pop();
        count++;

        for (int neighbor : adj[v]) {
            inDegree[neighbor]--;
            if (inDegree[neighbor] == 0)
                q.push(neighbor);
        }
    }
    return count != n; // Cycle exists if not all vertices are processed
}
````

### DFS on Directed Graph

We need to keep track of the path used to reach a node during DFS. Without a recursion stack (⁠`recStack`), the algorithm cannot properly identify **back edges**, which are key indicators of cycles in a directed graph.

In a directed graph, a **back edge** is an edge that points from a node to one of its ancestors in the current DFS path.

The ⁠visited array only keeps track of nodes that have been explored at any point. For example, if we run DFS starting from different nodes and come across a node that is already visited, it does **not** necessarily mean a cycle exists. The recursion stack (⁠recStack) keeps track of nodes currently in the call stack (the current path), allowing detection of back edges.

````txt
1 → 2 → 3 → 4
    ↘   ↗
      5
````

* Suppose DFS traverses straight from 1 → 2 → 3 → 4 → 5, marking all nodes visited.
* When DFS branches again from node 2, it encounters node 3 which is marked visited.
* This does **not** imply a cycle unless node 3 is still in the current recursion stack.
* Hence, tracking ⁠recStack is essential to detect cycles.

````c++
bool dfsDirected(int v, vector<vector<int>> &adj, vector<bool> &visited, vector<bool> &recStack) {
    visited[v] = true;
    recStack[v] = true;  // Mark current node in recursion stack

    for (int neighbor : adj[v]) {
        if (!visited[neighbor]) {
            if (dfsDirected(neighbor, adj, visited, recStack))
                return true;  // Cycle detected in DFS subtree
        } else if (recStack[neighbor]) {
            // Back edge found: neighbor is in current recursion stack
            return true;  // Cycle detected
        }
    }

    recStack[v] = false;  // Remove current node from recursion stack
    return false;         // No cycle detected from this node
}

bool hasCycleDirected(vector<vector<int>> &adj, int n) {
    vector<bool> visited(n, false);
    vector<bool> recStack(n, false);

    for (int i = 0; i < n; ++i) {
        if (!visited[i]) {
            if (dfsDirected(i, adj, visited, recStack))
                return true;  // Cycle found
        }
    }
    return false;  // No cycles in graph
}

````

### Bipartite(or 2/bi-colorable) Graph Check

````c++
bool isBipartite(vector<vector<pair<int, int>>>& adj, int s, int V) {
    queue<int> q;
    vector<int> color(V, -1); // -1 means unvisited
    color[s] = 0; // Start coloring the first node
    q.push(s);
		bool isBipartite = true;
  
    while (!q.empty() && isBipartite) {
        int u = q.front(); q.pop();
        for (auto& v : adj[u]) {
            int neighbor = v.first;
            if (color[neighbor] == -1) { // Unvisited node
                color[neighbor] = 1 - color[u]; // Alternate color
                q.push(neighbor);
            } else if (color[neighbor] == color[u]) {
                isBipartite = false; // Conflict found
                break;
            }
        }
    }
    return isBipartite; // Successfully colored
}
````

### K-Colorable Problem

* general k-Colorable problem is difficult to solve
* DFS/BFS ~ can work for 25 nodes at max
* If a problem can be expressed as a **digital circuit or logic gates**, it can be expressed in **Boolean algebra**, which can be reduced to **SAT (Boolean satisfiability)**, and from there, can often be transformed into a **graph k-coloring** problem (could be come complex).

## Problems on DFS/BFS

| **Problem**                                                                                      | **Concept**                     | **Approach**                                                                                                                                                                                                                          |
|--------------------------------------------------------------------------------------------------|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Number of Provinces](https://leetcode.com/problems/number-of-provinces/)                        | DFS on adjacency matrix         | Calculate connected components using a custom DFS implementation. Iterate through unvisited nodes, recursively traverse neighbors via adjacency matrix.                                                                              |
| [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/)                    | BFS for shortest path           | Use BFS starting from all rotten oranges simultaneously. Simulate the rotting process and track total and rotten orange counts to determine if any fresh oranges remain disconnected.                                               |
| [Flood Fill](https://leetcode.com/problems/flood-fill/)                                          | BFS / Flood Fill                | Perform BFS to change connected cells to the new color. Use the original color to track visited cells instead of a separate array.                                                                                                  |
| [Course Schedule](https://leetcode.com/problems/course-schedule/description/)                   | Topological Sort (Kahn’s Algo)  | Use Kahn's Algorithm for topological sorting. Challenge: Solve using a DFS approach by detecting cycles in the graph.                                                                                                               |
| [01 Matrix](https://leetcode.com/problems/01-matrix/description/)                                | Modified BFS                    | Initialize BFS from all 0-value cells with a queue storing `{i, j, distance}`. Increment distances during BFS traversal.                                                                                                            |
| [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/description/)              | Boundary DFS/BFS                | Traverse the board boundary and mark connected `O` regions. Any unmarked `O` regions are captured. Ensure comparisons are done on the board's characters.                                                                           |
| [Number of Enclaves](https://leetcode.com/problems/number-of-enclaves/description/)              | Boundary BFS/DFS                | Start BFS from boundary `1`s, marking reachable land cells. Count unmarked `1`s for enclosed regions.                                                                                                                              |
| [Word Ladder](https://leetcode.com/problems/word-ladder/)                                        | BFS with transformation         | Generate all possible transformations of each word in BFS. Use unordered maps to check validity and track visited words.                                                                                                           |
| [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/)                                  | BFS with path reconstruction    | Solve using BFS for shortest path. Use parent tracking for reconstructing paths. Avoid DFS as it explores all paths and may result in TLE.                                                                                         |
| [Is Graph Bipartite](https://leetcode.com/problems/is-graph-bipartite/description/)              | BFS/DFS with color assignment   | Check bipartiteness using BFS/DFS. Assign colors alternately and ensure there are no conflicts. Handle disconnected components by applying the algorithm to all nodes.                                                              |

#### Number of Distinct Islands

This problem requires identifying the shapes of the encountered island. The way to approach this problem is creating a **canonical hash** for the dfs we perform on each island.

Problem: https://leetcode.com/problems/number-of-distinct-islands/

Given a 2D array grid 0’s and 1’s island as a group of 1’s representing land connected by 4-neighbors.

Count number of distinct islands. An island is considered to be same  as another if and only if one island can be translated (and not  rotated/reflected) to equal the other.

Hmm make a island into a string xD and then store it in the map (kind of like serialization) , now for each island check before whether its  stored in map then its not distinct and don’t count it in result.

Now how to serialize : Create a traversal strings representing traversal DRLU representing the down,right,left,up!

````c++
  vector<vector<int>> dirs = {{0, 1, 'R'}, {1, 0, 'U'}, {-1, 0, 'L'}, {0, -1, 'D'}};
  void dfs(vector<vector<int>>& grid, int i, int j, vector<vector<bool>>& visited,string& island){
      visited[i][j] = true;

      for(auto dir: dirs){
          // neighbors
          int x = i + dir[0];
          int y = j + dir[1];

          if(x < 0 || y < 0 || x >= grid.size()||
          y >= grid[0].size()||visited[x][y] || grid[x][y] == 0)
              continue;

          island += dir[2];
          dfs(grid, x, y, visited, island);      
      }
      island+="#";
  }
  int numDistinctIslands(vector<vector<int>>& grid){
      int m = grid.size(), n = grid[0].size(), i, j;
      unordered_set<string> islands;
      vector<vector<bool>> visited(m,vector<bool>(n,false));

      for(i = 0; i< m; i++){
          for(j = 0; j < n; j++)
              if(grid[i][j] == 1 && !visited[i][j]){
                  string island_pattern = "";
                  dfs(grid, i, j, visited, island_pattern);
                  islands.insert(island_pattern);
              }
      }
      return (int) islands.size();
  }
````
