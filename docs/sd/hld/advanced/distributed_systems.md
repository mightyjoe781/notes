# Distributed Systems

A distributed system is one where multiple components running on multiple machines work together to appear as a single coherent system solving a bigger problem.

The best and worst thing about distributed systems is the same: _anything that can go wrong, will go wrong._

**Key design principle:** Start with a Day 0 architecture, then scale each component incrementally.

Observe behavior under load, rectify bottlenecks, rearchitect where necessary, and repeat.

**Why distributed systems?**

- Scale and horizontal scalability
- Fault tolerance

#### Load Balancers

Load balancers are one of the most important components in any system - and one we tend to take for granted.

![](assets/Pasted%20image%2020250912104430.png)

**Advantages:**

- Fault tolerance: traffic is rerouted away from failed servers
- Prevents any single server from being over-clocked

**Load balancing algorithms:**

![](assets/Pasted%20image%2020260425191835.png)

## Designing Load Balancer

**Requirements**

- balance the load
- support a tunable algorithm
- scale beyond a single machine

**Terminology:** LB Server, Backend Server

Brainstorm : LB configuration, monitoring, availability, extensibility

#### Configuration

A load balancer needs two things configured:

1. The balancing algorithm
2. The list of backend servers

![](assets/Pasted%20image%2020250912115446.png)

Making a DB call on every incoming request would be catastrophic for latency. 

![](assets/Pasted%20image%2020250912115552.png)

Instead, the LB server keeps a copy of its configuration in memory and syncs it with the Configuration DB in one of two ways:

- **Pull:** a cron job periodically fetches updates
- **Push:** a reactive approach where the DB pushes changes to the LB

![](assets/Pasted%20image%2020250912115910.png)

### Health Monitoring

How does a load balancer avoid forwarding requests to unhealthy backend servers? Through an **Orchestration** layer.
#### Orchestration

- Continuously monitors the health of backend servers
- If any of the servers are unhealthy
    - Marks unhealthy servers in the DB; 
    - changes propagate to the LB via pub-sub using CDC (Change Data Capture)
- Monitors LB server health and scales them up or down as needed

![](assets/Pasted%20image%2020250912120418.png)

> **Note:** Look into the φ (phi) Accrual Failure Detection algorithm - it's significantly better than simple health checks.

How will orchestration decide scaling LB servers ?

Orchestration decides when to scale LB servers based on metrics: CPU, memory, and number of TCP connections. These are collected by **monitoring agents** (e.g., Prometheus) running on each LB server.

![](assets/Pasted%20image%2020250912121102.png)

### Scaling Load Balancers

A single LB instance is itself a single point of failure. The solution is **DNS**, which is lightweight, horizontally scalable, and battle-tested (e.g., CoreDNS).

A domain like `lb.payments.minetest.in` can resolve to multiple IPs, each pointing to a different LB server.

- resolves IP for the domain name
- very light weight, e.g. *coreDNS*
- lb.payments.minetest.in would resolve in lets say 3 ips
    - 10.0.0.1
    - 10.0.0.2
    - 10.0.0.3

![](assets/Pasted%20image%2020250912121437.png)

#### Complete Infrastructure

![](assets/Pasted%20image%2020250912121605.png)

> **Paper to read:** _Maglev: A Fast and Reliable Software Load Balancer_

## Remote and Distributed Locks

A **Remote Lock** is a lock managed by a centralized Lock Manager, used to coordinate access across multiple machines.

![](assets/Pasted%20image%2020250913133352.png)

The 3 machines coordinate through a central lock manager.

- Threads synchronize via mutexes and semaphores
- Processes synchronize via disk (e.g., `apt-get upgrade` cannot run twice concurrently)
- Machines synchronize via remote locks

### Motivating Example: Synchronizing Multiple Consumers

To understand remote locks better, let's synchronize *multiple consumers* over an *unprotected remote queue*.


