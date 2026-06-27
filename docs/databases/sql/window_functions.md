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

## PySpark Window Transformations

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window
```

### Window Spec Building Blocks

```python
# partition only - aggregate over whole partition
w_part = Window.partitionBy("user_id")

# partition + order - running calculations, ranking, lag/lead
w_ord = Window.partitionBy("user_id").orderBy("event_time")

# partition + order + frame (physical rows)
w_running  = Window.partitionBy("user_id").orderBy("event_time") \
                   .rowsBetween(Window.unboundedPreceding, Window.currentRow)
w_trailing = Window.partitionBy("user_id").orderBy("event_time") \
                   .rowsBetween(-6, 0)           # last 7 rows including current
w_full     = Window.partitionBy("user_id").orderBy("event_time") \
                   .rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)

# no partition - whole dataset as one window (avoid on large data)
w_global = Window.orderBy("event_time")
```

### Ranking

```python
w = Window.partitionBy("dept").orderBy(F.desc("salary"))

df.withColumn("row_num",    F.row_number().over(w))   # unique, no ties
  .withColumn("rank",       F.rank().over(w))          # ties get same rank, gaps after
  .withColumn("dense_rank", F.dense_rank().over(w))    # ties get same rank, no gaps
  .withColumn("quartile",   F.ntile(4).over(w))        # bucket 1-4
  .withColumn("pct_rank",   F.percent_rank().over(w))  # 0.0 to 1.0
```

**Top N per group:**

```python
w = Window.partitionBy("dept").orderBy(F.desc("salary"))

top3 = (
    df.withColumn("rnk", F.dense_rank().over(w))
      .filter(F.col("rnk") <= 3)
      .drop("rnk")
)
```

**Deduplication - keep latest record per key:**

```python
w = Window.partitionBy("customer_id").orderBy(F.desc("updated_at"))

deduped = (
    df.withColumn("rn", F.row_number().over(w))
      .filter(F.col("rn") == 1)
      .drop("rn")
)
```

### Navigation - LAG / LEAD

```python
w = Window.partitionBy("user_id").orderBy("event_time")

df.withColumn("prev_event",  F.lag("event_type", 1).over(w))          # previous row
  .withColumn("next_event",  F.lead("event_type", 1).over(w))         # next row
  .withColumn("prev_2",      F.lag("event_type", 2, "none").over(w))  # 2 rows back, default "none"
  .withColumn("first_event", F.first("event_type").over(w))           # first in partition up to current row
  .withColumn("last_event",  F.last("event_type").over(w_full))       # last in full partition
```

**Time gap between events:**

```python
w = Window.partitionBy("user_id").orderBy("event_time")

df.withColumn("prev_time", F.lag("event_time", 1).over(w)) \
  .withColumn("gap_seconds",
      (F.col("event_time").cast("long") - F.col("prev_time").cast("long")))
```

**Detect changes (changed vs previous row):**

```python
w = Window.partitionBy("customer_id").orderBy("updated_at")

changed = (
    df.withColumn("prev_city", F.lag("city", 1).over(w))
      .withColumn("city_changed",
          F.when(F.col("city") != F.col("prev_city"), True).otherwise(False))
)
```

This is the foundation of SCD2 change detection in a pipeline.

### Running and Cumulative Aggregates

```python
w_run = Window.partitionBy("user_id").orderBy("txn_date") \
              .rowsBetween(Window.unboundedPreceding, Window.currentRow)

df.withColumn("running_total",   F.sum("amount").over(w_run))
  .withColumn("running_count",   F.count("*").over(w_run))
  .withColumn("running_avg",     F.avg("amount").over(w_run))
  .withColumn("running_max",     F.max("amount").over(w_run))
  .withColumn("running_min",     F.min("amount").over(w_run))
```

**Running balance (credits positive, debits negative):**

```python
w = Window.partitionBy("account_id").orderBy("txn_timestamp") \
          .rowsBetween(Window.unboundedPreceding, Window.currentRow)

df.withColumn("balance", F.sum("signed_amount").over(w))
```

**Find accounts that ever went negative:**

```python
w = Window.partitionBy("account_id").orderBy("txn_timestamp") \
          .rowsBetween(Window.unboundedPreceding, Window.currentRow)

