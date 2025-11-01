# Data Engineering Fundamentals

## Types of Data

### Structured

- Data organized in defined manner or schema, typically found in relational databases.
- Characteristics
    - Easily Queryable
    - Organized in rows/cols
    - consistent structure
- Examples
    - database tables
    - CSV files with consistent columns

### Unstructured Data

- Data doesn't have a predefined structure or schema
- Characteristics
    - Not easily queryable without preprocessing
    - Multiple format
- Examples:
    - Text files without a fixed format
    - video/audio files
    - images
    - word documents

### Semi-Structured Data

- Data that has some level of structure in form of tags, hierarchies, or other patterns
- Characteristics
    - elements might be tagged/categorised
- Examples
    - XML & JSON files
    - Email Headers
    - Log files with various formats

## Properties of Data

- Volume
    - size of data
    - may range from GBs to PBs or more
    - challenges in storing, processing & analyzing high volumes of data
- Velocity
    - speed at which data is generated, collected, processed
    - High velocity data requires real-time or near-real-time processing capabilities
    - rapid ingestion/processing could be critical for some application
- Variety
    - refers to different types, structure, sources of data

## Data Warehouse & Data Lakes

### Data Warehouse

- Definition : A centralized repository optimized for analysis where data from different sources is stored in a structured format
- characteristics:
    - designed for complex queries & analysis
    - Data is cleaned, transformed, and loaded (ETL process)
    - Typically uses a Star or snowflake schema
    - optimized for read-heavy operations

![](assets/Pasted%20image%2020251101103856.png)

### Data Lake

- a storage repository that holds vasts amount of raw data in native format, including structured, semi-structured, unstructured data
- characteristics
    - can store large volumes of raw data without predefined schema
    - data is loaded as-is
    - supports batch, real-time, & stream processing
    - can be queried for data transformation or exploration purposes
- Examples
    - Amazon s3 when used as data lake

![](assets/Pasted%20image%2020251101111804.png)

### Data Lakehouse

- hybrid data architecture that combines the best features of data lakes and data warehouses, aiming to provide the performance, reliability and capabilities of a data warehouse while maintaining the flexibility, scale, and low-cost storage of data lakes.
- Characteristics
    - supports both structured and unstructured data
    - allows for schema-on-write and schema-on-read
    - provides capabilities for both detailed analytics and machine learning tasks
    - typically built on top of cloud or distributed architectures
    - Benefits from technologies like Delta Lake, which brings ACID transactions to big data
- Examples
    - AWS Lake formation (with S3, Redshift Spectrum)
    - Delta Lake
    - Databricks Lakehouse Platform
    - Azure Synapse Analytics

## Data Mesh

- coined in 2019, its more about governance and organization
- individual teams own "team products" within a given domain
- These data products serve various *use-cases* around the organisation
- *Domain-based data managements*
- Federated governance with central standards
- Self-service tooling & infrastructure
- Data lakes, warehouses, etc. may be part of it
    - But a *Data Mesh* is more about the *data management paradigm* and not the specific technologies or architectures
![](assets/Pasted%20image%2020251101112513.png)

## Managing & Orchestrating ETL Pipelines

*Definition* : ETL stands for Extract, Transform, Load. It's a process used to move data from source systems into a data warehouse.

- Extract
    - retrieve raw data from source systems, which can databases, CRMs, flat files, APIs, etc.
    - Ensure data integrity during extraction phase
    - can be done in real-time or in batches, depending on requirements
- Transform
    - convert the extracted data into a format suitable for the largest data warehouse
    - can involve various operations such as
        - Data cleansing
        - Data enrichment
        - Format Changes
        - Aggregation/Computation
        - Encoding/Decoding Data
- Load
    - move the transformed data into into the target data warehouse or another data repository
    - Can be done in batches (all at once) or in a streaming manner
    - Ensure that data maintains its integrity during loading phase

### Managing ETL Pipelines

