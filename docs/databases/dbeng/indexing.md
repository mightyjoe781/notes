# Database Indexing


### Table Creation

Create a Postgres Table with a million rows (from scratch)

```postgresql
-- Step 1: Create table
CREATE TABLE my_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    value INTEGER
);

-- Step 2: Insert a million rows efficiently
-- Using generate_series for bulk insertion
INSERT INTO my_table (name, value)
SELECT
    'Name' || gs,
    (random() * 1000)::int
FROM generate_series(1, 1000000) AS gs;

```

### Indexing Basics

Index ~ data structure on top of table providing quick access to underlying table structure on some feature.

A query like `select * from my_table where id = 100` will be instant as its primary key is the index.

Run `explain analyze <sql_query>` to understand time statistics.
```postgresql
explain analyze select * from my_table where id = 1990; -- an index
-- Planning : 0.083ms
-- Execution : 2ms
```


Now lets run same query but instead search on different column which is not index 

```postgresql
explain analyze select * from my_table where name = 'Name7990'; -- not an index
-- Planning : 2.053ms
-- Execution : 3199 ms
```

| QUERY PLAN                                                               |
| ------------------------------------------------------------------------ |
| Gather  (cost=1000.00..35733.11 rows=1 width=11)                         |
| Workers Planned: 2                                                       |
| ->  Parallel Seq Scan on my_table  (cost=0.00..34733.01 rows=1 width=11) |
| Filter: ((name)::text = 'Name10'::text)                                  |

Now try same command again after creating index on name using `create index name on my_table(name)`

Now try analyze using `LIKE` query, notice how this query is not optimal even when index is present.

```
explain analyze select * from my_table where name like 'Name12%';
```

### SQL Query Planner & Optimizer

Run the following query :

```postgresql
explain analyze select * from my_table;
```

| QUERY PLAN                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------ |
| Seq Scan on my_table  (cost=0.00..16369.00 rows=1000000 width=18) (actual time=0.020..84.283 rows=1000000 loops=1) |
| Planning Time: 0.290 ms                                                                                            |
| Execution Time: 117.900 ms                                                                                         |

Seq Scan ~ sequential scan and postgres return entire table.
cost = (first_page...last_page) ~ total time to fetch data (statistics)
rows = (total number of rows) # this actually is faster than `select count(*)`
width ~ sum of all the bytes of all the rows

```postgresql
explain analyze select * from my_table order by id;
explain analyze select * from my_table order by name; -- not-index
```

| QUERY PLAN                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------- |
| Index Scan using my_table_pkey on my_table  (cost=0.42..32352.42 rows=1000000 width=18) (actual time=0.075..205.912 rows=1000000 loops=1) |
| Planning Time: 0.359 ms                                                                                                                   |
| Execution Time: 241.553 ms                                                                                                                |

Query Plan for non-indexed column being queries by using `order by`

| QUERY PLAN                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------- |
| Sort  (cost=136536.84..139036.84 rows=1000000 width=18) (actual time=1493.414..1751.711 rows=1000000 loops=1)          |
| Sort Key: name                                                                                                         |
| Sort Method: external merge  Disk: 29408kB                                                                             |
| ->  Seq Scan on my_table  (cost=0.00..16369.00 rows=1000000 width=18) (actual time=0.020..72.875 rows=1000000 loops=1) |
| Planning Time: 0.350 ms                                                                                                |
| Execution Time: 1792.246 ms                                                                                            |

notice how width is optimized as we stop using `*`

```postgresql
EXPLAIN (ANALYZE, VERBOSE) SELECT id FROM my_table;
EXPLAIN (ANALYZE, VERBOSE) SELECT name FROM my_table;
```

| QUERY PLAN                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------- |
| Seq Scan on public.my_table  (cost=0.00..49108.02 rows=3000002 width=4) (actual time=0.191..421.588 rows=3000002 loops=1) |
| JIT:<br>    Functions: 2<br>    Options: Inlining false, Optimization false, Expression True, Deforming true (4 rows)     |
|                                                                                                                           |

### Bitmap Index Scan vs Index Scan vs Table Scan


```postgresql
explain select name from my_table where id = 1000; -- index scan
explain select name from my_table where id < 100; -- index scan (optimal choice by postgresql)
explain select name from my_table where id > 100; -- seq scan based on table statistics

-- to see the bitmap index scan ~ create index first on value
CREATE INDEX value_idx ON my_table (value);
ANALYZE my_table;
EXPLAIN ANALYZE SELECT * FROM my_table WHERE value BETWEEN 100 AND 200; -- triggers bigtmap Heap Scan
```

| QUERY PLAN                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------- |
| Bitmap Heap Scan on my_table  (cost=4075.70..27643.13 rows=297295 width=19) (actual time=28.160..259.748 rows=302585 loops=1) |
| Recheck Cond: ((value >= 100) AND (value <= 200))                                                                             |
| Heap Blocks: exact=19108                                                                                                      |
| ->  Bitmap Index Scan on value_idx  (cost=0.00..4001.38 rows=297295 width=0) (actual time=23.915..23.916 rows=302585 loops=1) |
| Index Cond: ((value >= 100) AND (value <= 200))                                                                               |
| Planning Time: 0.735 ms                                                                                                       |
| Execution Time: 272.274 ms                                                                                                    |
It keeps a BitMap in memory and marks a bit for each page where it finds matching rows and then brings those pages rather than entire table.

