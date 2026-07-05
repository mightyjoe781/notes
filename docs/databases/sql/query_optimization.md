---
title: Query Optimization and EXPLAIN
description: Explains how to read PostgreSQL query plans, diagnose common performance problems (seq scans, bad join strategy, stale stats), and rewrite slow queries, plus PySpark's explain().
tags:
  - concept
---

# Query Optimization and EXPLAIN

## How a Query Gets Executed

```
SQL text -> Parser -> Query Rewriter -> Planner/Optimizer -> Executor
```

The **planner** generates multiple possible execution plans and picks the cheapest one based on table statistics (row counts, column cardinality, data distribution). Understanding what the planner chose - and why - lets you fix slow queries.

## EXPLAIN

`EXPLAIN` shows the query plan without executing the query. `EXPLAIN ANALYZE` actually runs it and shows real timing.

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 101;

EXPLAIN ANALYZE
SELECT o.order_id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.created_at > '2024-01-01';
```

## Reading a Query Plan (PostgreSQL)

Plans are trees - read from innermost (bottom) to outermost (top). Each node shows the operation, estimated vs actual rows, and cost.

```
Gather  (cost=1000.42..18523.58 rows=438 width=36) (actual time=1.234..89.432 rows=450)
  Workers Planned: 2
  ->  Hash Join  (cost=1000.42..18523.58 rows=183 width=36)
        Hash Cond: (o.customer_id = c.customer_id)
        ->  Parallel Seq Scan on orders  (cost=0..15000 rows=183 width=28)
              Filter: (created_at > '2024-01-01')
        ->  Hash  (cost=850..850 rows=10000 width=16)
              ->  Seq Scan on customers  (cost=0..850 rows=10000 width=16)
```

**Cost format:** `(startup cost..total cost)` - startup is time to first row, total is time to last row. Units are arbitrary but comparable within the same plan.

**Key node types:**

| Node | Meaning |
|------|---------|
| `Seq Scan` | Full table scan - reads every row |
| `Index Scan` | Uses index, reads heap for each match |
| `Index Only Scan` | Uses index, doesn't touch heap (all needed columns in index) |
| `Bitmap Heap Scan` | Collects matching pages via bitmap then fetches heap - good for moderate selectivity |
| `Nested Loop` | For each row in outer, scan inner. Good when outer is small |
| `Hash Join` | Build hash table on smaller side, probe with larger. Good for large equi-joins |
| `Merge Join` | Both sides sorted, walk in parallel. Good when both sides already sorted |
| `Sort` | Explicit sort - expensive if spilling to disk |
| `Hash Aggregate` | GROUP BY using hash table |
| `Gather` | Parallel query - merge results from workers |

## Common Performance Problems

### Seq Scan when you expect an index

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 101;
-- shows: Seq Scan on orders (rows=1000000)
```

Causes:
- No index on `customer_id` - create one.
- Index exists but planner estimates a full scan is cheaper (query returns many rows, e.g. 50%+ of table). This is correct behavior.
- Column has a cast or function applied: `WHERE LOWER(email) = 'x'` won't use an index on `email`. Use a functional index or fix the query.

```sql
-- bad: index on email is useless here
WHERE LOWER(email) = 'alice@example.com'

-- good: use functional index
CREATE INDEX ON users (LOWER(email));
-- or fix the query to use the stored case
```

### Wrong join strategy

```sql
-- if you see Nested Loop with a large outer side, that's bad
-- force hash join for testing
SET enable_nestloop = off;
EXPLAIN ANALYZE <your query>;
```

### Row count misestimate

The planner's cost estimates are only as good as statistics. If `rows=10` but actual is `10000`, the planner chose the wrong plan based on stale/bad stats.

```sql
ANALYZE orders;                 -- update stats for one table
ANALYZE;                        -- update all tables
```

