# Security, Identify, and Compliance

## Principle of Least Privilege

- Grant only the permissions required to perform a task
- Start with broad permissions while developing
- But lock it down once you have a better idea of the exact services and operations a workload requires
- Can use IAM Access Analyzer to generate least-privilege policies based on access activity
## Data Masking

- Dealing with PII or other sensitive data
- Masking obfuscates data
    - For example, masking all but the last 4 digits of a credit card or social security number
    - Masking passwords
    - Supported in Glue DataBrew and Redshift
- Anonymization Techniques
    - Replace with Random
    - Shuffle
    - Encrypt
    - Hashing
- Or just delete it or don't import it in the first place

## Key Salting

- Salting involves appending or prepending a random value, known as a "salt," to a piece of data (often a password) before hashing it.
- Prevents pre-computed "rainbow table" attacks where adversaries use pre-generated hashes of commonly used passwords to find matches.
- Ensures that the same piece of data (like two identical passwords) doesn't produce the same hash across different instances due to the unique salt.
- Use strong, cryptographically secure random values for salts
- Rotate salts periodically
- Each user should have a unique salt
- Salt and hash passwords before storing

![](assets/Pasted%20image%2020251112230858.png)
## Key Scaling



## Preventing Backups or Replication to Disallowed AWS Regions

## IAM Introduction: Users, Groups, Policies

![](assets/Pasted%20image%2020251112230952.png)

- IAM = Identity and Access Management, Global service
- Root account created by default, shouldn’t be used or shared
- Users are people within your organization, and can be grouped
- Groups only contain users, not other groups
- Users don’t have to belong to a group, and user can belong to multiple groups

### IAM: Permissions

![](assets/Pasted%20image%2020251112231104.png)

- Users or Groups can be assigned JSON documents called policies
- These policies define the permissions of the users
- In AWS you apply the least privilege principle: don’t give more permissions than a user needs

### IAM Policies Inheritance

![](assets/Pasted%20image%2020251112231134.png)

### IAM Policies Structure

- Consists of
    - Version: policy language version, always include “2012-10-17”
    - Id: an identifier for the policy (optional)
    - Statement: one or more individual statements (required)
- Statements consists of
    - Sid: an identifier for the statement (optional)
    - Effect: whether the statement allows or denies access (Allow, Deny)
    - Principal: account/user/role to which this policy applied to
    - Action: list of actions this policy allows or denies
    - Resource: list of resources to which the actions applied to
    - Condition: conditions for when this policy is in effect (optional)
### IAM - Password Policy

- Strong passwords = higher security for your account
- In AWS, you can setup a password policy:
    - Set a minimum password length
    - Require specific character types:
        - including uppercase letters
        - lowercase letters
        - numbers
        - non-alphanumeric characters
    - Allow all IAM users to change their own passwords
    - Require users to change their password after some time (password expiration)
    - Prevent password re-use
## IAM MFA

- Users have access to your account and can possibly change configurations or delete resources in your AWS account
- You want to protect your Root Accounts and IAM users MFA = password you know + security device you own
- MFA devices options in AWS
    - Virtual MFA ~ Authenticator
    - Universal 2nd Factor (U2F) ~ Security Key (YubiKey)
    - Hardware Key Fob MFA Device ~ Gemalto (3rd party)
    - Hardware Key Fob MFA Device for AWS GovCloud (US) ~ provided by Sure PassID

## IAM Roles

![](assets/Pasted%20image%2020251112234911.png)
- Some AWS service will need to perform actions on your behalf
- To do so, we will assign permissions to AWS services with IAM Roles
- Common roles:
    - EC2 Instance Roles
    - Lambda Function Roles
    - Roles for CloudFormation
## AWS Macie

![](assets/Pasted%20image%2020251112231843.png)

- Amazon Macie is a fully managed data security and data privacy service that uses machine learning and pattern matching to discover and protect your sensitive data in AWS.
- Macie helps identify and alert you to sensitive data, such as personally identifiable information (PII)

## AWS Secrets Manager

- Newer service, meant for storing secrets
- capability to force rotation of secret every X days
- Automated generation of secrets on rotation (uses Lambda)
- Integration with Amazon RDS (My SQL, PostgresSQL, Aurora)
- Secrets are encrypted using KMS
- Mostly meant for RDS integration
- Replicate Secrets across multiple AWS Regions
- Secret Manager keeps read replicas in sync with the primary Secret
- Ability to promote a read replica Secret to a standalone Secret
- Uses Cases : multi-region DB

![](assets/Pasted%20image%2020251112232337.png)
## WAF

- protects your web application from common web exploits (Layer 7)
- Layer 7 is HTTP (Application Layer)
- Deploy
    - ALB
    - APIGW
    - CloudFront
    - AppSync GraphQL API
    - Cognito User Pool
- doesn't support NLB
- We can use Global Accelerator for fixed IP and WAF on the ALB
- Define Web ACL (Web Access Control List)
    - IP Set
    - HTTP headers, HTTP body, or URI Strings protects from common attacks
    - Size constraints, geo-match (block countries)
    - Rate-based rules for DDoS protection

![](assets/Pasted%20image%2020251112232723.png)
## Shield

- DDoS protection
- Two plans
    - Standard
        - Free service for every AWS customers
        - Support from Basic attacks such as SYN/UDP Floods, Reflection Attack and other layer 3/layer 4 attacks
    - Shield Advanced
        - Dedicated service support from AWS
        - Paid Subscription
        - More sophistication attach preventions

## Security - Kinesis