ever_negative = (
    df.withColumn("balance", F.sum("signed_amount").over(w))
      .groupBy("account_id")
      .agg(F.min("balance").alias("min_balance"))
      .filter(F.col("min_balance") < 0)
)
```

### Moving / Rolling Window

```python
# 7-row trailing (physical rows - use when dates may have gaps)
w7_rows = Window.partitionBy("store_id").orderBy("date").rowsBetween(-6, 0)

# 7-day trailing (range-based - only works cleanly when date col is numeric/timestamp)
w7_range = Window.partitionBy("store_id").orderBy("date_int").rangeBetween(-6, 0)

df.withColumn("ma_7d",  F.avg("revenue").over(w7_rows))
  .withColumn("sum_7d", F.sum("revenue").over(w7_rows))
  .withColumn("max_7d", F.max("revenue").over(w7_rows))
```

**Centered moving average (3-row: 1 before, current, 1 after):**

```python
w_centered = Window.partitionBy("store_id").orderBy("date").rowsBetween(-1, 1)
df.withColumn("centered_ma", F.avg("revenue").over(w_centered))
```

### Partition-Wide Aggregates (no ORDER BY)

```python
w_part = Window.partitionBy("dept")

df.withColumn("dept_total",   F.sum("salary").over(w_part))
  .withColumn("dept_avg",     F.avg("salary").over(w_part))
  .withColumn("dept_count",   F.count("*").over(w_part))
  .withColumn("pct_of_dept",  F.col("salary") / F.sum("salary").over(w_part))
```

**Ratio to group total:**

```python
w = Window.partitionBy("category")

result = (
    df.withColumn("category_total", F.sum("revenue").over(w))
      .withColumn("share", F.round(F.col("revenue") / F.col("category_total"), 4))
)
```

### Sessionization

Group events into sessions where gap > 30 minutes = new session:

```python
w = Window.partitionBy("user_id").orderBy("event_time")

sessionized = (
    df.withColumn("prev_time", F.lag("event_time", 1).over(w))
      .withColumn("gap_sec",
          F.col("event_time").cast("long") - F.col("prev_time").cast("long"))
      .withColumn("new_session",
          F.when(F.col("gap_sec") > 1800, 1).otherwise(0))
      .withColumn("session_id",
          F.sum("new_session").over(
              Window.partitionBy("user_id").orderBy("event_time")
                    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
          ))
)

# aggregate sessions
sessions = (
    sessionized.groupBy("user_id", "session_id")
               .agg(
                   F.min("event_time").alias("session_start"),
                   F.max("event_time").alias("session_end"),
                   F.count("*").alias("event_count"),
                   F.first("event_type").alias("first_event"),
                   F.last("event_type").alias("last_event"),
               )
)
```

### Gaps and Islands (Consecutive Streaks)

Consecutive days with activity per user:

```python
from pyspark.sql.functions import datediff, lit

w = Window.partitionBy("user_id").orderBy("login_date")

streaks = (
    df.withColumn("rn", F.row_number().over(w))
      .withColumn("grp",
          F.datediff("login_date", F.expr("date_add('1970-01-01', rn - 1)")))
      # rows in the same streak share the same grp value
      .groupBy("user_id", "grp")
      .agg(
          F.count("*").alias("streak_len"),
          F.min("login_date").alias("streak_start"),
          F.max("login_date").alias("streak_end"),
      )
)

