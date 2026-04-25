# High Throughput

## Recap: Why These Designs Matter

**Why did we build the word dictionary on S3?**

- Demonstrates embedded/file-based databases without a traditional DB engine
- S3 is cheap storage with costly per-access pricing - ideal for cold storage with infrequent access
- Shows how indexing can make flat-file lookups practical

**Why did we study Bitcask?**

- Demonstrates log-structured storage - the foundation of high write throughput systems
- Kafka, metrics pipelines, analytics engines, and clickstream processors all use log-structured designs for the same reason: sequential appends are fast
- Establishes the building blocks for understanding LSM-Trees and SSTable-based engines

## Multi-Tiered Datastore

### The Problem: Cost-Efficient Order Storage at Scale

Consider Amazon's order system. Every order flows through a transactional database. At launch this works fine, but as the system grows:

- Write and read volume increases
- The orders table becomes very large
- Index lookups become disk-bound
- Query performance degrades

![](assets/Pasted%20image%2020250918113142.png)

Everything works fine for the first few months, and then Database performance degrades because of large number of writes & reads

![](assets/Pasted%20image%2020250918113341.png)

The next phase of DB scaling seems to be *Sharding* but sharding introduces significant problems:

- Multi-tenant isolation becomes difficult
- Cross-shard queries and transactions are painful
- Operational overhead is high

![](assets/Pasted%20image%2020250918113515.png)

#### What next after replicas ?

**Root cause of degradation:** The table is simply too large. All orders - new and old - compete for the same resources.

**Key insight:** Do users actually query 3-year-old orders as frequently as last week's orders? Almost never. Access patterns are heavily skewed toward recent data.

### Access Pattern

*Move orders between storage tiers* based on age. This reduces the working set of the hot transactional database without sharding it.

![](assets/Pasted%20image%2020250918113916.png)

### Tiered Storage Architecture

**Hot Store - Transactional (read/write)**

- Low latency, strong consistency
- Full transactional support (ACID)
- Expensive (e.g., RDS, Aurora)
- Stores recent orders (e.g., last 90 days)

**Warm Store - Read-heavy workloads**

- Read-only, non-transactional
- Slightly higher latency acceptable
- Horizontally scalable, less expensive
- Stores older orders (e.g., 90 days–2 years)

**Cold Store - Archival**

- Read-only, very infrequent access
- Compliance, accounting, offline analytics
- Very cheap, slow retrieval acceptable (e.g., S3, Glacier)
- Stores everything older than 2 years

A background migration job (driven by CDC or a scheduled process) moves records across tiers as they age. The API layer routes queries to the appropriate tier based on the order's age or ID range.

![](assets/Pasted%20image%2020250918115830.png)

## Designing S3

**Requirements:**

- Blob/object storage
- Accessible as a network file system
- Infinitely scalable and cheap

S3 : just a distributed file storage that scales *infinitely*

### Day 0: The Simplest Design

S3 is conceptually a static file server:

![](assets/Pasted%20image%2020250918232808.png)

```
s3://bucket.s3.aws.com/images/logo.png
```

Request comes to the API server then go to storage and fetch the file at the location specified and return it.

As storage needs grow, you add more HDDs. 

![](assets/Pasted%20image%2020250918233021.png)

As request volume grows, you add more API servers behind a load balancer and move to a centralized, shared storage layer.

![](assets/Pasted%20image%2020250918233259.png)

### Storage Layer Design

**Why HDDs over SSDs here?**

S3 is optimized for cost and throughput, not latency. Spinning disks (HDDs) are far cheaper per GB. The key to getting good write performance on HDDs is eliminating disk seeks - which is exactly what log-structured storage provides.

![](assets/Pasted%20image%2020250918222918.png)

**Log-structured filesystem on HDDs:**

- All writes are sequential appends - no random writes, no disk seeks
- High write throughput even on spinning disks

![](assets/Pasted%20image%2020250918224846.png)

**Achieving infinite/scalable storage:**

Each server rack has a device driver that manages all disks in the rack serially and tracks a single write-head pointer. When the current disk reaches ~70% capacity, new writes are redirected to the next disk. A higher-level rack monitor connects multiple racks, extending this to cluster scale.

**Deletes** in S3 are implemented as tombstone entries - the actual data is reclaimed lazily during background **merge and compaction** (defragmentation).

**Updates** in S3 write the new object to a new location and mark the old entry as a previous version - this is what gives S3 its **object versioning** feature naturally.

### Routing: How Does the API Server Know Which Node to Use?

#### Hash-Based Partitioning

Hash the object path → pick a storage node.

- **Advantages:** Near-random, near-uniform distribution; no explicit configuration
- **Disadvantages:**
    - Rebalancing and re-indexing required whenever nodes are added or removed
    - Files from the same bucket may be spread across many nodes - no tenant isolation
    - Load from one high-traffic tenant can impact others sharing the same node

Hash-based routing gives up locality and control, making it a poor choice for an object store.

