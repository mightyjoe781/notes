# Ad Hoc Systems

## Distributed Task Scheduler

**Reference implementations:** Dkron, AWS CloudWatch Events (EventBridge Scheduler)

**Requirements:**

- Schedule a task to run at a fixed time or on a recurring schedule (cron)
- 30-second SLA - a task scheduled at 10:01:00 AM must begin execution by 10:01:30 AM
- Minute-level scheduling granularity

**Core concerns:** store, pick, execute, track status (`SCHEDULED` / `IN_PROGRESS` / `COMPLETED` / `FAILED`)
### Store

**Naive schema:**

| id (uuid) | command | scheduled_at | status |
| --------- | ------- | ------------ | ------ |
|           |         |              |        |

Problem: `status` as a single column requires explicit updates and makes it hard to audit what happened (when was it picked, when did it fail, etc.).

**Better schema - derive status from timestamps:**

| id (uuid) | command | scheduled_at | picked_at | started_at | completed_at | failed_at |
| --------- | ------- | ------------ | --------- | ---------- | ------------ | --------- |
|           |         |              |           |            |              |           |

Status is inferred:

- `picked_at IS NULL` → SCHEDULED
- `picked_at IS NOT NULL AND completed_at IS NULL AND failed_at IS NULL` → IN_PROGRESS
- `completed_at IS NOT NULL` → COMPLETED
- `failed_at IS NOT NULL` → FAILED

A plain MySQL table is sufficient here - no sharding needed. Registering a task is a single `INSERT`.
 
![](assets/Pasted%20image%2020250920234318.png)
### Pick

![](assets/Pasted%20image%2020250921080825.png)

Multiple **task pullers** poll the DB and push tasks into a message broker (SQS, RabbitMQ) for **executor** nodes to process.

**The challenge:** Multiple pullers running concurrently must not pick the same task twice.

```sql
-- Atomically claim a batch of due tasks
SELECT * FROM jobs
WHERE scheduled_at <= NOW() + INTERVAL 30 SECOND
  AND picked_at IS NULL
ORDER BY scheduled_at ASC
LIMIT 10
FOR UPDATE SKIP LOCKED;  -- other pullers skip rows locked by this transaction, no blocking

-- Mark as picked
UPDATE jobs
SET picked_at = NOW()
WHERE id IN (...);
```

![](assets/Pasted%20image%2020250921081157.png)

`FOR UPDATE SKIP LOCKED` is the key - concurrent pullers skip rows already locked by another transaction rather than waiting, giving high-throughput non-blocking pulls.
### Execute

Executor nodes are beefy machines that run the actual job commands. An **orchestrator** scales the executor fleet up and down based on queue depth in the broker.

**Handling bursts - predictive scaling:**

Watching only the broker queue depth doesn't give enough lead time to provision new executors before the SLA window closes. Instead, the orchestrator reads the `jobs` table and looks ahead (e.g., 10 minutes into the future) to anticipate load and scale proactively.

![](assets/Pasted%20image%2020250921081640.png)

### Key Metrics to Monitor

- Tasks pulled per minute
- Task wait time (time between `scheduled_at` and `started_at`)
- Average time to completion
- Broker queue depth
### Handling Recurring Tasks

Recurring tasks use cron syntax (e.g., `* * * * 5`). Separate the concept of a **task definition** from individual **job executions**:

**tasks table** (the recurring definition)

|id|command|cron_schedule|
|---|---|---|
|2|send_report.sh|`0 9 * * 1`|

**jobs table** (concrete scheduled executions)

|id|task_id|scheduled_at|picked_at|completed_at|failed_at|
|---|---|---|---|---|---|
|20972|2|2025-01-06 09:00|...|...||
|20993|2|2025-01-13 09:00|...|...||

**Generation strategy:** When a task is created (or when a job is picked for execution), compute the next N occurrences from the cron expression and pre-insert them into the `jobs` table.

Flow: `CRON expression → next N absolute timestamps → insert into jobs → regular pick/execute flow`

Think of it like Google Calendar recurring meetings - the recurrence rule generates concrete event instances.

## Message Broker on a Relational DB

This is essentially the task puller pattern generalized. Building a simple queue on MySQL is more common than it sounds (and is exactly how Amazon SQS originally worked internally).

