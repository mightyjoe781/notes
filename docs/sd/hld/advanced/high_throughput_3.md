---
title: Scaling to 1M req/s
description: A practical walkthrough of throughput bottlenecks in order - language/framework choice, CPU, network, database, Redis, and kernel tuning.
tags:
  - concept
---

# Scaling to 1M req/s

A practical walkthrough of the bottlenecks you hit — in order — when pushing a system to extreme throughput, and the decisions that remove each ceiling.

![](assets/scaling_bottleneck_order.excalidraw.png)

## Language and Framework Choice

Raw throughput ceiling on a single powerful machine:

| Language | Framework | req/s (simple JSON) |
|---|---|---|
| C++ | Drogon + RapidJSON | 500k-1M+ |
| Rust | axum / actix-web | 400k-600k |
| Go | net/http / fiber | 200k-350k |
| Node.js | Fastify | 60k-100k |
| Node.js | Express | 15k-30k |
| Python | FastAPI + uvicorn | 15k-30k |

**Key insight:** Even on a 192-core machine, Node.js cannot hit 1M req/s for a CPU-intensive route. C++ with Drogon + RapidJSON was the only runtime that got there. For IO-bound routes (pure DB reads), language matters less — the DB becomes the bottleneck first.

**The JSON parser matters too.** Drogon's default JSON parser was 4x slower than Node's V8 JSON. Switching to RapidJSON was the breakthrough — it is one of the fastest JSON parsers available.

## CPU Utilization - Use Every Core

A single process uses 1 core by default. The first step is always to use all available cores.

**Node.js - Cluster mode (multiple processes)**

```bash
pm2 start ecosystem.config.js  # spawn N workers = N cores
```

Each worker is a separate process with no shared memory. The OS-level `accept()` lock causes contention when many workers compete for incoming connections — this is why Node does not scale linearly past a certain core count.

**Python - Multiple workers**

```bash
uvicorn main:app --workers 13  # (2 x cores) + 1
```

Same limitation as Node. The GIL forces multi-process rather than multi-thread.

**Rust - Tokio async thread pool**

```rust
#[tokio::main(flavor = "multi_thread", worker_threads = 8)]
```

Single process, N threads, shared memory. No `accept()` contention. Scales nearly linearly with core count.

**C++ - Drogon**

```cpp
drogon::app().setThreadNum(192)  // match your core count
```

**Rule:** Set worker/thread count to match CPU cores. Monitor idle CPU under load — if it is not near 0%, you are either under-provisioned on workers or the bottleneck has shifted elsewhere (network, DB).

### Measuring CPU Utilization

Two methods exist and tools disagree on which to use:

- **Method 1:** Sum all core utilizations — can exceed 100% (e.g. 800% on 8 cores = all cores maxed)
- **Method 2:** Average across cores — always 0-100%

```bash
mpstat 1   # per-core breakdown, shows idle %
htop       # visual, uses method 1
top        # per-process, uses method 2
```

At 1M req/s, idle CPU should be near 0%. If it is not, either you have headroom to push harder or the bottleneck has moved to network or DB.

## The Network Bottleneck

This hits before CPU at large payloads and is easy to miss.

```
1M req/s x 30KB payload = 30 GB/s = 240 Gbps
```

NIC limits by instance type:

| Machine | Network | Max payload throughput |
|---|---|---|
| Typical VPS | 1 Gbps | ~125 MB/s |
| AWS c8i.32xlarge | 50 Gbps | ~6.25 GB/s |
| AWS c8gn.48xlarge | 600 Gbps | ~75 GB/s |

**Why this matters:** A 50 Gbps NIC saturates at ~100k req/s with 30KB responses. Reducing the payload to 1KB on the same machine immediately jumped throughput to 3M req/s — no code changes.

**Solutions:**
- Reduce payload size — trim unnecessary fields
- Enable compression (gzip/brotli) — a 30KB repetitive JSON compresses to ~1KB
- Use a CDN (Cloudflare/Fastly) to absorb traffic before it hits your NIC
- Choose network-optimized instances (`n` suffix on AWS, e.g. `c8gn`)

