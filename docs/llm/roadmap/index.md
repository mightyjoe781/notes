---
title: AI Engineering Roadmap
description: Scaffold from an external roadmap graphic (beginner to advanced) - source for future notes across the LLM section.
tags:
  - index
---

# AI Engineering Roadmap

Parked TOC from an external "AI Engineering - Beginner to Advanced" roadmap
graphic. Not distilled content yet - use this as a checklist to pull topics
into proper notes under [`llm/`](../index.md) (`concepts/`, `design/`,
`prompting/`, `tooling/`) as they get worked through. Delete sections here
once they've graduated.

## Part 1: AI Engineering First - Months 1 to 5

### Hands-on projects

- Working with the OpenAI API - production-style Python utilities on top of the OpenAI API for summarization, translation, tone control, ticket routing, and code generation
- Customer support agent - classifies tickets, retrieves help docs via RAG, drafts replies, escalates to a human when out of depth
- Exploring embeddings - semantic search, recommendation, and classification systems powered by embeddings; reasoning about the vector space
- RAG chatbot over YouTube transcripts - Pinecone-backed RAG chatbot that ingests transcripts, retrieves relevant timestamps, answers grounded in what was said
- Enterprise advanced RAG - hybrid search (BM25 + vector), cross-encoder reranking, guardrails, end-to-end RAGAS evaluation on real corporate data
- Claude Code-like coding agent - understands a codebase, inspects files, makes edits, runs commands in a sandbox, iterates on fixes for hours at a time
- AI code reviewer agent like CodeRabbit - reads every PR, flags bugs/security issues with RAG over a style guide, posts structured inline comments via the GitHub API
- Voice-based AI agent - chained voice agent (STT to LLM to TTS) that holds natural conversations, calls tools, runs as a Cursor-style voice coding assistant
- Bonus HW project: AI trading agent - ingests market data and financial news, reasons over signals via agentic RAG, proposes structured trade ideas with risk controls
- Mini project: simple neural network in TensorFlow - feedforward neural network from scratch, forward pass, training loop, evaluation
- Mini project: MNIST autoencoder - unsupervised representation learning and reconstruction, first generative model
- Developing multi-input models for OCR - multi-input PyTorch model fusing image and metadata streams, weighting losses across multiple heads
- ChatGPT-style chatbot platform - Streamlit UI, persistent multi-turn memory, web search tools, ChromaDB vector store as long-term knowledge
- Chat with any document - ChatPDF-style app turning research papers, contracts, and textbooks into a conversation grounded in their source
- AI search engine like Perplexity - agentic web retrieval, hybrid search, inline citations, streaming answers, faithfulness evaluation
- AI web app builder like Lovable/v0 - prompt-to-app system with a multi-agent pipeline (planner to coder to reviewer) shipping a working version with live preview
- AI interview taker like Mercor - conducts real technical/behavioral interviews over voice, scores candidates against a rubric with Pydantic, generates a structured post-interview hiring report

### 0. Python refresher for AI engineering

Build the Python foundation needed to work through the whole course.

- Python basics revision - variables, data types, strings, numbers, booleans; lists/tuples/sets/dicts; loops and conditionals; functions and return values; scope, imports, modules
- Pythonic data handling - list/dict comprehensions, nested dicts and JSON-like data, sorting/filtering/mapping/reducing, `None`/optional values and defaults
- Object-oriented Python - classes and objects, constructors and instance methods, inheritance and composition, dataclasses, when to use OOP in AI/backend apps
- Error handling & debugging - exceptions and `try`/`except`, custom exceptions, logging basics, debugging common Python issues, writing clean error messages
- File handling & environment setup - reading/writing files, working with JSON, working with `.env` files, virtual environments, installing packages with `pip`, project structure for Python apps
- Type hints & Pydantic basics - type hints (`str`, `int`, `float`, `bool`, `list`, `dict`), `Optional`/`Union`/custom types, function signatures with type hints, Pydantic models for request/response validation, why type safety matters in AI apps
- Async Python basics - `async`/`await`, coroutines, async API calls, running concurrent tasks, where async matters in LLM/RAG/agent apps
- Python for APIs - HTTP basics from a Python dev perspective, calling APIs with `requests`, calling APIs asynchronously with `httpx`, handling API keys securely, parsing API responses
- Python for AI workflows - working with OpenAI/Gemini/Claude-style API responses, structuring prompts and responses in Python, parsing structured outputs, building reusable utility functions, creating simple CLI-based AI tools
- Python for data & ML foundations - NumPy basics, Pandas basics, tensors intuition, loading datasets, basic plotting/inspection, why these matter before PyTorch/TensorFlow/Hugging Face

