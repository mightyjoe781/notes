# Database (Part 2)

## Non-Relational Databases (NoSQL)

NOSQL: Data is non-relational structures

NoSQL databases store data in non-relational structures. The core tradeoff: **most NoSQL databases trade consistency for scalability and availability**, making them eventually consistent by default.

> A common misconception: "NoSQL scales, SQL doesn't." This isn't true — anything that shards will scale. The real question is what your data model and access patterns demand.

### Types of NoSQL Databases

#### Document DB

- Store data as JSON-like documents.
- Supports Complex Queries
- Partial Updates to documents possible
- closest to relational database
- Good default choice when your data is hierarchical but you still need query flexibility.
- Examples : *MongoDB*, *ElasticSearch*

#### Key Value Store

- Pure key-based access.
- Heavily partitioned and extremely fast, 
- but no complex query support.
- Use when your access pattern is always "give me X by its key." 
- Examples: _Redis, DynamoDB, Aerospike_

#### Column Oriented Databases

- Data is stored column-by-column on disk rather than row-by-row.
- The payoff is massive for analytics

If you run `SELECT avg(price) WHERE ts = '_'` on a 100-column table, a row-store reads and discards 98 columns per row. A column-store reads only the two columns (`price` and `ts`) it needs.

- This is why column-oriented DBs dominate analytics and data warehouses. Examples: _Redshift, BigQuery, Snowflake, Apache Parquet (storage format)_ 
- Foundational paper: _C-Store: A Column-Oriented DBMS (Stonebraker et al., 2005)_

#### Graph Databases

- Nodes and edges as first-class citizens.
- Shine when relationships between entities are the query
- social graphs, recommendations (collaborative filtering), and especially **fraud detection** where you're looking for suspicious relationship patterns.
- Examples: _Neo4j, Amazon Neptune, TigerGraph, DGraph_

#### Why non-relational DB scale

- There are no relations between tables.
- Data can be denormalised
- Data is modelled to be sharded

We can also achieve above properties on SQL databases, So saying SQL doesn't scale is not entirely correct.

#### When to Use SQL vs NoSQL

| Use SQL when                             | Use NoSQL when                             |
| ---------------------------------------- | ------------------------------------------ |
| You need ACID guarantees                 | You can tolerate eventual consistency      |
| Data has clear relations and constraints | Data is denormalized or document-shaped    |
| Schema is fixed and well-defined         | Schema is flexible or evolving             |
| Complex joins are required               | Access patterns are simple and predictable |

#### Consistency & NoSQL Databases

| Database            | Type                    | Notes                                              |
|---------------------|-------------------------|----------------------------------------------------|
| **Cassandra**       | Column-family store     | Tunable consistency, often configured for eventual consistency |
| **DynamoDB**        | Key-value / Document    | Default eventual consistency for reads, configurable for strong consistency |
| **Riak**           | Key-value store         | Designed for eventual consistency, high availability |
| **Couchbase**      | Document / Key-value    | Defaults to eventual consistency, with options for strong consistency |
| **Apache HBase**    | Column-family store     | Typically eventual consistency, with some options for strong consistency |

## Case Study : Slack's Realtime Communication

**Requirements:** 

- Multi-user, multi-channel messaging. 
- Real-time delivery. 
- Scrollable message history. 
- DMs and group channels.

_Similar systems:_ multiplayer games, live polls, collaborative tools, realtime notifications.

**Key Insight**: DMs are just channels with 2 members
This simplification means you only need to model **channels** well - the rest falls out naturally.

How to store messages in a Slack workspace?
Workspace -> multiple channels -> multiple messages

#### Schema

```
workspaces  : (id, name)
channels    : (id, workspace_id, name, channel_type)
messages    : (id, channel_id, user_id, message, ts)
membership  : (channel_id, user_id, checkpoint)
```

`membership` is worth calling out - the `checkpoint` field lets you track where each user last read in a channel, enabling unread counts and scroll position. This is a clean way to attach per-user state to channel interactions without bloating the messages table.

