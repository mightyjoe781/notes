---
title: What is Databricks SQL
description: The Databricks SQL query lifecycle, Photon engine, SQL Warehouse types, and connecting BI tools.
tags:
  - concept
---

## Databricks SQL

> Docs: [Databricks SQL](https://docs.databricks.com/aws/en/sql/) · [SQL Warehouses](https://docs.databricks.com/aws/en/compute/sql-warehouse/)

![Databricks SQL](https://www.databricks.com/sites/default/files/2025-01/dbsql-header_0.png?v=1737749860)

- Execute SQL statements directly on the Data Lakehouse
- Built-in visualization tool; develop agile dashboards and collaborate easily
- Set up automated alerts on data refresh
- Supports multiple BI tools

### Query lifecycle

```
Databricks SQL → BI Tools → Drivers → Routing Service (load balancing)
                → Query Planning (Spark) → Query Execution (Photon)
```

> Docs: [Photon engine](https://docs.databricks.com/aws/en/compute/photon)

**Photon** is Databricks' native vectorized query engine written in C++. It accelerates SQL and DataFrame workloads - especially scans, aggregations, and joins on large datasets - giving significant speedups over standard Spark execution.

### Setup requirements

Before querying, a data administrator configures three things:

| # | Requirement | Notes |
|---|---|---|
| 1 | **SQL Warehouse** (compute) | Classic (in your cloud account) · Serverless (fully managed, starts in seconds) · Pro (Photon + larger result sets) |
| 2 | **Data Catalog access** | First layer of Unity Catalog's 3-level namespace (`catalog.schema.table`) |
| 3 | **Database (Schema) access** | Second layer - a collection of tables |

### Querying basics

- An active SQL Warehouse is required to run queries
- Query editor supports auto-complete, syntax highlighting, and query history
- Results can be saved as visualizations or pinned to dashboards

### Automate workflows

- Schedule queries to run on a set interval
- Configure alerts to notify via email or webhooks when query results meet a threshold

### Connect BI tools

- Some BI tools require drivers and authentication via a Databricks personal access token (PAT) or OAuth
- Access to a running SQL Warehouse is required
- Partner Connect simplifies integration with Tableau, Power BI, Looker, and others

## See Also

- [Databricks Platform In Depth](ch4.md) - compute and Photon internals
- [Recent Platform Updates](ch5.md) - Unity Catalog Metric Views for governed business KPIs
