# Service Communication Patterns

## Synchronous vs Asynchronous Communication

### Synchronous Communication

The client sends a request and waits for a response before proceeding. The calling service blocks until it receives a response from the called service.

**Characteristics:**

- **Blocking**: Caller waits for response
- **Direct coupling**: Services communicate directly
- **Immediate response**: Results available instantly
- **Simple flow**: Request-response pattern

**When to Use Synchronous Communication:**

- **Real-time requirements**: User needs immediate feedback (login, payment processing)
- **Data consistency**: Need immediate confirmation of state changes
- **Simple workflows**: Linear process flows
- **User-facing operations**: Web requests, mobile app interactions

**Advantages:**

- Simple to understand and implement
- Immediate error handling
- Strong consistency guarantees
- Easy debugging and tracing

**Disadvantages:**

- **Cascading failures**: If service B is down, service A fails
- **Performance bottlenecks**: Slowest service determines overall speed
- **Resource blocking**: Threads/connections held during wait
- **Tight coupling**: Services become interdependent

**Examples:**

```
User Login Flow (Synchronous):
Client → API Gateway → Auth Service → User Database
     ← (wait) ← (wait) ← (response)
```

### Asynchronous Communication

The client sends a request and continues processing without waiting for a response. Communication happens through message queues, events, or callbacks.

**Characteristics:**

- **Non-blocking**: Caller doesn't wait for response
- **Loose coupling**: Services communicate via intermediaries
- **Eventual consistency**: Results available later
- **Complex flow**: Fire-and-forget or publish-subscribe

**When to Use Asynchronous Communication:**

- **Background processing**: Email sending, report generation, data processing
- **High throughput**: Need to handle many requests quickly
- **Independent workflows**: Services can work autonomously
- **Event-driven systems**: Reacting to state changes

**Advantages:**

- **Fault tolerance**: Service failures don't cascade
- **Better performance**: No blocking, higher throughput
- **Scalability**: Services can scale independently
- **Resilience**: System continues working with partial failures

**Disadvantages:**

- **Complexity**: Harder to implement and debug
- **Eventual consistency**: Data might be temporarily inconsistent
- **Error handling**: More complex failure scenarios
- **Monitoring**: Harder to trace request flows

**Examples:**

```
Order Processing (Asynchronous):
Order Service → Message Queue → [Inventory, Payment, Shipping Services]
                              ↓
                         Email Service (sends confirmation)
```

**Hybrid Approach:** Most real systems use both patterns strategically:

- **Synchronous for critical path**: User-facing operations requiring immediate response
- **Asynchronous for side effects**: Logging, notifications, analytics, background processing

## Service Discovery Mechanisms

### What is Service Discovery?

The process of automatically detecting and locating services in a distributed system. As services scale up/down and move between hosts, discovery mechanisms help services find and communicate with each other.

**The Problem:**

- Dynamic environments: Services change IP addresses, ports
- Load balancing: Multiple instances of same service
- Health monitoring: Avoid routing to unhealthy instances
- Configuration management: Services need to find dependencies

### Client-Side Discovery

The client is responsible for determining available service instances and load balancing.

**How it works:**

1. Service instances register with service registry
2. Client queries registry for available instances
3. Client selects instance and makes direct request
4. Client handles load balancing logic

**Advantages:**

- **Simple architecture**: No additional network hops
- **Client control**: Can implement custom load balancing
- **Performance**: Direct communication after discovery

**Disadvantages:**

- **Client complexity**: Each client needs discovery logic
- **Coupling**: Clients coupled to discovery mechanism
- **Language dependency**: Discovery logic per programming language

**Examples:** Eureka + Ribbon (Netflix), Consul + client libraries

### Server-Side Discovery

A load balancer or API gateway handles service discovery and routing.

**How it works:**

1. Service instances register with service registry
2. Client makes request to load balancer
3. Load balancer queries registry and selects instance
4. Load balancer forwards request to selected instance

**Advantages:**

