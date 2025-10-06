# Communication Design Patterns

## Request Response

- Client sends a Request
- Server parses the Request
- Server processes the Request
- Server sends a Response
- Client parses the Response and consume

![](assets/Pasted%20image%2020251004003608.png)

### Where it is used ?

- Web, HTTP, DNS, SSH
- RPC (remote procedure call)
- SQL and Database Protocols
- APIs (REST/SOAP/GraphQL)
- Implemented in all kinds of variations

### Anatomy of a Request/Response

- A request structure is defined by both client and server
- Request has a boundary
- Defined by a protocol and message format
- Same for the response

![](assets/Pasted%20image%2020251004004311.png)

Building an upload image service with request/response

- Send large request with the image (simple)
- Chunk image and send a request per chunk (resumable)

Doesn't Work Everywhere

- Notification Service
- Chat Applications
- Very Long Requests
- What if client disconnects
## Synchronous vs Asynchronous workloads

### Synchronous IO

- Caller sends a request and blocks
- Caller cannot execute any code meanwhile
- Receiver responds, Caller unblocks
- Caller and Receiver are in *sync*

Examples

- Program asks OS to read from disk
- Program main thread is taken off of the CPU
- Read completes, program can resume execution

### Asynchronous IO

- Caller sends a request
- Caller can work until it gets a response
- Caller either
    - Checks if the response is ready (*epoll*)
    - Receiver calls back when its done (*io_uring*)
    - spins up a new thread that blocks
- Caller and Receiver are not necessary in sync

Example of an OS asynchronous call

- Program spins up a secondary thread
- Secondary thread reads from disk, OS blocks it
- Main program still running and executing code
- Thread finish reading and calls back main thread

### Synchronous vs Asynchronous in Request Response

- Synchronicity is a client property
- Most modern client libraries are asynchronous
- Clients send an HTTP request and do work

Examples

- Asynchronous Programming (promises/futures)
- Asynchronous backend Processing
- Asynchronous commits in postgres
- Asynchronous IO in Linux (*epoll* , *io_uring*)
- Asynchronous replication
- Asynchronous OS *fsync* (fs cache)

## Push

### Request/Response drawback

- Client wants a real time notification from backend
    - A user just logged in
    - A message is just received
- Push Model is good for certain cases

### Push Model

- Client connects to a server
- Server sends data to the client
- Clients doesn't have to request anything
- Protocol must be bidirectional
- Used by RabbitMQ

### Pros vs Cons

- Pros
    - Real time
- Cons
    - Client must be online
    - Client might not be able to handle
    - Requires bidirectional protocol
    - Polling is preferred for light clients

## Short Polling

Drawbacks for request/response

- A request takes long time to process
    - Upload a youtube video
- The backend wants to send notification
    - A user just logged in
- polling is a good communication style

### What is Short Polling

- Client sends a request
- Server responds immediately with a handle
- Server continues to process the request
- Client uses that handle to check for status
- Multiple *short* request response as polls

![](assets/Pasted%20image%2020251004095154.png)

- Pros
    - Simple
    - Good for long running requests
    - Client can disconnect
- Cons
    - Too Chatty
    - Network Bandwidth
    - Wasted Backend Resource

## Long Polling

- A request takes long time to process
    - Upload a youtube video
- The backend want to sends notification
    - A user just logged in
- Short polling is a good but chatty
- Long Polling (*Kafka* uses it)

### Long Polling

- Client sends a request
- Server responds immediately with a handle
- Server continues to process the request
- Client uses that handle to check for status
- Server DOES not reply until it has the response
- So we got a handle, we can disconnect and we are less chatty
- Some variation has timeouts too

![](assets/Pasted%20image%2020251004095458.png)

- Pros
    - Less chatty and backend friendly
    - Client can still disconnect
- Cons
    - Not real time

## Server Sent Events

- A response has start and end
- Client sends a request
- Server sends logical events as part of response
- Server never writes the end of the response
- It is still a request but an unending response
- Client parses the streams data looking for events
- Works with request/response (HTTP)

![](assets/Pasted%20image%2020251004100619.png)

- Pros
    - Real time
    - Compatible with Request/response
- Cons
    - Clients must be online
    - Clients might not be able to handle
    - Polling is preferred for light clients
    - НTТP/1.1 problem (6 connections)

## Publish Subscribe (Pub/Sub)

![](assets/Pasted%20image%2020251004101518.png)

- Pros
    - Scales w/ multliple Receivers
    - Great for microservices
    - Losse Coupling
    - Works while clients are not running
- Cons
    - Message delivery issues (two generals problem)
    - complexity
    - Network Saturation

## Multiplexing vs Demultiplexing
*(h2 proxying vs Connection Pooling)*

![](assets/Pasted%20image%2020251004111035.png)

### Multiplexing example HTTP/2

![](assets/Pasted%20image%2020251004111424.png)

### Multiplexing example HTTP/2 on Backend

![](assets/Pasted%20image%2020251004111652.png)

![](assets/Pasted%20image%2020251004111749.png)

### Connection Pooling

![](assets/Pasted%20image%2020251004112041.png)

- NOTE: Browser also utilises connection pool, e.g. Chrome allows 6 connection per connection pool on per domain.
## Stateful vs Stateless

- Stateful
    - Stores state about clients in its memory
    - Depends on the information being there
- Stateless
    - Client is responsible to *transfer the state* with every request
    - May store but can safely lose it

### Stateless Backends

- Stateless backends can still store data somewhere else
- Can you restart the backend during idle time, while the client workflow continues to work
- Stateless backends can store state in database
- The backend remain stateless but the system is stateful
- Can we restart the backend during idle time and the client workflow continue to work ?


### Stateless vs Stateful Protocols

- The protocols can be designed to store state
- TCP is stateful
    - Sequence, Connection file descriptor
- UDP is stateless
    - DNS send queryID in UDP to identify queries
    - QUIC sends connectionID to identify connections
- You can build a stateless protocol on top of a stateful one and vice-versa
- HTTP on top of TCP
- if TCP breaks, HTTP blindly create another one
- QUIC on top UDP

### Complete Stateless System

- Stateless systems are rare
- State is carried with every request
- A backend service that relies completely on the input
    - Check if input param is a prime number
- JWT (JSON Web Token)
- Definition go nowhere


## Sidecar Pattern

Every protocol requires a library

![](assets/Pasted%20image%2020251004115134.png)

### Changing the Library is hard

- Once you use the library your app is entrenched
- App & Library should be same language
- Changing the library requires retesting
- Breaking changes Backward compatibility
- Adding features to the library is hard
- Microservices suffer

### What if we delegate communication ?

- Proxy communicate instead
- Proxy has the rich library
- Client has thin library (e.g. h1)
- Meet Sidecar Pattern
- Each client must have a sidecar proxy

### Sidecar Design Pattern

![](assets/Pasted%20image%2020251004115546.png)

![](assets/Pasted%20image%2020251004115637.png)

### Sidecar Examples

- Service Mesh Proxies
    - Linkerd, Istio, Envoy
- Sidecar Proxy Container
- Must be Layer 7 Proxy
