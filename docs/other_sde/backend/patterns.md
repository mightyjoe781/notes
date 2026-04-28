# Communication Design Patterns

## Request/Response

- Client sends a request
- Server parses and processes it
- Server sends a response
- Client parses the response and consumes it

![](assets/Pasted%20image%2020251004003608.png)

### Where It Is Used

- Web, HTTP, DNS, SSH
- RPC (Remote Procedure Call)
- SQL and database protocols
- APIs (REST, SOAP, GraphQL)

### Anatomy of a Request/Response

- A request structure is defined by both client and server
- Request has a boundary defined by the protocol and message format

![](assets/Pasted%20image%2020251004004311.png)

Building an upload image service with request/response:

- Send the full image in a single request (simple)
- Chunk the image and send one request per chunk (resumable)

**Doesn't work well for:**

- Notification services
- Chat applications
- Very long-running requests
- Scenarios where the client may disconnect

## Synchronous vs Asynchronous Workloads

### Synchronous I/O

- Caller sends a request and blocks until a response is received
- No code executes on the caller side during the wait
- Caller and receiver are in sync

Example: program asks the OS to read from disk → main thread is suspended → read completes → program resumes.

### Asynchronous I/O

- Caller sends a request and continues executing
- Caller either polls for the result (`epoll`) or receives a callback (`io_uring`), or spins up a blocking thread
- Caller and receiver are not necessarily in sync

Example: program spawns a secondary thread → thread reads from disk and blocks → main thread continues → thread calls back when done.

### Synchronous vs Asynchronous in Request/Response

Synchronicity is a client-side property. Most modern client libraries are asynchronous — they send an HTTP request and continue doing work.

Examples:

- Async programming (promises/futures)
- Async backend processing
- Async commits in PostgreSQL
- Async I/O in Linux (`epoll`, `io_uring`)
- Async replication
- Async `fsync` (filesystem cache)

## Push

### Push Model

- Client connects to a server
- Server sends data to the client without the client polling
- Protocol must be bidirectional
- Used by: RabbitMQ

**Pros:**

- Real-time

**Cons:**

- Client must remain online
- Client may be unable to handle the load
- Requires a bidirectional protocol
- Polling is preferred for lightweight clients

## Short Polling

### What Is Short Polling

- Client sends a request
- Server responds immediately with a handle
- Server continues processing in the background
- Client uses the handle to poll for status via repeated short requests

![](assets/Pasted%20image%2020251004095154.png)

**Pros:**

- Simple
- Good for long-running requests
- Client can disconnect between polls

**Cons:**

- Chatty (many requests)
- Wastes network bandwidth and backend resources

## Long Polling

*Used by Kafka*

- Client sends a request
- Server responds immediately with a handle
- Server continues processing in the background
- Client polls with the handle, but the server **does not respond until it has a result**
- Some variants include a timeout

![](assets/Pasted%20image%2020251004095458.png)

**Pros:**

- Less chatty than short polling
- Client can still disconnect

**Cons:**

- Not real-time

## Server-Sent Events (SSE)

- Client sends a single request
- Server streams logical events as part of the response, never writing the final end-of-response
- Client parses the stream, looking for events
- Works over standard HTTP

![](assets/Pasted%20image%2020251004100619.png)

**Pros:**

- Real-time
- Compatible with standard HTTP request/response

**Cons:**

- Client must remain online
- Client may be unable to handle the load
- Polling preferred for lightweight clients
- HTTP/1.1 connection limit (6 per domain)

## Publish/Subscribe (Pub/Sub)

![](assets/Pasted%20image%2020251004101518.png)

**Pros:**

- Scales with multiple receivers
- Great for microservices
- Loose coupling
- Works even when clients are offline

**Cons:**

- Message delivery issues (two generals problem)
- Added complexity
- Risk of network saturation

## Multiplexing vs Demultiplexing

*(HTTP/2 proxying vs connection pooling)*

![](assets/Pasted%20image%2020251004111035.png)

### Multiplexing — HTTP/2

![](assets/Pasted%20image%2020251004111424.png)

### Multiplexing — HTTP/2 on the Backend

![](assets/Pasted%20image%2020251004111652.png)

![](assets/Pasted%20image%2020251004111749.png)

### Connection Pooling

![](assets/Pasted%20image%2020251004112041.png)

Chrome allows up to 6 connections per domain in its connection pool.

## Stateful vs Stateless

- **Stateful**: server stores client state in memory and depends on it being there
- **Stateless**: client sends all necessary state with every request; server can lose it safely

### Stateless Backends

- Can store state externally (e.g., a database) while remaining stateless themselves
- A stateless backend can restart at any time without breaking in-flight client workflows

### Stateless vs Stateful Protocols

- **TCP** — stateful (sequence numbers, connection file descriptors)
- **UDP** — stateless (DNS adds a query ID; QUIC adds a connection ID)
- You can build a stateless protocol on top of a stateful one and vice versa
    - HTTP runs over TCP; if TCP breaks, HTTP opens a new connection transparently
    - QUIC runs over UDP

### Completely Stateless Systems

Rare. Examples:

- A pure function endpoint (e.g., "is this number prime?")
- JWT — all session state is encoded in the token

## Sidecar Pattern

Every protocol requires a library, and coupling your application to that library creates long-term problems:

- Library and application must use the same language
- Changing the library requires regression testing
- Backward-compatibility concerns on upgrades
- Difficult to add features across a microservices fleet

### Delegating Communication to a Proxy

Instead of embedding protocol logic in the application:

- A **sidecar proxy** runs alongside each service
- The proxy holds the rich protocol library
- The application uses a thin client (e.g., HTTP/1.1)

![](assets/Pasted%20image%2020251004115546.png)

![](assets/Pasted%20image%2020251004115637.png)

### Sidecar Examples

- Service mesh proxies: Linkerd, Istio, Envoy
- Sidecar proxy containers
- Must be a Layer 7 proxy
