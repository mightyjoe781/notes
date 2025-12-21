# Messaging and Streaming Systems

## Asynchronous Processing

![](assets/Pasted%20image%2020251221201204.png)


* user sent the request to API and immediately got the response is called as synchronous processing.
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
* Brokers can re-queue the message if not deleted by consumer (Visibility Timeout). After multiple failed retries it maybe put into a Dead-Letter Queue

## Message Stream (Kinesis, Kafka, etc.)

Let's assume in above example, workers perform two tasks, Update the DB and Writes to Elastic Search.

Then there are two approached to solve the problem,

Approach - 1 : One Message Brokers and add logic in consumers.

![](assets/Pasted%20image%2020251221202105.png)

Here process-1 & process-2, if either failed then we will not be able to process both events correctly, there is no co-ordination between workers and indexing 

Approach 2 : Two brokers & two set of consumers

- API server Writes to two brokers and each has its own set of consumers, (solves issue with partial complete writes)
* Issue - when API server writes to two RabbitMQ, one of them fails, we end up with original problem.

![](assets/Pasted%20image%2020251221202307.png)

Solution: write once, but read by many systems - Kafka, Kinesis try to solve this problem.

Approach 3 : Message Streams

Similar to Message Queue except there could be multiple consumers reading from the same stream.

![](assets/Pasted%20image%2020251221202730.png)

Message Queue vs Message Streams

* In Message Queue, consumers consume a message once while in Kinesis a specific consumer group consumes the message once (usually tracked by checkpoint)

### Kafka Essentials

* Kafka is a message stream that holds the messages. Internally Kafka has topics, with `n` partitions
* Message is sent to a topic, and depending on the configured hash key it is put into a partition.
* Within that partition, messages are ordered (no order guarantee, across partitions) 
* Limitation of Kafka : number of consumer = number of partition
* In Kafka, each consumer can commit their checkpoints. And deletion of messages happens based on the expiry time.

## Realtime Pub/Sub Systems

![](assets/Pasted%20image%2020251221203252.png)

* Both Message Broker and Streams, requires consumers to `pull` messages out (poll).
* Advantage : Consumers can pull at their own pace, and consumers don’t get overwhelmed
* Disadvantage: Consumption lag when high ingestion.

What if we want low latency  Zero Lag ? --> realtime pub-sub

* Instead of consumers pulling the message, the message is pushed to them.
* This way we get really fast delivery time, but can overwhelm the consumers if they are not able to process the message fast (usually we use queue at each consumer)
* Practical UseCase : Message Broadcast, Configuration Push, All systems receive updates without polling for data.

NOTE: Since SNS pushes messages to the services, if services fail to process or can't accept the message, then it will not be processed, As a general safeguard, we usually pair it with a Message Queue like SQS.

![](assets/Pasted%20image%2020251221203332.png)
