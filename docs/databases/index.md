---
title: Databases
description: Hub page linking to notes on SQL, PostgreSQL, joins and set operations, and database engineering internals.
tags:
  - index
---

# Database

A database is an organized collection of data stored and accessed electronically. *Small databases* can be stored on a file system, while *large databases* are hosted on computer clusters or cloud storage. 

The design of databases spans formal techniques and practical considerations including data modelling, efficient data representation and storage, query languages, security and privacy of sensitive data, and distributed computing issues including supporting concurrent access and fault tolerance.

A database management system (DBMS) is the software that interacts with end users, applications, and the database itself to capture and analyze the data. The DBMS software additionally encompasses the core facilities provided to administer the database. The sum total of the database, the DBMS and the associated applications can be referred to as a database system.

### Notes

- [SQL](sql/index.md)
    - [Window Functions](sql/window_functions.md)
    - [Normalization (1NF, 2NF, 3NF, BCNF)](sql/normalization.md)
    - [Slowly Changing Dimensions & MERGE](sql/scd.md)
    - [Recursive CTEs](sql/recursive_cte.md)
    - [Data Warehousing - Star, Snowflake, Data Vault](sql/data_warehousing.md)
    - [Query Optimization & EXPLAIN](sql/query_optimization.md)
- [PostgreSQL](postgresql/index.md)
- [Joins & Set Operations](joins_n_set.md)
- MongoDB [Upcoming]
- Redis [Upcoming]
- [Database Engineering](dbeng/index.md)

