# Fault Tolerance Patterns

*The ability of a system to continue operating properly in the event of the failure of some of its components.*

## Overview

Fault tolerance ensures your system remains operational even when individual components fail. The goal is not to prevent failures (which are inevitable) but to handle them gracefully.

#### Types of Failures

- **Hardware Failures**: Server crashes, disk failures, network outages
- **Software Failures**: Bugs, memory leaks, deadlocks
- **Human Errors**: Misconfigurations, accidental deletions
- **Network Failures**: Partitions, latency spikes, packet loss
- **External Dependencies**: Third-party service outages

#### Key Principles

1. **Assume Failures Will Happen**: Design for failure from the start
2. **Fail Fast**: Detect failures quickly and respond appropriately
3. **Isolate Failures**: Prevent cascade failures across the system
4. **Graceful Degradation**: Maintain core functionality when possible
5. **Monitor and Alert**: Continuous monitoring for early detection

------

## Redundancy & Replication

#### What is Redundancy?

Redundancy involves having multiple instances of critical components so that if one fails, others can take over. It's the foundation of fault tolerance.

#### Types of Redundancy

#### 1. Active Redundancy (Hot Standby)

- Multiple instances run simultaneously and share the load
- **Benefits**: No downtime during failures, better performance distribution
- **Drawbacks**: Higher resource costs, complexity in maintaining consistency
- **Use Cases**: Web servers, API gateways, microservices

**Key Implementation Points**:

```python
# Load balancer maintains list of healthy servers
servers = [server1, server2, server3]
healthy_servers = [s for s in servers if s.health_check()]
selected_server = round_robin(healthy_servers)
```

#### 2 Passive Redundancy (Cold Standby)

- Backup instances are activated only when primary fails
- **Benefits**: Lower resource costs, simpler consistency model
- **Drawbacks**: Failover time, potential data loss during transition
- **Use Cases**: Database masters, critical single-instance services

**Failover Process**:

1. Detect primary failure
2. Promote standby to primary
3. Redirect traffic to new primary
4. Update DNS/load balancer configuration

### Data Replication Strategies

#### 1. Synchronous Replication

- All replicas updated before acknowledging write
- **Pros**: Strong consistency, no data loss
- **Cons**: Higher latency, reduced availability if replicas fail
- **Best for**: Financial systems, critical data

#### 2. Asynchronous Replication

- Primary acknowledges write immediately, replication happens in background
- **Pros**: Better performance, higher availability
- **Cons**: Potential data loss, eventual consistency
- **Best for**: Social media, content management, analytics

### Replication Patterns

- **Master-Slave**: One write node, multiple read replicas
- **Master-Master**: Multiple write nodes (requires conflict resolution)
- **Quorum-based**: Majority consensus for reads/writes

------

## Graceful Degradation

### What is Graceful Degradation?

The ability to maintain limited functionality when some components fail, rather than failing completely.

### Implementation Strategies

#### 1. Feature Toggles

Enable/disable features based on system health.

**Example Decision Matrix**:

```
Feature: Recommendations
├── ML Service Available? → Full personalized recommendations
├── Cache Available? → Basic cached recommendations  
├── Database Available? → Popular items only
└── All Failed → Empty recommendations (don't break page)
```

**Implementation Pattern**:

```python
def get_recommendations(user_id):
    if ml_service.is_healthy():
        return ml_service.get_recommendations(user_id)
    elif cache.is_available():
        return cache.get_popular_items()
    else:
        return []  # Graceful fallback
```

#### 2. Circuit Breaker Pattern

Prevents cascading failures by stopping calls to failing services.

**States**:

- **Closed**: Normal operation, calls pass through
- **Open**: Service failing, reject calls immediately
- **Half-Open**: Testing if service recovered

**Key Metrics**:

- Failure threshold (e.g., 5 failures in 60 seconds)
- Recovery timeout (e.g., 30 seconds before retry)
- Success threshold for closing (e.g., 3 successful calls)

#### 3. Fallback Mechanisms

