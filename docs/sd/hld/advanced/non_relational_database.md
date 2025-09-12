# Database


## Non-Relational Databases

NOSQL: Data is non-relational structures

*In most cases, NOSQL databases provide scalability and availability by compromising consistency*
Most NOSQL DBs are eventually consistent.

!!! note
    NOSQL DBs scale does not mean SQL does not. (Anything that shards will scale)

### Types of NOSQL databases

#### Document DB

- Mostly JSON based
- Supports Complex Queries
- Partial Updates to documents possible
- closest to relational database
- Examples : *MongoDB*, *ElasticSearch*

#### Key Value Store

- Key-wise access pattern
- Heavily partitioned
- No complex queries supported
- Examples : *Redis*, *DynamoDB*, *Aerospike*

#### Column Oriented Databases

- storage layout is in columnar fashion

Say you have a table with 100 columns and you want to perform analytics.
`SELECT avg(price) WHERE ts='_'`

- all you care is two columns `price` and `ts`
- But a row DB will go row by row reading all columns & discarding 98 of them *inefficient*
- Column oriented databases will read columns that are part of the query and will not even skim others

Hence column oriented DBs are used in massive analytics & data warehouses e.g. Redshift

Foundational Paper on column oriented DB: *C-Store: A column oriented DMBS*

#### Graph Databases

- stores data in nodes and edges
- great for modelling social behaviours, recommendations (collaborative filtering)
- solid use case : Fraud Detection
- e.g. *Neptune*, *Neo4j*, *TigerGraph*, *DGraph*

### Why non-relational DB scale

- There are no relations
- Data can be denormalised
- Data is modelled to be sharded

We can also achieve above properties on SQL databases, So saying SQL doesn't scale is not entirely correct.

So, when to use SQL ?

- ACID
- Relations, Constraints
- Fixed Schema

When to use NoSQL

* No relations
* data can be denormalised
* Data can be sharded

## Designing : Slack's Realtime Communication

Requirements

- Multiple users, Multiple channels
- Users DM on message in channel
- Real-time chat
- Historical messages can be scrolled through

Similar System : Multiplayer games, realtime chat, interactions, realtime polls, creator tools, etc.



Insight 1: DMs are channel with 2 people.
Thus we only need to model *channels* very well.

How to store messages in slack workspace ?
Workspace -> multiple channels -> multiple messages

Schema:

- workspace : (id, name)
- channels : (id, workspace_id, name, channel_type)
- messages : (id, channel_id, message, user_id, ts)
- membership : (channel_id, user_id, checkpoint) ~ this entity allows us to add attributes on users and their interaction with channels.

Because there will be large number of messages, we store it in a sharded DB
Pick any DB that you can shard, ... even SQL Works.

All message of a channel in one DB, scrolling will be simple, no cross shard query.

*Cassandra* is a high ingestion database, but here any simple relational database will do since we have small load.

#### Simple Architecture Diagram

A very basic flow [to start with]

![](assets/Pasted%20image%2020250911110345.png)

`send_message(from_user, to_channel, text)` : REST Call

API server find relevant shard using `channel_id` and store message there. This way we solve sending messages for both DM & channel.

#### 3 Ways to Persist Message

![](assets/Pasted%20image%2020250911110141.png)

Depending upon criticality of persistence  we pick one over other.

- sending messages over API and then storing them into database ensures persistence, (*important for enterprise applications*), but we use *websockets* for receiving messages from edge servers so as to not poll the message.
- NOTE : Let's say if it was whatapp application, we will sends & receive on the Edge Server via websockets only. Or in case zoom where persistence doesn't matter we can just broadcast message and not store it at all.

### Websockets

Every user will have 1 websocket connection open with our backend infrastructure and that will be used for anything and everything *realtime*

Edge Servers : Because websockets are expensive (persist TCP) and have 6 concurrent TCP connection limit. We have to *multiplex* all realtime communication on *ONE WEBSOCKET* connection.

Hence, we need a fleet of servers (Edge Servers) to whom our end users connect  over websocket.

![](assets/Pasted%20image%2020250911110833.png)

Any service chat, notification, etc wants to talk to users in realtime the info will go through these edge servers.

Insight: Messages once sent will always be persisted, there will not be any DB level runtime exception like unique key failed, etc.

![](assets/Pasted%20image%2020250911111759.png)

Any thing related to messaging that is NOT *pushed*
Non-realtime usecases

- Channel Scroll
- DM Scroll
- Unimportant Messages that are loaded when channel is clicked, e.g. muted channels

### Realtime Communication

Every edge server knows which user is connected to it and *how to communicate with it* (Socket IO library manages this)

![](assets/Pasted%20image%2020250911112754.png)

Hence when the message is sent from A to B the edge server will

- persist message in kafka
- Find B in the local pool
- send message to B

![](assets/Pasted%20image%2020250911112819.png)

*But what if message is for a channel with 50 people* ? Since we are bounded by maximum connections in the pool, one strategy could be to just query from *membership* table we created.

*What if some messages are not sent in realtime ?*

We cannot drop the message hence we can use the channel scroll API (REST) to load the messages when channel is clicked. Just for the sake of connection !

*Will there be just one Edge Server ?*
How will we horizontally scale then ?
Core Idea : connect the servers

Say each server can handle 4 users. what if we get 5th user. The 5th user forms a websocket with another server
How will message from A go to B ? (local connection pool)
How will message go from A to E ? Possible only when message reaches Edge Server 2 and we use TCP for that

But we can connect Edge servers to one another over TCP.


![](assets/Pasted%20image%2020250911113421.png)

But if we have 100 edge server will every server to every another server ? It would be a very bad idea to send message thru mesh network of interconnected servers.

Use *Realtime PubSub*

Idea : Every slack channel has a *pubsub* channel (can be optimized). Each edge server subscribes to the *PubSub* channel corresponding to the slack channels that users connected to it are part of.

e.g.
- A is part of slack channel (c1, c2, c3)
- B is part of slack channel (c2, c4, c5)
- C is part of slack channel (c1, c3)

![](assets/Pasted%20image%2020250911114328.png)

Say E joins the system and is part of channel c3. Hence Edge Server 2 will connect to realtime pubsub & Sub(c3)
So users A, C and E are part of channel C3.
When A sends a message on C3

- message is asynchronously persisted in memory store 
- edge server 1 sends the message to user C connected locally
- edge server 1 pushes the message in pubsub (redis) on pubsub channel corresponding to c3
- edge server 2 receives the message because is subscribed to c3
- edge server 2 finds the local user sub(C3) & forwards the message
- thus E receives the message sent from A


![](assets/Pasted%20image%2020250911115437.png)

### Overall Architecture

![](assets/Pasted%20image%2020250911115245.png)

Further Reading

- encryption in chat
- web transport