### 1. LLM mental model & API setup

Understand how LLMs work and how to start building with them.

- How LLMs work: tokens, context windows, sampling, and statelessness
- How to configure OpenAI and Google Gemini accounts
- Anatomy of an LLM API call: requests, models, responses, and parameters
- How to think about LLMs as programmable reasoning engines

### 2. Conversations & first chatbot

Build your first conversational AI application from scratch.

- Chat roles and message structure
- System prompts and prompt-level guardrails
- Multi-turn conversations and conversation history
- How to build your first end-to-end AI chatbot

### 3. Prompt engineering - foundations to advanced

Master the art and science of communicating effectively with LLMs.

- Structured outputs and custom response formats
- Conditional prompts and reusable prompt templates
- Zero-shot, one-shot, and few-shot prompting
- Chain-of-thought, self-consistency, Auto-CoT, and persona-based prompting
- Prompt serialization formats such as Alpaca, ChatML, and INST
- Context engineering as the modern AI application design paradigm
- Context window management

### 4. Real-world text tasks & chatbot development

Apply LLMs to practical text-based use cases used in real products.

- Summarization, translation, tone control, and writing improvement
- Customer support ticket routing and analysis
- Code generation, modification, and explanation
- Role-playing chatbots, learning advisors, and support assistants
- Project: Working with the OpenAI API
- Project 4A: Customer Support Agent - build a production-style AI customer support agent that classifies tickets, retrieves relevant help docs, escalates when required, and generates helpful responses

### 5. Structuring end-to-end LLM applications

Learn how to build reliable and maintainable LLM-powered applications.

- JSON outputs and structured response handling
- Error handling and exception handling in AI applications
- Batching requests for efficiency
- Rate-limit retries and token-limit management

#### 5A. FastAPI basics for AI applications

- FastAPI project setup
- Routes, request/response models, and Pydantic schemas
- Building AI API endpoints
- Error handling and environment configuration
- Connecting FastAPI with LLM workflows

### 6. Function calling & structured outputs

Teach LLMs to interact with external systems using tools and typed outputs.

- Function calling and the tools parameter
- Multiple, parallel, and forced function calls
- Calling external APIs from inside the model loop
- Enforcing structured and typed outputs using Pydantic
- Project 6A: OpenAI SDK & Claude SDK for Production AI Apps - build real applications using both OpenAI and Anthropic Claude SDKs

### 7. Embeddings & semantic search

Learn how AI applications understand meaning beyond keywords.

- How to create and use embeddings
- How to investigate and reason about vector spaces
- Semantic search and recommendation systems
- Embedding-based classification
- Project: Exploring Embeddings

### 8. Vector databases

Build storage and retrieval systems for AI-native applications.

- Vector database theory: construction, compression, and indexing
- ChromaDB end-to-end: CRUD, metadata filtering, and cost estimation
- Pinecone end-to-end: ingestion, querying, namespaces, and multitenancy
- Milvus DB overview
- Project: How to build a RAG chatbot using Pinecone and OpenAI over YouTube transcripts

### 9. Retrieval-augmented generation (RAG)

Build AI systems that can answer using private or domain-specific knowledge.

- RAG fundamentals: indexing workflow and retrieval mechanism
- Building RAG using LangChain loaders, chunking, and retrievers
- Hybrid search, reranking, and query rewriting
- RAGAS metrics and improving the "I don't know" rate
- Project 9A: Enterprise Advanced RAG with Hybrid Search, Re-Ranking & Guardrails

#### 9A. LlamaIndex for production RAG applications

- LlamaIndex fundamentals
- Data connectors, documents, nodes, and indexes
- Query engines and retrievers
- Building RAG pipelines using LlamaIndex
- When to use LlamaIndex vs LangChain

### 10. Scalable RAG with async queues

Learn how to scale RAG systems beyond simple synchronous APIs.

- Sync vs async RAG architectures
- Python RQ with Redis/Valkey on Docker
- FastAPI chat queue design: enqueue, poll, and dequeue
- Worker orchestration and horizontal scaling

