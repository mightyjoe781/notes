# Analytics (ETL)

## AWS Glue

- Serverless discovery and definition of table definition & schema
    - S3 *Data Lakes*
    - RDS
    - Redshift
    - DynamoDB
    - Most other SQL databases
- Custom ETL jobs
    - Trigger-driven, on a schedule or on demand
    - Fully managed

### Glue Crawler / Data Catalog

![](assets/Pasted%20image%2020251110094526.png)

- Glue crawler scans data in S3, creates schema
- Can run periodically
- Populates the Glue Data Catalog
    - Stores only table definition
    - Original data stays in S3
- Once cataloged, you can treat unstructured data like it's structured
    - Redshift Spectrum
    - Athena
    - EMR
    - Quicksight

### Glue & S3 Partitions

- Glue crawler will extract partitions based on how your S3 data is organized
- Think up front about how you will be querying your data lake in S3
- Examples : device sends data every hour
    - 2 ways to partition
        - By device_id : `/dev/yyyy/mm/dd`
        - By time: `/yyyy/mm/dd/dev/`

### Glue & Hive

- Hive lets you run SQL-Like Queries from EMR
- The Glue Data Catalog can serve as a Hive *metastore*
- You can also import a Hive metastore into Glue

### Glue ETL

- Automatic code generation in Scala or Python
- Encryption
    - Server-Side (at rest)
    - SSL (in transit)
- Can be event driven
- Can provision additional DPU's (data processing units) to increase performance of underlying Spark jobs
    - always observe past metrices to predict require DPUs.
- Errors also reported to CloudWatch
    - could tie into SNS for notification
- Transform data, Clean data, Enrich Data (before analysis)
    - Generate ETL code in Python or Scala, you can modify the code
    - can provide your own Spark or PySpark scripts
    - Target could be S3, JDBC (RDS, Redshift), or in Glue Data Catalog
- Fully managed, cost effective, pay only for resources consumed
- Jobs are run on a serverless Spark platform
- Glue Scheduler to schedule the jobs
- Glue Triggers to automate job runs based on *events*

### Glue ETL: The DynamicFrame

- similar to DataFrame in Pyspark
- collection of DynamicRecords
- supports Scala & Python APIs

### Glue ETL: Transformations

- Bundled Transformation
    - DropFields, DropNullFields
    - Filter ~ specify a function to filter records
    - Join ~ to enrich data
    - Map ~ add fields, delete fields, perform external lookups
- Machine Learning Transformation
    - FindMatches ML : identify duplicate records in dataset (unstructured)
- Format Conversions : CSV, JSON, Avro, Parquet, ORC, XML
- Apache Spark transformations (ex - k-means)

### Glue ETL: Resolve Choice

- Deals with ambiguities in a Dynamic Frame & returns new one
- Ex ~ two fields same name
- `make_cols` ~ creates a new column for both types
- `cast`: casts all values to specified types
- `make_struct`: creates a structure that contains each data type
- `project`: projects every type to a given type

### Glue ETL: Modifying the Catalog

- ETL scripts can update your schema and partitions if necessary
- Adding new partitions
    - Re-run the crawler, or
    - Have the script use enableUpdateCatalog and partitionKeys options
- Updating table schema
    - Re-run the crawler, or
    - Use enableUpdateCatalog / updateBehavior from script
- Creating new tables
    - enableUpdateCatalog / updateBehavior with setCatalogInfo
- Restrictions
    - S3 only
    - Json, csv, avro, parquet only
    - Parquet requires special code
    - Nested schemas are not supported

### AWS Glue Development Endpoints

- Develop ETL scripts using a notebook
    - Then create an ETL job that runs your script (using Spark and Glue)
- Endpoint is in a VPC controlled by security groups, connect via:
    - Apache Zeppelin on your local machine
    - Zeppelin notebook server on EC2 (via Glue console)
    - SageMaker notebook
    - Terminal window
    - PyCharm professional edition
    - Use Elastic IP’s to access a private endpoint address

### Running Glue jobs

- Time-based schedules (cron style)
- Job bookmarks
    - Persists state from the job run
    - Prevents reprocessing of old data
    - Allows you to process new data only when re-running on a schedule
    - Works with S3 sources in a variety of formats
    - Works with relational databases via JDBC (if PK’s are in sequential order)
    - Only handles new rows, not updated rows
