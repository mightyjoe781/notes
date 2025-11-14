# Storage

## Amazon S3

- Main Building block of AWS
- Infinitely Scaling Storage
- Use Cases
    - Backup & Storage
    - Disaster Recovery
    - Archive
    - Hybrid Cloud Storage
    - Application Hosting
    - Media Hosting
    - Data Lakes & Big Data Analytics
    - Software Delivery & Static Websites

### Buckets

- S3 stores Objects (files) in Buckets (directories)
- Buckets must have *globally unique name* (across all regions all accounts)
- Buckets are defined at region level
- looks like global service, but its a regional service
- Name Convention
    - No uppercase, No underscore
    - 3-63 characters long
    - Not an IP
    - Must start with lowercase letter or number
    - Must NOT start with prefix `xn--`
    - Must NOT end with suffix `-s3alias`

### Objects

- Objects (files) have a Key
- The *key* is FULL path:
    - `s3://my-bucket/my_file.txt
    - `s3://my-bucket/dir1/my_file.txt`
- The *key* is composed of *prefix + object_name*
- Keys are long names consisting of `/`
- Max Object Size is 5 TB
- If uploading more than 5GB, must use *muti-part upload*
- Metadata
- Tags
- Version ID

### AWS S3 - Security

- User Based
    - IAM Policies - which API calls should be allowed for a specific user from IAM
- Resource Based
    - Bucket Policies - bucket wide rules from S3 console - allows cross account
    - Object Access Control List (ACL) - finer grain (can be disabled)
    - Bucket Access Control List - less common (can be disabled)
- Note: an IAM principal can access an S3 object if
    - The user IAM permissions ALLOW it OR the resource policy ALLOWS it
    - AND there is no explicit DENY
- Encryption : encrypt objects in Amazon S3 using encryption keys

### Bucket Policy

![](assets/Pasted%20image%2020251105114132.png)

- JSON based Policies
    - Resource : buckets & Objects
    - Effect: Allow/Deny
    - Action : set of API to allow or deny
    - Principal: The account or user to apply policy to
- Use S3 bucket for policy to
    - Grant public access to bucket
    - Force objects to be encrypted at upload
    - Grant Access to another account (Cross-Account)

- Bucket Settings for Block Public Access to avoid data leaks
### Versioning

- You can version your files in Amazon S3
- It is enabled at the bucket level
- Same key overwrite will change the `version` : 1, 2, 3...
- Advantages of Versioning
    - Protection against unintended deletes
    - Easy roll back to previous version
- NOTE:
    - files existing before versioning is enabled will have a *null* previous version
    - previous versions are not deleted if versioning is turned off

### Replication

- *Must enable Versioning* in source & Destination
- Types
    - Cross-Region Replication (CRR)
    - Same-Region Replication (SRR)
- Buckets can be in different AWS Account
- Copy is asynchronous
- Must give proper IAM permissions to S3
- Use Cases
    - CRR – compliance, lower latency access, replication across accounts
    - SRR – log aggregation, live replication between production and test accounts
- NOTE: Only new objects added after enabling replication will be replicated
- Optionally, existing objects can be replicated using *S3 Batch Replication*
- For delete operations
    - can replicate delete markers from source to target
    - Deletions with a version id are not replicated (to avoid malicious deletes)
- There is no *chaining* of replication
    - If bucket 1 has replication into bucket 2, which has replication into bucket 3
    - Then objects created in bucket 1 are not replicated to bucket 3

## S3 Storage Classes

- Amazon S3 Standard - General Purpose
- Amazon S3 Standard-Infrequent Access (IA)
- Amazon S3 One Zone-Infrequent Access
- Amazon S3 Glacier Instant Retrieval
- Amazon S3 Glacier Flexible Retrieval
- Amazon S3 Glacier Deep Archive
- Amazon S3 Intelligent Tiering

### S3 Durability & Availability

