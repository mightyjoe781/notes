# DP on Trees

Used when input is a **tree (acyclic connected graph)** and we need to calculate DP states at each node, often in a **bottom-up (post-order)** or **top-down (rerooting)** fashion.

Usually we do Post Order Traversal because of the we often aggregate solution from subtree states and then return the answer based on decision from calculation of the subtree.

## Tree Rerooting (Top-Down Tree DP)

**Tree Rerooting** refers to the process of changing the root of a tree data structure to a different node, while maintaining the original structure's connectivity and hierarchy.

Think of it like taking a node and pull it towards top, while not changing the hierarchy and structure of the graph.

![](assets/Pasted%20image%2020260202073749.png)

Let's try to solve a problem

### Sum of Distances in Tree

There is an undirected connected tree with `n` nodes labeled from `0` to `n - 1` and `n - 1` edges.

You are given the integer `n` and the array `edges` where `edges[i] = [ai, bi]` indicates that there is an edge between nodes `ai` and `bi` in the tree.

Return an array `answer` of length `n` where `answer[i]` is the sum of the distances between the `ith` node in the tree and all other nodes.

*Discussion*

From the looks of this problem, A naive strategy is to start at every and explore the graph, discovering distances and summing up all of them for that node, and that would `ans[i]`.

But this is not graph !!, Maybe I can traverse the transform this into a graph.
But that would still be a $O(n^2)$ solution.

Exploring graph for Each Node is a Brute Force Approach, Can we do better rather than brute forcing out way for answer.

*Intuition for DP*

![](assets/Pasted%20image%2020260202075517.png)

If we traverse the tree here from `root 0`, we will have `dist[0]` which would be distance from `root` to all nodes in structure,

Could we reuse that information to solve distance for other nodes without completely traversing graph for each node ?

$$
\begin{align}
ans[1] = f(ans[0]) \\
ans[2] = f(ans[0])
\end{align}
$$

![](assets/Pasted%20image%2020260202080122.png)

Now while solving for node 2, we notice that all of its children (node3, node4, node5) are now 1 step closer to it when tree is rerooted at 2, and its parent's other children (node 1) is 1 step farther to it.

We can generalize following

```
ans[i] = ans[root] - numSubnodes[i] (closer) + remainingNodes (farther)
```


![](assets/Pasted%20image%2020260202080653.png)\

Solution to above problem,

````python

def sumOfDistancesInTree(n: int, edges: List[List[int]]) -> List[int]:
    
    adj = defaultdict(list)

    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    size, dp = [0]*n, [0]*n

    # first round of DFS solves for node 0
    # dp[u] = sum of distances from u all nodes in subtree
    def dfs1(u, parent):
        size[u] = 1
        for v in adj[u]:
            if v == parent: # back edge
                continue
            dfs1(v, u)
            size[u] += size[v]
            dp[u] += dp[v] + size[v]

    # reroot DP to children
    def dfs2(u, parent):
        for v in adj[u]:
            if v == parent:
                continue
            dp[v] = dp[u] - size[v] + (n - size[v])
            dfs2(v, u)
    
    dfs1(0, -1)
    dfs2(0, -1)

    return dp
        
````

Summary :

Used when DP value is needed for every node as root.

We compute `dp[root]`, then update `dp[child]` by “rerooting” at each child using the parent’s value.

### Post-order DFS (Bottom Up Tree DP)

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

## Simple Problems

Following Tree problems are simpler, but builds intuition around managing states during traversals.

### Maximum Depth of Binary Tree

