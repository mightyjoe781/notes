# Amazon Bedrock & Generative AI (GenAI)

![](assets/Pasted%20image%2020251008095601.png)

## Generative AI

- subset of Deep Learning
- Used to generate new data that is similar to data it was trained on.
- Foundational Model : very expensive to train models trained on huge amount of unlabelled data
- LLM : Type of AI designed to generate coherent human-like-text

## Amazon Bedrock

- Build Gen-AI application on AWS
- Fully-managed service, no servers for you to manage
- Keep control of your data used to train the model
- Pay-per-use Pricing Model
- Unified APIs
- Leverage a wide array of foundational models
- Out-of-the box features RAG, LLM Agents, ..
- Access to a wide range of Foundational Models (FM)
    - AI21labs, cohere, anthropic, meta, mistral_ai

![](assets/Pasted%20image%2020251008101049.png)

NOTE: Before using models in the Bedrock, you need to enable models.

### Foundational Model (FM)

- How to choose ?
    - Model types, performance requirements, capabilities, constraints, compliance
    - Level of customization, model size, inference options, licensing agreements, context windows, latency
    - Multimodal models (varies types of input and otuputs)
- Amazon Titan
    - High-performing foundational models from AWS
    - Image, text, multi-modal choices via a fully-managed APIs
    - Can be customized with your data
- smaller models are more cost-effective

https://aws.amazon.com/bedrock/model-choice/
### Fine-Tuning a Model

- Adapt a copy of a foundation model with your own data
- Fine-tuning will change the weights of the base foudational model
- Training data must
    - adhere to a specific format
    - be stored in Amazon S3

Types of Fine Tuning

- Instruction-based Fine Tuning
    - Improves performance of a pre-trained FM on domain specific tasks
    - further training in a domain (area of knowledge)
    - uses labeled examples ~ prompt response pairs
- Continued Pre-Training
    - provide *unlabeled* data to continue training of an FM
    - Also called as domain-adaptation fine-tuning
    - feeding entire AWS documentation to a model to make it an expert on AWS
- Single-Turn Messaging
    - Part of instruction based fine-tuning
    - *system* : context for conversation
    - *message* : An array of message objects, each containing
        - *role*, *content*
- Multi-Turn Messaging
    - provide instruction based fine tuning for a conversation
    - chatbots
    - must alternative between *user* and *assistant* roles

NOTE:

- Re-training an FM requires high budget
- Instruction-based fine-tuning is usually cheaper as computation are less intense and amount of data requires is less

#### Transfer Learning

Transfer Learning - the broader concept of reusing a pre-trained model to adapt it to a new related task

- Widely used for image classification
- And for NLP (models like BERT and GPT)

#### Use Cases

- A chatbot with persona
- Training using more up-to date data
- Training on Exclusive Data (email, messages)
- Targeted Use cases (categorisation, assessing accuracy)

### Amazon Bedrock - FM Evaluation

Automatic Evaluation

- Evaluate a model for quality control
- Built-in task types:
    - Text summarisation
    - question and answer
    - text classification
    - open-ended text generation...
- Bring your own prompt dataset or use built-in curated prompt datasets
- Scores are calculated automatically
- Model scores are calculated using various statistical methods (e.g. BERTScore, Fl...)


![](assets/Pasted%20image%2020251008104944.png)

#### Automatic Metrics to Evaluate an FM

- ROUGE : Recall-Oriented Understudy for Gisting Evaluations
- BLEU : Bilingual Evaluation Understudy
- BERTScore : semantic similarity between generated text (cosine similarity)
- Perplexity: how well model predicts next token (lower is better)
### RAG & Knowledge Bases

RAG ~ Retrieval Augmented Generation

- Allows a Foundation Model to reference a data source outside of its training data
- RAG has primary two tasks
    - Storing the information into a Vector Database (after extraction and embedding)
    - Retrieving the information from Vector database for relevant queries.

![](assets/Pasted%20image%2020251008123810.png)

- https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/

![](assets/Pasted%20image%2020251009093409.png)

RAG Vector Databases

- Amazon OpenSearch Service (service & Managed Clusters)
- Amazon Aurora PostgresSQL - relational database, proprietary on AWS
- Amazon Neptune Analytics - graph database that support GraphRAG
- Amazon S3 Vectors - cost effective and durable storage with sub-second query peformance

RAG Data Sources

- Amazon S3
- confluence
- Microsoft Share point
- Salesforce
- Web pages

Use Cases

- Customer Service Chatbot
- Legal Research and Analysis
- Healthcare Question Answering

Online Tokenizer : https://platform.openai.com/tokenizer
### Guardrails

- Control the interaction between users and Foundation Models (FMs)
- Filter undesirable and harmful content
- Remove Personally Identifiable Information (PII)
- Enhanced Privacy
- Reduce Hallucinations
- Ability to create multiple Guardrails and monitor and analyze user inputs that can violate the Guardrails

### Agents

- Manage and carry out various multi-step tasks related to infrastructure provisioning, application deployment and operational activities
- Task co-ordination; Perform tasks in the correct order and ensure information is passed correctly between tasks
- Agents are configured to perform specific pre-defined action groups
- Integrate with other systems, services, DB and API to exchange data or initiate actions
- Leverage RAG to retrieve information when necessary.

![](assets/Pasted%20image%2020251009100148.png)

### CloudWatch Integration

- Model Invocation Logging
    - Can include text, images and embeddings
    - Analyze further and build alerting thanks to Cloud Watch Logs Insights
- CloudWatch Metrics
    - Published metrics from Bedrock to CloudWatch
        - Including ContentFilteredCount, which helps to see if Guardrails are functioning
    - Can build CloudWatch Alarms on top of Metrics
### Pricing

- On-Demand
    - pay-as-you-go
    - Text Models - charges for every input/output token processed
    - Embedding Models - charged for every input token processed
    - Image Models - charged for every image generated
    - Works with Base Models only
- Batch
    - Multiple predictions at a time (output is a single file in Amazon S3)
    - Can provide discounts of up to 50%
- Provisioned Throughput
    - Purchase Model units for a certain time (I month, 6 months...)
    - Throughput - max. number of input/output tokens processed per minute
    - Works with Base, Fine-tuned, and Custom Models

### Model Improvement Techniques Cost Order

- Prompt Engineering
    - No model training needed (no additional computation or fine-tuning)
- Retrieval Augmented Generation (RAG)
    - Uses external knowledge (FM doesn't need to "know everything", less complex)
    - No FM changes (no additional computation or fine-tuning)
- Instruction-based Fine-tuning
    - FM is fine-tuned with specific instructions (requires additional computation)
- Domain Adaptation Fine-tuning
    - Model is trained on a domain-specific dataset (requires intensive computation)

### Bedrock - Cost Savings

- On-Demand - great for unpredictable workloads, no long-term commitment
- Batch - provides up to 50% discounts
- Provisioned Throughput - (usually) not a cost-saving measure, great to "reserve" capacity
- Temperature, Top K, Top P - no impact on pricing
- Model size - usually a smaller model will be cheaper (varies based on providers)
- Number of Input and Output Tokens - main driver of cost
