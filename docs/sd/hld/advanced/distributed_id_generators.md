# Distributed ID generator

## Foundation for ID generation

ID : uniqueness to an object/row/document/event

Problem Statement:
Assign a globally unique ID to *anything*. Write a function that spits out something unique everytime it is invoked !
The function we are writing is part of application logic and *NOT* a central service.

So, what is unique thought time ? *Time* (always moves forward)

```go
func get_id() {
    return get_epoch_ms();
}
```

Everytime the function invoked the time would have moved forward, hence it seems unique, so whats the catch ?
The ID generation logic words fine when there is just *one machine* and the code is *not* invoked *twice within one*.

#### So, what if there are multiple machines ?
Function invoked at the same time on two machines will generate the same ID. *Collision*

We prepend machine id to time ...

```go
func get_id() {
    return concat(machine_id, get_epoch_ms());
}
```

#### What if the program has threads ?
Function can be invoked by two threads at the same time.

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
int counter = 0; // assume static threadsafe atomic cnt++
func get_id() {
    return concat(
        machine_id,
        get_epoch_ms(),
        counter++
    );
}
```

if we already have *static counter*, then time is redundant.
```go
int counter = 0; // assume static threadsafe atomic cnt++
func get_id() {
    return concat(
        machine_id,
        // get_epoch_ms(),
        counter++
    );
}
```

But whats the catch ? This will not work once counter reaches *INT_MAX*, but there is another issue, if machine reboots then counter will reset and start from *zero*.
Static counter is in memory *volatile*

Store counter to disk (*non-volatile*)
Everytime *counter++*, we store it to disk. (Fault Tolerance)

```go
int counter = load(); // assume static threadsafe atomic cnt++


func get_id() {
    counter++;
    save_counter();  // DISK I/O
    return concat(
        machine_id,
        counter++
    );
}
```

This puts pressure on the *disk* because our service is supposed to have high throughput and should be highly available (disk I/O is expensive).
Instead of doing it everytime, lets save counter every *1000* times

```go
int counter = load() + 1000; // flush frequency

func get_id() {
    counter++;
    if(counter % 100 == 0)
        save_counter();  // DISK I/O
    return concat(
        machine_id,
        counter++
    );
}
```

Say, disk flush happens every 3 values, we get repeated ids for the ids which were not saved (in event to *machine crash*)

## Monotonically increasing IDs

#### What if we only want monotonically increasing IDs ?

Why ? *Monotonically increasing IDs helps in conflict resolution*. e.g who came first

Assume `a=10` and lets say there is a thread *T1* (a = 20) and *T2* (a=30). Now how we say which thread came first and updated a variable `a`.

```go
func get_id() {
    return concat(
        get_time_ms(),
        machine_id
    );
}
```

Instead of `machine_time`, we now put `time-machine`, always moves forward

!!! note

    All ID generation algorithms have time on LHS (sortability)

*LHS* : Most significant part, Makes sorting simple, conflict in the first half, then *tie* breaking in the second

![](assets/Pasted%20image%2020250913190513.png)

Although a good solution, but it doesn't guarantee *monotonicity*. Because clocks across machines can go out of sync.
At the same time instant we invoke *get_id* on 4 machines.

```text
# not monotonically increasing
get_id on m2 -> 232
get_id on m4 -> 244
get_id on m7 -> 237
get_id on m9 -> 239
```

*Physical phenomenon* may affect quartz crystal that keeps system time and machines may go out of sync.

Instead of keeping ID generation logic on the application logic, let's create a central ID service. Should solve the clock skew problem.

## Central ID generation service

- Instead of thinking about ID generation, we are talking clock synchronization

![](assets/Pasted%20image%2020250913191903.png)

We run the same *get_id* function in server to generate monotonically increasing IDs.
But, this central ID service is a single point of failure!

ID server could fail, disk of the server could fail.

![](assets/Pasted%20image%2020250913192111.png)

To solve SPOF, we add multiple *ID* servers behind a load balancer
These ID server need to *gossip* to converge upon an agreed value.
We made the entire process super complicated.

One thing we did learn from these evolution is that.

*There is no way to distribute and guarantee strict monotonicity*

So, the solutions we see out there have *relaxed constraints*. (either non-integer, no monotonicity)

#### Central ID Service with Batching : Amazon's Way

![](assets/Pasted%20image%2020250914001056.png)

Anytime a server of a service wants IDs, it makes a call to ID generation service and asks for a batch (500,1000, etc), it re asks when *exhausted*

Simulation

- orders : server 1 : get_id_batch(500)
- orders : server 2 : get_id_batch(1000)
- payments : server 1 : get_id_batch(2000)
- payments : server 2 : get_id_batch(2000)
- orders : server 2 : get_id_batch(500)

NOTE : we are still not guaranteeing monotonicity across servers we are handing out ids in batches.

#### Why are we building ID generation if UUID already exists ?

UUIDs are 128 bit integers and are very inefficient at scale.

- they do not index well
- bloats up the index

4 byte int v/s 16 byte int. Your indexes are 4x larger. You lookups are disk I/O. So DB performance will take a hit.

Although they are random - good for security.

#### MongoDB Object ID

![](assets/Pasted%20image%2020250914002204.png)

96-bits long - 12 bytes - they also do not index well. *NOTE: epoch_sec is on LHS*

## Database Ticket Servers : Flickr

Why flickr needed its own ID generation ?

- database was sharded
- to avoid collision & Guarantee Uniqueness

Why not UUIDs ? Because they index badly

*If you cannot fit the indexes in-memory, you cannot make your DB fast.*

Central Ticket Server : MySQL

 - whoever wants an ID, fires a query to this DB

```mysql
CREATE TABLE `tickets` (
    id bigint unsigned not null auto_increment,
    stub char not null default ``
    PRIMARY KEY (id)
    UNIQUE KEY (stud)
)
```

Idea : Delete and re-insert the row will make DB generate the next id (auto incremented)

Use this ID for your use case.
We can either `DELETE` and then `INSERT` in one transaction, but it is extremely costly on the DB.

Use `UPSERTS (DELETE + INSERT)` in one query.

MySQL provides 2 ways of doing it.

- `INSERT .... ON DUPLICATE KEY UPDATE ....`
    - tries to insert, if it fails due to UNIQUE_KEY then the update clause is executed
- `REPLACE INTO ....` (NOTE: 32x slower than `ON DUPLICATE KEY)
    - tries to insert, if it fails due to UNQIUE KEY then the old row is deleted and the new row is inserted.

