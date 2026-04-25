# Distributed ID generator

## Foundation for ID generation

An ID gives a unique identity to any object - a row, document, or event. 

**Problem Statement**: Assign a globally unique ID to *anything*. Write a function that spits out something unique every time it is invoked!

Crucially, this function lives in **application logic**, not a central service.

What's naturally unique over time? _Time itself_ - it always moves forward.

```go
func get_id() int64 {
    return get_epoch_ms()
}
```

Every time the function is invoked the time would have moved forward, hence it seems unique, so what's the catch?

The ID generation logic works fine when there is just *one machine* and the code is *not* invoked *twice within one*.

### Evolution and Building Towards a Solution

#### Problem 1: Multiple Machines

Two machines invoking `get_id()` at the same millisecond produce the same ID. Fix: prepend a machine ID.

```go
func get_id() string {
    return concat(machine_id, get_epoch_ms())
}
```

#### Problem 2: Multiple Threads

Two threads on the same machine can call `get_id()` simultaneously. Fix: add a `thread_id`, or better, a shared atomic counter.

- add `thread_id` as a differentiator
- add counter that resets every few minutes

```go
func get_id() {
    return concat(
        machine_id,
        thread_id,
        get_epoch_ms()
    );
}
```


concatenating static counter
```go
var counter int64 = 0 // atomic, thread-safe

func get_id() string {
    return concat(
        machine_id, 
        get_epoch_ms(), 
        atomic.AddInt64(&counter, 1)
    )
}
```

Once you have a *counter*, time becomes redundant - the counter alone provides ordering within a machine.

```go
var counter int64 = 0 // atomic, thread-safe

func get_id() string {
    return concat(
        machine_id, 
        // get_epoch_ms(), 
        atomic.AddInt64(&counter, 1)
    )
}
```

But what's the catch? This will not work once counter reaches *INT_MAX*, but there is another issue, if machine reboots then counter will reset and start from *zero*.

#### Problem 3: Counter Reset on Reboot

An in-memory counter is **volatile** - it resets to zero on crash or restart, causing ID collisions. 

Fix : Store counter to disk (*non-volatile*). Every time *counter++*, we store it to disk. (Fault Tolerance)

```go
var counter int64 = load() // restore from disk on startup

func get_id() string {
    atomic.AddInt64(&counter, 1)
    save_counter() // disk I/O on every call
    return concat(machine_id, counter)
}
```

#### Problem 4: Disk I/O Pressure

Writing to disk on every ID generation is expensive and kills throughput. 

Fix: flush every N calls. Load the counter at startup pre-incremented by the flush interval to safely skip over any IDs that were generated but not persisted before a crash.

```go
const FLUSH_EVERY = 1000
var counter int64 = load() + FLUSH_EVERY // skip the danger zone

func get_id() string {
    atomic.AddInt64(&counter, 1)
    if counter % FLUSH_EVERY == 0 {
        save_counter() // disk I/O only every 1000 calls
    }
    return concat(machine_id, counter)
}
```

**Tradeoff:** if the machine crashes between flushes, the IDs generated since the last flush will be re-issued after restart. You get fault tolerance _or_ strict uniqueness - not both, without a stronger guarantee.

## Monotonically increasing IDs

#### Why Monotonicity Matters ?

Monotonically increasing IDs give you a *total ordering* of events - essential for conflict resolution ("which write came last?") and time-based pagination.

Assume `a=10` and lets say there is a thread *T1* (a = 20) and *T2* (a=30). Now how we say which thread came first and updated a variable `a`.

```go
func get_id() string {
    return concat(
        get_time_ms(), 
        machine_id // time-first = sortable
    ) 
}
```

The trick: put **time on the left** (most significant bits). If two IDs share the same timestamp, the right-hand bits serve as a tiebreaker.

!!! note

    All ID generation algorithms have time on LHS (sortability)

*LHS* : Most significant part, Makes sorting simple, conflict in the first half, then *tie* breaking in the second

![](assets/Pasted%20image%2020250913190513.png)

Although a good solution, it doesn't guarantee *monotonicity*. Because clocks across machines can go out of sync.

#### The Clock Skew Problem

This approach breaks down across machines. Physical clocks drift - the quartz crystal keeping system time is affected by temperature, load, and hardware variation. 

At the same logical instant:

At the same time instant we invoke *get_id* on 4 machines.

```
get_id on m2 → 232
get_id on m4 → 244   ← ahead
get_id on m7 → 237
get_id on m9 → 239
```

These IDs are not monotonically increasing. NTP can reduce skew but not eliminate it.

**Conclusion:** *There is no way to distribute ID generation and strictly guarantee monotonicity.* Every real-world solution relaxes at least one constraint (strict ordering, integer type, or decentralization).

## Central ID generation Service

![](assets/Pasted%20image%2020250913191903.png)

Move `get_id()` to a single server - clock skew disappears since there's only one clock (on ID Server).

**Problem:** single point of failure. The server fails, your entire system stops generating IDs.

