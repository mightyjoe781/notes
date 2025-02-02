# Redis

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

### Installation

Debain/Ubuntu

````bash
sudo apt update
sudo apt install redis-server

# check status
sudo systemctl status redis
````

macOS

````bash
brew install redis
brew service start redis
````

### Setup

#### Access Redis CLI : Connect to redis server

````bash
redis-cli
````

#### Test Connection

````bash
ping # server replies: PONG
````

#### Set and Get Data: storing and retrieving key-value pairs

````bash
SET mykey "Hello Redis"  
GET mykey 
````

#### Enabling Persistence

Edit `/etc/redis/redis.conf`

* For RDB (snapshotting)

````bash
save 900 1  # Save if 1 key changes in 900 seconds  
save 300 10 # Save if 10 keys change in 300 seconds
````

* For AOF (Append Only File)

````bash
appendonly yes  
appendfilename "appendonly.aof" 
````

Restart Redis

````bash
sudo systemctl restart redis
````

### Security

#### 1. Set a Password

Edit `/etc/redis/redis.conf`

````bash
requirepass yourpassword
````

````bash
sudo systemctl restart redis
````

````bash
# Authenticate in redis-cli
AUTH yourpassword
````

#### 2. Bind to Specific IP

Edit `/etc/redis/redis.conf`

````bash
bind 127.0.0.1
````

#### 3. Disable Dangerous Commands

````bash
rename-command FLUSHALL ""
````

#### 4. Enable Firewall

````bash
sudo ufw allow from 192.168.1.0/24 to any port 6379  
````

### Essential Commands

````bash
# set a key
SET mykey "Hello Redis"

# get a key
GET mykey

# delete a key
DEL mykey

# check if exists
EXISTS mykey
````

### Data Types

* Lists

  ````bash
  LPUSH mylist "item1"  
  RPUSH mylist "item2"  
  LRANGE mylist 0 -1  
  ````

* Sets

  ```bash
  SADD myset "item1"  
  SMEMBERS myset  
  ```

* Hashes

  ```bash
  HSET myhash field1 "value1"  
  HGET myhash field1 
  ```

* Sorted Sets

  ```bash
  ZADD myzset 1 "item1"  
  ZRANGE myzset 0 -1  
  ```

### Server Management

````bash
# flush all data
FLUSHALL

# get server info
INFO

# monitor commands
MONITOR
````

### Advanced Features

#### Pub/Sub Messaging

````bash
# publisher
PUBLISH mychannel "Hello"  

# sub
SUBSCRIBE mychannel
````

#### Transactions

Use `MULTI` and `EXEC` for atomic operations

````bash
MULTI  
SET key1 "value1"  
SET key2 "value2"  
EXEC  
````

#### Lua Scripting

````bash
EVAL "return redis.call('GET', 'mykey')" 0
````

### Troubleshooting

````bash
# view redis logs
sudo tail -f /var/log/redis/redis-server.log  

# test connection
redis-cli -h 127.0.0.1 -p 6379 ping  

# check memory usage
INFO memory
````

### Tips

````bash
# using redis as a cache
SET mykey "value" EX 60

# backup data using SAVE or BGSAVE to create snapshots
SAVE

# monitoring performance using redis-benchmark
redis-benchmark -n 100000 -c 50
````

