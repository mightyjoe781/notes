# Performance Optimization

*Techniques and strategies to minimize response time, maximize throughput, optimize resource utilization  and improve user experience in distributed systems.*

Performance can be measured for following aspect in a system

- Latency Optimization : response time
- Throughput Optimization : number of concurrent requests
- Resource Optimization : optimized CPU/memory usages

## Latency Optimization

Latency optimization focuses on reducing the time between a request and its response. Every millisecond matters for user experience, with studies showing that even 100ms delays can significantly impact user engagement and business metrics.

Latency could be due to multiple factors : Network, Processing delays, I/O bottlenecks, queuing, or serialization latency.

### Request Path Optimization

Optimizing the entire journey of a request from client to server and back, minimizing hops, processing time, and data transfer at each step.

- Prefer Newer versions of HTTP Protocols, as they support features like Multiplexing, No HOL blocking, better congestion control. Detailed info can be found here : [Network](network.md)
- Optimize Connection Management using techniques like `keep-alive`, `connection-polling`, `pipelining`, *multiplexing*, or connection prewarming.
- Optimize DNS Resolution using DNS caching, *prefetching*, anycast DNS, TTL Optimization. Usually DNS resolution hierarchy on a machine is in this order : Browser cache -> OS cache -> Router Cache -> ISP DNS -> Authoritative DNS
- Load Balancer Optimization : Should have following characteristics for optimal operation : health checking, geographic routing, least-latency routing, session affinity, circuit breaking, etc.
- API Design : apis should be designed correctly with features like, minimizing payload size, efficient serialization, compression (`gzip`, `brotli` for response compression), field selection (or implement graphQL if querying over bunch of fields), batch operations.

### Database Query Optimization

Database operations are often the primary source of latency in applications. Optimizing queries, indexes, and data access patterns can dramatically improve response times.

- One of the direct improvement that could be done is creating *indexes* (do not go overboard, as larger indexes usually will hit your writing capability fast), create indexes like primary, secondary, composite indexes, etc.
- Query Structure Optimization : Always write queries which are selective and not too broad to avoid full table scan. Analyze Execution plan to avoid such expensive operations.
- Connection Pooling : to avoid cost of re-setup of the connection overhead.
- Add read replicas, helping in splitting traffic and allowing higher throughput.
- Schema Optimization : Denormalize Tables !!!, too frequent join hits the performance quite soon
- Always create Materialized Views for expensive queries
- Add partitioning & Sharding to the database

### Network Latency Optimization

Network latency is often the largest component of end-to-end latency, especially for geographically distributed systems.

- Lowest hanging fruit in this is to put a server close to the user using a CDN or multi-region deployments near the regions with most user-base
- Protocol Optimization : Select a good protocol based on requirements, TCP provides guarantees at the little hit on performance, use UDP if not worries about the data integrity (a lot of games use UDP)
- Select correct application level protocols like HTTP/2, gRPC, Websockets, custom protocols, message packing based on the use-case requirements.
- Data Transfer Optimization : We could compress & encode the data before sending reducing overall transfer size. There are many techniques like `gzip` , *Brotli* for text compression, WebP, AVIF for images, adaptive bit-rate compression for streaming, Binary protocols like Protobuf, MessagePack, or sending just the delta for each update.
- Request Batching & Bundling from clients, combining multiple API calls, group database operations, event batching, etc.
### Application-Level Optimization

- A simple solution is to use asynchronous processing, we don't block I/O and return the response once its calculated, using resources optimally, there will not be any kind of blocking and a event-driven architecture will shine here.
- Techniques like, Req/Res, Webhooks, SSE, WebSockets and Polling are used.
- Precomputation can help an application to respond to requests fast, eg. Materialized Views, Aggregate tables, Search Indexes, etc.
- Precomputing (*Caching*) comes with problem of invalidation (stale-data serving) problems.

### Infrastructure Optimization

- Define the Success Metrics and KPIs to have a view about what to expect.
- Infrastructure Considerations
    - SSD vs HDD : Faster disk I/O for databases
    - Memory Sizing : Adequate RAM for caching
    - CPU selection: Single-core performance vs cores
    - Network bandwidth: Sufficient capacity for traffic
    - Geographic placement: Minimize physical distance
- Cloud Optimizations :
    - Instance types: Choose CPU/memory optimized
    - Placement groups: Co-locate related services
    - Enhanced networking: Higher bandwidth/lower latency
    - Local storage: NVMe SSD for temporary data
    - Dedicated tenancy: Avoid noisy neighbor issues

### Lazy Loading

