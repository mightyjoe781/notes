# Modules

## What are Modules?

A module is a directory of `.tf` files that packages related resources together. Modules enable you to:

- Reuse infrastructure patterns across projects
- Enforce security and compliance constraints
- Abstract complexity from the caller

Every Terraform project has at least one module - the **root module** (your working directory). All other modules are **child modules**.

## Root vs Child Modules

| | Root Module | Child Module |
|--|-------------|--------------|
| Location | Working directory where you run `terraform` | A subdirectory or external source |
| How to use | Run `terraform apply` directly | Called with a `module` block |
| State | Owns the state file | State managed by the calling root module |

```hcl
# root module calling a child module
module "networking" {
  source = "./modules/networking"
  vpc_cidr = "10.0.0.0/16"
}
```

## Module Sources

| Type | Syntax | Example |
|------|--------|---------|
| Local path | `./` or `../` prefix required | `source = "./modules/vpc"` |
| Terraform Registry | `<namespace>/<name>/<provider>` | `source = "hashicorp/consul/aws"` |
| Private Registry | `<hostname>/<namespace>/<name>/<provider>` | `source = "app.terraform.io/corp/vpc/aws"` |
| GitHub | `github.com/<org>/<repo>` | `source = "github.com/org/repo"` |
| S3 | `s3::<url>` | `source = "s3::https://s3.amazonaws.com/bucket/module.zip"` |

## Module Versioning

Always pin module versions to avoid unexpected changes.

```hcl
# public Terraform Registry
module "consul" {
  source  = "hashicorp/consul/aws"
  version = "~> 0.1"
  servers = 3
}
```

```hcl
# private registry
module "vpc" {
  source  = "app.terraform.io/example-corp/vpc/aws"
  version = "0.9.3"
}
```

Version constraint operators:

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Exact version | `= 1.2.0` |
| `!=` | Any except this | `!= 1.0.0` |
| `>`, `>=`, `<`, `<=` | Comparison | `>= 1.0.0` |
| `~>` | Pessimistic (patch only) | `~> 1.2` allows `1.2.x` |

> **Note:** Version pinning is required for modules from a private registry but optional for public registry modules. Pin anyway.

## Module Inputs and Outputs

Resources inside a module are **encapsulated** - the caller cannot access them directly. Use output values to expose what the caller needs.

**Inside the child module (`modules/s3/main.tf`):**

```hcl
variable "bucket_name" {}

resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
}

output "bucket_id" {
  value = aws_s3_bucket.this.id
}
```

**In the root module:**

```hcl
module "my_bucket" {
  source      = "./modules/s3"
  bucket_name = "my-app-assets"
}

# access child module output
resource "aws_iam_policy" "access" {
  # ...
  resource = "${module.my_bucket.bucket_id}/*"
}
```

### Sensitive Module Outputs

```hcl
output "db_password" {
  value     = aws_db_instance.db.password
  sensitive = true
}
```

- Hides the value in CLI output after `terraform apply`
- The value is **still stored in `terraform.tfstate`** in plain text
- Treat the state file as sensitive when outputs are marked sensitive

## Local Values

Locals assign a name to an expression so it can be reused without repetition. Think of them as computed constants within a module.

```hcl
locals {
  env    = "production"
  prefix = "myapp-${local.env}"
  common_tags = {
    Environment = local.env
    Project     = "my-app"
  }
}

resource "aws_instance" "app" {
  tags = local.common_tags
}
```

Rules:
- Locals can reference other locals
- Circular references are not allowed
- Group related locals into a single `locals` block

## After Calling `terraform init`

New modules are downloaded or linked. Run `terraform init` whenever you add or change a module source.
