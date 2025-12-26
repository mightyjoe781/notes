# Reliability

*Reliability* refers to the probability that a system performs its intended function without failure over a specified period under specified conditions.

Key Components of Reliability are

- Fault-Tolerance
- Graceful-Degradation
- Fast Failure
- Recovery

Failures could be of multiple types as well

- Transient Failure : Temporary network issues, resource exhaustion
- Persistent Failure : Service outages, configuration errors
- Cascading Failure : Failures that propagate through system components
- Silent Failures : Errors that occur without obvious symptoms

To evaluate reliability of a system we often use metrics like availability, MTTR (mean-time to recovery), MTBF (mean time between failures), Error rate, etc.

Following notes describe the process of building fault-tolerant system, and designing in such a way that it can recover from failures and do not create inconsistent or unreliable behavior.

## Fault-Tolerance

The ability of a system to continue operating properly in the event of the failure of some of its components. The goal is not to prevent failures ( which are inevitable) but to handle them gracefully.

Source of failures could be Hardware, Software, Human, Network Failures, External Dependencies, etc.

Steps to design a fault-tolerant system

- Assume failures will happen : design for failure from the start
- Fail Fast : Detect failures quickly and respond appropriately
- Isolate Failures : Prevent cascade failures across the system
- Graceful Degradation : maintain core functionality when possible
- Monitor & Alert : continuous monitoring for early detection

## Redundancy & Replication

Redundancy involves having multiple instances of critical components so that if one fails, others can take over. It's the foundation of fault tolerance.

Types of Redundancy

- Active Redundancy (Hot Standby)
    - Multiple instances run simultaneously and share the load.
    - Use Cases: Web servers, API Gateways, MicroServices
- Passive Redundancy (Cold Standby)
    - Backup instances are activated only when primary fails
    - Use Cases: Database Master, critical single-instance services
    - NOTE: Be careful of Failover time, and there could be a potential data loss during transition

To manage the failover scenario, whenever we detect any kind of failures in a primary server, we promote the secondary to primary and redirect traffic to new primary server.

There are two types of replication : synchronous and asynchronous Replication.

Following are most simple Replication Topologies

- Master-Slave: One write node, multiple read replicas
- Master-Master: Multiple write nodes (requires conflict resolution)
- Quorum-based: Majority consensus for reads/writes

## Graceful Degradation

The ability to maintain limited functionality when some components fail, rather than failing completely.

Implementation Strategies

- Feature Toggle : Enable/Disable features based on system health
- Circuit Breaker : Prevents cascading failures by stopping calls to failing services.
- FallBack Mechanism : Provide alternative functionality when primary services fail (e.g. default feed)

### Circuit Breaker

The Circuit Breaker pattern prevents cascading failures by monitoring service calls and "opening" the circuit when failures exceed a threshold, allowing the system to fail fast and recover gracefully.

Circuit could be any of the following states

- CLOSED State (Normal Operations) : all requests are processed normally.
- OPEN State (Circuit Breaker is activated) : blocks all request fail immediately calling downstream service
- Half-Open State (Testing Recovery) : a small number of requests are passed through to validate working.

Circuit Breaker could be implemented to work on following ways using configuration parameters

- Failure Thresholds : Failure rate threshold, request volume threshold, time window, consecutive failures, etc.
- Timing Parameters : Timeout duration, half-open success threshold, half-open request limit, reset timeout

### Fallback Strategies

There are two ways to fallback in case of failure, either recover by adding more instances and try to serve default responses (like default recommendation/feed) to your user.

- Circuit Breaker Decision Flow:
    - Check circuit state
    - If CLOSE -> call primary service
    - If OPEN -> Return fallback response
    - If HALF-OPEN -> call primary service with monitioring
- Fallback Hierarchy :
    - Try primary service
    - If fails -> Try secondary service
    - If fails -> Return cached data
    - If no cache -> return default response

#### User Experience Patterns

- Transparent Fallback : User doesn't notice degraded service
- Notification fallback: Inform user of limited functionality
- Retry invitation: Suggest user retry operation later
- Alternative action: Suggest alternative user actions

### Summary

Circuit Breaker Decision Flow:
1. Check circuit state
2. If CLOSED → Call primary service
3. If OPEN → Return fallback response
4. If HALF-OPEN → Call primary service with monitoring

Fallback Hierarchy:
1. Try primary service
2. If fails → Try secondary service
3. If fails → Return cached data
4. If no cache → Return default response

## Bulkhead Isolation

Isolates critical resources to prevent failures in one part from cascading to other parts. Named after ship compartments that prevent flooding.

Implementation Strategies

- Resource Pool Isolation : Separate resource pools for different operations. Ex- critical components have more resources (CPU, RAM, etc) assigned.
- Database Connection Isolation : Using connection pools with more capacity for transaction while a simple reporting tools might not need more connection in the pool.
- Service Isolation
    - Microservices: Each service has its own resources
    - Containerization: Resource limits per container
    - Process Isolation: Separate processes for different functions

## Timeout & Retry Mechanisms

Prevent systems from waiting indefinitely and provide resilience against transient failures.

Timeout Strategies

- Fixed Timeout : Simple timeout with predetermined duration.
- Adaptive Timeout : Adjusts based on historical response times, using like 95th percentile response time, etc.
- Progressive Timeout : Increase timeout for retry attempts, i.e. 5s, 10s, 20s, etc

Retry Strategies

- Linear Backoff : Fixed delay between retries.
- Exponential Backoff : Increase delay exponentially.
- Exponential Backoff with Jitter : Add randomness to prevent thundering herd.
- Retry with a Circuit Breaker


