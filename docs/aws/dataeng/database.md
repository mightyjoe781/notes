# Database

- Database are of two types
    - RDBS ~ MySQL, PostgreSQL, etc.
    - Non-RDBS ~ MongoDB, Cassandra, GraphQL, etc.
- RDBS are very good for joins, aggregations, and complex computations utilising SQL Query Language for easier access. 
- Traditionally easier to scale vertically (CPU/RAM/IO), with Horizontal Scaling (read capacity increase by using EC2/RDS Read Replicas)
- NoSQL Databases don't support *joins* (limited), perform well with aggregations but are *distributed* by design.
- NoSQL Databases scale horizontally naturally. 

## Amazon DynamoDB

- Fully Managed, highly available NoSQL Database with replication across multiple AZs
- Scales to massive workloads, distributed database
- Millions of requests per seconds, trillion of rows, 100s TB of storage
- Fast and consistent in performance (low latency on retrieval)
- Integrated with IAM for security, authorization and administrations
- Enabled event driven programming with DynamoDB Streams.
- Standard & IA (Infrequent Access) Table Class

### Basics

- DynamoDB is made of Tables
- Each table has Primary Key (must be decided at creation time)
- Each table can have infinite number of items (rows)
- Each items has attributes (Can be added over time ~ can be null)
- Max Size of an item is 400KB
- Data types supported are
    - Scalar Types ~ String, Number, Binary, Boolean, Null
    - Document Types ~ List, Map
    - Set Types ~ String Set, Number Set, Binary Set

### Choosing Primary Keys

![](assets/Pasted%20image%2020251108163637.png)

- Option 1 : Partition Key (HASH)
    - Partition key must be unique for each item
    - Partition key must be *diverse* so that the data is distributed
    - Example : `user_id` for a users table

![](assets/Pasted%20image%2020251108163654.png)

- Option 2: Partition Key + Sort Key (HASH + RANGE)
    - The combination must be unique for each item
    - Data is grouped by partition key

- Common use Cases in Big Data
    - Mobile Apps
    - Gaming
    - Digital ad serving
    - Live Voting
    - Audience interaction for live events
    - Sensor networks
    - Log Ingestion
    - Access control for web-based content
    - Metadata storage for S3 Objects
    - E-commerce shopping carts
    - Web Session Management
- Anti Pattern
    - Prewritten application tied to a traditional relational database use RDS instead
    - Joins or complex transactions
    - Binary Large Object (BLOB) data : store data in S3 & metadata in DynamoDB
    - Large data with low I/O rate: use S3 instead

### Read/Write Capacity Modes

- Control table's capacity (read/write throughput)

- Provisioned Mode
    - specify reads/writes per second
    - needs to be decided beforehand
    - pay for *provisioned* read/write capacity units
- On-Demand Mode (default)
    - Read/Write automatically scale up/down with workloads
    - No capacity planning needed
    - Pay for what you use, more expensive
- Can be switched once 24 hrs

#### Provisioned

- Tables must have read/write capacity units
- Read Capacity Units (RCU) ~ throughput for reads
- Write Capacity Units (WCU) – throughput for writes
- Option to setup *auto-scaling* of throughput to meet demand
- Throughput can be exceeded temporarily using “Burst Capacity”
- If Burst Capacity has been consumed, you’ll get a “ProvisionedThroughputExceededException”
- It’s then advised to do an exponential backoff retry

#### Calculation for WCU

- One WCU ~ one-write per second for an item upto 1KB in size
- If the items are larger than 1 KB, more WCUs are consumed
- Ex ~ 10 items/second with 2KB ~ 10 * (2/1) ~ 20WCUs
- Ex ~ 6 items/second with 4.5KB ~ 6 * (5/1) ~ 30WCUs

#### Strongly Consistent Read vs Eventually Consistent Read

![](assets/Pasted%20image%2020251108165634.png)

- Eventually Consistent Read (default)
    - possibility of reading stale data
- Strong Consistent Read
    - read after a write,
    - Set *ConsistentRead* parameter to *True* in API Calls
    - Consumes twice the RCUs

#### Calculations for RCUs

- One Read Capacity Unit (RCU) represents one *1 Strongly Consistent Read/sec* or *2 Eventually Consistent Reads/sec*  for an item upto *4KB* in size
- If items > 4KB, more RCUs are consumed
- Ex ~ 10 strongly consistent reads/sec for item with size 4KB ~ 10 RCUs
- Ex ~ 16 eventual consistent reads/sec for items with size 12 KB ~ 24 RCUs

