# B Tree
*Disk friendly ordered indexing*

Since scanning entire table for searching the data is too slow, we implement indexes, which take up some space in themselves but store reference to actual data.

Almost every database Index (MySQL, Postgres, SQLite, MongoDB) is B+ Tree.
NOTE: They are designed for *disk*, not RAM.

## Why not BST (Binary Search Tree)

A BST is designed for minimizing comparisons, But in databases we want to reduce disk reads (I/O), not CPU.

General Disk Access Costs

```
RAM Access ~ 100 ns
SSD Access ~ 100,000 ns
Disk Access ~ 10,000,000 ns
```

Reading 1 node is quite expensive, what if we make the node large. Instead of creating a Binary Tree let's create a Wide Tree (multiple children) making heights quite tiny.

```
2 (BST) ~ 1 Billion Records ~ 30 height
100 (BTree) ~ 1 Billion Records ~ 4 height
```

Effectively requiring on 4 Disk Reads.

## B Tree

- Balanced Data Structure for fast traversal
- In B Tree of `m` degree some nodes can have `m` child nodes
- Node has upto `m-1` elements
- Each element has a key and a value
- The value is usually data point to the row
- Data pointer can point to primary key or tuple
- Root Node, internal node and leaf nodes
- A node = disk page

![](assets/Pasted%20image%2020250925181131.png)

NOTE: Diagram in original paper is not correctly represented, $\alpha$ is not shown in the diagram.
NOTE: arrow are from inside the node, note this in the online simulator from sites below.

Try Online Visualizer

- https://www.cs.usfca.edu/~galles/visualization/BTree.html
- https://btree.app/

![](assets/Pasted%20image%2020250925191121.png)
## B Tree Limitations

- Elements in all nodes store both the key and the value.
- Internal nodes take more space thus require more IO, and can slow down traversal
- Range queries are slow because of random access (give me all values 1-5)
- B+ Trees solve both of these problems.

## B+ Tree

- Exactly like B-Tree but only stores keys in internal nodes
- Values are only stored in leaf nodes
- Internal nodes are smaller since they only store keys and they can fit more elements 
- Leaf nodes are `linked` so once you find a key you can find all values before and after that key.
- Great for Range Queries

Example B+ Tree of Degree 3

![](assets/Pasted%20image%2020250925192825.png)

Find rows (ID between (4 and 9))

![](assets/Pasted%20image%2020250925192920.png)

## B+ Tree Considerations

- Cost of leaf pointer (cheap)
- 1 Node fits in a DBMS page (most DBMS)
- Can fit internal nodes easily in memory for fast traversal
- Leaf nodes can live in data files in the heap
- Most DBMS systems use B+ Tree

![](assets/Pasted%20image%2020250925193108.png)
## B+ Tree storage cost in MySQL vs Postgres

- B+ Trees secondary index values can either point directly to tuple (postgres) or to the primary key (MYSQL)
- If the Primary key data type is expensive this can cause bloat in all secondary indexes for database such MySQL (innoDB)
- Leaf nodes in MySQL (InnoDB) contains the full row since its an IOT/Clustered Index.


