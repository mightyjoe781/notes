# Data Patterns

*Comprehensive guide to data patterns including Event Sourcing, CQRS, Saga Pattern, and Database per Service.*

## Overview

Data patterns are architectural patterns that address data management challenges in distributed systems, providing strategies for data consistency, scalability, and reliability across multiple services and databases.

### Data Pattern Fundamentals

**Key Data Challenges:**

- **Data consistency**: Maintaining consistency across distributed data stores
- **Data isolation**: Preventing services from interfering with each other's data
- **Transaction management**: Handling transactions across multiple services
- **Data evolution**: Managing schema changes and data migration
- **Query optimization**: Optimizing read and write operations

**Pattern Benefits:**

- **Scalability**: Enable independent scaling of data storage
- **Reliability**: Improve fault tolerance and recovery capabilities
- **Flexibility**: Support diverse data storage and access patterns
- **Maintainability**: Simplify data management and evolution
- **Performance**: Optimize for specific use cases and access patterns

**Trade-offs:**

- **Complexity**: Increased system complexity and operational overhead
- **Consistency**: Trade strong consistency for availability and performance
- **Data duplication**: Potential for data redundancy across services
- **Integration overhead**: Additional effort for cross-service data access

------

## Event Sourcing

### Event Sourcing Fundamentals

Event Sourcing is a pattern where all changes to application state are stored as a sequence of events, rather than storing just the current state. The current state is derived by replaying events from the event store.

### Core Concepts

#### Events as Source of Truth

**Event Characteristics:**

- **Immutable**: Events never change once written
- **Append-only**: New events are added, existing events never modified
- **Ordered**: Events have a defined sequence or timestamp
- **Complete**: Events contain all necessary information for state reconstruction
- **Auditable**: Full history of all changes preserved

**Event Structure:**

```
Event Example:
{
  "eventId": "uuid-1234",
  "eventType": "OrderPlaced",
  "aggregateId": "order-5678",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": 1,
  "data": {
    "customerId": "customer-999",
    "items": [
      {"productId": "product-123", "quantity": 2, "price": 50.00}
    ],
    "totalAmount": 100.00
  },
  "metadata": {
    "userId": "user-456",
    "correlationId": "correlation-789"
  }
}
```

#### Event Store

**Event Store Responsibilities:**

- **Event persistence**: Durable storage of events
- **Event retrieval**: Retrieve events by aggregate or stream
- **Event ordering**: Maintain event sequence integrity
- **Concurrency control**: Handle concurrent writes to same aggregate
- **Snapshotting**: Optimize state reconstruction with snapshots

**Event Store Implementation:**

- **Specialized databases**: EventStore, Apache Kafka, AWS EventBridge
- **Relational databases**: PostgreSQL, MySQL with event table design
- **NoSQL databases**: MongoDB, DynamoDB with document-based events
- **Distributed logs**: Apache Kafka, Amazon Kinesis for event streaming

### Event Sourcing Implementation

#### Aggregate Design

**Domain Aggregates:**

```
Order Aggregate Example:
class Order {
    private String orderId;
    private String customerId;
    private OrderStatus status;
    private List<OrderItem> items;
    private BigDecimal totalAmount;
    
    // Business methods that generate events
    public void placeOrder(List<OrderItem> items) {
        // Validate business rules
        OrderPlacedEvent event = new OrderPlacedEvent(orderId, customerId, items);
        applyEvent(event);
    }
    
    public void cancelOrder() {
        if (status != OrderStatus.PLACED) {
            throw new IllegalStateException("Cannot cancel order in current state");
        }
        OrderCancelledEvent event = new OrderCancelledEvent(orderId);
        applyEvent(event);
    }
    
    // Event application methods
    private void applyEvent(OrderPlacedEvent event) {
        this.customerId = event.getCustomerId();
        this.items = event.getItems();
        this.totalAmount = calculateTotal(items);
        this.status = OrderStatus.PLACED;
    }
}
```

**Event Application:**

- **Event handlers**: Methods that apply events to aggregate state
- **State reconstruction**: Replay events to rebuild current state
- **Business logic**: Encapsulate business rules in aggregate methods
- **Event validation**: Ensure events are valid before application

#### Command and Event Flow

**Command Processing:**

