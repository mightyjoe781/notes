# Redis

Most popular database on AWS as complex cloud application deployments. Redis popularity as a database, a cache, and a message broker in modern cloud architecture provides an explanation for its position in the AWS ranking but not in wider world.

*Redis ~  In Memory, key-value store, NoSQL Database*

- Redis is Key-Value Store NoSQL Database
- Key is a string, value is pretty much anything
- Redis is in memory first
- Single threaded (except when durability is enabled)
### Optional Durability

- Journaling (append only log AOP)
- Snapshotting
- Both of happen in background asynchronously

### Transport Protocol

- Uses TCP
- Request/Response just like HTTP
- Message format is RESP (REdis Serialization Protocol)

### PUB/SUB

- Redis support Publish subscribe model.
- switches to push model in that case.  (*push model* ~ can't guarantee whether client gets the message)

### Replication/Clustering

- Replication - One Leader many followers model.
- Clustering - Shard data across multiple nodes.
- Hybrid

### Example


```bash
docker run --name rdb -p 6379:6379 -d redis

# login
docker exec -it rdb redis-cli
```


```bash
set name "smk"

get name

set tempname "hmk" EX 10
get tempname

get tempname # -- (nil) (after 10s)

exists tempname # (integer) 0
exists name # (integer) 1

del name
append name "smk" # return len of the content (integer) 3
append name "hmk" # return len of the content (integer) 6

get name


subscibe news # blocks the shell, open a new terminal 

# new term
publish news "REDIS is good!" # (integer) 1
publish news "world on fire!" # (integer) 0
```

- Test db reset by killing the container ~ default is durability :)