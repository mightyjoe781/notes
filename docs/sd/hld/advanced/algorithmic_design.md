# Algorithmic Design (Part 2)

## Impression Counting

### Point in Polygon : *RayCasting*

Given a point, determine if it lies inside a polygon.

**Algorithm:** Cast a ray from the point in any direction (typically horizontal). Count how many times the ray crosses the polygon's edges. If the count is **odd**, the point is inside. If **even**, it's outside.

Read Advanced Algorithms/DSA unit for further description.

![](assets/Pasted%20image%2020250921110719.png)

**Use cases:**

- Location-based reminders (geofences)
- Ride-hailing airport zone detection
- Navigation - detecting when a user enters a region
- Pokémon Go - spawn zones, gym boundaries

## Impression Counting

Impression counting is one of the most widely applicable problems in large-scale systems:

- LinkedIn - post view counts
- YouTube - video view counts
- Google Search - impressions per search result
- Reddit - post view counts
- Google AdSense - ad impression counts
- Instagram - photo view counts

**The core problem:** Not every viewer interacts (likes, comments, clicks). Impressions measure raw engagement breadth — the total reach of a piece of content or ad.

AdTech firms need to render campaign performance graphs showing **total unique visitors in the last N time units**, where N is provided at query time.

---
### Requirements

- Real-time or near-real-time counting
- Each user counted at most once per time window (distinct count)
- No need for exact counts — a close approximation is acceptable
- Same rule engine as the view pipeline for filtering invalid events (bots, self-views, etc.)

### The Problem with Naive Counting



![](assets/Pasted%20image%2020250921115339.png)

**Naive approach:** Store a hash set of `user_id`s per time bucket.

```
2022-04-01_12:00 → {a, b, c, d, e, f}
2022-04-01_13:00 → {a, c, d, w, x}
2022-04-01_14:00 → {c, d, e, f}
```

To count unique visitors across a range, you take the **union** of the sets (not the sum — summing would double-count users appearing in multiple buckets).

```
unique(12:00–14:00) = union({a,b,c,d,e,f}, {a,c,d,w,x}, {c,d,e,f}) = 10
```

**Why this doesn't scale:**

- `user_id` is 4 bytes (int)
- 1M users view an ad per minute → 4 MB per bucket
- 1 hour of data for 1 ad → 60 × 4 MB = **240 MB**
- 5,000 ad campaigns → 5,000 × 240 MB = **~1.2 TB just for 1 hour of data**

Set union is also CPU-intensive at this scale. This approach works at small scale but is unsustainable for AdTech or large platforms.

### Cardinality Estimation - HyperLogLog

This is a **cardinality estimation problem**: efficiently approximate the number of distinct elements in the union of N sets.

**HyperLogLog (HLL)** - based on the Flajolet-Martin algorithm - is the standard solution.

**Memory savings:** 4 MB set → ~12 KB HLL. That's roughly **0.003%** of the original size, with a typical error rate of ~0.81%.

**Redis HLL operations (all O(1) except merge):**

```
PFADD   key element   → add an element to an HLL
PFCOUNT key           → get the estimated distinct count
PFMERGE dest src1 src2 ... → merge N HLLs into one (O(N))
```

HLL is **write-only** (like a Bloom filter) - you cannot remove elements. It is lossy by design.

**Example query - unique visitors from 12:00 to 14:00:**

```
PFMERGE temp_hll hll:ad1:2022-04-01_12 hll:ad1:2022-04-01_13 hll:ad1:2022-04-01_14
PFCOUNT temp_hll  → returns approximate unique count
```

Union is now a single `PFMERGE` command rather than a full set union computation.
### Architecture

**Ingestion pipeline:**

Input : Kafka with view events of a user

If user made `n` views in 1 min window, count as 1

![](assets/Pasted%20image%2020250921124951.png)

**Key filtering rules:**

- Ignore views on a user's own content
- Minimum watch time threshold (e.g., 5 seconds for an ad, longer for video)
- More than N views by the same user in 1 minute → count as 1 (or 0)

![](assets/Pasted%20image%2020250921125044.png)

Events always move forward in time.
For each event, counting consumers read from kafka and ingest it in corresponding HLL of the post. 

Each post gets one HLL key per minute bucket:

```
Key format:  hll:<post_id>:<YYYYMMDD_HHmm>
Command:     PFADD hll:post_1:20220401_1200 user_123
```

#### Querying

**Query path:**

A separate analytics query layer reads from Redis. Given a time range, it:

