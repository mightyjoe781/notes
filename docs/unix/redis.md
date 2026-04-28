# Redis

[:octicons-arrow-left-24:{ .icon } Back](index.md)

In-memory data structure store. Used as cache, message broker, session store, and real-time leaderboard.

### Installation

```bash
sudo apt install redis-server
sudo systemctl enable --now redis

# macOS
brew install redis && brew services start redis

# Connect
redis-cli
redis-cli -h 127.0.0.1 -p 6379
redis-cli -a yourpassword
```

### Core Commands

```bash
PING                                 # test connection (returns PONG)
SET key "value"
GET key
DEL key
EXISTS key                           # 1 if exists, 0 if not
TYPE key                             # string, list, set, zset, hash
KEYS pattern                         # find keys (avoid in prod - blocks)
SCAN 0 MATCH "user:*" COUNT 100      # non-blocking key scan
TTL key                              # time to live in seconds (-1 = no expiry)
EXPIRE key 3600                      # set expiry in seconds
PERSIST key                          # remove expiry
```

### Data Types

#### String

```bash
SET name "Alice"
GET name
APPEND name " Smith"
INCR counter                         # atomic increment
INCRBY counter 5
SETNX key value                      # set if not exists
SET session:abc token EX 3600        # with expiry
MSET k1 v1 k2 v2
MGET k1 k2
```

#### List (ordered, allows duplicates)

```bash
LPUSH mylist "first"                 # push to head
RPUSH mylist "last"                  # push to tail
LRANGE mylist 0 -1                   # get all elements
LPOP mylist                          # remove and return head
RPOP mylist                          # remove and return tail
LLEN mylist                          # length
LINDEX mylist 0                      # get by index
```

#### Set (unordered, unique)

```bash
SADD myset "a" "b" "c"
SMEMBERS myset
SISMEMBER myset "a"                  # check membership
SCARD myset                          # count elements
SREM myset "a"
SUNION set1 set2                     # union
SINTER set1 set2                     # intersection
SDIFF set1 set2                      # difference
```

#### Hash (field-value pairs)

```bash
HSET user:1 name "Alice" email "alice@example.com" age 30
HGET user:1 name
HMGET user:1 name email
HGETALL user:1
HINCRBY user:1 age 1
HDEL user:1 age
HLEN user:1
HEXISTS user:1 email
```

#### Sorted Set (unique, ordered by score)

```bash
ZADD leaderboard 100 "alice" 200 "bob" 150 "charlie"
ZRANGE leaderboard 0 -1 WITHSCORES  # sorted by score ascending
ZREVRANGE leaderboard 0 2           # top 3
ZRANK leaderboard "alice"           # rank (0-based)
ZSCORE leaderboard "bob"            # get score
ZINCRBY leaderboard 50 "alice"      # increment score
ZCARD leaderboard                   # count members
```

### Pub/Sub

```bash
# Terminal 1 - subscriber
SUBSCRIBE news updates

# Terminal 2 - publisher
PUBLISH news "Hello World"
PUBLISH updates "New version released"
```

### Transactions

```bash
MULTI
SET key1 "val1"
INCR counter
EXEC                                 # execute all atomically

# Discard
MULTI
SET key1 "val1"
DISCARD                              # cancel transaction
```

### Configuration

Edit `/etc/redis/redis.conf`:

```
# Bind to localhost only
bind 127.0.0.1

# Require password
requirepass yourpassword

# Disable dangerous commands
rename-command FLUSHALL ""
rename-command CONFIG ""

# Persistence: RDB (snapshot)
save 900 1    # save if 1 key changed in 900s
save 300 10
save 60 10000

# Persistence: AOF (append-only file, more durable)
appendonly yes
appendfsync everysec
```

### Server Management

```bash
INFO                                 # all server stats
INFO memory                          # memory usage
INFO replication                     # replication status
DBSIZE                               # number of keys
FLUSHDB                              # delete all keys in current db (careful)
FLUSHALL                             # delete all keys in all dbs (careful)
DEBUG SLEEP 0                        # check server responsiveness
redis-benchmark -n 100000 -c 50      # performance benchmark
```

### Tips

- Use `SCAN` not `KEYS` in production - `KEYS` blocks the event loop
- Prefer `EXPIRE` for session/cache keys to prevent memory bloat
- Use hashes to store objects (`HSET user:1 field val`) rather than JSON strings for partial updates
- `redis-cli --latency` monitors round-trip latency in real time
- For high availability: Redis Sentinel (automatic failover) or Redis Cluster (sharding)

### See Also

- [PostgreSQL](postgresql.md) for relational/persistent data
- Also: KeyDB (multi-threaded Redis fork), Valkey (open-source Redis fork), DragonflyDB
