# More on Protocols

## WebSockets
*Bidirectional communication on the web*

### HTTP 1.0

![](assets/Pasted%20image%2020251004202011.png)
### HTTP 1.1

![](assets/Pasted%20image%2020251004202029.png)

### Websockets

![](assets/Pasted%20image%2020251004202045.png)

### Websockets Handshake` ws://` or `wss://`

![](assets/Pasted%20image%2020251004202102.png)
### Handshake

#### Client

![](assets/Pasted%20image%2020251004202135.png)
#### Server

![](assets/Pasted%20image%2020251004202147.png)
#### UseCases

- Chatting
- Live Feed
- Multiplayer Gaming
- Showing Client Progress/logging
#### Pros & Cons

- Pros
    - Full-duplex (no polling)
    - HTTP Compatible
    - Firewall Friendly (standard)
- Cons
    - Proxying is tricky
    - L7 LB challenging (timeouts)
    - Stateful, difficult to horizontally scale

#### Do we have to use Websockets ?

- No
- Rule of thumb - do you absolutely need bidirectional communication
- Long Polling
- Server Sent Events

### WebSockets Proxying

#### Layer 4 vs Layer 7 Websocket Proxy

- In Layer 4 OSI model we see TCP/IP content
    - Connections, Ports, IP Addresses
    - Content remains encrypted (if unencrypted it is not inspected)
- In Layer 7 OSI Model we see all what's below
    - Layer 4 + Application layer content
    - Content is decrypted (TLS termination)
    - We can read headers, paths, urls, etc.

- Layer 4 Proxying on Websockets is done as a tunnel
- Nginx intercepts the SYN for a connection and creates another connection on the backend
- Any data sent on the frontend connection is tunnelled to backend connection
- The backend connections remain private and dedicated to the client.

## gRPC
*Taking HTTP/2 to the next level*

### Motivation

#### Client server communication

- SOAP, REST, GraphQL
- SSE, Websockets
- Raw TCP
#### The Problem with client libraries

- Any communication protocol needs client library for the language of choice
    - SOAP Library
    - HTTP Client Library
- Hards to maintain and patch client libraries
    - HTTP/1.1 HTTP/2, new features, security etc.
#### Why gRPC was invented ?

- Client Library : One Library for popular languages
- Protocol : HTTP/2 (hidden implementation)
- Message Format : Protocol buffers as format

### gRPC modes

- Unary RPC
- Server streaming RPC
- Client streaming RPC
- Bidirectional streaming RPC

#### Exercises

- Todo Application (server, client) with gRPC
- createTodo()
- readTodos() // synchronous
- readTodos() // server stream

### gRPC Pros & Cons

#### Pros

- Fast & Compact
- One Client Library
- Progress Feedback (upload)
- Cancel Request (H2)
- H2/Protobuff

#### Cons

- Schema
- Thick Client
- Proxies
- Error Handling
- No Native Browser Support
- Timeouts (pub/sub)

Example : https://www.youtube.com/watch?v=Yw4rkaTc0f8
## WebRTC
*Realtime communication on the web*

### Overview

- Stands for Web Real-Time Communication
- Find a peer to peer path to exchange video and audio in an efficient and low latency manner
- Standardized API
- Enables rich communication browsers, mobile, IOT devices

#### Working

- A want to connect to B
- A finds all possible ways the public can connect to it
- B finds all possible ways the public can connect to it
- A and B signal this session information via other means
    - WhatsApp, QR, Tweet, Websockets, HTTP Fetch...
- A connects to B via most optimal path
- A & B Exchange their supported media and security

### Demystified

#### NAT

- If both users have public IPs, then there is no problem,
- But if one of the user is behind a Router, they don't have public IP Address
- Router translates the src IP address in the IP Packet with its own public IP Address, creating a NAT Table for this transmission and acting as a middle man for this communication

NAT Translation Methods

