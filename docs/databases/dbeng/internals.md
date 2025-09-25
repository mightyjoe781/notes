# Understanding Database Internals

How tables and indexes are stored on disk ? How are they queried

## Storage Concepts

![](assets/Pasted%20image%2020250924195219.png)

#### row_id

- Internal & System Maintained
- In certain databases (mysql, innoDB) it is same as the primary key but other databases like Postgresql have a system column `row_id` (`tuple_id`)


| row_id | emp_id | emp_name | dob | salary |
| ------ | ------ | -------- | --- | ------ |
| 1      | 785    | smk      | -   | $10000 |
| 2      | 995    | hmk      | -   | $20000 |
| 3      | 1095   | dk       | -   | $30000 |

#### Page

- Depending on the storage model (row vs column store), the rows are stored and read in logical pages
- The database doesn't read a single row, it reads a page or more in a single IO and we get a lot of rows in that IO
- Each page has size (e.g. 8KB postgres, 16KB in MySQL)
- Assume each page holds 3 rows in this example, with 10001 rows, you will have 333 ~ pages

![](assets/Pasted%20image%2020250924195809.png)

#### IO

- IO operation (input/output) is a read request to the disk
- We try to minimize this as much as possible
- An IO can fetch 1 page or more depending on the disk partitions and other factors
- An IO cannot read a single row, its a page with many rows in them, you get them for free.
- You want to minimize the number of IOs as they are expensive.
- Some IOs in operating systems goes to the operating system cache and not disk. (postgres)
#### Heap Data Structure

- Heap is data structure where the table is stored with all its pages one after another
- This is where the actual data is stored including everything
- Traversing the heap is expensive as we need to read so many data to find what we want
- That is why we need indexes that help tell us exactly what part of the heap we need to read. What page(s) of the heap we need to pull.

#### Index data structure b-tree

- An index is another data structure separate from the heap that has *pointers* to the heap
- It has part of the data and used to quickly search for something
- You can index on one column or more.
- Once you find a value of the index, you go to the heap to fetch more information where everything is there
- Index tells you *EXACTLY* which page to fetch in the heap instead of taking the hit to scan every page in the heap
- The index is also stored as pages and cost IO to pull the entries of the index.
- The smaller the index, the more it can fit in memory the faster the search
- Popular data structure for index is *B-Tree*/LSM Trees

![](assets/Pasted%20image%2020250924200838.png)

#### Example of a query

```
select * from EMP where EMP_ID = 100000;
```

- above query in case of no index needs to pull each page, but if indexes are present they make you directly find the page where your row is and load that in memory

NOTES

- Sometimes the heap table can be organized around a single index. This is called a clustered index or an Index Organized Table
- Primary Key is usually a clustered index unless otherwise specified
- MySQL InnoDB always have a primary key (clustered index) other indexes point to primary key `value`
- Postgres only have secondary indexes and all indexes point directly to the `row_id` which lives in the heap.
- Choosing `uuid` as a primary key is a bad idea ! due to creation of multiple pages due to randomness of uuid generation.


## Row vs Column Oriented Databases


Lets say we have following table

| rowid | id | first_name | last_name | ssn | salary   | dob       | title | joined    |
|-------|----|------------|-----------|-----|----------|-----------|-------|-----------|
| 1001  | 1  | John       | Smith     | 111 | 101,000  | 1/1/1991  | eng   | 1/1/2011  |
| 1002  | 2  | Kary       | White     | 222 | 102,000  | 2/2/1992  | mgr   | 2/1/2012  |
| 1003  | 3  | Norman     | Freeman   | 333 | 103,000  | 3/3/1993  | mkt   | 3/1/2013  |
| 1004  | 4  | Nole       | Smith     | 444 | 104,000  | 4/4/1994  | adm   | 4/1/2014  |
| 1005  | 5  | Dar        | Sol       | 555 | 105,000  | 5/5/1995  | adm   | 5/1/2015  |
| 1006  | 6  | Yan        | Thee      | 666 | 106,000  | 6/6/1996  | mkt   | 6/1/2016  |
| 1007  | 7  | Hasan      | Ali       | 777 | 107,000  | 7/7/1997  | acc   | 7/1/2017  |
| 1008  | 8  | Ali        | Bilal     | 888 | 108,000  | 8/8/1998  | acc   | 8/1/2018  |

### Row-Oriented Database (Row store)

- Tables are stored as rows in disk
- A single block io read to the table fetches multiple rows with all their columns
- More IOs are required to find a particular row in a table scan, but once you find the row you get all columns for that row.

![](assets/Pasted%20image%2020250924201943.png)

```sql
select name from t1 where emp_id = 666;
```

- Without Index we will scan each block and find where (3rd block) `emp_id` is `666` and then return name from that block but with indexes databases can just directly jump with index.
- aggregates like `sum(salary)` will always scan the entire table, (some db can parallel perform this)

### Column-Oriented Database (Column store)

- Tables are stored as columns first in disk
- A single block io read to the table fetches multiple columns with all matching rows
- Less IOs are required to get more values of a given column. But with multiple columns require more IOs.
- OLAP

![](assets/Pasted%20image%2020250924203128.png)

- See how aggregates become efficient at the cost of expensive pointed access.
- First find the block where `emp_id` is 666, then scan entire blocks to find the name, DB can maybe optimize this using internal calculation but a query like `select *` will cause reading multiple blocks.

```sql
select name from t1 where emp_id = 666;
```

### Pros & Cons

| Row-Based                         | Column-Based                        |
| --------------------------------- | ----------------------------------- |
| Optimal for read/writes           | Writes are slower                   |
| OLTP                              | OLAP                                |
| Compression isn't efficient       | Compress greatly                    |
| Aggregation isn't efficient       | Amazing for aggregation             |
| Efficient queries w/ multi-column | Inefficient queries w/multi-columns |

### Optional Reading

Databases Pages - A deep dive (https://medium.com/p/38cdb2c79eb5)