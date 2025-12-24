# Message Queues & Streaming

## Messaging Fundamentals

**Synchronous Processing**

````text
[Client] --request--> [Server] --process--> [Response] ---> [Client]
      <--  response-----------  <--result ---    <--     <---
````

Characterstics:

* client waits for response
* blocking operation
* immediate feedback
* tight coupling

Examples: Login, Payment Processing, Real-time Validation

**Asynchronous Processing**

````text
[Client] --request--> [API Server] --enqueue--> [Message Queue] --> [Worker]
         <--task_id--<           
                                                                     |
[Client] --status?--> [API Server] <--update_status--< [Database] <--
````

Chracterstics:

* client gets immediate acknowledgment
* Non-blocking Operation
* Eventual Processing
* Loose Coupling

Examples: Email Sending, Image Processing, Report Generation

Example of Program Structures for Both Methods

````python
# Synchronous approach
def upload_video_sync(video_file):
    # Client waits for entire process
    transcoded_video = transcode_video(video_file)  # Takes 5 minutes
    thumbnail = generate_thumbnail(video_file)      # Takes 30 seconds
    return {"video": transcoded_video, "thumbnail": thumbnail}

# Asynchronous approach
def upload_video_async(video_file):
    # Immediate response to client
    task_id = str(uuid.uuid4())
    
    # Queue background tasks
    video_queue.enqueue("transcode_video", video_file, task_id)
    thumbnail_queue.enqueue("generate_thumbnail", video_file, task_id)
    
    return {"task_id": task_id, "status": "processing"}
````

**When to Use Asynchronous Processing**

Use Cases:

- **Long-running tasks**: Video processing, data imports
- **Non-critical operations**: Email notifications, analytics
- **Decoupling systems**: Microservices communication
- **Load balancing**: Distribute work across multiple workers
- **Fault tolerance**: Retry failed operations

Benefits:

- **Better user experience**: No waiting for slow operations
- **System scalability**: Handle more concurrent requests
- **Fault isolation**: Failures don't cascade
- **Resource optimization**: Workers process at optimal pace

## Point-to-Point vs Publish-Subscribe Patterns

### Point-to-Point (Queue Pattern)

````text
[Producer] --> [Queue] --> [Consumer 1]
                       --> [Consumer 2]  (Load balanced)
                       --> [Consumer 3]
````

**Characteristics**:

- **One-to-one** communication
- Each message consumed by **exactly one** consumer
- **Load balancing** across consumers
- Message **removed** after consumption

**Use Cases**:

- **Task distribution**: Email sending, image processing
- **Load balancing**: Distribute work among workers
- **Request processing**: Order processing, payment handling

### Publish-Subscribe (Topic Pattern)

````text
[Publisher] --> [Topic] --> [Subscriber 1]
                        --> [Subscriber 2]  (All receive copy)
                        --> [Subscriber 3]
````

**Characteristics**:

- **One-to-many** communication
- Each message delivered to **all** subscribers
- **Broadcast** pattern
- Message **copied** to all consumers

**Use Cases**:

- **Event broadcasting**: User actions, system events
- **Real-time updates**: Stock prices, live scores
- **Notification systems**: Multiple services need same data

Comparison

| Aspect            | Point-to-Point           | Publish-Subscribe                   |
| ----------------- | ------------------------ | ----------------------------------- |
| Message Delivery  | One Consumer             | All Subscribers                     |
| Use Cases         | Task Distribution        | Event Broadcasting                  |
| Scaling           | Add more consumers       | Add more Subscribers                |
| Message Lifecycle | Consumed Once            | Copied to All                       |
| Coupling          | Producer knows Consumers | Publishers doesn’t know subscribers |

## Message Brokers vs Message Streams

#### Message Brokers (Traditional Queues)

Examples: RabbitMQ, ActiveMQ, Amazon SQS

**Characteristics**:

- **Message deletion** after consumption
- **Push or pull** based delivery
- **Transactional** semantics
- **FIFO ordering** within queue

