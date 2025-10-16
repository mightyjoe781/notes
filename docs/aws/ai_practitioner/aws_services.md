# AWS Services

## IAM: Users & Groups

- IAM ~ Identity and Access Management, Global Service
- Root account created by default should not be used or shared
- Users are people within our organization, and can be groups. i.e Group: developers, Group: Operations, Group: admin
- Groups only contain users, not other groups
- Users don't have to belong to a group, and user can belong to multiple groups

### IAM: Permission

- Users or Groups can be assigned JSON documents called policies.
- These policies define the permission of the users
- In AWS you apply the least privilege principle: Don't give more permissions than a user needs

![](assets/Pasted%20image%2020251012165153.png)

### IAM Policies Structure

- Consists of
    - version: policy language version, always include `2012-1017`
    - `Id` : an identifier for the policy (optional)
    - *Statement* : one or more individual statements (required)
- Statements consist of
    - Sid : an identifier for the statement
    - *Effect* : whether the statement allows or denies access
    - Principal: account/user/role to which this policy is applied to
    - *Action*: list of actions this policy allows or denies
    - *Resource* : list of resources to which the actions applied to.
    - *Condition* : conditions for when this policy is in effect (optional)

![](assets/Pasted%20image%2020251012180232.png)

### IAM Roles for Service

- Some AWS service will need to perform actions on your behalf
- To do so, we will assign permissions to AWS services with IAM Roles
- Common roles
    - EC2 instance roles
    - Lambda function roles
    - Roles for CloudFormation
    - EKS roles

NOTE: IAM policy evaluation order

$$
\text{Final decision} = 
\begin{cases}
\text{Deny} & \text{if any policy explicitly denies} \\
\text{Allow} & \text{if allowed by policies and no deny} \\
\text{Deny} & \text{by default if no explicit allow}
\end{cases}
$$

## S3

- Amazon S3 is one of the main building blocks of AWS
- advertised as *infinitely scaling* storage
- Many websites use Amazon S3 as a backbone, Many services use Amazon S3 as an integration as well
- Use Cases
    - Backup and Storage
    - Disaster Recovery
    - Archive
    - Hybrid Cloud Storage
    - Application hosting
    - Media Hosting
    - Data lakes & Big Data Analytics
    - Static Websites

### S3: Buckets

- Amazon S3 allows people to store objects (files) in *buckets*
- Buckets must have a globally unique name (across all regions and all accounts)
- Buckets are defined at a region level
- S3 looks like a global service but buckets are created in a region
- Naming Convention
    - No uppercase, No underscore
    - 3-63 characters long
    - Not an IP
    - Must start with lowercase letter or number
    - Must NOT start with prefix `xn--`
    - Must NOT end with suffix `-s3alias`

### S3: Objects

- Objects (files) have a Key
- The *key* is the FULL path
    - `s3://my-bucket/my_file.txt`
    - `s3://my-bucket/my_folder/another_folder/my_file.txt`
- They key is consisting of *prefix* + *object name*
- There is no concepts of *directories* within buckets:  just keys with long names containing slashes (`/`)
- Object values are the content of the body.
    - Max Object size is 5TB
    - If uploading more than 5GB, must use *multi-part upload*
- Metadata (list of text key/values pairs - system or user metadata)
- Tags (unicode key/value pair - up to 10) - useful for security and lifecycle
- version ID (if versioning is enabled)

### S3 Storage Classes

- Amazon S3 Standard - General Purpose
- Amazon S3 Standard - Infrequent Access (IA)
- Amazon S3 One Zone-Infrequent Access
- Amazon S3 Glacier Instant Retrieval
- Amazon S3 Glacier Flexible Retrieval
- Amazon S3 Glacier Deep Archive
- Amazon S3 Intelligent Tiering

We can move between classes manually or using S3 lifecycle configurations.

### S3: Durability & Availability

- Durability
    - High durability (99.999999999 %) ~ 11 9's of objects across multiple AZs
    - If you store 10,000,000 objects in Amazon S3, you can expect incur a loss of a single objects once every 10,000 years
- Availability
    - Measures how readily available a service is
    - Varies depending on storage classes
    - Example: S3 standard has 99.99% availability = not available 53 minutes a year.

## Amazon EC2

- EC2 is one of the most popular of AWS's offering
- EC2 = Elastic Compute Cloud = Infrastructure as a Service
- It mainly consists in the capability of
    - Renting virtual Machines (EC2)
    - Storing data on virtual drives (EBS)
    - Distributing load across machines (ELB)
    - Scaling the service using Auto Scaling Groups (ASG)
- Knowing Ec2 is fundamental to understand how the Cloud works

### EC2 Sizing and configuration options

- OS
- Compute & Cores (CPU)
- RAM
- How much storage space
    - Network attached (EBS & EFS)
    - hardware (EC2 Instance Store)
- Network Card : speed, public IP address
- Firewall rules: security group
- Bootstrap Scripts: EC2 User Data

## AWS Lambda

- EC2
    - Virtual servers in cloud
    - Limited by RAM and CPU
    - Continuously Running
    - Scaling means intervention to add/remove servers
- Lambda
    - Virtual Servers - no servers to manage!
    - Limited by time - short execution (15min)
    - Run on-demand
    - Scaling is automated

### Benefits of AWS Lambda

- Easy Pricing
    - Pay per request and compute time
    - Free tier of 1,000,000 AWS Lambda requests and 400,000 GBs of compute time
    - Integrates with the whole AWS suite of services
    - Event-Driven: functions get invoked by AWS when needed
    - Integrated with many programming languages
    - Easy monitoring through Cloudwatch
    - Easy to get more resources per function (up to 10GB RAM)
    - Increasing RAM will also improve CPU and network

