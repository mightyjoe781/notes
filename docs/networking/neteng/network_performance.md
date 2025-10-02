# Network Performance


## MSS vs MTU vs PMTUD
*How large the packet can get*
### Overview

- TCP layer 4 unit is segment
- The segment slides into an IP Packet in Layer 3
- The IP Packet now has the segment + headers
- The IP Packet Slides into a layer 2 frame
- The frame has a fixed size based on the networking configuration
- The size of frame determines the size of segment

### Hardware MTU

- Maximum transmission Unit (MTU) is the size of the frame
- It is a network interface property default 1500 bytes
- Some network have jumbo frames up to 9000 bytes
- Are there any networks with larger MTUs ?

### IP Packets and MTU

- The IP MTU usually equals the Hardware MTU
- One IP packet *should* fit a single frame
- Unless IP fragmentation is in place
- Larger IP Packets will be fragmented into multiple frames

Important Article : https://blog.cloudflare.com/sad-dns-explained/

### MSS

- Maximum Segment Size is determined on MTU
- Segment must fit an IP Packet which *should* fit in a frame
- MSS = MTU - IP Headers - TCP Headers
- MSS = 1500 - 20 - 20 = 1460 bytes
- If you are sending 1460 bytes exactly that will fit nicely into a single MSS
- Which fits in a single frame

![](assets/Pasted%20image%2020251001120025.png)

### Path MTU Discovery

- MTU is network property each host can have different value
- You really need to use the smallest MTU in the network
- Path MTU help determine the MTU in the network path
- Client sends a IP packet with its MTU with a DF flag
- The host that their MTU is smaller will have to fragment but can't
- The host sends back an ICMP message fragmentation needed which will lower the MTU.

![](assets/Pasted%20image%2020251001120428.png)

## Nagle's Algorithm's Effect on Performance
*Delay in the client side*

### Nagle Algorithm

- In the telnet days sending a single byte in a segment is a waste
- Combine small segments and send them in a single one
- The client can wait for a full MSS before sending the segment
- No wasted 40 bytes header (IP + TCP) for few bytes of data

- Assume MSS = 1460, A sends 500 bytes
- 500 < 1460 client waits to fill the segments
- A sends 960 bytes, segment fills and send
- If there isn't anything to ACK data will be immediately sent

![](assets/Pasted%20image%2020251001120926.png)

### Problem with Nagle's Algorithm

- Sending large data causes delay
- A want to send 5000 bytes on 1460 MSS
- 3 full segments of 1460 with 620 bytes
- 4 th segment will not be sent
- 4th not full segment are only sent when an ACK is received

### Disabling Nagle's Algorithm

- Most clients today disable Nagle's Algorithm
- I rather get performance than small bandwidth
- TCP_NODELAY
- Curl disabled this back in 2016 by default because TLS handshake was slowed down

## Delayed Acknowledgement Effect on Performance
*Less packets are good but peformance is better*

- Waste to acknowledge segments right away
- We can wait little more to receive more segment and ack once

![](assets/Pasted%20image%2020251001121546.png)

### Problem with Delayed ACK

- Causes delays in some client that may lead to timeout and retransmission
- Noticeable performance degradation
- Combine with Nagle's algorithm can lead to 400ms delays !
- Each party is waiting on each other

## Cost of Connection Establishment

- TCP three way handshake
- The further apart the peers, the slower it is to segments
- Slow start keeps the connection from reaching its potential right away
- Congestion control and Nigel Algorithm can further slow down
- Destroying the connection is also expensive

### Connection Pooling

- Most implementation database backends and reverse proxies use pooling
- Establish a bunch of TCP connection to the backend and keeps them running!
- Any request that comes to the backend use an already opened connection
- This way your connections will be *warm* and slow start would have already kicked in
- Don't close the connection unless you absolutely don't need it

### Eager vs Lazy Loading

- Depending on what paradigm you take you can save on resources
- Eager Loading -> load everything and keep it ready
    - start up is slow but requests will be served immediately
    - some apps send warm up data to kick in the slow start but be careful of bandwidth and scalability
- Lazy Loading -> only load things on demand
    - startup is fast but requests will suffer initially

## TCP Fast Open

