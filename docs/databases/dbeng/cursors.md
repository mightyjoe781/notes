# Database Cursors

### What are Database Cursors ?

Assume we are running a query like 

```mysql
select * from grades; -- 12 Million records

-- how about we add filters
select * from grades where g between 90 and 100; -- 1 M recrods

```

Sending 1M records to clients is impossible, so cursors are introduced to break 1 single request into multiple calls, iteration over query results.

```postgresql
begin;
declare c cursor for select id from grades where g between 90 and 100; -- doesn't return the result

-- now execute
fetch c; -- rows according to query plan
fetch c; -- rows according to query plan
-- ....

```

- Pros
    - stream the results to clients and can be cancelled by user as well.
    - paging with cursors is also natural
    - pl/sql can be written
- Cons
    - stateful - memory is allocated in DB
    - Cursors can't be shared.
    - long running transactions

### Server Side vs Client Side Database Cursors

- Server Side Cursors
    - results are executed on the server and client fetches it incrementally
- Client Side Cursors
    - results are fetched in one-shot but cursor on client side iterates through the results.

### Inserting Million Rows with Python in Postgres using Client Side Cursor

```python

import psycopyg2

con = psycopyg2.connect(host="smk",
                        database="smk",
                        user="postgres",
                        password = "postgres")

cur = con.cursor()

for i in range(100000):
    cur.execute("insert into employees (id, name) values({i}, test{i}) ")

con.commit()

# close
con.close()
```

### Querying with Client Side Cursor

```python

import psycopyg2

con = psycopyg2.connect(host="smk",
                        database="smk",
                        user="postgres",
                        password = "postgres")

cur = con.cursor() # default client-side cursor ~ fast

cur.execute("select * from employees") # ~ slow

rows = cur.fetchmany(50) # fast

# close
con.close()
```
### Querying with Server Side Cursor

```python

import psycopyg2

con = psycopyg2.connect(host="smk",
                        database="smk",
                        user="postgres",
                        password = "postgres")


cur = con.cursor("c1") # server-side cursor ~ fast

cur.execute("select * from employees") # fast

rows = cur.fetchmany(50) # ~ slower


con.commit()

# close
con.close()
```
### Pros and Cons of Server vs Client Side Cursors

- If using client side cursors, network bandwidth will be consumed.
- If using server side cursors, and lets say client doesn't query all the data related to query, it will take a hit on DB Memory

 
 Exercise
 
 - read about server side cursor types in SQL Server