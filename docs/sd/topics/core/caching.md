# Caching & Optimizations

## What is Caching

**Definition**: Caching is the practice of storing frequently accessed data in a temporary, fast-access location to avoid expensive operations.

#### Key Concepts

- **Cache Hit**: Data found in cache (fast)
- **Cache Miss**: Data not in cache, must fetch from origin (slow)
- **Cache Hit Ratio**: Percentage of requests served from cache
- **TTL (Time To Live)**: How long data stays in cache

#### What makes operations expensive ?

- **Network I/O**: API calls, database queries across network
- **Disk I/O**: Reading from hard drives, file systems
- **Computation**: Complex calculations, joins, aggregations

#### Examples of Cacheable Data

- User profile information
- Authentication tokens
- Database query results
- Computed values (total posts, follower counts)
- Static content (images, CSS, JS files)

## Cache Levels

![](assets/Pasted%20image%2020251224114125.png)

### Client-side Caching

**Location**: Browser, Mobile Apps
**Use Cases**:

- Static assets (images, CSS, JS)
- User Preferences
- Offline functionality

Advantages: Zero Network Calls, fastest possible response
Disadvantages: Limited Control, potential for stale data

### Content Delivery Network

**Location**: Geographically distributed edge servers
**Use Cases**:

- Static content delivery
- Image/video streaming
- Global content distribution

**Popular CDNs**: Cloudflare, AWS CloudFront, Akamai

### Reverse Proxy Cache

**Location**: Between clients and application servers
**Use Cases**:

- Caching API responses
- Rate limiting
- Load balancing with cache

**Examples**: Nginx, Apache HTTP Server, AWS ALB 

### Application Level Cache

**Location**: Within application server memory

```python
# In-memory cache example
cache = {}

def get_user_profile(user_id):
    if user_id in cache:
        return cache[user_id]  # Cache hit
    
    profile = database.get_user(user_id)  # Cache miss
    cache[user_id] = profile
    return profile
```

### Distributed Cache (Remote Cache)

**Location**: Separate cache servers (Redis, Memcached)
**Advantages**: Shared across multiple application instances 
**Use Cases**: Session storage, computed results, hot data
### Database-Level Caching

**Types**:

- **Query Result Cache**: Cache query results
- **Buffer Pool**: Cache frequently accessed pages
- **Materialized Views**: Pre-computed query results

## Cache Patterns

### Cache-Aside (Lazy Loading)

**Most Popular Pattern**

```python
def get_data(key):
    # Try cache first
    data = cache.get(key)
    if data is None:
        # Cache miss - fetch from database
        data = database.get(key)
        cache.set(key, data, ttl=3600)  # Cache for 1 hour
    return data

def update_data(key, new_data):
    database.set(key, new_data)
    cache.delete(key)  # Invalidate cache
```

**Pros**: Only caches requested data, handles cache failures gracefully
**Cons**: Cache miss penalty, potential for stale data

### Write-Through Cache

````python
def update_data(key, data):
    database.set(key, data)      # Write to database first
    cache.set(key, data)         # Then update cache
    return data
````

**Pros**: Cache always consistent with database
**Cons**: Higher write latency, unnecessary cache writes

### Write Behind (Write-Back) Cache

````python
def update_data(key, data):
    cache.set(key, data)         # Write to cache immediately
    # Asynchronously write to database later
    queue.enqueue(lambda: database.set(key, data))
    return data
````

**Pros**: Fastest write performance, used in live scores dashboards etc.
**Cons**: Risk of data loss, complex implementation

### Refresh Ahead

````python
def get_data_with_refresh(key):
    data = cache.get(key)
    if data and is_near_expiry(key):
        # Asynchronously refresh cache
        asyncio.create_task(refresh_cache(key))
    return data
````

**Pros**: Reduces cache miss latency 
**Cons**: Complex logic, may refresh unused data

## Cache Population Strategies

![](../../hld/beginner/assets/Pasted%20image%2020251221195711.png)
### Lazy Population (Cache-Aside)

- Load data into cache only when requested
- Most common and practical approach
- Example: Blog posts, user profiles

### Eager Population (Proactive)

- Pre-load data into cache before requests
- Used for predictable access patterns
- Examples: Celebrity tweets, trending topics, live sports scores

### Scheduled Population

```python
# Cron job to warm cache
def warm_cache():
    popular_posts = database.get_trending_posts()
    for post in popular_posts:
        cache.set(f"post:{post.id}", post, ttl=7200)
```

## Cache Eviction Policies

### LRU (Least Recently Used)

