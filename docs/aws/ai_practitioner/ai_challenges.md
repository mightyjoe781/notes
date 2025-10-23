# AI Challenges

### Responsible AI

- Making sure AI systems are transparent and trustworthy
- Mitigating potential risk and negative outcomes
- Throughout the AI lifecycle: design, development, deployment, monitoring, evaluation

### Security

- Ensure that confidentiality, integrity, and availability are maintained
- On organizational data and information assets and infrastructure

### Governance

- Ensure to add value and manage risk in the operation of business
- Clear policies, guidelines, and oversight mechanisms to ensure AI systems align with legal and regulatory requirements
- Improve Trust

### Compliance

- Ensure adherence to regulations and guidelines
- Sensitive domains such as healthcare, finance, and legal applications

## Responsible AI
### Core Dimensions of Responsible AI

- Fairness
- Explainability
- Privacy & Security
- Transparency
- Veracity & Robustness
- Governance
- Safety
- Controllability

Responsible AI ~ AWS Services

- Amazon Bedrock : Human/Automatic Model Evaluation
- Guardrails for Amazon Bedrock
- SageMaker Clarify
- SageMaker Data Wranglers
    - Fix bias by balancing datasets
- SageMaker Model Monitor : quality analysis in production
- Amazon Augmented AI (A2I) : human review of ML Prediciton
- Governance: SageMaker Role Manager, Model Cards, Model Dashboards.

#### Human Centered Design (HCD) for Explainable AI

- Approach to design AI systems with priorities for humans' needs

### Challenges of Generative AI

- Regulatory Violations
- Social Risks
- Data security & Privacy Concerns
- Toxicity
- Hallucinations
- Plagiarism & Cheating
- Prompt Misuses
    - Poisoning
    - Hijacking/Prompt Injection
    - Exposure
    - Prompt Leaking

## Compliance
### Regulated Workflows

- Some Industries require extra level of Compliance
    - Financial Services
    - Healthcare
    - Aerospace
- Example
    - Fed Reports from Financial Institution to indicate health of bank
    - Regulated Income

### AI Standard Compliance Challenges

- Complexity and Opacity
- Dynamism and Adaptability
- Emergent Capabilities
- Unique Risks
- Algorithm accountability

### AWS Compliance

- Over 140 security standards and compliance certifications
- National Institute of Standards and Technology (NIST)
- European Union Agency for Cybersecurity (ENISA)
- International Organization for Standardization (ISO)
- AWS System and Organization Controls (SOC)
- Health Insurance Portability and Accountability Act (HIPAA)
- General Data Protection Regulation (GDPR)
- Payment Card Industry Data Security Standard (PCI DSS)

## Governance

### Importance of Governance & Compliance

- Managing, optimizing, and scaling the organizational AI initiative
- Governance is instrumental to build trust
- Ensure responsible and trustworthy AI practices
- Mitigate risks: bias, privacy violations, unintended consequences
- Establish clear policies, guidelines, and oversight mechanisms to ensure AI systems align with legal and regulatory requirements
- Protect from potential legal and reputational risks
- Foster public trust and confidence in the responsible deployment of AI
### Governance Framework

Example Approach

- *Establish an AI Governance Board or Committee*
- *Define Roles and Responsibilities*
- *Implement Policies and Procedures*

### AWS Tools for Governance

- AWS Config
- AWS Inspector
- AWS Audit Manager
- AWS Artifact
- AWS CloudTrail
- AWS Trusted Advisor

### Governance Strategies

- Policies
- Review Cadence
- Review Strategies
- Transparency Standards
- Team Training Requirements

Data Governance Strategies

- Responsible AI
- Governance Structure & Roles
- Data Sharing & Collaboration

#### Data Management Concepts

- Data Lifecycles — collection, processing, storage, consumption, archival
- Data Logging - tracking inputs, outputs, performance metrics, system events
- Data Residency - where the data is processed and stored (regulations, privacy requirements, proximity of compute and data)
- Data Monitoring - data quality, identifying anomalies, data drift
- Data Analysis - statistical analysis, data visualization, exploration
- Data Retention - regulatory requirements, historical data for training, cost

#### Data Lineage

- Source Citation
- Documenting Data Origins
- Cataloging
- Helpful for transparency, traceability and accountability

## Security and Privacy for AI Systems

- Threat Detections
- Vulnerability Management
- Infrastructure Protection
- Prompt Injection
- Data Encryption

Monitoring AI Systems

- Performance Metrics
- Infrastructure Monitoring
- Bias & Fairness, Compliance and Responsible AI

### AWS Shared Responsibility Model

![](assets/Pasted%20image%2020251021200303.png)

### Secure Data Engineering - Best Practices

- Assessing Data Quality
- Privacy-Enhancing Technologies
- Data Access Control
- Data Integrity

### Gen AI Security Scoping Matrix

- Framework designed to identify and manage security risks associated with deploying GenAI applications
- Classify your apps in 5 defined GenAI scopes, from low to high ownership

![](assets/Pasted%20image%2020251021200234.png)
### Phases of ML Project

![](assets/Pasted%20image%2020251021200103.png)
### ML Ops

- Make sure models aren’t just developed but also deployed, monitored, retrained systematically and repeatedly
- Extension of DevOps to deploy code regularly
- Key Principles
    - Version control: data, code, models could be rolled back if necessary
    - Automation: of all stages, including data ingestion, pre-processing, training, etc…
    - Continuous Integration: test models consistently
    - Continuous Delivery: of model in productions
    - Continuous Retraining
    - Continuous Monitoring