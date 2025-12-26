# Databases & Storage

## Database Fundamentals

**Definition**: A database is an organized collection of data that can be easily accessed, managed, and updated.

### Why Databases Matter in System Design

- **Most important component** of any system
- **Single source of truth** for application state
- **Bottleneck** in most systems at scale
- **Expensive to change** once system is in production

### Key Database Characteristics

- **Persistence**: Data survives system restarts
- **Concurrency**: Multiple users accessing simultaneously
- **Consistency**: Data integrity maintained
- **Performance**: Fast read/write operations
- **Scalability**: Handles growing data and load

## ACID Properties (Relational Databases)

### Atomicity

**Definition**: All operations in a transaction succeed or fail together - no partial updates.

```sql
-- Example: Bank transfer (atomic operation)
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'A';
UPDATE accounts SET balance = balance + 100 WHERE account_id = 'B';
COMMIT; -- Both updates happen or neither happens
```

**Real-world Example**:

- E-commerce order: Update inventory, charge payment, create shipping record
- Either all succeed or all fail (no partial orders)

**Implementation**:

- Write-ahead logging (WAL)
- Transaction rollback on failure
- Two-phase commit for distributed transactions

### Consistency

**Definition**: Database maintains data integrity rules and constraints.

- `C` in ACID is not same as one in CAP Theorem.
- C is more like a term thrown around to make the acronym work. It defines that data will always move from one consistent state to another.
- Defn : Data will never go incorrect, no matter what. Constraint, Cascades, Triggers ensure above property and bring data back in consistent state.
- Example - In a Financial system, all the debits must add up to equal to credits. 

```sql
-- Consistency example: Foreign key constraints
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT REFERENCES users(id), -- Ensures valid user
    total DECIMAL CHECK (total > 0)   -- Ensures positive total
);
```

**Types of Consistency**:

- **Entity Integrity**: Primary keys are unique and not null
- **Referential Integrity**: Foreign keys reference valid records
- **Domain Integrity**: Data values are valid (e.g., positive prices)
- **User-defined Integrity**: Custom business rules

### Isolation

**Definition**: Concurrent transactions don't interfere with each other.

- when multiple transactions are executing parallely, the *isolation level* determines how much changes of one trasactions are visible to other.
- Serializable ? Effect of all txn is as if they have executed serially. In Comparch people realised it was little slow they fiddled around locks to figure out to make it work fast.

#### Isolation Levels (Weakest to Strongest)

##### Read Uncommitted

- Transaction 1 can see uncommitted changes from Transaction 2
- Allows: Dirty reads, non-repeatable reads, phantom reads

**Use Case**: Analytics queries where approximate data is acceptable

##### Read Committed (Most Common)

* Only sees committed changes from other transactions, always read fresh values.
* Prevents: Dirty reads
* Allows: Non-repeatable reads, phantom reads
* Cons : Multiple reads withing same transaction are inconsistent

**Use Case**: Most OLTP applications

##### Repeatable Read

- Same read query returns same results within transaction
- Prevents: Dirty reads, non-repeatable reads
- Allows: Phantom reads
- It guarantees : both dirty reads and dirty writes never happen.

**Use Case**: Reports that need consistent data throughout, default in Postgres, Oracle, SQL Server

##### Serializable

- Every read is a locking read (depends on engine) and while one txn reads, other will have to wait
- Transactions appear to run sequentially
- Prevents: All read phenomena
- Highest isolation but lowest performance

**Use Case**: Financial systems requiring strict consistency

### Durability

**Definition**: Committed changes survive system failures.

- When archive tapes were used, you can restore database back from its initial state to final state using archives.

**Implementation Mechanisms**:

- **Write-Ahead Logging (WAL)**: Log changes before applying
- **Checkpoints**: Periodic saves of database state
- **Backup and Recovery**: Point-in-time restore capability
### SQL vs NoSQL Trade-Offs

### SQL Databases (RDBMS)

#### Strengths

- **ACID Compliance**: Strong consistency guarantees
- **Complex Queries**: Joins, aggregations, subqueries
- **Mature Ecosystem**: Tools, expertise, documentation
- **Standardized Language**: SQL is widely known
- **Data Integrity**: Foreign keys, constraints, triggers

#### Weaknesses

- **Vertical Scaling**: Limited horizontal scale
- **Schema Rigidity**: Difficult to change schema
- **Performance**: Complex queries can be slow
- **Fixed Structure**: Requires predefined schema

#### Popular SQL Databases

