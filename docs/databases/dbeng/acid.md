# ACID

### What is a Transaction

Transaction

- A collection of queries
- One unit of Work
- e.g. Account Deposit (SELECT, UPDATE, UPDATE)
- Transactions are wrapped in block of *BEGIN* and *COMMIT*
- Transactions can be roll backed in case of unexpected ending/crash using *ROLLBACK*

Nature of Transactions

- Usually Transactions are used to change and modify data
- However, it is perfectly normal to have a read only transactions
- Example, you want to generate a report and you want to get consistent snapshot based on the time of transaction.
- Example : While transferring money from one account to another, we can't lose money in system. Transaction either always completes or fails as a single unit.

## Atomicity

- All queries in a transaction must succeed.
- If one query fails, all prior successful queries in transaction should rollback.
- If the database went down prior to a commit of a transaction, all the successful queries in the transaction should rollback.
- Lack of atomicity leads to inconsistencies.

## Isolation

 - Can my inflight transaction see changes made by other transactions ?
### Read Phenomena

- Dirty Reads
    - some other transaction is performing some changes (not committed) and you just read that value. 
    - These changes could be rollbacked & you will be reading a wrong value.
- Non-Repeatable read
    - different queries that yield same values, but inconsistent results. some other transaction performing changes and commits. 
    - Further operations on our transaction will cause issues, as our read didn't have committed changes and further instances of the same query will result in the inconsistent results.
- Phantom reads
    - Values you can't read because they don't exist yet, Running range queries yields you some result, but some other transaction adds rows which satisfy your query, so later same query will give different results. 
    - Always happens when using where clause.
- Lost Updates
    - two parallel updates to same rows causes one of them get overwritten. (Row level locks can help here)
### Isolation Levels

- Read Uncommitted : 
    - No Isolation, any change from the outside is visible to the transaction, committed or not. 
    - You can get dirty reads here, 
    - Its quite fast, and only supported by MySQL.
- Read Committed
    - Each query in a transaction only sees committed changes by other transactions. 
    - Default Isolation in many databases.
- Repeatable Read
    - The transaction will make sure that when a query reads a row, that row will remain unchanged while its running.
    - Isolation level that fixes Non-Repeatable read, but doesn't fixes Phantom Read.
- Snapshot
    - Each query in a transaction only sees changes that have been committed up to the start the transaction
    - Its like a snapshot version of the database at that moment.
- Serializable
    - Transactions are run as if they serialized one after the other.
    - No Side Effects

| Isolation level  | Dirty reads | Lost updates | Non-repeatable reads | Phantoms    |
| ---------------- | ----------- | ------------ | -------------------- | ----------- |
| Read Uncommitted | may occur   | may occur    | may occur            | may occur   |
| Read Committed   | don't occur | may occur    | may occur            | may occur   |
| Repeatable Read  | don't occur | don't occur  | don't occur          | may occur   |
| Serializable     | don't occur | don't occur  | don't occur          | don't occur |

- Each DBMS implements Isolation level differently.
- Pessimistic ~ Row level locks, table locks, page locks to avoid lost updates.
- Optimistic ~ No locks, just track if things changed and fail the transaction if so. (Serializable Errors)
- Repeatable read `locks` the rows it reads but it could be expensive if you read a lot of rows, Postgres implements RR as snapshot. That is why you don't get phantom reads with Postgres in repeatable read.
- Serializable are usually implemented with optimistic concurrency control, you can implement it pessimistically with *SELECT FOR UPDATE*

## Consistency

### Consistency in Data

- defined by user
- Referential integrity (using foreign keys)
- atomicity
- isolation

### Consistency in Reads

![](assets/Pasted%20image%2020250924105410.png)

- If a transaction committed a change will a new transaction immediately see the change ? (Difficult in Replicas)
- Affects the system as a whole
- Relational and NoSQL databases suffer from this
- Eventual Consistency (Weak/Strong >?)

## Durability

- Changes made by committed transactions must be persisted in a durable non-volatile storage
- Durability Techniques
    - WAL ~ Write Ahead Log
    - Asynchronous Snapshots (flush memory to disk)
    - AOF ~ Append Only File

### WAL

- Writing a log of data of disk is expensive (indexes, data files, columns, rows, etc)
- That is why DBMSs persist a compressed version of the changes known as WAL (Write Ahead Log)

### OS Cache

- A write request in OS usually goes to the OS cache (OS does batching before writing to disk)
- When the write goes to OS cache, an OS crash, machine restart could lead to loss of data.
- `fsync` OS command forces writes to always go to disk (it will be slow without batching, now you will have to manage it)
- `fsync` can be expensive and slows down commits




Interested Take on ACID (Martin Kleppmann) ~ [Video](https://www.youtube.com/watch?v=5ZjhNTM8XU8)

