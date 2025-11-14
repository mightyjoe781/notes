# Analytics

## AWS Kinesis

![](assets/Pasted%20image%2020251110221321.png)

- Retention between 1 day to 365 days
- Ability to reprocess (replay) data
- Once data is inserted in Kinesis, it can't be deleted (immutability)
- Data that shares the same partition goes to the same shard (ordering)
- Producers : AWS SDK, Kinesis Producer Library (KPL), Kinesis Agent
- Consumers:
    - Write your own : Kinesis Client Library (KCL), AWS SDK
    - Managed: AWS lambda, Kinesis Data Firehose, Kinesis Data Analytics

### Kinesis Data Streams - Capacity Modes

- Provisioned Mode
    - You choose the number of shards provisioned, scale manually or using API
    - Each shard gets 1MB/s in (or 1000 records per second)
    - Each shard gets 2MB/s (classic or enhanced fan-out consumer)
    - You pay per shard provisioned per hour
- On-demand Mode:
    - No need to provision or manage the capacity
    - Default capacity provisioned (4 MB/s in or 4000 records per second)
    - Scales automatically based on observed throughput peak during the last 30 days
    - Pay per stream per hour & data in/out per GB

### Kinesis Data Streams Security

![](assets/Pasted%20image%2020251110222100.png)

- Control access / authorization using IAM policies
- Encryption in flight using HTTPS endpoints
- Encryption at rest using KMS
- You can implement encryption/decryption of data on client side (harder)
- VPC Endpoints available for Kinesis to access within VPC
- Monitor API calls using CloudTrail

### Kinesis Producers

- Kinesis SDK
- Kinesis Producer Library (KPL)
- Kinesis Agent
- 3rd pary libraries : Spark, Log4j Appenders, Flume, Kafka Connect, NiFi

### Kinesis Producers SDK - PutRecord(s)

- APIs that are used are PutRecord (one) and PutRecords (many records)
- PutRecords uses batching & increases throughput => less HTTP requests
- Provisioned ThroughputExceeded if we go over limits
- +AWS Mobile SDK: Android, iOS, etc
- Use case : low throughput, higher latency, simple API, AWS Lambda
- Managed AWS sources for Kinesis Data Streams
    - CloudWatch Logs
    - AWS IoT
    - Kinesis Data Analytics

### AWS Kinesis API - Exceptions

- ProvisionedThroughputExceeded Exceptions
    - Happens when sending more data (exceeding MB/s or TPS for any shard)
    - Make sure you don’t have a hot shard (such as your partition key is bad and too much data goes to that partition)
- Solution:
    - Retries with backoff
    - Increase shards (scaling)
    - Ensure your partition key is a good one

### Kinesis Producer Library (KPL)

- Easy to use and highly configurable C++ / Java library
- Used for building high performance, long-running producers
- Automated and configurable retry mechanism
- Synchronous or Asynchronous API (better performance for async)
- Submits metrics to CloudWatch for monitoring
- Batching (both turned on by default) – increase throughput, decrease cost:
    - Collect Records and Write to multiple shards in the same PutRecords API call
    - Aggregate – increased latency
        - Capability to store multiple records in one record (go over 1000 records per second limit)
        - Increase payload size and improve throughput (maximize 1MB/s limit)
- Compression must be implemented by the user
- KPL Records must be de-coded with KCL or special helper library

### Kinesis Producer Library (KPL)

![](assets/Pasted%20image%2020251110222714.png)

- We can influence the batching efficiency by introducing some delay with *RecordMaxBufferedTime* (default 100ms)

### KPL - When not to use

![](assets/Pasted%20image%2020251110222939.png)

- The KPL can incur an additional processing delay of up to RecordMaxBufferedTime within the library (user-configurable)
- Larger values of RecordMaxBufferedTime results in higher packing efficiencies and better performance
- Applications that cannot tolerate this additional delay may need to use the AWS SDK directly

### Kinesis Agent

- Monitor Log files and sends them to Kinesis Data Streams
- Java-based agent, built on top of KPL
- Install in Linux-based server environments
- Features:
    - Write from multiple directories and write to multiple streams
    - Routing feature based on directory / log file
    - Pre-process data before sending to streams (single line, csv to json, log to json…)
    - The agent handles file rotation, checkpointing, and retry upon failures
    - Emits metrics to CloudWatch for monitoring