### 11. Hugging Face - pre-trained models in production

Use open-source AI models in practical production workflows.

- Hugging Face Hub, datasets, inference providers, and CLI
- Accessing instruction-tuned models such as Google Gemma
- AutoModels, AutoTokenizers, and AutoClasses
- Document Q&A pipelines with PyPDF

### 12. Multi-modal AI with Hugging Face

Work with models that understand text, images, audio, and video.

- Computer vision tasks: image classification, object detection, and background removal
- Speech recognition, embeddings, denoising, and text-to-speech
- Zero-shot image and video classification using CLIP and CLAP
- Visual question answering, document VQA, diffusion, inpainting, and video models

### 13. AI agents - from first agent to multi-agent systems

Build intelligent systems that can reason, use tools, and complete multi-step tasks.

- Agentic AI fundamentals
- Building your first AI agent
- Hugging Face smolagents
- Custom tools using `@tools`
- Web search and data access tools
- Agentic RAG with stateful RAG search tools
- Multi-agent systems with specialists, coordination, and memory
- Workflow patterns: chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer
- Project 13A: AutoGen & CrewAI for Multi-Agent Applications - popular multi-agent frameworks for collaborative AI systems with specialized agents
- Project 13B: A2A Protocol & Spinning Up Subagents - A2A and subagent orchestration as a dedicated advanced section

### 14. LangGraph & stateful agent workflows

Design advanced agent workflows with state, memory, and persistence.

- LangGraph core concepts: nodes, edges, state, and StateGraph
- Designing complex agent graphs with LangChain and LCEL
- Debugging stateful agent workflows
- Checkpointing workflows with MongoDB for persistence
- Project 14A: Claude Code-like Coding Agent - build a coding agent inspired by Claude Code that can understand a codebase, inspect files, make edits, run commands, and iterate on fixes

#### 14A. LangFlow for visual AI workflow building

- Building AI workflows visually
- Connecting LLMs, prompts, tools, retrievers, and memory
- Rapid prototyping of RAG and agent workflows
- Exporting and understanding generated workflow logic
- When LangFlow is useful in real teams

### 15. The memory layer in AI agents

Give AI agents the ability to remember, retrieve, and reason across interactions.

- Short-term, long-term, factual, episodic, and semantic memory
- Mem0 setup and configuration
- Vector-database-backed memory for agents
- Deep agents and deep research agents

### 16. Graph memory & knowledge graphs

Use graph databases to build richer and more connected AI memory systems.

- Why graph memory matters for agents
- Neo4j and Kuzu for graph storage
- Cypher query basics
- Adding and testing graph memory in an AI agent

### 17. Multi-modal agents & voice agents

Build agents that can see, hear, speak, and respond across modalities.

- Multi-modal agents and image-based reasoning
- Speech-to-speech voice agents
- Chained voice agents: STT to LLM to TTS

### 18. Model Context Protocol (MCP) & agent SDK

Understand the modern tooling ecosystem around AI agents.

- What MCP is and why it matters
- MCP architecture
- Building a tiny MCP server
- Agent SDK concepts: hosted tools, function tools, and agent as a tool
- Project 18A: AI Code Reviewer Agent like CodeRabbit - build an AI code reviewer that analyzes pull requests, understands diffs, detects bugs, suggests improvements, and posts structured review comments

### 19. Streaming, retries, fallbacks & rate limits

Build robust AI APIs that work reliably in production.

- Streaming responses using Server-Sent Events (SSE)
- Exponential backoff and retry strategies
- Idempotency keys
- Token budgets
- Building a multi-provider LLM gateway with automatic fallback

### 20. Local LLM deployment

Run and deploy models locally using modern open-source tooling.

- Ollama as a local LLM runtime engine
- Dockerized LLM environments
- OpenWebUI
- Building FastAPI services on top of Ollama

### 21. Prompt caching & cost/latency optimization

Optimize AI applications for speed, cost, and scale.

- Anthropic and OpenAI prompt-caching mechanics
- Prefix-based caching and cache-friendly prompt design
- KV cache fundamentals
- Batching, prefill, and decode phases

### 22. Observability & tracing

Monitor, debug, and improve AI applications like production systems.