- Durability:
    - High durability (99.999999999%, 11 9’s) of objects across multiple AZ
    - If you store 10,000,000 objects with Amazon S3, you can on average expect to incur a loss of a single object once every 10,000 years
    - Same for all storage classes
- Availability:
    - Measures how readily available a service is
    - Varies depending on storage class
    - Example: S3 standard has 99.99% availability = not available 53 minutes a year

### S3 Standard - General Purpose

- 99.99% Availability
- Used for frequently accessed data
- Low latency and high throughput
- Sustain 2 concurrent facility failures
- Use Cases: Big Data analytics, mobile & gaming applications, content distribution…

### S3 Storage Classes - Infrequent Access

- For data that is less frequently accessed, but requires rapid access when needed
- Lower cost than S3 Standard
- Amazon S3 Standard-Infrequent Access (S3 Standard-IA)
    - 99.9% Availability
    - Use cases: Disaster Recovery, backups
- Amazon S3 One Zone-Infrequent Access (S3 One Zone-IA)
    - High durability (99.999999999%) in a single AZ; data lost when AZ is destroyed
    - 99.5% Availability
    - Use Cases: Storing secondary backup copies of on-premises data, or data you can recreate

### Amazon S3 Glacier Storage Classes

- Low-cost object storage meant for archiving / backup
- Pricing: price for storage + object retrieval cost
- Amazon S3 Glacier Instant Retrieval
    - Millisecond retrieval, great for data accessed once a quarter
    - Minimum storage duration of 90 days
- Amazon S3 Glacier Flexible Retrieval (formerly Amazon S3 Glacier):
    - Expedited (1 to 5 minutes), Standard (3 to 5 hours), Bulk (5 to 12 hours) – free
    - Minimum storage duration of 90 days
- Amazon S3 Glacier Deep Archive – for long term storage:
    - Standard (12 hours), Bulk (48 hours)
    - Minimum storage duration of 180 days

### S3 Intelligent-Tiering

- Small monthly monitoring and auto-tiering fee
- Moves objects automatically between Access Tiers based on usage
- There are no retrieval charges in S3 Intelligent-Tiering

- Frequent Access tier (automatic): default tier
- Infrequent Access tier (automatic): objects not accessed for 30 days
- Archive Instant Access tier (automatic): objects not accessed for 90 days
- Archive Access tier (optional): configurable from 90 days to 700+ days
- Deep Archive Access tier (optional): config. from 180 days to 700+ days
### Express One Zone

- High performance, *single Availability Zone* storage class
- Objects stored in a *Directory Bucket (bucket in a single AZ)*
- Handle 100,000s requests per second with *single-digit millisecond* latency
- Up to 10x better performance than S3 Standard (50% lower costs)
- High Durability (99.999999999%) and Availability (99.95%)
- Co-locate your storage and compute resources in the same AZ (reduces latency)
- Use cases: latency-sensitive apps, data-intensive apps, AI & ML training, financial modeling, media processing, HPC…
- Best integrated with SageMaker Model Training, Athena, EMR, Glue

#### Moving between Storage Classes 

![](assets/Pasted%20image%2020251105115459.png)

- You can transition objects between storage classes
- For infrequently accessed object, move them to Standard IA
- For archive objects that you don’t need fast access to, move them to Glacier or Glacier Deep Archive
- Moving objects can be automated using a Lifecycle Rules

### Lifecycle Rules

- Transition Actions - configure objects to transition to another storage class
    - Move objects to Standard IA class 60 days after creation
    - Move to Glacier for archiving after 6 months
- Expiration actions – configure objects to expire (delete) after some time
    - Access log files can be set to delete after a 365 days
    - Can be used to delete old versions of files (if versioning is enabled)
    - Can be used to delete incomplete Multi-Part uploads
- Rules can be created for a certain prefix (example: `s3://mybucket/mp3/*`)
- Rules can be created for certain objects Tags (example: Department: Finance)


### Amazon S3 Analytics - Storage Class Analysis

![](assets/Pasted%20image%2020251105115852.png)

