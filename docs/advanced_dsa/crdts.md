# Conflict-Free Replicated Data Types (CRDTs)
*Convergent state without coordination*

NOTE: following notes serve as mathematical intuition towards why does CRDTs work, after understanding understanding rest of the resources should be easier.

The core problems in distributed systems are : 

- Multiple replicas
- Network Partitions
- Concurrent Updates
- Eventual Synchronization

We want to ensure that all replicas *converge* to the same state without coordination without using Locks, Leaders, Global Ordering, Central Authority, etc.

- Why this is Hard ?

Example :

There are two users incrementing a counter concurrently

```python
# Replica A : +1
# Replica B : +1
```

Syncing naively, Last Write wins ~ 1 but here correct answer should be 2. This is fundamental distributed conflict problem.

*Convergent CRDTs are perfect for asynchronous gossip*

- You can merge them in any order
- You can merge the same ones multiple times
- You can use them even if messages are delayed, reordered, or duplicated.
- They always converge towards a global value

They have these properties because they form a *join semi-lattice*

## Introduction to Order Theory

To understand *join semi-lattices*, we need three core concepts.

- $a \le b$ (order)
- $a \parallel b$ (incomparability)
- $a \cup b$ (join)

### Order

An order is a binary relation $\le$ on a set S. We can write this $<S, \le>$

Ordered set could be the set of integers and $\le$ could be *less than or equal to*

$$
\{0, 1, 2, 3, 4, 5, .... \}
$$
We have a order because we can compare any two integers from the list.

An order $<S, \le>$ is a *total order* iff for every a and b in $S$, either $a \le b$ or $b \le a$.

When it comes to CRDTs we are interested  in *partial order*, which is weaker than a total order.

It doesn't require that every pair a and b in S can be compared.

If a and b aren't comparable according to $\le$, then we write $a \parallel b$

Examples : Define $\le$ as `located-in`

NYC $\le$ US (good) but $NY \parallel \text{Seattle}$ (incomparable).

India $\le$ Earth, but $US || India$ (incomparable) (Neither is located in another)

Example 2 : Define $\le$ as `happened-before`

Set is going to be made up of vector clock timestamps, (vector of timestamps), e.g. (4, 3, 1)

Each element of vector represents node in system.

$v1 \le v2$ iff every element v1 is less than or equal to the corresponding element in v2.

$(1,3,5) \le (1, 4, 6)$ but $(5, 1, 4) \parallel (5, 2, 3)$ (incomparable) might be conflicting(concurrent) clock times.

![](assets/Pasted%20image%2020260222002019.png)

Now imagine we have an ordered set S and we pick subset P ($P \subseteq S$)

An upper bound of P is an element in S thats greater than or equal to every element in P

![](assets/Pasted%20image%2020260222002512.png)

So 4 is greater and equal to every element 

Say $P \subseteq S$ has only two elements : $a, b$. Least upper bound of $\{ a, b \}$ is the join of a and b: $a \cup b$

When two elements can be compared directly their join is the max of the two.

Whenever we take a join $a \cup b$, we are moving `upwards` in terms of our order $<S, \le >$

![](assets/Pasted%20image%2020260222003211.png)

There must be only one least upper bound for a join to exist between two elements.

![](assets/Pasted%20image%2020260222003345.png)

Join obey 3 laws

- Associativity : $(a \cup b) \cup c = a \cup (b \cup c)$
- Commutativity : $a \cup b = b \cup a$
- Idempotence : $a \cup a = a$

Say we have an ordered set S, If we can find a join for every pair of elements in S then we have a join *semi-lattice*

If $x \cup y$ exits for all $\{x, y \} \subseteq S$, then $S$ is a *join semi-lattice.*

![](assets/Pasted%20image%2020260222074056.png)

- $(0, 0, 0) \le (0, 1, 0)$ is a valid pair.
- $(1, 0, 0) \le (1, 0, 1)$ and $(0, 0, 1) \le (1, 0, 1)$ is a valid pair but 
- (1, 1, 0) and (0, 1, 1) doesn't have a element for comparisons,

This is not a *join semi-lattice*

![](assets/Pasted%20image%2020260222074330.png)

Adding $(1, 1, 1)$ simply makes all pairs have the corresponding upper bound, and this is a *join semi-lattice*

## Convergent CRDTs

State-based CRDTs allow us to asynchronously share our nodes' local views.

Another type is operational CRDTs.

As we merge them across nodes, they converge towards a global value.

Each node remains available for answering queries.

