# Real-time Systems

Real-time systems enable immediate data exchange and processing, providing users with live updates and interactive experiences. These systems are critical for applications requiring instant communication, live data feeds, and collaborative features.

### Real-time System Characteristics

Low Latency:

- Sub-second response times: Typically under 100ms for user interactions
- Minimal processing delays: Efficient data processing and routing
- Network optimization: Reduced network round trips
- Edge processing: Computation closer to users

High Concurrency:

- Concurrent connections: Support thousands to millions of simultaneous users
- Connection pooling: Efficient resource utilization
- Load distribution: Balance load across multiple servers
- Scalability: Horizontal scaling for growing user base

Event-Driven Architecture:

- Asynchronous processing: Non-blocking operations
- Event propagation: Broadcast events to interested parties
- State synchronization: Maintain consistent state across clients
- Message ordering: Preserve event ordering when required

### Real-time Use Cases

Communication Applications:

- Chat systems: Instant messaging and group conversations
- Video conferencing: Real-time audio and video communication
- Voice calls: Real-time voice communication
- Screen sharing: Live screen broadcasting

Collaborative Applications:

- Document editing: Real-time collaborative document editing
- Code editors: Simultaneous code editing and sharing
- Whiteboards: Collaborative drawing and diagramming
- Design tools: Real-time design collaboration

Live Data Applications:

- Stock market feeds: Real-time financial data
- Sports scores: Live game updates and statistics
- News feeds: Breaking news and live updates
- IoT monitoring: Real-time sensor data and alerts

Gaming Applications:

- Multiplayer games: Real-time game state synchronization
- Live tournaments: Real-time tournament updates
- In-game chat: Instant communication between players
- Leaderboards: Live ranking updates

------

## WebSocket Architecture

WebSockets provide full-duplex communication channels over a single TCP connection, enabling real-time bidirectional data exchange between clients and servers.

### WebSocket Protocol

#### Protocol Overview

**WebSocket Handshake:**

1. HTTP Upgrade Request: Client requests protocol upgrade
2. Upgrade Response: Server accepts WebSocket connection
3. Protocol Switch: Connection switches from HTTP to WebSocket
4. Bidirectional Communication: Full-duplex message exchange

**Connection Lifecycle:**

- **Opening**: Establish WebSocket connection via handshake
- **Message Exchange**: Send and receive messages bidirectionally
- **Ping/Pong**: Keep connection alive with heartbeat mechanism
- **Closing**: Graceful connection termination

**WebSocket Frame Types:**

- Text frames: UTF-8 encoded text messages
- Binary frames: Binary data transmission
- Control frames: Connection control (ping, pong, close)
- Continuation frames: Fragmented message continuation

#### WebSocket vs HTTP

| Aspect            | HTTP                       | WebSocket             |
| ----------------- | -------------------------- | --------------------- |
| **Communication** | Request-response           | Bidirectional         |
| **Connection**    | Stateless                  | Persistent            |
| **Overhead**      | High (headers per request) | Low (minimal framing) |
| **Real-time**     | Polling required           | Native real-time      |
| **Server push**   | Not supported              | Native support        |
| **Caching**       | Extensive support          | Limited caching       |

### WebSocket Server Architecture

#### Connection Management

**Connection Handling:**

- Connection registry: Track active WebSocket connections
- User session mapping: Associate connections with user sessions
- Connection pooling: Organize connections by rooms or topics
- Resource limits: Prevent resource exhaustion from too many connections

**Scaling Patterns:**

- Vertical scaling: Increase server resources for more connections
- Horizontal scaling: Distribute connections across multiple servers
- Connection affinity: Route related connections to same server
- Load balancing: Distribute new connections across servers

#### Message Broadcasting

**Broadcasting Strategies:**

- Fan-out: Send message to all connected clients
- Room-based: Send messages to clients in specific rooms
- User-targeted: Send messages to specific users
- Filtered broadcasting: Send messages based on criteria

**Message Routing:**

