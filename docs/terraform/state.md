# State Management

## What is State?

Terraform keeps a record of all infrastructure it has created in a **state file** (`terraform.tfstate`). This file:

- Maps your config to real-world resources
- Tracks metadata and dependency order
- Enables Terraform to detect **drift** (differences between config and actual infrastructure)
- Is required for `plan`, `apply`, and `destroy` to work correctly

> **Do not edit `terraform.tfstate` manually.** Use `terraform state` commands instead.

## Local State (Default)

By default, state is stored in `terraform.tfstate` in your working directory. A backup is kept in `terraform.tfstate.backup`.

**Problems with local state:**

- Not shareable - teammates cannot collaborate
- No locking - concurrent applies can corrupt state
- No encryption - sensitive values are in plain text on disk

## Remote State

Store state in a remote backend to enable team collaboration and improve security.

### S3 Backend (AWS)

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    region         = "us-west-2"
    key            = "terraform.tfstate"
    encrypt        = true
    dynamodb_table = "terraform-lock-table"
  }
}
```

**Required AWS resources:**

| Resource | Purpose |
|----------|---------|
| S3 bucket | Stores the state file |
| DynamoDB table | Provides state locking |

**DynamoDB table requirements:**
- Partition key: `LockID` (type: String)

### Benefits of Remote State

- State is encrypted at rest (S3 with SSE)
- State in transit is protected by TLS
- Locking prevents concurrent modifications
- Accessible to all team members with appropriate IAM permissions

## State Locking

When Terraform writes to state, it acquires a lock. This prevents two people from running `apply` at the same time and corrupting the state file.

- Supported by DynamoDB (AWS), Azure Blob Storage, GCS, and Terraform Cloud
- If a lock is not released (e.g., after a crash), use `terraform force-unlock <LOCK_ID>`

## Useful State Commands

| Command | Description |
|---------|-------------|
| `terraform state list` | List all resources in state |
| `terraform state show <resource>` | Show details of a resource |
| `terraform state mv` | Move/rename a resource in state |
| `terraform state rm <resource>` | Remove a resource from state (does not destroy it) |
| `terraform apply -refresh-only` | Sync state with real infrastructure (replaces deprecated `terraform refresh`) |
| `terraform force-unlock <ID>` | Release a stuck lock |

## State Security Checklist

- Store state in a remote backend, not local filesystem
- Enable encryption at rest on the S3 bucket
- Restrict access to the state bucket with IAM policies
- Enable versioning on the S3 bucket so you can recover previous state
- Audit state access via S3 access logs or CloudTrail
- Never commit `terraform.tfstate` to version control