### Kinesis Consumers - Classic

- Kinesis SDK
- Kinesis Client Library (KCL)
- Kinesis Connector Library
- 3rd party libraries: Spark, Log4J Appenders, Flume, Kafka Connect…
- Kinesis Firehose
- AWS Lambda
- (Kinesis Consumer Enhanced Fan-Out discussed in the next lecture)

### Kinesis Consumer SDK - Get Records

![](assets/Pasted%20image%2020251110223542.png)

- Classic Kinesis - Records are polled by consumers from a shard
- Each shard has 2 MB total aggregate throughput
- GetRecords returns up to 10MB of data (then throttle for 5 seconds) or up to 10000 records
- Maximum of 5 GetRecords API calls per shard per second = 200ms latency
- If 5 consumers application consume from the same shard, means every consumer can poll once a second and receive less than 400 KB/s

### Kinesis Client Library (KCL)

![](assets/Pasted%20image%2020251110224308.png)

- Java-first library but exists for other languages too (Golang, Python, Ruby, Node, .NET …)
- Read records from Kinesis produced with the KPL (de-aggregation)
- Share multiple shards with multiple consumers in one “group”, shard discovery
- Checkpointing feature to resume progress
- Leverages DynamoDB for coordination and checkpointing (one row per shard)
    - Make sure you provision enough WCU / RCU
    - Or use On-Demand for DynamoDB
    - Otherwise DynamoDB may slow down KCL
- Record processors will process the data
- ExpiredIteratorException => increase WCU

### Kinesis Connector Library

![](assets/Pasted%20image%2020251110224408.png)

- Older Java library (2016), leverages the KCL library
- Write data to:
    - Amazon S3
    - DynamoDB
    - Redshift
    - OpenSearch
- Kinesis Firehose replaces the Connector Library for a few of these targets, Lambda for the others

### AWS Lambda sourcing from Kinesis

- AWS Lambda can source records from Kinesis Data Streams
- Lambda consumer has a library to de-aggregate record from the KPL
- Lambda can be used to run lightweight ETL to:
    - Amazon S3
    - DynamoDB
    - Redshift
    - OpenSearch
    - Anywhere you want
- Lambda can be used to trigger notifications / send emails in real time
- Lambda has a configurable batch size (more in Lambda section)

### Kinesis Enhanced Fan Out

- New game-changing feature from August 2018.
- Works with KCL 2.0 and AWS Lambda (Nov 2018)
- Each Consumer get 2 MB/s of provisioned throughput per shard
- That means 20 consumers will get 40MB/s per shard aggregated
- No more 2 MB/s limit!
- Enhanced Fan Out: Kinesis pushes data to consumers over HTTP/2
- Reduce latency (~70 ms)

### Enhanced Fan-Out vs Standard Consumers

- Standard consumers:
    - Low number of consuming applications (1,2,3…)
    - Can tolerate ~200 ms latency
    - Minimize cost
- Enhanced Fan Out Consumers:
    - Multiple Consumer applications for the same Stream
    - Low Latency requirements ~70ms
    - Higher costs (see Kinesis pricing page)
    - Default limit of 20 consumers using enhanced fan-out per data stream

### Kinesis Operations - Adding Shards

![](assets/Pasted%20image%2020251110235926.png)

- aka *Shard Splitting*
- Can be used to increase the Stream capacity (1MB/s data in per shard)
- can be used to divide a *hot-shard*
- the old shard is closed and will be deleted once the data is expired
### Kinesis Operations - Merging Shards

![](assets/Pasted%20image%2020251111000012.png)

- Decrease the Stream capacity and save costs
- Can be used to group two shards with low traffic
- Old shards are closed and deleted based on data expiration

### Out-of-order records after resharding

![](assets/Pasted%20image%2020251111000129.png)

- After a reshard, you can read from child shards
- However, data you haven’t read yet could still be in the parent
- If you start reading the child before completing reading the parent, you could read data for a particular hash key out of order
- After a reshard, read entirely from the parent until you don’t have new records
- Note: The Kinesis Client Library (KCL) has this logic already built-in, even after resharding operations

### Kinesis Operations - Auto scaling

- Autoscaling is not a native feature of Kinesis
- The API call to change the number of shards is Update Shard Count
- We can implement AutoScaling with AWS Lambda
- See : https://aws.amazon.com/blogs/big-data/scaling-amazon-kinesis-data-streams-with-aws-application-auto-scaling/

