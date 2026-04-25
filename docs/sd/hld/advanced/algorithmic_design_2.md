# Algorithmic Design

## Geo-Proximity

What made Tinder, Ola, Uber, Swiggy, Zomato, Facebook Nearby Friends, and Pokémon Go possible? **Geo-proximity** — efficiently finding who and what is near a given location.

**Problem statement:** Given a user's location, find all entities (drivers, restaurants, people) within a radius of `k` km.

![](assets/Pasted%20image%2020250921164045.png)

### Why Is Geo-Proximity Hard?

Location data is **two-dimensional** (latitude, longitude). Most data structures and indexing strategies - B-trees, hash maps, sorted lists - work efficiently in one dimension. Naive approaches like scanning all entities and computing distances are O(n) and completely unscalable.

The solution is **divide and conquer**: recursively partition the 2D space into smaller regions and assign identifiers to each region.
### Core Idea : Divide & Conquer

![](assets/Pasted%20image%2020250921175017.png)

Split in half every time & assign left = 0, right = 1, top = 0, bottom = 1

- zoom in ... more bits in the right
- zoom out ... remove bits from the right

Edge case: nearby points may be far apart in GeoHash

### GeoHash

Convert two dimensional (lat, long) into a single dimension point giving you an ability to quickly check *nearby*

![](assets/Pasted%20image%2020250921175424.png)

On one dimension you can very efficiently find out who's near you using Range Queries (efficiently done using Segment Trees)

GeoHash converts a 2D coordinate (lat, long) into a **single 1D string** by recursively bisecting the world map.

**How it works:**

1. Split the world in half horizontally and vertically
2. Assign 0 to the left/bottom half, 1 to the right/top half
3. Recurse into the relevant cell, appending a bit at each step
4. More bits = more zoom = higher precision

```
More bits  → zoom in  → smaller region, higher precision
Fewer bits → zoom out → larger region, lower precision
```

A 32-bit binary string isn't human-readable, so GeoHash encodes the result in **base-32**, producing a short alphanumeric string like `tdrlvu`.

**Key property:** Locations that are geographically close share a common prefix in their GeoHash string.

![](assets/Pasted%20image%2020250921175651.png)

All geo locations can be represented by a base 32 string and closer the points closer the geohash

Check if these two points are closer - *qrzkst* and *qrzksx*

```
qrzkst  ←→  qrzksx   (close — long common prefix)
qrzkst  ←→  w3gvxp   (far — no common prefix)
```

### Querying with GeoHash

Because nearby locations share a common prefix, proximity queries reduce to **prefix matching** - a problem solved efficiently by:

- **SQL `LIKE` queries** (simple, works for moderate scale)
- **Trie** (fast prefix traversal in memory)
- **Native geospatial indexes** (Redis, Elasticsearch, MongoDB - recommended for production)

```sql
-- Find all people in Bengaluru (GeoHash prefix: tdrlv)
SELECT * FROM people
WHERE geohash LIKE 'tdrlv%';
```

Or load all users into a trie: traverse to the node for `tdrlv` and every node in its subtree is a nearby user.

**In practice:** Don't implement GeoHash from scratch. Use geospatial-aware databases:

- **Redis** - `GEOADD`, `GEOSEARCH`
- **Elasticsearch** -  `geo_distance` queries
- **MongoDB** - `$near`, `$geoWithin` operators
- **PostGIS** - geospatial extension for PostgreSQL

> Related: **Zippr** (India) assigned short human-readable codes to addresses - similar concept, not GeoHash. **Google Plus Codes** (what Google Maps calls "landmarks") use a similar 8-character open location code.

> Related algorithm: **Isolation Forest** for anomaly detection uses a near-identical divide-and-conquer space partitioning strategy.

Alex Xu  ~ Video on Proximity Service

![](assets/Pasted%20image%2020250921171340.png)

### Gojek's Geo-Proximity Architecture at Scale

**Design priorities:** Availability and low latency over strong consistency - a driver's location being 1–2 seconds stale is acceptable; a request timing out is not.

**Storage and querying: Redis**

- In-memory → fast reads and writes
- Native geo-query support (`GEOSEARCH`)
- Multi-master, multi-replica cluster

Data is sharded across masters. Each master owns an exclusive region of the key space and has a set of read replicas.


![](assets/Pasted%20image%2020250921172632.png)


**Challenge: `EVAL` on replicas**

