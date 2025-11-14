# Containers

## Docker

- software development platform to deploy apps
- apps are packaged into *containers* that can be run on any OS
- Apps run the same regardless of where they run
- Use cases : microservices architecture, lift-and-shift apps from on-prem to AWS

![](assets/Pasted%20image%2020251109115040.png)

- Docker images are stored in Docker Repository 
    - E.g. Dockerhub (Public)
    - Amazon ECR
        - Private Repository
        - Public Repository (Amazon ECR Public Gallary)
- Difference between Docker and VM is that Resources are shared with host in case of Docker

![](assets/Pasted%20image%2020251109115227.png)

### Docker Containers Management on AWS

- Amazon ECS (Elastic Container Service) ~ AWS own container platform
- Amazon EKS ~ Amazon's managed Kubernetes
- AWS Fargate
    - Amazon's own Serverless Container Platform
    - Works with ECS, EKS
- Amazon ECR ~ container repository

## ECS

### ECS - EC2 Launch Type

![](assets/Pasted%20image%2020251109115910.png)

- ECS = Elastic Container Service
- Launch Docker containers on AWS = Launch ECS Tasks on ECS Clusters
- EC2 Launch Type: you must provision & maintain the infrastructure (the EC2 instances)
- Each EC2 Instance must run the ECS Agent to register in the ECS Cluster
- AWS takes care of starting / stopping containers

### ECS - Fargate Launch Type

![](assets/Pasted%20image%2020251109115929.png)

- Launch Docker containers on AWS
- You do not provision the infrastructure (no EC2 instances to manage)
- It’s all Serverless!
- You just create task definitions
- AWS just runs ECS Tasks for you based on the CPU / RAM you need
- To scale, just increase the number of tasks. Simple - no more EC2 instances

### ECS - IAM Roles for EC2

![](assets/Pasted%20image%2020251109120254.png)

- **EC2 Instance Profile (EC2 Launch Type only)**:
    - Used by the ECS agent
    - Makes API calls to ECS service
    - Send container logs to CloudWatch Logs
    - Pull Docker image from ECR
    - Reference sensitive data in Secrets Manager or SSM Parameter Store
- **ECS Task Role**:
    - Allows each task to have a specific role
    - Use different roles for the different ECS Services you run
    - Task Role is defined in the task definition

### ECS - Load Balancer Integrations

ECS supports 

- ALB
- NLB
- CLB (not recommended)
### ECS Data Volumes

- Mount EFS file systems onto ECS tasks
- Works for both EC2 and Fargate launch types
- Tasks running in any AZ will share the same data in the EFS file system
- Fargate + EFS = Serverless
- Use cases: persistent multi-AZ shared storage for your containers
- Note:
    - Amazon S3 cannot be mounted as a file system

## ECR

![](assets/Pasted%20image%2020251109115641.png)

- ECR = Elastic Container Registry
- Store and manage Docker images on AWS
- Private and Public repository (Amazon ECR Public Gallery https://gallery.ecr.aws)
- Fully integrated with ECS, backed by Amazon S3
- Access is controlled through IAM (permission errors => policy)
- Supports image vulnerability scanning, versioning, image tags, image lifecycle, …

## EKS

- Amazon EKS = Amazon Elastic Kubernetes Service
- It is a way to launch managed Kubernetes clusters on AWS
- Kubernetes is an open-source system for automatic deployment, scaling and management of containerized (usually Docker) application
- It’s an alternative to ECS, similar goal but different API
- EKS supports EC2 if you want to deploy worker nodes or Fargate to deploy serverless containers
- Use case: if your company is already using Kubernetes on-premises or in another cloud, and wants to migrate to AWS using Kubernetes
- Kubernetes is cloud-agnostic (can be used in any cloud – Azure, GCP…)
- For multiple regions, deploy one EKS cluster per region
- Collect logs and metrics using CloudWatch Container Insights

![](assets/Pasted%20image%2020251109115449.png)

### EKS Node Types

- Managed Node Groups
    - Creates and manages Nodes (EC2 instances) for you
    - Nodes are part of an ASG managed by EKS
    - Supports On-Demand or Spot Instances
- Self-Managed Nodes
    - Nodes created by you and registered to the EKS cluster and managed by an ASG
    - You can use prebuilt AMI - Amazon EKS Optimized AMI
    - Supports On-Demand or Spot Instances
- AWS Fargate
    - No maintenance required; no nodes managed

### AWS EKS - Data Volumes

- Need to specify StorageClass manifest on your EKS cluster
- Leverages a Container Storage Interface (CSI) compliant driver
- Support for…
    - Amazon EBS
    - Amazon EFS (works with Fargate)
    - Amazon FSx for Lustre
    - Amazon FSx for NetApp ONTAP