### Kinesis Scaling Limitation

- Resharding cannot be done in parallel. Plan capacity in advance
- You can only perform one resharding operation at a time and it takes a few seconds
- For 1000 shards, it takes 30K seconds (8.3 hours) to double the shards to 2000
- You can’t do the following:
    - Scale more than 10x for each rolling 24-hour period for each stream
    - Scale up to more than double your current shard count for a stream
    - Scale down below half your current shard count for a stream
    - Scale up to more than 10,000 shards in a stream
    - Scale a stream with more than 10,000 shards down unless the result is less than 10,000 shards
    - Scale up to more than the shard limit for your account

### Kinesis Data Streams - Handling Duplicates for Producers

![](assets/Pasted%20image%2020251111000326.png)

- Producer retries can create duplicates due to network timeouts
- Although the two records have identical data, they also have unique sequence numbers
- Fix: embed unique record ID in the data to de-duplicate on the consumer side

### Kinesis Data Streams - Handling Duplicates for Consumers

- Consumer retries can make your application read the same data twice
- Consumer retries happen when record processors restart:
    - A worker terminates unexpectedly
    - Worker instances are added or removed
    - Shards are merged or split
    - The application is deployed
- Fixes:
    - Make your consumer application idempotent
    - If the final destination can handle duplicates, it’s recommended to do it there

### Kinesis Security

- Control access / authorization using IAM policies
- Encryption in flight using HTTPS endpoints
- Encryption at rest using KMS
- Client side encryption must be manually implemented (harder)
- VPC Endpoints available for Kinesis to access within VPC

## AWS Data Firehose

![](assets/Pasted%20image%2020251111000813.png)

- Fully Managed Service, no administration
- Near Real Time (Buffer based on time and size, optionally can be disabled)
- Load data into Redshift / Amazon S3 / OpenSearch / Splunk
- Automatic scaling
- Supports many data formats
- Data Conversions from JSON to Parquet / ORC (only for S3)
- Data Transformation through AWS Lambda (ex: CSV => JSON)
- Supports compression when target is Amazon S3 (GZIP, ZIP, and SNAPPY)
- Only GZIP is the data is further loaded into Redshift
- Pay for the amount of data going through Firehose
- Spark / KCL do not read from KDF

### Kinesis Data Firehose Delivery Diagram

![](assets/Pasted%20image%2020251111000910.png)

### Firehose Buffer Sizing

- Firehose accumulates records in a buffer
- The buffer is flushed based on time and size rules
- Buffer Size (ex: 32MB): if that buffer size is reached, it’s flushed
- Buffer Time (ex: 2 minutes): if that time is reached, it’s flushed
- Firehose can automatically increase the buffer size to increase throughput
- High throughput => Buffer Size will be hit
- Low throughput => Buffer Time will be hit

### Kinesis Data Streams vs Firehose

- Streams
    - Going to write custom code (producer / consumer)
    - Real time (~200 ms latency for classic, ~70 ms latency for enhanced fan-out)
    - Must manage scaling (shard splitting / merging)
    - Data Storage for 1 to 365 days, replay capability, multi consumers
    - Use with Lambda to insert data in real-time to OpenSearch (for example)
- Firehose
    - Fully managed, send to S3, Splunk, Redshift, OpenSearch
    - Serverless data transformations with Lambda
    - Near real time
    - Automated Scaling
    - No data storage
### Troubleshooting Kinesis Data Stream Producers : Performance

- Writing is too slow
    - Service limits may be exceeded. Check for throughput exceptions, see what operations are being throttled. Different calls have different limits.
    - There are shard-level limits for writes and reads
    - Other operations (ie, CreateStream, ListStreams, DescribeStreams) have stream-level limits of 5-20 calls per second
    - Select partition key to evenly distribute puts across shards
- Large producers
    - Batch things up. Use Kinesis Producer Library, PutRecords with multi-records, or aggregate records into larger files.
- Small producers (i.e. apps)
    - Use PutRecords or Kinesis Recorder in the AWS Mobile SDKs

### Other Kinesis Data Stream Producer Issues

- Stream returns a 500 or 503 error
    - This indicates an AmazonKinesisException error rate above 1%
    - Implement a retry mechanism
