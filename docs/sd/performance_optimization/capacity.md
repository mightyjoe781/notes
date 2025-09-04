# Capacity Planning

*Strategic planning to ensure systems can handle expected load and growth while optimizing costs and performance.*

#### Overview

Capacity planning is the process of determining the infrastructure resources needed to meet current and future demand. It involves estimating system requirements, predicting growth patterns, and ensuring adequate resources are available when needed.

#### Why Capacity Planning Matters

- **Avoid outages**: Ensure systems can handle peak loads
- **Control costs**: Right-size resources to avoid over-provisioning
- **Maintain performance**: Keep response times within acceptable limits
- **Enable growth**: Plan for business expansion and user growth
- **Risk management**: Prepare for unexpected traffic spikes

#### Types of Capacity Planning

- **Reactive planning**: Respond to current bottlenecks and issues
- **Proactive planning**: Anticipate future needs based on projections
- **Strategic planning**: Long-term capacity aligned with business goals
- **Tactical planning**: Short-term adjustments for immediate needs

### Business Impact of Poor Planning

**Under-provisioning Consequences:**

- System outages and downtime
- Poor user experience and churn
- Lost revenue opportunities
- Damage to brand reputation
- Emergency scaling costs

**Over-provisioning Consequences:**

- Wasted budget on unused resources
- Higher operational costs
- Reduced profitability
- Resource allocation inefficiency

------

## Back-of-Envelope Calculations

### Fundamental Numbers Every Engineer Should Know

#### Latency Numbers

| Operation                            | Latency | Notes             |
| ------------------------------------ | ------- | ----------------- |
| L1 cache reference                   | 0.5 ns  | CPU cache         |
| L2 cache reference                   | 7 ns    | CPU cache         |
| RAM access                           | 100 ns  | Main memory       |
| SSD random read                      | 150 μs  | Solid state drive |
| HDD seek                             | 10 ms   | Mechanical drive  |
| Network round trip (same datacenter) | 0.5 ms  | Local network     |
| Network round trip (coast-to-coast)  | 150 ms  | Cross-country     |

#### Storage and Data Sizes

**Powers of 2:**

- 2^10 = 1,024 ≈ 1 Thousand (K)
- 2^20 = 1,048,576 ≈ 1 Million (M)
- 2^30 = 1,073,741,824 ≈ 1 Billion (G)
- 2^40 = 1,099,511,627,776 ≈ 1 Trillion (T)

**Common Data Sizes:**

- ASCII character: 1 byte
- Unicode character: 2-4 bytes
- Integer: 4 bytes
- Long/Timestamp: 8 bytes
- UUID: 16 bytes

### Traffic and Load Calculations

#### Request Volume Estimation

**Daily Active Users (DAU) to QPS Conversion:**

```
Peak QPS = DAU × Actions per user per day / (24 × 3600) × Peak factor

Example: Social Media Platform
- 100M DAU
- 50 actions per user per day
- Peak factor: 3x (traffic isn't evenly distributed)

Peak QPS = 100M × 50 / 86,400 × 3 = 173,611 QPS
```

**Common Peak Factors:**

- Consumer applications: 2-4x average
- Business applications: 1.5-2x average
- Global applications: 1.5-2x (due to time zone distribution)
- Regional applications: 3-5x average

#### Read/Write Ratio Analysis

**Typical Read/Write Ratios:**

- Social media feeds: 100:1 (read-heavy)
- E-commerce: 10:1 (read-heavy)
- Analytics platforms: 1000:1 (read-heavy)
- Chat applications: 1:1 (balanced)
- Logging systems: 1:100 (write-heavy)

### Storage Calculations

#### Data Growth Estimation

**User-Generated Content Example (Instagram-like):**

```
Storage Requirements:
- 500M users
- Average 2 photos per user per day
- Average photo size: 2MB
- Keep photos for 5 years

Daily storage: 500M × 2 × 2MB = 2TB/day
Annual storage: 2TB × 365 = 730TB/year
5-year storage: 730TB × 5 = 3,650TB = 3.65PB

Including replicas (3x): 3.65PB × 3 = 10.95PB
```

**Database Storage Estimation:**

```
User Metadata Example:
- 500M users
- 500 bytes per user record
- 3x replication factor

Storage = 500M × 500 bytes × 3 = 750GB
```

#### Data Retention Policies

**Storage Cost Optimization:**

- **Hot data**: Recent, frequently accessed (expensive storage)
- **Warm data**: Older, occasionally accessed (medium cost)
- **Cold data**: Archive, rarely accessed (cheap storage)

