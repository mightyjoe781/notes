# Paxos

Best Explanation Video : [Link](https://www.youtube.com/watch?v=d7nAGI_NZPk)

*Paxos is a family of distributed algorithms used to reach consensus*.

### Roles in Paxos

There are three conceptual roles (often same node plays multiple roles)

- Proposer : proposes values.
- Acceptor : votes on proposals
- Learner : Learns the chosen value.

Key Idea is Consensus is achieved by : *Majority Agreement among acceptors*

If a majority agrees on a value, no conflicting value can ever be chosen. This is quorum intersection property

### Single Decree Paxos (Basic Paxos)

Phase 1 : Prepare Phase

- Proposer chooses proposal number n

It sends out

```
id = "ptc5ux"
PREPARE(n)
```

Acceptors respond:

```
id = "4x1q4t"

PROMISE:

- I won't accept proposals < n
- here's the highest proposal I already accepted (if any)
```

Phase 2 - Accept Phase

After receiving majority promises, proposer sends

```
id "r2qjmm"

ACCEPT(n, value)
```

Important Rule:

- If any acceptor reported previously accepted value, proposer must use the highest numbered one.

Acceptors reply

```
id = "u3w9db"

ACCEPTED
```

Once majority accepts -> value is chosen


### Why this is Safe

Because:

- Majorities intersect.
- If a value was chosen earlier, at least one acceptor in new majority knows it.
- Proposer must adopt that value.

Thus: Two different values cannot both be chosen.

Safety Rule : If a value is chosen, all higher-numbered proposals must choose that same value.

This is the invariant Paxos maintains.

### Proposal Numbers

Proposal numbers must be

- globally unique
- monotonically increasing

Common Implementation

```
id="lb7yzn"
proposal_number = node_id + logical_counter
```

### Multi-Paxos

Basic Paxos agrees on one value only.

Real systems need:

- A sequence of decisions (log entries).

Multi-Paxos optimizes:

- First round elects stable leader
- Subsequent proposals skip prepare phase
- Only do accept phase

This reduces overhead significantly.

In stable networks Multi-Paxos behaves like Leader -> Followers, quite similar to Raft

### Why Paxos is Considered Hard

Non-intuitive proof

- Minimalistic description
- No obvious state machine structure
- Hard to implement correctly
- Liveness depends on timing

Leslie Lamport famously said: “Paxos is simple. It’s the explanations that are complicated.”

### Paxos vs Raft

|**Feature**|**Paxos**|**Raft**|
|---|---|---|
|Clarity|Hard to understand|Designed to be understandable|
|Leader|Emerges implicitly|Explicit election|
|Log replication|Extension (Multi-Paxos)|Built-in|
|Industry use|Foundation|More common in practice|
### Paxos Guarantees

- Safety: No two nodes decide differently.
- Fault tolerance: Works if majority of acceptors alive.
- Asynchronous model: No clock assumptions.

### Paxos in Real Life

- Chubby (Google lock service)
- Spanner (Google)
- ZooKeeper (Zab inspired by Paxos)
- Cassandra (in early designs)
- Etcd (Raft-based but conceptually similar)

### Further Study

- Read original Lamport paper “Paxos Made Simple”
- Understand quorum systems
- FLP impossibility theorem
- Multi-Paxos
- Compare with Raft