# Aws Notes - Part 1
Generated on: 2025-06-01 14:11:13
Topic: aws
This is part 1 of 1 parts

---

## File: aws/cloud/fundamentals/ch1.md

## Understanding Cloud Computing

### Traditional Data Centers

 Traditional Data Centers requires : 

- Large up-front investment
- forecasting demand is difficult
- slow to deploy new data centers and servers
- maintaining data centers is expensive
- you own all of the security and compliance burden

### Benefits of Cloud Computing

- Trade capital expense for variable expenses
- benefits from massive economies of scale
- stop guessing capacity
- increase speed and agility
- stop spending money maintaining data centers
- go global in minutes

**Elasticity** is the ability to acquire resources as you need them and release resources when you no longer need them. In the cloud, you want to do this automatically.

**Reliability**

**Agility** : The cloud lowers the cost of trying new ideas of business processes.

### Fundamentals of Cloud Computing

**Cloud Computing** is the on-demand delivery of compute power, database, storage, application, and other IT resources through cloud services resources through cloud services platform via the Internet with pay-as-you-go pricing.

Cloud Computing Models

- IaaS (Infrastructure as a Service): Max Control, Max Maintenance
- PaaS (Platform as a Service): Beanstalk
- SaaS(Software as a Service): Min Maintenance, Min Control

Cloud Deployment Models

- Public Cloud : Deployed onto a public cloud provider like AWS
- On-Premises (Private Cloud) : Cloud-like platform in a private data center.
- Hybrid (Cloud applications connected to a private data center)

---

## File: aws/cloud/index.md

### Cloud Practioner



- [Fundamentals](./fundamentals/ch1.md)

---

## File: aws/database/ch0.md

## Introduction

Exam Structure

- Code : DBS-CA01

- 750+ marks are required to pass the exam out of 1000.

Topics

- Domain 1 : **Workload Specific Database Design** : 26%
  - Overview of AWS Database Service
  - Differences between relational and non-relational DBs
  - High availibility of your database services
  - Cost optimization techniques
  - Database Performance Options
- Domain 2 : **Deployment and Migration** : 20%
  - Using CloudFormation to deploy databases
  - Understanding Database Migration
  - Using AWS Secrets Manager with CloudFormation
- Domain 3 : **Management and Operations** : 18%
  - Understanding DB Maintenance windows, DB Clusters, Parameter Groups and Option Groups
  - Managing an effective backup and restore strategy to recover from unexpected incidents
  - Maintaining Automatic and Manual Backups using different databases services
- Domain 4 : **Monitoring and Troubleshooting** : 18%
  - Managing Root Cause Analysis
  - Common Troubleshooting Techniques
  - AWS Logging Mechanism and Capabilities
  - Using AWS CloudWatch and CloudTrail as effective monitoring and troubleshooting tools
  - Amazon DynamoDB Accelerator (DAX)
  - Enhancing Database Performance
- Domain 5 : **Database Security** : 18%
  - Managing Encryption with AWS KMS
  - Alternate Encryption Options
  - How to manage access control to AWS databases
  - Implementing Effective IAM permissions to adopt the principle of least privilege
  - Security best practices surrounding AWS Databases



---

## File: aws/database/ch1.md

## AWS Global Infrastructure



The components of AWS Global Infra are:

- Availability Zones (AZs)
- Regions
- Edge Locations
- Regional Edge Caches
- Local Zones
- Wavelength Zones
- Outposts

**Availability Zones (AZs)**

- Physical data-centers of AWS
- Multiple Physical data-centers close enough together form one Availability Zone
- Each AZ will have at least nearby sister AZ(probably in nearby city) which is connected via very low latency private fibre optic (used by many AWS Services to replicate data : Read up synchronous and asynchronous replication)
  - Note Both AZ will be separate power resources and network connectivity
  - This is all because of resilience and availability purpose.
- Making use of 2 AZs in one Region ensures your infra remains stable, available, and resilient even in worse times

**Region**

- Collection of AZs that are located geographically close to each other
- Every Region works independently of others and will have atleast 2 AZs
- Having global regions allows organisation to comply with local laws to store data
- Use mulitple region if you are a global organisation and downtime may cost money
- Currently there 32 Regions and 102 AZs. (Note : this number may have changed)
- Note : not all services are available in every region. IAM and CloudFront are global Services
- AWS GovCloud is a region only available to approved US Companies
- Naming convention of region : region-direction-number

![image-20230219124734176](ch1.assets/image-20230219124734176.png)

NOTE : AWS maps these AZ letters to different AZs for different AWS Accounts for ensuring even distribution of resources across all AZs within a Region.

**Edge Locations :**

- AWS Sites deployed in Major Cities and highly populated areas across the globe.
- Outnumber AZs
- Utilised for services such as CloudFront and Lambda to cache data and reduce latency for end-users by using Edge Locations as CDN.

**Regional Edge Cache**

- These Edge Location sit between your CloudFront Origin servers and the Edge Locations.
- Large Cache-width than each of individual Edge Locations
- Data is retained at Regional Edge Cache while it expires at Edge Locations

**Local Zones**

- 2022 : Amazon launches first 16 Local Zones
- Local Zone : a new type of infrastructure deployment designed to place core AWS Compute, Storage, Networking & Database services near highly populated areas.
- All Local Zones will be connected to a parent Region, allowing seamless connection between other AWS Services.
- Available in 33 metropolitan areas (19 more planned)

**Wavelength Zones**

- Similar to Local Zones but differs how it connects to its parent Region i.e. 5G mobile broadband networks and re deployed within the data centers of large telecommunication providers.
- AWS Wavelength Zones are available through Verizon in US, KDDI in Japan, SK Telecom in South Korea, Vodafone in UK/Germany & Bell in Canada

**Outposts**

- brings capabilites of AWS Cloud to your on-premises data center, includes same hardware used by AWS in their data centres
- allows users to use native AWS services, including the same tools and APIs you would use when running your infra within AWS.
- available as 1U or 2U rack-mountable servers, or as 42U racks that can be scaled to 96 racks
- provides PrivateLink Gateway endpoints to securely and privately connect to other services and resources such as DynamoDB
- aws will patch and update those servers


---

## File: aws/database/ch2.md

## Differences Between AWS Database Types

### The AWS Database Landscape

In AWS three primary types of services used by Consumers : Compute, Storage, Database

There are two types of databases

- Relation (SQL)
  - optimized around data storage
  - based on Structured Query Language for data retrieval
- Non-Relational
  - process unstructured and semi-structured data quickly
  - often distributed on multiple nodes

There are nine primary categories of Databases available in AWS

1. Relational 
2. Key-Value
3. Document
4. In-Memory
5. Graph
6. Columnar
7. Time-Series
8. Quantum Ledger
9. Search

- Size, Shape and Computational Requirements of data gives idea to developers which kind of database is best for them.

- Cloud promises agility, ability to use and select appropriate database or multiple of them according to workload, rather than using one general purpose database.
- *Scalability* and *Elasticity* is another benefit from cloud

Types of Workloads

- Operational
  - Online Transactional Processing (OLTP) : OLTP is centered around a set of common business processes that are : *Regular, Repeatable* and *Durable*.
  - Examples includes : E-commerce, IT, CMS, etc.

- Analytical
  - Online Analytics Processing (OLAP) : Run for Business Intelligence Workloads or Data Analytics
  - Workloads are often : Retrospective(Company’s Quarter Analysis), Streaming(Real Time Processing) and Predictive(ML/AI)

### Relational Databases

**Schema :** structure that needs to defined before entering data into the database and designed based on reporting requirements.

- Relation DBs are highly structured and have been around since 60s.
- Schema changes are expensive in terms of time and compute power, with risk of corrupting data
- Data is stored in tables (Relation)
- Each Row is referred as *Record* and Each Column is referred as *Key*, and the value referenced is called as *Attribute*
- Each Table will have unique primary key that is used for relational purposes for other tables via foreign key.
- Data Integrity(data stored is reliable and accurate) is particular concern in RDBS : ACID transactions
  - Atomicity : A single database transaction (which succeeds or fails completely)
  - Consistency : Transaction must take database from one valid state to another valid state.
  - Isolation : Two transactions don’t interfere with each other
  - Durability : Data changes become permanent once the transaction is committed to database.