Driver filtering (applying business constraints like vehicle type, rating, availability) is done via Redis `EVAL` (Lua scripting). Redis does not execute `EVAL` on replicas because Lua scripts can contain write commands - running them on a replica would cause inconsistency. When fired on a replica, Redis responds with `MOVED <master_ip>`, redirecting to the master.

![](assets/Pasted%20image%2020250921172452.png)

**Gojek's solution:** They needed `EVAL` on replicas for read-only filtering. They raised this with the Redis team and proposed the `EVAL_RO` command - a read-only variant of `EVAL` that is safe to execute on replicas. This was upstreamed into Redis and the `go-redis` client library was updated accordingly.

**Availability through query fan-out**

Instead of a single `GEOSEARCH` on one node, Gojek splits the search region into smaller sub-regions and fires parallel queries across multiple nodes simultaneously.

Benefits:

- If one node is slow, others still respond - no single node is a bottleneck
- Parallel execution reduces overall latency
- Partial results are returned if the SLA deadline is reached before all nodes respond

![](assets/Pasted%20image%2020250921173336.png)

**Hot shard problem**

Dense urban areas (e.g., central Bengaluru) generate far more reads and writes than rural areas. If sharding is purely by geographic region, some shards become hot.

**Solution:** Manual shard allocation by the ADS (Availability and Distribution Service) - intentionally mixing high-traffic and low-traffic regions onto the same physical shard. Native Redis sharding has no business context; this business-aware allocation is done at the application layer.

**Results at scale:**

- 600,000 writes/minute
- 200,000 reads/minute
- Truly horizontally scalable - add nodes to handle more load

## User Affinity Service (Follow Graph)

On a social network, users follow each other. How do you model and query a follow graph at scale?

**The naive choice:** A graph database (Neo4j, etc.) - seems obvious. Some networks use this (e.g., Koo India).

**Why a graph DB may be overkill here:**

- A follow relationship is just a directed edge - no sophisticated graph traversal algorithms (PageRank, shortest path) are needed
- Graph DBs are operationally complex and expensive
- Cursor-based pagination is painful in graph DBs
- Most follow graph queries are simple lookups, not graph traversals

A **relational database with careful schema design** handles this better.

### Requirements

- Who follows user B? (followers)
- Who does user B follow? (following)
- Does user A follow user B? (existence check - fast)
- Count of followers and following - accurate and fast
- Efficient pagination regardless of how deep the user scrolls
- High write throughput
- Scalable beyond a single DB node

![](assets/Pasted%20image%2020250921181712.png)

### Naive Schema and Its Problems

```
edges(src, dest)

-- followers of B
SELECT * FROM edges WHERE dest = B;

-- following of B
SELECT * FROM edges WHERE src = B;
```

To answer both queries efficiently, you need indexes on both `src` and `dest`. This is expensive to maintain.

**Sharding problem:** If you shard by `src`, then:

- "Who does B follow?" → single shard lookup ✓
- "Who follows B?" → scatter across all shards, then aggregate ✗


Say, we shard and *src* is the partitioning key

Say, we have 4 shards and 4 users A, B, C, D and each user is on one shard.

![](assets/Pasted%20image%2020250921185336.png)

- calculating followers of B is calculated over multiple shard and then aggregated,
- calculating who B follows, is simple and calculated from one shard

We need somehow have both, follow and following on the same shard ! i.e. if we shard by src we want to ensure we have to never query on dest.

You cannot efficiently answer both queries with a single partitioning key unless you restructure the data.

Solution :

For every follow action (A follows B), write **two rows**:

```
(src=A, dest=B, state="follows")
(src=B, dest=A, state="followed_by")
```

For each follow create 2 entries with relation.

![](assets/Pasted%20image%2020250921185705.png)

![](assets/Pasted%20image%2020250921190047.png)

Now **both queries are on `src`** - the partitioning key. No cross-shard queries needed.

```sql
-- Who follows B?
SELECT * FROM edges WHERE src = B AND state = 'followed_by';

-- Who does B follow?
SELECT * FROM edges WHERE src = B AND state = 'follows';

-- Does A follow B?
SELECT 1 FROM edges WHERE src = A AND dest = B AND state = 'follows';
```

All three queries hit a single shard.

### Twitter's FlockDB Schema

This is exactly what Twitter built with **FlockDB** - a graph store on top of a relational DB.

**Schema:**

|column|type|description|
|---|---|---|
|source_id|int64|the node this row belongs to (partition key)|
|dest_id|int64|the other node in the edge|
|position|int64|cursor / sort key (typically a timestamp)|
|state|int8|`follows`, `followed_by`, `archived`, etc.|