- Connection errors from Flink to Kinesis
    - Network issue or lack of resources in Flink’s environment
        - Could be a VPC misconfiguration
- Timeout errors from Flink to Kinesis
- Adjust RequestTimeout and `#setQueueLimit` on FlinkKinesisProducer
- Throttling errors
    - Check for hot shards with enhanced monitoring (shard-level)
    - Check logs for “micro spikes” or obscure metrics breaching limits
    - Try a random partition key or improve the key’s distribution
    - Use exponential backoff
    - Rate-limit

### Troubleshooting Kinesis Data Stream Consumer

- Lambda function can’t get invoked
    - Permissions issue on execution role
    - Function is timing out (check max execution time)
    - Breaching concurrency limits
    - Monitor `IteratorAge` metric; it will increase is this is a problem
- ReadProvisionedThroughputExceeded exception
    - Throttling
    - Reshard your stream
    - Reduce size of GetRecords requests
    - Use enhanced fan-out
    - Use retries and exponential backoff
### Other Kinesis Data Stream Consumer Issues

- High latency
    - Monitor with GetRecords.Latency and IteratorAge
    - Increase shards
    - Increase retention period
    - Check CPU and memory utilization (may need more memory)
- 500 errors
    - Same as producers – indicates a high error rate (>1%)
    - Implement a retry mechanism
- Blocked or stuck KCL application
    - Optimize your processRecords method
    - Increase maxLeasesPerWorker
    - Enable KCL debug logs
## Kinesis Data Analytics/Managed Service for Apache Flink
*Querying streams of data*

![](assets/Pasted%20image%2020251111000511.png)

### Reference Tables

- nexpensive way to “join” data for quick lookups
    - i.e., look up the city associated with a zip code
    - Mapping is stored in S3 which is very inexpensive
    - Just use a “JOIN” command to use the data in your queries
### Kinesis Data Analytics + lambda

- AWS Lambda can be a destination as well
- Allows lots of flexibility for post-processing
    - Aggregating rows
    - Translating to different formats
    - Transforming and enriching data
    - Encryption
- Opens up access to other services & destinations
    - S3, DynamoDB, Aurora, Redshift, SNS, SQS, CloudWatch
### Managed Service for Apache Flink

![](assets/Pasted%20image%2020251111002636.png)

- Formerly Kinesis Data Analytics for Apache Flink or for Java
    - Kinesis Data Analytics always used Flink under the hood
    - But now supports Python and Scala
    - Flink is a framework for processing data streams
- MSAF integrates Flink with AWS
    - Instead of using SQL, you can develop your own Flink application from scratch and load it into MSAF via S3
    - In addition to the DataStream API, there is a Table API for SQL access
    - Serverless

### Apache Flink capabilities

![](assets/Pasted%20image%2020251111002546.png)

- Connectors
    - The flink-connector-kinesis library lets you consume a data stream from Java
    - A library of “Table API Connectors” are included in Flink
        - Kafka, DynamoDB, Firehose, Kinesis, MongoDB, Opensearch, JDBC…
    - Custom “sink” connectors allow Flink to talk to anything you have an SDK for
        - For example, you could write a sink to connect to a Timestream database
- Operators
    - Transform one or more DataStreams into a new DataStream
    - Similar to Apache Spark transformations
        - Map, Flatmap, Filter, Reduce, Windows, Join
    - Physical partitioning
    - Task chaining

### Common Use-Cases

- Streaming ETL
- Continuous metric generation
- Responsive analytics

### Kinesis Analytics

- Pay only for resources consumed (but it’s not cheap)
    - Charged by Kinesis Processing Units (KPU’s) consumed per hour
    - 1 KPU = 1 vCPU + 4GB
- Serverless; scales automatically
- Use IAM permissions to access streaming source and destination(s)
- Schema discovery

### RANDOM_CUT_FOREST

- SQL function used for anomaly detection on numeric columns in a stream
- They’re especially proud of this because they published a paper on it
- It’s a novel way to identify outliers in a data set so you can handle them however you need to
- Example: detect anomalous subway ridership during the NYC marathon

## Amazon MSK