- Help you decide when to transition objects to the right storage class
- Recommendations for Standard and Standard IA
- Does NOT work for One-Zone IA or Glacier
- Report is updated daily
- 24 to 48 hours to start seeing data analysis
- Good first step to put together Lifecycle Rules (or improve them)!

### Event Notification

![](assets/Pasted%20image%2020251105120004.png)

- S3:ObjectCreated, S3:ObjectRemoved, S3:ObjectRestore, S3:Replication…
- Object name filtering possible (`*.jpg)`
- Use case: generate thumbnails of images uploaded to S3
- Can create as many “S3 events” as desired
- S3 event notifications typically deliver events in seconds but can sometimes take a minute or longer

![](assets/Pasted%20image%2020251105120047.png)

#### S3 Event Notification with Amazon EventBridge

![](assets/Pasted%20image%2020251105120118.png)

- Advanced filtering options with JSON rules (metadata, object size, name...)
- Multiple Destinations – ex Step Functions, Kinesis Streams / Firehose…
- EventBridge Capabilities – Archive, Replay Events, Reliable delivery

## S3 Performance

### Baseline Performance

- Amazon S3 automatically scales to high request rates, latency 100-200 ms
- Your application can achieve at least 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second per prefix in a bucket.
- There are no limits to the number of prefixes in a bucket.
- Example (object path => prefix):
    - bucket/folder1/sub1/file => /folder1/sub1/
    - bucket/folder1/sub2/file => /folder1/sub2/
    - bucket/1/file => /1/
    - bucket/2/file => /2/
- If you spread reads across all four prefixes evenly, you can achieve 22,000 requests per second for GET and HEAD

### Performance

- Multi-Part upload
    - recommended for files > 100MB, must use for files > 5GB
    - Can help parallelize uploads (speed up transfers)

![](assets/Pasted%20image%2020251105120514.png)

- S3 Transfer Acceleration
    - Increase transfer speed by transferring file to an AWS edge location which will forward the data to the S3 bucket in the target region
    - Compatible with multi-part upload

![](assets/Pasted%20image%2020251105120502.png)

### S3 Byte-Range Fetches

![](assets/Pasted%20image%2020251105120916.png)

- Parallelize GETs by request specific bytes ranges
- Better resilience in case of failure

## S3 Encryption

- You can encrypt objects in S3 buckets using one of 4 methods
- Server-Side Encryption (SSE)
    - Server-Side Encryption with Amazon S3-Managed Keys (SSE-S3) – Enabled by Default
    - Server-Side Encryption with KMS Keys stored in AWS KMS (SSE-KMS)
    - Server-Side Encryption with Customer-Provided Keys (SSE-C)
- Client-Side Encryption

### SSE - S3

![](assets/Pasted%20image%2020251106114951.png)

- Encryption using keys handled, managed, and owned by AWS
- Object is encrypted server-sice
- Encryption type is AES-256
- Must set header *"x-amz-server-side-encryption":"AES256"* 
- Enabled by default for new buckets & objects

### SSE - KMS

![](assets/Pasted%20image%2020251106115006.png)

- Encryption using keys handled and managed by AWS KMS (Key Management Service)
- KMS advantages: user control + audit key usage using Cloud Trail
- Object is encrypted server side
- Must set header `"x-amz-server-side-encryption": "aws:kms"`
- Limitations of using KMS
    - impact of KMS limits
    - When objects are uploaded, *GenerateDataKey* KMS API is called
    - When object are downloaded, *Decrypt* KMS API is called
    - counts towards KMS quota/seconds (can be increased)
### SSE-C

![](assets/Pasted%20image%2020251106115235.png)

- Server-Side Encryption using keys fully managed by the customer outside of AWS
- Amazon S3 does NOT store the encryption key you provide
- HTTPS must be used
- Encryption key must provided in HTTP headers, for every HTTP request made

### CSE

![](assets/Pasted%20image%2020251106115304.png)

- Use client libraries such as Amazon S3 Client-Side Encryption Library
- Clients must encrypt data themselves before sending to Amazon S3
- Clients must decrypt data themselves when retrieving from Amazon S3
- Customer fully manages the keys and encryption cycle

### Encryption in transit (SSL/TLS)

- Encryption in flight is also called SSL/TLS
- Amazon S3 exposes two endpoints:
    - HTTP Endpoint – non encrypted
    - HTTPS Endpoint – encryption in flight
- HTTPS is recommended
- HTTPS is mandatory for SSE-C
- Most clients would use the HTTPS endpoint by default

## More on S3

### Access Points

![](assets/Pasted%20image%2020251105121035.png)

- Access Points simplify security management for S3 Buckets
- Each Access Point has:
    - its own DNS name (Internet Origin or VPC Origin)
    - an access point policy (similar to bucket policy) – manage security at scale
- We can define the access point to be accessible only from within the VPC
- You must create a VPC Endpoint to access the Access Point (Gateway or Interface Endpoint)
- The VPC Endpoint Policy must allow access to the target bucket and Access Point

![](assets/Pasted%20image%2020251105121135.png)

### Object Lambda

![](assets/Pasted%20image%2020251105121233.png)

- Use AWS Lambda Functions to change the object before it is retrieved by the caller application
- Only one S3 bucket is needed, on top of which we create S3 Access Point and S3 Object Lambda Access Points.
- Use Cases:
    - Redacting personally identifiable information for analytics or non- production environments.
    - Converting across data formats, such as converting XML to JSON.
    - Resizing and watermarking images on the fly using caller- specific details, such as the user who requested the object.

## Amazon S3: Storage Lens

### Metrics

- Summary Metrices
- Cost-Optimization Metrics
- Data Protection Metrics
- Access-management Metrics
- Event Metrics
- Performance Metrics
- Activity Metrics
- Detailed Status Code Metrics

### Free vs Paid

- Free
    - Automatically available for all customers
    - Contains around 28 usage metrics
    - Data is available for queries for 14 days
- Advanced Metrics & Recommendations
    - Additional paid metrics and features
    - Advanced Metrics – Activity, Advanced Cost Optimization, Advanced Data Protection, Status Code
    - CloudWatch Publishing – Access metrics in CloudWatch without additional charges
    - Prefix Aggregation – Collect metrics at the prefix level
    - Data is available for queries for 15 months
## EBS

- An EBS (Elastic Block Store) Volume is a network drive you can attach to your instances while they run
- It allows your instances to persist data, even after their termination
- *They can only be mounted to one instance at a time (at the CCP level)*
- They are bound to a *specific availability zone*


- It’s a network drive (i.e. not a physical drive)
    - It uses the network to communicate the instance, which means there might be a bit of latency
    - It can be detached from an EC2 instance and attached to another one quickly
- It’s locked to an Availability Zone (AZ)
    - An EBS Volume in us-east-1a cannot be attached to us-east-1b
    - To move a volume across, you first need to snapshot it
- Have a provisioned capacity (size in GBs, and IOPS)
    - You get billed for all the provisioned capacity
    - You can increase the capacity of the drive over time

![](assets/Pasted%20image%2020251106115742.png)

### EBS - Delete on Termination Attribute

- Controls the EBS behaviour when an EC2 instance terminates
    - By default, the root EBS volume is deleted (attribute enabled)
    - By default, any other attached EBS volume is not deleted (attribute disabled)
- This can be controlled by the AWS console / AWS CLI
- Use case: preserve root volume when instance is terminated

### EBS Elastic Volume

- You don’t have to detach a volume or restart your instance to change it!
    - Just go to actions / modify volume from the console
- Increase volume size
    - You can only increase, not decrease
- Change volume type
    - Gp2 -> Gp3
    - Specify desired IOPS or throughput performance (or it will guess)
- Adjust performance
    - Increase or decrease

## EFS

![](assets/Pasted%20image%2020251106120834.png)

- Managed NFS (network file system) that can be mounted on many EC2
- EFS works with EC2 instances in multi-AZ
- Highly available, scalable, expensive (3x gp2), pay per use
- Use cases: content management, web serving, data sharing,\ Wordpress
- Uses NFSv4.1 protocol
- Uses security group to control access to EFS
- Compatible with Linux based AMI (not Windows)
- Encryption at rest using KMS
- POSIX file system (~Linux) that has a standard file API
- File system scales automatically, pay-per-use, no capacity planning!

### Performance & Storage Classes

- EFS Scale
    - 1000s of concurrent NFS clients, 10 GB+ /s throughput
    - Grow to Petabyte-scale network file system, automatically
- Performance Mode (set at EFS creation time)
    - General Purpose (default) – latency-sensitive use cases (web server, CMS, etc…)
    - Max I/O – higher latency, throughput, highly parallel (big data, media processing
- Throughput Mode
    - Bursting – 1 TB = 50MiB/s + burst of up to 100MiB/s
    - Provisioned – set your throughput regardless of storage size, ex: 1 GiB/s for 1 TB storage
    - Elastic – automatically scales throughput up or down based on your workloads
        - Up to 3GiB/s for reads and 1GiB/s for writes
        - Used for unpredictable workloads
- Storage Tiers (lifecycle management feature – move file after N days)
    - Standard: for frequently accessed files
    - Infrequent access (EFS-IA): cost to retrieve files, lower price to store.
    - Archive: rarely accessed data (few times each year), 50% cheaper
    - Implement lifecycle policies to move files between storage tiers
- Availability and durability
    - Standard: Multi-AZ, great for prod
    - One Zone: One AZ, great for dev, backup enabled by default, compatible with IA (EFS One Zone-IA)

## EFS vs EBS

![](assets/Pasted%20image%2020251106120058.png)


- EBS Volumes
    - one instance (except multi-attach io1/io2)
    - are locked at AZ level
    - gp2: IO increases if the disk size increases
    - gp3 & io1 : can increase IO independently
- To migrate an EBS Volume across AZ
    - Take snapshot
    - restore snapshot to another AZ
- Root EBS Volumes of instances get terminated by default if the EC2 instance gets terminated. (you can disable that) 

![](assets/Pasted%20image%2020251106120112.png)
- EFS Volumes
    - Mounting 100s of instances across AZ
    - EFS share website files (WordPress)
    - Only for Linux Instances (POSIX)
    - EFS has a higher price point than EBS
    - Can leverage Storage Tiers for cost saving
    - Remember: EFS vs EBS vs Instance Store
## AWS Backup

- Fully managed service
- Centrally manage and automate backups across AWS services
- No need to create custom scripts and manual processes
- Supported services:
    - Amazon EC2 / Amazon EBS
    - Amazon S3
    - Amazon RDS (all DBs engines) / Amazon Aurora / Amazon DynamoDB
    - Amazon DocumentDB / Amazon Neptune
    - Amazon EFS / Amazon FSx (Lustre & Windows File Server)
    - AWS Storage Gateway (Volume Gateway)
- Supports cross-region backups
- Supports cross-account backups
- Supports PITR for supported services
- On-Demand and Scheduled backups
- Tag-based backup policies
- You create backup policies known as Backup Plans
    - Backup frequency (every 12 hours, daily, weekly, monthly, cron expression)
    - Backup window
    - Transition to Cold Storage (Never, Days, Weeks, Months, Years)
    - Retention Period (Always, Days, Weeks, Months, Years)

![](assets/Pasted%20image%2020251106120536.png)

### AWS Backup Vault Lock

- Enforce a WORM (Write Once Read Many) state for all the backups that you store in your AWS Backup Vault
- Additional layer of defense to protect your backups against:
- Inadvertent or malicious delete operations
- Updates that shorten or alter retention periods
- Even the root user cannot delete backups when enabled