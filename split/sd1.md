# Sd Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: sd
This is part 1 of 1 parts

---

## File: sd/company.md

# Real-world Systems and Architectures

## Social Media and Messaging

- Facebook Timeline: Brought To You By The Power Of Denormalization - https://goo.gl/FCNrbm
- Scale at Facebook - https://goo.gl/NGTdCs
- Building Timeline: Scaling up to hold your life story - https://goo.gl/8p5wDV
- Erlang at Facebook (Facebook chat) - https://goo.gl/zSLHrj
- Facebook Chat Architecture - https://goo.gl/qzSiWC
- Finding a Needle in Haystack: Facebook’s Photo Storage - https://goo.gl/edj4FL
- Serving Facebook Multifeed: Efficiency, Performance Gains Through Redesign - https://goo.gl/adFVMQ
- Scaling Memcache at Facebook - https://goo.gl/rZiAhX
- TAO: Facebook’s Distributed Data Store for the Social Graph - https://goo.gl/Tk1DyH
- The WhatsApp Architecture Facebook Bought For $19 Billion - https://bit.ly/2AHJnFn

## E-Commerce & Cloud Infrastructure

- Amazon Architecture - https://goo.gl/k4feoW
- Dynamo: Amazon’s Highly Available Key-value Store - https://goo.gl/C7zxDL
- Scaling Uber’s Marketplace Platform - https://goo.gl/kGZuVy
- How Uber Handles 14 Million Rides Per Day - https://eng.uber.com/uber-architecture/
- Scaling Pinterest - https://goo.gl/KtmjW3
- Pinterest Architecture Update - https://goo.gl/w6rRsf
- A Brief History of Scaling LinkedIn - https://goo.gl/8A1Pi8
- How We've Scaled Dropbox - https://goo.gl/NjBDtC
- Flickr Architecture - https://goo.gl/dWtgYa

## Streaming & Entertainment

- A 360-Degree View of the Netflix Stack - https://goo.gl/rYSDTz
- It’s All A/Bout Testing: The Netflix Experimentation Platform - https://goo.gl/agbA4K
- Netflix Recommendations: Beyond the 5 Stars (Part 1) - https://goo.gl/A4FkYi
- Netflix Recommendations: Beyond the 5 Stars (Part 2) - https://goo.gl/XNPMXm
- YouTube Architecture - https://goo.gl/mCPRUF
- Seattle Conference on Scalability: YouTube Scalability - https://goo.gl/dH3zYq

## Search & Big Data

- Google Architecture - https://goo.gl/dvkDiY
- The Google File System (Google Docs) - https://goo.gl/xj5n9R
- Differential Synchronization (Google Docs) - https://goo.gl/9zqG7x
- Bigtable: A Distributed Storage System for Structured Data - https://goo.gl/6NaZca

## Microservices, Databases, and Scalability

- Announcing Snowflake (A Network Service for Generating Unique ID Numbers at High Scale) - https://goo.gl/GzVWYm
- Timelines at Scale - https://goo.gl/8KbqTy
- How Twitter Scales for 150M+ Active Users - https://goo.gl/EwvfRd
- Scaling Twitter: Making Twitter 10000 Percent Faster - https://goo.gl/nYGC1k
- Building Scalable Payment Systems at PayPal - https://engineering.paypal.com/scaling
- Scaling Reddit’s Web Stack - https://www.redditinc.com/blog/scaling-reddit

---

# List of Company Engineering Blogs

## Tech Companies

- Airbnb - https://medium.com/airbnb-engineering
- Amazon - https://developer.amazon.com/blogs
- Apple Machine Learning Research - https://machinelearning.apple.com/
- Asana - https://blog.asana.com/category/eng
- Atlassian - https://developer.atlassian.com/blog
- Dropbox - https://blogs.dropbox.com/tech
- Facebook - https://code.facebook.com/posts
- GitHub - https://githubengineering.com
- Google - https://developers.googleblog.com
- LinkedIn - https://engineering.linkedin.com/blog
- Netflix - https://medium.com/netflix-techblog
- Quora - https://engineering.quora.com
- Reddit - https://redditblog.com
- Salesforce - https://developer.salesforce.com/blogs/engineering
- Shopify - https://engineering.shopify.com
- Slack - https://slack.engineering
- Spotify - https://labs.spotify.com
- Stripe - https://stripe.com/blog/engineering
- System Design Primer - https://github.com/donnemartin/system-design-primer
- Twitter - https://blog.twitter.com/engineering/enus.html
- Uber - http://eng.uber.com
- Yahoo - https://yahooeng.tumblr.com
- Yelp - https://engineeringblog.yelp.com
- Zoom - https://medium.com/zoom-developer-blog

## Cloud, DevOps & Infrastructure

- Cloudflare - https://blog.cloudflare.com/
- Docker - https://blog.docker.com
- Kubernetes Blog - https://kubernetes.io/blog/
- Terraform by HashiCorp - https://www.hashicorp.com/blog
- Grafana Labs - https://grafana.com/blog/
- Fastly Blog - https://www.fastly.com/blog/

## AI & Data Science

- OpenAI Blog - https://openai.com/research/
- DeepMind Blog - https://www.deepmind.com/blog/
- Meta AI Research - https://ai.facebook.com/research/
- Google AI - https://ai.googleblog.com/
- Hugging Face Blog - https://huggingface.co/blog
- NVIDIA AI - https://developer.nvidia.com/blog/

## Security & Privacy

- Google Security Blog - https://security.googleblog.com/
- Microsoft Security Blog - https://www.microsoft.com/security/blog/
- Cloudflare Security - https://blog.cloudflare.com/tag/security/
- OWASP Blog - https://owasp.org/www-blog/
- Tailscale Blog - https://tailscale.com/blog/

---

# Additional Resources on System Design & Scalability

## Books

- Designing Data-Intensive Applications - https://dataintensive.net/
- Site Reliability Engineering (SRE) by Google - https://landing.google.com/sre/
- The Phoenix Project: DevOps and Continuous Delivery - https://itrevolution.com/product/the-phoenix-project/
- The Art of Scalability - https://www.amazon.com/Art-Scalability-Scalable-Designs-Organizations/dp/0321636408/
- High Performance MySQL - https://www.oreilly.com/library/view/high-performance-mysql/9780596101718/

## GitHub Repositories

- System Design Primer - https://github.com/donnemartin/system-design-primer
- Awesome Scalability - https://github.com/binhnguyennus/awesome-scalability
- The Algorithms - Python - https://github.com/TheAlgorithms/Python
- Awesome Data Engineering - https://github.com/igorbarinov/awesome-data-engineering

---

## File: sd/hld/cache.md

# Caching and Optimization

## What is Caching

* caches are anything that helps you avoid an expensive *network I/O*, *disk I/O* or computation.
  * API call to get profile information
  * reading specific line from a file
  * doing multiple table joins
