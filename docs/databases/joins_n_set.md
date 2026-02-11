# Joins and Set Operation

SQL operations used to combine data are broadly categorized into

Joins (connecting tables side-by-side via columns) and Set Operators (stacking results vertically via rows).

## Joins

![](assets/Pasted%20image%2020260211094016.png)

Read this Explanation First : https://stackoverflow.com/questions/38549/what-is-the-difference-between-inner-join-and-outer-join

### Cross Join

![](assets/Pasted%20image%2020260211094722.png)

`select A.color, B.color FROM A CROSS JOIN B`

![](assets/Pasted%20image%2020260211094729.png)

### Inner Join

Evaluate the condition in the `ON` for all rows in the cross join result. If `true`, return the joined row. Otherwise, discard it.

`SELECT A.Colour, B.Colour FROM A INNER JOIN B ON A.Colour = B.Colour`

![](assets/Pasted%20image%2020260211103650.png)

### Left Outer Join

Same as inner join then for any rows in the left table that did not match anything output these with NULL for right columns.

`SELECT A.Colour, B.Colour FROM A LEFT OUTER JOIN B ON A.Colour = B.Colour`

![](assets/Pasted%20image%2020260211103832.png)

### Right Outer Join

Same as inner join, then for any rows in the right table that did not match anything, output these with NULL values.

`SELECT A.Colour, B.Colour FROM A RIGHT OUTER JOIN B ON A.Colour = B.Colour`

![](assets/Pasted%20image%2020260211103925.png)

### FULL Outer Join

Same as inner join, then preserve left non-matched rows as in left outer join and right non-matching rows as per right outer join.

`SELECT A.Colour, B.Colour FROM A RIGHT OUTER JOIN B ON A.Colour = B.Colour`

![](assets/Pasted%20image%2020260211104057.png)

## Advanced Joins

### Left Anti Join

Same as Left Join, but returns rows from the left table that have **no match** in the right table.

`SELECT A.Colour, B.Colour FROM A LEFT OUTER JOIN B ON A.Colour = B.Colour WHERE B.COLOR IS NULL`

![](assets/Pasted%20image%2020260211104544.png)
### Left Semi Join

Returns rows from the left table only if a match exists in the right table, but unlike an inner join, it doesn't duplicate left rows for multiple right-side matches

![](assets/Pasted%20image%2020260211110519.png)

### Self-Joins

A Self Join is a regular join where a table is joined with itself. Because you are using the same table twice, **aliases** are mandatory to distinguish between the two "virtual" copies and avoid column name ambiguity.

Use Cases

- **Organizational Hierarchies:** Finding the name of an employee's manager when both are stored in the same `Employees` table.
- **Comparing Rows:** Finding employees who live in the same city or identifying products in the same category.
- **Sequential Data Analysis:** Comparing a current row with a previous or next row, such as comparing today's stock price to yesterday's within the same table.
- **Finding Duplicates:** Identifying records with identical values in specific columns by joining the table to itself on those columns.

```sql
SELECT e1.name AS Employee, e2.name AS Manager
FROM Employees e1
JOIN Employees e2 ON e1.ManagerID = e2.EmployeeID;
```

|ID|Name|ManagerID|
|---|---|---|
|1|Alice|NULL|
|2|Bob|1|
|3|Charlie|1|
### Summary

![](assets/Pasted%20image%2020260211093240.png)

The Venn diagrams are good for representing Unions and Intersections and Differences but not joins. They have some minor educational value for very simple joins, i.e. joins where the joining condition is on unique columns.

## Set Operations

### Union

Combines results from two queries and removes duplicate rows.

```sql
SELECT Colour FROM A
UNION
SELECT Colour FROM B;
```

![](assets/Pasted%20image%2020260211110354.png)

### Union All

Combines results but keeps all duplicates; it is faster than a standard `UNION`

```sql
SELECT Colour FROM A
UNION ALL
SELECT Colour FROM B;
```

![](assets/Pasted%20image%2020260211104906.png)