- Topic-based routing: Route messages based on topics/channels
- Content-based routing: Route based on message content
- Geographic routing: Route based on client location
- Load-based routing: Route based on server load

### WebSocket Implementation Patterns

#### Real-time Chat System

**Architecture Components:**

- **WebSocket server**: Handle client connections and messages
- **Message broker**: Route messages between servers
- **User presence service**: Track online/offline status
- **Message persistence**: Store chat history
- **Push notification service**: Notify offline users

**Message Flow:**

1. **Client connects**: Establish WebSocket connection
2. **Authentication**: Verify user identity and permissions
3. **Room joining**: Subscribe to relevant chat rooms
4. **Message sending**: Client sends message via WebSocket
5. **Message broadcasting**: Server broadcasts to room participants
6. **Message persistence**: Store message in database
7. **Presence updates**: Update user online status

#### Live Data Feeds

**Stock Market Feed Example:**

- Data sources: Market data providers and exchanges
- Data processing: Real-time price calculations and aggregations
- Subscription management: Client subscription to specific symbols
- Rate limiting: Prevent overwhelming clients with data
- Data compression: Minimize bandwidth usage

**Feed Architecture:**

- Data ingestion: Receive data from external sources
- Stream processing: Process and transform data in real-time
- Client subscriptions: Manage client interest in specific data
- Data broadcasting: Push relevant data to subscribed clients

#### Collaborative Editing

**Operational Transformation:**

- Operation capture: Capture user editing operations
- Conflict resolution: Transform operations to handle conflicts
- Operation broadcasting: Send operations to all participants
- State synchronization: Maintain consistent document state

**CRDT Implementation:**

- Conflict-free operations: Use CRDTs for automatic conflict resolution
- Local operations: Apply operations locally first
- Operation synchronization: Sync operations with other participants
- Eventual consistency: Guarantee eventual document consistency

### WebSocket Scaling and Performance

#### Horizontal Scaling

**Multi-Server Architecture:**

- Load balancer: Distribute connections across WebSocket servers
- Session affinity: Route user to same server for session
- Message broker: Enable communication between servers
- Shared state: Use Redis or database for shared state

**Cross-Server Communication:**

- Message queues: Use Redis Pub/Sub or RabbitMQ
- Event streaming: Use Apache Kafka for high-throughput scenarios
- Database sharing: Share connection and user state in database
- Service mesh: Use service mesh for server-to-server communication

#### Performance Optimization

**Connection Optimization:**

- Connection pooling: Reuse connections efficiently
- Keep-alive: Maintain connections with ping/pong
- Connection draining: Gracefully handle server shutdowns
- Resource monitoring: Monitor memory and CPU usage per connection

**Message Optimization:**

- Message compression: Compress large messages
- Batching: Combine multiple small messages
- Message prioritization: Prioritize important messages
- Rate limiting: Prevent message flooding

### WebSocket Security

#### Authentication and Authorization

**Connection Authentication:**

- Token-based: Use JWT or session tokens for authentication
- OAuth integration: Integrate with OAuth providers
- Certificate-based: Use client certificates for authentication
- Custom protocols: Implement custom authentication schemes

**Authorization Patterns:**

- Room-based permissions: Control access to specific rooms/channels
- Feature-based permissions: Control access to specific features
- Dynamic permissions: Change permissions during session
- Permission inheritance: Inherit permissions from user roles

#### Security Best Practices

**Input Validation:**

- Message validation: Validate all incoming messages
- Rate limiting: Prevent abuse through excessive messages
- Content filtering: Filter malicious or inappropriate content
- Size limits: Limit message sizes to prevent DoS attacks

**Connection Security:**

- WSS (WebSocket Secure): Use TLS encryption
- Origin validation: Validate connection origins
- CSRF protection: Prevent cross-site request forgery
- Connection limits: Limit connections per IP or user

------

## Server-Sent Events (SSE)