**Attempted fix:** multiple ID servers behind a load balancer. But now they need to coordinate to avoid issuing the same IDs - you've traded one problem for a distributed consensus problem. This gets complicated fast.

![](assets/Pasted%20image%2020250913192111.png)

These ID server need to *gossip* to converge upon an agreed value. We made the entire process super complicated.

One thing we did learn from these evolution is that.

*There is no way to distribute and guarantee strict monotonicity*

So, the solutions we see out there have *relaxed constraints*. (either non-integer, no monotonicity)

### Amazon's Approach: Batching

![](assets/Pasted%20image%2020250914001056.png)

Anytime a server of a service wants IDs, it makes a call to ID generation service and asks for a batch (500,1000, etc), it re-asks when *exhausted*.

Simulation

- orders : server 1 : get_id_batch(500)
- orders : server 2 : get_id_batch(1000)
- payments : server 1 : get_id_batch(2000)
- payments : server 2 : get_id_batch(2000)
- orders : server 2 : get_id_batch(500)

This drastically reduces load on the ID service.

**Tradeoff:** IDs are not globally monotonic - server 1 might issue ID 450 _after_ server 2 has already issued ID 800.

#### Why Not Just Use UUIDs?

UUIDs (128-bit random integers) are globally unique without coordination - but they're expensive at scale:

- **Poor index locality:** random values scatter across B-tree index pages, causing many cache misses
- **Index bloat:** 16 bytes vs. 4 bytes for an int means indexes are 4× larger
- **DB performance degrades** once indexes no longer fit in memory - every lookup becomes a disk I/O

UUIDs are fine for security (unpredictable) and small-scale systems. At FAANG scale, you need something better.

#### MongoDB Object ID

![](assets/Pasted%20image%2020250914002204.png)

**MongoDB ObjectID** (96 bits / 12 bytes) suffers from the same index bloat problem, though it puts epoch seconds on the LHS for rough sortability.
### Flickr's Ticket Servers

Why flickr needed its own ID generation ?

- database was sharded
- to avoid collision & Guarantee Uniqueness

Why not UUIDs ? Because they index badly

*If you cannot fit the indexes in-memory, you cannot make your DB fast.*

**Solution:** a central MySQL "ticket server" using auto-increment.

```mysql
CREATE TABLE tickets (
    id   BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    stub CHAR(1)         NOT NULL DEFAULT '',
    PRIMARY KEY (id),
    UNIQUE KEY (stub)
);
```

Idea : Delete and re-insert the row will make DB generate the next id (auto incremented)

Use this ID for your use case.
We can either `DELETE` and then `INSERT` in one transaction, but it is extremely costly on the DB.

To get an ID, a service does an upsert (`delete` + `insert`) on this table — the auto-increment produces the next unique integer. MySQL offers two upsert mechanisms:

MySQL provides 2 ways of doing it.

- `INSERT ... ON DUPLICATE KEY UPDATE` — tries insert; on unique key conflict, runs the update clause. **Preferred.**
- `REPLACE INTO` — tries insert; on conflict, deletes the old row and inserts new. ~32× slower due to delete overhead.

Both are atomic. The returned `LAST_INSERT_ID()` is your unique ID.

```mysql
INSERT INTO tickets (stub)
VALUES ('a')
ON DUPLICATE KEY UPDATE id = id + 1;
```


![](assets/Pasted%20image%2020250914003728.png)

But this single DB server is single point of failure : How to fix it ?

Have two ticket servers. But that poses a problem of *gossip protocol* among both servers.
We can fix this using *Round Robin* between two servers where each generates

**Fixing the SPOF:** run two ticket servers, one generating odd IDs and one even.


![](assets/Pasted%20image%2020250914003928.png)

*Ticket Server 1:*
    auto-increment-increment = 2
    auto-increment-offset = 1
*Ticket Server 2*:
    auto-increment-increment = 2
    auto-increment-offset = 2

If one server goes down, the other continues (e.g., only even IDs for a while). When the failed server comes back, reset both servers' offsets to `MAX_ISSUED + BUFFER` to avoid re-issuing IDs.

### Snowflake: Twitter (and Beyond)

Used for tweet IDs; also adopted by Discord, Instagram, and Sony. 

**Snowflakes are 64-bit integers** with a defined bit layout:

![](assets/Pasted%20image%2020250914005803.png)

```
[ 1 bit sign | 41 bits epoch ms | 10 bits machine ID | 12 bits sequence ]
```

NOTE:

- time on the LHS
- tie breaker on the right

Snowflake runs **in the application server as a library function** - no network call, no central service, no extra DB load.

No moving parts. No service. Just a function call.

![](assets/Pasted%20image%2020250914010344.png)

So this way we can guarantee generation of about 4096 ids per millisecond and on each machine. Which is a huge number, because there is no way a server can handle 4096 or more requests per millisecond.

IDs are **roughly sortable** by time (first 41 bits increase monotonically per machine), enabling efficient time-based queries and cursor pagination. 

This gives us an ability to get objects

- before/after a certain time
- before/after a certain ID

