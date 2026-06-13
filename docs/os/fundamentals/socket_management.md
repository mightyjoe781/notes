# Socket Management

## Network Fundamentals

Refer to Course on Networking : [Link](../../networking/neteng/index.md)

## Sockets, Connections and Kernel Queues

### Socket

![](../../networking/neteng/assets/Pasted%20image%2020250930113520.png)

- When a process calls `listen()` on an IP/port, the kernel creates a **socket** for it
- On Linux, a socket is represented as a file descriptor - "everything is a file"
- The listening process *owns* the socket (the diagram shows process A holding a socket file descriptor)
- Because a socket is just a file descriptor, it follows the same rules as any other fd - in particular, it can be **shared across a `fork()`**, which is exactly how multi-process servers like Postgres or nginx let multiple child processes accept connections on the same listening socket (see [process_management.md - Fork](process_management.md#fork))

### SYN Queue, Accept Queues

![](../../networking/neteng/assets/Pasted%20image%2020250930113715.png)

- When a socket starts listening, the kernel creates **two queues** alongside it:
    - **SYN queue** - holds connections that have received a SYN but haven't completed the handshake yet (half-open connections)
    - **Accept queue** - holds connections that have *completed* the three-way handshake and are waiting for the application to `accept()` them
- In the diagram, process A's socket S has its own SYN queue and accept queue
- The maximum size of these queues is controlled by the **backlog** argument to `listen()`
- Despite being called "queues", they're not implemented as simple FIFOs internally - the kernel uses hash tables, so it can quickly look up a connection by its `(src IP, src port, dst IP, dst port)` tuple regardless of arrival order

```c
#include <sys/socket.h>
int listen(int sockfd, int backlog);
```

### Connection, Receive and Send Queue

![](../../networking/neteng/assets/Pasted%20image%2020250930114035.png)

- Once a connection finishes its handshake, it sits in the accept queue (as connection C in the diagram)
- When the process calls `accept()`, the kernel removes that connection from the accept queue and hands the process a **new file descriptor** representing it
- This new connection gets its own pair of queues:
    - **Send queue** - outgoing data the application has written, waiting to be sent over the network
    - **Receive queue** - incoming data from the network, waiting for the application to `read()` it

Note: a *client* never has a listening socket, a SYN queue, or an accept queue - it only ever has a connection (represented as a socket-like fd) with its own send and receive queues.

### Connection Establishment

- TCP's three-way handshake is SYN / SYN-ACK / ACK - but what actually happens on the server side?
    - The server process is listening on `address:port`
    - A client connects
    - The **kernel** carries out the handshake and builds the connection - the application isn't involved yet
    - Only once the handshake is done does the backend process `accept()` the connection

**Step by step:**

![](assets/Pasted%20image%2020260613083004.png)

1. The kernel creates the listening socket along with its SYN queue and accept queue (both initially empty). The client sends a **SYN**.

![](assets/Pasted%20image%2020260613083035.png)

2. The kernel adds an entry to the **SYN queue** and replies with **SYN/ACK**. The client responds with the final **ACK**, completing the handshake. The kernel moves the now-complete connection from the SYN queue into the **accept queue**.

![](assets/Pasted%20image%2020260613083119.png)

3. The backend process calls `accept()`. The kernel removes the connection from the accept queue and hands the process a new file descriptor for it - this is the `accept() copy` step shown going from the accept queue to the process.

In summary: the kernel adds the new connection to the SYN queue on the initial SYN, removes it from the SYN queue and adds it to the accept queue once the handshake completes, and finally removes it from the accept queue (and creates a file descriptor) when the application calls `accept()`.

#### Problems with Accepting Connections

- The backend process isn't calling `accept()` fast enough - completed connections pile up in the accept queue
- Clients that send SYN but never complete the handshake (don't send the final ACK) tie up entries in the SYN queue
- A small `backlog` value means both queues fill up quickly under load, causing the kernel to drop or reject new connection attempts
- If the application calls `accept()` while the accept queue is empty, that call **blocks** the calling thread/process - this is exactly why asynchronous I/O models (see below) exist, so a single thread doesn't have to sit idle waiting for a connection

### Socket Sharding

![344](assets/Pasted%20image%2020260613083404.png)

- Normally, only one socket can bind to a given IP/port pair - a second `bind()` to the same address fails
- The `SO_REUSEPORT` socket option overrides this: **multiple distinct sockets**, owned by different processes (or threads), can all bind to the *same* IP/port
- This is how servers like nginx scale across multiple worker processes without needing a single process to accept and hand off every connection
- The kernel itself load-balances incoming connections across these sockets - each gets its own SYN/accept queues, so the accept-queue bottleneck is spread across all of them instead of funneling through one

### Summary

- The kernel manages all of the networking machinery described above
- A socket represents a listening `IP:port`
- Every connected client gets its own connection, with its own send/receive queues
- Internally these aren't literal FIFO queues but kernel hash tables, used to quickly route an incoming packet to the correct listening socket and connection

## Reading and Sending Data

### Send and Receive Buffers

- When a client sends data on an established connection, the kernel places it into that connection's **receive queue** (receive buffer)
- The kernel ACKs the data (possibly delaying the ACK slightly to batch it with other traffic) and updates its advertised TCP window
- The application calls `read()` to **copy** that data out of the kernel's receive buffer into a user-space buffer

That `read()`/`send()` copy - from kernel-space memory into user-space memory (and vice versa) - is real overhead: it's an extra memory copy and, depending on the call, can involve a page-table-mapping change between kernel and user address spaces (see [memory.md](memory.md) on virtual memory and page tables). Runtimes that want maximum network throughput try to avoid this copy where possible - this is generally called **zero-copy I/O** (e.g. using `sendfile()`/`splice()` to move data from a file descriptor straight to a socket without round-tripping through a user-space buffer). The Bun JavaScript runtime advertises zero-copy I/O as part of why its HTTP server throughput is higher than Node's in some benchmarks - by minimizing buffer copies and reusing buffers across the request/response lifecycle rather than copying data into and out of user space at every step.

### Receive Buffers

![](assets/Pasted%20image%2020260613084957.png)

The client sends `data`, the kernel places it into the connection's receive buffer and sends an `ACK` back. The application later calls `read()`, which **copies** the buffered data from kernel space into the process's (PID's) memory.

Note: the kernel may deliberately wait for more data to arrive before copying it out (and before ACKing), to batch small writes together rather than copying one byte at a time.

### Send Buffer

![](assets/Pasted%20image%2020260613085059.png)

When the application calls `send()`, the data is **copied** from the process's memory into the connection's send buffer in kernel space. The kernel is then responsible for actually transmitting it onto the network - which it may not do immediately (e.g. it can coalesce small writes, subject to things like Nagle's algorithm).

**Problems with Reading and Sending**

- The backend process isn't calling `read()` fast enough, so the receive queue fills up
- Once the receive queue is full, the kernel stops ACKing new data and advertises a shrinking TCP window, which causes the *sender* to slow down
- Symmetrically, if the backend writes faster than the network/client can drain it, the send queue fills and `send()`/`write()` starts blocking (or returning `EAGAIN` in non-blocking mode)

## Socket Programming Patterns

### Single Listener/Single Worker Thread

![409](assets/Pasted%20image%2020260613092316.png)

The simplest model: one thread does everything - it's the listener, the acceptor, *and* the reader for every connection (this is Node's default single-threaded event-loop model). Simple to reason about, but this one thread is a single point of contention for accepting new connections and processing all I/O.

### Single Listener/Multiple Worker threads

![474](assets/Pasted%20image%2020260613092630.png)

One thread acts as the listener/acceptor, but hands off accepted connections to a pool of **worker threads** that do the actual reading/processing (this is roughly how memcached's threading model works). This spreads the I/O-handling work across cores while keeping connection acceptance centralized.

![474](assets/Pasted%20image%2020260613092944.png)

A variation on the same idea: one listener/acceptor thread, but incoming messages/requests are explicitly load-balanced across multiple worker threads (RAMCloud's approach) - useful when message processing itself is the bottleneck, not just accepting connections.

### Multiple Acceptor Thread (Processes) single Socket

![414](assets/Pasted%20image%2020260613093036.png)

Multiple threads (or processes, as with nginx workers) each act as their own listener/acceptor/reader, all working off the same underlying socket. Because accepting is spread across multiple acceptors, no single thread's `accept()` loop becomes the bottleneck for new connections.

### Multiple Listeners on the same Port

![404](assets/Pasted%20image%2020260613093216.png)

Taking this further with `SO_REUSEPORT` (socket sharding, described above): each worker gets its *own* independent socket - and therefore its own SYN/accept queues - all bound to the same port, with the kernel distributing new connections across them. This avoids any shared-socket contention between workers entirely.

## Async IO

### Blocking Operations

![361](assets/Pasted%20image%2020260613123657.png)

- `read()`, `write()`, and `accept()` are all **blocking** by default
- A blocking call means the calling thread's program counter can't advance until the call completes - the thread is descheduled
- `read()` blocks if there's no data yet in the receive buffer; `accept()` blocks if the accept queue is empty
- In the diagram, a thread looping over `read()` on connections `con1`-`con10` succeeds instantly for `con1` and `con2` (data already buffered), but blocks on `con3` (nothing to read yet) - even though `con4` onward *do* have data ready and could have been served immediately
- Blocking like this forces a context switch (see [process_management.md - Context Switching](process_management.md#context-switching)) every time a thread waits, which adds real overhead if it happens constantly across many connections

### Asynchronous I/O

- `read()` blocks when there's no data in the receive buffer; `accept()` blocks when there's nothing in the accept queue
- **Readiness-based approach**: ask the OS to tell you *which* file descriptors are ready, then call `read`/`write`/`accept` on those without blocking - `select`, `poll`, `epoll`, `kqueue`
- **Completion-based approach**: ask the OS (or a kernel worker thread) to perform the blocking I/O itself, and notify you when it's *done* - IOCP (Windows), `io_uring` (Linux)
- Readiness-based APIs generally don't work well for regular file I/O (as opposed to sockets) - a regular file is almost always "ready", even if the actual disk read would block

### Select (polling)

- `select()` takes a set of file descriptors for the kernel to monitor
- `select()` itself blocks (optionally with a timeout) until at least one fd is ready
- When it returns, the process loops over all the fds, checking each with `FD_ISSET` to find out which ones are ready
- The process then calls `read`/`write`/`accept` on the ready fds

```c
#include <sys/select.h>
typedef /* ... */ fd_set;

int select(int nfds, fd_set *_Nullable restrict readfds,
           fd_set *_Nullable restrict writefds,
           fd_set *_Nullable restrict exceptfds,
           struct timeval *_Nullable restrict timeout);

void FD_CLR(int fd, fd_set *set);
int  FD_ISSET(int fd, fd_set *set);
void FD_SET(int fd, fd_set *set);
void FD_ZERO(fd_set *set);

int pselect(int nfds, fd_set *_Nullable restrict readfds,
            fd_set *_Nullable restrict writefds,
            fd_set *_Nullable restrict exceptfds,
            const struct timespec *_Nullable restrict timeout,
            const sigset_t *_Nullable restrict sigmask);
```

![297](assets/Pasted%20image%2020260613124103.png)

In the diagram, `select()` is asked to monitor `con1`-`con10`. Only `con9` turns out to be ready - but to discover that, the process has to iterate over *all ten* file descriptors checking `FD_ISSET`.

**Select pros and cons**

- Pros
    - Avoids calling `read`/`write`/`accept` on fds that aren't ready (so it avoids blocking)
    - Enables an asynchronous, single-threaded event loop
- Cons
    - Checking readiness is $O(n)$ - the process has to scan every monitored fd, even if only one is ready
    - Each call copies the entire fd set between user space and kernel space
    - `fd_set` has a fixed maximum size (`FD_SETSIZE`), capping how many fds can be monitored at once

### epoll (eventing)

![](assets/Pasted%20image%2020260613124312.png)

- The application registers its file descriptors with the kernel **once**, via `epoll_create` + adding `con1`, `con2`, `con3`, etc. to the interest list
- The kernel then tracks readiness for those fds as packets arrive - e.g. an incoming packet for `con3` marks it ready in the kernel's internal ready list
- The application calls `epoll_wait()`, and the kernel returns just the events for the fds that are *actually* ready (here, `con3`) - no scanning of every registered fd required

**epoll drawbacks**

- More complex API than `select` - in particular, the level-triggered vs. edge-triggered distinction is easy to get wrong
- Linux-specific (other platforms have their own equivalents - `kqueue` on BSD/macOS, IOCP on Windows)
- Can still mean a lot of syscalls under high connection churn (registering/deregistering fds)
- Like `select`, doesn't work well for regular file I/O

### io_uring

![](assets/Pasted%20image%2020260613125515.png)

- `io_uring` is a **completion-based** async I/O interface
- The application and kernel share memory-mapped ring buffers: a **submission queue** (`io_uring_submit_sqe`) and a **completion queue** (`io_uring_complete`)
- The application places a "job" (e.g. a read or write request) onto the submission ring; the kernel (using a pool of worker threads for blocking operations) performs the work and writes the result onto the completion ring
- The application can poll the completion ring (`io_uring_poll_wake`/`io_uring_poll_arm`) or be notified when results are ready, without a syscall per operation

Sharing memory directly between user space and the kernel like this has also made `io_uring` a significant attack surface: it has been the source of a number of Linux kernel security vulnerabilities, to the point that Google disabled `io_uring` by default across its fleet and in ChromeOS. See [Google limiting io_uring use due to security vulnerabilities](https://www.phoronix.com/news/Google-Restricting-IO_uring) (also referenced in [introduction.md](introduction.md#user-space-vs-kernel-space)).

### Cross Platform

Writing directly to `epoll`/`kqueue`/IOCP is platform-specific. Runtimes that need to run everywhere build a cross-platform abstraction over all of them - Node's `libuv` is the canonical example, picking the appropriate readiness or completion mechanism per OS while presenting one event-loop API to JavaScript.

![Node Example](https://miro.medium.com/v2/resize:fit:1400/1*RM0-HzY4w5VYJAHfSMeRUw.png)

## TCP Server with Python

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("127.0.0.1", 8880))
    server.listen()

    conn, addr = server.accept()
    with conn:
        print(f"TCP handshake successful with {addr[0]}:{addr[1]}")
        conn.sendall(b"hello client!")

        while data := conn.recv(1024):
            print(f"Received data {data.decode()}")
```

```bash
nc 127.0.0.1 8880 # default ~ tcp
```

## TCP Server with C

```c
//https://github.com/nikhilroxtomar/tcp-client-server-in-C

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8801

int main(){

	int sockfd;
	struct sockaddr_in serverAddr;

	int newSocket;
	struct sockaddr_in newAddr;

	socklen_t addr_size;
	char buffer[1024];

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	printf("Server Socket Created Sucessfully.\n");
	memset(&serverAddr, '\0', sizeof(serverAddr));

	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(PORT);
	serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

	bind(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
	printf("[+]Bind to Port number %d.\n", PORT);

	listen(sockfd, 5); // notice (backlog) passed here
	printf("[+]Listening...\n");

	newSocket = accept(sockfd, (struct sockaddr*)&newAddr, &addr_size);

	strcpy(buffer, "Hello");
	send(newSocket, buffer, strlen(buffer), 0);
	printf("[+]Closing the connection.\n");

  return 0;

}
```

### Understanding TCP using `tcpdump`

```bash
tcpdump -n -v -i en0 '(src 93.184.216.34 or dst 93.184.216.34) and port 80' # find ip of example.com using nslookup

# open browser and go to example.com

```

## Resources

- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/) - the classic, approachable introduction to sockets, `accept`/`bind`/`listen`, and blocking vs. non-blocking I/O
- [Operating Systems: Three Easy Pieces - I/O and concurrency chapters](https://pages.cs.wisc.edu/~remzi/OSTEP/) - covers the threading models and async I/O mechanisms discussed above
- [The `man7.org` socket(7), tcp(7), and epoll(7) man pages](https://man7.org/linux/man-pages/man7/socket.7.html) - the authoritative reference for socket options (including `SO_REUSEPORT`), the TCP state machine, and `epoll`'s level-triggered vs. edge-triggered behavior
- [select(2) vs poll(2) vs epoll(7) - "The method to epoll's madness"](https://copyconstruct.medium.com/the-method-to-epolls-madness-d9d2d6378642) - a deep, practical comparison of the polling/eventing approaches covered in this note
- [What is io_uring?](https://unixism.net/loti/what_is_io_uring.html) - a clear walkthrough of `io_uring`'s submission/completion ring design
- [Google limiting io_uring use due to security vulnerabilities](https://www.phoronix.com/news/Google-Restricting-IO_uring) - the security tradeoffs of `io_uring`'s shared-memory design, referenced above
- [cpu.land - Putting the "You" in CPU](https://cpu.land/) - ties sockets, syscalls, and scheduling together from the process's point of view
- [process_management.md](process_management.md) and [memory.md](memory.md) - for the context-switch and kernel/user-space-copy costs referenced throughout this note
