# Recursive CTEs

A recursive CTE calls itself. Use it to traverse hierarchical or graph-structured data stored in a flat table - things like org charts, folder trees, bill of materials, or category hierarchies.

## Syntax

```sql
WITH RECURSIVE cte_name AS (
    -- anchor: the starting rows (non-recursive)
    SELECT ...
    FROM table
    WHERE <base condition>

    UNION ALL

    -- recursive: joins cte back to itself
    SELECT ...
    FROM table
    JOIN cte_name ON <join condition>
)
SELECT * FROM cte_name;
```

The engine evaluates the anchor once, then repeatedly evaluates the recursive term using the previous iteration's result, until the recursive term returns no new rows.

`UNION ALL` is almost always correct here. `UNION` would deduplicate every iteration, which is expensive and usually wrong for traversal.

## Example 1 - Org Chart (top-down traversal)

```
employees table:
id | name    | manager_id
1  | Alice   | NULL        <- CEO
2  | Bob     | 1
3  | Carol   | 1
4  | Dave    | 2
5  | Eve     | 2
```

Find all employees under Alice (id=1) including herself:

```sql
WITH RECURSIVE org AS (
    -- anchor: start at Alice
    SELECT id, name, manager_id, 0 AS depth
    FROM employees
    WHERE id = 1

    UNION ALL

    -- recursive: find direct reports of everyone found so far
    SELECT e.id, e.name, e.manager_id, org.depth + 1
    FROM employees e
    JOIN org ON e.manager_id = org.id
)
SELECT * FROM org ORDER BY depth, name;
```

Result:

```
id | name  | depth
1  | Alice | 0
2  | Bob   | 1
3  | Carol | 1
4  | Dave  | 2
5  | Eve   | 2
```

## Example 2 - Path accumulation

Find the full path from root to each node:

```sql
WITH RECURSIVE org AS (
    SELECT id, name, manager_id, name::TEXT AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id,
           org.path || ' -> ' || e.name
    FROM employees e
    JOIN org ON e.manager_id = org.id
)
SELECT id, name, path FROM org;
```

Result:

```
id | name  | path
1  | Alice | Alice
2  | Bob   | Alice -> Bob
4  | Dave  | Alice -> Bob -> Dave
```

## Example 3 - Folder tree (bottom-up)

Given a folder, find all its ancestors:

```sql
WITH RECURSIVE ancestors AS (
    -- anchor: start at the target folder
    SELECT id, name, parent_id
    FROM folders
    WHERE id = 42

    UNION ALL

    -- recursive: walk up to parent
    SELECT f.id, f.name, f.parent_id
    FROM folders f
    JOIN ancestors a ON f.id = a.parent_id
)
SELECT * FROM ancestors;
```

## Example 4 - Consecutive number generation

Recursive CTEs can also generate sequences:

```sql
WITH RECURSIVE nums AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 100
)
SELECT * FROM nums;
```

Useful for generating a date spine:

```sql
WITH RECURSIVE date_spine AS (
    SELECT '2024-01-01'::DATE AS d
    UNION ALL
    SELECT d + 1 FROM date_spine WHERE d < '2024-12-31'
)
SELECT * FROM date_spine;
```

## Cycle Detection

If your data can have cycles (graph, not just tree), a naive recursive CTE will loop forever. Guard with a visited array or depth limit:

```sql
WITH RECURSIVE traversal AS (
    SELECT id, ARRAY[id] AS visited
    FROM nodes
    WHERE id = 1

    UNION ALL

    SELECT n.id, t.visited || n.id
    FROM nodes n
    JOIN traversal t ON n.parent_id = t.id
    WHERE NOT n.id = ANY(t.visited)   -- skip already-visited nodes
)
SELECT * FROM traversal;
```

Or simply cap depth:

```sql
WHERE depth < 20
```

## PySpark equivalent

Spark SQL supports recursive CTEs from Spark 3.5+ (still experimental). For older versions, use iterative joins:

```python
from functools import reduce

# simulate traversal with iterative joins
frontier = df.filter(F.col("manager_id").isNull()).select("id", "name")
all_nodes = frontier

for _ in range(max_depth):
    next_level = df.join(frontier, df["manager_id"] == frontier["id"], "inner") \
                   .select(df["id"], df["name"])
    if next_level.count() == 0:
        break
    frontier = next_level
    all_nodes = all_nodes.union(next_level)
```

## When to use

- Org charts / reporting hierarchies
- Folder / category trees
- Bill of materials (product made of parts, parts made of sub-parts)
- Finding connected components in a graph
- Generating date spines or number sequences
- Any "walk until you hit a base case" problem stored relationally
