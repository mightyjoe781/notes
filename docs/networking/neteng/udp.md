# User Datagram Protocol (UDP)

## What is UDP ?

- Stands for User Datagram Protocol
- Layer 4 protocol
- Ability to address processes in a host using ports
- Simple protocol to send and receive data
- Prior communication not required (double edged sword)
- Stateless no knowledge is stored on the host
- 8 byte header Datagram

### UDP Use Cases

- Video Streaming
- VPN
- DNS
- WebRTC

### Multiplexing and demultiplexing

- IP target hosts only
- Hosts run many apps each with different requirements
- Ports now identify the `app` or `processes`
- Sender multiplexes all its apps into UDP
- Receiver demultiplexes UDP datagrams to each app

![](assets/Pasted%20image%2020250929220342.png)

### Source and Destination Port

- App1 on 10.0.0.1 sends data to AppX on 10.0.0.2
- Destination Port = 53
- AppX responds back to App 1
- We need Source Port so we know how to send back data
- Source Port = 5555

![](assets/Pasted%20image%2020250929231847.png)
## User Datagram Structure

### UDP Datagram

- UDP Header is 7 bytes only (IPv4)
- Datagram slides into an IP packet as *data*
- Port are 16 bit (0 to 65535)

![](assets/Pasted%20image%2020250929232204.png)

## UDP Pros & Cons

### UDP Pros

- Simple protocol
- Header Size is small so datagrams are small
- Uses less bandwidth
- Stateless (scales nicely)
- Consumes less memory (no state stored in the server/client)
- Low Latency - no handshake, order, retransmission or guaranteed delievery

### UDP Cons

- No acknowledgement
- No guarantee delievery
- Connection less - anyone can send data without prior knowledge
- no flow control
- No congestion Control
- No order packets
- Security - can easily spoofed

## UDP server with JS

```javascript
// index.js

import dgram from 'dgram'

const socket = dgram.createSocket("udp4")
socket.bind(5500, "127.0.0.1")

socket.on("message", (msg, info) => {
    console.log(`my server got a datagram ${msg}, from: ${infor.address}:${info.port`)
})

```

```bash
npm install dgram
npm index.js

# use nc to udp
nc -u 127.0.0.1.5500
> hi
> my name is smk

```

## UDP server with C

```c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, char **argv) {
    int port = 5501;
    int sockfd;
    
    struct sockaddr_in myaddr, remoteAddr;
    char buffer[1024];
    socklen_t addr_size;
    
    socketfd = socket(AF_INET, SOCK_DGRAM, 0);
    
    memset(&myaddr, '\0', sizeof(myaddr));
    myaddr.sin_family = AF_INET;
    myaddr.sin_port = htons(port);
    myaddr.sin_addr.s_addr = inet_adr("127.0.0.1")
    
    bind(sockfd, (struct sockaddr*)& myaddr, sizeof(myaddr));
    addr_size. = sizeof(remoteAddr);
    
    recvfrom(sockfd, bugger, 1024, 0, (struct sockaddr*)& remoteAddr, &addr_size);
    print("got data from %s", buffer);
    
    return 0;
}

```

## Capturing UDP traffic with `tcpdump`

- This example tries to resolve DNS nameserver using `tcpdump`

```bash
tcpdump -n -v -i en0 src 8.8.8.8 or dst 8.8.8.8

# another terminal
nslookup smk.minetest.in 8.8.8.8
```