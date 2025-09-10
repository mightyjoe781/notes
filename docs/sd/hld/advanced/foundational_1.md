# Foundational Topics - I

## Online Offline Indicator

Approaching System Design :

Spiral Building :
Decide the core & build your systems around it. 
Core is use-case specific : Database, Communication.

Incremental Building :
1. start with a Day Zero architecture
2. See how each component would behave
    1. under load
    2. at scale
3. identify the bottleneck
4. re-architect

Points to remember :

- understand the core property ? access pattern
- affinity towards a tech comes second
- build an *intuition* towards building systems

#### Storage :

$$
user(int) \to offline/online (bool)
$$

Access would be based on *Key-Value*

#### Interfacing API :

![](assets/Pasted%20image%2020250909111107.png)

NOTE: we expose a bulk endpoint to reduce multiple network calls.

#### Updating the database

Push based model : Users push their status periodically.
Out API servers cannot *pull* from client because we cannot proactively talk to client. (unless there is a persistent connection)

Every user periodically sends *heartbeat* to the service

`POST   /heartbeat` -> the authenticated user will be marked as alive.

So, when is a user offline ?
    When we did not receive *heartbeat* for long enough time it will mark user offline.

#### Offline
When we do not receive heartbeat long enough (Handled through business logic)

In database store *time received the last heartbeat*


| user_id | last_hb |
| ------- | ------- |
| u1      | 1000    |
| u2      | 1050    |
| u3      | 1060    |

When you receive the heartbeat.

```sql
UPDATE pulse
SET last_hb = now() -- epoch seconds
WHERE user_id = u1
```

User sends heartbeat every 10 seconds.

#### Get status API

`GET   /status/<user_id>`

* if no entry in the database for user : *offline*
* if entry and `entry.last_hb < now() - 30s` : offline ? online

#### Scale Estimation

* user_id : int -> 4B
* last_hb : int -> 4B

Total size = 8Bytes

for 1B users ~ 1 B x 8Bytes ~ 8 GB

Can we do better on storage ?
Requirement : is that we only care whether user is online/offline. We could design if absence means offline ?
Idea : if user not present in the DB, we return offline. So let's expire (TTL) the entries after 30
seconds.
Total entries = Active users = 100k x 8B ~ 800 KB

#### How to auto delete ?

Approach 1 : Write a CRON job that deletes expired entries

 - not a robust solution
 - we need to handle edge case in business logic

