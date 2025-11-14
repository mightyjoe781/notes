# Application Integration

## SQS

![](assets/Pasted%20image%2020251112204204.png)

- oldest offering (10yrs old)
- fully managed
- scales from 1 message per second to 15,000/s
- Default Retention of 4 days, max 14 days
- No limit on number of messages in the queue
- Low Latency (< 10ms on publish & receive)
- Horizontal scaling in terms of number of consumers
- Can have duplicated messages (at least once delivery, occasionally)
- can have out of order messages (best effort ordering)
- Limitation of 1024KB/message sent

### SQS Producing Messages

![](assets/Pasted%20image%2020251112204452.png)

- Define Body
- Add message attributes (metadata – optional)
- Provide Delay Delivery (optional)
- Get back
- Message identifier
- MD5 hash of the body

### SQS Consuming Messages

![](assets/Pasted%20image%2020251112204536.png)

- Consumers…
- Poll SQS for messages (receive up to 10 messages at a time)
- Process the message within the visibility timeout
- Delete the message using the message ID & receipt handle

### SQS - FIFO Queue

- Newer offering (First In - First out) – not available in all regions!
- Name of the queue must end in .fifo
- Lower throughput (up to 3,000 per second with batching, 300/s without)
- Messages are processed in order by the consumer
- Messages are sent exactly once
- 5-minute interval de-duplication using “Duplication ID”

### SQS Extended Client

![](assets/Pasted%20image%2020251112204647.png)

- Message size limit is 1024 KB, how to send large messages?
- Using the SQS Extended Client (Java Library)

### Use-Cases

- decouple applications (ex ~ handling payments asynchronously)
- Buffer writes to a database
- Handle large loads of messages coming in
- SQS can be integrated with Auto Scaling through Cloud Watch

### SQS Limits

- Max of 120, 000 in-flight messages being processed by consumers
- Batch Request has a maximum of 10 messages - max 1024KB
- Message content is XML, JSON, Unformatted text
- Standard queues have an unlimited TPS
- FIFO queues support up to 3,000 messages per second (using batching)
- Max message size is 1024 KB (or use Extended Client)
- Data retention from 1 minute to 14 days
- Pricing:
    - Pay per API Request
    - Pay per network usage

### SQS Security

- Encryption in flight using the HTTPS endpoint
- Can enable SSE (Server Side Encryption) using KMS
    - Can set the CMK (Customer Master Key) we want to use
    - SSE only encrypts the body, not the metadata (message ID, timestamp, attributes)
- IAM policy must allow usage of SQS
- SQS queue access policy
    - Finer grained control over IP
    - Control over the time the requests come in
### Kinesis vs SQS

![](assets/Pasted%20image%2020251112205003.png)

### SQS vs Kinesis ~ Use Cases

- SQS use cases:
    - Order processing
    - Image Processing
    - Auto scaling queues according to messages.
    - Buffer and Batch messages for future processing.
    - Request Offloading
- Kinesis Data Streams use cases:
    - Fast log and event data collection and processing
    - Real Time metrics and reports
    - Mobile data capture
    - Real Time data analytics
    - Gaming data feed
    - Complex Stream Processing
    - Data Feed from “Internet of Things”
### SQS Dead-Letter Queue (DLQ)

![](assets/Pasted%20image%2020251112205154.png)

- If a consumer fails to process a message within the Visibility Timeout… the message goes back to the queue!
- We can set a threshold of how many times a message can go back to the queue
- After the MaximumReceives threshold is exceeded, the message goes into a Dead Letter Queue (DLQ)
- Useful for debugging!
- DLQ of a FIFO queue must also be a FIFO queue
- DLQ of a Standard queue must also be a Standard queue
- Make sure to process the messages in the DLQ before they expire:
    - Good to set a retention of 14 days in the DLQ

### SQS DLQ - Redrive to Source

- Feature to help consume messages in the DLQ to understand what is wrong with them
- When our code is fixed, we can redrive the messages from the DLQ back into the source queue (or any other queue) in batches without writing custom code

## SNS
*send one message to many receivers ?*

![](assets/Pasted%20image%2020251112221621.png)

- The *event producer* only sends message to one SNS topic
- As many *event receivers* (subscriptions) as we want to listen to SNS topic
- Each subscriber to topic will get all the messages (NOTE: new features to filter messages)
- Up to 12,50,000 subscriptions per topic
- 100, 000 topics limit
- Many AWS services can send data directly to SNS for notifications

![](assets/Pasted%20image%2020251112221750.png)

![](assets/Pasted%20image%2020251112221819.png)

### How to publish

- Topic Publish (using the SDK)
    - Create a topic
    - Create a subscription (or many)
    - Publish to the topic
- Direct Publish (for mobile apps SDK)
    - Create a platform application
    - Create a platform endpoint
    - Publish to the platform endpoint
    - Works with Google GCM, Apple APNS, Amazon ADM…

### SNS Security

- Encryption:
    - In-flight encryption using HTTPS API
    - At-rest encryption using KMS keys
    - Client-side encryption if the client wants to perform encryption/decryption itself
- Access Controls: IAM policies to regulate access to the SNS API
- SNS Access Policies (similar to S3 bucket policies)
    - Useful for cross-account access to SNS topics
    - Useful for allowing other services ( S3…) to write to an SNS topic

### SNS + SQS: Fan Out

![](assets/Pasted%20image%2020251112222045.png)

- Push once in SNS, receive in all SQS queues that are subscribers
- Fully decoupled, no data loss
- SQS allows for : data persistence, delayed processing and retries of work
- Ability to add more SQS subscribers over time
- Cross-Region Delivery works with SQS Queues in other regions

