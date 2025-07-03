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

```python
# Conceptual durability implementation
def commit_transaction(transaction):
    # 1. Write to log first
    write_to_log(transaction.changes)
    sync_log_to_disk()  # Force write to disk
    
    # 2. Apply changes to database
    apply_changes(transaction.changes)
    
    # 3. Mark transaction as committed
    mark_committed(transaction.id)
```

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

```
PostgreSQL: Full-featured, extensible, JSON support
MySQL: Fast, widely used, good for web applications
Oracle: Enterprise features, high performance
SQL Server: Microsoft ecosystem, enterprise features
SQLite: Embedded, serverless, zero-configuration
```

#### Best Use Cases

- **Financial Systems**: Banking, accounting (need ACID)
- **E-commerce**: Inventory, orders, payments
- **CRM Systems**: Customer relationships, sales data
- **Traditional Web Apps**: User management, content

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

### Detailed Comparison

| Aspect          | SQL                      | NoSQL                       |
| --------------- | ------------------------ | --------------------------- |
| Schema          | Fixed, predefined        | Flexible, dynamic           |
| Scaling         | Vertical (Scale Up)      | Horizontal (scale out)      |
| Consistency     | Strong (Acid)            | Eventual (BASE)             |
| Query Language  | Standardized SQL         | Database-specific           |
| Transactions    | Full ACID support        | Limited or Eventual         |
| Join Operation  | Efficient                | Limited or None             |
| Learning Curve  | Moderate                 | Varies by Type              |
| Data Structures | Tables with rows/columns | Documents, key-value, graph |

## Database Replication Patterns

### Master-Slave Replication (primary-replica)

````text
[Application]
         |
    [Load Balancer]
    /             \
[Write to Master] [Read from Slave]
    |                    |
[Master DB] ---------> [Slave DB]
            Replication
````

**How it Works**:

1. All writes go to master
2. Master replicates changes to slaves
3. Reads distributed across slaves
4. Slaves are read-only

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

````text
[App Instance 1] --> [Master DB 1] <---> [Master DB 2] <-- [App Instance 2]
                         |                    |
                         v                    v
                   [Slave DB 1]        [Slave DB 2]
````

**How it Works**:

1. Multiple masters accept writes
2. Masters replicate to each other
3. Each master can have slaves for reads

**Advantages**:

- No single point of failure
- Better write scalability
- Geographic distribution

**Disadvantages**:

- Complex conflict resolution
- Consistency challenges
- More complex setup

````python
# Last-write-wins strategy
def resolve_conflict(record1, record2):
    if record1.timestamp > record2.timestamp:
        return record1
    return record2

# Application-level resolution
def merge_user_profile(profile1, profile2):
    merged = {}
    merged['name'] = profile2['name']  # Latest name wins
    merged['preferences'] = {**profile1['preferences'], **profile2['preferences']}
    return merged
````

### Replication Strategies

#### Synchronous Replication

```python
def synchronous_write(data):
    # Write to master
    master.write(data)
    
    # Wait for all slaves to acknowledge
    for slave in slaves:
        slave.write(data)
        wait_for_ack(slave)
    
    return "Write successful"
```

**Pros**: Strong consistency, zero data loss **Cons**: Higher latency, availability issues

#### Asynchronous Replication

```python
def asynchronous_write(data):
    # Write to master immediately
    master.write(data)
    
    # Queue replication to slaves
    for slave in slaves:
        replication_queue.enqueue(slave, data)
    
    return "Write successful"  # Don't wait for slaves
```

**Pros**: Lower latency, better availability **Cons**: Replication lag, potential data loss

#### Semi-Synchronous Replication

```python
def semi_synchronous_write(data):
    # Write to master
    master.write(data)
    
    # Wait for at least one slave to acknowledge
    wait_for_ack(primary_slave)
    
    # Asynchronously replicate to other slaves
    for slave in other_slaves:
        replication_queue.enqueue(slave, data)
    
    return "Write successful"
```

**Pros**: Balance of consistency and performance **Cons**: More complex implementation

## Database Partitioning & Sharding

### Partitioning (Within Single Instance)

#### Horizontal Partitioning