![](assets/Pasted%20image%2020260222074719.png)

Each node will have Local views of global states. If a bird click comes to a node it will update local states.

| Increasing Bird Counter                         | Gossip                                          |
| ----------------------------------------------- | ----------------------------------------------- |
| ![](assets/Pasted%20image%2020260222074854.png) | ![](assets/Pasted%20image%2020260222074911.png) |
So these Nodes can gossip and accept bird click at the same time eventually merging towards a global value.

![](assets/Pasted%20image%2020260222075037.png)

Now when a client requests a count, we can send the node's local view, significantly improving user-experience without blocking the operation, eventually counter will converge and client will get the real count of the values.

For state-based CRDTs, we need three things.

- A *state type* $S$ ordered by some $<S, \le >$ ~ represent local view of a node
- A *merge()* function acting as a join on our state type.
- A *update()* function that mutates our state locally.

As we call `merge()` on our states, the results converge towards a global value. We define the global value as the upper bound on our *semi-lattice diagram*

![](assets/Pasted%20image%2020260222075518.png)

The join laws give us nice properties

- Associativity and Commutativity : The order of merges doesnt' matter
- Idempotence: We can merge in the same state multiple times.

![](assets/Pasted%20image%2020260222075712.png)

No matter how we merge we will always reach to global value.

|                                                 |                                                 |
| ----------------------------------------------- | ----------------------------------------------- |
| ![](assets/Pasted%20image%2020260222075748.png) | ![](assets/Pasted%20image%2020260222075840.png) |
Users of our distributed counter should not worry about merging details.

A simple interface : `increment()` and `value()`

NOTE: The global value doesn't necessarily exists on any one node.

It's the value toward which our merges are converging. The global value will *eventually* be reflected in all nodes.

Though constant asynchronous updates mean *eventually* might not come at all.

## Implement G Counter

Grow only Counter.

Our counter will be grow only. BirdWatch is relentlessly positive.

We need

- A *state type* $S$ ordered by some $<S, \le >$ ~ represent local view of a node
- A *merge()* function acting as a join on our state type.
- A *update()* function that mutates our state locally.

![](assets/Pasted%20image%2020260222080327.png)

Here `merge()` operations are called asynchronously.

Naive approach

local state as integer

Addition is not idempotent : Gossip will keep incrementing the values across nodes, 

*max* is idempotent, but it will never sum the node values, rather converge them towards max. We actually lose information when we perform merges.

Better Approach

local state is a vector, e.g. (1, 0, 5)

Each integer corresponds to the number of times increment() was called at one node in the network.

![](assets/Pasted%20image%2020260222080908.png)

Each node has a view on everyone's current local count.

```
update(node_id: Int)
    increments at vector index corresponding to local node id
    
# (1, 0, 5) ---> (2, 0, 5) ---> (3, 0, 5)

merge(x: Vector)
    coordinatewise max
    
(3, 0, 5) - (0, 1, 4)
merge : (3, 1, 5) ~ join

value():
    sum of all values in nodes (3 + 1 + 5)
```

More Types of Counter

- Positive-Negative Counter
- Non-Negative Counter
- Registers
- Sets
- Maps
- Graphs

### Monotonic Join Semi-Lattice

The term comes from the CRDT literature, not order theory.

- Our states form a join semi-lattice with *merge()* acting as join
- Our local update() moves us monotonically upward in terms of our order

Idea is that no matter when we *update()* and *merge()*, we move upwards towards a global value.

![](assets/Pasted%20image%2020260222081811.png)

### Resources

- [John Mumm - A CRDT Primer: Defanging Order Theory](https://www.youtube.com/watch?v=OOlnp2bZVRs)
- [CRDTs The Hard Parts](https://www.youtube.com/watch?v=x7drE24geUw) ~ martin kleppmann
- [# Conflict Resolution for Eventual Consistency](https://www.youtube.com/watch?v=yCcWpzY8dIA)  ~ martin kleppmann
- [CRDTs and the Quest for Distributed Consistency](https://www.youtube.com/watch?v=B5NULPSiOGw)
- [Conflict-free Replicated Data Types](https://arxiv.org/abs/1805.06358) ~ paper by Marc Shapiro (Regal)
- [CRDTs Primer](http://github.com/jtfmumm/curryon2018)
- [dotJS 2019 - James Long - CRDTs for Mortals](https://www.youtube.com/watch?v=DEcwa68f-jY) ~ full implementation 
- [CRDT Simpler Explanation](https://www.youtube.com/watch?v=M8-WFTjZoA0)

