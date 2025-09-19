# High Throughput

Why we build word dictionary on S3 ?

- embedded database
- cheap storage, costly access
- cold storage with infrequent access

Why we studied Bitcask ?

- log-structured storage
- Kafka  Similar high write throughput systems use that
- Metrics, Analytics, click-stream, uses log-structured.

## Multi-Tiered Datastore

Cost efficient Order Storage Systems

Transactional System : *Orders* -> all orders that happen on Amazon goes through this. So scale on the system becomes a top priority

![](assets/Pasted%20image%2020250918113142.png)

Everything works fine for the first few months, and then Database performance degrades -> large number of writes & reads

![](assets/Pasted%20image%2020250918113341.png)

The next phase of DB scaling seems to *Sharding*
Sharding is not always a great choice because

- multi-tenant isolation
- operational overhead.

![](assets/Pasted%20image%2020250918113515.png)

#### What next after replicas ?

Root cause of DB degradation. -> Table is too large, computation takes time, index lookups are disk bound.

Can we reduce the table size ?

### Access Pattern

The Idea : move orders from one DB to another depending on its age to *reduce the load* on the transactional database.

![](assets/Pasted%20image%2020250918113916.png)

### Tiered Datastore
By moving data from one tier to another we are reducing the time to computation

#### Hot Store : Transactional store (read/write)

- transactional
- low latency
- strong consistency
- expensive

#### Warm Store : Read-only workloads

- read-only
- non-transactional
- frequent reads
- could be a little slower
- horizontally scalable
- less expensive

#### Cold Store : Infrequent reads, cheap, very slow

- read-only
- very infrequent reads
- compliance and accounting
- offline analytics

![](assets/Pasted%20image%2020250918115830.png)

## Designing S3

Requirements

- Blob Storage
- Network File System
- Scalable & Cheap

S3 : just a distributed file storage that scales *infinitely*

Day 0 architecture

![](assets/Pasted%20image%2020250918232808.png)

S3 is just like a Static File Server. `s3://bucket.s3.aws.com/image/logo.png`
Request comes to the API server then goto storage and fetch the file at the location specified and return it.

If one HDD is not enough what is the next stage of evolution. ? *Two HDDs*

![](assets/Pasted%20image%2020250918233021.png)

What if one computer is not able to support all the request. You can add more machines ! But before that makes the storage central and add a load balancer.

![](assets/Pasted%20image%2020250918233259.png)

#### Storage Layer

What type of storage to use here ? and why ?

![](assets/Pasted%20image%2020250918222918.png)

How can we have an infinite storage ?

Spinning disk (cheap) HDD. To get write performance. No disk seek. Log Structured Storage Filesystem.

![](assets/Pasted%20image%2020250918224846.png)

*How do we get infinite/scalable storage ?*

There is a device driver in each server rack which connects all disk in serial, and keeps track of the head of the write pointer. To ensure new write don't conflict with switching to new disk we redirect new writes to new disk, 70% full on current disk.

But device driver is limited to the rack, we can have another monitor/switch application connecting racks.

Delete in S3 is classic use case of merge and compact (defragmentation).
Updating in S3 would require writing the same object to a new location, in a structured log manner and mark previous items old version. (*giving object versioning feature*)

How does the S3 API server know which HDD (nodes) to go to ?

### Routing

#### Hash Based Partitioning
For every path, compute hash & pick a HDD and store/read there.

*Advantages:* near random allocation, near uniform distribution, no explicit configuration

Disadvantages : What if number of HDD changes ?

- rebalancing
- reindexing

Files of same bucket may lie on different nodes. You do not get *tenant isolation*
Files from multiple tenants may lie on same node, load from one client will affect performance of others.

Hash Based Routing is almost always bad as it takes control away from user & doesn't enforce data locality.

#### Consistent Hashing

Partitioning & keys on a consistent hash ring.
The node to the right owns the data

Advantages: Minimal data transfer when new storage node is added or removed, Near random/near uniform distribution.
Disadvantage:

- no tenant isolation
- workload of one will affect the other
- files of one tenant are spread across nodes.

#### Range Based Partitioning

*Hash based approaches loses locality of objects*
We want more control to partitioning logic.

- easier performance isolation
- locality of objects
- more control over where objects are residing

`bucket/_/_`

`amzn/image/a.jpg`
`amzn/image/b.jpg`

![](assets/Pasted%20image%2020250918231428.png)

*Dealing with hot nodes*

When a node becomes *hot*, scale out (split into two)
Simple with ranges based partitioning. If requests go beyond a certain limit you can limit `#request` per account.

![](assets/Pasted%20image%2020250918231758.png)

#### Another way to solve Hot Nodes (not S3)
Have large number of logical shards (partitions) on a few physical machines

![](assets/Pasted%20image%2020250918232129.png)

- Elastic Search uses this strategy. (Head Plugin)
- Instagram did this with their main posts table.

Key reason : Moving one exclusive subset of data across data nodes (load balancing) is simpler & efficient.

How do we know which partition is on which node ?

There has to be an entry some where *Partition Map Table*, and someone (*Partition Manager*) needs to manage the partitions movement.


![](assets/Pasted%20image%2020250919000601.png)

One partition is owned by one partition server but one partition server can own multiple partitions.


![](assets/Pasted%20image%2020250919001259.png)

Making partition manager no *SPOF*

![](assets/Pasted%20image%2020250919001524.png)


NOTE: below diagram seems counterintuitive to having each microservice own its own data. but here since data can be huge it makes sense to directly pickup the files rather than sending it around.

![](assets/Pasted%20image%2020250919001944.png)

What happens when a partition server goes down ?


### Data Durability

Duplication Data : only way to achieve durability

![](assets/Pasted%20image%2020250919002306.png)



#### Data Integrity : End-to end checksum

Within same storage node durability ? *RAID*

- We have to ensure that we never save or return corrupted data
- So, we check & validate checksum across all systems & components while storing & retrieving data
- Multiple Chunk -> combined -> integrity -> checksum

Read following Research papers

- Windows Azure Storage : A highly available cloud storage service with strong consistency
- Building a database on S3
- SCUBA by Facebook

Following Book is great for DB

- Database internals by Alex Petrov

