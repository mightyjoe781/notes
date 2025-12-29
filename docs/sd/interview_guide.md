# Interview Guide

Usually interviews for LLD/HLD are time bound, approximately 60-90 mins on average. Let's assume its only 60 min interview, then 5 mins for introduction and 10 min on running through some hiccups in your local setup, leaves you with realistically 45 min for interview.

LLD interviews come in two flavors, one where interview may not want to have a working code, but want to evaluate you on how well you design your classes, other one are completely evaluate on working code, which is really hard to get right under time constraint.

HLD interviews in general involves communication around the clock, so everything you discuss either correct/incorrect would be evaluated throughout the process.

Although it may seems that you know all the concepts, its just the practice under time constraint that makes the difference. Here is the some structure for approaching the problems.

## LLD Interview Guide

First we should understand what interviewers are looking for ?

- Clear separation of Concern
- Reasonable trade-offs
- Working Solution
- Ability to explain solutions

Interviewers do not evaluate on Fancy Patterns, Over Abstraction, Framework-level code, etc.

Following is a simple structured guide to approach the interviews

- Read the Problem Carefully (don't jump to code)
    - Read the question *end-to-end* once without coding
    - Identify the *core problem* being solved, not just entities
    - Watch for hidden constraint that may be present (scale, concurrency, mutability)
- Extract Requirements Explicitly
    - What actions must the system support ?
        - Create/Update/Delete
        - Query/Search
        - State Transitions
    - Write all of the above as *bullet* points
    - Ex - *System must allow multiple users to book tickets concurrently.*
- Clarify Solution Scope
    - Can I use *in-memory* storage ? 
    - Is persistence required ?
    - Is this CLI/Library/API ?
    - Do we need **multi-threading support**?
    - Are failure scenarios in scope ?
- Identify Core-Domain Models
    - Extract *nouns* -> classes
    - Keep the models thin (data + *minimal behavior*)
    - Prefer `@dataclasses` for clarity & avoid adding too much logic to models.
- Identify Enums & States Early
    - States, types, modes → Enum
    - Prevent magic strings
- Define Interfaces and Responsibilities
    - Decide
        - Which class owns the Business Logic
        - Which class is a Data Holder
        - Which class is a Service/Co-ordinator
    - Use
        - ABC + interface only if needed
        - Composition over inheritance
- Decide the Design Patterns
    - object creation complexity : factory
    - multiple strategies : strategy
    - state transitions : state
    - event notification : observer
    - access control/caching : proxy
    - NOTE: Don't over engineer here, as working solution is better than *partial* perfect solution.
- Think about Concurrency Explicitly
    - If concurrency is required
        - Decide Lock Granularity, Thread-Safe Collections, Idempotency, etc.
- Error Handling & Validation
    - Invalid Inputs
    - State Violations
    - Duplicate Requests
- Write Code Incrementally : Enums, Data Models, Interfaces, Core service logic, then driver class
- Add Simple Driver or Test
    - demonstrates correctness
    - helps interviewer follow logic
- Call out Extensions, (don't implement)
    - How to scale
    - Where caching fits in
    - How to make application distributed
    - How to add persistence

As you can see its a lot to do actually and have it working, requires a lot of practice to get it right.
## HLD Interview Guide

HLD interviews are more about understanding the *reasoning* & *trade-offs* rather than code.

Interviewer are actually looking for structured thinking, realistic assumptions and clear trade-offs, ability to communicate clearly.

Ideal Interview will be like this

- Requirements -> Estimates : 10min
- Architecture : 15 min
- Deep Dives : 15 min
- Trade-Offs & Extension : 10 min

As you can see you barely have any time to *guess* stuff here, and this also requires a lot of practice and revision to get it right.

Following is a simple structured guide to approach the interviews

- Understand the problem & Define the Goal
    - What exactly we are building ?
    - Who are the *users* ? 
    - What is the core use case ?
    - Above question will help you catch misalignment early on
- Clarify Requirements (Always)
    - Functional Requirements (CRUD, search, messaging, streaming, etc)
    - User Flows (write-heavy vs read-heavy)
    - Sync vs Async Operations
    - ex - user can upload files, share and download file as well
- Non-Functional Requirements
    - QPS/TPS
    - Latency (p50, p99)
    - Availability
    - Consistency Requirements
    - Durability
    - NOTE: If not given, **make reasonable assumptions and state them clearly**. Don't make problem hard for yourself, by asking it to interviewers.
- Back-of the Envelope Calculations
    - This shows real word thinking
        - DAU/MAU
        - request per second
        - data-size per request
        - storage growth per day/year
        - Bandwidth
    - These number help decide the architectures
- Define APIs and Data Contracts
    - REST/gRPC endpoints
    - Request/Response Shapes
    - Idempotency
    - Pagination
- High Level Architecture Diagram
    - Draw Boxes, client, load-balancer, service, database/cache/queues
    - explain
        - sync vs async
        - read vs write flow
- Data Modeling & Storage Choices
    - Strong Consistency : SQL
    - High-Throughput Writes : NoSQL
    - Analytics : Columnar Storage
    - Cache : Redis
    - Search : ElasticSearch
- Scaling Strategies
    - Horizontal vs Vertical
    - Stateless Services
    - Sharding Strategy
    - Consistent Hashing
- Caching Strategies
    - where to cache : client, CDN, Application, DB
    - what to cache : hot reads, aggregates, metadata
    - discuss : cache invalidation, TTL, write-through, etc.
- Asynchronous Processing
    - Use Queues for : Notifications, Back-ground jobs, fan-out, re-triable work
    - Discuss : at-least-once delivery, idempotency, DLQ
- Consistency, Concurrency & Failure Handling
    - Address : Race Conditions, Distributed Locks, Idempotency Keys, Retry Strategies
    - Also Mention : Timeouts, Circuit Breakers, Graceful Degradation, etc.
- Bottlenecks & Hotspots
    - DB write bottlenecks
    - Hot Partitions
    - Thundering Herd
    - Cache Stampede
    - NOTE: propose mitigations for above issues in design
- Security & Access Control (discuss briefly)
    - Authentication/Authorization
    - Rate Limiting
    - Input Validation
- Observability
    - show production awareness like Metrics (QPS, latency), Logs, Tracing, Alerts
- Trade-Offs & Alternatives
- Extensions & Future Improvements
    - End Strong : Multi-region, Disaster Recovery, Cost Optimization, Schema Evolution.

As you can see it requires really a strong grip on following concepts to even answer the question correctly,

*Good Luck*