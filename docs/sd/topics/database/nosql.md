# NoSQL Patterns

NoSQL databases emerged to address the limitations of relational databases in handling large-scale, distributed systems with varying data structures and access patterns. Each NoSQL database type is optimized for specific use cases, offering different trade-offs between consistency, availability, partition tolerance, and performance.

Core NoSQL Characteristics:

- Schema Flexibility: Dynamic schemas that can evolve without migrations
- Horizontal Scalability: Built for distributed, scale-out architectures
- Eventual Consistency: Trade immediate consistency for availability and performance
- Specialized Data Models: Optimized for specific access patterns and use cases
- High Performance: Optimized for specific read/write patterns

CAP Theorem Implications: NoSQL databases typically choose two of the three CAP properties:

- **Consistency**: All nodes see the same data simultaneously
- **Availability**: System remains operational and responsive
- **Partition Tolerance**: System continues despite network failures

------

## Key-Value Store Design (Redis, DynamoDB)

### Key-Value Store Fundamentals

**Data Model Characteristics:** Key-value stores are the simplest NoSQL model, storing data as unique key-identifier paired with associated values. The database treats values as opaque data, placing no constraints on value structure or content.

**When to Use Key-Value Stores:**

- Caching layers: Session data, frequently accessed objects, computed results
- Real-time recommendations: User preferences, product recommendations
- Gaming applications: Player profiles, game state, leaderboards
- Shopping carts: Temporary data that doesn't require complex queries
- Configuration management: Application settings, feature flags

### Redis Patterns

**Data Structure Optimization:**

**String Operations:** Redis strings can store text, numbers, or binary data up to 512MB. Use strings for simple key-value pairs, counters, and caching serialized objects.

**Counter Pattern:**

```
INCR user:123:page_views
INCRBY user:123:points 50
EXPIRE user:123:session 3600
```

**Hash Operations:** Use hashes to store objects with multiple fields, providing memory efficiency and atomic operations on individual fields.

**User Profile Pattern:**

```
HSET user:123 name "John Doe" email "john@example.com" last_login "2024-01-15"
HGET user:123 name
HMGET user:123 name email
```

**List Operations:** Implement queues, activity feeds, and time-ordered data using Redis lists.

**Activity Feed Pattern:**

```
LPUSH user:123:feed "New post from friend"
LTRIM user:123:feed 0 99  # Keep only latest 100 items
LRANGE user:123:feed 0 19  # Get first 20 items
```

**Set Operations:** Use sets for unique collections, tags, and relationship modeling.

**Tagging System Pattern:**

```
SADD post:456:tags "technology" "programming" "redis"
SISMEMBER post:456:tags "technology"
SINTER post:456:tags post:789:tags  # Common tags
```

**Sorted Set Operations:** Implement leaderboards, time-series data, and priority queues with sorted sets.

**Leaderboard Pattern:**

```
ZADD game:leaderboard 1500 "player1" 1200 "player2"
ZREVRANGE game:leaderboard 0 9 WITHSCORES  # Top 10 players
ZRANK game:leaderboard "player1"  # Player's rank
```

**Advanced Redis Patterns:**

**Publish/Subscribe for Real-time Features:** Implement real-time notifications and messaging using Redis pub/sub capabilities.

**HyperLogLog for Analytics:** Use HyperLogLog for approximate counting of unique items with minimal memory usage.

```
PFADD unique_visitors:2024-01-15 user123 user456 user789
PFCOUNT unique_visitors:2024-01-15  # Approximate unique count
```

**Geospatial Operations:** Store and query location-based data using Redis geospatial commands.

```
GEOADD locations 13.361389 38.115556 "Sicily"
GEORADIUS locations 15 37 200 km  # Find locations within 200km
```

### DynamoDB Patterns

**Single Table Design:** DynamoDB performs best when related data is stored in a single table using composite keys and sparse indexes.

**Access Pattern Modeling:** Design your table structure around your application's query patterns rather than normalizing data:

**E-commerce Single Table Example:**

