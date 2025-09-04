# Scability Patterns

*The ability of a system to handle increasing amounts of work by adding resources to the system.*

## Overview

Scalability is the capability of a system to handle a growing amount of work or its potential to accommodate growth. There are two main approaches to scaling:

- **Horizontal Scaling (Scale Out)**: Adding more machines to the resource pool
- **Vertical Scaling (Scale Up)**: Adding more power (CPU, RAM) to existing machines

## Horizontal Scaling

#### What is Horizontal Scaling?

Horizontal scaling involves adding more servers to your existing pool of servers to handle increased load. It's also known as "scaling out".

#### Key Characteristics

- **Distributed Load**: Work is distributed across multiple machines
- **Linear Growth**: Can theoretically scale infinitely by adding more nodes
- **Fault Tolerance**: Failure of one node doesn't bring down the entire system
- **Geographic Distribution**: Can place servers closer to users globally

### Stateless Application Design

**Definition**: Applications that don't store client data between requests. Each request contains all information needed to process it.

#### Benefits of Stateless Design

- **Easy to Scale**: Any server can handle any request
- **Load Distribution**: Simple to distribute load across multiple servers
- **Fault Tolerance**: Server failures don't affect user sessions
- **Caching Friendly**: Responses can be cached effectively

#### Implementation Strategies

**Example: Stateless vs Stateful**

````python
# Stateful Design (Avoid)
class StatefulCounter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        return self.count

# Stateless Design (Preferred)
class StatelessCounter:
    def increment(self, current_count):
        return current_count + 1
    
    def get_count_from_db(self, user_id):
        # Fetch from database/cache
        return database.get_count(user_id)
````

**Best Practices**:

- Store session data in external stores (Redis, database)
- Use immutable data structures
- Avoid server-side session storage
- Design APIs to be idempotent

### Session Management

Managing user sessions in a horizontally scaled environment requires careful consideration.

#### Sticky Sessions (Session Affinity)

**How it Works**: Load balancer routes all requests from a user to the same server.

**Pros**:

- Simple to implement
- No need to share session data
- Good performance for session-heavy applications

**Cons**:

- Uneven load distribution
- Single point of failure for user sessions
- Difficult to scale down
- Hot spotting issues

````nginx
# Example: Sticky session configuration (NGINX)
"""
upstream backend {
    ip_hash;  # Routes based on client IP
    server server1.example.com;
    server server2.example.com;
    server server3.example.com;
}
"""
````

#### Shared Storage Sessions

**How it Works**: Session data is stored in a shared, external storage system.

**Storage Options**:

- **Redis/Memcached**: Fast, in-memory storage
- **Database**: Persistent but slower
- **Distributed Cache**: Scalable and fault-tolerant

Example of redis database

````python
# Example: Redis session storage
import redis
import json
from flask import Flask, session

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class RedisSessionManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.session_timeout = 3600  # 1 hour
    
    def set_session(self, session_id, data):
        session_data = json.dumps(data)
        self.redis.setex(
            f"session:{session_id}", 
            self.session_timeout, 
            session_data
        )
    
    def get_session(self, session_id):
        data = self.redis.get(f"session:{session_id}")
        return json.loads(data) if data else None
    
    def delete_session(self, session_id):
        self.redis.delete(f"session:{session_id}")

# Usage example
session_manager = RedisSessionManager(redis_client)
````

**Pros**:

- True load balancing
- Server failures don't affect sessions
- Easy to scale horizontally
- Centralized session management

**Cons**:

- Additional network latency
- External dependency
- More complex implementation

### Auto-scaling Strategies

**Definition**: Automatically adjusting the number of servers based on current demand.

#### Types of Auto-scaling

1. Reactive Auto-scaling

- Scale based on current metrics (CPU, memory, request count)
- Responds to load after it occurs

2. Predictive Auto-scaling

- Scale based on predicted future demand
- Uses historical data and machine learning

3. Scheduled Auto-scaling

- Scale based on known patterns (time of day, day of week)
- Useful for predictable traffic patterns

#### Auto-scaling Considerations

