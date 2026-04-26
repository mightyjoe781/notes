## Databricks SQL

- Execute SQL statements directly on the Data Lakehouse
- Built-in visualization tool
- Develop agile dashboards and collaborate easily
- Set up automated alerts on data refresh
- Supports multiple BI tools

### Query Lifecycle

Databricks SQL → BI Tools → Drivers → Routing Service (load balancing) → Query Planning (Spark) → Query Execution (Photon)

**Photon** is Databricks' native vectorized query engine written in C++. It accelerates SQL and DataFrame workloads, especially for scans, aggregations, and joins on large datasets — providing significant speedups over standard Spark execution.

### Setup Requirements

Before querying, a data administrator needs to configure three things:

1. **SQL Warehouse** (formerly called SQL Endpoint): the compute resource that powers queries.
   - **Classic Warehouse**: resides in the user's cloud account
   - **Serverless Warehouse**: fully managed by Databricks; starts in seconds with no infrastructure to manage
   - **Pro Warehouse**: supports queries needing extra features like Photon and larger result sets
2. **Access to a Data Catalog**
   - Catalog: first layer of Unity Catalog's 3-level namespace (`catalog.schema.table`); used to organise data assets
3. **Access to a Database (Schema)**
   - Schema: collection of tables; the second layer of Unity Catalog's 3-level namespace

### Querying Basics

- An active SQL Warehouse is required to run queries.
- The query editor supports auto-complete, syntax highlighting, and query history.
- Results can be saved as visualizations or pinned to dashboards.

### Automate Workflows

- Schedule queries to run on a set interval
- Configure alerts to notify via email or webhooks when query results meet a threshold

### Connect BI Tools

- Some BI tools require drivers and authentication with a Databricks personal access token (PAT) or OAuth
- Access to a running SQL Warehouse is required
- Partner Connect simplifies integration with popular solutions like Tableau, Power BI, and Looker
