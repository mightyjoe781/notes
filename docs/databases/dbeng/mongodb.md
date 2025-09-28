# NoSQL Architecture

![](assets/Pasted%20image%2020250927204924.png)

### SQL vs NoSQL

NoSQL is alternative data format rather than previously standardized SQL which assumed storage always to be in form of tables.
Storage Engine always stores the data in *pages*.
In MongoDB we store a document in the page of storage engine. Because to efficiently write to disk we are supposed to write in blocks, sectors, etc in chunks. RAM supports byte addressability that is why we can do pointed writes quite fast.

While writing to RAM (marking page as dirty page), database engine writes to WAL/journal as well, later it flushes to disk.

Difference between NoSQL and SQL is just frontend and restrictions coming from inherent old tabular design.
Tables and rows becomes, (JSON -> BSON) before persisting.



### MongoDB Basics

![](assets/Pasted%20image%2020250927212805.png)

MongoDB is a *document* based NoSQL database which means it doesn't operate on relation level.

Users submit JSON document to Mongo where they are internally stored as BSON (Binary JSON) format for faster and efficient storage. Mongo retrieves BSON and convert it back to JSON for users.

Because these documents can be large, Mongo can sometimes compress them further to reduce the size.

Users create collections (similar to tables in RDBMS), but since documents are schema-less we can store anything in a document. This features is most famous and most abused feature of Mongo :).

### `_id` index

When we create a collection in Mongo, a primary key `_id` representing document id is created along side a B+ Tree index, so that search is optimal. Its uniquely locates a document and can be used to find it.

`_id` is 12 bytes long to ensure is can be uniquely identifies across machines or shards for scalability.

### Secondary Indexes

Users can create secondary B+ Tree indexes on any field on the collections which then points back to BSON documents satisfying the index. This allows fast traversal on the different fields, not just the default `_id` field.
The size of secondary index depends on two things, the key size which represents the field size being indexed and document pointer size.

Prior version (4.2) used the document identifier (`_id`) and `offset` to find the document to fetch. But this design has shortcoming of updates to document (offset changes), strict concurrency control (global lock). Basically two txns can't change documents in the collections. Even tho it was updated to collection locks it was still problematic.
Later Mongo acquired WiredTiger storage Engine, for ability of document level locking on same collections concurrently, compression, clustered indexes(similar to rows in the MySQL). Range queries are efficient due to linked list fashion documents are arranged in.

In later versions `_id` field becomes the index and points to the clustered documents. Secondary indexes points to `_id`, 12 bytes (too large to guarantee uniqueness). So this suffers from randomness :)

### MongoDB Clustered Collections

In July 2022, Mongo introduced Clustered collection which basically stores the leaf page results in the index itself. What is commonly known as Index-only Scans in MySQL (Clustered Indexes) removing hidden WT index.


References for above sections

- https://medium.com/@hnasr/mongodb-internal-architecture-9a32f1403d6f
- [https://groups.google.com/g/wiredtiger-users/c/qQPqhjxyU00](https://groups.google.com/g/wiredtiger-users/c/qQPqhjxyU00)
- [http://smalldatum.blogspot.com/2021/08/on-storage-engines.html?m=1](http://smalldatum.blogspot.com/2021/08/on-storage-engines.html?m=1)
- [http://smalldatum.blogspot.com/2015/07/linkbench-for-mysql-mongodb-with-cached.html](http://smalldatum.blogspot.com/2015/07/linkbench-for-mysql-mongodb-with-cached.html)
- [https://groups.google.com/g/mongodb-dev/c/8dhOvNx9mBY](https://groups.google.com/g/mongodb-dev/c/8dhOvNx9mBY)
- [https://www.mongodb.com/docs/upcoming/core/clustered-collections/#clustered-collections](https://www.mongodb.com/docs/upcoming/core/clustered-collections/#clustered-collections)
- [https://jira.mongodb.org/browse/SERVER-14569](https://jira.mongodb.org/browse/SERVER-14569)
- [https://www.mongodb.com/docs/v4.4/reference/operator/meta/showDiskLoc/](https://www.mongodb.com/docs/v4.4/reference/operator/meta/showDiskLoc/)
- [https://github.com/mongodb/mongo/commit/374438c9134e6e31322b05c8ab4c5967d97bf3eb](https://github.com/mongodb/mongo/commit/374438c9134e6e31322b05c8ab4c5967d97bf3eb)


