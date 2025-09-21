# Ad Hoc Systems

## Distributed Task Scheduler
*without retries*

- dkron, AWS Cloudwatch Events
- Schedule a task to be executed
    - at a certain time [fixed]
    - recurring task [cron]
- 30 seconds SLA
    - eg. task scheduled at 10:01 AM should execute before 10:01:30 AM
- Minute Level Granularity

Discuss : store, pick, execute, status (COMPLETED/FAILED/IN-PROGRESS/SCHEDULED)
### Store

Schema for Relational DB

| id (uuid) | command | scheduled_at | status |
| --------- | ------- | ------------ | ------ |
|           |         |              |        |

Above design is not robust, rather have this table and then we can infer *status* from the tables.


| id (uuid) | command | scheduled_at | picked_at | started_at | completed_at | failed_at |
| --------- | ------- | ------------ | --------- | ---------- | ------------ | --------- |
|           |         |              |           |            |              |           |

Store in normal *MYSQL* table, no need of sharding, etc.
Registering a task is as simple as making an entry in tasks table.
 
![](assets/Pasted%20image%2020250920234318.png)
### Pick

![](assets/Pasted%20image%2020250921080825.png)

How will a task puller pull the task & schedule it for execution.

Challenge : how will multiple task puller pull with high throughput ?

Picking a Task

```sql
SELECT * FROM jobs
where scheduled_at < now() + 30 AND picked_at is NULL
ORDER BY scheduled_at ASC LIMIT 10 -- batched pull
FOR UPDATE SKIP LOCKED -- this is important, so multiple puller don't wait
```

![](assets/Pasted%20image%2020250921081157.png)

Worker/Executor are bulky machines which will run the jobs, and *Orchestration* will scale up and scale down number of workers based on load. To adhere to 30seconds SLA, we have to compute time it takes for a task to be picked from DB into the queue and started at executor nodes.

Executors are scaled in proportion of number of tasks in the Broker (SQS/RabbitMQ)
#### Handling Bursts:

- keep an eye on the number of task in DB in coming few minutes and *SCALE UP* and *DOWN* accordingly. *predictive scaling*, as look just at message broker may not give enough time to bring up executors before SLA.
- Orchestrator, read DB, see tasks 10 mins in future and scales up & down.

![](assets/Pasted%20image%2020250921081640.png)

Key metrics to monitor

- number of task pulled per minute
- task wait time
- average time to completion
#### Handling recurring tasks

CRON Syntax : `* * * * 5`

tasks

| id  | task | schedule  | scheduled_at |
| --- | ---- | --------- | ------------ |
| 2   | -    | * * * * * | -            |

jobs

| id    | task_id | scheduled_at | picked_at/st_at/failed_at |
| ----- | ------- | ------------ | ------------------------- |
| 20972 | 2       | -            | -                         |
| 20993 | 2       | -            | -                         |

When task is created

- find the next 10 executions and add them to *jobs* when task is picked for execution from *jobs* tasks
- find the next 10 executions and add them to *jobs* table

Example : *Google Calendar Recurring Meetings*

CRON -> ABSOLUTE -> Regular Flow

## Message Brokers on Relational DB

Requirements

- FIFO
- Consumer reads and deletes the message
- High Throughput
- When one consumer reads the message, it should become unavailable for others

Very similar to distributed task scheduler. *Task Puller* part of distributed task scheduler.

messages

| id       | msg | created_at | picked_at | deleted_at | reciept_handle |
| -------- | --- | ---------- | --------- | ---------- | -------------- |
| AUTO_INC |     |            |           |            | uuid1          |

![](assets/Pasted%20image%2020250921083620.png)

Query will something like this for picking up the message from the table.

```sql
-- get
SELECT * FROM messages
WHERE picked_at is NULL
AND deleted_at is NULL
ORDER BY created_at ASC
LIMIT n
FOR UPDATE SKIP LOCKED

-- updating the row
UPDATE messages
SET picked_at = NOW()
reciept_handle = uuid()
WHERE id = ?
```

#### Visibility Timeout

If a message is read but not deleted then after 10 mins it should appear in front of queue.

CRON job that
```sql
UPDATE message
SET picked_at = NULL
WHERE picked_at < now() - 10min;;
AND deleted_at IS NULL
```

## YouTube Views Counter

- views happening on YouTube count them
- You will need to filter out some views as per the rule engine

![](assets/Pasted%20image%2020250921090345.png)

Questions to Ask Here

- why are we re-ingestion it in kafka
- what is the parallelism here
- how are we partitioning ?
- why are we counting in so many machines ?


## Flash Sale
*Fixed Inventory + Contention* 
*NOT Distributed Transactions*

Requirements

- fixed set of items
- people come-in to buy them in short window

Resource : https://www.youtube.com/watch?v=-I4tIudkArY

Flow : Similar to what happens in real world.

Phase 0: Prepare the stock

- As a store owner, you stock the items in store

units

| id  | item_id | picked_at | picked_by | purchased_by |
| --- | ------- | --------- | --------- | ------------ |
| 1   | 720     | NULL      | NULL      | NULL         |
|     |         |           |           |              |

If you are selling 10,000 iphone phones (product_id = 720), have 10,000 entries in your units table.

Phase 1: let them pick it

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
SELECT * from units
WHERE item_id = 720
AND picked_at IS NULL
ORDER BY id
LIMIT 1
FOR UPDATE SKIP LOCKED -- non-squential exclusive & non-blocking

UPDATE units
SET picked_at = NOW()
picked_by = 1023 -- making item unavailable for others
WHERE id = ?
```

Phase 2 : Payment

User continues with the normal flow of payment and confirms the purchase

On successful payment

- mark item set purchased_by = ? & puchased_at = now()
- create order, etc...

On unsuccessful payment

- make item re-available by settings, picked_at = NULL, picked_by = NULL

You cannot have a distributed transaction spanning, add to cart and payment

#### What if no payment after adding to cart

Run a cron job that iterated through *expired* unites and sets picked_at = NULL, picked_by = NULL
```sql
UPDATE units SET picked_at = NULL
picked_by = NULL
where picked_at < NOW() - 12 mins
```

Either you disappoint some of your consumers or you as a company get disappointed with under selling.


Similar Systems

- any ticket booking site
    - BookMyShow
    - IRCTC
    - Hotel Booking