```
Event Sourcing Flow:
1. Receive command (PlaceOrder)
2. Load aggregate from events
3. Execute business logic
4. Generate domain events
5. Persist events to event store
6. Publish events for other services
7. Return success/failure response

Benefits:
- Complete audit trail
- Time travel capabilities
- Event-driven architecture support
- Natural replication and backup
```

### Event Sourcing Patterns

#### Snapshotting

**Snapshot Strategy:**

- **Performance optimization**: Avoid replaying thousands of events
- **Snapshot frequency**: Balance performance vs storage cost
- **Snapshot versioning**: Handle aggregate schema evolution
- **Incremental snapshots**: Store only changed state portions

**Implementation:**

```
Snapshot Example:
{
  "aggregateId": "order-5678",
  "aggregateType": "Order", 
  "version": 100,
  "timestamp": "2024-01-15T15:30:00Z",
  "data": {
    "customerId": "customer-999",
    "status": "SHIPPED",
    "items": [...],
    "totalAmount": 150.00
  }
}

State Reconstruction:
1. Load latest snapshot (version 100)
2. Load events after snapshot (versions 101-105)
3. Apply events to snapshot state
4. Current state at version 105
```

#### Event Upcasting

**Schema Evolution:**

- **Event versioning**: Handle changes to event structure
- **Backward compatibility**: Support reading old event versions
- **Event transformation**: Convert old events to new format
- **Migration strategies**: Gradual migration vs big-bang conversion

**Upcasting Example:**

```
Event Schema Evolution:
Version 1: OrderPlacedEvent {orderId, items}
Version 2: OrderPlacedEvent {orderId, customerId, items, metadata}

Upcasting Logic:
if (event.version == 1) {
    // Add default customerId for old events
    event.customerId = "unknown";
    event.metadata = {};
    event.version = 2;
}
```

### Event Sourcing Benefits and Challenges

#### Benefits

**Audit and Compliance:**

- **Complete history**: Every change tracked and auditable
- **Regulatory compliance**: Meet audit requirements naturally
- **Debugging**: Replay events to reproduce issues
- **Analytics**: Rich data for business intelligence

**Scalability and Performance:**

- **Read/write separation**: Optimize reads and writes independently
- **Event streaming**: Natural fit for event-driven architectures
- **Horizontal scaling**: Partition events by aggregate ID
- **Caching**: Cache current state while maintaining event history

#### Challenges

**Complexity:**

- **Learning curve**: Requires understanding of event-driven concepts
- **Event design**: Careful design of event schema and evolution
- **Debugging complexity**: Tracing through event sequences
- **Testing complexity**: Testing event sequences and state transitions

**Performance Considerations:**

- **Event replay cost**: Performance impact of rebuilding state
- **Storage growth**: Events accumulate over time
- **Query complexity**: Complex queries require read models
- **Eventual consistency**: Asynchronous processing implications

### Advanced Event Sourcing Patterns

#### Event Sourcing with CQRS

**Integrated Pattern:**

- **Command side**: Events stored in event store
- **Query side**: Read models built from events
- **Event projection**: Transform events into query-optimized views
- **Eventual consistency**: Read models eventually consistent with events

#### Distributed Event Sourcing

**Multi-Service Events:**

- **Event correlation**: Track events across service boundaries
- **Saga orchestration**: Coordinate long-running transactions
- **Event choreography**: Services react to events independently
- **Event ordering**: Handle ordering across distributed systems

------

## CQRS (Command Query Responsibility Segregation)

### CQRS Fundamentals

CQRS separates read and write operations into different models, allowing optimization of each for their specific use cases and enabling independent scaling and evolution.

### CQRS Architecture

#### Command and Query Separation

**Command Side (Write Model):**

- **Purpose**: Handle commands that change system state
- **Optimization**: Optimized for writes, business logic, and consistency
- **Structure**: Domain model with aggregates and business rules
- **Storage**: Normalized data optimized for transactional integrity
- **Consistency**: Strong consistency and immediate validation

**Query Side (Read Model):**

- **Purpose**: Handle queries that read system state
- **Optimization**: Optimized for reads, performance, and specific use cases
- **Structure**: Denormalized views tailored for specific queries
- **Storage**: Query-optimized data structures and indexes
- **Consistency**: Eventually consistent with command side

#### Data Flow

**CQRS Flow:**

