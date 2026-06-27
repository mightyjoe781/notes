# Slowly Changing Dimensions (SCD) and MERGE

## What is a Dimension?

In a data warehouse, a **dimension** is a descriptive table - customers, products, employees. A **fact** table stores events/measurements that reference dimensions. The problem: real-world dimensions change over time. A customer moves cities, a product gets repriced. How you track that change is your SCD strategy.

## SCD Types

### Type 0 - Retain Original

Never update. The original value at load time is permanent. Rarely used; only when historical accuracy of the dimension doesn't matter (e.g., a customer's original signup country for auditing).

### Type 1 - Overwrite

Just update the row. No history kept.

```sql
UPDATE customers
SET city = 'Mumbai'
WHERE customer_id = 101;
```

- Simple, no history.
- Use when the old value is wrong (data correction) or history genuinely doesn't matter.
- All past facts now point to the new value when joined - history is rewritten.

### Type 2 - Add a New Row (most common in DE)

Keep the old row, insert a new row. Track which is current with a flag and validity dates.

Schema addition:

```sql
ALTER TABLE customers ADD COLUMN valid_from  DATE;
ALTER TABLE customers ADD COLUMN valid_to    DATE;    -- NULL means current
ALTER TABLE customers ADD COLUMN is_current  BOOLEAN;
ALTER TABLE customers ADD COLUMN surrogate_key SERIAL PRIMARY KEY;
```

| surrogate_key | customer_id | name  | city      | valid_from | valid_to   | is_current |
|---------------|-------------|-------|-----------|------------|------------|------------|
| 1             | 101         | Alice | Delhi     | 2022-01-01 | 2024-03-15 | false      |
| 2             | 101         | Alice | Mumbai    | 2024-03-15 | NULL       | true       |

Facts join to `surrogate_key`, not `customer_id`. A fact recorded in 2023 joins to row 1 (Delhi). A fact recorded in 2025 joins to row 2 (Mumbai). History is preserved exactly.

SCD2 insert logic (when a change arrives):

```sql
-- expire the current row
UPDATE customers
SET valid_to = CURRENT_DATE, is_current = false
WHERE customer_id = 101 AND is_current = true;

-- insert the new version
INSERT INTO customers (customer_id, name, city, valid_from, valid_to, is_current)
VALUES (101, 'Alice', 'Mumbai', CURRENT_DATE, NULL, true);
```

### Type 3 - Add a Column

Add a `previous_value` column. Tracks only one prior state.

```sql
ALTER TABLE customers ADD COLUMN prev_city VARCHAR(100);

UPDATE customers
SET prev_city = city, city = 'Mumbai'
WHERE customer_id = 101;
```

- Simple but limited - only one level of history.
- Use when you need "before and after" comparison but not full history.

### Type 4 - History Table

Keep the main table as current only, push old rows to a separate history table. Good when current lookups need to be fast and history is rarely queried.

```sql
-- before updating, archive to history
INSERT INTO customers_history SELECT *, CURRENT_TIMESTAMP AS archived_at FROM customers WHERE customer_id = 101;

-- then update current table
UPDATE customers SET city = 'Mumbai' WHERE customer_id = 101;
```

### Type 6 - Hybrid (1 + 2 + 3)

Combines types 1, 2, and 3. Each row has surrogate key + validity dates (Type 2) + a `current_value` column that's always updated in-place (Type 1) + a `prev_value` column (Type 3). Lets you query both the value at a point in time AND the current value from any historical row without a second join.

---

## MERGE / UPSERT

`MERGE` applies conditional INSERT/UPDATE/DELETE in a single statement. Critical for incremental loads and SCD implementations.

### Standard SQL MERGE

```sql
MERGE INTO target_table t
USING source_table s
ON t.id = s.id

WHEN MATCHED AND t.city != s.city THEN
    UPDATE SET city = s.city, updated_at = CURRENT_TIMESTAMP

WHEN NOT MATCHED THEN
    INSERT (id, name, city, created_at)
    VALUES (s.id, s.name, s.city, CURRENT_TIMESTAMP)

WHEN NOT MATCHED BY SOURCE THEN   -- row in target but not in source
    DELETE;                        -- optional, use carefully
```

### PostgreSQL - no MERGE before v15, use INSERT ON CONFLICT

```sql
INSERT INTO customers (customer_id, name, city)
VALUES (101, 'Alice', 'Mumbai')
ON CONFLICT (customer_id)
DO UPDATE SET
    city = EXCLUDED.city,
    updated_at = CURRENT_TIMESTAMP;
```

`EXCLUDED` refers to the row that was proposed for insertion.

### Delta Lake MERGE (used heavily in Databricks / PySpark)

```python
from delta.tables import DeltaTable

target = DeltaTable.forPath(spark, "/data/customers")

target.alias("t").merge(
    source_df.alias("s"),
    "t.customer_id = s.customer_id"
).whenMatchedUpdate(set={
    "city": "s.city",
    "updated_at": "current_timestamp()"
}).whenNotMatchedInsert(values={
    "customer_id": "s.customer_id",
    "name": "s.name",
    "city": "s.city",
    "created_at": "current_timestamp()"
}).execute()
```

### SCD2 with MERGE

Full SCD2 in one MERGE - expire old row and insert new:

```sql
-- Step 1: expire changed rows
MERGE INTO customers t
USING incoming_changes s
ON t.customer_id = s.customer_id AND t.is_current = true

WHEN MATCHED AND t.city != s.city THEN
    UPDATE SET valid_to = CURRENT_DATE, is_current = false;

-- Step 2: insert new versions for changed + new customers
INSERT INTO customers (customer_id, name, city, valid_from, valid_to, is_current)
SELECT s.customer_id, s.name, s.city, CURRENT_DATE, NULL, true
FROM incoming_changes s
LEFT JOIN customers t ON t.customer_id = s.customer_id AND t.is_current = true
WHERE t.customer_id IS NULL OR t.city != s.city;
```

Some databases let you do both in a single MERGE using a CTE to flag changed rows, then handling insert and update in separate WHEN clauses.

## SCD Type Comparison

| Type | History kept | Storage cost | Complexity | Use when |
|------|-------------|--------------|------------|----------|
| 0    | None        | Low          | None       | Immutable reference data |
| 1    | None        | Low          | Low        | Corrections, no history needed |
| 2    | Full        | High         | High       | Need point-in-time accuracy |
| 3    | One version | Medium       | Medium     | Only current vs previous matters |
| 4    | Full        | Medium       | Medium     | Fast current lookups + rare history access |
| 6    | Full        | High         | Highest    | Need both point-in-time and current from same row |

## Interview Pattern

You'll be given a scenario and asked which SCD type to use. Rule of thumb:

- "Track the full history" or "how many cities has a customer lived in" -> Type 2
- "Fix a data error, old value was wrong" -> Type 1
- "Show before/after for a recent change" -> Type 3
- "Current value needs to be super fast to join" -> Type 4
- "We need to audit compliance at any past date" -> Type 2 or 6
