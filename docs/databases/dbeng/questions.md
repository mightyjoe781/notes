# Questions


### Heap Index Scan instead of Index only Scan why ?

in Index scan, postgres scans the index and the moment it finds the an entry that matches the where clause it jumps back to the table (heap) to fetch whatever the user asks for (in our case example id was the key indexed and name was on the table) and it is going to do that for every entry it finds in the index.. so you can see that its gonna be random access to the table and index back and forth ... so if we are just selected 1 value that is great..  even if we are selecting multiple rows that happened to be next to each other (1->10 for example) index scan is still great because when we went back to the table to select that row we pulled a whole block which contained multiple rows so chances that the next rows are in the same block are high..However assume we are selecting random values id =1 or id = 8 or id =1000 that is random access and index scan are bad for those because of the jump back and forth of between index and table ..

so postgres solves this problem by saying "hey, there are chances that I am going to select multiple rows from multiple blocks so index scan is gonna destroy the performance  "so let us scan the entire index (or multiple indexes if any) and come up with a list of things that we need to fetch from the table and do a single call to the table instead of multiple ... thats is the power of bitmap ..the bad thing about bitmap is they are not always great if , example is your rows are next to each other and you can quickly get them but jumping immediately to the table (just like index scan) but you had me waiting to scan the entire index instead ... 

### cost unit in postgres plan

Its not time in `ms` but an arbitaray unit decided by database. Source : https://scalegrid.io/blog/postgres-explain-cost/

### Snapshot Isolation Level

- Repeatable Read - For the rows we read, they should not change within the transaction. When we are doing range scan, lets say student between grade 90 -100, 10 students. and some inserts a new row a student with grade 95. Next read will fetch 11 students.
- While above statement in confusing, think of it this way that we acquired lock on 10 student/rows, we did not get any guarantee of adding new rows, phantom rows.
- Phantom Rows are problem in Repeatable Read.

- Snapshot Isolation ~ Read happens in range, and every single row in query is versioned with timestamps. Snapshotting entire Database will not scale. When we read we filter using a time t0, we don't care about later inserts then.

### Why my table is using Sequential Scan rather than index

If tables are small, and all the rows in single page, then postgres will read the entire page(single IO) rather than specific ids (requires index traversal on small table)

### Index on column with duplicate values

https://www.mydbops.com/blog/deduplication-of-b-tree-indexes-in-postgresql-13
Read up more Index Selectivity.

