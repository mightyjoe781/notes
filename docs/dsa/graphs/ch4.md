# Shortest Path

**Definition:** *A **shortest path** between two vertices s and t in a network(weighted digraphs) is a directed simple path from s to t with property that no other such path has a lower weight*.

**Source-sink shortest path** Given a start vertex s and a finish vertex t, find a shortest path in graph from s to t. s-source vertex and t-sink vertex.

**Single-source shortest path** Given a start vertex s, find the shortest path from s to each other vertex in graph.

**All-pairs shortest path** Find the  shortest path connecting each pair of vertices in the graph, we  sometimes use the term *all shortest * to refer to this set of $V^2$ paths.

## Underlying Principle

We apply repeatedly two operations

*Edge relaxation* Test whether travelling along a given edges gives a new shortest path to its destination vertex.

*Path relaxation* Test whether traveling through a given vertex gives a new shortest path connecting two other given vertices.

````c++
if(wt [w] > wt[v] + e->wt()) {	
  wt[w] = wt[v] + e->wt(); // edge-relaxation
  spt[w] = e; // path-relaxation
}
````

**Property:** *If a vertex x is on a shortest  path from s to t, then that path consists of a shortest path from s to x followed by a shortest path from x to t.*

### Dijkstra’s Algorithm (SPSP)

**Property 2:** *Dijkstra’s algorithm solves the single-source shortest-paths* *problem in networks that have **nonnegative weights**.*

Dijkstra’s original implementation, which is suitable for dense  graphs, is precisely like Prim’s MST algorithm. Specifically we simple  change the assignment of priority P from `p=e->wt()` (edge wt) to `p=wt[v]+e->wt()` ( distance from the source to edge’s destination)

**Property 3** *With Dijkstra’s algorithm, we can find any SPT in a dense network in linear time.*

**Property 4** *For all networks and all priority functions, we can compute a spanning tree with PFS in time proportional to the time required for V insert , V delete the minimum , and E decrease key operations in a priority queue of size at most V.*

**Property 5** *With a PFS implementation of Dijkstra’s algorithm that uses  a heap for the priority-queue implementation, we can compute any SPT in time proportional to E lg V.*

````c++
int dijkstra(int V, vector<vector<int>>& edges, int src) {
    // Construct the graph as an adjacency list
    vector<vector<pair<int, int>>> graph(V + 1); // {weight, destination}
    vector<bool> vis(V + 1, false);
    vector<int> dis(V + 1, INT_MAX);
    //$ vector<int> p(int,-1);
    int processed = 0;

    for (const auto& e : edges) {
        graph[e[0]].push_back({e[2], e[1]}); // {weight, destination}
    }

    // Min-heap: stores {distance, vertex}
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;

    // Initialize source node
    pq.push({0, src});
    dis[src] = 0;

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if (vis[u])
            continue;

        vis[u] = true;
        processed++;

        // Relax neighbors
        for (const auto& [w, v] : graph[u]) {
            if (!vis[v] && d + w < dis[v]) {
                dis[v] = d + w;
                //$ p[v] = u;
                pq.push({dis[v], v});
            }
        }
    }

    // Return the maximum shortest distance or -1 if not all vertices are reachable
    return processed == V ? *max_element(dis.begin() + 1, dis.end()) : -1;
}
````

A variant of above algorithm can be used to print the path as well. Uncomment lines `//$`

````c++
vector<int> restore_path(int s, int d, vector<int>& p) {
    vector<int> path;
    for(int v = d; v!=s; v=p[v])
        path.push_back(v);
    path.push_back(s);
    // reverse the path do correct the ordering
    reverse(path.begin(),path.end());
    return path;
}
````

## Floyd-Warshall Algorithm (APSP)

````c++
void floydWarshall(int V, vector<vector<int>>& edges) {
    // Initialize distance matrix
    vector<vector<int>> dis(V, vector<int>(V, INT_MAX));

    // Set diagonal to 0 (distance to itself)
    for (int i = 0; i < V; i++) 
        dis[i][i] = 0;

    // Populate initial distances from edges
    for (const auto& e : edges) 
        dis[e[0]][e[1]] = e[2]; // edge from u to v with weight w

    // Floyd-Warshall algorithm
    for (int k = 0; k < V; k++) {         // Intermediate vertex
        for (int u = 0; u < V; u++) {     // Source vertex
            for (int v = 0; v < V; v++) { // Destination vertex
                if (dis[u][k] != INT_MAX && dis[k][v] != INT_MAX)
                    dis[u][v] = min(dis[u][v], dis[u][k] + dis[k][v]);
            }
        }
    }
}
````

## Bellman Ford Algorithm

- Used to find the shortest path from a source node to all other nodes in a **graph**, even if there are negative edge weights.