**Typical Retention Patterns:**

- User activity logs: 90 days hot, 2 years warm, 7 years cold
- Transaction data: 1 year hot, 7 years warm, permanent cold
- Media files: 30 days hot, 1 year warm, 5 years cold

### Network Bandwidth Calculations

#### Bandwidth Requirements

**Video Streaming Platform Example:**

```
Bandwidth Calculation:
- 10M concurrent viewers
- Average bitrate: 5 Mbps
- Peak factor: 2x

Peak bandwidth = 10M × 5 Mbps × 2 = 100 Tbps
```

**CDN Distribution:**

- Origin bandwidth: 10% of total (10 Tbps)
- Edge bandwidth: 90% distributed globally

#### API Traffic Estimation

**RESTful API Bandwidth:**

```
Request/Response Sizing:
- Average request size: 1KB
- Average response size: 10KB
- QPS: 100,000

Inbound bandwidth: 100,000 × 1KB = 100MB/s
Outbound bandwidth: 100,000 × 10KB = 1GB/s
```

### Resource Estimation Examples

#### Web Application Scaling

**E-commerce Platform:**

```
Requirements:
- 1M daily active users
- 50 page views per user per day
- Peak factor: 4x

Peak QPS = 1M × 50 / 86,400 × 4 = 2,315 QPS

Server Estimation:
- Each server handles 500 QPS
- Required servers: 2,315 / 500 = 5 servers
- With redundancy (2x): 10 servers
- With growth buffer (50%): 15 servers
```

#### Database Sizing

**Relational Database Example:**

```
Transaction System:
- 1M transactions per day
- 1KB per transaction
- 7-year retention

Data growth: 1M × 1KB × 365 × 7 = 2.5TB
With indexes (3x): 7.5TB
With replication (3x): 22.5TB

Memory requirements:
- Working set: 20% of data = 1.5TB
- Buffer pool: 50% of working set = 750GB
```

------

## Performance Testing

### Performance Testing Methodology

#### Types of Performance Testing

**Load Testing:**

- **Purpose**: Verify system performance under expected load
- **Duration**: Extended periods (hours to days)
- **User pattern**: Gradual ramp-up to target load
- **Goal**: Establish baseline performance metrics

**Stress Testing:**

- **Purpose**: Find system breaking point
- **Duration**: Short bursts with high intensity
- **User pattern**: Rapid scaling beyond normal capacity
- **Goal**: Identify maximum capacity and failure modes

**Spike Testing:**

- **Purpose**: Test response to sudden traffic increases
- **Duration**: Short spikes followed by normal load
- **User pattern**: Sudden traffic surges
- **Goal**: Verify auto-scaling and recovery capabilities

**Volume Testing:**

- **Purpose**: Test with large amounts of data
- **Duration**: Varies based on data processing time
- **Data pattern**: Large datasets or high data velocity
- **Goal**: Verify data handling and storage performance

#### Performance Testing Strategy

**Test Planning Framework:**

1. **Define objectives**: What are you trying to measure?
2. **Identify scenarios**: Real-world usage patterns
3. **Set acceptance criteria**: Performance thresholds
4. **Design test data**: Representative datasets
5. **Plan test environment**: Production-like setup
6. **Execute tests**: Systematic testing approach
7. **Analyze results**: Bottleneck identification
8. **Optimize and retest**: Iterative improvement

### Key Performance Metrics

#### Response Time Metrics

**Latency Measurements:**

- **Mean response time**: Average across all requests
- **Median (P50)**: 50th percentile response time
- **P95**: 95% of requests complete within this time
- **P99**: 99% of requests complete within this time
- **P99.9**: 99.9% of requests complete within this time

**Why Percentiles Matter:**

- Mean can be misleading due to outliers
- P95/P99 represent user experience more accurately
- Tail latencies impact user satisfaction significantly

#### Throughput Metrics

**Capacity Measurements:**

- **Requests per second (RPS)**: Web application throughput
- **Transactions per second (TPS)**: Database throughput
- **Messages per second**: Queue processing rate
- **Concurrent users**: Simultaneous active users
- **Connection capacity**: Maximum concurrent connections

#### Resource Utilization Metrics

**System Resources:**

- **CPU utilization**: Percentage of processing capacity used
- **Memory usage**: RAM consumption patterns
- **Disk I/O**: Read/write operations and throughput
- **Network bandwidth**: Data transfer rates
- **Database connections**: Connection pool utilization

