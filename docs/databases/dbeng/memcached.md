# Memcached

- An item consists of key and value
- A key is a string (250 chars)
- The value can be any type (1MB configurable) *
- Keys have expiration date (TTL) (not reliable, LRU can evict)
- Everything is stored in memory
- don't confuse with Memcachedb
## Memory Management

- Memory allocation is random
- Items freed/allocated causes gaps
- Results in fragmentation
- Memory is allocated in pages (1MB configurable)
- Pages are organized by slab classes
- Pages consists of chunks of fixed size
## LRU

- Memory is limited
- When an item is access its goes to the head
- items that aren't used *may* get removed
- LRU crawler/daemon Cache eviction
- LRU cache per slab cache.

## Threads

![](assets/Pasted%20image%2020250928112203.png)

- One listener thread
- For each connection a new thread is created
- Used to be one global lock
- Changed to a per-item lock.
- Refcounting

## Read/Writes

Internally *hash tables* are used for Read items, which are connected with LRU structure (which is updated as we read the tables)
Writes just update *hash tables* and then updates chunk, and updates the LRU. NOTE: *hash tables* upon collision put the items in buckets, which are to be read in the order.


## Distributed Cache

- Memcached servers are unaware of each other
- client is configured with a server pool
- clients do the distribution through consistent hashing
- upto clients to reshuffle keys when adding/removing servers



Link ~ https://www.youtube.com/watch?v=NCePGsRZFus