```python
# linear backoff
delay = 2

# exponential backoff
delay = initial_delay * (backoff_multiplier ** attempt_number)

# exponential backoff with jitter
delay = base_delay * (2 ** attempt) + random(0, 1)

# using circuit-breaker call to fallback to default repsonse
def resilient_call(func, *args):
    try:
        return circuit_breaker.call(func, *args)
    except CircuitOpenException:
        return fallback_response()

```

### Retry Best Practices

NOTE: Always retrying every single failure doesn't make sense, we should retry errors which are transient and might disappear after some time.

Ex - Auth Failure (401), Bad Request (400), Not-Found (404) all are unrecoverable failure, so we should not retry them.

Errors like Network Timeouts, HTTP 5xx errors, Connection refused, Temporary Rate limits (249), etc should be retried.

### Advanced Patterns

#### Dead Letter Queue (DLQ)

Failed messages after all retries go to DLQ for manual investigation, regarding failures.

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

## Availability

High Availability (HA) is about designing systems that remain operational despite failures. It's measured by uptime percentages and directly impacts user experience and business revenue.

Its closely related to Reliability in terms, highly-available system is by design reliable.

Availability Levels (SLA Standard)

- 99% (Basic): 3.65 days downtime/year - Acceptable for internal tools
- 99.9% (Standard): 8.77 hours downtime/year - Typical web applications
- 99.95% (High): 4.38 hours downtime/year - E-commerce, SaaS platforms
- 99.99% (Very High): 52.6 minutes downtime/year - Banking, critical systems
- 99.999% (Extreme): 5.26 minutes downtime/year - Emergency services, trading

Key Principles for highly available solution are Eliminating Single points of Failures (redundancy) and detect failures quickly and recover from failures.

### Active-Passive

One primary system handles all traffic while backup systems remain on standby, ready to take over during failures.

Types of Active-Passive

- Cold Standby : Backup systems are powered off or minimal state
- Warm Standby : Backup systems running but not processing traffic
- Hot Standby : Backup systems fully operational, synchronized

Although it seems that it is resource wasteful but that provides benefits of Simple Architecture and Data Consistency, Cost is associated with active instances only.
### Active-Active Configuration

Multiple systems simultaneously handle traffic and share the load, providing both high availability and improved performance.


Types of Active-Active

- Shared Nothing Architecture
- Shared Database Architecture
- Geographic Active-Active

A bit complicated to maintain, eventually consistency reads are natural, Write conflict appear often and Distributed Transactions are complex to co-ordinate. We will need Sticky session to ensure no conflicts.

### Geographic Distribution

Deploying systems across multiple geographic locations to improve availability, performance, and disaster resilience.

There could be multiple strategies to improve resilience using

- Multi-Region Deployments
- CDN
- DNS-Based Geographic Routing
- Data Replication Across Regions : Be aware cross-region data restriction and compliance

Challenges in Geographic Distribution

- Network Partitions : requires Quorum System, Witness/Arbiter, Graceful Degradation, etc.
- Data Consistency Across Region : Synchronous Replication (strong consistency) will result in higher latency, but eventual consistency will have low latency.

### Disaster Recovery

The process of preparing for and recovering from catastrophic events that could cause extended system outages.

Metrics to judge Disaster Recovery are RTO (Recovery Time Objective) and RPO (Recovery point objective)

RTO : Maximum acceptable downtime

- **Tier 1**: RTO < 1 hour (Critical systems)
- **Tier 2**: RTO < 4 hours (Important systems)
- **Tier 3**: RTO < 24 hours (Standard systems)
- **Tier 4**: RTO < 72 hours (Non-critical systems)

RPO : Maximum acceptable data loss

- **RPO = 0**: No data loss acceptable (sync replication)
- **RPO < 15 min**: Minimal data loss (frequent backups)
- **RPO < 1 hour**: Acceptable for most businesses
- **RPO < 24 hours**: Acceptable for non-critical data

There are multiple Disaster Recovery Strategies

- Cold Site Recovery : Backup facility with basic infrastructure but no active systems.
    - RTO : 24-72 hrs
    - RPO : 4-24 hrs
- Warm Site Recovery : Backup facility with partial infrastructure and recent data.
    - RTO : 2-12 hrs
    - RPO : 1-4 hrs
- Hot Site Recovery : Fully operational backup facility with real-time or near-real-time data.
    - RTO : 15min-2hrs
    - RPO : 0-15min

#### Backup Strategies

The 3-2-1 backup rule

- 3 copies of critical data
- 2 different storage media types
- 1 offsite/cloud backup

There are different types of Backups & Schedule

- Full Backup (Weekly)
- Incremental Backup (daily)
- Differential Backup


Many companies do disaster recovery practices based on calendar schedule

- Tabletop Exercise (monthly)
- Partial Testing (quarterly)
- Full DR Testing (Annually)

## Choosing the Right Patterns

Following are some decisions based on popular patterns.

**E-commerce Checkout**:

- Redundancy: Multiple payment processors
- Degradation: Fallback to basic checkout flow
- Bulkhead: Separate pools for payment vs catalog
- Retry: Exponential backoff for payment calls

**Social Media Feed**:

- Redundancy: CDN + multiple data centers
- Degradation: Cached feed -> Popular posts -> Empty feed
- Bulkhead: Separate analytics from user feeds
- Timeout: Quick timeouts for real-time features

**Financial Trading**:

- Redundancy: Synchronous replication
- Degradation: Read-only mode if writes fail
- Bulkhead: Strict isolation between trading engines
- Retry: Minimal retries with manual intervention

Remember: Fault tolerance comes with complexity and cost trade-offs. The level should match your system's reliability requirements and business needs.