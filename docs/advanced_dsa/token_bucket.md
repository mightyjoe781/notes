# Token Bucket
*Rate Limiting & Traffic Shaping*

The token bucket algorithm is widely used for rate limiting. It is simple, well understood and commonly used by internet companies.

The token bucket algorithm works as follows :

- A bucket is a container that has pre-defined capacity.
- Token are put in bucket at preset rates periodically. Once the bucket is full no more tokens can be added.
- Each request consumes one token. When a request arrives, we check if there are enough tokens in the bucket

![](assets/Pasted%20image%2020260222135233.png)

Pros:

- The algorithm is easy to implement
- Memory Efficient
- Token bucket allows a burst of traffic for short periods. A request can go through as long as there are tokens left.

Cons

- Two parameters in the algorithm are bucket size and token refill rate. However, it mightbe challenging to tune them properly.

## Leaking Bucket Algorithm

Leaking bucket algorithm is similar to token bucket except that requests are processed at a fixed rate.

It is usually implemented with FIFO queue.

- When a request arrives, the system checks if the queue is full. If it is not full, the request is added to the queue.
- Otherwise, the request is dropped.
- Requests are pulled from the queue and processed at regular intervals.

![](assets/Pasted%20image%2020260222134632.png)

Leaking bucket algorithm takes two parameters

- Bucket Size : equal to queue size, queue holds the request to be processed at fixed rate
- Outflow rate : defines how many request can be processed at a fixed rate, usually in seconds

Pros:

- Memory efficient given the limited queue size.
- Requests are processed at a fixed rate therefore it is suitable for use cases that a stable outflow rate is needed.

Cons:

- A burst of traffic fills up the queue with old requests, and if they are not processed in time, recent requests will be rate limited.
- There are two parameters in the algorithm. It might not be easy to tune them properly.

## Other Algorithms

### Fixed Window Counter Algorithm

Fixed window counter algorithm works as follows:

- The algorithm divides the timeline into fix-sized time windows and assign a counter for  each window.
- Each request increments the counter by one.
- Once the counter reaches the pre-defined threshold, new requests are dropped until a new time window starts.

Pros:

- Memory efficient
- Easy to understand.
- Resetting available quota at the end of a unit time window fits certain use cases.

Cons:

- Spike in traffic at the edges of a window could cause more requests than the allowed quota to go through.
### Sliding Window Log Algorithm

### Sliding Window Counter Algorithm

