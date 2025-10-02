# Network Routing

## Fundamentals

### Data Links

- Each device has a link address (or MAC address)
- Devices that are directly reachable devices can communicate with link address
- Using layer 2 frames
- Each device advertises their presence
- Switches in the middle remember which port each device is at
- This is critical for performance

![](assets/Pasted%20image%2020251002125714.png)

### Links

- A wants to send to B (How does A knows B's MAC ?)
- Send it across the network
- The switch receives it
- Switch knows B is at P2
- Switch only forwards the frame on port 2 (P2)

### Where links break ?

- MAC Addresses are unique but random
- They don't scale on large networks with millions of devices
- Need a new address system, a *routable one*
- IP (Internet Protocol)
- Very Similar to an Index in database

### IP Address

- Internet Protocol
- 4 bytes, 32 bit (IPv4)
- Network and host sections
- E.g. 24 bit network, 8 bit for host
- RULE: Hosts within the same network can use link address.
![](assets/Pasted%20image%2020251002130415.png)

### How to check if an IP is in my network ?

- We use the network mask or subnet mask
- e.g. 192.168.1.4 is in network 192.168.1.0/24 or 255.255.255.0
- `192.168.1.5 AND 255.255.255.0 = 192.168.1.0` (same network)
- `10.0.0.6 AND 255.255.255.0 = 10.0.0.0` (not the same network)

### ARP

- 192.168.1.4 (A) wants to send a message to 192.168.1.5 (B)
- No communication can happen unless A knows the MAC of B
- A sends a broadcast ARP request to everyone in the same network asking who has 192.168.1.5
- Only 192.168.1.5 matches accepting the message, everyone else drops it
- B now prepare to reply back A, with its MAC address

ARP Table -

```bash
# arp table
ip neigh show

# on mac/bsd
arp -a
```

### ARP Notes

- ARP only works on the same subnet
- 192.168.1.4 cannot ask for 10.0.0.2'a MAC
- no ARP request will be sent
- How do we send the request then ?

### Gateway

- For a device to talk on a device on another network needs gateway
- the gateway belongs to both networks
- Devices are aware of their gateway (configured)
- Router/Gateway is just another device with a MAC
- Switches get updated with the MACs of the connected devices

![](assets/Pasted%20image%2020251002131147.png)

### Link networking example - Same Network

- 192.168.1.4 wants to talk to 192.168.1.5 (It only knows the IP)
- Checks if its in the same network
    - 192.168.1.5 × 255.255.255.0 = 192.168.1.0, same network
    - Means we can directly communicate with data link (MAC Addresses)
    - 192.168.1.4 needs the MAC address of 192.168.1.5 (Sends ARP)
- ARP gets to the switches, sends it to all ports
- The router itself is a device, and it is not 192.168.1.5 so it doesn't response
- The ARP request is NOT sent through the other network (saving bandwidth)
- B replies back, switch sends the message only to A (why?)
- Now that we know the direct link address we send an IP packet
- Source IP: 192.168.1.4, Destination IP 192.168.1.5
- Encapsulated in a Data Link frame
- Source MAC: A, Destination MAC: B
- The frame goes to the switch, switch writes it to P2 only!
- Local link delivery

![](assets/Pasted%20image%2020251002131657.png)
### Inter-Network Communication

- 192.168.1.4 wants to send a message to 10.0.0.2
- Can't do ARP, because it is not in the same network. (No direct link)
    - 192.168.1.0 != 10.0.0.0
- Only way is the gateway (default)
    - We will learn later that routing rules are critical here
- 192.168.1.5 needs to talk to the gateway which is 192.168.1.1
- 192.168.1.5 and 192.168.1.1 in the same network
- We do ARP to get the gateway's MAC
- The gateway reply that 192.168.1.1 = X
- A now knows that X = 192.168.1.1 and prepares to send the data frame
- The IP Packet is Destination 10.0.0.2
- Source IP is 192.168.1.4
- Frame: Source MAC : A
- Frame: Dest MAC : X
- Gateway gets the frame
    - The frame is destined to gateway (X)
    - Gateway cracks the frame, sees the IP packet
    - The destination IP is NOT same as his
    - IP 10.0.0.2 is not 10.0.0.1 nor 192.168.1.1, IP Forwarding kicks in..
- IP Forwarding
    - In normal situations the packet is dropped (nothing is there
    - The OS kernel has a feature to enable IP Forwarding,
    - i.e. if you receive a frame that is for you but the IP is not for you
    - You can forward the IP packet to other interfaces
- ARP on the other network
    - The gateway now has to do an ARP on the other network
    - Who has 10.0.0.2 ? Note that Z is our MAC now.
    - We get D!
    - D replies back to the ARP
    - Goes through port P1 on switch
    - Gateway sends the packet.
- Gateway forwards the packet
    - D replies back to the ARP
    - Goes through port P1 on switch
    - Gateway sends the packet in a frame destined for D
    - Gateway keeps the source ip (unless NAT)
    - Switch sends the frame on port P2.
- Machine receives it
    - 10.0.0.2 receives the frame, it is destined for D so it accepts it.
    - Cracks open the IP packet, the IP is also destined to it 10.0.0.2
    - Kernel delivers it to the application.

### Multiple Gateways and paths ?

- You can have multiple gateways
- With one default gateway doesn't always work
- We need more granularity
- Meet the routing table

#### Routing Table

- Where do you want go? (Network)
- What is the nextHop (gateway)?
- Is it direct link or not?
- Weight (metric)
- Which interface to go through

### Who updates the Routing Table

- Kernel, DHCP, other protocols like OSPF, BGP or even manually
- Kernel - Direct network links and other administrative
- DHCP -> automatically detect and assign IPs and gateways
- OSPF -> multiple paths! Which one is the shortest?
- BGP -> On the Internet between ISPs
- Everything pours down eventually to the routing table

```bash

# windows
route print

# linux
ip route show

# mac
netstat -rn
```

### Summary

- Each device has a unique link address (Mac address) per network
- Devices can talk each other via data link and mac addresses
- Direct links can't scale for large number of devices
- IP Address was invented
- Concept of a network was born
- Routing is the key for IP and networks
## Docker

```bash
docker run -p 80:80 -d httpd

# curl from local machine should work
curl localhost:80


docker ps

docker inspect <container_id>
# notice its a bridge network, inside docker host

# docker gateway has 172.17.0.1, but curl http://172.17.0.2 doesn't work
# notice above issue with mac only
```

Create docker file with content to understand the container

```Dockerfile
FROM httpd
RUN apt-get update
RUN apt-get install -y iputils-ping
RUN apt-get install -y inetutils-traceroute
RUN apt-get install -y iproute2
RUN apt-get install -y curl telnet dnsutils vim
```

```bash
docker build . -t nhttpd
docker rm <container_id>
docker run --name s1 -d nhttpd
docker run --name s2 -d nhttpd

# curl will not work, but from inside we should be able to, as they both are in bridge network
docker inspect s1
docker inspect s2

docker inspect bridge
```

![](assets/Pasted%20image%2020251002133632.png)

```bash
docker exec -it s1 bash

> hostname -i
> 172.17.0.2

ping s1 # fails
ping s2 # fails

nslookup google.com # resolves
DNS Server : 192.168.65.5 # docker for mac has configured for internet

ping 172.17.0.2 # works
ping 172.17.0.3 # works

curl 172.17.0.3 # works

# edit in both containers, /usr/local/apache2/htdocs/index.html
# make then say hello from server - 1 / 2
```

```bash
docker network create backend --subnet 10.0.0.0/24

docker network inspect backend

docker network connect backend s1
docker network connect backend s2

docker inspect s1

```

![](assets/Pasted%20image%2020251002150647.png)

```bash
docker network disconnect bridge s1
docker network disconnect bridge s2

# exec into contianer
docker exec -it s1 bash

nslookup s1 # this work now
traceroute s1
traceroute s2

```

Spin up new network and put s1 in frontend

```bash
docker network create frontend --subnet 10.0.1.0/24
docker disconnect backend s2
docker network connect frontend s2

docker inspect s2
docker inspect s1
```

![](assets/Pasted%20image%2020251002163643.png)

### Connecting two separate network

```bash
# creating the gateway
docker run --name gw --network backend -d nhttp
docker network connect frontend gw

# login into gw
exec -it gw bash

ping s1
ping s2
```

![](assets/Pasted%20image%2020251002163624.png)

Still ping from `s1, s2` will not work for both of them.

```bash
# add a route
# sudo ip route add 10.0.0.0/24 via 10.0.1.3

docker stop s1
dokcer stop s2
docker rm s1 s2

docker run --name s1 --network backend --cap-add=NET_ADMIN -d nhttp
dokcer run --name s2 --network frontend --cap-add=NET_ADMIN -d nhttp

# s1 container, add route thru gw
docker exec -it s1 bash
> ip route add 10.0.0.0/24 via 10.0.1.3
> 

# s2 container, add route thru gw

docker exect -it s2 bash
> ip route add 10.0.1.0/24 via 10.0.0.3
> 

ping 10.0.1.2 # works
ping 10.0.0.2
```