- CloudWatch Events
    - Fire off a Lambda function or SNS notification when ETL succeeds or fails
    - Invoke EC2 run, send event to Kinesis, activate a Step Function

### Glue cost model

- Billed by the second for crawler and ETL jobs
- First million objects stored and accesses are free for the Glue Data Catalog
- Development endpoints for developing ETL code charged by the minute

### Glue Anti-Patterns

- Multiple ETL Engines
    - Glue ETL is based on Spark
    - If you want to use other engines (Hive, Pig, etc) Data Pipeline EMR would be a better fit.

#### No-longer an anti-pattern : Streaming

- As of April 2020, Glue ETL supports serverless streaming ETL
    - Consumes from Kinesis or Kafka
    - Clean & transform in-flight
    - Store results into S3 or other data stores
- Runs on Apache Spark Structured Streaming

### AWS Glue Studio

- Visual Interface for ETL workflows
- Visual Job Editor
    - Create DAG's for complex workflows
    - Sources include S3, Kinesis, Kafka, JDBC
    - Transform/Sample/Join data
    - Target to S3 or Glue Data Catalog
    - Support Partitioning
- Visual Job Dashboard
    - Overviews, Status, Run times

### AWS Glue Data Quality

- Data quality rules maybe created manually or recommended automatically
- Integrates into Glue Jobs
- Uses Data Quality Definition (DQDL)
- Results can be used to fail the job, or just be reported to CloudWatch

### Glue DataBrew

- A visual data preparation tool
    - UI for pre-processing large data sets\
    - Input from S3, data warehouse, or database
    - Output to S3
- Over 250 ready-made transformations
- You create “recipes” of transformations that can be saved as jobs within a larger project
- May define data quality rules
- May create datasets with custom SQL from Redshift and Snowflake
- Security
    - Can integrate with KMS (with customer master keys only)
    - SSL in transit
    - IAM can restrict who can do what
    - CloudWatch & CloudTrail
### Handling PII in Data Brew Transformations

- Enable PII statistics in a DataBrew profile job to identify PII
- Substitution (`REPLACE_WITH_RANDOM…`)
- Shuffling (`SHUFFLE_ROWS`)
- Deterministic encryption (`DETERMINISTIC_ENCRYPT`)
- Probabilistic encryption (`ENCRYPT`)
- Decryption (`DECRYPT`)
- Nulling out or deletion (`DELETE`)
- Masking out (`MASK_CUSTOM, _DATE, _DELIMITER, _RANGE`)
- Hashing (`CRYPTOGRAPHIC_HASH`)

### Glue Workflows

![](assets/Pasted%20image%2020251110141610.png)

- Design multi-job, multi-crawler ETL processes run together
- Create from AWS Glue blueprint, from the console, or API
- This is only for orchestrating complex ETL operations using Glue
### Glue Workflows Trigger

- Triggers within workflows start jobs or crawlers
    - Or can be fired when jobs or crawlers complete
- Schedule
    - Based on a cron expression
- On demand
- EventBridge events
    - Start on single event or batch of events
    - For example, arrival of a new object in S3
    - Optional batch conditions
        - Batch size (number of events)
        - Batch window (within X seconds, default is 15 min)

## AWS Lake Formation

![](assets/Pasted%20image%2020251110154815.png)

- No cost for Lake Formation itself
- But underlying services incur charges
    - Glue
    - S3
    - EMR
    - Athena
    - Redshift

### Important Points

- Cross-account Lake Formation permission
    - recipient must be set up as a data lake administrator
    - Can use AWS Resource Access Manager (RAM) for accounts external to org
    - IAM permissions for cross-account access
- Lake Formation doesn't support manifests in Athena or Redshift queries
- IAM permissions on the KMS encryption key are needed for encrypted data catalogs in Lake Formation
- IAM Permission needed to create blueprint and workflows

### Permissions

- can tie to IAM users/roles, SAML, or external AWS accounts
- can use policy tags on databases, tables or columns
- can select specific permission for tables or columns

### Data Filters in Lake Formation

- Column, row, or cell-level security
- Apply when granting SELECT permission on tables
- “All columns” + row filter = row-level security
- “All rows” + specific columns = column-level security
- Specific columns + specific rows = cell-level security
- Create filters via the console or via CreateDataCellsFilter API