Both of these operations are Atomic.
What our query then ?

```mysql
INSERT INTO `tickets` (stub)
    VALUES (`a`)
ON DUPLICATE KEY UPDATE
    id = id + 1
```

![](assets/Pasted%20image%2020250914003728.png)

But this single DB server is single point of failure : How to fix it ?

Have two ticket servers. But that poses a problem of *gossip protocol* among both servers.
We can fix this using *Round Robin* between two servers where each generates

- one : odd
- other : even

![](assets/Pasted%20image%2020250914003928.png)

*Ticket Server 1:*
    auto-increment-increment = 2
    auto-increment-offset = 1
*Ticket Server 2*:
    auto-increment-increment = 2
    auto-increment-offset = 2

If one server goes down other continues to works e.g. 2, 4, 6, ...., 200, 202, ...
When the odd comes back up we reset the offset on both DB by `MAX + BUFFER` e.g. 240 and 241

## Snowflake : Twitter

Used for IDs of tweets ~ also adopted at Discord and Instagram
Snowflakes are 64 bits integers

![](assets/Pasted%20image%2020250914005803.png)

NOTE:

- time on the LHS
- tie breaker on the right

Snowflake is not central service, instead it runs in app server as a native function.

![](assets/Pasted%20image%2020250914010344.png)

So this way we can guarantee generation of about 4096 ids per millisecond and on each machine. Which is a huge number, because there is no way a server can handle 4096 or more requests per millisecond.

Snowflakes are *roughly* sortable

- first 41 bits are epoch milliseconds
- with every ms the ID will be moving forward

This gives us an ability to get objects

- before/after a certain time
- before/after a certain ID

Hence, pretty awesome for pagination

Twitter's pagination is not limit/offset based, instead it uses `since_id` to paginated
I read till this tweet, give me next set. This type of pagination is also used by sharded DB like MongoDB and its extremely efficient.

### Snowflake at Discord

Same logic as Twitter, just epoch = 1st second of 2015 (to get a larger range)
### Snowflake at Sony

They call it *Sonyflake* and their Go-based implement is open sources and can be found on github.
Twitter and other products scales because of this decentralised ID generation.

The logic is handled by API servers which is excellent

- No moving part
- No service
- Just a function call [lib]
- No extra load on DB

### Snowflake at Instagram

Instagram does Snowflake in the DB during INSERT

Requirements

- IDs sortable by time (pagination, filter & batch processing)
- ~ 64 bits to be efficient on index
- No new service

Structure

- 41 bits : epoch ms since Jan 1, 2011
- 13 bits : DB shard ID
- 10 bits : per shard sequence number

Instagram has logical shards (partition) (1000s) on Physical DB servers (10/15)

e.g. MySQL server ~ Physical, CREATE DATABASE : logical separation

```mysql
CREATE DATABASE insta5;

CREATE TABLE insta5.photos (
    id bigint not null default insta5.next_id(),
    ....
);

CREATE OR REPLACE FUNCTION
    insta5.next_id(OUT result bigint) AS $$
DECLARE
    epoch bigint := 1314220021721
    seq_id bigint
    now_ms bigint
    shard_id := 5
BEGIN
    SELECT nextval('insta5.table_id_seq')%%1024 AS sequence_id
    now_ms := ....
    result := (now_ms - epoch) << 23;
    result := result | (shard_id << 10);
    result := result | (seq_id);
END
```


Exercises

- read : https://www.newyorker.com/magazine/2018/12/10/the-friendship-that-made-google-huge
- 