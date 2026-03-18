# Foundational Topics - I

## Online/Offline Indicator

Design Philosophy :

Spiral Building - Identify the *core* of the system first, then build outward around it. The *core* is use-case specific. It could be a database choice, a communication pattern, or a protocol.

Incremental Building :

1. Start with a Day Zero (simplest viable) architecture.
2. Stress-test each component - under load and at scale (observe behaviour)
3. Identify the bottleneck.
4. Re-architect around it.

Guiding Principles

- Understand the access patterns before choosing a technology.
- Affinity towards a particular tech comes second
- Build *intuition*, not just familiarity

### Storage Model

We need to answer : is a user online or offline ?

```
user_id (int) -> online/offline (bool)
```

This is natural *Key-Value* access pattern.

### API Design

#### Bulk Status Endpoint

*preferred over individual lookups*

```http
GET /status/users?ids=u1,u2,u3
```


![](assets/Pasted%20image%2020250909111107.png)

Exposing a bulk endpoint reduces multiple round-trip network calls into one.

#### Heartbeat Model

Since servers cannot proactively talk to clients (without a persistent connection), we use a **push-based model**: every client periodically sends a heartbeat to the service.

```http
POST /heartbeat
```

The authenticated user is marked as alive upon each request.

**How offline is determined:** If no heartbeat is received within a threshold window (e.g., 30 seconds), the user is considered offline.

#### Database Schema

In database store *time received the last heartbeat* (`last_hb`)

| user_id | last_hb |
| ------- | ------- |
| u1      | 1000    |
| u2      | 1050    |
| u3      | 1060    |

When you receive the heartbeat.

```sql
UPDATE pulse
SET last_hb = now() -- epoch seconds
WHERE user_id = u1
```

User sends heartbeat every 10 seconds.

#### Get status API

```
GET /status/<user_id>
```

- No entry in DB : offline
- `last_hb` < `now()` - 30 : offline
- otherwise : online

#### Scale Estimation

| Field     | Size |
| --------- | ---- |
| `user_id` | 4B   |
| `last_hb` | 4B   |
| Total     | 8B   |

For 1 billion users : `1B x 8Bytes = 8GB`

Can we do better on storage ?

Requirement : is that we only care whether user is online/offline. We could design if absence means offline ?

If absence of an entry implies offline, we only need to store _currently active_ users. Use a TTL of 30 seconds on each entry - it expires automatically if no heartbeat arrives.

For 100K active users: `100K × 8B ≈ 800 KB` — a dramatic reduction.
#### Auto Expiry Strategy

Approach 1 : Write a CRON job that periodically deletes expired entries.

 - not a robust solution at scale
 - we need to handle edge case in business logic