**Requirements:**

- FIFO ordering
- High throughput
- When one consumer reads a message, it must be invisible to all other consumers
- If a consumer fails to delete the message, it reappears after a timeout (visibility timeout)

Very similar to distributed task scheduler. *Task Puller* part of distributed task scheduler.

### Schema

**messages table**

|id (AUTO_INC)|body|created_at|picked_at|deleted_at|receipt_handle|
|---|---|---|---|---|---|

`receipt_handle` is a UUID generated at pick time. The consumer must present it to delete the message - this prevents a consumer from accidentally deleting a message it didn't pick.


![](assets/Pasted%20image%2020250921083620.png)

Query will something like this for picking up the message from the table.

```sql
-- Pick messages (non-blocking, concurrent consumers safe)
SELECT * FROM messages
WHERE picked_at IS NULL
  AND deleted_at IS NULL
ORDER BY created_at ASC
LIMIT 10
FOR UPDATE SKIP LOCKED;

-- Mark as picked (make invisible to other consumers)
UPDATE messages
SET picked_at = NOW(),
    receipt_handle = UUID()
WHERE id = ?;

-- Delete after successful processing
UPDATE messages
SET deleted_at = NOW()
WHERE id = ?
  AND receipt_handle = ?;  -- must match to prevent accidental deletes
```

### Visibility Timeout

If a consumer picks a message but crashes before deleting it, the message would be lost forever without a safety net. A periodic background job re-enqueues stuck messages:

```sql
-- Run every minute via cron
UPDATE messages
SET picked_at = NULL,
    receipt_handle = NULL
WHERE picked_at < NOW() - INTERVAL 10 MINUTE
  AND deleted_at IS NULL;
```

After the timeout window, the message becomes visible again and another consumer can pick it up.
## YouTube View Counter

A view event pipeline with a rule engine for filtering invalid views (bots, repeated views, etc.).

![](assets/Pasted%20image%2020250921090345.png)

**Design questions worth thinking through:**

- **Why re-ingest into Kafka after filtering?** Decouples the filter stage from the counting stage - each can scale independently and fail independently
- **What is the parallelism here?** Kafka partitions by video ID - all events for the same video go to the same partition, ensuring counts are aggregated in order per video
- **Why count across many machines?** A single counter would be a bottleneck at YouTube's write volume - partitioning by video ID distributes the counting load
- **How do you handle approximate vs. exact counts?** At scale, exact real-time counts are expensive - systems like this often use approximate counting (HyperLogLog) for display and reconcile exact counts in batch

## Flash Sale

**Problem:** Fixed inventory, high contention, short purchase window.

**Core challenge:** Many users trying to buy the same items simultaneously - requires locking without distributed transactions.