- Keys and Data Integrity
  - Primary and Foreign Key are constraints
  - Entity Integrity ensure primary key is unique to table and it has a value (NOT NULL)
  - Referential Integrity ensures that foreign key is primary key to its originating table. Orphaned Data is BAD !
- API of relational database is SQL (Structured Query Language)
- Relation databases have Data Access Controls and features like : Authentication, Authorization and Audit Logging

**Data Normalization: ** Normalisation is a process where information is organised efficiently and consistently before storing it.

- Duplicate data is discarded
- Closely related fields are aggregated

**Scaling and Sharding**

- Relational Databases are not partition tolerant, data partitions are called as shards. Two shards needs to co-ordinate to validate data consistency and it becomes costly. Both shards will same number of Keys (Horizontal Scaling (adds copy of the db))
- Most of the times Relational databases are scaled vertically (growing server by adding memory, cpu and a disk volume).

**AWS Relation Database Engines**(6) : Aurora(native to AWS), MySQL, Postgres, MariaDB, Oracle and Microsoft SQL Server.

---

## File: aws/database/index.md

### Notes





0. [Introduction](ch0.md)
1. [AWS Global Infrastructure](ch1.md)
2. [Differences Between AWS Database Types](ch2.md)

---

## File: aws/developer/ch1.md

## Cloud Academy Developer Associate (DVA-C01)

#### About the Exam

Expected learning from the exam : 

- Understanding of core AWS services, uses and basic AWS architecture best practices (common in other three associate programs)
- Proficiency in developing, deploying and debugging cloud-based application using AWS

- comphrehensive understanding of application life-cycle management

Exam Logistics :

- 65 questions
- 130 minutes to complete (over 2 hrs)
- 2 min/question
- passing score of 720/1000 (scaled score)

Scenario ----> Specific Question about Scenario ----> Set of possible answers

Common Question Theme : Highly Available, Cost effective, the most secure, performance improvement and least amount of downtime. (won’t be asked for best/easiest solution because in that aspect opinion varies person to person)

Focus is on use of services and features rather than **memorisation**.

Question Type : Single correct and Multiple Correct Type Questions

Skipped question = Incorrect questions. There is no penality for guessing.

### Exam Content

1. #### Deployment - 22%

   - Deploy written code in AWS using existing CI/CD pipelines, processes, and patterns
     - AWS Code Commit
     - AWS Code Build
     - AWS Code Deploy
     - AWS Code Pipeline
   - Deploy Application using Elastic Beanstalk
   - Prepare the application deployment package to be deployed to AWS (5 deployment policies)
   - Deploy serverless applications (SAM, API Gateway)

2. #### Security - 26%

   - Make authenticated calls to AWS services
   - Implement encryption using AWS services
   - Implement application authentication, and authorization
   - Services Covered (AWS IAM **(as user management doesn’t scale)**, Amazon Cognito, AWS KMS, AWS Secrets Manager, Identity federation, SAML, Identity providers)

3. #### Development with AWS Services - 30%

   - Write code for serverless application
   - translate function requirements into application design (SQL -> AWS RDS)
   - implement application design into application code
   - write code that interacts with AWS services by using APIs, SDKs and AWS CLI

4. #### Refactoring - 10%

   “Services not servers” : Always stop services that you don’t use to save money !

   - Optimize application to best use AWS services and features
   - Migrate existing application code to run on AWS (Auth application to Amazon Cognito)

5. #### Monitoring and Troubleshooting - 12%

   - Write code that can be monitores
   - Perform root cause analysis on faults found in testing or production
   - Tools/Services like Amazon Cloud Watch, Amazon Cloud Trail, AWS X-ray.



Next : [Compute](ch1.md)



---

## File: aws/developer/ch10.md

## Containers

**The problems of Monolithic Application**

- Unnecessary scaling of unused component

- Containers differ from VMs becuase it is always same under the effect of some config file that creates the image, no matter what Host OS is. Container Enginer (Docker) is responsible for this. While VMs can be quite large in size, and can be platform/host OS dependent.
- Hypervisor can help orchestrate bunch of VMs
- ECS (based on Docker) is container Orchestration Platform

2 Ways to setup

- EC2 with docker engine installed on them and works as Cluster.
- Amazon Fargate : serverless platform, not always on (Sleep)

### Amazon Elastic Container Registry (ECR)

- Fully managed docker container registry, built in Amazon ECS
- helps in hosting images with bunch of nice features
- To run container on EC2, we will need ***Task Definitions***
- *Task Definitions* (Important, asked in my exam lol)
  - Configuring Memory Limits
  - Network Details : ports mapping etc
  - Container Details : names, tagging
- ECS Service : allows to manage, run, maintain a specific number of task definitions within an amazon ECS Cluster.
  - Self Healing Clusters
  - Allows to setup ELB in front of Containers

**When should we use Serverless v/s ECS**

|                 Servered                  |        Serverless        |
| :---------------------------------------: | :----------------------: |
| Workload supports long-running operations |      Cost Effective      |
|     Fully Utilizes the CPU and Memory     |  Lower Development Cost  |
|                                           | Reduced Operational Cost |
|                                           |    Better Scalability    |

Fargate is always using AWS VPC mode network while ECS gives flexibility to use any mode.

Three Networking Modes

- HOST Mode
- AWS VPC Mode
- Bridge Mode

<hr>

### ECS for Kubernetes

- Kubernetes is open-source container orchestration tool designed to automate, deploy, scale and operate containerised application.
- It can grow from tens, thousands or even millions of containers
- Its container runtime agnostic

### EKS (ECS for Kubernetes)

- Managed service allowing you to run Kubernetes across your AWS Infra without having to take care provisioning and running Kubernetes Management Infrastructure in **Control Plane**
- You only need to provision and maintain the **Worker Nodes**

**Control Plane **: # of different APIs. The Kubelet processes **Kubernetes Master**.

- Schedules container onto nodes
- Tracks state of all containers

**Nodes ** : EC2 Instances

#### Working with EKS

1. Create an EKS Service Role
2. Create an EKS Cluster VPC
3. Install kubectl and IAM Authenticator
4. Create your EKS Cluster
5. Configure Kubectl for EKS
6. Configure and provision worker nodes
7. Configure Worker nodes to join EKS Cluster

---

## File: aws/developer/ch11.md

## Security, Identity and Compliance

### AWS IAM

**What is Identity and Access Mangement**

- Identity : more related to “who” you are.
- Access Management : more related to “what” you can do.

**Access Control :** method of accessing secured resources.

**IAM Features**

- provides the component to maintain this management of access, but it is only as strong and secure as ***you configure it***.
- Best Practices
  - Priniciple of Least Priviledge Access
  - Enable Identity Federation (SSO, SAML, etc)
  - Enable MFA (Multi-Factor Authentication)
  - Rotate Credentials Regularly
  - Enable IAM Access Analyser

**Users : ** Identity Object (arn) : Real person or application

**User Groups :** Object : Collection of *IAM Users* and *Associated Policies*. 

- These policies allow **authorised** group members access to certain AWS Resource.
- There is no **authentication** involved in groups.

**Roles :** Allows IAM users/other application and services to adopt a set of temporary IAM permission to access AWS Resources

- Identity with access to associated objects.
- Are not associated to a person, they are supposed to assumed by a user.

**Policies :** 

- AWS Managed Policies : Library of usable policies
- IN-Line Policies : written by consumers. Associates with a user/role.

- These can be applied to User Groups and Roles

**Identity Providers : ** Auth, SSO, SAML, etc.

**Password Policies : ** applies to all users.

**Cross Account Access** : 

![image-20230218172438866](ch11.assets/image-20230218172438866.png)

1. Create a new role within trusting account(prod).
2. Specify permissions attached to this newly created role which users in dev will assume to carry out tasks and actions
3. Switch to Trusted Account (dev) to grant permissions to develop to allow them to use newly created roles in Trusting Account (prod)
4. Test the configs by Swithching Roles.