### Partition Internals

![](assets/Pasted%20image%2020251108165951.png)

- Data is stored in partitions
- Partition Keys go through a Hashing Algorithm to know which partition to put data in

To compute the number of partitions

$$
\# \text{ of partitions}_{\text{by capcity}} = \frac{\text{RCUs}_\text{Total}}{3000}
 + \frac{\text{WCUs}_\text{Total}}{1000} $$
$$
\# \text{ of partitions}_{\text{by size}} = \frac{\text{Total Size}}{10 GB}
$$
$$
\# \text{of partitions} = \text{ceil}(\max (\# \text{ of partitions}_{\text{by capcity}}, \# \text{ of partitions}_{\text{by size}}))
$$

- WCUs & RCUs are spread evenly across partitions

### Throttling

- If we exceed provisioned RCUs or WCUs, we get *ProvisionedThroughputExceededExceptions*
- Reasons
    - Hot Keys
    - Hot partitions
    - Very large items, remember RCU and WCU depend on item size
- Solution
    - Exponential Back-Off
    - Choose a good partition key
    - If RCU issue use DynamoDB Accelerator (DAX)

### On-Demand

- Read/Writes automatically scales up/down with your workloads
- No Capacity planning needed (WCU/RCU)
- Unlimited WCU/RCU, no throttle, more expensive
- You are charged for reads/writes that you use in terms of RRU (read request units) WRU (write request units)
- 2.5x more expensive than provisioned capacity

### Basic APIs

#### Writing

- `PutItem` : creates a new item or fully replace an old item
    - Consumes WCUs
- `UpdateItem` : Edits an existing item's attributes or adds a new items if it doesn't exist
    - Can be used to implement *Atomic Counters*
- `ConditionalWrites` : Accept a write/update/delete only if conditions are met, otherwise return error
    - Helps with concurrent access to items
    - No performance Impact

#### Reading Data

- `GetItem`
    - read based on Primary Key
    - Primary Key can be Hash or Hash + Range
    - Eventually Consistent Read (Default)
    - Option to use Strongly Consistent Reads
    - Projection Expression can be specified to retrieve only certain attributes

#### Reading Data (Query)

- `Query` returns items based on
    - *KeyConditionExpression*
        - partition key value must be `= operator` ~ required
        - sort key value could be (`=, <, <=, >, >=, Between, Begins with`) ~ optional
    - *Filter Expression*
        - additional filtering after the Query Operation (before data is returned)
        - Use only with non-key attributes
- Returns
    - The number of items specified in *Limit*
    - or up to 1MB of data
- Ability to do pagination on the results
- Can query table, a Local Secondary Index, or a Global Secondary Index

#### Reading Data (Scan)

- Scan the entire table and then filter out data (inefficient)
- Returns up to 1 MB of data – use pagination to keep on reading
- Consumes a lot of RCU
- Limit impact using Limit or reduce the size of the result and pause
- For faster performance, use Parallel Scan
    - Multiple workers scan multiple data segments at the same time
    - Increases the throughput and RCU consumed
    - Limit the impact of parallel scans just like you would for Scans
- Can use ProjectionExpression & FilterExpression (no changes to RCU)

#### Deleting Data

- DeleteItem
    - Delete an individual item
    - Ability to perform a conditional delete
- DeleteTable
    - Delete a whole table and all its items
    - Much quicker deletion than calling DeleteItem on all items
#### Batch Operations

- Allows you to save in latency by reducing the number of API calls
- Operations are done in parallel for better efficiency
- Part of a batch can fail; in which case we need to try again for the failed item
- BatchWriteItem
    - Up to 25 PutItem and/or *DeleteItem* in one call
    - Up to 16 MB of data written, up to 400 KB of data per item
    - Can’t update items (use *UpdateItem*)
    - *UnprocessedItems* for failed write operations (exponential backoff or add WCU)
- BatchGetItem
    - Return items from one or more tables
    - Up to 100 items, up to 16 MB of data
    - Items are retrieved in parallel to minimize latency
    - *UnprocessedKeys* for failed read operations (exponential backoff or add RCU)

### PartiQL

