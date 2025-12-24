# Communication & Protocols

## Network Protocol Fundamentals

### TCP (Transmission Control Protocol)

**Connection-oriented, reliable protocol**

````text
[Client] ---- SYN -----> [Server]
[Client] <-- SYN-ACK --- [Server]  (3-way handshake)
[Client] ---- ACK -----> [Server]
[Client] <==== DATA ====> [Server]  (Reliable data transfer)
[Client] ---- FIN -----> [Server]
[Client] <--- ACK ------ [Server]  (Connection termination)
````

**Key Features**:

- Reliability: Guaranteed delivery with acknowledgments
- Ordering: Messages arrive in order
- Flow Control: Prevents overwhelming receiver
- Error Recovery: Automatic retransmission of lost packets
- Connection State: Maintains connection state

**Advantages**:

- **Data integrity**: No data loss or corruption
- **Ordered delivery**: Messages arrive in sequence
- **Built-in flow control**: Automatic congestion management

**Disadvantages**:

- **Higher latency**: Connection setup overhead
- **More bandwidth**: Headers and acknowledgments
- **Connection state**: Server must track connections

### UDP

**Connectionless, unreliable protocol**

````text
[Client] ---- DATA -----> [Server]  (No handshake)
[Client] ---- DATA -----> [Server]  (Fire and forget)
[Client] ---- DATA -----> [Server]  (No guaranteed delivery)
````

**Advantages**:

- **Low latency**: No connection setup
- **Lower overhead**: Minimal headers
- **Stateless**: Server doesn't track connections
- **Broadcast/Multicast**: Can send to multiple recipients

**Disadvantages**:

- **No reliability**: Packets may be lost
- **No ordering**: Messages may arrive out of order
- **No flow control**: Can overwhelm receiver

````python
import socket

# TCP client example
def tcp_client_example():
    # Create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Establish connection (3-way handshake)
        sock.connect(('server.example.com', 80))
        
        # Send HTTP request
        request = "GET / HTTP/1.1\r\nHost: server.example.com\r\n\r\n"
        sock.send(request.encode())
        
        # Receive response (guaranteed delivery)
        response = sock.recv(4096)
        print(response.decode())
        
    finally:
        # Close connection (proper teardown)
        sock.close()
        
# UDP client example
def udp_client_example():
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send data (no connection setup)
        message = "Hello, UDP!"
        sock.sendto(message.encode(), ('server.example.com', 53))
        
        # Receive response (if any)
        try:
            response, addr = sock.recvfrom(1024)
            print(f"Response from {addr}: {response.decode()}")
        except socket.timeout:
            print("No response received")
            
    finally:
        sock.close()
````

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

## HTTP/1.0 (1996)

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

## HTTP/1.1 (1997)

**Major Improvements**:

#### Persistent Connections

```http
# HTTP/1.1 Request with keep-alive
GET /index.html HTTP/1.1
Host: www.example.com
Connection: keep-alive

# Connection stays open for subsequent requests
GET /style.css HTTP/1.1
Host: www.example.com
Connection: keep-alive
```

#### Pipelining

```python
# Multiple requests without waiting for responses
def http_pipelining_example():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('www.example.com', 80))
    
    # Send multiple requests at once
    requests = [
        "GET /page1.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n",
        "GET /page2.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n",
        "GET /page3.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n"
    ]
    
    for request in requests:
        sock.send(request.encode())
    
    # Responses arrive in order
    for _ in requests:
        response = sock.recv(4096)
        process_response(response)
```

#### Enhanced Caching

```http
# Cache control headers
GET /api/data HTTP/1.1
Host: api.example.com
If-None-Match: "etag-123"
If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT

# Server response
HTTP/1.1 304 Not Modified
ETag: "etag-123"
Cache-Control: max-age=3600
```

#### Chunked Transfer Encoding

```http
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

- **Head-of-line blocking**: One slow request blocks others
- **Limited pipelining**: Not widely supported
- **Large headers**: Repeated headers waste bandwidth

### HTTP/2.0 (2015)

**Revolutionary Changes**:

#### Binary Protocol

```python
# HTTP/2 frame structure
class HTTP2Frame:
    def __init__(self, stream_id, frame_type, flags, payload):
        self.length = len(payload)
        self.type = frame_type     # DATA, HEADERS, SETTINGS, etc.
        self.flags = flags         # END_STREAM, END_HEADERS, etc.
        self.stream_id = stream_id # Stream identifier
        self.payload = payload
    
    def to_bytes(self):
        # Pack frame into binary format
        header = struct.pack('!LBBBL', 
                           self.length,
                           self.type,
                           self.flags,
                           self.stream_id)
        return header + self.payload
