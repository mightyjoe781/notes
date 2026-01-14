# Binary Trees

*In a binary tree each node has at most two children (left and right).*

### Height of a Binary Tree

Given the `root` of a binary tree, return _its maximum depth_.

Generally there are two approaches to solving recursion on binary tree. Either create global variables and do a simple traversal while calculating object during traversal.

Other method is more preferred as it forms foundation of recursion and DP problems later on. In this case function returns the solution.


```python


## global var approach
def maxDepth(self, root: Optional[TreeNode]) -> int:
    res = 0

    def dfs(node, lvl = 0):
        nonlocal res
        if not node:
            return node
        lvl += 1
        res = max(res, lvl)
        dfs(node.left, lvl)
        dfs(node.right, lvl)

    dfs(root)
    return res

# Functional approach
def maxDepth(root):

    def dfs(node):
        if not node:
            return 0
        
        return 1 + max(
            dfs(node.left),
            dfs(node.right)
        )
    
    return dfs(root)

```

### Check if Binary tree is height-balanced or not

```python

def isBalanced(self, root: Optional[TreeNode]) -> bool:

    ans = True

    def dfs(node):
        nonlocal ans

        if not node:
            return 0
        
        l = dfs(node.left)
        r = dfs(node.right)
        # every node compare this heights
        if abs(l -r) > 1: 
            ans = False

        return 1 + max(l, r)
        
    dfs(root)

    return ans

```

Notice how dfs keeps happening even tho we found that constraint is violated and do not early exit.

### Diameter of Binary Tree

Given the `root` of a binary tree, return _the length of the **diameter** of the tree_.

```python

def diameterOfBinaryTree(root):

    ans = 0

    def height(node):
        nonlocal ans
        if not node:
            return 0

        left = height(node.left)
        right = height(node.right)

        ans = max(ans, left + right)
        return 1 + max(left, right)

    height(root)
    return ans

```

A more idiomatic DP style recursion might be difficult here, will require multi-return solution.

```python

def diameterOfBinaryTree(self, root):
    def dfs(node):
        if not node:
            return 0, 0  # height, diameter

        lh, ld = dfs(node.left)
        rh, rd = dfs(node.right)

        height = 1 + max(lh, rh)
        diameter = max(ld, rd, lh + rh)

        return height, diameter

    return dfs(root)[1]

```

### Maximum Path Sum

A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence **at most once**. Note that the path does not need to pass through the root.

```python

def maxPathSum(self, root):
    ans = float('-inf')

    def dfs(node):
        nonlocal ans
        if not node:
            return 0

        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)

        # path that ends at this node (can fork)
        ans = max(ans, node.val + left + right)

        # path that can be extended to parent (no fork)
        return node.val + max(left, right)

    dfs(root)
    return ans

```


### Same Tree

Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.

```python

def isSameTree(p, q) -> bool:
    if p == None and q == None:
        return True
    if p == None or q == None:
        return False
    if p.val != q.val:
        return False
    return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
    
```


### Vertical Order Traversal

```python

from collections import defaultdict
def verticalTraversal(root) -> List[List[int]]:
    mp = defaultdict(list)

    def dfs(node, x = 0, y = 0):
        if not node:
            return
        
        mp[y].append((x, node.val))

        dfs(node.left, x+1, y-1)
        dfs(node.right, x+1, y+1)

    dfs(root)
    res = []
    for k in sorted(mp.keys()):
        res.append([b for a, b in sorted(mp[k])])
    return res

```

