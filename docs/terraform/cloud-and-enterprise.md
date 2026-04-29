# Cloud and Enterprise

## Terraform Editions

Terraform comes in five editions:

| Edition | Description |
|---------|-------------|
| **Open Source** | Free CLI binary, local state only |
| **Cloud Free** | Terraform Cloud with remote state and runs, up to 500 resources |
| **Cloud Team** | Team management, SSO, audit logging |
| **Cloud Business** | Agents, private networking, clustering, SSO |
| **Self-Hosted Enterprise (TFE)** | Full Terraform Cloud features, hosted on your own infrastructure |

## Terraform Cloud

Terraform Cloud runs `terraform plan` and `terraform apply` remotely on HashiCorp's infrastructure, with log streaming back to your terminal.

### Tiers

**Free**
- Remote state storage and locking
- Remote runs
- VCS integration

**Team**
- Team-based access controls
- Audit logging
- SSO

**Business**
- Terraform Cloud Agents (for private/on-premises infra)
- Private data center networking
- Clustering
- Advanced audit features

### Remote Backend

Store state and run operations on Terraform Cloud instead of locally.

```hcl
terraform {
  cloud {
    organization = "my-org"
    workspaces {
      name = "my-workspace"
    }
  }
}
```

Or use the legacy `remote` backend:

```hcl
terraform {
  backend "remote" {
    organization = "my-org"
    workspaces {
      name = "my-workspace"
    }
  }
}
```

Remote operations include:
- `terraform plan` and `terraform apply` run on Terraform Cloud servers
- Logs stream back to your local terminal
- State is stored and locked by Terraform Cloud

## Terraform Enterprise (TFE)

Self-hosted version of Terraform Cloud for organizations that cannot use SaaS.

- `terraform plan` and `terraform apply` run on TFE servers
- State stored and locked by TFE
- Supports Sentinel policy engine
- Air-gapped deployments supported

## Workspaces

A workspace is an isolated environment with its own state file, variables, and Terraform version. Use workspaces to manage multiple environments (dev, staging, prod) from a single configuration.

### CLI Workspaces

```bash
terraform workspace new staging      # create
terraform workspace list             # list all
terraform workspace show             # show current
terraform workspace select staging   # switch
terraform workspace delete staging   # delete (cannot delete 'default')
```

> **Important:** The `default` workspace cannot be deleted.

Each workspace stores its state in `terraform.tfstate.d/<workspace_name>/terraform.tfstate`.

### Using Workspace Name in Config

```hcl
resource "aws_instance" "app" {
  instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"

  tags = {
    Environment = terraform.workspace
  }
}
```

### Workspace Limitations

- Workspaces share the same backend and config
- Not suitable for strict environment isolation (use separate root modules or separate backends for full isolation)
- Each workspace can run a different version of Terraform and have different environment variables

## Organizations

Organizations are shared spaces for teams to collaborate on workspaces in Terraform Cloud.

```
Terraform Enterprise
  |- Development Organization
  |    |- Networking workspace  (VPC, S3)
  |    |- Persistence workspace (Databases)
  |    |- Compute workspace     (EKS, ASG)
  |    |- Services workspace    (SNS, SQS, Lambda)
  |- Testing Organization
  |- Production Organization
```

- Teams are groups of users within an organization
- Organizations grant workspace permissions to teams
- A user can belong to teams in multiple organizations
- Workspace permissions are scoped to a single organization

## Sentinel - Policy as Code

Sentinel is HashiCorp's Policy as Code framework, available in the Team and Enterprise tiers.

- Runs policy checks **between** `terraform plan` and `terraform apply`
- Lets platform teams enforce rules that developers cannot bypass
- Policies are written in the Sentinel language

### Execution Order

```
terraform plan -> Sentinel checks -> terraform apply
```

If Sentinel checks fail, `terraform apply` is blocked.

### Example Use Cases

- Require all EC2 instances to have a `CostCenter` tag
- Require all S3 buckets to have encryption enabled
- Prevent resources in certain regions
- Enforce minimum instance sizes in production

## State Security (Enterprise)

When storing state remotely, treat it like a secrets file - it contains resource attributes, passwords, and keys in plain text.

| Practice | Details |
|----------|---------|
| Encrypt at rest | S3 with SSE, or Terraform Cloud (encrypted by default) |
| Encrypt in transit | TLS enforced by all supported backends |
| Restrict access | IAM policies on S3 bucket, org-level access in Terraform Cloud |
| Enable versioning | S3 bucket versioning enables state recovery |
| Audit access | S3 access logs or CloudTrail, Terraform Cloud audit log |
| Never commit to VCS | Add `terraform.tfstate` to `.gitignore` |