1. Identifies all relevant minute-bucket keys
2. Issues `PFMERGE` into a temporary key
3. Issues `PFCOUNT` on the merged key
4. Returns the result (and optionally discards the temp key)

![](assets/Pasted%20image%2020250921125219.png)

### Scaling Beyond Redis

At YouTube/AdSense scale, keeping all HLLs in Redis is too expensive. But events always move forward in time - old buckets are immutable.

- we cannot keep entire data in Redis
- Only Redis know HLLs

Keep last 30min/1hour data in Redis (events always move forward)

Keep older data in cheap KV storage (Data is anyways immutable)

![](assets/Pasted%20image%2020250921125652.png)

**Flow:**

1. Counting consumers always write to Redis
2. A background job periodically (e.g., every 10 seconds) copies HLL snapshots to DynamoDB
3. If a key is requested but absent from Redis, it is fetched from DynamoDB and loaded back into Redis
4. For analytics queries spanning old data, all relevant HLLs are loaded into Redis, merged, and counted
## Remote File Sync

Say, you are building Dropbox

![](assets/Pasted%20image%2020250921135811.png)

**Core challenges:**

1. How to upload and download files efficiently and resumably
2. How clients discover and sync changes made on other devices

Challenge 1 : how to build resumable upload & downloads ?
Challenge 2 : how will clients know about new changes ?

![](assets/Pasted%20image%2020250921141144.png)

Chunking a file makes it better for parallel upload and resumable

File is broken into chunks of 4MB and each chunk is called as *block*
Each block is then passed through a Hash Function spitting out a *hash* (identifier)

File representation : A file is represented as a series of hash called as Blocklist.
`video.avi -> [h1, h2, h3, h4]`

Blocks are stored on Blob Storage (S3) with identifier hash
e.g. `s3://my-dropbox/<acc_id>/<block_hash>`

### Data Model

**Blocks DB**

|account_id|block_hash|size|
|---|---|---|

Answers: does this block already exist for this account?

This simple table will help us identify if a block exists in an account, if yes we can obtain the content.

How is a file information hold in DB.  File is a list of block hashes.

**File Metadata DB**

|version|namespace (account_id)|relative_path|blocklist|
|---|---|---|---|
|1|my-drive|/video.avi|h1, h2, h3, h4|
|2|my-drive|/video.avi|h1, h2, h3', h4|
|3|my-drive|/photo.jpg|h5, h6|

`version` is a **monotonically increasing integer scoped to a namespace** - it increments on every change across the entire account, not per file.

### Upload Flow

**First upload of `video.avi` with blocklist `[h1, h2, h3, h4]`:**

1. Client sends a **commit intent** to the Metaserver: "I want to commit `/video.avi` with blocks `[h1, h2, h3, h4]`"
2. Metaserver checks the Blocks DB - none of the hashes exist
3. Metaserver responds: "upload these blocks"
4. Client uploads blocks to the Block Server in parallel (e.g., 2 at a time), waits for ACK per block
5. Client re-commits - all blocks now exist
6. Metaserver writes the entry to File Metadata DB → commit succeeds


![](assets/Pasted%20image%2020250921142714.png)

The file is saved implies an entry in file metadata DB.

#### What if a file changed ?