```sql
-- Partition users table by age
CREATE TABLE users_young (
    id INT,
    name VARCHAR(100),
    age INT
) CHECK (age < 25);

CREATE TABLE users_adult (
    id INT,
    name VARCHAR(100),
    age INT
) CHECK (age >= 25 AND age < 65);

CREATE TABLE users_senior (
    id INT,
    name VARCHAR(100),
    age INT
) CHECK (age >= 65);
```

#### Vertical Partitioning

```sql
-- Split user data into frequently vs rarely accessed columns
CREATE TABLE users_core (
    id INT PRIMARY KEY,
    email VARCHAR(100),
    name VARCHAR(100),
    created_at TIMESTAMP
);

CREATE TABLE users_profile (
    user_id INT REFERENCES users_core(id),
    bio TEXT,
    profile_image_url VARCHAR(200),
    last_login TIMESTAMP
);
```

### 5.2 Sharding (Across Multiple Instances)

#### Range-Based Sharding

```python
class RangeShardRouter:
    def __init__(self):
        self.shards = {
            'shard1': {'min': 0, 'max': 1000000},
            'shard2': {'min': 1000001, 'max': 2000000},
            'shard3': {'min': 2000001, 'max': 3000000}
        }
    
    def get_shard(self, user_id):
        for shard_name, range_config in self.shards.items():
            if range_config['min'] <= user_id <= range_config['max']:
                return shard_name
        raise ValueError("No shard found for user_id")
```

**Pros**: Simple range queries, easy to add new shards **Cons**: Hotspots, uneven distribution

#### Hash-Based Sharding

```python
import hashlib

class HashShardRouter:
    def __init__(self, shard_count):
        self.shard_count = shard_count
    
    def get_shard(self, user_id):
        hash_value = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16)
        return f"shard_{hash_value % self.shard_count}"
```

**Pros**: Even distribution, no hotspots **Cons**: Range queries difficult, resharding complex

#### Directory-Based Sharding

```python
class DirectoryShardRouter:
    def __init__(self):
        # Lookup service maps entities to shards
        self.directory = {
            'user_1': 'shard_1',
            'user_2': 'shard_2',
            'user_3': 'shard_1'
        }
    
    def get_shard(self, user_id):
        return self.directory.get(f'user_{user_id}')
    
    def migrate_user(self, user_id, new_shard):
        self.directory[f'user_{user_id}'] = new_shard
```

**Pros**: Flexible, easy migration **Cons**: Additional complexity, lookup overhead

### 5.3 Sharding Challenges

#### Cross-Shard Queries

```python
def get_user_posts_across_shards(user_id):
    results = []
    # Query all shards - expensive!
    for shard in all_shards:
        shard_results = shard.query(f"SELECT * FROM posts WHERE user_id = {user_id}")
        results.extend(shard_results)
    
    # Merge and sort results
    return sorted(results, key=lambda x: x['created_at'], reverse=True)
```

**Solutions**:

- Denormalization: Store frequently accessed data together
- Application-level joins
- Distributed query engines

#### Rebalancing Shards

```python
def rebalance_shards():
    # Monitor shard sizes
    shard_sizes = get_shard_sizes()
    
    # Identify overloaded shards
    overloaded = [s for s in shard_sizes if s['size'] > threshold]
    
    # Split or migrate data
    for shard in overloaded:
        if can_split(shard):
            split_shard(shard)
        else:
            migrate_data(shard, find_target_shard())
```

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

### Detailed Comparison

| Property     | ACID                          | BASE                       |
| ------------ | ----------------------------- | -------------------------- |
| Consistency  | Strong, immediate             | Eventual, Flexible         |
| Availability | May sacrifice for consistency | High Availability Priority |
| Performance  | Maybe slower due to overhead  | Generally Faster           |
| Complexity   | Comple Transaction management | Simpler Operation          |
| Use Cases    | Financial, Critical Data      | Social Media, Analytics    |

### Consistency Models

#### Strong Consistency

```python
# All nodes see the same data at the same time
def write_with_strong_consistency(key, value):
    # Write to all replicas synchronously
    for replica in all_replicas:
        replica.write(key, value)
        wait_for_ack(replica)
    return "Write successful"
```

#### Eventual Consistency

```python
# System becomes consistent over time
def write_with_eventual_consistency(key, value):
    # Write to one replica immediately
    primary_replica.write(key, value)
    
    # Asynchronously propagate to others
    for replica in other_replicas:
        async_queue.enqueue(replica, key, value)
    
    return "Write successful"
```

