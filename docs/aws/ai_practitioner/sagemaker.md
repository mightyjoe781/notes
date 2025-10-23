# Amazon SageMaker

## Overview

- Fully managed service for developers/data scientist to build ML models
- Lifecycle of ML Service in SageMaker
    - Collect & prepare data
    - Build and train machine learning models
    - Deploy the models and monitor the performance of the prediction
- SageMaker - Built-in Algorithm (extract)
    - Supervised Algorithms
        - Linear Regression and Classification
        - KNN Algorithm (for classication)
    - Unsupervised Algorithms
        - Principle Component Analysis (PCA) ~ dimensionality reduction
        - K-means ~ find grouping within data
        - Anomaly Detection
    - Textual Algorithms - NLP, Summarization, ...
    - Image Processing ~ classification, detection

### SageMaker - AMT (Automatic Model Tuning)

- Define the Objective Matric
- AMT automatically chooses hyperparameter ranges, search strategy, maximum runtime of a tuning job, and early stop condition
- Saves you time and money
- Helps you not wasting money on suboptimal configurations

### SageMaker - Model Deployment & Inference

- Deploy with one-click, automatic scaling, no servers to manage
- Managed solution : reduced overhead
- *Real-time*
    - one prediction at a time
- *Serverless*
    - Idle period between traffic spikes
    - Can tolerate more latency (cold starts)
- *Asynchronous*
    - For large payload sizes up to 1GB
    - Long processing times
    - Near-real time latency requirements
    - Request and responses are in Amazon S3
- *Batch*
    - Prediction for an entire dataset
    - Request and responses are in S3

### SageMaker Studio

- End-to-end ML development from a unified interface
- Team collaboration
- Tune & debug ML models
- Deploy ML models
- Automated Workflows

## Data Tools

### SageMaker - Data Wrangler

- Prepare tabular and image data for machine learning
- Data preparation, transformation and feature engineering
- Single interface for data selection, cleansing, exploration, visualization, and processing
- SQL Support
- Data Quality Tool

![](assets/Pasted%20image%2020251021165614.png)

### SageMaker - Feature Store

- Ingests features from variety of sources
- Ability to define the transformation of data into feature from within Feature Store
- Can publish directly from SageMaker Data Wrangler into SageMaker Feature Store.
- Features are discoverable within SageMaker Studio

## Models and Humans
### SageMaker Clarify

- Evaluate Foundational Models
- Evaluating human-factors such as friendliness or humor
- Leverage and AWS managed team or bring your own employees
- Use built-in datasets or bring your own dataset
- Built in metric and algorithm
- Part of SageMaker Studio

### SageMaker Clarify - Detect Bias

- Ability to detect and explain biases in your datasets and models
- Measure bias using statistical metrics
- Specify input features and bais will be automatically detected

Different Types of Biases

- Sampling Bias ~ training data doesn't represent full population fairly.
- Measurement Bias : tools/measurements in data collection are skewed
- Observer bias : person collecting or interpreting has biases
- Confirmation Bias : individuals interpret or favour information that confirms their preconceptions, *Applies to human decision-making rather than automated model outputs*

### SageMaker Ground Truth

![](assets/Pasted%20image%2020251021170521.png)

- RLHF - Reinforcement Learning from Human Feedback
- Human Feedback for ML
- Reviewers : Amazon, Mechanical Turk Workers, your employees or third party vendors
- SageMaker Ground Truth Plus : Label Data
## Governance

- SageMaker Model Cards
    - Essential model information
    - Example: intended uses, risk ratings, and training details
- SageMaker Model Dashboard
    - Centralized repository
    - Information and insights for all models
- SageMaker Role Manager
    - Define roles for personas
    - Example: data scientists, MLOps engineers

## Consoles

### Model Dashboard

- Centralized portal where you can view, search and explore all of your models
- Example : track which models are deployed for inference
- Can be accessed from the SageMaker Console
- Helps you find models that violate thresholds you set for data quality, model quality, bias, explainability

### Model Monitor

- Monitor the quality of your model in production: continuous or on-schedule
- Alerts for deviations in the model quality: fix data & retrain model
- Example: loan model starts giving loans to people who don’t have the correct credit score (drift

### Model Registry

- Centralized repository allows you to track, manage, and version ML models
- Catalog models, manage model versions, associate metadata with a model
- Manage approval status of a model, automate model deployment, share models..

### SageMaker Pipelines

- SageMaker Pipeline – a workflow that automates the process of building, training, and deploying a ML model
- Continuous Integration and Continuous Delivery (CI/CD) service for Machine Learning
-  Helps you easily build, train, test, and deploy 100s of models automatically
-  Iterate faster, reduce errors (no manual steps), repeatable mechanisms…
-  Pipelines composed of Steps and each Step performs a specific task (e.g., data preprocessing, model training…)
- Supported Step Types
    - Processing
    - Training
    - Tuning
    - AutoML
    - Model
    - Clarify Check
    - Quality Check


For a full list check docs: https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html#build-and-manage-steps-types

### SageMaker JumpStart

- ML Hub to find pre-trained Foundation Model (FM), computer vision models, or natural language processing models
- Large collection of models from Hugging Face, Databricks, Meta, Stability AI…
- Models can be fully customized for your data and use-case
- Models are deployed on SageMaker directly
- Pre-built ML solutions for demand forecasting, credit rate prediction, fraud detection and computer vision

![](assets/Pasted%20image%2020251021171443.png)
### SageMaker Canvas

- Build ML models using a visual interface (no coding required)
- Access to ready-to-use models from Bedrock or JumpStart
- Build your own custom model using AutoML powered by SageMaker Autopilot
- Part of SageMaker Studio
- Leverage Data Wrangler for data preparations
- Ready to Use Models
    - From Amazon Rekognition, Amazon Comprehend, Textract
- Makes it easy to build a full ML pipeline without writing code and leveraging various AWS AI services.

### MLFlow on Amazon SageMaker

-  *MLFlow* – an open-source tool which helps ML teams manage the entire ML lifecycle
- MLFlow Tracking Servers
    - Used to track runs and experiments
    - Launch on SageMaker with a few clicks
- Fully integrated with SageMaker