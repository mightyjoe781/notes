# B Tree

## Full Table Scans

- To find a row in a large table we perform full table scan
- reading large tables is slow
- Requires many IOs to read all pages,
- We need a way to reduce the IOs

## B Tree

- Balanced Data Structure for fast traversal
- B-Tree has Nodes
- In B-Tree of `m` degree some nodes can have `m` child nodes
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


