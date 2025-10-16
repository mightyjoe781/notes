# AWS Managed AI Services

### Why AWS AI Managed Service

- AWS AI services are pre-trained ML services for use-cases
- Responsiveness and Availability
- Redundancy and Regional Coverage: deployed across multiple AZs and AWS Regions
- Performance: specialized CPU and GPUs for specific use-cases for cost saving
- Token-based Pricing: pay for what you use
- Provisioned throughput: for predictable workloads, cost savings and predictable performance.

![](assets/Pasted%20image%2020251012225513.png)

## Amazon Comprehend

- For Natural Language Processing - NLP
- Fully managed and serverless service
- Uses machine learning to find insights and relationships in text
    - Language of the text
    - Extracts key phrases, places, people, brands or events
    - Understands how positive and negative text is
    - Analyzes text using tokenization and parts of speech
    - Automatically organizes a collection of text files by topics
- Sample use cases
    - Analyze Customer Interactions (emails) to find what leads to positive or negative experience

### Comprehend - Custom Classification



## Amazon Translate

## Amazon Transcribe

## Amazon Polly

## Amazon Rekognition

## Amazon Lex

## Amazon Personalize

## Amazon Textract

## Amazon Kendra

## Amazon Mechanical Turk

- Crowdsourcing marketplace to perform simple human tasks
- Distributed virtual workforce
- Example:
    - You have a dataset of 10,000,000 images and you want to labels these images
    - You distribute the task on Mechanical Turk and humans will tag those images
    - You set the reward per image (for example $0.10 per image)
- Use cases: image classification, data collection, business processing
- Integrates with Amazon A2I, SageMaker Ground Truth…

## Amazon Augment AI (A2I)

- Human oversight of ML prediction in productions
    - Can be your own employees, over 500,000 contractors from AWS or AWS Mechanical Turk
    - Some vendors are pre-screened for confidentiality requirements
- The ML model can be built on AWS or elsewhere (SageMaker; Rekognition...)

![](assets/Pasted%20image%2020251012230620.png)

## Amazon Transcribe Medical

- Automatically convert medical-related speech to text (HIPAA Compliant)
- Ability to transcribes medical terminologies such as
    - Medicine names
    - Procedures
    - Conditions and diseases
- Supports both real-time (microphone) and batch (upload files) transcriptions
- Use Cases
    - Voice applications that enable physicians to dictate medical notes
    - Transcribe phone calls that report on drug safety and side effects

## Amazon Comprehend Medical

- Amazon Comprehend Medical detects and returns useful information in unstructured clinical text
    - Physician's notes
    - Discharge Summaries
    - Test Results
    - Case notes
- Uses NLP to detect Protected Health Information (PHI) ~ DetectPHI API
- Store your documents in S3
- Analyze real-time data with Kinesis Data Firehose
- Use Amazon Transcribe to transcribe patient narratives into text that can be analyzed by Amazon Comprehend Medical

## Amazon's Hardware for AI

- GPU based EC2 instances (P3, P4, P5...)
- *AWS Trainium*
    - ML chip built to perform Deep Learning on 100B+ parameter models
    - Trn I instance has for example 16 Trainium Accelerators
    - 50% cost reduction when training a model
- *AWS Inferentia*
    - ML chip built to deliver inference at high performance and low cost
    - Inf I, Inf 2, instances are powered by AWS Inferentia
    - Upto 4x throughput and 70% cost reduction
- Trn & Inf have lowest environmental footprint