# Communication and Protocols

## Client-Server Model and Communication Protocols

![](assets/Pasted%20image%2020251221210118.png)

![](assets/Pasted%20image%2020251221210659.png)

* most common way for machines to talk to each other.
* The communication happens over the common network connecting the two. Two protocols to exchange data TCP(mostly used) and UDP
* Some important properties of TCP
    * TCP connections requires 3-way handshake for setup
    * TCP connections requires 2-way handshake for teardown
    * TCP connection does not break immediately after data is exchanged
        * breaks might be due to network interruption 
        * breaks could be due to server/client
    * Hence connection remains open almost *forever*
* Protocol over TCP
    * TCP does not dictate what data can be sent over it.
    * Common format agreed upon by client and server is called a protocol : HTTP
* HTTP is just a format that client and server understand
* You can define your own  and make your client send data in it and server parses & process it
* There are many versions of it - HTTP 1.1/HTTP 2/ HTTP 3
* HTTP 1.1 is most commonly used one
    * For client and server to talk over HTTP 1.1, they need to establish TCP connection
    * Connection is typically *terminated* once response is sent to client
    * almost new connection for every *request/response*
    * Hence people pass : *Connection: keep-alive* header, which tells client and server to not close the connection. This depends on the server allows or not.

### Web Socket

* WebSockets are mean to do *bi-directional communication*
* Key Features : Server can proactively send data to client, without client asking for it
* Because there is no need for setting up TCP, every single time. We get really low latency in communication
* Any where we need *realtime*, *low-latency* communication. Your end user *over the internet* think about web socket.
* Use Cases - Chat (WhatsApp, Telegram, etc), Realtime likes on live stream, Stock Market ticks.

## Blob Storage and S3

* Earlier when people uploaded any files, they uploaded it to *server* and were stored on hard disk attached to it. In static websites we use `/var/www/<site>/a.txt` to store files.
* Above method does work correctly in case of Scaling Storage.
* Blob Storage/S3 is an infinitely scalable network attached storage/file-system. Any *file* that needs to be accessed by an server, is stored at a place accessible by all.
* Components of S3
    * Bucket : (namespace) e.g. my-bucket - needs to be unique
    * Keys : path of the file within bucket e.g. s3://my-bucket/user123/7829.jpg
* You can seamlessly, create the file, replace the file, delete the file, read entire file or segments of it. But these are not full fledged file systems.
* Advantages 
    * cheap, durable storage
    * can store literally any file
    * scalable and available
    * integration with a lot of AWS and Big Data Services
* Disadvantage
    * read on S3 are slow
    * So if you want quick read, you should not use S3. SSD/Hard Disk attached to instances are better for it.
    * not a full-fledged file system
* S3 Usecases
    * Database Backups
    * Logs Archival
    * Static Website Hosting
    * Infrequently accessed data dumping ground
    * Big Data Storage

## Bloom Filters

* Bloom filters are *approximate & probabilistic data structures* that says with 100 % confidence that element doesn’t belong to a set.
* For example : Instagram wants to recommend reels but it doesn’t to recommend something you saw already.
* Naive Way : keep track of everything that a user saw in a set, which will cause space-constraints
* To check existance of a key, we have to go through all the elements. Set will be BST with logarithmic insertion and existence
* Key Insight: Once something is inserted, you can’t take it out. Means when storing the actual data is not worth it, we use bloom fiters
* Filter ~ bit array. We take hash of element (needs to be hashable) and put it in the hash table represented by binary bits.
* Bloom Filter will surely will confirm non-existance of an item in the set, but doesn’t guarantee existence
* Advantage:
    * Space Efficiency
    * False Positivity Rate (increases as more and more keys are inserted)
    * Hence, when # keys increases, we have to recreate bloom-filter with larger size & populate keys again. So Estimation of max keys and provision a large one start with it.
* Redis provides bloom filter as internal data structure
* Practical Bloom Filter - Already implemented in all libraries
    * C++ :  `libbloom`
    * Python : `from pybloom_live import BloomFilter`
    * Go : `import "github.com/willf/bloom"`
* Practical Application
    * You need to insert but not remove data
    * You need a No with 100% certainity
    * having false positive is okay
* Ex - recommendation engines, web crawler, feed generators
* Resources:
    * [https://www.youtube.com/watch?v=kfFacplFY4Y](https://www.youtube.com/watch?v=kfFacplFY4Y)
    * [https://www.youtube.com/watch?v=V3pzxngeLqw](https://www.youtube.com/watch?v=V3pzxngeLqw)

## Consistent Hashing

* It only solves the problem of *Data Ownership*

### Hash Based Ownership

* Load Balancers use Ownership to find which server handles the user request. Sticky Sessions on user are a common usecase.
* Simple method is : `HASH(item) % #servers`
* If data is stateless then Hash Based Ownership Works wonderfully
* But this becomes problematic in stateful application when suddenly few servers leave the network. Only way to solve this is to repartition the data, and it could be very cumbersome task.
* Moving the data could be even more expensive then the request

### Consistent Hashing

* Consistent hashing helps determine data ownership in a distributed system, even when nodes dynamically join or leave.
* It’s visualized as a circular ring of slots, where each node is placed based on a hash function.
* The structure behaves like an ordered array with wraparound using modulo (%) to locate neighboring nodes.
* To find the owner of a key like `k1`, its hash is computed, and ownership is assigned to the first node clockwise (right) from the hash point.
* [More Here](../advanced/storage_engines.md)

### Scaling Up

* When a new node is added to the ring, it takes over responsibility for the keys that lie between it and its immediate predecessor.
* Only a subset of keys need to be moved, minimizing rebalancing.

### Scaling Down

* If a node leaves the ring, its keys are reassigned to the next clockwise node.
* This ensures data availability with minimal disruption.

NOTE: Consistent Hashing Doesn’t move the data, only answers the owner of the data.