```
CQRS Architecture:
Commands → Command Handlers → Domain Model → Event Store
                                    ↓
Events → Event Handlers → Read Model Builders → Query Models
                                    ↓
Queries → Query Handlers → Read Models → Query Results

Synchronization:
- Commands modify write model
- Events published from write model
- Read models updated from events
- Queries served from read models
```

### CQRS Implementation Patterns

#### Simple CQRS

**Shared Database:**

```
Simple CQRS Pattern:
Application
├── Command Side
│   ├── Command Handlers
│   ├── Domain Model
│   └── Write Database
└── Query Side
    ├── Query Handlers
    ├── Read Models
    └── Read Database (same as write)

Benefits:
- Simple to implement
- Single database to manage
- Easier consistency management
- Lower infrastructure complexity
```

#### CQRS with Separate Databases

**Database Segregation:**

```
Segregated CQRS Pattern:
Commands → Write Database (Normalized)
    ↓ (Events/Change Streams)
Queries ← Read Database (Denormalized)

Write Database:
- Optimized for transactions
- Normalized schema
- Strong consistency
- ACID properties

Read Database:
- Optimized for queries
- Denormalized views
- Eventually consistent
- Read replicas/caching
```

### Read Model Patterns

#### Materialized Views

**Query-Specific Views:**

```
Customer Read Models:
├── CustomerSummaryView (Basic info for lists)
├── CustomerDetailView (Complete customer data)
├── CustomerOrderHistoryView (Order history with items)
├── CustomerAnalyticsView (Aggregated statistics)
└── CustomerSearchView (Search-optimized structure)

Each view optimized for specific queries:
- Different data structures
- Specialized indexes
- Denormalized data
- Cached computations
```

**View Materialization:**

- **Real-time**: Update views immediately when events occur
- **Batch**: Update views in scheduled batches
- **On-demand**: Build views when first requested
- **Hybrid**: Combine real-time critical updates with batch processing

#### Projection Strategies

**Event Projection:**

```
Event to Read Model Projection:
OrderPlacedEvent → {
    CustomerOrderHistoryView.addOrder(event.orderId, event.customerId)
    ProductSalesView.incrementSales(event.productId, event.quantity)
    InventoryView.decreaseStock(event.productId, event.quantity)
    RevenueReportView.addRevenue(event.totalAmount, event.date)
}

Projection Characteristics:
- Idempotent: Safe to replay events
- Error handling: Handle projection failures
- Ordering: Maintain event order when necessary
- Performance: Optimize for projection speed
```

### CQRS with Different Storage Technologies

#### Polyglot Persistence

**Technology Selection:**

```
Storage Technology Matching:
Write Side:
├── PostgreSQL: Strong ACID properties for transactions
├── MongoDB: Flexible schema for aggregates
└── Event Store: Specialized event storage

Read Side:
├── Elasticsearch: Full-text search and analytics
├── Redis: High-performance caching and session data
├── InfluxDB: Time-series data and metrics
├── Neo4j: Graph relationships and recommendations
└── Cassandra: High-scale, distributed reads
```

**Data Synchronization:**

- **Event-driven sync**: Use events to sync between storage systems
- **Change data capture**: Capture changes from write database
- **ETL pipelines**: Batch synchronization processes
- **Stream processing**: Real-time data transformation and loading

### CQRS Challenges and Solutions

#### Consistency Management

**Eventual Consistency:**

- **Read-after-write**: Queries may not see immediate writes
- **User experience**: Design UI for eventual consistency
- **Conflict resolution**: Handle concurrent updates
- **Consistency monitoring**: Track synchronization lag

**Consistency Patterns:**

```
Consistency Strategies:
├── Accept eventual consistency
├── Provide consistency indicators to users
├── Use read-your-writes consistency
├── Cache command results for immediate display
└── Implement conflict detection and resolution
```

#### Complexity Management

**Implementation Complexity:**

- **Infrastructure overhead**: Multiple databases and synchronization
- **Debugging complexity**: Trace through command/query separation
- **Testing complexity**: Test both command and query sides
- **Operational complexity**: Monitor multiple data stores

**Mitigation Strategies:**

- **Start simple**: Begin with simple CQRS and evolve
- **Incremental adoption**: Apply CQRS to specific bounded contexts
- **Tooling**: Use frameworks and tools that support CQRS
- **Documentation**: Maintain clear documentation of data flows

