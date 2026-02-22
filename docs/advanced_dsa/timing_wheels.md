# Hierarchical Timing Wheels
 *Efficient time management at scale*

Problem : Suppose you need to support 10 million timers, with different expiration times. Frequent Insertions & Cancellations with millisecond precision.

Naive Solutions would involve keeping a sorted list, but we could easily optimize that and keep a priority queue to handle this.

But with millions of timers -> becomes expensive.

```
O(1) insert
O(1) expire
O(1) delete (amortized)
```

thats what timing wheel provide

## Basic Timing Wheel

Imagine a circular array

![](assets/Pasted%20image%2020260222114309.png)

Here 1 slot = 1 second, 60 slots -> covers 60 seconds

When time advances :

- Pointer moves to next slot
- Execute all timers in that bucket

*Usually we use DelayQueue (Java) to drive the clock, this helps remove the empty ticks in case of a very sparse request queued in the Wheel.*

### How It Works

To schedule a timer for a delay d

```python
slot = (current_time + d) % wheel_size
```

Insert timer in that bucket
When pointer reached that slots -> execute.

### Problem ? Limited Range

If wheel size = 60 seconds. How do we schedule something for 2 hours ? We need something bigger.

## Hierarchical Timing Wheel

Instead of one wheel, use multiple wheels,

Think something like this

```
Seconds Wheel
Minutes Wheel
Hours Wheel
Days Wheel
```

Also NOTE: Wheel doesn't need to granular till 1 sec or slot, we can choose resolution for the wheel as we desire.

![](assets/Pasted%20image%2020260222115106.png)

Another Example

- Level 0 : 256 slots
    - 1ms per tick : covers 256 ms
- Level 1 : 256 slots
    - 256 ms per tick : covers 65s
- Level 2 : 256 slots
    - 65s per tick : covers 4.6 hours

### Core Idea

If delay fits in lowest wheel -> put there.

If too large:

- Place in higher level wheel.
- When higher level slot expires, move timers down to lower wheel.

This is called cascading.

### Timer Insertion Logic

Given delay d:

1. If d < level0_range -> insert into level 0
2. Else if d < level1_range -> insert into level 1
3. Else -> next level
4. And so on

### Cascading

When a higher-level slot expires:

- Its timers are redistributed into lower-level wheel.
- Eventually end up in level 0.
- Finally executed.

### Real World Use Cases

|**System**|**Usage**|
|---|---|
|Kafka|Request timeouts|
|Netty|HashedWheelTimer|
|Linux Kernel|Timer management|
|Redis|Expiration scheduling|
|Akka|Actor timeouts|

### TradeOffs


- Tick granularity limits precision.
- Cascading adds complexity.
- Large memory footprint if too many slots.
- Not ideal if timers are extremely sparse and huge range.

| **Feature**     | **Heap**    | **Timing Wheel** |
| --------------- | ----------- | ---------------- |
| Insert          | O(log n)    | O(1)             |
| Expire          | O(log n)    | O(1)             |
| Memory locality | Poor        | Excellent        |
| Precision       | High        | Tick-based       |
| Best for        | Small scale | Massive scale    |


### Resources

- [Apache Kafka, Purgatory, and Hierarchical Timing Wheels](https://www.confluent.io/blog/apache-kafka-purgatory-hierarchical-timing-wheels/)
- [Adrian Colyer](https://blog.acolyer.org/2015/11/23/hashed-and-hierarchical-timing-wheels/)
- [Rewriting Pushpin's connection manager in Rust](https://blog.fanout.io/2020/08/11/rewriting-pushpins-connection-manager-in-rust/)
- [Bartosz Zbytniewski explanation on Above Article](https://zbysiu.dev/til/hierarchical-timing-wheels/)

