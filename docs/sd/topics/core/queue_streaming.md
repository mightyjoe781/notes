# Message Queues & Streaming

## Messaging Fundamentals

**Synchronous Processing**

![](assets/Pasted%20image%2020251224180328.png)

Characteristics:

* client waits for response
* blocking operation
* immediate feedback
* tight coupling

Examples: Login, Payment Processing, Real-time Validation

**Asynchronous Processing**

![](../../hld/beginner/assets/Pasted%20image%2020251221201204.png)
Characteristics:

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

![](assets/Pasted%20image%2020251224182101.png)

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

![](assets/Pasted%20image%2020251224182112.png)

**Characteristics**:

- **One-to-many** communication
- Each message delivered to **all** subscribers
- **Broadcast** pattern
- Message **copied** to all consumers

**Use Cases**:

- **Event broadcasting**: User actions, system events
- **Real-time updates**: Stock prices, live scores
- **Notification systems**: Multiple services need same data

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

![](assets/Pasted%20image%2020251224183233.png)

- Total Ordering
    - Pros: Ensures a strict ordering
    - Cons: Single Point of BottleNeck, No Parallelism
- Partition-Level Ordering
    - Pros: Parallel Processing, Partition-Level Ordering
    - Cons: No Global ordering across Partitions

Different Types of Ordering Strategy that can be employed are

- User-Based Partitioning (orders for same users stay ordered)
- Time-Based Partitioning (events in time-windows)
- Content-Based Partitioning (similar events grouped)

### Durability Guarantees

- At-Most-Once Delivery
    - No Duplicated, but messages may be lost
    - Metrics, Logs, where its acceptable to lose some data
- At-Least-Once Delivery
    - Messages delivered, but may have duplicates
    - Most Common Pattern, Requires Idempotent Consumers
    - Use Exponential Backoff in Retry for delivery with some limit.
- Exactly-Once Delivery
    - Messages are delivered Once
    - Financial transactions, critical operations.
    - Usually people use idempotency as well with this.
## Retry Mechanisms Implementations

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

NOTE: we can add some jitter as well in Exponential Backoff.

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

## Stream Processing vs Batch Processing

### Batch Processing

**Definition**: Process large volumes of data in discrete chunks

**Characteristics**:

- **High throughput**: Process large volumes efficiently
- **High latency**: Results available after batch completion
- **Resource efficiency**: Optimized for bulk operations
- **Complexity**: Simpler programming model

**Use Cases**: ETL jobs, daily reports, data warehousing

### Stream Processing

**Definition**: Process data continuously as it arrives

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
| Data Volume    | Large Bounded datasets | Continuous unbounded streams |

### Hybrid Approaches

In Big Data we often use following approaches which is a mix of both

- Lambda Architecture
- Kappa Architecture
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

### WebSockets Based Real-time System

### SSE (Server Sent Events)

## Advanced Patterns

### Event Sourcing Pattern
### CQRS (Command Query Responsibility Segregation)
### Backpressure Handling

### Message Deduplication

## Design Considerations

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