### Lambda Language Support

- Node.js
- Python
- Java
- C# (.NET Core)
- Ruby
- Custom Runtime API (community supported, example Rust or Golang)
- Lambda Container Images
    - The container image must implement the Lambda Runtime API
    - ECS/Fargate is preferred for running arbitrary Docker Images

### Use-Cases

- Serverless Thumbnail creation
- Serverless CRON Job

Lambda Pricing : https://aws.amazon.com/lambda/pricing/


## AWS Macie

- Amazon Macie is a fully managed data security and data piracy service that uses machine learning and pattern matching to discover and protect sensitive data in AWS
- Macie helps identify and alert you to sensitive data, such as PII Data.

## AWS Config

- Helps with auditing and recording compliance of your AWS resources 
- Helps records configurations and changes over time
- Possibility of storing the configuration data into S3
- Question that can be solved by AWS Config
    - Is there unrestricted SSH access to my security groups
    - Do my buckets have any public access
    - How has my ALB configuration changed over time

## Amazon Inspector

- Automated Security Assessments
- For EC2 instances
    - Leveraging the AWS system Manager (ASM) agent
    - Analyze against unintended network accessibility
    - Analyze the running OS against known vulnerabilities
- For Container Images push to Amazon ECR
    - Assessment of Container Images as they are pushed
- For Lambda Functions
    - Identifies software vulnerabilities in function code and package dependencies
    - Assessment of functions as they are deployed
- Report & integration with AWS Security Hub
- Send findings to Amazon Even Bridge

## AWS CloudTrail

- Provides governance, compliance and audit for your AWS Account
- CloudTrail is enabled by default!
- Get an history of events / API calls made within your AWS Account by:
    - Console
    - SDK
    - CLI
    - AWS Services
- Can put logs from CloudTrail into CloudWatch Logs or S3
- A trail can be applied to All Regions (default) or a single   Region.
- If a resource is deleted in AWS, investigate Cloud Trail first!

![](assets/Pasted%20image%2020251012210225.png)

## AWS Artifact (not really a service)

- Portal that provides customers with on-demand access to AWS compliance documentation and AWS agreements
- *Artifact Reports* - Allows you to download AWS security and compliance documents from third-party auditors, like AWS ISO certifications, Payment Card Industry (PCI), and System and Organization Control (SOC) reports
- *Artifact Agreements* - Allows you to review, accept, and track the status of
- AWS agreements such as the Business Associate Addendum (BAA) or the Health Insurance Portability and Accountability Act (HIPAA) for an individual account or in your organization
- Can be used to support internal audit or compliance
- On-demand access to security compliance reports of Independent Software Vendors (ISVs)
- ISV compliance reports will only be accessible to the AWS customers who have been granted access to AWS Marketplace Vendor Insights for a specific ISV
- Ability to receive notifications when new reports are available
## AWS Audit Manager

- Assess risk and compliance of your AWS workloads
- Continuously audit AWS services usage and prepare audits
- Prebuilt frameworks include:
    - CIS AWS Foundations Benchmark 1.2.0 & 1.3.0
    - General Data Protection Regulation (GDPR),
    - Health Insurance Portability and Accountability Act (HIPAA)
    - Payment Card Industry Data Security Standard (PCI DSS) v3.2.1
    - Service Organization Control 2 (SOC 2)
- Generates reports of compliance alongside evidence folders

## Trusted Advisor

- No need to install anything – high level AWS account assessment
- Analyze your AWS accounts and provides recommendation on 6 categories:
    - Cost optimization
    - Performance
    - Security
    - Fault tolerance
    - Service limits
    - Operational Excellence
- Business & Enterprise Support plan
    - Full Set of Checks
    - Programmatic Access using AWS Support AP


## Networking Primer

- VPC - Virtual Private Cloud: private network to deploy your resources (regional resource)
- Subnets allow you to partition your network inside your VPC (Availability Zone resource)
- A public subnet is a subnet that is accessible from the internet
- A private subnet is a subnet that is not accessible from the internet 

![](assets/Pasted%20image%2020251012210957.png)

### VPC Diagram

![](assets/Pasted%20image%2020251012211030.png)

- Internet Gateways helps our VPC instances connect with the internet
- Public Subnets have a route to the internet gateway
- NAT Gateways (AWS-managed) allow your instances in your Private Subnets to access internet while remaining private.

![](assets/Pasted%20image%2020251012211206.png)

### AWS Endpoints and Private Link

- AWS services are by default accessed over the public internet
- Application deployed in Private subnets in VPC may not have internet access.
- We want to use VPC Endpoints
    - Access an AWS service privately without going over the public internet
    - Usually powered by AWS PrivateLink
    - Keep your network traffic internal to AWS
    - Example you application deployed in a VPC can access a Bedrock model Privately
- S3 Gateway Endpoint
    - Access the S3 privately
    - There is an S3 interface endpoint
    - Example: Sagemaker notebooks can access the S3 data privately.

## Examples

### Bedrock must access an encrypted S3 Bucket

![](assets/Pasted%20image%2020251012211653.png)

- Bedrock much have an IAM role that gives it access to
    - Amazon S3
    - The KMS key with the decrypt permission

### Deploy SageMaker Model in your VPC

![](assets/Pasted%20image%2020251012211719.png)

### Analyze Bedrock access with CloudTrail

![](assets/Pasted%20image%2020251012211746.png)