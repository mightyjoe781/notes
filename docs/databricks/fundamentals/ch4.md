---
title: Databricks Platform In Depth - Lakehouse, Delta Lake, and Compute
description: Deep dive into the lakehouse architecture, Delta Lake internals, Unity Catalog, compute options, Delta Live Tables, Auto Loader, Workflows, MLflow, Apps, and Asset Bundles.
tags:
  - concept
---

## Databricks Platform In Depth

> Docs: [Delta Lake](https://docs.databricks.com/aws/en/delta/) · [Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/) · [Compute](https://docs.databricks.com/aws/en/compute/)

### The Lakehouse Platform

Traditional architectures force a choice between a data warehouse (great for BI, poor for AI/unstructured data) and a data lake (cheap and flexible, but unreliable without careful management). The lakehouse unifies both.

| | Data Warehouse | Data Lake | Lakehouse |
|---|---|---|---|
| Storage cost | High | Low | Low |
| Structured data | ✓ | ✓ | ✓ |
| Unstructured / semi-structured | ✗ | ✓ | ✓ |
| ACID transactions | ✓ | ✗ | ✓ |
| BI & reporting | ✓ | Poor | ✓ |
| ML & AI | Poor | ✓ | ✓ |
| Open formats | ✗ | ✓ | ✓ |

The lakehouse is built on **Delta Lake** (open-source) sitting on top of cloud object storage. Databricks adds governance (Unity Catalog), compute (Photon, serverless), and tooling (Workflows, DLT, MLflow) on top.

### Medallion Architecture

Data quality tiers used to progressively refine data as it moves through the pipeline:

- **Bronze** - raw ingestion, exact copy of source, full history retained
- **Silver** - cleaned, filtered, and enriched; joins and light transformations applied
- **Gold** - aggregated, business-ready tables used for dashboards, reporting, and ML training

### Delta Lake

> Docs: [Delta Lake](https://docs.databricks.com/aws/en/delta/) · [Delta table Z-ordering & OPTIMIZE](https://docs.databricks.com/aws/en/delta/optimize) · [UniForm (Iceberg compatibility)](https://docs.databricks.com/aws/en/delta/uniform)

![Delta Lake](https://www.databricks.com/sites/default/files/2025-05/header-lakehouse-storage.png?v=1747675003)

Delta Lake is the open-source storage layer underneath all Databricks tables - Parquet files plus a JSON/Parquet **transaction log** that records every write.

**Delta tables** (what you actually query as `catalog.schema.table`) get, for free:

- **ACID transactions** - safe concurrent reads and writes using optimistic concurrency control
- **Schema enforcement** - rejects writes that violate the table schema; `MERGE SCHEMA` opt-in for evolution
- **Time travel** - query past snapshots with `VERSION AS OF n` or `TIMESTAMP AS OF 'date'`, restorable via `RESTORE TABLE`
- **`OPTIMIZE`** - compacts small files into larger ones for faster reads (small-file problem from many incremental writes)
- **Z-ordering** - co-locates related data within files on the sort columns you query most, minimising data scanned
- **`VACUUM`** - removes files no longer referenced by the transaction log; default 7-day retention window
- **Change Data Feed (CDF)** - exposes row-level change events (insert/update/delete) for downstream consumers (e.g. incremental Silver/Gold builds)

**Delta Live Tables (DLT)** - now branded **Lakeflow Spark Declarative Pipelines** (see below) - is the framework for *building and refreshing* Delta tables declaratively, whereas "Delta table" is just the storage format itself; you can write to Delta tables directly with plain Spark SQL/DataFrame writes too.

**Interoperability - UniForm & Apache Iceberg**

Delta UniForm generates Iceberg (and Hudi) metadata alongside the existing Delta log, over the *same* Parquet files - no duplicate storage, negligible write overhead. This lets Iceberg-only engines (Snowflake, BigQuery, Redshift, Athena) read a Delta table without a conversion job. Databricks also added native **Apache Iceberg v3** read/write support - see [Recent Platform Updates](ch5.md#apache_iceberg_v3_ga).

### Unity Catalog

![Unity Catalog](https://www.databricks.com/sites/default/files/2026-06/unity-catalog-header-image.png?v=1781204795)

Unity Catalog is the unified governance layer - one place to manage access, lineage, and discovery across all clouds and workspaces.

**Namespace**: `catalog.schema.table` - three levels. Catalogs group schemas; schemas group tables, views, and functions.

- **Metastore**: top-level container, one per region; workspaces attach to a metastore
- **Managed tables**: data stored and fully managed inside Unity Catalog storage
- **External tables**: data stored at a user-defined cloud path, registered in Unity Catalog
- **External locations**: map S3/ADLS/GCS paths using storage credentials
- **Row and column-level security**: row filters and column masks applied transparently at query time
- **Data lineage**: automatic end-to-end lineage captured across notebooks, jobs, SQL, and dashboards
- **System tables**: audit logs, billing, lineage, and more as queryable SQL tables under `system.*`

### Compute

**Clusters**

- **All-purpose clusters**: long-lived, shared interactive use (notebooks)
- **Job clusters**: created per job run, terminated on completion - most cost-efficient
- **Pools**: pre-warmed idle instances; clusters acquire nodes from a pool to cut start times

**Photon Engine**

> Docs: [Photon](https://docs.databricks.com/aws/en/compute/photon)

![Photon](https://www.databricks.com/sites/default/files/2023-03/photon-hero.png?v=1678143313){ width="400" }

Databricks' native vectorized query engine written in C++. Drop-in replacement for Spark execution - no API changes. Biggest gains on wide table scans, aggregations, and joins. Enabled by default on SQL Warehouses.

**Adaptive Query Execution (AQE)**

> Docs: [Adaptive query execution](https://docs.databricks.com/aws/en/optimizations/aqe)

Spark/Photon re-optimises a query plan *during* execution, using accurate runtime statistics gathered after each shuffle/broadcast exchange - instead of relying only on stale pre-execution estimates. Enabled by default. Four main behaviours:

- **Dynamic partition coalescing** ("adaptive partitioning") - merges many small post-shuffle partitions into fewer, reasonably-sized ones, since tiny tasks waste time on scheduling/setup overhead relative to actual I/O
- **Join strategy switching** - converts a sort-merge join into a broadcast hash join at runtime if one side turns out to be small enough
- **Skew join handling** - splits oversized skewed partitions so one hot key doesn't bottleneck a whole stage
- **Empty relation detection** - short-circuits joins/aggregations known to produce no rows

**Serverless Compute**

Removes infrastructure management entirely; Databricks provisions and scales compute automatically.

- **Serverless SQL Warehouses**: start in seconds, billed per second of use
- **Serverless Jobs**: job and pipeline tasks run without configuring a cluster
- No idle cluster costs - compute shuts down immediately when not in use

### Delta Live Tables (DLT)

> Docs: [Lakeflow Spark Declarative Pipelines](https://docs.databricks.com/aws/en/ldp/) (DLT was renamed/absorbed into Lakeflow - see [ch5](ch5.md))

![Lakeflow Declarative Pipelines](https://www.databricks.com/sites/default/files/2025-06/Lakedflow-declarative-pipelines-hero.png?v=1748976836)

Declarative ETL framework built on Delta Lake. You define *what* the data should look like; DLT figures out *how* to compute, order, and refresh it - as opposed to a plain Delta table, which just stores whatever you explicitly write to it with no built-in orchestration.

- Python: `@dlt.table` decorator; SQL: `CREATE OR REFRESH LIVE TABLE`
- Builds a dependency graph automatically from table references in your code; handles ordering, retries, and incremental processing
- **Expectations**: data quality rules declared inline - failing rows can be dropped, quarantined, or flagged, without hand-written validation logic
- **Streaming tables**: append-only, incrementally updated from a streaming source (e.g. Auto Loader, Kafka)
- **Materialised views**: batch tables recomputed (fully or incrementally) whenever upstream data changes
- Two pipeline modes: *development* (stop on error, keep cluster running for fast iteration) vs *production* (retry on error, terminate on completion to save cost)

### Auto Loader

> Docs: [Auto Loader](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/) · [Schema inference & evolution](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/schema)

Incrementally and idempotently ingests new files arriving in cloud object storage - the standard entry point for streaming Bronze-layer ingestion. Read as a Spark Structured Streaming source via `cloudFiles`.

- Formats: JSON, CSV, Parquet, Avro, ORC, text, binary
- **Directory listing mode**: simple, lists the target path incrementally on each trigger; fine for lower file volumes
- **File notification mode**: event-driven via cloud pub/sub (S3 events, Event Grid, Pub/Sub) - scales to billions of files without repeatedly re-listing the directory
- **Schema inference & evolution**: infers schema from a sample of files and stores it at `cloudFiles.schemaLocation`; when a genuinely new column shows up mid-stream it fails fast with `UnknownFieldException`, merges the new column into the stored schema, then resumes
- **Checkpointing**: tracks exactly which files have been processed (RocksDB-backed), so the stream can safely stop/restart without re-reading or skipping files
- First-class integration with Delta Live Tables/Lakeflow Declarative Pipelines; superseded on the marketing side by **Lakeflow Connect** for pre-built connectors (see [ch5](ch5.md)), but the `cloudFiles` source itself is unchanged

### Databricks Workflows

> Docs: [Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/)

![Databricks Workflows](https://www.databricks.com/sites/default/files/2025-05/hero-image-databricks-workflows_0.png?v=1747942666)

Orchestrate multi-step data pipelines as jobs.

- Task types: notebook, Python script, JAR, SQL, dbt, DLT pipeline, another job
- Define task dependencies; Databricks parallelises independent tasks automatically
- **Repair and rerun**: retry only failed tasks without re-running successful ones
- Trigger modes: scheduled (cron), continuous, file arrival, or API call
- Job clusters are created per run and terminated on completion

### Machine Learning

**MLflow**

![MLflow](https://www.databricks.com/sites/default/files/2023-03/managedmlfow-header.svg?v=1678448848)

Native open-source ML lifecycle platform.

- **Tracking**: log runs with metrics, parameters, tags, and artifacts for comparison
- **Model Registry**: versioned model store with stage transitions (Staging → Production → Archived)
- **Model Serving**: deploy registered models as low-latency REST endpoints with auto-scaling
- **Projects**: reproducible ML code packaging

**AutoML**

Point AutoML at a labelled dataset and it generates a ranked set of baseline models.

- Supports classification, regression, and forecasting
- Produces fully editable notebooks for every trial - transparent, not a black box
- Results logged to MLflow automatically

**Feature Store**

![Feature Store](https://www.databricks.com/sites/default/files/2021/12/feature-store-img-1.png?v=1660758008){ width="400" }

Centralised repository for ML features.

- Write features once, reuse across training and inference without duplication
- Automatic lineage between features and models
- Point-in-time lookups prevent data leakage during training

### Databricks Apps

Build and host data applications (Streamlit, Dash, Gradio, or any Python web framework) directly inside a Databricks workspace.

- Apps run within the workspace security perimeter with direct access to Unity Catalog
- No separate infrastructure - deployed and versioned via the UI or CLI

### Databricks Asset Bundles (DABs)

Infrastructure-as-code for Databricks resources.

- Define jobs, pipelines, clusters, SQL warehouses, and permissions in YAML
- `databricks bundle validate` → `databricks bundle deploy` workflow
- Parameterised targets for dev/staging/prod environments
- The modern replacement for `dbx` and older Databricks CLI deployment patterns

## See Also

- [PySpark Notes Hub](../../pyspark/index.md) - Spark internals that Photon and Databricks clusters run on
- [Scalability](../../sd/topics/core/scalability.md)