## The Database Bottleneck

This is almost always the real wall. CPU and network can be solved with hardware. The DB requires architectural changes.

### PostgreSQL limits (single node)

| Operation | Approx limit |
|---|---|
| Simple reads (indexed) | 200k-400k/s |
| Writes (INSERT) | 30k-60k/s |
| Writes with high IOPS disk | 50k-100k/s |

### Query complexity kills throughput

```sql
SELECT * FROM codes ORDER BY RANDOM() LIMIT 1  -- O(N), scans entire table
SELECT COUNT(*) FROM codes                      -- O(N), full table scan
```

These are O(N) operations. With 10M rows, a single query like this can take 43 seconds. At scale, one bad query can bring down the entire database — all other queries wait behind it.

*Always prefer indexed lookups:*

```sql
SELECT id, code FROM codes WHERE id = $1  -- O(log N), instant
```

### DB connection pooling

Each application worker opens connections to the DB. At 128 Node workers with 10 connections each, that is 1280 simultaneous connections. PostgreSQL defaults to a max of 5000, but connection overhead degrades performance well before that.

**Solution:** Use **PgBouncer** in front of Postgres. It pools connections so the DB sees a small number of long-lived connections while the app sees as many as it needs.

### Scaling the DB

| Strategy | Write throughput | Cost |
|---|---|---|
| Single Postgres | 30-60k/s | $ |
| Postgres + faster IOPS disk | 60-100k/s | $$ |
| Postgres sharding | 500k+/s | $$$ |
| Cassandra / ScyllaDB | 500k-1M/s | $$$ |

## Redis - The Game Changer

RAM access is **1000x faster** than SSD. Redis is an in-memory key-value store - a single instance handles ~100k-200k ops/s.

### Pattern: Write to Redis, sync to DB async

**The core idea:** decouple the fast path (accepting requests) from the slow path (disk writes).

![](assets/Pasted%20image%2020260603000835.png)

This pattern can achieve **1M writes/s** because writes land in RAM immediately and return - the disk write happens later in bulk.

```python
# Fast path - write to Redis queue
redis.lpush(f"queue:{shard}", json.dumps(data))

# Background sync job
batch = redis.lrange("queue", 0, 1999)
postgres.execute("INSERT INTO codes VALUES ...")  # bulk insert
```

### Redis Cluster Mode

A single Redis instance is single-threaded and caps at ~100k-200k ops/s. To scale writes further, shard across multiple instances:

```bash
# 30 Redis instances (15 masters + 15 replicas)
redis-cli --cluster create <nodes...> --cluster-replicas 1
```

In cluster mode, use hash tags to route each key to the correct shard:

```python
redis.set(f"{{{shard_key}}}:data", value)
```

With 30 Redis instances, you can reliably hit **1M writes/s**.

![](assets/Pasted%20image%2020260603001211.png)

### Migrate hot data from Postgres to Redis

If a table gets hammered constantly, moving it entirely to Redis is often the right call:

```
Postgres table (16GB on disk)  ->  Redis (20GB in RAM)
Read throughput:  400k/s       ->  300k-1M/s
Write throughput:  50k/s       ->  1M/s (cluster)
```

The tradeoff is cost (RAM is expensive) and durability (Redis can lose data on crash unless configured with AOF/RDB persistence).

## Unique ID Generation at Scale

Incrementing sequential IDs requires a global counter — every insert needs to coordinate with a central source of truth. At 1M req/s, this becomes a serialization bottleneck.

**Use UUID v4 instead:**

```python
import uuid
id = str(uuid.uuid4())  # 122-bit random ID, no coordination needed
```

Collision probability at 1M req/s: **86,000 years** to reach 50% probability of a single collision (birthday paradox). Effectively zero risk.

## Horizontal Scaling Architecture

No single machine handles all production 1M req/s traffic. Real deployments distribute across nodes globally.

![](assets/Pasted%20image%2020260603002007.png)

### Load balancer overhead