**Primary key:** `(source_id, state, position)` - rows are physically stored in this order on disk.

**Unique index:** `(source_id, dest_id, state)` - for fast existence checks.

**Soft deletes:** When an edge is removed, `state` is updated to `archived` rather than deleting the row. This enables undo/restoration of follows.

### Cursor-Based Pagination

Using `LIMIT / OFFSET` for pagination has a well-known problem: as the offset increases, the database must scan and discard all prior rows - performance degrades linearly with page depth.

FlockDB avoids this by paginating on `position` (a timestamp):

Data is partitioned by node so any query would not require cross partition execution

Pagination is done *position* and not Limit/Offset -> any page of result equally fast

for `src = B`

| src | dest | state      | position |
|-----|------|------------|----------|
| B   | C    | Follows    | 100      |
| B   | D    | Follows    | 200      |
| B   | F    | Follows    | 250      |
| B   | A    | Follows    | 500      |
| B   | A    | Followed By| 50       |
| B   | C    | Followed By| 70       |
| B   | D    | Followed By| 102      |
|     |      |            | 200      |
|     |      |            | 300      |

```sql
-- Page 1
SELECT * FROM edges
WHERE src = B AND state = 'follows'
ORDER BY position ASC
LIMIT 20;

-- Page 2 (using last position from page 1 as cursor)
SELECT * FROM edges
WHERE src = B AND state = 'follows'
  AND position > <last_seen_position>
ORDER BY position ASC
LIMIT 20;
```

Because the primary key physically orders rows by `(source_id, state, position)`, every page is a sequential scan from a known position - **O(1) per page regardless of depth**.

**Properties:**

- Range-based partitioning on `source_id` - all edges for a node on one shard
- Horizontally scalable - add shards as user base grows
- Writes are 2× but still fast (two simple inserts)
- Counter queries (`COUNT(*)`) are single-shard scans with a covered index

---
## Exercises

- Implement GeoHash encoding and decoding from scratch - understand how precision changes with string length
- Build a trie-based geo-proximity lookup: insert 1M GeoHash strings, query by prefix
- Implement the dual-write follow graph in Postgres - verify that both follower/following queries hit a single index
- Implement cursor-based pagination on the `position` column and benchmark it against `LIMIT/OFFSET` at depth 10,000

---

## Further Reading

**GeoHash & Spatial Indexing**

- [GeoHash original paper and specification](http://geohash.org/) - Gustavo Niemeyer's original description
- [Google S2 Geometry Library](https://s2geometry.io/) - a more sophisticated alternative to GeoHash using spherical geometry; used by Google Maps, Foursquare, and Yelp
- [Uber H3: A Hexagonal Hierarchical Geospatial Indexing System](https://eng.uber.com/h3/) - Uber's open-source alternative; hexagons minimize edge-case boundary problems
- [Redis Geospatial documentation](https://redis.io/docs/latest/develop/data-types/geospatial/) - practical `GEOADD` / `GEOSEARCH` usage

**Gojek Architecture**

- [How Gojek Handles Millions of Driver Location Updates](https://blog.gojek.io/how-gojek-handles-millions-of-driver-location-updates/) - the source for the EVAL_RO story and fan-out query strategy

**Proximity Service Design**

- [Alex Xu — Proximity Service (System Design Interview Vol. 2)](https://bytebytego.com/courses/system-design-interview/proximity-service) - the canonical system design walkthrough referenced in the original notes

**Follow Graph & FlockDB**

- [FlockDB: Twitter's distributed graph database](https://blog.twitter.com/engineering/en_us/a/2010/introducing-flockdb) - Twitter's original announcement post; short and worth reading
- [Pagination done the right way](https://use-the-index-luke.com/sql/partial-results/fetch-next-page) - Marcus Winand; deep dive into why `LIMIT/OFFSET` is broken and how keyset/cursor pagination works at the DB level
- _Database Internals_ by Alex Petrov - Ch. 2 covers B-tree storage order, which explains why cursor pagination on a primary key is O(1) per page

**Graph Databases (for contrast)**

- [When to use a graph database](https://neo4j.com/developer/graph-database/) - Neo4j's honest take; useful to understand when graph DBs _are_ the right choice (multi-hop traversal, recommendations)
- [TAO: Facebook's Distributed Data Store for the Social Graph](https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf) - how Facebook models its social graph at massive scale without a native graph DB