# Operational Transformation (OT)
*Real-time collaborative editing*

Multiple users are editing the same document concurrently.

![](assets/Pasted%20image%2020260222090020.png)

Problem is if we apply these changes in a different order on different replicas, document will diverge.

We need all users to end up with same document regardless of the operation order. So above example would also be acceptable if both receives `Hello :-) World!`

![](assets/Pasted%20image%2020260222090409.png)

There are two algorithms for convergence,

- Operational transformation
- Conflict Free Replicated Data Types

## What is OT

Operational Transformation (OT) is a technique that:

- Transforms operations against concurrent operations
- So they can be applied in different orders
- Yet still converge to the same final state

### Simple Example

![](assets/Pasted%20image%2020260222090619.png)

This is probably most overused example to explain OT. But its easier.

Consider we are given work `Helo` and two users change the word, but editing at index 3 and at index 4 respectively.

They send the request to server saying they want to do operation (`insert` at some idx `idx`)

Server takes both request and transforms (`insert "!" at pos 5`) them in such a way that no matter what order these changes are applied they always converge to the same state.

When O2 arrives at replica A, transform it : `O2' = transform(O2, O1)`. Meaning if `O1` is inserted at position 1, shift `O2's` positions accordingly.

As a result both replica will converge.

### Types of Operations

In text editors

- Insert(position, char)
- delete(position)
- replace
- move (advanced systems)

### Two Critical Properties

OT must satisfy

- Convergence : All replicas reach same state
- Intention Preservation : Operation effect remains what user intended.

## Architecture Pattern

![](assets/Pasted%20image%2020260222091301.png)

Traditional OT uses

- Central Server
- Total Order of Operations
- Clients transform against known operations

```
Client -> Server -> Broadcast
```

Server acts as authority.

Why OT needs Central Authority ?

- Transform logic depends on ordering
- requires consistent operation history
- complex to implement fully decentralized


Use Cases

- Google Docs (early Versions)
- Etherpad
- ShareJS

### Why OT is Hard

Major challenges:

- Designing correct transform functions
- Handling all edge cases
- Scaling to many users
- Dealing with out-of-order operations

There are entire research papers on transform correctness.

### Forward to CRDTs

OT says:

> “Adjust operations so they can be applied safely.”

CRDT says:

> “Design data structure so operations are always safe.”

OT transforms. CRDT merges.

### Further Reading

- Inclusion transformation
- Exclusion transformation
- Context vectors
- Control algorithms
- Jupiter algorithm (Google Docs)
- dOPT, adOPTed (early algorithms)

### Resources

- Original OT paper (Ellis & Gibbs, 1989)
- “Google Docs Operational Transformation” (Jupiter paper)
- Martin Kleppmann — CRDT vs OT comparison
- [Early Introduction from CRDTs: The Hard Parts](https://www.youtube.com/watch?v=x7drE24geUw)