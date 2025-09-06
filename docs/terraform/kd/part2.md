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