Server-Sent Events provide a simple way for servers to push data to web clients over HTTP, enabling real-time updates with automatic reconnection and event streaming.

### SSE vs WebSockets

#### SSE Characteristics

**Unidirectional Communication:**

- Server-to-client only: Data flows from server to client
- Simple implementation: Built on standard HTTP
- Automatic reconnection: Browser handles reconnection automatically
- Event streaming: Natural fit for event-based data

**HTTP-Based Protocol:**

- Standard HTTP: Uses regular HTTP connections
- Streaming response: Long-lived HTTP response
- Text-based: Events sent as text over HTTP
- Built-in caching: Can leverage HTTP caching

#### When to Choose SSE

**SSE Use Cases:**

- Live feeds: News feeds, social media updates
- Monitoring dashboards: Real-time metrics and alerts
- Notifications: Push notifications to web clients
- Progress tracking: File upload or processing progress
- Live scores: Sports scores and game updates
### SSE Implementation

#### SSE Protocol

**Event Stream Format:**

```
data: This is a simple message

data: This is a message
data: with multiple lines

event: userJoined
data: {"user": "alice", "timestamp": "2024-01-01T10:00:00Z"}

id: 12345
event: stockPrice
data: {"symbol": "AAPL", "price": 150.25}
retry: 3000
```

**SSE Fields:**

- **data**: The message data (can span multiple lines)
- **event**: Event type for client-side event handling
- **id**: Unique identifier for event (enables resumption)
- **retry**: Reconnection timeout in milliseconds

#### Client-Side Implementation

**JavaScript EventSource API:**

```javascript
const eventSource = new EventSource('/api/events');

// Handle default events
eventSource.onmessage = function(event) {
    console.log('Received:', event.data);
};

// Handle custom events
eventSource.addEventListener('stockPrice', function(event) {
    const data = JSON.parse(event.data);
    updateStockPrice(data.symbol, data.price);
});

// Handle connection events
eventSource.onopen = function() {
    console.log('Connection opened');
};

eventSource.onerror = function(event) {
    console.log('Error occurred:', event);
};
```

**Automatic Reconnection:**

- Default behavior: Browser automatically reconnects on connection loss
- Last-Event-ID: Browser sends last received event ID on reconnection
- Retry interval: Server can specify reconnection delay
- Manual control: Application can close and recreate connections

### SSE Server Implementation

#### Basic SSE Server

**HTTP Response Headers:**

```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
Access-Control-Allow-Origin: *
```

**Event Generation Patterns:**

- Periodic events: Send events at regular intervals
- Event-driven: Send events based on external triggers
- Data changes: Send events when data changes
- Subscription-based: Send events based on client subscriptions

#### SSE with Load Balancing

**Sticky Sessions:**

- Session affinity: Route client to same server
- Load balancer configuration: Configure sticky sessions
- Server state: Maintain client subscription state per server
- Failover handling: Handle server failures gracefully

**Shared State Architecture:**

- External event bus: Use Redis Pub/Sub or message queues
- Stateless servers: Keep servers stateless for better scaling
- Event broadcasting: Broadcast events to all servers
- Client subscription tracking: Track subscriptions in shared storage

### SSE Use Cases and Patterns

#### Live Dashboard

**Metrics Dashboard:**

- Real-time metrics: System performance, business metrics
- Alert notifications: Critical alerts and warnings
- Status updates: Service status and health checks
- Progress tracking: Long-running operation progress

**Implementation Pattern:**

1. Metric collection: Collect metrics from various sources
2. Event generation: Generate events for metric updates
3. Client subscription: Clients subscribe to relevant metrics
4. Event streaming: Stream metric updates to subscribed clients
5. UI updates: Update dashboard UI with new data

#### Live News Feed

**News Stream Architecture:**

- Content ingestion: Receive news from multiple sources
- Content processing: Process and categorize news items
- User preferences: Track user interests and subscriptions
- Personalized delivery: Send relevant news to users

**Feed Optimization:**

