# Management and Governance

## Amazon CloudWatch

### CloudWatch Metrics

- CloudWatch provides metrics for *every* service in AWS
- Metric is a variable to monitor (CPUUtilization, NetworkIN, ...)
- Metrics belong to *namespaces*
- *Dimension* is an attribute of a metric(instance id, environment, etc...)
- Up to 30 dimensions per metric
- Metric can have *timestamps*
- Can create CloudWatch dashboards of metrics
- Can create CloudWatch Custom Metrics (for RAM for example)
- Metrics can be streamed with *near-real-time delivery* & low-latency via Data Firehose to multiple Sinks like S3, Redshift, OpenSearch, Athena (from S3)

### CloudWatch Logs

- *Log Groups*: arbitrary name, usually representing an application
- *Log Stream*: instances within application/log files/containers
- can define log expiration policies (never expire, 1 day to 10 years)
- CloudWatch Logs can be sent : S3, Kinesis Stream, Kinesis Firehose, AWS Lambda, OpenSearch, etc.
- Logs are encrypted by default
- Can setup KMS-Based Encryption with your own keys

### CloudWatch Logs Sources

- SDK, CloudWatch Logs Agent, CloudWatch Unified Agent
- Elastic Beanstalk: collection of logs from application
- ECS: collection from containers
- AWS Lambda: collection from function logs
- VPC Flow Logs: VPC specific logs
- API Gateway
- CloudTrail based on filter
- Route53: Log DNS queries
### CloudWatch Logs Insights

![](assets/Pasted%20image%2020251113100214.png)

- Search and analyze log data stored in CloudWatch Logs
- Example: find a specific IP inside a log, count occurrences of “ERROR” in your logs…
- Provides a purpose-built query language
- Automatically discovers fields from AWS services and JSON log events
- Fetch desired event fields, filter based on conditions, calculate aggregate statistics, sort events, limit number of events…
- Can save queries and add them to CloudWatch Dashboards
- Can query multiple Log Groups in different AWS accounts
- It’s a query engine, not a real-time engine

### CloudWatch Logs - S3 Export

- Log data can take up to 12 hours to become available for export
- The API call is CreateExportTask
- Not near-real time or real-time… use Logs Subscriptions instead

### CloudWatch Logs Subscriptions

- Get a real-time log events from CloudWatch Logs for processing and analysis
- Send to Kinesis Data Streams, Kinesis Data Firehose, or Lambda
- Subscription Filter – filter which logs are events delivered to your destination
- Cross-Account Subscription – send log events to resources in a different AWS account (KDS, KDF)

![](assets/Pasted%20image%2020251113104011.png)
### CloudWatch Logs Agent & Unified Agent

- For virtual servers (EC2 instances, on-premises servers…)
- **CloudWatch Logs Agent**
    - Old version of the agent
    - Can only send to CloudWatch Logs
- **CloudWatch Unified Agent**
    - Collect additional system-level metrics such as RAM, processes, etc…
    - Collect logs to send to CloudWatch Logs
    - Centralized configuration using SSM Parameter Store
### CloudWatch Alarms

- Alarms are used to trigger notifications for any metric
- Various options (sampling, %, max, min, etc…)
- Alarm States:
    - OK
    - INSUFFICIENT_DATA
    - ALARM
- Period:
    - Length of time in seconds to evaluate the metric
    - High resolution custom metrics: 10 sec, 30 sec or multiples of 60 sec

### CloudWatch Alarm Targets

- Stop, Terminate, Reboot, or Recover an EC2 Instance
- Trigger Auto Scaling Action
- Send notification to SNS (from which you can do pretty much anything)

### CloudWatch Alarms - composite Alarms

- CloudWatch Alarms are on a single metric
- Composite Alarms are monitoring the states of multiple other alarms
- AND and OR conditions
- Helpful to reduce “alarm noise” by creating complex composite alarms
![](assets/Pasted%20image%2020251113104152.png)

### EC2 Instance Recovery

![](assets/Pasted%20image%2020251113104240.png)

- Status Check:
    - Instance status = check the EC2 VM
    - System status = check the underlying hardware
    - Attached EBS status = check attached EBS volumes
- Recovery: Same Private, Public, Elastic IP, metadata, placement group

### CloudWatch Alarms Good to Know

![](assets/Pasted%20image%2020251113104341.png)

- Alarms can be created based on CloudWatch Logs Metrics Filters
- To test alarms and notifications, set the alarm state to Alarm using CLI

```bash
aws cloudwatch set-alarm-state --alarm-name "myalarm" --state-
value ALARM --state-reason "testing purposes"
```

## Amazon CloudTrail