**Dead Letter Queue**: Handle messages that cannot be processed successfully.

#### Message Streams (Event Logs)

**Examples**: Apache Kafka, Amazon Kinesis, Apache Pulsar

**Characteristics**:

- **Messages retained** for configured time
- **Offset-based** consumption
- **Replay capability**
- **Partitioned** for scale

| Feature             | Message Brokers            | Message Streams            |
| ------------------- | -------------------------- | -------------------------- |
| Message Persistence | Deleted after Consumption  | Retained for time Period   |
| Consumption Model   | Each message consumed once | Message can be replayed    |
| Ordering            | FIFO within queue          | Ordered within a partition |
| Scalability         | Vertical Scaling           | Horizontal Scaling         |
| Use Cases           | Task Queues, RPC           | Event Sourcing, Analytics  |

## Message Ordering & Durability

### Message Ordering

**Message Ordering Guarantees**

````python
# Single partition ensures global order
class GlobalOrderQueue:
    def __init__(self):
        self.messages = []  # Single queue for global order
        self.sequence = 0
    
    def send(self, message):
        self.sequence += 1
        ordered_message = {
            "sequence": self.sequence,
            "timestamp": time.time(),
            "payload": message
        }
        self.messages.append(ordered_message)
        return self.sequence
````

**Pros**: Strict ordering **Cons**: Single point of bottleneck, no parallelism

**Partition-Level Ordering**

```python
# Kafka-style partitioned ordering
class PartitionedQueue:
    def __init__(self, num_partitions=3):
        self.partitions = [[] for _ in range(num_partitions)]
        self.sequences = [0] * num_partitions
    
    def send(self, message, partition_key=None):
        # Determine partition
        if partition_key:
            partition = hash(partition_key) % len(self.partitions)
        else:
            partition = random.randint(0, len(self.partitions) - 1)
        
        # Maintain order within partition
        self.sequences[partition] += 1
        ordered_message = {
            "partition": partition,
            "sequence": self.sequences[partition],
            "payload": message
        }
        self.partitions[partition].append(ordered_message)
        return partition, self.sequences[partition]
```

**Pros**: Parallel processing, partition-level ordering **Cons**: No global ordering across partitions

**Ordering Strategies**

````python
# Strategy 1: User-based partitioning (orders for same user stay ordered)
def get_user_partition(user_id, num_partitions):
    return hash(str(user_id)) % num_partitions

