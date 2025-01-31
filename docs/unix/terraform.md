# Terraform 

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../terraform/index.md)

Infrastructure as Code (IaC) for cloud provisioning.

### Installation

````bash
# Using apt  
sudo apt-get update && sudo apt-get install terraform  

# Manual install  
wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip  
unzip terraform_1.5.7_linux_amd64.zip && sudo mv terraform /usr/local/bin/  
````

### Commands

| Command                | Description                  |
| ---------------------- | ---------------------------- |
| `terraform init`       | Initialize working directory |
| `terraform plan`       | Preview changes              |
| `terraform apply`      | Apply configuration          |
| `terraform destroy`    | Delete infrastructure        |
| `terraform state list` | List managed resources       |

### Sample AWS EC2 Config

Example `main.tf`

````hcl
provider "aws" {  
  region = "us-west-2"  
}  

resource "aws_instance" "web" {  
  ami           = "ami-0c55b159cbfafe1f0"  
  instance_type = "t2.micro"  

  tags = {  
    Name = "Terraform-Web"  
  }  
}  
````

### State Management

* local state

````bash
terraform state pull > backup.tfstate  
````

* remote backend (s3)

````bash
terraform {  
  backend "s3" {  
    bucket = "my-tf-state"  
    key    = "prod/terraform.tfstate"  
    region = "us-east-1"  
  }  
}  
````

### Tips

* Variables

````hcl
variable "region" {  
  default = "us-west-2"  
}  
````

* Workspaces

````hcl
terraform workspace new dev  
````

* plan output

````hcl
terraform plan -out=tfplan  
terraform apply tfplan  
````

### Security

1. **Secret Management**:

   ```hcl
   data "aws_secretsmanager_secret" "db_pass" {  
     name = "prod/db"  
   }  
   ```

2. **Lock State**: Use S3/DynamoDB for state locking.

### Troubleshooting

| Issue                | Solution                        |      |
| -------------------- | ------------------------------- | ---- |
| "Provider not found" | Run `terraform init`            |      |
| "State locked"       | Manually remove `.tfstate.lock` |      |
| Plan/apply mismatch  | Use `-refresh=false` flag       |      |

### Resources

* [Terraform Registry](https://registry.terraform.io/)
* [AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)