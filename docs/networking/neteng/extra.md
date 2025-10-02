# Extra Topics

## Exposing local servers locally

when we build a local web server listening on a private IP on LAN, only hosts from same network can access it. To expose it to outside we require NAT.

SSH tunneling and ngrok are examples of services that allow us to do that.

- Public IP Address ~ IP is routable through the internet
- Private IP Address  ~ only hosts local to that network can access it

Yet router has a public reachable ip address. You can add port forwarding rules on your router public ip and to port 8080, allowing external traffic. But this requires to be admin to modify router settings.

Another way is using Remote Port Forwarding. If we create a VPS server, we can remotely command it to forward packets on a specific port to us on the local server. Problem still remains same, we can't receive data, so we connect to it directly.

- The local agent running will connect to public agent
- The local agent commands public agent to listen on a port
- the local agent commands public agent to link listen port to its address
- A new connection attempt to public agent
- client sends data to public agent on connection
- Local server responds

SSH supports Local Port Forwarding which allows your local client to access hosts in a private network that a public agent also lives in. 
So public agent has a public IP and it also has a private IP, using the public IP we can connect to public agent, and then public agent using the private network, it can connect to final Private Hosts.
Useful to access a machine at work when there a public SSH server exposed.

To do a local port forwarding ing SSH:

```bash
ssh -L local_port:remote_address:remote_port username@sshserver
```

To do a remote port forwarding in SSH

```bash
ssh -L remote_port:local_adress:local_port username@sshserver
```


## What is SNI (server name indication TLS Extension)

SNI (Server Name Indication) is an extension of the TLS (Transport Layer Security) protocol. It allows a client to specify the hostname it wants to connect to during the TLS handshake. This is particularly useful for hosting multiple websites on a single IP address, enabling the server to present the correct SSL/TLS certificate for the requested hostname.

| Aspect    | Description                                                     |
| --------- | --------------------------------------------------------------- |
| Full form | Server Name Indication                                          |
| Purpose   | Allows multiple SSL certificates on one IP address<br>          |
| Function  | Sends hostname during TLS handshake                             |
| Benefit   | Facilitates hosting of multiple secure sites on a single server |

## Replacing TCP for Data Centers

Paper ~ https://arxiv.org/abs/2210.00714
Explanation ~ https://www.youtube.com/watch?v=nEFOni_87Yw




## Postgres failure caused by a Cisco router (TCP Issues)

A Postgres client lost its connection after 90 minutes because the Cisco router between client and server dropped the idle TCP session after its 60-minute default timeout. Since the client was busy processing data locally and no packets were exchanged, the router cleared the state, though both client and server still thought the connection was alive. When the client tried to reuse the connection, the router dropped the packet. The fix was to configure Postgres tcp_keepalives_idle to send keep-alive messages sooner (under 60 minutes), instead of relying on Windows’ 2-hour default, ensuring the router’s idle timeout isn’t triggered.