- PostgreSQL: Full-featured, extensible, JSON support
- MySQL: Fast, widely used, good for web applications
- Oracle: Enterprise features, high performance
- SQL Server: Microsoft ecosystem, enterprise features
- SQLite: Embedded, serverless, zero-configuration

### NoSQL Databases

#### Document Databases

```json
// MongoDB example - flexible schema
{
  "_id": "user123",
  "name": "John Doe",
  "email": "john@example.com",
  "preferences": {
    "theme": "dark",
    "notifications": true
  },
  "tags": ["premium", "early-adopter"]
}
```

**Strengths**:

- Schema flexibility
- Natural object mapping
- Horizontal scaling
- JSON-like documents

**Examples**: MongoDB, CouchDB, Amazon DocumentDB **Use Cases**: Content management, catalogs, user profiles

#### Key-Value Stores

```python
# Redis example - simple operations
redis.set("user:123:session", "abc123", ex=3600)  # Set with expiration
redis.get("user:123:session")  # Fast retrieval
redis.incr("page:views")  # Atomic increment
```

**Strengths**:

- Extremely fast
- Simple operations
- High throughput
- Easy to scale

**Examples**: Redis, DynamoDB, Riak **Use Cases**: Caching, session storage, real-time recommendations

#### Column-Family

```
// Cassandra example - wide rows
RowKey: user123
  profile:name -> "John Doe"
  profile:email -> "john@example.com"
  activity:2023-01-01 -> "login"
  activity:2023-01-02 -> "purchase"
```

**Strengths**:

- Time-series data
- High write throughput
- Compression
- Distributed by design

**Examples**: Cassandra, HBase, Amazon SimpleDB **Use Cases**: IoT data, time-series, analytics

#### Graph Databases

```cypher
// Neo4j example - relationships are first-class
CREATE (user:Person {name: "Alice"})
CREATE (product:Product {name: "iPhone"})
CREATE (user)-[:PURCHASED]->(product)
CREATE (user)-[:FRIENDS_WITH]->(other_user)
```

**Strengths**:

- Complex relationships
- Graph algorithms
- Pattern matching
- Traversal queries

**Examples**: Neo4j, Amazon Neptune, ArangoDB **Use Cases**: Social networks, fraud detection, recommendations
## Database Replication Patterns

### Master-Slave Replication (primary-replica)

![](assets/Pasted%20image%2020251224115325.png)

**Advantages**:

- Simple to implement
- Good read scalability
- Clear separation of concerns

**Disadvantages**:

- Single point of failure (master)
- Write bottleneck
- Replication lag

**Use Cases**: Read-heavy applications (90:10 read:write ratio)

### Master-Master Replication (Multi-Master)

![](assets/Pasted%20image%2020251224115725.png)


**Advantages**:

- No single point of failure
- Better write scalability
- Geographic distribution

**Disadvantages**:

- Complex conflict resolution : Last-write wins or merge at application level.
- Consistency challenges
- More complex setup
### Replication Strategies

#### Synchronous Replication

- Changes are immediately reflected in replicas

**Pros**: Strong consistency, zero data loss 

**Cons**: Higher latency, availability issues

#### Asynchronous Replication

- Changes are sent to replicas, assuming that they will reflect master db eventually.

**Pros**: Lower latency, better availability 

**Cons**: Replication lag, potential data loss

#### Semi-Synchronous Replication

- Wait for at-least one of the replica to confirm replication

**Pros**: Balance of consistency and performance

**Cons**: More complex implementation

## Database Partitioning & Sharding


![](../../hld/beginner/assets/Pasted%20image%2020251221193317.png)

![](../../hld/beginner/assets/Pasted%20image%2020251221193850.png)
### Partitioning (Within Single Instance)

- It could be of two types
    - Horizontal Partition : Where we divide the data based on ranges of rows.
    - Vertical Partitioning : Divide data into set of frequently accessed data (user_id, name, email, etc.) and in-frequently accessed data (e.g. address, date of birth, etc.)

### Sharding (Across Multiple Instances)

We can shard on based on multiple criteria.

- Range-Based Sharding
    - **Pros**: Simple range queries, easy to add new shards
    - **Cons**: Hotspots, uneven distribution
- Hash-Based Sharding
    - **Pros**: Even distribution, no hotspots
    - **Cons**: Range queries difficult, re-sharding complex
- Directory-Based Sharding
    - **Pros**: Flexible, easy migration
    - **Cons**: Additional complexity, lookup overhead

Most Challenging problems in Sharding are

- Cross-Shard Queries
- Rebalancing Shards