![](assets/Pasted%20image%2020250913134116.png)

Queue is remote & unprotected. We want one consumer to make call to the queue at a time. We need to make sure all consumers coordinate via shared lock.

```
ACQ_LOCK()
    READ_MSG()
REL_LOCK()
```

All consumers block on `ACQ_LOCK()` while one proceeds to `READ_MSG()`.

**Requirements from the lock manager:**

- **Atomic operations** - prevent two machines from acquiring the lock simultaneously
- **Automatic expiration** - prevent perpetual locking if a consumer crashes

So which DB : *redis*(popular choice because in-mem(fast)) , *dynamo_db*

**Implementation using Redis:** Store a key like `queue7:consumer2 (ex: 300)` - meaning consumer 2 holds the lock on queue 7 for 300 seconds.

![](assets/Pasted%20image%2020250913135153.png)

```python
def acquire_lock(q):
    consumer_id = get_my_id()
    while True:
        v = redis.setnx(q, consumer_id, ex=300)  # SETNX = set if not exists (atomic)
        if v == 1:
            return  # lock acquired
        # else: keep retrying

def release_lock(q):
    consumer_id = get_my_id()
    v = redis.get(q)
    if v == consumer_id:
        redis.delete(q)
    # IMPORTANT: the get + delete must be executed atomically using Lua's EVAL,
    # otherwise another consumer could acquire the lock between the check and the delete.
```

>**Note:** This single Redis instance is not horizontally scalable. MongoDB transactions use a similar remote locking mechanism on the rows involved.

#### Distributed Locks (Redlock)

Redlock extends the remote lock idea across multiple independent Redis instances to eliminate the single point of failure.

**Setup:** 5 independent Redis master nodes (no replication between them)

**Acquire lock:**

1. The client attempts to acquire the lock on all 5 nodes with a timeout
2. If the lock is acquired on **more than 50%** of nodes -> **ACQUIRED**
3. Otherwise -> release locks on any acquired nodes and return **FAILED**

Distributed locks are the right tool when **correctness matters more than throughput** - that's the core tradeoff here.

But why are we doing this ? *We are doing this to avoid single-point of failure(SPOF)*

## Further Reading

**Implementation**

- [Build a load balancer locally](https://github.com/karanpratapsingh/system-design#load-balancing) - implement round-robin, least-connections, and consistent-hash algorithms yourself; the implementation details reveal trade-offs that theory glosses over

**Papers**

- [Maglev: A Fast and Reliable Software Network Load Balancer — Google (2016)](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/44824.pdf) — Google's production load balancer; covers consistent hashing with Maglev hashing (better distribution than standard consistent hashing), connection tracking, and fault tolerance at Google scale
- [Chubby: The Chubby Lock Service for Loosely-Coupled Distributed Systems — Burrows (2006)](https://research.google/pubs/the-chubby-lock-service-for-loosely-coupled-distributed-systems/) - Google's distributed lock service; the inspiration for ZooKeeper and etcd; explains how leader election and distributed coordination are done in production

**Distributed Locking**

- [Redlock — Redis Distributed Locking](https://redis.io/docs/latest/develop/use/patterns/distributed-locks/) - the official Redis documentation on Redlock; read the algorithm description carefully before the controversy
- [How to do distributed locking — Martin Kleppmann](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) - Kleppmann's critique of Redlock; argues it is unsafe under certain timing assumptions; essential reading
- [Is Redlock safe? — Antirez (Redis author) response](http://antirez.com/news/101) - Salvatore Sanfilippo's rebuttal to Kleppmann; read both back-to-back and form your own view; this exchange is one of the best public distributed systems debates available

**Blogs**

- [Arpit Bhayani — Distributed Systems & Distributed Transactions](https://arpitbhayani.me/blogs) - 15+ posts covering distributed transactions, sagas, two-phase commit, and consistency patterns; written for practitioners, not academics; high signal-to-noise ratio