- Dev Account temporarily gets access to Prod Resources through above process. (For Security and Compliance)

**IAM Policy Types**

- Identity Based : Users, User-Groups, Roles
- Resource Based : Resources (principal to config user identity)
- Permission Boundaries : Roles/Users only
- Organization Service Control Policies (SCPs) : Boundary of Max. Permission

<hr>

### Amazon Cognito

- An authentication and user management service
- has strong integration with 3rd-party providers such as Apple, Facebook, Google and Amazon
- allows federating identity from your own Active Directory Services

**User Pools : ** 

- To create and maintain directory of your users for mobile and web applications

- Deals with both signing up, and signing in, your new & returning users.

- **User Pools Auth Flow**

  ![image-20230218173433741](ch11.assets/image-20230218173433741.png)

**Identity Pools**: 

- Provide Temporary access to AWS crendentials for users or guests
- Can work in tandem with User Pools, allowing users to operate & access whatever specific feature they need from AWS

<hr>

### KMS (Key Management Service)

Types of Encryption

- Symmetric : Same Key decrypts and encrypts data.
  - Not Safe for secure communication
  - Ex : AES, Blowfish, DES, Triple DES, etc.
- Asymmetric : Private/Public Key craeted at same Time. 
  - Ex : RSA, Diffie-Helman, Digital Signature Algorithms, etc.

**KMS : ** managed service, used to craete and store encryption keys that are used by other AWS Services and Applications

- KMS is only for Encryption at Rest. Use **SSL** for data in transit.
- KMS is multi-region service now.

#### CMK (Customer Master Keys)

- Can Encrypt data upto 4KB in size
- Typically used in relation to DEK
- CMK can generate, encrypt, decrypt these DEK

Types :

- Customer Manged CMKs : Greater flexibility
- AWS Managed CMKs : used by AWS Services

**DEK : ** Data Encryption Keys can encrypt your data of any size.

![IMG_EC3B94927CDA-1](ch11.assets/IMG_EC3B94927CDA-1.jpeg)



**Key Policies : ** tied with CMKs, resource bassed policies. Each different CMK will have different policies.

- Key Policies defines who can use and define keys in KMS

**Grants : **

- controlling access and use of the CMKs held within KMS
- allows to delegate a subset of your own access to CMK for principals
- less risk of someone altering the access control permission of CMK

To manage access to your CMK, you must use a key policy associated with your CMK.

Can’t be generated by IAM alone.

- Key Policies : Resource based policy tied to your CMK json
- Key Policies with IAM Role : 

- Key Policies with Grants : resources based policy to delegate your permissions to another AWS principal with your AWS Account.

---

## File: aws/developer/ch12.md

## Application Integration

### Amazon EventBridge

- Problems with monoliths

  - tightly coupled
  - single point of failure
  - scaling certain parts is not possible

- Monolith ------> Microservices

- Each Microservice would have their teams, resources etc. 

- Issues with Microservices

  - Noisy communication between several services might introduce inefficiencies.

  - Sometimes team communication becomes difficult in microservices.

**Event Based Architecture**

- Services are more decoupled
- Services will wait for a flag (event) to be sent from upstream and then action will be taken based on event.

**Amazon EventBridge :** An *event co-ordinator*

- Events are json made of strings and define some activity
- **[IMP]** : version, id, detail_type, src, account, time, region, resources, details : are common option among all events.
- The only event-based service that integrates directly with third party support. Eg. Zendesk, Auth0, Segments, etc.

**Event Bus :** Like a funnel that catches events generated by all AWS Services. 

- Each account comes with a **default** event bus.

- Event Bus has upto 100 event rules.

**Rule :** allows to filter a large number of events.

- **[IMP]** Rules are ***not*** processed in an order.
- We need to specify targets. (EC2, Kinesis, ECS, Lambda)

*AWS Supports Cross-Account Events.*

*Event Bridge is just CloudWatch with new features and support for **SAAS(Software as a Service)** products.*

#### Replaying Events and EventBridge Archives

- **Event Bridge Archives**
  - Greate to store as a backup
  - No Cost to Store
  - Replay Events
- **Schema registry** : Defines the structure of Event and helps describes what can you expect from event.
  - comes with pre-written schema for all AWS Service, and for few SAAS providers.
  - Schema can be generated automatically.

<hr>

### SNS (Simple Notification Service)

- Publish/subscribe messaging service
- managed, highly scalable

![image-20230218165652816](ch12.assets/image-20230218165652816.png)

- SNS is mostly used as a *producer* for SQS Queue
- Another Pattern

````
SNS ----> Lambda (modify notifications) ---->  SNS (new)
											|----> May take some action
````

<hr>

### SQS (Simple Queue Service)

- capability of sending storing and recieving messages at scale without dropping message data.
- Dead-letter-queue : Queue where dead letters/letters which are not cosumed are put at.
  - DLQ must be same type as the queue it is supposed to get letters from.

**MODEL**

- **Producers** puts data in Queue
- **Consumers** consumes data from Queue
  - Deletes data from queue : If processed
  - Puts back : If not processed

**Standard Queue**

- At least once delievary of message
- provides almost unlimited number of txn/sec
- Best Effort to preserve order (not necessary)

**FIFO Queue**

- Order is maintained (condition)
- limited #TXN/sec (default 30 TPS)
- Batching allows to perform action against 10 messages at once with a single action
- Exactly once processing

<hr>

### AWS Step Functions

- Lambda has limited flexibility and execution time limit of 15 min.
- Step Function : State Machine Services
  - Parallel
  - Sequential
  - In-Retry
  - If-Then
- States of Step Functions : 
  1. PASS
  2. TASK
  3. CHOICE
  4. WAIT
  5. SUCCESS
  6. FAIL
  7. PARALLEL
  8. MAP

<hr>

**Important Comparisons for AWS Exam**

**EventBridge**

- A very complex and sophisticated service

**SNS**

- limited parameters
- easily scales to millions
- No direct connectivity to Saas
- Limited Routing Capability
- Difficult to trigger Step Function
- Filtering is limited to attributes only





---

## File: aws/developer/ch2.md

## Compute

#### What is Compute ?

Physical Server within a data center would be considered as Compute resource as it may have multiple CPUs/GBs of RAM.