**Storage:** Messages are sharded by `channel_id`. 

All messages for a channel live on the same shard. 

This means channel scroll is always a single-shard query with no cross-shard joins. Any DB that supports sharding works here, including relational ones. 

_Cassandra_ is often cited for high write ingestion, but for Slack's access patterns a sharded relational DB is perfectly fine.
#### Simple Architecture Diagram

A very basic flow [to start with]

![](assets/Pasted%20image%2020250911110345.png)

`send_message(from_user, to_channel, text)` : REST Call

API server find relevant shard using `channel_id` and store message there. This way we solve sending messages for both DM & channel.

#### 3 Ways to Persist Message

![](assets/Pasted%20image%2020250911110141.png)

Depending upon criticality of persistence  we pick one over other.

1. **Persist-first via API, then push via WebSocket** - strongest durability guarantee. Message is written to DB before delivery. Right choice for enterprise/compliance-heavy products.
2. **Send and receive on edge servers via WebSocket, persist asynchronously** - good balance of speed and durability. WhatsApp-style.
3. **Broadcast only, no persistence** - for ephemeral interactions where history doesn't matter (e.g., Zoom meeting reactions).

### Websockets

Every user will have 1 websocket connection open with our backend infrastructure and that will be used for anything and everything *realtime*

**Why a fleet of edge servers?** WebSocket connections are expensive (they hold open a TCP connection). Browsers also limit concurrent WebSocket connections. You can't have every user connected to a single server. So you run a fleet of **Edge Servers**, each managing a pool of active WebSocket connections via a library like Socket.IO.

Any backend service that wants to reach a user in realtime routes through these edge servers.

![](assets/Pasted%20image%2020250911110833.png)

Any service chat, notification, etc wants to talk to users in realtime the info will go through these edge servers.

Insight: Messages once sent will always be persisted, there will not be any DB level runtime exception like unique key failed, etc.

![](assets/Pasted%20image%2020250911111759.png)

### Realtime Communication

Every edge server knows which user is connected to it and *how to communicate with it* (Socket IO library manages this).

![](assets/Pasted%20image%2020250911112754.png)

Hence when a message is sent from A to B.

**Happy path (A and B on the same edge server):**

1. A sends a message to channel C3
2. Edge server persists the message asynchronously (Kafka to DB)
3. Edge server finds B in its local connection pool
4. Delivers directly

![](assets/Pasted%20image%2020250911112819.png)

*But what if message is for a channel with 50 people* ? Since we are bounded by maximum connections in the pool, one strategy could be to just query from *membership* table we created.

*What if some messages are not sent in realtime ?*

We cannot drop the message hence we can use the channel scroll API (REST) to load the messages when channel is clicked. Just for the sake of connection !

*Will there be just one Edge Server ?*

How will we horizontally scale then ?

Core Idea : Connect the servers in a mesh manner.

Say each server can handle 4 users. what if we get 5th user. The 5th user forms a websocket with another server.

How will message from A go to B ? (local connection pool)

How will message go from A to E ? Possible only when message reaches Edge Server 2 and we use TCP for that.

But we can connect Edge servers to one another over TCP. Yes

![](assets/Pasted%20image%2020250911113421.png)

But if we have 100 edge servers, will every server connect to every other server? It would be a very bad idea to send messages through a mesh network of interconnected servers.

Naively, you could connect every edge server to every other edge server (full mesh). At 100 servers that's ~5000 TCP connections — clearly doesn't scale.

**The right solution: Realtime PubSub**

Each Slack channel maps to a **PubSub channel** (e.g., via Redis Pub/Sub). Each edge server subscribes to the PubSub channels corresponding to the Slack channels that its locally-connected users are part of.

e.g.
- A is part of slack channel (c1, c2, c3)
- B is part of slack channel (c2, c4, c5)
- C is part of slack channel (c1, c3)