#### Consistent Hashing

Map both objects and nodes onto a hash ring. Each node owns the keys in the arc to its left.

- **Advantages:** Minimal data movement when nodes are added/removed; near-uniform distribution
- **Disadvantages:** Same tenant isolation problems as hash-based partitioning - files are still spread across nodes, and one tenant's workload affects others

#### Range-Based Partitioning (What S3 Actually Uses)

Partition the key space by prefix ranges. This preserves **locality of objects**.

- **Advantages:**
    - Tenant isolation - one bucket's files can be colocated
    - Easier performance isolation per tenant
    - Full control over where data resides
    - When a node becomes hot, **split its range** into two sub-ranges and assign each to a separate node

```
amzn/images/a.jpg  →  Node A
amzn/images/b.jpg  →  Node A
amzn/videos/x.mp4  →  Node B
```

![](assets/Pasted%20image%2020250918231428.png)

**Handling hot nodes:** If a single prefix receives too much traffic, split the range. You can also enforce per-account request rate limits as an additional control

![](assets/Pasted%20image%2020250918231758.png)

### Logical Shards on Physical Nodes (General Strategy)

An alternative to direct range ownership is maintaining many **logical shards** mapped onto fewer **physical nodes** via a partition map.

This is how **Elasticsearch** (index shards) and Instagram's posts table work.

![](assets/Pasted%20image%2020250918232129.png)


**Why it helps:**

- Moving one logical shard between physical nodes is a well-defined, bounded operation
- Load balancing becomes: reassign a shard, not migrate arbitrary data ranges

**Components needed:**

- **Partition Map Table:** Records which logical shard lives on which physical node
- **Partition Manager:** Orchestrates shard movement and keeps the map consistent




![](assets/Pasted%20image%2020250919000601.png)

One physical node can own multiple logical shards, but each logical shard has exactly one owning node at a time (plus replicas).


![](assets/Pasted%20image%2020250919001259.png)

**Avoiding a Single Point of Failure (SPOF) on the Partition Manager:**

The Partition Manager must itself be highly available — run it as a replicated service (e.g., backed by ZooKeeper, etcd, or Raft consensus).

![](assets/Pasted%20image%2020250919001524.png)


NOTE: The following diagram seems counterintuitive to having each microservice own its own data. But here, since data can be huge, it makes sense to directly pick up the files rather than sending them around.

![](assets/Pasted%20image%2020250919001944.png)

What happens when a partition server goes down ?
### Data Durability

The only reliable way to achieve durability is **replication**.

Each object is written to multiple storage nodes (typically 3 replicas across different racks or availability zones). A write is acknowledged only after a quorum of replicas confirm it.

![](assets/Pasted%20image%2020250919002306.png)



**Data Integrity: End-to-End Checksums**

Bit rot, hardware faults, and network corruption are real at scale. Every component in the read/write path validates a checksum:

- Computed when data is written
- Verified when data is read
- Applied at each hop: client → API server → storage node
- For large objects split into chunks, each chunk carries its own checksum; a combined checksum covers the full object

Within a single storage node, **RAID** provides an additional layer of hardware-level redundancy.

---

## Exercises

- Trace a PUT and GET request through the full S3 design above, identifying every component touched
- Implement a simplified range-based partition manager with a shard map
- Read the papers listed below

---

## Further Reading

**Research Papers**

- [Windows Azure Storage: A Highly Available Cloud Storage Service with Strong Consistency](https://sigops.org/s/conferences/sosp/2011/current/2011-Cascais/printable/11-calder.pdf) - Microsoft's production blob storage architecture; covers stream layer, partition layer, and end-to-end checksums
- [Building a Database on S3](https://dl.acm.org/doi/10.1145/1376616.1376645) - Brantner et al.; explores using S3 as a database storage backend
- [SCUBA: Diving into Data at Facebook](https://research.facebook.com/publications/scuba-diving-into-data-at-facebook/) - Facebook's fast, scalable in-memory analytics store

**Books**

- _Database Internals_ by Alex Petrov - covers storage engines, log-structured storage, B-Trees, and distributed consensus in depth; directly extends everything in this module
- _Designing Data-Intensive Applications_ by Martin Kleppmann - Ch. 3 (Storage and Retrieval) and Ch. 6 (Partitioning) are directly relevant

**Log-Structured Storage**

- [The Log-Structured Merge-Tree (LSM-Tree)](https://www.cs.umb.edu/~poneil/lsmtree.pdf) - O'Neil et al.; the paper that formalized log-structured storage for databases
- [WiscKey: Separating Keys from Values in SSD-Conscious Storage](https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf) - a modern take on Bitcask-style key-value separation, optimized for SSDs

**Tiered Storage**

- [Amazon S3 storage classes](https://aws.amazon.com/s3/storage-classes/) - a practical overview of hot/warm/cold tiers as implemented in production (S3 Standard → S3-IA → Glacier)