- Evicts least recently accessed items
- Good for temporal locality
- **Implementation**: Doubly linked list + hash map

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)  # Mark as recently used
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove LRU item
```

### LFU (Least Frequently Used)

- Evicts least frequently accessed items
- Good for items with different access frequencies
- Tracks access count for each item

### FIFO (First In, First Out)

- Evicts oldest items regardless of usage
- Simple but not optimal for most use cases

### Random Eviction

- Randomly selects items to evict
- Simple implementation, surprisingly effective in some scenarios

### TTL-based Eviction

- Items expire after a set time period
- Prevents indefinite storage of stale data

## Cache Invalidation Strategies

> "There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

### TTL (Time-Based Expiration)

```python
cache.set("user:123", user_data, ttl=3600)  # Expires in 1 hour
```

**Pros**: Simple, prevents indefinite staleness **Cons**: May serve stale data, cache misses after expiration

### Manual Invalidation

```python
def update_user(user_id, new_data):
    database.update_user(user_id, new_data)
    cache.delete(f"user:{user_id}")  # Explicitly remove from cache
```

### Event-Driven Invalidation

```python
# Using message queue for cache invalidation
def on_user_updated(event):
    user_id = event['user_id']
    cache.delete(f"user:{user_id}")
    
message_queue.subscribe("user.updated", on_user_updated)
```

### Tag-Based Invalidation

```python
# Tag related cache entries
cache.set("user:123", user_data, tags=["user", "profile"])
cache.set("posts:user:123", posts, tags=["user", "posts"])

# Invalidate all entries with "user" tag
cache.invalidate_by_tag("user")
```

### Write-Through Invalidation

- Update cache immediately when database changes
- Ensures consistency but adds write overhead

## Cache Consistency Patterns

### Strong Consistency

- Cache and database always in sync
- Use write-through or immediate invalidation
- Higher latency, guaranteed correctness

### Eventual Consistency

- Cache may be temporarily out of sync
- Use TTL or asynchronous invalidation
- Better performance, acceptable staleness

### Cache Warming

```python
def warm_user_cache(user_id):
    """Pre-populate cache with user data"""
    user = database.get_user(user_id)
    friends = database.get_user_friends(user_id)
    posts = database.get_user_posts(user_id)
    
    cache.mset({
        f"user:{user_id}": user,
        f"friends:{user_id}": friends,
        f"posts:{user_id}": posts
    })
```

## Common Caching Challenges

### Cache Stampede

**Problem**: Multiple requests try to regenerate same expired cache entry

```python
import threading

cache_locks = {}

def get_with_lock(key):
    if key not in cache_locks:
        cache_locks[key] = threading.Lock()
    
    with cache_locks[key]:
        data = cache.get(key)
        if data is None:
            data = expensive_database_call(key)
            cache.set(key, data)
        return data
```

### Hotspot Problem

**Problem**: Few keys get most of the traffic 

**Solutions**:

- Consistent hashing for distribution
- Local caching for hot keys
- Read replicas

### Cold Start Problem

**Problem**: Empty cache leads to poor performance initially 

**Solutions**:

- Cache warming strategies
- Gradual cache population
- Fallback mechanisms

### Memory Management

```python
# Monitor cache memory usage
def check_cache_health():
    memory_usage = cache.memory_usage()
    hit_ratio = cache.hit_ratio()
    
    if memory_usage > 0.8:  # 80% memory used
        # Trigger aggressive eviction
        cache.evict_expired()
    
    if hit_ratio < 0.6:  # Less than 60% hit ratio
        # Review caching strategy
        log.warning("Low cache hit ratio")
```

## Cache Metrics and Monitoring

### Key Metrics to Track

- **Hit Ratio**: cache_hits / (cache_hits + cache_misses)
- **Miss Ratio**: cache_misses / (cache_hits + cache_misses)
- **Latency**: Response time for cache operations
- **Memory Usage**: Cache memory consumption
- **Eviction Rate**: How often items are evicted
## Technology Choices

### In-Memory Caches

- **Redis**: Persistent, rich data types, clustering
- **Memcached**: Simple, fast, distributed
- **Hazelcast**: Java-based, distributed computing

### Application-Level Libraries

- **Python**: `functools.lru_cache`, `cachetools`
- **Java**: Caffeine, Guava Cache
- **Node.js**: node-cache, memory-cache

### Managed Cache Services

- **AWS ElastiCache**: Redis/Memcached as a service
- **Google Cloud Memorystore**: Managed Redis
- **Azure Cache for Redis**: Managed Redis service

## Best Practices

### Design Principles

1. **Measure First**: Profile before adding caches
2. **Start Simple**: Begin with basic caching, optimize later
3. **Monitor Everything**: Track metrics and performance
4. **Plan for Failures**: Cache should enhance, not break your system

### Implementation Guidelines

1. **Set Appropriate TTLs**: Balance freshness vs performance
2. **Use Consistent Naming**: Standard key naming conventions
3. **Handle Cache Failures**: Graceful degradation when cache is down
4. **Security**: Don't cache sensitive data unnecessarily

### Common Pitfalls to Avoid

- Caching everything (memory waste)
- Not monitoring cache performance
- Ignoring cache invalidation complexity
- Caching data that changes frequently
- Not handling cache failures gracefully