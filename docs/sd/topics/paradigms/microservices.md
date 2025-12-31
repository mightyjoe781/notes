# Microservices Architecture

Microservices architecture decomposes applications into small, autonomous services that are organized around business capabilities. Each service is owned by a small team and can be developed, deployed, and scaled independently.

#### Key Characteristics

- **Business Capability Focus**: Services organized around business functions
- **Decentralized**: Independent teams, databases, and deployments
- **Technology Agnostic**: Each service can use different tech stacks
- **Failure Isolation**: Service failures don't cascade across the system
- **Evolutionary Design**: Services can evolve independently

#### When Microservices Make Sense

- Large organizations (> 20 developers) with multiple teams
- Complex domains with distinct business capabilities
- Independent scaling requirements across features
- Technology diversity needs
- High deployment frequency requirements
- Strong DevOps culture and operational expertise

#### When to Avoid Microservices

- Small teams (< 10 developers)
- Simple, well-defined domains
- Limited operational expertise
- Strong consistency requirements across all operations
- Prototype or MVP development
- Monolith-first approach often recommended

------

## Service Decomposition Strategies

#### What is Service Decomposition?

The process of breaking down a monolithic application or designing a new system as independent services, each responsible for specific business capabilities.

### Decomposition Approaches

#### Domain-Driven Design (DDD)

**Bounded Contexts** as service boundaries:

E-commerce Domain Decomposition:

- User Management (Identity & Access)
    - User registration/authentication
    - Profile management
    - Access control
- Product Catalog (Product Information)
    - Product information
    - Categories and search
    - Inventory tracking
- Order Management (Order Processing)
    - Shopping cart
    - Order placement
    - Order tracking
- Payment Processing (Financial Transactions)
    - Payment methods
    - Transaction processing
    - Refunds and billing
- Shipping & Fulfillment (Logistics)
    - Shipping calculation
    - Delivery tracking
    - Warehouse management

#### Business Capability Decomposition

Identify Core Business Capabilities:

- Customer-facing capabilities
    - Product discovery
    - Order placement
    - Customer support
- Operational capabilities  
    - Inventory management
    - Order fulfillment
    - Supplier management
- Support capabilities
    - Analytics and reporting
    - Notification services
    - Audit and compliance

#### Data Ownership Decomposition

```python
# Each service owns its data completely
User Service:
├── users table
├── user_profiles table
└── user_preferences table

Product Service:
├── products table
├── categories table
└── product_reviews table

Order Service:
├── orders table
├── order_items table
└── order_status_history table

# No shared database access between services
```

### Decomposition Patterns

#### Strangler Fig Pattern

Gradually replace monolith functionality:

Legacy Monolith Decomposition Timeline:

Month 1-2: Extract User Service

- Route `/api/users/*` to new User Service
- Keep authentication in monolith temporarily
- Migrate user data to separate database

Month 3-4: Extract Product Service 

- Route `/api/products/*` to new Product Service
- Handle product data migration
- Update order service integration

Month 5-6: Extract Order Service

- Most complex due to dependencies
- Implement saga pattern for order processing
- Update all service integrations

#### Branch by Abstraction

```python
# Create abstraction layer during decomposition
class PaymentProcessor:
    def process_payment(self, payment_data):
        if feature_flag.is_enabled("new_payment_service"):
            return self.new_payment_service.process(payment_data)
        else:
            return self.legacy_payment_module.process(payment_data)
```

#### Database Per Service

Service Database Patterns:

- User Service → PostgreSQL (relational user data)
- Product Service → MongoDB (flexible product catalog)
- Order Service → PostgreSQL (transactional data)
- Analytics Service → ClickHouse (time-series data)
- Notification Service → Redis (temporary message storage)

### Service Sizing Guidelines

#### Microservice Size Principles

Size Indicators:

