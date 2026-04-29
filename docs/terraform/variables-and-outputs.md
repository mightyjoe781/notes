# Variables and Outputs

## Variables

Variables make Terraform configurations reusable. A variable with no default and no supplied value will prompt interactively at runtime.

### Variable Types

**1. Simple Types**

```hcl
variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "instance_count" {
  type    = number
  default = 2
}

variable "enable_vpn_gateway" {
  type    = bool
  default = false
}
```

**2. Collection Types** (all values must be the same type)

| Type | Description | Example |
|------|-------------|---------|
| `list` | Ordered sequence | `["a", "b", "c"]` |
| `map` | Key-value pairs | `{ env = "dev" }` |
| `set` | Unordered, unique values | like list but no duplicates |

```hcl
variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "resource_tags" {
  type = map(string)
  default = {
    project     = "project-alpha"
    environment = "dev"
  }
}
```

**3. Structural Types** (values can be different types)

| Type | Description | Example |
|------|-------------|---------|
| `tuple` | Fixed-length sequence of mixed types | `["a", 15, true]` |
| `object` | Named attributes with specified types | like a struct |

```hcl
variable "server_config" {
  type = object({
    instance_type = string
    count         = number
    enabled       = bool
  })
}
```

### Variable Declarations

A variable block can have these optional arguments:

```hcl
variable "instance_type" {
  type        = string
  default     = "t2.micro"
  description = "EC2 instance type"
  sensitive   = false
}
```

## Variable Precedence

Values are resolved in this order - **highest wins:**

| Priority | Source | Example |
|----------|--------|---------|
| 1 (highest) | `-var` or `-var-file` flag on CLI | `terraform apply -var "region=us-east-1"` |
| 2 | `*.auto.tfvars` or `*.auto.tfvars.json` | `prod.auto.tfvars` |
| 3 | `terraform.tfvars` or `terraform.tfvars.json` | `instance_type = "t2.large"` |
| 4 | Environment variables (`TF_VAR_name`) | `export TF_VAR_region=us-east-1` |
| 5 (lowest) | `default` in `variables.tf` | `default = "t2.micro"` |

**CLI example:**

```bash
terraform apply -auto-approve \
  -var "aws_access_key=<KEY>" \
  -var "aws_secret_key=<KEY>"
```

**Environment variable example:**

```bash
# add to ~/.bashrc or ~/.zshrc
export TF_VAR_instance_type=t2.micro
export TF_VAR_ami=ami-12345abc
```

## Outputs

Outputs print values after `terraform apply` completes and expose values for use by parent modules.

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "subnet_ids" {
  value = aws_subnet.main[*].id
}
```

Access a module's output from a parent: `module.<MODULE_NAME>.<OUTPUT_NAME>`

```hcl
# in parent
resource "aws_instance" "app" {
  subnet_id = module.networking.subnet_id
}
```

### Sensitive Outputs

Mark an output `sensitive = true` to hide it from CLI output. Note: the value is **still stored in plain text in `terraform.tfstate`**.

```hcl
output "db_password" {
  value     = aws_db_instance.db.password
  sensitive = true
}
```

## Splat Expressions

The splat operator `[*]` iterates over all elements of a list and returns one attribute from each.

```hcl
resource "aws_iam_user" "lb" {
  count = 3
  name  = "loadbalancer.${count.index}"
  path  = "/system/"
}

output "user_arns" {
  value = aws_iam_user.lb[*].arn
  # equivalent to: [aws_iam_user.lb[0].arn, aws_iam_user.lb[1].arn, aws_iam_user.lb[2].arn]
}
```