### Advanced CQRS Patterns

#### Multi-Model CQRS

**Multiple Read Models:**

```
Advanced CQRS Architecture:
Write Model → Event Store
    ↓ (Events)
Read Model 1: Real-time dashboard (Redis)
Read Model 2: Analytics reports (ClickHouse)
Read Model 3: Search index (Elasticsearch)
Read Model 4: Graph analysis (Neo4j)
Read Model 5: Mobile API cache (DynamoDB)

Benefits:
- Specialized optimization per use case
- Independent scaling per read model
- Technology diversity for optimal performance
- Isolation of query concerns
```

#### CQRS with Event Sourcing

**Integrated Pattern:**

- **Natural fit**: Event sourcing provides events for CQRS
- **Audit capabilities**: Complete audit trail with query optimization
- **Time travel**: Query historical states
- **Event replay**: Rebuild read models from events

------

## Saga Pattern

### Saga Pattern Fundamentals

The Saga pattern manages long-running transactions across multiple services by breaking them into a series of smaller, compensatable transactions that can be coordinated to maintain data consistency.

### Saga Types

#### Orchestration-Based Saga

**Centralized Coordination:**

```
Orchestrator Saga Pattern:
Order Saga Orchestrator
├── Step 1: Reserve Inventory
├── Step 2: Process Payment
├── Step 3: Ship Order
└── Step 4: Send Notification

Orchestrator Responsibilities:
- Define transaction sequence
- Invoke service operations
- Handle failures and compensation
- Maintain transaction state
- Coordinate rollback if needed
```

**Benefits:**

- **Centralized control**: Single point of coordination
- **Clear flow**: Explicit transaction sequence
- **Easy monitoring**: Centralized state tracking
- **Complex logic**: Support for complex decision logic

**Drawbacks:**

- **Single point of failure**: Orchestrator becomes critical component
- **Coupling**: Services coupled to orchestrator
- **Complexity**: Orchestrator logic can become complex

#### Choreography-Based Saga

**Decentralized Coordination:**

```
Choreography Saga Pattern:
Order Service → OrderPlaced Event
    ↓
Inventory Service → InventoryReserved Event
    ↓
Payment Service → PaymentProcessed Event
    ↓
Shipping Service → OrderShipped Event
    ↓
Notification Service → NotificationSent Event

Each service:
- Listens for relevant events
- Performs its operation
- Publishes result events
- Handles compensation if needed
```

**Benefits:**

- **Decentralized**: No single point of failure
- **Loosely coupled**: Services only depend on events
- **Scalable**: Natural horizontal scaling
- **Flexible**: Easy to add new participants

**Drawbacks:**

- **Complex flow**: Harder to understand overall flow
- **Debugging**: Distributed state makes debugging difficult
- **Monitoring**: No central place to monitor progress

### Saga Implementation

#### Compensation Actions

**Compensating Transactions:**

```
Saga Compensation Example:
Forward Transaction: ReserveInventory(productId, quantity)
Compensating Transaction: ReleaseInventory(productId, quantity)

Forward Transaction: ChargePayment(customerId, amount)
Compensating Transaction: RefundPayment(customerId, amount)

Forward Transaction: CreateShipment(orderId, address)
Compensating Transaction: CancelShipment(shipmentId)

Compensation Requirements:
- Semantic rollback (not technical rollback)
- Idempotent operations
- Handle partial failures
- Maintain business invariants
```

#### State Management

**Saga State Tracking:**

```
Saga State Example:
{
  "sagaId": "saga-12345",
  "sagaType": "OrderProcessingSaga",
  "currentStep": 3,
  "status": "IN_PROGRESS",
  "startTime": "2024-01-15T10:00:00Z",
  "steps": [
    {
      "stepId": 1,
      "stepType": "ReserveInventory",
      "status": "COMPLETED",
      "timestamp": "2024-01-15T10:00:15Z",
      "compensationData": {"reservationId": "res-123"}
    },
    {
      "stepId": 2,
      "stepType": "ProcessPayment",
      "status": "COMPLETED", 
      "timestamp": "2024-01-15T10:00:30Z",
      "compensationData": {"transactionId": "txn-456"}
    },
    {
      "stepId": 3,
      "stepType": "ShipOrder",
      "status": "IN_PROGRESS",
      "timestamp": "2024-01-15T10:00:45Z"
    }
  ]
}
```

