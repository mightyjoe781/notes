# Binary Search Tree

## Introduction

Binary Search Trees, popularly known as BST, are the category of Binary Trees used to optimize the operation of searching an element among the Tree Nodes in a Binary Tree.

For every given node in a Binary Search Tree if a left or a right child exists then:

```
left_child < root < root_child
```

BST lay down the foundation for Heaps.

Since a lot of tree traversing is skipped using above constraint and search is directed in a form where we are performing directed DFS. So for a $n$ nodes tree it would probably take $O(\log_2 n)$ time to traverse and perform most of operations.
## Problems

### Search in BST

```python

def searchBST(root, val):

    def search(node):
        if not node:
            return node

        if node.val == val:
            return node
        
        if node.val > val:
            return search(node.left)
        else:    
            return search(node.right)

    return search(root)

```

More minified version

```python

def searchBST(root, val):

    def search(node):
        if not node or node.val == val:
            return node
 
        return search(node.left) if node.val > val else search(node.right)
        
    return search(root)

```

### Ceil & Floor in a BST

Following is iterative approach to do Search in BST

```python

def findCeil(root, key):

    ceil = -1

    while root:

        if root.val == key:
            ceil = root.val
            return ceil
        
        if key > root.val:
            root = root.right
        else:
            ceil = root.val
            root = root.left

    return ceil

```

### Insert a node in BST

You are given the `root` node of a binary search tree (BST) and a `value` to insert into the tree. Return _the root node of the BST after the insertion_. It is **guaranteed** that the new value does not exist in the original BST.

**Notice** that there may exist multiple valid ways for the insertion, as long as the tree remains a BST after insertion. You can return **any of them**.

![](assets/Pasted%20image%2020260115163223.png)


```python

def insertIntoBST(root, val):

    # find insertion pt
    p = root
    prev = None
    while p:
        prev = p
        if p.val > val:
            p = p.left
        else:
            p = p.right
        
    if prev:
        if prev.val > val:
            prev.left = TreeNode(val)
        else:
            prev.right = TreeNode(val)
    else:
        # no suitable insertion point
        return TreeNode(val)
    
    return root

```

### Delete a node in BST

Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return _the **root node reference** (possibly updated) of the BST_.

Basically, the deletion can be divided into two stages:

1. Search for a node to remove.
2. If the node is found, delete the node.

```python

def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
    if not root:
        return None

    if root.val == key:
        # Case 1: no right child → replace with left subtree
        if not root.right:
            return root.left

        # Case 2: has right child
        # find inorder successor (leftmost node in right subtree)
        succ = root.right
        while succ.left:
            succ = succ.left

        # swap values
        root.val, succ.val = succ.val, root.val

    # continue deletion (now key exists lower in tree)
    root.left = self.deleteNode(root.left, key)
    root.right = self.deleteNode(root.right, key)

    return root


```

### Find k-th Largest Element in BST

Do Inorder traversal in BST and stop traversal at `kth` value or store traversal in a array and return `res[k-1]`

### Validate whether Tree is BST or not

Given the `root` of a binary tree, _determine if it is a valid binary search tree (BST)_.

```python

def isValidBST(self, root: Optional[TreeNode]) -> bool:
    
    def check(node, cmin, cmax):
        if not node:
            return True
        
        if node.val <= cmin or node.val >= cmax:
            return False
        
        return (check(node.left, cmin, node.val) and check(node.right, node.val, cmax)

    return check(root, float('-inf'), float('inf'))

```

### LCA in BST

Similar to LCA in Binary Tree but we can utilize `p` and `q` to direct the search.


```python

def lca(node, p, q):
    if node.val > p.val and node.val > q.val:
        return lca(node.left, p, q)
    if node.val < p.val and node.val < q.val:
        return lca(node.right, p, q)
    return node

```

### Construct a BST from preorder traversal

Since inorder traversal of the BST is sorted then we have got `inorder` and `preorder` traversal of a tree, we can simply generate the tree.
Refer to previous sections.

### Two Sum in BST

```python

## keep doing inorder traversal of the tree and keep found numbers in set to
# quickly check if other number exists

def findTarget(root, k: int):

    if not root:
        return False
    
    bfs, s = [root], set()

    # notice how this works because for loop call `next()` on extending bfs
    for i in bfs:
        if k - i.val in s:
            return True
        s.add(i.val)
        if i.left: bfs.append(i.left)
        if i.right: bfs.append(i.right)
    
    return False

```

### Recover BST

You are given the `root` of a binary search tree (BST), where the values of **exactly** two nodes of the tree were swapped by mistake. _Recover the tree without changing its structure_.

```

BST : 1, 2, 3, 4, 5
Swapped Case: 1, 4, 3, 2, 5

```

We can clearly see that (4,2) are swapped here.

There are two possibility of Swapped Nodes

- Swapped nodes are adjacent
- Swapped nodes are far apart

In both cases we find nodes where `prev.val > curr.val`