- **Client simplicity**: Clients unaware of discovery complexity
- **Centralized logic**: Load balancing and routing in one place
- **Language agnostic**: Works with any client technology

**Disadvantages:**

- **Additional network hop**: Slight latency increase
- **Single point of failure**: Load balancer becomes critical
- **Operational complexity**: Need to manage load balancer

**Examples:** AWS ELB + ECS, Kubernetes Services, Istio Service Mesh

### Service Registry Patterns

#### Self-Registration Pattern

Services register themselves with the registry.

```
Service Startup:
1. Service starts up
2. Service registers itself with registry
3. Service sends periodic heartbeats
4. Service deregisters on shutdown
```

**Pros:** Simple, services control their lifecycle **Cons:** Service becomes coupled to registry

#### Third-Party Registration Pattern

A separate system component handles registration.

```
Deployment Process:
1. Deployment system starts service
2. Deployment system registers service with registry
3. Health checker monitors service health
4. Registry automatically removes unhealthy services
```

**Pros:** Services decoupled from registry **Cons:** Additional infrastructure complexity

### Service Discovery Technologies

| Technology         | Type              | Key Features                              |
| ------------------ | ----------------- | ----------------------------------------- |
| **Consul**         | External Registry | Health checks, KV store, multi-datacenter |
| **Eureka**         | External Registry | Self-preservation, AWS integration        |
| **etcd**           | External Registry | Distributed, strong consistency           |
| **Kubernetes DNS** | Platform-native   | Built-in service discovery                |
| **AWS ELB**        | Platform-native   | Managed load balancing                    |
| **Istio**          | Service Mesh      | Advanced traffic management               |

## Circuit Breaker Pattern

### What is Circuit Breaker?

A design pattern that prevents cascading failures in distributed systems by monitoring service calls and "opening" when failure rates exceed thresholds, similar to electrical circuit breakers.

**The Problem:** When a service becomes slow or unresponsive, calling services can:

- Waste resources waiting for timeouts
- Cascade failures upstream
- Create resource exhaustion
- Reduce overall system availability

### Circuit Breaker States

#### Closed State (Normal Operation)

- All requests pass through to the service
- Monitor success/failure rates
- Track response times

#### Open State (Failing Service)

- Requests fail fast without calling the service
- Return cached data or default response
- Periodically attempt to "half-open"

#### Half-Open State (Testing Recovery)

- Allow limited number of test requests
- If requests succeed → Close circuit
- If requests fail → Open circuit again

### Circuit Breaker Configuration

**Metrics Tracked:**

- **Failure Rate**: Percentage of failed requests
- **Response Time**: Average/percentile response times
- **Request Volume**: Minimum requests before evaluation
- **Time Window**: Period for calculating metrics

**Configuration Parameters:**

```
Failure Threshold: 50% failure rate
Request Volume: Minimum 20 requests
Time Window: 10 seconds
Open Timeout: 30 seconds (before half-open)
Half-Open Max Calls: 3 test requests
```

### Benefits

- **Fail Fast**: Quick failure response instead of timeouts
- **Resource Protection**: Prevent resource exhaustion
- **Cascade Prevention**: Stop failure propagation
- **Graceful Degradation**: Return fallback responses
- **Automatic Recovery**: Self-healing when service recovers

### Fallback Strategies

- **Cached Data**: Return last known good response
- **Default Values**: Return sensible defaults
- **Alternative Service**: Route to backup service
- **Graceful Degradation**: Reduce functionality but keep working

### Circuit Breaker + Retry Pattern

```
Request Flow:
1. Check circuit breaker state
2. If closed → make request with retries
3. If request fails → record failure
4. If failure threshold exceeded → open circuit
5. If open → return fallback immediately
```

## Request/Response vs Event-Driven

### Request/Response Pattern

Direct communication where one service makes a request to another and waits for a response.

**Characteristics:**

- **Synchronous**: Immediate response expected
- **Point-to-point**: Direct service-to-service communication
- **Stateful interaction**: Request context maintained
- **Strong coupling**: Services need to know about each other