### Performance Testing Tools and Approaches

#### Load Testing Tools

**Open Source Tools:**

- **Apache JMeter**: Comprehensive GUI-based testing
- **Artillery**: Modern, lightweight load testing
- **k6**: Developer-centric performance testing
- **Gatling**: High-performance load testing

**Cloud-Based Solutions:**

- **AWS Load Testing**: Distributed load generation
- **Azure Load Testing**: Managed load testing service
- **Google Cloud Load Testing**: Scalable performance testing
- **BlazeMeter**: SaaS load testing platform

#### Test Environment Considerations

**Environment Parity:**

- **Hardware**: Similar CPU, memory, storage specifications
- **Network**: Comparable bandwidth and latency
- **Data**: Production-like datasets and volumes
- **Configuration**: Matching application settings
- **Dependencies**: Same external service integrations

**Isolation Strategies:**

- **Dedicated test environment**: Separate from production
- **Production testing**: Limited scope with monitoring
- **Synthetic monitoring**: Continuous performance checks
- **Shadow testing**: Duplicate traffic for testing

### Interpreting Performance Test Results

#### Bottleneck Identification

**Common Bottleneck Patterns:**

**CPU Bottleneck:**

- High CPU utilization (>80%)
- Response time increases with load
- Queue depth grows
- Thread pool exhaustion

**Memory Bottleneck:**

- High memory usage
- Frequent garbage collection
- Memory allocation failures
- Swapping activity

**Database Bottleneck:**

- High database response times
- Connection pool exhaustion
- Lock contention
- Query timeout errors

**Network Bottleneck:**

- High network utilization
- Connection timeout errors
- Bandwidth saturation
- Geographic latency issues

#### Performance Analysis Framework

**Result Analysis Steps:**

1. **Baseline establishment**: Normal operation metrics
2. **Load correlation**: How metrics change with load
3. **Bottleneck identification**: Resource constraints
4. **Scalability assessment**: Linear vs sub-linear scaling
5. **Breaking point analysis**: System failure modes

------

## Resource Estimation

### Hardware Resource Planning

#### Server Sizing Methodology

**Capacity Planning Formula:**

```
Required Capacity = Peak Load × Safety Factor / Utilization Target

Where:
- Peak Load: Maximum expected demand
- Safety Factor: 1.2-2.0 (20-100% buffer)
- Utilization Target: 60-80% (avoid resource saturation)
```

**Example Calculation:**

```
Web Server Sizing:
- Peak QPS: 10,000
- Server capacity: 1,000 QPS at 70% CPU
- Safety factor: 1.5

Required servers = 10,000 × 1.5 / 1,000 = 15 servers
```

#### Resource Allocation Guidelines

**CPU Allocation:**

- **Web servers**: 2-4 cores per 1,000 QPS
- **Application servers**: 4-8 cores per 1,000 TPS
- **Database servers**: 8-16 cores + high clock speed
- **Cache servers**: 4-8 cores + high memory

**Memory Allocation:**

- **Web servers**: 4-8GB base + 1-2GB per 1,000 QPS
- **Application servers**: 8-16GB base + 2-4GB per 1,000 TPS
- **Database servers**: 50-80% of data working set
- **Cache servers**: 90% dedicated to cache storage

### Cloud Resource Planning

#### Cloud Sizing Strategy

**Instance Type Selection:**

- **Compute-optimized**: CPU-intensive workloads
- **Memory-optimized**: In-memory databases, caches
- **Storage-optimized**: Data-intensive applications
- **General purpose**: Balanced workloads
- **GPU instances**: Machine learning, graphics processing

**Auto-scaling Configuration:**

```
Auto-scaling Parameters:
- Minimum instances: Handle baseline load
- Maximum instances: Cost and capacity limits
- Scale-up threshold: 70% resource utilization
- Scale-down threshold: 30% resource utilization
- Cooldown period: 5-10 minutes
```

#### Cost Optimization Strategies

**Reserved Capacity:**

- **Reserved instances**: 1-3 year commitments for predictable workloads
- **Spot instances**: Discounted capacity for fault-tolerant workloads
- **Savings plans**: Flexible pricing for consistent usage

**Resource Optimization:**

- **Right-sizing**: Match instance size to actual usage
- **Schedule-based scaling**: Scale down during off-hours
- **Geographic optimization**: Use cheaper regions when possible
- **Storage tiering**: Move old data to cheaper storage

### Growth Forecasting

#### Traffic Growth Modeling

**Growth Prediction Methods:**