[**104. Maximum Depth of Binary Tree**](https://leetcode.com/problems/maximum-depth-of-binary-tree/) - Base DFS post-order depth calculation.

```python

def maxDepth(root: Optional[TreeNode]) -> int:

    def dfs(node):
        if not node:
            return 0
        
        return 1 + max(
            dfs(node.left),
            dfs(node.right)
        )
    
    return dfs(root)

```

### Balanced Binary Tree

[**110. Balanced Binary Tree**](https://leetcode.com/problems/balanced-binary-tree/) - Simple bottom-up recursion to calculate subtree height.

Check at every node level during traversal for the subtree heights.

```python

def isBalanced(root: Optional[TreeNode]) -> bool:

    ans = True

    def dfs(node):
        nonlocal ans
        if not node:
            return 0

        l = dfs(node.left)
        r = dfs(node.right)

        if abs(l - r) > 1: # every node compare this height
            ans = False
        
        return 1 + max(l, r)

    dfs(root)
    return ans

```

Time : $O(n)$ : (each node visited once)
Space : $O(h)$ : recursion stack (`h = tree height`)

A more faster version which exits early for above solution, stop at unbalanced condition returning a sentinel (`-1`)

```python
def isBalanced(root):
    def dfs(node):
        if not node:
            return 0

        left = dfs(node.left)
        if left == -1:
            return -1

        right = dfs(node.right)
        if right == -1:
            return -1

        if abs(left - right) > 1:
            return -1

        return 1 + max(left, right)

    return dfs(root) != -1
```

### House Robber III

[**337. House Robber III**](https://leetcode.com/problems/house-robber-iii/) - Classic DP on binary tree. Decide to rob or not rob each node.*(2 states per node: include or exclude)*

- Houses form a Binary Tree
- If you rob a house you cannot rob its direct children
- You want to maximize the total money

There is no linear order here, so we cannot use simple suffix/prefix pattern from *array*

At each node we can take two decisions

- Rob this node ~ you cannot rob direct children of current nodes
- Don't Rob this node ~ freely explore children

A naive BruteForce Approach

```python

def rob(node, parent_robbed):
    if not node:
        return 0

    if parent_robbed:
        return rob(node.left, False) + rob(node.right, False)
    else:
        return max(
            node.val + rob(node.left, True) + rob(node.right, True),
            rob(node.left, False) + rob(node.right, False)
        )

```

So optimal answer at a node depends on two states.

State Transition

```
# two states

rob = node.val + left_not + right_not
not_rob = max(left_rob, left_not) + max(right_rob, right_not)

```


```python
def rob(root):
    
    def dfs(node):
        if not node:
            return (0, 0) # (rob, not_rob)
        
        left_rob, left_not = dfs(node.left)
        right_rob, right_not = dfs(node.right)
        
        rob = node.val + left_not + right_not
        not_rob = max(left_rob, left_not) + max(right_rob, right_not)
        
        return (rob, not_rob)
    
    return max(dfs(root))

```


A question might arise why we not memoizing anything here ? `@cache`

In a tree

- every node has exactly one parent
- `dfs(node)` is called once

There is no recomputation.

You might need DP when

- Graph (not Tree) : Nodes may be revisited via multiple paths
- DP state has extra parameters
- Rerooting with multiple queries

### Binary Tree Maximum Path Sum

[**124. Binary Tree Maximum Path Sum**](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Compute the max path sum going through each node using child contributions.

A path can start and end at any node, It must go *downwards* along *parent-child* links. Doesn't need to pass through the root.

Cannot Branch upwards twice (no cycles)

So at any node, a path can come from *left child*, *right child*, or *stop at the node itself*

```python

def maxPathSum(root):
    ans = float('-inf')

    def dfs(node):
        nonlocal ans
        if not node:
            return 0

        # clamps the result with 0, to avoid negative contributions
        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)

        # path that ends at this node (can fork)
        ans = max(ans, node.val + left + right)

        # path that can be extended to parent (no fork)
        return node.val + max(left, right)

    dfs(root)
    return ans

```


## Difficult Problems
### Distribute Coins in Binary Tree

[**979. Distribute Coins in Binary Tree**](https://leetcode.com/problems/distribute-coins-in-binary-tree/) - Pass extra coins up/down tree using post-order traversal.

You are given the `root` of a binary tree with `n` nodes where each `node` in the tree has `node.val` coins. There are `n` coins in total throughout the whole tree.

In one move, we may choose two adjacent nodes and move one coin from one node to another. A move may be from parent to child, or from child to parent.

Return _the **minimum** number of moves required to make every node have **exactly** one coin_.

This is a textbook Tree DP with post-order traversal, and key is to model it as *flow of coins on a tree*

Key Insight : At each node, after fixing its children, The only thing that matters is how many coins this subtree has in *excess* or in *deficit*

We only care about how many coins must cross each edge.

```
balance(node) = (coins in subtree rooted at node) - (number of nodes in that subtree)
```

- `balance > 0` ~ Extra coins to send up
- `balance < 0` ~ coins needed from parent
- `balance = 0` ~ subtree is perfectly balanced

```python

def distributeCoins(root):
    moves = 0

    def dfs(node):
        nonlocal moves
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        # count moves across edges
        moves += abs(left) + abs(right)

        # return balance to parent
        return node.val + left + right - 1

    dfs(root)
    return moves

```

Why this is tree DP

- You compute a DP value from children
- That value summarizes the subtree
- parent only needs that summary

This is example of difference between a *local flow DP* and *rerooting DP*

We don't reroot the tree because answer is a global sum of edges flows, not a per root value. Coins flow along edges regardless of where the root is.

### Sum of Distances in Tree

 [**834. Sum of Distances in Tree**](https://leetcode.com/problems/sum-of-distances-in-tree/) - Tree rerooting technique (top-down DP after bottom-up DP).

Already *discussed*. in the introductory section

### Binary Tree Cameras

- [**968. Binary Tree Cameras**](https://leetcode.com/problems/binary-tree-cameras/) - 3-state DP: covered with camera, covered without camera, not covered.

You are given the `root` of a binary tree. We install cameras on the tree nodes where each camera at a node can monitor its parent, itself, and its immediate children.

Return _the minimum number of cameras needed to monitor all nodes of the tree_.

Problem asks for *one global minimum* number of cameras to cover the entire tree. It doesn't ask for

- best answer if rooted at each node
- best answer when treating different nodes as root

So we don't need rerooting.

Another thought could be to try greedy strategy like

- Put cameras on parents of leaves
- Put cameras on nodes with many children

But local greedy choices can conflict globally.

Key Insight :

- At every node we care about three possible states
    - This node has a camera
    - This node is covered but has no camera
    - This node is not covered

```
dp[u][0] = min cameras if u HAS a camera
dp[u][1] = min cameras if u is COVERED (no camera)
dp[u][2] = min cameras if u is NOT COVERED
```

Why its a post order DFS ?

To decide best state for $u$, we must already know

- best states of $u.left$
- best states of $u.right$

```python

def minCameraCover(self, root):
    INF = 10**9

    def dfs(node):
        if not node:
            # cannot place camera, covered, not covered
            return (INF, 0, 0)

        L0, L1, L2 = dfs(node.left)
        R0, R1, R2 = dfs(node.right)

        # place camera here
        dp0 = 1 + min(L0, L1, L2) + min(R0, R1, R2)

        # covered, no camera
        dp1 = min(
            L0 + min(R0, R1),
            R0 + min(L0, L1)
        )

        # not covered
        dp2 = L1 + R1

        return (dp0, dp1, dp2)

    # root must be covered
    # min(dp[root][0], dp[root][1])
    return min(dfs(root)[:2])

```

### Diameter of Binary Tree

- [**543. Diameter of Binary Tree**](https://leetcode.com/problems/diameter-of-binary-tree/) -  Standard diameter logic using two max child depths.

The length (number of edges) of the longest path between any two nodes in the tree

Important NOTE:

- The longest path doesn't necessarily pass through the root
- The path can go left -> parent -> right
- We count edges not nodes

The longest path in a tree may pass through any node

- For each node, the best path through it depends on:
- longest downward path in left subtree
- longest downward path in right subtree

Above shows that local computation aggregated globally ~ Tree DP

At every node, the longest path passing through that node is

```
left_depth + right_depth
```

The overall diameter is the maximum of this value across all nodes.

```python

def diameterOfBinaryTree(self, root):
    diameter = 0

    def dfs(node):
        nonlocal diameter
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        diameter = max(diameter, left + right)

        return 1 + max(left, right)

    dfs(root)
    return diameter

```