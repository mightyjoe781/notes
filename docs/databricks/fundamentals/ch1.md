## Databricks SQL

- Can directly excuted SQL Statements on Data Lakehouse
- Visualization tool
- Develop Agile Dashboards & Collaborate Easily
- Track APIs using automated alerts on data refresh
- Supports multiple BI Tools

Various Steps followed in Databricks SQL Query Lifecycle :

- Databricks SQL/BI Tools -> Drivers -> Routing Service (Load Balancing) -> Query Planning(Spark) -> Query Execution (Photon)

Before Querying a Data Administrator needs to setup 3 things

1. SQL Endpoint : Computation resource that powers queries.
   - Classic Endpoint : resides in a users cloud account
   - Serverless Endpoints : managed by databricks
2. Access to a Data Catalog
   - Catalog : first layer of unity catalog’s 3-level namespace, used to organise data assets. Catalogs contain databases.
3. Access to a Database
   - Database : Collection of Tables/Schemas, 2nd layer of unity catalog’s 3-lvl namespace.

**Querying Basics**

- An active endpoint is required to query the database.

**Automate Workflows**

- you can use schedule to set up query schedule and then can setup alert to get notified.

**Connect BI Tools**

- Some BI Tools will require drivers and needs to authenticate with databricks compute resources(Personal Access Token).
- Access to SQL Endpoints is a must.
- You can utlize partner connect for popular solutions.

