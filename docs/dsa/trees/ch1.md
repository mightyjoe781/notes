# Trees

* Trees are hierarchical data structures consisting of nodes connected by edges.
* Each tree has a root node, and zero or more child nodes forming a *parent-child* relationship without cycles.

## Types of Trees

| Tree Type                    | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| **Binary Tree**              | Each node has at most two children (left and right).         |
| **Binary Search Tree (BST)** | A binary tree where left child < parent < right child, enabling efficient search operations. |
| **Balanced Trees**           | Trees maintaining height balance for efficient operations (e.g., AVL, Red-Black trees). |
| **Heap**                     | Complete binary tree satisfying heap property (min-heap or max-heap). |
| **Trie (Prefix Tree)**       | Tree used for storing strings, where each node represents a character, enabling fast prefix queries. |
| **Fenwick Tree (BIT)**       | Binary Indexed Tree for efficient prefix sum queries and updates. |
| **Segment Tree**             | Tree structure to efficiently answer range queries and updates on arrays. |
| **N-ary Tree**               | Each node can have any number of children, generalizing binary trees. |
| **Suffix Tree**              | Compressed trie of all suffixes of a string, used in string processing. |

## Implementation

````c++
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};
````

## Tree Traversal

| Traversal Type  | Description                      | Order of Processing                    |
| --------------- | -------------------------------- | -------------------------------------- |
| **Preorder**    | Visit root, traverse left, right | Root → Left → Right                    |
| **Inorder**     | Traverse left, visit root, right | Left → Root → Right                    |
| **Postorder**   | Traverse left, right, visit root | Left → Right → Root                    |
| **Level Order** | Traverse level by level (BFS)    | Top to bottom, left to right per level |

### Traversal Implementation

````c++
void preorder(TreeNode* root) {
    if (!root) return;
  	cout << root->val << " ";
    preorder(root->left);
    preorder(root->right);
}

void inorder(TreeNode* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->val << " ";
    inorder(root->right);
}

void postorder(TreeNode* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    cout << root->val << " ";
}

void levelOrderTraversal(TreeNode* root) {
    if (!root) return;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* node = q.front(); q.pop();
        cout << node->val << " ";
        if (node->left) q.push(node->left);
        if (node->right) q.push(node->right);
    }
}
````

## Binary Search Trees

* NOTE: Inorder traversal of the BST returns a sorted list

````c++
#include <iostream>
using namespace std;

class BST {
private:
    struct Node {
        int key;
        Node *left, *right;
        Node(int k) : key(k), left(nullptr), right(nullptr) {}
    };

    Node* root;

    // Recursive search
    Node* search(Node* node, int key) {
        if (node == nullptr || node->key == key)
            return node;
        if (key < node->key)
            return search(node->left, key);
        else
            return search(node->right, key);
    }

    // Recursive insert
    void insert(Node*& node, int key) {
        if (node == nullptr) {
            node = new Node(key);
            return;
        }
        if (key < node->key)
            insert(node->left, key);
        else
            insert(node->right, key);
    }

public:
    BST() : root(nullptr) {}

    // Public API
    void insert(int key) { insert(root, key); }
    bool search(int key) { return search(root, key) != nullptr; }
};
````

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


