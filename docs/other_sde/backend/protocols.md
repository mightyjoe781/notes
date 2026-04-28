# Protocols

## What Is a Protocol

A system that defines how two parties communicate, designed around a specific set of properties depending on its purpose. Examples: TCP, UDP, HTTP, gRPC, FTP.

## Protocol Properties

- **Data Format**
    - Text-based: plain text, JSON, XML
    - Binary: Protobuf, RESP, HTTP/2, HTTP/3
- **Transfer Mode**
    - Message-based: UDP, HTTP
    - Stream: TCP, WebRTC
- **Addressing System**
    - DNS name, IP, MAC
- **Directionality**
    - Bidirectional: TCP
    - Unidirectional: HTTP
    - Full / half duplex
- **State**
    - Stateful: TCP, gRPC, Apache Thrift
    - Stateless: UDP, HTTP
- **Routing**
    - Proxies, gateways
- **Flow & Congestion Control**
    - TCP: both flow and congestion control
    - UDP: no control
- **Error Management**
    - Error codes
    - Retries and timeouts

## Prerequisites

[OSI Layer](../../networking/neteng/fundamentals.md)  
[IP](../../networking/neteng/ip.md)  
[UDP](../../networking/neteng/udp.md)  
[TCP](../../networking/neteng/tcp.md)  
[DNS & TLS](../../networking/neteng/protocols.md)  
[HTTP & its versions](../../networking/neteng/https.md)  
[More Protocols](../../networking/neteng/protocols2.md)