longest = streaks.groupBy("user_id").agg(F.max("streak_len").alias("longest_streak"))
```

### SCD2 Change Detection Pipeline

Full incremental SCD2 pattern - detect what changed, expire old rows, insert new:

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import hashlib

# step 1: compute hash of all tracked attributes to detect changes cheaply
incoming = (
    source_df.withColumn(
        "row_hash",
        F.md5(F.concat_ws("|", F.col("city"), F.col("segment"), F.col("tier")))
    )
)

# step 2: join incoming to current records
current = spark.read.format("delta").load("/data/dim_customer") \
               .filter(F.col("is_current") == True)

joined = incoming.alias("s").join(
    current.alias("t"),
    on="customer_id",
    how="full_outer"
)

# step 3: classify each row
changed = joined.withColumn("action",
    F.when(F.col("t.customer_id").isNull(), "insert")           # new customer
     .when(F.col("s.customer_id").isNull(), "no_change")        # not in source (handle separately)
     .when(F.col("s.row_hash") != F.col("t.row_hash"), "update")# attributes changed
     .otherwise("no_change")
)

# step 4: expire old rows for changed customers
to_expire = (
    changed.filter(F.col("action") == "update")
           .select(F.col("t.surrogate_key"), F.current_date().alias("valid_to"))
)

# step 5: insert new versions
to_insert = (
    changed.filter(F.col("action").isin("insert", "update"))
           .select(
               F.col("s.customer_id"),
               F.col("s.city"),
               F.col("s.segment"),
               F.col("s.tier"),
               F.current_date().alias("valid_from"),
               F.lit(None).cast("date").alias("valid_to"),
               F.lit(True).alias("is_current"),
               F.col("s.row_hash"),
           )
)
```

### FIRST_VALUE / LAST_VALUE

```python
w_full = Window.partitionBy("user_id").orderBy("event_time") \
               .rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)

w_run  = Window.partitionBy("user_id").orderBy("event_time") \
               .rowsBetween(Window.unboundedPreceding, Window.currentRow)

df.withColumn("first_event_ever", F.first("event_type").over(w_run))
  .withColumn("last_event_ever",  F.last("event_type").over(w_full))
  # NOTE: last() without full frame gives last value seen so far, not partition last
```

### NTH_VALUE / NTILE

```python
w = Window.partitionBy("dept").orderBy(F.desc("salary"))
w_full = w.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)

df.withColumn("second_highest", F.nth_value("salary", 2).over(w_full))
  .withColumn("quartile",       F.ntile(4).over(w))
```

### Quick Reference

| SQL function | PySpark |
|---|---|
| `ROW_NUMBER()` | `F.row_number().over(w)` |
| `RANK()` | `F.rank().over(w)` |
| `DENSE_RANK()` | `F.dense_rank().over(w)` |
| `NTILE(n)` | `F.ntile(n).over(w)` |
| `PERCENT_RANK()` | `F.percent_rank().over(w)` |
| `LAG(col, n)` | `F.lag("col", n).over(w)` |
| `LEAD(col, n)` | `F.lead("col", n).over(w)` |
| `FIRST_VALUE(col)` | `F.first("col").over(w)` |
| `LAST_VALUE(col)` | `F.last("col").over(w)` |
| `NTH_VALUE(col, n)` | `F.nth_value("col", n).over(w)` |
| `SUM() OVER (...)` | `F.sum("col").over(w)` |
| `AVG() OVER (...)` | `F.avg("col").over(w)` |
| `COUNT() OVER (...)` | `F.count("col").over(w)` |
| `MIN() OVER (...)` | `F.min("col").over(w)` |
| `MAX() OVER (...)` | `F.max("col").over(w)` |
| `ROWS BETWEEN n PRECEDING AND CURRENT ROW` | `.rowsBetween(-n, 0)` |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | `.rowsBetween(Window.unboundedPreceding, Window.currentRow)` |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | `.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)` |

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

## Problem Patterns

Most window function problems map to one of these recurring shapes. Recognizing the shape gives you the query structure immediately.

| Pattern | Signal words | Functions |
|---------|-------------|-----------|
| First/last per group | "first order", "most recent", "earliest" | ROW_NUMBER |
| Ranking within group | "top N per category", "rank employees" | RANK, DENSE_RANK |
| Running aggregate | "cumulative", "running total", "YTD" | SUM/COUNT OVER ORDER BY |
| Moving window | "7-day average", "rolling", "trailing N" | SUM/AVG OVER ROWS BETWEEN |
| Row comparison | "change from previous", "growth", "diff" | LAG, LEAD |
| Gaps and islands | "consecutive", "streaks", "sessions" | ROW_NUMBER difference trick |
| Percentile / distribution | "top 10%", "median", "quartile" | NTILE, PERCENTILE_CONT |
| Ratio within group | "% of total", "share", "contribution" | SUM OVER PARTITION (no ORDER BY) |

