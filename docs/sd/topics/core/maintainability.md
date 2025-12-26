# Maintainability

*The ability of designing systems which are easy to maintain, in terms of servicing the components and maintain the code.*

## Monitoring & Observability

Observability is about building systems that can explain themselves. While monitoring tells you **what** is happening, observability helps you understand **why** it's happening.

Three Pillars of Observability

- Logs : Discrete events with timestamps and context
- Metrics : Numerical measurements over time
- Traces : Request journey across distributed systems

Key Principles of designing a system which we can debug easily is to instrument everything, Have data with rich cardinality for better insights. Balance Details with storage/processing costs, Data logged should be useful and actionable.

![](assets/Pasted%20image%2020251227002803.png)
### Logs

Logs are immutable, timestamped records of events that happened in your system. They provide detailed context about system behavior and are essential for debugging and auditing.

Log Levels and when to use them

- ERROR : System errors, exceptions, failed operations
- WARN : Potential problems, degraded performance  
- INFO : Important business events, state changes
- DEBUG : Detailed execution flow, variable values
- TRACE : Very detailed execution path (rarely used in production)

Generally its preferred to have Structured Logging (json), as its much easier to search and filter, consistent format. Better integration with log analysis tools like *loki*

#### What to Log ?

This could be thought as a guideline and not strict rule for logging

- Always Log
    - Auth events : failures, denied access, login/logout
    - Business Transactions : Orders, payments & critical workflows
    - Errors and exceptions
    - External API calls
    - Performance Milestones like slow queries and timeouts
- Sometimes
    - User actions
    - Data changes : CRUD operations (redact the PII data)
    - System Events : Deployments and Configuration Changes
    - Resource Usage : Memory spikes, CPU usage
- Never Log
    - Password or Secrets : even hashed passwords
    - PIIs without consent : due to compliance reasons
    - High-frequency events : health-checks and cache hits/misses
    - Redundant Information

#### Log Aggregation Strategies

![](assets/Pasted%20image%2020251227002702.png)

There are multiple ways to ship logs like directly shipping log files (incrementally) (could be pull/push based), Async Queue based.

#### Logging Best Practices

Best Practices include :

- Correlation-ids should be included in every log record, easier to trace the log record.
- Contextual Logging to include relevant information
- Log Sampling for High Volume application


```json
{
  "trace_id": "abc123",      // Unique per request across all services
  "span_id": "def456",       // Unique per service operation
  "user_id": "user789",      // Business context
  "session_id": "sess101"    // Session context
}
```


```python
# Bad: Hard to correlate logs
logger.info("Processing payment")
logger.info("Validating card")
logger.error("Payment failed")

# Good: Rich context in every log
logger.info("Processing payment", {
    "user_id": "user123", 
    "order_id": "order456",
    "amount": 99.99,
    "payment_method": "credit_card"
})

# Sampling based on business importance
def should_log(event_type, user_tier):
    if event_type == "error":
        return True  # Always log errors
    elif user_tier == "premium":
        return True  # Always log premium user events
    elif event_type == "page_view":
        return random.random() < 0.01  # 1% sampling for page views
    else:
        return random.random() < 0.1   # 10% sampling for other events
```

### Metrics and Alerting

Metrics are numerical measurements of your system over time. They provide quantitative insights into system behavior and performance trends.

Types of Metrics to trace

- Business Metrics : Like revenue, user engagement, conversions, growth, etc.
- Application Metrics : Throughput, Latency, Error Rates, Availability, etc.
- Infrastructure Metrics : Resource Usage, Capacity, Performance
- Custom Business Logic Metrics : Background job queue size, cache performance, feature usage, data quality.

Metrics Collection Patterns

- Push Model : StatsD, CloudWatch : Application sends metrics to collector
- Pull Model (prometheus) : Collector scrapes metrics from application endpoints e.g. /metrics endpoint.

Key Metrics to Track

- The Golden Signals (google SRE) : Traffic, Latency, Errors, and Saturation
- The RED Method (for Services) : Rate, Errors, and Duration
- The USE Method (for Resources) : Utilization, Saturation, Errors

#### Alerting

![](assets/Pasted%20image%2020251227004012.png)

There are 3 types of Alerts

- Threshold-based Alerts : e.g. CPU Usage > 80% for 5 minutes → WARNING
- Anomaly based Alerts : e.g. Request volume deviates > 3 standard deviations from weekly pattern
- Composite Alerts : e.g. High Error Rate AND High Latency AND Low Throughput = Service Degradation

Another important concept is Alert Fatigue, Be very sure about the level of alerting, if you alert people too often they will start ignoring the alerts.

Few simple strategies to get rid of Alert Fatigue are

- Alert Tuning Strategies : Setup appropriate Thresholds, Time-based Rules, Alert Grouping and Auto-resolution.
- Alert Escalation : Alert should be escalated through its Lifecycle.

Example of Alert Escalation

```
Alert Lifecycle:
1. Alert fires ~ Notification sent
2. 15 minutes no ack ~ Escalate to team lead
3. 30 minutes no ack ~ Escalate to manager  
4. 60 minutes no ack ~ Escalate to director
5. Alert resolves ~ Send resolution notification
```

### Distributed Tracing

Distributed tracing tracks requests as they flow through multiple services, providing visibility into complex distributed system interactions.

Core Concepts

- **Trace**: Complete journey of a request across all services
- **Span**: Individual operation within a trace (API call, database query)
- **Tags**: Key-value metadata attached to spans
- **Baggage**: Data carried through the entire trace

![](assets/Pasted%20image%2020251227005226.png)

What should we trace ?

- Service Boundaries : HTTP Requests, Database Operations, External API calls, Cache operations and *Message Queue* operations.
- Internal Operations : Business Logic, Expensive Operation, Async Operations, Resource Operations, etc.

Traces are very useful in performance testing, as they help us identify slow components.

## Health Checks

Already Discussed here : [Link](load_balancers.md)

## Monitoring Architecture Patterns

### Centralized Monitoring vs Distributed Monitoring

![](assets/Pasted%20image%2020251227010156.png)

![](assets/Pasted%20image%2020251227010421.png)

### Monitoring Data Pipelines

Real-Time Pipelines

![](assets/Pasted%20image%2020251227010647.png)

Batch Processing Pipeline

![](assets/Pasted%20image%2020251227010804.png)
