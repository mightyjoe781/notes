---
title: What is the Databricks Lakehouse Platform
description: How the lakehouse combines data warehouse and data lake strengths, the medallion architecture, and platform security and governance via Unity Catalog.
tags:
  - concept
---

## Introduction

> Docs: [Lakehouse architecture](https://docs.databricks.com/aws/en/lakehouse-architecture/) · [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)

Databricks: The Data + AI Company

- Inventor and pioneer of the data lakehouse
- Creator of highly successful open-source projects: Delta Lake, Apache Spark, and MLflow

**Why Databricks?**

1. Big data is difficult to manage - more than 80% of projects fail to manage it effectively
2. Firms need a consolidated data security policy that meets regulatory standards like GDPR and HIPAA
3. Redundant copies of the same data for different use cases make enforcing those policies harder

The Databricks Lakehouse **Platform** unifies all data in one place, built on open source standards and formats - no vendor lock-in.

## Warehouse vs. Lake vs. Lakehouse

| | Data Warehouse | Data Lake |
|---|---|---|
| Strengths | Purpose-built for BI and reporting; unifies disparate systems | Stores any kind of data cheaply; good starting point |
| Downsides | Poor support for unstructured data, data science, AI, streaming; closed/proprietary formats; expensive to scale | Complex to set up; poor BI performance; can become an unreliable "data swamp" |

**Databricks Lakehouse Platform** combines the best of both:

- Simple, open, multi-cloud
- ACID transactions and schema enforcement
- Governance support, open format
- Direct access to source data for BI
- Fully scalable, real-time collection and reporting
- Supports structured, unstructured, and semi-structured data

![Databricks Lakehouse Platform Architecture](https://www.databricks.com/sites/default/files/inline-images/marchitecture-120823.png)

## Lakehouse Components

Data lands in an organisation's open data lake. Adding **Delta Lake** on top turns it into a lakehouse.

| Delta Lake pillar | Delivers |
|---|---|
| Reliability → ACID transactions | Quality data accelerates innovation |
| Performance → Indexing | Lower TCO with a simpler architecture |
| Governance → Unity Catalog | Automation increases productivity |
| Quality → Expectations | Reduces security risk |

### Medallion architecture (data quality tiers)

- **Bronze** - raw ingestion and history (landing zone)
- **Silver** - filtered, cleaned, and augmented data
- **Gold** - aggregated, business-ready data used for reporting and ML

> Docs: [Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion)

MLflow integrates natively with the lakehouse to track experiments, manage models, and serve predictions.

## Platform Security

Databricks connects directly to your lakehouse and supports federated access (e.g. SSO). Encryption and certificate management are handled by Databricks - no manual setup required.

- Optional customer-managed VPC/VNET
- IP access lists
- Code isolation
- Private network between data plane (cloud provider) and control plane (Databricks)
- Secure cluster connectivity - no open inbound ports required

## Unity Catalog

Unity Catalog is the unified governance layer for the lakehouse.

- **Unify governance across clouds** - fine-grained governance based on ANSI SQL open standards
- **Unify data and AI assets** - centrally share, audit, secure, and manage all asset types through a single interface
- **Unify existing catalogs** - works alongside existing data/storage/catalogs, no hard migration
- **Three-level namespace** - `catalog.schema.table` organises all assets
- **Attribute-based access control** - row-level and column-level security policies
- **Data lineage** - automatic end-to-end lineage across tables, notebooks, jobs, and dashboards

## See Also

- [Databricks Platform In Depth](ch4.md) - Delta Lake and Unity Catalog internals
- [Recent Platform Updates](ch5.md) - Lakeflow, Lakebase, Agent Bricks, Genie
