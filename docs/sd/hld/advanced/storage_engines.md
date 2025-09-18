# Storage Engines



## Designing a Distributed Cache

Requirements

- Hight Throughput, low latency, distributed
- GET, PUT, DEL, TTL
- Scale is default

#### Single Node Cache

![](assets/Pasted%20image%2020250915194835.png)

Bare minimum functionalities : *GET/PUT/DEL*

You can always extend the functionalities to support complex data structures like sets, lists, etc.

key -> object

```go
object struct {
    type list
    data ...
}
```

Each key has an associates type which determines the functionalities supported.

The objects are store in a Hash Table.
```json
{
    key1 -> object(type, list)
    key2 -> object(type, set)
}
```

![](assets/Pasted%20image%2020250915195150.png)

Communication: TCP Protocol ---> gRPC

![](assets/Pasted%20image%2020250915195329.png)

Every protocol has its own set of pros and cons. But we can support all 3 ways of communication by abstracting out the implementation.

![](assets/Pasted%20image%2020250915195629.png)

Why should we use gRPC or custom/raw TCP ?

- connection pool
- saving 3-way handshakes upon every request
- performant serialization and deserialization

#### Cache is Full ?

Eviction : Make place for newer entries.

Eviction Algorithms : 

- LRU : least recently used (CDN, Google News)
- LFU : least frequently user (Wikipedia)
- Random Eviction: randomly evict one

Read about implementation of constant time LRU & LFU.

How will you find if the cache is full ?
Cap on the max number of keys in the cache (Hash Table)
Cap on the cumulative size of values inserted

$$
\text{total\_size} = sizeof(obj)
$$

`zmalloc()`

You can trigger cache eviction only when you know the *cache is full*.


#### Handling TTLs

Every key has an associated expiry (absolute time)
Every cache server has a cleanup process running

- free up the expired keys : `free(obj)`
- garbage collector then pick it up

#### How to effectively find the key to be cleaned up ?

Priority Queue

absolute expiration time ->> order of eviction

Advantages : Simple, Consistent
Disadvantages : Need an additional data structure
Sampling : *Lazy Deletion* + Sample 20 keys, free the expired ones,

[Redis] = repeat until the sample < 25% expired.

#### Scaling

scaling a single node cache : vertical

- add more RAM CPU, Network

Core operations

- GET k -> check the hash table & return
- PUT k, v -> add to hash table
- DEL k -> delete from the hash table

#### Concurrency

When two or more update/delete operations on key came to a cache server at the same time

Classical Concurrency Problem

- pessimistic locking
- optimistic locking
- single threaded

**Pessimistic Locking**

```sql
ACQ_LOCK()
    DELETE K
REL_LOCK()
```

so if there are two thread trying to update the same value, we just block the other thread from accessing the memory, using *mutexes and semaphores*.
Atomic variables to keep track of threads.

**Optimistic Locking**

Lets say a = 10. there are two threads trying to update the value to a = 20, a = 30 respectively.

```txt
// only one would succeed
update a = 20 where a = 10
update a = 30 where a = 10
```

- Idea : Make updates conditional
- Implementation : compare and swap (standard instruction in most of languages)
Fun exercise : How would you use MySQL as a cache server ?
Same throughput as any other cache !

**Single Threaded**

- redis takes this approach, rather than having parallelism

### Making Cache Distributed

why ? one node is not enough to handle the load.

Storage : Have multiple cache stores each storing a range of the key. e.g. C1 (a, j), C2 (k, t), C3(u, z). Range based routing.

There could be 4 scenarios for range based routing

![](assets/Pasted%20image%2020250917000941.png)

### Consistent Hashing : for determining ownership

![](assets/Pasted%20image%2020250916234538.png)

#### Add a new cache server
We create cache 5 using cache 1 and the add it to the ring. *Minimal Data Transfer*

![](assets/Pasted%20image%2020250916234743.png)


NOTE: adding virtual node is a bad idea for stateful applications.
Scaling up and down is now as simple as it requires to read data from diff notes.

Practically : Take snapshot of cache 1 as cache 5, and slowly clean up rows in the cache1

#### Removing a cache server

![](assets/Pasted%20image%2020250916234947.png)

1. Graceful shutdown
2. abrupt outage

Minimal Data Transfer

High Availability

- replicas (state data)
- standby nodes

Reliability

- write ahead logging
### Distributed Hash Table

A distributed cache under the covers is a *DHT* which maps values to key spread across nodes.

DHTs are optimised for *minimal* data movement when nodes are added or removed. DHTs are used is building

- Distributed File Systems
- DNS servers
- Instant Messaging
- Peer-to-Peer Sharing

*BitTorrent* uses DHTs. (IPFS)

![](assets/Pasted%20image%2020250916235611.png)

![](assets/Pasted%20image%2020250917000027.png)

## ETL & Tiered Storage

Say, we are building a multi-user blogging application in which the data is stored in *Transactional Database* like Mongo DB

![](assets/Pasted%20image%2020250915114251.png)

Our application grew big and now the CEO wants detailed reporting and stats and dashboards and for that you have a dedicated Insights Team.
But the insights team only knows SQL.
So, how will they build the dashboards on MongoDB when they only know SQL ?

One way would be to send *events* from API in Kafka then process it into worker and put it into some SQL server.

![](assets/Pasted%20image%2020250915115004.png)

But is this the best way ?

- events have context of the application
- events might not contain all the data
- everything might not have an event
- what if changes done but sending event failed ... ? consistency ?

So many challenges ! can we do better

### Change Data Capture (CDC)

Instead of relying on Events, what if we rely on Source of Truth ? (our database)

![](assets/Pasted%20image%2020250915115340.png)

CDC pulls the changes happening on the database through its `COMMIT_LOG/BIN_LOG` and provides a way to

- optionally transform the data
- put it into a *sink* database

You can also choose to do it manually or your own way just pick appropriate SINK e.g. Kafka, SQS, Broker, and build your own complex transformations.

The core idea is to NOT rely on events and rely on Database.

Say we have *Blogs* table and we insert, update, delete something. we get one CDC event for every change that happened in the database.

CDCs are very heavily used in building *Multi-Tiered Storage*

![](assets/Pasted%20image%2020250915120028.png)

Implement quick CDC using Airbyte (if you have never used it)




Exercise

- setup a CDC pipeline locally
- Read about implementation of constant time LRU & LFU
- implement your own consistent hashing algorithm