```
PK (Partition Key) | SK (Sort Key) | GSI1PK | GSI1SK | Attributes
USER#123          | PROFILE       | -      | -      | name, email, address
USER#123          | ORDER#456     | ORDER  | 2024-01-15 | total, status, items
PRODUCT#789       | DETAILS       | CATEGORY#electronics | PRICE#99.99 | name, description
PRODUCT#789       | REVIEW#001    | USER#456 | 2024-01-10 | rating, comment
```

**Global Secondary Indexes (GSI):** Create GSIs to support different query patterns on the same data:

**Query Patterns Supported:**

- Get user profile: PK = USER#123, SK = PROFILE
- Get user orders: PK = USER#123, SK begins_with ORDER#
- Get orders by date: GSI1PK = ORDER, GSI1SK between dates
- Get products by category: GSI1PK = CATEGORY#electronics
- Get reviews by user: GSI1PK = USER#456, GSI1SK begins_with date

**Hot Partition Prevention:** Distribute data evenly across partitions to avoid throttling:

**Time-Based Data Distribution:** Instead of using date as partition key, use date with random suffix:

```
PK: 2024-01-15#001, 2024-01-15#002, 2024-01-15#003
```

**High-Cardinality Partition Keys:** Use user IDs, order IDs, or other high-cardinality values as partition keys to ensure even distribution.

**DynamoDB Optimization Strategies:**

**Batch Operations:** Use batch operations for better throughput and cost efficiency:

- BatchGetItem for reading multiple items
- BatchWriteItem for writing up to 25 items
- Query with pagination for large result sets

**Conditional Writes:** Implement optimistic locking and prevent overwrites using conditional expressions:

```
UpdateExpression: "SET #status = :new_status"
ConditionExpression: "#status = :current_status"
```

**TTL for Automatic Cleanup:** Use Time-To-Live to automatically delete expired data:

```
TTL attribute: expires_at (Unix timestamp)
```

------

## Document Store Design (MongoDB, CouchDB)

**Document Model Benefits:** Document databases store semi-structured data as documents (typically JSON/BSON), allowing flexible schemas and nested data structures that map naturally to application objects.

**When to Use Document Stores:**

- **Content management**: Articles, blogs, product catalogs with varying attributes
- **Real-time analytics**: Event data with flexible schemas
- **Product catalogs**: Items with different attribute sets
- **User-generated content**: Comments, reviews, social media posts
- **Configuration management**: Complex nested configuration data

### MongoDB Patterns

**Schema Design Strategies:**

**Embedding vs Referencing:** Choose between embedding related data within documents or referencing separate documents based on data size, update frequency, and query patterns.

**Embed When:**

- Related data is frequently queried together
- Related data size is bounded and relatively small
- Related data doesn't change frequently
- One-to-few relationships (user and addresses)

```javascript
// Embedded approach for user addresses
{
  "_id": ObjectId("..."),
  "name": "John Doe",
  "email": "john@example.com",
  "addresses": [
    {
      "type": "home",
      "street": "123 Main St",
      "city": "Boston",
      "zipcode": "02101"
    },
    {
      "type": "work",
      "street": "456 Business Ave",
      "city": "Boston", 
      "zipcode": "02102"
    }
  ]
}
```

**Reference When:**

- Related data is large or unbounded
- Related data changes frequently
- Many-to-many relationships
- Need to query related data independently

```javascript
// Referenced approach for user orders
// Users collection
{
  "_id": ObjectId("user123"),
  "name": "John Doe",
  "email": "john@example.com"
}

// Orders collection
{
  "_id": ObjectId("order456"), 
  "userId": ObjectId("user123"),
  "items": [...],
  "total": 299.99,
  "orderDate": ISODate("2024-01-15")
}
```

**Polymorphic Schema Pattern:** Store different types of related objects in the same collection using a type field:

```javascript
// Products with different attributes
{
  "_id": ObjectId("..."),
  "type": "book",
  "title": "Database Design",
  "author": "John Smith",
  "isbn": "978-1234567890",
  "pages": 450
}

{
  "_id": ObjectId("..."),
  "type": "electronics",
  "name": "Laptop",
  "brand": "TechCorp",
  "model": "Pro-2024",
  "specs": {
    "cpu": "Intel i7",
    "ram": "16GB",
    "storage": "512GB SSD"
  }
}
```

**Indexing Strategies:**

**Compound Indexes:** Create indexes that support multiple query patterns:

```javascript
// Support queries by status, user, and date
db.orders.createIndex({ "status": 1, "userId": 1, "orderDate": -1 })

// Supports these queries efficiently:
// - { status: "pending" }
// - { status: "pending", userId: ObjectId("...") }
// - { status: "pending", userId: ObjectId("..."), orderDate: { $gte: date } }
```

**Text Indexes:** Enable full-text search across document fields:

```javascript
db.articles.createIndex({ 
  "title": "text", 
  "content": "text", 
  "tags": "text" 
}, {
  weights: { title: 10, content: 5, tags: 1 }
})
```

**Geospatial Indexes:** Support location-based queries:

```javascript
db.restaurants.createIndex({ "location": "2dsphere" })

// Find restaurants near a point
db.restaurants.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [-73.9857, 40.7484] },
      $maxDistance: 1000  // meters
    }
  }
})
```

**Aggregation Pipeline Optimization:**

**Pipeline Stage Ordering:** Place filtering stages ($match) early in the pipeline to reduce data volume:

```javascript
db.orders.aggregate([
  { $match: { orderDate: { $gte: new Date("2024-01-01") } } },  // Filter early
  { $lookup: { from: "users", localField: "userId", foreignField: "_id", as: "user" } },
  { $unwind: "$user" },
  { $group: { _id: "$user.region", totalSales: { $sum: "$total" } } },
  { $sort: { totalSales: -1 } }
])
```

**Index Usage in Aggregation:** Ensure aggregation pipelines can use indexes for optimal performance:

```javascript
// Create index to support aggregation
db.orders.createIndex({ "orderDate": -1, "status": 1 })

// Aggregation that uses the index
db.orders.aggregate([
  { $match: { orderDate: { $gte: new Date("2024-01-01") }, status: "completed" } },
  { $group: { _id: { $dateToString: { format: "%Y-%m", date: "$orderDate" } }, count: { $sum: 1 } } }
])
```

### CouchDB Patterns

**Document Versioning:** CouchDB's MVCC (Multi-Version Concurrency Control) requires understanding of document revisions:

**Conflict Resolution:** Handle document conflicts in distributed environments:

```javascript
// Document with revision
{
  "_id": "user123",
  "_rev": "2-abc123def456",
  "name": "John Doe",
  "email": "john@newdomain.com"
}

// Update requires current revision
PUT /database/user123
{
  "_id": "user123", 
  "_rev": "2-abc123def456",  // Must match current revision
  "name": "John Doe",
  "email": "john@updatedemail.com"
}
```

**View-Based Querying:** CouchDB uses MapReduce views for querying and indexing:

```javascript
// Map function for user orders by date
function(doc) {
  if (doc.type === 'order') {
    emit([doc.userId, doc.orderDate], {
      total: doc.total,
      status: doc.status,
      itemCount: doc.items.length
    });
  }
}

// Reduce function for user order totals
function(keys, values, rereduce) {
  if (rereduce) {
    return sum(values);
  } else {
    return sum(values.map(function(v) { return v.total; }));
  }
}
```

------

## Wide-Column Store Design (Cassandra, HBase)

**Data Model Characteristics:** Wide-column stores organize data in column families with dynamic columns, optimized for write-heavy workloads and time-series data with predictable query patterns.

**When to Use Wide-Column Stores:**

- Time-series data: IoT sensor data, application metrics, financial data
- Write-heavy applications: Logging systems, event tracking, audit trails
- Large-scale analytics: Data warehousing, real-time analytics dashboards
- Content management: Versioned content, media metadata
- Distributed systems: Applications requiring high availability and partition tolerance

### Cassandra Patterns

