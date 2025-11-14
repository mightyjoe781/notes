# AWS Networking Management & Governance

## Amazon VPC IP Address Manager (IPAM)

- IPAM
    - Scope (public or private)
        - pools
            - sub-pools
                - VPCs
- AWS account level
- AWS organization level

### IPAM Pools

![](assets/Pasted%20image%2020251030231647.png)
![](assets/Pasted%20image%2020251030231700.png)
![](assets/Pasted%20image%2020251030231722.png)

### IPAM with AWS Organization

![](assets/Pasted%20image%2020251030231820.png)

- Amazon VPC IPAM can be integrated with your organization's structure
- Create an IPAM-administrator account for your Organization
- This account must be a member of the Organization
- AWS Organization Service control policy (SCP) to enforce CIDR allocation through IPAM while creating VPCs
- Enforce using specific IPAM pools
- Enforce specific IPAM pools to specific OUs

### Apply rules for IP allocation

![](assets/Pasted%20image%2020251030232001.png)
![](assets/Pasted%20image%2020251030232013.png)
![](assets/Pasted%20image%2020251030232026.png)
![](assets/Pasted%20image%2020251030232041.png)

### IPAM integration with AWS tools
![](assets/Pasted%20image%2020251030232143.png)

### IPAM Pools - Quick Walkthrough

![](assets/Pasted%20image%2020251030232118.png)
### Tracking & Monitoring IP addresses with IPAM

- Monitor CIDR usage with IPAM Dashboard
- Monitor CIDR usage by resource
- Monitor IPAM with Amazon CloudWatch
- View IP address history
- View public IP insights
## AWS CloudFormation

### Infrastructure as a Code

- If you have been doing a lot of manual work for deployment of the infrastructure in AWS e.g. creating VPC, Subnets, EC2 instances, VPN connection etc. …
- All this manual work will be very tough to reproduce:
- In another region
- in another AWS account
- Within the same region if everything was deleted
- Wouldn’t it be great, if all our infrastructure was… code?
- CloudFormation is a declarative way of outlining your AWS Infrastructure, for any resources (most of them are supported).
    - I want a VPC and Subnets
    - I want an internet gateway and attach it to the VPC
    - I want a security group
    - I want two EC2 machines using this security group in the subnet just created
- Then CloudFormation creates those for you, in the right order, with the exact configuration that you specify

### Benefits of AWS CloudFormation

- IaC
- Cost
- Productivity
- Separation of concern
- Don't re-invent the wheel

![](assets/Pasted%20image%2020251030233356.png)

### CloudFormation - Feature & Components

- CloudFormation Designer
- ChangeSets
    - generate & preview the changes before applying
- StackSets
    - deploy a CloudFormation stack across multiple account & region
- Stack Policies
- Cross Stacks
- Nest Stacks

### Managing Resource Dependencies

- Depends On
- Wait Condition
### AWS Cloud Development Kit (CDK)

- An open-source software development framework to define your cloud application resources using familiar programming languages.
![](assets/Pasted%20image%2020251030233431.png)

## AWS Service Catalog

- Allows users to launch group of approved IT resources as a Product in a self-service manner
- It uses Cloud Formation templates to launch the related resources/architecture/software/servers.
- Products can be versioned and can be shared across AWS organization, Organization Units (OU) or AWS accounts
- It uses user's IAM permissions or a launch constraint for launching the products
- Users can optionally provide the parameter
- Administrator can also provide details like support email.
- Output of CloudFormation can also be part of the launch output e.g. Website URL etc.

![](assets/Pasted%20image%2020251030230945.png)

- user browse the products listed in AWS Service Catalog
- User selects the product
- User launches the product

## AWS Config

Assess, Audit and Evaluate the configuration of your AWS resources

![](assets/Pasted%20image%2020251030231120.png)

Auto remediation using Systems Manager SSM documents

![](assets/Pasted%20image%2020251030231153.png)

- View compliance of a resource over time
- View configuration of a resource over time
- View CloudTrail API calls if enabled

### Summary

- AWS Config Rule does not prevent actions from happening (no deny)
- Questions that can be solved by AWS Config:
    - Is there unrestricted SSH access to my security groups?
    - Do my buckets have any public access?
    - How my ALB configuration has changed over time?
- Can make custom config rules (must be defined in AWS Lambda)
    - Example 1: Evaluate if each EBS disk is of type gp2
    - Example 2: Evaluate if each EC2 instance is t2.micro
- AWS Config is a regional service however can aggregate data across multiple regions and accounts

## AWS CloudTrail

- Provides audit for your AWS Account activities by logging all the API calls
- CloudTrail is enabled by default!
- Get an history of events / API calls made within your AWS Account by:
    - Console
    - SDK
    - CLI
    - AWS Services
- If a resource is deleted in AWS, look into CloudTrail first!
- CloudTrail console shows the past 90 days of activity. Optionally, you can persist the CloudTrail logs into CloudWatch or S3
- Can be region specific or global & include global events (e.g. IAM)

![](assets/Pasted%20image%2020251030231436.png)