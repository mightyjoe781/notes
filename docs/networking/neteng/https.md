# HTTP
*HyperText Transfer Protocol*

## HTTP/1.1
*Simple web protocol lasts decades*

### Client/Server

- (Client) Browser, python or javascript app, or any app that makes HTTP request
- (Server) HTTP Web server, e.g. IIS Apache Tomcat, NodeJS, Python Tornado, Flask, Django, etc.

### HTTP Request

![](assets/Pasted%20image%2020251004125453.png)

`curl -v http://minetest.in/`

![](assets/Pasted%20image%2020251004125442.png)

### HTTP Response

![](assets/Pasted%20image%2020251004125528.png)

![](assets/Pasted%20image%2020251004125650.png)

### HTTP

![](assets/Pasted%20image%2020251004134406.png)
### HTTPS

![](assets/Pasted%20image%2020251004134435.png)

### HTTP 1.0

- New TCP connection with each request
- Slow
- Buffering (transfer-encoding: chunked didn't exist)
- no multi-homed websites (HOST header)

![](assets/Pasted%20image%2020251004134540.png)

### HTTP 1.1

- Persisted TCP Connection
- Low Latency & Low CPU Usage
- Streaming with Chunked Transfer
- Pipelining (disabled by default)
- Proxying & Multiple Websites on single IP

![](assets/Pasted%20image%2020251004134648.png)

Pipelining Example

![](assets/Pasted%20image%2020251004134701.png)

![](assets/Pasted%20image%2020251004152026.png)


### HTTP/2

- Multiplexing over Signal Connection (save resources) (SPDY)
- Compression
- Multiplexing
- Server Push
- Secure by default
- Protocol Negotiation during TLS (NPN/ALPN)

![](assets/Pasted%20image%2020251004152103.png)

![](assets/Pasted%20image%2020251004152135.png)

- Cons
    - TCP Head of Line Blocking
    - Server Push never picked up
    - High CPU usage

### HTTP over QUIC (HTTP/3)

- replaces TCP with QUIC (UDP with Congestion control)
- All HTTP/2 features
- Without HOL (Head of Line Blocking) [Read More Here](network_performance.md)

#### TCP HOL

- TCP segment must be delivered in order.
- But streams don't have to
- Blocking request

#### Pros vs Cons of HTTP over QUIC

- Pros
    - QUIC has many other benefits
    - Merge connection setup + TLS in one handshake
    - Hash congestion control at stream level
    - Connection Migration (connection ID)
    - Why not HTTP/2 over QUIC ?
        - Header Compression algorithm
- Cons
    - Takes a lot of CPU (parsing logic)
    - UDP could be blocked
    - IP Fragmentation is the enemy

## More Ways to HTTPS

### HTTPS Communication Basics

- Establish Connection
- Establish Encryption
- Send Data
- Close Connection (when Absolutely done)

### HTTPS over TCP with TLS 1.2

- HTTP/1.1 and HTTP/2 supports TCP
- TCP Handshake (Unencrypted)
- Symmetric Encryption Keys Exchange using Key Exchange Algorithm.
- Client Hello Sends a list of algorithm supported, server replies with algorithm, AES 256 bits, ... They share parameter to generate the keys.
- Normal Encrypted request is sent

![](assets/Pasted%20image%2020251004192841.png)

### HTTPS over TCP with TLS 1.3

- TCP Handshake (Unencrypted)
- Client sends list of Algorithm it supports and picks an Algorithm along with public parameters as well, server replies
- Client sends encrypted Request

![](assets/Pasted%20image%2020251004193301.png)

### HTTPS over QUIC (HTTP/3)

- Protocol is changes from TCP to QUIC
- Smart Enough to do Handshake and Sharing of Encryption keys etc in the same request
- Client sends the encrypted request to server

![](assets/Pasted%20image%2020251004193526.png)

### HTTPS over TFO with TLS 1.3

- Theoretical using TCP Fast Open (Cookies to resume already existing connection)

![](assets/Pasted%20image%2020251004193945.png)

### HTTPS over TCP with TLS 1.3 and ORTT

- GET request along with the ACK, 0 RTT using preshared keys between client server
- Use preshared keys to encrypt the data.

![](assets/Pasted%20image%2020251004193905.png)

### HTTPS over QUIC with ORTT

- In same request send Handshake, with TCP Fast Open and zero Round Trip
- Fastest you can send the request

![](assets/Pasted%20image%2020251004194123.png)

Resource : https://blog.cloudflare.com/even-faster-connection-establishment-with-quic-0-rtt-resumption/
