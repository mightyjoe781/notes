# Storage Systems II

## Word Dictionary without using any DB

**Requirements**

- Scalable storage (portable) and API servers (response time can be high)
- No traditional database
- Words and meanings are updated weekly via a changelog
- Lookup is always a single word
- Dictionary is 1TB, containing ~170,000 words

### Storage Design

Since we can't use a traditional DB, let's use S3 (network-attached storage) as a raw filesystem.

**Approach 1: One file per word**

```txt
s3://word-dict/a/apple.txt
            .../america.txt
            ....
            .../z/zoo.txt
```

One folder per starting character. Lookup: `get_word(w)` → construct S3 path → read file → return meaning.

Problem: breaks the **portability** requirement. 170,000 separate files tied to S3's path structure can't be easily packaged or moved.

**Approach 2: Single flat file (CSV)**

Store all words and meanings in one file. Simple, portable. But the file is 1TB - a linear scan for lookup is far too slow and expensive.

### Making Lookups Fast - Indexing

The universal strategy for fast lookups is **indexing**. We split the data logically into two parts: `index.dat` and `data.dat`.

```
word → (offset in data.dat, length)
```

![](assets/Pasted%20image%2020250917211217.png)

**How big is the index?**

```
~171,476 words × avg entry size of ~15.7 bytes ≈ 2.6 MB
```

2.6 MB fits comfortably in memory. This changes the whole lookup flow.

**API server boot sequence:**

1. Load `index.dat` into memory
2. On receiving a request, look up the word in the in-memory index
3. Get the offset and length
4. Issue a single S3 range-read at that offset
5. Return the meaning

![](assets/Pasted%20image%2020250917214912.png)

---

### Updating the Dictionary

Updates arrive as a **changelog** (a diff of added/modified words).

**Update procedure:**

1. Spin up a new server
2. Download the current dictionary locally
3. Download the changelog
4. Merge in O(n) - produce a new `data.dat` and `index.dat` locally
5. Upload both to S3

**Why is merge O(n)?**

Both the dictionary and the changelog are sorted. Merging two sorted lists is O(n) - a standard merge step from merge sort.

![](assets/Pasted%20image%2020250917214633.png)

### Handling the Transition (Zero Downtime Updates)

If we overwrite files at the same S3 path, in-flight servers still hold the old index, causing garbage responses. Three options:

1. **Periodic refresh:** Servers reload the index on a schedule (e.g., every hour)
2. **Reactive:** Use Redis Pub/Sub to notify all API servers to reload immediately
3. **Parallel setup (cleanest):**
    - Upload the new `index.dat` and `data.dat` to a new versioned S3 path
    - Update a `meta.json` file to point to the new path
    - New/restarted servers read `meta.json` on boot and serve from the new files
    - Old servers continue serving the old files until they restart or refresh

![](assets/Pasted%20image%2020250917214923.png)

This gives a clean, atomic cutover with no user-visible inconsistency.

![](assets/Pasted%20image%2020250917223334.png)

### Solving Portability — The Single-File Format

Two separate files (`index.dat` + `data.dat`) aren't portable. Let's merge them into one file.

**Problem:** How does a reader know where the index ends and data begins?

**Bad idea:** Use a separator character - the separator could appear in data.

**Good idea:** Use a **fixed-width header**.

![](assets/Pasted%20image%2020250917222136.png)

The header stores:

- Byte offset where the index starts
- Byte offset where the data starts
- Metadata: total word count, version, etc.

![](assets/Pasted%20image%2020250917222143.png)

**New API server boot sequence:**

1. Read the fixed-size header (known size, always at byte 0)
2. Use header offsets to load the index section into memory
3. Begin serving requests

This single-file format is fully portable - copy it anywhere and it works.

### Real-World Applications of This Pattern

- **Multi-tiered storage:** Recent orders in MySQL, historical orders as indexed flat files on S3 - without losing query ability on historical data
- **Apache Parquet / ORC:** Column-oriented file formats that embed their own index/schema in a file footer (same idea as our header)
- **AWS Athena / Data Lakes:** Query structured flat files on S3 directly, no database required
## Superfast DB KV

**Requirements:** Superfast reads, writes, deletes - with persistence

### Why Append-Only Files Are Fast

SSDs are closer to memory than spinning disks in both cost and speed, but the design principle here matters most for **HDDs**: sequential writes avoid disk seeks, which are the bottleneck on rotating media.

![](assets/Pasted%20image%2020250917230428.png)

**Log-Structured Storage:**

- Data written to append-only files
- Sequential writes only - no random updates, no disk seeks during writes
- Result: very high write throughput, especially on HDDs

> Note: SSDs don't benefit as dramatically from sequential writes since they have no seek penalty, but the design still simplifies the storage engine considerably.

