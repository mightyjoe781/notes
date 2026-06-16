# Window Functions

Window functions compute a value across a set of rows related to the current row - without collapsing rows like `GROUP BY` does. Each input row keeps its own output row.

```sql
function() OVER (
    PARTITION BY col      -- defines the window (optional)
    ORDER BY col          -- defines ordering within window (optional)
    ROWS/RANGE BETWEEN .. -- defines the frame (optional)
)
```

## Ranking Functions

```sql
ROW_NUMBER()   -- unique sequential number, no ties
RANK()         -- ties get same rank, next rank skips (1,1,3)
DENSE_RANK()   -- ties get same rank, no skipping (1,1,2)
NTILE(n)       -- divides into n buckets, returns bucket number
```

```sql
SELECT
    user_id,
    session_start,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY session_start) AS rn,
    RANK()       OVER (PARTITION BY user_id ORDER BY session_start) AS rnk,
    DENSE_RANK() OVER (PARTITION BY user_id ORDER BY session_start) AS dense_rnk
FROM sessions;
```

**First record per group** - the most common interview pattern:

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY session_start) AS rn
    FROM sessions
)
SELECT * FROM ranked WHERE rn = 1;
```

## Navigation Functions

```sql
LAG(col, offset, default)   -- value from a previous row
LEAD(col, offset, default)  -- value from a following row
FIRST_VALUE(col)            -- first value in window frame
LAST_VALUE(col)             -- last value in window frame (watch frame boundary)
NTH_VALUE(col, n)           -- nth value in window frame
```

```sql
SELECT
    user_id,
    session_start,
    LAG(session_start, 1)  OVER (PARTITION BY user_id ORDER BY session_start) AS prev_session,
    LEAD(session_start, 1) OVER (PARTITION BY user_id ORDER BY session_start) AS next_session
FROM sessions;
```

Gap between sessions:

```sql
SELECT
    user_id,
    session_start,
    session_start - LAG(session_start) OVER (PARTITION BY user_id ORDER BY session_start) AS gap
FROM sessions;
```

## Aggregate as Window Functions

Any aggregate can become a window function by adding `OVER`:

```sql
SELECT
    user_id,
    amount,
    SUM(amount)   OVER (PARTITION BY user_id ORDER BY txn_date) AS running_total,
    AVG(amount)   OVER (PARTITION BY user_id ORDER BY txn_date) AS running_avg,
    COUNT(*)      OVER (PARTITION BY user_id)                   AS total_sessions,
    MAX(amount)   OVER (PARTITION BY user_id)                   AS user_max
FROM transactions;
```

Without `ORDER BY` in OVER, the aggregate applies to the whole partition:

```sql
-- total per user attached to every row
SELECT user_id, amount, SUM(amount) OVER (PARTITION BY user_id) AS user_total
FROM transactions;
```

## Frame Clause

The frame defines which rows within the partition are included in the calculation relative to the current row. Only meaningful when `ORDER BY` is present.

```
ROWS  BETWEEN start AND end   -- physical rows
RANGE BETWEEN start AND end   -- logical range (by value)
```

Frame boundaries:

```
UNBOUNDED PRECEDING   -- first row of partition
n PRECEDING           -- n rows before current
CURRENT ROW
n FOLLOWING           -- n rows after current
UNBOUNDED FOLLOWING   -- last row of partition
```

Default frame when ORDER BY is present: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`

```sql
-- 7-day moving average
SELECT
    date,
    revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM daily_revenue;
```

```sql
-- running total (explicit frame)
SUM(amount) OVER (PARTITION BY user_id ORDER BY txn_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

`LAST_VALUE` gotcha - default frame stops at current row, so LAST_VALUE is just the current row. Fix:

```sql
LAST_VALUE(col) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
```

## Common Patterns

**Deduplication** - keep the latest record per key:

```sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) AS rn
    FROM users
)
SELECT * FROM ranked WHERE rn = 1;
```

**Running total / cumulative sum**:

```sql
SELECT date, revenue, SUM(revenue) OVER (ORDER BY date) AS cumulative
FROM daily_revenue;
```

**Percent of total per group**:

```sql
SELECT
    dept,
    salary,
    salary * 1.0 / SUM(salary) OVER (PARTITION BY dept) AS pct_of_dept
FROM employees;
```

**Sessionization** - group events into sessions (gap > 30 min = new session):

```sql
WITH gaps AS (
    SELECT *,
        CASE WHEN event_time - LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time)
                  > INTERVAL '30 minutes'
             THEN 1 ELSE 0 END AS new_session_flag
    FROM events
),
sessions AS (
    SELECT *, SUM(new_session_flag) OVER (PARTITION BY user_id ORDER BY event_time) AS session_id
    FROM gaps
)
SELECT user_id, session_id, MIN(event_time) AS start, MAX(event_time) AS end
FROM sessions
GROUP BY user_id, session_id;
```

**Median** (no built-in in most DBs, use PERCENTILE_CONT):

```sql
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees;
```

## PySpark Equivalents

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# window spec
w = Window.partitionBy("user_id").orderBy("session_start")
w_unbounded = w.rowsBetween(Window.unboundedPreceding, Window.currentRow)

# ranking
df.withColumn("rn",         F.row_number().over(w))
df.withColumn("rnk",        F.rank().over(w))
df.withColumn("dense_rnk",  F.dense_rank().over(w))
df.withColumn("ntile",      F.ntile(4).over(w))

# navigation
df.withColumn("prev", F.lag("session_start", 1).over(w))
df.withColumn("next", F.lead("session_start", 1).over(w))

# aggregates
df.withColumn("running_total", F.sum("amount").over(w_unbounded))
df.withColumn("user_total",    F.sum("amount").over(Window.partitionBy("user_id")))

# 7-day moving window (by rows)
w7 = Window.orderBy("date").rowsBetween(-6, 0)
df.withColumn("moving_avg", F.avg("revenue").over(w7))
```

**First record per group in PySpark**:

```python
w = Window.partitionBy("user_id").orderBy("session_start")
first_sessions = (
    df.withColumn("rn", F.row_number().over(w))
      .filter(F.col("rn") == 1)
      .drop("rn")
)
```

## When to Use Window vs GROUP BY

| Need | Use |
|------|-----|
| Aggregate + keep all rows | Window function |
| Aggregate + collapse rows | GROUP BY |
| First/last per group | Window + ROW_NUMBER |
| Running total | Window + SUM OVER ORDER BY |
| Compare row to previous row | LAG / LEAD |
| Rank within group | RANK / DENSE_RANK |
| Percent within group | Window aggregate |

## Execution Order

Window functions execute after WHERE, GROUP BY, and HAVING - but before the outer SELECT and ORDER BY. This means:

- You cannot filter on a window function result in the same query's WHERE - wrap it in a CTE or subquery.
- You can ORDER BY a window function result.
