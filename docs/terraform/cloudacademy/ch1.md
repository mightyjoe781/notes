## Terraform 1.0 - Provisioning AWS Infrastructure

### IaC

- Infrastructure as Code


### Terraform Root Module

- Root Module : simply a directory on local filesystem containing Terraform Code + Configuration
- Terrafrom files : `*.tf` or `*.tfvars`
- Root Module typically contains
  - `main.tf`
  - `variables.tf`
  - `outputs.tf`
- May contain terraform state files
  - `terraform.tfstate`
  - `terraform.tfstate.backup`
- Other files
  - `.terraform`
  - `.terraform.lock.hcl`

### Terraform Workspaces

- way to manage multiple but different infrastructure environments using same set of terraform files.
- workspaces are managed using command: `terraform workspace <subcommand>`
- subcommands : `new, list, show, select and delete`
- create env for each separate environment e.g. dev, test and prod
- Workspace isolate and manage multiple copies of terraform state files : namely `tfstate` and `tfstate.backup` files

#### The Main File (`main.tf`)

- located in project root workspace
- contains your core terraform code
  - resources
  - provider
  - data sources
- complex infra requirements may be split across multiple `*.tf` files
- modularized templates will each have their own `main.tf`

Example

```hcl
# main.tf

resource "aws_instance" "compute1" {
	ami							= data.aws.ami.ubuntu.id
	instance_type		= var.instance_type
	key_name				= var.key_name
	subnet_id				= var.subnet_id
	security_groups = [var.sg_id]
	
	tags = {
		Name = "Cloudacadmey.Compute1"
	}
}
```

#### The Variables File (`variables.tf`)

- located alongside `main.tf`
- variables are referenced from within `main.tf`
- variables can be type and have defaults and can be overriden

Example

````
# variables.tf

variable "instance_type" {}
variable "key_name" {}
variable "vpc_id" {}

// explicit type defined
variable "asg_desired" {
	type = number
	default = 2
}
````

#### The Outputs File (`outputs.tf`)

- used to explicitly export values back out at the end of a `terraform apply` execution
- outputs can be referenced within any parent terraform template
- often used when creating modules : allows module values to be used within parent template
- module declared outputs accessed as : `module.<MODULE NAME>.<OUTPUT NAME>`

Example

````
# outputs.tf

output "vpc_id" {
	value = aws_vps.main.id
}

output "subnet1_id" {
	value = aws_subnet.subnet1.id
}
````



### Terraform State

- Terraform is stateful
- keeps track of all infra provisioned beyond day 0
- manage full lifecycle of your infrastructure
- manages infrastructure configuration drift and can be refreshed using `terraform refresh`
- terraform state tracked and recorded within the files : `terraform.tfstate` and `terraform.tfstate.backup`
- NOTE : terraform by default stores state on local filesystem but we can configure it to store state remotely
  - S3 backend
  - Remote state more secure
    - Data encrypted at rest
    - tls connections

### Terraform State - Locking

- state files locked during writes
- prevents potential conflict and corruptions
- consistency checks

````
# main.tf

terraform {
  backend "s3" {
    # S3 Remote State
    bucket = "cloudacademy-remote-state-s3"
    region = "us-west-2"
    key = "terraform. tfstate"
    encrypt = true
    
    # DynamoDB Locking Table
    dynamodb_table = "cloudacademy-dynamodb-locktable"
  }
}
````

### Terraform CLI AWS Authentication

- terraform IAM role with programmatic access
- AWS Credentials can be put (same order of preference)
  - in `main.tf` : fastest but worse method in terms of security
  - environment_variables : detected by `terraform cli`
  - shared credentials file : referenced in `main.tf` (`~/.aws/credentials`)

### Terraform CLI

- type `terraform -help`
- type `terrform init`
  - without any content in `main.tf`, above command will not do anything
  - add this code to main.tf

````
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.55.0"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

data "aws_availability_zones" "available" {
    state = "available"
}
````

- After this
  - type `terraform init`
  - it will initialize `backend` and then get plugins
  - create `lock file` and `.terraform` directory
- `terraform validate` just validates the syntax of tf files
- `terraform plan` : dry run command ( doesn’t actually create resources / more like an execution plan)
- `terraform apply` : reruns plan but this time actually creates resources
  - if fails in mid-way, doesn’t rerun or roll because plan is actually executed.
  - better to use git for that
- `terraform destroy` : removes all resources

### Terraform Language (HCL Syntax)

- HCL : Hashicorp Configuration Language (HCL)
- Comments :
  -  `# Single line`
  - `/* */ Multi-line`
- Interpolation `${var.varname}`
- JSON/YML
- TYPE : Boolean, String and Numbers, Map, List, Tuple
- provider version is optional
- `resource <type> <name>` : then to access : `smk_id = resource_type.resource_name`
- `data <type> <naem>` : then to access : `smk_id = data.data_type.data_name`
- `varible <varible_name>` : then to access : `smk_id = var.variable_name`
- module : an abstraction that can be used to combine related resources together for reusability purposes

### Terraform Exercises

https://github.com/cloudacademy/terraform-aws/
