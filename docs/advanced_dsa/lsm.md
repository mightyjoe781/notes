# LSM Trees
*Write-optimized Storage Engines*

## Superfast DB KV (Bitcask)

Requirements : superfast reads, writes, deletes, persistence

SSD are more closer to memory rather than magnetic disks, both in terms of cost and speed.
Each hard disk has sector and data is read based on offsets across sectors.

![](assets/Pasted%20image%2020250917230428.png)

Log - Structured Storage

Data stored files

- append-only
- sequential writes
- no random updates

No disk seeks during writes

What we get ? High write throughput (even on HDD)
The SSD doesn't give similar gain


**Simple Design** : Single files of KV pairs

![](assets/Pasted%20image%2020250917231928.png)

PUT (k, v) -> append to this file (lighting fast operations)

DEL (k) -> delete operation is also a *PUT* with special value (-1) (representational)
DEL(k) = PUT(K, -1)

#### How one entry in file looks like ?

![](assets/Pasted%20image%2020250917232240.png)

When reading one entry from file, do we know how much to read. We cannot read *until newline*, not optimal
*Because key and value are of variable length*

![](assets/Pasted%20image%2020250917232248.png)

We read KS2 (4 bytes) VS2(4 bytes) and then read
KS2 bytes for key
VS2 bytes for values

#### Solving Integrity

![](assets/Pasted%20image%2020250917232732.png)

Finding corrupt entries : CRC -> first thing we flush

![](assets/Pasted%20image%2020250917232724.png)

#### Faster GET(k)

To get O(1) GET we use *Index*.
We create an in-memory Hash Table

![](assets/Pasted%20image%2020250917233018.png)

GET(k) -> pointed queries

- Hash Table lookup
- disk seek
- disk read

limitation : index to fit in memory

#### When file grows too big ?

Solution : rotate the file every *t* bytes.
We create new file and old file is made *immutable*


![](assets/Pasted%20image%2020250917233227.png)

#### Changes in our in-memory index

![](assets/Pasted%20image%2020250917233700.png)

We have a lot of files, can we optimize ?

We merge & compact.
All immutable files are merged(stale entries skipped) & compact(deleted entries skipped)

![](assets/Pasted%20image%2020250917233832.png)

Because files are merged offset changes, we have to update index atomically !

Limitations of the DB : Keys must fit in memory
Strength of this DB : O(1) reads, writes, deletes

- High throughput, low latency
- I/O stauration
- Easy Backups

What we just designed is *Bitcask*

![](assets/Pasted%20image%2020250917234340.png)

Most efficient KV database, used by uber in production as backend for Riak, Each node of Riak has an instances of Bitcask running

Riak ~ wrapper on top of Bitcask, helps in distributed features for Bitcask.


Exercise

- implement Riak/Bitcask
- read the paper on bitcask

## LSM Trees

### Attempting to better Bitcask

Bitcask does

- append only files (no disk seek during write)
- in memory index (quick lookup)

Core Idea : Attempt to make writes faster

So can we write directly to RAM ? instead of disk ? that would make writes faster.

Another question is why are we trying to this ? Usually all products eventually start by solving small problem or niche in the already existing sea of solutions and then expand to compete against them. Ex - Duck DB started as a small scale analytics solutions.

Niche where this works in real-time data, which requires a very high write throughputs, e.g. sensors, IOT, clickstream, logging, location updates data, etc.

![](assets/Pasted%20image%2020250919090931.png)

Because we are writing directly to RAM, this gives you higher write throughput ! (but at the cost of Durability)

Excellent for high *ingestion* volumes.

Reads : You need RAM first, If key is present (latest values) return it. Or else fallback to disk for searching the key, but if its not in disk then return NOT Found.

If key is in memory it has to be the most recent value. *Tiered Storage*

#### Periodic Flush

Every `t` minutes in-memory buffer is flushed to the disk at once.
Where should we flush ?

- existing file
    - file too long
    - flush too long
- new file every flush ?
    - faster and efficient
    - flush everything in one shot

#### Get Key

Every flush creates a new file *SSTable* (in-memory & disk). It writes index and data in same file.
*SSTable* ~ sorted string table.

![](assets/Pasted%20image%2020250919101112.png)

GET (k) flow :
    lookup in memory if key is there, return the value or else start from the latest file on disk
    check if key is present, if yes return value, if no, then keep on checking in backwards in older files. if key is not found return *NOT_FOUND*

We do not need to go through each file, we check the indexes to see if the key present in the file.

#### SS Tables

![](assets/Pasted%20image%2020250919102217.png)

#### Merge and Compaction

Large number of files (immutable) on disk ---> Merge and compaction

Merging of SS table would take $O(n)$ time because data is already sorted !

Worst Case : k files on the disk, you look through all of them to realise key does not exists. Can we optimize this ?

![](assets/Pasted%20image%2020250919102917.png)

What if we have a way to know if key exists or not ?

*Set* -> becomes inefficient at scale. A better data structure which is space efficient ?
*Bloom Filters*

- return Yes (with uncertainty)
- return No (with certainty that it is not present)

### Bloom Filters

![](assets/Pasted%20image%2020250919103638.png)

Above bloom filters can be included in our design now. Another reason we can't use set is because its size will grow/change, and managing its space in our current layout becomes a challenge due to our append only design, while BLOOM filters will be fixed in size and can be allocated in memory as well easily or onto disk.

![](assets/Pasted%20image%2020250919103800.png)

#### How to handle data loss ?
Append all update/delete operations in *WAL* file (write-ahead-log)
This WAL file is truncated on every flush. (*configurations*)

If we are writing to disk every write, how is it faster than Bitcask ?
If we need zero data loss, we have to have WAL

How is it better than Bitcask ?
Keys are disk bound and not memory bound, we get comparable write amplification while being disk bound.

Whole uses LSM ? *RocksDB, LevelDB, BadgerDB* (why not redis) ?
Use cases: Bidding (4 min, bid then persistence, redis key expires and data is gone), Adtech

Some piece of data in memory and some on disk.

![](assets/Pasted%20image%2020250919110030.png)

LSM outperform everything where you want a quickly access for recently inserted keys at scale as LSM is stored in memory before being flushed in the disk.
Redis even though provides persistence, but requires everything to be stored in memory. LSM outshine Redis in recency data access and size bound memory.

