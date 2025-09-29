# Fundamentals of Networking

## Client Server Architecture

![](assets/Pasted%20image%2020250928230335.png)

- Machines are expensive, applications are complex
- Separate the application in two components
- Expensive workload can be done on the server
- Clients call servers to perform expensive tasks
- Remote Procedure call (RPC) was born

- Servers have beefy hardware
- Clients have commodity hardware
- Clients can still perform lightweight tasks
- Clients no longer require dependencies
- However, we need a communication model
## OSI Model

Open Systems Interconnection model

### Why do we need a communication model ?

- Agnostic application
    - Without a standard model, your application must have knowledge of the underlying network medium
    - Imagine if you have to author different version of your apps so that it works on WiFi vs Ethernet vs LTE vs fiber
- Network Equipment Management
    - Without a standard model, upgrading network equipments becomes difficult
- Decoupled Innovation
    - Innovations can be done in each layer separately without affecting the rest of the models.

### What is the OSI Model ?

- 7 layers each describe a specific networking component
- Layer 7 - Application - HTTP/FTP/gRPC
- Layer 6 - Presentation - Encoding, Serialization
- Layer 5 - Session - Connection Establishment
- Layer 4 - Transport - UDP/TCP
- Layer 3 - Network - IP
- Layer 2 - Data link - Frames, Mac Address Ethernet 
- Layer 1 - Physical - Electric signals, Fiber or radio waves

Mnemonic : *Please do not throw pizza sausage away* or *All people seem to need data processing*


![](assets/Pasted%20image%2020250928233602.png)
### The OSI Layers - an Example (Sender)

- Example sending a POST request. to HTTPS webpage
- Layer 7 - Application
    - POST request with JSON data to HTTPs server
- Layer 6 - Presentation
    - Serialize JSON to flat byte strings
- Layer 5 - Session
    - Request to establish TCP connection/TLS
- Layer 4 - Transport
    - Sends SYN request target port 443
- Layer 3 - Network
    - SYN is placed an IP packet(s) and adds source/destination IPs
- Layer 2 - Data Link
    - Each packet. goes into a single frame and adds the source/destination MAC Address
- Layer 1 - Physical
    - Each frame becomes string of bits which converted into either a radio wave, electric signal or light.

### The OSI Layers - an Example (Receiver)

- Receiver computer receives the POST request other way round
- Layer 1 - Physical
    - Radio, electric or light is received and converted into digital bits
- Layer 2 - Data Link
    - The bis from Layer 1 are assembled into frames
- Layer 3 - Network
    - The frames from layer 2 are assembled into IP packet
- Layer 4 - Transport
    - The IP packets from layer 3 are assembled into TCP segments
    - Deals with Congestion Control/flow control/retransmission in case of TCP
    - If segment is SYN we don't need to go further into more layers as we are still processing the connection request
- Layer 5 - Session
    - Connection session is established or identified
    - We only arrive at this layer when necessary (3 way handshake is done)
- Layer 6 - Presentation
    - deserialize flat byte strings back to JSON for the app to consume
- Layer 7 - Application
    - Application understands the JSON POST request and your express json/apache request receive event is triggered.

![](assets/Pasted%20image%2020250928234408.png)

![](assets/Pasted%20image%2020250928235214.png)

- Notice how at load balancer level deciphering of the encryption is done already.
- VPNs are at layer 3, they can swap IPs in packets there

### Shortcomings of OSI Model

- OSI Model has too many layers which can be hard to comprehend
- Hard to argue about which layer does what
- Simpler to deal with Layers 5-6-7 as just one layer, application
- TCP/IP Model does just that.

### TCP/IP Model

- Much simpler than OSI just 4 layers
- Application (Layer 5, 6 and 7)
- Transport (Layer 4)
- Internet (Layer 3)
- Data link (Layer 2)
- Physical layer is not officially covered in the model
## Host to Host Communications

![](assets/Pasted%20image%2020250929081028.png)

*How messages are sent between host* ~ Layer2/3 concepts

-  I need to send a message from host A to host B
- Usually a request to do something on host B (RPC)
- Each host network card has a unique Media Access Control (MAC)
- E.g. `00:00:5e:00:53:aa`
- A send a message to B specifying MAC address
- Everyone in the network will `get` the message but only B will accept it.

![](assets/Pasted%20image%2020250929081927.png)

- Imagine with million machine above topology of network will be inefficient
- We can add routing-ability to current addressing scheme to make it better ~ *IP Address*


- The IP Address is built in two parts
- One part identifies the network, other is the host
- We use the network portion to eliminate many networks
- The host part is used to find the host
- Still needs MAC Address!

![](assets/Pasted%20image%2020250929083105.png)

- Above diagram in IP format

![](assets/Pasted%20image%2020250929083117.png)

But my host have many apps !

- It's not enough to just address the host
- The host is running many apps each with different requirements ~ *Ports
- You can send an HTTP request on port 80, a DNS request on port 53 and an SSH request on port 22 all running on the same server!