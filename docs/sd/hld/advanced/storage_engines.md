# Storage Engines

## Designing a Distributed Cache

**Requirements**

- High throughput, low latency, distributed
- GET, PUT, DEL, TTL support
- Designed to scale by default

### Single Node Cache

**Bare minimum operations:** GET / PUT / DEL

![](assets/Pasted%20image%2020250915194835.png)

You can always extend functionality to support complex data structures like sets, lists, sorted sets, etc.

Each key maps to an object:

```go
type Object struct {
    dataType string  // e.g., "list", "set", "string"
    data     any
}
```

Each key has an associated type which determines the operations supported on it.

Objects are stored in a Hash Table:

```text
key1 -> Object{type: "list",  data: [...]}
key2 -> Object{type: "set",   data: {...}}
```


![](assets/Pasted%20image%2020250915195150.png)

**Communication: TCP → gRPC (or custom binary protocol)**

![](assets/Pasted%20image%2020250915195329.png)

Every protocol has trade-offs, but you can support multiple communication modes by abstracting the transport layer behind an interface.

![](assets/Pasted%20image%2020250915195629.png)

**Why prefer gRPC or raw TCP over HTTP?**

- Connection pooling - avoids repeated TCP 3-way handshakes per request
- Performant serialization/deserialization (Protocol Buffers vs JSON)
- Lower overhead per request

### Cache Eviction (Cache Full)

When the cache is full, you need to make space for newer entries.

**Eviction Algorithms:**

- **LRU (Least Recently Used):** Good for CDNs, news feeds (recency matters)
- **LFU (Least Frequently Used):** Good for encyclopedias/wikis (popular pages stay hot)
- **Random Eviction:** Simple, works surprisingly well in practice

**Detecting a full cache - two approaches:**

1. Cap on the maximum number of keys in the hash table
2. Cap on the cumulative byte size of all values


$$
\text{total\_size} = sizeof(obj)
$$


Redis uses `zmalloc()` to track allocated memory precisely.

Eviction is triggered only when the cache is full. Read about constant-time LRU and LFU implementations (both achievable with a doubly linked list + hash map).

### Handling TTLs

Every key has an associated absolute expiry timestamp. A background cleanup process on each cache server periodically:

1. Identifies expired keys
2. Frees their memory (`free(obj)`)
3. Lets the garbage collector (or allocator) reclaim it

**Efficiently finding keys to expire - two strategies:**

**Priority Queue (Min-Heap on expiry time)**

- Keys ordered by absolute expiration timestamp
- Advantages: Simple, consistent, predictable
- Disadvantages: Extra memory; heap operations are O(log n)

**Lazy Deletion + Sampling (Redis approach)**

- On every access, check if the key is expired and delete if so (lazy deletion)
- Additionally, sample 20 random keys, free the expired ones
- Repeat the sampling loop until fewer than 25% of sampled keys are expired

### Scaling a Single Node

Vertical scaling: add more RAM, CPU, network bandwidth.

**Core operations and their complexity:**

- `GET k` → O(1) hash table lookup and return
- `PUT k, v` → O(1) hash table insert
- `DEL k` → O(1) hash table delete

### Concurrency

When two or more concurrent write/delete operations target the same key, you have a classic concurrency problem. Three standard approaches:

**Pessimistic Locking**

```
acquire_lock()
    DELETE k
release_lock()
```

Block other threads from accessing shared memory using mutexes/semaphores. Simple correctness guarantee, but contention can hurt throughput.

**Optimistic Locking**

Assume conflicts are rare. Make updates conditional using compare-and-swap (CAS):

```
// Only one succeeds; the other retries or fails
CAS(a, expected=10, new=20)
CAS(a, expected=10, new=30)

```

Standard CAS instructions exist in most languages/CPUs. This avoids lock contention under low conflict.

**Single-Threaded Event Loop**

Redis takes this approach - all commands are processed sequentially by a single thread, avoiding locking overhead entirely. Parallelism is achieved by running multiple Redis instances.

> **Fun exercise:** How would you use MySQL as a cache? (Hint: it can match cache throughput with the right schema, indexes, and connection pooling.)

## Making the Cache Distributed

A single node cannot handle the full load beyond a point - you need to shard data across multiple cache servers.

Range-Based Routing (Naive)
Partition the key space by range:

- C1: keys [a–j]
- C2: keys [k–t]
- C3: keys [u–z]

Problems: uneven key distribution, hotspots, and painful rebalancing when nodes are added/removed.

There could be 4 scenarios for range based routing

![](assets/Pasted%20image%2020250917000941.png)

### Consistent Hashing : for determining ownership

Consistent hashing solves the rebalancing problem by mapping both keys and nodes onto a ring (hash ring). A key is owned by the first node clockwise from it on the ring.

![](assets/Pasted%20image%2020250916234538.png)

#### Add a new cache server

New node (C5) takes over a slice of an existing node's (C1's) range