#### Causal Consistency

```python
# Causally related operations are seen in order
def causal_write(key, value, depends_on=None):
    if depends_on:
        wait_for_dependency(depends_on)
    
    write_with_vector_clock(key, value)
```

## Database Selection Criteria

### Key Questions for Database Selection

1. What is your data model?
   - Structured (SQL)
   - Semi-structured (Document)
   - Key-value pairs (KV Store)
   - Relationships (Graph)
2. What are your consistency requirements?
   - Strong consistency (ACID)
   - Eventual consistency (BASE)
   - Session consistency
3. What is your expected scale?
   - Data size (GB, TB, PB)
   - Query volume (QPS)
   - Geographic distribution
4. What are your performance requirements?
   - Latency (milliseconds)
   - Throughput (operations/second)
   - Availability (99.9%, 99.99%)

### Common Database Patterns by Use Case

#### E-commerce Platform

```
Users, Orders, Inventory: PostgreSQL (ACID transactions)
Product Catalog: Elasticsearch (search)
Shopping Cart: Redis (session data)
Recommendations: Neo4j (graph relationships)
Analytics: BigQuery (data warehouse)
```

#### Social Media Platform

```
User Profiles: MongoDB (flexible schema)
Posts/Feed: Cassandra (time-series)
Real-time Chat: Redis (pub/sub)
Friend Relationships: Neo4j (graph)
Media Storage: S3 + CDN
```

#### IoT Platform

```
Sensor Data: InfluxDB (time-series)
Device Metadata: MongoDB (documents)
Real-time Processing: Apache Kafka
Analytics: Apache Spark + Parquet
Configuration: Redis (key-value)
```

## Advanced Database Concepts

### 8.1 NewSQL Databases

**Goal**: Combine ACID properties with horizontal scalability

```
Examples:
- CockroachDB: Distributed SQL with ACID
- TiDB: MySQL-compatible distributed database
- Spanner: Google's globally distributed database
- YugabyteDB: PostgreSQL-compatible distributed SQL
```

### 8.2 Polyglot Persistence

**Concept**: Use different databases for different parts of your application

```python
class DataService:
    def __init__(self):
        self.user_db = PostgreSQL()      # User accounts (ACID)
        self.session_cache = Redis()     # Session data (fast access)
        self.catalog_db = MongoDB()      # Product catalog (flexible)
        self.analytics_db = BigQuery()   # Analytics (aggregations)
    
    def create_user(self, user_data):
        return self.user_db.insert(user_data)
    
    def get_session(self, session_id):
        return self.session_cache.get(session_id)
    
    def search_products(self, query):
        return self.catalog_db.search(query)
```

### Database Monitoring and Metrics

**Key Metrics to Monitor**:

- **Performance**: Query latency, throughput
- **Availability**: Uptime, replication lag
- **Resource Usage**: CPU, memory, disk, connections
- **Business Metrics**: Transaction success rate

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

## Interview Tips and Common Questions

### Common Interview Questions

1. "How would you scale a database that's reaching its limits?"
   - Start with read replicas
   - Consider caching strategies
   - Vertical scaling first, then horizontal
   - Eventually move to sharding
2. "When would you choose NoSQL over SQL?"
   - Rapid development with changing schema
   - Need for horizontal scaling
   - Specific data models (document, graph)
   - Eventual consistency is acceptable
3. "How do you handle database failures?"
   - Replication for redundancy
   - Automated failover
   - Regular backups
   - Health monitoring
4. "Explain the CAP theorem and its implications"
   - Consistency, Availability, Partition tolerance
   - Can only guarantee two of three
   - Real-world trade-offs

### Key Points to Remember

- **No perfect database**: Every choice involves trade-offs
- **Start simple**: Use what you know, optimize later
- **Measure everything**: Monitor performance and usage
- **Plan for growth**: Consider future scaling needs
- **Consistency matters**: Understand your consistency requirements

### Database Selection Cheat Sheet

```
Strong Consistency + Transactions = PostgreSQL/MySQL
High Performance + Simple Operations = Redis/DynamoDB  
Flexible Schema + Complex Queries = MongoDB
Relationships + Graph Algorithms = Neo4j
Analytics + Large Data = BigQuery/Redshift
Time-series Data = InfluxDB/TimescaleDB
Full-text Search = Elasticsearch
```