- One-to-One NAT (Full-cone NAT)
    - Packets to external IP:port on the router always maps to internal IP:port without exception
- Address restricted NAT
    - Packets to external IP:port on the router always maps to internal IP:port as long as source address from packet matches the table (regardless of port)
    - Allow if we communicated with this host before
- Port restricted NAT
    - Packets to external IP:port on the router always maps to internal IP:port as long as source address and port from packet matches the table.
    - Allow if we communicated with this host before
- Symmetric NAT
    - Packets to external IP:port on the router always maps to internal IP:port as long as source address and port from packet matches the table
    - Only Allow if the full pair match
    - ~ kinda of doesn't work with webRTC correctly
#### STUN, TURN

- Session Traversal Utilities for NAT
- Tell me my public ip address/port through NAT
- Works for Full-cone, Port/Address restricted NAT
- Doesn't work for symmetric NAT
- STUN server port 3478, 5349 for TLS
- Cheap to Maintain

![](assets/Pasted%20image%2020251005232232.png)

![](assets/Pasted%20image%2020251005232201.png)

#### TURN

- Traversal Using Relays around NAT
- In case of Symmetric NAT we use TURN
- It's just a server that relays packets
- TURN default server port 3478, 5349 for TLS
- Expensive to maintain and run

![](assets/Pasted%20image%2020251005232407.png)

#### ICE

- Interactive Connectivity Establishment
- ICE collects all available candidates (local IP addresses, reflexive addresses - STUN ones and relayed addresses - TURN ones)
- Called ice candidates
- All the collected addresses are then sent to the remote peer via SDP

#### SDP

- Session Description Protocol
- A format that describes ice candidates, networking options, media options, security options and other stuff
- Not really a protocol its a format
- Most important concept in WebRTC
- The goal is to take the SDP generated by a user and send it "somehow" to the other party

#### Signalling the SDP

- SDP Signaling
- Send the SDP that we just generated somehow to the other party we wish to communicate with
- Signaling can be done via a tweet, QR code, Whatsapp,
- WebSockets, HTTP request DOESN'T MATTER! Just get that large string to the other party
### Demo

- A wants to connect to B
- A creates an "offer", it finds all ICE candidates, security options, audio/video options and generates SDP, the offer is basically the SDP
- A signals the offer somehow to B (whatsapp)
- B creates the "answer" after setting A's offer
- B signals the "answer" to A
- Connection is created

- We will connect two browsers (Browser A & Browser B)
- A will create an offer (sdp) and set it as local description
- B will get the offer and set it as remote description
- B creates an answer sets it as its local description and signal the answer (sdp) to A
- A sets the answer as its remote description
- Connection established, exchange data channel

Video : https://www.youtube.com/watch?v=FExZvpVvYxA

### WebRTC Pros & Cons

- Pro
    - p2p is great ! low latency for high bandwidth content
    - Standardized API, so we don't have to build our own
- Cons
    - Maintaining STUN & TURN servers
    - Peer 2 Peer falls apart in case of multiple participants (discord)

### More WebRTC content
*So more to discuss beyond this content*

#### Media API

- getUserMedia to access microphone, video camera
- RTCPConnection.addTrack(stream)
- https://www.html5rocks.com/en/tutorials/webrtc/basics/

#### onIceCandidate and addIceCandidate

- To maintain the connection as new candidates come and go
- onIceCandidate tells user there is a new candidate after the SDP has already been created
- The candidate is signaled and sent to the other party
- The other party uses addiceCandidate to add it to its SDP

#### Set custom TURN and STUN Servers
![](assets/Pasted%20image%20202510042353241.png)

#### Create your own STUN & TURN server

- COTURN open source project
- https: //github. com/coturn/coturn

- Public STUN servers
    - stunl.1.google.com: 19302
    - stun2.1.google.com: 19302
    - stun3.1.google.com: 19302
    - stun4.1.google.com: 19302
    - stun.stunprotocol.org: 3478