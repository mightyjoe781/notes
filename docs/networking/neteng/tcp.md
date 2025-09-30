# TCP

### TCP

- stands for Transmission Control Protocol
- Layer 4 protocol
- Ability to address processes in a host using ports
- `Controls` the transmission unlike UDP which is firehose
- Connection
- Requires Handshake
- 20 bytes headers Segment (can go to 60)
- Stateful

### TCP Use Cases

- Reliable Communication
- Remote Shell
- Database Connections
- Web Communication
- Web Communications
- Any Bidirectional Communication

### TCP Connection

- Connection is a Layer 5 (*session*)
- Connection is an agreement between client and server
- Must create a connection to send data
- Connection is identified by 4 properties
    - SourceIP- SourcePort
    - DestinationIP - Destination Port
- Can't send data outside of a connection
- Sometimes called socket or file descriptor
- Requires a 3-way TCP Handshake
- Segments are sequenced and ordered
- Segments are acknowledged
- Lost Segments are retransmitted

### Multiplexing and Demultiplexing

- IP target hosts only
- Hosts run many apps each with different requirements
- Ports now identify the `app` or `process`
- Sender multiplexes all its apps into TCP connections
- Receiver multiplexes TCP segments to each app based on connection pairs

![](assets/Pasted%20image%2020250929220342.png)

### Connection Establishment

- App1 on `10.0.0.1` want to send data to AppX on `10.0.0.7`
- App1 sends SYN to AppX to synchronous sequence numbers
- AppX sends SYN/ACK to synchronous its sequence number
- App1 ACKs AppX SYN
- Three way handshake

![](assets/Pasted%20image%2020250930073643.png)

### Sending Data

- App sends data to AppX
- App1 encapsulate the data in a segment and send it
- AppX acknowledges the segments
- Hint: Can App1 send a new segment before ack of old segment arrives ?

![](assets/Pasted%20image%2020250930073632.png)

### Acknowledgement

- App1 sends segment 1, 2, 3 to AppX
- AppX acknowledges all of then with single ACK3

![](assets/Pasted%20image%2020250930073815.png)

### Lost Data

- App1 sends segment 1, 2, and 3 to AppX
- Seg3 is lost, AppX acknowledges 2
- App1 resend Seq3

![](assets/Pasted%20image%2020250930074036.png)

### Closing the Connections

- App1 wants to close the application
- App1 sends FIN, AppX ACK
- AppX sends FIN, App1 ACK
- Four way handshake

![](assets/Pasted%20image%2020250930074154.png)

## TCP Segment

- TCP segment Header is 20 bytes and can go up to 60 bytes
- TCP segments slide into an IP packet as *data*
- Port are 16 bit (0 to 65535)
- Sequences, Acknowledgement, flow control and more

![](assets/Pasted%20image%2020250930074439.png)

- Ports
- Sequences and ACK numbers
- Flow Control Window Size
- 9 bit flags

### Maximum Segment Size

- Segment Size depends on MTU(Maximum Transmission Unit) of the network
- Usually 512 bytes can go up to 1460
- Default MTU in the internet is 1500 (results in MSS 1460)
- Jumbo frames MTU goes to 9000 or more
- MSS can be large in Jumbo frames Case

## Flow Control

- A wants to send 10 segments to B
- A sends segment 1 to B
- B acknowledges segment 1
- A sends segment 2 to B
- B acknowledges segment 2
- Very SLOW !

![](assets/Pasted%20image%2020250930075712.png)

- A can send multiple segments and B can acknowledges all in 1 ACK
- The question is ... how much A can send ? (or B can handle)
- This is called flow control

![](assets/Pasted%20image%2020250930075529.png)

- When TCP segments arrive they are put in receiver's buffer
- If we kept sending data the receiver will be overwhelmed
- Segments will be dropped
- Solution ? let the sender know how much you can handle. *Receiver Window*

![](assets/Pasted%20image%2020250930075419.png)

### Window Size (receiver window) RWND

- 16 bit up to 64KB
- Updated with each acknowledgement
- Tells the sender how much to send before waiting for ACK
- Receiver can decide to decrease the Window Size (out of memory) more important stuff
![](assets/Pasted%20image%2020250930082151.png)
### Sliding Window

- Can't keep waiting for receiver to acknowledge all segments
- Whatever gets acknowledge moves
- We *slide* the window
- Sender maintains the sliding window for receiver

![](assets/Pasted%20image%2020250930080202.png)

### Window Scaling

- 64KB is too small
- We can't increase the bits on the segment
- Meet Window Scaling Factor (0-14)
- Window Size can go up to 1GB ($(2^{16}-1) \times 2^{14}$)
- Only Exchanged during the handshake

### Summary

- Receiver host has a limit
- We need to let the sender know how much it can send
- Receiver Window is in the segment
- Sender maintains the sliding window to know how much it can send
- window scaling can increase that
## Congestion Control

- The receiver might handle the load but the middle boxes might not
- The routers in the middle have limit
- We don't want to congest the network with data
- We need to avoid congestion
- A new window :Congestion (CWND)

###  Two Congestion Algorithms

- TCP Slow Start
    - Start slow goes fast !
    - CWND + 1 MSS (maximum segment size) after each ACK
- Congestion Avoidance
    - Once slow start reaches its threshold this kicks in
    - CWND + 1 MSS after complete RTT (Round Trip)
- CWND must not exceed RWND

### Slow Start

- CWND starts with 1 MSS (or more)
- Send 1 Segment and waits for ACK
- With EACH ACK received CWND is incremented by 1MSS
- Until we reach slow start threshold we switch to congestion avoidance algorithm