### Simple Design: Append-Only KV File

![](assets/Pasted%20image%2020250917231928.png)

```
PUT(k, v) → append entry to file   ← extremely fast
DEL(k)    → append a tombstone entry: PUT(k, tombstone)
```

Deletes are also appends - no random disk writes ever.

**On-disk entry format:**

![](assets/Pasted%20image%2020250917232240.png)

When reading one entry from file, do we know how much to read. We cannot read *until newline*, not optimal
*Because key and value are of variable length*

![](assets/Pasted%20image%2020250917232248.png)

```
[ CRC (4B) | Key Size (4B) | Value Size (4B) | Key | Value ]
```

- Read `Key Size` and `Value Size` first (fixed 4 bytes each)
- Then read exactly that many bytes for the key and value
- **CRC** is written first — used to detect corruption on read

**Detecting corruption:** Compute CRC over the entry; if it doesn't match the stored CRC, the entry is corrupt and can be discarded.

#### Solving Integrity

![](assets/Pasted%20image%2020250917232732.png)

Finding corrupt entries : CRC -> first thing we flush

![](assets/Pasted%20image%2020250917232724.png)

### Faster GET - In-Memory Hash Index

To achieve O(1) reads, maintain an in-memory hash table:

![](assets/Pasted%20image%2020250917233018.png)

```
key → (file_id, offset, size)
```

**GET(k):**

1. Hash table lookup → get file ID + offset
2. Seek to that offset on disk
3. Read and return the value

**Limitation:** All keys must fit in memory (values live on disk, only keys are indexed).

### File Rotation and Compaction

**Problem:** The append-only file grows forever.

**Solution:** Rotate the file every _t_ bytes. The current file becomes **immutable**; a new active file is created.


![](assets/Pasted%20image%2020250917233227.png)


#### Changes in our in-memory index

![](assets/Pasted%20image%2020250917233700.png)

**Problem:** Many files accumulate stale and deleted entries.

**Solution:** **Merge and compact** immutable segments in the background:

- **Merge:** Combine multiple segment files, keeping only the latest value per key
- **Compact:** Skip tombstone (deleted) entries entirely

![](assets/Pasted%20image%2020250917233832.png)

After compaction, byte offsets change - the in-memory index must be **updated atomically** to reflect new file IDs and offsets.

Limitations of the DB : Keys must fit in memory
Strength of this DB : O(1) reads, writes, deletes

- High throughput, low latency
- I/O stauration
- Easy Backups

What we just designed is *Bitcask*

### Bitcask

This is the **Bitcask** storage engine, used in production at Uber as the storage backend for **Riak**.

**Riak** is a distributed key-value store that wraps Bitcask, adding distributed features (consistent hashing, replication, fault tolerance) on top of each node's local Bitcask instance.

![](assets/Pasted%20image%2020250917234340.png)

**Bitcask characteristics:**

|Property|Detail|
|---|---|
|Reads|O(1) — one disk seek per GET|
|Writes|O(1) — sequential append|
|Deletes|O(1) — tombstone append|
|Throughput|Very high — I/O saturating|
|Constraint|All keys must fit in RAM|
|Backups|Trivial — copy the immutable segment files|

---

## Exercises

- Implement a basic Bitcask-style storage engine
- Read the [Bitcask paper](https://riak.com/assets/bitcask-a-log-structured-hash-table-for-fast-key-value-data.pdf)
## Further Reading

**Word Dictionary / Indexed Flat Files**

- [Apache Parquet format spec](https://parquet.apache.org/docs/file-format/) - see how Parquet embeds its schema and row-group index in a file footer (same header concept, production-grade)
- [SSTable and LSM-Tree](https://www.cs.umb.edu/~poneil/lsmtree.pdf) - O'Neil et al., the LSM-Tree paper - a natural next step from the indexed flat file design

**Log-Structured Storage**

- [Bitcask: A Log-Structured Hash Table for Fast Key/Value Data](https://riak.com/assets/bitcask-a-log-structured-hash-table-for-fast-key-value-data.pdf) - the original Basho paper, short and very readable
- _Designing Data-Intensive Applications_ - Ch. 3 (Storage and Retrieval) covers log-structured engines, SSTables, and LSM-Trees in depth
- [LevelDB implementation notes](https://github.com/google/leveldb/blob/main/doc/impl.md) - how Google's LSM-based KV store extends the ideas here

**Compaction & Merge Strategies**

- [RocksDB tuning guide](https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide) - production-grade compaction strategies (size-tiered vs leveled) used at Facebook

**Riak**

- [Riak architecture overview](https://docs.riak.com/riak/kv/latest/learn/concepts/) - how Riak distributes Bitcask across a cluster using consistent hashing