### Saga Coordination Patterns

#### Orchestrator Implementation

**Saga Orchestrator Service:**

```
Order Processing Orchestrator:
class OrderSagaOrchestrator {
    
    public void processOrder(OrderRequest request) {
        Saga saga = createSaga(request);
        executeStep(saga, RESERVE_INVENTORY);
    }
    
    private void executeStep(Saga saga, StepType stepType) {
        switch(stepType) {
            case RESERVE_INVENTORY:
                inventoryService.reserve(saga.getOrderData());
                break;
            case PROCESS_PAYMENT:
                paymentService.charge(saga.getPaymentData());
                break;
            case SHIP_ORDER:
                shippingService.ship(saga.getShippingData());
                break;
        }
        saga.markStepCompleted(stepType);
        executeNextStep(saga);
    }
    
    public void handleStepFailure(Saga saga, StepType failedStep) {
        compensateCompletedSteps(saga, failedStep);
    }
}
```

#### Event-Driven Choreography

**Service Choreography:**

```
Choreography Implementation:
Each Service:
1. Subscribes to relevant events
2. Processes business logic
3. Publishes result events
4. Handles compensation events

Order Service:
- Publishes: OrderPlaced
- Subscribes to: PaymentFailed, ShippingFailed
- Compensation: CancelOrder

Inventory Service:
- Subscribes to: OrderPlaced
- Publishes: InventoryReserved, InventoryReservationFailed
- Compensation: ReleaseInventory

Payment Service:
- Subscribes to: InventoryReserved
- Publishes: PaymentProcessed, PaymentFailed
- Compensation: RefundPayment
```

### Saga Error Handling

#### Failure Recovery Strategies

**Retry Mechanisms:**

- **Immediate retry**: Retry failed operations immediately
- **Exponential backoff**: Increase delay between retries
- **Circuit breaker**: Stop retrying after repeated failures
- **Dead letter queue**: Handle permanently failed messages

**Compensation Strategies:**

```
Compensation Approaches:
├── Backward Recovery: Undo completed steps
├── Forward Recovery: Continue with alternative steps
├── Partial Compensation: Compensate some steps, continue others
└── Manual Intervention: Escalate to human operators

Example Compensation Flow:
1. Payment fails at step 3
2. Compensate step 2: Refund payment
3. Compensate step 1: Release inventory
4. Mark saga as FAILED
5. Notify customer of order failure
```

#### Timeout Handling

**Saga Timeouts:**

- **Overall saga timeout**: Maximum time for entire saga
- **Step timeouts**: Maximum time for individual steps
- **Compensation timeouts**: Time limit for compensation actions
- **Escalation**: Handle timeouts with manual intervention

### Advanced Saga Patterns

#### Nested Sagas

**Hierarchical Sagas:**

```
Nested Saga Example:
Order Processing Saga
├── Customer Onboarding Sub-Saga
│   ├── Verify Identity
│   ├── Create Account
│   └── Set Preferences
├── Order Fulfillment Sub-Saga
│   ├── Reserve Inventory
│   ├── Process Payment
│   └── Ship Order
└── Post-Order Sub-Saga
    ├── Send Confirmation
    ├── Update Loyalty Points
    └── Schedule Follow-up

Benefits:
- Modular composition
- Reusable sub-sagas
- Independent scaling
- Simplified testing
```

#### Parallel Saga Execution

**Concurrent Steps:**

```
Parallel Saga Execution:
Step 1: Reserve Inventory
    ↓
Parallel Execution:
├── Step 2a: Process Payment
├── Step 2b: Prepare Shipping Label
└── Step 2c: Send Order Confirmation
    ↓
Step 3: Ship Order (waits for all parallel steps)

Coordination:
- Use barriers for synchronization
- Handle partial failures in parallel steps
- Compensate all parallel steps if any fails
- Optimize for performance while maintaining consistency
```

------

## Database per Service

### Database per Service Fundamentals

The Database per Service pattern ensures that each microservice owns its data and accesses it only through well-defined APIs, promoting service autonomy and reducing coupling.

### Service Data Ownership

#### Data Encapsulation

**Service Boundaries:**