Approach 2 : Can we not offload this to our datastore. (Don't reinvent the wheel)

Databases like *Redis*, *DynamoDB* natively support per key TTL features.

Upon receiving a heartbeat

- Upsert the entry with `TTL = 30 seconds`
- No manual deletion needed

#### Which one would you pick & why ?

| Features                                               | Redis | DynamoDB |
| ------------------------------------------------------ | ----- | -------- |
| Persistence                                            | ❌     | ✅        |
| Fully Managed                                          | ❌     | ✅        |
| Vendor lock-in                                         | ✅     | ❌        |
| future extensibility                                   | ✅     | ❌        |
| time sensitivity <br>(persistent connections use case) | ✅     | ❌        |


> **Note:** In production systems, WebSockets are typically used for online/offline indicators. This Day Zero design intentionally avoids that complexity.

#### How is our DB doing ?

**Load Calculations**

- Users send a heartbeat every 10 seconds -> 6 heartbeats/minute per user.
- 1M active users -> *6M DB writes per minute*

This creates a high-frequency micro-write pattern, which becomes a network bottleneck.

**Solutions**

- Connection Pooling : Reuse existing DB connections rather than opening a new one per request.
- Micro-Batching : Buffer heartbeat updates in memory and flush them to the DB in bulk at short intervals.

![](assets/Pasted%20image%2020250909115345.png)

Connection Pool solves the problem too many noisy queries thrashing the Database.

## The Six Pillars of System Design

Almost every design decision in a system maps back to one of these six areas:

1. **Database**
2. **Scaling**
3. **Concurrency**
4. **Caching**
5. **Delegation**
6. **Communication**

Any and every decision would affect one of these 6 factors.

We'll explore each using a multi-user blogging platform (think: Medium) as the running example 

- one user, multiple blogs
- multiple users

### Database

#### Schema

```
users
-----
id
name
bio

blogs
-----
id
author_id (FK → users.id)
title
is_deleted      ← soft delete flag
published_at    ← epoch integer
body
```

#### Importance of `is_deleted` [soft delete]

When a user deletes a blog, set `is_deleted = true` instead of running a `DELETE`

Reasons :

- **Recoverability** - accidental deletions can be undone.
- **Auditing** - maintain a history of what existed.
- **Archival** - keep data for analytics without it being user-visible.
- **DB performance** - avoids B-tree rebalancing from physical row deletion.

#### Column Type

![](assets/Pasted%20image%2020250909125838.png)

#### Storing `datetime` in DB

| Format          | Example                | Trade-off                                         |
| --------------- | ---------------------- | ------------------------------------------------- |
| `DATETIME` type | `2022-04-02T09:01:36Z` | Human-readable, but heavy on storage and indexing |
| Epoch integer   | `1648893696`           | Efficient, lightweight, easy arithmetic           |
| Custom int      | `20220402`             | Compact for date-only, loses time precision       |

**Recommendation:** Use epoch integers for `published_at` and similar fields.
### Caching

Core Idea : Avoid re-computing or re-fetching the same data. A cache is essentially a hash table with an optional eviction policy.

Use-Cases :

- Reduce disk I/O (avoid hitting DB for repeated reads)
- Reduce network I/O (CDN for static assets)
- Reduce compute (cache results of expensive aggregations)

Exercise : Find possible places that you can use as cache with an example. central cache (RAM) for application-level cache. (save DB computations)

Solution : Caching layers (from closest to farthest from the user):

| Layer                   | Example                      | Notes                               |
| ----------------------- | ---------------------------- | ----------------------------------- |
| Browser / Local Storage | Personalized recommendations | Highly specific to the user         |
| CDN                     | Static HTML, images, CSS     | Distributed globally                |
| Load Balancer           | Cached responses             | Reduces upstream pressure           |
| API Server (in-memory)  | Recent blog reads            | Fast but local, risks inconsistency |
| API Server (disk)       | Pre-rendered pages           | Slower than RAM, larger capacity    |
| DB Materialized Views   | Pre-joined tables            | Refreshed via DB triggers           |

### Scaling

**Goal:** Handle a large number of _concurrent_ requests.

**Vertical Scaling (Scale Up)**

- Upgrade the machine (more CPU, RAM).
- Simple to manage, but has a ceiling.
- Risk of downtime during upgrades.

**Horizontal Scaling (Scale Out):**

- Add more machines running the same service.
- Theoretically unbounded.
- Adds architectural complexity (load balancing, distributed state).
- Provides fault tolerance.

In general a good scaling strategy is to start scaling vertically first, then move towards horizontal scaling.

Horizontal Scaling ~ $\infty$ , but there is a catch !!

Stateless API servers are easy to scale horizontally. But stateful components (databases, caches) are the real bottleneck.

Always scale from the data layer upward - not the other way around.

![](assets/Pasted%20image%2020250909150413.png)

**Scaling a Database**

![](assets/Pasted%20image%2020250909150700.png)

### Delegation

**Mantra for Performance:** _What does not need to happen in real time should not happen in real time._

**Core idea** : *Delegate & Respond*

Acknowledge the request immediately. Delegate the actual work to background workers via a message broker.

![](assets/Pasted%20image%2020250909161947.png)


On publishing a blog, instead of synchronously updating `total_blogs` on the user record, emit an event to a broker and let a worker handle the update asynchronously.

Similar delegation would happen for publish, deletion (`ON_DELETE` events)
#### Brokers

Buffer to keep the tasks and messages.

Two common implementations

- Message Queues : SQS, RabbitMQ
- Message Streams : Kafka, Kinesis

|Feature|Message Queue (SQS, RabbitMQ)|Message Stream (Kafka, Kinesis)|
|---|---|---|
|Consumer model|Homogeneous; message pulled and removed|Heterogeneous; each consumer tracks offset|
|Replay|❌|✅|
|Error recovery|Harder|Replay from checkpoint|
|Ordering|Per-queue|Per-partition|

![](assets/Pasted%20image%2020250909162704.png)

#### Kafka Essentials

Kafka is a distributed message stream. Key concepts:

- **Topic:** A named channel for a category of events (e.g., `blog.published`).
- **Partition:** Each topic is split into `n` ordered partitions. Messages are routed to partitions via a hash key.
- **Ordering:** Guaranteed _within_ a partition, not across partitions.
- **Consumer Groups:** Each group reads from the topic independently. Each partition is consumed by exactly one consumer in a group at a time.

**Limitations:**

- Max parallelism per consumer group = number of partitions.
- Kafka guarantees **at-least-once** delivery (not exactly-once by default). Consumers must handle *idempotency*.

Now with Kafka, previous architecture will become :

![](assets/Pasted%20image%2020250909163125.png)

### Concurrency

**Goal:** Execute work faster using threads or multiprocessing.

**Problems introduced:**

- **Shared state:** Multiple threads modifying the same variable or DB row simultaneously.
- **Race conditions:** Final state depends on execution order.

**Solutions for Handling Concurrency**

- **Pessimistic locking:** Lock the row before reading; others wait.
- **Optimistic locking:** Read, compute, write with a version check; retry on conflict.
- **Mutexes / Semaphores:** OS-level synchronization primitives.
- **CRDTs:** Conflict-free replicated data types — lock-free by design.

**Example - clap count race condition:** Two users clap simultaneously. Both read `count = 5`. Both write `count = 6`. The correct answer is `7`.

We protect our data through : *Transactions* or *Atomic Instructions*

```sql
-- Atomic increment - no race condition
UPDATE blogs SET clap_count = clap_count + 1 WHERE id = 'b1';

-- Or wrap in a transaction for complex operations
BEGIN;
SELECT clap_count FROM blogs WHERE id = 'b1' FOR UPDATE;
UPDATE blogs SET clap_count = clap_count + 1 WHERE id = 'b1';
COMMIT;
```

### Communication

#### Standard Request-Response (HTTP):

![](assets/Pasted%20image%2020250909183415.png)

Simple, stateless. Works for most use cases.

#### Short Polling

Client repeatedly sends requests at a fixed interval to check for updates.

![](assets/Pasted%20image%2020250909183520.png)

- Use case: Checking if an EC2 instance is ready, refreshing a cricket score.
- Downside: High HTTP overhead, many empty responses.

#### Long Polling

Client sends a request. Server holds the connection open and responds only when new data is available (or on timeout).

![](assets/Pasted%20image%2020250909184007.png)

- Use case: EC2 provisioning status, chat messages.
- Advantage: Fewer wasted responses than short polling.

Short Polling v/s long polling
- short polling *sends response right away*
- long poling sends response only when done
    - connection kept open for entire duration

e.g. EC2 provisioning
- short polling - get status every few seconds
- long polling - get response when server ready

#### Web Sockets

A persistent, full-duplex connection over the `wss://` protocol (not HTTP).

![](assets/Pasted%20image%2020250909184213.png)

- Server can proactively push data to the client.
- Use cases: 
    - Real-time chat
    - stock tickers
    - live collaboration
    - multiplayer games.
- Advantage: 
    - Lowest latency
    - minimal overhead per message.

#### Server-sent events (SSE)

A persistent, _unidirectional_ HTTP-based connection. Server pushes; client only listens.

![](assets/Pasted%20image%2020250909184459.png)

- Use cases
    - Deployment log streaming
    - live like count updates
    - notification feeds
- Advantage
    - Simpler than WebSockets when you only need server -> client push.

Realtime interactions

- on twitter, like count updates without refresh
- on medium, one article clapped, other readers should see it in realtime
- instagram live interaction

**Choosing a pattern:**

| Pattern       | Direction       | Connection | Best For               |
| ------------- | --------------- | ---------- | ---------------------- |
| Short Polling | Client → Server | Stateless  | Simple status checks   |
| Long Polling  | Client → Server | Held open  | Delayed responses      |
| WebSockets    | Bidirectional   | Persistent | Real-time, interactive |
| SSE           | Server → Client | Persistent | Live feeds, logs       |

## Exercises

- https://github.com/Addi-11/system-design-excercises?tab=readme-ov-file