- Content filtering: Filter based on user preferences
- Rate limiting: Control update frequency per user
- Batching: Group related updates together
- Prioritization: Prioritize important news items

#### Notification System

**Real-time Notifications:**

- Event sources: Various application events trigger notifications
- User targeting: Send notifications to specific users
- Notification types: Different types for different events
- Delivery tracking: Track notification delivery status

**Notification Flow:**

1. Event trigger: Application event triggers notification
2. User lookup: Identify users who should receive notification
3. Notification generation: Create notification message
4. Delivery: Send notification via SSE to connected users
5. Fallback: Use push notifications for offline users

------

## Real-time Data Processing

Real-time data processing involves continuous processing of data streams as they arrive, enabling immediate insights and actions based on fresh data.

### Stream Processing Concepts

#### Data Streams

**Stream Characteristics:**

- Continuous data flow: Unbounded sequence of data elements
- Time-ordered: Events typically ordered by occurrence time
- High velocity: Data arrives at high rates
- Varying volume: Data volume can fluctuate significantly

**Stream Sources:**

- **User interactions**: Clicks, page views, application events
- **IoT sensors**: Temperature, pressure, motion sensors
- **Financial markets**: Stock prices, trade executions
- **System logs**: Application logs, security events
- **Social media**: Posts, comments, likes, shares

#### Processing Models

**Event Time vs Processing Time:**

- Event time: When event actually occurred
- Processing time: When event is processed by system
- Watermarks: Track progress of event time in stream
- Late arrival handling: Handle events that arrive out of order

**Window Processing:**

- Tumbling windows: Fixed-size, non-overlapping windows
- Sliding windows: Fixed-size, overlapping windows
- Session windows: Dynamic windows based on activity
- Custom windows: Application-specific windowing logic

### Stream Processing Architectures

#### Lambda Architecture

![](assets/Pasted%20image%2020251231125406.png)

**Architecture Components:**

- Batch layer: Process historical data in large batches
- Speed layer: Process real-time data streams
- Serving layer: Merge results from batch and speed layers
- Query interface: Unified interface for both batch and real-time data

**Benefits and Drawbacks:**

- Benefits: Fault tolerance, eventual consistency, comprehensive processing
- Drawbacks: Complexity, duplicate logic, consistency challenges

Use Cases : ClickStream Analytics, Massive Historical Datasets, Old HDFS Systems, etc.
#### Kappa Architecture

*One Streaming pipeline does everything*

![](assets/Pasted%20image%2020251231125741.png)

**Simplified Approach:**

- Stream-only processing: All data processed as streams
- Reprocessing: Handle both real-time and historical data as streams
- Simplified architecture: Single processing paradigm
- Event sourcing: Store all events for reprocessing

**Advantages:**

- Reduced complexity: Single processing model
- Consistent logic: Same code for real-time and batch processing
- Easier maintenance: Simpler operational model
- Modern Approach : industry is moving towards streaming ~ batch + real_time

Applications : Fraud Detection, Monitoring, Metrics, IoT, etc.
### Real-time Processing Patterns

#### Event Sourcing

**Event Store Architecture:**

- Event logging: Store all changes as sequence of events
- Event replay: Reconstruct state by replaying events
- Snapshots: Periodic state snapshots for performance
- Event versioning: Handle event schema evolution

**Processing Patterns:**

- Event projection: Create read models from event streams
- Event aggregation: Aggregate events into summaries
- Event correlation: Correlate related events across streams
- Event filtering: Filter events based on criteria

#### Complex Event Processing (CEP)

**Pattern Detection:**

- Temporal patterns: Detect patterns across time
- Correlation patterns: Detect related events
- Threshold patterns: Detect when metrics exceed thresholds
- Trend patterns: Detect trends and anomalies

**CEP Use Cases:**

- Fraud detection: Detect suspicious transaction patterns
- System monitoring: Detect system performance issues
- Trading systems: Detect trading opportunities
- IoT analytics: Detect equipment failures or anomalies