```
Service Data Ownership:
User Service
├── User Database (PostgreSQL)
├── User profiles, authentication, preferences
└── APIs: getUserById, updateProfile, authenticate

Order Service  
├── Order Database (MongoDB)
├── Orders, order items, order status
└── APIs: createOrder, getOrderHistory, updateOrderStatus

Inventory Service
├── Inventory Database (PostgreSQL)
├── Product stock, reservations, locations
└── APIs: checkAvailability, reserveStock, updateInventory

Payment Service
├── Payment Database (PostgreSQL + Encryption)
├── Payment methods, transactions, billing
└── APIs: processPayment, getPaymentHistory, refundPayment
```

**Data Access Rules:**

- **Direct database access forbidden**: No cross-service database access
- **API-only communication**: Services communicate only through APIs
- **Data ownership**: Each service owns its database schema
- **Independent evolution**: Services can evolve databases independently

#### Service Data Models

**Domain-Specific Models:**

```
Data Model Examples:
User Service Model:
- Focus on identity and preferences
- Optimized for authentication flows
- User profile management
- Privacy and security compliance

Order Service Model:  
- Focus on order lifecycle
- Optimized for order processing workflows
- Order state management
- Integration with fulfillment systems

Inventory Service Model:
- Focus on stock management
- Optimized for availability queries
- Real-time stock updates
- Integration with supply chain
```

### Data Consistency Challenges

#### Cross-Service Queries

**Query Challenges:**

- **No joins**: Cannot join data across service databases
- **Aggregation complexity**: Difficult to aggregate across services
- **Real-time queries**: Challenging to get consistent view across services
- **Reporting**: Complex to generate cross-service reports

**Solutions:**

```
Cross-Service Query Patterns:
├── API Composition: Combine data from multiple API calls
├── Data Synchronization: Replicate needed data between services
├── CQRS Read Models: Build specialized views for queries
├── Event-Driven Views: Maintain views using events
└── Batch ETL: Extract data for analytics and reporting
```

#### Distributed Transactions

**Transaction Challenges:**

- **ACID across services**: Cannot use traditional ACID transactions
- **Consistency guarantees**: Difficult to maintain strong consistency
- **Failure handling**: Complex error handling across service boundaries
- **Performance impact**: Distributed transactions affect performance

**Alternative Patterns:**

- **Saga Pattern**: Long-running transactions with compensation
- **Event Sourcing**: Eventually consistent event-driven updates
- **Eventual Consistency**: Accept temporary inconsistencies
- **Idempotent Operations**: Safe to retry operations

### Technology Diversity

#### Polyglot Persistence

**Database Selection per Service:**

```
Technology Matching:
User Service → PostgreSQL
- ACID properties for user data
- Strong consistency for authentication
- Mature ecosystem and tooling

Order Service → MongoDB  
- Flexible schema for order variations
- Document model fits order structure
- Horizontal scaling capabilities

Inventory Service → Redis + PostgreSQL
- Redis for real-time stock checks
- PostgreSQL for persistent inventory data
- Fast read performance for availability

Analytics Service → ClickHouse
- Columnar storage for analytics
- High-performance aggregations
- Time-series data optimization

Search Service → Elasticsearch
- Full-text search capabilities
- Real-time indexing
- Faceted search support
```

#### Technology Benefits and Challenges

**Benefits:**

- **Optimal fit**: Choose best technology for each use case
- **Performance optimization**: Optimize for specific access patterns
- **Team expertise**: Teams can specialize in specific technologies
- **Innovation**: Adopt new technologies without affecting other services

**Challenges:**

- **Operational complexity**: Multiple databases to manage
- **Skill requirements**: Need expertise in multiple technologies
- **Tooling diversity**: Different monitoring and backup tools
- **Cost overhead**: Multiple database licenses and infrastructure

### Implementation Strategies

#### Gradual Migration

**Migration Approach:**

```
Migration Strategy:
Phase 1: Identify Service Boundaries
- Define service domains
- Identify data ownership
- Plan service interfaces

Phase 2: Duplicate Data
- Copy shared data to service databases
- Implement data synchronization
- Test service independence

Phase 3: Switch to Service APIs
- Update code to use service APIs
- Remove direct database dependencies
- Implement fallback mechanisms

Phase 4: Remove Shared Database
- Clean up unused data
- Decommission shared database
- Optimize service databases
```

