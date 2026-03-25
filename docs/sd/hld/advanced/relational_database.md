# Databases

## Relational Databases

Data is organized into *rows* and *columns*, with **relations** between tables being the defining feature. Relational databases are built around ACID guarantees - Atomicity, Consistency, Isolation and Durability.

Users pick the relational database for *relations*.

**Database Indexes** : speed up **reads** at the cost of slower **writes**, since the index structure must be updated on every write.

### Database Locking

#### Pessimistic Locking

The core idea: **acquire the lock before doing any work**, then release it after.

```sql
ACQ_LOCK()
    READ / UPDATE -- operations
REL_LOCK()
```

**Why locks?** To protect data **consistency and integrity** against concurrent updates. Without locks, two transactions can read the same row, both decide to update it, and one update silently overwrites the other (lost update problem).

**Risk:** Transactional Deadlock - two transactions each hold a lock the other needs. The database detects this and kills one of the transactions automatically.

There are two types of locks :

**Shared Lock** : Used for **reads** where you want to prevent concurrent modification.

- Other transactions **can read** the locked rows
- Other transactions **cannot modify** the locked rows
- If the current transaction later needs to write, the lock is **upgraded to exclusive**

```sql
SELECT * FROM ... FOR SHARE;
```

**Exclusive Lock** (`FOR UPDATE`) : Used when you **intend to write**.

- reserved for *write* by the current transaction
- other transactions cannot *read* the locked rows
- other transactions cannot *modify* the locked rows

```sql
SELECT * FROM ... FOR UPDATE;
```

####  Modifiers

`SKIP LOCKED` : exclude locked rows from the result set entirely. Useful for job queues and seat-booking systems where you just want _any_ available row, not a specific one

```sql
SELECT * FROM t WHERE id = 2 FOR UPDATE SKIP LOCKED;
```

`NOWAIT` : fail immediately instead of waiting if the row is already locked. Avoids the transaction hanging.

```sql
SELECT * FROM t WHERE id = 2 FOR UPDATE NOWAIT;
-- ERROR 3572: Do not wait for lock
```

## Case Study: Airline Check-in System

- multiple airlines
- every airline has multiple plan (flight)
- each flight has 120 seats
- every flight has multiple trips
- user books a seat in one trip of a flight

**Problem:** 120 passengers on the same flight trying to pick seats simultaneously.

This is the classic **fixed inventory + high contention** problem, seen in systems like IRCTC, BookMyShow, CoWIN, and flash sales.

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
    | 2   | hmk  |
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

**The Contention Problem** : When 120 threads simultaneously query for an available seat:

```sql
SELECT id, name, trip_id, user_id
FROM seats
WHERE trip_id = 1 AND user_id IS NULL
ORDER BY name LIMIT 1
FOR UPDATE;
```

- **Without any lock modifier:** All 120 threads queue up waiting for the first locked row to release. After release, the DB re-evaluates the query for each waiting thread one by one. This serializes the entire check-in process - very slow.
- **With `SKIP LOCKED`:** Each thread skips rows locked by others and grabs the next available seat. All 120 can proceed near-simultaneously. This is the correct approach here.

> If neither modifier is used, behavior falls back to the database's isolation level, which won't give you the semantics you want for this use case.

---

## Case Study: KV Store on a Relational DB

**Requirements:** 

- GET, PUT, DELETE, TTL support.
- Infinitely scalable.

Brainstorm : Storage, optimize storage, insert updates, TTL.

### Storage

MYSQL : start with single node & then scale as the system demands.

**Schema**

```
key | value | ttl (absolute Unix timestamp) | is_deleted
```


Instead of a separate `is_deleted` flag, use `ttl = -1` to signal deletion. This saves a column and simplifies queries.

| key | value | ttl                   |
| --- | ----- | --------------------- |
|     |       | (absolute expiration) |

How to hard delete ? Batch & periodic cleanup

- Run a separate cleanup process to hard delete the soft deleted rows.
- Minimize I/O.

#### PUT(Upsert)

- key exists - update
- key doesn't exist - insert

Avoid a separate GET + INSERT/UPDATE. Use a single atomic upsert:

```mysql
-- MySQL
REPLACE INTO store VALUES (k, v, ttl);

-- PostgreSQL
INSERT INTO store (key, value, ttl) VALUES (k, v, ttl)
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, ttl = EXCLUDED.ttl;
```

For concurrent PUTs on the same key, use `FOR UPDATE NOWAIT` to fail fast instead of queuing:

```sql
SELECT * FROM store WHERE key = k1 FOR UPDATE NOWAIT;
UPDATE store SET value = v2 WHERE key = k1;
```

#### GET

Filter out expired keys at query time:

```sql
SELECT * FROM store WHERE key = k1 AND ttl > UNIX_TIMESTAMP();
```

#### DELETE (Soft)

Mark as deleted by setting `ttl = -1`

```sql
UPDATE store SET ttl = -1 WHERE key = k1 AND ttl > UNIX_TIMESTAMP();
```

### TTL Cleanup Strategies

**Approach 1 : Cron batch delete**

- Simple, but expired keys remain readable between runs unless the GET query filters by TTL (which it does above).

```sql
DELETE FROM store WHERE ttl < UNIX_TIMESTAMP();
```

**Approach 2: Lazy Evaluation (in-mem)**

Hard-delete an expired key when it's fetched. 

What if the key is never fetched ?

Problem: keys never fetched are never cleaned up. Needs a cron as a fallback anyway.

**Approach 3 : Random Sampling(Redis-Style)**

- Not suitable for disk backed DBs
- Randomly sample 20 keys that have a TTL set
- Delete all expired keys in the sample
- If >25% of the sample was expired, repeat immediately

The intuition: if fewer than 25% of a random sample are expired, the overall population likely has fewer than 25% expired keys - good enough. The sample size of 20 comes from the **Central Limit Theorem** ensuring the sample is statistically representative. This is what Redis uses internally.

> This approach is designed for in-memory stores. For disk-backed DBs, a simple scheduled batch delete is more practical.

### High Level Architecture (Scaling)


![](assets/Pasted%20image%2020250910123246.png)

- Start with a single MySQL node
- For read-heavy workloads (e.g., 99:1 read/write), add **read replicas**
- For write scaling, use **sharding** — each node owns an exclusive key range or hash bucket
- Run batch cleanup as a separate background process to minimize I/O impact on the primary


![](assets/Pasted%20image%2020250910123839.png)

## Further Study

- [Why ORMs are bad ideas?](https://www.google.com/search?q=why+ORMs+are+bad+ideas) - start with Matthas Noback's critiques and the "ORM is an anti-pattern" discourse; form your own opinion
- [Central Limit Theorem - why does a sample size of 20 work?](https://en.wikipedia.org/wiki/Central_limit_theorem) - understanding this explains why Redis's random 20-key TTL sampling is statistically sound
- [B+ Tree rebalancing](https://en.wikipedia.org/wiki/B%2B_tree) - understand splits and rotations; critical for reasoning about write amplification in indexes
- [FizzBuzz Enterprise Edition](https://github.com/EnterpriseQualityCoding/FizzBuzzEnterpriseEdition) - a joke, but an instructive one on over-engineering

## More Resources

- [A Critique of ANSI SQL Isolation Levels — Berenson et al. (1995)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) - properly defines isolation anomalies (dirty read, phantom, lost update); the paper that fixed decades of ambiguous SQL spec language
- [DDIA - Chapter 7 (Transactions)](https://dataintensive.net/) - clearest explanation of isolation levels in practice; read alongside the Berenson paper
- [PostgreSQL docs on Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html) - best practical reference for `FOR UPDATE`, `SKIP LOCKED`, `NOWAIT` and their interaction with MVCC
- [Use The Index, Luke](https://use-the-index-luke.com/) - free, deep dive into how B-Tree indexes actually work and why most developers misuse them
- [Uber's migration from PostgreSQL to MySQL](https://www.uber.com/blog/postgres-to-mysql-migration/) - real-world case where B-Tree rebalancing on write-heavy workloads drove the decision
- [Redis source - `expire.c`](https://github.com/redis/redis/blob/unstable/src/expire.c) - see the random sampling TTL strategy implemented directly