A few solution help us in this

- Denormalization: Store frequently accessed data together
- Application-level joins
- Distributed query engines
## ACID vs BASE Properties

### ACID (Traditional RDBMS)

- **Atomicity**: All or nothing transactions
- **Consistency**: Data integrity maintained
- **Isolation**: Transactions don't interfere
- **Durability**: Changes survive failures

### BASE (NoSQL Systems)

- **Basically Available**: System remains operational
- **Soft State**: Data may change over time
- **Eventual Consistency**: System becomes consistent eventually

| Property     | ACID                          | BASE                       |
| ------------ | ----------------------------- | -------------------------- |
| Consistency  | Strong, immediate             | Eventual, Flexible         |
| Availability | May sacrifice for consistency | High Availability Priority |
| Performance  | Maybe slower due to overhead  | Generally Faster           |
| Complexity   | Comple Transaction management | Simpler Operation          |
| Use Cases    | Financial, Critical Data      | Social Media, Analytics    |

### Consistency Models

- There are 3 types of Consistency Model
    - Strong : Data immediately becomes consistent
    - Eventual : eventually data becomes consistent
    - Causal : Related Operation are seen in order using vector clocks.

## How to Choose a DB for your application ?

Ideally if its a very small application, you can default to options like PostgreSQL, Dynamo DB or Mongo DB for bigger applications, you will need specialized databases

Key Question to ask for Database Selections

- What is the data model ? options could be SQL, document (semi-structured), key-value or relationship (graph)
- What are consistency requirements ?
- What is expected size or scale of database ? options here size (GB, TB, PB), query Volume (QPS), Geographic Location, etc.
- What are performance requirements ? latency (ms), throughput (ops/s), availability, etc.

Common Databases Pattern based on Use Cases are as following

**Domain : E-Commerce Platform**

- Users, Orders, Inventory : PostgreSQL (ACID transactions)
- Product Catalog: Elastic-Search (search)
- Shopping Cart: Redis (session data)
- Recommendations: Neo4j (graph relationships)
- Analytics: BigQuery (data warehouse)

**Social Media Platform**

- User Profiles: MongoDB (flexible schema)
- Posts/Feed: Cassandra (time-series)
- Real-time Chat: Redis (pub/sub)
- Friend Relationships: Neo4j (graph)
- Media Storage: S3 + CDN

**IoT Platform**

- Sensor Data: InfluxDB (time-series)
- Device Metadata: MongoDB (documents)
- Real-time Processing: Apache Kafka
- Analytics: Apache Spark + Parquet
- Configuration: Redis (key-value)

**Database Selection Cheat Sheet**

- Strong Consistency + Transactions = PostgreSQL/MySQL
- High Performance + Simple Operations = Redis/DynamoDB  
- Flexible Schema + Complex Queries = MongoDB
- Relationships + Graph Algorithms = Neo4j
- Analytics + Large Data = BigQuery/Redshift
- Time-series Data = InfluxDB/TimescaleDB
- Full-text Search = Elasticsearch

## Common Database Anti-patterns

### The God Table

```sql
-- Anti-pattern: Everything in one table
CREATE TABLE users (
    id INT,
    name VARCHAR(100),
    email VARCHAR(100),
    address TEXT,
    billing_info TEXT,
    preferences JSON,
    activity_log TEXT,
    -- ... 50+ more columns
);
```

**Solution**: Normalize into related tables

### Fear of Joins

```python
# Anti-pattern: Avoiding joins leads to N+1 queries
def get_user_posts(user_id):
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    posts = []
    for post_id in user.post_ids.split(','):  # N+1 problem
        post = db.query("SELECT * FROM posts WHERE id = ?", post_id)
        posts.append(post)
    return posts
```

**Solution**: Use appropriate joins or batch queries

### Premature Sharding

* Start with single instance first
* If current load exceeds threshold scale and implement sharding

## Common Questions


- How would you scale a database that's reaching its limits?
    - Start with read replicas
    - Consider caching strategies
    - Vertical scaling first, then horizontal
    - Eventually move to sharding
- When would you choose NoSQL over SQL ?
    - Rapid development with changing schema
    - Need for horizontal scaling
    - Specific data models (document, graph)
    - Eventual consistency is acceptable
- How do you handle database failures?
    - Replication for redundancy
    - Automated failover
    - Regular backups
    - Health monitoring
- Explain the CAP theorem and its implications
    - Consistency, Availability, Partition tolerance
    - Can only guarantee two of three
    - Real-world trade-offs