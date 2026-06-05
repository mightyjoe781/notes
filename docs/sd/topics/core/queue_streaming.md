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

**When to Use Asynchronous Processing (Queues)**

Use Cases:

- **Async work** - user doesn't need an immediate result (email sending, image processing, report generation). Litmus test: does the user need the result *right now*? If no, queue it.
- **Bursty traffic** - absorb traffic spikes without dropping requests; queue acts as a buffer, worst case is a delay not an error
- **Decoupling** - producer and consumer have different scaling or hardware needs (e.g. lightweight upload servers vs GPU-heavy processing workers)
- **Reliability** - can't afford to lose work; queue holds messages until a downstream service comes back online

**When NOT to Use Queues**

If you have strict latency requirements (e.g. sub-500ms response), a queue will almost certainly break that constraint. You've now added the round-trip of enqueueing, the consumer picking it up, processing it, and getting the result back to the client. Don't introduce a queue into a synchronous workload - queues are for work you can afford to do *later*, even if later is a few seconds from now.

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

## Acknowledgements & Duplicate Prevention

When a consumer pulls a message, the queue does **not** delete it immediately. The consumer must send an explicit **ACK** (acknowledgement) back after successful processing. If the consumer crashes before ACK-ing, the queue redelivers the message to another consumer - nothing is lost.

The problem: while worker A is processing and hasn't ACK'd yet, worker B could grab the same message and do duplicate work. Each queue system handles this differently:

| System   | Approach |
| -------- | -------- |
| SQS      | **Visibility timeout** - message becomes invisible to all other consumers for a configurable window (e.g. 30s). If no ACK in time, becomes visible again for retry. |
| Kafka    | Assigns each partition to **exactly one consumer** in a group - no competition in the first place. |
| RabbitMQ | Channel-level **prefetch limits** + ACK timeouts. |

The concept is always the same: only one consumer actively processes a message at a time.

## Message Brokers vs Message Streams

#### Message Brokers (Traditional Queues)

Examples: RabbitMQ, ActiveMQ, Amazon SQS

**Characteristics**:

- **Message deletion** after consumption
- **Push or pull** based delivery
- **Transactional** semantics
- **FIFO ordering** within queue

#### Message Streams (Event Logs)

**Examples**: Apache Kafka, Amazon Kinesis, Apache Pulsar

**Characteristics**:

- **Messages retained** for configured time (not deleted after consumption)
- **Offset-based** consumption
- **Replay capability** - reprocess past messages if a consumer had a bug
- **Partitioned** for horizontal scale

| Feature             | Message Brokers            | Message Streams            |
| ------------------- | -------------------------- | -------------------------- |
| Message Persistence | Deleted after Consumption  | Retained for time Period   |
| Consumption Model   | Each message consumed once | Message can be replayed    |
| Ordering            | FIFO within queue          | Ordered within a partition |
| Scalability         | Vertical Scaling           | Horizontal Scaling         |
| Use Cases           | Task Queues, RPC           | Event Sourcing, Analytics  |

#### Technology Comparison

**Kafka** - recommended default for interviews
- Persists messages to disk, replicated across brokers (fault tolerant)
- Configurable retention (days, weeks, forever)
- Replay: if consumers go offline for an hour, they catch up on restart; if consumer had a bug, point a new consumer to replay from before the bug
- Consumer groups + partitions for horizontal scale

**SQS (Amazon Simple Queue Service)**
- Fully managed, no infrastructure to worry about
- Two flavors:
    - **Standard queue** - best-effort ordering, very high throughput
    - **FIFO queue** - strict ordering guaranteed, lower throughput
- Visibility timeout prevents duplicate processing
- Good choice when you want simplicity in the AWS ecosystem

**RabbitMQ**
- Traditional message broker
- Supports complex **routing patterns** via exchanges and bindings
- Less common in system design interviews
- Useful when sophisticated message routing logic is needed

## Message Ordering & Durability

### Message Ordering

![](assets/Pasted%20image%2020251224183233.png)

- Total Ordering
    - Pros: Ensures a strict ordering
    - Cons: Single point of bottleneck, no parallelism
- Partition-Level Ordering
    - Pros: Parallel processing, ordering guaranteed within a partition
    - Cons: No global ordering across partitions

**Partition Key Selection**

The partition key determines which messages go to which partition. Two competing concerns:

- **Ordering** - messages with the same key always go to the same partition, so they stay ordered. E.g. use `account_id` for bank transactions so deposit and withdrawal for the same account can't be reordered.
- **Even distribution** - if one key has far more traffic than others you get a **hot partition** where one consumer is slammed while others are idle. E.g. partitioning a ride-sharing app by `city` puts all New York traffic on one partition while Boise sits empty.

The key that gives you ordering is often not the key that gives you even distribution - this trade-off is worth discussing in an interview.

**Partitioning Strategies**

- User-based partitioning (orders for same users stay ordered)
- Time-based partitioning (events in time-windows)
- Content-based partitioning (similar events grouped)

**Consumer Groups**

A consumer group is a pool of workers that divides partitions amongst themselves. With 6 partitions and 3 consumers, each consumer handles 2 partitions. Adding more consumers increases throughput - but you cannot have more consumers than partitions (the extra consumer gets nothing).

### Durability Guarantees

- At-Most-Once Delivery
    - No duplicates, but messages may be lost
    - Use for: metrics, logs, analytics - where losing a few data points is acceptable
- At-Least-Once Delivery
    - Messages always delivered, but may have duplicates
    - **Most common pattern** - almost always the right answer in interviews
    - Requires **idempotent consumers** (see below)
    - Use exponential backoff in retry with a max retry limit, then DLQ
- Exactly-Once Delivery
    - Every message processed exactly once
    - Extremely hard to achieve in distributed systems
    - Kafka supports a form of it within its own ecosystem, but with real trade-offs
    - **Don't promise this in an interview unless you can explain the mechanism**

### Idempotency

An idempotent operation produces the same result no matter how many times it's run. Required when using at-least-once delivery.

**Non-idempotent (bad):**
```
"Increment user 123's post count by 1"
# Running twice → count goes up by 2, not 1
```

**Idempotent (good):**
```
"Set user 123's post count to 54"
# Running twice → count is still 54
```

Design operations to be naturally idempotent (set vs increment), or check whether the action was already completed before executing.
## Retry Mechanisms Implementations

[Amazing Article by Amazon on Exponential Backoff](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)

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

Happens when producers generate messages faster than consumers can process them. The queue grows indefinitely and eventually exhausts memory. **A queue delays a capacity problem - it doesn't solve it.**

Example: receiving 300 msg/s but consumers handle 200 msg/s - queue grows by 100 msg/s and will never catch up.

Options:
1. **Scale consumers** - autoscale based on queue depth; add more partitions if at the consumer-per-partition ceiling
2. **Apply back pressure to producers** - reject new messages or return an error to the client ("system busy, retry in a minute"), slowing the source down
3. **Monitor and alert** - set alerts on queue depth so you catch this early

### Poisoned Messages

A message that consistently fails to process - e.g. a corrupted file that will never succeed no matter how many retries.

Without guard rails: retries forever, consuming a consumer's resources indefinitely while all other messages are stuck behind it.

**Solution - Dead Letter Queue (DLQ)**:
- Configure a **max retry count** (e.g. 5 attempts)
- After exceeding retries, shunt the message to a **separate DLQ** instead of the main queue
- Main queue keeps processing; failed messages sit in DLQ for manual inspection or automated analysis
- Mentioning DLQ proactively in interviews signals production experience

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