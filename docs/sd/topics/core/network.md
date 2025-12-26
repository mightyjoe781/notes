# Communication & Protocols

NOTE: A Complete guide to Networking is present here : [Link](../../../networking/index.md)
Following notes are just for reference.
## Network Protocol Fundamentals

### TCP (Transmission Control Protocol)

**Connection-oriented, reliable protocol**

![](../../hld/beginner/assets/Pasted%20image%2020251221210659.png)

**Key Features**:

- Reliability: Guaranteed delivery with acknowledgments
- Ordering: Messages arrive in order
- Flow Control: Prevents overwhelming receiver
- Error Recovery: Automatic retransmission of lost packets
- Connection State: Maintains connection state

**Advantages**:

- Data integrity: No data loss or corruption
- Ordered delivery: Messages arrive in sequence
- Built-in flow control: Automatic congestion management

**Disadvantages**:

- Higher latency: Connection setup overhead
- More bandwidth: Headers and acknowledgments
- Connection state: Server must track connections

### UDP

**Connectionless, unreliable protocol**

![](assets/Pasted%20image%2020251224193027.png)

**Advantages**:

- Low latency: No connection setup
- Lower overhead: Minimal headers
- Stateless: Server doesn't track connections
- Broadcast/Multicast: Can send to multiple recipients

**Disadvantages**:

- No reliability: Packets may be lost
- No ordering: Messages may arrive out of order
- No flow control: Can overwhelm receiver
### Application Layer Protocol

````python
# Custom protocol example
class CustomProtocol:
    def __init__(self):
        self.version = "1.0"
        self.message_types = {
            0x01: "HEARTBEAT",
            0x02: "REQUEST",
            0x03: "RESPONSE",
            0x04: "ERROR"
        }
    
    def encode_message(self, msg_type, payload):
        """Encode message in custom binary format"""
        # Header: version(1) + type(1) + length(4) + payload
        header = struct.pack('!BBL', 
                           int(self.version.replace('.', '')),  # Version
                           msg_type,                            # Message type
                           len(payload))                        # Payload length
        
        return header + payload.encode('utf-8')
    
    def decode_message(self, data):
        """Decode message from binary format"""
        if len(data) < 6:  # Minimum header size
            raise ValueError("Invalid message length")
        
        version, msg_type, length = struct.unpack('!BBL', data[:6])
        payload = data[6:6+length].decode('utf-8')
        
        return {
            'version': f"{version//10}.{version%10}",
            'type': self.message_types.get(msg_type, "UNKNOWN"),
            'payload': payload
        }
````

## HTTP Evolution (1.0 to 3.0)

### HTTP/1.0 (1996)

**Characteristics**:

- **New connection per request**: TCP connection closed after each request
- **No persistent connections**: High overhead
- **Simple request/response**: Basic GET/POST methods

```
# HTTP/1.0 Request
GET /index.html HTTP/1.0
Host: www.example.com

# Connection closed after response
```

**Limitations**:

- High latency due to connection overhead
- Server cannot send multiple files efficiently
- No caching mechanisms

### HTTP/1.1 (1997)

**Major Improvements**:

- Persistent Connections : Using a header for `Connection: keep-alive`
- Pipelining : Multiple Requests sent at once
- Enhanced Caching : using `ETag` & `Cache-Control`
- Chunked Transfer Encoding

```
# Response with chunked encoding
HTTP/1.1 200 OK
Transfer-Encoding: chunked
Content-Type: text/html

1A
<html><head><title>Example
1C
</title></head><body>
E
Hello, World!
0
```

**Limitations**:

- Head-of-line blocking: One slow request blocks others
- Limited pipelining: Not widely supported
- Large headers: Repeated headers waste bandwidth

### HTTP/2.0 (2015)

**Revolutionary Changes**:

- Binary Protocol : Frame is converted into binary format
- Multiplexing : Stream Support
- Server Push
- Header Compression : HPACK


```
# Example of Multiplexing
# Single TCP connection with multiple streams
Connection: TCP
├── Stream 1: GET /index.html
├── Stream 2: GET /style.css
├── Stream 3: GET /script.js
├── Stream 4: GET /image.png
└── Stream 5: POST /api/data
```

**Benefits**:

- Multiplexing: No head-of-line blocking
- Server push: Proactive resource delivery
- Header compression: Reduced overhead
- Stream priorities: Important requests first

### HTTP/3.0 (2022)

**Built on QUIC (UDP-based)**:

- QUIC Protocol Features: 0-RTT or 1-RTT handshake combining connection & TLS Setup
- 0-RTT Connection Resumption
- Stream Independence

