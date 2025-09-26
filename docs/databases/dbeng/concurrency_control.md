# Concurrency Control

### Exclusive Lock vs Shared Lock

If you want to obtain exclusive lock, then no one should have shared lock on the same rows, and vice-versa. We can have multiple users having shared locks

- Exclusive Lock ~ no one can acquire the lock
- Shared Lock ~ multiple users can own the lock (long running multiple reads), (write processes will wait till shared lock is expired so they can edit the values).

These locks enforce consistency.

Deadlock ~ when two resource are in contention for a resource and stuck waiting on each other to release locks. Most DBs can detect and fail the transactions.


```postgresql

-- term 1
begin transaction;
insert into test values(21); -- step - 1
insert into test values(20); -- step - 3

-- term 2
begin transaction;
insert into test values(20); -- step - 2
insert into test values(21); -- step - 4

ERROR: deadlock detected ! -- NOTE : term1 will not terminate

```

### Two Phase Locking

two phase : acquire, acquire, ..... release, release, .....
Example : two tickets booking in airplanes.


Double Booking Problem

```postgresql
-- term 1
begin transaction;
select * from seats where id = 13 -- step - 2 -- available
insert into test values(20); -- step - 3
update seats set isbooked = 1, name = 'hmk' where id = 13 -- step - 4 (waits)
commit; -- step - 6 completes, overwrites previous step 5

-- term 2
begin transaction;
select * from seats where id = 13 -- step - 1 -- available
update seats set isbooked = 1, name = 'smk' where id = 13 -- step - 3 (success)
commit; -- step - 5 completes
```

Two Phase Locking solution

```postgresql
-- term 1
begin transaction;
select * from seats where id = 14 -- step - 2 -- available (waits because of exclusive locks)
-- this unblocks and execute showing the seat as booked ! -- step - 5

-- term 2 (obtain exclusive lock)
begin transaction;
select * from seats where id = 14 for update; -- step - 1 -- available (exclusive lock, no one will not see in its select) (acquire phase)
update seats set isbooked = 1, name = 'smk' where id = 14 -- step - 3 (success)
commit; -- step - 4 completes (release phase)
```

~ Online Booking System - [Link](https://www.youtube.com/watch?v=_95dCYv2Xv4)

- important concepts : FOR UPDATE, FOR UPDATE SKIP LOCKED (optimal to allow parallel processing)

### Why should be avoid *OFFSET* in SQL Query for Paginations

Read More Here ~ https://use-the-index-luke.com/sql/partial-results/fetch-next-page

```postgresql
SELECT title FROM news offset 100 limit 10;
```

- offset by design fetches all the rows in the page/pages (heap) (let's say 110) and drop the 100 records to give limit 10
- another problem is duplicate reading problem when new row is inserted, e.g. `select titel from news offset 110 limit 10`

### Connection Pooling

- helps thrashing the database by multiple clients
- makes queries fast by avoiding the connection setup times

Code Example : [Link](https://github.com/hnasr/javascript_playground/tree/master/postgresnode-pool) [Video](https://www.youtube.com/watch?v=GTeCtIoV2Tw)