**Gaps and islands** deserves its own explanation - it comes up constantly in DE interviews:

```sql
-- consecutive login days per user
-- idea: if logins are consecutive, (date - ROW_NUMBER) is constant within each streak
WITH ranked AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM logins
),
grouped AS (
    SELECT user_id, login_date,
           login_date - rn * INTERVAL '1 day' AS grp   -- constant within a streak
    FROM ranked
)
SELECT user_id, grp, COUNT(*) AS streak_len,
       MIN(login_date) AS streak_start, MAX(login_date) AS streak_end
FROM grouped
GROUP BY user_id, grp
ORDER BY user_id, streak_start;
```

## Worked Examples

### Q1 - Streaming sessions (first session as viewer)

Find users whose first session was as a Viewer. Return user_id and total session count, ordered by count desc, user_id desc.

```sql
WITH ranked AS (
    SELECT user_id, session_type,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY session_start) AS rn
    FROM sessions
),
first_viewers AS (
    SELECT user_id FROM ranked WHERE rn = 1 AND session_type = 'Viewer'
)
SELECT s.user_id, COUNT(*) AS streaming_sessions_count
FROM sessions s
JOIN first_viewers fv ON s.user_id = fv.user_id
GROUP BY s.user_id
ORDER BY streaming_sessions_count DESC, s.user_id DESC;
```

Pattern: **first per group** - ROW_NUMBER to tag rn=1, filter, join back.

### Q2 - Department salary ranking

For each employee show their salary rank within their department. Show top 3 earners per dept.

```sql
WITH ranked AS (
    SELECT name, dept, salary,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT * FROM ranked WHERE rnk <= 3;
```

Pattern: **top N per group** - DENSE_RANK (not RANK, to avoid gaps; not ROW_NUMBER, to handle ties correctly).

### Q3 - Month-over-month revenue growth

For each month, show revenue and % growth vs previous month.

```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(amount) AS revenue
    FROM orders
    GROUP BY 1
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
        / LAG(revenue) OVER (ORDER BY month), 2
    ) AS pct_growth
FROM monthly
ORDER BY month;
```

Pattern: **row comparison** - LAG to pull previous row's value.

### Q4 - Running balance

For each user, show each transaction and their running account balance.

```sql
SELECT
    user_id,
    txn_date,
    amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY txn_date
                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance
FROM transactions
ORDER BY user_id, txn_date;
```

Pattern: **running aggregate** with explicit ROWS frame (safer than RANGE when duplicate dates are possible).

### Q5 - Longest login streak per user

```sql
WITH daily AS (
    SELECT DISTINCT user_id, DATE(login_time) AS login_date FROM logins
),
ranked AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM daily
),
grouped AS (
    SELECT user_id, login_date,
           login_date - (rn * INTERVAL '1 day')::date AS grp
    FROM ranked
)
SELECT user_id, MAX(streak) AS longest_streak
FROM (
    SELECT user_id, grp, COUNT(*) AS streak FROM grouped GROUP BY user_id, grp
) t
GROUP BY user_id;
```

Pattern: **gaps and islands** - date minus row number gives a constant group key for consecutive sequences.

## Practice Problems

Try these without looking at solutions. The pattern label is a hint.

1. **(First per group)** Leetcode 185 - Department Top Three Salaries. Find employees who earn one of the top three unique salaries in their department.

2. **(Row comparison)** Given a `temperatures` table with `(id, recordDate, temperature)`, find all dates where temperature was higher than the previous day. (Leetcode 197)

3. **(Gaps and islands)** Given a `tasks` table with `(task_id, status, updated_at)`, find all tasks that had 3 or more consecutive status updates of `'failed'` within the same day.

4. **(Running aggregate)** You have `transactions(account_id, txn_date, amount)`. Find all accounts that went negative at any point in their running balance history.

5. **(Moving window)** Given `page_views(date, views)`, compute a 3-day centered moving average (1 preceding, current, 1 following).

