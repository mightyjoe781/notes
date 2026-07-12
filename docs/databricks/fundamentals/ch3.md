---
title: What is Databricks Machine Learning
description: The Databricks ML lifecycle - common challenges, MLflow components, AutoML, Feature Store, and ML workflows.
tags:
  - concept
---

## Databricks Machine Learning

> Docs: [Databricks Machine Learning](https://docs.databricks.com/aws/en/machine-learning/) · [MLflow](https://docs.databricks.com/aws/en/mlflow/)

![Databricks Machine Learning](https://www.databricks.com/sites/default/files/2025-11/hero-image-1280x329-2x.jpg?v=1763066560)

Databricks ML manages the end-to-end machine learning lifecycle - from data preparation to model deployment.

- Production ML depends on both code and data
- Requires many roles: data engineers, data scientists, ML engineers, business stakeholders
- Requires integrating many components: feature engineering, training, evaluation, deployment, monitoring

### Common ML challenges

- **Data quality** - issues during storage, loading, or transformation
- **Compute resources** - managing autoscaling, GPU clusters, and cost
- **Feature development** - preparing consistent features for training and inference
- **Model development** - experiment tracking, hyperparameter tuning
- **Governance and security** - access restrictions and compliance policies
- **ML operations** - model serving, deployment pipelines, monitoring
- **Automation** - triggering retraining on data drift or schedule

### MLflow components

MLflow is the open-source ML lifecycle platform natively integrated with Databricks.

| Component | Purpose |
|---|---|
| **Tracking** | Log and compare metrics, parameters, and artifacts across model runs |
| **Models** | Manage and deploy models from various ML libraries (scikit-learn, PyTorch, TensorFlow) to diverse serving platforms |
| **Projects** | Package ML code in a reusable, reproducible format for sharing |
| **Model Registry** | Centralised model store - staging, production, and archival transitions |
| **Model Serving** | Host MLflow models as REST endpoints for real-time inference |

### Databricks AutoML

> Docs: [AutoML](https://docs.databricks.com/aws/en/machine-learning/automl/)

Given a dataset and a target column, AutoML:

- Runs trials with different algorithms and hyperparameters
- Generates editable Python notebooks per trial so you can inspect and customise the approach
- Supports classification, regression, and forecasting tasks

### Feature Store

> Docs: [Feature Engineering](https://docs.databricks.com/aws/en/machine-learning/feature-store/)

Centralised repository for creating, storing, and sharing ML features.

- Written once, reused across training and inference pipelines
- Automatically tracks lineage between features and the models that use them
- Supports point-in-time lookups to prevent data leakage during training

### Databricks Workflows for ML

- Run ML pipelines non-interactively on a schedule or on-demand
- Automate retraining, evaluation, and promotion workflows
- Full control over the execution environment (cluster type, dependencies)

### Databricks Repos

- Synchronise projects with Git repositories (GitHub, GitLab, Bitbucket, Azure DevOps)
- Collaborate across workspaces and development environments
- Enables CI/CD patterns for ML pipelines

## See Also

- [Databricks Platform In Depth](ch4.md) - MLflow, AutoML, and Feature Store internals
- [Recent Platform Updates](ch5.md) - Agent Bricks for building governed AI agents on top of this ML stack
