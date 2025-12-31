# Data Modeling

Data modeling is the foundation of any successful system design. It involves understanding how data flows through your system, how it's accessed, and how it needs to scale. Unlike traditional database design that focuses on normalization and relationships, modern data modeling prioritizes access patterns, performance, and scalability requirements.

**Modern Data Modeling Principles:**

- **Access Pattern Driven**: Design around how data will be queried, not just how it's structured
- **Performance Optimization**: Optimize for read/write patterns and latency requirements
- **Scale Planning**: Design for horizontal scaling and data distribution
- **Consistency Trade-offs**: Balance consistency requirements with performance needs
- **Technology Agnostic**: Focus on logical models before choosing specific databases

**Key Considerations:**

- What are the primary data access patterns?
- How will data volume grow over time?
- What are the consistency and durability requirements?
- How will data be distributed across systems?
- What are the performance and latency constraints?

------

## Schema Design

### Logical vs Physical Schema Design

**Logical Schema Design:** The logical schema represents the conceptual structure of data independent of any specific database technology. It focuses on entities, relationships, and business rules.

**Entity Identification Process:** Start by identifying the core business entities and their relationships:

**E-commerce Example Entities:**

- **Users**: Customers, administrators, vendors
- **Products**: Items for sale with attributes and categorization
- **Orders**: Purchase transactions with line items and fulfillment status
- **Inventory**: Stock levels, warehouses, supply chain information
- **Payments**: Transaction records, payment methods, financial data

**Relationship Analysis:** Map the relationships between entities considering cardinality and business rules:

**One-to-Many Relationships:**

- User to Orders: One user can have many orders
- Order to Order Items: One order contains many items
- Category to Products: One category contains many products

**Many-to-Many Relationships:**

- Products to Categories: Products can belong to multiple categories
- Users to Products (Wishlist): Users can wishlist many products
- Orders to Promotions: Orders can use multiple promotions

**Attribute Definition:** Define the properties of each entity with data types, constraints, and business rules:

**User Entity Attributes:**

```
User:
- user_id: Unique identifier (UUID)
- email: Contact information (String, unique, required)
- password_hash: Authentication (String, required)
- created_at: Registration timestamp (DateTime, required)
- last_login: Activity tracking (DateTime, nullable)
- status: Account state (Enum: active, suspended, deleted)
- profile: Extended information (JSON, optional)
```

### Physical Schema Implementation

**Technology-Specific Considerations:** Transform logical schemas into physical implementations optimized for chosen database technologies.

**Relational Database Implementation:**

```sql
-- Normalized approach for strong consistency
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    profile JSONB
);

CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_id UUID REFERENCES orders(order_id),
    product_id UUID,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_id)
);
```

**Document Database Implementation:**

```javascript
// MongoDB - Embedded approach for performance
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "password_hash": "...",
  "created_at": ISODate("2024-01-15T10:00:00Z"),
  "last_login": ISODate("2024-01-20T14:30:00Z"),
  "status": "active",
  "profile": {
    "name": "John Doe",
    "phone": "+1-555-0123",
    "preferences": {
      "newsletter": true,
      "notifications": false
    }
  },
  "recent_orders": [
    {
      "order_id": ObjectId("..."),
      "status": "completed",
      "total_amount": 299.99,
      "created_at": ISODate("2024-01-18T09:15:00Z"),
      "items": [
        {
          "product_id": ObjectId("..."),
          "name": "Product Name",
          "quantity": 2,
          "unit_price": 149.99
        }
      ]
    }
  ]
}
```

**Schema Evolution Strategies:**

**Versioned Schemas:** Plan for schema changes by versioning your data structures:

```javascript
// Document with schema version
{
  "_id": ObjectId("..."),
  "schema_version": "2.1",
  "email": "user@example.com",
  "created_at": ISODate("2024-01-15T10:00:00Z"),
  // ... other fields
}
```

**Backward Compatibility:** Design schemas that can handle both old and new data formats during migrations:

```sql
-- Add new column with default value
ALTER TABLE users ADD COLUMN phone VARCHAR(20) DEFAULT NULL;

-- Gradual migration with application logic handling both cases
-- Old records: phone = NULL
-- New records: phone = actual phone number
```

**Forward Compatibility:** Use flexible data types that can accommodate future requirements:

```sql
-- Use JSONB for flexible attributes
ALTER TABLE products ADD COLUMN attributes JSONB DEFAULT '{}';

-- Allows adding new product attributes without schema changes
UPDATE products SET attributes = '{"color": "red", "size": "large"}' WHERE product_id = 'xyz';
```