Say, now a few bytes of the file changed so client tries to commit the file and sees the blocks are [`h1, h2, h3', h4]

The file is saved implies an entry in the file metadata DB

| version | namespace | relative_path | blocklist       |
| ------- | --------- | ------------- | --------------- |
| 1       | my-drive  | /video.avi    | h1, h2, h3, h4  |


![](assets/Pasted%20image%2020250921161850.png)


**If a few bytes of the file change (e.g., `h3` becomes `h3'`):**

1. Client computes new blocklist: `[h1, h2, h3', h4]`
2. Client sends commit intent to Metaserver
3. Metaserver checks - `h1`, `h2`, `h4` exist; `h3'` does not
4. Client uploads only `h3'` - the other 12 MB are skipped (delta sync)
5. Client re-commits → new version row written to File Metadata DB

This is the key efficiency win: **only changed blocks are transferred**.

| version | namespace | relative_path | blocklist       |
| ------- | --------- | ------------- | --------------- |
| 1       | my-drive  | /video.avi    | h1, h2, h3, h4  |
| 2       | my-drive  | /video.avi    | h1, h2, h3', h4 |
| 3       | my-drive  | /photo.jpg    | h5, h6          |

#### How client knows what changed

We need a way to *sequentialize* the updates and every client can maintain till which update it has the changes.

- this looks oddly similar to checkpoints in Kafka, Kinesis. Can we get some inspiration ?
- *VersionID*

Version ID ~ Every-time any update happening in a namespace the version ID is incremented.

| version | namespace | relative_path | blocklist       |
| ------- | --------- | ------------- | --------------- |
| 1       | my-drive  | /video.avi    | h1, h2, h3, h4  |
| 2       | my-drive  | /video.avi    | h1, h2, h3', h4 |
| 3       | my-drive  | /photo.jpg    | h5, h6          |
| 4       | my-drive  | /notes.txt    | h7, h8          |
| 5       | my-drive  | /photo.jpg    | h6'             |

Client can now say, I am at version `2`, any new changes ?

Metaserver can then forward all updates to the client post 2.

#### Multi-version

| version | namespace | relative_path | blocklist       |
| ------- | --------- | ------------- | --------------- |
| 1       | my-drive  | /video.avi    | h1, h2, h3, h4  |
| 2       | my-drive  | /video.avi    | h1, h2, h3', h4 |
| 3       | my-drive  | /photo.jpg    | h5, h6          |
| 4       | my-drive  | /notes.txt    | h7, h8          |
| 5       | my-drive  | /photo.jpg    | h6'             |
| 6       | my-drive  | /video.avi    | h1, h2, h3, h4  |
We can very easily re-construct and old version of a file.

h1, h2, h3', h4(v2 of video) ---> h1, h2, h3, h4 (v1 of video)

Since server holds reference to $h_3$ . The file can be reconstructed easily.

Block deletion only happens when **no version of any file in the namespace references that block** - safe garbage collection.

**Similar systems using this pattern:** Google Drive, iCloud Drive, OneDrive, Slack/Teams file sharing, any system requiring "track updates" semantics.

## Exercises

- Implement Ray Casting for point-in-polygon detection
- Implement HyperLogLog from scratch - understand the role of hash function count on false positive rate
- Read about differential synchronisation (the algorithm behind collaborative text editors)
- Implement operational transformations (OT) - the mechanism behind Google Docs concurrent editing
- Read the Netflix A/B testing blog - how they measure experiment impressions at scale

---

## Further Reading

**HyperLogLog & Cardinality Estimation**

- [HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm](http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf) - Flajolet et al., the original paper
- [Redis HyperLogLog documentation](https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/) - practical usage of `PFADD`, `PFCOUNT`, `PFMERGE`
- [Big Data Counting: How to count a billion distinct objects using only 1.5KB of Memory](http://highscalability.com/blog/2012/4/5/big-data-counting-how-to-count-a-billion-distinct-objects-us.html) - approachable explainer with concrete numbers

**Probabilistic Data Structures**

- [Probabilistic Data Structures for Web Analytics and Data Mining](https://highlyscalable.wordpress.com/2012/05/01/probabilistic-structures-web-analytics-data-mining/) - covers HLL, Bloom filters, Count-Min Sketch together
- [Count-Min Sketch](https://florian.github.io/count-min-sketch/) - related to HLL; useful for frequency estimation (top-K views, not just distinct counts)

**Ray Casting & Computational Geometry**

- [PNPOLY — Point Inclusion in Polygon Test](https://wrfranklin.org/Research/Short_Notes/pnpoly.html) - W. Randolph Franklin's canonical implementation and explanation
- [Segment Trees](https://cp-algorithms.com/data_structures/segment_tree.html) - referenced in exercises; essential for range queries on impression data

**Remote File Sync**

- [Dropbox Datastore API design](https://dropbox.tech/infrastructure/building-dropbox) - Dropbox engineering blog on their sync architecture
- [Differential Synchronisation](https://neil.fraser.name/writing/sync/) - Neil Fraser (Google); the algorithm behind efficient text and file sync
- [Operational Transformation](https://en.wikipedia.org/wiki/Operational_transformation) - the concurrency control mechanism behind Google Docs; start here then read the Jupiter paper
- [The Jupiter Collaboration System](https://dl.acm.org/doi/10.1145/215585.215706) - Nichols et al.; the paper that introduced OT as used in collaborative editors

**A/B Testing at Scale**

- [Netflix: Reimagining Experimentation Analysis at Netflix](https://netflixtechblog.com/reimagining-experimentation-analysis-at-netflix-71356393af21) - how Netflix measures impressions and experiment exposure at scale
- [Overlapping Experiment Infrastructure: More, Better, Faster Experimentation](https://research.google/pubs/overlapping-experiment-infrastructure-more-better-faster-experimentation/) - Google's paper on running thousands of simultaneous A/B tests