```

#### Multiplexing

```
# Single TCP connection with multiple streams
Connection: TCP
├── Stream 1: GET /index.html
├── Stream 2: GET /style.css
├── Stream 3: GET /script.js
├── Stream 4: GET /image.png
└── Stream 5: POST /api/data
```

```python
# HTTP/2 multiplexing simulation
class HTTP2Connection:
    def __init__(self):
        self.streams = {}
        self.next_stream_id = 1
    
    def send_request(self, method, path, headers=None):
        stream_id = self.next_stream_id
        self.next_stream_id += 2  # Odd numbers for client-initiated
        
        # Create new stream
        stream = HTTP2Stream(stream_id, method, path, headers)
        self.streams[stream_id] = stream
        
        # Send HEADERS frame
        headers_frame = HTTP2Frame(
            stream_id=stream_id,
            frame_type=HEADERS,
            flags=END_HEADERS,
            payload=self.encode_headers(method, path, headers)
        )
        
        self.send_frame(headers_frame)
        return stream_id
    
    def send_multiple_requests(self):
        # All requests sent concurrently
        stream1 = self.send_request('GET', '/index.html')
        stream2 = self.send_request('GET', '/style.css')
        stream3 = self.send_request('GET', '/script.js')
        
        # Responses can arrive in any order
        return [stream1, stream2, stream3]
```

#### Server Push

```python
# Server push implementation
class HTTP2Server:
    def handle_request(self, stream_id, method, path):
        if path == '/index.html':
            # Send main response
            self.send_response(stream_id, self.get_html_content())
            
            # Push related resources
            self.push_resource('/style.css', 'text/css')
            self.push_resource('/script.js', 'application/javascript')
            self.push_resource('/logo.png', 'image/png')
    
    def push_resource(self, path, content_type):
        # Server initiates push stream
        push_stream_id = self.get_next_server_stream_id()
        
        # Send PUSH_PROMISE frame
        push_promise = HTTP2Frame(
            stream_id=self.original_stream_id,
            frame_type=PUSH_PROMISE,
            flags=0,
            payload=self.encode_push_promise(push_stream_id, path)
        )
        self.send_frame(push_promise)
        
        # Send the resource
        resource_content = self.get_resource(path)
        self.send_response(push_stream_id, resource_content, content_type)
```

#### Header Compression (HPACK)

```python
# HPACK compression example
class HPACKCompressor:
    def __init__(self):
        # Static table with common headers
        self.static_table = [
            (":authority", ""),
            (":method", "GET"),
            (":method", "POST"),
            (":path", "/"),
            (":path", "/index.html"),
            (":scheme", "http"),
            (":scheme", "https"),
            (":status", "200"),
            ("cache-control", ""),
            ("content-type", "text/html"),
            # ... more entries
        ]
        self.dynamic_table = []
    
    def compress_headers(self, headers):
        compressed = []
        
        for name, value in headers:
            # Check static table
            index = self.find_in_static_table(name, value)
            if index:
                compressed.append(('indexed', index))
                continue
            
            # Check dynamic table
            index = self.find_in_dynamic_table(name, value)
            if index:
                compressed.append(('indexed', index + len(self.static_table)))
                continue
            
            # Add to dynamic table and encode literally
            self.dynamic_table.append((name, value))
            compressed.append(('literal', name, value))
        
        return self.encode_compressed_headers(compressed)
```

**Benefits**:

- **Multiplexing**: No head-of-line blocking
- **Server push**: Proactive resource delivery
- **Header compression**: Reduced overhead
- **Stream priorities**: Important requests first

### HTTP/3.0 (2022)

**Built on QUIC (UDP-based)**:

#### QUIC Protocol Features

```python
# QUIC connection establishment
class QUICConnection:
    def __init__(self):
        self.streams = {}
        self.connection_id = self.generate_connection_id()
        self.encryption_keys = None
    
    def establish_connection(self, server_addr):
        # 0-RTT or 1-RTT handshake
        initial_packet = self.create_initial_packet()
        
        # QUIC handshake combines connection and TLS setup
        handshake_packet = QUICPacket(
            packet_type=INITIAL,
            connection_id=self.connection_id,
            payload=initial_packet
        )
        
        # Send over UDP
        self.udp_socket.sendto(handshake_packet.to_bytes(), server_addr)
        
        # Receive handshake response
        response = self.udp_socket.recv(1500)
        self.process_handshake_response(response)
```

#### Stream Independence

```
# QUIC streams are independent
UDP Connection
├── Stream 1: /index.html (blocked by packet loss)
├── Stream 2: /style.css (continues processing)
├── Stream 3: /script.js (continues processing)
└── Stream 4: /image.png (continues processing)
```

```python
# Independent stream processing
class HTTP3Stream:
    def __init__(self, stream_id, connection):
        self.stream_id = stream_id
        self.connection = connection
        self.receive_buffer = []
        self.packet_numbers = set()
    
    def receive_packet(self, packet):
        if packet.packet_number in self.packet_numbers:
            return  # Duplicate packet
        
        self.packet_numbers.add(packet.packet_number)
        
        # Process packet immediately (no head-of-line blocking)
        if self.is_complete_frame(packet):
            self.process_frame(packet.payload)
        else:
            self.receive_buffer.append(packet)
            self.try_reassemble()
    
    def handle_packet_loss(self, lost_packet_number):
        # Only affects this stream, not others
        self.request_retransmission(lost_packet_number)