**Linear Growth:**

```
Future Traffic = Current Traffic + (Growth Rate × Time Period)

Example:
Current: 1,000 QPS
Growth: 20% annually
Year 2: 1,000 + (1,000 × 0.20) = 1,200 QPS
```

**Exponential Growth:**

```
Future Traffic = Current Traffic × (1 + Growth Rate)^Time Period

Example:
Current: 1,000 QPS
Growth: 50% annually
Year 2: 1,000 × (1.5)^1 = 1,500 QPS
Year 3: 1,000 × (1.5)^2 = 2,250 QPS
```

**S-Curve Growth:**

- Initial slow growth
- Rapid acceleration phase
- Eventual plateau

#### Business-Driven Capacity Planning

**User Growth Correlation:**

```
Infrastructure Scaling:
- User growth: 100% increase
- Data growth: 100-150% increase (user-generated content)
- Compute growth: 80-120% increase (efficiency improvements)
- Storage growth: 120-200% increase (data retention)
```

**Feature Impact Assessment:**

- **New features**: 10-50% increase in resource usage
- **Mobile app launch**: 2-5x increase in API calls
- **Real-time features**: 3-10x increase in infrastructure needs
- **Analytics features**: 2-5x increase in data processing

### Risk Assessment and Planning

#### Capacity Risk Management

**Risk Categories:**

- **Demand risk**: Higher than expected traffic
- **Performance risk**: Lower than expected system performance
- **Availability risk**: Infrastructure failures
- **Cost risk**: Budget overruns
- **Timeline risk**: Delayed capacity deployment

**Mitigation Strategies:**

- **Over-provisioning**: 20-50% capacity buffer
- **Multi-region deployment**: Geographic redundancy
- **Auto-scaling**: Automatic capacity adjustment
- **Performance monitoring**: Early warning systems
- **Disaster recovery**: Backup capacity plans

#### Capacity Planning Timeline

**Planning Horizons:**

- **Immediate (0-3 months)**: Tactical adjustments
- **Short-term (3-12 months)**: Planned growth accommodation
- **Medium-term (1-3 years)**: Strategic infrastructure investments
- **Long-term (3+ years)**: Architectural evolution planning

**Review Cycles:**

- **Weekly**: Operational metrics review
- **Monthly**: Capacity utilization analysis
- **Quarterly**: Growth trend assessment
- **Annually**: Strategic capacity planning

------

## Monitoring and Continuous Improvement

### Capacity Monitoring Framework

#### Key Performance Indicators

**Utilization Metrics:**

- **Peak utilization**: Maximum resource usage during peak hours
- **Average utilization**: Mean resource usage over time
- **Utilization trending**: Growth patterns and seasonality
- **Efficiency ratios**: Useful work per resource unit

**Capacity Metrics:**

- **Headroom**: Available capacity before constraints
- **Time to exhaustion**: When current capacity will be insufficient
- **Scaling effectiveness**: How well additional resources improve performance
- **Cost per unit**: Resource cost efficiency

### Capacity Planning Best Practices

#### Planning Principles

**Proactive Approach:**

- Monitor leading indicators
- Plan capacity 3-6 months ahead
- Build in safety margins
- Test capacity limits regularly

**Data-Driven Decisions:**

- Use historical trends for projections
- Consider business seasonality
- Account for marketing campaigns
- Include feature rollout impacts

**Cost Optimization:**

- Balance performance and cost
- Use tiered storage strategies
- Optimize for actual usage patterns
- Regular capacity rightsizing

------

## Key Takeaways

1. **Start with business requirements**: Understand growth expectations and user patterns
2. **Use historical data**: Base projections on actual usage trends
3. **Plan for peaks**: Design for maximum expected load, not average
4. **Build in safety margins**: Include 20-50% capacity buffers
5. **Monitor continuously**: Track utilization and adjust plans regularly
6. **Test capacity limits**: Validate assumptions through performance testing
7. **Consider cost trade-offs**: Balance performance needs with budget constraints

### Common Planning Mistakes

- **Under-estimating growth**: Using linear projections for exponential growth
- **Ignoring seasonality**: Not accounting for traffic patterns
- **Over-optimizing**: Planning for unrealistic efficiency levels
- **Single point analysis**: Not considering system-wide bottlenecks
- **Static planning**: Not updating plans as requirements change

> **Remember**: Capacity planning is an ongoing process that requires regular review and adjustment. Start with conservative estimates, validate with testing, and refine based on actual usage patterns and business growth.