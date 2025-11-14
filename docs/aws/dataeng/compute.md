# Compute

## EC2 in Big Data

- On demand, Spot & Reserved instances:
    - Spot: can tolerate loss, low cost => checkpointing feature (ML, etc)
    - Reserved: long running clusters, databases (over a year)
    - On demand: remaining workloads
- Auto Scaling:
    - Leverage for EMR, etc
    - Automated for DynamoDB, Auto Scaling Groups, etc…
- EC2 is behind EMR
    - Master Nodes
    - Compute Nodes (contain data) + Tasks Nodes (do not contain data)

## AWS Graviton

- Amazon’s own family of processors, powers several EC2 instance types
    - General purpose: M7, T4
    - Compute optimized: C7, C6
    - Memory optimized: R7, X2
    - Storage optimized: Im4, Is4
    - Accelerated computing (game streaming, ML inference): G5
- Offers best price performance
- Option for many data engineering services
    - MSK, RDS, MemoryDB, ElastiCache, OpenSearch, EMR, Lambda, Fargate

## AWS Lambda

- A way to run code-snippets *in the cloud*, serverless, continuous scaling
- Often used to process data as it's moved around

Example ~ Order History App

![](assets/Pasted%20image%2020251109104708.png)

NOTE: In case datasource is Kinesis, Kinesis doesn't push data into lambda, Lambda polls and picks batched events from kinesis

Example : Transactions rate alarm

![](assets/Pasted%20image%2020251109104809.png)

- Use Cases
    - Real-time file processing
    - Real-time stream processing
    - Cron Replacement
    - ETL
    - Process AWS Events
- Supported Languages: Node.js, Python, Java, C#, Go, Rust, etc

### Lambda Triggers

![](assets/Pasted%20image%2020251109104918.png)

Examples of Lambda Integrations

![](assets/Pasted%20image%2020251109104938.png)

Lambda and Data Pipeline

![](assets/Pasted%20image%2020251109104949.png)

Lambda & Redshift

![](assets/Pasted%20image%2020251109105006.png)

NOTE: Best practice for loading data into Redshift is the COPY command
Generally used to with DynamoDB to track what's been loaded, Lambda can batch up the data and load it with *COPY* Command

### Lambda + Kinesis

- Your Lambda code receives an event with a batch of stream records
    - You specify a batch size when setting up the trigger (up to 10,000 records)
    - Too large a batch size can cause timeouts!
    - Batches may also be split beyond Lambda’s payload limit (6 MB)
- Lambda will retry the batch until it succeeds or the data expires
    - This can stall the shard if you don’t handle errors properly
    - Use more shards to ensure processing isn’t totally held up by errors
- Lambda processes shard data synchronously

### Cost Model

- Pay for what you use”
- Generous free tier (1M requests / month, 400K GB-seconds compute time)
- $0.20 / million requests
- $.00001667 per GB/second

### Other Promises

- High Availability
- Unlimited Scalability (safety throttle of 1000 concurrent executions)
- High Performance (max timeout of 900s)

### Lambda Anti Patterns

- Long-running applications
    - Use EC2 instead or chain functions
- Dynamic Websites
- Stateful application
    - But can work with DynamoDB or S3 to track state

### Lambda - File Systems Mounting

![](assets/Pasted%20image%2020251109105515.png)

- Lambda functions can access EFS file systems if they are running in a VPC
- Configure Lambda to mount EFS file systems to local directory during initialization
- Must leverage EFS Access Points
- Limitations: watch out for the EFS connection limits (one function instance = one connection) and connection burst limits


## AWS SAM

- SAM = Serverless Application Model
- Framework for developing and deploying serverless applications
- All the configuration is YAML code
- Generate complex CloudFormation from simple SAM YAML file
- Supports anything from CloudFormation: Outputs, Mappings, Parameters, Resources…
- SAM can use CodeDeploy to deploy Lambda functions
- SAM can help you to run Lambda, API Gateway, DynamoDB locally

### AWS SAM - Recipe

- Transform Header indicates it’s SAM template:
    - Transform: 'AWS::Serverless-2016-10-31'
- Write Code
    - AWS::Serverless::Function
    - AWS::Serverless::Api
    - AWS::Serverless::SimpleTable
- Package & Deploy: sam deploy (optionally preceded by “`sam package`”)
- Quickly sync local changes to AWS Lambda (SAM Accelerate): `sam sync -- watch`

![](assets/Pasted%20image%2020251109105845.png)

### SAM Accelerate (sam sync)

- SAM Accelerate is a set of features to reduce latency while deploying resources to AWS
- sam sync
    - Synchronizes your project declared in SAM templates to AWS
    - Synchronizes code changes to AWS without updating infrastructure (uses service APIs & bypass CloudFormation)

![](assets/Pasted%20image%2020251109105927.png)

## AWS Batch

- Run batch jobs as Docker images
- Dynamic provisioning of the instances (EC2 & Spot Instances)
- Optimal quantity and type based on volume and requirements
- No need to manage clusters, fully serverless
- You just pay for the underlying EC2 instances
- Schedule Batch Jobs using CloudWatch Events
- Orchestrate Batch Jobs using AWS Step Functions

### AWS Batch vs Glue

- Glue:
    - Glue ETL - Run Apache Spark code, Scala or Python based, focus on the ETL
    - Glue ETL - Do not worry about configuring or managing the resources
    - Data Catalog to make the data available to Athena or Redshift Spectrum
- Batch:
    - For any computing job regardless of the job (must provide Docker image)
    - Resources are created in your account, managed by Batch
    - For any non-ETL related work, Batch is probably better