Idea is simple to do inorder traversal, where on violation (above condition), first time we mark first = prev, every time -> mark second = curr

```python

def recoverTree(self, root: TreeNode) -> None:
    first = second = prev = None

    def inorder(node):
        nonlocal first, second, prev
        if not node:
            return

        inorder(node.left)

        if prev and prev.val > node.val:
            if not first:
                first = prev
            second = node

        prev = node
        inorder(node.right)

    inorder(root)
    first.val, second.val = second.val, first.val

```

### Binary Search Tree Iterator using Stack

```python

class BSTIterator:

    def __init__(self, root: Optional[TreeNode]):
        self.node = root
        self.stk = []
        

    def next(self) -> int:
        # put all left nodes in stack
        while self.node:
            self.stk.append(self.node)
            self.node = self.node.left

        # top has smallest number
        next_ = self.stk.pop()

        # internal node points to right now
        self.node = next_.right
        return next_.val

    def hasNext(self) -> bool:
        return self.node is not None or len(self.stk) != 0

```

### Largest BST

At each node we need to check 4 things about its subtree.

- Is it a BST
- Size of subtree
- Min. val in the subtree
- Max. val in the subtree.

This is a *postorder DP* on trees problem.

A Subtree root at node is a `BST` iff

- left is BST
- right is BST
- `left.max` < node.val < `right.min`

```python

def largestBSTSubtree(self, root: TreeNode) -> int:
    self.ans = 0

    def dfs(node):
        # returns: (is_bst, size, min_val, max_val)
        if not node:
            return True, 0, float("inf"), float("-inf")

        l_bst, l_size, l_min, l_max = dfs(node.left)
        r_bst, r_size, r_min, r_max = dfs(node.right)

        if l_bst and r_bst and l_max < node.val < r_min:
            size = l_size + r_size + 1
            self.ans = max(self.ans, size)
            return True, size, min(l_min, node.val), max(r_max, node.val)

        return False, 0, 0, 0

    dfs(root)
    return self.ans

```


### Merge Two BSTs

A simple strategy is to combine inorder traversal of both BSTs, and generate a Balanced BST out of that inorder traversal.

It is combined question involving

- inorder traversal
- merging sorted lists
- build a balanced BST from inorder list

```python

def mergeBSTs(self, root1: TreeNode, root2: TreeNode) -> TreeNode:
    def inorder(node, arr):
        if not node:
            return
        inorder(node.left, arr)
        arr.append(node.val)
        inorder(node.right, arr)

    a, b = [], []
    inorder(root1, a)
    inorder(root2, b)

    # merge two sorted list problem
    merged = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            merged.append(a[i]); i += 1
        else:
            merged.append(b[j]); j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])

    # build bst
    def build(arr, l, r):
        if l > r:
            return None
        m = (l + r) // 2
        node = TreeNode(arr[m])
        node.left = build(arr, l, m - 1)
        node.right = build(arr, m + 1, r)
        return node

    return build(merged, 0, len(merged) - 1)


```


## Selecting Optimal Tree

| **Data Structure**          | **Point Update** | **Point Query** | **Range Update** | **Range Query** | **Time Complexity (Update / Query)** | **Space**  | **Common Use Cases**                                         |
| --------------------------- | ---------------- | --------------- | ---------------- | --------------- | ------------------------------------ | ---------- | ------------------------------------------------------------ |
| **Fenwick Tree (Classic)**  | ✅                | ❌*              | ❌                | ✅ (prefix)      | O(log n) / O(log n)                  | O(n)       | Prefix sums, XORs, frequency counts                          |
| **Fenwick Tree (Dual)**     | ❌                | ✅               | ✅                | ❌               | O(log n) / O(log n)                  | O(n)       | Range add + point read, simulation of cumulative effects     |
| **Fenwick Tree (2-BIT)**    | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(n)       | Full support for sum range queries with range updates        |
| **Segment Tree**            | ✅                | ✅               | ❌                | ✅               | O(log n) / O(log n)                  | O(4n)      | RMQ, range sum/min/max/gcd with point updates                |
| **Segment Tree + Lazy**     | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(4n)      | Full range queries + range updates, e.g., add 5 over [l..r]  |
| **Sparse Segment Tree**     | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(k log n) | Sparse values over large domains (e.g., up to 1e9)           |
| **Persistent Segment Tree** | ❌ (new ver)      | ✅ (old ver)     | ❌ (immutable)    | ✅ (prev ver)    | O(log n) / O(log n)                  | O(n log n) | Time-travel queries, undo/rollback, version control          |
| **Sqrt Decomposition**      | ✅                | ✅               | ✅* (limited)     | ✅               | O(√n) / O(√n)                        | O(n)       | Simpler implementation for mid-size n, not time-critical problems |
| **Wavelet Tree**            | ❌                | ✅ (rank)        | ❌                | ✅ (freq)        | O(log n) / O(log n)                  | O(n log n) | K-th smallest, rank/select, frequency queries in a range     |
