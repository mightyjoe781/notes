# Graph Properties and Types

Major Application of Graph includes *Maps, Hypertext, Circuits, Schedules, Transactions, Matching, Networks, Program Structure(Compiler).*

## Glossary

***Definition** :* A **graph** is a set of **vertices** and a set of **edges** that connect pairs of distinct vertices ( with at most one edge connecting any pair of vertices ).

$V$: # of vertices/nodes, $E$: number of edges/links

Above definition puts two restrictions on graphs

1. Disallow duplicate edges (*Parallel edges, and a graph that contains them multigraph*)
2. Disallows edges that connect to itself (*Self-Loops*)

***Property 1:*** *A graph with $V$ vertices has at most $V(V-1)/2$ edges.*

When there is an edge connecting two vertices, we say that the vertices are *adjacent* to one another and the edge is *incident* on them.

Degree of Vertex: Number of edges incident on it. $v-w$ represents edge from $v$ to $w$ and $w-v$ represents edge from $w$ to $v$.

A *subgraph* is a subset of a graph's edges (and associated vertices) that constitutes a graph.

**Same graph represented 3-ways**

![Graph represented three ways](./assets/graph-three-representations.png)

A graph is defined by its vertices and its edges, not the way that we choose to draw it.

A *planar graph* is one that can be drawn in the plane without any edges crossing. For some graphs, the drawing can carry information — vertices correspond to points on a plane and edges represent distances. These are called *Euclidean graphs.*

Two graphs are *isomorphic* if we can change the vertex labels on one to make its set of edges identical to the other. (Difficult computation problem since there are $V!$ possibilities).

**Definition 2:** *A **path** in a graph is a sequence of vertices in which each successive vertex (after the first) is adjacent to its predecessor in the path.* In a **simple path**, the vertices and edges are distinct. A *cycle* is a path that is simple except that the first and final vertices are the same.

Sometimes we refer to *cyclic paths* to describe a path whose first and last vertices are the same; and we use the term *tour* to refer to a cyclic path that includes every vertex.

Two simple paths are *disjoint* if they have no vertices in common other than, possibly, their endpoints.

![Paths and cycles](./assets/paths-and-cycles.png)

**Definition 3:** A graph is a ***connected graph*** if there is a path from every vertex to every other vertex in the graph. A graph that is not connected consists of a set of ***connected components***, which are maximal connected subgraphs.

**Definition 4:** An acyclic connected graph is called a **tree**. A set of trees is called a **forest**. A **spanning tree** of a connected graph is a subgraph that contains all of that graph's vertices and is a single tree.

A **spanning forest** of a graph is a subgraph that contains all of that graph's vertices and is a forest.

A graph $G$ with $V$ vertices is a tree if and only if it satisfies any of the following four conditions.

- $G$ has $V-1$ edges and no cycles.
- $G$ has $V-1$ edges and is connected
- Exactly one simple path connects each pair of vertices in $G$
- $G$ is connected, but removing any edge disconnects it

Graphs with all edges present are called *complete graphs.*

*Complement of a graph $G$ has the same set of vertices as the complete graph but with the edges of $G$ removed*.

Total number of graphs with $V$ vertices is $2^{V(V-1)/2}$. A complete subgraph is called a *clique*.

*Density* of a graph is the average vertex degree, or $\frac{2E}{V}$. A *dense graph* is one whose density is proportional to $V$. A *sparse graph* is one whose complement is dense.

A graph is dense if $E \propto V^2$ and sparse otherwise. Density of graphs helps us choose an efficient algorithm for processing the graph.

When analyzing graph algorithms, we assume $\frac{V}{E}$ is bounded above by a small constant, so we can abbreviate expressions such as $V(V+E)\approx VE$.

A *bipartite graph* is a graph whose vertices we can divide into two sets such that all edges connect a vertex in one set with a vertex in the other set. It is quite useful in matching problems. Any subgraph of a bipartite graph is bipartite.

![Bipartite graph](./assets/bipartite-graph.png)

Graphs defined above are all *undirected graphs*. In *directed graphs*, also known as *digraphs*, edges are one-way. Pairs of vertices are in the form of ordered pairs.

The first vertex in a digraph edge is called the *source* and the final vertex is called the *destination*.

We speak of *indegree and outdegree* of a vertex (the number of edges where it is destination and source respectively).

A *directed cycle* in a digraph is a cycle in which all adjacent vertex pairs appear in the order indicated by the directed graph edges.

A *directed acyclic graph (DAG)* is a digraph that has no directed cycles.

In *weighted graphs*, we associate numbers (weights) with each edge, denoting cost or distance.

## Graph Representation

### Edge List

An **edge-list representation** of a graph is a way of representing the edges of a graph as a list of pairs (or tuples) of vertices. Each pair corresponds to an edge in the graph, indicating a connection between two vertices.

* For a **directed graph**, each pair (u, v) in the list represents a directed edge from vertex u to vertex v.

* For an **undirected graph**, each pair (u, v) in the list represents an undirected edge between vertices u and v. (Note: Duplicate or reverse entries, such as (u, v) and (v, u), are often avoided since they represent the same edge.)

This representation is well-suited for **sparse graphs** where the number of edges is much smaller compared to the number of possible edges.

### Adjacency Matrix

An *adjacency-matrix* representation of a graph is a matrix of Boolean values, with the entry in row $u$ and column $v$ set to 1 if there is an edge connecting vertex $u$ to vertex $v$, and 0 otherwise.

This representation is well suited for dense graphs.

NOTE: This matrix is symmetric for undirected graphs.

![Adjacency matrix](./assets/adjacency-matrix.png)

```python
def build_adj_matrix(edges, n):
    adj = [[0] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = 1
        adj[v][u] = 1  # remove for directed graph
    return adj
```

### Adjacency List

Preferred when graphs are not dense. We keep track of all vertices connected to each vertex in a list associated with that vertex.

Primary advantage is space efficiency. The disadvantage is that checking whether a specific edge exists takes $O(\deg(v))$ time.

```python
def build_adj_list(edges, n):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # remove for directed graph
    return adj
```

Cost Comparison of these representations

![Representation cost comparison](./assets/representation-cost-comparison.png)

## Simple, Euler and Hamilton Paths

**Simple Path:** Given two vertices, is there a simple path in the graph that connects them?

* Property: We can find a path connecting two given vertices in a graph in linear time.

**Hamilton Path:** Given two vertices, is there a simple path connecting them that visits every vertex in the graph exactly once? If the path is from a vertex back to itself, this problem is known as the Hamilton Tour.

* Property: *A recursive search for a Hamilton tour could take exponential time.*

**Euler Path:** Is there a path connecting two given vertices that uses each edge in the graph exactly once? The path need not be simple — vertices may be visited multiple times. If the path is from a vertex back to itself, we have an Euler tour problem.

* *Property:* A graph has an Euler tour if and only if it is connected and all its vertices are of even degree.
* *Corollary:* A graph has an Euler path if and only if it is connected and exactly two of its vertices are of odd degree.
* Property: We can find an Euler tour in a graph, if one exists, in linear time.