* **Key Features**:
    * Works for both **directed** and **undirected** graphs.
    * Handles **negative edge weights**, unlike Dijkstra’s algorithm.
    * Can also detect **negative weight cycles** in the graph.
    * Time Complexity: $O(V \times E)$, where V is the number of vertices and E is the number of edges.

````c++
vector<int> bellmanFord(int V, int E, vector<Edge>& edges, int source) {
    // Initialize distances from the source
    vector<int> dist(V, INT_MAX);
    dist[source] = 0;

    // Relax edges V-1 times
    for (int i = 1; i < V; ++i) {
        for (const auto& edge : edges) {
            int u = edge.u;
            int v = edge.v;
            int w = edge.weight;

            // If the distance to the destination vertex is greater
            // through the current edge, update the distance
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }

    // Check for negative weight cycles
    for (const auto& edge : edges) {
        int u = edge.u;
        int v = edge.v;
        int w = edge.weight;

        // If the distance can still be minimized, it means there's a negative cycle
        if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
            cout << "Graph contains negative weight cycle!" << endl;
            return {};  // Return an empty vector to indicate a negative cycle
        }
    }

    return dist;  // Return the shortest distances from the source
}
````

### Other Applications

#### Solving SSSP Problem on Small Weighted Graph

If we have the APSP information we also know the SSSP information.

Printing Shortest Path

A common issue encountered by programmers who use four-liner Floyd Warshall’s without understanding how it works is when they are asked to print shortest paths too. In BFS/Dijkstra’s/ Bellman Ford’s algorithm we just need to remember the shortest paths spanning tree by using a 1D vector to store parent information for each vertex. In Floyd Warshall’s we need to store a 2D parent matrix. The modified code is as

````c++
for(int i = 0; i < V; i++)
  for(int j = 0; j < V; j++)
    p[i][j] = i; // initialize the parent matrix
