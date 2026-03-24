# High Throughput Systems

## LSM Trees

### Improving on Bitcask

Bitcask gives us:

- Append-only files (no disk seeks during writes)
- In-memory index (O(1) lookups)

**The limitation:** All keys must fit in RAM. The in-memory index grows with the number of unique keys, eventually becoming the bottleneck.

**The question:** Can we write directly to RAM instead of disk? That would make writes even faster - at the cost of durability.

**Where this niche matters:** Systems with extremely high write ingestion rates - IoT sensors, clickstream events, location updates, logging, time-series data. These workloads write far more than they read, and reads are almost always for _recent_ data.

### The Core Design: MemTable + SSTables

Instead of writing directly to disk, writes land in an **in-memory sorted buffer** called a **MemTable**.

![](assets/Pasted%20image%2020250919090931.png)

This gives higher write throughput than Bitcask because RAM writes are faster than disk appends.

**Key property:** If a key is in the MemTable, it is guaranteed to be the latest value - no need to check disk.

### Periodic Flush: MemTable → SSTable

Every `t` seconds (or when the MemTable reaches a size threshold), the buffer is flushed to disk.

**Flush to an existing file?**

- File grows too large
- Flush takes too long (writing into the middle of a large file)

**Flush to a new file on every flush (correct approach):**

- Fast - one sequential write to a new file
- Simple - each flush is an independent, immutable file

Each flush produces a new **SSTable (Sorted String Table)** — a file containing sorted key-value pairs with an embedded index. The data is sorted because the MemTable is maintained as a sorted structure (typically a red-black tree or skip list).
#### Get Key

Every flush creates a new file *SSTable* (in-memory & disk). It writes index and data in same file.
*SSTable* ~ sorted string table.

![](assets/Pasted%20image%2020250919101112.png)

**GET(k) flow:**

1. Check MemTable first - if found, this is the most recent value, return it
2. If not found, scan SSTable files on disk from newest to oldest
3. Use each file's index to check presence before reading data
4. If not found in any file, return `NOT_FOUND`

We do not need to go through each file, we check the indexes to see if the key present in the file.

### SSTable Format

Each SSTable file contains:

- An **index section** - sparse index mapping keys to byte offsets
- A **data section** - sorted key-value entries

Because SSTables are sorted, lookups within a file can use binary search. Merging multiple SSTables is O(n) - a standard merge of sorted lists.

![](assets/Pasted%20image%2020250919102217.png)

### Merge and Compaction

Over time, many immutable SSTable files accumulate on disk. This creates two problems:

1. **Space waste:** The same key may appear in multiple files (with older values being stale)
2. **Slow reads:** In the worst case, a GET must scan through every file to conclude a key doesn't exist

**Merge and compaction** runs as a background process:

- Merges multiple SSTables into one (O(n) because data is already sorted)
- Discards stale values (keeps only the latest entry per key)
- Skips tombstone entries (deleted keys)

**Worst-case read problem:** Even with compaction, checking k files to confirm a missing key is expensive.

![](assets/Pasted%20image%2020250919102917.png)

What if we have a way to know if key exists or not ?
### Bloom Filters

![](assets/Pasted%20image%2020250919103638.png)

To avoid scanning every SSTable for a missing key, each SSTable carries a **Bloom filter** - a space-efficient probabilistic data structure.

**Bloom filter properties:**

- Returns **"maybe present"** (with a configurable false positive rate)
- Returns **"definitely not present"** (with certainty)

**Why not a hash set?**

- A set grows with the number of keys - memory and disk footprint become unmanageable
- A Bloom filter has a **fixed size** regardless of the number of keys inserted, making it easy to keep in memory or embed in the SSTable file header

![](assets/Pasted%20image%2020250919103800.png)

**Updated GET(k) flow:**

1. Check MemTable - if found, return
2. For each SSTable (newest to oldest): check the Bloom filter first
    - If Bloom filter says "no" → skip this file entirely (guaranteed miss)
    - If Bloom filter says "maybe" → read the index and do the lookup
3. If not found anywhere → return `NOT_FOUND`
### Handling Data Loss - Write-Ahead Log (WAL)

The MemTable lives in RAM. A crash before a flush means losing all unflushed writes.

**Solution:** Every write is also appended to a **Write-Ahead Log (WAL)** on disk before being applied to the MemTable.

On crash recovery: replay the WAL to rebuild the MemTable state.

The WAL is **truncated after every successful flush** - once data is safely in an SSTable, the WAL entries for it are no longer needed.

**"If we write to disk on every write, how is this faster than Bitcask?"**

The WAL write is a sequential append to a single file - cheap. The expensive part (organizing data into sorted SSTables with indexes) happens lazily in the background during flush and compaction, not on the critical write path.

For zero data loss, you need a WAL. For high-throughput with some loss tolerance (e.g., metrics), you can skip or batch WAL writes.

![](assets/Pasted%20image%2020250919110030.png)

### LSM Tree vs. Bitcask vs. Redis

| Property       | Bitcask                  | LSM Tree                      | Redis               |
| -------------- | ------------------------ | ----------------------------- | ------------------- |
| Write speed    | Fast (sequential)        | Faster (RAM first)            | Fast (RAM)          |
| Read speed     | O(1)                     | O(log n) amortized            | O(1)                |
| Key constraint | All keys in RAM          | Keys can exceed RAM           | All data in RAM     |
| Durability     | WAL                      | WAL                           | Configurable        |
| Best for       | Simple KV, low key count | High ingestion, recency reads | Low-latency caching |