- Alternative to Kinesis (Kafka vs Kinesis next lecture)
- Fully managed Apache Kafka on AWS
    - Allow you to create, update, delete clusters
    - MSK creates & manages Kafka brokers nodes & Zookeeper nodes for you
    - Deploy the MSK cluster in your VPC, multi-AZ (up to 3 for HA)
    - Automatic recovery from common Apache Kafka failures
    - Data is stored on EBS volumes
- You can build producers and consumers of data
- Can create custom configurations for your clusters
    - Default message size of 1MB
    - Possibilities of sending large messages (ex: 10MB) into Kafka after custom configuration

![](assets/Pasted%20image%2020251111082248.png)

### MSK - Configurations

![](assets/Pasted%20image%2020251111082334.png)

- Choose the number of AZ (3 – recommended, or 2)
- Choose the VPC & Subnets
- The broker instance type (ex: kafka.m5.large)
- The number of brokers per AZ (can add brokers later)
- Size of your EBS volumes (1GB – 16TB)

### MSK Security

![](assets/Pasted%20image%2020251111082433.png)

- Encryption:
    - Optional in-flight using TLS between the brokers
    - Optional in-flight with TLS between the clients and brokers
    - At rest for your EBS volumes using KMS
- Network Security:
    - Authorize specific security groups for your Apache Kafka clients
- Authentication & Authorization (important):
    - Define who can read/write to which topics
    - Mutual TLS (AuthN) + Kafka ACLs (AuthZ)
    - SASL/SCRAM (AuthN) + Kafka ACLs (AuthZ)
    - IAM Access Control (AuthN + AuthZ)

### MSK - Monitoring

- CloudWatch Metrics
    - Basic monitoring (cluster and broker metrics)
    - Enhanced monitoring (++enhanced broker metrics)
    - Topic-level monitoring (++enhanced topic-level metrics)
- Prometheus (Open-Source Monitoring)
    - Opens a port on the broker to export cluster, broker and topic-level metrics
    - Setup the JMX Exporter (metrics) or Node Exporter (CPU and disk metrics)
- Broker Log Delivery
    - Delivery to CloudWatch Logs
    - Delivery to Amazon S3
    - Delivery to Kinesis Data Streams

### MSK Connect

- Managed Kafka Connect workers on AWS
- Auto-scaling capabilities for workers
- You can deploy any Kafka Connect connectors to MSK Connect as a plugin
    - Amazon S3, Amazon Redshift, Amazon OpenSearch, Debezium, etc…
- Example pricing: Pay $0.11 per worker per hour

![](assets/Pasted%20image%2020251111082632.png)

### MSK Serverless

- Run Apache Kafka on MSK without managing the capacity
- MSK automatically provisions resources and scales compute & storage
- You just define your topics and your partitions and you’re good to go!
- Security: IAM Access Control for all clusters
- Example Pricing:
    - $0.75 per cluster per hour = $558 monthly per cluster
    - $0.0015 per partition per hour = $1.08 monthly per partition
    - $0.10 per GB of storage each month
    - $0.10 per GB in
    - $0.05 per GB out

### MSK vs Kinesis

| Kinesis Data Streams                                                | Amazon MSK                                                                                                                                  |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 MB message size limit                                             | 1MB default, configure for higher (ex:<br>10MB)                                                                                             |
| Data Streams with Shards                                            | - Can only add partitions to a topic<br>- Kafka Topics with Partitions                                                                      |
| Shard Splitting & Merging                                           | PLAINTEXT or TLS In-flight Encryption                                                                                                       |
| TLS In-flight encryption                                            | KMS At-rest encryption                                                                                                                      |
| KMS At-rest encryption<br>Security:<br>IAM policies for AuthN/AuthZ | Security:<br>- Mutual TLS (AuthN) + Kafka ACLs (AuthZ)<br>- SASL/SCRAM (AuthN) + Kafka ACLs (AuthZ)<br>- IAM Access Control (AuthN + AuthZ) |
|                                                                     |                                                                                                                                             |

## Amazon OpenSearch (formerly ElasticSearch)

### What is OpenSearch ?

- A fork of Elasticsearch and Kibana
- A search engine
- An analysis tool
- A visualization tool (Dashboards = Kibana)
- A data pipeline
- Kinesis replaces Beats & LogStash
- Horizontally scalable

### Opensearch Applications

- Full-text search
- Log analytics
- Application monitoring
- Security analytics
- Clickstream analytics

### Opensearch Concepts

![](assets/Pasted%20image%2020251111083454.png)