- Team Size: 2-8 developers (Amazon's "two-pizza team")
- Codebase: 10k-50k lines of code
- Development Time: Rewrite in 2-4 weeks
- Cognitive Load: One person can understand entire service
- Business Capability: Single, well-defined responsibility

#### Anti-patterns to Avoid

Too Small (Nano-services):

- Single function per service
- Excessive network overhead
- Operational complexity exceeds benefits
- Distributed monolith behavior

Too Large (Mini-monoliths):

- Multiple business capabilities
- Multiple teams working on same service
- Difficulty in independent deployment
- Complex internal architecture

### Decomposition Best Practices

#### Start with Monolith

Recommended Evolution Path:

1. Start with well-structured monolith
2. Identify service boundaries through usage patterns
3. Extract services incrementally (highest value first)
4. Learn and improve with each extraction
5. Avoid "big bang" decomposition

#### Service Boundary Identification

Coupling Indicators

- High Cohesion : Functions That change together, shared data structures, related business rules
- Low Coupling : Independent Business Capabilities, Different Change Frequencies, Minimal Data Sharing

Look for natural Boundaries :

- Different teams owning different features
- Different scaling requirements
- Different technology needs
- Different data models

------

## Data Consistency Across Services

In microservices, each service owns its data, making traditional ACID transactions across services impossible. This creates challenges for maintaining consistency across the system.

### Consistency Models

#### Eventual Consistency

Order Processing Example:

1. Order Service creates order (status: PENDING)
2. Payment Service processes payment (async)
3. Order Service updates order (status: CONFIRMED)
4. Inventory Service reserves items (async)
5. Order Service updates order (status: RESERVED)

Timeline:

T0: Order created (PENDING)
T1: Payment processed (but order still PENDING)
T2: Order updated (CONFIRMED)  
T3: Inventory reserved (RESERVED)

System is eventually consistent, not immediately consistent

#### Strong Consistency Patterns

Generally 2 Phase Commit (2PC) - generally avoided in Microservices

- Blocking protocol (coordinator failure blocks all)
- Network partitions cause issues
- Performance overhead
- Not suitable for microservices

### Saga Pattern

Manages distributed transactions as a sequence of local transactions, with compensating actions for rollback.

#### Choreography-based Saga


In Choreography Based Saga Co-ordination among microservices is decentralized, Each service knows the next step and the communication is event driven. Services react to events they receive.
#### Orchestration-based Saga

In Orchestration Based Saga Co-ordination among microservices is centralized and done by Saga Orchestrator which manages the flow. Central Decision Making does the explicit state managements.
### Event Sourcing Pattern

Store all changes as a sequence of events, allowing reconstruction of current state.
### Data Synchronization Patterns

#### Event-Driven Data Sync

Data Synchronization Flow:

1. User Service updates user profile
2. Publishes UserProfileUpdated event  
3. Order Service listens and updates local user cache
4. Analytics Service listens and updates user dimension
5. Recommendation Service listens and refreshes user model

Benefits:

- Near real-time synchronization
- Loose coupling between services
- Audit trail of all changes
- Support for multiple consumers

#### Polling-based Sync

Periodic Data Synchronization, every 5 minutes, get the latest updates and update the local cache/database.

Trade Offs

- Pro : Simple, Predictable
- Cons : Latency, Resource Usage, Potential for Conflicts

### Distributed Transaction Alternatives

#### Outbox Pattern

The **Outbox Pattern** is a reliability pattern used in **distributed systems** to ensure **atomicity between database state changes and event/message publishing**.

Instead of publishing messages directly to a message broker inside a business transaction, the application **writes events to an outbox table in the same database transaction** as the domain data. A **separate process** later reads these outbox records and publishes them to the messaging system.

#### Command Query Responsibility Segregation (CQRS)

CQRS Pattern:

- Command Side (Writes)
    - Handles business operations
    - Updates normalized data store
    - Publishes events
- Query Side (Reads)  
    - Handles read requests
    - Uses denormalized views
    - Optimized for queries

Benefits:

-  Independent scaling of reads/writes
- Optimized data models for different use cases
- Event sourcing compatibility
- Improved performance

------

## Inter-service Communication Patterns

Microservices communicate through network calls, requiring careful consideration of communication patterns, protocols, and failure handling.

### Synchronous Communication

- HTTP/REST APIs
- gRPC Communication
- GraphQL Federation
### Asynchronous Communication

- Message Queues
- Event Streaming

### Communication Patterns

- Request-Response Pattern
- Fire and Forget Pattern
- Publish-Subscribe Pattern
### Communication Best Practices

#### API Versioning Strategies

- URL-based versioning: `/api/v1/users` vs `/api/v2/users`
- Header-based versioning: `API-Version: 2` in request headers
- Semantic versioning: For backward compatibility guarantees
- Deprecation timeline: Clear communication about version lifecycle

#### Circuit Breaker for Service Calls

Prevents cascading failures by monitoring service health:

- **Closed State**: Normal operation, requests pass through
- **Open State**: Service failing, requests rejected immediately
- **Half-Open State**: Testing if service recovered

Key Configuration:

- Failure threshold (e.g., 5 consecutive failures)
- Timeout period (e.g., 60 seconds before retry)
- Success threshold for closing (e.g., 3 successful calls)

#### Timeout and Retry Strategies

**Timeout Configuration**:

- Connection timeout: 5 seconds
- Read timeout: 30 seconds for normal operations
- Different timeouts for different service types

**Retry Patterns**:

- **Exponential backoff**: 1s, 2s, 4s, 8s intervals
- **Retry conditions**: Only retry on transient failures (5xx errors, timeouts)
- **Maximum attempts**: Typically 3-5 retries
- **Jitter**: Add randomness to prevent thundering herd

------

## Service Mesh Architecture

A dedicated infrastructure layer that handles service-to-service communication, providing features like load balancing, service discovery, security, and observability without requiring changes to application code.

### Service Mesh Components

#### Data Plane

![](assets/Pasted%20image%2020251231211048.png)

Sidecar Proxy Responsibilities:

- Load balancing
- Health checking  
- Circuit breaking
- Retries and timeouts
- TLS termination
- Metrics collection
- Traffic routing

#### Control Plane

Service Mesh Control Plane:

- Service Discovery (Registry of all services)
- Configuration Management (Routing rules, policies)
- Certificate Management (mTLS certificates)
- Policy Enforcement (Access control, rate limiting)
- Telemetry Collection (Metrics, traces, logs)

### Service Mesh Benefits

#### Traffic Management

```yaml
# Example: Istio traffic management
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  http:
  - match:
    - headers:
        user-type:
          exact: premium
    route:
    - destination:
        host: user-service
        subset: v2
      weight: 100
  - route:
    - destination:
        host: user-service  
        subset: v1
      weight: 90
    - destination:
        host: user-service
        subset: v2
      weight: 10
```

#### Security Features

```yaml
# Automatic mTLS between services
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT  # Require mTLS for all communication

# Authorization policies
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: order-service-policy
spec:
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/api-gateway"]
  - to:
    - operation:
        methods: ["POST", "GET"]
```

#### Observability

Service Mesh Observability:

- Automatic metrics collection (latency, throughput, errors)
- Distributed tracing (request path across services)
- Access logs (all service-to-service communication)
- Service topology visualization

### Service Mesh Patterns

#### Circuit Breaker Pattern

```yaml
# Istio circuit breaker configuration
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  trafficPolicy:
    outlierDetection:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 50
```

#### Canary Deployments

```yaml
# Progressive traffic shifting
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: canary-deployment
spec:
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: user-service
        subset: canary
  - route:
    - destination:
        host: user-service
        subset: stable
      weight: 95
    - destination:
        host: user-service
        subset: canary
      weight: 5
```

### Service Mesh Trade-offs

#### Benefits

- **Zero-code observability**: Automatic metrics and tracing
- **Security by default**: mTLS and policy enforcement
- **Traffic management**: Advanced routing and load balancing
- **Operational consistency**: Standardized patterns across services

#### Drawbacks

- **Complexity**: Additional infrastructure to manage
- **Performance overhead**: Proxy adds latency (1-10ms)
- **Learning curve**: New concepts and configuration
- **Vendor lock-in**: Platform-specific features

#### When to Use Service Mesh

Consider Service Mesh When:

- 10+ microservices
- Complex networking requirements
- Strong security requirements
- Need advanced traffic management
- Multiple teams/languages

Avoid Service Mesh When:

- Simple microservices architecture
- Performance is critical (latency sensitive)
- Limited operational expertise
- Cost is a major concern

------

## Microservices Implementation Best Practices

### Service Design Principles

#### Single Responsibility Principle

**Good Service Design**:

- Focused on one business capability
- Clear, well-defined responsibility
- Minimal external dependencies
- Easy to understand and maintain

**Poor Service Design (Avoid)**:

- Multiple unrelated responsibilities
- Complex internal architecture
- Many external dependencies
- Requires multiple teams to maintain

#### API-First Design

```yaml
# OpenAPI specification first, then implementation
openapi: 3.0.0
info:
  title: User Service API
  version: 1.0.0
paths:
  /users/{userId}:
    get:
      summary: Get user by ID
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
```

### Data Management

#### Database Per Service

Service Data Ownership:

- User Service → PostgreSQL (user data)
- Product Service → MongoDB (product catalog)  
- Order Service → PostgreSQL (transactional data)
- Analytics Service → ClickHouse (events)
- Search Service → Elasticsearch (indexed data)

No cross-service database access allowed

#### Event-Driven Data Synchronization

When data changes in one service, events are published for other services to consume:

**Event Publishing**: Service publishes events when data changes

- UserProfileUpdated, OrderCreated, PaymentProcessed
- Include necessary data in event payload
- Use consistent event schemas across organization

**Event Consumption**: Other services subscribe to relevant events

- Update local caches or read models
- Trigger business processes
- Maintain data consistency across services

### Testing Strategies

#### Testing Pyramid for Microservices

![](assets/Pasted%20image%2020251231210835.png)

#### Contract Testing

Ensures service compatibility without running all services:

**Consumer-Driven Contracts**:

- Consumer defines expected API behavior
- Provider verifies it can meet the contract
- Catches breaking changes early
- Tools: Pact, Spring Cloud Contract

**Benefits**:

- Independent service development
- Faster feedback on breaking changes
- Better API design collaboration
- Reduced integration testing overhead

### Deployment and Operations

#### Independent Deployments

```yaml
# Each service has its own CI/CD pipeline
# user-service-pipeline.yml
stages:
  - test:
      - unit_tests
      - integration_tests
      - contract_tests
  - build:
      - docker_build
      - security_scan
  - deploy:
      - staging_deployment
      - automated_tests
      - production_deployment
      - health_checks

# Independent versioning
services:
  - user-service: v2.3.1
  - product-service: v1.8.2  
  - order-service: v3.1.0
  - payment-service: v1.5.4
```

#### Service Discovery Patterns

**Service Registry**: Central location where services register and discover each other

- Services register their location (host, port, health check URL)
- Clients query registry to find service instances
- Health checking removes unhealthy instances
- Examples: Consul, Eureka, etcd

**Client-Side Discovery**: Client queries registry and chooses instance

- Lower latency (no extra network hop)
- Client controls load balancing
- More complex client implementation

**Server-Side Discovery**: Load balancer queries registry

- Simpler client implementation
- Centralized load balancing logic
- Additional network hop

### Monitoring and Observability

#### Distributed Tracing Implementation

**Trace Context Propagation**:

- Extract trace context from incoming requests
- Start new span for current service operation
- Inject trace context into outgoing requests
- Use correlation IDs to track requests across services

**Key Benefits**:

- Visualize request flow across services
- Identify performance bottlenecks
- Debug distributed system issues
- Monitor service dependencies

#### Service Health Monitoring

**Comprehensive Health Checks**:

- **Shallow checks**: Basic connectivity and resource availability
- **Deep checks**: External dependency health and functionality
- **Business logic checks**: End-to-end workflow validation

**Health Check Levels**:

- `/health/live`: Liveness probe (restart if failing)
- `/health/ready`: Readiness probe (remove from load balancer)
- `/health/detailed`: Comprehensive status for debugging

**Monitoring Strategy**:

- Different timeouts for different check types
- Graceful degradation when dependencies are unhealthy
- Clear status reporting (healthy/degraded/unhealthy)

------

## Decision Framework

### Architecture Decision Matrix

| Factor                     | Monolith         | Modular Monolith   | Microservices    |
| -------------------------- | ---------------- | ------------------ | ---------------- |
| **Team Size**              | 1-10 devs        | 10-20 devs         | 20+ devs         |
| **Domain Complexity**      | Simple           | Moderate           | Complex          |
| **Deployment Frequency**   | Weekly/Monthly   | Daily              | Multiple/day     |
| **Scaling Requirements**   | Uniform          | Moderate variation | High variation   |
| **Technology Diversity**   | Single stack     | Limited diversity  | High diversity   |
| **Operational Complexity** | Low              | Medium             | High             |
| **Development Speed**      | Fast (initially) | Medium             | Slow (initially) |
| **Fault Isolation**        | None             | Limited            | High             |
| **Data Consistency**       | Strong           | Strong             | Eventual         |
|                            |                  |                    |                  |

### Common Anti-patterns

#### Distributed Monolith

Anti-pattern: Distributed Monolith

- Services that must be deployed together
- Synchronous communication for everything
- Shared database across services
- High coupling between services
- No independent scaling

Symptoms:

- Cannot deploy services independently
- Cascading failures across services
- Long deployment pipelines
- High network latency
- Complex debugging across services

#### Microservice Anarchy

Anti-pattern: Microservice Anarchy

- No consistent patterns across services
- Each team chooses different technologies
- No standard monitoring or logging
- Inconsistent API patterns
- No shared infrastructure

Problems

- Operational nightmare
- Difficult to hire and train
- No reusable components
- Inconsistent user experience
- High maintenance overhead

------

## Conclusion

1. **Microservices solve organizational problems**: Most beneficial for large, multi-team organizations
2. **Start with monolith**: Build domain knowledge before decomposing
3. **Conway's Law applies**: Service boundaries should match team boundaries
4. **Operational complexity**: Requires significant investment in tooling and processes
5. **Data consistency trade-offs**: Embrace eventual consistency and compensating patterns