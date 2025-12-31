# Relational Database Patterns

Relational databases remain the backbone of most modern applications due to their ACID guarantees, mature tooling, and well-understood patterns. Understanding how to properly design, optimize, and scale relational databases is crucial for building robust systems that can handle growing data volumes and user loads while maintaining data consistency and performance.

Core Relational Database Concepts:

- ACID Properties: Atomicity, Consistency, Isolation, Durability
- SQL Standards: Structured Query Language for data manipulation
- Schema Enforcement: Strict data types and constraints
- Relational Integrity: Foreign keys and referential constraints
- Transaction Support: Multi-statement operations with rollback capabilities

When to Choose Relational Databases:

- Complex relationships: Multiple entities with intricate relationships
- ACID requirements: Strong consistency and transaction guarantees needed
- Mature ecosystem: Extensive tooling, monitoring, and expertise available
- Structured data: Well-defined schema with predictable data types
- Reporting needs: Complex queries, joins, and analytical operations

------

## Normalization vs Denormalization

Normalization is the process of organizing data to *minimize redundancy and dependency* by dividing large tables into smaller, related tables. The goal is to eliminate duplicate data and ensure data integrity through proper table relationships.

### Normal Form Progression

**First Normal Form (1NF):**

- Each table cell contains a single value
- Each record is unique with a primary key
- No repeating groups or arrays in columns
- All entries in a column are of the same data type

**Second Normal Form (2NF):**

- Must be in 1NF
- All non-key attributes are fully dependent on the primary key
- No partial dependencies on composite primary keys
- Eliminates redundancy in tables with composite keys

**Third Normal Form (3NF):**

- Must be in 2NF
- No transitive dependencies between non-key attributes
- Non-key attributes depend only on the primary key
- Most commonly used normal form in practice

**Boyce-Codd Normal Form (BCNF):**

- Stricter version of 3NF
- Every determinant must be a candidate key
- Eliminates certain anomalies not addressed by 3NF
- Used when higher data integrity is required

**Normalization Example:**

![](assets/Pasted%20image%2020251229221231.png)

Consider above student and course table.

Let's understand 1 NF : NF fixes the structure, not redundancy

![](assets/Pasted%20image%2020251229221539.png)

2 NF : Table must be in 1NF and every non-key attribute must depend on the full primary key.
Primary Key : `(student_id, course_id)`

![](assets/Pasted%20image%2020251229221904.png)

Correct 2NF Tables :

![](assets/Pasted%20image%2020251229222050.png)

- No partial dependencies
- Each non-key attribute depends on full key

for 3NF Table must be in 2NF and no transitive dependency should exist

![](assets/Pasted%20image%2020251229222355.png)

![](assets/Pasted%20image%2020251229222607.png)

- No non-key -> non-key dependency, removes indirect dependency

BCNF : for every functional dependency A -> B, A must be superkey. Stronger form of 3NF

![](assets/Pasted%20image%2020251229223023.png)

![](assets/Pasted%20image%2020251229223142.png)

- All determinants are super-keys


| Normal Form | Fixes                 | Eliminates                     |
| ----------- | --------------------- | ------------------------------ |
| 1NF         | Atomicity             | Multi-valued fields            |
| 2NF         | Partial Dependency    | Redundancy from composite keys |
| 3NF         | Transitive Dependency | indirect redundancy            |
| BCNF        | Weak Determinants     | All FD Anomalies               |


**Benefits of Normalization:**

**Data Integrity:**

- Eliminates update anomalies where changing one piece of information requires multiple updates
- Prevents insert anomalies where you cannot add data without having other unrelated data
- Avoids delete anomalies where removing a record loses other important information
- Ensures referential integrity through foreign key constraints

**Storage Efficiency:**

- Reduces data redundancy and storage requirements
- Minimizes disk space usage through elimination of duplicate data
- Enables more efficient backup and restore operations
- Reduces memory footprint for database operations

**Maintenance Benefits:**

- Schema changes are isolated to specific tables
- Business rule changes affect fewer locations
- Data validation is centralized and consistent
- Easier to understand and maintain table relationships

### Strategic Denormalization

**When to Denormalize:**