[Resource Link](https://aws.amazon.com/products/compute)

### Amazon EC2

EC2 allows you to deploy virtual servers within your AWS environment.

Components

- Amazon Machine Images (AMIs)
  - templates of pre-configured EC2 Instance for quick setup
  - you can create your own AMIs for deployments
  - AWS Marketplace : market to buy from AMIs from trusted vendors like Citrix,etc
  - Community AMIs
  - Instances : Micro (small) , General Purpose, Compute Optimized, GPU, FPGA (genomics, financial), Memory Optimised Instances
- Instance Purchasing Options : 
  - On-Demand : Launched at any time, usually short-term uses
  - Reserved : set period of time purchase for reduced cost
  - Scheduled : similar to reserved instance but recurring/ fixed schedule
  - Spot : Bid for a unused EC2 compute resources, fluctuating price
  - On-Demand Capacity Reservations : Reserve capacity based on platform, tenancy and area availability
- Tenancy
  - Shared Tenancy : EC2 is launched on any available host with required host, same host may be used by multiple customers.
  - Dedicated Instances : hosted on hardware that no other customer can access
  - Dedicated Hosts : Additional visibility and control on physical host

- User Data : allows to enter commands that will run during the first boot cycle of instance.
- Storage Options : Purely varying option as per need
  - Persistent Storage : Available by attaching EBS volume (network attached devices served by AWS network)
  - Ephemeral Storage : Created by EC2 instances using local storage : Physically attached to underlying host. All data gets terminated if you stop or terminate the instance, while during reboots data remains intact.

- Security
  - Security Group : Creates a security network rules which govern ingress/egress traffic.
  - Public Key/ Private Key


#### EC2 Autoscaling

We can setup scaling up and down based on CPU Utilization and helps size of EC2 fleet be cost effective.

- Automation
- Greater Customer Satisfication
- Cost reduction

Components of EC2 Auto Scaling

1. Create a Launch Configuration/Template
2. Create a Auto Scaling Group

### AWS Elastic Beanstalk

*AWS Elastic Beanstalk is an AWS managed service that automatically provisions and deploys resources required to run web application based on uploaded source code.*

Resources : AWS services and features such as EC2, Route 53, Auto Scaling, Health-Monitoring and ELB (Elastic Load Balancing)

AWS Elastic Beanstalk can operate with different platforms and lanaguages : Packer Builder, Single Container Docker, MultiContainer Docker, Preconfigured Docker, Go, Java SE, JAVA with Tomcat, .NET on Windows Server with IIS, Node.js, PHP, Python, Ruby.

**Note: AWS Elastic Beanstalk is free, only the resources that are created will cost money according to their charges. **

- Application Version : A specific version/section of code
- Environment : refers to application version taht has been deployed on AWS, comprised of all the resouces created by ECB
- Environment Configuration : Collection of parameters and settings that control environment
- Environmnet Tier : how Elastic Beanstalk provisions resources based on the application
- Configuration Template : provides baseline for creating a new, unique, environment configuration
- Platform : combination of components on which we build our Application like OS, Language etc.
- Application : collection of different elements like environment, environment configuration, etc.

#### Environment Tiers

Reflects on how Elastic Beanstalk provisions resources based on what the application is designed to do.

- HTTP Requests ---> Web Server Environment
- SQS Queue ---> Worker Environment

##### Web Server Tier

- Typically used for standard web application serving requests over **port 80**
- This tier typically uses following services and features : **Route 53**, **Elastic Load Balancer**, **Auto Scaling**, **EC2** Instances and **Security Groups**.

- A host manager is installed on every EC2 Instance
- **Host manager** responsibilities includes
  - Aid in deployment of application
  - Collecting different metrices and different events from EC2 instances which can be reviewed from within the console, or vial AWS CLI or API
  - It generates instance level events
  - It monitors both the application log files and application server itself
  - It can be used to patch instance components
  - manages log files allowing them to be published to S3

##### Worker Tier

- Used by application that will have a backend processing task, interacting with AWS SQS
- This tier typically uses the following AWS resources in the environment : **SQS Queue**, **IAM service roles**, **Auto Scaling** and **EC2** Instances

- A minimum of one EC2 instance is used and is attached to auto scaling groups
- Each EC2 instance in the environment will read from the same SQS Queue
- A **daemon** is installed on every EC2 instance to pull request from the SQS queue
- You can develop and add your **own** Elastic Beanstalk configuration files withing your application **source code**. These file need to be save as `.config` file extension and stored withinn `.ebextensions` folder of source code.

![image-20220727165713696](ch2.assets/image-20220727165713696.png)

#### Deployment Options

- All at once (Default Option) : Abruptly resources deploy the application
- Rolling : minimise disruption and deploys in batches (2 versions of application up at a time)
- Rolling with Additional Batch : updated in batched until all resources have the new update, added batch ensures application availability
- Immutable : create an entirely new set of instances and serve through a temporary autoscaling group behind your ELB

#### Health Monitoring

- Basic Health Reporting

  - High level overview of how environment is performing
  - resources will send metrices to Amazon CloudWatch in 5 minutes interval
  - 4 colors within AWS Elastic Beanstalk dashboard that show the health status
  - Every 10s ELB will send a health check request to every instance in the auto scaling group and wait for response to confirm health status

  - For single instance environments the health of instance is determined by its EC2 instance status check
  - Elastic Beanstalk will ensure that in a web environment, an autoscaling group has a min of 1 instance running that is healthy
  - Check to ensure the CNAME in Route 53 is redirected to correct ELB
  - Check the security groups for EC2 instances that allows port 80 inbound
  - In worker environments, check to ensure SQS queue being used is being polled every 3 minutes at a minimum.

- Advanced Health Reporting

  - Enhanced health monitoring display additional information to that over basic
  - AMIs used for EC2 instances have a health agent installed and running
  - Health Agent Captures additional Information about system metrices & logs
  - Metrices can be sent to AWS CloudWatch as custom metrices, for additional cost

### AWS Lambda

It is serverless compute service that allows you to run your application code without having to maange EC2 instances.

Responsibility to maintain and administer the EC2 instances is passed over to AWS to manage for you.

Only pay for compute power when Lambda is in use via Lambda Functions. AWS Lambda charges compute power per 100ms of use only when your code is running, in addition to the number of times your code runs.

Four Steps to Operation

- Write/Upload source code to Lambda
- Configure your Lambda functions to execute upon specific triggers from supported event sources (like file upload on s3 bucket)
- Once triggered, Lambda will run code using required compute power
- AWS records the compute time in milliseconds and the quantity of Lambda functions run to ascertain the cost of service.

Components for AWS Lambda

- Lambda Function : parts of our own code that want Lambda to invoke
- Event Sources : AWS services that can be used to trigger Lambda Function
- Downstream Resources : resources that are required during the execution of your Lambda function
- Log Streams : helps to identify issues and troubleshoot issues with your Lambda functions

*Always use 644 permissions on zip file uploaded to Lambda*

#### Event Sources

An event source is an AWS service that produces the events that your Lambda function responds to by invoking it

- Push Based Services : BucketS3, CloudWatch, etc.
- Poll Based Services : Amazon Kinesis, Amazon SQS, Amazon DynamoDB, etc.

Event Source Mapping : configuration that links events source to Lambda function

- Push-based service : mapping is maintained within event source
  - requires specific access to allow your event source to invoke the function
- poll-based service : configuration mapping is held within lambda function
  - Permission is required in the execution role policy

Synchronous Invocation :

- It enables you to access the result before moving onto the next operation required
- Controls the flow of invocations
- Poll Based event sources are always synchronous while push based events it varies with service.

![image-20220728224401128](ch2.assets/image-20220728224401128.png)

#### Monitoring and Troubleshooting

Monitoring statistics related to Lambda function with Amazon CloudWatch is by default already configured. This also includes monitoring your function as they are running.

Mertices : Invocations, Errors, Dead Letter Errors (SQS Queues drop), Duration, Throttles, Iterator Age, Concurrent Executions, Unreserved Concurrent Execution.



---

## File: aws/developer/ch3.md

## Storage 

### Amazon S3

#### Overview

- Amazon S3 is a fully manage object based storage service that is highly available, highly durable, cost effective and widely accessible.
- Smallest Size : 0KB, Largest Size : 5TB
- Each object uploaded does not conform to file structure level heirarchy like OS, instead its storage as object with flat address space and located by unique url.
- Its a regional service. [Resource](https://cloudacademy.com/blog/aws-global-infrastructure)
- To locate a specific file within the bucket we use keys and to access that object via internet we use object url. Bucket url and object key makes up the object url.

#### Storage Classes

1. S3 Standard : 
2. S3 INT (Intelligent Tiering) : for both frequent and infrequent access (use when frequency is not known)
3. S3 S-IA (Standard Infrequent Access) :
4. S3 Z-IA (One zone and Infrequent Access) :
5. S3 Glacier : Long term archival storage solution
6. S3 G-DA (Glacier Deep Archive) : same as S3 Glacier with min 12 hours retrieval time.

All 4 above services offer **High Throughput**, **low latency**, **SSL to encrypt data during transit**, **lifecycle rules to automate data storage management**.

S3 has Highest availability of 99.99% and Eleven 9s durability. S3 INT, S3 S-IA have similar availability and durability. S3 Z-IA have such durability and availability only for a region.

**Lifecycle Rules** : You are able to set and configure specific criteria which can automatically move your data from one storage class to another or delete it. (to save cost we can move around data not in use to other cheaper classes).

Intelligent Tiering is based on principle : *more frequently accessed data is more faster to access*. Within the same class there are two tiers : Frequent Access and Infrequent Access, thoughout the life cycle data keeps moving around according to its demand.

Glacier Services do not offer graphical user interface and its a two step process to setup to move data into glacier.

1. Create your valut as a container for your archives
2. Move your data into the Glacier vault using the available APIs or SDKs

Access to data is costly depending on how urgently you need the data : expedited (under 250mb available in 5 minutes) , standard (any size, 3-5 hours) and bulk (PB of data, 5-12 hours) options.



### S3 Management Features

#### Versioning

- Versioning is maintained automatically completely by AWS if enabled (not enabled by default) but once enabled can’t be disabled only paused/suspended.
- Version ID is used to maintain versions. Deleted versioned files can be seen when show/hide is toggled with version called *Delete Marker*.
- If you enable versioning on an existing bucket in Amazon S3, how are the unmodified objects already in them labeled? : Null

#### Server Access Logging

- Logs are collected every hour and there is no hard and fast rule that every request is logged, sometimes specific logs may not be available.
- You will need to configure Target bucket (used to store the logs, should be same zone as source bucket) and target prefix for management. You can also configure this while bucket creation.
- If you using AWS Console then Log Delievery Groups are automatically added to Access Control List of the target bucket. But if you are utilizing some API/SDK you will need to manually add access to ACL.
- Log Naming Standard : \<Target Prefix\>YYYY-MM-DD-HH-MM-SS-UniqueString/
- Entries in logs are as : BucketOwner Bucket TimeStamp RemoteIPAddress Requester Operation Key RequestURI HTTPStatus ErrorCode ByteSent ObjectSize TotalTime(ms) TurnAroundTime Referer User-Agent VersionID HostID Cipher Suite AuthHeader TLS Version

#### Object Level Logging

- Closely related to AWS Cloudtrail and logs DeleteObject, GetObject, PutObject requests. It also logs Identity of the caller, timestamp and source IP address.
- Can be configured at Bucket level or AWS Cloudtrail Console.

#### Transfer Acceleration

- Amazon Front is a CDN (Content Delievery Network) greatly increased transfer speeds between client to S3 or vice-versa.
- There is a cost associated with Transfer Acceleration per GB according to Edge region.
- NOTE : your bucket name always should be DNS complaint and should not contain any periods to utlize this feature.
- Trasfer Acceleration doesn’t Support GET Server, PUT bucket, DELETE Bucket and Cross-region copies using PUT Object Copy

### Amazon S3 Security

#### Using Policies to Control Access

- Identity Based Policies : Attached to IAM identity requiring access, using IAM permission policies, either in-line or managed.
  - Assoiciated to a User or role or group
  - We can control access with **conditions** [Resource](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html)
- Resource Based Policy : policy is associated with a resource
  - Forms : Access Control Lists and Bucket Policies
  - Need to define who will be allowed/denied access
  - Written in JSON or use AWS policy generator
  - permissions are controlled with **principals**
- IAM Policies are desired in case to centrally manage access and you have several roles to assign rather than 1 bucket/policy, Can control access for more than one service at a time. (max allowed policy size : 2Kb is size for users, 5Kb for groups, 10Kb for roles)
- Bucket Policies : controls S3 buckets and its objects, Used to maintain security policies within S3 alone. Can grant cross-account access without having to create and assume roles using IAM (max allowed policy size : 20Kb)

Both are not mutually exclusive and used together. In case of information conlict : principal of Least-Priviledged is utilised : if there is even single deny, any authorized request will be denied.

#### S3 Access Control List

- ACLs allows control of access to bucket, and specific objects within a bucket by groupings and AWS accounts
- can set different permissions per object
- ACLs do not follow same JSON format as the policies defined by IAM and bucket policies
- More Granular Control, can be applied at Bucket Level or Object Level.

- Permissions : LIST, WRITE, BUCKET ACL READ, BUCKET ACL WRITE

#### Cross Origin Resource Sharing (CORS) with S3

CORS allows specific resouces on a web page to be requested from a different domain than its own.

This allows to build client-side web application and then, if required, you can utilise CORS support to access resouce stored in S3.

Policy(JSON) is evaluated on three fold rules

1. Requestors *Origin* header matches and entry made in *Allowed Origins* element
2. The method used in request is matched in Allowed methods
3. The headers used in Access-Control Request Headers within a preflight request matches a value in the *Allowed Header* element.

### Amazon S3 Encryption

- SSE-S3 (Server Side Encryption with S3 managed keys)
  - minimal configuration, upload all data and S3 will manage everything
  - AWS will manage all encryption keys
- SSE-KMS (Server Side Encryption with KMS managed keys)
  - allows S3 to use Key Management Service to generate data encryption keys
  - gives greater flexibility of key diabled, rotate and apply access controls.
- SSE-C (Server Side Encryption with customer provided keys)
  - provide you master keys
  - S3 will manage encryption
- CSE-KMS (Client Side Encryption with KMS managed keys)
  - uses key management service to generate data encryption keys
  - KMS is called upon viathe client, not S3
  - encryption happends on client side and encrypted data send to S3
- CSE-C (Client Side Encryption with customer managed keys)
  - utlise your keys
  - use an AWS SDK client to encrypt data before sending to AWS for storage

### Best Techniques to Optimize S3 Performance

1. TCP Window Scaling
2. TCP Selective Acknowledgement
3. Scaling S3 Request Rates
4. Integration of Amazon CloudFront



---

## File: aws/developer/ch4.md

## Databases

### Amazon DynamoDB

- NoSQL Database (Key-Value Store) : A collection of items or records.
- You can look up data : 
  - Using a primary key for each item
  - Through the use of indexes
- Very High Performance mainly used for Gaming, Web, Mobile and IoT
- Fully Managed : backups, patches etc are managed by AWS
- Bill consists of two factors
  - The total amount of throughput that you configure for your tables (provisioned capacity )
  - The total amount of storage space used by your data
- DynamoDB tables are schemaless, schema is defined per item
  - As long as the primary key is valid there is no limit on attributes
  - primary key consists of two attributes : partition key and sort key
- You can define several secondary indexes besides primary key for search
  - There are two types of secondary indexes : Global and Local Indexes
- Disadvantages
  - Since replication of data is present thorough multiple zones so it relies on concept of ***Eventual Consistency***, so its possible some zones might have older data
  - Queries are less flexible than SQL
  - Strict Workflow limitations like max record size : 400kb, max indexes per table : 20 global, 5 local
  - provisioned throughput (ProvisionedThroughputExceededException)

### Amazon Relational Database Service (RDS)

- Its a fully managed RDS that allows users to *Provision, Create, Scale* a relation database
- RDS allows us to choose from various Database Engines : MySQL, MariaDB, PostgreSQL, Amazon Aurora (fork of MySQL), Oracle (Common in Corporate), SQL Server
- Choice of compute instances is available while provisioning Database
  - General Purpose
  - Memory Optimized
- Synchrous Replication between primary and secondary instance. In case if primary instance fails then AWS automatically points DNS to secondary instance within (60-120s). [Multi AZ]
- Storage Autoscaling
  - EBS (Elastic Block Storage) (MySQL, Postgres, MariaDB, Oracle, SQL server)
    - General Purpose SSD storage, good for broad range of cases
    - Provisioned IOPS (SSD Storage), good for workloads that operate at very hight I/O
    - Magnetic Storage (mostly for backwards compatibility)
  - Shared Cluster Storage (Amazon Aurora)
    - Configuration options doesn’t exists and scaling occurs automatically
- vertical scaling : scaling towards computing capability
- horizontal scaling : increasing replicas of storage instances to deal with high volume of read queries. Note all replicas are synchrously linked.

### Amazon ElastiCache

- This service improves performance by using caching, where web application allow you to retrieve information fast, managed, in-memory data stores.
- Caching : Additional memory enables our devices to store frequently accessed information in memory instead of having to request the information from the hard drive
- It improves the read-only performance of server.
- Engines
  - Amazon Elasticache for Memcached : A high performance, submillisecond latency Memcached Compatible in-memory, key-value store service that can either be used as a cache, in addition to a data store
  - Amazon Elasticache for Redis : An in-memory data store designed for high performance and again providing sub-millisecond latency on a huge scale to real-time applications
- Components of Elasticode
  - Node : a fixed sized chunk of secure network attached RAM
  - Shard : redis shard (node group) a group of up to 6 Elasticache nodes
  - Redis Cluster : group of 1-90 redis shards
  - Memcached Cluster :  a collection of more cache nodes
- Elasticache should never used 
  - when data persistence is necessary
  - when working with primary data records
  - when we need write performance, rather than read performance



---

## File: aws/developer/ch5.md

## Network & Content Delivery

### What is an API ?

API : Application Programming Interface, provides users or programs a clean and clear method of interacting with the underlying service.

Internet is based on Request/Response model based on HTTP protocols.

Most common requests are : GET, POST, PUT, DELETE. Response codes are returned are 1xx,2xx,3xx,4xx,5xx.

- 1xx ~ Information
- 2xx ~ Success
- 3xx ~ Redirection
- 4xx ~ Client Error
- 5xx ~ Server Error

HTTP is a communication protocol, while REST API set of constraints defined on a communication protocol. REST : Representational State Transfer. REST is more like an architecture design pattern, it could easily be build upon other protocols like TCP. Just because of a lot of usage with HTTP it is used interchangeably with HTTP.

- Lightweight, loose coupling between client and server.
- No assumptions by client or server.
- Requests should not be stored by server.
- Clients can only access resources using URI

### Amazon Gateway

Amazon API Gateway provides complete solution related to publishing, maintaining, monitoring, building and securing an API using its services.

It supports serverless, generic servers and containerized workloads.

You don’t need to manage infrastructure and its cost effective as you pay for what you use.

How does requests come into the API ? API Endpoints

- Edge-Optimized API Endpoint
  - many geographically distinct and distributed clients
  - all requests are forwarded to closed cloudfront
  - reduces TLS overhead and overall improves response speeds


- Regional API Endpoint
  - when user wished to use their own CDN or doesn’t want to use CDN

- Private API Endpoint
  - can only be accessed within VPC, microservices or internal applications

#### Supported Protocols

1. HTTP (REST) Endpoints

   - REST Api : 
     - Single price for all inclusive features to manage, publish API

   - HTTP API (NEW)
     - Building proxy APIs for AWS Lambda or any HTTP endpoint
       - Building modern APIs that are equipped with OIDC and OAuth2
       - Workloads that are likey to grow very large APIs for latency-sensitive workloads

2. Websocket Endpoints
   - Creates real-time communication apps
   - requires a good connection
   - use case specific

#### API Integration

Two ways to do API Integration

1. Proxy Integration : 
   1. easy to setup
   2. almost everything is handled in the backend service
   3. great for rapid prototyping
2. Direct Integration :
   1. Decouples Amazon API Gateway for backend’s request and response payloads, headers and status code
   2. Make changes and not be locked into the backend service’s response

#### Integration Types

![image-20220915125206428](ch5.assets/image-20220915125206428.png)

![image-20220915125307895](ch5.assets/image-20220915125307895.png)

[Pictures : From CloudAcademy :)]

#### API Gateway Authorizers

- IAM Authorizer
  - client requirements : signature v4, “execute API” permissions
  - rest api, http api, websocket endpoints
- AWS Lambda
  - legacy or third party auth providers
  - rest api, http api, websocket endpoints
- Cognito Authorizer
  - complete auth solution
  - only rest api
- JWT Authorizer
  - Auth2 compliant anything like openID authorizers
  - only with http

AWS WAF are available by default protects users APIs using DDOS prevention.

#### API Management and Usage

You can set up for consumers usage plans like, premium user and basic user. 

API keys can be distributed to consumers and can manually be set up with throttling and quota for consumers.

Only Rest API versions can access this feature.

#### Caching Responses

Builtin into the API Gateways, useful for speed and costs. TTL can be setup between 0 and 3600 seconds. Usually having 1sec cache can greatly improve application.

Only Rest API version can access this feature.

#### Monitoring Metrices

These metrices can be sent to Cloud Watch where it can visualised, set and alarm and do multiple things with the exam.

- CacheHitCount
- CacheMissCount
- Count
- Integration Latency
- Latency

Rest API being expensive features niche features but HTTP API is most cost friendly.

### Amazon CloudFront

AWS’s fault-tolerant and globally scalable content delivery network service. It provides seamless integration with other Amazon Web Services to provide an easy way to distribute content.

Speeds up distribution of your static and dynamic content through its global network of edge locations which answer to closest user rather than the source increasing overall speeds.

Its main aim is distribution, not to store data for you. Its more used to cache data.

CloudFront uses distribution to control which data needs to be distributed.

- Web Distribution
  - Speed up static and dynamic content
  - distribute media files using HTTP or HTTPS
  - add, update or delete objects and submit data from web forms
  - use live streaming to stream an event in real-time
- RTMP Distribution
  - distribute streaming media services, adobe flash media services
  - resource data can only stored in s3 bucked not ec2 instances

If using an S3 bucket as origin, then for additional security you can create a CloudFront user called an **origin access identity** (OAI)

This OAI can access and serve content from your bucket.

### Elastic Load Balancer (ELB)

ELB manages and controls the flow of inbout requests destined to a group of targets by distributing these request evenly across targeted resource group.

Targets could be fleet of EC2 instances, Lambda function, range of ip addresses and even containers.

Targets could be from different zones.

There are three types of Load Balancers

- Application Load Balancer
  - for web application running HTTP or HTTPS
  - operates at request level
  - Advanced routing, TLS termination and visibility features targeteted at application architecture
- Network Load Balancer
  - ultra high performance while maintaining very low latencies
  - operates at the connection level, routing traffic to targets within your VPC
  - handles millions of request per second
- Classic Load Balancer
  - used for application that were built in the existing EC2
  - Classic environment

#### ELB Components

- Listener : for each load balancer we must configure at least one listener
- Target Groups : group of resource where traffic is routed by ELB
- Rules : defines how an incoming requests gets routed to which target group

![image-20220915154222242](ch5.assets/image-20220915154222242.png)

All listeners ends up to a single actions.

Health check of Target Groups can be taken to check if target is healthy for traffic or not

Internet facing ELB : shields servers from external traffic and then route traffic accordingly.

Internal ELB only responds to traffic withing VPC only

### SSL Server Certificates

When using HTTPS as listener 

- HTTPS allows encrypted communication channel to be setup between clients initiating the request and your ALB
- To allow your ALB recieve encryted traffic over HTTPS it will need a server certificate and an associated security policy
- SSL (Secure Sockets Layer) is a cryptographic protocol much like TLS (transport layer security). 

The server certificate used by ALB is X.509 certificate, which is digital ID provisioned by Certificate Authority such as AWS certificate Manger (ACM)

This certificate is used to terminate the encrypted connection recieved from the remote client, and then the request is decrypted and forwarded to the resources in the ELB target group.

#### Application Load Balancer

ALB operates at layer 7, the application layer in OSI Model. It provides application processes or services it offers are http, ftp, smtp and nfs.

Target groups can be configured to respond to different protocols.

#### Network Load Balancer

Conceptually both are same but Network Load Balancer sits right at layer 4, Transport Layer. It operates and balancer request purely based on UDP/TCP protocol.

NLB cross-zone load balancing can be enabled or disabled.

#### Classic Load Balancer

Its supports all TCP, SSL/TLS, HTTP and HTTPS protocols. It lets you load balancing an existing applciation running in EC2 classic network.

EC2 classic is no longer supported for newer AWS accounts.

It supports sticky sessions using application-generated cookies.



---

## File: aws/developer/ch6.md

## Analytics

- Amazon Kinesis was desinged to address complexity and costs of streaming data in AWS cloud
- Data in Cloud is processed by Kinesis. (Event Logs, Social Media Data, Clickstream data, App Data, IOT Sensor Data)
  - Connect
  - Process
  - Analyze
- Processes in real time or near real time.
- Amazon Kinesis processes
  - Video Streams (binary encoded)
  - Data Streams (base64 encoded)
  - Data Firehose (base64 encoded)
  - Data Analytics (base64 encoded)

- Layers of Streaming
  - Source
  - Stream Ingestion (Kinesis Agent/Producer Library/ SDK)
  - Stream Storage (Kinesis Data Streams) : Data here is *immutable*, Data only expires (24hrs-365days).
  - Stream Processing (Kinesis Data Analytics/Data Firehose/Consumer Library)
  - Destination

#### Amazon Kinesis Video Streams

- Stream binary encoded data (not limited to video only)
- AWS SDK makes it possible to securely stream data into AWS for playback, storage, analytics, ML or other processing
- supports WebRTC --> 2 Way communication
- *doesn’t have ability to autoscale*
- Kinesis Producers can be created using : AWS SDKs, Kinesis Agent, Kinesis API, Kinesis Provider Lib

**SHARD** : contains sequence of data records namely : (Sequence No, Partition Key, Data Blob)

- There is a charge for retrieving data older than 7 days from a Kinesis Data Stream using this API : `GetRecords()`
- There is no charge for long term data retrieval when using *Enhanced Fanout Consumer* : `SubscribeToShard()`

Consumer can consume data using two methods

| Classic               | Enhanced Fanout                                              |
| --------------------- | ------------------------------------------------------------ |
| pulls data from shard | push method : subscription method                            |
| Polling               | shard limits are removed                                     |
|                       | every consumer gets 2 mbps of provisioned throughput per shard |

### Kinesis Data Firehose

- fully managed data delievary service
- Ingested data can dynamically
  - tranformed
  - scaled auto
  - auto delivers
- uses producers to load data streams in batches once inside the stream data is delieverd to a data store
- There is no need for custom code or application to processes data in data streams
- Buffer Size : 60-900s
- Data Stores : Elastisearch, RedShift, S3, Splunk, Generic HTTP Endpoints, MongoDB, DataDog, New Relic
- No Free Tier
- Costs are incurred when data is in stream
- There is no bill for provisioned capacity, only used for capacity

### Kinesis Data Analytics

- Ability to read from streams in real time and do aggregation and analysis on data while it is in motion
- leverages SQL Queries (Firehose) or Apache Flink (Data Streams)
  - Uses Java/Scala to do time series analytics, feed real time dashboard & metrices
- Use Cases ETL, generation of const metrices and doing real-time analytics
- No free tiers

### Fundamentals of Stream Processing

- Not all data is created equally, its *value changes over time*
- traditionally data is stored in RDS or Enterprise cloud server which is later processed in batches

**Batch Processing :** data is collected, stored, and analyzed in chunks of fixed size on a regular interval

- regular interval depends on freq of data collection, relative `value`(*Central Idea of this concept*) of insight gained
- Advantages
  - Evenly Spaced
  - Predictable
- Disadvantages
  - Has no intelligence. (session intermixing due to fixed batch size)
  - Wait until specific amount of data is accumulated

**Stream Processing** : solves latency, session boundaries and inconsistent loads

- DataSources : Application, Networking devices, server log files, web activity, location
- Events are recieved from stream which in turn can do any of of following
  - Trigger an action
  - update an aggregate or similar statistic
  - cache the event for future reference

**Consumers :** Application that process the data from stream, can create new streams too.

- Stream Application has 3 important parts
  1. Producers
  2. Data Stream
  3. Consumers
- Benefits of Streaming Data
  - Never ending streams of data
  - best processed in flight (realtime)
  - limited storage capacity (price)
  - detect patterns, inspect results, intermix streams
  - reaction in RealTime (no logs)
  - Decouples architecture and improves operation efficiency
- Benefits of Batch Application
  - predictable in terms of pricing/cost
  - response is not required to be *instant*

#### A Streaming Framework :

- Common use cases of streaming data : Industrial Automation, Smart Home, log analytics, datalakes, IOT
- Events : Search result, financial transactions, user activity, Telemetry data, log files, application metrices.
- data is processed in motion
  - MI/AI applications
  - trigger other events
- Data is immutable, consumer subscribe and create new stream out of it.
- Stream matches real world application high velocity and volume data

Use Cases for data Streaming

- Clickstream Analysis
- Preventive Maintenance
- Fraud Detection (used by credit card companies)
- Sentiment Analysis (ML/AI Applications)
- Dynamic Price Engine

![IMG_906F104BB956-1](ch6.assets/IMG_906F104BB956-1.jpeg)

Challanges

- “High Touch System” : very difficult to automate
- difficult to setup : `# of moving parts`
- Expensive
- Issues with scaling operation

Streaming as a managed Service : *Amazon Kinesis*

- Minimize chance of data loss
- Provision resources automatically on request
- fully scalable (not shards)
- highly integrated with AWS

### Elements of Kinesis Data Stream

- No free tier, cost is for `open shards` and for Data Records stored in stream

Creating an AWS Kinesis Stream

```bash
aws kinesis create-stream --stream-name myStream --shard-count 3
```

Other important flags : `--describe-stream-summary`

- Each shard has unique id, hash key range (unique) and doesn’t overlap
- Capacity of each shard is limited to 1000 each shard
- Concept of *Hot Shard* <-- lots of data records go into one shard. 
  - ***Resharding*** is used to add more shards for increasing throughput limit of 1000 Records
- Data Retention Period : 365 days (earlier 24 days)
- Data Stream Limitations
  - Max Size of 1 MB (for Records)
  - Shard can accept 1k records/s
  - default retention : 24hrs
  - size of data records cannot be increased but retention period can be extended upto 7 days for additional charge upto a year
- Producer(writes) ----> Shard
  - limitation : 1MB/s per shard
  - returns : `ProvisionedThroughputExceededException`
- Consumers
  - Classic Consumer : 2MB/s read
    - Throttle if read more than 2 MB/s
    - polls data
  - Enhanced Fanout Consumer : 2MB/s read
    - can’t pull data of shard
    - keeps requesting subscribe to stream call
    - uses HTTP/2
    - utilised a push mechanism

#### Shard Capacity and Scaling

2 types of limits

1. Write Rate : 1k records/s ~ 1MB/s
2. Std Consumer : 5 txn at 2MB/s

- It becomes essential to utilise all shards equally basically there should not be hot/cold shards
- Total throughput = Sum of all shards
- Kinesis streams are elastic but scaling is not supported/managed by AWS

**Shard Splitting** : adds throughput, increases capacity by 1 MB/s and can be used to divide hot shard

- For splitting shard is closed (to stop producer from writing), data stays till its expires(consumers can read data till shard split happens)

**Merging Shards** : useful for cold shards to reduce costs

***Resharding*** is managed programitically using API

- Update Shard Count
- Split Shard
- Merge Shard

**Update API Limitations**

- Max Number of Shards : double of current shard cnt
- Min Number of Shards : half of current shard cnt
- Max of 10 times reshard in 24 hrs
- Not possible to scale past shard limits

default shard quota

- AWS US East/West or AWS Europe : 500/account
- other regions : 200/account
- This quota can be increased by talking to Amazon Tech Support

*10k shard is default hard limit of Kinesis*

### Kinesis Data Stream

- A real time data ingestion service from AWS “Stream Storage Layer”
- firehose (needs to be prefixed by lambda) easier to work with S3
- Putting data in Kinesis Data Stream, requires 3 inputs : Stream Name, Partition Key, Data
  - `putRecord()`
  - `putRecords()` (preferred)
- 200ms min time consumers can request data
- 5 locations to access shards from consumers
- Data Stream Design

![IMG_41CEF7A0F30E-1](ch6.assets/IMG_41CEF7A0F30E-1.jpeg)

**Retryable** : Exponential Back-off (Retry Timer)

- partial failures are considered as success so don’t rely on 200 response

**Network Latency: **

- Traffic spikes may put records in streams unevenly which results in spikes in throughput
- use interface VPC endpoint to normalize traffic
- Producer ----> VPC Endpoint ----> Data Stream
- handle Backpressure (resistance to flow of data) to relieve stream of spikes.

**KPL** : Kinesis Producer Library for putting data in stream

**SDK** : helps keeping cost calculation simple

- KPL can do data aggregation while KCL can do deaggregation
- KPL improves throughput and reduces cost

- KPL has builtin retrying functionality
- KCL has a checkpoint feature which keeps track of resume point in case of client failure.
  - Amazon DynamoDB tracks subsequence, can be a throttle subsequence

#### Kinesis Data Stream Security

Principle of Least Privilege is still very important.

1. Organisational
2. Technical
3. Personal

- Real about IAM, Access and Management
- Defaults : deny (permissions)
- Policy to grant acess
  - Effect : allow/deny
  - Action :
  - Resource : ‘arn:aws....’

IAM Best Practices through 4 policies

- Administrators : Create/Delete/Tags

- Stream Resharding : Merge/Split
- Producers : Writing, Put, Describe
- Consumer : Read, Get

Kinesis Data Streams can be encrypted using HTTPs Endpoints : Using KMS

- FIPS : Federal Infromation Processing Standard

---

## File: aws/developer/ch7.md

## Management and Governance

### Amazon Cloudwatch

- window to monitor (Health, Operation Performance) of your (Apps & Infra).
- By window ---> Meaningful data ---> Insights on Manual or Automated responses (changes/modification to apps or Infra)
- Cost : 5 min free metrices for EC2
- Every minute insights costs fee

Different Services

- CloudWatch Dashboards
- CloudWatch Metrices and Anomaly Detection : One of the reasons AWS is famous !!
- CloudWatch Alarms (automated action based on several condition) : SNS, SQS, SQE
- CloudWatch EventBridge (Connect ot other AWS services based of events), Rules(event bus) ---> Target
- CloudWatch Logs (Real Time Monitoring)
- CloudWatch Insights (Container Lambda logs)

### CloudWatch Dashboards

- Can be created by yourself or generated automatically.
- can use visual editor to play with widget or programatically (JSON)
- Line, Stacked Area, Number, Bar, Pie charts, Text Widget, Log Tables, Alarm Status.
- Can apply general mathematical operation on graph like normalization etc
- 3 Dashboard with 50 widgets are free more than that is 8$/month per dashboard

Best Practice

- Large Graphs for important graphs
- Keep all metrices in single screen
- Display Timezones (UTC) - Teams may be in different TZ
- Annotate but not point entire ROME on it

### CloudWatch Anomalies Detection

- powered by machine learning
- Automates creation and maintenance of cloudwatch alarms
- learns from past data, so model improves over time
- **FUNNY STORY :** EC2 was left idle for a long time and when used after a while will be treated as anomaly.
- Intially model maybe jancky, gets better eventually

### CloudWatch Subscriptions

- Centralised Realtime feed of logs which can be filtered from Cloudwatch to trigger events on other AWS Services (S3, Firehose, Kinesis)
- Filter (log group name, filter pattern, destination, role arn, distribution method)
- can be shared among vairous aws accounts

## AWS Cloudformation

*Very important topic recently, was asked 10 question from this topic along  :)*