**Data Modeling by Query Pattern:** Cassandra data modeling starts with understanding query patterns, then designing tables to serve those queries efficiently.

**Denormalization Strategy:** Create separate tables for each query pattern, accepting data duplication for query performance:

**Time-Series Data Example:**

```cql
-- Table for queries by user and time range
CREATE TABLE user_metrics_by_time (
    user_id UUID,
    metric_date DATE, 
    metric_time TIMESTAMP,
    cpu_usage DECIMAL,
    memory_usage DECIMAL,
    disk_usage DECIMAL,
    PRIMARY KEY ((user_id, metric_date), metric_time)
) WITH CLUSTERING ORDER BY (metric_time DESC);

-- Table for queries by metric type and time
CREATE TABLE metrics_by_type_time (
    metric_type TEXT,
    metric_time TIMESTAMP,
    user_id UUID,
    value DECIMAL,
    PRIMARY KEY ((metric_type), metric_time, user_id)
) WITH CLUSTERING ORDER BY (metric_time DESC);
```

**Partition Key Design:** Choose partition keys that distribute data evenly and support your query patterns:

**Time-Based Partitioning:**

```cql
-- Good: Distributes data across time periods
PRIMARY KEY ((sensor_id, date), timestamp)

-- Avoid: Creates hot partitions for active sensors
PRIMARY KEY (sensor_id, timestamp)
```

**Compound Partition Keys:** Use multiple columns in partition key for better distribution:

```cql
-- Better distribution for user activity logs
CREATE TABLE user_activity (
    user_id UUID,
    activity_date DATE,
    activity_time TIMESTAMP,
    activity_type TEXT,
    details MAP<TEXT, TEXT>,
    PRIMARY KEY ((user_id, activity_date), activity_time)
);
```

**Clustering Column Optimization:** Order clustering columns to support range queries and sorting:

```cql
-- Supports time range queries within partition
PRIMARY KEY ((user_id), created_time, post_id)

-- Query: SELECT * FROM posts WHERE user_id = ? AND created_time > ? AND created_time < ?
```

**Collection Types:** Use Cassandra's collection types for denormalized data storage:

```cql
CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    tags SET<TEXT>,                    -- Unique tags
    preferences MAP<TEXT, TEXT>,        -- Key-value preferences  
    recent_orders LIST<UUID>           -- Ordered list of recent orders
);
```

**Cassandra Anti-Patterns:**

**Avoid Large Partitions:** Keep partition sizes under 100MB to prevent performance issues:

```cql
-- Bad: Unbounded partition growth
PRIMARY KEY (user_id, timestamp)

-- Good: Bounded partitions by time
PRIMARY KEY ((user_id, date), timestamp)
```

**Avoid Secondary Indexes on High-Cardinality Columns:** Secondary indexes work poorly on columns with many unique values:

```cql
-- Avoid indexing on email (high cardinality)
CREATE INDEX ON users (email);  -- Poor performance

-- Instead, create a table with email as partition key
CREATE TABLE users_by_email (
    email TEXT PRIMARY KEY,
    user_id UUID,
    name TEXT
);
```

### HBase Patterns

**Row Key Design:** HBase performance depends heavily on row key design for data distribution and query efficiency.

**Reverse Timestamp Pattern:** For time-series data, use reverse timestamp to get recent data first:

```
Row Key: userId + (Long.MAX_VALUE - timestamp) + sequenceId
Example: user123_9223370536854775807_001
```

**Salting Pattern:** Add random prefix to distribute hot rows across regions:

```
Row Key: saltValue + originalKey
Example: 05_user123_20240115_12345
```

**Hierarchical Keys:** Design row keys to support range scans for related data:

```
Row Key: country_state_city_userId
Example: US_CA_SF_user123
```

**Column Family Design:** Group related columns in column families for optimal storage and retrieval:

```
Column Family 'profile': name, email, phone, address
Column Family 'activity': last_login, page_views, session_count
Column Family 'preferences': theme, language, notifications
```

**Versioning Strategy:** HBase stores multiple versions of data; configure version retention appropriately:

```java
// Keep only latest 3 versions, expire after 30 days
HColumnDescriptor columnFamily = new HColumnDescriptor("profile");
columnFamily.setMaxVersions(3);
columnFamily.setTimeToLive(30 * 24 * 60 * 60); // 30 days in seconds
```

------

## Graph Database Design (Neo4j, Amazon Neptune)

### Graph Database Fundamentals

**Graph Model Components:** Graph databases store data as nodes (entities) and relationships (connections) with properties, optimized for traversing connected data and analyzing relationships.

**When to Use Graph Databases:**

- **Social networks**: Friend relationships, content sharing, influence analysis
- **Recommendation systems**: User-item relationships, collaborative filtering
- **Fraud detection**: Transaction patterns, suspicious relationship networks
- **Knowledge graphs**: Entity relationships, semantic data modeling
- **Network analysis**: Infrastructure monitoring, dependency mapping

### Neo4j Patterns

**Node and Relationship Design:**

**Node Modeling:** Design nodes to represent distinct entities with properties that don't require relationships:

```cypher
// User node with properties
CREATE (u:User {
  id: 'user123',
  name: 'John Doe', 
  email: 'john@example.com',
  joinDate: date('2024-01-15'),
  isActive: true
})

// Product node with properties
CREATE (p:Product {
  id: 'product456',
  name: 'Laptop Pro',
  category: 'Electronics',
  price: 1299.99,
  inStock: true
})
```

**Relationship Modeling:** Use relationships to connect nodes with properties that describe the connection:

```cypher
// User purchases product relationship
MATCH (u:User {id: 'user123'}), (p:Product {id: 'product456'})
CREATE (u)-[r:PURCHASED {
  orderId: 'order789',
  purchaseDate: datetime('2024-01-15T10:30:00'),
  quantity: 1,
  totalPrice: 1299.99
}]->(p)

// User follows user relationship
MATCH (u1:User {id: 'user123'}), (u2:User {id: 'user456'})
CREATE (u1)-[r:FOLLOWS {
  followDate: datetime('2024-01-10T15:20:00'),
  notificationsEnabled: true
}]->(u2)
```

**Graph Query Patterns:**

**Traversal Queries:** Find connected data through relationship patterns:

```cypher
// Find friends of friends who purchased similar products
MATCH (user:User {id: 'user123'})-[:FOLLOWS*2]->(friendOfFriend:User)
MATCH (friendOfFriend)-[:PURCHASED]->(product:Product)
MATCH (user)-[:PURCHASED]->(userProduct:Product)
WHERE product.category = userProduct.category
RETURN DISTINCT friendOfFriend.name, product.name
```

**Recommendation Queries:** Use graph patterns for collaborative filtering:

```cypher
// Product recommendations based on similar users
MATCH (user:User {id: 'user123'})-[:PURCHASED]->(product:Product)
MATCH (similarUser:User)-[:PURCHASED]->(product)
MATCH (similarUser)-[:PURCHASED]->(recommendation:Product)
WHERE NOT (user)-[:PURCHASED]->(recommendation)
RETURN recommendation.name, count(*) as score
ORDER BY score DESC
LIMIT 10
```

**Shortest Path Queries:** Find optimal paths between nodes:

```cypher
// Find shortest connection between two users
MATCH path = shortestPath(
  (user1:User {id: 'user123'})-[:FOLLOWS*]-(user2:User {id: 'user789'})
)
RETURN length(path) as connectionDegree, nodes(path) as connectionPath
```

**Performance Optimization:**

**Index Strategy:** Create indexes on frequently queried node properties:

```cypher
// Create index on user ID for fast lookups
CREATE INDEX user_id_index FOR (u:User) ON (u.id)

// Create composite index for complex queries
CREATE INDEX user_name_active FOR (u:User) ON (u.name, u.isActive)
```

**Query Optimization:** Use PROFILE and EXPLAIN to optimize query performance:

```cypher
// Profile query to identify bottlenecks
PROFILE
MATCH (u:User)-[:PURCHASED]->(p:Product {category: 'Electronics'})
WHERE u.joinDate > date('2024-01-01')
RETURN u.name, count(p) as purchaseCount
ORDER BY purchaseCount DESC
```