- Provides governance, compliance and audit for your AWS Account
- CloudTrail is enabled by default!
- Get an history of events / API calls made within your AWS Account by:
    - Console
    - SDK
    - CLI
    - AWS Services
- Can put logs from CloudTrail into CloudWatch Logs or S3
- A trail can be applied to All Regions (default) or a single Region.
- If a resource is deleted in AWS, investigate CloudTrail first!

![](assets/Pasted%20image%2020251113100425.png)

### CloudTrail Events

- Management Events ~ ops performed on resources in AWS Account
- Data Event ~
    - By default data events are not logged
    - Amazon S3 object level activity like get, delete, put or maybe lambda execution
- CloudTrail Insights Events
    - detect unusual activity automatically like : inaccurate resource provisioning, burst of AWS IAM actions, service limits, etc
    - It creates a baseline by observing events at normal times and the continuously analyses write events to unusual patterns

![](assets/Pasted%20image%2020251113101110.png)

- Events are stored for 90 days in CloudTrail
- To keep events beyond this period, log them to S3 and use Athena

![](assets/Pasted%20image%2020251113101149.png)

### AWS CloudTrail Lake

- Managed data lake for CloudTrail events
- Integrates collection, storage, preparation, and optimization for analysis & query
- Events are converted to ORC format
- Enables querying CloudTrail data with SQL
- Enable it with the “Create event data store” menu choice in the console
- Data is retained for up to 7 years
- Specify the event types you want to track
- Note KMS events add up fast and can make your costs blow up
- Basic event selectors can be selected in the UI
- Finer grained selection may be achieved with advanced event selectors
    - This can help control your ingestion and storage costs
- You can create “channels” to integrate with events outside of AWS
    - Built-in support for Okta, LaunchDarkly, Clumio, and other CloudTrail partners
    - Or custom integrations

### Querying CloudTrail Lake

![](assets/Pasted%20image%2020251113101406.png)

- Lake dashboards allow you to visualize events
- Roll your own SQL queries
- Start from sample queries in the CloudTrail Lake Editor
- Remember to bound your queries by eventTime to constrain costs
## AWS Config

- Helps with auditing and recording compliance of your AWS resources
- Helps record configurations and changes over time
- Questions that can be solved by AWS Config:
    - Is there unrestricted SSH access to my security groups?
    - Do my buckets have any public access?
    - How has my ALB configuration changed over time?
- You can receive alerts (SNS notifications) for any changes
- AWS Config is a per-region service
- Can be aggregated across regions and accounts
- Possibility of storing the configuration data into S3 (analyzed by Athena)

### Config Rules

- Can use AWS managed config rules (over 75)
- Can make custom config rules (must be defined in AWS Lambda)
    - Ex: evaluate if each EBS disk is of type gp2
    - Ex: evaluate if each EC2 instance is t2.micro
- Rules can be evaluated / triggered:
    - For each config change
    - And / or: at regular time intervals
    - AWS Config Rules does not prevent actions from happening (no deny)
- Pricing: no free tier, $0.003 per configuration item recorded per region, $0.001 per config rule evaluation per region

### AWS Config Resource

- View compliance of a resource over time
- View configuration of a resource over time
- View CloudTrail API calls of a resource over time

### Config Rules - Remediations

- Automate remediation of non-compliant resources using SSM Automation Documents
- Use AWS-Managed Automation Documents or create custom Automation Documents
    - Tip: you can create custom Automation Documents that invokes Lambda function
- You can set Remediation Retries if the resource is still non-compliant after auto-remediation

![](assets/Pasted%20image%2020251113102014.png)

### Config Rules - Notifications

- Use EventBridge to trigger notifications when AWS resources are non-compliant

![](assets/Pasted%20image%2020251113101910.png)

- Ability to send configuration changes and compliance state notifications to SNS (all events – use SNS Filtering or filter at client-side)

![](assets/Pasted%20image%2020251113101935.png)

### CloudWatch vs CloudTrail vs Config

- CloudWatch
    - Performance monitoring (metrics, CPU, network, etc…) & dashboards
    - Events & Alerting
    - Log Aggregation & Analysis
- CloudTrail
    - Record API calls made within your Account by everyone
    - Can define trails for specific resources
    - Global Service
- Config
    - Record configuration changes
    - Evaluate resources against compliance rules
    - Get timeline of changes and compliance

### For an Elastic Load Balancer

- CloudWatch:
    - Monitoring Incoming connections metric
    - Visualize error codes as % over time
    - Make a dashboard to get an idea of your load balancer performance
- Config:
    - Track security group rules for the Load Balancer
    - Track configuration changes for the Load Balancer
    - Ensure an SSL certificate is always assigned to the Load Balancer (compliance)
