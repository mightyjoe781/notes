# Workflow and CLI

## Core Commands

Run these in order for a typical provisioning workflow:

```
terraform init -> terraform validate -> terraform plan -> terraform apply -> terraform destroy
```

### `terraform init`

Prepares the working directory. Must be run before any other command.

- Downloads provider plugins listed in `required_providers`
- Initializes the backend (local or remote)
- Creates `.terraform/` directory and `.terraform.lock.hcl`

```hcl
# minimum config needed to run init
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}
```

```bash
terraform init
```

### `terraform validate`

Checks the syntax and structure of `.tf` files. Does not connect to any provider.

```bash
terraform validate
```

### `terraform plan`

Shows a preview of what Terraform will create, change, or destroy. Does not make any real changes.

```bash
terraform plan

# save plan to a file
terraform plan -out=tfplan
```

Symbols in plan output:

| Symbol | Meaning |
|--------|---------|
| `+` | Resource will be created |
| `-` | Resource will be destroyed |
| `~` | Resource will be updated in-place |
| `-/+` | Resource will be destroyed and recreated |

### `terraform apply`

Executes the plan and makes real infrastructure changes. Prompts for confirmation unless `-auto-approve` is passed.

```bash
terraform apply

# skip confirmation prompt
terraform apply -auto-approve

# apply a saved plan file
terraform apply tfplan
```

> **Note:** If `apply` fails midway, Terraform does not automatically roll back. Re-run `terraform apply` to continue. Use version control to manage rollbacks.

### `terraform destroy`

Destroys all resources managed by the current configuration.

```bash
terraform destroy

# target a single resource
terraform destroy -target aws_instance.my_instance
```

### `terraform refresh` (deprecated)

Use `terraform apply -refresh-only` instead to sync state with real infrastructure without making changes.

```bash
terraform apply -refresh-only
```

## Workspace Commands

Workspaces let you manage multiple state files from the same config (e.g., dev, staging, prod).

```bash
terraform workspace new dev        # create workspace
terraform workspace list           # list all workspaces
terraform workspace show           # show current workspace
terraform workspace select dev     # switch workspace
terraform workspace delete dev     # delete workspace (cannot delete 'default')
```

Use `terraform.workspace` in config to reference the current workspace name:

```hcl
resource "aws_instance" "app" {
  tags = {
    Environment = terraform.workspace
  }
}
```

## Debugging

Enable verbose logging with the `TF_LOG` environment variable.

| Level | Verbosity |
|-------|-----------|
| `TRACE` | Highest - everything |
| `DEBUG` | Detailed internal steps |
| `INFO` | High-level operations |
| `WARN` | Warnings only |
| `ERROR` | Errors only (lowest) |

```bash
# enable trace logging
export TF_LOG=TRACE

# write logs to a file
export TF_LOG_PATH=/tmp/terraform.log

# disable logging
unset TF_LOG
```

## Quick Reference

```bash
terraform -help                     # list all commands
terraform -help <command>           # help for a specific command
terraform fmt                       # format .tf files
terraform state list                # list resources in state
terraform output                    # print output values
terraform taint <resource>          # mark resource for recreation on next apply
terraform import <resource> <id>    # import existing resource into state
```