- SQL-compatible query language for DynamoDB
- Allows you to select, insert, update, and delete data in DynamoDB using SQL
- Run queries across multiple DynamoDB tables
- Run PartiQL queries from:
    - AWS Management Console
    - NoSQL Workbench for DynamoDB
    - DynamoDB APIs
    - AWS CLI
    - AWS SDK

```sql
SELECT OrderID, Total
FROM Orders
WHERE OrderID IN [1, 2, 3]
ORDER BY OrderID DESC
```

### Amazon Dynamo DB Indexes (LSI & GSI)

#### LSI (Local Secondary Index)

- Alternative Sort Key for your table (same *Partition Key* as that of base table)
- The sort key consists of one scalar attribute (String, Number, or Binary)
- Up to 5 local Secondary indexes per table
- Must be defined at the table creation time
- Attribute Projections - can contain some or all attributes of the base table

![](assets/Pasted%20image%2020251108190004.png)

#### Global Secondary Index (GSI)

- Alternative Primary Key (HASH or HASH + RANGE) from the base table
- Speed up queries on non-key attributes
- The Index key consists of scalar attributes (String, Number, or Binary)
- *Attribute Projects* - some or all the attributes of the base table (KEYS_ONLY, INCLUDE, ALL)
- Must provision RCUs & WCUs for the index
- Can be modified/added after table creation

![](assets/Pasted%20image%2020251108190215.png)

#### Indexes & Throttling

- Global Secondary Index (GSI):
    - If the writes are throttled on the GSI, then the main table will be throttled!
    - Even if the WCU on the main tables are fine
    - Choose your GSI partition key carefully!
    - Assign your WCU capacity carefully!
- Local Secondary Index (LSI):
    - Uses the WCUs and RCUs of the main table
    - No special throttling considerations

### DynamoDB DAX

- Fully-managed, highly available, seamless in-memory cache for DynamoDB
- Microseconds latency for cached reads & queries
- Doesn’t require application logic modification (compatible with existing DynamoDB APIs)
- Solves the “Hot Key” problem (too many reads)
- 5 minutes TTL for cache (default)
- Up to 10 nodes in the cluster
- Multi-AZ (3 nodes minimum recommended for production)
- Secure (Encryption at rest with KMS, VPC, IAM, CloudTrail, …)

![](assets/Pasted%20image%2020251108191604.png)

#### DAX vs ElastiCache

![](assets/Pasted%20image%2020251108191546.png)
### DynamoDB Streams

- Ordered stream of item-level modifications (create/update/delete) in a table
- Stream records can be:
    - Sent to Kinesis Data Streams
    - Read by AWS Lambda
    - Read by Kinesis Client Library applications
- Data Retention for up to 24 hours
- Use cases:
    - react to changes in real-time (welcome email to users)
    - Analytics
    - Insert into derivative tables
    - Insert into OpenSearch Service
    - Implement cross-region replication

![](assets/Pasted%20image%2020251108192312.png)

- Ability to choose the information that will be written to the stream:
    - **KEYS_ONLY** – only the key attributes of the modified item
    - **NEW_IMAGE** – the entire item, as it appears after it was modified
    - **OLD_IMAGE** – the entire item, as it appeared before it was modified
    - **NEW_AND_OLD_IMAGES** – both the new and the old images of the item
- DynamoDB Streams are made of shards, just like Kinesis Data Streams
- You don’t provision shards, this is automated by AWS
- Records are not retroactively populated in a stream after enabling it

#### DynamoDB Streams & AWS Lambda

- You need to define an *Event Source Mapping* to read from a Dynamo DB
- You need to ensure the Lambda function has appropriate permissions
- Your lambda function is invoke synchronously

![](assets/Pasted%20image%2020251108192603.png)

### DynamoDB TTL

![](assets/Pasted%20image%2020251108193542.png)

- Automatically delete items after an expiry timestamp
- Doesn’t consume any WCUs (i.e., no extra cost)
- The TTL attribute must be a “Number” data type with “Unix Epoch timestamp” value
- Expired items deleted within few days of expiration
- Expired items, that haven’t been deleted, appears in reads/queries/scans (if you don’t want them, filter them out)
- Expired items are deleted from both LSIs and GSIs
- A delete operation for each expired item enters the DynamoDB Streams (can help recover expired items)
- Use cases: reduce stored data by keeping only current items, adhere to regulatory obligations, …

