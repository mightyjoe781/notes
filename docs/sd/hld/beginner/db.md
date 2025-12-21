# Databases and Scaling

>    Data is the new oil — but only if you can store, query, and scale it.

Databases can be divided into two categories: *Relational* or *Non-Relational* Databases, 
## Relational Databases

* Data is stored and represented in row & columnar fashion.

History of Relational Databases

* Computers first did *accounting* -> *ledgers* -> *Rows & Columns*
* Databases were developed to support accounting
* Key Properties
    * Data consistency
    * Data durability
    * Data integrity
    * Constraints
    * Everything in one place
* Because of this reason, relational databases provides ACID properties to support *Transactions*

* A - Atomicity
* C - Consistency
* I - Isolation
* D - Durability
* [Lecture on ACID by Martin Klepmann](https://www.youtube.com/watch?v=5ZjhNTM8XU8)

### Atomicity

* All statements within a transaction takes effect or none
* e.g. start transaction { publish a post and increase total posts count } commit
* Often confused with concurrency, while it actually defines how system recovers from faults (rollback). Should have been called *Abortability*.

### Consistency

* `C` in ACID is not same as one in CAP Theorem.
* C is more like a term thrown around to make the acronym work. It defines that data will always move from one consistent state to another.
* Definition : Data will never go incorrect, no matter what. Constraint, Cascades, Triggers will ensure above property in one way or another.
* Ex - In a Financial system, all the debits must add up to equal to credits. 
* Foreign Keys Checks ensure parent can't be deleted if child exists (can be turned on in DB). You can enable cascades or triggers to ensure data comes back to consistent state.

### Durability

* when transaction commits, the changes outlives outage.
* When archive tapes were used, you can restore database back from its initial state to final state using archives.

### Isolation

* when multiple transactions are executing parallely, the *isolation level* determines how much changes of one transactions are visible to other.
* Serializable ? Effect of all transaction is as if they have executed serially. In Computer Architecture people realized it was little slow, so they fiddled around locks to figure out to make it work fast.

## Database Isolation Levels

* Isolation levels dictate how much one transaction knows about the other.

NOTE: Following examples assumes that there are two txns executing parallely, i.e. T1, T2

### Repeatable Reads

* consistent reads within same transaction.
* Even if other transaction(T2) committed 1st transaction(T1) would not see the changes (if value is already read)
* Default in Postgres, Oracle, SQL Server. 
* It guarantees : both dirty reads and dirty writes never happen.
### Read Committed

* Read within same transaction always reads fresh value.
* cons : multiple reads within same transaction are inconsistent
### Read Uncommitted

* reads even uncommitted values from other transactions : *dirty reads*
* Example: Let's say both T1, and T2 begins, T2 modifies some value but doesn't commit. Yet querying same value in T1 will show the changes.
### Serializable

* Every read is a locking read (depends on engine) and while one txn reads, other will have to wait.
* NOTE: Every storage engine has its own implementation of serializable isolation, read documentation carefully.

## Scaling Databases

* These techniques are applicable to most databases out there

### Vertical Scaling

* add more CPU, RAM, Disk to the database
* requires downtime during reboot
* gives ability to handle *scale*, more load
* vertical scaling has physical hardware limitation

### Horizontal Scaling : Read Replicas

* when read: write = 90:10
* you move reads to other databases using Master-Slave Topology
* Master is the only replica that can write, API servers must know which DB to get connected to get things done.

### Replication

* Changes on one database (Master) needs to be sent to Replica to Maintain Consistency
* There are two types to of replication

#### Synchronous Replication

* Strong Consistency
* Zero Replication Lag
* Slower Writes

#### Asynchronous Replication

* Eventual Consistency
* Some Replication Lag
* Faster Writes

![](assets/Pasted%20image%2020251221192552.png)

## Sharding and Partitioning

* Since one node cannot handle the data/load, we can split it into multiple exclusive subsets.
* writes on a particular row/document will go to one particular shard, allowing us to scale overall database load
* NOTE: Shards are independent no replication b/w them
* API server needs to know which shard to connect, some databases have their own proxy to take care of routing. Each shard can have its own replica as well.
* NOTE: *Indexing* is just a quick reference to keys, doesn't physically divide the table.

### Sharding & Partitioning

![](assets/Pasted%20image%2020251221193317.png)

![](assets/Pasted%20image%2020251221193850.png)

* Sharding : Method of distributing data across *multiple machines*.
* Partitioning : splitting a subset of data *within* the same instance.
* How a database is scaled
    * A database server is just a databases process running on an EC2
    * post production deploying, your service is serving the real traffic (100wps)
    * Suddenly there is a surge of users (200wps)
    * To handle load, you can scale up your database, increase RAM, CPU and DISK
    * Now, suddenly traffic surges in popularity (1000wps)
    * you can’t scale up beyond limits of the provider, you will have to scale horizontally 
    * Then you should split the data into multiple databases, providing higher throughput
* In above example splitting data into multiple database(shard) is called *partitioned*
* How to partition the data ? There are two categories of partitioning
    * Horizontal Partitioning (Common) - Within table take rows based on some property into multiple partitions
    * Vertical Partitioning
* In above split depends on *load*, *use-case*, and *access patterns*
* Shards
    * Advantages
        * Handle large Read and Writes
        * Increases overall storage capacity
        * Higher Availability
    * Disadvantages
        * Operationally Complex
        * Cross-Shard Queries Expensive

## Non-Relational Databases

* broad generalization of database, mostly supporting *sharding* (supporting horizontal scalability)

### Document DB

* Ex - MongoDB, DynamoDB (supports documentDB features)
* Mostly JSON based
* Support complex queries (almost like relational databases)
* Partial Updates to documents possible (no need to update entire document)
* Closest to Relational Database
* in-app notification service, catalog service

### Key Value Stores

* Redis, ElasticSearch, Aerospike, DynamoDB (primarily key-store)
* Extremely simple databases
* Limited Functionality (GET, PUT, DEL)
* meant for key-based access pattern
* doesn’t support complex queries (aggregations)
* can be heavily sharded and partitioned
* use case: profile data, order data, auth data, messages, etc.
* You can use relational databases and document DBs as KV stores

### Graph Databases

* Neo4j, Neptune, DGraph
* what if our graph data structure had a database
* it stores data that are represented as nodes, edges and relations
* useful for running complex graph algorithms
* powerful to model, social networks, recommendation systems, fraud detection

## Picking the Right Database

* A database is designed to solve a *particular problem* really well.
* Common Misconception: Picking Non-relational DB because relational databases do not scale.
* Why non-relational DBs scale
    * There are no relations & constraint
    * Data is modeled to be sharded
* If we relax above condition on relational databases then they can be scaled.
    * do not use foreign key check
    * do not use cross shard transaction
    * do manual sharding
* Does this mean, no DB is different
    * No every single database has some peculiar properties and guarantees and if you need those, pick that DB
* How does this help in designing system
    * While designing any system, do no jump to DB directly
    * Understand *what* & *how much* data you will be storing
    * Understand the *access pattern* for data
    * Any special feature like *TTL* etc required.