Despite the benefits of normalization, there are scenarios where controlled denormalization improves performance and simplifies operations.

**Read-Heavy Workloads:**

- Applications with 90% reads and 10% writes benefit from denormalized read models
- Reduces complex joins that can be expensive at scale
- Enables faster query execution for common access patterns
- Simplifies application logic by reducing the number of tables to query

**Performance Critical Paths:**

- User-facing features that require sub-100ms response times
- Dashboard and reporting queries that aggregate data from multiple tables
- Real-time features where join complexity adds unacceptable latency
- Mobile applications with limited bandwidth where fewer round trips are crucial

**Denormalization Strategies:**

**Calculated Fields:** Store computed values that would otherwise require expensive calculations or aggregations at query time.

```sql
-- Instead of calculating every time:
SELECT customer_id, COUNT(*) as order_count, SUM(total) as total_spent
FROM orders 
GROUP BY customer_id

-- Store in customer table:
ALTER TABLE customers ADD COLUMN order_count INT DEFAULT 0;
ALTER TABLE customers ADD COLUMN total_spent DECIMAL(10,2) DEFAULT 0.00;
```

**Redundant Data for Performance:** Duplicate frequently accessed data to avoid joins in critical queries.

```sql
-- Store customer name in orders table for quick order listing
ALTER TABLE orders ADD COLUMN customer_name VARCHAR(255);

-- Update trigger to maintain consistency
CREATE TRIGGER update_customer_name 
AFTER UPDATE ON customers
FOR EACH ROW
UPDATE orders SET customer_name = NEW.name WHERE customer_id = NEW.customer_id;
```

**Materialized Views:** Pre-computed query results stored as tables for complex analytical queries.

```sql
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
  DATE_TRUNC('month', order_date) as month,
  customer_id,
  COUNT(*) as order_count,
  SUM(total) as total_sales
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
GROUP BY DATE_TRUNC('month', order_date), customer_id;
```

**Managing Denormalization Complexity:**

**Consistency Maintenance:**

- Database triggers to automatically update redundant data
- Application-level consistency checks and corrections
- Batch jobs to reconcile and fix inconsistencies
- Event-driven updates using message queues for eventual consistency

**Data Validation:**

- Regular consistency checks between normalized and denormalized data
- Automated tests to verify data integrity after updates
- Monitoring alerts for data inconsistencies
- Manual reconciliation processes for critical data

------

## Indexing Strategies

### Index Fundamentals

**Index Types and Use Cases:**

**Primary Indexes:** Every table should have a primary key that automatically creates a unique index. This index enforces uniqueness and provides the fastest way to locate specific rows.

**Secondary Indexes:** Additional indexes created on frequently queried columns to improve query performance. These indexes create separate data structures that point back to the actual table rows.

**Composite Indexes:** Indexes spanning multiple columns, where column order significantly impacts performance. The leftmost column principle means queries can use the index if they filter or sort by the leftmost columns.

**Index Selection Strategy:**

**Query Pattern Analysis:** Before creating indexes, analyze actual query patterns from application logs and database query statistics. Focus on queries that:

- Execute frequently (high query volume)
- Take significant time to complete (slow queries)
- Are critical to user experience (user-facing features)
- Support business-critical operations (payments, core features)

**WHERE Clause Optimization:** Create indexes on columns frequently used in WHERE clauses, particularly for equality and range queries.

```sql
-- For query: SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending'
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);

-- For query: SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31'
CREATE INDEX idx_orders_date ON orders(order_date);
```

**JOIN Optimization:** Foreign key columns should almost always be indexed to accelerate join operations between tables.

```sql
-- Essential indexes for joins
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

**Composite Index Design:**

**Column Order Importance:** The order of columns in composite indexes dramatically affects their usefulness. Place the most selective columns first, followed by columns used in range queries.

```sql
-- Good: Status has few values, customer_id is highly selective
CREATE INDEX idx_orders_status_customer_date ON orders(customer_id, status, order_date);

