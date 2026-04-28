# Backend Execution Patterns

## Process vs Threads

### Process

- A set of instructions with isolated memory
- Has a PID (process identifier)
- Scheduled by the CPU

### Thread

- Lightweight process (LWP)
- A set of instructions
- Shares memory with the parent process
- Has its own ID

![](assets/Pasted%20image%2020251006180634.png)

### Single-Threaded Process

- One process, one thread
- Simple execution model
- Example: Node.js

### Multi-Process

- Multiple independent processes, each with its own memory
- Examples: nginx, PostgreSQL
- More memory usage but strong isolation
- Example: Redis uses copy-on-write (COW) for async snapshotting to disk

### Multi-Threaded

- One process, multiple threads sharing memory
- Takes advantage of multiple cores with lower memory overhead
- Risk of race conditions; requires synchronization (locks, latches)
- Examples: Apache, Envoy

### How Many Is Too Many?

- Excessive processes/threads cause costly CPU context switches
- Rule of thumb: number of processes/threads ≈ number of CPU cores

## Connection Establishment

*SYN / Accept Queues*

- Client connects via TCP three-way handshake (SYN → SYN-ACK → ACK)
- The kernel manages the handshake; the backend calls `accept()`

![](assets/Pasted%20image%2020251006182909.png)

### Detailed Process

1. Kernel creates a socket with a SYN queue and an Accept queue
2. Client sends SYN → kernel adds entry to SYN queue, replies with SYN-ACK
3. Client replies with ACK → kernel moves the entry to the Accept queue
4. Backend calls `accept()` → entry removed from Accept queue, file descriptor created

![](assets/Pasted%20image%2020251006183511.png)

### Problems with Accepting Connections

- Backend is too slow to call `accept()`
- Clients that never send ACK (SYN flood)
- Backlog too small

## Reading and Sending Socket Data

*Receive vs Send Buffers*

- Client sends data → kernel places it in the receive buffer
- Kernel sends ACK and updates the receive window
- Application calls `read()` to copy data out of the buffer

![](assets/Pasted%20image%2020251006184008.png)

### Problems with Reading and Sending

- Backend reads too slowly → receive buffer fills up → client is throttled

## Socket Programming Patterns

Three key roles in socket communication:

- **Listener** — calls `listen()` with address and port; receives a socket ID
- **Acceptor** — calls `accept()` on the socket ID; receives file descriptors for connections (may differ from the listener)
- **Reader/Writer** — reads and writes data on established connections

All three roles can be separate entities/processes, enabling flexible and scalable architectures.

### Flow

Listener → creates socket and listens  
Acceptor → accepts incoming connections  
Reader/Writer → processes data

### Common Patterns

| Pattern | Example |
|---|---|
| Single listener / single worker thread | Node.js |
| Single listener / multiple worker threads | Memcached |
| Single listener / multiple worker threads with load balancing | RAMCloud |
| Multiple acceptor threads on a single socket | nginx (legacy default) |
| Multiple listeners on the same port (`SO_REUSEPORT`) | nginx (modern) |

## Backend Idempotency

*Retrying a request without side effects*

If a client or proxy retries a request (e.g., `POST /comment`), the backend may process it multiple times, producing duplicate records. This is especially harmful in financial systems.

An idempotent request can be retried without affecting the result. The common solution is an **idempotency token** (also called a request ID):

- Client sends a unique `requestId` with each request
- Server checks if `requestId` has already been processed; if so, returns the cached response

In HTTP:

- `GET` is idempotent by specification — browsers and proxies treat it as safe to retry
- `POST` is not idempotent by default, but can be made so with an idempotency token
- Ensure `GET` endpoints have no side effects