Lazy Loading is a design pattern that defers the loading of resources until they are actually needed, improving initial load times and reducing unnecessary resource consumption.

In design patterns its often implemented using virtual proxy pattern.

Real Life Usages includes JPA/Hibernate, Entity Frameworks, Proxy Objects in ORM, Session Requirements

Read more about N+1 Query Problem,

## Throughput Optimization

Throughput optimization focuses on maximizing the volume of work a system can process within a given timeframe. Unlike latency optimization which focuses on individual request speed, throughput optimization aims to handle the maximum number of concurrent operations efficiently.

A Biggest drawback of optimizing throughput comes with cost of increased latency. Batch processing although improved throughput but responses are delayed.

- Connection Reuse improves both throughput and latency.
- Parallel processing improves both with proper design.
- A Resource Contention can hurt both throughput and latency.

Metrics to measure throughput are Request per seconds (RPS), txn per second (TPS), messages per second, bytes per second, operations per second.

### Connection Pooling

Connection pooling maintains a pool of reusable database connections to eliminate the overhead of creating and destroying connections for each operation, significantly improving throughput.

Components of Connection Pool : Pool Manager, Connection Factory, Connection Validator, Pool Monitor and Eviction Policy(for connections).


```
Optimal Pool Size = (Core Count × 2) + Effective Spindle Count
```

### Batch Processing

Batch processing groups multiple operations together to reduce per-operation overhead and improve overall throughput by amortizing fixed costs across multiple operations

Example of Database Batching Operations like Batch Inserts/Updates/Deletes, etc

```sql
INSERT INTO users (name, email, created_at) VALUES
  ('User1', 'user1@example.com', NOW()),
  ('User2', 'user2@example.com', NOW()),
  ('User3', 'user3@example.com', NOW());
```


Messages Batching Strategies

- Size-based batching: Process N messages together
- Time-based batching: Process messages every T seconds
- Hybrid batching: Whichever threshold is reached first
- Priority batching: Group messages by priority
- Destination batching: Group by target system

#### Batch Collection Strategies

Collection Patterns:

- Queue-based collection: Accumulate in memory queue
- Buffer-based collection: Fixed-size circular buffer
- Time-window collection: Collect for specific duration
- Trigger-based collection: External event triggers processing
- Adaptive collection: Dynamic batch size based on load

Buffer Management:

- Single buffer: Simple but blocks during processing
- Double buffer: Switch buffers for continuous collection
- Ring buffer: Circular buffer for memory efficiency
- Priority buffers: Separate buffers by message priority
- Partitioned buffers: Multiple buffers for parallel processing

Batch Processing Execution Patterns could be as follows : Sequential, Parallel, Pipeline, Stream (I use this at job) & scheduled.

Error handling in Batches becomes important as well, how to deal when batch fails to process ?

- All or nothing
- Partial Success
- Individual retry
- Dead Letter Handling

### Parallel Processing

Parallel processing divides work across multiple execution units (threads, processes, or machines) to increase overall throughput by utilizing available computational resources effectively.

There are multiple types of threading model, few are given as follows

- Thread pool: Fixed number of worker threads
- Fork-join: Divide work and merge results
- Pipeline: Sequential stages with parallel execution
- Producer-consumer: Separate threads for different roles
- Actor model: Independent actors processing messages

Thread Pool Sizing refers to configuring number of threads

- CPU-intensive tasks : number of cores
- I/O intensive : number of CPU cores x (1 + wait time / cpu time)

Since threads work under a single process and really works on concurrency rather than parallelism, for true parallel processing we should use Process Pools

Process Pool Models 

- Multiprocessing: Multiple processes on same machine
- Distributed processing: Processes across multiple machines
- Map-reduce: Distribute computation across cluster
- Microservices: Independent services processing requests
- Serverless: Event-driven parallel execution

The main issue with Processes is they can't have shared state by design, to avoid memory access, so solely relies on message passing which is flexible but introduces a network overhead.

A good message passing mechanism can be implemented using message queue (asynchronous), database (persisted) and event-stream (real-time)

#### Parallel Processing Patterns

Data Parallelism

- Partition Processing
- Map-Reduce
- Scatter-Gather
- Fork-join
- Parallel Loops

Task Parallelism

- Pipelines
- Worker Pool
- Master-Worker
- Peer-to-peer
- Event-Driven

Another Topic which is important in this regard is Synchronization and Coordination. There are multiple synchronization mechanisms like locks, semaphores, barriers, Atomic Operations, Message passing etc.

