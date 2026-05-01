# Retrieval-Augmented Generation (RAG)

RAG connects LLMs to external knowledge at query time. Instead of baking facts into weights (which go stale), retrieve relevant documents and include them in the prompt.

## Why RAG

- LLM knowledge has a training cutoff - RAG adds current information
- Models hallucinate facts - RAG grounds answers in real sources
- Fine-tuning is expensive for knowledge updates - RAG is just an index update
- Answers can cite sources - increases trust and verifiability

## The Basic Pipeline

```
Query -> Embed query -> Search index -> Retrieve top-k chunks -> Augment prompt -> Generate
```

```python
# Minimal RAG with LangChain
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=retriever)
result = qa.invoke("What is the refund policy?")
```

## Embeddings

Embeddings convert text into dense vectors where semantically similar text lands close together in vector space.

Popular embedding models:
- `text-embedding-3-large` (OpenAI) - 3072 dims, strong across tasks
- `voyage-3` (Anthropic/Voyage) - best for retrieval tasks
- `nomic-embed-text` (open source) - strong, runs locally
- `bge-m3` (BAAI) - multilingual, hybrid dense+sparse

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Context:\n{retrieved_docs}\n\nQuestion: {query}"}]
)
```

## Chunking

Documents must be split into chunks before indexing. Chunk strategy heavily affects retrieval quality.

| Strategy | When to use |
|---|---|
| Fixed size (512 tokens, 50 overlap) | General purpose, simple to implement |
| Sentence/paragraph boundary | Preserves natural units, better coherence |
| Recursive character splitting | Good default for mixed content |
| Semantic splitting | Groups by meaning; best quality, slower |
| Document-aware (headers, sections) | Structured docs like PDFs, markdown |

Overlap between chunks prevents relevant context from being cut at chunk boundaries.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " "]
)
chunks = splitter.split_text(document)
```

## Vector Databases

| Database | Best for |
|---|---|
| Chroma | Local dev, prototyping |
| Pinecone | Managed, production scale |
| Weaviate | Hybrid search, GraphQL API |
| Qdrant | High performance, filtering |
| pgvector | Already using PostgreSQL |
| FAISS | In-memory, no server needed |

`pgvector` is often the right choice if you already have Postgres - avoids adding another service.

## Retrieval Methods

**Dense retrieval** - embed query, find nearest vectors by cosine similarity. Good semantic match.

**Sparse retrieval (BM25)** - keyword-based TF-IDF scoring. Better for exact terms, product names, IDs.

**Hybrid retrieval** - combine dense + sparse scores. Best overall; use a reranker to merge results.

```python
# Hybrid with reciprocal rank fusion
from langchain.retrievers import EnsembleRetriever

ensemble = EnsembleRetriever(
    retrievers=[dense_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)
```

## Reranking

First retrieval returns top-k candidates (e.g. k=20). A reranker cross-encodes query+doc pairs to produce a more accurate relevance score, then you keep top-n (e.g. n=4).

Rerankers are slower but much more accurate than embedding similarity alone.

- `cross-encoder/ms-marco-MiniLM-L-6-v2` - fast, open source
- Cohere Rerank API - strong, managed
- Voyage Rerank - best quality

## Advanced RAG Patterns

**HyDE (Hypothetical Document Embeddings)** - generate a hypothetical answer first, embed that, retrieve on the embedding. Bridges vocabulary gap between short queries and long documents.

**Self-RAG** - model decides when to retrieve (not every query needs retrieval), critiques retrieved docs, and reflects on its output quality.

**Contextual compression** - before adding to prompt, compress each retrieved chunk to only the part relevant to the query. Saves tokens.

**Multi-query retrieval** - generate multiple phrasings of the query, retrieve for each, deduplicate. Improves recall.

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=ChatOpenAI()
)
```

## Common Failure Modes

- **Retrieval misses** - query phrasing doesn't match chunk phrasing; fix with hybrid search or HyDE
- **Context too diluted** - too many chunks in prompt; use reranking + fewer top-k
- **Chunk boundary cuts context** - increase overlap or use semantic chunking
- **Stale index** - documents updated but index not; build incremental update pipeline
- **Lost in the middle** - model ignores middle chunks in long context; put most relevant chunks first and last