> Good reference: [How Flash Sales Work at Scale](https://www.youtube.com/watch?v=-I4tIudkArY)

### Phase 0: Pre-stock Inventory

Before the sale, insert one row per physical unit into the `units` table:

**units table**

| id  | item_id | picked_at | picked_by | purchased_at | purchased_by |
| --- | ------- | --------- | --------- | ------------ | ------------ |
| 1   | 720     | NULL      | NULL      | NULL         | NULL         |
| 2   | 720     | NULL      | NULL      | NULL         | NULL         |
Selling 10,000 iPhones (item_id = 720) → 10,000 rows. One row = one unit.

### Phase 1: Add to Cart (Pick a Unit)

Users attempt to claim a unit. Exactly N users should succeed where N is inventory count.

- you want to let as many people in as many items you have and they physically pick and add to their cart.
- Fixed inventory, contention -> locking
- users come in
    - they try to grab the items
    - they add to their cart, and only N should succeed.

High Throughput and contention

units

| id  | item_id | picked_at  | picked_by | purchased_by |
| --- | ------- | ---------- | --------- | ------------ |
| 1   | 720     | 03/03/2023 | 1023      | NULL         |
|     |         |            |           |              |

```sql
-- Find and lock one available unit atomically
SELECT id FROM units
WHERE item_id = 720
  AND picked_at IS NULL
ORDER BY id ASC
LIMIT 1
FOR UPDATE SKIP LOCKED;  -- non-blocking, non-sequential exclusive lock

-- Claim it
UPDATE units
SET picked_at = NOW(),
    picked_by = 1023  -- user_id
WHERE id = ?;
```

`FOR UPDATE SKIP LOCKED` ensures concurrent users each get a distinct unit without contention - no queueing on locked rows.

### Phase 2: Payment

The user proceeds through checkout normally.

**On successful payment:**

```sql
UPDATE units
SET purchased_at = NOW(), purchased_by = ?
WHERE id = ?;
-- then create order record, etc.
```

**On payment failure or abandonment:**

```sql
UPDATE units
SET picked_at = NULL, picked_by = NULL
WHERE id = ?;
```

You cannot span a distributed transaction across "add to cart" and "payment" - they are separate systems. The picked/purchased split handles this gracefully.

### Handling Cart Abandonment

A background cron job reclaims units that were picked but never paid for:

```sql
UPDATE units
SET picked_at = NULL,
    picked_by = NULL
WHERE picked_at < NOW() - INTERVAL 12 MINUTE
  AND purchased_at IS NULL;
```

**The trade-off:** Too short a timeout → users lose items mid-checkout. Too long → inventory appears sold out when it isn't. Pick a window that matches your expected checkout duration.

Either you occasionally disappoint users (item reclaimed before they pay) or the business under-sells (items held by abandonments). Most systems accept the former.

---

### Similar Systems

This exact pattern applies to:

- Ticket booking (BookMyShow, IRCTC) - seats are units
- Hotel booking - room-nights are units
- Airline seat selection - seats are units

The schema and locking strategy are nearly identical in all cases.

---
## Exercises

- Implement the task scheduler end-to-end locally: MySQL + a task puller in Go/Python + a worker that executes shell commands
- Add retry logic to the scheduler - how do you distinguish a failed task from one still in progress?
- Implement the message broker on MySQL from scratch - test visibility timeout behavior by killing a consumer mid-processing
- Benchmark `FOR UPDATE SKIP LOCKED` vs `FOR UPDATE` under concurrent load - measure throughput difference at 10, 50, 100 concurrent pullers
- Simulate a flash sale locally: pre-stock 100 units, fire 1000 concurrent requests, verify exactly 100 succeed with no overselling

## Further Reading

**Task Scheduling**

- [Dkron documentation](https://dkron.io/docs/basics/getting-started/) - open-source distributed job scheduler; read the architecture section to see how they handle leader election and fault tolerance
- [AWS EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html) - managed alternative; useful to understand what problems a production scheduler actually solves
- [Sidekiq Pro - job scheduling internals](https://github.com/mperham/sidekiq/wiki/Scheduled-Jobs) - Ruby-based but the polling and retry design maps directly to what we built

**Locking & Concurrency**

- [PostgreSQL docs - FOR UPDATE SKIP LOCKED](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE) - authoritative reference; covers interaction with MVCC and subtleties around visibility
- [SELECT FOR UPDATE and SKIP LOCKED - Use The Index, Luke](https://use-the-index-luke.com/sql/row-locks) - explains the index implications of row-level locking that most developers miss

**Message Queues on Relational DBs**

- [Transactional outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html) - the production-grade evolution of the MySQL queue pattern; solves the dual-write problem between DB and broker
- [PGMQ - Postgres Message Queue](https://github.com/tembo-io/pgmq) - a well-implemented open-source message queue on Postgres; read the source to see how visibility timeout and receipt handles are implemented in practice

**Flash Sales & Inventory Locking**

- [How Shopify handles flash sales](https://shopify.engineering/surviving-flashes-of-high-write-traffic-using-queues-inspired-by-cache-theory) - real-world inventory contention at scale; covers queue-based approaches as an alternative to DB locking
- [IRCTC architecture](https://www.youtube.com/watch?v=4-A5lPq2jMk) - one of the most extreme flash-sale-like systems in the world; 1.4 billion users competing for train tickets

**View Counting**

- [Counting at Scale - Stripe Engineering](https://stripe.com/blog/counting-with-prometheus) - batching, approximate vs exact counts, when each is appropriate
- [Lambda Architecture](https://en.wikipedia.org/wiki/Lambda_architecture) - the batch/stream hybrid pattern behind reconciling approximate real-time counts with exact batch counts