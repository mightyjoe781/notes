# A. Reference Materials

*Quick reference tables and comparison charts for system design decisions*

------

## Quick Reference Tables

### Latency Numbers Every Programmer Should Know

| Operation                             | Latency                 | Relative Scale |
| ------------------------------------- | ----------------------- | -------------- |
| **L1 cache reference**                | 0.5 ns                  | 1x             |
| **Branch mispredict**                 | 5 ns                    | 10x            |
| **L2 cache reference**                | 7 ns                    | 14x            |
| **Mutex lock/unlock**                 | 25 ns                   | 50x            |
| **Main memory reference**             | 100 ns                  | 200x           |
| **Compress 1KB with Zippy**           | 10,000 ns (10 μs)       | 20,000x        |
| **Send 1KB over 1 Gbps network**      | 10,000 ns (10 μs)       | 20,000x        |
| **Read 4KB randomly from SSD**        | 150,000 ns (150 μs)     | 300,000x       |
| **Read 1MB sequentially from memory** | 250,000 ns (250 μs)     | 500,000x       |
| **Round trip within same datacenter** | 500,000 ns (0.5 ms)     | 1,000,000x     |
| **Read 1MB sequentially from SSD**    | 1,000,000 ns (1 ms)     | 2,000,000x     |
| **HDD disk seek**                     | 10,000,000 ns (10 ms)   | 20,000,000x    |
| **Read 1MB sequentially from HDD**    | 30,000,000 ns (30 ms)   | 60,000,000x    |
| **Send packet CA→Netherlands→CA**     | 150,000,000 ns (150 ms) | 300,000,000x   |

### Powers of Two for Capacity Estimation

| Power    | Exact Value           | Approximate   | Shorthand |
| -------- | --------------------- | ------------- | --------- |
| **2^10** | 1,024                 | 1 thousand    | 1 KB      |
| **2^16** | 65,536                | 64 thousand   | 64 KB     |
| **2^20** | 1,048,576             | 1 million     | 1 MB      |
| **2^30** | 1,073,741,824         | 1 billion     | 1 GB      |
| **2^32** | 4,294,967,296         | 4 billion     | 4 GB      |
| **2^40** | 1,099,511,627,776     | 1 trillion    | 1 TB      |
| **2^50** | 1,125,899,906,842,624 | 1 quadrillion | 1 PB      |

**Common Calculations:**

- 1 GB = 10^9 bytes ≈ 2^30 bytes
- 1 million users ≈ 10^6 ≈ 2^20
- 1 billion requests/day ≈ 12K requests/second
- 100M users × 100 bytes = 10 GB storage

### Common Performance Benchmarks

#### Web Application Metrics

| Metric                | Good    | Acceptable | Poor    |
| --------------------- | ------- | ---------- | ------- |
| **Page Load Time**    | < 1s    | 1-3s       | > 3s    |
| **API Response Time** | < 100ms | 100-300ms  | > 300ms |
| **Database Query**    | < 10ms  | 10-100ms   | > 100ms |
| **Search Response**   | < 100ms | 100-500ms  | > 500ms |
| **File Upload (1MB)** | < 2s    | 2-5s       | > 5s    |

#### System Throughput

| System Type                     | Transactions/Second | Notes           |
| ------------------------------- | ------------------- | --------------- |
| **MySQL (simple queries)**      | 10K-50K TPS         | Single instance |
| **PostgreSQL (simple queries)** | 10K-40K TPS         | Single instance |
| **Redis (in-memory)**           | 100K-1M ops/sec     | Single instance |
| **Cassandra (writes)**          | 10K-100K TPS        | Per node        |
| **Elasticsearch (indexing)**    | 1K-10K docs/sec     | Per node        |
| **Kafka (messages)**            | 100K-1M msgs/sec    | Per broker      |

#### Storage Performance