Provide alternative functionality when primary services fail.

**Fallback Hierarchy Example**:

1. **Primary**: Real-time user recommendations
2. **Secondary**: Cached recommendations from last session
3. **Tertiary**: Popular items in user's category
4. **Final**: Generic trending items

------

## Bulkhead Isolation

### What is Bulkhead Isolation?

Isolates critical resources to prevent failures in one part from cascading to other parts. Named after ship compartments that prevent flooding.

### Implementation Strategies

#### 1. Resource Pool Isolation

Separate resource pools for different operations.

**Example Architecture**:

```
Application Server
├── Critical Operations Pool (5 threads) → Payments, Auth
├── User Operations Pool (8 threads) → Profile, Search  
├── Analytics Pool (3 threads) → Reports, Metrics
└── Batch Operations Pool (2 threads) → Background jobs
```

**Benefits**:

- Heavy analytics workload can't impact payment processing
- Background jobs don't affect user-facing operations
- Each pool can be tuned for its specific workload

#### 2 Database Connection Isolation

**Pattern**:

```
Database Connection Pools
├── OLTP Pool (10 connections) → User transactions
├── Analytics Pool (5 connections) → Heavy queries
└── Reporting Pool (3 connections) → Background reports
```

#### 3 Service Isolation

- **Microservices**: Each service has its own resources
- **Containerization**: Resource limits per container
- **Process Isolation**: Separate processes for different functions

### Isolation Levels

1. **Thread Level**: Thread pools for different operations
2. **Process Level**: Separate processes for critical vs non-critical
3. **Machine Level**: Dedicated servers for different workloads
4. **Network Level**: Separate network segments
5. **Data Center Level**: Geographic isolation

------

## Timeout & Retry Mechanisms

### What are Timeout & Retry Mechanisms?

Prevent systems from waiting indefinitely and provide resilience against transient failures.

### Timeout Strategies

#### Fixed Timeout

Simple timeout with predetermined duration.

```python
# Connection timeout: 5s, Read timeout: 30s
response = requests.get(url, timeout=(5, 30))
```

#### Adaptive Timeout

Adjusts based on historical response times.

- Monitor 95th percentile response time
- Set timeout to 1.5x the 95th percentile
- Adjust periodically based on recent performance

#### Progressive Timeout

Increase timeout for retry attempts.

```
Attempt 1: 5 seconds
Attempt 2: 10 seconds  
Attempt 3: 20 seconds
```

### Retry Strategies

#### Linear Backoff

Fixed delay between retries.

```
Retry 1: Wait 1 second
Retry 2: Wait 1 second
Retry 3: Wait 1 second
```

#### Exponential Backoff

Increase delay exponentially.

```python
delay = initial_delay * (backoff_multiplier ** attempt_number)
# Example: 1s, 2s, 4s, 8s, 16s...
```

#### Exponential Backoff with Jitter

Add randomness to prevent thundering herd.

```python
delay = base_delay * (2 ** attempt) + random(0, 1)
```

#### Retry with Circuit Breaker

```python
def resilient_call(func, *args):
    try:
        return circuit_breaker.call(func, *args)
    except CircuitOpenException:
        return fallback_response()
```

### Retry Best Practices

**What to Retry**:

- ✅ Network timeouts
- ✅ HTTP 5xx errors
- ✅ Connection refused
- ✅ Temporary rate limits (429)
- ❌ Authentication failures (401)
- ❌ Bad requests (400)
- ❌ Not found (404)

**Configuration Guidelines**:

```
Service Type         | Max Retries | Initial Delay | Max Delay
---------------------|-------------|---------------|----------
Critical (Payments)  |     3       |     100ms     |    1s
User-facing (Search) |     2       |     200ms     |    2s  
Background (Reports) |     5       |     1s        |   30s
External APIs        |     3       |     500ms     |   10s
```

### Advanced Patterns

#### Dead Letter Queue (DLQ)

Failed messages after all retries go to DLQ for manual investigation.

