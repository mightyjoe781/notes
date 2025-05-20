# DP on Trees

Used when input is a **tree (acyclic connected graph)** and we need to calculate DP states at each node, often in a **bottom-up (post-order)** or **top-down (rerooting)** fashion.

## Post-order DFS (Bottom Up Tree DP)

We process children first, then compute the parent’s result using children’s DP.

````c++
vector<int> adj[N];
int dp[N];

void dfs(int node, int parent) {
    for (int child : adj[node]) {
        if (child == parent) continue;
        dfs(child, node);
        dp[node] += dp[child];  // Combine child results
    }
    dp[node] += value[node];  // Include current node’s own value
}
````

## Common Patterns

### Subtree Size

````c++
int size[N];

void dfs(int u, int p) {
    size[u] = 1;
    for (int v : adj[u]) {
        if (v == p) continue;
        dfs(v, u);
        size[u] += size[v];
    }
}
````

### Longest Path (Diameter of Tree)

````c++
int diameter = 0;

int dfs(int u, int p) {
    int max1 = 0, max2 = 0;
    for (int v : adj[u]) {
        if (v == p) continue;
        int d = dfs(v, u);
        if (d > max1) {
            max2 = max1;
            max1 = d;
        } else if (d > max2) {
            max2 = d;
        }
    }
    diameter = max(diameter, max1 + max2);
    return max1 + 1;
}
````

## Tree Rerooting (Top-Down Tree DP)

We compute `dp[root]`, then update `dp[child]` by “rerooting” at each child using the parent’s value.

````c++
void dfs1(int u, int p) {
    for (int v : adj[u]) {
        if (v == p) continue;
        dfs1(v, u);
        dp[u] += dp[v] + size[v];
    }
}

void dfs2(int u, int p) {
    for (int v : adj[u]) {
        if (v == p) continue;
        dp[v] = dp[u] - size[v] + (total_nodes - size[v]);
        dfs2(v, u);
    }
}
````

### Problems

**Easy to Medium**

- [**337. House Robber III**](https://leetcode.com/problems/house-robber-iii/) - Classic DP on binary tree. Decide to rob or not rob each node.*(2 states per node: include or exclude)*
- [**110. Balanced Binary Tree**](https://leetcode.com/problems/balanced-binary-tree/) - Simple bottom-up recursion to calculate subtree height.
- [**104. Maximum Depth of Binary Tree**](https://leetcode.com/problems/maximum-depth-of-binary-tree/) - Base DFS post-order depth calculation.
- [**124. Binary Tree Maximum Path Sum**](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Compute the max path sum going through each node using child contributions.

**Medium to Hard**

- [**979. Distribute Coins in Binary Tree**](https://leetcode.com/problems/distribute-coins-in-binary-tree/) - Pass extra coins up/down tree using post-order traversal.
- [**834. Sum of Distances in Tree**](https://leetcode.com/problems/sum-of-distances-in-tree/) - Tree rerooting technique (top-down DP after bottom-up DP).
- [**968. Binary Tree Cameras**](https://leetcode.com/problems/binary-tree-cameras/) - 3-state DP: covered with camera, covered without camera, not covered.
- [**543. Diameter of Binary Tree**](https://leetcode.com/problems/diameter-of-binary-tree/) -  Standard diameter logic using two max child depths.