* Frequently accessed data is stored in a temporary location. The API server first checks the cache. If the item is not present, it fetches it from the actual database and stores it in the cache.
* Cache are faster and expensive. Cache is not a breaking point in a design, it helps improve the design.
* Caches are just glorified hash tables
* Examples
  * Google News
  * Auth Tokens
  * Live Stream

## Populating and Scaling a Cache

* cache is put in between API server and database
* Lazy Population (most popular)
  * Read first goes to cache, if data exists return it, or else fetch from db, store in cache, and then return
  * Ex - Caching Blogs, (multiple joins involved)
* Eager Population
  * Writes go to both database and cache in the request call. Ex - live cricket score
  * Proactively push data to cache, because you anticipate the need. Ex - Twitter Celebrity Problem

## Caching at Different Levels

* Caching can placed at everywhere, but it comes with a cost of stale data and invalidation. Caching is ideally a very difficult problem to solve perfectly, you only need to approximate your usecase solution.

### Client Side Caching

* storing frequently accessed data on client side. Ex - browser, mobile devices, etc
* cache near constant data (e.g. images, ui components, user information)
* it should be okay serving cached info (stale)
* invalidation by time (expiry)

Massive Performance boost, as we need not make any requests to backend

### Content Delivery Networks (CDN)

* CDNs are a set of servers distributed across the world, used for caching
* request from a user goes to geographically nearest CDN server and user gets a quick response.
* Example - this site is hosted in Dublin, and ideally would be slower to load from India, but a CDN for a user in India will make it fast. For this site, I am using Cloudflare CDN.
* CDN does lazy cache population!

### Remote Cache (Redis)

* Centralized cache that we most commonly use (Redis). Multiple API servers use it to store frequently accessed data.
* Every key stored should have an expiration date(memory leak)
* Size of cache is relatively very small as compared to a database

### Database Caching

* Instead of computing total post by users every time, we store `total_posts` as column and update it once in a while (saves an expensive DB computation)
* This often involves re-evaluating the data model.



NOTE:

* There are other places like load Balancer where we can use cache.
* We can cache some data at every single component, and it should be used sparingly because make sure that staleness of the data doesn’t affect the speed of your component.
* Cache Invalidation is really hard to solve problem.





---

## File: sd/hld/communication.md

# Communication and Protocols

## Client-Server Model and Communication Protocols

* most common way for machines to talk to each other.
* The communication happens overt the common network connecting the two. Two protocols to exchange data TCP(mostly used) and UDP
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

* Websockets are mean to do *bi-directional communication*
* Key Features : Server can proactively send data to client, without client asking for it
* Because there is no need for setting up TCP, every single time. We get really low latency in communication
* Any where we need *realtime*, *low-latency* communication. Your end user *over the internet* think about web socket.
* Use Cases - Chat, Realtime likes on live stream, Stock Market ticks.

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

### Scaling Up

* When a new node is added to the ring, it takes over responsibility for the keys that lie between it and its immediate predecessor.
* Only a subset of keys need to be moved, minimizing rebalancing.

### Scaling Down

* If a node leaves the ring, its keys are reassigned to the next clockwise node.
* This ensures data availability with minimal disruption.

NOTE: Consistent Hashing Doesn’t move the data, only answers the owner of the data.


---

## File: sd/hld/db.md

# Databases and Scaling

* most important component of any system

## Relational Databases

* Data is stored and represented in rows & column 

History of Relational Databases

* Computers first did *accounting* -> *ledgers* -> *Rows & Columns*
* Databases were developed to support accounting
* Key Properties
  * Data consistency
  * Data durability
  * Data integrated
  * Constraints
  * Everything in one place
* Because of this reason, relational databases provides ACID properties to support *Transactions*

