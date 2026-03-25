# Search Engines

## Designing Recent Searches

Your insights team surfaces the following data:

- 50% of users tap the search bar within the first 5 seconds of opening the app
- 30% of all searches happen through recent searches
- Requirement: show each user their 10 most recent searches

**Key design tensions:** bounded vs. unbounded data, write latency vs. throughput, cross-device consistency, and whether stale data is acceptable.

### Storage

We need to store search queries per user. There are no relational requirements - just high-volume, per-user writes and reads.

**Characteristics:**

- Large volume of data
- High write throughput
- All access is per-user (no cross-user queries)

This points to a **partitioned NoSQL database** (e.g., MongoDB, DynamoDB), sharded by `user_id`.

![](assets/Pasted%20image%2020250920154240.png)

#### Schema Decision: One Document per User vs. One Document per Query

**Option 1: One document per user**

```
user_id → [q1, q2, q3, ...]
```

The array grows unboundedly. Updating it on every search requires reading and rewriting the entire document. Gets expensive fast.

**Option 2: One document per query (correct approach)**

```
{ query: "sachin", user_id: u1, timestamp: ..., device: ..., os: ... }
{ query: "sehwag", user_id: u1, timestamp: ..., device: ..., os: ... }
```

Each search event is an independent document. Unbounded data should always be stored this way - individual events, not growing arrays.


![](assets/Pasted%20image%2020250920155116.png)

### Write Path: Sync or Async?

**Decision 1: Sync vs. async write from API to DB**

Search is one of the most heavily hit APIs in any consumer product. The delay between a search query and its persistence should be as close to zero as possible - if a user searches and immediately re-opens recent searches, they expect to see it.

**Decision 2: If async, Kafka or SQS?**

Kafka adds extensibility (other consumers can process the search event - analytics, recommendations, ML features). But it introduces latency between the search and the record appearing in the DB.

**Decision 3: What about the read path?**

A partitioned NoSQL DB can handle writes, but for reads - especially at the moment a user taps the search bar - you need pre-computed, in-memory results. Fetching and sorting the 10 most recent queries from a DB partition on every tap is too slow at scale.

**Resolution:**

Do a **synchronous write to Redis** (pre-computed recent searches) and an **async write to the persistent DB via Kafka** (for durability and extensibility).


```
User searches
      ↓
API → SYNC write to Redis (immediate, fast)
API → Kafka → DB (async, durable, extensible)
```



![](assets/Pasted%20image%2020250920155805.png)

**Benefits of this approach:**

- Reads from Redis are O(1), no disk I/O, no index traversal
- Results are consistent across all devices (Redis is the single source for recent searches)
- Kafka write gives you extensibility - the same event stream can feed analytics, personalization, or abuse detection pipelines
### Cost Optimisation

**Redis only stores the most recent 10 queries per user** - not the full history. Use a Redis sorted set with timestamp as the score, capped at 10 entries. On every new search, add the new entry and trim to 10.

**Archive old data in the persistent DB.** Queries older than 6 months are unlikely to ever be accessed. Move them to cold storage (S3) or delete them entirely.

![](assets/Pasted%20image%2020250920160204.png)

```
Active queries (< 6 months)  → NoSQL DB (partitioned)
Older queries                → Archive (S3) or delete
```

This is a product decision: do old queries surface at all (with higher latency), or never? Either way, the cost savings are significant.

### Pre-warming Redis

Given that 50% of users tap the search bar within 5 seconds of opening the app, recent searches must be in Redis **before the user taps** - not fetched on demand.

If a user's recent searches are missing from Redis (cache eviction, new deployment, etc.) and you fall back to the DB, the latency is unacceptable for this UX pattern.

**Solution: pre-warm on app open.** When a user opens the app (or authenticates), trigger a background job that ensures their recent searches are loaded into Redis. This can be done as part of the session initialization API call.


![](assets/Pasted%20image%2020250920161603.png)


## Designing Cricbuzz's Live Text Commentary

**Requirements:**

- Users see live ball-by-ball text commentary
- Cost-efficient architecture
- Good user experience


![](assets/Pasted%20image%2020250920173853.png)

**Core tension:** Commentary updates happen every 30-60 seconds during play. Keeping a persistent connection open per user (WebSockets) for this update frequency is expensive at scale. Short polling is cheaper and sufficient given the update cadence.

**Key design decisions:**

- **Short polling over WebSockets:** Commentary updates every ~30 seconds. Keeping millions of persistent connections alive for this cadence is wasteful. Short polling every 15–30 seconds is cost-efficient and UX-acceptable.
- **Write directly to Redis:** The latest commentary entry is always served from Redis - no DB read on the hot path.
- **Async write to DB via Kafka:** Durability and historical access without blocking the write path.
- **Retry on the write path:** If the Kafka or DB write fails, retry - commentary must not be lost.
- **Archival:** After the match ends, the commentary is immutable. Move it to cheap storage. Only live and recent matches need to be in the hot path.

![](assets/Pasted%20image%2020250920180509.png)

## Designing a Simple Text-Based Search Engine