| Type | Overhead |
|---|---|
| HAProxy L4 (TCP) | ~0.05ms, negligible |
| Nginx L7 (HTTP) | ~0.2-0.5ms |
| AWS ALB | ~1-5ms |
| Kong (with plugins) | ~5-15ms |

**Use L4 load balancing when possible** — it forwards raw TCP packets without parsing HTTP. L7 load balancers (Nginx, Kong) parse every request, which adds overhead that compounds at extreme throughput.

### Gateway overhead

| Setup | Avg req/s | Drop from raw |
|---|---|---|
| Rust axum (raw) | ~420,000 | baseline |
| Nginx -> Rust axum | ~250,000 | ~40% |
| Kong (no plugins) -> Rust axum | ~100,000 | ~76% |
| Kong + auth -> Rust axum | ~60,000 | ~86% |
| Kong + auth + rate limit -> Rust axum | ~30,000 | ~93% |

Kong with 2 plugins drops throughput to ~30k req/s — roughly the same as Python FastAPI with no gateway at all. Embed auth and rate limiting inside the application instead.

### In-app auth vs gateway comparison

| Framework | Raw | + Auth (in-app) | + Auth + Rate limit (in-app) |
|---|---|---|---|
| Rust axum | 420k | 350k (-17%) | 300k (-29%) |
| C++ Drogon | 380k | 310k (-18%) | 260k (-32%) |
| Go net/http | 280k | 220k (-21%) | 180k (-36%) |
| Fastify | 100k | 75k (-25%) | 60k (-40%) |
| FastAPI (13w) | 23k | 15k (-35%) | 10k (-57%) |
| Express | 30k | 19k (-37%) | 13k (-57%) |

## Kernel Tuning - Free Performance

Before buying more hardware, tune the OS. These are one-time changes that yield 20-40% more throughput.

```bash
# Each connection consumes one file descriptor
ulimit -n 1000000

# Larger accept queue — more connections can wait before being dropped
sysctl -w net.core.somaxconn=65535

# Reuse TIME_WAIT sockets instead of waiting for them to expire
sysctl -w net.ipv4.tcp_tw_reuse=1

# Larger NIC receive queue
sysctl -w net.core.netdev_max_backlog=65535

# Make permanent
echo "net.core.somaxconn=65535" >> /etc/sysctl.conf
```

**Why this matters:** By default, Linux limits open file descriptors to 1024 per process and has a small accept queue. Under high load, connections get dropped before your application ever sees them. Raising these limits costs nothing.

## Consistency vs Speed Tradeoffs

Async queues (Redis/Kafka) break strong consistency. Knowing when that is acceptable is the key architectural decision.

| Data type | Consistency needed | Solution |
|---|---|---|
| Bank transactions, orders | Strong | Postgres, synchronous write |
| User profiles, settings | Strong | Write-through cache |
| Location updates, logs | Eventual | Redis queue -> async Postgres |
| Analytics, activity feeds | Eventual | Kafka -> ClickHouse |
| Sessions, rate limits | Weak (ok to lose) | Redis standalone |

**Read-your-writes problem:** After a write goes to Redis, a subsequent read may hit a Postgres replica that has not yet received the batch sync. Solution: route that user's reads to the primary DB for ~5 seconds after a write, then fall back to replica.

**CAP Theorem applied here:**

```
Postgres:    Consistency + Availability       (drops partition tolerance)
Cassandra:   Availability + Partition tolerance   (eventual consistency)
ZooKeeper:   Consistency + Partition tolerance    (sacrifices availability)
```

## Cost Reality Check

| Setup | Monthly cost | Max req/s |
|---|---|---|
| Single small VPS | $20 | ~50k |
| AWS c8i.32xlarge (128 cores) | $5,000 | 3M (simple) / 200k (complex) |
| AWS c8gn.48xlarge (192 cores, 600Gbps) | $8,000 | 1M+ (complex, C++) |
| Beast DB (64 cores, 256GB RAM) | $5,000-$7,000 | 50k writes/s |

