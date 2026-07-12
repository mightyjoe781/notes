---
title: Recent Databricks Platform Updates
description: Newer Databricks capabilities layered on the lakehouse - Lakeflow, Lakebase, Agent Bricks, the Genie suite, and Unity Catalog Metric Views.
tags:
  - concept
---

## Recent Platform Updates

These build on the [core lakehouse concepts](ch0.md) - product names and GA/preview status move fast, so check the linked docs for the current state.

## Lakeflow - unified data engineering

> Docs: [Lakeflow Connect](https://docs.databricks.com/aws/en/ingestion/overview) · [Lakeflow Spark Declarative Pipelines](https://docs.databricks.com/aws/en/ldp/) · [Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/) · [Lakeflow Designer](https://docs.databricks.com/aws/en/designer/what-is-lakeflow-designer)

![Lakeflow](https://www.databricks.com/sites/default/files/inline-images/lakeflow-image.png)

Lakeflow merges ingestion, transformation, and orchestration into one Unity Catalog-governed product - the successor umbrella for Delta Live Tables + Workflows + connectors.

| Component | Replaces / covers | Notes |
|---|---|---|
| **Lakeflow Connect** | Ad-hoc ingestion scripts | 100+ managed connectors (databases, SaaS apps, files); streaming ingestion via **Zerobus** |
| **Lakeflow Spark Declarative Pipelines** | Delta Live Tables (DLT) | Same declarative `@dlt.table` / `CREATE OR REFRESH LIVE TABLE` model, new name |
| **Lakeflow Jobs** | Databricks Workflows | Same orchestration engine, folded under the Lakeflow brand |
| **Lakeflow Designer** | - | No-code visual canvas for building pipelines (analyst-friendly) |
| **Genie Code** | - | AI-assisted pipeline/code generation inside the Lakeflow Pipelines Editor |

### Apache Iceberg v3 (GA)

> Docs: [Use Apache Iceberg v3 features](https://docs.databricks.com/aws/en/iceberg/iceberg-v3) · [Read Delta tables with Iceberg clients (UniForm)](https://docs.databricks.com/aws/en/delta/uniform)

Databricks tables can now be read natively by Iceberg v3 clients, on top of the existing **Delta Lake UniForm** support (see [ch4](ch4.md#delta_lake)) - one copy of Parquet data, readable by both Delta and Iceberg ecosystems without a conversion job.

## Lakebase - operational Postgres on the lakehouse

> Docs: [Lakebase Postgres overview](https://developers.databricks.com/docs/lakebase/overview) · [Lakebase Postgres (AWS)](https://docs.databricks.com/aws/en/oltp/projects/)

![Lakebase](https://www.databricks.com/sites/default/files/2026-05/01-2026-product-page-lakebase-hero-1456x564-2x.png?v=1778615586)

Fully managed, serverless **Postgres** database that lives inside a Databricks workspace, for OLTP-style workloads (app state, sessions, chat history, agent memory) alongside analytical data - not a replacement for Delta Lake.

- **Instant branching** - copy-on-write, git-style branches/snapshots created in sub-second time
- **Autoscaling to zero** - no cost when idle
- **Native Unity Catalog governance** - same permissions model as the rest of the lakehouse
- **Lakebase Search** (beta) - hybrid vector + full-text retrieval
- Cross-cloud / cross-region disaster recovery

## Agent Bricks - governed enterprise AI agents

> Docs: [Build agents on Databricks](https://docs.databricks.com/aws/en/generative-ai/agent-framework/build-agents) · [Agent Bricks](https://www.databricks.com/product/artificial-intelligence/agent-bricks)

![Agent Bricks](https://www.databricks.com/sites/default/files/2026-02/agent-bricks-header.png?v=1778700331)

Task-first platform for building, evaluating, and deploying production AI agents on top of governed lakehouse data.

- Connects LLMs to your data via **Vector Search** (retrieval), **Model Serving** (hosting), **MLflow** (tracing/eval), **Unity Catalog** (permissions/lineage)
- Model choice is open - Databricks-hosted models plus external ones (e.g. Kimi, Grok)
- Native **MCP** (Model Context Protocol) support for tool/API integration
- Works with external agent harnesses (LangGraph, CrewAI) as well as its own framework
- Automatic synthetic data generation + benchmark-driven quality optimisation
- Agent memory can be backed by Lakebase

## Genie suite - natural-language BI

> Docs: [AI/BI overview](https://docs.databricks.com/aws/en/ai-bi/) · [Genie](https://docs.databricks.com/aws/en/genie/) · [Genie Code](https://docs.databricks.com/aws/en/genie-code/)

![Genie](https://www.databricks.com/sites/default/files/inline-images/Genie-Hero-1_0.gif?v=1749163689)

Compound-AI BI layer for asking questions of governed data in natural language.

| Product | Role |
|---|---|
| **Genie One** | Business-user chat interface; answers plus generated reports/documents |
| **Genie Agents** (Spaces) | Domain-specific configuration of trusted data, metrics, and business rules that power Genie One |
| **Genie Code** | AI pair-programmer inside notebooks, SQL editor, Pipelines Editor, dashboards, MLflow |
| **Genie ZeroOps** | Background agent that monitors platform health, root-causes failures, proposes fixes in a sandbox (human-in-the-loop) |

Agent mode (GA) uses multi-step reasoning for exploratory questions, returning a report with citations, visualizations, and supporting tables.

## Unity Catalog Metric Views

> Docs: [Unity Catalog metric views](https://docs.databricks.com/aws/en/business-semantics/metric-views/)

Define a business metric (revenue, churn, active users) **once** as a governed, reusable object, then query it consistently from SQL, BI tools, APIs, and agents - instead of every team re-deriving the same KPI with slightly different SQL.

- Defined via SQL DDL or the Catalog Explorer UI (YAML spec under the hood)
- Separates *measures* from *dimensions* used to group/filter/aggregate
- Supports window measures (trailing averages, period-over-period, cumulative totals)
- Query engine can auto-rewrite to pre-aggregated materialisations for performance

## See Also

- [Databricks Hub](../index.md)
- [Databricks Platform In Depth](ch4.md) - the underlying Delta Lake / Unity Catalog / compute concepts these features build on