-- This index supports these queries efficiently:
-- WHERE customer_id = 123
-- WHERE customer_id = 123 AND status = 'pending'
-- WHERE customer_id = 123 AND status = 'pending' AND order_date > '2024-01-01'
```

**Covering Indexes:** Include frequently accessed columns in the index to avoid table lookups entirely.

```sql
-- Include commonly selected columns to avoid table access
CREATE INDEX idx_orders_covering ON orders(customer_id, status) 
INCLUDE (order_date, total, shipping_address);
```

### Advanced Indexing Techniques

**Partial Indexes:** Create indexes on subsets of data to reduce index size and improve performance for specific query patterns.

```sql
-- Index only active orders to reduce index size
CREATE INDEX idx_active_orders ON orders(customer_id, order_date) 
WHERE status IN ('pending', 'processing', 'shipped');

-- Index only recent data for better performance
CREATE INDEX idx_recent_orders ON orders(order_date, customer_id) 
WHERE order_date > CURRENT_DATE - INTERVAL '1 year';
```

**Functional Indexes:** Create indexes on expressions or function results when queries frequently use computed values.

```sql
-- For queries using LOWER() function
CREATE INDEX idx_customers_email_lower ON customers(LOWER(email));

-- For date part queries
CREATE INDEX idx_orders_month ON orders(EXTRACT(MONTH FROM order_date));
```

**Index Maintenance Considerations:**

**Write Performance Impact:** Every index adds overhead to INSERT, UPDATE, and DELETE operations. Balance query performance improvements against write performance degradation.

**Storage Overhead:** Indexes consume additional disk space, sometimes significant amounts for large tables with many indexes. Monitor index size and utility regularly.

**Index Monitoring:** Regularly analyze index usage statistics to identify unused indexes that should be dropped and missing indexes that should be created.

```sql
-- PostgreSQL: Check index usage
SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes 
ORDER BY idx_tup_read DESC;

-- Identify unused indexes
SELECT schemaname, tablename, indexname
FROM pg_stat_user_indexes 
WHERE idx_tup_read = 0 AND idx_tup_fetch = 0;
```

------

## Query Optimization

### Query Performance Analysis

**Execution Plan Analysis:** Understanding how the database executes queries is crucial for optimization. Execution plans reveal whether indexes are being used, how tables are joined, and where performance bottlenecks exist.

**Common Performance Anti-patterns:**

**Full Table Scans:** When queries scan entire tables instead of using indexes, performance degrades significantly as table size grows. This typically happens with:

- Missing indexes on WHERE clause columns
- Functions applied to indexed columns in WHERE clauses
- Type mismatches between query parameters and column types
- Complex WHERE conditions that prevent index usage

**Inefficient Joins:** Poor join strategies can multiply query execution time, especially with:

- Cartesian products from missing join conditions
- Nested loop joins on large tables without proper indexes
- Hash joins that exceed available memory
- Multiple table joins without considering join order optimization

**Subquery Inefficiencies:** Correlated subqueries that execute once per row of the outer query can be extremely expensive:

```sql
-- Inefficient correlated subquery
SELECT customer_id, name 
FROM customers c
WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) > 5;

-- Optimized with JOIN
SELECT DISTINCT c.customer_id, c.name
FROM customers c
JOIN (
  SELECT customer_id 
  FROM orders 
  GROUP BY customer_id 
  HAVING COUNT(*) > 5
) o ON c.customer_id = o.customer_id;
```

### SQL Optimization Techniques

**Query Rewriting Strategies:**

**EXISTS vs IN Optimization:** For subqueries, EXISTS often performs better than IN, especially when the subquery result set is large:

```sql
-- Less efficient with large order tables
SELECT * FROM customers 
WHERE customer_id IN (SELECT customer_id FROM orders WHERE status = 'pending');

-- More efficient
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'pending');
```

**JOIN vs Subquery Trade-offs:** JOINs are typically more efficient than subqueries for retrieving related data:

```sql
-- Subquery approach
SELECT * FROM customers 
WHERE customer_id IN (
  SELECT customer_id FROM orders 
  WHERE order_date > '2024-01-01'
);

-- JOIN approach (usually faster)
SELECT DISTINCT c.*
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date > '2024-01-01';
```

**Pagination Optimization:** Traditional LIMIT/OFFSET pagination becomes inefficient for large offsets:

```sql
-- Inefficient for large offsets
SELECT * FROM orders ORDER BY order_date LIMIT 20 OFFSET 100000;