* A - Atomicity
* C - Consistency
* I - Isolation
* D - Durability
* [Lecture on ACID by Martin Klepmann](https://www.youtube.com/watch?v=5ZjhNTM8XU8)

### Atomicity

* All statements within a transaction takes effect or non
* e.g. start transaction { publish a post and increase total posts count } commit
* Often confused with concurrency, while it actually defines how system recovers from faults (rollback). Should have been called *Abortability*.

### Consistency

* `C` in ACID is not same as one in CAP Theorem.
* C is more like a term thrown around to make the acronym work. It defines that data will always move from one consistent state to another.
* Defn : Data will never go incorrect, no matter what. Constraint, Cascades, Triggers ensure above property
* Ex - In a Financial system, all the debits must add up to equal to credits. 
* Foreign Keys Checks ensure parent cant’ be deleted if child exists (can be turned on in DB). You can enable cascades or triggers to ensure data comes back to consistent state.

### Durability

* when transaction commits, the changes outlives outage.
* When archive tapes were used, you can restore database back from its initial state to final state using archives.

### Isolation

* when multiple transactions are executing parallely, the *isolation level* determines how much changes of one trasactions are visible to other.
* Serializable ? Effect of all txn is as if they have executed serially. In Comparch people realised it was little slow they fiddled around locks to figure out to make it work fast.

## Database Isolation Levels

* Isolation levels dictate how much one transaction knows about the other

### Repeatable Reads

* consistent reads within same transaction
* Even if other transaction commited 1st transaction would not see the changes (if value is already read)
* Default in Postgres, Oracle, SQL Server. 
* It guarantees : both dirty reads and dirty writes never happen.

### Read Commited

* Read within same transaction always reads fresh value.
* con : multiple reads withing same transaction are inconsistent

### Read Uncommited

* reads even uncommited values from other transactions : *dirty reads*

### Serializable

* Every read is a locking read (depends on engine) and while one txn reads, other will have to wait
* NOTE: Every storage engine has its own implementation of serializable isolation, read documentation carefully.

## Scaling Databases

* These techniques are applicable to most databases out there

### Vertical Scaling

* add more CPU, RAM, Disk to the database
* requires downtime during reboot
* gives ability to handle *scale*, more load
* vertical scaling has physical hardware limitation

### Horizaontal Scaling : Read Replicas

* when read: write = 90:10
* you move reads to other databases using Master-Slave Topology
* Master is the only replica that can write, API servers must know which DB to get connected to get things done.

### Replication

* Changes on one database (Master) needs to be sent to Replica to Maintain Consistency
* There are two types to of replication

#### Synchronous Replication

* Strong Consistency
* Zero Replication Lag
* Slower Writes

#### Asynchronous Replication

* Eventual Consistency
* Some Replication Lag
* Faster Writes

| Difference between Synchronous & Asynchronous Replication    |
| ------------------------------------------------------------ |
| ![image-20250429130423029](./db.assets/image-20250429130423029.png) |

## Sharding and Partitioning

* Since one node cannot handle the data/load, we can split it into muultiple exlusive subsets.
* writes on a particular row/document will go to one particular shard, allowing use to scale overall database load
* NOTE: Shards are independent no replication b/w them
* API server needs to know which shard to connect, some databases have their own proxy to take care of routing. Each shard can have its own replica as well.

### Sharding & Partitioning

* Sharding : Method of distributing data across *multiple machines*.
* Partitioning : splitting a subset of data *within* the same instance.
* How a database is scaled
  * A database server is just a databases process running on an EC2
  * post production deploying, your service is serving the real traffic (100wps)
  * Suddenly there is a surge of users (200wps)
  * To handle load, you can scale up your database, increase RAM, CPU and DISK
  * Now, suddenly traffic surges in popularity (1000wps)
  * you can’t scale up beyond limits of the provider, you will have to scale horizontally 
  * Then you should split the data into multiple databases, providing higher throughput
* In above example splitting data into multiple database(shard) is called *partitioned*
* How to partition the data ? There are two categories of partitioning
  * Horizontal Partitioning (Common) - Within table take rows based on some propety into multiple partitions
  * Vertical Partitioning
* In above split depends on *load*, *usecase*, and *access patterns*
* Shards
  * Advantages
    * Handle large Read and Writes
    * Increases overall storage capacity
    * Higher Availability
  * Disadvantages
    * Operationally Complex
    * Cross-Shard Queries Expensive

## Non-Relational Databases

* broad generalization of database, mostly supporting *sharding* (supporting horizontal scalability)

### Document DB

* Ex - MongoDB, DynamoDB (supports documentDB features)
* Mostly JSON based
* Support complex queries (almost like relational databases)
* Partial Updates to documents possible (no need to update entire document)
* Closest to Relational Database
* in-app notification service, catalog service

### Key Value Stores

* Redis, ElasticSearch, Aerospike, DynamoDB (primarily key-store)
* Extremely simple databases
* Limited Functionality (GET, PUT, DEL)
* meant for key-based access pattern
* doesn’t support complex queries (aggregations)
* can be heavily sharded and partitioned
* use case: profile data, order data, auth data, messages, etc.
* You can use relational databases and document DBs as KV stores

### Graph Databases

* Neo4j, Neptune, Dgraph
* what if our graph data structure had a database
* it stores data that are represented as nodes, edges and relations
* useful for running complex graph algorithms
* powerful to model, social networks, recommendation systems, fraud detection

## Picking the Right Database

* A database is designed to solve a *particular problem* really well.
* Common Misconception: Picking Non-relational DB because relational databases do not scale.
* Why non-relational DBs scale
  * There are no relations & constraint
  * Data is modelled to be sharded
* If we relax above condition on relational databases then they can be scaled.
  * do not use foreign key check
  * do not use cross shard transaction
  * do manual sharding
* Does this mean, no DB is different
  * No every single database has some peculiar properties and guarantees and if you need those, pick that DB
* How does this help in designing system
  * While designing any system, do no jump to DB directly
  * Understand *what* & *how much* data you will be storing
  * Understand the *access pattern* for data
  * Any special feature like *TTL* etc required.

---

## File: sd/hld/index.md



# Notes

When it comes to courses, especially video courses, I am very skeptical. This is probably one of the few no-nonsense courses available.

## Basics

- [Introduction to System Design](intro.md)
  
- [Databases and Scaling](db.md)
  
- [Caching and Optimization](cache.md)
  
- [Messaging and Streaming Systems](streaming.md)
  
- [Load Balancing and Fault Tolerance](load.md)
  
- [Communication and Protocols](communication.md)
  
- [Big Data and Applications](big_data.md)
  

## Real-world System Designs

- Designing an E-commerce Product Listing
- Designing an API Rate Limiter
- Designing and Scaling Notification Systems
- Designing a Realtime Abuse Detection System
- Designing a Tinder-like Feed
- Designing Twitter Trends
- Designing a URL Shortener
- Designing GitHub Gists / Pastebin
- Designing a Fraud Detection System
- Designing a Recommendation Engine
- Designing a Web Crawler

## Advanced Topics

- Foundational Concepts
  - Foundational Topics in System Design - I
  - Foundational Topics in System Design - II

- Deep Dive into Databases
  - Relational Databases (Advanced)
  - Non-Relational Databases (Advanced)

- Distributed Systems
  - Distributed Systems [Storm Overview]
  - Distributed ID Generators

- Storage Systems
  - Storage Engines - I
  - Storage Engines - II

- High Throughput System Design
  - High Throughput Systems - I
  - High Throughput Systems - II

- Information Retrieval Systems
  - Building Search Engines and Retrieval Systems

- Building Large-Scale Social Networks
  - Building a Social Network - I
  - Building a Social Network - II

- Advanced System Design Techniques
  - Adhoc System Design
  - Algorithmic System Design - I
  - Algorithmic System Design - II


---

## File: sd/hld/intro.md

# Introduction to System Design



## What is System Design ?

* set of requirements which requires defining :
  * architecture
  * components
  * modules
* deals with how above 3 pieces interact with each other, cummulatively solving the problem

## Framework for designing a system

* Pattern for solving a system design problem
  * Break down problem statement into *solvable* sub-problem (divide & conquer)
  * Decide key components and responsibilities
  * Delare boundaries of each component
  * Understand Key Challenges in scaling your solution
  * Make architecture fault-tolerant and available


* How to approach System Design
  * Understand the problem statement
  * Break it down into components
    * Be mindful of the components and start with components you know
  * Dissect each component
    * Feed System might have - generator, aggregator, web server
  * For each sub-component look into
    * Database & Caching
    * Scaling & Fault Tolerance
    * Async Processing (Delegation)
    * Communication
  * Add more sub-compoents if needed
    * Understand the scope
    * In above example a generator could be made up of Post SVC, Recommendation System, Follow SVC which all connect to merger, and puts in feed database.

## How do you evaluate a system ?

* Every system can be improved *infinitely* & you should have a better idea when to stop
* Follow these pointers
  * Break system into components
  * Each Component has a clear set of responsibility(Exclusive)
  * For Each Component have Clear technical details on database, caching, scaling, fault-tolerance, async processing, communication
* Make sure Each Component in Isolation is
  * Scalable - horizontally scalable
  * Fault-Tolerant - Plan for recovery in case of a failure
  * Available - Component function even when some component fails

---

## File: sd/hld/load.md

# Load Balancing and Fault Tolerance

## Load Balancers

* One of the most important component in distributed system that makes it easy to scale horizontally
* load Balancer is the only point of contact
* Every Load Balancer has either
  * Static IP
  * static DNS Name
* load balancer hides the #server that are *behind* it allowing us to add *as many servers* as possible without client knowing about it
* Request Response Flow
  * Client already has IP/domain of load balancer
  * client makes API call and it comes to load balancer
  * load balancer picks one server and makes the same request
  * load balancer gets the response from the server
  * load balancer responds back to the client

### Load Balancing Algorithms

#### Round Robin

* distribute the load iteratively (uniform)

#### Weighted Round Robin

* distribute the load iteratively but as per weights

#### Least Connection

* pick server with least connection from the balancer. Used when response time has a big variance (analytics)

#### Hash Based Routing

* has of some attributes (ip, user id, url) determines which serve to pick

### Key Advantages of Load Balancers

* Scalability - servers can be scaled up and scaled down without User ever knowing.
* Availability - crashing of one server doesn’t affect entire infra, load balancer can route traffic to healthy nodes

## Circuit Breakers

* circuit breakers prevent *cascading failure*
* Example
  * User request comes to a feed service
  * Feed service pulls some info from recommendation system/Trending System
  * Recommendation and trending btoh relies on Profiles service
  * Recommendation and trending depends on Post Service
  * Post Service depends on Post Service
* There are lots of services that depend on profile service, if profile DB is overwhelmed (shuts down) and transitively all dependents on it are affected causing “Timeout”
* Two major affects
  * complete outage
  * unresponsiveness
* Idea : if recommendation service works without profile service, and returns some default feed. Then recommendation service becomes *circuit breaker* and stops cascading fialures

* How to Implement ?
  * A common database holds the settings for each breaker
  * services before making calls to each other checks the config (cahce the config to avoid checking the DB)
* In case of the outage, the circuit is tripped and DB updated, services will periodically check and stop sending requests to affected services

## Data Redundancy and Recovery

* API servers are *stateless* but databases are *stateful*
* API servers going down is fine because it can be respawned but thats no the cash if disk crashes
* A good system always takes care of such catastrophic situation
* The only way to protect against loss of data to create multiple copies of it - *Data Redudancy*
* Backup & Restore
  * Daily backup of data (incremental)
  * weekly complete backup
  * storing one copy across region (Disaster Recovery)
  * When something goes wrong, just restore the last backup
  * almost always easiest thing to do

### Continous Redundancy

* Setup Replica of the database and writes go to both DB (sync/async)
  * API server writes to both Database
  * API writes to one and is copied to other async
* If master database goes down, writes can be redirected to slave database replica which is temporarily promoted to master and handles writes.

## Leader Election for Auto-Recovery

* If there are bunch of nodes serving traffic, then if any of the node goes down, then a *orchrestration* service should bring up another replica of that node.
  * No human intervention involved
  * Minimal Time - outage
* But above scenario always keeps happening as orchestration might be down, how do we keep orchestration correctly ? orchestrator for orchestrators :(
* We keep two orchestration called as Orch leader, Orch workers. (Master-Slave Topology)
* If any of the worker figures out that orch leader is down, orch slave is promoted to master orchestration by the workers by consensus algorithms.
* Read up more on various Consensus Algorithms

---

## File: sd/hld/streaming.md

# Messaging and Streaming Systems

## Asynchronous Processing

* user sents the request and immediately recieving response is called as synchronous
* Ex - loading feed, login, payments.
* Asynchronous Systems usually will accept the user payload and forward it to message brokers which will pass this work to workers. User will not wait for response and get back some id to track status of the work, and When workers complete their task, they can just update the DB & status of the task.

![image-20250429201600969](./streaming.assets/image-20250429201600969.png)



## Message Brokers and Queues

Brokers help two services/application communicate through messages. We use message brokers when we want to do something *asynchronous*

* Long Running Tasks
* Trigger Dependent tasks across machines

Features of Message Brokers

* Brokers help us connect different sub-systems
* Brokers acts as a buffer for the messages, allowing consumers to consume messages at their pace. Ex - Notification service
* Brokers can retain messages for `n` days
* Brokers can re-queue the message if not deleted (Visibility Timeout)

## Message Stream and Kafka Essentials

* Ex- assume workers in above example does two things, writes to Elastic Search and to DB

![image-20250429211936714](./streaming.assets/image-20250429211936714.png)

* Approach - 1 : One Message Brokers and add logic in consumers

  * process - 1 & process 2, if either failed then we will not be able process both events correctly

  ![image-20250429212343027](./streaming.assets/image-20250429212343027.png)

* Approach - 2 : Two Brokers & two sets of consumers

  * API server Writes to two brokers and each has its own set of consumers, (solves issue with partial complete writes)
  * Issue - when api server writes to two RabbitMQ, one of them fails, we end up with original problem.

* Solution: write once, but read by many systems - Kafka, Kinesis try to solve this problem.

Message Streams

* Similar to Message Queue except there could be multiple consumers reading from the same stream.

![image-20250429212638563](./streaming.assets/image-20250429212638563.png)

Message Queue vs Message Streams

* In Message Queue, consumers consume a message once while in Kinesis a specific consumer group consumes the message once (usually tracked by checkpoint)

### Kafka Essentials

* Kafka is a message stream that holds the messages. Internally Kafka has topics, with `n` partitions
* Message is sent to a topic, and depending on the configured hash key it is put into a partition.
* Within that partition, messages are ordered (no order guarantee, across partitions) 
* Limitation of Kafka : number of consumer = number of partition
* In Kafka, each consumer can commit their checkpoints. And deletion of messages happens based on the expiry time.

## Realtime Pub/Sub Systems

* Both Message Broker and Streams, requires consumers to `pull` messages out.
* Advantage : Consumers can pull at their own pace, and consumers don’t get overwhelmend
* Disadvantage: Consumption lag when high ingestion.

What if we want low latency  Zero Lag ? --> realtime pubsub

* Instead of consumers pulling the message, the message is pushed to them.
* This way we get really fast delievery time, but can overwhelm the consumers if they are not able to process the message fast (usually we use queue at each consumer)
* Practical Usecase : Message Broadcast, Configuration Push, All systems receive updates without polling for data.



---

## File: sd/index.md

# System Design
*The process of defining a system’s architecture, components, and interfaces to meet functional and non-functional requirements.*

**Key Aspects**
* Scalability
* Performance
* Reliability
* Maintainability
* Cost-effectiveness

 [General Software Engineering Principle Overview](principles.md)

## High Level Design (HLD) - Architecture & Strategy

Topics

* System Architecture - APIs, Databases, Caching, Load Balancing
* Technology Choices - SQL vs NoSQL, Monolith vs Microservices
* Data Flows - Request Handling, processing, storage flows
* Scalability & Fault Tolerance - Replication, Sharding, Failover
* Trade-offs & Bottlenecks - CAP Theorem, latency, cost

Notes

* [Notes on HLD](hld/index.md)

## Low-Level Design (LLD) - Implementation & Code
* Class Diagrams - Object-oriented structure
* Database Schema - Tables, indexing, query optimization
* API Design - REST, GraphQL, gRPC best practices
* [Design Patterns](lld/design_patterns.md) - Singleton, Factory, CQRS, Event-Driven
* Problem Implementations - Examples & Case Studies
## Resources

Required

* _System Design Interview Guide_ 1 & 2 – Alex Xu
* _Designing Data-Intensive Applications_ – Martin Kleppmann

Other

* _The Art of Scalability_ – Abbott & Fisher
* [Arpit Bhayani YouTube Channel & Courses](https://www.youtube.com/c/ArpitBhayani)
* [Company Engineering Blogs/Content](company.md)


---

## File: sd/lld/design_patterns.md

# Design Patterns

* Design Pattern serves as typical solution to common problems in software design
* All patterns can categorized by their *intent*
	* Creational Pattern - deals with object creation
	* Structural Pattern - deals organisation of objects/classes
	* Behavioural Patterns - deals with object/classes communications
* [Refactoring Guru](https://refactoring.guru/design-patterns)
## Creational Patterns
### Factory Method ⭐
* also known as virtual constructor
* provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created
```python
from abc import ABC, abstractmethod

# Step 1: Define an abstract product
class Vehicle(ABC):
    @abstractmethod
    def create(self):
        pass

# Step 2: Implement concrete products
class Car(Vehicle):
    def create(self):
        return "Car is created 🚗"

class Bike(Vehicle):
    def create(self):
        return "Bike is created 🏍️"

# Step 3: Define a factory class with a factory method
class VehicleFactory(ABC):
    @abstractmethod
    def get_vehicle(self) -> Vehicle:
        pass

# Step 4: Implement concrete factories for each vehicle type
class CarFactory(VehicleFactory):
    def get_vehicle(self) -> Vehicle:
        return Car()

class BikeFactory(VehicleFactory):
    def get_vehicle(self) -> Vehicle:
        return Bike()

# Step 5: Client code
def client_code(factory: VehicleFactory):
    vehicle = factory.get_vehicle()
    print(vehicle.create())

# Example Usage
if __name__ == "__main__":
    car_factory = CarFactory()
    bike_factory = BikeFactory()

    client_code(car_factory)  # Output: Car is created 🚗
    client_code(bike_factory)  # Output: Bike is created 🏍️
```

* NOTES
	* Decouples Object Creation - Client Classes don't need to know how objects are created
	* Encapsulation - Factory class has the logic to create objects
	* Extensionability - Adding a new Vehicle requires just adding a new subclass, without modifying client code
* Why you don't want user to create objects directly ??
	* Client codes should not be affected with changes in the code. Let's say your process to create object becomes complicated(db calls, using different configurations), then client has no need to know about object creations.
	* Easier Dependency Injection & Testing
	  * If you create Car() directly, testing requires changing the entire class.
	  * With a factory, you can **inject dependencies**, making testing more modular.
### Abstract Factory
### Builder ⭐
* lets you construct complex objects step by step
* The pattern allows you to produce different types and representations of an object using the same construction code.

Why Use Builder PatternTest

* Better Readability – Instead of a constructor with too many parameters, we build the object step by step.
* Flexibility – Can construct different variations of an object (e.g., Car, SportsCar, SUV).
* Encapsulation – The construction logic is separate from the object representation.

```python
# without builder pattern
class Car:
    def __init__(self, brand, engine, seats, sunroof):
        self.brand = brand
        self.engine = engine
        self.seats = seats
        self.sunroof = sunroof

    def __str__(self):
        return f"Car({self.brand}, {self.engine}, {self.seats} seats, Sunroof: {self.sunroof})"

# Creating a car object with a long constructor
car = Car("Tesla", "Electric", 5, True)
print(car)
```

Above Implementation has following issues

- Long Constructor
- Optional Parameter
- Hard to Extend


````python
#using builder pattern
class Car:
    def __init__(self, brand=None, engine=None, seats=None, sunroof=None):
        self.brand = brand
        self.engine = engine
        self.seats = seats
        self.sunroof = sunroof

    def __str__(self):
        return f"Car({self.brand}, {self.engine}, {self.seats} seats, Sunroof: {self.sunroof})"

class CarBuilder:
    def __init__(self):
        self.car = Car()

    def set_brand(self, brand):
        self.car.brand = brand
        return self  # Enables method chaining

    def set_engine(self, engine):
        self.car.engine = engine
        return self

    def set_seats(self, seats):
        self.car.seats = seats
        return self

    def set_sunroof(self, sunroof):
        self.car.sunroof = sunroof
        return self

    def build(self):
        return self.car

# Using the builder pattern
car = CarBuilder().set_brand("Tesla").set_engine("Electric").set_seats(5).set_sunroof(True).build()
print(car)  # ✅ Car(Tesla, Electric, 5 seats, Sunroof: True)
````

- **Readable & Flexible**: No need to remember constructor parameters.
- **Handles Optional Parameters**: Can omit sunroof, engine, etc.
- **Method Chaining**: Allows easy, fluent object creation.
- **Scalability**: Easily add new features without modifying existing code.

### Prototype
### Singleton ⭐
* lets you ensure that a class has only one instance, while providing a global access point to this instance
* Advantages
  * **Prevents multiple instances** of a resource-heavy class.
  * **Centralized access** to a shared instance across the application.
  * **Ensures consistency** when only one instance should exist (e.g., one DB connection)
* Examples Use Cases are one-root logger or one spark context, because spark initialization is costly.
```python
class Singleton:
    _instance = None  # Holds the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
        # The __new__ method ensures only one instance is created
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

# Usage
obj1 = Singleton()
obj2 = Singleton()
print(obj1 is obj2)  # ✅ True (Same instance)
```

Other Interesting ways to create Singleton Classes in Python
```python
# using decorator
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Logger:
    def log(self, msg):
        print(f"[LOG]: {msg}")

# Usage
logger1 = Logger()
logger2 = Logger()
print(logger1 is logger2)  # ✅ True (Same instance)

# using metaclasses
# Ensures **any subclass** automatically follows the Singleton pattern.
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def connect(self):
        return "Connected to database"

# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # ✅ True (Same instance)

```

| **Approach** | **Pros**             | **Cons**         |
| ------------ | -------------------- | ---------------- |
| __new__      | Simple, widely used  | Not extendable   |
| Decorator    | Clean, reusable      | Harder debugging |
| Metaclass    | Works for subclasses | Complex          |

## Structural Patterns
### Adapter ⭐
* allows objects with incompatible interfaces to collaborate
* usecases
  * helps integrate 3rd-party library without modifying their code
  * makes incompatible classes work together
```python
# without adapter
class MP3Player:
    def play_mp3(self, filename):
        print(f"Playing MP3 file: {filename}")

# Client Code
player = MP3Player()
player.play_mp3("song.mp3")  # Works fine ✅
player.play_mp4("video.mp4")  # ❌ AttributeError: 'MP3Player' object has no attribute 'play_mp4'
```
* Using Adapter to modify this class
```python
class MP3Player:
    def play_mp3(self, filename):
        print(f"Playing MP3 file: {filename}")

# Adapter to support other formats
class MediaAdapter:
    def __init__(self, media_type):
        self.media_type = media_type
        self.player = MP3Player()  # Uses existing player

    def play(self, filename):
        if self.media_type == "mp3":
            self.player.play_mp3(filename)
        elif self.media_type == "mp4":
            print(f"Converting {filename} to MP3 format... 🎵")
            self.player.play_mp3(filename.replace(".mp4", ".mp3"))
        else:
            print(f"Error: Unsupported format {self.media_type} ❌")

# Client Code
player = MediaAdapter("mp4")
player.play("video.mp4")  # ✅ Plays after conversion
```
### Bridge
* **decouples an abstraction from its implementation**, allowing them to evolve **independently**
* When to Use
  * **When you want to avoid a rigid class hierarchy** – Prevents class explosion due to multiple variations.
  * **When you need to support multiple implementations** – Example: Different platforms (Windows, Linux, macOS).
  * **When abstraction and implementation should vary independently** – Example: Devices and their remote controls.
* Key Components
  * **Abstraction** – Defines a high-level interface (e.g., RemoteControl).
  * **Refined Abstraction** – Extends abstraction with additional behavior.
  * **Implementation Interface** – Defines the low-level details (e.g., Device).
  * **Concrete Implementations** – Provide specific implementations.
```python
from abc import ABC, abstractmethod

# Implementation Interface (Device)
class Device(ABC):
    """Defines a common interface for all devices."""
    
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

# Concrete Implementations (TV & Radio)
class TV(Device):
    def turn_on(self):
        print("📺 TV is now ON")

    def turn_off(self):
        print("📺 TV is now OFF")

class Radio(Device):
    def turn_on(self):
        print("📻 Radio is now ON")

    def turn_off(self):
        print("📻 Radio is now OFF")

# Abstraction (Remote Control)
class RemoteControl:
    """Bridge between the abstraction (Remote) and implementation (Device)."""
    
    def __init__(self, device: Device):
        self.device = device

    def toggle_power(self):
        print("🔘 Toggling Power...")
        self.device.turn_on() if isinstance(self.device, TV) else self.device.turn_off()

# Client Code
tv_remote = RemoteControl(TV())
radio_remote = RemoteControl(Radio())

tv_remote.toggle_power()   # 📺 TV is now ON
radio_remote.toggle_power() # 📻 Radio is now OFF
```
### Composite
### Decorator ⭐
* lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.
* Usage
  * logging, security, caching & UI improvements
* why use it ?
  * **Extends functionality** without modifying the original class.
  * **Follows Open-Closed Principle** (open for extension, closed for modification).
  * **Allows multiple decorators** to be combined flexibly.
```python
# without Decorator, adding milk to coffee is cumbersome
class Coffee:
    def cost(self):
        return 5

    def description(self):
        return "Basic Coffee"

# Adding features by modifying the class (Not scalable ❌)
class CoffeeWithMilk(Coffee):
    def cost(self):
        return super().cost() + 2

    def description(self):
        return super().description() + " + Milk"

coffee = CoffeeWithMilk()
print(coffee.description())  # Basic Coffee + Milk
print(coffee.cost())  # 7
```
* creating an ingredient decorator
```python
# Base Component
class Coffee:
    def cost(self):
        return 5

    def description(self):
        return "Basic Coffee"

# Decorator Base Class
class CoffeeDecorator:
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost()

    def description(self):
        return self._coffee.description()

# Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return super().cost() + 2

    def description(self):
        return super().description() + " + Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return super().cost() + 1

    def description(self):
        return super().description() + " + Sugar"

# Client Code
coffee = Coffee()
print(coffee.description(), "->", coffee.cost())  # Basic Coffee -> 5

coffee = MilkDecorator(coffee)
print(coffee.description(), "->", coffee.cost())  # Basic Coffee + Milk -> 7

coffee = SugarDecorator(coffee)
print(coffee.description(), "->", coffee.cost())  # Basic Coffee + Milk + Sugar -> 8
```

- Flexible & Scalable
- Combinable - decorators can be combines
- **Follows SOLID principles** – No unnecessary subclasses or modifications.

### Facade
### Flyweight
### Proxy ⭐
* lets you provide a substitute or placeholder for another object. A proxy controls access to the original object, allowing you to perform something either before or after the request gets through to the original object.
* Advantages
  * Lazy Initialization - Virtual Proxy
  * Access Proxy (Control) - Restriction to access original object
  * Logging/monitoring Proxy - record requests for analytics and debugging
  * Caching Proxy - store results to avoid recomputation
  * Remote Proxy - Interface for calling methods on a remote object
* Virtual Proxy
```python
class RealImage:
    """Heavy object that loads an image from disk."""
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()

    def load_from_disk(self):
        print(f"Loading image: {self.filename}")

    def display(self):
        print(f"Displaying image: {self.filename}")

class ProxyImage:
    """Proxy that delays the creation of RealImage until display is called."""
    def __init__(self, filename):
        self.filename = filename
        self.real_image = None

    def display(self):
        if self.real_image is None:
            self.real_image = RealImage(self.filename)  # Lazy Initialization
        self.real_image.display()

# Client Code
image = ProxyImage("test_image.jpg")  # Image not loaded yet
image.display()  # Loads image only when needed
image.display()  # Second call does not reload image
```

* logging Proxy
```python
class RealService:
    def operation(self):
        print("Performing an operation in RealService")

class LoggingProxy:
    """Logs requests before calling the actual object."""
    def __init__(self, real_service):
        self.real_service = real_service

    def operation(self):
        print("Logging: Operation is about to be executed")
        self.real_service.operation()
        print("Logging: Operation executed successfully")

# Client Code
service = RealService()
proxy = LoggingProxy(service)
proxy.operation()
```
## Behavioural Patterns
### Chain of Responsibility ⭐
* lets you pass requests along a chain of handlers. Upon receiving a request,
* Each handler decides
  * ✅ **Process the request** OR
  * ✅ **Forward it to the next handler**
* When to Use
  * **Logging and Debugging** – Different loggers (file, console, database) handle messages.
  * **Event Handling** – UI elements process events (buttons, forms, popups).
  * **Request Validation** – Middleware authentication in web frameworks.
  * **Customer Support System** – Requests escalate from agent → supervisor → manager.
* Key Components
  * Handler (abstract class) - Defines the method to handle requests.
  * **Concrete Handlers** – Implement request processing & decide whether to pass it forward.
  * **Client** – Sends requests to the first handler in the chain.
```python
# logging System
class Logger:
    """Base Handler"""
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def log(self, level, message):
        if self.next_handler:
            self.next_handler.log(level, message)

class DebugLogger(Logger):
    def log(self, level, message):
        if level == "DEBUG":
            print(f"[DEBUG] {message}")
        else:
            super().log(level, message)

class WarningLogger(Logger):
    def log(self, level, message):
        if level == "WARNING":
            print(f"[WARNING] {message}")
        else:
            super().log(level, message)

class ErrorLogger(Logger):
    def log(self, level, message):
        if level == "ERROR":
            print(f"[ERROR] {message}")
        else:
            super().log(level, message)

# Setting up the chain
logger_chain = DebugLogger(WarningLogger(ErrorLogger()))

# Client Code
logger_chain.log("DEBUG", "This is a debug message.")
logger_chain.log("WARNING", "This is a warning message.")
logger_chain.log("ERROR", "This is an error message.")
```

```python
# web middleware - auth -> role -> log
class Handler:
    """Base Handler"""
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return "Request reached the end of the chain"

class AuthHandler(Handler):
    """Authentication Middleware"""
    def handle(self, request):
        if not request.get("user"):
            return "Authentication Failed"
        return super().handle(request)

class RoleHandler(Handler):
    """Authorization Middleware"""
    def handle(self, request):
        if request.get("role") != "admin":
            return "Access Denied"
        return super().handle(request)

class LoggingHandler(Handler):
    """Logging Middleware"""
    def handle(self, request):
        print(f"Logging request: {request}")
        return super().handle(request)

# Setting up the chain
middleware_chain = AuthHandler(RoleHandler(LoggingHandler()))

# Client Code
request1 = {"user": "Alice", "role": "admin"}
print(middleware_chain.handle(request1))  # Success

request2 = {"user": "Bob", "role": "guest"}
print(middleware_chain.handle(request2))  # Access Denied

request3 = {"role": "admin"}  # Missing user
print(middleware_chain.handle(request3))  # Authentication Failed
```
### Command ⭐
* encapsulates a request as an object, allowing for **delayed execution, undo/redo functionality, and queuing commands**.
* When to Use
  * **Undo/Redo functionality** – Text editors, Photoshop.
  * **Job Scheduling** – Task execution in threads.
  * **Remote Control Devices** – TV remote buttons, IoT devices.
* Key Components
  * **Command Interface** – Declares an execution method.
  * **Concrete Commands** – Implement specific actions.
  * **Invoker** – Triggers commands.
  * **Receiver** – Performs the actual work.
```python
# tv remote
from abc import ABC, abstractmethod

class Command(ABC):
    """Command Interface"""
    @abstractmethod
    def execute(self):
        pass

class TV:
    """Receiver"""
    def turn_on(self):
        print("TV is ON")

    def turn_off(self):
        print("TV is OFF")

class TurnOnCommand(Command):
    """Concrete Command: Turn ON"""
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self):
        self.tv.turn_on()

class TurnOffCommand(Command):
    """Concrete Command: Turn OFF"""
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self):
        self.tv.turn_off()

class RemoteControl:
    """Invoker"""
    def __init__(self):
        self.command = None

    def set_command(self, command: Command):
        self.command = command

    def press_button(self):
        if self.command:
            self.command.execute()

# Client Code
tv = TV()
remote = RemoteControl()

turn_on = TurnOnCommand(tv)
turn_off = TurnOffCommand(tv)

remote.set_command(turn_on)
remote.press_button()  # TV is ON

remote.set_command(turn_off)
remote.press_button()  # TV is OFF
```
### Iterator
### Mediator
### Memento
* lets you save and restore the previous state of an object without revealing the details of its implementation
* When to use
  * *Undo/Redo operations** – Text editors, games, drawing applications.
  * **State recovery** – Crash recovery in software.
  * **Checkpointing** – Saving progress in a game.
* Key Components
  * **Memento** – Stores the state of an object.
  * **Originator** – Creates and restores mementos.
  * **Caretaker** – Manages mementos and handles state restoration.
```python
class Memento:
    """Memento stores the state of an object."""
    def __init__(self, state):
        self._state = state

    def get_saved_state(self):
        return self._state

class TextEditor:
    """Originator - Creates and restores mementos."""
    def __init__(self):
        self._text = ""

    def write(self, text):
        self._text = text

    def save(self):
        return Memento(self._text)

    def restore(self, memento):
        self._text = memento.get_saved_state()

    def show(self):
        print(f"Current Text: {self._text}")

class Caretaker:
    """Caretaker - Manages saved states."""
    def __init__(self):
        self._history = []

    def save_state(self, memento):
        self._history.append(memento)

    def restore_state(self):
        if self._history:
            return self._history.pop()
        return None

# Client Code
editor = TextEditor()
caretaker = Caretaker()

editor.write("Hello, World!")
caretaker.save_state(editor.save())  # Save state

editor.show()  # Output: Current Text: Hello, World!

editor.write("New Text")
editor.show()  # Output: Current Text: New Text

# Restore previous state
editor.restore(caretaker.restore_state())
editor.show()  # Output: Current Text: Hello, World!
```
### Observer ⭐
* The **Observer Pattern** allows multiple objects (**observers**) to listen to and react to changes in another object (**subject**). When the subject’s state changes, all registered observers are notified automatically.
* When to Use
  * **Event-driven programming** – UI elements react to user actions.
  * **Publish-Subscribe systems** – Notification services, message brokers.
  * **Data Binding** – React.js, Vue.js frameworks.
  * **Stock Market Updates** – Multiple clients get real-time stock prices.
* Key Components
  * **Subject (Publisher)** – Maintains a list of observers and notifies them when state changes.
  * **Observer (Subscriber)** – Listens for updates from the subject.
  * **Concrete Subject** – Implements state changes and observer management.
```python
class StockMarket:
    """Subject (Publisher)"""
    def __init__(self):
        self.observers = []
        self.stock_price = 0

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.stock_price)

    def set_price(self, price):
        self.stock_price = price
        self.notify_observers()

class Investor:
    """Observer (Subscriber)"""
    def __init__(self, name):
        self.name = name

    def update(self, price):
        print(f"{self.name} received stock price update: {price}")

# Client Code
market = StockMarket()
investor1 = Investor("Alice")
investor2 = Investor("Bob")

market.add_observer(investor1)
market.add_observer(investor2)

market.set_price(100)  # Both investors get notified
market.set_price(120)  # Another update is sent
```
### Stage
* models an **object’s behavior as a finite set of states**, with **each state defining its own behavior**.
* When to Use
  * When an object has different modes or stages** – Traffic lights, vending machines.
  * **State-dependent behavior** – Objects act differently in different states.
  * **Reducing complex if-else logic** – Avoids conditionals in methods.
* Key Components
  * **State Interface** – Defines behavior for all states.
  * **Concrete States** – Implement specific behavior for each state.
  * **Context (Object)** – Maintains current state & delegates actions.
```python
from abc import ABC, abstractmethod

class TrafficLightState(ABC):
    """Abstract state class defining state-specific behavior."""
    
    @abstractmethod
    def handle(self, light):
        pass

class RedLight(TrafficLightState):
    def handle(self, light):
        print("🚦 Red Light - Stop!")
        light.state = GreenLight()

class GreenLight(TrafficLightState):
    def handle(self, light):
        print("🚦 Green Light - Go!")
        light.state = YellowLight()

class YellowLight(TrafficLightState):
    def handle(self, light):
        print("🚦 Yellow Light - Slow Down!")
        light.state = RedLight()

class TrafficLight:
    """Context class maintaining the current state."""
    
    def __init__(self):
        self.state = RedLight()  # Initial state

    def change(self):
        self.state.handle(self)

# Client Code
traffic_light = TrafficLight()

for _ in range(4):
    traffic_light.change()
```
### Strategy ⭐
* **define a family of algorithms**, put them in separate classes, and make them **interchangeable** at runtime.
* When to use
     * **Multiple algorithms for the same task** – Sorting, Compression.
     * **Reducing conditional logic (if-else/switch)** – Payment methods, Authentication.
     * **Behavior modification at runtime** – Game difficulty levels.
* Key Components
     * **Context** – Maintains a reference to a strategy object.
     * **Strategy Interface** – Defines a common interface for all strategies.
     * **Concrete Strategies** – Implement different algorithms.
```python
# payment strategy
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    """Strategy Interface"""
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    """Concrete Strategy: Credit Card"""
    def pay(self, amount):
        print(f"Paid ${amount} using Credit Card.")

class PayPalPayment(PaymentStrategy):
    """Concrete Strategy: PayPal"""
    def pay(self, amount):
        print(f"Paid ${amount} using PayPal.")

class PaymentContext:
    """Context that uses a strategy"""
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def checkout(self, amount):
        self.strategy.pay(amount)

# Client Code
context = PaymentContext(CreditCardPayment())
context.checkout(100)  # Paid using Credit Card

context.set_strategy(PayPalPayment())  
context.checkout(200)  # Paid using PayPal
```
### Template Method
* defines the **skeleton** of an algorithm in a **base class**, allowing subclasses to **override specific steps** without modifying the structure of the algorithm.
* When to Use
  * **Common workflow with variations** – Report generation, data processing.
  * **Code reuse** – Avoids duplicate code in similar processes.
  * **Standardized behavior** – Ensures steps are executed in a defined order.
* Key Components
  * **Abstract Class (Template)** – Defines the algorithm structure.
  * **Concrete Class** – Implements missing steps of the algorithm.
```python
from abc import ABC, abstractmethod

class ReportGenerator(ABC):
    """Abstract class defining the template method."""
    
    def generate_report(self):
        """Template method defining the report generation process."""
        self.collect_data()
        self.analyze_data()
        self.format_report()
        self.print_report()

    @abstractmethod
    def collect_data(self):
        pass

    @abstractmethod
    def analyze_data(self):
        pass

    def format_report(self):
        """Common implementation."""
        print("Formatting report in PDF format.")

    def print_report(self):
        """Common implementation."""
        print("Printing report...")

class SalesReport(ReportGenerator):
    """Concrete class implementing specific steps."""
    
    def collect_data(self):
        print("Collecting sales data.")

    def analyze_data(self):
        print("Analyzing sales trends.")

# Client Code
report = SalesReport()
report.generate_report()
```
### Visitor
* **add new behaviors to objects** **without modifying their structure**, by **separating the operation from the object itself**.
* When to Use
  * **Extending behavior without modifying existing classes** – Syntax tree traversal.
  * **Applying different operations to a group of objects** – Compilers, AST manipulation
  * **Avoiding clutter in existing classes** – Separates logic from data structures.
* Components
  * **Visitor** – Defines new operations on elements.
  * **Concrete Visitors** – Implement specific behavior.
  * **Element** – Accepts a visitor and allows it to operate on itself.
```python

# We **separate operations (size calculation & compression)** from the **file structure**
from abc import ABC, abstractmethod

class FileElement(ABC):
    """Abstract element accepting visitors."""
    
    @abstractmethod
    def accept(self, visitor):
        pass

class File(FileElement):
    """Concrete file class."""
    
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def accept(self, visitor):
        visitor.visit_file(self)

class Folder(FileElement):
    """Concrete folder class."""
    
    def __init__(self, name, children):
        self.name = name
        self.children = children

    def accept(self, visitor):
        visitor.visit_folder(self)

class Visitor(ABC):
    """Abstract visitor defining operations."""
    
    @abstractmethod
    def visit_file(self, file):
        pass

    @abstractmethod
    def visit_folder(self, folder):
        pass

class SizeCalculator(Visitor):
    """Concrete visitor calculating total size."""
    
    def visit_file(self, file):
        print(f"File: {file.name}, Size: {file.size} KB")
    
    def visit_folder(self, folder):
        print(f"Folder: {folder.name} contains:")
        for child in folder.children:
            child.accept(self)

# Client Code
file1 = File("Document.txt", 120)
file2 = File("Photo.jpg", 450)
folder = Folder("MyFolder", [file1, file2])

size_calculator = SizeCalculator()
folder.accept(size_calculator)
```

---

## File: sd/principles.md


## Solid Principles

* Single Responsibility Principle (SRP) - _Do one thing and do it well._
* Open/Closed Principle - _Don’t modify existing code; extend it instead._
* Liskov Substitution Principle (LSP) - _Derived classes must extend without changing functionality._
* Interface Segregation Principle (ISP) - _Many small interfaces are better than one large one._
* Dependency Inversion Principle (DIP) - _Depend on abstractions, not concretions._

## General OOPs Principles

* Encapsulation - *Hide implementation details; expose only what is necessary*
* Prefer Composition over Inheritance - _Favor has-a over is-a relationship_
* Tell, Don't Ask - _Ask for what you need, not how to get it_

## Code Simplicity & Maintainability Principles

* KISS (Keep it Simple, Stupid) - _Complexity is the enemy of maintainability_
* YAGNI (You ain't gonna need it) - _Avoid unnecessary features_
* DRY (Don't Repeat Yourself) - _Every piece of knowledge must have a single representation._
* Law of Demeter (LoD) - _Talk only to your friends, not strangers._

## Design and Architecture

* Separation of Concerns - _Each module should have a clear purpose._
* Cohesion & Coupling - _Tightly coupled systems are harder to maintain._ High Cohesion, Low Coupling.
* Fail Fast - _Crash early, fix early._ Detect Early errors rather than failing silently
* Convention over Configuration - _Less configuration, more productivity._ Use sensible Defaults.
* Poka - Yoke (Mistake - Proofing) - _Make incorrect states impossible_
* Single Level of Abstraction - _Don’t mix high and low-level details in the same function._

## Performance & Scalability Principles

* You shouldn't Optimize prematurely - _Premature optimization is the root of all evil._ Donald Knuth
* C10k & C10M Problem Awareness - _Plan for high concurrency._ Be mindful of 10k+ concurrent connections in server
* Horizontal Scaling vs Vertical Scaling - _Scale out, not up._ Prefer Horizontal Scaling.

## Software Development Process Principles

* Agile Manifesto - Prioritize **individuals, working software, customer collaboration, and flexibility**. - _Respond to change over following a plan._
* Boy Scout Rule - Leave the code **better than you found it**. - _Always leave the campground cleaner than you found it._
* Test Driven Development (TDD) - Write **tests first**, then write the code to pass them. - _Red → Green → Refactor._
* CI/CD - Automate testing and deployment. - _Deploy fast, deploy often._
* Feature Flags/Toggle - Enable or disable features **without deploying code**. - _Separate deployment from release._

## Security & Reliability Principles

* Principle of Least Privilege - _Don’t give a process more power than it needs._
* Fail Safe, Not Open - Systems should **default to a safe state** in case of failure. - _Security should not rely on obscurity._
* Indepotency - The same request should produce the **same result** if repeated. - _Safe to retry.”_
* CAP Theorem - In distributed systems, you can have **only two out of three**:
    * Consistency (all nodes see the same data)
    * Availability (system always responds)
    * Partition Tolerance (handles network failures)


---