But introducing such constructs makes a program less maintainable and difficult to understand without proper documentation, A lot of high-level programming languages like python, java provides constructs which are simpler and instructive to use.
Examples : compare-and-swap (CAS), Lock-free data structures (queues, stacks, maps), wait-free algorithms, memory barriers, hazard pointers, borrow-checker system from Rust, etc.

Although Parallel processing sounds cool and it does introduce performance but when used carefully, some of the well known problem inherently arises from introducing parallel processing are

- Contention
- False Sharing
- Context Switching
- Memory Locality
- NUMA effects : Non-uniform access costs

### System Level Optimization

We can broadly divide these into actual hardware improvements and network improvements

- CPU Optimizations
- Memory Optimizations
- I/O Optimizations

Network Optimizations are discussed above, which include having *keep-alive* connections, *multiplexing*, *compression*, *CDN optimizations*, and *Protocol-Optimization*

Bandwidth Management

- Keep-alive connections: Reuse TCP connections
- HTTP/2 multiplexing: Multiple requests per connection
- Compression: Reduce data transfer volume
- CDN utilization: Offload static content delivery
- Protocol optimization: Choose efficient protocols

### Application Level Optimizations

There optimizations can be implemented in the actual business logic of the application, for e.g. using optimal algorithms, caring about time-space complexity of the algorithm, use parallel algorithm if you have multiple cores, use approximate algorithm if problem is really hard to solve.

Another much simpler optimization is using *cache*, store responses for expensive operations.

### Database Optimization

To increase throughput of the database we should use *connection pooling*, *connection/splitting*, Create Master-Replica for read/writes, *connection affinity* and connection health-monitoring.

We can use use the optimizations introduced for performance as well to improve throughput.
## Resource Optimization

Resource optimization focuses on making the most efficient use of available system resources. This involves understanding resource constraints, identifying bottlenecks, and implementing strategies to maximize resource utilization while maintaining acceptable performance levels.

A system can have following resources which we can Aim to improve : CPU, Memory, Storage I/O, Network I/O, GPU.

We should not blindly try to optimize the resources, we should first identify the bottleneck and measure the baselines and potential gains we could make. In computer science everything is a trade-off and improving something will cost you something else. Profile your optimization and right-size your infra.

Common Bottleneck Patterns are

-  CPU-bound: High CPU utilization, low I/O wait time
- Memory-bound: High memory usage, frequent garbage collection
- I/O-bound: High disk/network wait times, low CPU usage
- Network-bound: High network latency, bandwidth saturation
- Mixed bottlenecks: Multiple resources limiting performance

### Memory Management

Effective memory management is crucial for system performance, involving efficient allocation, usage, and deallocation of memory resources to minimize waste and maximize performance.

There are multiple ways to allocate memory : Stack (fast) and Heap Memory (flexible).

We can use concepts like Memory Pool Allocation to reduce fragmentation and faster allocation with reduced overhead, it provides better cache locality.

Few other improvements can be done using optimizing Garbage collection. Garbage collector tuning could be complicated and difficult to do, but I will just outline quite basic introduction here.

Garbage collection removes old unreferenced memory, it marks the reachable objects, sweeps unreachable ones, only issue is this could be a stop-the-world process and memory becomes fragmented. So its more about tuning and finding the correct balance.

Some basic JVM tuning parameters are

```bash
# Heap sizing
-Xms2g -Xmx4g  # Initial and maximum heap size

# Generational tuning
-XX:NewRatio=3  # Old/Young generation ratio
-XX:SurvivorRatio=8  # Eden/Survivor space ratio

# GC algorithm selection
-XX:+UseG1GC  # G1 garbage collector
-XX:MaxGCPauseMillis=200  # Target pause time

# GC monitoring
-XX:+PrintGC -XX:+PrintGCDetails
```

There are some notes already present on GC Tuning in Pyspark topics in this site.

Another Optimization is using cache-friendly memory patterns : Array of structures (AoS) has poor cache locality while Structure of Arrays (SoA) has better cache-locality.
### CPU Optimization

CPU optimization involves maximizing computational efficiency through algorithm optimization, parallelization, and efficient resource utilization.

Generally following types of utilization patterns cause High CPU Usage : CPU-bound workloads, Inefficient algorithm, excessive context switching, lock contentions, cache misses, all of these hammer the CPU

We use techniques like, thread affinity (binding thread to cpu cores) and NUMA to improve Performance, other such examples are vectorization and SIMD, having a simpler data layout helps as well.

Example of using SIMD (Single-Instruction, Multiple Data)