Hitting 1M writes/s with raw PostgreSQL scaling would cost ~$33,000/month for the DB alone. Using Redis cluster + async sync costs a fraction of that. The architectural decision to decouple writes from the DB is not just a performance choice — it is a cost choice.

## The Step-by-Step Roadmap

| Step | What to do | Expected gain |
|---|---|---|
| 1 | Pick the right framework (Fastify > Express) | 3-5x |
| 2 | Run in cluster/multi-worker mode | 2-4x |
| 3 | Kernel tuning (ulimit, sysctl) | 20-40% |
| 4 | Fix O(N) queries -> O(log N) indexed lookups | 100-1000x on DB reads |
| 5 | Add Redis cache layer for hot data | 3-10x on DB-bound routes |
| 6 | Switch to Redis cluster for writes | scales writes to 1M/s |
| 7 | Decouple writes with async queue (Redis/Kafka) | removes DB write ceiling |
| 8 | Horizontal scaling (multiple nodes + HAProxy) | linear scaling |
| 9 | Rewrite hot paths in C++/Rust if CPU-bound | 2-5x over Node/Python |
| 10 | Use UUID instead of sequential IDs | removes ID contention |

## Key Mental Models

**"The database is always the bottleneck"** - only true at moderate scale. At extreme scale, your NIC, JSON parser, ID generation, and load balancer all become the bottleneck before the DB if you architect correctly.

**"A simple mistake costs tens of thousands of dollars"** - O(N) vs O(log N) is not academic at this scale. A full table scan with 10M rows took 43 seconds per query. At 1M req/s, that is catastrophic.

**"Decouple the fast path from the slow path"** - accept requests instantly into memory, write to disk asynchronously. This single decision is what separates 50k/s systems from 1M/s systems.

**"Horizontal scaling has limits too"** - more workers help until the OS/network becomes the bottleneck. More connections help until the app queue fills. A better runtime removes the ceiling entirely.

## Real Companies at 1M+ req/s

| Company | Approach |
|---|---|
| Cloudflare | Rust + XDP kernel bypass |
| Netflix | FreeBSD kernel tuning + C |
| Discord | Migrated from Go to Rust for throughput |
| Figma | Rust for real-time sync |
| Amazon IAM | C++ - ~400M req/s |
| Uber | Redis for location writes + async sync to DB |

## Exercises

- Given a service at 50k req/s hitting CPU limits, trace through the roadmap table above and identify which steps apply before buying more hardware
- Design the connection pooling strategy for a Python FastAPI service with 13 workers talking to a single Postgres node — what is the max safe pool size per worker?
- Sketch the Redis cluster setup for 1M writes/s — how many shards, what replication factor, and what happens on a master failure?
- A route does `SELECT COUNT(*) FROM events WHERE user_id = $1` on a 100M row table. The query takes 2s. Propose a fix without changing the schema.

---

## Further Reading

**Primary Source**

- [Let's Handle 1 Million Requests per Second, It's Scarier Than You Think!](https://www.youtube.com/watch?v=W4EwfEU8CGA) - the video walkthrough this note is based on; covers the full experiment from Node.js to C++, network saturation, and Redis cluster setup live

**Throughput and Performance**

- _Designing Data-Intensive Applications_ by Martin Kleppmann - Ch. 1 (Reliability, Scalability, Maintainability) and Ch. 5 (Replication) are directly relevant to the consistency tradeoffs covered here
- [Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) by Brendan Gregg - covers kernel tuning, CPU profiling, and network stack performance in depth

**Redis**

- [Redis Cluster Specification](https://redis.io/docs/reference/cluster-spec/) - covers hash slot distribution, failover, and the guarantees (and non-guarantees) of cluster mode
- [Redis Persistence](https://redis.io/docs/management/persistence/) - AOF vs RDB tradeoffs for durability when using Redis as a primary store

**Databases at Scale**

- [PgBouncer documentation](https://www.pgbouncer.org/usage.html) - connection pooling modes (session, transaction, statement) and when each applies
- [Use the Index, Luke](https://use-the-index-luke.com/) - practical guide to SQL indexing; directly relevant to the O(N) vs O(log N) query problem