**When to Use Request/Response:**

- **Data queries**: Getting user profiles, product information
- **Transactions**: Payment processing, order placement
- **Real-time operations**: Authentication, validation
- **Simple workflows**: Linear process flows

**Advantages:**

- **Immediate feedback**: Results available instantly
- **Simple debugging**: Clear request/response traces
- **Strong consistency**: Immediate state confirmation
- **Easy testing**: Straightforward integration tests

**Disadvantages:**

- **Tight coupling**: Services become interdependent
- **Cascading failures**: Failures propagate upstream
- **Performance bottlenecks**: Limited by slowest service
- **Scalability limits**: Synchronous processing constraints

### Event-Driven Pattern

Services communicate by producing and consuming events without direct coupling.

**Characteristics:**

- **Asynchronous**: Events processed independently
- **Publish-subscribe**: One-to-many communication
- **Stateless events**: Self-contained event information
- **Loose coupling**: Services only know about events

**Event Types:**

- **Domain Events**: Business state changes (OrderCreated, UserRegistered)
- **Integration Events**: Cross-service communication events
- **System Events**: Infrastructure events (ServiceStarted, HealthCheck)

**When to Use Event-Driven:**

- **Business workflows**: Order processing, user registration flows
- **Data synchronization**: Keeping read models updated
- **Audit logging**: Recording all system changes
- **Real-time notifications**: User alerts, system monitoring

**Advantages:**

- **Loose coupling**: Services don't need to know about each other
- **Scalability**: Services can scale independently
- **Resilience**: System continues working with partial failures
- **Extensibility**: Easy to add new event consumers

**Disadvantages:**

- **Eventual consistency**: Data might be temporarily inconsistent
- **Complex debugging**: Hard to trace event flows
- **Event ordering**: Challenges with event sequence
- **Error handling**: Complex failure scenarios

### Event Sourcing vs Event-Driven

- **Event Sourcing**: Store events as the primary source of truth
- **Event-Driven**: Use events for communication between services

### Choosing Communication Patterns

| Scenario                     | Best Pattern     | Reason                                       |
| ---------------------------- | ---------------- | -------------------------------------------- |
| User login                   | Request/Response | Need immediate authentication result         |
| Send welcome email           | Event-Driven     | Can happen asynchronously after registration |
| Payment processing           | Request/Response | Need immediate confirmation                  |
| Update recommendation engine | Event-Driven     | Can process user behavior events later       |
| Get user profile             | Request/Response | Need current data immediately                |
| Audit logging                | Event-Driven     | Background process, doesn't block user       |

### Hybrid Architecture Example

```
E-commerce Order Flow:
1. User places order (Request/Response)
   → Order Service validates and creates order
   → Returns order confirmation to user

2. Order created event published (Event-Driven)
   → Inventory Service: Reserve items
   → Payment Service: Process payment
   → Shipping Service: Prepare shipment
   → Email Service: Send confirmation
   → Analytics Service: Update metrics
```

### Event-Driven Implementation Patterns

#### Event Bus/Message Broker

Central message routing system (RabbitMQ, Apache Kafka, AWS EventBridge)

- **Pros**: Centralized, reliable, feature-rich
- **Cons**: Additional infrastructure, potential bottleneck

#### Direct Event Publishing

Services publish events directly to interested consumers

- **Pros**: Simple, no additional infrastructure
- **Cons**: Tight coupling, harder to manage

#### Event Store

Dedicated storage for events with replay capabilities

- **Pros**: Event history, debugging, replay functionality
- **Cons**: Complex to implement, storage overhead

## Best Practices for Service Communication

1. **Design for failure**: Assume services will fail
2. **Implement timeouts**: Don't wait indefinitely
3. **Use bulkheads**: Isolate failure domains
4. **Monitor everything**: Track all communication patterns
5. **Plan for scale**: Design for growth from the beginning
6. **Choose patterns wisely**: Match pattern to use case requirements