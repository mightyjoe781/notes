# Tokenization

Tokens are the basic unit LLMs operate on - not characters, not words, but subword pieces. Understanding tokenization prevents a surprising number of bugs and cost surprises.

## What Is a Token

A token is a chunk of text - typically 3-4 characters on average for English. The model never sees raw text; it sees a sequence of integer IDs.

```
"Hello, world!" -> [9906, 11, 995, 0]   (GPT-4 tokenization)
"tokenization"  -> [5263, 2065]          (split into two pieces)
"1234567"       -> [4513, 19707]         (numbers split unpredictably)
```

Common token counts:
- 1 token ~ 4 characters / ~0.75 words (English)
- 100 tokens ~ 75 words
- 1 page of text ~ 500-700 tokens

## BPE (Byte Pair Encoding)

The dominant algorithm for building a tokenizer vocabulary.

1. Start with individual characters (or bytes)
2. Repeatedly merge the most frequent adjacent pair
3. Stop when vocabulary reaches target size (e.g. 50k, 100k tokens)

Result: common words become single tokens, rare words split into subwords, unknown text falls back to byte-level pieces. This handles any language or code.

Variants used by major models:
- `tiktoken` - OpenAI's BPE implementation (GPT-3.5, GPT-4, o1)
- `SentencePiece` - Google's implementation (T5, LLaMA, Gemini)
- Anthropic uses its own BPE-based tokenizer for Claude

## Context Window

The maximum number of tokens the model can process in one call (input + output combined).

| Model | Context Window |
|---|---|
| Claude Sonnet 4.x | 200k tokens |
| GPT-4o | 128k tokens |
| Gemini 1.5 Pro | 1M tokens |
| LLaMA 3 8B | 128k tokens |

Larger context = more memory and compute cost. Most models degrade in quality near their limit - the "lost in the middle" problem where content in the middle of a long context gets less attention.

## Practical Implications

**Numbers tokenize poorly.** `9999` might be one token but `10000` might be three. Arithmetic errors in LLMs are partly a tokenization artifact.

**Code is token-dense.** Indentation, brackets, and special characters are often separate tokens. A 100-line Python file might be 500-800 tokens.

**Whitespace matters.** ` hello` (leading space) and `hello` are different tokens in most tokenizers. This matters for few-shot examples and structured output.

**Non-English is more expensive.** English text averages ~4 chars/token. CJK characters often 1-2 chars/token - 2-3x more tokens for equivalent content.

**Splitting strategy for RAG.** Chunk documents by token count, not character count, to avoid exceeding context limits silently.

## Counting Tokens

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
tokens = enc.encode("Hello, world!")
print(len(tokens))  # 4

# For Claude, use the anthropic tokenizer
import anthropic
client = anthropic.Anthropic()
response = client.messages.count_tokens(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "Hello, world!"}]
)
print(response.input_tokens)
```

## Special Tokens

Tokenizers reserve IDs for control purposes:

- `<|endoftext|>` - document separator (GPT)
- `<s>`, `</s>` - sequence start/end (LLaMA)
- `[CLS]`, `[SEP]`, `[MASK]` - BERT's classification/separation/masking tokens
- `<|im_start|>`, `<|im_end|>` - chat message boundaries (ChatML format)

Injecting these in user input can sometimes break the model's chat formatting - a class of prompt injection attacks.