for(int k = 0; k < V; k++)
  for(int i = 0; i < V; i++)
    for(int j = 0; j < V; j++)
      if(adj[i][k] + adj[k][j] < adj[i][j) {
        adj[i][j] = adj[i][k] + adj[k][j];
        p[i][j] = p[k][j];
      }
//------------------------------------------------------
void printPath(int i, int j) {
  if(i!=j) printPath(i,p[i][j]);
  printf(" %d", j);
}
````

#### Transitive Closure (Warshall’s Algorithm)

Given a graph, determine if vertex i is connected to j, directly or indirectly. This variant uses bitwise operators which are much faster than arithmatic operators.

Initially set entire adj to 1 if i connected to j otherwise 0.

After running Floyd’s Algorithm we can check if any two vertices are connected by check adj matrix

````c++
for(int k = 0; k < V; k++)
  for(int i = 0; i < V; i++)
    for(int j = 0; j < V; j++)
      adj[i][j] != (adj[i][k] & adj[k][j]);
````

#### Minimax and Maximin

We have seen the minimax(and maximin) path problem earlier. The solution using Floyd Warshall’s is shown below. First intialize `adj[i][j]` to be the weight of edge (i,j). This is default minimax cost for two vertices that are directly connected. For pair i-j without any direct edge, set `adj[i][j] = INF`. Then we try all possible intermediate vertex k. The minimax cost `adj[i][j]` is minimum of either (itself) or (the maximum between `adj[i][k]] or adj[k][j]`) However this approach works only for  V $\le$ 400.

````c++
for (int k = 0; k < V; k++)
	for(int i = 0; i < V; i++)
		for(int j = 0; j < V; j++)
			adj[i][j] = min(adj[i][j], max(adj[i][k],adj[k][j]))
````

#### Finding the Cheapest/Negative Cycle

We know Bellman Ford will terminate after O(VE) steps regardless of the type of input graph, same is the case with Floyd Warshall it terminates in $O(V^3)$.

To solve this problem, we intially set the main diagonal of the adj matrix to a very large value, i.e. `adj[i][i] = INF`, which now mean shortest cyclic paht weight strating from vertex i goes thru up to V-1 other intermediate vertices and return back to i. If `adj[i][i]` is no longer INF for any $i \in [0…V-1]$, then we have a cycle. The smallest non-negative `adj[i][j]` $\forall i \in [0…V-1]$ is the cheapest cycle.

If `adj[i][j]` < 0 for any $i \in [0…V-1]$, then we have a negative cycle because if we take this cyclic path one more time, we will get even shorter `shortest` path.

#### Finding the Diameter of a Graph

The diameter is maximum shortest path distance between any pair, just find the i and j s.t. its maximum of the matrix adj.

#### Finding the SCCs of a Directed Graph

Tarjan’s algorithm can be used to identify SCCs of a digraph. However code is bit long. If input graph is small, we can also identify the SCCs of graph in $O(V^3)$ using Warshall’s transitive closure algorithm and then use the following check.

 To find all the members of SCC that contains vertex i check all other vertices $V\in [0…V-1]$. If `adj[i][j] && adj[j][i]` is true, then vertex i and j belong to same SCC.

## Summary

| Algorithm      | Graph Type          | Complexity            | Special Features                         |
| -------------- | ------------------- | --------------------- | ---------------------------------------- |
| BFS            | Unweighted          | \(O(V + E)\)          | Layer-by-layer exploration               |
| Dijkstra       | Weighted (Non-Neg.) | \(O((V + E) \log V)\) | Priority queue-based; greedy approach    |
| Bellman-Ford   | Weighted (Neg.)     | \(O(V \times E)\)     | Handles negative weights; detects cycles |
| Floyd-Warshall | Small Graphs/APSP   | \(O(V^3)\)            | Solves all-pairs shortest paths          |

## Problems

1. https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1 NOTICE few things, first there is no need to track visited since in undirected graph it processes layer by layer, its a special case of floyd warshal which is special case PFS.
2. https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph/1 NOTICE NOW we need visited array to for safeguard and efficiency. Try removing it and see memory comparisons.
3. https://www.geeksforgeeks.org/problems/implementing-dijkstra-set-1-adjacency-matrix/1 for fun try to use set for this approach to implement dijkstras

| **Aspect**               | **Priority Queue**                              | **Set**                                                                 |
|--------------------------|-------------------------------------------------|-------------------------------------------------------------------------|
| **Insertion Time**        | \( $O(\log N)$ \)                               | \( $O(\log N)$ \)                                                      |
| **Update Time**           | Not supported directly; push new value instead | \( $O(\log N)$ \): Remove old value, insert new value                  |
| **Deletion Time**         | \( $O(\log N)$ \)                             | \( $O(\log N)$ \)                                                      |
| **Ease of Implementation**| Simple (standard libraries like `priority_queue`)| More complex, as updates require additional operations                 |
| **Duplicates**            | Allows duplicates                               | Does not allow duplicates                                              |
| **Space Usage**           | May grow larger due to duplicate entries        | Minimal, as it keeps only one instance of each node                    |
| **Efficiency in Practice**| Generally faster due to less overhead           | Slightly slower for the same operations due to extra bookkeeping       |

4. https://leetcode.com/problems/shortest-path-in-binary-matrix/ Now it maybe tempting to store all distances but the quesiton only ask for a specific target, so try to optimize space without using matrix to store all distances.
5. https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/ The best solution would be to keep track of number of ways in an array ways and increment each time your traverse priority queue.

6. https://leetcode.com/problems/path-with-minimum-effort/description/ This problem requires to drive dijkstra in the direction where the abs difference encountered so far is minimum, so our priority function changes here.

7. https://leetcode.com/problems/network-delay-time/description/ This is straightforward question find all distances and then find the longest distance from the dist array.

8. https://www.geeksforgeeks.org/problems/minimum-multiplications-to-reach-end/1 This problem does have any graph structure and we don’t actually need to create the graph, its an application of PFS (doesn’t really matter as PFS function is not obvious). Think of it as a graph with 1e5 nodes and you are traversing using multiplication rules.

9. https://leetcode.com/problems/cheapest-flights-within-k-stops/ Cheapest flight with K stops, this is important question look at DFS solution presented as well.

Even though this problem looks like a Dijkstra problem it is not, but Dijkstra traverses the optimal path, while problem doesn't care about the minimum cost, it just needs to be within k stops.

Dijkstra might fail here since optimal path doesn't may be have less than k stops.

````python

from collections import defaultdict
def findCheapestPrice(n, flights, src, dst, k):

    graph = defaultdict(list)

    for u, v, w in flights:
        graph[u].append((v, w))

    @cache
    def dfs(i, k):
        if i == dst:
            return 0

        if k < 0:
            return float('inf')

        cost = float('inf')
        for v, w in graph[i]:
            cost = min(cost, w + dfs(v, k-1))
        return cost
       
    res = dfs(src, k)
    return -1 if res == float('inf') else res

````

10. https://www.geeksforgeeks.org/problems/distance-from-the-source-bellman-ford-algorithm/1 Use bellman ford
11. https://www.geeksforgeeks.org/problems/distance-from-the-source-bellman-ford-algorithm/1 Use floyd warshal
12. https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/description/ Use floyd warshall and do post processing on resulting matrix as per conditions presented.
13. https://leetcode.com/problems/swim-in-rising-water/ Use dijkstra to solve and select a path which does not have max element present in it.