### An index is split into *shards*

![](assets/Pasted%20image%2020251111083526.png)

### Redundancy

![](assets/Pasted%20image%2020251111083551.png)

### Amazon OpenSearch Service (managed)

- Fully-managed (but not serverless)
    - There is a separate serverless option now
- Scale up or down without downtime
    - But this isn’t automatic
- Pay for what you use
    - Instance-hours, storage, data transfer
- Network isolation
- AWS integration
    - S3 buckets (via Lambda to Kinesis)
    - Kinesis Data Streams
    - DynamoDB Streams
    - CloudWatch / CloudTrail
    - Zone awareness

### Amazon Opensearch Options

- Dedicated master node(s)
    - Choice of count and instance types
- “Domains”
- Snapshots to S3
- Zone Awareness

### Cold/Warm/UltraWarm/Hot Storage

- Standard data nodes use “hot” storage
    - Instance stores or EBS volumes / fastest performance
- UltraWarm (warm) storage uses S3 + caching
    - Best for indices with few writes (like log data / immutable data)
    - Slower performance but much lower cost
    - Must have a dedicated master node
- Cold storage
    - Also uses S3
    - Even cheaper
    - For “periodic research or forensic analysis on older data”
    - Must have dedicated master and have UltraWarm enabled too
    - Not compatible with T2 or T3 instance types on data nodes
    - If using fine-grained access control, must map users to cold_manager role in OpenSearch Dashboards
- Data may be migrated between different storage types

### Index State Management

 - Automates index management policies
 - Examples
     - Delete old indices after a period of time
     - Move indices into read only state after a period of time
     - Move indices from hot -> UltraWarm -> cold storage over time
     - Reduce replica count over time
     - Automate index snapshots
 - ISM policies are run every 30-48 minutes
     - Random jitter to ensure they don’t all run at once
 - Can even send notifications when done
 - Index rollups
     - Periodically roll up old data into summarized indices
     - Saves storage costs
     - New index may have fewer fields, coarser time buckets
 - Index transforms
     - Like rollups, but purpose is to create a different view to analyze data differently.
     - Groupings and aggregations

### Cross-Cluster Replication

- Replicate indices / mappings / metadata across domains
- Ensures high availability in an outage
- Replicate data geographically for better latency
- “Follower” index pulls data from “leader” index
- Requires fine-grained access control and node-to-node encryption
- “Remote Reindex” allows copying indices from one cluster to another on demand

### OpenSearch Stability

- 3 dedicated master nodes is best
    - *Avoid splits brain*
- Don't run out of disk space
    - Min storage requirement is roughly: Source Data * (1 + number of replicas) * 1.45
- Choosing the number of shards
    - (source data + room to grow) * ( 1 + indexing overhead)/ desired shard size
    - In rare cases you may need to limit the number of shards per node
        - You usually run out of disk spaces first
- Choosing instance types
    - At least 3 nodes
    - Mostly about storage requirements
    - i.e. m6g.large.search, i3.4xlarge.search, i3.16xlarge.search

### Amazon Opensearch Security

- Resource-based policies
- Identity-based policies
- IP-based policies
- Request signing
- VPC
- Cognito

### Securing Dashboards

![](assets/Pasted%20image%2020251111110210.png)

- Cognito
- Getting inside a VPC from outside is hard
    - nginx reverse proxy on EC2 forwarding to ES domain
    - SSH tunnel for port 5601
    - VPC Direct Connect
    - VPN

### Amazon Opensearch anti-patterns

- OLTP
    - No transactions
    - RDS or DynamoDB is better
- Ad-hoc data querying
    - Athena is better
- Remember Opensearch is primarily for search & analytics

### Amazon Opensearch performance

- Memory pressure in the JVM can result if:
    - You have unbalanced shard allocations across nodes
    - You have too many shards in a cluster
- Fewer shards can yield better performance if JVMMemoryPressure errors are encountered
    - Delete old or unused indices

### Amazon Opensearch Serverless

- On-demand autoscaling!
- Works against “collections” instead of provisioned domains
    - May be “search” or “time series” type
- Always encrypted with your KMS key
    - Data access policies
    - Encryption at rest is required
    - May configure security policies across many collections
- Capacity measured in Opensearch Compute Units (OCUs)
    - Can set an upper limit, lower limit is always 2 for indexing, 2 for search

