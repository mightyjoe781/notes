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

- Organize documents into categories that you define
- Ex ~ categorize customer emails so that you can provide guidance based on type of request
- Support for different types of documents.

![](assets/Pasted%20image%2020251019223645.png)
### Named Entity Recognition (NER)

- NER ~ Extracts predefined, general-purpose entities like people, places, organizations, dates and other standard categories, from *text*
- Comprehend supports for Custom Entity Recognition
## Amazon Translate

- Natural and accurate language translation
- Amazon Translate allows you to localize content ~ such as website and applications for international users.
- Easily Translate large volume of text efficiently
## Amazon Transcribe

- Automatically convert speech to text
- Uses a deep learning process called automatic speech recognition (ASR) to convert speech to text quickly and accurately.
- Automatic PII data removal using redaction
- Use cases
    - transcribe customer service calls
    - automate closed captioning and subtitling
    - generate metadata for media assets to create a fully searchable archive

### Transcribe Improving Accuracy

- allows transcribe to capture domain specific or non standard terms
- Custom Vocabularies (for words)
- Custom Language Models (for context)
- NOTE: use both for highest transcription accuracy

## Amazon Polly

- Turn text into lifelike speech using deep learning
- Allowing to create applications that talk
- Advanced Features
    - Lexicons
    - SSML ~ Speech Synthesis Markup Language
    - Voice engine : generative, long-form, neutral, standard
    - Speech mark
        - encode where a sentence starts and ends in the audio.

## Amazon Rekognition

- Find objects, people, text, scenes in images and videos using ML
- Facial analysis and facial search to do user verification, people counting
- Create a database of *familiar faces* or compare against celebrities
- Use Cases
    - Labeling
    - Content Moderation
    - Text Detection
    - Face Detection
    - Face Search and Verification
    - Pathing

#### Content Moderation API Example

![](assets/Pasted%20image%2020251019225806.png)
## Amazon Lex

- Build Chatbots quickly for your application using voice and text
- Example ~ chatbot ordering pizza or book a hotel
- supports multiple languages
- Integration with AWS Lambda, Comprehend, Connect, Kendra
- The bot automatically understands the user intent to invoke the correct lambda function to *fulfill the intent*

## Amazon Personalize

- Fully managed ML-service to build apps with real-time personalized recommendations
- Example ~ personalized product recommendations
- Same technology used by `amazon.com`
- Integrates into existing website, application, SMS, etc..
- Implement in days, not months
- Use cases retail stores, media and entertainment.

![](assets/Pasted%20image%2020251019230633.png)

- Amazon Personalize Recipes are multiple ways to extract different types of recommendations based on algorithms.
## Amazon Textract

- Automatically extracts text, handwriting, and data from any scanned documents using Al and ML

![](assets/Pasted%20image%2020251019230706.png)

- Extract data from forms and tables
- Read and process any type of document (PDFs, images, ...)
- Use cases:
    - Financial Service
    - Healthcare
    - Public Sector

## Amazon Kendra

- Fully managed document search service powered by ML
- Extract answers from within a document (text, pdf, HTML, etc..)
- Natural language search capabilities
- Learn from user interactions/feedback to promote preferred results (Incremental Learning)
- Ability to manually fine-tune search results (importance of data, freshness, custom, ...)

![](assets/Pasted%20image%2020251019230943.png)
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