# What's New - Changes and Deprecations

Track breaking changes, deprecated features, and migration notes here as Terraform and its providers evolve.

## Terraform Core

### Terraform 1.x

| Change | Old | New | Notes |
|--------|-----|-----|-------|
| `terraform refresh` deprecated | `terraform refresh` | `terraform apply -refresh-only` | The standalone `refresh` command still works but prints a deprecation warning |
| Interpolation syntax | `"${var.name}"` (required) | `var.name` (direct) | String interpolation `${}` is still valid inside strings like `"prefix-${var.name}"` |
| `terraform.tfstate.d/` | Only in Terraform Cloud | Also local CLI workspaces | Each workspace stores state here when using local backend |

### Terraform >= 0.12

- Direct variable reference: use `var.name` instead of `"${var.name}"` outside strings
- Proper type system: `string`, `number`, `bool`, `list`, `map`, `set`, `tuple`, `object`
- HCL2 (HashiCorp Configuration Language v2) with first-class expressions

## AWS Provider

### v4.x and v5.x Breaking Changes

| Resource | Change | Old | New |
|----------|--------|-----|-----|
| `aws_eip` | `vpc` attribute removed | `vpc = true` | `domain = "vpc"` (or omit - VPC is now the default) |
| `aws_s3_bucket` | `acl` attribute removed | `acl = "private"` | Use separate `aws_s3_bucket_acl` resource |
| `aws_s3_bucket` | `policy` attribute removed | `policy = ...` | Use separate `aws_s3_bucket_policy` resource |
| `aws_s3_bucket` | `logging` block removed | `logging { ... }` | Use separate `aws_s3_bucket_logging` resource |
| `aws_s3_bucket` | `website` block removed | `website { ... }` | Use separate `aws_s3_bucket_website_configuration` resource |

### Amazon Linux

| Change | Old | New | Notes |
|--------|-----|-----|-------|
| Package manager | `amazon-linux-extras` | `dnf` | `amazon-linux-extras` removed in Amazon Linux 2023 |

```bash
# Old (Amazon Linux 2 only)
sudo amazon-linux-extras install -y nginx1

# New (Amazon Linux 2023+)
sudo dnf install -y nginx
```

### Ubuntu AMI Filter

Use Ubuntu 22.04 (Jammy) or 24.04 (Noble) instead of 18.04 (Bionic - EOL April 2023).

```hcl
# Ubuntu 22.04 (Jammy)
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
```

## Deprecation Checklist

When setting up a new project, check for these common mistakes from older tutorials:

- [ ] `aws_eip.vpc = true` - replace with `domain = "vpc"`
- [ ] `aws_s3_bucket.acl` - use `aws_s3_bucket_acl` resource
- [ ] `terraform refresh` - use `terraform apply -refresh-only`
- [ ] `amazon-linux-extras` in `remote-exec` - use `dnf` on AL2023
- [ ] Ubuntu 18.04 / 20.04 AMI filters - update to 22.04 or 24.04
- [ ] AWS provider version `~> 3.x` or `~> 4.x` - update to `~> 5.0`
- [ ] `"${var.name}"` outside strings - simplify to `var.name`