- Kinesis Data Streams
    - SSL endpoints using the HTTPS protocol to do encryption in flight
    - AWS KMS provides server-side encryption [Encryption at rest]
    - For client side-encryption, you must use your own encryption libraries
    - Supported Interface VPC Endpoints / Private Link – access privately
    - KCL – must get read / write access to DynamoDB table
- Kinesis Data Firehose:
    - Attach IAM roles so it can deliver to S3 / ES / Redshift / Splunk
    - Can encrypt the delivery stream with KMS [Server side encryption]
    - Supported Interface VPC Endpoints / Private Link – access privately
- Kinesis Data Analytics
- Attach IAM role so it can read from Kinesis Data Streams and reference sources and write to an output destination (example Kinesis Data Firehose)

## Security - SQS

- Encryption in flight using the HTTPS endpoint
- Server Side Encryption using KMS
- IAM policy must allow usage of SQS
- SQS queue access policy
- Client-side encryption must be implemented manually
- VPC Endpoint is provided through an Interface
## Security - AWS IoT

- AWS IoT policies:
    - Attached to X.509 certificates or Cognito Identities
    - Able to revoke any device at any time
    - IoT Policies are JSON documents
    - Can be attached to groups instead of individual Things.
- IAM Policies:
    - Attached to users, group or roles
    - Used for controlling IoT AWS APIs
- Attach roles to Rules Engine so they can perform their actions

## Security - Amazon S3

- IAM policies
- S3 bucket policies
- Access Control Lists (ACLs)
- Encryption in flight using HTTPS
- Encryption at rest
    - Server-side encryption: SSE-S3, SSE-KMS, SSE-C
    - Client-side encryption – such as Amazon S3 Encryption Client
- Versioning + MFA Delete
- CORS for protecting websites
- VPC Endpoint is provided through a GatewayGlacier – vault lock policies to prevent deletes (WORM)

## Security - DynamoDB

- Data is encrypted in transit using TLS (HTTPS)
- DynamoDB tables are encrypted at rest
    - KMS encryption for base tables and secondary indexes
    - AWS owned key (default)
    - AWS managed key (aws/dynamodb)
    - AWS customer managed key (your own)
- Access to tables / API / DAX using IAM
- DynamoDB Streams are encrypted
- VPC Endpoint is provided through a Gateway

## Security - RDS

- VPC provides network isolation
- Security Groups control network access to DB Instances
- KMS provides encryption at rest
- SSL provides encryption in-flight
- IAM policies provide protection for the RDS API
- IAM authentication is supported by PostgreSQL, MySQL and MariaDB
- Must manage user permissions within the database itself
- MSSQL Server and Oracle support TDE (Transparent Data Encryption)
## Security - Aurora

- VPC provides network isolation
- Security Groups control network access to DB Instances
- KMS provides encryption at rest
- SSL provides encryption in-flight
- IAM authentication is supported by PostgreSQL and MySQL
- Must manage user permissions within the database itself

## Security - Lambda

- IAM roles attached to each Lambda function
- Sources
- Targets
- KMS encryption for secrets
- SSM parameter store for configurations
- CloudWatch Logs
- Deploy in VPC to access private resources

## Security - Glue

- IAM policies for the Glue service
- Configure Glue to only access JDBC through SSL
- Data Catalog: Encrypted by KMS
- Connection passwords: Encrypted by KMS
- Data written by AWS Glue – Security Configurations:
    - S3 encryption mode: SSE-S3 or SSE-KMS
    - CloudWatch encryption mode
    - Job bookmark encryption mode

## Security - EMR

- Using Amazon EC2 key pair for SSH credential
- Attach IAM roles to EC2 instances for:
    - proper S3 access
    - for EMRFS requests to S3
    - DynamoDB scans through Hive
- EC2 Security Groups
    - One for master node
    - Another one for cluster node (core node or task node)
- Encrypts data at-rest: EBS encryption, Open Source HDFS Encryption, LUKS + EMRFS for S3
- In-transit encryption: node to node communication, EMRFS, TLS
- Data is encrypted before uploading to S3
- Kerberos authentication (provide authentication from Active Directory)
- Apache Ranger: Centralized Authorization (RBAC – Role Based Access) – setup on external EC2

## Security - OpenSearch Service

- Amazon VPC provides network isolation
- OpenSearch policy to manage security further
- Data security by encrypting data at-rest using KMS
- Encryption in-transit using HTTPS (TLS)
- IAM or Cognito based authentication
- Amazon Cognito allow end-users to log-in to OpenSearch Dashboards through enterprise identity providers such as Microsoft Active Directory using SAML

## Security - Redshift

- VPC provides network isolation
- Cluster security groups
- Encryption in flight using the JDBC driver enabled with SSL
- Encryption at rest using KMS or an HSM device (establish a connection)
- Supports S3 SSE using default managed key
- Use IAM Roles for Redshift
- To access other AWS Resources (example S3 or KMS)
- Must be referenced in the COPY or UNLOAD command (alternatively paste access key and secret key creds)

## Security - Athena

- IAM policies to control access to the service
- Data is in S3: IAM policies, bucket policies & ACLs
- Encryption of data according to S3 standards: SSE-S3, SSE- KMS, CSE-KMS
- Encryption in transit using TLS between Athena and S3 and JDBC
- Fine grained access using the AWS Glue Catalog

## Security - QuickSight

- Standard edition:
    - IAM users
    - Email based accounts
- Enterprise edition:
    - Active Directory
    - Federated Login
    - Supports MFA (Multi Factor Authentication)
    - Encryption at rest and in SPICE
- Row Level Security to control which users can see which rows
- Column Level Security to restrict access to specific columns in dataset