#### Data Synchronization

**Synchronization Patterns:**

```
Data Sync Approaches:
├── Event-Driven Sync: Use events to sync data changes
├── CDC (Change Data Capture): Capture database changes
├── API-Based Sync: Periodic sync via API calls
├── Message Queue Sync: Async sync via message queues
└── Batch ETL: Scheduled batch synchronization

Event-Driven Example:
User Profile Updated → Event Published
    ↓
Order Service: Updates customer name in orders
Notification Service: Updates contact information
Analytics Service: Updates customer dimensions
```

### Advanced Patterns

#### Shared Reference Data

**Reference Data Management:**

```
Reference Data Patterns:
├── Replicated Reference Data: Copy to each service
├── Reference Data Service: Dedicated service for reference data
├── Cached Reference Data: Cache reference data locally
└── Embedded Reference Data: Include reference data in events

Example - Country Codes:
Option 1: Each service maintains own copy
Option 2: Shared reference data service
Option 3: Cache reference data with TTL
Option 4: Include country data in relevant events
```

#### Data Service Composition

**Composite Services:**

```
Data Composition Patterns:
API Gateway Composition:
├── Gateway aggregates data from multiple services
├── Client makes single request to gateway
├── Gateway fans out to backend services
├── Gateway combines responses
└── Returns aggregated response to client

Backend for Frontend (BFF):
├── Create specialized aggregation services
├── Optimize for specific client needs
├── Handle service-specific data transformations
├── Implement client-specific caching
└── Manage client-specific API contracts
```

#### Event-Driven Data Architecture

**Event Sourcing Integration:**

```
Event-Driven Data Flow:
Commands → Service → Events → Event Store
    ↓
Event Stream → Other Services → Update Local Data
    ↓
Projections → Read Models → Query APIs

Benefits:
- Services get eventual consistent updates
- Complete audit trail of all changes
- Ability to rebuild service data from events
- Support for temporal queries and analytics
```

### Monitoring and Operations

#### Multi-Database Monitoring

**Monitoring Strategies:**

```
Database Monitoring:
├── Performance Metrics: Query performance per database
├── Health Checks: Database availability and connectivity  
├── Resource Usage: CPU, memory, storage per database
├── Query Analysis: Slow queries and optimization opportunities
└── Capacity Planning: Growth trends and scaling needs

Cross-Service Metrics:
├── API Response Times: Service-to-service communication
├── Data Consistency: Lag between related data updates
├── Error Rates: Failed cross-service operations
├── Dependency Health: Impact of service failures
└── Business Metrics: End-to-end business process health
```

#### Backup and Disaster Recovery

**Data Protection Strategies:**

- **Per-service backups**: Independent backup strategies per service
- **Cross-service recovery**: Coordinate recovery across services
- **Point-in-time recovery**: Restore services to consistent point in time
- **Disaster recovery testing**: Test recovery procedures regularly

------

## Key Takeaways

1. **Event Sourcing provides complete audit trail**: Store all changes as events for full history and auditability
2. **CQRS optimizes read and write separately**: Separate command and query responsibilities for better performance
3. **Saga Pattern manages distributed transactions**: Coordinate long-running transactions across services with compensation
4. **Database per Service ensures autonomy**: Each service owns its data and evolves independently
5. **Eventual consistency is acceptable**: Trade strong consistency for availability and scalability
6. **Event-driven architecture complements data patterns**: Events provide natural integration between patterns
7. **Complexity requires careful consideration**: Data patterns add complexity that must be justified by benefits

### Common Data Pattern Mistakes

- **Event sourcing without clear business need**: Adding complexity without sufficient benefit
- **CQRS for simple CRUD operations**: Over-engineering simple data access patterns
- **Saga for short transactions**: Using saga pattern for operations that could be single transactions
- **Ignoring data consistency requirements**: Not properly analyzing consistency needs
- **Poor event design**: Creating events that are too granular or too coarse
- **Inadequate monitoring**: Not monitoring eventual consistency and data synchronization

> **Remember**: Data patterns are powerful but complex. Start with simpler approaches and evolve to these patterns when you have clear requirements that justify the additional complexity. Always consider the trade-offs between consistency, availability, and partition tolerance based on your specific business needs.