- Why traditional logs are not enough for agentic apps
- Langfuse, LangSmith, Braintrust, and OpenLLMetry
- OpenTelemetry GenAI semantic conventions
- Tracing model calls, tools, retrieval, and agent workflows

### 23. Evaluations - the underrated AI engineering skill

Learn how to systematically measure and improve AI application quality.

- Trace-by-hand workflow on production traces
- Failure bucketing
- Binary pass/fail evaluations
- LLM-as-judge prompts
- Achieving strong judge alignment
- The three gulfs model: comprehension, specification, and generalization
- RAGAS metrics in practice

### 24. Security, guardrails & responsible deployment

Build AI products that are safer, more reliable, and production-ready.

- OWASP Top 10 for LLM applications
- Defense-in-depth for AI systems
- Least-privilege tool design
- Schema validation
- Human-in-the-loop workflows
- NeMo Guardrails, Llama Guard, and ShieldGemma
- Prompt injection testing
- Hands-on: prompt-injecting your own agent

### 25. MLOps & LLMOps in production

Understand the complete lifecycle of deploying and maintaining AI systems.

- MLOps lifecycle, roles, deployment, monitoring, and drift
- LLMOps lifecycle: ideation, development, and operations
- Cost management and prompt compression
- Governance and production readiness
- Choosing between RAG and fine-tuning

### 26. Production best practices

Learn the final layer of practices required to ship reliable AI products.

- Moderation APIs
- Prompt-injection mitigation
- Guardrails and output validation
- Adversarial testing
- Minimizing model risks in production
- Project: AI Trading Agent - build an AI-powered trading research agent that can analyze market data, read financial news, reason over signals, and generate structured trade ideas with risk controls

## Part 2: Deep Learning Foundations - Month 6

Go deeper into the fundamentals behind modern AI systems: theory,
implementation, and understanding how models work from the inside.

### 27. Math & PyTorch foundations

Build the mathematical and programming foundation required for deep learning.

- Linear algebra, probability, statistics, and calculus
- Gradient descent
- PyTorch tensors, layers, weights, and parameters
- Training loops, optimizers, learning rate, and momentum
- Overfitting, dropout, and model evaluation with torchmetrics
- Mini project: Simple Neural Network in TensorFlow
- Mini project: MNIST Autoencoder

### 28. Robust deep learning & computer vision

Learn how to structure deep learning projects cleanly and train vision models.

- PyTorch with object-oriented programming
- Clean Dataset, DataLoader, Model, and Trainer classes
- Vanishing and exploding gradients
- ReLU vs ELU
- Batch normalization
- CNNs end-to-end
- Convolutional layers, augmentation, training, and evaluation

### 29. Sequence modeling & multi-IO architectures

Understand models that work with sequences and multiple inputs or outputs.

- RNNs, LSTMs, and GRUs
- Forecasting with RNNs
- Multi-input and multi-output architectures
- Loss weighting for complex models
- Project: Developing Multi-Input Models for OCR

### 30. Transformers from scratch

Understand the architecture that powers modern LLMs.

- Self-attention
- Positional encoding
- Multi-head attention
- Masked attention
- Full transformer architecture
- Encoder-only, decoder-only, and encoder-decoder models
- Pretraining objectives: MLM and CLM
- GPT vs BERT
- Building a custom BPE tokenizer

### 31. Deep generative models

Learn how modern generative AI models are built.

- GAN fundamentals
- Implementing a GAN for handwritten digit generation
- Variational autoencoders (VAEs)
- Training a face-generation VAE on CelebA
- TensorBoard for generative-model metrics

### 32. LLM internals - theory to match the practice

Go deeper into the engineering and architecture choices behind modern LLMs.

- KV cache
- Paged attention
- Flash attention
- Sparse attention
- Quantization
- Mixture of experts
- Distillation
- Speculative decoding
- RLHF
- Chain of thought and tree of thought
- DeepSeek architecture case study

### 33. Fine-tuning, LoRA/QLoRA & trending topics

Learn how to adapt existing models for domain-specific tasks.

- Pretraining vs fine-tuning
- When to use fine-tuning and when not to
- LoRA and QLoRA
- Parameter-efficient fine-tuning
- Hands-on fine-tuning with Unsloth
- Diffusion models
- Vision transformers
- CLIP recap

## See Also
- [LLM & AI Agents index](../index.md)
- [Agents](../concepts/agents.md)
- [RAG](../concepts/rag.md)