### Application: S3 Events to multiple queues

![](assets/Pasted%20image%2020251112222237.png)

- For the same combination of: event type (e.g. object create) and prefix (e.g. images/) you can only have one S3 Event rule
- If you want to send the same S3 event to many SQS queues, use fan-out

### Application: SNS to Amazon S3 thru Kinesis Data Firehose

![](assets/Pasted%20image%2020251112222316.png)

- SNS can send to Kinesis and therefore we can have the following solutions architecture:

### Amazon SNS - FIFO Topic

- FIFO ~ First In First Out (ordering of messages in the topic)

![](assets/Pasted%20image%2020251112222429.png)

- Similar features as SQS FIFO:
    - Ordering by Message Group ID (all messages in the same group are ordered)
    - Deduplication using a Deduplication ID or Content Based Deduplication
- Can have SQS Standard and FIFO queues as subscribers
- Limited throughput (same throughput as SQS FIFO)

### SNS FIFO + SQS FIFO: Fan Out

- In case you need fan out + ordering + deduplication

![](assets/Pasted%20image%2020251112222518.png)

### SNS - Message Filtering

- JSON policy used to filter messages sent to SNS topic’s subscriptions
- If a subscription doesn’t have a filter policy, it receives every message

![](assets/Pasted%20image%2020251112222606.png)

## Step Functions

- Use to design workflows
- Easy visualizations
- Advanced Error Handling and Retry mechanism outside the code
- Audit of the history of workflows
- Ability to “Wait” for an arbitrary amount of time
- Max execution time of a State Machine is 1 year

### Example : Tune a Machine Learning Model

![](assets/Pasted%20image%2020251112222712.png)

### AWS Step Functions

- Your workflow is called a state machine
- Each step in a workflow is a state
- Types of states
    - Task: Does something with Lambda, other AWS services, or third party API’s
    - Choice: Adds conditional logic via Choice Rules (ie, comparisons)
    - Wait: Delays state machine for a specified time
    - Parallel: Add separate branches of execution
    - Map: Run a set of steps for each item in a dataset, in parallel
    - This is most relevant to data engineering! Works with JSON, S3 objects, CSV files
    - Also Pass, Succeed, Fail

## Amazon AppFlow

- Fully managed integration service that enables you to securely transfer data between Software-as-a-Service (SaaS) applications and AWS
- Sources: Salesforce, SAP, Zendesk, Slack, and ServiceNow
- Destinations: AWS services like Amazon S3, Amazon Redshift or non-AWS such as SnowFlake and Salesforce
- Frequency: on a schedule, in response to events, or on demand
- Data transformation capabilities like filtering and validation
- Encrypted over the public internet or privately over AWS PrivateLink
- Don’t spend time writing the integrations and leverage APIs immediately

![](assets/Pasted%20image%2020251112224844.png)
## Amazon EventBridge

- Schedule : Cron job (scheduled scripts)
- Event Pattern : Event rules to react to a service doing something
- Trigger Lambda Functions, send SQS/SNS messages

![](assets/Pasted%20image%2020251112224916.png)

### Amazon EventBridge

![](assets/Pasted%20image%2020251112225048.png)

- Event buses can be accessed by other AWS accounts using Resource-based Policies
- You can archive events (all/filter) sent to an event bus (indefinitely or set period)
- Ability to replay archived events

### EventBridge - Schema Registry

- EventBridge can analyze the events in your bus and infer the schema
- The Schema Registry allows you to generate code for your application, that will know in advance how data is structured in the event bus
- Schema can be versioned

### EventBridge - Resource Based Policy

- Manage permissions for a specific Event Bus
- Example: allow/deny events from another AWS account or AWS region
- Use case: aggregate all events from your AWS Organization in a single AWS account or AWS region

![](assets/Pasted%20image%2020251112225212.png)

## Amazon Managed Workflows for Apache Airflow

- Apache Airflow is batch-oriented workflow tool
- Develop, schedule, and monitor your workflows
- Workflows are defined as Python code that creates a Directed Acyclic Graph (DAG)
- Amazon MWAA provides a managed service for Apache Airflow so you don’t have to deal with installing or maintaining it
- Use cases:
    - Complex workflows
    - ETL coordination
    - Preparing ML data 

![](assets/Pasted%20image%2020251112225435.png)

### Airflow + MWAA

- Your DAGs (Python code) are uploaded into S3
- May also zip it together with required plugins and requirements
- Amazon MWAA picks it up, and orchestrates and schedules the pipelines defined by each DAG.
- Runs within a VPC
    - In at least 2 AZ’s
- Private or public endpoints
    - IAM-managed
    - (Access to Airflow Web Server)
- Automatic scaling
- Airflow Workers autoscale up to the limits you define

### Amazon MWAA Integration

- Leverages open-source integrations
    - Athena, Batch, CloudWatch, DynamoDB, DataSync
    - EMR, Fargate, EKS, Kinesis, Glue, Lambda
    - Redshift, SQS, SNS, SageMaker, S3… and more
    - Security services (AWS Secrets Manager, etc)
- Schedulers and Workers are AWS Fargate containers
### Amazon MWAA Architecture

![](assets/Pasted%20image%2020251112225249.png)

## Full Data Engineering Pipeline

### Real-Time Layer

![](assets/Pasted%20image%2020251112222855.png)

### Video Layer

![](assets/Pasted%20image%2020251112222916.png)

### Batch Layer

![](assets/Pasted%20image%2020251112222935.png)

###  Analytics Layer

![](assets/Pasted%20image%2020251112222956.png)
