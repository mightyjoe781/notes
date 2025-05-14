## Problems on Binary Trees & BST

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