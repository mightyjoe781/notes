# Protocols

## What is a protocol

- A system that allows two parties to communicate
- A protocol is designed with a set of properties
- Depending on the purpose of the protocol
- TCP, uDP, HTTP, gRPC, FTP

## Protocol Properties

- Data Format
    - Text based (plain text, JSON, XML)
    - Binary (protobuff, RESP, h2, h3)
- Transfer Mode
    - Message Based (UDP, HTTP)
    - Stream (TCP, WebRTC)
- Addressing System
    - DNS name, IP, MAC
- Directionality
    - Bidirectional (TCP)
    - Unidirectional (HTTP)
    - Full/Half Duplex
- State
    - Stateful (TCP, gRPC, apache thrift)
    - Stateless (UDP, HTTP)
- Routing
    - proxies, gateways
- Flow & Congestion Control
    - TCP (Flow & Congestion)
    - UDP (No Control)
- Error Management
    - Error Code
    - Retries and timeouts

## Important Topics (Pre-requisites)

[OSI Layer](../../networking/neteng/fundamentals.md)
[IP](../../networking/neteng/ip.md)
[UDP](../../networking/neteng/udp.md)
[TCP](../../networking/neteng/tcp.md)
[DNS & TLS](../../networking/neteng/protocols.md)
[HTTP & its versions](../../networking/neteng/https.md)
[More Protocols](../../networking/neteng/protocols2.md)