Wait can I send data during handshake ?

#### Handshake is Slow

- We know it, the handshake is slow
- I already know the server I have established a connection prior
- Can we use a predetermined token to send data immediately during the handshake
- TCP Fast Open

### TCP Fast Open (TFO)

- client and server establishes connection 1, server sends an encrypted cookie
- Client stores the TFO cookie
- Client want to create another connection
- Client sends SYN, data and TFO cookie in TCP Options
- Server authenticates the cookie and sends response + SYN/ACK

![](assets/Pasted%20image%2020251001121846.png)

- TFO is enabled by default in linux 3.13
- You can enable TFO in curl --tcp-fastopen
- Goes without saying, you still get TCP slow start with TCP Fast open
- You can take advantage of this feature to send early data

## Listening Server

- You create a server by listening on a port on a specific ip address
- Your machine might have multiple interfaces with multiple IP address
- `listen(127.0.0.1, 8080)` -> listens on the local host ipv4 interface on port 8080
- `listen(::1, 8080)` -> listens on localhost ipv6 interface on port 8080
- `listen(192.168.1.2, 8080)` -> listens on `192.168.1.2` on port 8080
- `listen(0.0.0.0, 8080)` -> listens on all interfaces on port 8080 (can be dangerous)

- You can only have one process in a host listening on IP/Port
- No two processes can listen on the same port
- P1 -> `Listen(127.0.0.1, 8080)`
- P2 -> `Listen(127.0.0.1, 8080)` -> error

### There is an exception

- There is a configuration that allows more than one process to listen on the same port
- `SO_PORTREUSE`
- Operating System balance segments among processes
- OS create a hash source ip/source port/ dest ip/ dest port
- Guarantees always go to same process if the pair match

## TCP Head of line blocking (HOL)

- TCP orders packets in the order they are sent
- The segments are not acknowledged or delivered to the app until they are in order
- This is great ! But what if multiple clients are using the same connection

- HTTP requests may use the same connection to send multiple requests
- Request 1 is segments 1, 2
- Request 2 is segments 3, 4
- Segments 2, 3, 4 arrive but 1 is lost ?
- Request 2 technically was delivered but TCP is blocking it
- Huge latency in apps, big problem in HTTP/2 with streams
- QUIC solves it

![](assets/Pasted%20image%2020251002085123.png)

## Importance of Proxy and Reverse Proxies

Proxy is a server that makes request on behalf of clients.

![](assets/Pasted%20image%2020251002085623.png)

Use cases of Proxy

- Caching
- Anonymity
- Logging
- Block Sites
- Microservices

![](assets/Pasted%20image%2020251002090015.png)

![](assets/Pasted%20image%2020251002090024.png)

- Can Proxy & Reverse Proxy used in the same time ? Yes
- Can I use Proxy instead of VPN for anonymity ? No, proxy takes a look at the packet
- Is proxy just for HTTP traffic ? No there are multiple types HTTPS/SOCK4/SOCKS5
## Load Balancing at Layer 4 vs Layer 7

### Layer 4 

![](assets/Pasted%20image%2020251002090845.png)

- When a client connects to the L4 load balancer, the LB chooses one server and all segments for that connections go to that server
- L4 Load Balancer, doesn't know anything about request(HTTP/HTTPS/) other than its TCP packet, it doesn't buffer data, immediately passes request to servers.

| Pros                                                                                                                                 | Cons                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| - Simpler Load Balancing<br>- Efficient (no data lookup)<br>- More secure<br>- Works with any protocol<br>- One TCP connection (NAT) | - No smart Load Balancing<br>- NA microservices<br>- Sticky per connection<br>- No caching<br>- Protocol unaware (can be dangerous) bypass rules |

### Layer 7

![](assets/Pasted%20image%2020251002091939.png)

| Pros                                                                                                        | Cons                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| - Smart Load Balancing<br>- Caching<br>- Great for microservices<br>- API Gateway Logic<br>- Authentication | - Expensive (looks at the data)<br>- Decrypts (terminates TLS)<br>- Two TCP Connections<br>- Must share TLS certificate<br>- Needs to buffer<br>- Needs to understand protocol |

## Network Access Control to database Servers

https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
