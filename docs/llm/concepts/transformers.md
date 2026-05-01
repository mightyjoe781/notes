# Transformer Architecture

The architecture behind every modern LLM. Introduced in the 2017 paper *Attention Is All You Need*.

## Core Idea

Before transformers, sequence models (RNNs, LSTMs) processed tokens one at a time - slow and unable to capture long-range dependencies. Transformers process all tokens in parallel and let every token attend to every other token directly.

## Self-Attention

The key operation. For each token, compute how much it should "attend to" every other token.

```
Q = query  (what am I looking for?)
K = key    (what do I offer?)
V = value  (what do I return if matched?)

Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

- `QK^T` - dot product scores how well each query matches each key
- `sqrt(d_k)` - scaling factor to prevent softmax saturation
- `softmax` - converts scores to a probability distribution (weights that sum to 1)
- Final output - weighted sum of values

## Multi-Head Attention

Run self-attention multiple times in parallel with different learned projections. Each head can specialize - one may track syntax, another coreference, another semantics.

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) * W_O
```

Typical transformer: 12-96 heads depending on model size.

## Transformer Block

One block stacks these components (repeated N times):

```
Input
  -> Multi-Head Self-Attention
  -> Add & LayerNorm            (residual connection)
  -> Feed-Forward Network       (two linear layers + activation)
  -> Add & LayerNorm
Output
```

**Residual connections** - add input back to output; prevent vanishing gradients, allow very deep stacks.
**Layer Norm** - normalize activations; stabilizes training.
**FFN** - usually 4x the model dimension; where most "knowledge" is believed to be stored.

## Positional Encoding

Self-attention is permutation-invariant - it doesn't know token order. Positional encodings inject position information.

- **Absolute (sinusoidal)** - original paper; fixed sin/cos patterns per position
- **Learned absolute** - trainable embeddings per position (GPT-2 style)
- **RoPE (Rotary)** - rotates Q/K vectors by position angle; used in LLaMA, Mistral, Gemini; extends well to longer contexts
- **ALiBi** - adds a bias to attention scores based on distance; good zero-shot length generalization

## Model Variants

| Type | Architecture | Used for | Examples |
|---|---|---|---|
| Encoder-only | Bidirectional attention | Classification, embeddings | BERT, RoBERTa |
| Decoder-only | Causal (left-to-right) attention | Text generation | GPT, LLaMA, Claude, Gemini |
| Encoder-Decoder | Encoder sees all, decoder attends to encoder | Translation, summarization | T5, BART |

Most modern chat/coding LLMs are **decoder-only** - autoregressive generation one token at a time.

## KV Cache

During inference, re-computing K and V for all previous tokens every step is wasteful. The KV cache stores them and only computes for the new token.

- Dramatically speeds up generation
- Memory cost grows with context length - a key constraint for long contexts
- Quantized KV caches (e.g. FP8) reduce memory pressure

## Mixture of Experts (MoE)

Instead of one dense FFN, use many "expert" FFNs and a learned router that activates only 1-2 per token.

- More parameters, same compute per token
- Used in GPT-4 (rumored), Mixtral, Gemini 1.5
- Trade-off: more memory to load all experts, complex load balancing

## Scaling Laws

Model performance follows predictable power laws with:
- Parameter count
- Training data size
- Compute budget (FLOPs)

Chinchilla scaling (2022): for a given compute budget, it's better to train a smaller model on more data than a larger model on less data. Most pre-Chinchilla models were undertrained.