-- Cursor-based pagination (more efficient)
SELECT * FROM orders 
WHERE order_date > '2024-01-15 10:30:00'  -- last seen timestamp
ORDER BY order_date 
LIMIT 20;
```

**Aggregate Query Optimization:**

**Window Functions vs Group By:** Window functions can be more efficient than self-joins for ranking and comparative analysis:

```sql
-- Traditional approach with self-join
SELECT o1.customer_id, o1.order_date, o1.total,
       COUNT(o2.order_id) as order_rank
FROM orders o1
LEFT JOIN orders o2 ON o1.customer_id = o2.customer_id 
                    AND o2.total >= o1.total
GROUP BY o1.customer_id, o1.order_date, o1.total;

-- More efficient with window function
SELECT customer_id, order_date, total,
       RANK() OVER (PARTITION BY customer_id ORDER BY total DESC) as order_rank
FROM orders;
```

**Batch Processing for Large Updates:** Break large UPDATE or DELETE operations into smaller batches to avoid long-running transactions:

```sql
-- Instead of updating millions of rows at once
UPDATE orders SET status = 'archived' WHERE order_date < '2023-01-01';

-- Process in batches
DO $$
BEGIN
  LOOP
    UPDATE orders SET status = 'archived' 
    WHERE order_date < '2023-01-01' AND status != 'archived'
    LIMIT 1000;
    
    EXIT WHEN NOT FOUND;
    COMMIT;
  END LOOP;
END $$;
```

### Query Caching Strategies

**Query Result Caching:** Cache expensive query results in application memory or external cache stores like Redis:

**Database Query Cache:** Many databases provide built-in query caching for identical queries:

- MySQL has a query cache for SELECT statements
- PostgreSQL caches execution plans for prepared statements
- Oracle provides result set caching for frequently executed queries

**Application-Level Caching:** Implement caching at the application layer for maximum control:

- Cache expensive aggregation queries that don't change frequently
- Use time-based or event-based cache invalidation
- Implement cache warming for predictably accessed data
- Consider cache-aside pattern for flexibility

**Materialized Views for Analytics:** For complex analytical queries that don't need real-time data:

```sql
-- Create materialized view for monthly sales reports
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT 
  DATE_TRUNC('month', order_date) as month,
  COUNT(*) as order_count,
  SUM(total) as total_sales,
  AVG(total) as avg_order_value
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '2 years'
GROUP BY DATE_TRUNC('month', order_date);

