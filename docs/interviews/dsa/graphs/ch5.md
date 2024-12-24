## Minimum Spanning Trees

Given a connected, undirected, and weighted graph G, select a subset $E' \in G $ such that graph G is (still) connected and weight of selected edge E' is minimal !!

To satisfy connectivity criteria

- we need at least V-1 edges that form a tree and this tree must span all $V \in G$.

- MST can be solved with several well known algorithms
  - Prim's
  - Krushkal's

Application of MSTs

* Network Design : Minimize cost of laying cable networks
* Clustering and Machine Learning to remove expensive edges in tree
* TSP (Travelling Saleman Problem): used for approximation solution
* Pathfinding Algorithms in Games often use MST.

## Prim’s Algorithm

This algorithm takes a starting vertex and flags it as taken and enqueues a pair of information into a priority queue. The weight `w` and the other end point `u` of edge 0->u that is not taken yet.

These pairs are sorted in the priority queue based on increasing weight, and if tie, by increasing vertex number. Then Prim's algorithm greedily selects pair (w,u) in front of priority queue which has the minimum weight w - if the end point of this edge - which is u has not been taken before. ( to prevent cycle).

- O(process each edge once x cost of enqueue/dequeue) = $O(E \log E)$ = $O(E \log V)$

````c++
int primsMST(int V, vector<vector<Edge>>& adj) {
    vector<bool> visited(V, false);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    int mstWeight = 0;
    pq.push({0, 0});  // Start with node 0, weight 0
    while (!pq.empty()) {
        auto [w, u] = pq.top(); pq.pop();
        if (visited[u]) continue;
        visited[u] = true;
      	// take weight and process adjacent edges
        mstWeight += w;
        for (auto& [edge] : adj[u]) {
            if (!visited[edge.to]) {
                pq.push({edge.weight, edge.to});
            }
        }
    }
    return mstWeight;
}
````

## Krushkal’s Algorithm

This algorithm first sorts E edges based on non-decreasing weight. Then greedily try to add each edge into MST as long as such addition doesn't form a cycle. This check can be done using lightweight Union-Find Disjoint Sets implementation.

- Runtime O(sorting + trying to add each edge x Cost of Union-Find)
- $O(E \log E + E \times (\approx 1)) = O(E\log E) = O(E \log {V^2} = O(E\log V))$

````c++
bool compareEdges(const Edge& a, const Edge& b) {
    return a.weight < b.weight;
}

int kruskalMST(int V, vector<Edge>& edges) {
    sort(edges.begin(), edges.end(), compareEdges);
    DSU dsu(V);
    int mstWeight = 0;

    for (auto& edge : edges) {
        if (dsu.unite(edge.u, edge.v)) {
            mstWeight += edge.weight;
        }
    }

    return mstWeight;
}
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

## Problems

1. https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1 implement prim’s algorithm with negative weights to simulate min-heap.
2. https://www.geeksforgeeks.org/problems/disjoint-set-union-find/1 Recursive Find Implementation
3. https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1 Same Problem and use simplified UFs and unpack adjacency graph into edges, make sure to use undirected edges only once.
4. https://leetcode.com/problems/number-of-operations-to-make-network-connected/ Use Union-Find to find out the components in the graph, rest can be simple calculations around that.
5. https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/  This solution is complicated better to read discussion on the platform.
6. https://leetcode.com/problems/accounts-merge/description/ In this problem you basically have to track owners separately and try to build union set on strings (emails) and then print those back with owner.
7. https://leetcode.com/problems/number-of-islands-ii/ This problem makes u think of 2d array as flattened array list to simplify the UnionFind implementation, so there is a trade off :)
8. 