- process must be automated in some reliable way
- AWS Glue
- Orchestration Services
    - EventBridge
    - Amazon Managed Workflows for Apache Airflow
    - AWS Step Functions
    - Lambda
    - Glue Workflows


## Common Data Sources & Data Formats

### Data Sources

- JDBC
    - Java Database Connectivity
    - Platform-independent
    - Language-dependent
- ODBC
    - open database connectivity
    - Platform-dependent (thx to drivers)
    - Language-independent
- Raw Logs
- APIs
- Streams
### Data Formats

- CSV
    - text based format that represents data in tabular form where each line corresponds to a row and values within a row are separated by delimiters
    - Use-Cases
        - small-medium datasets
        - human-readable & editable data storage
        - importing/exporting data from databases or spreadsheets
    - Systems: databases (SQL Based), Excel, Pandas in Python, R, many ETL tools.
- JSON
    - lightweight, text-based, and human-readable data interchange format, representing semi-structured data based on key-values
    - Use-Cases
        - data interchange between web-server and web-client
        - configuration/settings for software application
        - flexible schema or nested data structure
    - Systems : web browsers, javascript, RESTful APIs, NoSQL database, etc.
- Avro
    - binary format that stored both data & its schema allowing it to be processed later with different systems without needing the original system's  context
    - Use Cases
        - big-data & real-time processing systems
        - when schema evolution is needed
        - Efficient serialization for data transport between systems
    - Systems : Apache Kafka, Apache Spark, Apache Flink, Hadoop ecosystem.
- Parquet
    - columnar storage format optimized for anlaytics, allowing for efficient compression and encoding schemas
    - Use Cases
        - analyzing large datasets with analytics engines
        - reading specific columns rather than records
        - storing data on distributed systems where I/O operations and storage need optimizations
    - Systems : Hadoop Ecosystem, Apache Spark, Apache Hive, Apache Impala, Amazon Redshift Spectrum.

## Data Modeling, Data Lineage, and Schema Evolution

### Data Modelling

![](assets/Pasted%20image%2020251101120322.png)

Example of Star Schema

- Fact tables
- Dimension
- Primary/Foreign Keys

This sort of diagram is an Entity Relationship Diagram
### Data Lineage

- Visual representation that traces the flow & transformation of data through its lifecycle, from its source to its final destination.
- Importance
    - Helps in tracking errors back to their source
    - Ensures compliance with regulations
    - Provides a clear understanding of how data is moved transformed, and consumed within systems
- Example of Capturing Data Lineage

![](assets/Pasted%20image%2020251101120507.png)

### Schema Evolution

- The ability to adapt and change the schema of a dataset over time without disrupting existing processes or systems
- Importance
    - Ensure data systems can adapt to changing business requirements.
    - Allows modification of columns/fields in the dataset
    - Maintains backward compatibility with older data records
- Glue Schema Registry
    - Schema discovery, compatibility, validation, registration
## Database Performance Optimizations

- Indexing
    - Avoid full table scans
    - Enforce data uniqueness & integrity
- Partitioning
    - Reduce amount of data scanned
    - Helps with data lifecycle management
    - Enables parallel processing
- Compression
    - speed up data transfer, reduce storage & disk reads
    - GZIP, LZOP, BZIP2, ZSTD
    - Columnar Compression
## Data Sampling Techniques 

- Random Sampling
    - Everything has an equal change
- Stratified Sampling
    - divide population into homogenous subgroups (strata)
    - Random sample within each stratum
    - Ensures representation of each subgroup
- Other
    - Systemic, Cluster, Convenience, Judgemental
## Data Skew mechanism

- Data skew refers to the unequal distribution or imbalance of data across various nodes or partitions in distributed computing systems.
- “The celebrity problem”
    - Even partitioning doesn’t work if your traffic is uneven
- Causes:
    - Non-uniform distribution of data
    - Inadequate partitioning strategy
    - Temporal skew
- Important to monitor data distribution and alert when skew issues arise.

### Addressing Data Skew

