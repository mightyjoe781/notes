# Backend Execution Patterns

## Process vs Threads

### Process

- A set of instructions
- Has an isolated memory
- Has a PID (process identifier)
- scheduled in the CPU
### Thread

- Light Weight Process (LWP)
- A set of instructions
- Shares Memory with parent process
- Has an ID

![](assets/Pasted%20image%2020251006180634.png)
### Single Threaded Process

- One Process with a single thread
- Simple
- Example NodeJS
### Multi-Processes

- App has multiple Processes
- Each has its own Memory
- Examples *nginx/Postgresql*
- Take Example of Multiple cores ~ can share memory using shared buffer pool etc.
- More memory but isolated
- Redis Backup Routine (COW) ~ Asynchronous Snapshot (Flush Cache to Disk)
### Multi-Threaded

- One Process, Multiple threads
- Shared Memory (compete)
- Take advantage of multi-cores
- Requires less Memory
- Race Conditions
- Locks and Latches (SQL Server)
- Examples Apache, Envoy

### How many is too Many ?

- Too many processes/threads
- CPU context switch
- Multiple Cores help
- Rules of thumb -> # cores = # processes

## Connection Establishment
*SYN/Accept Queues*

- TCP Three way handshake
- SYN/SYN-ACK/ACK
- But what happens on Backend

![](assets/Pasted%20image%2020251006182909.png)

- Server Listens on an address:port
- Client connects
- Kernel does the handshake creating a connection
- Backend process "Accepts" the connection

#### Detailed Process

- Kernel creates a socket & two queues SYN and Accept
- Client sends a SYN
- Kernels adds to SYN queue, replies with SYN/ACK
- Client replies with ACK
- Kernel finish the connection
- Kernel removes SYN from SYN queue
- Kernel adds full connection to Accept queue
- Backend accepts a connection, removed from accept queue
- A file descriptor is created for the connection

![](assets/Pasted%20image%2020251006183511.png)

#### Problems with accepting connections

- Backend doesn't accept fast enough
- Clients who don't ACK
- Small Backlog

## Reading and Sending Socket Data
*Receive vs Send buffers*

### Send and Receive buffers

- Client sends data on a connection
- Kernel puts data in receive queue
- Kernel ACKs (may delay) and update window
- App calls read to copy data

### Receive Buffers & Send Buffers

![](assets/Pasted%20image%2020251006184008.png)

#### Problems with reading and sending

- Backend doesn't read fast enough
- Receive queue is full
- Client slows down

## Socket Programming Patterns

Three Key Roles in Socket Communication

- Listener
    - Role: Thread/process that initiates listening
    - Function
        - Calls ⁠listen() with port and address parameters
        - Receives back a socket ID/number
    - Responsibility: 
        - Just listening - establishes the memory location where the file/socket exists
- Acceptor
    - Role: Entity with access to the socket ID
    - Function:
        - Calls ⁠accept() on the socket ID
        - Gets back file descriptors pointing to connections
        - Note: Can be different from the listener
- Reader/Writer
    - Role: Handles actual data transfer on established connections 
    - Function:
        - Reader: reads data from the connection
        - Writer: writes data to the connection
    - Note:
        - Reader and writer can be the same entity or different
        - Focus is primarily on reading requests rather than responding
#### Key Distinctions

- All three roles can be different entities/processes
- Each has a specific responsibility in the socket communication flow
- The separation allows for more flexible and scalable network architectures
#### Flow Summary

- Listener → Creates socket and listens
- Acceptor → Accepts incoming connections
- Reader → Processes the actual data from connections

#### Different Patterns

- Single Listener/Single Worker Thread ~ NodeJS
- Single Listener/Multiple Worker Thread ~ Memcached
- Single Listener/Multiple Worker threads with load balancing ~ RAMCLOUD
- Multiple Acceptor Thread single Socket - *nginx* (used to default)
- Multiple Listener on the same port - *SO_REUSEPORT* Option allows this. *nginx* supports this.

## Backend Idempotency
*Resending the Request without affecting backend*

### What is idempotency ?

- API /postcomment
- Takes comment and appends it to table
- What if the user/proxy retries it ?
- You will have duplicate comments
- Very bad for financial systems
- Idempotent request can be retried without affecting backend
- Easy implementation send a requestld
- If requestld has been processed return
- Also known as *idempotency token*

In HTTP

- GET is idempotent
- POST isn't, but we can make it
- Browsers and proxies treat GET as idempotent
- Make sure your GETs are