#### Stream Analytics

**Real-time Aggregations:**

- Count aggregations: Count events in time windows
- Sum aggregations: Sum numeric values in windows
- Average calculations: Calculate averages over time
- Min/max tracking: Track minimum and maximum values

**Stateful Processing:**

- Running totals: Maintain running counts or sums
- Moving averages: Calculate moving averages over time
- State checkpointing: Persist processing state for fault tolerance
- State recovery: Recover processing state after failures

### Stream Processing Technologies

#### Apache Kafka

**Kafka as Stream Platform:**

- Event streaming: Publish-subscribe event streaming
- Stream processing: Kafka Streams for stream processing
- Connect framework: Integrate with external systems
- Schema registry: Manage event schema evolution

**Kafka Streams Patterns:**

- Stateless transformations: Map, filter, transform events
- Stateful transformations: Aggregations, joins, windowing
- Stream-table duality: Streams and tables as dual concepts
- Exactly-once semantics: Guarantee exactly-once processing

#### Apache Flink

**Flink Capabilities:**

- Low latency: Sub-second latency processing
- Event time processing: Handle out-of-order events correctly
- Fault tolerance: Automatic recovery from failures
- Scalability: Scale processing to thousands of cores

**Flink Features:**

- DataStream API: API for stream processing applications
- CEP library: Complex event processing capabilities
- Machine learning: Real-time machine learning on streams
- SQL support: SQL queries on streaming data

#### Apache Storm

**Storm Architecture:**

- Spouts: Data sources that emit streams
- Bolts: Processing components that transform streams
- Topologies: Networks of spouts and bolts
- Stream groupings: How streams are distributed between bolts

**Storm Use Cases:**

- Real-time analytics: Calculate metrics in real-time
- Online machine learning: Update models with streaming data
- ETL processing: Extract, transform, load streaming data
- Monitoring systems: Real-time system monitoring

### Real-time Analytics

#### Metrics and KPIs

**Real-time Metrics:**

- Application metrics: Response times, error rates, throughput
- Business metrics: Sales, conversions, user engagement
- System metrics: CPU, memory, network utilization
- Custom metrics: Domain-specific measurements

**Metric Processing:**

- Aggregation: Sum, count, average, percentile calculations
- Alerting: Trigger alerts when metrics exceed thresholds
- Trending: Detect trends and anomalies in metrics
- Correlation: Correlate metrics across different systems

#### Real-time Dashboards

**Dashboard Architecture:**

- Data ingestion: Collect data from multiple sources
- Stream processing: Process and aggregate data in real-time
- Data storage: Store processed data for querying
- Visualization: Display data in charts, graphs, and tables
- Real-time updates: Push updates to dashboard users

**Dashboard Patterns:**

- Push-based updates: Server pushes updates to clients
- Pull-based updates: Clients poll for updates
- WebSocket updates: Real-time updates via WebSockets
- SSE updates: Server-sent events for dashboard updates

### Performance and Scalability

#### Stream Processing Optimization

**Performance Tuning:**

- Parallel processing: Process streams in parallel
- Partitioning: Partition streams for parallel processing
- Batching: Process events in micro-batches
- Caching: Cache frequently accessed data
- Resource allocation: Optimize CPU and memory usage

**Fault Tolerance:**

- Checkpointing: Save processing state periodically
- Replication: Replicate processing across multiple nodes
- Retry mechanisms: Retry failed operations automatically
- Dead letter queues: Handle messages that cannot be processed

#### Scaling Strategies

Horizontal Scaling:

- Add processing nodes: Scale out processing capacity
- Data partitioning: Partition data across processing nodes
- Load balancing: Distribute processing load evenly
- Auto-scaling: Automatically scale based on load

Vertical Scaling:

- Increase resources: Add CPU, memory, or storage
- Optimize algorithms: Improve processing efficiency
- Hardware acceleration: Use GPUs or specialized hardware
- Memory optimization: Optimize memory usage patterns