**LSM shines when:**

- Write volume is very high
- Reads are skewed toward recently written keys (still in MemTable)
- Dataset size exceeds available RAM (LSM is not memory-bound on keys)

**Redis can't replace LSM here:** Redis requires all data to reside in memory. LSM stores the bulk of data on disk and only keeps recent writes in RAM.

**Who uses LSM trees?** RocksDB, LevelDB, BadgerDB, Apache Cassandra, InfluxDB - all high-ingestion, write-heavy systems.

**Example use case - ad bidding:** A bid event needs to be persisted quickly. If stored in Redis, the key can expire and the data is gone. LSM gives you persistence with comparable write speed.

## Designing a Video Processing Pipeline

**Requirements:**

- Video upload
- Video processing (transcoding)
- Video distribution

### Why Transcoding Is Necessary

A raw recorded video (e.g., `.mov` at 4K) cannot be served directly to all clients because:

- Different devices support different **codecs** and **container formats**
- Different network conditions require different **bitrates**

**Key concepts:**

**Container:** A file format that packages audio, video, subtitles, and metadata together. Examples: `.mp4`, `.mkv`, `.avi`

**Codec:** The algorithm used to compress and decompress the audio/video stream. Examples: H.264, H.265/HEVC, VP9, AV1

**Bitrate:** The amount of data encoded per second. Higher bitrate = higher quality, but requires more bandwidth and processing power.

Since not all users have fast connections or powerful devices, a single video must be transcoded into multiple resolutions and bitrates (e.g., 1080p, 720p, 480p, 360p). The client dynamically switches between them based on network conditions - this is **Adaptive Bitrate Streaming (ABR)**, the mechanism behind HLS and DASH.

> Useful reference: [howvideo.works](https://howvideo.works) for a visual deep-dive into video fundamentals.

Use **ffmpeg** for transcoding in practice.

![](assets/Pasted%20image%2020250919231336.png)


*Janus*, *WebRTC*, *TURN servers*, *100ms* website, etc are great sources of content.

Now that we know transcoding is essential, we put it in our design.

### Transcoding Architecture

- Workflow Management - Airflow, Luigi
- Event Driven - Kafka

**Two orchestration approaches:**

**Workflow management (Airflow, Luigi, Temporal):**

- Better for complex, multi-step pipelines with dependencies (upload → validate → transcode → thumbnail → publish)
- Provides retry logic, observability, and DAG-based scheduling out of the box
- Avoids managing multiple Kafka topics for each pipeline stage

**Event-driven (Kafka):**

- Better when transcoding is one step in a broader real-time data platform
- Higher operational complexity for a pure video pipeline

For a dedicated video processing system, a **workflow management tool is the cleaner choice**.

![](assets/Pasted%20image%2020250919231819.png)


![](assets/Pasted%20image%2020250919232030.png)

### Should We Transcode Every Video?

No. Similar to on-demand image optimization, transcode **on demand** - only when a user requests a resolution that doesn't yet exist.

**Exception: live streaming.** Live video is captured in small buffers (~2–10 seconds), transcoded in real time, and served via CDN segments. This is why live streams run approximately 15–30 seconds behind the actual live event.
### CDN Caching Strategy

CDN caching is expensive - don't cache everything. Cache only videos that cross a watch-count or popularity threshold. Long-tail videos (rarely watched) are served directly from origin storage.

### Full Architecture

![](assets/Pasted%20image%2020250919233814.png)

The workflow manager handles retries, fan-out (spawning one transcode job per target resolution), and status tracking. The CDN sits in front of the processed output for popular content.
## Exercises

- Implement your own Bloom filter from scratch (understand the hash function count vs. false positive rate trade-off)
- Trace a full video upload through the pipeline above - what happens at each step?

---

## Further Reading

**LSM Trees & Storage Engines**

- [The Log-Structured Merge-Tree (LSM-Tree)](https://www.cs.umb.edu/~poneil/lsmtree.pdf) - O'Neil et al., the original paper
- [RocksDB internals](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview) - Facebook's production LSM engine; good companion to the theory
- [WiscKey: Separating Keys from Values in SSD-Conscious Storage](https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf) - a modern extension of LSM ideas optimized for SSDs
- _Database Internals_ by Alex Petrov - Ch. 7–9 cover LSM trees, SSTables, and compaction strategies in depth

**Bloom Filters**

- [Bloom Filters by Example](https://llimllib.github.io/bloomfilter-tutorial/) - interactive visual walkthrough
- [Network Applications of Bloom Filters](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=b33b8a1f516ab3bba8ab97de3b3e8498d9b82f65) - Broder & Mitzenmacher; covers variants and false positive rate analysis

**Video Processing**

- [HLS (HTTP Live Streaming) spec](https://developer.apple.com/streaming/) - Apple's ABR streaming protocol; the most widely used
- [MPEG-DASH standard](https://dashif.org/) - the open alternative to HLS
- [How video works](https://howvideo.works) - referenced above; excellent visual primer on containers, codecs, and bitrates
- [FFmpeg documentation](https://ffmpeg.org/documentation.html) - the practical tool for all transcoding work