#### Retry Storm Prevention

```python
# Use circuit breakers with retries
# Add jitter to prevent synchronized retries
# Implement backpressure when overwhelmed
```

#### Bulkhead + Retry

```python
def isolated_retry_call(pool_name, func, *args):
    pool = get_resource_pool(pool_name)
    return pool.execute_with_retry(func, *args)
```

------

## Monitoring and Observability

### Key Metrics to Track

**Availability Metrics**:

- Success rate (SLA compliance)
- Error rate by type
- Mean Time To Recovery (MTTR)
- Mean Time Between Failures (MTBF)

**Performance Metrics**:

- Response time percentiles (50th, 95th, 99th)
- Throughput (requests per second)
- Resource utilization

**Fault Tolerance Metrics**:

- Circuit breaker state changes
- Retry attempt counts
- Failover events
- Fallback usage frequency

### Alerting Strategy

**Alert Levels**:

1. **Critical**: Immediate response required (pager duty)
   - Service completely down
   - Data corruption detected
   - Security breach
2. **Warning**: Investigation needed (within hours)
   - High error rate (>5%)
   - Performance degradation
   - Circuit breaker opened
3. **Info**: Awareness (review during business hours)
   - Retry rate increase
   - Fallback usage increase
   - Resource utilization changes

### Health Check Design

**Multi-Level Health Checks**:

```
Shallow Health Check (< 100ms)
├── Service process running?
├── Basic connectivity?
└── Memory/CPU within limits?

Deep Health Check (< 5s)  
├── Database connectivity?
├── External service calls?
└── Critical workflows working?
```

------

## Choosing the Right Patterns

### Decision Matrix

| Requirement           | Redundancy          | Graceful Degradation | Bulkhead            | Timeout/Retry       |
| --------------------- | ------------------- | -------------------- | ------------------- | ------------------- |
| **High Availability** | ✅ Active            | ✅ Feature Toggles    | ✅ Service Isolation | ✅ Circuit Breaker   |
| **Performance**       | ✅ Load Distribution | ✅ Caching Fallbacks  | ✅ Resource Pools    | ✅ Adaptive Timeouts |
| **Cost Optimization** | ⚠️ Passive Only      | ✅ Smart Degradation  | ⚠️ Shared Resources  | ✅ Efficient Retries |
| **Consistency**       | ✅ Sync Replication  | ❌ May Compromise     | ✅ Isolated Txns     | ⚠️ Idempotent Only   |

### Pattern Combinations

**E-commerce Checkout**:

- Redundancy: Multiple payment processors
- Degradation: Fallback to basic checkout flow
- Bulkhead: Separate pools for payment vs catalog
- Retry: Exponential backoff for payment calls

**Social Media Feed**:

- Redundancy: CDN + multiple data centers
- Degradation: Cached feed → Popular posts → Empty feed
- Bulkhead: Separate analytics from user feeds
- Timeout: Quick timeouts for real-time features

**Financial Trading**:

- Redundancy: Synchronous replication
- Degradation: Read-only mode if writes fail
- Bulkhead: Strict isolation between trading engines
- Retry: Minimal retries with manual intervention

------

## Conclusion

### Key Takeaways

1. **Layer Multiple Patterns**: Combine redundancy, graceful degradation, bulkhead isolation, and timeout/retry
2. **Design for Your SLA**: Choose patterns based on availability requirements
3. **Monitor Everything**: Comprehensive observability enables quick failure detection
4. **Test Failure Scenarios**: Regular chaos engineering and disaster recovery testing
5. **Document Procedures**: Clear runbooks for incident response

### Implementation Checklist

- Identify single points of failure
- Implement appropriate redundancy levels
- Design fallback mechanisms for critical features
- Isolate resources by criticality and workload type
- Configure timeouts and retries for all external calls
- Set up comprehensive monitoring and alerting
- Create incident response procedures
- Regular failure testing and drills

Remember: Fault tolerance comes with complexity and cost trade-offs. The level should match your system's reliability requirements and business needs.