| Storage Type        | IOPS     | Throughput    | Latency     |
| ------------------- | -------- | ------------- | ----------- |
| **HDD (7200 RPM)**  | 100-200  | 100-200 MB/s  | 10-15 ms    |
| **SSD (SATA)**      | 10K-100K | 500-600 MB/s  | 0.1-1 ms    |
| **NVMe SSD**        | 100K-1M  | 2-7 GB/s      | 0.02-0.1 ms |
| **RAM**             | 10M+     | 50-100 GB/s   | 100 ns      |
| **Network Storage** | 1K-10K   | 100-1000 MB/s | 1-10 ms     |

------

## Comparison Charts

### Database Comparison Matrix

| Database          | Type        | Consistency     | Scalability | Query Language | Use Cases                         |
| ----------------- | ----------- | --------------- | ----------- | -------------- | --------------------------------- |
| **PostgreSQL**    | RDBMS       | ACID            | Vertical    | SQL            | Complex queries, transactions     |
| **MySQL**         | RDBMS       | ACID            | Vertical    | SQL            | Web apps, OLTP                    |
| **MongoDB**       | Document    | Eventual        | Horizontal  | MongoDB Query  | JSON documents, rapid development |
| **Cassandra**     | Wide-column | Eventual        | Horizontal  | CQL            | Time-series, IoT, high writes     |
| **Redis**         | Key-value   | Eventual        | Horizontal  | Redis Commands | Caching, sessions, real-time      |
| **DynamoDB**      | Key-value   | Eventual/Strong | Horizontal  | DynamoDB API   | Serverless, gaming, IoT           |
| **Elasticsearch** | Search      | Eventual        | Horizontal  | Query DSL      | Search, analytics, logging        |
| **Neo4j**         | Graph       | ACID            | Vertical    | Cypher         | Relationships, recommendations    |

#### Detailed Database Features

| Feature                         | PostgreSQL | MongoDB   | Cassandra | Redis | DynamoDB    |
| ------------------------------- | ---------- | --------- | --------- | ----- | ----------- |
| **ACID Transactions**           | ✅          | ✅ (4.0+)  | ❌         | ❌     | ✅ (limited) |
| **Multi-document Transactions** | ✅          | ✅         | ❌         | ❌     | ✅           |
| **Auto-sharding**               | ❌          | ✅         | ✅         | ✅     | ✅           |
| **SQL Support**                 | ✅          | ❌         | ✅ (CQL)   | ❌     | ❌           |
| **JSON Support**                | ✅          | ✅         | ✅         | ✅     | ✅           |
| **Full-text Search**            | ✅          | ✅         | ❌         | ✅     | ❌           |
| **Geospatial Queries**          | ✅          | ✅         | ❌         | ✅     | ❌           |
| **Time-series Optimization**    | ✅          | ✅         | ✅         | ✅     | ❌           |
| **Multi-region**                | ❌          | ✅         | ✅         | ✅     | ✅           |
| **Managed Service**             | ✅ (RDS)    | ✅ (Atlas) | ✅         | ✅     | ✅           |

### Message Queue Feature Comparison

| Feature                   | Apache Kafka      | RabbitMQ      | Amazon SQS      | Redis Pub/Sub | Apache Pulsar     |
| ------------------------- | ----------------- | ------------- | --------------- | ------------- | ----------------- |
| **Message Ordering**      | ✅ (per partition) | ✅ (per queue) | ✅ (FIFO queues) | ❌             | ✅ (per partition) |
| **Message Persistence**   | ✅                 | ✅             | ✅               | ❌             | ✅                 |
| **Message TTL**           | ✅                 | ✅             | ✅               | ❌             | ✅                 |
| **Dead Letter Queue**     | ❌                 | ✅             | ✅               | ❌             | ✅                 |
| **Message Replay**        | ✅                 | ❌             | ❌               | ❌             | ✅                 |
| **Exactly-once Delivery** | ✅                 | ❌             | ❌               | ❌             | ✅                 |
| **Multi-tenancy**         | ❌                 | ✅             | ✅               | ❌             | ✅                 |
| **Schema Registry**       | ✅                 | ❌             | ❌               | ❌             | ✅                 |
| **Geo-replication**       | ✅                 | ✅             | ✅               | ✅             | ✅                 |
| **Throughput**            | Very High         | High          | High            | Very High     | Very High         |