## AWS Athena

- serverless interactive queries of S3 data

### What is Athena ?

- interactive query service for S3 (SQL)
    - no need to load data, it stays in S3
- Presto under the hood
- serverless
- supports many data formats
    - CSV, TSV
    - JSON
    - ORC
    - Parquet
    - Avro
    - Snappy, Zlin, LZO, Gzip compression
- Unstructured, semi-structured or structured

### Examples

- Ad-hoc queries of web logs
- Querying staging data before loading to Redshift
- Analyze CloudTrail / CloudFront / VPC / ELB etc logs in S3
- Integration with Jupyter, Zeppelin, RStudio notebooks
- Integration with QuickSight
- Integration via ODBC / JDBC with other visualization tools

### Athena + Glue

![](assets/Pasted%20image%2020251110155713.png)

### Athena Workgroups

- Can organize users / teams / apps / workloads into Workgroups
- Can control query access and track costs by Workgroup
- Integrates with IAM, CloudWatch, SNS
- Each workgroup can have its own:
    - Query history
    - Data limits (you can limit how much data queries may scan by workgroup)
    - IAM policies
    - Encryption settings

### Athena Cost Model

- Pay-as-you-go
    - $5 per TB scanned
    - successful or cancelled queries count, failed queries do not
    - No charge for DDL
- Save lots of money by using columnar formats
    - ORC, Parquet
    - Save 30-90% and get better performance
- Glue and S3 have their own charges

### Athena Security

- Access control
    - IAM, ACLs, S3 bucket policies
    - AmazonAthenaFullAccess / AWSQuicksightAthenaAccess
- Encrypt results at rest in S3 staging directory
    - Server-side encryption with S3-managed key (SSE-S3)
    - Server-side encryption with KMS key (SSE-KMS)
    - Client-side encryption with KMS key (CSE-KMS)
- Cross-account access in S3 bucket policy possible
- Transport Layer Security (TLS) encrypts in- transit (between Athena and S3)

### Athena Anti-Patterns

- Highly formatted reports / visualization
    - That’s what QuickSight is for
- ETL
    - Use Glue instead

### Optimizing performance

- Use columnar data (ORC, Parquet)
- Small number of large files performs better than large number of small files
- Use partitions
    - If adding partitions after the fact, use MSCK REPAIR TABLE command

### Athena ACID Transactions

- Powered by Apache Iceberg
    - Just add `‘table_type’ = ‘ICEBERG’` in your CREATE TABLE command
- Concurrent users can safely make row-level modifications
- Compatible with EMR, Spark, anything that supports Iceberg table format.
- Removes need for custom record locking
- Time travel operations
    - Recover data recently deleted with a SELECT statement
- Remember governed tables in Lake Formation? This is another way of getting ACID features in Athena.
- Benefits from periodic compaction to preserve performance
### Fine-Grained Access to AWS Glue Data Catalog

- IAM-based Database and table- level security
- Broader than data filters in Lake Formation
- Cannot restrict to specific table versions
- At a minimum you must have a policy that grants access to your database and the Glue Data Catalog in each region.
- You might have policies to restrict access to:
    - ALTER or CREATE DATABASE
    - CREATE TABLE
    - DROP DATABASE or DROP TABLE
    - MSCK REPAIR TABLE
    - SHOW DATABASES or SHOW TABLES
- Just need to map these operations to their IAM actions
- Example: DROP TABLE

### Iceberg

- Apache Iceberg is a table format for data lakes
    - PetaBytes scale
    - Originally from Netflix
- ACID Compliance
    - Row-level updates and deletes for GDPR compliance
- Schema Evolution
- Hidden Partitioning
- Time Travel
- Efficient Metadata Management
- Works with Spark, Flink, Trino, Presto, Hive
- Integrated with AWS Glue, EMR and Athena

### Iceberg + AWS Glue/S3

![](assets/Pasted%20image%2020251110190633.png)

- Glue can take the place of Hive as Iceberg's source of table metadata
- Iceberg's API communicates with Glue Catalog for metadata
- Iceberg stores/retrieves files from Amazon S3
    - Usually in Parquet Format
