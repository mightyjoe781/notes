# Introduction to LLM System Design

> "An LLM is just another service — until you ignore what makes it different."

As the world goes through the hype cycle of AI, everyone will have media knowledge about AI. It is important to be aware important concepts and standards design being implemented everywhere in the industry.

These application of LLM are quite generic enough and useful to stay beyond the AI Hype. Traditional HLD intuitions still apply here. You still reason about latency, throughput, failure modes, and cost. What changes is _where_ the bottlenecks live and _what_ failure looks like.

A quick summary of important concepts that every developer should is as follows.
## What Changes When LLMs Enter Your Stack

In a normal service, a slow DB query or a network timeout is the problem. In an LLM system, the model itself is often the slowest, most expensive, and least deterministic component in the critical path.

Three properties make LLMs architecturally different:

**Non-determinism** - the same input can produce different outputs. You cannot cache naively. You cannot assert exact equality in tests. Evaluation requires semantic scoring, not string matching.

**Token-based cost and latency** - every call has a cost proportional to input + output tokens. A 10x increase in context length means 10x the cost and roughly 10x the latency for the first token. Context window size is a first-class design constraint, not an afterthought.

**Opaque failure** - LLMs don't throw 500 errors when they hallucinate. The system "works" but produces wrong output. You need evaluation pipelines, not just uptime monitors.

## The New Stack

A traditional backend has: client → API server → DB/cache.

An LLM-backed system adds a layer:

![](assets/Pasted%20image%2020260510183321.png)

Each of these components has HLD analogs - but each has LLM-specific failure modes and tuning knobs.

## Core Primitives

Before going into patterns, these three concepts appear in almost every design.

### Tokens and Context Windows

A **token** is roughly 0.75 words. The **context window** is the maximum token count an LLM can process in one call - both input and output combined.

|Model|Context Window|
|---|---|
|GPT-4o|128K tokens|
|Claude Sonnet|200K tokens|
|Gemini 1.5 Pro|1M tokens|

Larger context = more information per call, but also more cost and latency. Good design avoids stuffing the context window - retrieve only what is relevant.

**Token budget** is a design decision: how many tokens are reserved for system prompt, retrieved context, chat history, and output respectively.

![Token Budget](assets/Pasted%20image%2020260510183452.png)

### Embeddings

An **embedding model** converts text into a dense vector. Semantically similar text lands close together in vector space. This is the foundation of semantic search, RAG, and the semantic cache.

![Embedding Space](assets/Pasted%20image%2020260510183612.png)

Key tradeoffs when choosing an embedding model:

|Property|Consideration|
|---|---|
|Dimensionality|Higher dims = more expressive, more storage, slower ANN search|
|Model size|Larger = better quality, higher latency to embed|
|Domain fit|General-purpose vs. code vs. multilingual|
|Hosting|API (OpenAI, Voyage) vs. self-hosted (bge, nomic)|

Embedding model choice is **coupled** to the vector DB and cannot be changed without re-embedding the entire corpus - choose carefully.

### Vector Databases and ANN Search

A **vector DB** stores embeddings and answers nearest-neighbour queries: _given this query vector, find the k most similar stored vectors_.

Exact nearest-neighbour search is O(n) - too slow at scale. All production vector DBs use **Approximate Nearest Neighbour (ANN)** algorithms.

**HNSW** (Hierarchical Navigable Small World) - graph-based index. Fast queries, high memory usage. Default in Pinecone, Weaviate, Qdrant.

**IVF** (Inverted File Index) - clusters vectors, searches only relevant clusters. Lower memory, slightly less accurate. Used in FAISS.

**PQ** (Product Quantization) - compresses vectors for storage. Often combined with IVF.

|Vector DB|When to use|
|---|---|
|`pgvector`|Already on Postgres, low operational overhead, moderate scale|
|Pinecone|Managed, production scale, no infra to run|
|Qdrant|High-performance filtering + semantic search|
|Weaviate|Hybrid search (dense + sparse), rich schema support|
|FAISS|In-memory, batch offline workloads, no server needed|

> If you're already on Postgres, start with `pgvector`. Add a dedicated vector DB only when query latency or scale demands it.

## Patterns Overview

There are seven core LLM system design patterns. Each one addresses a different problem:

![Design Patterns](assets/Pasted%20image%2020260510183737.png)

These patterns compose. A production system is typically RAG + Semantic Cache + LLM Gateway at minimum.

## How to Approach an LLM Design Interview

The same framework from traditional HLD applies - but stress-test these LLM-specific dimensions at each step.

**Requirements phase** - ask about:

- Freshness: how often does the underlying knowledge change?
- Latency SLA: can the user wait 3-5s, or is this real-time?
- Cost budget: is this an internal tool or user-facing at scale?
- Accuracy bar: is a wrong answer a UX annoyance or a liability?

**Component design** - for each LLM-touching component, answer:

- What goes in the context window, and how much of it?
- What happens on a model timeout or a hallucinated output?
- How is this evaluated - what does "correct" mean here?

**Scale and cost** - LLM calls are ~100–1000x more expensive than DB reads. Always ask:

- Can this call be cached?
- Can this call be async / batched?
- Can a smaller/cheaper model handle this?

**Failure modes** - beyond uptime, consider:

- Retrieval miss (RAG returns irrelevant chunks)
- Prompt injection (user input hijacks system instructions)
- Token limit exceeded (context too large, call fails or truncates)
- Model degradation (provider silently updates a model)

---

## Further Reading

- [Anthropic Engineering Blog](https://www.anthropic.com/research) - production learnings on context window use, tool use, and evaluation
- [Building LLM Applications for Production - Chip Huyen](https://huyenchip.com/2023/04/11/llm-engineering.html) - practical overview of where LLM systems break in production; high signal
- [HNSW Algorithm Explained](https://www.pinecone.io/learn/series/faiss/hnsw/) - Pinecone's walkthrough; intuition for why graph-based ANN is fast
- [Patterns for Building LLM-based Systems & Products - Eugene Yan](https://eugeneyan.com/writing/llm-patterns/) - covers evals, RAG, guardrails, and caching with real examples