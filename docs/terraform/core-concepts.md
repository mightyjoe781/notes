# Core Concepts

## Providers

A provider is a plugin that lets Terraform interact with a cloud platform or service (AWS, Azure, GCP, Kubernetes, etc.).

- Providers must be declared in the `terraform` block
- Terraform downloads the provider plugin during `terraform init`
- Pin the provider version to avoid unexpected breaking changes

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
  region = "us-east-1"
}
```

### AWS Authentication

Terraform reads AWS credentials in this order (first match wins):

1. Hard-coded in `main.tf` - works but insecure, avoid in production
2. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
3. Shared credentials file (`~/.aws/credentials`) - reference via `profile`

```hcl
provider "aws" {
  profile = "default"
  region  = "us-east-1"
}
```

## Resources

A resource represents a single infrastructure object (an EC2 instance, an S3 bucket, a DNS record, etc.).

### Syntax

```hcl
resource "<TYPE>" "<NAME>" {
  argument = value
}
```

| Part | Example | Description |
|------|---------|-------------|
| TYPE | `aws_instance` | Provider + resource kind |
| NAME | `my_instance` | Local label, used to reference this resource |
| argument | `ami`, `instance_type` | Configuration for the resource |

### Example

```hcl
resource "aws_instance" "my_instance" {
  ami           = "ami-1234qwerty"
  instance_type = "t2.micro"
}
```

To reference this elsewhere: `aws_instance.my_instance.id`

## Data Sources

A data source fetches read-only information about existing infrastructure that Terraform did not create (or that exists outside this configuration).

```hcl
data "aws_ami" "example" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["myami-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
```

Reference: `data.aws_ami.example.id`

## Dependencies

Terraform builds a dependency graph to determine creation order. There are two ways to express dependencies.

### Implicit Dependency

When one resource references another, Terraform automatically creates the dependency. It ensures `aws_eip` is created before `aws_instance`.

```hcl
resource "aws_eip" "my_eip" {
  domain = "vpc"
}

resource "aws_instance" "my_instance" {
  ami           = "ami-1234qwerty"
  instance_type = "t2.micro"
  # references my_eip, so Terraform knows the order
  public_ip     = aws_eip.my_eip.private_ip
}
```

### Explicit Dependency

Use `depends_on` when one resource depends on the **behavior** of another (not its attributes). For example, an instance needs an S3 bucket to exist first even though it doesn't reference it directly.

```hcl
resource "aws_s3_bucket" "example" {}

resource "aws_instance" "my_instance" {
  instance_type = "t2.micro"
  depends_on    = [aws_s3_bucket.example]
}
```

> **Rule of thumb:** Use implicit dependency whenever possible. Use `depends_on` only when there is no direct attribute reference.
