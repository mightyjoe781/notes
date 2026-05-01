# Prompt Engineering - Basics

Prompting is the fastest way to improve model outputs. Most quality problems are prompting problems before they are model problems.

## The Mental Model

The model predicts the most likely continuation of its input. A good prompt makes the desired output the most likely continuation.

**Concise + precise > long + vague.** Every unnecessary word is noise. Every missing constraint is an opportunity for the model to guess wrong.

## System Prompts

Set persistent behavior, persona, and constraints. Applied before every user message.

```
System: You are a senior software engineer reviewing Python code.
        Be concise. Flag bugs before style issues.
        Always provide a corrected code snippet when suggesting changes.
```

Tips:
- Define the role and expertise level
- State output format explicitly
- List what to avoid ("do not explain what the code does, only what's wrong")
- Keep it focused - long system prompts get ignored at the edges

## Zero-Shot

Ask directly, no examples. Works well for well-defined tasks on capable models.

```
Classify the sentiment of this review as positive, negative, or neutral:
"The battery life is great but the camera is disappointing."
```

## Few-Shot

Provide 2-5 input/output examples before your actual query. Teaches the model format, style, and task definition without fine-tuning.

```
Extract the company name and founding year.

Text: "Apple was founded by Steve Jobs in 1976."
Company: Apple, Year: 1976

Text: "Stripe launched in 2010 under Patrick Collison."
Company: Stripe, Year: 2010

Text: "Mistral AI was established in Paris in 2023."
Company:
```

Rules for good few-shot examples:
- Cover edge cases (not just the easy case)
- Keep format consistent - the model copies it exactly
- Order matters - put the most representative example last
- 3-5 examples is usually the sweet spot; diminishing returns beyond that

## Chain-of-Thought (CoT)

Ask the model to show its reasoning before answering. Dramatically improves accuracy on math, logic, and multi-step tasks.

```
# Zero-shot CoT - just add this phrase:
Q: If I have 3 boxes with 8 items each and give away 10 items, how many remain?
A: Let's think step by step.

# Few-shot CoT - show the reasoning in examples:
Q: Roger has 5 tennis balls. He buys 2 more cans of 3 balls each. How many does he have?
A: Roger starts with 5. He buys 2 * 3 = 6 more. 5 + 6 = 11. The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 for lunch and bought 6 more, how many remain?
A:
```

When to use CoT:
- Math and quantitative reasoning
- Multi-step logic or deduction
- Tasks where wrong answers are plausible without careful reasoning
- Debugging (ask model to trace through code step by step)

When NOT to use CoT:
- Simple classification or retrieval tasks (adds tokens, no benefit)
- Latency-sensitive applications
- Tasks where the answer is a direct lookup

## Formatting Your Prompt

Structure improves reliability, especially for complex prompts.

**Use XML tags to separate sections** (Claude is trained on XML-heavy data):

```
<task>Summarize the following article in 3 bullet points.</task>

<article>
{article_text}
</article>

<constraints>
- Each bullet should be one sentence
- Focus on key decisions, not background
- Do not include opinions
</constraints>
```

**Use headers and lists** for multi-part instructions:

```
Your job:
1. Extract all action items from the meeting notes below
2. Format each as: "[Owner] - [Task] - [Due date]"
3. If no due date is mentioned, write "No deadline"

Meeting notes:
{notes}
```

**Specify output format explicitly:**

```
Respond with valid JSON only. No explanation, no markdown.
Schema: {"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0}
```

## Temperature and Sampling

- `temperature=0` - deterministic, picks highest probability token each step; best for factual tasks, code, structured output
- `temperature=0.7` - balanced; good for most chat applications
- `temperature=1.0` - default for many models; more varied
- `temperature>1.0` - increasingly random; rarely useful

`top_p` (nucleus sampling) - only sample from the smallest set of tokens whose cumulative probability exceeds p. `top_p=0.9` is a common alternative to temperature tuning.

Rule of thumb: use temperature for creative tasks, keep it low (or zero) for tasks requiring precision.

## Common Mistakes

- **Ambiguous instructions** - "be helpful" is not a constraint; "respond in under 100 words" is
- **Asking multiple unrelated things** - split into separate prompts
- **No output format specified** - the model guesses; guess is inconsistent
- **Burying the key instruction** - put the most important thing first or last, not in the middle
- **Negations** - "do not say X" is weaker than "only say Y"; negations are easy to violate
