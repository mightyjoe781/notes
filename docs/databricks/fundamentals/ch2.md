---
title: What is the Data Science and Engineering Workspace
description: Core Databricks workspace assets - notebooks, repos, jobs, Delta Live Tables, clusters, pools, DBFS, and Auto Loader.
tags:
  - concept
---

## Databricks Data Science and Engineering Workspace

> Docs: [Workspace](https://docs.databricks.com/aws/en/workspace/) · [Notebooks](https://docs.databricks.com/aws/en/notebooks/) · [Jobs](https://docs.databricks.com/aws/en/jobs/)

![Databricks collaborative notebooks](https://www.databricks.com/sites/default/files/2023-03/collaborativeNotebooks-heroImage.png?v=1678477276){ width="450" }

### Core assets

| Asset                             | What it is                                                                                                                                                      |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Notebooks**                     | Web-based interface for interactive code. Cells support Python, Scala, SQL, R. Attach to a cluster; run interactively or schedule as a job                      |
| **Folders**                       | File-system-like constructs for organising notebooks, files, and other assets                                                                                   |
| **Repos**                         | Git integration for version control, CI/CD, collaboration. Supports GitHub, GitLab, Bitbucket, Azure DevOps                                                     |
| **Jobs**                          | Non-interactive, scheduled or triggered task execution - notebooks, Python scripts, JARs, Scala, dbt, SQL. Supports multi-task pipelines with dependency graphs |
| **Pipelines (Delta Live Tables)** | Declarative ETL framework - a DAG that transforms source data into target datasets. Handles retries, data quality checks, incremental processing automatically  |
| **Clusters**                      | Compute for notebooks/jobs. *All-purpose*: interactive, shared. *Job clusters*: spun up per job, terminated on completion                                       |
| **Pools**                         | Idle, pre-configured instances that clusters attach to for instant node acquisition, cutting start/autoscale time                                               |

> Docs: [Delta Live Tables](https://docs.databricks.com/aws/en/ldp/) · [Clusters](https://docs.databricks.com/aws/en/compute/) · [Workflows](https://docs.databricks.com/aws/en/jobs/)

### Databricks File System (DBFS)

> Docs: [DBFS](https://docs.databricks.com/aws/en/dbfs/)

DBFS is a distributed file system abstraction mounted on the workspace, backed by cloud object storage. It provides a POSIX-like path interface (`/dbfs/...`) for accessing files from notebooks and jobs.

Databricks now steers new workloads toward **Unity Catalog volumes** for non-tabular file storage instead - governed, catalog-namespaced file paths (`/Volumes/catalog/schema/volume/...`) with the same access controls as tables. DBFS (especially DBFS mounts to external storage) is still around for existing workloads but is treated as legacy.

### Auto Loader

> Docs: [Auto Loader](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/) · [Lakeflow Connect](https://docs.databricks.com/aws/en/ingestion/overview)

![Lakeflow ingestion](https://www.databricks.com/sites/default/files/2025-06/lakeflow-hero-image-2x.png?v=1748944874)

Auto Loader incrementally and idempotently ingests new files arriving in cloud object storage (S3, ADLS, GCS) as they land - the usual entry point for streaming Bronze-layer ingestion.

- **Directory listing mode**: lists the target path incrementally each trigger - simple, fine for moderate file volumes
- **File notification mode**: event-driven via cloud pub/sub (S3 event notifications, Event Grid, Pub/Sub) - scales to billions of files without re-listing the directory
- Infers and evolves schema automatically as new columns show up, and checkpoints exactly which files were processed so streams can safely restart
- Feeds straight into Delta Live Tables / Lakeflow Declarative Pipelines; see [ch4](ch4.md#auto_loader) for the full detail and [ch5](ch5.md) for Lakeflow Connect, which layers pre-built connectors on top

## See Also

- [Databricks Platform In Depth](ch4.md) - DLT, Auto Loader, and Workflows internals
- [Recent Platform Updates](ch5.md) - Lakeflow now unifies ingestion, pipelines, and orchestration
