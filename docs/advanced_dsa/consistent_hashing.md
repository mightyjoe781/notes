# Consistent Hashing
*Stable sharding with minimum reshuffling*

In a large scale distributed system, data doesn't fit on a single machine. Data is often distributed across many machines, often known as *Horizontal Scaling*,

To build such systems with predictable performance, it is important to distribute data evenly across the systems.

![](assets/Pasted%20image%2020260218092246.png)

A common method to distribute data as evenly as possible is simple hashing, like *MD5* or *MurmurHash*. This maps the object keys into a known range of numerical values,

A good hashing function would distribute hashes evenly across the range. Second we perform module on the hash with number of servers. This determines the server where data is located at.

If in above diagram if lets say server 1 goes down, we may need to recompute hash of all object and data will be reshuffled a lot.

![](assets/Pasted%20image%2020260218092906.png)

*Note* how drastic reshuffling was for data not only on the server(server 1) which left the cluster, even the rest of the data got reshuffled.

Similar scenario plays out in case we add new server, entire data gets redistributed if we use a simple hash function.

For situation where servers almost always come online and go offline, this impact is pretty drastic.

*Consistent hashing* is an effective technique to mitigate this problem. *Solves the data ownership problem,* Almost all the data remain with server and reduces shuffling.

Earlier we hashed only the object keys, now we will hash the server names as well.

![](assets/Pasted%20image%2020260218094011.png)

![](assets/Pasted%20image%2020260218094205.png)

Let's say now a new server s4 is added, in that only key k0 needs to be moved, not the rest of the data.

![](assets/Pasted%20image%2020260218094447.png)

Similarly, let's say a server is removed, in that case we don't need to do anything, only $k_0$ needs to be mapped to $s_1$ .

![](assets/Pasted%20image%2020260218094624.png)

So in conclusion, *Consistent Hashing* helps in deciding data ownership without reshuffling entire data.

### Use Cases

Example:

- Cache cluster
- Distributed DB like *Cassandra*, *DynamoDB*, etc.
- Sharded storage
- Microservices

### Uneven Distribution Problem

If we hash each node once, Some nodes may end up owning large range of keys. Conceptually we pick $n$ random point on the ring and it is rare to have even distribution.

![](assets/Pasted%20image%2020260218095153.png)

Server S1 ends up owning 3 keys in this example, S2 and S0 own no data at all, if server comes and goes all the time, it may happen that one server ends up owning a lot keys.

We use Virtual Nodes to mitigate this.

![](assets/Pasted%20image%2020260218095617.png)

In real life we use a large number of virtual nodes, rather than 3, distribute the data evenly with an overhead of maintaining metadata of those virtual nodes, which is a fair trade-off.

## More on Consistent Hashing

### Rendezvous Hashing

Simpler, no ring required. For each key

```
choose node with max hash(key, node)
```

Better uniformity

Used in

- Envoy
- Modern Distributed Systems

### Jump Consistent Hashing

- O(1) : calculation without a ring

Used in :

- Google Systems