```
# QUIC streams are independent
UDP Connection
├── Stream 1: /index.html (blocked by packet loss)
├── Stream 2: /style.css (continues processing)
├── Stream 3: /script.js (continues processing)
└── Stream 4: /image.png (continues processing)
```


```python
def zero_rtt_example():
    # First connection establishes shared state
    client = HTTP3Client()
    client.connect_to_server("example.com")
    
    # Server provides resumption ticket
    resumption_ticket = client.get_resumption_ticket()
    client.close()
    
    # Later connection can send data immediately
    client = HTTP3Client()
    
    # Send request in first packet (0-RTT)
    client.send_early_data(
        ticket=resumption_ticket,
        request="GET /api/fast HTTP/3\r\nHost: example.com\r\n\r\n"
    )
    
    # No round-trip wait for handshake
    response = client.receive_response()
```

**Benefits over HTTP/2**:

- No head-of-line blocking: UDP-based streams
- Faster connection setup: Combined handshake
- Better mobility: Connection migration
- Improved congestion control: Per-stream control

## HTTPS and Security

### TLS Handshake Process

![](../../../networking/neteng/assets/Pasted%20image%2020251001083155.png)

NOTE: TLS 1.2 had a *heartbleed* vulenerability.
### Modern Security Features

- HTTP Strict Transport Security (HSTS)
- Certificate Transparency

```
# HSTS header forces HTTPS
HTTP/1.1 200 OK
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

## Real-time Communication Patterns

### WebSockets (Bidirectional)

WebSockets provide a persistent, full-duplex connection between client and server. After an initial HTTP handshake, the connection is upgraded to the WebSocket protocol and stays open.

![](assets/Pasted%20image%2020251224230759.png)

- One TCP Connection is kept open after handshake.
- Both Client & Server can send messages at any time.

Use Cases : Chat applications, real-time collaboration, gaming, Trading Platforms

### SSE - Server Sent Events (Unidirectional)

Server-Sent Events (SSE) allow the server to push updates to the client over a long-lived HTTP connection. Communication is one-way: server to client.

![](assets/Pasted%20image%2020251224230810.png)

- Client opens an HTTP connection using *EventSource*
- Server continuously streams events
- Automatic reconnects on disconnections (built-in)

Use Cases :  Live feeds, notifications, real-time dashboards
### Long-Polling

Long-polling simulates real-time behavior using repeated HTTP requests. The client sends a request, and the server holds it open until data is available or a timeout occurs.

![](assets/Pasted%20image%2020251224230819.png)

- Client sends requests
- Server waits till some event occurs
- Responds, then client immediately sends another request.

Use Cases: Simple real-time updates, fallback for WebSocket

| **Aspect**          | **WebSockets** | **Server-Sent Events** | **Long-Polling** |
| ------------------- | -------------- | ---------------------- | ---------------- |
| **Direction**       | Bi-directional | Server-to-client       | Request-response |
| **Protocol**        | WS/WSS         | HTTP/HTTPS             | HTTP/HTTPS       |
| **Complexity**      | High           | Medium                 | Low              |
| **Browser Support** | Excellent      | Good                   | Universal        |
| **Firewall/Proxy**  | May block      | HTTP-friendly          | HTTP-friendly    |
| **Overhead**        | Low            | Medium                 | High             |
| **Use Cases**       | Chat, gaming   | Feeds, dashboards      | Simple updates   |

## Common Questions

### Common Protocol Questions

- Explain the difference between TCP and UDP
    - TCP: Reliable, connection-oriented, ordered delivery
    - UDP: Fast, connectionless, no guarantees
    - Use cases for each
- How does HTTP/2 improve upon HTTP/1.1?
    - Multiplexing eliminates head-of-line blocking
    - Binary protocol reduces parsing overhead
    - Server push proactively sends resources
    - Header compression reduces bandwidth
- When would you use WebSockets vs Server-Sent Events?
    - WebSockets: Bidirectional real-time communication
    - SSE: Unidirectional server-to-client updates
    - Consider browser support and infrastructure
- How do you handle network failures in distributed systems?
    - Timeout mechanisms
    - Retry with exponential backoff
    - Circuit breaker patterns
    - Graceful degradation

### Critical Design Principles

1. **Choose the right tool for the job**: Different protocols solve different problems
2. **Plan for failure**: Networks are unreliable, design accordingly
3. **Optimize for your specific use case**: Latency vs throughput vs reliability
4. **Monitor everything**: You can't optimize what you don't measure
5. **Start simple, scale smartly**: Begin with basic solutions, add complexity as needed
