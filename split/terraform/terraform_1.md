# Terraform Notes - Part 1
Generated on: 2025-06-01 14:11:13
Topic: terraform
This is part 1 of 1 parts

---

## File: terraform/cloudacademy/ch1.md

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


---

## File: terraform/index.md

### Terraform

Terraform is an open-source infrastructure-as-code software tool created by HashiCorp. Users define and provide data center infrastructure using a declarative configuration language known as HashiCorp Configuration Language (HCL), or optionally JSON.



Resources : 

- [Cloudacademy Notes](cloudacademy/ch1.md)
- [KDsouza’s Notes](kd/index.md) : Recommended for Terraform Certificates

---

## File: terraform/kd/index.md

### Notes for Terraform Certificates

Credits : Keerthi Dsouza, put up here based on permission from owner.

Github : [Link](https://github.com/KSD-26/Terraform)

Contents

- [Part - 1](part1.md)
- [Part - 2](part2.md)

---

## File: terraform/kd/part1.md

### 1. Introduction

Terraform is written in Golang.
Terraform uses graph theory to plot relationships between resources.

HCL - Hashicorp configuration language.

IaC tools:

- AWS :: Cloudformation
- Azure :: Resource Manager
- GCP :: Deployment Manager
- Terraform

<hr>

### 2. Files in Terraform


files:

- provider.tf :: A provider in Terraform is a connection that allows Terraform to manage infrastructure using predefined interface
- resources.tf :: define the resource - represent things in real world
- variables.tf :: dynamic values - value set at runtime
- data-source.tf :: used to fetch data from a resource that is not managed by terraform
- outputs.tf :: outputs from provisioning

<hr>

### 3. Terraform State

NOTE: terraform.tfstate :: state according to terraform

`Terraform state :: terraform.tfstate`

- record of all resources that it has created
- it stores in local file terraform.tfstate
- the file also stores dependency order of the resources that have been created

<hr>

### 4. Resources

- allows you to define what you want to create in real world

**Resource Block**

- describes one or more infrastructure objects
ex: virtual network, compute instances, dns record

- declares a resource of a:
    + given type "aws_instance"
    + given name "my_instance"

ex:

````
resource "aws_instance" "my_instance"{
    ami = "ami-1234qwerty"
    instance_type = "t2.micro"
}
````

where::
    1. resource type  = aws_instance
    2. local resource name = my_instance

3. argument name = ami, instance_type
4. argument value =  ami-1234qwerty,t2.micro

**Implicit dependency in Resource Block**

- Terraform will automatically manage Implicit dependency by find reference objects and creating an Implicit ordering

ex:

```
resource "aws_eip" "my_eip"{
	vpc = "true"
}
```

    resource "aws_instance" "my_instance"{
        ami = "ami-1234qwerty"
        instance_type = "t2.micro"
        public_ip = aws_eip.my_eip.private_ip
    }

**Explicit dependency in Resource Block**

- is only required when resource relies on another resource behavior

ex:

````
resource "aws_s3_bucket" "example"{
		acl = "private"
}
````

    resource "aws_instance" "my_instance"{
        instance_type = "t2.micro"
        depends_on = [aws_s3_bucket.example]
    }

-----------------------

### 5. Terraform workflow/lifecycle

1. terraform init :: Prepare your working directory for other command
2. terraform plan :: show changes required by the current configuration
3. terraform apply :: create, update, or delete infrastructure
4. terraform destroy ::  destroy previously created infrastructure

----------------------

### 6. Terraform debugging/troubleshooting

- enable logging in terraform with `TF_LOG` environment variable
- presist logging output with `TF_LOG_PATH`

Values:

- TF_LOG=TRACE :: Highest verbosity
- TF_LOG=DEBUG
- TF_LOG=INFO
- TF_LOG=WARN
- TF_LOG=ERROR :: lowest verbosity

ex:

- ​    export TF_LOG=TRACE
- ​    export TF_LOG_PATH=/logs/terraform.log


------------------------

### 7. Data Sources

- used to fetch data from a resource that is not managed by terraform 
- allows data to be fetched or computed from elsewhere in terraform configuration

ex:

````
data "aws_ami" "example"{
    executable_users = ["self"]
    most_recent = true
    name_regex = "^myami-\\d{3}"
    owners = ["self"]
    filter {
        name="name"
        values = ["myami-*"]
    }
    filter {
        name="root-device-type"
        values=["ebs"]
    }
    filter {
        name="virtualization-type"
        values=["hvm"]
    }
}
````

------------------------------

### 8. Variables in Terraform

- something set at runtime
- allows you to vary what terraform will do when passing in or using a dynamic value
- variable with *undefined* values will not directly result in ERROR
    - NOTE: Terraform will ask you to supply a value **IMPORTANT** 
        ex: `variable custom_var {}`
    
- In version 0.12>=  :: `var.instance_type` declaration
- In version 0.11<=  :: `${var.instance_type}` declaration

**3 types of variable types**

1. Simple variable types
    - String
    - Number
    - boolean

    ````
    variable "aws_region"{
        type=string #type enforcement
        default="us-west-2"
    }
    variable "instance_count"{
        type=Number
        default=2
    }
    variable "enable_vpn_gateway"{
        type=bool
        default=false
    }
    ````


2. Collection Variable types (NOTE: all values of same type)
    - list :: [] 
    - map :: {k1=v1,k2=v2}
    - set :: an unordered collection of unique Values

    ex:
    
    ````
    variable "private_subnet_cidr_blocks"{
      type = list(string)
      default=[
        "10.0.101.0/24",
        "10.0.102.0/24",
        "10.0.103.0/24"
      ]
    }
    ````
    
        variable "resouce_tags"{
            type=map(string)
            default={
                project="project-alpha",
                environment="dev"
            }
        }


3. Structure Variable types
    - tuple :: fixed-length sequence of values of specified types - ["a",15,true]
    - object - A lookup table, matching a fixed set of keys to values of specified types

**Variable Precendence Order (Highest to lowest)**

1. -var or -var-file on command line

    ````bash
    terraform apply -auto-approve \
        -var "aws_access_key=<KEY>" \
        -var "aws_secret_key="<KEY>"
    ````

2. `*.auto.tfvars` or `*.auto.tfvars.json`

3. terraform.tfvars
    ex: `instance_type="t2.large"`

4. variables.tf

    ````
    variable "instance_type"{
    		default="t2.micro"
    }
    ````

5. environment variables
    - can be used to set a variable

    - must be in format TF_VAR_name
      
    - ````
      .bashrc
      export TF_VAR_instance_type=t2.micro
      export TF_VAR_ami=ami-12345abc
      ````

-----------------------------

### 9. Splat Expressions

- The splat[*]
- the special splat[*] symbol iterates over all the elements of a given list to its left and accesses from each one the attribute name given on its right.

    ex:
    
    ````
    resource "aws_iam_user" "lb"{
      name="loadbalancer.${count.index}"
      count=3
      path="/system/"
    }
    ````
    
    ````
    output "arns"{
        value=aws_iam_user.lb[*].arn
    }
    ````

--------------------------------

### 10. Functions in Terraform

Built-in functions
1. Numeric Functions : 
    `abs/ceil/floor/log/max/min/parseint/pow/signum`

2. String
    `chomp/format/formatlist/indent/join/lower/regex/regexall/replace/split/strrev/substr/title/trim/trimprefix/trimsuffix/trimspace/upper`

3. Collection 
    `alltrue/anytrue/chunklist/coalesce/coalescelist/compact/concat/contains/distinct/element/flatten/index/keys/length/list/lookup/map/matchkeys/merge/one/range/reverse/setintersection/setproduct/setsubtract/setunion/slice/sort/sum/transpose/values/zipmap`

4. Encoding
    `base64decode/base64encode/base64gzip/csvdecode/jsondecode/jsonencode/textdecodebase64/textencodebase64/urlencode/yamldecode/yamlencode`

5. Filesystem
    `abspath/dirname/pathexpand/basename/file/fileexists/fileset/filebase64/templatefile`

6. Date and Time 
    `formatdate/timeadd/timestamp`

7. Hash and crypto
     `base64sha256/base64sha512/bcrypt/filebase64sha256/filebase64sha512/filemd5/filesha1/filesha256/filesha512/md5/rsadecrypt/sha1/sha256/sha512/uuid/uuidv5`

8. IP network
    `cidrhost/cidrnetmask/cidrsubnet/cidrsubnets`

9. Type Conversion
    `can/defaults/nonsensitive/sensitive/tobool/tolist/tomap/tonumber/toset/tostring/try/type`

ex:

- join :: produces a string by concatenating together all elements of a given list of strings with given delimeter

- chomp :: removes newline characters at the end of a string
- split :: produces a list by dividing string at all occurences of a given separator
- max :: takes one or more numbers and returns the greatest number from the set
- slice :: extracts some consecutive elements from within a list

NOTE: User defined functions are not supported
NOTE: **IMPORTANT**
    - slice is NOT part of "string" function it is part of "Collection" function

--------------------------------


---

## File: terraform/kd/part2.md

### 11. Provisioners

- run commands after infrastructure has been provisioned
- can run script locally or remotely after a resource has been created
- should be used apringly, better alternatives for configuration management(chef,puppet,ansible)
- are inside resource block


````
resource "aws_instance" "my_instance"{
    ami=data.aws_ami.app_ami.id
    instance_type=var.instance_type
    provisioner "local-exec"{
    		command="echo ${aws_instance.my_instance.private_ip} >> private_ips.txt"
    }
} 
````

- local-exec provisioner
  - invokes a local executable after the resource is created
  - invokes a process on machine running terraform NOT the target resource **IMPORTANT**

````
resource "aws_instance" "my_instance"{
    ami=data.aws_ami.app_ami.id
    instance_type=var.instance_type
    provisioner "local-exec"{
    		command="echo ${aws_instance.my_instance.private_ip} >> private_ips.txt"
    }
} 
````

- remote-exec provisioner
  - invokes a script on a remote resource after it is created
  - supports:
      - winrm - Windows Remote Management (WinRM)
      - ssh - Secure shell

````
resource "aws_instance" "myec2"{
    ami="ami-1234qwerty"
    instance_type="t2.micro"
    key_name"terraform-key-name"
    vpc_security_group_ids=[aws_security_group.allow_ssh.id]
    provisioner "remote-exec"{
        inline=[
        "sudo amazon-linux-extras install -y nginx1.12",
        "sudo systemctl start nginx"
        ]

        connection{
            type="ssh"
            user"ec2-user"
            private_key=file("~/terraform.pem")
            host=self.public_ip
        }
    }
}
````

```
## NOTE - Adding a new security group resource to allow the terraform provisioner from laptop to connect to ec2 instance via SSH 
resource "aws_security_group" "allow_ssh"{
    name="allow_ssh"

    ingress{
        from_port=22
        to_port=22
        protocol="tcp"
        cidr_blocks=["0.0.0.0/0"]
    }
    egress{
        from_port=0
        to_port=65535
        protocol="tcp"
        cidr_blocks=["0.0.0.0/0"]
    }
}
```

**Types of Provisioners**
`chef/puppet/connection/file/habitat/local-exec/null_resource/remote-exec/salt-masterless`

**Types of Temporal Provisioners**

Creation-Time provisioner

1. only run during Creation

2. if fails the resource is marked as tainted


Destroy-Time provisioner
- only run during before a resource is destroyed
  
      resource "aws_instance" "my_instance"{
          ami=data.aws_ami.app_ami.id
          instance_type=var.instance_type
          provisioner "local-exec"{
              when=detroy
              command="echo ${aws_instance.my_instance.private_ip} >> private_ips.txt"
          }
      }

**Failure Behavior of Provisioners**

- on_failure

  - continue :: ignore error and continue creation or destruction

  - fail :: default behaviour, raise an error and stop, mark resource as tainted.


----------------------------------------------------------

### 12. Output Values

- shows a piece of data after terraform successfully completes
- are useful as they echo values from terraform to the command line after the completion
- can be used as input between modules

````
output "instance_ip_addr"{
		value=aws_instance.server.private_ip
}
````

----------------------------------------------------------

### 13. Modules

- containers for multiple reources that are used together
- consists of a collection of .tf and/or .tf.json files kept together in a directory
- main way to package and reuse resource configurations with terraform
- can define inputs/outputs,enforce constraints and provision a number of resources per invocation
- can enforce security and regulory constraints
- are useful as they allow us define reusable blocks of terraform code 
- of which you can have many instances in the main terraform project
- root module calls child module
    - root modules are resources defined in the .tf files in the main working directory

**Module Sources**

- local Path :: must start with either ./ or ../
- Terraform Registry
- Github
- S3 

**Local values in Modules**

- a "local" assigns a name to an expression, allowing it to be used multiple times
- expression of a local can refer to other locals
- reference cycles are not allowed
- group logically related locals into a single block

**Module - Root and Child modules**

- every terraform configuration has atleast one module, known as the ROOT module
- ROOT module consists of the resources defined in the .tf files in the main working directory
- a module can call other modules which allows you to include the child modules resources
- a module can include a module block that is the calling module of the child module

````
module "servers"{ #module servers = root module
    source="./app-cluster" #app-cluster = child module
    servers=5
}
````

**Module Outputs**

- Resource defined in a module are encapsulated, so calling module cannot access their attributes directly
- a child module can declare OUTPUT values to selectively export certain values to be accessed by the calling module

````
output "instance_ip_addr"{
		value=aws_instance.server.private_ip
}
````

`Module - sensitive=true`

- output can be marked as containing SENSITIVE material
- sensitive=true prevents Terraformfrom showing value in list of outputs at the end of terraform apply
- Sensitive output values are STILL RECORDED in terraform.tfstate and visible to anyone with access terraform.tfstate

````
output "db_password"{
  value=aws_db_instance.db.password
  sensitive=true
}
````

**module - versions**

- it is NOT mandatory to include module version argument when pulling code from terraform Registry
- explicitly constrain version numbers for external modules to avoid unwated changes
- version constraints are supported for modules installed from:
  - Terraform Registry :: `Reference <NAMESPACE>/<NAME>/<PROVIDER>`
  - Private Registry :: `Reference <HOSTNAME>/<NAMESPACE>/<NAME>/<PROVIDER>`

specifying a VERSION is mandatory when fetching a module

````
#public Registry
module "consul"{
    source="hashicorp/consul/aws"
    version="0.0.5"
    servers=3
}
````

```
#private Registry
module "vpc"{
    source="app.terraform.io/example-corp/vpc/aws"
    version="0.9.3"
}
```

**Create your own module**

- Create module for S3

````
variable "s3_name"{}

resource "aws_s3_bucket" "my_bucket"{
    name=var.s3_name
}

output "bucket_id"{
    value=aws_s3_bucket.bucket.id
}
````

- Use S3 module

````
module "my_sample_bucket"{
    s3_name="sample_bucket"
    source="<path to module folder>"
}
````

-----------------------------------------------------------------------------------------------

### 14. Registries

- is simply a repository for modules

- Terraform Registry
    - is a repository of modules written by terraform Community
    - instead of writing your own module search registry if someone has written one already
    - VERIFIED MODULES(blue verification badge) in Terraform registry are maintained by various Third Parties like AWS

**Terraform Cloud Public Registry**

- Terraform Registry at registry.terraform.io hosts public modules and providers, but most organizations use modules or providers that cannot or do not need to be publicly available.

**Terraform Cloud Private Registry**

- Terraform cloud includes a private registry that is available to all accounts including free organizations
- unlike public registry, the private registry can import modules from your private VCS repositories on any terraform clouds supported VCS providers.
- also lets you upload and manage private,custom providers through the Terraform cloud API and curate list of commonly-used public providers and modules.

----------------------------------------------------------------------------------

### 15. Organizations

````
                            --------------- Development Organizations
​                            |
​                            |
Terraform Enterprise ---------------------- Testing Organizations
​                            |
​                            |
​                            --------------- Production Organizations
````


- are shared spaces for teams to collaborate on workspaces
- teams are groups of terraform cloud users within an organization
- to delgate provisioning work the organization can grant workspace permissions to specific teams
- teams can only have permissions on workspaces within their organization, although any user in a team can belong to other teams in other organization


example hierarchy:

- Development Organization
  - Networking workspace :: VPC and S3
  - Persistence workspace :: S3 and Databases
  - compute workspace :: EKS and ASG
  - Shared Services workspace :: SNS and SQS and Lambda
- Testing Organization
- Production Organization

--------------------------------------------------------------------------

### 16. Workspaces

- is simply a directory that contains terraform code
- working with terraform invloves managing collections of infrastructure resources and most organizations manage different collections
- when run locally, Terraform manages each collection of infrastructure with a persistent working directory which contains configuration,state data and variables
- since terraform CLI uses content from the directory it runs in, you can organize infrastructure resources into meaningful groups by keeping their configurations in separate directories
- Terraform Cloud manages infrastructure collections with WORKSPACES instead of directories
- A workspace contains everything terraform needs to manage a given collection of infrastructure and separate workspaces function like completely separate working directories
- WORKSPACES are way of creating multiple environments using same code
- separate WORKSPACES function like separate working directories
    - each WORKSPACE has its own terraform.tfstate
    - can run its own version of Terraform
    - can have different set of environment variables
    - terraform.tfstate is stored in directory called terraform.tfstate.d
- Workspaces are not suitable for strong separation isolation
- The default workspace CANNOT be deleted **IMPORTANT**

--------------------------------------------------------------------------------------------

### 17. Terraform - Flavours

Terraform comes in five Flavours:

1. open source - the binary you download and run at home 
2. cloud free
3. cloud team
4. cloud business
5. self hosted Enterprise (ex: tfe)

Terraform offerings

- Terraform Cloud
  - free
  - Team
  - business
    - SSO 
    - auditing
    - self-hosted terraformcloud agents
      - terraform cloud agents allow terraform cloud to communicate with isolated, private or on-premises infrastructure
      - terraform cloud agents can establish a simple connection between your environment and terraform cloud which allows for provisioning operations and management
    - private data center Networking
    - clustering



- Terraform Self-Hosted Enterprise (ex: TFE)
  - internally hosted product to run terraform at scale
  - terraform plan and terraform apply happens on the TFE servers
  - state is stored on TFE and TFE provides state locking
  - TFE also supports the Sentinel Policy Engine

Enterprise offerings

- Sentinel
  - Sentinel is an embedded Policy as Code framework
  - Sentinel enables fine grained logic based control policy decisions
  - Sentinel is an embedded proactive policy as code framework
  - Sentinel use cases:
    - verify if ec2 instaces have tags
    - verify if the S3 buckets have encryption enabled
  - Sentinel execution sequence:
    - terraform plan
    - Sentinel checks
    - terraform apply

- Enterprise state security
  - treat terraform.tfstate as sensitive
  - Encrypt terraform.tfstate at rest
  - encrypt terraform.tfstate in transit with TLS 
  - Perform audit on State access and operations
  - S3 backend supports encryption at rest 

- Remote Backend 
  - remote backend stores terraform.tfstate and supports running operations on terraform cloud
  - full remote operations include:
    - executing terraform plan remotely on terraform cloud environment
    - executing terraform apply remotely on terraform cloud environment
    - with log streaming to back to a local terminal

------------------------------------------------------------------------------------

### 18. Conditional logic

Creating conditional logic within Terraform configurations allows for creating a more dynamic configuration. 

- This allows for greater abstraction and logic flow in the code. 
- It's essential to understand the logical conditions that can be created within the HCL (HashiCorp Configuration Language) language as it provides even more reusability.
- condition ? true : false

````
terraform {
    required_providers {
        aws = {
        source  = "hashicorp/aws"
        version = ">=3.7.0"
        }
    }
}
data "aws_ami" "default" {
    most_recent = "true"
    filter {
        name   = "name"
        values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
    }
    filter {
        name   = "virtualization-type"
        values = ["hvm"]
    }
    owners = ["099720109477"]
}
resource "aws_instance" "server" {
    ami           = var.ami != "" ? var.ami : data.aws_ami.default.image_id
    instance_type = var.instance_size
    tags = {
    		Name = "calabvm"
    }
}
````

The condition is if the variable AMI does not contain an empty string. If it is true, then set the AMI to the value of var.ami. If it is false, set the value of the AMI to the ID of data.aws_ami.default[0].image_id which is the AMI ID that was collected in the data block. This strategy gives the module the ability to take in AMI ID input or find an AMI on its own and makes the module more dynamic

---------------------------------------------------------------------------------------------

### 19. Loops in terraform

- Using loops in Terraform can give code a cleaner look and follows the DRY (Don't Repeat Yourself)  principles of programming where the same concepts aren't repeated throughout the Terraform configuration. 
- Loops also allow for resources to scale efficiently. 

    ex:
    
    
        ##foreach
            resource "aws_instance" "server" {
                ami           = "ami-0528a5175983e7f28"
            instance_type = "t2.micro"
                associate_public_ip_address = var.associate_public_ip_address    
            #dynamic block with for_each loop
            dynamic "ebs_block_device" {
                for_each = var.ebs_block_device
                    content {
                    delete_on_termination = lookup(ebs_block_device.value, "delete_on_termination", null)
                    device_name           = ebs_block_device.value.device_name
                    encrypted             = lookup(ebs_block_device.value, "encrypted", null)
                    iops                  = lookup(ebs_block_device.value, "iops", null)
                    kms_key_id            = lookup(ebs_block_device.value, "kms_key_id", null)
                    snapshot_id           = lookup(ebs_block_device.value, "snapshot_id", null)
                    volume_size           = lookup(ebs_block_device.value, "volume_size", null)
                    volume_type           = lookup(ebs_block_device.value, "volume_type", null)
                    }
            }
        
            tags = {
                Name = "${var.servername}"
            }
        }

- Dynamic blocks can be used for resources that contain repeatable configuration blocks. Instead of repeating several ebs_block_device blocks, a dynamic block is used to simplify the code. This is done by combining the dynamic block with a for_each loop inside. The first line inside the dynamic block is the for_each loop. The loop is iterating through the list of the ebs_block_device variable, which is a list of maps. In the content block, each value of the map is referenced using the lookup function. The logic here is to look for a value in the map variable and if it's not there, set the value to null. The dynamic block will iterate through each map in the list

- **count**


````
#public IP address with Count Conditional Expression
resource "aws_eip" "pip" {
  count             = var.associate_public_ip_address ? 1 : 0
  network_interface = aws_instance.server.primary_network_interface_id
  vpc               = true
}
````

Count allows for creating multiple instances of a resource block. Almost all resource blocks can use the count attribute. It is simply the number of times to create the resource block. It can also be used as conditional logic. In this case, the value of count is a conditional expression. If var.associate_public_ip_address is true set the count value to 1, if false set it to 0. This allows resource blocks to be created conditionally. In this example, a public IP address is not created if var.associate_public_ip_address is set to false.

**count and count index**

- count parameter can simplify configuratios and scale resources by incrementing a number think LOOP 
- in resource blocks where count is set an additional count object called count.index is available to allow unique naming of each resource instance.
- count is a loop starting at 0
- count.index value is incremented on each loop

    ex:

````
resource "aws_instance" "server"{
    count=4
    ami="ami-a1b2c3d4"
    tags={
    		name="Server ${count.index}"
    }
} 
````



---------------------------------------------------------------------------------------

---