- **Warm-up Time**: New instances need time to start
- **Cool-down Period**: Prevent thrashing between scale events
- **Health Checks**: Ensure new instances are ready before routing traffic
- **Graceful Shutdown**: Handle existing connections during scale-in

## Vertical Scaling

### What is Vertical Scaling?

Vertical scaling involves adding more power (CPU, RAM, storage) to existing machines. It's also known as "scaling up."

### Resource Optimization

**CPU Optimization**:

- Profile application to identify bottlenecks
- Optimize algorithms and data structures
- Use efficient programming practices
- Implement proper caching strategies

**Memory Optimization**:

- Reduce memory footprint
- Implement proper garbage collection
- Use memory-efficient data structures
- Monitor memory leaks

### Performance Tuning

**Database Performance**:

- Optimize queries and add proper indexes
- Use connection pooling
- Implement query caching
- Monitor slow queries

````python
# Example: Database connection pooling
import sqlite3
from contextlib import contextmanager
import threading
import queue

class ConnectionPool:
    def __init__(self, database_path, max_connections=5):
        self.database_path = database_path
        self.max_connections = max_connections
        self.pool = queue.Queue(maxsize=max_connections)
        self.lock = threading.Lock()
        
        # Initialize connections
        for _ in range(max_connections):
            conn = sqlite3.connect(database_path, check_same_thread=False)
            self.pool.put(conn)
    
    @contextmanager
    def get_connection(self):
        conn = self.pool.get()
        try:
            yield conn
        finally:
            self.pool.put(conn)

# Usage
db_pool = ConnectionPool('example.db')

def fetch_user(user_id):
    with db_pool.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
````

**Application Performance**:

- Use profiling tools
- Implement efficient algorithms
- Reduce I/O operations
- Use asynchronous programming where appropriate

### Scaling Limitations

**Physical Limits**:

- Maximum CPU cores and RAM capacity
- Storage I/O limitations
- Network bandwidth constraints

**Cost Implications**:

- Exponential cost increase for high-end hardware
- Diminishing returns on performance gains
- Vendor lock-in for specialized hardware

**Single Point of Failure**:

- Entire application depends on one machine
- Hardware failure affects entire system
- Maintenance requires downtime

**When to Choose Vertical Scaling**:

- Simple applications with predictable load
- Legacy applications difficult to distribute
- Applications requiring shared state
- Cost-effective for small to medium scale

## Data Scaling

### Overview

As applications grow, databases often become the primary bottleneck. Data scaling strategies help distribute database load and improve performance.

### Read Replicas

**Definition**: Creating read-only copies of the primary database to distribute read traffic.

#### How Read Replicas Work

1. **Master-Slave Setup**: One primary (master) database handles writes
2. **Replication**: Changes are replicated to slave databases
3. **Read Distribution**: Read queries are distributed across replicas

````python
# Example: Database router for read replicas
import random
from enum import Enum

class DatabaseOperation(Enum):
    READ = "read"
    WRITE = "write"

class DatabaseRouter:
    def __init__(self, master_config, replica_configs):
        self.master_config = master_config
        self.replica_configs = replica_configs
        self.replica_weights = [1] * len(replica_configs)  # Equal weights
    
    def get_connection(self, operation_type):
        if operation_type == DatabaseOperation.WRITE:
            return self._connect_to_master()
        else:
            return self._connect_to_replica()
    
    def _connect_to_master(self):
        # Connect to master database
        return Database(self.master_config)
    
    def _connect_to_replica(self):
        # Weighted random selection of replica
        replica_config = random.choices(
            self.replica_configs, 
            weights=self.replica_weights
        )[0]
        return Database(replica_config)

class Database:
    def __init__(self, config):
        self.config = config
        # Database connection logic here

# Usage example
router = DatabaseRouter(
    master_config={'host': 'master-db', 'port': 5432},
    replica_configs=[
        {'host': 'replica1-db', 'port': 5432},
        {'host': 'replica2-db', 'port': 5432},
        {'host': 'replica3-db', 'port': 5432}
    ]
)

