# Databases

## Relational Databases & Pessimistic locking

### Relational Databases

Data is stored and represented in *rows* and *column*. Key highlight of relational databases are *Relations*.
Users pick the relational database for *relations*.

Relational Database are known for *ACID*.

### Database Indexes

Indexes make reads *faster* and writes *slower*.

### Database Locking :
Pessimistic Locking

Core Idea : You acquire the lock before proceeding.
Typical Flow
```sql
ACQ_LOCK()
    READ UPDATE -- operations
REL_LOCK()
```

Two types of locking strategies

- shared lock
- exclusive lock

**why do we need locks** ?
- to protect the sanity of the data.
- sanity : consistency & integrity

Protecting the data against **concurrent** updates.

Risk : Transactional Deadlock !!
The transaction that detects the deadlock, kills itself.

### Shared Locks

- reserved for read by the current transaction
- other transactions can read the locked rows
- other transactions cannot modify the locked rows
- if the current transaction wants to *modify* then the locks will be upgraded to exclusive lock.

Implementation
```sql
SELECT * FROM ... FOR SHARE;
```

### Exclusive Locks

- reserved for *write* by the current transaction
- other transactions cannot *read* the locked rows
- other transactions cannot *modify* the locked rows

Implementation
```sql
SELECT * FROM ... FOR UPDATE;
```

####  Skip Locked

Remove the locked rows from the result set.

```sql
SELECT * FROM t where id = 2
FOR UPDATE SKIP LOCKED;
```

#### NOWAIT

locking read does not wait for the lock to be acquired. Th fails immediately if row is locked.

```sql
SELECT * FROM t where id = 2
FOR UPDATE NOWAIT;
```

- if the row is locked *kill the txn*
- ERROR 3572: Do Not wait for lock

## Designing: Airline Checkin System

- multiple airlines
- every airline has multiple plan (flight)
- each flight has 120 seats
- every flight has multiple trips
- user books a seat in one trip of a flight

Handle multiple people trying to pick seat on the plane.

#### Schema

<div class="grid cards" markdown >

-    *airlines*

    | id  | name     |
    | --- | -------- |
    | 1   | AIRINDIA |
    | 2   | INDIGO   |
    | 3   | GOAIR    |

-    *flights*
    
    | id  | airline_id | name          |
    | --- | ---------- | ------------- |
    | 1   | 1          | AIRINDIA 101  |
    | 2   | 1          | AIRINDIA 279  |
    | 3   | 1          | INDIGO 6E 101 |
    
-    *trips*

    | id  | flight_id | fly time         |
    | --- | --------- | ---------------- |
    | 1   | 1         | 08/04/2022 10:00 |
    | 2   | 1         | 09/04/2022 10:00 |
    | 3   | 2         | 08/04/2022 9:00  |
    | 4   | 3         | 09/04/2022 12:00 |


-    *users*
    
    | id  | name  |
    | --- | ----- |
    | 1   | smk   |
    | 2   | anup  |
    | 3   | Abhay |
    | 4   | Ram   |
    | 5   | Mohan |

-    *seats*
    
    | id  | name | trip_id | user_id |
    | --- | ---- | ------- | ------- |
    | 1   | 1A   | 1       | 1       |
    | 2   | 1B   | 1       | 3       |
    | 3   | 1C   | 1       | 2       |
    | 4   | 1D   | 1       | 5       |
    | 5   | 1E   | 1       | 4       |


</div>


### High Level Architecture

![](assets/Pasted%20image%2020250910111134.png)

Admin adds new flights, trips, keeps the status updates.

*Locking Demonstration* : how will we handle when all 120 people flying in one flight in the same trip check-in at the same time !

*Similar System* : Fixed Inventory + Contentions (cowin, irctc, bookmyshow, flash sale)

```sql
'SELECT id, name, trip_id, user_id from seats
where trip_id = 1 and user_id IS null
ORDER BY ia LIMIT 1 FOR UPDATE
```

* using `FOR UPDATE`: each thread waits for first thread (which acquired lock on row-1) and as soon as lock is released, database engine will re-evaluate the query for waiting threads then it picks second seat, happens for 120 seats, increasing overall time of queries/
* using `FOR UPDATE SKIP LOCKED` : now each thread will try its best to get a row which is not locked, entire process will work within microseconds.

If above locks are not used, then database isolation levels will be the one processing the query.

## Designing : KV store on relational DB

Requirements

- Infinitely Scalable
- GET/PUT/DEL/TTL

Brainstorm : Storage, optimize storage, insert updates, TTL

### Storage

MYSQL : start with single node & then scale as the system demands

schema : store

| key | value | ttl                   | is_deleted  |
| --- | ----- | --------------------- | ----------- |
|     |       | (absolute expiration) | soft delete |

Saving Storage : mark `ttl` as negative for deletion

| key | value | ttl                   |
| --- | ----- | --------------------- |
|     |       | (absolute expiration) |

How to hard delete ? Batch & periodic cleanup

- Run a separate cleanup process to hard delete the soft deleted rows.
- Minimize I/O

### Insert

- key exists - update
- key doesn't exist - insert

Instead of apply GET & INSERT/UPDATE, use *UPSERTS* (PostgreSQL)
or `REPLACE INTO store values (k, v, ttl)` (MySQL)

Multiple PUT request ? *locks* (protects data integrity), when one is update other waits.

```sql
SELECT * from store FOR UPDATE NOWAIT;
UPDATE store SET value = v2
WHERE key = k1
```


### Implementing TTL

Approach 1 : Batch deletion with CRON Job

- what about expired keys before they are hard deleted, filter out

Approach 2: Lazy Evaluation (in-mem)

Do hard delete when an expired key is fetched,

- what if the key is never fetched ?
- key will never be deleted
- cron to delete expired keys (but with small pauses)

Approach 3 : Random Sampling & Deletion

- Not suitable for disk backed DBs
- Randomly sample 20 keys having expiration set
- delete all keys that are expired from the sample
- if delete key > 25%, repeat the process

!!! note "idea"

    If sample has `<25%` of expired keys, population will have `<25% of expired keys>`

This approach is used by Redis & the number (sample size) 20 comes from the *Central Limit Theorem*

### Implementing DELETE

```sql
UPDATE store SET ttl = -1
WHERE key = k1 AND ttl > now();
```

### Implementing DELETE for Batch Cleanup

```sql
DELETE FROM store WHERE ttl < now();
```

### Implementing GET

```sql
SELECT * FROM store
WHERE key = k1 AND ttl > now();
```

### High Level Architecture


![](assets/Pasted%20image%2020250910123246.png)

We add as many KV API servers to support the load. (Assuming MySQL is able to handle the load)

If we have a *99:1* read requests and one DB is not able to handle the load, we can add read replicas & a batch cleanup process.

We can have sharding where each node owns an exclusive fragment of the data.


![](assets/Pasted%20image%2020250910123839.png)


Further Study

- Why ORMs are bad ideas
- Central Limit Theorem
- B+ Tree Rebalancing
- FizzBuzz Test Enterprise Edition