#### Message Queue Performance

| System            | Throughput             | Latency | Retention      | Max Message Size |
| ----------------- | ---------------------- | ------- | -------------- | ---------------- |
| **Kafka**         | 1M+ msgs/sec           | 2-5 ms  | Days/weeks     | 1MB (default)    |
| **RabbitMQ**      | 100K msgs/sec          | 1-2 ms  | Until consumed | 128MB            |
| **SQS**           | 3K msgs/sec (standard) | 10ms    | 14 days        | 256KB            |
| **Redis Pub/Sub** | 1M+ msgs/sec           | < 1ms   | None           | 512MB            |
| **Pulsar**        | 1M+ msgs/sec           | 5-10 ms | Configurable   | 5MB              |

### Load Balancer Capabilities

| Load Balancer  | Type     | Protocol Support | Health Checks | SSL Termination | Geographic |
| -------------- | -------- | ---------------- | ------------- | --------------- | ---------- |
| **NGINX**      | Software | HTTP/TCP/UDP     | ✅             | ✅               | ❌          |
| **HAProxy**    | Software | HTTP/TCP         | ✅             | ✅               | ❌          |
| **AWS ALB**    | Managed  | HTTP/HTTPS       | ✅             | ✅               | ✅          |
| **AWS NLB**    | Managed  | TCP/UDP/TLS      | ✅             | ✅               | ✅          |
| **Cloudflare** | CDN/LB   | HTTP/HTTPS       | ✅             | ✅               | ✅          |
| **F5 BigIP**   | Hardware | All              | ✅             | ✅               | ✅          |

#### Load Balancing Algorithms

| Algorithm                | Use Case                   | Pros                            | Cons                      |
| ------------------------ | -------------------------- | ------------------------------- | ------------------------- |
| **Round Robin**          | Equal capacity servers     | Simple, fair distribution       | Ignores server load       |
| **Weighted Round Robin** | Different capacity servers | Accounts for server differences | Static weights            |
| **Least Connections**    | Variable request times     | Dynamic load consideration      | Connection count overhead |
| **Least Response Time**  | Performance optimization   | Best performance routing        | Complex monitoring        |
| **IP Hash**              | Session persistence        | Consistent routing              | Uneven distribution       |
| **Geographic**           | Global applications        | Reduced latency                 | Complex setup             |

#### Load Balancer Features

| Feature               | NGINX | HAProxy | AWS ALB | Cloudflare |
| --------------------- | ----- | ------- | ------- | ---------- |
| **Layer 4 (TCP)**     | ✅     | ✅       | ❌       | ❌          |
| **Layer 7 (HTTP)**    | ✅     | ✅       | ✅       | ✅          |
| **SSL Termination**   | ✅     | ✅       | ✅       | ✅          |
| **WebSocket Support** | ✅     | ✅       | ✅       | ✅          |
| **Request Routing**   | ✅     | ✅       | ✅       | ✅          |
| **Rate Limiting**     | ✅     | ✅       | ❌       | ✅          |
| **Caching**           | ✅     | ❌       | ❌       | ✅          |
| **DDoS Protection**   | ❌     | ❌       | ✅       | ✅          |
| **Global Anycast**    | ❌     | ❌       | ❌       | ✅          |
| **Auto Scaling**      | ❌     | ❌       | ✅       | ✅          |

------

## Storage and Networking Quick Reference

### Storage Types Comparison

| Storage Type       | Capacity   | Performance | Cost     | Durability | Use Case                |
| ------------------ | ---------- | ----------- | -------- | ---------- | ----------------------- |
| **Local SSD**      | 100GB-10TB | Highest     | Medium   | Low        | App servers, caching    |
| **Network SSD**    | 1GB-64TB   | High        | High     | High       | Databases, file systems |
| **Object Storage** | Unlimited  | Medium      | Low      | Very High  | Backups, static content |
| **Tape Archive**   | Very High  | Very Low    | Very Low | High       | Long-term archival      |
| **Cold Storage**   | Unlimited  | Low         | Very Low | Very High  | Infrequent access       |