# Read operations go to replicas
read_conn = router.get_connection(DatabaseOperation.READ)

# Write operations go to master
write_conn = router.get_connection(DatabaseOperation.WRITE)
````

#### Benefits of Read Replicas

- **Improved Read Performance**: Distribute read load across multiple servers
- **Geographic Distribution**: Place replicas closer to users
- **High Availability**: Fallback option if master fails
- **Backup and Analytics**: Use replicas for backup and reporting

#### Considerations

- **Replication Lag**: Replicas may be slightly behind master
- **Eventual Consistency**: Need to handle stale reads
- **Increased Complexity**: More moving parts to manage

### Write Scaling Strategies

Write operations are more challenging to scale as they typically require consistency guarantees.

#### Write Scaling Approaches

**1. Write-through Caching**

````python
# Example: Write-through cache implementation
class WriteThroughCache:
    def __init__(self, cache, database):
        self.cache = cache
        self.database = database
    
    def write(self, key, value):
        # Write to database first
        self.database.write(key, value)
        # Then update cache
        self.cache.set(key, value)
    
    def read(self, key):
        # Try cache first
        value = self.cache.get(key)
        if value is None:
            # Cache miss, read from database
            value = self.database.read(key)
            if value is not None:
                self.cache.set(key, value)
        return value
````

**2. Write-behind (Write-back) Caching**    

```python
import queue
import threading
import time

class WriteBehindCache:
    def __init__(self, cache, database, batch_size=100, flush_interval=5):
        self.cache = cache
        self.database = database
        self.write_queue = queue.Queue()
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self._start_background_writer()
    
    def write(self, key, value):
        # Write to cache immediately
        self.cache.set(key, value)
        # Queue for eventual database write
        self.write_queue.put((key, value))
    
    def _start_background_writer(self):
        def background_writer():
            batch = []
            last_flush = time.time()
            
            while True:
                try:
                    # Get item with timeout
                    item = self.write_queue.get(timeout=1)
                    batch.append(item)
                    
                    # Flush if batch is full or enough time has passed
                    if (len(batch) >= self.batch_size or 
                        time.time() - last_flush >= self.flush_interval):
                        self._flush_batch(batch)
                        batch = []
                        last_flush = time.time()
                        
                except queue.Empty:
                    # Timeout occurred, flush any pending items
                    if batch:
                        self._flush_batch(batch)
                        batch = []
                        last_flush = time.time()
        
        writer_thread = threading.Thread(target=background_writer, daemon=True)
        writer_thread.start()
    
    def _flush_batch(self, batch):
        # Write batch to database
        self.database.write_batch(batch)
```

**Database Sharding for Writes**

- Distribute writes across multiple database shards
- Each shard handles a subset of the data
- Requires careful shard key selection

### Data Partitioning Techniques

**Definition**: Splitting large datasets across multiple databases or servers to improve performance and manageability.

#### Horizontal Partitioning (Sharding)

**1. Range-based Partitioning**

````python
class RangeBasedPartitioner:
    def __init__(self, ranges):
        self.ranges = ranges  # [(0, 1000), (1001, 2000), (2001, 3000)]
    
    def get_shard(self, key):
        for i, (start, end) in enumerate(self.ranges):
            if start <= key <= end:
                return f"shard_{i}"
        raise ValueError(f"Key {key} not in any range")

# Example usage
partitioner = RangeBasedPartitioner([
    (0, 1000000),
    (1000001, 2000000),
    (2000001, 3000000)
])

user_id = 1500000
shard = partitioner.get_shard(user_id)  # Returns "shard_1"
````

**2. Hash-based Partitioning**

````python
import hashlib

class HashBasedPartitioner:
    def __init__(self, num_shards):
        self.num_shards = num_shards
    
    def get_shard(self, key):
        # Convert key to string if it's not already
        key_str = str(key)
        # Create hash and determine shard
        hash_value = int(hashlib.md5(key_str.encode()).hexdigest(), 16)
        return f"shard_{hash_value % self.num_shards}"

# Example usage
partitioner = HashBasedPartitioner(4)
user_id = "user_12345"
shard = partitioner.get_shard(user_id)  # Returns "shard_2" (example)
````