*Minimal data transfer* - only the keys in the transferred range move

![](assets/Pasted%20image%2020250916234743.png)

In practice: snapshot C1's state → bootstrap C5 → gradually clean up migrated keys from C1

> Note: Virtual nodes are generally a good idea for stateless services (they improve load distribution). For stateful applications like a cache, virtual nodes complicate rebalancing significantly — use with caution or avoid.

#### Removing a cache server

![](assets/Pasted%20image%2020250916234947.png)

Two cases:

1. **Graceful shutdown:** Migrate data to the next node on the ring before going offline
2. **Abrupt outage:** Rely on replicas to serve the lost node's data

### High Availability & Reliability

- **Replicas:** Each cache node has one or more replicas that hold the same state — used for failover
- **Standby nodes:** Warm standbys ready to take over on failure
- **Write-Ahead Logging (WAL):** Persist writes to a log before applying them, enabling recovery after a crash

### Distributed Hash Table (DHT)

A distributed cache is fundamentally a **Distributed Hash Table (DHT)** - a system that maps keys to values spread across nodes, optimized for minimal data movement when nodes join or leave.

DHTs are used in:

- Distributed file systems (IPFS, GFS)
- DNS resolution
- Peer-to-peer file sharing (BitTorrent uses the Kademlia DHT)
- Instant messaging infrastructure


![](assets/Pasted%20image%2020250916235611.png)

![](assets/Pasted%20image%2020250917000027.png)

## ETL & Tiered Storage

Say, we are building a multi-user blogging application in which the data is stored in *Transactional Database* like MongoDB

![](assets/Pasted%20image%2020250915114251.png)

Our application grew big and now the CEO wants detailed reporting and stats and dashboards and for that you have a dedicated Insights Team.
But the insights team only knows SQL.
So, how will they build the dashboards on MongoDB when they only know SQL ?

One way would be to send *events* from API in Kafka then process it into worker and put it into some SQL server.

![](assets/Pasted%20image%2020250915115004.png)

**Problems with event-based CDC:**

- Events carry application context, not raw data - they may be incomplete
- Not all changes produce events (e.g., bulk updates, migrations)
- If an event fails to send after a write, you have an inconsistency

So many challenges ! can we do better

### Change Data Capture (CDC)

Instead of relying on application events, tap directly into the **database's commit log** (also called the binary log / `binlog` in MySQL, or the oplog in MongoDB).

![](assets/Pasted%20image%2020250915115340.png)

CDC tools read these logs and:

1. Optionally transform the data
2. Write it to a sink (Kafka, SQS, another database, a data warehouse)

You can also choose to do it manually or your own way just pick appropriate SINK e.g. Kafka, SQS, Broker, and build your own complex transformations.

The core idea is to NOT rely on events and rely on Database.

Say we have *Blogs* table and we insert, update, delete something. we get one CDC event for every change that happened in the database.

**CDC is heavily used in:**

- Multi-tiered storage architectures (hot → warm → cold)
- Real-time analytics pipelines
- Database migrations and replication
- Keeping search indexes in sync with transactional DBs

![](assets/Pasted%20image%2020250915120028.png)

**Popular CDC tools:** Debezium, Airbyte, AWS DMS, Fivetran

## Exercises

- Set up a CDC pipeline locally (Debezium + Kafka + Postgres is a solid starting point)
- Read about and implement constant-time LRU and LFU (doubly linked list + hash map)
- Implement your own consistent hashing algorithm with virtual node support

## Further Reading

**Distributed Caching**

- [Redis Architecture](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/) - Redis Cluster internals, hash slots, and replication
- _Designing Data-Intensive Applications_ - Ch. 6 (Partitioning) and Ch. 5 (Replication) by Martin Kleppmann
- [Consistent Hashing and Random Trees](https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf) - Karger et al., the original paper

**Eviction & Memory Management**

- [Redis eviction policies](https://redis.io/docs/latest/develop/reference/eviction/) - LRU, LFU, and allkeys-* policies explained
- [How Redis expires keys](https://redis.io/docs/latest/develop/use/keyspace/) - lazy + active expiry internals

**Consistent Hashing**

- [Amazon Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) - §4.2 covers consistent hashing with virtual nodes in production

**CDC & ETL**

- [Debezium documentation](https://debezium.io/documentation/) - most widely used open-source CDC framework
- [The Log: What every software engineer should know about real-time data's unifying abstraction](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) - Jay Kreps, LinkedIn (foundational read, already on your list)
- [Turning the database inside out](https://martin.kleppmann.com/2015/11/05/database-inside-out.html) - Martin Kleppmann's talk on CDC and stream processing

**DHTs**

- [Kademlia: A Peer-to-peer Information System Based on the XOR Metric](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) - the DHT algorithm BitTorrent uses
- [Chord: A Scalable Peer-to-peer Lookup Service](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf) - a simpler DHT, good for understanding the fundamentals