### Network Bandwidth Reference

| Connection Type         | Bandwidth          | Latency | Cost   | Use Case             |
| ----------------------- | ------------------ | ------- | ------ | -------------------- |
| **Gigabit Ethernet**    | 1 Gbps             | < 1ms   | Low    | Local networks       |
| **10 Gigabit Ethernet** | 10 Gbps            | < 1ms   | Medium | Data centers         |
| **Fiber Internet**      | 100 Mbps - 10 Gbps | 5-20ms  | Medium | Business connections |
| **Cable/DSL**           | 10-100 Mbps        | 20-50ms | Low    | Consumer connections |
| **Satellite**           | 10-100 Mbps        | 600ms   | High   | Remote locations     |
| **5G Mobile**           | 100 Mbps - 1 Gbps  | 10-50ms | High   | Mobile applications  |

------

## Capacity Planning Quick Calculations

### User Activity Patterns

```
Daily Active Users (DAU) Ratios:
├── Mobile Apps: 10-20% of total users
├── Web Apps: 5-15% of total users  
├── Gaming: 15-30% of total users
├── Social Media: 20-40% of total users
└── Enterprise: 60-80% of total users

Peak Traffic Multipliers:
├── 2x average: Most web applications
├── 3-5x average: E-commerce during sales
├── 10x average: News sites during events
├── 20x+ average: Live streaming events
└── Seasonal: Holiday shopping, tax season
```

### Storage Growth Estimates

```
Data Growth Patterns:
├── User profiles: 1-10 KB per user
├── Social posts: 1-100 KB per post
├── Images: 100 KB - 10 MB each
├── Videos: 10 MB - 1 GB each
├── Logs: 1-100 KB per request
└── Analytics: 100 bytes - 10 KB per event

Annual Growth Rates:
├── User data: 50-100% per year
├── Transaction logs: 100-300% per year
├── Media content: 200-500% per year
├── Analytics data: 300-1000% per year
└── Backup storage: 150-250% per year
```

### Bandwidth Calculations

```
Common Bandwidth Requirements:
├── REST API call: 1-10 KB
├── Web page load: 1-5 MB
├── Image download: 100 KB - 5 MB
├── Video streaming (720p): 2-5 Mbps
├── Video streaming (1080p): 5-10 Mbps
├── Video streaming (4K): 25-50 Mbps
└── Database replication: 10-100 MB/hour

Peak Bandwidth Formula:
Peak = Average × Peak Multiplier × Safety Factor
Safety Factor: 1.5-2x for capacity planning
```

------

## SLA and Availability Reference

### Availability Calculations

| Availability % | Downtime/Year | Downtime/Month | Downtime/Week | Use Case       |
| -------------- | ------------- | -------------- | ------------- | -------------- |
| **90%**        | 36.5 days     | 3 days         | 16.8 hours    | Development    |
| **95%**        | 18.25 days    | 1.5 days       | 8.4 hours     | Internal tools |
| **99%**        | 3.65 days     | 7.2 hours      | 1.68 hours    | Standard web   |
| **99.9%**      | 8.77 hours    | 43.8 minutes   | 10.1 minutes  | Business apps  |
| **99.95%**     | 4.38 hours    | 21.9 minutes   | 5.04 minutes  | E-commerce     |
| **99.99%**     | 52.6 minutes  | 4.38 minutes   | 1.01 minutes  | Financial      |
| **99.999%**    | 5.26 minutes  | 26.3 seconds   | 6.05 seconds  | Emergency      |

### SLA Budget Calculation

```
Error Budget = (1 - SLA) × Time Period

Examples (per month):
├── 99.9% SLA = 43.8 minutes error budget
├── 99.95% SLA = 21.9 minutes error budget  
├── 99.99% SLA = 4.38 minutes error budget
└── 99.999% SLA = 26.3 seconds error budget

Use for:
├── Planned maintenance windows
├── Deployment risk assessment
├── Incident impact analysis
└── Feature release decisions
```

This reference appendix provides quick lookup tables for common system design decisions, performance benchmarks, and capacity planning calculations that every system architect should know.