```postgresql
EXPLAIN ANALYZE SELECT * FROM my_table WHERE value BETWEEN 100 AND 200 and id < 200; -- notice how it doesn 'and' operation for both bitmaps
```

### Key vs Non-Key Column Database Indexing

- Key Index ~ contains the index column and reference to actual data in table.
- Non-Key Column Index allows you to include other fields in indexes (PostgreSQL allows this)

```postgresql
explain analyze select id, g from students where g > 80 and g < 95 order by g desc
```

With Key-Index on id above query takes 30-40 seconds for 5 Million records. Because it fetched a lot of pages only to be excluded,
Here we can include g(grade) column in index to make this query fast.

```postgresql
create index g_idx on students(g);
```

```postgresql
explain (analyze, buffer) select id, g from students where g > 80 and g < 95 order by g desc
-- this still take a lot of time, because it needs to go to do backward indexing scan on g column, then it does reverse mapping for ids
```

~ Having two Key-Indexes didn't help much, to perform a Key only index scan, we can do something like this.

```postgresql
drop index g_idx;
create index g_idx on students(g) include(id);
```

Now running the same query blazingly fast and read small amount of heap.

NOTE: Running the same query twice actually triggers cache, make second executions quite fast for a table.

### Index Scan vs Index Only Scan

```postgresql
explain analyze select name from my_table where id = 9; -- does slow sequential scan, quickly finds the scanned id, and then fetched row from the heap space.
-- INDEX SCAN

explain analyze select id from my_table where id = 9; -- does slow sequential scan, quickly finds the scanned id, and then fetched index only.
-- INDEX ONLY SCAN
```

~ if our most of the queries are about the name from the table, we can modify our index to avoid going into heap space

```postgresql
drop index id_idx;
create index id_idx on grades(id) include(name);
explain analyze select name from my_table where id = 9;
-- INDEX ONLY SCAN :)
```

### Combining Indexes for Better Performance

Assume a table with three column `a, b, c` all integers. Insert 100 million random integers

```postgresql
create index on test(a);
create index on test(b);

explain analyze select c from test where a = 70; -- BITMAP HEAP Scan, Bitmap Index Scan

explain analyze select c from test where b = 1000; -- BITMAP HEAP Scan, Bitmap Index Scan

explain analyze select c from test where a = 100 and b = 100; -- AND of two Bitmaps

explain analyze select c from test where a = 100 or b = 100; -- OR of two Bitmaps -- takes more time than AND :)

drop index test_a_idx, test_b_idx;
create index on test(a, b); -- composite index ~ longer to create

explain analyze select c from test where a = 70; -- BitMap Heap Index on test_a_b (because its on left side, postgres can compare)

explain analyze select c from test where b = 70; -- BitMap Heap Index on test_a_b ~ Parallel Sequential Scan

explain analyze select c from test where a = 70 AND b = 70; -- BitMap Heap Index on test_a_b ~ Index Scan, superfast

explain analyze select c from test where a = 70 OR b = 70; -- BitMap Heap Index on test_a_b ~ Parallel Sequential Scans for OR
```

Now lets create a additional index `b`

```postgresql
create index on test(b)

explain analyze select c from test where a = 70; -- Index Scan
explain analyze select c from test where b = 70; -- Index Scan
explain analyze select c from test where a = 70 AND b = 70; -- Index Scan
explain analyze select c from test where a = 70 OR b = 70; -- Index Scans and Uses OR Bitmap Operations
```

### Create Index Concurrently 

~ Avoiding Production Database Writes freezes

```postgresql
create index concurrently g on grades(g);
```

### Bloom Filters

- Probabilistic Data Structure that gives negative queries with 100% certainty but positive queries with a *maybe*, with a very small space.
- We can revert predicate that is fed into bloom filter to get inverted probability guarantees from above definition.
- *Redis provides built-in support for it, Cassandra uses it all the time in its internals.*
- Video Explanation : https://www.youtube.com/watch?v=kfFacplFY4Y

### Working with Billion - Row Table

- We can bruteforce our way with Billion Rows table using distributed computing engines like *spark*, but indexing correctly gives huge gains if done correctly.
- Partitioning correctly here might help us as well, NOTE: Partitioning is physically division of blocks of data based on the key and its different from indexing.
- We could shard and add it to multiple machines to get redundancy, but it complicates the transactions, and all distributed computed problem come into picture.
- Or alternatively redesign using smaller tables :) rethink about design
### How UUIDs in B+ Tree Indexes affect performances

- randomness in general hurts inserts
- Having things out of order creates new leaves in the b-tree and then moving the data around to maintain tree property, but if keys are in order then the tree rebalancing is not done often.
* Try this app, and use random inserts and then ordered inserts : https://btree.app/
* Use later versions of UUIDs which are in order like 7 or 8 or ULID
* NOTE: even if you pass UUIDs in hash keys in dynamo DB, it anyways hashes them removing this issue.


NOTE: 

- If a long transaction that has updated millions of rows rolls back, then the new row versions created by this transaction (million in this specific case) are now invalid and should NOT be read by any new transaction.
- Postgres executes a command called `vacuum` which is called periodically. Postgres attempts to remove dead rows and free up space on the page.
- This actually help DB maintain the pages with latest rows and remove stale version which might be fetched during reads.


Exercise

- database hinting ~ give hints to database query planner to explicitly trigger index scans.