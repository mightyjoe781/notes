---
title: Messaging and Streaming Systems
description: Covers asynchronous processing with message brokers, delivery guarantees, Kafka-style message streams, and realtime pub/sub systems.
tags:
  - concept
---

# Messaging and Streaming Systems

>    Move data, don’t wait for it.
## Asynchronous Processing

![](assets/Pasted%20image%2020251221201204.png)


* When a user sends a request to an API and immediately gets a response, this is called synchronous processing.
* Ex - loading feed, login, payments.
* Asynchronous Systems usually will accept the user payload and forward it to message brokers which will pass this work to workers. User will not wait for response and get back some id to track status of the work, and When workers complete their task, they can just update the DB & status of the task.
* There are three ways of message passing:
    * Message Brokers
    * Message Streams
    * Notification(Pub/Sub) Systems
## Message Brokers and Queues

Brokers help two services/application communicate through messages. We use message brokers when we want to do something *asynchronous*. For example, in above example broker helped us to connect API with Workers.

* Long Running Tasks
* Trigger Dependent tasks across machines

Features of Message Brokers

* Brokers help us connect different sub-systems
* Brokers acts as a buffer for the messages, allowing consumers to consume messages at their pace. Ex - Notification service
* Brokers can retain messages for `n` days
* **ACK mechanism** - queue does not delete a message when a consumer picks it up; the consumer must explicitly ACK it after successful processing. If the consumer crashes before ACK-ing, the message is redelivered to another consumer.
* Brokers can re-queue the message if not ACK'd in time (Visibility Timeout in SQS). After multiple failed retries, the message is put into a **Dead-Letter Queue (DLQ)**.
* **Poisoned messages** - a message that consistently fails (e.g. corrupted payload) will keep retrying forever and block the queue. DLQ solves this: configure a max retry count, then shunt failures to DLQ for manual inspection while the main queue keeps moving.

**Delivery Guarantees**

- **At-most-once** - fire and forget, message deleted immediately on pickup. May be lost. Use for metrics/analytics where some loss is acceptable.
- **At-least-once** - message guaranteed to be delivered but may be delivered more than once. Requires **idempotent consumers** (processing the same message twice must produce the same result). Almost always the right answer.
- **Exactly-once** - very hard in distributed systems, avoid promising this in interviews unless you can defend the mechanism.

**Idempotency example**: "set user's post count to 54" is idempotent (running twice is fine); "increment post count by 1" is not (running twice gives wrong result).

**When NOT to use a queue**

If you have strict latency requirements (e.g. sub-500ms), a queue will break that constraint - you've added the enqueue + consumer pickup + processing roundtrip. Queues are for work you can afford to do *later*.

**Backpressure**

If producers generate messages faster than consumers can process them, the queue grows unboundedly - it delays the capacity problem, doesn't solve it. 

Options: scale consumers, or apply back pressure to producers (reject/rate-limit incoming messages).

## Message Stream (Kinesis, Kafka, etc.)

Let's assume in above example, workers perform two tasks, Update the DB and Writes to Elastic Search.

Then there are two approaches to solve the problem,

Approach - 1 : One Message Broker, adding logic in consumers.

![](assets/Pasted%20image%2020251221202105.png)

Here process-1 & process-2, if either failed then we will not be able to process both events correctly, there is no co-ordination between workers and indexing 

Approach 2 : Two brokers & two set of consumers

- API server Writes to two brokers and each has its own set of consumers, (solves issue with partial complete writes)
* Issue - when API server writes to two RabbitMQ instances and one of them fails, we end up with the original problem.

![](assets/Pasted%20image%2020251221202307.png)

Solution: write once, but read by many systems - Kafka, Kinesis try to solve this problem.

Approach 3 : Message Streams

Similar to Message Queue except there could be multiple consumers reading from the same stream.

![](assets/Pasted%20image%2020251221202730.png)

Message Queue vs Message Streams

* In a Message Queue, consumers consume a message once; while in Kinesis, a specific consumer group consumes the message once (usually tracked by checkpoint)

### Kafka Essentials

* Kafka is a message stream that holds messages. Internally Kafka has topics with `n` partitions.
* Message is sent to a topic, and depending on the configured **partition key** it is put into a partition.
* Within a partition, messages are ordered (no order guarantee across partitions).
* **Consumer groups** - a pool of workers dividing partitions amongst themselves. 6 partitions + 3 consumers = each consumer handles 2 partitions. Adding a 7th consumer when you only have 6 partitions does nothing - there's no partition left for it.
* Limitation: number of active consumers per group = number of partitions (ceiling).
* In Kafka, each consumer commits their own checkpoint (offset). Message deletion happens based on expiry time, not consumption - so messages can be replayed.
* **Replay** - if a consumer had a bug, point a new consumer to an earlier offset and reprocess. Consumers going offline don't lose messages; they just catch up on restart.

**Partition key trade-off**: the key that gives ordering (e.g. `account_id` for bank transactions) may not give even distribution. A bad key creates a **hot partition** where one consumer is overwhelmed while others are idle (e.g. partitioning a ride-sharing app by `city` - New York gets everything, Boise gets nothing). Choose accordingly.

## Realtime Pub/Sub Systems

![](assets/Pasted%20image%2020251221203252.png)

* Both Message Broker and Streams, requires consumers to `pull` messages out (poll).
* Advantage : Consumers can pull at their own pace, and consumers don’t get overwhelmed
* Disadvantage: Consumption lag when high ingestion.

What if we want low latency, zero lag? --> realtime pub-sub

* Instead of consumers pulling the message, the message is pushed to them.
* This way we get really fast delivery time, but can overwhelm the consumers if they are not able to process the message fast (usually we use queue at each consumer)
* Practical UseCase : Message Broadcast, Configuration Push, All systems receive updates without polling for data.

NOTE: Since SNS pushes messages to the services, if services fail to process or can't accept the message, then it will not be processed, As a general safeguard, we usually pair it with a Message Queue like SQS.

![](assets/Pasted%20image%2020251221203332.png)
