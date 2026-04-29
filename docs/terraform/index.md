# Terraform

Terraform is an open-source Infrastructure as Code (IaC) tool by HashiCorp. It lets you define, provision, and manage cloud infrastructure using a declarative language called HCL (HashiCorp Configuration Language). Terraform is written in Go and uses graph theory to resolve resource dependencies automatically.

## Learning Path

**Beginner:** [Introduction](introduction.md) -> [Core Concepts](core-concepts.md) -> [Variables and Outputs](variables-and-outputs.md) -> [State](state.md) -> [Workflow](workflow.md)

**Intermediate:** [Modules](modules.md) -> [Advanced HCL](advanced-hcl.md) -> [Provisioners](provisioners.md)

**Exam / Enterprise:** [Cloud and Enterprise](cloud-and-enterprise.md) -> [What's New](whats-new.md)

## Table of Contents

| File                                              | Topics Covered                                           |
| ------------------------------------------------- | -------------------------------------------------------- |
| [Introduction](introduction.md)                   | IaC overview, HCL syntax, file structure, root module    |
| [Core Concepts](core-concepts.md)                 | Providers, resources, data sources, dependencies         |
| [Variables and Outputs](variables-and-outputs.md) | Variable types, precedence, outputs, splat expressions   |
| [State](state.md)                                 | Local state, remote backends, S3 + DynamoDB, locking     |
| [Workflow](workflow.md)                           | CLI commands, AWS auth, debugging with TF_LOG            |
| [Modules](modules.md)                             | Root/child modules, sources, versioning, local values    |
| [Advanced HCL](advanced-hcl.md)                   | Functions, conditionals, count, for_each, dynamic blocks |
| [Provisioners](provisioners.md)                   | local-exec, remote-exec, failure behavior                |
| [Cloud and Enterprise](cloud-and-enterprise.md)   | Workspaces, organizations, Sentinel, Terraform Cloud     |
| [What's New](whats-new.md)                        | Deprecated features, breaking changes, migration notes   |

## Resources

- Practice repo: [cloudacademy/terraform-aws](https://github.com/cloudacademy/terraform-aws/)
- Module registry: [registry.terraform.io](https://registry.terraform.io)
- Docs: [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform)