### DynamoDB ~ S3 Patterns

#### Large Objects Pattern

![](assets/Pasted%20image%2020251108193635.png)

#### Indexing S3 Objects Metadata

![](assets/Pasted%20image%2020251108193658.png)


### DynamoDB ~ Security & Other Features

- Security
    - VPC Endpoints available to access DynamoDB without using the Internet
    - Access fully controlled by IAM
    - Encryption at rest using AWS KMS and in-transit using SSL/TLS
- Backup and Restore feature available
    - Point-in-time Recovery (PITR) like RDS
    - No performance impact
- Global Tables
    - Multi-region, multi-active, fully replicated, high performance
- DynamoDB Local
    - Develop and test apps locally without accessing the DynamoDB web service (without Internet)
- AWS Database Migration Service (AWS DMS) can be used to migrate to DynamoDB (from MongoDB, Oracle, MySQL, S3, …)

#### DynamoDB ~ Fine-Grained Access

- Using Web Identity Federation or Cognito Identity Pools, each user gets AWS credentials
- You can assign an IAM Role to these users with a Condition to limit their API access to DynamoDB
- LeadingKeys – limit row-level access for users on the Primary Key
- Attributes – limit specific attributes the user can see

Example Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        "Effect": "Allow" ,
        "Action": [
            "dynamodb: GetIem", "dynamodb:BatchGetItem", "dynamodb: Query" ,
            "dynamodb: PutItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem",
            "dynamodb: BatchWriteItem"
            "Resource": "arn:aws: dynamodb: us-west-2: 123456789012: table/MyTable",
        "Condition": {
            "ForAllValues:StringEquals": {
                "dynamodb: LeadingKeys": ["${cognito-identity.amazonaws.com: sub}"]
                }
            }
        }
    ]
}
```

## Amazon RDS

What is RDS ?

- Hosted relational database
    - Amazon Aurora
    - MySQL
    - PostgreSQL
    - MariaDB
    - Oracle
    - SQL Server
- Not for *big data*

### ACID

- RDS databases offer full ACID Compliance
    - Atomicity
    - Consistency
    - Isolation
    - Durability

### Amazon Aurora

- MySQL & PostgreSQL - compatible
- Up to 5X faster than MySQL, 3X faster than PostgreSQL
- 1/10 the cost of commercial databases
- Up to 128TB per database volume
- Up to 15 read replicas
- Continuous backup to S3
- Replication across regions and availability zones
- Automatic scaling with Aurora Serverless

### Aurora Security

- VPC network isolation
- At-rest with KMS
    - Data, backup, snapshots, and replicas can be encrypted
- In-transit with SSL

### Using the LOCK Command

- Relational databases implicitly “lock” tables to prevent two things writing to it at the same time, or reading while a write is in process.
- Tables or rows can also be explicitly locked to ensure data integrity and concurrency control.
- Types of locks:
    - Shared Locks: Allow reads, prevent writes. Can be held by multiple transactions. (*FOR SHARE*)
    - Exclusive Locks: Prevent all reads and writes to a resource. Only one transaction can hold an exclusive lock. (*FOR UPDATE*)

### Examples (MySQL)

- Lock an entire table:
    - `LOCK TABLES employees WRITE;` -- Locks the entire 'employees' table for write operations
    - Use `UNLOCK TABLES;` to release the lock.
    - Note: Redshift also has a LOCK command for the same purpose.
- Shared lock (allow reads, prevent other writes during this transaction.)
- `SELECT * FROM employees WHERE department = 'Finance' FOR SHARE;`
- Exclusive lock (prevent all reads and writes during this transaction)
- `SELECT * FROM employees WHERE employee_id = 123 FOR UPDATE;`
- Make sure the transactions any locks are in complete, or you could end up with a “deadlock”

### RDS Best Practices

- CloudWatch to monitor memory, CPU, storage, replica lag
- Perform automatic backups during daily low in write IOPS
- Insufficient I/O will make recovery after failure slow
- Set TTL on DNS for your DB instances to 30s or ess from your apps
- Test failover before you need it
- Provision enough RAM to include your entire working set
    - If you *ReadIOPS* metric is small & stable, you are good
- Rate limits in Amazon APIGW can be used to protect your database

### Query Optimizations in RDS

- Use indexes to accelerate SELECT statements
- Use EXPLAIN plans to identify the indexes you need
- Avoid full table scans
- Use ANALYZE TABLE periodically
- Simplify WHERE clauses
- Engine-specific optimizations
    - MySQL, MariaDB
        - Have enough RAM to hold indexes of actively used tables
        - Try to have less than 10,000 tables
        - Use InnoDB for storage engine
    - When loading data, disable DB backups and multi-AZ. Tweak various DB parameters such as maintenance_work_mem, max_wal_size, checkpoint_timeout. Disable synchronous_commit, autovacuum, and ensure tables are logged.
    - Use autovacuum
    - SQL Server
        - Use RDS DB Events to monitor failovers
        - Do not enable simple recover mode, offline mode, or read-only mode (this breaks Multi-AZ)
        - Deploy into all AZ’s
## Amazon Document DB

- Amazon implementation for MongoDB (which is NoSQL Database)
- Used to store, query and index JSON data
- Fully Managed, highly available with Replication across 3 AZ
- Document DB storage automatically grows in increments of 10GB
- Automatically scales to workloads with millions of requests/sec

## Amazon Memory DB (Redis)

- Redis-compatible, durable, in-memory database service
- Ultra-fast performance with over 160 millions requests/second
- Durable in-memory data storage with Multi-AZ transactional log
- Scale seamlessly from 10s GBs to 100s TBs of storage
- Use cases: web and mobile apps, online gaming, media streaming, …

![](assets/Pasted%20image%2020251109062704.png)
## Amazon Keyspaces (Cassandra)

- Apache *Cassandra* is an open-source NoSQL Distributed database
- A managed Apache Cassandra-compatible database service
- Serverless, Scalable, highly available, fully managed by AWS
- Automatically scale tables up/down based on the application’s traffic
- Tables are replicated 3 times across multiple AZ
- Using the Cassandra Query Language (CQL)
- Single-digit millisecond latency at any scale, 1000s of requests per second
- Capacity: On-demand mode or provisioned mode with auto-scaling
- Encryption, backup, Point-In-Time Recovery (PITR) up to 35 days
- Use cases: store IoT devices info, time-series data, …

## Amazon Neptune

![](assets/Pasted%20image%2020251109062930.png)

- Fully managed graph database
- A popular graph dataset would be a social network
    - Users have friends
    - Posts have comments
    - Comments have likes from users
    - Users share and like posts…
- Highly available across 3 AZ, with up to 15 read replicas
- Build and run applications working with highly connected datasets – optimized for these complex and hard queries
- Can store up to billions of relations and query the graph with milliseconds latency
- Highly available with replications across multiple AZs
- Great for knowledge graphs (Wikipedia), fraud detection, recommendation engines, social networking
- Supported graph query languages: Gremlin, openCypher, SPARQL

## Amazon Timestream

- Fully managed, fast, scalable, serverless time series database
- Automatically scales up/down to adjust capacity
- Store and analyze trillions of events per day
- 1000s times faster & 1/10th the cost of relational databases
- Scheduled queries, multi-measure records, SQL compatibility
- Data storage tiering: recent data kept in memory and historical data kept in a cost-optimized storage
- Built-in time series analytics functions (helps you identify patterns in your data in near real-time)
- Encryption in transit and at rest
- Use cases: IoT apps, operational applications, real-time analytics,

### Timestream Architectures

![](assets/Pasted%20image%2020251109063059.png)
## Amazon Redshift

What is Redshift ?

- fully-managed, petabyte scale data warehouse service
- 10x better performance than other DWs
    - via machine learning, massively parallel query execution, columnar storage
- Designed for OLAP, not OLTP
- Cost Effective
- SQL, ODBC, JDBC interfaces
- Scale up or down on demand
- Built-in replication & backups
- Monitoring via CloudWatch/CloudTrail

### Use Cases

- Accelerate analytics workloads
- Unified data warehouse & data lake
- Data warehouse modernization
- Analyze global sales data
- Store historical stock trade data
- Analyze ad impressions & clicks
- Aggregate gaming data
- Analyze social trends

![](assets/Pasted%20image%2020251109063411.png)

### Redshift Spectrum

- Query exabytes of unstructured data in S3 without loading
- Limitless concurrency
- Horizontal scaling
- Separate storage & compute resources
- Wide variety of data formats
- Support of Gzip and Snappy compression

### Redshift Performance

- Massively Parallel Processing (MPP)
- Columnar Data Storage
- Column Compression

### Redshift Durability

- Replication within cluster
- Backup to S3
    - Asynchronously replicated to another region
- Automated snapshots
- Failed drives / nodes automatically replaced
- However – limited to a single availability zone (AZ)
- Multi-AZ for RA3 clusters now available

### Scaling Redshift

- Vertical and horizontal scaling on demand
- During scaling:
    - A new cluster is created while your old one remains available for reads
    - CNAME is flipped to new cluster (a few minutes of downtime)
    - Data moved in parallel to new compute nodes

### Redshift Distribution Styles

- AUTO
    - Redshift figures it out based on size of data
- EVEN
    - Rows distributed across slices in round-robin
- KEY
    - Rows distributed based on one column
- ALL
    - Entire table is copied to every node

### Importing/Exporting Data

- COPY command
    - Parallelized; efficient
    - From S3, EMR, DynamoDB, remote hosts
    - S3 requires a manifest file and IAM role
- UNLOAD command
    - Unload from a table into files in S3
- Enhanced VPC routing
- Auto-copy from Amazon S3
- Amazon Aurora zero-ETL integration
    - Auto replication from Aurora -> Redshift
- Redshift Streaming Ingestion
    - From Kinesis Data Streams or MSK

### COPY Command

- Use COPY to load large amounts of data from outside of Redshift
- If your data is already in Redshift in another table,
    - Use INSERT INTO …SELECT
    - Or CREATE TABLE AS
- COPY can decrypt data as it is loaded from S3
    - Hardware-accelerated SSL used to keep it fast
- Gzip, lzop, and bzip2 compression supported to speed it up further
- Automatic compression option
    - Analyzes data being loaded and figures out optimal compression scheme for storing it
- Special case: narrow tables (lots of rows, few columns)
    - Load with a single COPY transaction if possible
    - Otherwise hidden metadata columns consume too much space

### Redshift copy grants for cross-region snapshot copies

- Let’s say you have a KMS-encrypted Redshift cluster and a snapshot of it
- You want to copy that snapshot to another region for backup
- In the destination AWS region:
    - Create a KMS key if you don’t have one already
    - Specify a unique name for your snapshot copy grant
    - Specify the KMS key ID for which you’re creating the copy grant
- In the source AWS region:
    - Enable copying of snapshots to the copy grant you just created

### DBLINK

- Connect Redshift to PostgreSQL (possibly in RDS)
- Good way to copy and sync data between PostgreSQL and Redshift

### Integration with other services

- S3
- DynamoDB
- EMR / EC2
- Data Pipeline
- Database Migration Service

### Redshift Workload Management (WLM)

- Prioritize short, fast queries vs. long, slow queries
- Query queues
- Via console, CLI, or API

### Concurrency Scaling

- Automatically adds cluster capacity to handle increase in concurrent read queries
- Support virtually unlimited concurrent users & queries
- WLM queues manage which queries are sent to the concurrency scaling cluster

### Automatic Workload Management

- Creates up to 8 queues
- Default 5 queues with even memory allocation
- Large queries (ie big hash joins) -> concurrency lowered
- Small queries (ie inserts, scans, aggregations) -> concurrency raised
- Configuring query queues
    - Priority
    - Concurrency scaling mode
    - User groups
    - Query groups
    - Query monitoring rules

### Manual Workload Management

- One default queue with concurrency level of 5 (5 queries at once)
- Superuser queue with concurrency level 1
- Define up to 8 queues, up to concurrency level 5
    - Each can have defined concurrency scaling mode, concurrency level, user groups, query groups, memory, timeout, query monitoring rules
    - Can also enable query queue hopping
        - Timed out queries “hop” to next queue to try again

### Short Query Acceleration (SQA)

- Prioritize short-running queries over longer-running ones
- Short queries run in a dedicated space, won’t wait in queue behind long queries
- Can be used in place of WLM queues for short queries
- Works with:
    - CREATE TABLE AS (CTAS)
    - Read-only queries (SELECT statements)
- Uses machine learning to predict a query’s execution time
- Can configure how many seconds is “short”

### VACUUM Command

- Recovers space from deleted rows and restores sort order
- VACUUM FULL
- VACUUM DELETE ONLY
    - Skips the sort
- VACUUM SORT ONLY
    - Does not reclaim space!
- VACUUM REINDEX
    - Re-analyzes distribution of sort key columns
    - Then does a full VACUUM

### Redshift anti-patterns

- Small data sets
    - Use RDS instead
- OLTP
    - Use RDS or Dynamo DB instead
- Unstructured data
    - ETL first with EMR etc.
- BLOB data
    - Store references to large binary files in S3, not files themselves

### Resizing Redshift Clusters

- Elastic resize
    - Quickly add or remove nodes of same type
        - (It *can* change node types, but not without dropping connections – it creates a whole new cluster)
    - Cluster is down for a few minutes
    - Tries to keep connections open across the downtime
    - Limited to doubling or halving for some dc2 and ra3 node types.
    - Classic resize
        - Change node type and/or number of nodes
        - Cluster is read-only for hours to days
    - Snapshot, restore, resize
        - Used to keep cluster available during a classic resize
        - Copy cluster, resize new cluster

### newer Redshift Features

- RA3 nodes with managed storage
    - Enable independent scaling of compute and storage
    - SSD-based
- Redshift data lake export
    - Unload Redshift query to S3 in Apache Parquet format
    - Parquet is 2x faster to unload and consumes up to 6X less storage
    - Compatible with Redshift Spectrum, Athena, EMR, SageMaker
    - Automatically partitioned
- Spatial data types
    - GEOMETRY, GEOGRAPHY
- Cross-Region Data Sharing
    - Share live data across Redshift clusters without copying
    - Requires new RA3 node type
    - Secure, across regions and across accounts

### Redshift ML

![](assets/Pasted%20image%2020251109071302.png)

### Redshift Security Concerns

- Using a Hardware Security Module (HSM)
    - Must use a client and server certificate to configure a trusted connection between Redshift and the HSM
    - If migrating an unencrypted cluster to an HSM-encrypted cluster, you must create the new encrypted cluster and then move data to it.
- Defining access privileges for user or group
    - Use the GRANT or REVOKE commands in SQL
    - Example: grant select on table foo to bob;

### Redshift Serverless

- Automatic scaling and provisioning for your workload
- Optimizes costs & performance
    - Pay only when in use
- Uses ML to maintain performance across variable & sporadic workloads
- Easy spinup of development and test environments
- Easy ad-hoc business analysis
- You get back a serverless endpoint, JDBC/ODBC connection, or just query via the console’s query editor

### Redshift Serverless

- Need an IAM role with this policy
- Define your
    - Database name
    - Admin user credentials
    - VPC
    - Encryption settings
    - AWS-owned KMS by default
    - Audit logging
- Can manage snapshots & recovery points after creation

### Resource Scaling in Redshift Serverless

- Capacity measured in Redshift Processing Units (RPU’s)
- You pay for RPU-hours (per second) plus storage
- Base RPU’s
    - You can adjust base capacity
    - Defaults to AUTO
    - But you can adjust from 32-512 RPU’s to improve query performance
- Max RPU’s
    - Can set a usage limit to control costs
    - Or, increase it to improve throughput

### Redshift Serverless

- Does everything Redshift can, except:
    - Parameter Groups
    - Workload Management
    - AWS Partner integration
    - Maintenance windows / version tracks
- No public endpoints (yet)
    - Must access within a VPC

### Redshift Serverless : Monitoring

- Monitoring views
    - SYS_QUERY_HISTORY
    - SYS_LOAD_HISTORY
    - SYS_SERVERLESS_USAGE
    - …and many more
- CloudWatch logs
    - Connection & user logs enabled by default
    - Optional user activity log data
    - Under /aws/redshift/serverless/
- CloudWatch metrics
    - QueriesCompletedPerSecond, QueryDuration, QueriesRunning,etc.
    - Dimensions: DatabaseName, latency (short/medium/long), QueryType, stage

### Redshift Materialized Views

- Contain precomputed results based on SQL queries over one or more base tables.
- This differs from a “normal” view in that it actually stores the results of the query
- Provide a way to speed up complex queries in a data warehouse environment, especially on large tables.
- You can query materialized views just like any other tables or views.
- Queries return results faster since they use precomputed results without accessing base tables.
- They're particularly beneficial for predictable and recurring queries, e.g., populating dashboards like Amazon QuickSight

### Using Materialized Views

- CREATE MATERIALIZED VIEW…
- Keeping them refreshed
    - REFRESH MATERIALIZED VIEW…
    - Set AUTO REFRESH option on creation
- Query them just like any other table or view
- Materialized views can be built from other materialized views
- Useful for re-using expensive joins

### Redshift Data Sharing

- Securely share live data across Redshift clusters for read purposes
- Why?
    - Workload isolation
    - Cross-group collaboration
    - Sharing data between dev/test/prod
    - Licensing data access in AWS Data Exchange
- Can share DB’s, schemas, tables, views, and/or UDFs.
- Fine-grained access control
- Producer / consumer architecture
    - Producer controls security
    - Isolation to ensure producer performance unaffected by consumers
    - Data is live and transactionally consistent
- Both must be encrypted, must use RA3 nodes
- Cross-region data sharing involves transfer charges
- Types of data shares
    - Standard
    - AWS Data Exchange
    - AWS Lake Formation - managed

### Redshift Lambda UDF

- Use custom functions in AWS Lambda inside SQL queries
- Using any language you want!
    - Do anything you want!
        - Call other services (AI?)
        - Access external systems
        - Integrate with location service
- Register with CREAT EXTERNAL FUNCTION
- Must GRANT USAGE ON LANGUAGE EXFUNC for permissions
- Redshift communicates with Lambda using JSON


### Redshift Federated Queries

![](assets/Pasted%20image%2020251109072738.png)

- Query and analyze across databases, warehouses, and lakes
- Ties Redshift to Amazon RDS or Aurora for PostgreSQL and MySQL
    - Incorporate live data in RDS into your Redshift queries
    - Avoids the need for ETL pipelines
- Offloads computation to remote databases to reduce data movement
- Must establish connectivity between your Redshift cluster and RDS / Aurora
    - Put them in the same VPC subnet
    - Or use VPC peering
- Credentials must be in AWS Secrets Manager
- Include secrets in IAM role for your Redshift cluster
- Connect using CREATE EXTERNAL SCHEMA
- Can also connect to S3 / Redshift Spectrum this way
- The SVV_EXTERNAL_SCHEMAS view contains available external schemas
- Read-only access to external data sources
- Costs will be incurred on external DB’s
- You can query RDS/Aurora from Redshift, but not the other way around


### Redshift Systems Tables & Views

- Contains info about how Redshift is functioning
- Types of system tables / views
    - SYS views: Monitor query & workload usage
    - STV tables: Transient data containing snapshots of current system data
    - SVV views: metadata about DB objects that reference STV tables
    - STL views: Generated from logs persisted to disk
    - SVCS views: Details about queries on main & concurrency scaling clusters
    - SVL views: Details about queries on main clusters
- Many system monitoring views & tables are only for provisioned clusters, not serverless

### Redshift Data API

![](assets/Pasted%20image%2020251109073032.png)

- Secure HTTP endpoint for SQL statements to Redshift clusters
    - Provisioned or serverless
    - Individual or batch queries
- Asynchronous
- Does not require managing connections
- No drivers needed
- Passwords not sent via API
- Uses AWS Secrets Manager or temporary credentials
- Can be invoked by AWS SDK
- C++, Go, Java, JavaScript, .NET, Node.js, PHP, Python, Ruby
- AWS CloudTrail captures API calls

### Use Cases of Data API

![](assets/Pasted%20image%2020251109073217.png)

- Application integration
    - REST endpoints
- It can also integrate with a variety of other services
    - ETL Orchestration with AWS Step Functions
        - Serverless data processing workflows
        - Event-driven ETL
    - Access from SageMaker notebooks
- Use with Amazon EventBridge
    - Stream data from application to Lambda
        - Set WithEvent parameter to true
    - Schedule Data API operations

### Important Point for Redshift APIs

- Maximum…
    - Query duration: 24 hours
    - Active queries: 500
    - Query result size (gzip’ed): 100 MB
    - Result retention time: 24 hours
    - Query statement size: 100 KB
    - Packet for query (data per row) : 64 KB
    - Client token retention time: 8 hours
    - Transaction per Second quotas per API (30 for ExecuteStatement)
- API Calls
    - ExecuteStatement, BatchExecuteStatement
    - DescribeStatement, DescribeTable
    - GetStatementResult, CancelStatement
    - Users must have same IAM role or permissions to operate on a given statement
- Cluster must be in a VPC