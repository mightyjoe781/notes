## Differences Between AWS Database Types

### The AWS Database Landscape

In AWS three primary types of services used by Consumers : Compute, Storage, Database

There are two types of databases

- Relation (SQL)
  - optimized around data storage
  - based on Structured Query Language for data retrieval
- Non-Relational
  - process unstructured and semi-structured data quickly
  - often distributed on multiple nodes

There are nine primary categories of Databases available in AWS

1. Relational 
2. Key-Value
3. Document
4. In-Memory
5. Graph
6. Columnar
7. Time-Series
8. Quantum Ledger
9. Search

- Size, Shape and Computational Requirements of data gives idea to developers which kind of database is best for them.

- Cloud promises agility, ability to use and select appropriate database or multiple of them according to workload, rather than using one general purpose database.
- *Scalability* and *Elasticity* is another benefit from cloud

Types of Workloads

- Operational
  - Online Transactional Processing (OLTP) : OLTP is centered around a set of common business processes that are : *Regular, Repeatable* and *Durable*.
  - Examples includes : E-commerce, IT, CMS, etc.

- Analytical
  - Online Analytics Processing (OLAP) : Run for Business Intelligence Workloads or Data Analytics
  - Workloads are often : Retrospective(Company’s Quarter Analysis), Streaming(Real Time Processing) and Predictive(ML/AI)

### Relational Databases

**Schema :** structure that needs to defined before entering data into the database and designed based on reporting requirements.

- Relation DBs are highly structured and have been around since 60s.
- Schema changes are expensive in terms of time and compute power, with risk of corrupting data
- Data is stored in tables (Relation)
- Each Row is referred as *Record* and Each Column is referred as *Key*, and the value referenced is called as *Attribute*
- Each Table will have unique primary key that is used for relational purposes for other tables via foreign key.
- Data Integrity(data stored is reliable and accurate) is particular concern in RDBS : ACID transactions
  - Atomicity : A single database transaction (which succeeds or fails completely)
  - Consistency : Transaction must take database from one valid state to another valid state.
  - Isolation : Two transactions don’t interfere with each other
  - Durability : Data changes become permanent once the transaction is committed to database.
- Keys and Data Integrity
  - Primary and Foreign Key are constraints
  - Entity Integrity ensure primary key is unique to table and it has a value (NOT NULL)
  - Referential Integrity ensures that foreign key is primary key to its originating table. Orphaned Data is BAD !
- API of relational database is SQL (Structured Query Language)
- Relation databases have Data Access Controls and features like : Authentication, Authorization and Audit Logging

**Data Normalization: ** Normalisation is a process where information is organised efficiently and consistently before storing it.

- Duplicate data is discarded
- Closely related fields are aggregated

**Scaling and Sharding**

- Relational Databases are not partition tolerant, data partitions are called as shards. Two shards needs to co-ordinate to validate data consistency and it becomes costly. Both shards will same number of Keys (Horizontal Scaling (adds copy of the db))
- Most of the times Relational databases are scaled vertically (growing server by adding memory, cpu and a disk volume).

**AWS Relation Database Engines**(6) : Aurora(native to AWS), MySQL, Postgres, MariaDB, Oracle and Microsoft SQL Server.