Approach 2 : Can we not offload this to our datastore. (Don't reinvent the wheel)

DB with KV + expiration -> *redis, dynamodb*
upon receiving an heartbeat
- update entry in redis/dynamodb with ttl = 30seconds

#### Which one would you pick & why

| Features                                  | Redis | DynamoDB |
| ----------------------------------------- | ----- | -------- |
| Persistence                               |       | ✅        |
| Managed                                   |       | ✅        |
| Vendor Lockin                             | ✅     |          |
| future extensionability                   | ✅     |          |
| time sensitivity (persistent connections) | ✅     |          |
|                                           |       |          |
NOTE: in real world, web-sockets are used in such systems, but this is Day 1, hence we keep things simple.

#### How is our DB doing ?

Heartbeat is sent every 10 seconds, each user sends 6 heartbeats every seconds,
then 1M active users send 6M req/minute

That is 6M DB calls in a minute. Micro Reads/Updates -> hence n/w bottleneck

So this means our must support high throughput, and we should utilise connection pool rather than creating new connections for each request. We should micro-batch this update and send it as a bulk updates.

![](assets/Pasted%20image%2020250909115345.png)

Connection Pool solves the problem too many noisy queries with Database.

## Foundational Topics in System Design

- Database
- Scaling
- Concurrency
- Caching
- Delegation
- Communication

Any and every decision would affect one of these 6 factors.

We design a multi-user blogging platform (medium.com)
- one user multiple blogs
- multiple users

### Database

| users |
| ----- |
| id    |
| name  |
| bio   |

| blogs        |     |
| ------------ | --- |
| id           |     |
| author_id    |     |
| title        |     |
| is_deleted   |     |
| published_at |     |
| body         |     |
#### Importance of `is_deleted` [soft delete]

When user invokes delete blog, instead of DELETE we update the entry.
Key Reasons : *recoverability, archival, audit*
Easy on the database engine. (No tree re-balancing)

#### Column Type

![](assets/Pasted%20image%2020250909125838.png)

#### Storing datetime in DB

datetime as *datetime* : 02-04-2022 T 09:01:362 (serialized format) : convenient sub-optimal, heavy on size and index

datetime as *epoch integer* : 172562347162 (seconds since 1st Jan 1970) : efficient optimal, and light weight

datetime as *custom format* (int) : YYYYMMDD - 20220402

### Caching

- reduce response times by saving any heavy computation : Cache are not only RAM based
- Typical Use : reduce disk I/O or network I/O or compute (CDNs)
- Cache are just glorified Hash Tables with some advanced data structures.

Exercise : 
Find possible places that you can use as cache with an example. central cache (RAM) for application-level cache. (save DB computations)


### Caching at different levels

- Main memory of the API server
    - limited
    - API server cache
    - inconsistency, (local to server)
- DB Views (Materialised)
    - pre-join tables
    - database triggers can refresh materialised views
- Browser Cache (local Storage) / Personalised Recom. (Ranking stored on Browsers)
- CDN (cache response)
- Disk of API Server
- Load Balancer
### Scaling

Ability to handle large number of *concurrent* requests.
Two scaling strategies

- vertical scaling
    - easy to manage
    - risk of downtime
    - make infra bulky (hulk)
- horizontal scaling
    - complex architecture
    - linear amplification
    - fault tolerance
    - network partitioning
    - add more machines (minions)

In general a good scaling strategy is to start with scale vertically, then move towards horizontal scaling.

Horizontal Scaling ~ $\infty$ , but there is a catch !!

You stateful components like DB and cache can handle those many concurrent requests.
Hence whenever you scale, always do it *bottom up* ! 

![](assets/Pasted%20image%2020250909150413.png)

scaling DB

![](assets/Pasted%20image%2020250909150700.png)

### Delegation

*What does not need to be done in realtime should not be done in realtime.* (mantra for performance)

Core idea : *Delegate & Respond*

![](assets/Pasted%20image%2020250909161947.png)

Here in the example, lets say if we want total blogs, we can create a *field*, `total_blogs` in user_schema and update this in db, via workers as it is not required to be processed immediately.
Similar delegation would happen for publish, deletion (`ON_DELETE` events)

#### Brokers

Buffer to keep the tasks and messages.

Two common implementations

- Message Queues : SQS, RabbitMQ
    - consumers are homogenous, and poll the messages from queue, and pull them out of queue
- Message Streams : Kafka, Kinesis
    - heterogenous consumers, and they keep track of messages via checkpointing or until expired, provides error recovery by just replaying old checkpoint.

![](assets/Pasted%20image%2020250909162704.png)

Now with Kafka, previous architecture will become :
![](assets/Pasted%20image%2020250909163125.png)


### Kafka Essentials

Kafka is a message stream that holds the messages. Internally kafka has topics.
Every topic has `n` partitions. Message is sent to a topic and depending on the configured hash key, it is put into a partition.
Within partition, messages are ordered. (no ordering guarantee across partitions)

Limitations of Kafka
- number of consumers = numbers of partitions
- kafka doesn't guarantee 1 consumption, it guarantees at least 1 consumption as consumer resume from last commit point.

### Concurrency

Concurrency -> to get faster execution (*Threads & Multiprocessing*)

Issue with concurrency

- communication between threads
- concurrent use of shared resources (database, in-memory variables)

Handling Concurrency

- Locks (Optimistic & Pessimistic)
- Mutexes and Semaphores
- go lock-free (CRDTs)

Concurrency in our blogging platform : two users clap the same, count should be `+=2`
We protect our data through : *Transactions* or *Atomic Instructions*

### Communication

The usual communication

![](assets/Pasted%20image%2020250909183415.png)


**Short Polling**

![](assets/Pasted%20image%2020250909183520.png)

continuously
- refreshing cricket score
- checking if server ready

disadvantages
- HTTP overhead
- requests & responses


**Long Polling**

![](assets/Pasted%20image%2020250909184007.png)

response only when the ball is bowled
connection re-established, after timeout & retrieved

Short Polling v/s long polling
- short polling *sends response right away*
- long poling sends response only when done
    - connection kept open for entire duration

e.g. EC2 provisioning
- short polling - get status every few seconds
- long polling - get response when server ready

**Web Sockets**

![](assets/Pasted%20image%2020250909184213.png)

its a protocol, wss (not running on top of HTTP)

- server can proactively send data to the client

Advantages:

- realtime data transfer
- low communication overhead

Applications

- realtime communication
- stock market ticker
- live experiences
- multiplayer games

**Server-sent events**

![](assets/Pasted%20image%2020250909184459.png)

Application :

- stock market ticker
- deployment logs streaming

Realtime interactions

- on twitter, like count updates without refresh
- on medium, one article clapped, other readers should see it in realtime
- instagram live interaction