### The Problem

**Information retrieval:** Given a search query, find the most _relevant_ documents from a corpus (JSON documents, web pages, text files, etc.).

### Naive Approach - Why It Fails

Scan every document and check if the query string appears in it. This is O(n) per query and relies on substring matching - it doesn't scale and produces poor relevance.

### Inverted Index

The universal solution is an **inverted index** - a map from each word to the list of documents containing it:

```
"sachin"  → [doc_3, doc_7, doc_42]
"cricket" → [doc_1, doc_3, doc_99]
```

At query time, look up the word in the index - O(1) - and retrieve the document list. Multi-word queries are resolved by intersecting the document lists for each term.

Building the index is expensive (done offline or incrementally), but querying is fast.
### Relevance Techniques

Raw term matching gives you recall but not relevance. The following techniques improve result quality:

**Weighted scoring** Assign different weights to matches in different fields. A match in the document title is more significant than a match in a footnote. Compute a composite score and rank results by it.

**Fuzzy search - BK Trees** Handles typos by finding words within a given edit distance of the query term.

```
"lat" → matches "bat", "cat", "hat" (edit distance 1)
```

BK Trees organize a vocabulary by edit distance, making nearest-neighbor lookup efficient.

**Spell correction** Detect likely misspellings and correct before querying the index.

```
"HOUPE" → corrected to "HOUSE" → search proceeds normally
```

**Synonymic expansion** Expand the query to include synonyms before querying the index.

```
"home" → also search for "house", "residence", "dwelling"
```

Documents matching any synonym are returned.

**Phonetic matching - Soundex / Metaphone** Convert words to a phonetic root and index/query by that root. People often remember how a word sounds but not how it's spelled.

```
"Arnold Schwarzenegger" / "Swarzeneger" / "Swarzenger"
→ all map to the same phonetic root → same results
```

Fuzzy search alone fails here because the edit distance between these variants is too large. Phonetic matching is the right tool.

**Query segmentation** Users frequently omit spaces, especially on mobile.

```
"mcdonalds" → "mc donalds" → "McDonald's"
```

A query segmentation step splits run-together tokens before index lookup.

### Putting It Together

A production search engine applies these techniques in a pipeline:

```
Raw query
    ↓
Spell correction
    ↓
Query segmentation
    ↓
Synonymic expansion
    ↓
Inverted index lookup (per token)
    ↓
Phonetic / fuzzy fallback (if low recall)
    ↓
Relevance scoring (weighted fields, TF-IDF, BM25)
    ↓
Ranked results
```

Elasticsearch applies almost exactly this pipeline - understanding these building blocks makes its configuration and query DSL much more intuitive.

---
## Exercises

- Implement an inverted index from scratch: tokenize a set of documents, build the index, support multi-word queries via set intersection
- Implement a BK Tree for fuzzy word lookup - query for all words within edit distance 2 of a given term
- Implement Soundex or Metaphone - run a set of name variants through it and verify they map to the same code
- Design the Redis data structure for recent searches: sorted set with timestamps as scores, capped at 10 - write the `ZADD` + `ZREMRANGEBYRANK` sequence

---
## Further Reading

**Recent Searches & Caching**

- [Redis Sorted Sets documentation](https://redis.io/docs/latest/develop/data-types/sorted-sets/) - the right data structure for recent/top-N queries: O(log n) insert, O(1) range retrieval
- [How Slack handles search at scale](https://slack.engineering/search-at-slack/) - covers indexing, relevance, and personalization in a real product

**Inverted Index & Information Retrieval**

- _Introduction to Information Retrieval_ - Christopher Manning, Prabhakar Raghavan, Hinrich Schütze; freely available online; the canonical textbook referenced in the original notes
- [Lucene's handling of inverted indexes](https://lucene.apache.org/core/9_0_0/core/overview-summary.html) - Lucene is the engine under Elasticsearch; reading its architecture docs is illuminating

**Fuzzy Search & Edit Distance**

- [BK Trees](https://signal-to-noise.xyz/post/bk-tree/) - clear walkthrough of BK Tree construction and nearest-neighbor queries
- [Levenshtein automata](https://julesjacobs.com/2015/06/17/disqus-levenshtein-redis-realtime.html) - a more efficient approach to fuzzy matching at scale than naive BK Trees

**Phonetic Algorithms**

- [Soundex specification](https://www.archives.gov/research/census/soundex.html) - the original NARA definition
- [Metaphone algorithm](https://en.wikipedia.org/wiki/Metaphone) - more accurate than Soundex for modern English; Double Metaphone handles non-English names

**Elasticsearch in Practice**

- [Elasticsearch: The Definitive Guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html) - free online; covers inverted indexes, relevance scoring (TF-IDF, BM25), analyzers, and fuzzy queries end-to-end

**Live Commentary / Short Polling vs. WebSockets**

- [When to use SSE vs. WebSockets vs. polling](https://ably.com/topic/websockets-vs-sse) - Ably's breakdown; useful for understanding the cost/complexity trade-offs that drove the Cricbuzz architecture