Correlations between columns fool the planner (e.g., filtering by both `city` and `zip_code` - they're not independent). Use extended statistics:

```sql
CREATE STATISTICS city_zip_stats ON city, zip_code FROM customers;
ANALYZE customers;
```

### Sort spilling to disk

```
Sort  (cost=...) (actual ... Batches=4)
```

`Batches > 1` means the sort spilled to disk. Fix by increasing `work_mem` for the session:

```sql
SET work_mem = '256MB';
EXPLAIN ANALYZE <your query>;
```

## Index Types and When to Use Them

```sql
-- B-tree (default): equality, range, ORDER BY, IS NULL
CREATE INDEX ON orders (customer_id);
CREATE INDEX ON orders (created_at);

-- Composite: covers queries filtering on both columns
-- column order matters - put equality-filtered column first
CREATE INDEX ON orders (customer_id, created_at);

-- Partial: index only a subset of rows (e.g., active records)
CREATE INDEX ON orders (customer_id) WHERE status = 'active';

-- Covering / include: stores extra columns in index to enable index-only scans
CREATE INDEX ON orders (customer_id) INCLUDE (order_total, status);

-- Hash: equality only, faster than B-tree for equality, can't do range
CREATE INDEX ON sessions USING hash (session_token);

-- GIN: full-text search, array containment, JSONB
CREATE INDEX ON articles USING gin (to_tsvector('english', body));

-- BRIN: very large tables with naturally ordered data (timestamps, IDs)
-- tiny index, good for append-only logs
CREATE INDEX ON events USING brin (event_time);
```

## Query Rewriting Patterns

**Push filters down - avoid filtering after aggregation when possible:**

```sql
-- slow: computes full join then filters
SELECT * FROM (
    SELECT o.*, c.country FROM orders o JOIN customers c ON o.customer_id = c.customer_id
) sub WHERE country = 'India';

-- better: filter before joining (if index on country exists)
SELECT o.*, c.country
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.country = 'India';
```

**Avoid SELECT * in subqueries - only pull columns you need.**

**Avoid correlated subqueries that run once per row - rewrite as a join:**

```sql
-- bad: correlated subquery, O(n) subquery executions
SELECT name, (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) AS order_count
FROM customers c;

-- good: one aggregation + join
SELECT c.name, COALESCE(o.order_count, 0)
FROM customers c
LEFT JOIN (
    SELECT customer_id, COUNT(*) AS order_count FROM orders GROUP BY customer_id
) o ON c.customer_id = o.customer_id;
```

**Use EXISTS instead of IN for large subquery results:**

```sql
-- IN materializes the full subquery result
WHERE customer_id IN (SELECT customer_id FROM vip_customers)

-- EXISTS short-circuits on first match
WHERE EXISTS (SELECT 1 FROM vip_customers v WHERE v.customer_id = c.customer_id)
```

## Useful PostgreSQL Commands

```sql
-- see all indexes on a table
\d orders

-- table size and index sizes
SELECT pg_size_pretty(pg_total_relation_size('orders'));
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass))
FROM pg_indexes WHERE tablename = 'orders';

-- find slow queries (requires pg_stat_statements extension)
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- find missing indexes (sequential scans on large tables)
SELECT relname, seq_scan, idx_scan
FROM pg_stat_user_tables
ORDER BY seq_scan DESC;

-- check last time stats were updated
SELECT relname, last_analyze, last_autoanalyze
FROM pg_stat_user_tables;
```

## Spark / Distributed EXPLAIN

In PySpark, use `.explain()` to see the physical plan:

```python
df.explain()           # default - physical plan
df.explain("extended") # logical + optimized logical + physical
df.explain("cost")     # includes cost estimates
df.explain("formatted") # formatted, easier to read
```

Key things to look for:

- `BroadcastHashJoin` vs `SortMergeJoin` - broadcast is faster when one side is small (< `spark.sql.autoBroadcastJoinThreshold`, default 10MB)
- `Exchange hashpartitioning` - a shuffle stage. Count the shuffles to understand stage boundaries.
- `FileScan` with `PushedFilters` - partition pruning and predicate pushdown are working if you see filters here
- `*(n)` prefix on node names - whole-stage code generation is active (good)

```python
# force broadcast join for testing
from pyspark.sql.functions import broadcast
df = large.join(broadcast(small), "key")

# see AQE runtime plan (after execution)
spark.conf.set("spark.sql.adaptive.enabled", "true")
```

## See Also
- [Database Indexing](../dbeng/indexing.md)
- [Understanding Database Internals](../dbeng/internals.md)