```python
import numpy as np

# Scalar operation - processes one element at a time
def scalar_add(a, b):
    result = []
    for i in range(len(a)):
        result.append(a[i] + b[i])
    return result

# Vectorized operation - processes multiple elements simultaneously
def vectorized_add(a, b):
    return np.add(a, b)  # Uses SIMD instructions

# Performance comparison
a = list(range(1000000))
b = list(range(1000000))

# Vectorized is typically 10-100x faster
```

### I/O Optimization

I/O optimization focuses on minimizing the time spent waiting for disk reads/writes and network operations, which are often the slowest components in a system.


| Storage Type | Latency  | Throughput   | Cost      | Use Case                     |
| ------------ | -------- | ------------ | --------- | ---------------------------- |
| NVMe SSD     | 10-100μs | 3-7 GB/s     | High      | High-performance databases   |
| SATA SSD     | 50-150μs | 500-600 MB/s | Medium    | General applications         |
| HDD          | 5-15ms   | 100-200 MB/s | Low       | Archival, bulk storage       |
| RAM Disk     | <1μs     | 10-20 GB/s   | Very High | Temporary high-speed storage |

- Sequential I/O is always more efficient than random access
- File system optimization is also important
    - **ext4**: Good general-purpose performance
    - **XFS**: Better for large files and high throughput
    - **ZFS**: Advanced features, built-in compression
    - **Btrfs**: Copy-on-write, snapshots
    - **tmpfs**: RAM-based file system for temporary data
- Always use Non-Blocking (Asynchronous) Operation as Disk I/O is very slow.
- Simple and straightforward improvements for Network I/O are
    - TCP Optimization
    - Connection Pooling
    - I/O Buffering
    - Caching
- Memory Mapped files can improve the performance as well, if the file is open accessed.

### Resource Monitoring and Optimization

#### Memory

Memory Profiling Tools

- Java: JProfiler, VisualVM, Eclipse MAT
- Python: memory_profiler, pympler, tracemalloc
- C/C++: Valgrind, AddressSanitizer, Intel VTune
- Go: go tool pprof, runtime.MemStats
- JavaScript: Chrome DevTools, Node.js --inspect

Memory Usage Metrics

- Heap utilization: Percentage of heap memory used
- Allocation rate: Objects allocated per second
- GC frequency: Garbage collection cycles per minute
- GC pause time: Time spent in garbage collection
- Memory leaks: Objects that should be freed but aren't
- Fragmentation: Unusable memory due to layout

#### CPU

Profiling Tools

- **perf**: Linux performance analysis
- **Intel VTune**: Comprehensive CPU profiling
- **gprof**: GNU profiler for C/C++
- **py-spy**: Python profiling
- **Node.js --prof**: JavaScript profiling

Key Metrics to Observe

- **CPU utilization per core**: Identify uneven load distribution
- **Context switch rate**: High rate indicates inefficiency
- **Cache hit ratios**: L1/L2/L3 cache effectiveness
- **Branch prediction accuracy**: CPU pipeline efficiency
- **Memory bandwidth utilization**: Memory subsystem performance

#### I/O

Key Metrics to Observe

- **IOPS**: Input/output operations per second
- **Throughput**: Bytes transferred per second
- **Latency**: Time to complete I/O operation
- **Queue depth**: Pending I/O operations
- **Utilization**: Percentage of time device is busy

Monitoring Tools

- `iostat -x 1` : Monitor I/O statistics, extended statistics every second
- `iotop -o` : Monitor per-process I/O, shows only process doing I/O
- `sar -d 1` : Detailed I/O analysis, device utilization statistics
- `iftop` : Network traffic by connections
- `nethogs` : Network usage by process, very useful in real-life.

## Capacity Planning

*Very Important for interviews,*

Capacity planning is the process of determining the infrastructure resources needed to meet current and future demand. It involves estimating system requirements, predicting growth patterns, and ensuring adequate resources are available when needed.

Idea is to have rough estimates of size of infrastructure to handle the load on the application, ultimately helping in avoiding outages, control costs(budget), maintain performance, and future extendibility/scaling.

### Back-of-Envelope Calculations

These are just estimation numbers, and are very useful in getting the rough-estimate of design.

Read This Before Proceeding : [Estimation Numbers](../../appendices/ref_numbers.md)

Traffic and Load Calculations

Lets calculate DAU (daily active users) to QPS (query/second) Conversion.

Problem : You are given to calculate QPS for a social media platform, with 100M (million) DAU, users take almost 50 actions per day, and the peak factor is : 3x (traffic is not evenly distributed).

$$
QPS = \frac{DAU \times \text{actions per user per sec}}{24 \times 3600} \times \text{peak fator}
$$

