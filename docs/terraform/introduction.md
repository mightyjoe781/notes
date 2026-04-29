# Introduction to Terraform

## What is Terraform?

Terraform is an open-source IaC tool by HashiCorp.

- Written in **Go**
- Uses **graph theory** to determine the order in which resources are created or destroyed
- Uses **HCL** (HashiCorp Configuration Language) as its config language (JSON also supported)
- **Declarative** - you describe the desired end state; Terraform figures out how to get there

## IaC Tools Comparison

| Cloud | Native IaC Tool |
|-------|----------------|
| AWS | CloudFormation |
| Azure | Azure Resource Manager |
| GCP | Deployment Manager |
| Any | Terraform |

Terraform is **cloud-agnostic** - the same workflow works across all major providers.

## HCL Syntax Basics

### Comments

```hcl
# single line comment

/* multi-line
   comment */
```

### String Interpolation

Use `${}` only inside strings. Outside strings, reference directly.

```hcl
# inside a string
name = "server-${var.env}"

# outside a string (Terraform >= 0.12)
instance_type = var.instance_type
```

### Types

| Category | Types |
|----------|-------|
| Primitive | `string`, `number`, `bool` |
| Collection | `list`, `map`, `set` |
| Structural | `tuple`, `object` |

### Reference Syntax

| Block type | Declaration | Access |
|------------|-------------|--------|
| Resource | `resource "type" "name" {}` | `type.name.attribute` |
| Data source | `data "type" "name" {}` | `data.type.name.attribute` |
| Variable | `variable "name" {}` | `var.name` |
| Module output | `module "name" {}` | `module.name.output_name` |

## File Structure

A Terraform project (called a **root module**) is a directory containing `.tf` files.

| File | Purpose |
|------|---------|
| `main.tf` | Core resources, providers, data sources |
| `variables.tf` | Input variable declarations |
| `outputs.tf` | Output value declarations |
| `provider.tf` | Provider configuration (sometimes in `main.tf`) |
| `terraform.tfvars` | Variable values (not committed if sensitive) |
| `terraform.tfstate` | State file - do not edit manually |
| `terraform.tfstate.backup` | Previous state backup |
| `.terraform/` | Downloaded provider plugins |
| `.terraform.lock.hcl` | Provider version lock file - commit this |

> **Tip:** For large projects, split resources across multiple `.tf` files. Terraform reads all `.tf` files in a directory together.

## Root Module

The root module is simply the directory where you run Terraform commands. It typically contains `main.tf`, `variables.tf`, and `outputs.tf`.

Modularized projects have additional child module directories, each with their own `main.tf`.

```
my-project/
  main.tf           # root module
  variables.tf
  outputs.tf
  modules/
    networking/     # child module
      main.tf
    compute/        # child module
      main.tf
```