```

#### 0-RTT Connection Resumption

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

- **No head-of-line blocking**: UDP-based streams
- **Faster connection setup**: Combined handshake
- **Better mobility**: Connection migration
- **Improved congestion control**: Per-stream control

## HTTPS and Security

### TLS Handshake Process

````text
[Client] ---- ClientHello -----> [Server]
[Client] <--- ServerHello ------ [Server]
[Client] <--- Certificate ------ [Server]
[Client] <--- ServerDone ------- [Server]
[Client] -- ClientKeyExchange -> [Server]
[Client] -- ChangeCipherSpec --> [Server]
[Client] ---- Finished --------> [Server]
[Client] <-- ChangeCipherSpec -- [Server]
[Client] <----- Finished ------ [Server]
````

#### Certificate Validation

```python
import ssl
import socket

def verify_certificate(hostname, port=443):
    # Create SSL context with verification
    context = ssl.create_default_context()
    
    # Connect and verify certificate
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            
            # Check certificate details
            print(f"Subject: {cert['subject']}")
            print(f"Issuer: {cert['issuer']}")
            print(f"Version: {cert['version']}")
            print(f"Serial Number: {cert['serialNumber']}")
            print(f"Not Before: {cert['notBefore']}")
            print(f"Not After: {cert['notAfter']}")
            
            # Verify hostname
            ssl.match_hostname(cert, hostname)
            print(f"Certificate verified for {hostname}")
```

### Modern Security Features

#### HTTP Strict Transport Security (HSTS)

```http
# HSTS header forces HTTPS
HTTP/1.1 200 OK
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

#### Certificate Transparency

## Real-time Communication Patterns

### WebSockets vs Server-Sent Events vs Long-Polling

#### WebSockets (Bi-directional)

```javascript
// Client-side WebSocket
const ws = new WebSocket('wss://example.com/chat');

ws.onopen = function(event) {
    console.log('Connected to WebSocket');
    ws.send(JSON.stringify({type: 'join', room: 'general'}));
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('Received:', message);
};

ws.send(JSON.stringify({
    type: 'message',
    text: 'Hello, everyone!',
    timestamp: Date.now()
}));
```

```python
# Server-side WebSocket (using asyncio)
import asyncio
import websockets
import json

class WebSocketServer:
    def __init__(self):
        self.clients = set()
        self.rooms = {}
    
    async def register_client(self, websocket, path):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.handle_message(websocket, data)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
    
    async def handle_message(self, websocket, data):
        if data['type'] == 'join':
            room = data['room']
            if room not in self.rooms:
                self.rooms[room] = set()
            self.rooms[room].add(websocket)
            
        elif data['type'] == 'message':
            # Broadcast to all clients in room
            room = self.get_client_room(websocket)
            if room and room in self.rooms:
                message = {
                    'type': 'broadcast',
                    'text': data['text'],
                    'timestamp': data['timestamp']
                }
                await self.broadcast_to_room(room, message)
    
    async def broadcast_to_room(self, room, message):
        if room in self.rooms:
            tasks = []
            for client in self.rooms[room].copy():
                tasks.append(self.send_safe(client, json.dumps(message)))
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def send_safe(self, websocket, message):
        try:
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            # Client disconnected
            pass

# Start server
server = WebSocketServer()
start_server = websockets.serve(server.register_client, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
```

**Use Cases**: Chat applications, real-time collaboration, gaming

#### Server-Sent Events (Unidirectional)

```javascript
// Client-side SSE
const eventSource = new EventSource('/events');

eventSource.onopen = function(event) {
    console.log('SSE connection opened');
};

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received update:', data);
};

eventSource.addEventListener('custom-event', function(event) {
    console.log('Custom event:', event.data);
});

// Handle connection errors
eventSource.onerror = function(event) {
    console.log('SSE error:', event);
};
```