**3. Directory-based Partitioning**

````python
class DirectoryBasedPartitioner:
    def __init__(self):
        self.directory = {}  # Maps keys to shards
        self.default_shard = "shard_0"
    
    def set_shard_mapping(self, key, shard):
        self.directory[key] = shard
    
    def get_shard(self, key):
        return self.directory.get(key, self.default_shard)
    
    def migrate_key(self, key, new_shard):
        old_shard = self.directory.get(key, self.default_shard)
        self.directory[key] = new_shard
        return old_shard, new_shard
````

#### Vertical Partitioning

Split tables by columns rather than rows.

````python
# Example: Vertical partitioning
"""
Original table: users
+----+----------+-------+----------+-------------+
| id | username | email | password | profile_pic |
+----+----------+-------+----------+-------------+

Split into:
Table 1: user_auth (frequently accessed)
+----+----------+----------+
| id | username | password |
+----+----------+----------+

Table 2: user_profile (less frequently accessed)
+----+-------+-------------+
| id | email | profile_pic |
+----+-------+-------------+
"""

class VerticallyPartitionedUser:
    def __init__(self, auth_db, profile_db):
        self.auth_db = auth_db
        self.profile_db = profile_db
    
    def authenticate(self, username, password):
        # Only access auth database
        return self.auth_db.verify_credentials(username, password)
    
    def get_full_profile(self, user_id):
        # Combine data from both databases
        auth_data = self.auth_db.get_user(user_id)
        profile_data = self.profile_db.get_profile(user_id)
        return {**auth_data, **profile_data}
````

#### Considerations for Data Partitioning

**Pros**:

- Improved performance through parallel processing
- Better resource utilization
- Reduced contention and locking
- Easier maintenance of smaller datasets

**Cons**:

- Increased complexity
- Cross-shard queries are expensive
- Rebalancing can be challenging
- Potential for hotspots

**Best Practices**:

- Choose partition keys carefully
- Monitor shard distribution
- Plan for rebalancing
- Avoid cross-shard transactions when possible

## Choosing the Right Scaling Strategy

### Decision Matrix

| **Factor**      | **Horizontal Scaling** | **Vertical Scaling** | **Data Scaling** |
| --------------- | ---------------------- | -------------------- | ---------------- |
| Cost            | Linear growth          | Exponential growth   | Moderate         |
| Complexity      | High                   | Low                  | Very High        |
| Fault Tolerance | Excellent              | Poor                 | Good             |
| Performance     | Good                   | Excellent            | Excellent        |
| Flexibility     | High                   | Low                  | High             |

### When to Use Each Strategy

**Horizontal Scaling**:

- High traffic applications
- Geographically distributed users
- Need for high availability
- Stateless applications

**Vertical Scaling**:

- Legacy applications
- Applications with shared state
- Simple scaling requirements
- Cost-effective for small to medium scale

**Data Scaling**:

- Database is the bottleneck
- Large datasets
- High read/write volumes
- Need for geographical data distribution

### Hybrid Approaches

Most real-world systems use a combination of scaling strategies

## Monitoring and Metrics

### Key Metrics to Track

**Performance Metrics**:

- Response time and latency
- Throughput (requests per second)
- Error rates
- Resource utilization (CPU, memory, disk, network)

**Scaling Metrics**:

- Number of active instances
- Auto-scaling events
- Load distribution across servers
- Queue lengths and processing times

## Conclusion

Scalability patterns are essential for building systems that can grow with demand. The choice between horizontal and vertical scaling depends on specific requirements, constraints, and growth patterns. Data scaling adds another dimension, focusing on database performance and distribution.

**Key Takeaways**:

1. **Start Simple**: Begin with vertical scaling for simple applications
2. **Plan for Growth**: Design with horizontal scaling in mind
3. **Monitor Continuously**: Use metrics to guide scaling decisions
4. **Consider Data Early**: Database scaling often becomes the primary bottleneck
5. **Use Hybrid Approaches**: Combine different strategies for optimal results