- dashboard within management console allows you to setup and config the associated resouces you are interested in
- dashboard is helpful for simple workflows that are pretty much daily chore of multiple services --> Automate
- Use Templates `yml/json`
- Security Standards to enforce regulations
- Infrastructure Replication

Components of AWS CloudWatch

1. **Stack** : Set of AWS resources that can be provisioned/updated or deleted all at once.
2. **Template** : `json/yml` : describes env and resources to build
3. **Stack Set** : manage all stack across a number of AWS account across region
4. **Designer** : allows you to visually create env through drag n drop interface

Important Ques : What are minimum parameters needs to be defined in a Template in CloudFormation.



### VPS Flow Logs

- Capture IP traffic information that flows within your VPC
- Resolve incidents with network communication and traffic flows
- helps spot traffic reaching a destination that should be prohibited.
- VPC flow logs -----> CloudWatch
- VPC peered connection are being used, you can only see information b/t VPCs under your account

**Limitation** : Not Logged

- DHCP Traffic within VPC
- Traffic from instances destined for Amazon DNS Servers
- Traffic destined to IP Addresses for the VPC default router
- `169.254.169.254` : Amazon Instance Meta Data
- `169.254.169.123` : Amazon Time Sync
- Traffic from windows activation license from AWS
- Traffic b/t Network Load Balancer and Interface and Endpoint Network Interface

