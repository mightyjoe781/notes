# Sockets


## Introduction

*A socket is an endpoint for bidirectional communication between two processes over a network, identified by (IP, PORT, PROTOCOL)*

| TCP                 | UDP                    |
| ------------------- | ---------------------- |
| Reliable            | Unreliable             |
| Ordered             | No Ordering            |
| Connection Oriented | Connections            |
| Used for Chat, HTTP | Used for Video, Games, |

## Minimal TCP Server & Client

### Minimal TCP Server

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9000))
server.listen()

conn, addr = server.accept()
data = conn.recv(1024)
conn.sendall(b"Hello Client")
conn.close()
```

### Minimal TCP Client

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9000))
client.sendall(b"Hello Server")
print(client.recv(1024))
client.close()
```

NOTE: TCP is a byte stream. So sending two messages in the stream, `recv()` will not receive them separately. Message Boundaries in a stream are not preserved.

Solution to above problem is :

- Fixed Size Messages
- Length-prefixed messages
- Delimiter-based


## Simple Chat Application using Sockets

Note: Its a simple 1-server, 1-client application.

Server

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9000))
server.listen()

print("Server listening...")
conn, addr = server.accept()
print("Connected:", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Client:", data.decode().strip())
    reply = input("You: ")
    conn.sendall((reply + "\n").encode())

conn.close()
```

Client Code

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9000))

while True:
    msg = input("You: ")
    client.sendall((msg + "\n").encode())
    data = client.recv(1024)
    print("Server:", data.decode().strip())
```

NOTE:

- We used `sendall` to ensure that full buffer is transmitted, rather than sending the part of data.
- If client disconnects, then server returns empty bytes `b''`, indicating a connection close
- To handle multiple client we will need to use threading, multiprocessing, select/poll or async I/O
- Above code is not OS dependent, socket API is standard
- `AF_INET` : Address family for IPv4 addresses.
- `SOCK_STREAM` : Socket type for TCP (Transmission Control Protocol). It indicates a connection-oriented, reliable data stream.