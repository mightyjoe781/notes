# Training & Fine-tuning

How LLMs go from random weights to useful assistants - and how to adapt them for specific tasks.

## Stage 1: Pre-training

Train on massive text corpora (trillions of tokens) using next-token prediction. The model learns language, facts, reasoning patterns, and code by trying to predict what comes next.

```
Loss = -log P(next_token | all_previous_tokens)
```

This is self-supervised - no labels needed, just raw text. The internet is the training set.

Scale required: GPT-3 used 45TB of text, 3.5 months on 10k GPUs. Pre-training is done once by the model provider; you almost never do this yourself.

## Stage 2: Supervised Fine-tuning (SFT)

Take the pre-trained model and train it on (prompt, ideal response) pairs. Teaches the model to follow instructions rather than just predict text.

```
Dataset format:
[
  {"prompt": "Summarize this article: ...", "response": "The article discusses..."},
  {"prompt": "Write a Python function that...", "response": "def ..."},
  ...
]
```

Typically 10k-1M high-quality examples. Quality matters far more than quantity. SFT converts a "text predictor" into an "instruction follower".

## Stage 3: Alignment (RLHF / DPO)

Fine-tuning alone doesn't make models helpful and safe. Alignment trains the model to produce outputs humans prefer.

### RLHF (Reinforcement Learning from Human Feedback)

1. Collect human comparisons: for the same prompt, which response is better?
2. Train a **reward model** to predict human preference scores
3. Use PPO (a RL algorithm) to optimize the LLM to maximize reward

Complex to implement, training can be unstable. Used by early ChatGPT and InstructGPT.

### DPO (Direct Preference Optimization)

Skips the reward model - directly fine-tunes on (prompt, chosen, rejected) triples. Simpler, more stable, comparable results.

```python
# DPO dataset format
{
  "prompt": "Explain recursion",
  "chosen": "Recursion is when a function calls itself...",
  "rejected": "Recursion is a computer thing..."
}
```

Most models released after 2024 use DPO or a variant.

### Constitutional AI (Anthropic)

Claude is trained with Constitutional AI: rather than human ratings at scale, the model is given a set of principles and critiques/revises its own outputs. Reduces reliance on expensive human labeling for safety feedback.

## Parameter-Efficient Fine-tuning (PEFT)

Full fine-tuning of a 70B model requires ~140GB of GPU memory just for weights, plus optimizer state. PEFT methods adapt models with far fewer trainable parameters.

### LoRA (Low-Rank Adaptation)

Freeze original weights. Add small trainable rank-decomposition matrices alongside specific layers.

```
W_new = W_original + (A * B)
# W_original: frozen, e.g. 4096 x 4096
# A: 4096 x r  (r = rank, typically 4-64)
# B: r x 4096
# Trainable params: 2 * 4096 * r  vs  4096^2 original
```

At rank 16, LoRA trains ~0.5% of parameters vs full fine-tuning. At inference, merge A*B back into W for zero overhead.

### QLoRA

LoRA + quantized base model. Load the frozen weights in 4-bit (NF4) quantization, train the LoRA adapters in 16-bit. Fits a 65B model fine-tuning on 2x 48GB GPUs.

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="bfloat16",
)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8b-hf",
    quantization_config=bnb_config,
)
lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"])
model = get_peft_model(model, lora_config)
```

## When to Fine-tune vs. Prompt Engineer

| Situation | Approach |
|---|---|
| Need specific output format consistently | Fine-tuning |
| Domain-specific terminology/style | Fine-tuning |
| Tasks solvable with good examples | Few-shot prompting |
| Limited data (< 100 examples) | Prompting + RAG |
| Latency/cost constraint | Fine-tune smaller model |
| New capability the base model lacks | Fine-tuning |

Rule of thumb: exhaust prompt engineering and RAG before fine-tuning. Fine-tuning teaches style and format well; it teaches new facts poorly (RAG is better for that).

## Evaluation After Fine-tuning

- **Task-specific metrics** - BLEU/ROUGE for summarization, pass@k for code, accuracy for classification
- **LLM-as-judge** - use a stronger model (e.g. Claude Opus) to rate outputs on dimensions like helpfulness, correctness, style
- **Human eval** - slow but gold standard; compare fine-tuned vs base on your real use cases
- **Regression testing** - check that fine-tuning didn't break general capabilities (MMLU, HellaSwag)
