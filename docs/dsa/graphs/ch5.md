# Minimum Spanning Trees

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
int primsMST(int V, vector<vector<pair<int, int>>>& adj) {
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
        for (auto& [v, wt] : adj[u]) {
            if (!visited[v]) {
                pq.push({wt, v});
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

## Famous Variants of MST Applications

- ##### 'Maximum' Spanning Tree

The solution for this is very simple : Modify Kruskal's algorithm a bit, we no simply sort the edges based on non-increasing weight.

- ##### 'Minimum' Spanning Subgraph

In this variant, we do not start with a clean slate. Some edges in the given graph have already been fixed and must be taken as part of the solution. These default edges may form a non-tree in the first place. Our task is to continue selecting the remaining edges (if necessary) to make the graph connected in the least cost way. The resulting Spanning Subgraph may not be a tree and even if its a tree, it may not be the MST. That's why we put term 'Minimum' in quotes and use the term 'subgraph' rather than `tree`.

After taking into account all the fixed edges and their cost we can continue running Kruskal's algorithm on the remaining free edges until we have a spanning subgraph (or spanning tree).

- ##### Minimum 'Spanning Forest'

In this variant, we want to form a forest of K connected components (k subtrees) in the least cost way where K is given beforehand.

To get the minimum spanning forest is simple. Run Kruskal's algorithm as normal, but as soon as the number of connected components equals to the desired pre-determined number K, we can terminate the algorithm.

- ##### Second Best Spanning Tree

A solution for this variant is a modified Kruskal's: sort the edges in $O(E\log E) = O(E\log V)$ then find MST using Kruskal's in $O(E)$. Next for each edge in the MST, temporarily flag it so that it can't be chosen, then try to find MST again in $O(E)$ but now excluding that flagged edge. Note that we do not have to resort the edges at this point. The best spanning tree found after this process is the second best ST.

O(sort the edges once + find the original MST + find the second best ST) = $O(E\log V + E + VE) = O(EV)$

- ##### Minimax (and Maximin)

The minimax path problem is a problem of finding he minimum of maximum edge weight among all possible paths between two vertices i to j. The cost of a path from i to j is determined by maximum edge weight along this path. Among all these possible paths from i to j, pick the one with the minimum max-edge weight.

The problem can be modeled as MST problem. With a rationale that path with low individual edge weights even if the path is longer in terms of number of vertices/edges involved, then having the MST of given weighted graph is correct step. The MST is connected thus ensuring a path between any two vertices. The minimax path solution is thus the max edge weight along the unique path between vertex i and j in this MST.

The overall complexity is O(build MST + one traversal on the resulting tree.)  As E = V-1 in a tree, any traversal is just O(V).

Total Complexity : O(E log V + V) = O(E log V)

## Problems

1. https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1 implement prim’s algorithm with negative weights to simulate min-heap.
2. https://www.geeksforgeeks.org/problems/disjoint-set-union-find/1 Recursive Find Implementation
3. https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1 Same Problem and use simplified UFs and unpack adjacency graph into edges, make sure to use undirected edges only once.
4. https://leetcode.com/problems/number-of-operations-to-make-network-connected/ Use Union-Find to find out the components in the graph, rest can be simple calculations around that.
5. https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/  This solution is complicated better to read discussion on the platform.
6. https://leetcode.com/problems/accounts-merge/description/ In this problem you basically have to track owners separately and try to build union set on strings (emails) and then print those back with owner.
7. https://leetcode.com/problems/number-of-islands-ii/ This problem makes u think of 2d array as flattened array list to simplify the UnionFind implementation, so there is a trade off :)
8. https://leetcode.com/problems/swim-in-rising-water/ This time we will use MST to solve this problem.