![](assets/Pasted%20image%2020250930084213.png)

### Congestion Avoidance

- Send CWND worth of Segments and waits for ACK
- Only when ALL segments are ACKed add UP to one MSS to CWND
- Precisely CWND = CWND + MSS * MSS/CWND

![](assets/Pasted%20image%2020250930084408.png)

## Congestion Notification

- We don't want routers dropping packets
- Can Routers let us know when congestion hit ?
- Meet ECN (Explicit Congestion Notification)
- Routers and middle boxes can tag IP packets with ECN
- The receiver will copy this bit back to the sender
- ECN is IP Header bit
- So routers don't drop packets just let me know you are reaching your limit.

### Summary

- Why the receiver may handle large data middle boxes might not
- Middle routers buffers may fill up
- Need to control the congestion in network
- Sender can send segment up to CWND or RWND without ACK
- Isn't normally a problem in hosts connected directly over LAN

## Congestion Detection

- The moment we get timeouts, dup ACKs or packet drops
- The slow start threshold reduced to the half of whatever unacknowledged data is sent (roughly CWND/2 if all CWND worth of data is unacknowledged)
- The CWND is reset to 1 and we start over
- Min Slow start threshold is 2 * MSS

![](assets/Pasted%20image%2020250930094351.png)

![](assets/Pasted%20image%2020250930094819.png)

## NAT

- Network Address Translation
- IPv4 is limited only 4 billion
- Private vs Public IP Address
- E.g. 192.168.x.x , 10.0.0.x is private not routable in the Internet
- Internal hosts can be assigned private addresses
- Only your router need public IP address
- Router need to translate requests, it swaps the private IP/Port in the packet with its own public IP, and then transmit request back to the machine (AAA).
- Router in NAT mode acts as both layer 3, layer 4 device.

![](assets/Pasted%20image%2020250930095742.png)

### NAT Applications

- Private to Public translations
    - so we don't run out IPv4
- Port forwarding
    - Add a NAT entry in the router to forward packets to 80 to a machine in your LAN
    - No need to have root access to listen on port 80 on your device
    - Expose your local web server publicly (bad idea)
- Layer 4 Load Balancing
    - HAProxy NAT Mode - Your load balancer is your gateway
    - Clients send a request to a bogus service IP
    - Router intercepts that packet and replaces the service IP with a destination server
    - Layer 4 reverse Proxying

## TCP Connection States

- TCP is a stateful protocol
- Both client and server need to maintain all sorts of state
- Window sizes, sequences and the state of connection
- The connection goes through many states

![](assets/Pasted%20image%2020250930100913.png)

NOTE: Notice how client doesn't immediately close its file descriptor.

## Pros & Cons of TCP

### Pros

- Guarantee delivery
- No one can send data priori knowledge
- Flow Control and Congestion Control
- Ordered Packets no corruption or app level work
- Secure and can't be easily spoofed

### Cons

- Large header overhead compared to UDP
- More Bandwidth
- Stateful - consumes memory on server and clients
- Considered high latency for certain workloads (slow start/congestion/ acks)
- Does too much at a low level (hence QUIC) (*TCP Head of line Blocking*)
    - Single connection to send multiple streams of data (HTTP requests)
    - stream 1 has nothing to do with stream 2
    - both stream 1 and stream 2 packets must arrive
- TCP meltdown
    - Not a good candidate for VPN

## Sockets, Connections and Kernel Queues

### Socket

- When a process listens on an IP/Port it produces a socket
- Socket is a file (at least in linux)
- the process owns the socket
- Can be shared during fork

![](assets/Pasted%20image%2020250930113520.png)

### SYN Queue, Accept Queues

- When a socket is created we get two queues with it
- SYN Queue, stores incoming SYNs
- Accept Queue, stores completed connections
- The size of queues is determined by the *backlog*
- not really queues but implemented as hash tables

![](assets/Pasted%20image%2020250930113715.png)

### Connection, Receive and Send Queue

- Completed connections are placed in the accept queue
- When a process *accepts* a connection is created
- Accept returns a file desc for the connection
- Two new queues created with the connection
- Send queues stores connection outgoing data
- Receive queue stores incoming connection data

![](assets/Pasted%20image%2020250930114035.png)

### Connection Establishment

- TCP Three way handshake
- SYN/SYN-ACK/ACK
- But what happens in the backend ?
- Server listens on an address: port
- Client connects
- Kernel does the handshake creating a connection
- Backend process *Accepts* the connections

Details :

- Kernel creates a socket & two queues SYN and Accept
- Client sends a SYN
- Kernel adds to SYN queue replies with SYN/ACK
- Client replies with ACK
- Kernel finish the connection
- Kernel remove SYN from SYN queue
- Kernel adds full connection to Accept Queue
- Backend accepts a connection, remove from the Accept Queue
- A file descriptor is created for the connection

### Socket Sharding

- Normally listening on active port/ ip fails
- But you can override it with `SO_REUSEPORT`
- Two distinct sockets different processes on the same ip/port pair
- used by *nginx*

![](assets/Pasted%20image%2020250930115348.png)

## TCP Server with JS

```javascript
import net from 'net';

const server = net.createServer( socket => {
    console.log("TCP handshake successful with " + socket.remoteAddress + ":" socket.remotePort);
    socket.write("hello client!");
    
    socket.on("data", data=> {
        console.log("Received data" + data.toString());
    })
})
server.listen(8880, "127.0.0.1");
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
tcpdump -n -v -i en0 src 93.184.216.34 or dst 93.184.216.34 and port 80 # find ip of example.com using nslookup

# open browser and go to example.com

```