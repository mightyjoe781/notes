# Distributed Systems

Multiple Components, Multiple Machines but acts a single coherent system which solves a bigger problem

The best and worst thing about distributed system is : *Anything that could go wrong would go wrong*

Key to designing a good Distributed System
Start with a *Day 0* architecture and *scale* each component. See how it performs under load *rectify the system*, *rearchitect* and *repair*.

Why Distributed Systems ?

- Scale
- Horizontal Scalability
- Fault Tolerance

#### Load Balancers

One of the most *important* component in any system. We kinda take it for granted.

![](assets/Pasted%20image%2020250912104430.png)

Advantages of using a Load Balancer

- Fault Tolerance
- No over-clocked server

Load Balancing Algorithms

**Round Robin**
Distribute the load iteratively
Uniform infrastructure

**Weighted Round Robin**
Distribute the load iteratively but as per weights
Non-Uniform Infrastructure

**Least Connection**
Pick the server having the least connections
When response times has a big variance. (*Analytics*)

![](assets/Pasted%20image%2020250912105111.png)

## Designing Load Balancer

Requirements

- balance the load
- tunable algorithm
- scaling beyond one machine

Terminology : LB Server, Backend Server

Brainstorm : LB Configuration, Monitoring, Availability, Extensibility

#### Load Balancer Needs Configuration

- balancing configuration
- backend server list

![](assets/Pasted%20image%2020250912115446.png)

Configuration DB will config per load balancer.
But making a DB call upon getting every request will be *catastrophic* to response times
Hence we keep a copy of the configuration in memory of the LB server.

![](assets/Pasted%20image%2020250912115552.png)

How to keep the LB configuration in sync between : LB Server & Configuration DB

- write a CRON job (PULL)
- reative approach (PUSH)

![](assets/Pasted%20image%2020250912115910.png)

How will a load balancer ensure that it is not forwarding request to an *Unhealthy* backend server ?

#### Orchestration

- keeps and eye *on the health* of the backend servers
- if any backend server is unhealthy
    - orchestration updates the DB
    - changes then reach the LB server through a pub-sub using CDC (change data capture)
- monitors health of LB servers & scales them up and down

![](assets/Pasted%20image%2020250912120418.png)

NOTE: read about $\phi$ accrual failure detection algorithm, better than simple health checks.

How will orchestration decide scaling LB servers ?
Scaling will happen on CPU, Memory, # TCP connections, where do we have this data ?
*Monitoring Agents* on Load Balancer, example ~ prometheus

![](assets/Pasted%20image%2020250912121102.png)

### Scaling Load Balancers

LB servers cannot be just 1 instance, so how do we scale, What is that one thing sharded & Scales well ? *DNS*

- resolves IP for the domain name
- very light weight, e.g. *coreDNS*
- lb.payments.minetest.in would resolve in lets say 3 ips
    - 10.0.0.1
    - 10.0.0.2
    - 10.0.0.3

![](assets/Pasted%20image%2020250912121437.png)

#### Complete Infra

![](assets/Pasted%20image%2020250912121605.png)

Read this Paper : Maglev : A fast and reliable software load balancer

## Remote and Distributed Locks

Remote Locks: Locks managed by a central machine lock Manager.

![](assets/Pasted%20image%2020250913133352.png)

The 3 machines co-ordinate through a central lock manager.

* Multiple threads synchronise through *mutexes & semaphores*
* Multiple processes synchronise through *Disk* (Interesting Example: `apt-get upgrade` cannot be run twice concurrently)
* Multiple machines synchronise through *Remote Locks*

## Synchronizing Consumers

To understand remote locks better, lets synchronise *multiple consumers* over an *unprotected remote queue*

![](assets/Pasted%20image%2020250913134116.png)

Queue is remote & unprotected. We want one consumer to make call to the queue at a time. We need to make sure all consumer co-ordinate via shared lock.

#### Consumers pseudocode

```
ACQ_LOCK()
    READ_MSG()
REL_LOCK()
```

All consumers wait on `ACQ_LOCK()`, while one of them `READ_MSG()`.
Out requirements from the lock manager ?

- Atomic Operations ~ so that two machines do not `ACQ_LOCK()`
- Automatic Expiration ~ avoid perpetual locking

So which DB : *redis*(popular choice because in-mem(fast)) , *dynamo_db*

*Implementation* : Set the key in *redis* that says which consumer holds the lock and can read the message.
e.g. *queue7:consumer2(ex: 300)* : lock held by consumer 2 for expirations of 300s.

![](assets/Pasted%20image%2020250913135153.png)

```python

def acquire_lock(q):
    consumer_id = get_my_id()
    while True:
        v = redis.setnx(q, consumer_id, ex=300) # set non-existent ~ atomic
        if v == 1: return
        else: continue
        

def release_lock(q):
    # validate ownership of lock, before delete
    consumer_id = get_my_id()
    v = redis.get(q)
    if v == consumer_id: redis.delete(q) 
    # Use : 'Eval' ~ Executed Atomically using Lua, because when entering if condition, lock can be acquired by other consumer and you delete their lock.
```

NOTE: This one redis instance is not horizontally scalable.
Where else do you see this in action ? Mongo transaction uses remote locks on involved rows.
Distributed Locks (*Redlock*) ~ Distributed locks with Redis.

Idea : What we did in remote lock, just distribute it across multiple instances of redis.
5 master nodes of Redis, No replication, all independent.
Acquire lock :

- client goes through 5 nodes, trying to *ACQ_LOCK()* with timeout
- if lock acquired on > 50% then *ACQUIRED*
- else release the lock on acquired instances and return *FAILED*

Distributed Locks are used in systems which demand correctness not the high throughput, here its a simple tradeoff.

But why are we doing this ? *We are doing this to avoid single-point of failure(SPOF)*

Exercises

- Implement a load balancer with tunable algorithm locally.
- Read this Paper : Maglev : A fast and reliable software load balancer
- Read about redis : *Redlock* : Martin Kleppmann & implementation blog
- Read on Chubby Lock: Lock service for loosely coupled distributed systems
- https://arpitbhayani.me/blogs > 15 blogs on distributed systems & distributed transactions.
