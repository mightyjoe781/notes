# Databricks Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: databricks
This is part 1 of 1 parts

---

## File: databricks/fundamentals/ch0.md

## Introduction

Databricks : The Data + AI Company

- Inventor and pioneer of the data lakehouse
- Creator of highly successful OSS data projects : Delta Lake, Apache Spark, and MLflow

The Databricks Lakehouse **Platform**

- unify all data in one place (platform)
- open source standards and format ---> no vendor lock-in

Why Databricks ?

1. Big Data is difficult to manage and more than 80% of project fail to manage big data
2. All firms require consolidated data security policy which should be government recognised like GDPR, HIPPA.
3. reduce redundancy of same data available for different use cases, makes difficult to enforce pt-2 ^

![image-databricks-intro](ch0.assets/image-20230125125256655.png)

### The Lakehouse Platform

**Data Warehouse** : 

- Strengths
  - Purpose-built for BI and reporting
  - Meant to unify disparate systems
- Downside
  - Poor support for Unstructured Data, data science, AI and streaming
  - Closed and Proprietary formats
  - Expensive to scale

**Date Lake** :

- Strengths
  - Store any kind of data
  - Inexpensive Storage
  - Good starting point
- Downsides
  - Complex to setup
  - Poor BI performance
  - Can become unreliable data swamps

**DataBricks Lakehouse Platform** : Mixture of both of above paradigm.

- Simple, Open, multicloud
- ACID Txn
- Schema Enforcement
- Governance Support
- Direct access to source data (BI Data)
- Fully scalable
- Open format
- Structured, unstructured or semi-structured 
- Real time data collection and reporting

### Databricks Lakehouse Components

![image-20230125133138173](ch0.assets/image-20230125133138173.png)

Data lands in organisation’s open data lake, by adding Delta lake to that you achieve lakehouse part of platform.

**Delta Lake**

- Reliability -> ACID : Quality data accelerates innovation
- Performance -> Indexing : Lower TCO with a simple architecture
- Governance -> Unity Catalog : Automation increases productivity
- Quality -> Expectation : Reduces Security Risk

Quality of Data

- Bronze : Raw ingestion and history
- Silver : Filtered, Cleaned, Augmented

![image-databricks-mlflow](ch0.assets/image-20230125134216348.png)

### Databricks Platform Security

Databricks can directly connect to consure lake house and utilise federated access like SSO to allow users to access the Data. While users can manage their data using keys on public cloud, in databricks users don’t have to worry about certficates and encryption as its handled by databricks.

Some features for ensuring privacy :

- Optional Consumer managed VPC/VNET
- IP Access List
- Code Isolation
- Private network between data plane (managed by cloud provider) and control plane(managed by databricks in backend)
- Secure cluster connectivity

### Databricks Unity Catalog

- Unify governance across clouds : Fine grained governance for data lakes across clouds - based on open standards of ANSI SQL
- Unify data and AI assets : Centrally share, audit,  secure and manage all types of data in simple interface
- Unify existing catalogs : Works in concert with existing data, storage and catalogs - no hard migration required

---

## File: databricks/fundamentals/ch1.md

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



---

## File: databricks/fundamentals/ch2.md

## Databricks Data Science and Engineering Workspace

Databricks Assets Map :

![image-20230129194018392](ch2.assets/image-20230129194018392.png)

- Notebooks : web-based interface that documents the containers using series of cells.
- Folders : file-system like constructs.
- Repos : provide to ability to sync/push/pull events for ci/cd tools
- Jobs : automatic tasks, can be implemented using notebooks, jars, python scripts, Scala, java etc.
- Pipelines : DAG that targets data-sources to target datasets. Implemented using notebooks.
- Clusters : Computation-Resources
- Pools : reduces cluster start and scaling times by maintaining sets of idle compute resources. Cluster are attached to pool.


---

## File: databricks/fundamentals/ch3.md

## Databricks Machine Learning

- helps manage end-to-end databricks machine learning lifecycle

- Production Machine Learning depends on code and data
- ML requires many different roles to get involved
- ML requires integrating many different components



### Common Machine Learning Problems

- Data Quality (while storage/loading of data)
- Struggle with Compute Resources (autoscaling etc.)
- Feature development (training models or inference data preparation)
- Model Development
- Governace and Security (access restriction and policies)
- Machine Learning Operations (serving and deployment)
- Automation

![image-20230129202123289](ch3.assets/image-20230129202123289.png)

### Databricks Workflow

**Automating Data Work**

- Non-interactively run AI workflows on a schedule or on-demand
- Automate Machine Learning pipelines
- Full control of execution environment

### Databricks Repos

- Syncronize projects with git repositories
- Supports Gitlab, GitHub, Bitbucket
- Collaborate across workspaces or development environments

### MLflow Components

- Tracking : track your model runs and compare results
- Models : manage and deploy models from variety of ML libraries to a variety of models serving and inference platforms
- Projects : package ML code in reusable, reproducible form to share 
- Model Registry : centralize a model store for managing models full lifecycle stage transition
- Model Serving : host MLflow Models for real-time serving

---

## File: databricks/fundamentals/index.md

### Fundamentals of Databricks Lakehouse

- [What is the Databricks Platform](ch0.md)
- [What is Databricks SQL](ch1.md)
- [What is Data Science and Engineering Workspace](ch2.md)
- [What is Datbricks Machine Learning](ch3.md)

---

## File: databricks/index.md

## Databricks





- [Databricks Lakehouse Fundamentals Notes](fundamentals/index.md)


---

