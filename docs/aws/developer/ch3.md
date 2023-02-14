## Databases

### Amazon DynamoDB

- NoSQL Database (Key-Value Store) : A collection of items or records.
- You can look up data : 
  - Using a primary key for each item
  - Through the use of indexes
- Very High Performance mainly used for Gaming, Web, Mobile and IoT
- Fully Managed : backups, patches etc are managed by AWS
- Bill consists of two factors
  - The total amount of throughput that you configure for your tables (provisioned capacity )
  - The total amount of storage space used by your data
- DynamoDB tables are schemaless, schema is defined per item
  - As long as the primary key is valid there is no limit on attributes
  - primary key consists of two attributes : partition key and sort key
- You can define several secondary indexes besides primary key for search
  - There are two types of secondary indexes : Global and Local Indexes
- Disadvantages
  - Since replication of data is present thorough multiple zones so it relies on concept of ***Eventual Consistency***, so its possible some zones might have older data
  - Queries are less flexible than SQL
  - Strict Workflow limitations like max record size : 400kb, max indexes per table : 20 global, 5 local
  - provisioned throughput (ProvisionedThroughputExceededException)

### Amazon Relational Database Service (RDS)

- Its a fully managed RDS that allows users to *Provision, Create, Scale* a relation database
- RDS allows us to choose from various Database Engines : MySQL, MariaDB, PostgreSQL, Amazon Aurora (fork of MySQL), Oracle (Common in Corporate), SQL Server
- Choice of compute instances is available while provisioning Database
  - General Purpose
  - Memory Optimized
- Synchrous Replication between primary and secondary instance. In case if primary instance fails then AWS automatically points DNS to secondary instance within (60-120s). [Multi AZ]
- Storage Autoscaling
  - EBS (Elastic Block Storage) (MySQL, Postgres, MariaDB, Oracle, SQL server)
    - General Purpose SSD storage, good for broad range of cases
    - Provisioned IOPS (SSD Storage), good for workloads that operate at very hight I/O
    - Magnetic Storage (mostly for backwards compatibility)
  - Shared Cluster Storage (Amazon Aurora)
    - Configuration options doesn’t exists and scaling occurs automatically
- vertical scaling : scaling towards computing capability
- horizontal scaling : increasing replicas of storage instances to deal with high volume of read queries. Note all replicas are synchrously linked.

### Amazon ElastiCache

- This service improves performance by using caching, where web application allow you to retrieve information fast, managed, in-memory data stores.
- Caching : Additional memory enables our devices to store frequently accessed information in memory instead of having to request the information from the hard drive
- It improves the read-only performance of server.
- Engines
  - Amazon Elasticache for Memcached : A high performance, submillisecond latency Memcached Compatible in-memory, key-value store service that can either be used as a cache, in addition to a data store
  - Amazon Elasticache for Redis : An in-memory data store designed for high performance and again providing sub-millisecond latency on a huge scale to real-time applications
- Components of Elasticode
  - Node : a fixed sized chunk of secure network attached RAM
  - Shard : redis shard (node group) a group of up to 6 Elasticache nodes
  - Redis Cluster : group of 1-90 redis shards
  - Memcached Cluster :  a collection of more cache nodes
- Elasticache should never used 
  - when data persistence is necessary
  - when working with primary data records
  - when we need write performance, rather than read performance