3 places to enable log 

1. Network Interface
2. VPC
3. VPC Subnets

**Flow Record Log Example**

![IMG_BC91ADD33BEA-1](ch7.assets/IMG_BC91ADD33BEA-1.jpeg)

---

## File: aws/developer/ch8.md

## CI/CD

### Continous Integration

- CI is a practice, supported by people and software
- continously integrating small changes to code into existing codebase using git, build automation, linters etc.

Creating a development Environment

- local development environment mirrors production code
- `vagrant` + `virtualbox` : to create VMs

NOTE : we could something liike puppet or ansible playbook also in place of vagrant

Some important vagrant commands :

````
vagrant up
vagrant ssh
vagrant halt
vagrant destroy
````

<hr>

### Version Control System (VCS)

- Tracking changes to code overtime
- Git Basics are required to achieve this
  - Personal Notes
  - Blog Article Link

<hr>

### Testing

- All code should be considered broken until proven otherwise
- Unit Testing and Integration Testing

- Testing is important because it catches problems early when they are cheap to fix

````
Unit Testing -----------------------------> Integration Testing
|																									 ^
|-----> Linters ---> Coverage ---> Static Scans ---|
````

<hr>

### Database Schema Changes

- Schema Migration poses Challenges
- ORM + Schema Migration tools + Strategy could easily help in tracking DB Changes
- ORM stands for Object Relation Mapper

