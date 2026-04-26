## Databricks Platform In Depth

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

- **Bronze** — raw ingestion, exact copy of source, full history retained
- **Silver** — cleaned, filtered, and enriched; joins and light transformations applied
- **Gold** — aggregated, business-ready tables used for dashboards, reporting, and ML training

### Delta Lake

Delta Lake is the open-source storage layer underneath all Databricks tables.

- **ACID transactions**: safe concurrent reads and writes using optimistic concurrency control
- **Schema enforcement**: rejects writes that violate the table schema; `MERGE SCHEMA` opt-in for evolution
- **Time travel**: query past snapshots with `VERSION AS OF n` or `TIMESTAMP AS OF 'date'`
- **`OPTIMIZE`**: compacts small files into larger ones for faster reads
- **Z-ordering**: co-locates related data within files to minimise data scanned per query
- **`VACUUM`**: removes files no longer in the transaction log; default 7-day retention window
- **Change Data Feed (CDF)**: exposes row-level change events (insert/update/delete) for downstream consumers

### Unity Catalog

Unity Catalog is the unified governance layer — one place to manage access, lineage, and discovery across all clouds and workspaces.

**Namespace**: `catalog.schema.table` — three levels. Catalogs group schemas; schemas group tables, views, and functions.

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
- **Job clusters**: created per job run, terminated on completion — most cost-efficient
- **Pools**: pre-warmed idle instances; clusters acquire nodes from a pool to cut start times

**Photon Engine**

Databricks' native vectorized query engine written in C++. Drop-in replacement for Spark execution — no API changes. Biggest gains on wide table scans, aggregations, and joins. Enabled by default on SQL Warehouses.

**Serverless Compute**

Removes infrastructure management entirely; Databricks provisions and scales compute automatically.

- **Serverless SQL Warehouses**: start in seconds, billed per second of use
- **Serverless Jobs**: job and pipeline tasks run without configuring a cluster
- No idle cluster costs — compute shuts down immediately when not in use

### Delta Live Tables (DLT)

Declarative ETL framework built on Delta Lake. You define *what* the data should look like; DLT figures out *how* to compute and refresh it.

- Python: `@dlt.table` decorator; SQL: `CREATE OR REFRESH LIVE TABLE`
- Handles dependency ordering, retries, and incremental processing automatically
- **Expectations**: data quality rules declared inline — failing rows can be dropped, quarantined, or flagged
- **Streaming tables**: append-only, incrementally updated from a streaming source
- **Materialised views**: recomputed when upstream data changes
- Two pipeline modes: *development* (stop on error, keep cluster running) vs *production* (retry on error, terminate on completion)

### Auto Loader

Incrementally ingests new files arriving in cloud storage (`cloudFiles` source).

- Formats: JSON, CSV, Parquet, Avro, ORC, text, binary
- **Directory listing mode**: simple, scans the path periodically
- **File notification mode**: event-driven via cloud pub/sub — scales to billions of files
- Checkpoint tracks exactly which files have been processed; safe to restart
- First-class integration with Delta Live Tables

### Databricks Workflows

Orchestrate multi-step data pipelines as jobs.

- Task types: notebook, Python script, JAR, SQL, dbt, DLT pipeline, another job
- Define task dependencies; Databricks parallelises independent tasks automatically
- **Repair and rerun**: retry only failed tasks without re-running successful ones
- Trigger modes: scheduled (cron), continuous, file arrival, or API call
- Job clusters are created per run and terminated on completion

### Machine Learning

**MLflow**

Native open-source ML lifecycle platform.

- **Tracking**: log runs with metrics, parameters, tags, and artifacts for comparison
- **Model Registry**: versioned model store with stage transitions (Staging → Production → Archived)
- **Model Serving**: deploy registered models as low-latency REST endpoints with auto-scaling
- **Projects**: reproducible ML code packaging

**AutoML**

Point AutoML at a labelled dataset and it generates a ranked set of baseline models.

- Supports classification, regression, and forecasting
- Produces fully editable notebooks for every trial — transparent, not a black box
- Results logged to MLflow automatically

**Feature Store**

Centralised repository for ML features.

- Write features once, reuse across training and inference without duplication
- Automatic lineage between features and models
- Point-in-time lookups prevent data leakage during training

### Databricks Apps

Build and host data applications (Streamlit, Dash, Gradio, or any Python web framework) directly inside a Databricks workspace.

- Apps run within the workspace security perimeter with direct access to Unity Catalog
- No separate infrastructure — deployed and versioned via the UI or CLI

### Databricks Asset Bundles (DABs)

Infrastructure-as-code for Databricks resources.

- Define jobs, pipelines, clusters, SQL warehouses, and permissions in YAML
- `databricks bundle validate` → `databricks bundle deploy` workflow
- Parameterised targets for dev/staging/prod environments
- The modern replacement for `dbx` and older Databricks CLI deployment patterns