- CloudTrail:
    - Track who made any changes to the Load Balancer with API calls

## AWS CloudFormation

- CloudFormation is a declarative way of outlining your AWS Infrastructure, for any resources (most of them are supported).
- For example, within a CloudFormation template, you say:
    - I want a security group
    - I want two EC2 instances using this security group
    - I want an S3 bucket
    - I want a load balancer (ELB) in front of these machines
- Then CloudFormation creates those for you, in the right order, with the exact configuration that you specify

### Benefits of AWS CloudFormation

- Infrastructure as code
    - No resources are manually created, which is excellent for control
    - Changes to the infrastructure are reviewed through code
- Cost
    - Each resources within the stack is tagged with an identifier so you can easily see how much a stack costs you
    - You can estimate the costs of your resources using the CloudFormation template
    - Savings strategy: In Dev, you could automation deletion of templates at 5 PM and recreated at 8 AM, safely
- Productivity
    - Ability to destroy and re-create an infrastructure on the cloud on the fly
    - Automated generation of Diagram for your templates!
    - Declarative programming (no need to figure out ordering and orchestration)
- Don’t re-invent the wheel
    - Leverage existing templates on the web!
    - Leverage the documentation
- Supports (almost) all AWS resources:
    - Everything we’ll see in this course is supported
    - You can use “custom resources” for resources that are not supported

### CloudFormation + Infrastructure Composer

- Example: WordPress CloudFormation Stack
- We can see all the resources
- We can see the relations between the components

![](assets/Pasted%20image%2020251113102349.png)

## SSM Parameter

![](assets/Pasted%20image%2020251113102443.png)

- Secure storage for configuration and secrets
- Optional Seamless Encryption using KMS
- Serverless, scalable, durable, easy SDK
- Version tracking of configurations / secrets
- Security through IAM
- Notifications with Amazon EventBridge
- Integration with CloudFormation
- SSM Parameter Store Hierarchy
    - `/my-dept/`
        - `my-app/`
            - `dev/`
                - `db-url`
                - `db-password`

### Parameter Tiers

![](assets/Pasted%20image%2020251113102826.png)
### Parameter Policies (for advanced parameters)

- Allow to assign a TTL to a parameter (expiration date) to force updating or deleting sensitive data such as passwords
- Can assign multiple policies at a time

![](assets/Pasted%20image%2020251113102751.png)
### Well Architected Framework 6 Pillar

- Operational Excellence
- Security
- Reliability
- Performance Efficiency
- Cost Optimization
- Sustainability
- They are not something to balance, or trade-offs, they’re a synergy
## Amazon Managed Grafana

![](assets/Pasted%20image%2020251113103205.png)

- Grafana is a popular open-source platform used to monitor, visualize, and alert on metrics and logs.
- Integrated with IAM Identity Center (formerly AWS SSO) and/or SAML for user management and permissions
- Compatible with Grafana plugins and alerts
- Fully managed, scales automatically
- Encrypted at rest and in transit, can use KMS
- Integrated with many AWS data sources
    - CloudWatch, OpenSearch, Timestream, Athena, Redshift, X-Ray
    - Amazon Managed Service for Prometheus (AMP)
- Also with everything else Grafana integrates with
    - GitHub, Google, Azure, MySQL, Redis, JSON, OpenTelemetry, much more.

![](assets/Pasted%20image%2020251113103218.png)

## Amazon DataZone

- Data management service
    - Facilitates cataloging, discovering, sharing, and governing data
- Supports
    - AWS
    - On-Premises data
    - Third-party data
- Users
    - Engineers
    - Data scientists
    - Product managers
    - Analysts, business users
- Easy and secure access to data with governance and transparency
- Becoming subsumed into SageMaker Unified Studio

### Amazon DataZone Uses

- Catalog and discover data
- Automated metadata management
- Govern data access
- Fine-grained access controls
- Governance workflows
- Collaborate across teams
- Projects, shared analytics tools
- Automate workflows
- Share data between producers and consumers

### Key Components

- Domains
    - Organizational entities to group users, data, and projects
- Data portal
    - Web application, outside of AWS console
    - Catalog, discover, govern, share, analyze data
    - IAM authentication
- Business Data Catalog
    - Define taxonomy / glossary
- Data projects
    - Groups people, data sets, analytics tools
- Data environments
    - Provides infrastructure within projects (storage, analytics tools)
- Governance and access control
    - Built-in workflows for requesting data access and approving it
    - Manages permissions via Lake Formation, Redshift

![](assets/Pasted%20image%2020251113103652.png)

![](assets/Pasted%20image%2020251113103708.png)