**Schema Design Patterns:**

**Time-Based Relationships:** Model temporal aspects of relationships:

```cypher
// Create time-based interaction nodes
CREATE (u:User {id: 'user123'})
CREATE (p:Post {id: 'post456', content: 'Hello World', timestamp: datetime()})
CREATE (i:Interaction {type: 'LIKE', timestamp: datetime()})
CREATE (u)-[:PERFORMED]->(i)-[:ON]->(p)
```

**Hierarchical Data:** Model organizational or categorical hierarchies:

```cypher
// Category hierarchy
CREATE (electronics:Category {name: 'Electronics'})
CREATE (computers:Category {name: 'Computers'})
CREATE (laptops:Category {name: 'Laptops'})
CREATE (computers)-[:SUBCATEGORY_OF]->(electronics)
CREATE (laptops)-[:SUBCATEGORY_OF]->(computers)

// Query all products in electronics category and subcategories
MATCH (category:Category {name: 'Electronics'})<-[:SUBCATEGORY_OF*0..]-(subcat:Category)
MATCH (product:Product)-[:IN_CATEGORY]->(subcat)
RETURN product.name, subcat.name
```

### Amazon Neptune Patterns

**Multi-Model Support:** Neptune supports both property graph (Gremlin) and RDF (SPARQL) models:

**Property Graph with Gremlin:**

```groovy
// Add user vertex with properties
g.addV('User')
 .property('id', 'user123')
 .property('name', 'John Doe')
 .property('email', 'john@example.com')

// Add relationship with properties
g.V().hasLabel('User').has('id', 'user123')
 .addE('FOLLOWS')
 .to(g.V().hasLabel('User').has('id', 'user456'))
 .property('followDate', '2024-01-15')
 .property('strength', 0.8)
```

**RDF with SPARQL:**

```sparql
# Insert RDF triples
INSERT DATA {
  <http://example.org/user123> <http://example.org/name> "John Doe" .
  <http://example.org/user123> <http://example.org/email> "john@example.com" .
  <http://example.org/user123> <http://example.org/follows> <http://example.org/user456> .
}

# Query RDF data
SELECT ?name ?email WHERE {
  <http://example.org/user123> <http://example.org/name> ?name .
  <http://example.org/user123> <http://example.org/email> ?email .
}
```

**Bulk Loading Strategies:** Use Neptune's bulk loading capabilities for large datasets:

```csv
# Vertices CSV format
~id,~label,name:String,email:String
user123,User,John Doe,john@example.com
user456,User,Jane Smith,jane@example.com

# Edges CSV format  
~id,~from,~to,~label,followDate:Date
follow1,user123,user456,FOLLOWS,2024-01-15
```

------

## Key Takeaways

1. **Choose the right NoSQL type**: Match database characteristics to your specific use case and access patterns
2. **Design for query patterns**: NoSQL schemas should be optimized for how data will be accessed, not normalized structures
3. **Embrace denormalization**: Accept data duplication in exchange for query performance and scalability
4. **Understand consistency trade-offs**: Most NoSQL databases offer eventual consistency in exchange for availability and partition tolerance
5. **Plan for scale**: Design data models that distribute load evenly and avoid hot spots
6. **Leverage database-specific features**: Each NoSQL database has unique capabilities that should influence design decisions
7. **Monitor and optimize**: Use database-specific tools to monitor performance and optimize queries

### Common NoSQL Design Mistakes

- **Applying relational patterns**: Using normalized schemas and complex joins in NoSQL databases
- **Ignoring data distribution**: Creating hot partitions that limit scalability
- **Over-indexing**: Creating too many secondary indexes, especially in write-heavy workloads
- **Inconsistent data modeling**: Not maintaining consistency in how similar data is modeled across the application
- **Neglecting data size limits**: Exceeding database-specific limits for document or partition sizes
- **Poor key design**: Using sequential or timestamp-based keys that create hot spots