Hence, pretty awesome for pagination

Twitter uses `since_id` / `max_id` pagination instead of `LIMIT/OFFSET` - this is far more efficient on sharded databases because it avoids full scans.

### Snowflake at Discord

Same structure as Twitter, but epoch = January 1, 2015 — pushed the epoch forward to maximize the 41-bit range into the future.
### Snowflake at Sony (Sonyflake)

Go-based open-source implementation. Uses 39-bit timestamp (10ms resolution instead of 1ms, for a longer range), 8-bit sequence, 16-bit machine ID. 

Available on GitHub: [github.com/sony/sonyflake](https://github.com/sony/sonyflake).

Twitter and other products scale because of this decentralized ID generation.

The logic is handled by API servers which is excellent

- No moving part
- No service
- Just a function call [lib]
- No extra load on DB

### Snowflake at Instagram

Instagram generates IDs **inside the database** at INSERT time using a PostgreSQL stored function - no separate service, no application-layer logic.

Requirements

- IDs sortable by time (pagination, filter & batch processing)
- ~ 64 bits to be efficient on index
- No new service

Structure

- 41 bits : epoch ms since Jan 1, 2011
- 13 bits : DB shard ID
- 10 bits : per shard sequence number

Instagram uses **logical shards** (1,000s) mapped onto fewer physical DB servers (10–15). Each logical shard has its own sequence and its own `next_id()` function:

e.g. MySQL server ~ Physical, CREATE DATABASE : logical separation

```postgresql
CREATE OR REPLACE FUNCTION insta5.next_id(OUT result bigint) AS $$
DECLARE
    epoch    bigint := 1314220021721;
    seq_id   bigint;
    now_ms   bigint;
    shard_id int    := 5;
BEGIN
    SELECT nextval('insta5.table_id_seq') % 1024 INTO seq_id;
    SELECT FLOOR(EXTRACT(EPOCH FROM clock_timestamp()) * 1000) INTO now_ms;
    result := (now_ms - epoch) << 23;
    result := result | (shard_id << 10);
    result := result | seq_id;
END;
$$ LANGUAGE plpgsql;
```

## Summary: Choosing an Approach

| Approach                | Monotonic? | Centralized? | Integer? | Notes                            |
| ----------------------- | ---------- | ------------ | -------- | -------------------------------- |
| UUID                    | No         | No           | No       | Easy, bad for indexes            |
| Counter + machine ID    | Roughly    | No           | Yes      | Volatile without disk flush      |
| Central ID service      | Yes        | Yes          | Yes      | SPOF risk                        |
| Batching (Amazon)       | Roughly    | Yes (light)  | Yes      | Reduces central service load     |
| Ticket servers (Flickr) | Yes        | Yes          | Yes      | MySQL-based, odd/even for HA     |
| Snowflake (Twitter)     | Roughly    | No           | Yes      | Best overall for most systems    |
| DB-embedded (Instagram) | Roughly    | No           | Yes      | Elegant if DB is already sharded |

## Further Reading & Exercises

**Essential Reads**

- [Instagram Engineering: Sharding & IDs at Instagram](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c) - how Instagram generates 64-bit sortable IDs using Postgres schemas, avoiding a central ID service entirely
- [Twitter's Snowflake announcement](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake) - the original announcement; short and worth reading before diving into implementations
- [Flickr's Ticket Servers](https://code.flickr.net/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap/) - MySQL-based centralized ID generation; simpler than Snowflake, instructive on the trade-offs
- [Discord's Snowflake documentation](https://discord.com/developers/docs/reference#snowflakes) - how Discord adapted Snowflake for their epoch, worker IDs, and API sorting guarantees
- [DDIA Chapter 9 — Consistency and Consensus](https://dataintensive.net/) - covers linearizability and ordering guarantees in depth; the theoretical grounding for why ID ordering is harder than it looks

**Go Deeper**

- [Sonyflake on GitHub](https://github.com/sony/sonyflake) - Sony's Snowflake variant; well-structured open-source implementation worth reading for how they handle machine IDs across AWS instances
- [Lamport Clocks](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) and [Vector Clocks](https://en.wikipedia.org/wiki/Vector_clock) - the theoretical foundation for logical time in distributed systems; the next step if you care about ordering without a central clock
- [Hybrid Logical Clocks (HLC)](https://cse.buffalo.edu/tech-reports/2014-04.pdf) - used in CockroachDB; combines physical and logical time for causally consistent IDs
- [TiDB's approach to distributed auto-increment](https://docs.pingcap.com/tidb/stable/auto-increment/) - similar to Amazon batching but with monotonicity guarantees within a session

**Exercises**

- Implement Snowflake ID generation in Go - handle sequence overflow and clock rollback gracefully
- Benchmark UUID vs. int64 Snowflake IDs in PostgreSQL: create two tables with 10M rows and compare index size and range query performance
- [The Friendship That Made Google Huge — The New Yorker](https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge) - about Jeff Dean and Sanjay Ghemawat; gives context for how Google's infrastructure was built