```python
# Server-side SSE (Flask example)
from flask import Flask, Response
import json
import time
import threading

app = Flask(__name__)

class SSEManager:
    def __init__(self):
        self.clients = []
        self.start_background_updates()
    
    def add_client(self):
        client_queue = queue.Queue()
        self.clients.append(client_queue)
        return client_queue
    
    def remove_client(self, client_queue):
        if client_queue in self.clients:
            self.clients.remove(client_queue)
    
    def broadcast(self, event_type, data):
        message = f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
        
        dead_clients = []
        for client_queue in self.clients:
            try:
                client_queue.put(message, timeout=1)
            except queue.Full:
                dead_clients.append(client_queue)
        
        # Remove unresponsive clients
        for dead_client in dead_clients:
            self.remove_client(dead_client)
    
    def start_background_updates(self):
        def update_loop():
            while True:
                # Send periodic updates
                self.broadcast('status', {
                    'timestamp': time.time(),
                    'message': 'System status update'
                })
                time.sleep(30)
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()

sse_manager = SSEManager()

@app.route('/events')
def events():
    def event_stream():
        client_queue = sse_manager.add_client()
        try:
            while True:
                try:
                    message = client_queue.get(timeout=30)
                    yield message
                except queue.Empty:
                    # Send heartbeat
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
        finally:
            sse_manager.remove_client(client_queue)
    
    return Response(
        event_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

@app.route('/notify/<message>')
def notify(message):
    sse_manager.broadcast('notification', {'message': message})
    return 'Notification sent'
```

**Use Cases**: Live feeds, notifications, real-time dashboards

#### Long-Polling

```javascript
// Client-side long-polling
class LongPolling {
    constructor(url) {
        this.url = url;
        this.running = false;
    }
    
    start() {
        this.running = true;
        this.poll();
    }
    
    stop() {
        this.running = false;
    }
    
    async poll() {
        while (this.running) {
            try {
                const response = await fetch(this.url, {
                    method: 'GET',
                    headers: {
                        'Cache-Control': 'no-cache'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    this.onMessage(data);
                }
                
                // Small delay before next poll
                await this.sleep(1000);
                
            } catch (error) {
                console.error('Polling error:', error);
                await this.sleep(5000); // Longer delay on error
            }
        }
    }
    
    onMessage(data) {
        console.log('Received:', data);
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Usage
const poller = new LongPolling('/api/poll');
poller.start();
```

```python
# Server-side long-polling
from flask import Flask, jsonify, request
import asyncio
import time

app = Flask(__name__)

class LongPollingServer:
    def __init__(self):
        self.pending_requests = []
        self.message_queue = []
    
    def add_message(self, message):
        self.message_queue.append(message)
        self.notify_pending_requests()
    
    def notify_pending_requests(self):
        # Notify all pending requests
        for request_handler in self.pending_requests:
            request_handler.set_result(self.message_queue.copy())
        
        self.pending_requests.clear()
        self.message_queue.clear()
    
    async def wait_for_messages(self, timeout=30):
        if self.message_queue:
            # Return immediately if messages available
            messages = self.message_queue.copy()
            self.message_queue.clear()
            return messages
        
        # Wait for new messages
        future = asyncio.Future()
        self.pending_requests.append(future)
        
        try:
            # Wait with timeout
            return await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            # Remove from pending requests
            if future in self.pending_requests:
                self.pending_requests.remove(future)
            return []

polling_server = LongPollingServer()

@app.route('/api/poll')
async def poll():
    # Long-polling endpoint
    messages = await polling_server.wait_for_messages(timeout=30)
    return jsonify({
        'messages': messages,
        'timestamp': time.time()
    })

@app.route('/api/send/<message>')
def send_message(message):
    polling_server.add_message({
        'text': message,
        'timestamp': time.time()
    })
    return 'Message sent'
```

**Use Cases**: Simple real-time updates, fallback for WebSocket

| **Aspect**          | **WebSockets** | **Server-Sent Events** | **Long-Polling** |
| ------------------- | -------------- | ---------------------- | ---------------- |
| **Direction**       | Bi-directional | Server-to-client       | Request-response |
| **Protocol**        | WS/WSS         | HTTP/HTTPS             | HTTP/HTTPS       |
| **Complexity**      | High           | Medium                 | Low              |
| **Browser Support** | Excellent      | Good                   | Universal        |
| **Firewall/Proxy**  | May block      | HTTP-friendly          | HTTP-friendly    |
| **Overhead**        | Low            | Medium                 | High             |
| **Use Cases**       | Chat, gaming   | Feeds, dashboards      | Simple updates   |

## Interview Tips and Common Questions

### Common Protocol Questions

1. "Explain the difference between TCP and UDP"
   - TCP: Reliable, connection-oriented, ordered delivery
   - UDP: Fast, connectionless, no guarantees
   - Use cases for each
2. "How does HTTP/2 improve upon HTTP/1.1?"
   - Multiplexing eliminates head-of-line blocking
   - Binary protocol reduces parsing overhead
   - Server push proactively sends resources
   - Header compression reduces bandwidth
3. "When would you use WebSockets vs Server-Sent Events?"
   - WebSockets: Bidirectional real-time communication
   - SSE: Unidirectional server-to-client updates
   - Consider browser support and infrastructure
4. "How do you handle network failures in distributed systems?"
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
