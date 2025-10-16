# Prompt Engineering

*Naive Prompt:* Summarize what is AWS

- Prompt gives little guidance and leaves a lot to the model interpretation
- *Prompt Engineering* ~ developing, designing, and optimizing prompts to enhance the output of Foundational Models
- Improved Prompting technique
    - **Instruction** ~ a task for the model to do (description, how the model should perform)
    - **Context** ~ external information to guide the model
    - **Input Data** ~ the input for which you want a response
    - **Output Indicator** ~ the output type of format

Enhanced Prompt:

![](assets/Pasted%20image%2020251009121502.png)
### Negative Prompting

- A technique where we explicitly instruct the model on what not to include or do in its response
- Negative Prompting helps
    - Avoid unwanted content
    - Maintain Focus
    - Enhance Clarity

![](assets/Pasted%20image%2020251009121520.png)
### Prompt Performance Optimization

- System Prompts ~ how the model should behave and reply
- Temperature (0 to 1) ~ creativity of model's output
- Top P (0 to 1)
    - Low P ~ consider 25% most likely words, will make a more coherent response
    - High P ~ consider a broad range of possible words, possible more creative and diverse output
- Top K ~ limits the number of probably words
- Length ~ maximum length of answer
- Stop Sequences ~ tokens that signal the model to stop generating output

NOTE: Latency is *not impacted* by Top P, Top K, Temperature

### Zero-Shot Prompting

- present a task to the model without providing the examples or explicit training for that specific task

*write a short story about a dog that helps solve a mystery*

- we fully rely on the mode's general knowledge
- The larger and more capable FM, the more likely you will get good results.
### Few-Shot Prompting

- Provide few examples of a task to model to guide its output.
- We provide a *few shots* to model to perform the task.

*Here are two examples of stories where animal help solve mystery.*

- *Whiskers the Cat noticed....*
- *Buddy the Bird saw that all garden ....*
*Write a short story about a dog that helps solve a mystery.*

### Chain of Thought Prompting

- Divide the task into a sequence of reasoning steps, leading to more structure and coherence.
- Using a sentence like *Think step by step* helps
- Can be combined with Zero-Shot/Few-Shot Prompting

*Let's write a story about a mystery solving dog*
*First, describe the setting and dog*
*Then, introduce the mystery*
...

### Retrieval-Augmented Generation (RAG)

- Combine the model's capability with external data sources to generate more informed and contextually rich response
- The initial prompt is them augmented with the external information.