# Strategy 2: Time-based partitioning (events in time windows)
def get_time_partition(timestamp, window_size_hours, num_partitions):
    time_window = int(timestamp // (window_size_hours * 3600))
    return time_window % num_partitions

# Strategy 3: Content-based partitioning (similar events grouped)
def get_content_partition(event_type, num_partitions):
    return hash(event_type) % num_partitions
````

### Durability Guarantees

#### At-Most-Once Delivery

**Guarantee**: No duplicates, but messages may be lost 

**Use Case**: Metrics, logs where some loss is acceptable

#### At-Least-Once Delivery

**Guarantee**: Messages delivered, but may have duplicates 

**Use Case**: Most common pattern, requires idempotent consumers

Tip: Use Exponential Backoff in Retry for Delivery with some limit

#### Exactly-Once Delivery

**Guarantee**: Messages delivered exactly once

**Use Case**: Financial transactions, critical operations

#### Durability Implementation

````python
class DurableMessageQueue:
    def __init__(self, persistence_type="disk"):
        self.persistence = persistence_type
        self.wal = WriteAheadLog() if persistence_type == "disk" else None
        self.memory_buffer = []
        self.ack_timeout = 30  # seconds
    
    def send(self, message, durability_level="sync"):
        # Generate unique message ID
        message_id = str(uuid.uuid4())
        timestamped_message = {
            "id": message_id,
            "timestamp": time.time(),
            "payload": message
        }
        
        if durability_level == "sync":
            # Synchronous durability - wait for disk write
            if self.wal:
                self.wal.write(timestamped_message)
                self.wal.sync()  # Force flush to disk
            self.memory_buffer.append(timestamped_message)
            
        elif durability_level == "async":
            # Asynchronous durability - background write
            self.memory_buffer.append(timestamped_message)
            if self.wal:
                asyncio.create_task(self.wal.write_async(timestamped_message))
        
        return message_id
    
    def acknowledge(self, message_id):
        # Remove from unacknowledged messages
        if self.wal:
            self.wal.mark_acknowledged(message_id)
````

## Retry Mechanisms

**Exponential Backoff**

````python
def exponential_backoff_retry(func, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
````

**Fixed Interval Retry**

````python
def fixed_interval_retry(func, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay)
````

**Linear Backoff**

* `delay = base_delay * (attempt + 1)`

### Error Handling Patterns

````python
class ErrorHandler:
    def __init__(self):
        self.retry_policies = {
            "transient": {"max_retries": 5, "strategy": "exponential"},
            "rate_limit": {"max_retries": 10, "strategy": "linear"},
            "permanent": {"max_retries": 0, "strategy": "none"}
        }
    
    def classify_error(self, exception):
        """Classify error type for appropriate handling"""
        if isinstance(exception, (ConnectionError, TimeoutError)):
            return "transient"
        elif isinstance(exception, RateLimitError):
            return "rate_limit"
        elif isinstance(exception, (ValueError, TypeError)):
            return "permanent"
        else:
            return "transient"  # Default to retryable
    
    def handle_error(self, message, exception):
        error_type = self.classify_error(exception)
        policy = self.retry_policies[error_type]
        
        if policy["max_retries"] == 0:
            # Send directly to DLQ
            self.send_to_dlq(message, exception)
        else:
            # Apply retry strategy
            self.schedule_retry(message, policy)
````

## Stream Processing vs Batch Processing

### Batch Processing

**Definition**: Process large volumes of data in discrete chunks

```python
# Batch processing example
class BatchProcessor:
    def __init__(self, batch_size=1000, processing_interval=3600):
        self.batch_size = batch_size
        self.processing_interval = processing_interval  # 1 hour
        self.batch_buffer = []
    
    def add_event(self, event):
        self.batch_buffer.append(event)
        
        if len(self.batch_buffer) >= self.batch_size:
            self.process_batch()
    
    def process_batch(self):
        if not self.batch_buffer:
            return
        
        # Process entire batch
        batch_to_process = self.batch_buffer.copy()
        self.batch_buffer.clear()
        
        # Aggregate operations
        user_stats = self.calculate_user_stats(batch_to_process)
        daily_metrics = self.calculate_daily_metrics(batch_to_process)
        
        # Bulk database operations
        self.database.bulk_insert(user_stats)
        self.database.bulk_insert(daily_metrics)
    
    def calculate_user_stats(self, events):
        user_aggregates = {}
        for event in events:
            user_id = event['user_id']
            if user_id not in user_aggregates:
                user_aggregates[user_id] = {
                    'page_views': 0,
                    'session_time': 0,
                    'events_count': 0
                }
            
            user_aggregates[user_id]['page_views'] += 1
            user_aggregates[user_id]['session_time'] += event.get('duration', 0)
            user_aggregates[user_id]['events_count'] += 1
        
        return user_aggregates
```

**Characteristics**:

- **High throughput**: Process large volumes efficiently
- **High latency**: Results available after batch completion
- **Resource efficiency**: Optimized for bulk operations
- **Complexity**: Simpler programming model

**Use Cases**: ETL jobs, daily reports, data warehousing

### Stream Processing

**Definition**: Process data continuously as it arrives

```python
# Stream processing example
class StreamProcessor:
    def __init__(self, window_size=60):  # 60 second windows
        self.window_size = window_size
        self.current_window = {}
        self.window_start = time.time()
    
    def process_event(self, event):
        current_time = time.time()
        
        # Check if we need to emit current window
        if current_time - self.window_start >= self.window_size:
            self.emit_window_results()
            self.start_new_window()
        
        # Process event immediately
        self.add_to_current_window(event)
        
        # Real-time alerts
        self.check_real_time_alerts(event)
    
    def add_to_current_window(self, event):
        user_id = event['user_id']
        if user_id not in self.current_window:
            self.current_window[user_id] = {
                'events': 0,
                'total_value': 0
            }
        
        self.current_window[user_id]['events'] += 1
        self.current_window[user_id]['total_value'] += event.get('value', 0)
    
    def emit_window_results(self):
        # Emit aggregated results for the window
        for user_id, stats in self.current_window.items():
            result = {
                'user_id': user_id,
                'window_start': self.window_start,
                'window_end': time.time(),
                'metrics': stats
            }
            self.output_stream.send(result)
    
    def check_real_time_alerts(self, event):
        # Immediate processing for alerts
        if event.get('value', 0) > 10000:  # High-value transaction
            alert = {
                'type': 'high_value_transaction',
                'user_id': event['user_id'],
                'value': event['value'],
                'timestamp': time.time()
            }
            self.alert_system.send_alert(alert)
```

**Characteristics**:

- **Low latency**: Real-time processing
- **Continuous processing**: Handle unbounded data streams
- **Resource intensive**: Maintain state and windows
- **Complex**: Handle ordering, late data, exactly-once

**Use Cases**: Real-time analytics, fraud detection, monitoring

| Aspect         | Batch Processing       | Stream Processing            |
| -------------- | ---------------------- | ---------------------------- |
| Latency        | High (hours/days)      | Low (seconds/minutes)        |
| Throughput     | Very high              | Moderate                     |
| Complexity     | Low                    | High                         |
| Resource Usage | Periodic Spikes        | Consistent Usage             |
| Use Cases      | Reports, ETL           | Real-time Alerts, Monitoring |
| Data Volume    | Large Bounded datasets | Continous unbounded streams  |

### Hybrid Approaches

Lambda Architecture

````text
         [Data Stream]
              |
         [Speed Layer]     [Batch Layer]
              |                |
         [Real-time View] [Batch View]
              |                |
              +---[Query]------+
                    |
              [Unified View]
````

Kappa Architecture

````text
[Data Stream] --> [Stream Processor] --> [Serving Layer]
                           |
                      [Reprocessing]
````

## Real-Time Pull/Push Systems

### Pull Model

````python
class PullBasedConsumer:
    def __init__(self, queue):
        self.queue = queue
        self.running = True
    
    def consume(self):
        while self.running:
            # Consumer actively polls for messages
            messages = self.queue.poll(timeout=1000)  # 1 second timeout
            
            if messages:
                for message in messages:
                    self.process_message(message)
            else:
                # No messages - consumer can do other work or sleep
                time.sleep(0.1)
````

* **Pros**: Consumer controls pace, can handle backpressure 
* **Cons**: Polling overhead, higher latency

### Push Model

````python
class PushBasedConsumer:
    def __init__(self, pubsub_system):
        self.pubsub = pubsub_system
        self.message_buffer = queue.Queue(maxsize=1000)
    
    def subscribe(self, topic):
        # Register callback for real-time message delivery
        self.pubsub.subscribe(topic, self.on_message_received)
    
    def on_message_received(self, message):
        try:
            # Messages pushed immediately when available
            self.message_buffer.put(message, timeout=1)
        except queue.Full:
            # Handle backpressure - maybe drop or apply different strategy
            self.handle_overflow(message)
    
    def process_messages(self):
        while True:
            try:
                message = self.message_buffer.get(timeout=1)
                self.process_message(message)
                self.message_buffer.task_done()
            except queue.Empty:
                continue
````

- **Pros**: Lower latency, immediate delivery
- **Cons**: Can overwhelm consumers, harder backpressure handling

NOTE: below 2 topics are covered in network notes

### Websockets Based Real-time System

### SSE (Server Sent Events)

## Popular Technologies and Use Cases

| **Technology** | **Type** | **Strengths**                         | **Use Cases**                              |
| -------------- | -------- | ------------------------------------- | ------------------------------------------ |
| Apache Kafka   | Stream   | High throughput, durability, ordering | Event sourcing, analytics, log aggregation |
| RabbitMQ       | Broker   | Reliability, flexible routing, AMQP   | Task queues, RPC, complex routing          |
| Redis Pub/Sub  | Pub/Sub  | Low latency, simple                   | Real-time notifications, caching events    |
| Amazon SQS     | Queue    | Managed, scalable, reliable           | Decoupling microservices, async processing |
| Apache Pulsar  | Stream   | Multi-tenancy, geo-replication        | Enterprise messaging, IoT                  |
| NATS           | Pub/Sub  | Lightweight, high performance         | Microservices communication, IoT           |

## Advanced Patterns

### Event Sourcing Pattern

````python
class EventSourcingSystem:
    def __init__(self):
        self.event_store = EventStore()
        self.snapshots = SnapshotStore()
        self.projections = ProjectionManager()
    
    async def handle_command(self, aggregate_id, command):
        # Load current state from events
        events = await self.event_store.get_events(aggregate_id)
        aggregate = self.rebuild_aggregate(events)
        
        # Process command and generate new events
        new_events = aggregate.handle_command(command)
        
        # Store new events
        for event in new_events:
            await self.event_store.append_event(aggregate_id, event)
            
            # Update projections in real-time
            await self.projections.update(event)
        
        return {"status": "success", "events": len(new_events)}
    
    def rebuild_aggregate(self, events):
        # Rebuild aggregate state from events
        aggregate = UserAggregate()
        for event in events:
            aggregate.apply_event(event)
        return aggregate

class UserAggregate:
    def __init__(self):
        self.user_id = None
        self.email = None
        self.status = "inactive"
        self.version = 0
    
    def handle_command(self, command):
        if command['type'] == 'create_user':
            return [self.create_user_event(command)]
        elif command['type'] == 'activate_user':
            return [self.activate_user_event(command)]
        # ... other commands
    
    def apply_event(self, event):
        if event['type'] == 'user_created':
            self.user_id = event['user_id']
            self.email = event['email']
        elif event['type'] == 'user_activated':
            self.status = "active"
        
        self.version += 1
````

### CQRS (Command Query Responsibility Segregation)

````python
class CQRSSystem:
    def __init__(self):
        self.command_bus = CommandBus()
        self.query_bus = QueryBus()
        self.event_store = EventStore()
        self.read_models = ReadModelStore()
    
    # Command side (writes)
    async def execute_command(self, command):
        handler = self.command_bus.get_handler(command.type)
        events = await handler.execute(command)
        
        # Store events
        for event in events:
            await self.event_store.append(event)
            
            # Update read models asynchronously
            await self.update_read_models(event)
        
        return events
    
    # Query side (reads)
    async def execute_query(self, query):
        handler = self.query_bus.get_handler(query.type)
        return await handler.execute(query)
    
    async def update_read_models(self, event):
        # Update denormalized views for fast queries
        if event.type == "order_created":
            await self.read_models.update_user_order_summary(
                event.user_id, event
            )
            await self.read_models.update_product_popularity(
                event.product_id, event
            )
````

### Backpressure Handling

````python
class BackpressureHandler:
    def __init__(self, max_queue_size=10000, overflow_strategy="drop_oldest"):
        self.max_queue_size = max_queue_size
        self.overflow_strategy = overflow_strategy
        self.message_queue = asyncio.Queue(maxsize=max_queue_size)
        self.dropped_messages = 0
    
    async def enqueue_message(self, message):
        try:
            # Try to add message to queue
            self.message_queue.put_nowait(message)
        except asyncio.QueueFull:
            # Apply overflow strategy
            if self.overflow_strategy == "drop_oldest":
                # Remove oldest message and add new one
                try:
                    self.message_queue.get_nowait()
                    self.message_queue.put_nowait(message)
                    self.dropped_messages += 1
                except asyncio.QueueEmpty:
                    pass
            
            elif self.overflow_strategy == "drop_newest":
                # Drop the new message
                self.dropped_messages += 1
                return False
            
            elif self.overflow_strategy == "block":
                # Wait for space (can cause backpressure up the chain)
                await self.message_queue.put(message)
            
            elif self.overflow_strategy == "spill_to_disk":
                # Spill to slower storage
                await self.disk_overflow.store(message)
        
        return True
    
    async def process_messages(self):
        while True:
            try:
                message = await self.message_queue.get()
                await self.process_single_message(message)
                self.message_queue.task_done()
            except Exception as e:
                # Handle processing errors
                await self.handle_processing_error(message, e)
````

### Message Deduplication

````python
class DeduplicationManager:
    def __init__(self, window_size=3600):  # 1 hour dedup window
        self.window_size = window_size
        self.seen_messages = {}  # message_id -> timestamp
        self.cleanup_interval = 300  # 5 minutes
        
        # Start cleanup task
        asyncio.create_task(self.cleanup_expired())
    
    async def is_duplicate(self, message_id):
        current_time = time.time()
        
        # Clean up expired entries
        if message_id in self.seen_messages:
            if current_time - self.seen_messages[message_id] < self.window_size:
                return True  # Duplicate within window
            else:
                del self.seen_messages[message_id]  # Expired
        
        # Mark as seen
        self.seen_messages[message_id] = current_time
        return False
    
    async def cleanup_expired(self):
        while True:
            current_time = time.time()
            expired_keys = [
                msg_id for msg_id, timestamp in self.seen_messages.items()
                if current_time - timestamp >= self.window_size
            ]
            
            for key in expired_keys:
                del self.seen_messages[key]
            
            await asyncio.sleep(self.cleanup_interval)

# Usage with message processor
class DeduplicatedProcessor:
    def __init__(self):
        self.dedup_manager = DeduplicationManager()
    
    async def process_message(self, message):
        message_id = message.get('id') or self.generate_message_id(message)
        
        if await self.dedup_manager.is_duplicate(message_id):
            # Skip duplicate message
            return {"status": "duplicate", "message_id": message_id}
        
        # Process unique message
        result = await self.business_logic(message)
        return result
````

## Interview Tips & Common Questions

### Common Interview Questions

1. "How would you design a notification system?"
   - Use pub/sub for broadcasting
   - Queue for reliable delivery
   - Different channels (email, SMS, push)
   - User preferences and targeting
2. "Explain the difference between Kafka and RabbitMQ"
   - Kafka: Stream platform, high throughput, ordering
   - RabbitMQ: Message broker, flexible routing, lower latency
3. "How do you handle message ordering?"
   - Single partition for global ordering
   - Partition by key for per-entity ordering
   - Trade-offs between ordering and throughput
4. "What happens if a consumer is slower than producer?"
   - Backpressure handling
   - Queue overflow strategies
   - Scaling consumers

### Design Considerations Checklist

**Reliability**:

-  Message durability requirements
-  Delivery guarantees (at-least-once, exactly-once)
-  Error handling and retry strategies
-  Dead letter queue implementation

**Performance**:

-  Throughput requirements (messages/second)
-  Latency requirements (real-time vs batch)
-  Scaling strategy (horizontal vs vertical)
-  Backpressure handling

**Ordering**:

-  Global vs partition-level ordering
-  Out-of-order message handling
-  Late-arriving messages

**Monitoring**:

-  Message lag monitoring
-  Consumer health checks
-  Error rate tracking
-  Throughput metrics

**Key Takeaways**:

- **Choose based on use case**: Task queues vs event streams vs real-time
- **Consider trade-offs**: Throughput vs latency vs complexity
- **Plan for failures**: Retries, dead letters, monitoring
- **Start simple**: Can always add complexity later
- **Measure everything**: Monitor performance and adjust