## Amazon QuickSight
*Business analytics and visualizations in the cloud*

- Fast, easy, cloud-powered business analytics service
- Allows all employees in an organization to:
    - Build visualizations
    - Build paginated reports
    - Perform ad-hoc analysis
    - Get alerts on detected anomalies
    - Quickly get business insights from data
    - Anytime, on any device (browsers, mobile)
- Serverless

### QuickSight Data Sources

- Redshift, Aurora/RDS, Athena, OpenSearch, IoT Analytics, EC2 Hosted databases, Files (S3 or on-premises)
- Data Preparation allows limited ETL

### SPICE

- Data sets are imported into SPICE
    - super-fast, parallel, in-memory Calculation Engine
    - Uses columnar storage, in-memory, machine code generation
    - Accelerates interactive queries on large datasets
- Each user gets 10GB of SPICE
- Highly available / durable
- Scales to hundreds of thousands of users
- Can accelerate large queries that would time out in direct query mode (hitting Athena directly)
- But if it takes more than 30 minutes to import your data into SPICE it will still time out

### QuickSight Use Cases

- Interactive ad-hoc exploration / visualization of data
- Dashboards and KPI’s
- Analyze / visualize data from:
    - Logs in S3
    - On-premise databases
    - AWS (RDS, Redshift, Athena, S3)
    - SaaS applications, such as Salesforce
    - Any JDBC/ODBC data source

### QuickSight Anti-Patterns

- ETL
    - Use Glue instead, although QuickSight can do some transformations

### QuickSight Security

- Multi-factor authentication on your account
- VPC connectivity
    - Add QuickSight’s IP address range to your database security groups
- Row-level security
    - New for 2021: Column-level security too (CLS) – Enterprise edition only
- Private VPC access
- Elastic Network Interface, AWS Direct Connect
- Resource access
    - Must ensure QuickSight is authorized to use Athena / S3 / your S3 buckets
    - This can be managed within the QuickSight console (Manage Quicksight / Security & Permissions)\
- Data access
    - Can create IAM policies to restrict what data in S3 given QuickSight users can access


### QuickSight + Redshift : Security

- By default Quicksight can only access data stored IN THE SAME REGION as the one Quicksight is running within
- So if Quicksight is running in one region, and Redshift in another, that’s a problem
- A VPC configured to work across AWS regions won’t work!
- Solution: create a new security group with an inbound rule authorizing access from the IP range of QuickSight servers in that region

### QuickSight/Redshift : RDS Cross-Region

![](assets/Pasted%20image%2020251111114141.png)

- Other ways to do it (if you have Enterprise Edition)
- Create a private subnet in a VPC
- Use Elastic Network Interface to put Quicksight in the subnet
    - This is the part that requires Enterprise Edition
- This can also enable cross- account access
- Now you can create a peering connection between your private subnet and another private subnet containing your data
- This also works for cross-account access

### QuickSight/Redshift : RDS Cross-Account

![](assets/Pasted%20image%2020251111114308.png)

- Can use an AWS Transit Gateway to connect your subnets
    - But this must be in the same org & region
    - Or you can peer Transit Gateways in different regions
- OR use AWS PrivateLink to connect them
- OR use VPC sharing to connect them

### User Management

- Users defined via IAM, or email signup
- Active Directory connector with QuickSight Enterprise Edition
    - All keys are managed by AWS; you CANNOT use customer-provided keys
    - Enterprise edition only!
    - Can tweak security access using IAM if needed

### Pricing

- Annual subscription
    - Standard: $9 / user /month
    - Enterprise: $18 / user / month
    - With Quicksight Q: $28 / user /month
- Extra SPICE capacity (beyond 10GB)
    - $0.25 (standard) $0.38 (enterprise) / GB / month
- Month to month
    - Standard: $12 / user / month
    - Enterprise: $24 / user / month
    - With Quicksight Q: $34 / user / month
- Enterprise edition
    - Encryption at rest
    - Microsoft Active Directory integration

### QuickSight Dashboards

- Read-only snapshots of an analysis
- Can share with others with Quicksight access
- Can share even more widely with embedded dashboards
    - Embed within an application
    - Authenticate with Active Directory / Cognito / SSO
    - QuickSight Javascript SDK / QuickSight API
    - Whitelist domains where embedding is allowed

