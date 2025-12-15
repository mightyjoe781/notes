# API Design Principles

> _What does a great API look like, and why should we care about the APIs we build?_

> A thoughtfully designed API can be a game changer—it directly shapes the developer experience and determines how easily others can build on top of it.

Few examples of such *clean, consistent, developer-first* APIs comes from Stripe, Twilio, Plaid, GitHub, Slack, Shopify, SendGrid etc.

What makes these APIs stand out is following

- Consistency : Same naming, same patterns everywhere
- Predictability : You can guess the next endpoint
- Clear Error Models : Structured errors, not strings
- Good Default : Sensible pagination, limits, retries
- Strong Documentation : Examples > Explanations
- Backwards Compatibility : Versioning without surprise
- Developer Empathy : Designed for Humans, not machines

Good Video on API Design : [Link](https://www.youtube.com/watch?v=IEe-5VOv0Js)

- APIs should be *Approachable, Flexible, Composable*.
- Example of Stripe API Release Process

![](assets/Pasted%20image%2020251216003034.png)

- API Design Patterns
    - Avoid Industry Jargon
    - Nested Structures : introduces structure with extensionability
    - Properties as Enums: prefer enums rather than booleans
    - Reflect API Request in Response
    - Polymorphic Objects : Use type field to define the type of object we gonna receive.
    - Express changes with verbs : `/v1/payment_intents/:id/capture` or `/v1/invoices/:id/mark_uncollectible`
    - Timestamp parameter names `<verb>_at`
    - Gated Features

![](assets/Pasted%20image%2020251216003550.png)

Other Few Important Concepts in reference of robust APIs is *Pagination, Idempotency Key, etc.*

Resources : 

- [Postman Blog on Stripe APIs](https://blog.postman.com/how-stripe-builds-apis/)