![](assets/Pasted%20image%2020250911114328.png)

Say E joins the system and is part of channel c3. Hence Edge Server 2 will connect to realtime pubsub and Sub(c3).

So users A, C and E are part of channel C3.

When A sends a message on C3

- message is asynchronously persisted in memory store 
- edge server 1 sends the message to user C connected locally
- edge server 1 pushes the message in pubsub (redis) on pubsub channel corresponding to c3
- edge server 2 receives the message because is subscribed to c3
- edge server 2 finds the local user sub(C3) & forwards the message
- thus E receives the message sent from A


![](assets/Pasted%20image%2020250911115437.png)

This scales cleanly — adding more edge servers just means more PubSub subscribers, no mesh rewiring.

**What if a user is offline or their message isn't delivered in realtime?** Don't drop it. When they open the channel, the **channel scroll REST API** loads historical messages from the DB. Realtime delivery is best-effort; the DB is the source of truth.
### Overall Architecture

#### Non-Realtime Operations

Not everything needs WebSockets. These go through regular REST APIs backed by the sharded message DB:

- Channel scroll / message history
- DM history
- Loading muted or low-priority channels
- Search

![](assets/Pasted%20image%2020250911115245.png)


## Further Reading

**Foundational Texts**

- [Designing Data-Intensive Applications — Kleppmann](https://dataintensive.net/) - chapters on replication, partitioning, and stream processing are directly relevant

**Messaging & Chat at Scale**

- [Discord: How We Switched from Cassandra to ScyllaDB](https://discord.com/blog/how-discord-stores-trillions-of-messages) - excellent real-world case study on Cassandra data modeling for messaging and why they migrated; covers tombstone accumulation, hot partitions, and latency tail issues
- [Discord: How We Store Billions of Messages](https://discord.com/blog/how-discord-stores-billions-of-messages) - the earlier post; read this first, then the ScyllaDB migration post for the full arc

**Redis**

- [Redis Pub/Sub documentation](https://redis.io/docs/latest/develop/interact/pubsub/) - fire-and-forget fanout; no persistence, no consumer groups, no replay
- [Redis Streams documentation](https://redis.io/docs/latest/develop/data-types/streams/) - persistent, consumer-group-aware, replayable; the right choice when you need delivery guarantees
- [Redis Pub/Sub vs Streams — when to use each](https://redis.io/blog/redis-pub-sub-under-the-hood/) - use Pub/Sub for ephemeral presence signals (typing indicators, online status); use Streams for messages that must not be lost

**WebSockets & Real-Time Transport**

- [RFC 6455 — The WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455) - short and readable as RFCs go; understanding the handshake, framing, and close sequence is worth the hour
- [Socket.IO internals](https://socket.io/docs/v4/how-it-works/) - how it handles transport fallback (WebSocket → HTTP long-poll), reconnection with exponential backoff, and namespace multiplexing over a single connection
- [WebTransport — the successor to WebSockets over HTTP/3](https://developer.chrome.com/docs/capabilities/web-apis/webtransport) - built on QUIC; eliminates head-of-line blocking that plagues WebSockets over TCP; actively being adopted by browsers and CDNs

**Async Persistence**

- [Kafka as a write buffer — the case for async persistence](https://kafka.apache.org/documentation/#introduction) - a message queue between edge servers and the DB decouples write spikes from DB capacity; under load, direct DB writes cause cascading failures whereas Kafka absorbs the burst and lets the DB drain at its own pace

**End-to-End Encryption**

- [The Signal Protocol — technical overview](https://signal.org/docs/) - the Double Ratchet Algorithm and X3DH key agreement; used by WhatsApp, Signal, and Google Messages; the starting point for understanding E2E encryption in messaging
- [WhatsApp Encryption Overview](https://www.whatsapp.com/security/WhatsApp-Security-Whitepaper.pdf) - WhatsApp's whitepaper describing their Signal Protocol implementation; a concrete applied example