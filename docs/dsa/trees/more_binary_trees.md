## Problems on Binary Trees & BST



| Types                         | Pattern                                         | Examples                                         |
| ----------------------------- | ----------------------------------------------- | ------------------------------------------------ |
| **Recursion with Return**     | Return values from children, accumulate results | Path Sum in Tree, Sum of Subsets                 |
| **Recursion with Parameters** | Track path, state                               | Subsequence with sum K, Combinations with k size |

| Problem Type                       | Description                                         | Example Questions          |
| ---------------------------------- | --------------------------------------------------- | -------------------------- |
| **Basic Traversals**               | Implement preorder, inorder, postorder, level order | Leetcode 94, 144, 102      |
| **Lowest Common Ancestor (LCA)**   | Find lowest shared ancestor of two nodes            | Leetcode 236, 1650         |
| **Balanced Tree Check**            | Check if tree height difference is bounded          | Leetcode 110               |
| **Validate BST**                   | Check if a binary tree satisfies BST property       | Leetcode 98                |
| **Serialize & Deserialize**        | Convert tree to string and back                     | Leetcode 297               |
| **Diameter of Binary Tree**        | Longest path between any two nodes                  | Leetcode 543               |
| **Path Sum**                       | Check if path with given sum exists                 | Leetcode 112, 113          |
| **Construct Tree from Traversals** | Rebuild tree from preorder/inorder/postorder        | Leetcode 105, 106          |
| **Trie Operations**                | Insert, search, prefix queries                      | Leetcode 208               |
| **Fenwick & Segment Trees**        | Range queries and updates                           | Range sum, minimum queries |


**Most Commonly Asked Interview Questions**

| Question Name                                     | Description                       | Difficulty |
| ------------------------------------------------- | --------------------------------- | ---------- |
| Binary Tree Inorder Traversal                     | Recursive and iterative traversal | Easy       |
| Validate Binary Search Tree                       | Check BST property                | Medium     |
| Lowest Common Ancestor of a Binary Tree           | Find LCA without BST property     | Medium     |
| Serialize and Deserialize Binary Tree             | Convert tree to string and back   | Hard       |
| Maximum Depth of Binary Tree                      | Find height of tree               | Easy       |
| Balanced Binary Tree                              | Check if tree is height-balanced  | Medium     |
| Construct Binary Tree from Preorder and Inorder   | Build tree from traversals        | Medium     |
| Trie: Implement Insert and Search                 | Basic trie implementation         | Medium     |
| Range Sum Query - Mutable (Segment Tree, Fenwick) | Handle dynamic range queries      | Hard       |

## Problems on Binary Trees

### Binary Tree Maximum Path Sum