Some good DB practices

- Database should be versioned
- One Schems Change per migration
- Changes should be non-destructive
- New columns require same defaults

<hr>

### CI with Jenkins

---

## File: aws/developer/ch9.md

## AWS Developer Tools

### AWS CodeCommit

- fully managed private Repository Hosting
- All features of git are supported
- Integration with Cloudwatch Events, SNS Subscription
- IAM
  - HTTPS git credentials
  - SSH
- Codecommit permissions

### CI/CD Pipeline

![image-20230218212300791](ch9.assets/image-20230218212300791.png)

### AWS Code Build

- fully managed build service
- uses docker build containers/allows custom images
- `buildspec file` ----> defines build artifacts(Lambda, S3 Hooks, etc) can be stored

### AWS Code Deploy

- fully managed deploy service
- it can deploy artefacts from builds
- can be automated on successful build
- Agent install ~ need to choose OS to deploy Code
- `appspec` file : (For EC2 deploy `yml`) , for lambda it can be `yml` or `json`
- deployment groups will have agent installed

### AWS Code Pipeline

- continous delievary system
- features
  - automation of build,test & release
  - manual approvals
  - pipelines history reports
  - pipeline status visualisation
- very good integration with other code services
- Pipeline Concepts : Pipeline, Stage, Action, Transition
- Action Types : Approval, Source, Build, Test, Deploy, Invoke
- Integration Options
  - Pipeline Action Types
  - CloudWatch Events
  - Invoke Lambdas

