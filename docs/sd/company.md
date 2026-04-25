# Engineering Blogs & Case Studies

---

## Engineering Blogs

### Big Tech

- [Meta Engineering](https://engineering.fb.com) - infra, AI, distributed systems at Facebook/Instagram/WhatsApp scale
- [Google Research Blog](https://research.google/blog/) - ML, systems, languages, and infrastructure research
- [AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/) - cloud patterns, reference architectures, Well-Architected content
- [Apple Machine Learning Research](https://machinelearning.apple.com) - on-device ML, privacy-preserving systems
- [Microsoft Developer Blogs](https://devblogs.microsoft.com) - Azure, .NET, TypeScript, and platform engineering

### Infrastructure & Developer Tools

- [Cloudflare Blog](https://blog.cloudflare.com) - networking, edge computing, security, DNS at scale
- [Stripe Engineering](https://stripe.com/blog/engineering) - payments infrastructure, API design, reliability
- [GitHub Engineering](https://github.blog/engineering/) - Git at scale, developer tooling, CI/CD
- [Figma Engineering](https://www.figma.com/blog/engineering/) - real-time collaboration, WebAssembly, rendering
- [Dropbox Tech](https://dropbox.tech) - storage systems, desktop sync, migration stories
- [HashiCorp Blog](https://www.hashicorp.com/blog) - infrastructure as code, service mesh, secrets management

### Product Companies

- [Netflix Tech Blog](https://netflixtechblog.com) - streaming infrastructure, chaos engineering, personalization
- [Uber Engineering](https://www.uber.com/en-US/blog/engineering/) - geospatial systems, real-time dispatch, microservices
- [Airbnb Engineering](https://airbnb.tech/blog/) - data infrastructure, search, ML platform
- [LinkedIn Engineering](https://engineering.linkedin.com/blog) - feed ranking, Kafka (originated here), data systems
- [Shopify Engineering](https://shopify.engineering) - scaling e-commerce, flash sales, resilience patterns
- [Spotify Engineering](https://engineering.atspotify.com) - data pipelines, recommendations, squad model
- [Slack Engineering](https://slack.engineering) - real-time messaging, presence, WebSocket at scale
- [Discord Engineering](https://discord.com/category/engineering) - voice/video, database migrations, Rust at scale
- [DoorDash Engineering](https://careersatdoordash.com/engineering-blog/) - logistics, real-time dispatch, ML for ETAs

### AI & Data

- [Anthropic Research](https://www.anthropic.com/research) - safety-focused AI, Constitutional AI, interpretability
- [OpenAI Research](https://openai.com/research/) - large language models, alignment, safety
- [Google DeepMind](https://deepmind.google/research/) - reinforcement learning, protein folding, frontier AI
- [Hugging Face Blog](https://huggingface.co/blog) - open-source ML, model deployment, transformers
- [Databricks Blog](https://www.databricks.com/blog) - data lakehouse, Spark, ML pipelines, Delta Lake

---

## Architecture Case Studies

### Foundational Papers

These are the canonical references for distributed systems design - widely cited and worth reading in full.

| Paper | Company | Year | Key Concepts |
|-------|---------|------|--------------|
| [Dynamo: Highly Available Key-Value Store](https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html) | Amazon | 2007 | Consistent hashing, vector clocks, eventual consistency |
| [The Google File System](https://research.google/pubs/the-google-file-system/) | Google | 2003 | Distributed file system, chunk servers, single master |
| [Bigtable: Distributed Storage for Structured Data](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data-awarded-best-paper/) | Google | 2006 | Wide-column store, SSTable, Chubby lock service |
| [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) | Google | 2004 | Batch processing, fault-tolerant map-reduce |
| [Spanner: Google's Globally Distributed Database](https://research.google/pubs/spanner-googles-globally-distributed-database/) | Google | 2012 | TrueTime, external consistency, global transactions |
| [Chubby: A Lock Service for Loosely-Coupled Distributed Systems](https://research.google/pubs/the-chubby-lock-service-for-loosely-coupled-distributed-systems/) | Google | 2006 | Distributed locking, Paxos-based consensus, coarse-grained locks |
| [Dapper: A Large-Scale Distributed Systems Tracing Infrastructure](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/) | Google | 2010 | Distributed tracing, sampling, trace propagation |
| [Borg: Large-Scale Cluster Management at Google](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) | Google | 2015 | Container scheduling, resource management, predecessor to Kubernetes |
| [TAO: Facebook's Distributed Data Store for the Social Graph](https://research.facebook.com/publications/tao-facebooks-distributed-data-store-for-the-social-graph/) | Meta | 2013 | Read-optimized graph storage, tiered caching |
| [Finding a Needle in Haystack: Facebook's Photo Storage](https://research.facebook.com/publications/finding-a-needle-in-haystack-facebooks-photo-storage/) | Meta | 2010 | Blob storage, metadata elimination, write-once CDN |
| [Scaling Memcache at Facebook](https://research.facebook.com/publications/scaling-memcache-at-facebook/) | Meta | 2013 | Cache consistency, regional pools, lease mechanism |
| [Zanzibar: Google's Consistent, Global Authorization System](https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/) | Google | 2019 | Relation-based ACLs, global consistency, low-latency authz |
| [Kafka: A Distributed Messaging System for Log Processing](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/09/Kafka.pdf) | LinkedIn | 2011 | Log-structured messaging, consumer groups, durable pub-sub |
| [In Search of an Understandable Consensus Algorithm (Raft)](https://raft.github.io/raft.pdf) | Stanford | 2014 | Leader election, log replication, simpler alternative to Paxos |
| [Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases](https://dl.acm.org/doi/10.1145/3035918.3056101) | Amazon | 2017 | Shared storage, log as the database, cloud-native RDBMS |

### Notable Blog Posts

Real-world engineering decisions with context on why they were made.

- [How Discord Stores Trillions of Messages](https://discord.com/blog/how-discord-stores-trillions-of-messages) - Cassandra → ScyllaDB migration at massive scale
- [Netflix: Chaos Engineering](https://netflixtechblog.com/chaos-engineering-upgraded-878d341f15fa) - origin of Chaos Monkey, resilience by design
- [Uber: Service-Oriented Architecture](https://www.uber.com/en-US/blog/service-oriented-architecture-uber-engineering/) - microservice migration from monolith
- [LinkedIn: From Monolith to Microservices](https://engineering.linkedin.com/architecture/brief-history-scaling-linkedin) - scaling story behind LinkedIn's infrastructure
- [Shopify: Resiliency Through Simplicity](https://shopify.engineering/simplify-retry-handling-with-exponential-backoff) - how Shopify handles flash sales and traffic spikes
- [Cloudflare: How We Run Our DNS](https://blog.cloudflare.com/how-cloudflares-architecture-allows-us-to-scale-to-stop-the-biggest-attacks-in-history/) - anycast, DDoS mitigation, edge architecture

---

## Conference Talks

### Distributed Systems & Architecture

| Talk | Speaker | Conference | Key Ideas |
|------|---------|------------|-----------|
| [Turning the Database Inside-Out with Apache Samza](https://www.youtube.com/watch?v=fU9hR3kiOK0) | Martin Kleppmann | Strange Loop 2014 | Log-centric architecture, materialized views, stream-table duality |
| [Simple Made Easy](https://www.youtube.com/watch?v=SxdOUGdseq4) | Rich Hickey | Strange Loop 2011 | Simplicity vs. easiness, complecting, design philosophy |
| [The Language of the System](https://www.youtube.com/watch?v=ROor6_NGIWU) | Rich Hickey | Strange Loop 2012 | Values, processes, queues, and how systems communicate |
| [CQRS and Event Sourcing](https://www.youtube.com/watch?v=JHGkaShoyNs) | Greg Young | GOTO 2014 | Command/query separation, event-driven state, audit logs |
| [Microservices](https://www.youtube.com/watch?v=wgdBVIX9ifA) | Martin Fowler | GOTO 2014 | Microservice definition, trade-offs, when to use |
| [Jepsen: Distributed Systems Safety Analysis](https://www.youtube.com/watch?v=tRc0O9VgzB0) | Kyle Kingsbury (aphyr) | Strange Loop 2014 | Linearizability testing, real-world DB failures, Jepsen framework |
| [Consistency Without Consensus in Production Systems](https://www.youtube.com/watch?v=em9zLzM8O7c) | Peter Bailis | Strange Loop 2014 | Coordination avoidance, invariants, CRDT-style thinking |

### Reliability & Operations

| Talk | Speaker | Conference | Key Ideas |
|------|---------|------------|-----------|
| [How Netflix Thinks About DevOps](https://www.youtube.com/watch?v=UTKIT6STSVM) | Dave Hahn | Netflix | Chaos engineering, failure injection, operational maturity |
| [Designing for Failure at Netflix](https://www.youtube.com/watch?v=RWyZkNzvC-c) | Ben Schmaus | AWS re:Invent | Fallbacks, circuit breakers, degraded modes |
| [SRE at Google: How Google Runs Production Systems](https://www.youtube.com/watch?v=d2wn_E1jxn4) | Liz Fong-Jones | Various | SLOs, error budgets, toil reduction |
| [The Error Model](https://www.youtube.com/watch?v=oFdaJjkDNtg) | Joe Duffy | Lang.NEXT | Failures as first-class types, checked exceptions revisited |

### Data Systems & Streaming

| Talk | Speaker | Conference | Key Ideas |
|------|---------|------------|-----------|
| [The World Beyond Batch: Streaming 101](https://www.youtube.com/watch?v=9fWdCQNS5Yg) | Tyler Akidau | Various | Event time vs. processing time, watermarks, triggers |
| [Apache Kafka and the Rise of Streaming](https://www.youtube.com/watch?v=el-SqcZLZlI) | Jay Kreps | Various | Log as universal integration layer, stream processing |
| [Questioning the Lambda Architecture](https://www.youtube.com/watch?v=UPr1e3zMqns) | Jay Kreps | QCon | Kappa architecture, log-based unification |

### Performance & Systems

| Talk | Speaker | Conference | Key Ideas |
|------|---------|------------|-----------|
| [Latency Numbers Every Programmer Should Know](https://www.youtube.com/watch?v=UvTyDP_r8bA) | Various | Various | Cache/disk/network latency intuition, system design grounding |
| [Solid Cache: How Basecamp Saved $1M with a Disk Cache](https://www.youtube.com/watch?v=wh98s0XhMmQ) | DHH / Basecamp | Rails World 2023 | SSD-backed cache, cost vs. RAM cache, real-world trade-offs |
| [Understanding the JVM JIT Compiler](https://www.youtube.com/watch?v=oH4_unx8eJQ) | Doug Hawkins | GOTO | Tiered compilation, JIT warmup, performance implications |