- [Problem Link](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
- We have to find a path in the binary tree, that gives the max sum
- Maximum at a node could be following
    - Node’s value
    - Node’s value + max. sum from left subtree
    - Node’s value + max. sum from right subtree
    - Node’s Value + max. sum including both subtree

````c++
int maxSum = INT_MIN;
int solve(TreeNode* node) {
    if(!node)
        return 0;
    int left = max(solve(node->left), 0);
    int right = max(solve(node->right), 0);
    int rooted = node->val + left + right;

    maxSum = max(maxSum, rooted); // no need to check other 3 condition

    return node->val + max(left, right);
}
int maxPathSum(TreeNode* root) {
    solve(root);
    return maxSum;
}
````

### Root to Node Path in Binary Trees

Given a Binary Tree and a reference to a root belonging to it. Return the path from the root node to the given leaf node.

NOTE: Assume no two nodes in the tree have the same value, and value and path always exists.


| ![](assets/Pasted%20image%2020260115114738.png) |
| ----------------------------------------------- |
|                                                 |

```python

# read up the recursion portion for this

def getPath(root, x):

    def dfs(node, x, arr):
        if not node:
            return False
            
        arr.append(node.val)
        
        if node.val == x:
            return True
        
        if dfs(node, x, arr) or (node.right, x, arr):
            return True
            
        arr.pop()
        return False
    
    res = []
    dfs(root, x, res) # passed as reference
    return res

```

### Lowest Common Ancestor of a Binary Tree

Important and famous Question

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

![](assets/Pasted%20image%2020260115115331.png)

In the Image LCA of 5 and 1 is 3. Similarly LCA(5,4) is 5 itself.

NOTE: Below solution is for Binary Tree, not specifically for BST.

```python

def lowestCommonAncestor(root, p, q):
    def lca(node):
        # neither p nor q exists in subtree - None
        # either p or q exists and we found it - return p or q
        if not node or node in (p, q):
            return node
        
        # 6 possibility here
        # (p, q), (q, p) -> node is the actual LCA
        # (p, None), (None, p), (q, None), (None, q) -> LCA is higher up
        left, right = lca(node.left), lca(node.right)
        
        # only (p, q) and (q, p) ~ final LCA ~ return Node
        # return p or q ~ LCA is higher up
        return node if left and right else left or right
    return lca(root)

```

Fun Fact : LCA can be reduced into RMQ problem.

### Maximum Width of Binary Tree

Given the `root` of a binary tree, return _the **maximum width** of the given tree_.

The **maximum width** of a tree is the maximum **width** among all levels. 

NOTE: the width should be computed at each level, and null nodes are counted in width, as a result width calculations jump `2 * parent` and `2*parent + 1` for each left and right nodes respectively.

If it was simply co-ordinate system and nulls are not counted then it would be `width-1` and `width + 1`

```python

from collections import deque

def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:

    dq = deque()
    dq.append((root, 0))

    ans = 0
    while dq:
        n = len(dq)
        xmin, xmax = float('inf'), float('-inf')
        for _ in range(n):
            node, width = dq.popleft()
            if not node:
                continue
            xmin = min(xmin, width)
            xmax = max(xmax, width)
            dq.append((node.left, width*2))
            dq.append((node.right, width*2 + 1))
        
        ans = max(ans, xmax - xmin + 1)
    
    return ans

```


### Check for Children Sum Property in a Binary Tree

**Problem Statement:** Given a Binary Tree, convert the value of its nodes to follow the Children Sum Property. The Children Sum Property in a binary tree states that for every node, the sum of its children's values (if they exist) should be equal to the node's value. If a child is missing, it is considered as having a value of `0`.

NOTE:

- The node values can be increased by any positive integer any number of times, but decrementing any node value is not allowed.
- A value for a NULL node can be assumed as 0.
- We cannot change the structure of the given binary tree.


| ![](assets/Pasted%20image%2020260115124139.png) | ![](assets/Pasted%20image%2020260115124210.png) |
| ----------------------------------------------- | ----------------------------------------------- |
| Binary Tree Before Change                       | Binary Tree After Change                        |

```python

def changeTree(root):
    # Base case: If the current node
    # is None, return and do nothing.
    if root is None:
        return

    # Calculate the sum of the values of
    # the left and right children, if they exist.
    child = 0
    if root.left:
        child += root.left.val
    if root.right:
        child += root.right.val

    # Compare the sum of children with
    # the current node's value and update
    if child >= root.val:
        root.val = child
    else:
        # If the sum is smaller, update the
        # child with the current node's value.
        if root.left:
            root.left.val = root.val
        elif root.right:
            root.right.val = root.val

    # Recursively call the function
    # on the left and right children.
    changeTree(root.left)
    changeTree(root.right)

    # Calculate the total sum of the
    # values of the left and right
    # children, if they exist.
    tot = 0
    if root.left:
        tot += root.left.val
    if root.right:
        tot += root.right.val

    # If either left or right child
    # exists, update the current node's
    # value with the total sum.
    if root.left or root.right:
        root.val = tot

```



### All Nodes Distance K Binary Tree

Given the `root` of a binary tree, the value of a target node `target`, and an integer `k`, return _an array of the values of all nodes that have a distance_ `k` _from the target node._

You can return the answer in **any order**.

![](assets/Pasted%20image%2020260115125209.png)


```python


def distanceK(root, target, k):

    def links(node, parent=None):
        if not node:
            return
        
        node.parent = parent
        links(node.left, node)
        links(node.right, node)
    
    # build the graph for dfs, connect back-edge
    links(root)

    res = []
    seen = set()

    def dfs(node, d=0):
        if not node or d > k or node in seen:
            return
        seen.add(node)
        if d == k:
            res.append(node.val)
            return
        
        # in graph this would have been a : for u in adj[v]:
        dfs(node.parent, d+1)
        dfs(node.left, d+1)
        dfs(node.right, d+1)
    
    dfs(target)

    return res

```

### Minimum time taken to BURN the Binary Tree from a Node

**Problem Statement:** Given a target node data and a root of binary tree. If the target is set on fire, determine the shortest amount of time needed to burn the entire binary tree. It is known that in 1 second all nodes connected to a given node get burned. That is its left child, right child, and parent.

Approach : Convert the Tree into Graph, using backlinks, Then either run dfs, or bfs to find out the maximum length path in the graph.

## Binary Tree Structural Problems

A *binary tree can be uniquely reconstructed* **iff** you are given:

- *Inorder traversal + (Preorder or Postorder) traversal*

Nothing else guarantees uniqueness.

| **Traversals Given**  | **Unique Tree?** | **Why**                                 |
| --------------------- | ---------------- | --------------------------------------- |
| Inorder + Preorder    | Yes              | Root known, split via inorder           |
| Inorder + Postorder   | Yes              | Root known, split via inorder           |
| Preorder + Postorder  | No               | Left/right boundary ambiguous           |
| Inorder alone         | No               | No root info                            |
| Preorder alone        | No               | Structure ambiguous                     |
| Postorder alone       | No               | Structure ambiguous                     |
| Level-order alone     | No               | Multiple shapes possible                |
| Inorder + Level-order | No               | Root known, but subtree split ambiguous |

### Unique Binary Tree From Inorder + Postorder


![](assets/Pasted%20image%2020260115131454.png)

![](assets/Pasted%20image%2020260115132426.png)

NOTE: diagram only shows 2nd layer for right node only!

```python

def buildTree(inorder, postorder):
    
    n = len(inorder)

    # two pointer for both orders
    def build(x, y, a, b):
        if x > y or a > b:
            return None
        node = TreeNode(postorder[b])
        si = x
        while node.val != inorder[si]:
            si += 1
        
        node.left = build(x, si - 1, a, a+si-x-1)
        node.right = build(si+1, y, a + si -x, b-1)
        return node
    
    return build(0, n-1, 0, n-1)

```


### Unique Binary Tree From Inorder + Preorder

Similar concept as above, but removed the while loop searching for the `x` using `si` in inorder array with direct search in map.

![](assets/Pasted%20image%2020260115133605.png)

```python

def buildTree(preorder, inorder):

    idx_map = {v: i for i, v in enumerate(inorder)}
    # pick items one-by-one in preorder
    idx = 0

    def solve(start, end):
        nonlocal idx
        if start > end:
            return None
        
        node = TreeNode(preorder[idx])
        idx += 1

        mid = idx_map[node.val]

        node.left = solve(start, mid - 1)
        node.right = solve(mid + 1, end)

        return node

    return solve(0, len(inorder) - 1)

```

### Serialize and Deserialize a Binary Tree

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

```python

class Codec:

    def serialize(self, root):
        if not root: return "#"
        return str(root.val) + "," + self.serialize(root.left) + "," + self.serialize(root.right)
        

    def deserialize(self, data):
        nodes = iter(data.split(','))
        def build():
            val = next(nodes)
            if val == "#": return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        return build()

```

### Morris Pre-order Traversal

**Problem Statement:** Given a Binary Tree, implement Morris Preorder Traversal and return the array containing its preorder sequence.  
  
Morris Preorder Traversal is a tree traversal algorithm aiming to achieve a space complexity of O(1) without recursion or an external data structure. The algorithm should efficiently visit each node in the binary tree in preorder sequence, printing or processing the node values as it traverses, without using a stack or recursion.

Generally Morris Traversal can destroy tree, but we can mend it back together while traversal to recover it.

```python

# Morris - 1 (Destroys the tree)

def inorderTraversal(root_: TreeNode | None) -> list[int]:
    def inorder(root: TreeNode | None) -> Iterator[TreeNode]:
        node = root
        while node:
            if node.left:
                last = node.left
                while last.right: last = last.right
                
                last.right = node
                node = node.left
                last.right.left = None
            else:
                yield node
                node = node.right
            
    return [node.val for node in inorder(root_)]

# Morris - 2 (Destroys and recovers the tree)
def inorderTraversal(self, root_: TreeNode | None) -> list[int]:

    def inorder(root: TreeNode | None) -> Iterator[TreeNode]:
        node = root
        while node:
            if node.left:
                last = node.left
                while last.right and last.right != node:
                    last = last.right
                
                if last.right:
                    last.right = None
                    yield node
                    node = node.right
                else:
                    last.right = node
                    node = node.left
            else:
                yield node
                node = node.right
            
    return [node.val for node in inorder(root_)]


```

### Flattening the Tree into Linked List

solution link : [Link](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/solutions/940394/python3-iterative-solution-with-explanat-0h8s/)

![](assets/Pasted%20image%2020260115152457.png)

```python

def flatten(self, root: TreeNode) -> None:
    cur = root
    while cur:
        if cur.left:
            prev = cur.left
            while prev.right:
                # We go to left Subtree's rightMost Node
                prev = prev.right    
            # We make current Node's right Subtree prev's right Subtree
            prev.right = cur.right 
            cur.right = cur.left    # We make it right Subtree
            cur.left = None   # Removing left 
        
        cur = cur.right

```

A recursive Solution to the problem

```python

def flatten(self, root: Optional[TreeNode]) -> None:
    if not root:
        return 
    self.flatten(root.right)
    self.flatten(root.left)
    root.left=None
    root.right=self.prev
    self.prev=root

```