NOTE: implementation using full-outer join : `SELECT COALESCE(A.Colour, B.Colour) AS Colour FROM A FULL OUTER JOIN B ON 1 = 0`

This is not optimal at all.

Without COALESCE this would like this.

![](assets/Pasted%20image%2020260211105003.png)
### Intersect

Intersect: Returns only the rows that appear in both query results.

```sql
SELECT Colour FROM A
INTERSECT
SELECT Colour FROM B;
```

![](assets/Pasted%20image%2020260211110125.png)

### Except/Minus

Returns rows from the first query that are not present in the second. 

```sql
SELECT Colour FROM A
INTERSECT
SELECT Colour FROM B;
```

![](assets/Pasted%20image%2020260211110309.png)

## Language Semantics

### PostgreSQL

PostgreSQL follows strict SQL standards, where set operations **remove duplicates** by default unless the `ALL` keyword is added.

| Operation      | PostgreSQL SQL Syntax    | Duplicate/Null Handling                                             |
| -------------- | ------------------------ | ------------------------------------------------------------------- |
| **Inner Join** | `JOIN` / `INNER JOIN`    | Only returns rows with a match in **both** tables.                  |
| **Left Join**  | `LEFT JOIN`              | Returns all left rows; fills right columns with `NULL` if no match. |
| **Full Join**  | `FULL OUTER JOIN`        | Returns all rows from both tables; fills missing sides with `NULL`. |
| **Cross Join** | `CROSS JOIN`             | Cartesian product (every row in A paired with every row in B).      |
| **Semi Join**  | `WHERE EXISTS (...)`     | Returns left rows that **have** a match in the right table.         |
| **Anti Join**  | `WHERE NOT EXISTS (...)` | Returns left rows that **do not have** a match in the right table.  |
| **Union**      | `UNION`                  | Stacks rows and **removes duplicates**.                             |
| **Union All**  | `UNION ALL`              | Stacks rows and **keeps all duplicates**.                           |
| **Intersect**  | `INTERSECT`              | Returns only unique rows common to both tables.                     |
| **Except**     | `EXCEPT`                 | Returns unique rows in the first table but not the second.          |

### Pyspark

PySpark uses methods that often **keep duplicates** by default (like `.union()`), requiring an explicit `.distinct()` call to match standard SQL behavior.

| Operation          | PySpark Method (`df1.join(df2, ...)` ) | Duplicate/Null Handling                                          |
| ------------------ | -------------------------------------- | ---------------------------------------------------------------- |
| **Inner Join**     | `how="inner"`                          | Only returns rows with a match in **both** DataFrames.           |
| **Left Join**      | `how="left"`                           | Returns all left rows; fills right columns with `None`.          |
| **Full Join**      | `how="outer"`                          | Returns all rows from both; fills missing sides with `None`.     |
| **Cross Join**     | `.crossJoin(df2)`                      | Cartesian product (every row in A paired with every row in B).   |
| **Semi Join**      | `how="semi"`                           | Native support; returns left rows with at least one match.       |
| **Anti Join**      | `how="anti"`                           | Native support; returns left rows with **no** match.             |
| **Union**          | `.union(df2)`                          | Stacks rows and **keeps all duplicates** (like SQL `UNION ALL`). |
| **Union (Unique)** | `.union(df2).distinct()`               | Stacks rows and **removes duplicates** (like SQL `UNION`).       |
| **Intersect**      | `.intersect(df2)`                      | Returns only unique rows common to both DataFrames.              |
| **Except**         | `.subtract(df2)`                       | Returns unique rows in the first but not the second.             |

### Demo

This should spin up postgres and pgadmin.

```bash
# docker run
docker run --name pg -p 5432:5432 -e POSTGRES_PASSWORD=password postgres

# run pgadmin --
docker run -e PGADMIN_DEFAULT_EMAIL="smk@minetest.in" -e PGADMIN_DEFAULT_PASSWORD="password" -p 5555:80 --name pgadmin dpage/pgadmin4

```

... TODO ~ find a great example explaining all these.