- *Adaptive Partitioning* : Dynamically adjust partitioning based on data characteristics to ensure a more balanced distribution
- *Salting* : introduce a random factor or `salt` to data to distribute it more uniformly
- *Repartitioning* : regularly redistribute the data based on its current distribution characterstics
- *sampling* : use a sample of the data to determine the distribution characteristics.
- *Custom Partitioning* - Define custom rules/functions for partitioning based on Domain Knowledge.

## Data Validation & Profiling

- Completeness
    - ensures all required data is present and no essential parts are missing
- Consistency
    - ensures data values are consistent across datasets and do not contradict each other
- Accuracy
    - data is correct, reliable, and represents what its supposed to
- Integrity
    - ensures data maintains its correctness and consistency over its lifecycle across systems

## SQL Review

Aggregations

```postgresql

-- count
SELECT COUNT(*) AS total_rows FROM employees;

-- sum
SELECT SUM(salary) AS total_salary FROM employees;

-- avg
SELECT AVG(salary) AS average_salary FROM employees;

-- max/min
SELECT MAX(salary) AS highest_salary FROM employees;

```

Aggregations with CASE

```postgresql

-- where clauses to filter
SELECT COUNT(*) AS high_salary_count
FROM employees
WHERE salary > 70000;

-- applying multiple filters while aggregation
SELECT
    COUNT(CASE WHEN salary > 70000 THEN 1 END) AS high_salary_count,
    COUNT(CASE WHEN salary BETWEEN 50000 AND 70000 THEN 1 END) AS medium_salary_count,
    COUNT(CASE WHEN salary < 50000 THEN 1 END) AS low_salary_count
FROM employees;
```

Grouping, Nested Grouping, Sorting

```postgresql

-- grouping
SELECT department_id, COUNT(*) AS number_of_employees
FROM employees
WHERE join_date > '2020-01-01'
GROUP BY department id:

-- department_id | number_of_employees
-- HR  | 6
-- IT  | 18

-- nested grouping/sorting

SELECT YEAR(sale_date) AS sale_year, product_id, SUM(amount) AS total sales
FROM sales
GROUP BY sale-year,
product_id
ORDER BY sale_year,
total_sales DESC;

```

Pivoting

- Inverting data visualisation of axis, row-level-data into columnar data
- could be done without *PIVOT* command as well

```postgresql

SELECT salesporson, [Jan] AS Jan_sales, [Feb] AS Feb_sales
FROM
(SELECT salesperson, month, sales FROM sales) AS sourceTable
PIVOT (
    SUM(sarlies
    FOR month IN (Jan), [Feb))
) As PivotTable:


-- without pivot
SELECT
salesperson,
SUM(CASE WHEN month = 'Jan' THEN sales ELSE O END) AS Jan_sales,
SUM(CASE WHEN month = 'Feb' THEN sales ELSE 0 END) AS Feb_sales
FROM sales
GROUP BY salesperson;

```

### joins

![](assets/Pasted%20image%2020251101123205.png)

https://stackoverflow.com/questions/13997365/sql-joins-as-venn-diagram

## Git Basics

```bash

# setup
git init
git config --global user.name "smk"
git config --global user.email "smk@minetest.in"

# basic commands
git clone <repo_url>
git status
git add <filename>
git commit -m <msg>
git log

# branching
git branch # list all local branches
git branch <branchname> # create
git checkout <branchname> # switch
git checkout -b <branchname> # create & switch
git merge <branchname>
git branch -d <branchname> # delete

# remote
git remote add <remote_name> <url>
git remote
git remote -v
git push <remote_name> <branch>
git pull <remote_name> <branch>

## undo

git reset # reset staging area
git reset --hard # reset staging area & work dir.
git revert <commit>

### advanced

git stash
git stash pop
git cherry-pick <commit>

## collaboration

git blame <file>
git diff
git fetch # pull without merge

## maintenance/recovery

git fsck # check database errors
git gc # clean up-optimize local repo
git reflog # record when ref were updated

```