- Spark/Flink can then sit on top of the Iceberg API
- Also Athena for ACID Transactions !

### Migrating Glue Data Catalogs to Iceberg

- Glue Data catalogs must be made compatible with Iceberg API
- Once done, Athena can use it for ACID transactions
- Other reasons to migrate
    - compliance, historical reporting with time travel queries
    - data lake with many active producers and consumers
- In-Place Migrations : leave data files where they are, just create Iceberg metadata
- Shadow Migration
    - copies the data over
    - allows additional validation
    - easier rollback and recovery

### Athena Federated Queries

- Query data from sources other than S3
- Data source connectors translate between source and Athena
- These run on Lambda
- Many, many are available : cloudwatch, DynamoDB, Document DB, RDS, OpenSearch, etc.
- Views on federated data sources
    - Stored in AWS Glue
- Can use with AWS Secrets Manager
- Some connectors maybe integrated with AWS Glue
    - provides fine-grained access control via Lake Formation
    - Redshift, BigQuery, DynamoDB, Snowflake, MySQL etc
- Cross-account federated queries are possible with appropriate permissions
- Passthrough Queries allow you to use the native query language of the data source
- Some connectors may be used as Spark data sources

## Apache Spark

![](assets/Pasted%20image%2020251110191455.png)

- Distributed Processing Framework for big data
- In-Memory Caching, optimized query execution
- Supports Java, Scala, Python, and R
- Supports code reuse acroos
    - Batch Processing
    - Interactive Queries ~ SparkSQL
    - Real-Time Analytics
    - Machine Learning
        - MLLib
    - Graph Processsing
- Spark Streaming
    - Integrated with Kinesis, Kafka, on EMR
- Spark is NOT meant for OLTP

### How Spark Works

![](assets/Pasted%20image%2020251110191751.png)

- Spark apps are run as independent processes on a cluster
- The SparkContext(driver program) coordinates them
- Spark Context works through a Cluster Manager
- Executors run computations and store data
- Spark Context sends application code and tasks to executors

### Spark Components

![](assets/Pasted%20image%2020251110192213.png)

### Spark Structured Streaming (A constantly growing DataSet)

![](assets/Pasted%20image%2020251110192300.png)

```python
val inputDF = spark.readStream.json("s3://logs") 
inputDF.groupBy($"action", window($"time", "1 hour")).count()
        .writeStream.format("jdbc").start("jdbc:mysql//...")
```

### Spark Streaming + Kinesis

![](assets/Pasted%20image%2020251110192509.png)

### Spark + Redshift

- spark-redshift package allows Spark datasets from Redshift
    - Its a spark SQL data source
- Useful for ETL using Spark

![](assets/Pasted%20image%2020251110192606.png)

### Amazon Athena for Apache Spark

- Can run Jupyter notebooks with Spark within Athena console
    - Notebooks may be encrypted automatically or with KMS
- Totally serverless
- Selectable as an alternate analytics engine (vs. Athena SQL)
- Uses Firecracker for quickly spinning up Spark resources
- Programmatic API / CLI access as well
    - create-work-group, create-notebook, start-session, start-calculation-execution
- Can adjust DPU’s for coordinator and executor sizes
- Pricing based on compute usage and DPU per hour

## Amazon EMR

- Elastic MapReduce
- Managed Hadoop framework on EC2 instances
- Includes Spark, HBase, Presto, Flink, Hive & More
- EMR Notebooks
- Several integration points with AWS

### An EMR Cluster

![](assets/Pasted%20image%2020251110195041.png)

- Master node: manages the cluster
    - Tracks status of tasks, monitors cluster health
    - Single EC2 instance (it can be a single node cluster even)
    - AKA “leader node”
- Core node: Hosts HDFS data and runs tasks
    - Can be scaled up & down, but with some risk
    - Multi-node clusters have at least one
- Task node: Runs tasks, does not host data
    - Optional
    - No risk of data loss when removing
    - Good use of *spot instances*

### EMR Usage

- Transient vs Long-Running Clusters
    - Transient clusters terminate once all steps are complete
        - Loading data, processing, storing – then shut down
        - Saves money
    - Long-running clusters must be manually terminated
    - Basically a data warehouse with periodic processing on large datasets
    - Can spin up task nodes using Spot instances for temporary capacity
    - Can use reserved instances on long-running clusters to save $
    - Termination protection on by default, auto-termination off
