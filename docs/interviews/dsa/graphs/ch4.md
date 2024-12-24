## Shortest Path

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



## Problems

1. https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1 NOTICE few things, first there is no need to track visited since in undirected grpah it processes layer by layer, its a special case of floyd warshal which is special case PFS.
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

````c++
    int dfs(vector<vector<pair<int,int>>> &graph, vector<vector<int>> &vis, int i, int dst, int k) {
        if(i == dst){
            return 0;
        }
        if(k < 0) {
            return INT_MAX;
        }
        if(vis[i][k] != 0) {
            return vis[i][k];
        }

        int cost = INT_MAX;
        for(auto nbr: graph[i]) {
            int next = nbr.first;
            int weight = nbr.second;
            int subproblem = dfs(graph, vis, next, dst, k - 1);
            if (subproblem != INT_MAX) {
                cost = min(cost, weight + subproblem);
            }
        }
        return vis[i][k] = cost;

    }
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        // looks like a weighted graph with bfs
        // vector<vector<pair<int,int>>> graph(n);
        unordered_map<int, vector<pair<int,int>>> graph;


        // construct graph
        for(auto f : flights) {
            graph[f[0]].push_back({f[1],f[2]});
        }

        // ----------- bfs ----------
        queue<pair<int,int>> q;
        vector<int> dist(n+1, INT_MAX);
        dist[src] = 0;
        q.push({src,0});
        while(!q.empty() && k >= 0) {
            // travel all current level nodes - level order traversal
            int n = q.size();
            for(int i = 0; i < n; i++) {
                auto t = q.front(); q.pop();
                // do edge relaxation from all neighbors
                for(auto nbr: graph[t.first]) {
                    if(t.second + nbr.second < dist[nbr.first]) {
                        dist[nbr.first] = t.second + nbr.second;
                        q.push({nbr.first, dist[nbr.first]});
                    }
                }
            }
            k--;
        }
        return dist[dst] >= INT_MAX ? -1 : dist[dst];

        // ----------- dfs -----------
        // vector<vector<int>> vis(n, vector<int>(k + 2, 0)); // Initializing vis with -1
        // start from src and do bfs till k dist or destination
        // int result = dfs(graph, vis, src, dst, k);
        // return result == INT_MAX ? -1 : result;
        
    }
````

10. https://www.geeksforgeeks.org/problems/distance-from-the-source-bellman-ford-algorithm/1 Use bellman ford
11. https://www.geeksforgeeks.org/problems/distance-from-the-source-bellman-ford-algorithm/1 Use floyd warshal
12. https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/description/ Use floyd warshall and do post processing on resulting matrix as per conditions presented.