6. **(Sessionization)** Given `events(user_id, event_time, event_type)`, define a session as a sequence of events with no gap > 30 minutes. For each session, find the first and last event type. (This is the DE interview most common question.)

7. **(Hard - combined)** Leetcode 615 - Average Salary: Departments VS Company. For each month, compare each department's average salary vs the company-wide average. Return departments that were above average.

8. **(Hard - gaps and islands)** Given `stock_prices(date, price)`, find the longest streak of consecutive days where price increased each day.

## Window Functions in PySpark - Issues and Trade-offs

### How Spark Executes Window Functions

Spark must **shuffle all data for a given partition key to the same executor** before it can compute the window. This is similar to a wide transformation (like a join or groupBy). The result:

- Window functions always trigger a shuffle (even with PARTITION BY).
- Without PARTITION BY, the entire dataset goes to a single executor - this will OOM on large data.

### Common Issues

**Skew** - if one partition key has vastly more rows than others (e.g., `user_id = -1` is a catch-all for anonymous users), that executor gets overwhelmed while others are idle. Signs: one task takes 100x longer than rest.

```python
# bad - anonymous users all go to one executor
w = Window.partitionBy("user_id").orderBy("event_time")

# fix: either filter out skewed keys first, or add a salt bucket
df_no_anon = df.filter(F.col("user_id") != -1)
```

**Unbounded window without PARTITION BY** - this sends all data to one task. Avoid entirely on large datasets.

```python
# dangerous on large data - whole dataset to one task
w = Window.orderBy("date")
df.withColumn("running_total", F.sum("amount").over(w))  # OOM risk
```

**Multiple window specs on the same DataFrame** - each distinct window spec is a separate shuffle stage. Computing 3 different windows = 3 shuffles.

```python
# 3 shuffles - expensive
w1 = Window.partitionBy("user_id").orderBy("date")
w2 = Window.partitionBy("dept").orderBy("salary")
w3 = Window.partitionBy("region")

df.withColumn("a", F.row_number().over(w1)) \
  .withColumn("b", F.rank().over(w2)) \
  .withColumn("c", F.sum("amount").over(w3))

# better: group operations with same window spec together, cache intermediate results
```

**Frame with RANGE on non-integer types** - Spark supports `RANGE` frames only on numeric and timestamp types. Using it on strings or other types fails at runtime.

**`rangeBetween` vs `rowsBetween`** - in Spark, RANGE frames can produce surprising results when there are duplicate values in the ORDER BY column (all duplicates are treated as tied, expanding the frame). Prefer `rowsBetween` for deterministic results.

```python
# rowsBetween is usually what you want - physical rows
w = Window.partitionBy("user_id").orderBy("date").rowsBetween(-6, 0)

# rangeBetween uses value range - tricky with duplicates
w = Window.partitionBy("user_id").orderBy("date").rangeBetween(-6, 0)
```

### Pros and Cons

**Pros:**

- Expressive - operations like running totals, rankings, and lag/lead that would require self-joins are a single function call.
- Preserves row granularity - you get the aggregated value alongside the original row without needing a join back.
- Composable - multiple window specs can be computed in one pass over the data.
- In SQL, often more readable than equivalent self-join approaches.

**Cons:**

- Always triggers a shuffle in Spark - cannot be pushed down past a filter (no predicate pushdown through window).
- Memory pressure - executor must buffer the entire partition in memory to sort and compute the frame.
- No PARTITION BY = full dataset on one node - dangerous.
- Skew amplification - uneven partition sizes cause stragglers.
- Multiple distinct window specs = multiple shuffle stages - can be slower than a single aggregation + join approach for simpler cases.
- Ordering within a partition is non-deterministic if ties exist in the ORDER BY column (especially with ROW_NUMBER).

### When to Avoid Window Functions in Spark

- When you only need a group-level aggregate (use `groupBy().agg()` + join - one shuffle vs one shuffle, but avoids per-row overhead).
- When the partition cardinality is very low (e.g., PARTITION BY country with 5 countries - you get 5 tasks max, parallelism is wasted).
- When the dataset is too skewed to partition cleanly - pre-filter or pre-aggregate first.
- For simple dedup, `dropDuplicates()` is faster than ROW_NUMBER + filter.