### Multi-Model Schema Design

**Polyglot Persistence Strategy:** Use different databases for different data types and access patterns within the same application:

**Database Selection by Use Case:**

- **User Authentication**: PostgreSQL for ACID guarantees and complex queries
- **Product Catalog**: MongoDB for flexible product attributes and search
- **Shopping Cart**: Redis for fast read/write and automatic expiration
- **Order Processing**: PostgreSQL for transaction integrity
- **Analytics**: Cassandra for time-series data and high write throughput
------

## Data Access Patterns

### Read vs Write Optimization

**Read-Heavy Pattern Optimization:**

Denormalization for Read Performance: Pre-compute and store frequently accessed data combinations:

```sql
-- Instead of joining every time
SELECT u.name, COUNT(o.order_id) as order_count, SUM(o.total) as lifetime_value
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.name;

-- Store computed values
ALTER TABLE users ADD COLUMN order_count INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN lifetime_value DECIMAL(10,2) DEFAULT 0.00;

-- Update via triggers or batch jobs
CREATE OR REPLACE FUNCTION update_user_stats()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE users 
  SET order_count = (SELECT COUNT(*) FROM orders WHERE user_id = NEW.user_id),
      lifetime_value = (SELECT COALESCE(SUM(total), 0) FROM orders WHERE user_id = NEW.user_id)
  WHERE user_id = NEW.user_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

Read Replica Strategies: Design for eventual consistency with read replicas:

**Write-Heavy Pattern Optimization:**

Batch Writing Strategies: Group related writes to improve throughput:

```javascript
class AnalyticsService {
  constructor() {
    this.eventBuffer = [];
    this.batchSize = 1000;
    this.flushInterval = 5000; // 5 seconds
    
    setInterval(() => this.flushEvents(), this.flushInterval);
  }
  
  async trackEvent(event) {
    this.eventBuffer.push({
      ...event,
      timestamp: new Date()
    });
    
    if (this.eventBuffer.length >= this.batchSize) {
      await this.flushEvents();
    }
  }
  
  async flushEvents() {
    if (this.eventBuffer.length === 0) return;
    
    const events = this.eventBuffer.splice(0);
    await cassandra.analytics_events.insertMany(events);
  }
}
```

**Asynchronous Write Patterns:** Decouple write operations from user-facing requests:

```javascript
class OrderService {
  async placeOrder(orderData) {
    // 1. Immediate response to user
    const orderId = generateOrderId();
    
    // 2. Queue order processing
    await messageQueue.publish('order.process', {
      order_id: orderId,
      ...orderData
    });
    
    // 3. Return immediately
    return { order_id: orderId, status: 'processing' };
  }
}

// Background worker processes actual order
class OrderProcessor {
  async processOrder(orderData) {
    const transaction = await db.beginTransaction();
    try {
      // Validate inventory
      await this.checkInventory(orderData.items);
      
      // Create order record
      await this.createOrder(orderData);
      
      // Update inventory
      await this.updateInventory(orderData.items);
      
      // Process payment
      await this.processPayment(orderData.payment);
      
      await transaction.commit();
      
      // Notify user of success
      await this.sendConfirmationEmail(orderData.user_id);
      
    } catch (error) {
      await transaction.rollback();
      await this.handleOrderFailure(orderData, error);
    }
  }
}
```

### Time-Series Data Patterns

**Time-Based Partitioning:** Organize data by time periods for efficient querying and maintenance:

```sql
-- PostgreSQL table partitioning by month
CREATE TABLE metrics (
    id BIGSERIAL,
    user_id UUID,
    metric_type VARCHAR(50),
    value DECIMAL,
    recorded_at TIMESTAMP
) PARTITION BY RANGE (recorded_at);

-- Create monthly partitions
CREATE TABLE metrics_2024_01 PARTITION OF metrics
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE metrics_2024_02 PARTITION OF metrics
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

**Rolling Window Aggregations:** Pre-compute time-based aggregations for dashboards:

```sql
-- Materialized view for hourly metrics
CREATE MATERIALIZED VIEW hourly_metrics AS
SELECT 
  user_id,
  metric_type,
  DATE_TRUNC('hour', recorded_at) as hour,
  COUNT(*) as event_count,
  AVG(value) as avg_value,
  MAX(value) as max_value,
  MIN(value) as min_value
FROM metrics
WHERE recorded_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY user_id, metric_type, DATE_TRUNC('hour', recorded_at);

-- Refresh every hour
SELECT cron.schedule('refresh-hourly-metrics', '0 * * * *', 'REFRESH MATERIALIZED VIEW hourly_metrics;');
```