### AWS Codestar

- quickly launch CI/CD pipeline that suits your requirements
- Dashboard Visualisation
- Team Membership Management
- Issues and Ticket Tracking Management

### AWS X-ray

- Trend : Monoliths ----> Microservices
- Challange : Distributes Applications are harder to debug !!!
- *Has too many moving parts, they are difficult to keep track of efficiency issue*
- provides visibility in working microservices and trace pathways and find error, bottlenecks in application.
- X-Ray Sampling is a great way to debug performance issues in distributed applications

![image-20230218213123796](ch9.assets/image-20230218213123796.png)

---

## File: aws/developer/index.md

## Cloud Academy Notes



1. [Developer Associate Introduction](ch1.md)
2. [Compute](ch2.md)
3. [Storage](ch3.md)
4. [Database](ch4.md)
5. [Network & Content Delivery](ch5.md)
6. [Analytics](ch6.md)
7. [Management & Governance](ch7.md)
8. [Understanding CI/CD](ch8.md)
9. [Developer Tools](ch9.md)
10. [Containers](ch10.md)
11. [Security, Identity, and Compliance](ch11.md)
12. [Application Integration](ch12.md)



---

## File: aws/index.md

### AWS Notes



- [Cloud Practioner](./cloud/index.md) (WIP NOT Publised yet)
- [Developer Associate Notes](./developer/index.md)
- [Database Speciality](database/index.md)

---

