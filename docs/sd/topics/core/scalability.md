# Scalability

Scalability is the capability of a system to handle a growing amount of work or its potential to accommodate growth. There are two main approaches to scaling:

- **Horizontal Scaling (Scale Out)**: Adding more machines to the resource pool
- **Vertical Scaling (Scale Up)**: Adding more power (CPU, RAM) to existing machines

![](assets/Pasted%20image%2020251225225344.png)

## Horizontal Scaling

Horizontal scaling involves adding more servers to your existing pool of servers to handle increased load. It's also known as "scaling out".

Key Characteristics of such scaling is following : Distributed Load, Linear Growth, Fault Tolerance, Geographic Distribution.

Horizontal Scaling inherently introduces problems related to state of application and consistency of the data.

Stateless Applications are application which don't store the client data between requests, each such request contains all information needed to process it. Such design makes the application easy to scale and easy to distribute load. Such system is fault-tolerant (as data is not lost when nodes are disconnected,) and cache-friendly. Even if some portion of your app needs to store the data, then it should be stored in shared store, strictly avoid storing any kind of data which when lost makes your system inconsistent.

![](assets/Pasted%20image%2020251225230021.png)

A very common design in APIs is to create idempotency to avoid multiple processing of the same request. Use full to avoid multiple charge back on the user.

Session can be managed effectively using two ways

- Sticky Session (Session Affinity) : Each request is always sent to same server, based on some logic on Load Balancer Layer. Not reliable as if server goes down during communication then system might not recover and reprocess the same request. Other issues could be like hot-spotting issue, as same server is mapped to same server.
- Shared Session Storage : Session data is stored in a shared, external storage system.
    - There are multiple options for storing session data.
        - Redis/Memcached: Fast, in-memory storage
        - Database: Persistent but slower
        - Distributed Cache: Scalable and fault-tolerant
    - Only issue with this is network latency and operational difficulty of managing such setup.

## Vertical Scaling

Vertical scaling involves adding more power (CPU, RAM, storage) to existing machines. It's also known as "scaling up."

Vertical Scaling often is not limited to just adding more power, it may include resource optimizations as well so that server handles more load.

Resource Optimizations which help in such scaling are

- CPU Optimization
    - profile applications to identify bottlenecks
    - optimize algorithms and data structures
    - use efficient programming practices
    - implement proper caching strategies
- Memory Optimizations
    - Reduce memory footprints
    - implement proper garbage collections
    - use memory-efficient data structures
    - monitor memory leaks.

Performance Tuning involves following

- For Database
    - optimize queries & add proper indexes
    - use connection pools
    - implement query caching
- For Application
    - Use profiling tools
    - implement efficient algorithms
    - reduce I/O operations
    - Use asynchronous programming where appropriate

Ultimately, Vertical Scaling is still bounded by the physical limitations of the host machines, based on attributes like Maximum CPU cores and RAM capacity, storage I/O limitations, Network Bandwidth constraints.
The performance gain on the Vertical Scaling gives diminishing gains, as we start scaling it. Since we have only one machine it could be a single point of failures.

Ideally we prefer vertical scaling in scenarios where the actual codebase is too old to be modified and needs scaling, or application which require shared states.

## Data Scaling

As applications grow, databases often become the primary bottleneck. Data scaling strategies help distribute database load and improve performance.

### Read Replicas

Creating read-only copies of the primary database to distribute read traffic.

1. Master-Slave Setup: One primary (master) database handles writes
2. Replication: Changes are replicated to slave databases
3. Read Distribution: Read queries are distributed across replicas

Advantages of Read Replicas are improved read performance, and database becomes highly available. We could use replicas for backups and analytics without any performance hit to performance.
But this comes the cost of Replication Lags and introducing eventual consistency in the system, and system becomes complex to manage.
### Write Scaling Strategies

Write operations are more challenging to scale as they typically require consistency guarantees.

Write Scaling Approaches

- Write-through Caching : write to db first, then update cache, when reading check cache first
- Write-behind Caching : write to cache first, then database

We could shard our database as well to have efficient write performance, but be careful as this will introduce hot-spot problem, which needs to be dealt with care.
### Data Partitioning Techniques

Splitting large datasets across multiple databases or servers to improve performance and manageability.

Data could be partitioned following ways

- Horizontal Partitioning (Sharding)
    - Range-Based
    - Hash-Based
    - Directory Based.
- Vertical Partitioning : Split tables by columns rather than rows.

Partitioning Data allows us to use parallel processing on different partitions and helps in better resource utilizations, transactions do not need to lock entire database, and care about of only current partition, Easier maintenance of smaller datasets.

If data access pattern is too much reliant on joins or cross-shard queries then this could be the worst decision taken, or data is rebalanced too often.

That is why choosing partitioning key is very important, and we should monitor for potential hot shards, and avoid cross-shard queries whenever possible.
## Auto-Scaling Strategies

Automatically adjusting the number of servers based on current demand.

Types of Auto Scaling

- Reactive Auto-Scaling : scale based on current metrics like (CPU, memory, request count), responds to load after it has occurred.
- Predictive Auto-Scaling : scale based on predicted future demand, often predicted based on older data using machine learning
- Scheduled Auto-Scaling : scale based on known patterns (time of day, day of week)

Points to Consider when implementing a Autoscaling strategy

- Warm-up Time: New instances need time to start
- Cool-down Period: Prevent thrashing between scale events
- Health Checks: Ensure new instances are ready before routing traffic
- Graceful Shutdown: Handle existing connections during scale-in

## Comparisons

| **Factor**      | **Horizontal Scaling** | **Vertical Scaling** | **Data Scaling** |
| --------------- | ---------------------- | -------------------- | ---------------- |
| Cost            | Linear growth          | Exponential growth   | Moderate         |
| Complexity      | High                   | Low                  | Very High        |
| Fault Tolerance | Excellent              | Poor                 | Good             |
| Performance     | Good                   | Excellent            | Excellent        |
| Flexibility     | High                   | Low                  | High             |

## Important Points

### When to Use Each Strategy

**Horizontal Scaling**:

- High traffic applications
- Geographically distributed users
- Need for high availability
- Stateless applications

**Vertical Scaling**:

- Legacy applications
- Applications with shared state
- Simple scaling requirements
- Cost-effective for small to medium scale

**Data Scaling**:

- Database is the bottleneck
- Large datasets
- High read/write volumes
- Need for geographical data distribution
## Monitoring and Metrics

### Key Metrics to Track

**Performance Metrics**:

- Response time and latency
- Throughput (requests per second)
- Error rates
- Resource utilization (CPU, memory, disk, network)

**Scaling Metrics**:

- Number of active instances
- Auto-scaling events
- Load distribution across servers
- Queue lengths and processing times

## Conclusion

Scalability patterns are essential for building systems that can grow with demand. The choice between horizontal and vertical scaling depends on specific requirements, constraints, and growth patterns. Data scaling adds another dimension, focusing on database performance and distribution.

In practical system we may often use combination of above techniques creating hybrid scaling patterns.