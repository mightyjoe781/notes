# Trees

* Trees are hierarchical data structures consisting of nodes connected by edges.
* Each tree has a root node, and zero or more child nodes forming a *parent-child* relationship without cycles.

## Types of Trees

| Tree Type                    | Description                                                                                          |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Binary Tree**              | Each node has at most two children (left and right).                                                 |
| **Binary Search Tree (BST)** | A binary tree where left child < parent < right child, enabling efficient search operations.         |
| **Balanced Trees**           | Trees maintaining height balance for efficient operations (e.g., AVL, Red-Black trees).              |
| **Heap**                     | Complete binary tree satisfying heap property (min-heap or max-heap).                                |
| **Trie (Prefix Tree)**       | Tree used for storing strings, where each node represents a character, enabling fast prefix queries. |
| **Fenwick Tree (BIT)**       | Binary Indexed Tree for efficient prefix sum queries and updates.                                    |
| **Segment Tree**             | Tree structure to efficiently answer range queries and updates on arrays.                            |
| **N-ary Tree**               | Each node can have any number of children, generalizing binary trees.                                |
| **Suffix Tree**              | Compressed trie of all suffixes of a string, used in string processing.                              |

## Implementation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## Tree Traversal

| Traversal Type  | Description                      | Order of Processing                    |
| --------------- | -------------------------------- | -------------------------------------- |
| **Preorder**    | Visit root, traverse left, right | Root → Left → Right                    |
| **Inorder**     | Traverse left, visit root, right | Left → Root → Right                    |
| **Postorder**   | Traverse left, right, visit root | Left → Right → Root                    |
| **Level Order** | Traverse level by level (BFS)    | Top to bottom, left to right per level |

### Traversal Implementation

```python
def preorder(root):
    if not root: return
    print(root.val)
    preorder(root.left)
    preorder(root.right)

def inorder(root):
    if not root: return
    inorder(root.left)
    print(root.val)
    inorder(root.right)

def postorder(root):
    if not root: return
    postorder(root.left)
    postorder(root.right)
    print(root.val)

from collections import deque
def level_order(root):
    if not root: return
    q = deque([root])
    while q:
        node = q.popleft()
        print(node.val)
        if node.left: q.append(node.left)
        if node.right: q.append(node.right)
```

## Binary Search Trees

* NOTE: Inorder traversal of the BST returns a sorted list

### Iterative Approach to Above Traversals

Pre-order Traversal

```python

from collections import deque
def preorderTraversal(root):

    res = []
    stk = deque()
    stk.append(root)

    while stk:
        t = stk.pop()
        if not t:
            continue
        res.append(t.val)
        stk.append(t.right)
        stk.append(t.left)
    
    return res
```

## Problems


