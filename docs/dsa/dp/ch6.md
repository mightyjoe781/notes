# DP on Trees

Used when input is a **tree (acyclic connected graph)** and we need to calculate DP states at each node, often in a **bottom-up (post-order)** or **top-down (rerooting)** fashion.

We assume :

 Post-order DFS (Bottom Up Tree DP)

We process children first, then compute the parent’s result using children’s DP.

````python
def dfs(u, parent):
    for v in adj[u]:
        if v == parent: # don't go to back edge
            continue
        dfs(v, u)
        dp[u] += dp[v]          # combine child results
    dp[u] += value[u]           # include current node
````

## Common Patterns

### Subtree Size

````python
def dfs(u, parent):
    size[u] = 1
    for v in adj[u]:
        if v == parent:
            continue
        dfs(v, u)
        size[u] += size[v]
````

### Longest Path (Diameter of Tree)

````python
diameter = 0

def dfs(u, parent):
    global diameter
    max1 = max2 = 0

    for v in adj[u]:
        if v == parent:
            continue
        d = dfs(v, u)

        if d > max1:
            max2 = max1
            max1 = d
        elif d > max2:
            max2 = d

    diameter = max(diameter, max1 + max2)
    return max1 + 1
````

## Tree Rerooting (Top-Down Tree DP)

Used when DP value is needed for every node as root.

We compute `dp[root]`, then update `dp[child]` by “rerooting” at each child using the parent’s value.

````python

def solve():
    N = len(adj)
    size = [0] * N
    dp = [0] * N
    
    # dp[u] = sum of distances from u to all nodes in its subtree
    def dfs1(u, parent):
        size[u] = 1
        for v in adj[u]:
            if v == parent:
                continue
            dfs1(v, u)
            size[u] += size[v]
            dp[u] += dp[v] + size[v]
    # Reroot DP to children
    def dfs2(u, parent):
        for v in adj[u]:
            if v == parent:
                continue
            dp[v] = dp[u] - size[v] + (N - size[v])
            dfs2(v, u)

    dfs1(0, -1)
    dfs2(0, -1)

    return dp
````

## Problems



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
