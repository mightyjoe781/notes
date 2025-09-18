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