- Frameworks and applications are specified at cluster launch
- Connect directly to master to run jobs directly
- Or, submit ordered steps via the console
    - Process data in S3 or HDFS
    - Output data to S3 or somewhere
    - Once defined, steps can be invoked via the console

### EMR/AWS Integration

- Amazon EC2 for the instances that comprise the nodes in the cluster
- Amazon VPC to configure the virtual network in which you launch your instances
- Amazon S3 to store input and output data
- Amazon CloudWatch to monitor cluster performance and configure alarms
- AWS IAM to configure permissions
- AWS CloudTrail to audit requests made to the service
- AWS Data Pipeline to schedule and start your clusters
### EMR Storage

- HDFS
    - Hadoop Distributed File System
    - Multiple copies stored across cluster instances for redundancy
    - Files stored as blocks (128MB default size)
    - Ephemeral – HDFS data is lost when cluster is terminated!
    - But, useful for caching intermediate results or workloads with significant random I/O
    - Hadoop tries to process data where it is stored on HDFS
- EMRFS: access S3 as if it were HDFS
    - Allows persistent storage after cluster termination
    - EMRFS Consistent View – Optional for S3 consistency
        - Uses DynamoDB to track consistency
        - May need to tinker with read/write capacity on DynamoDB
    - S3 is Now Strongly Consistent

- Local file system
    - Suitable only for temporary data (buffers, caches, etc)
- EBS for HDFS
    - Allows use of EMR on EBS-only types (M4, C4)
    - Deleted when cluster is terminated
    - EBS volumes can only be attached when launching a cluster
    - If you manually detach an EBS volume, EMR treats that as a failure and replaces it

### EMR Promise

- EMR charges by the hour
    - Plus EC2 charges
- Provisions new nodes if a core node fails
- Can add and remove tasks nodes on the fly
- Increase processing capacity, but not HDFS capacity
- Can resize a running cluster’s core nodes
- Increases both processing and HDFS capacity
- Core nodes can also be added or removed
- But removing risks data loss

### EMR Managed Scaling

- EMR Automatic Scaling
    - The old way of doing it
    - Custom scaling rules based on CloudWatch metrics
    - Supports instance groups only
- EMR Managed Scaling
    - Introduced in 2020
    - Support instance groups and instance fleets
    - Scales spot, on-demand, and instances in a Savings Plan within the same cluster
    - Available for Spark, Hive, YARN workloads
- Scale-up Strategy
    - First adds core nodes, then task nodes, up to max units specified
- Scale-down Strategy
- First removes task nodes, then core nodes, no further than minimum constraints
- Spot nodes always removed before on-demand instances
### EMR Serverless

- Choose an EMR Release and Runtime (Spark, Hive, Presto)
- Submit queries / scripts via job run requests
- EMR manages underlying capacity
    - But you can specify default worker sizes & pre-initialized capacity
    - EMR computes resources needed for your job & schedules workers accordingly
    - All within one region (across multiple AZ’s)
- Why is this a big deal?
    - You no longer have to estimate how many workers are needed for your workloads – they are provisioned as needed, automatically.
- Serverless? Really?
- TBH you still need to think about worker nodes and how they are configured


![](assets/Pasted%20image%2020251110200926.png)

### EMR Serverless Application Lifecycle

![](assets/Pasted%20image%2020251110200954.png)
### Pre-initialized Capacity

- Spark adds 10% overhead to memory requested for drivers & executors
- Be sure initial capacity is at least 10% more than requested by the job
### EMR serverless security

- Basically the same as EMR
- EMRFS
    - S3 encryption (SSE or CSE) at rest
    - TLS in transit between EMR nodes and S3
- S3
    - SSE-S3, SSE-KMS
- Local disk encryption
- Spark communication between drivers & executors is encrypted
- Hive communication between Glue Metastore and EMR uses TLS
- Force HTTPS (TLS) on S3 policies with aws:`SecureTransport`

### EMR on KMS

![](assets/Pasted%20image%2020251110201106.png)

- Allows submitting Spark job on Elastic Kubernetes Service without provisioning clusters
- Fully managed
- Share resources between Spark and other apps on Kubernetes