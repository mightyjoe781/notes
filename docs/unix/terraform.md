# Terraform

[:octicons-arrow-left-24:{ .icon } Back](index.md) | [Detailed Guides](../terraform/index.md)

Infrastructure as Code for cloud provisioning. Declarative HCL config files describe the desired state; Terraform figures out what to create, update, or destroy.

### Installation

```bash
# Official apt repo
sudo apt install terraform

# Or via tfenv (version manager)
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
ln -s ~/.tfenv/bin/* /usr/local/bin/
tfenv install latest
tfenv use latest
```

### Core Workflow

```bash
terraform init         # download providers and modules
terraform validate     # check syntax
terraform plan         # preview changes
terraform apply        # apply (prompts for confirmation)
terraform apply -auto-approve
terraform destroy      # delete all managed resources
terraform fmt          # format .tf files
```

### HCL Basics

```hcl
# Variables
variable "region" {
  type    = string
  default = "us-east-1"
}

# Locals (computed values)
locals {
  env = "prod"
  name_prefix = "${var.project}-${local.env}"
}

# Output
output "instance_ip" {
  value = aws_instance.web.public_ip
}

# Data source (read existing resource)
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*"]
  }
}
```

### Sample AWS EC2

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags = {
    Name = "${local.name_prefix}-web"
  }
}
```

### State Management

```bash
terraform state list              # list managed resources
terraform state show aws_instance.web
terraform state mv old_name new_name    # rename resource in state
terraform state rm resource.name        # remove from state (orphan)
terraform import aws_instance.web i-1234567890   # import existing resource
```

Remote backend (S3 + DynamoDB locking):

```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-state-lock"
    encrypt        = true
  }
}
```

### Workspaces

```bash
terraform workspace list
terraform workspace new staging
terraform workspace select prod
terraform workspace show         # current workspace
```

Use `${terraform.workspace}` in resources to differentiate environments.

### Modules

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

```bash
terraform get      # download modules
```

### Useful Commands

```bash
terraform plan -out=tfplan         # save plan
terraform apply tfplan             # apply saved plan (no prompt)
terraform plan -var="region=eu-west-1"
terraform plan -var-file="prod.tfvars"
terraform output                   # show outputs
terraform console                  # interactive expression evaluation
```

### Tips

- Use `-target=resource.name` to apply only one resource (use sparingly)
- Store state remotely (S3, Terraform Cloud) - never commit `.tfstate` to git
- Use `prevent_destroy = true` lifecycle rule to protect critical resources
- `terraform providers lock` pins provider checksums for reproducible builds

### See Also

- [Ansible](ansible.md) for configuration management after provisioning
- Also: Pulumi (Terraform alternative with real languages), OpenTofu (open-source Terraform fork), Terragrunt (DRY wrapper for Terraform)