Here answer would be : `173,611 QPS`

This is a huge-load, but traffic either be write or read, assume it would be more *read-heavy* almost (100:1)

Let's estimate storage requirements here : Assume users will be uploading average of 2 photos/user/day and average photo size is 2GB, and we require to store the data for user 5 years

Let's estimate Storage Requirements

```
Daily storage: 100M × 2 × 2MB = 400TB/day
Annual storage: 400TB × 365 = 146 PB/year
5-year storage: 146PB x 5 = 760 PB

Including replicas (3x): 760PB × 3 = 2280 PB
```

This is huge storage to completely in real-time, but in real-life we optimize storage using various retention policies

- **Hot data**: Recent, frequently accessed (expensive storage)
- **Warm data**: Older, occasionally accessed (medium cost)
- **Cold data**: Archive, rarely accessed (cheap storage)

Let's calculate database size required for this application

```
Users Metadata
- 100M users
- 500 bytes per user recrods
- 3 x replication factor
  
Storage : 100M x 500 bytes x 3 = 150 GB (pretty decent size)
```

So we understood our focus should be more on storage of the actual user content and design should be heavily focused on that.

Let's calculate network bandwidth required

```
Bandwidth Calculation:
- 10M concurrent viewers
- Average bitrate: 5 Mbps
- Peak factor: 2x

Peak bandwidth = 10M × 5 Mbps × 2 = 100 Tbps
```

Let's calculate approximate API traffic on microservices around this service

```
Request/Response Sizing:
- Average request size: 1KB
- Average response size: 10KB
- QPS: 173,611 ~ 200, 000

Inbound bandwidth: 200,000 × 1KB = 200MB/s
Outbound bandwidth: 200,000 × 10KB = 2GB/s
```

### Performance Testing

Types of Performance Testing

- Load Testing : verify system performance under expected load, extended periods (hours to days)
- Stress Testing : Find system breaking, short-bursts with high intensity, evaluates scaling
- Spike Testing : Test response to sudden traffic increase, sudden traffic surges
- Volume Testing : Test with large amounts of data, Varies based on data processing time


Usually mean response time is a bad indicator of user experience as outliers deviate mean, P95/P99 are more realistically represent the user experience accurately

Open-Source Tools for Performance Testing:

- Apache JMeter: Comprehensive GUI-based testing
- Artillery: Modern, lightweight load testing
- k6: Developer-centric performance testing
- Gatling: High-performance load testing

Cloud Based Solution

- AWS Load Testing: Distributed load generation
- Azure Load Testing: Managed load testing service
- Google Cloud Load Testing: Scalable performance testing
- BlazeMeter: SaaS load testing platform

Under Stress Evaluate CPU, Memory, Database, and Network Bottlenecks
### Resource Estimation

#### Server Sizing Methodology

- Capacity Estimation can be used to estimate sizing, ``

```
Required Capacity = Peak Load × Safety Factor / Utilization Target

Where:
- Peak Load: Maximum expected demand
- Safety Factor: 1.2-2.0 (20-100% buffer)
- Utilization Target: 60-80% (avoid resource saturation)
```

- General Recommendation
    - CPU Allocation
        - Web servers: 2-4 cores per 1,000 QPS
        - Application servers: 4-8 cores per 1,000 TPS
        - Database servers: 8-16 cores + high clock speed
        - Cache servers: 4-8 cores + high memory
    - Memory Allocation
        - Web servers: 4-8GB base + 1-2GB per 1,000 QPS
        - Application servers: 8-16GB base + 2-4GB per 1,000 TPS
        - Database servers: 50-80% of data working set
        - Cache servers: 90% dedicated to cache storage

#### Cost Optimization Strategies

There are two main ways to optimize costs

- Reserved Capacity : Have a combination of reserved and spot instances for operations.
    - Select instances which are optimized for tasks at hand, compute-optimized, memory, storage optimized, or general purpose instances.
- Resource Optimization
    - Right-Sizing
    - Schedule based Scaling
    - Geographic Optimizations
    - Storage Tiering

#### Growth Forecasting

- Linear Growth : `Future Traffic = Current Traffic + (Growth Rate × Time Period)`
- Exponential Growth : `Future Traffic = Current Traffic × (1 + Growth Rate)^Time Period`
- S-Curve Growth
    - Initial slow growth
    - Rapid acceleration phase
    - Eventual plateau

**Remember**: Capacity planning is an ongoing process that requires regular review and adjustment. Start with conservative estimates, validate with testing, and refine based on actual usage patterns and business growth.