**Data Retention Policies:** Implement automatic cleanup for time-series data:

```javascript
class DataRetentionService {
  async cleanupOldData() {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - 90); // 90 days retention
    
    // Archive old data to cold storage
    const oldRecords = await db.metrics.find({
      recorded_at: { $lt: cutoffDate }
    });
    
    if (oldRecords.length > 0) {
      // Archive to S3 or similar
      await this.archiveToS3(oldRecords);
      
      // Delete from primary database
      await db.metrics.deleteMany({
        recorded_at: { $lt: cutoffDate }
      });
    }
  }
}
```

### CQRS and Event Sourcing Patterns

**Command Query Responsibility Segregation:** Separate read and write models for optimal performance:

```javascript
// Write Model (Commands)
class OrderWriteModel {
  async createOrder(command) {
    const events = [
      { type: 'OrderCreated', data: command, timestamp: new Date() },
      { type: 'InventoryReserved', data: { items: command.items }, timestamp: new Date() }
    ];
    
    await eventStore.appendEvents(command.order_id, events);
    
    // Publish events for read model updates
    events.forEach(event => eventBus.publish(event.type, event));
  }
}

// Read Model (Queries)
class OrderReadModel {
  async getOrderHistory(userId) {
    // Optimized read model with denormalized data
    return await readDB.order_history.find({ user_id: userId })
      .sort({ created_at: -1 })
      .limit(50);
  }
  
  async getOrderSummary(orderId) {
    // Pre-computed summary data
    return await readDB.order_summaries.findOne({ order_id: orderId });
  }
}
```

**Event Sourcing Implementation:** Store all changes as events for complete audit trail and state reconstruction:

------

## Hot Spotting Prevention

### Identifying Hot Spot Patterns

**Common Hot Spot Scenarios:**

**Temporal Hot Spots:** Data access concentrated during specific time periods:

- Black Friday sales creating order processing bottlenecks
- Social media trending topics generating massive read traffic
- End-of-month reporting queries overwhelming analytical systems
- Daily batch jobs creating periodic load spikes

**Geographic Hot Spots:** Uneven data distribution across geographic regions:

- Popular content going viral in specific regions
- Time zone-based access patterns (business hours)
- Regional events driving localized traffic spikes
- Content delivery network edge cache misses

**Entity Hot Spots:** Specific records receiving disproportionate attention:

- Celebrity user profiles in social media systems
- Popular product pages in e-commerce systems
- Trending posts or viral content
- System configuration records accessed by all services

### Distribution Strategies

**Hash-Based Distribution:** Use consistent hashing to distribute data evenly:

**Random Sharding:** Add randomness to predictable patterns:

**Geographic Distribution:** Distribute data based on geographic regions:
### Load Balancing Strategies

**Application-Level Load Balancing:** Implement smart routing based on current load:

**Circuit Breaker for Hot Spot Protection:** Protect against cascading failures from hot spots:
### Caching Strategies for Hot Data

**Multi-Level Caching:** Implement hierarchical caching to handle hot spots: (L1, L2, L3, etc..)

**Predictive Caching:** Pre-load data based on access patterns:

------

## Key Takeaways

1. **Design for access patterns**: Schema design should optimize for how data will be queried, not just logical relationships
2. **Plan for scale early**: Consider data distribution and hot spot prevention from the beginning
3. **Embrace appropriate trade-offs**: Balance consistency, performance, and complexity based on actual requirements
4. **Use the right tool for the job**: Different data types and access patterns may require different database technologies
5. **Monitor and adapt**: Continuously monitor access patterns and adjust data models accordingly
6. **Implement defense in depth**: Use multiple strategies (sharding, caching, load balancing) to prevent hot spots
7. **Design for evolution**: Build schemas that can adapt to changing requirements without major rewrites

### Common Data Modeling Mistakes

- **Premature normalization**: Over-normalizing data that will primarily be read together
- **Ignoring access patterns**: Designing schemas without understanding query requirements
- **Single database assumption**: Trying to fit all data into one database technology
- **Hot spot ignorance**: Not considering data distribution and load balancing
- **Static design**: Creating rigid schemas that can't evolve with requirements
- **Consistency over-engineering**: Requiring strong consistency where eventual consistency would suffice