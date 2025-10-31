# Hybrid Networking

## Static Routing vs Dynamic Routing

### AS - Autonomous Systems

- Routers controlled by one entity in a network
- Assigned by IANA for Public ASN (1-64495)
- Private ASN (64512-65534)

![](assets/Pasted%20image%2020251027160909.png)

### Static Routing


![](assets/Pasted%20image%2020251027161044.png)

- Each new additional router will require manually updating the Route Tables in Router A
- Assume Router C joins the router B, then unless Route tables not added to router A, it will simply drop requests for 10.30.0.0/16

![](assets/Pasted%20image%2020251027161412.png)

![](assets/Pasted%20image%2020251027161558.png)

### Dynamic Routing

- This same entry is automatically propagated in Dynamic Routing

![](assets/Pasted%20image%2020251027161640.png)

## How Border Gateway Protocol (BGP) works ?

### BGP - Border Gateway Protocol

- Dynamic Routing using Path-Vector protocol where it exchanges the best path to a destination between peers or AS (ASPATH)
- iBGP - Routing within AS
- eBGP - Routing between AS's
- Routing decision is influenced by
    - Weight - (Cisco routers specific - works within AS)
    - ASPATH - Series of AS's to traverse the path (Works between AS)
    - Local Preference *LOCAL_PREF* (works within AS)
    - MED - Multi-Exit Discriminator (Works between AS)

![](assets/Pasted%20image%2020251027161927.png)

![](assets/Pasted%20image%2020251027162223.png)

![](assets/Pasted%20image%2020251027162243.png)
![](assets/Pasted%20image%2020251027162303.png)

Summary 

- Highest Weight
    - Cisco routers specific attribute
    - Works within AS and set by originating router
    - Not exchanged between external BGP routers
- Highest local preference
    - Choose the outbound external BGP path
    - Set by the local AS for internal BGP routers
    - Not exchanged between external BGP routers
    - Default value 100
- Shorted AS Path
    - As path can be modified using AS path prepend to make it appear longer
- Lowest MED
    - Used when there are multiple paths between two ASs
    - MED is exchanged between autonomous systems