-- Refresh periodically
REFRESH MATERIALIZED VIEW monthly_sales;
```

------

## Database Federation

### Federation Architecture Patterns

**What is Database Federation:** Database federation is a technique for splitting databases across multiple machines while presenting a unified interface to applications. Unlike sharding, federation splits databases by function or feature rather than by data distribution.

**Functional Federation:** Split databases based on business domains or application modules:

**Service-Based Federation:**

- User service has its own database for authentication and profiles
- Order service manages order and payment data
- Inventory service handles product catalog and stock levels
- Analytics service maintains reporting and metrics data

**Benefits of Functional Federation:**

- Independent scaling based on service-specific load patterns
- Technology diversity allowing optimal database choice per service
- Fault isolation where one service's database issues don't affect others
- Team autonomy with clear data ownership boundaries

**Geographic Federation:** Distribute databases across geographic regions to improve latency and comply with data residency requirements:

**Regional Data Distribution:**

- North American users' data stored in US data centers
- European users' data stored in EU data centers for GDPR compliance
- Asian users' data stored in regional data centers for latency optimization
- Global shared data replicated across regions with eventual consistency

### Federation Implementation Strategies

**Database Router/Proxy Layer:** Implement a routing layer that directs queries to appropriate database instances:

**Routing Logic:**

- Route user authentication queries to user database
- Route order-related queries to order database
- Route product queries to inventory database
- Handle cross-service queries through application logic or data synchronization

**Connection Management:**

- Maintain separate connection pools for each federated database
- Implement health checks and failover logic for database availability
- Handle connection scaling based on per-service load patterns
- Monitor connection utilization across all federated databases

**Cross-Federation Challenges:**

**Distributed Transactions:** Traditional ACID transactions don't work across federated databases, requiring alternative approaches:

**Saga Pattern Implementation:** Break distributed transactions into a series of local transactions with compensating actions:

1. Begin local transaction in first database
2. If successful, proceed to next database transaction
3. If any step fails, execute compensating transactions to undo previous steps
4. Maintain transaction state and retry logic for failure scenarios

**Event-Driven Consistency:** Use event sourcing and eventual consistency for cross-federation data integrity:

- Publish events when data changes in one federation
- Subscribe to relevant events in other federations
- Apply changes asynchronously with conflict resolution
- Accept temporary inconsistency for improved performance and availability

**Data Synchronization Patterns:**

**Read Replicas Across Federations:** Maintain read-only copies of essential data across federations for query performance:

- Replicate user profile data to order database for order processing
- Replicate product data to analytics database for reporting
- Use Change Data Capture (CDC) for real-time synchronization
- Implement eventual consistency with conflict resolution strategies

**Shared Reference Data:** Some data needs to be consistent across all federations:

- Product catalog information
- Configuration and system settings
- User authentication tokens and sessions
- Tax rates and pricing information

### Federation Scaling Considerations

**Federation vs Sharding Trade-offs:**

**When to Choose Federation:**

- Clear functional boundaries between different types of data
- Different performance requirements for different data types
- Team organization aligns with functional data boundaries
- Different compliance requirements for different data types

**When to Choose Sharding:**

- Single large dataset that exceeds single database capacity
- Uniform access patterns across all data
- Need for transparent scaling without application changes
- Complex cross-functional queries are common

**Operational Complexity:** Federation increases operational overhead through:

- Multiple database technologies to maintain and monitor
- Complex backup and disaster recovery across federations
- Schema migration coordination across multiple databases
- Performance monitoring and optimization for different database types

**Performance Optimization in Federated Systems:**

**Query Planning:**

- Minimize cross-federation queries through careful data design
- Cache frequently accessed cross-federation data locally
- Use asynchronous processing for non-critical cross-federation operations
- Implement smart routing to minimize network latency

**Data Locality:**

- Co-locate related data that's frequently accessed together
- Denormalize data across federations when appropriate
- Use event sourcing to maintain derived data locally
- Implement intelligent caching strategies for cross-federation data

------

## Key Takeaways

1. **Normalization provides data integrity**: Use normalized designs for transactional systems where consistency is critical
2. **Strategic denormalization improves performance**: Denormalize for read-heavy workloads and performance-critical paths
3. **Index strategy requires query analysis**: Create indexes based on actual query patterns, not assumptions
4. **Query optimization is iterative**: Continuously monitor and optimize based on real-world usage patterns
5. **Federation enables functional scaling**: Split databases by business domain for independent scaling and technology choices
6. **Balance consistency and performance**: Accept trade-offs between strict consistency and system performance
7. **Monitor and measure everything**: Use database metrics to guide optimization decisions

### Common Relational Database Mistakes

- **Over-normalization**: Creating so many tables that simple queries require complex joins
- **Under-indexing**: Not creating indexes for common query patterns, leading to poor performance
- **Over-indexing**: Creating too many indexes, slowing down write operations unnecessarily
- **Ignoring query patterns**: Designing schemas without understanding how data will be accessed
- **Poor federation boundaries**: Splitting databases in ways that require frequent cross-database operations
- **Neglecting maintenance**: Not monitoring index usage, query performance, and database health

### Interview Tips

**Effective Database Design Discussion:**

- Always ask about query patterns and access frequencies before designing schemas
- Explain the trade-offs between normalization and denormalization for specific use cases
- Discuss index strategy based on expected query volumes and patterns
- Consider operational complexity when proposing federation strategies
- Address both read and write performance implications of design decisions

**Red Flags:**

- Proposing normalized designs for all scenarios without considering performance
- Creating indexes without understanding query patterns
- Suggesting federation without clear functional boundaries
- Not considering transaction requirements across federated databases
- Ignoring operational complexity of proposed database architectures