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
### Guardrails



### Agents

### Pricing
