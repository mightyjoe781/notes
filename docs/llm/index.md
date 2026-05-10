# LLM & AI Agents

Practical notes on using and building with large language models.

## Concepts

- [Transformer Architecture](concepts/transformers.md) - attention, layers, how LLMs are built
- [Tokenization](concepts/tokenization.md) - BPE, context windows, token cost implications
- [Training & Fine-tuning](concepts/training.md) - pre-training, SFT, RLHF, LoRA
- [RAG](concepts/rag.md) - retrieval, embeddings, chunking strategies
- [Agents](concepts/agents.md) - tool use, planning loops, memory, multi-agent patterns

## LLM System Design [🔧 WIP]

- [Introduction](design/intro.md) - What changes when LLMs enter your stack
- [LLM Infrastructure Primitives](design/primitives.md)
    - Embedding models, Vector DBs (HNSW, IVF, pgvector)
    - Context windows, token cost as a design constraint
    - LLM Gateway - routing, rate limiting, cost attribution
- [RAG Pipeline](design/rag_pipeline.md)
    - Chunking strategies, embedding, offline indexing
    - Query → retrieve → rerank → generate (online path)
    - Failure modes & evaluation (recall@k, faithfulness)
- [Enterprise Knowledge Base](design/enterprise_kb.md)
    - Multi-tenant isolation, ACL (pre vs post retrieval)
    - Freshness - re-indexing triggers, change detection
- [LLM in Data Pipelines](design/llm_data_pipeline.md)
    - Structured extraction, JSON mode, function calling
    - Idempotency, retry design, batch vs streaming
- [Agentic Systems](design/agentic_systems.md)
    - Tool use, ReAct / Plan-and-Execute loops
    - State management, blast radius control, human-in-the-loop
- [Semantic Cache](design/semantic_cache.md)
    - Similarity threshold, TTL vs change-triggered invalidation
    - Placement in the stack, hit rate vs staleness
- [Fine-tuning vs RAG](design/finetuning_vs_rag.md)
    - Decision matrix: knowledge type, update frequency, cost
    - Evaluation strategy per approach

## LLM Design Problems [🔧 WIP]

- [Document Q&A System](problems/doc_qa.md)
- [LLM Gateway for Multi-team Org](problems/llm_gateway.md)
- [Semantic Search over Product Catalog](problems/semantic_search.md)
- [AI-Powered Data Extraction Pipeline](problems/extraction_pipeline.md)
- [Coding Agent / Autonomous Task Runner](problems/coding_agent.md)

## Prompt Engineering

- [Basics](prompting/basics.md) - zero-shot, few-shot, CoT, system prompts
- [Advanced](prompting/advanced.md) - ReAct, self-consistency, structured output, extended thinking

## Tooling

- [Claude Code](tooling/claude_code.md) - Anthropic's CLI coding agent
- [GitHub Copilot](tooling/copilot.md) - VS Code AI coding assistant
