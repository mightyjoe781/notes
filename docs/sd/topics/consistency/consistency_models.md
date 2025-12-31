# Consistency Models

Consistency models are contracts between distributed systems and applications that specify what values can be returned by read operations. They define the behavior applications can expect when multiple processes access shared data concurrently across different nodes in a distributed system.

Why Consistency Models Matter ?

- **Correctness guarantees**: Define what behaviors are allowed in distributed systems
- **Performance trade-offs**: Stronger consistency typically means higher latency
- **Programming models**: Affect how applications must be designed and reasoned about
- **System design**: Influence architecture decisions and implementation complexity

### Consistency Spectrum

![](assets/Pasted%20image%2020251230113518.png)

Common Misconceptions :

- **Consistency is binary**: There are many levels between strong and weak
- **Stronger is always better**: Business requirements should drive consistency choice
- **Consistency equals correctness**: Applications can be correct with weaker consistency
- **Database choice determines consistency**: Many systems offer tunable consistency

------

There are 4 types of Consistency

- Strong Consistency
- Eventual Consistency
- Weak Consistency
- Session Consistency
## Strong Consistency

Strong consistency ensures that all nodes see the same data at the same time. After a write operation completes, all subsequent reads will return the updated value, regardless of which node serves the read.

### Strong Consistency Characteristics

#### Linearizability (Strongest Model)

Definition : Once a write is acknowledged, all subsequent reads from any node will return the new value

Properties

- Real-time ordering : Operations appear in a global order
- Atomic Operation : Each operation takes effect simultaneously
- Immediate Visibility : Writes visible to all nodes immediately
- Single-Copy Semantics: Appears as single, non-replicated system
- Global Clock : Operations ordered as if on global timeline

#### Sequential Consistency

Properties

- Program order: Operations from each process in program order
- Global sequence: All operations appear in single total order
- No real-time constraints: Operations may be reordered
- All processes agree: Same order seen by all processes
- Atomic operations: Operations appear instantaneous

Difference from Linearizability : "Operations may appear to happen in different order than real-time, but all processes agree on the order"
### Strong Consistency Implementation

#### Consensus-Based Approaches

Consensus Algorithm Requirements:

- Agreement: All nodes decide on same value
- Validity: Decided value was proposed by some node
- Termination: All correct nodes eventually decide
- Integrity: Each node decides at most once
- Fault tolerance: Works despite node failures

Common Algorithms

- Raft: Leader-based consensus with log replication
- Paxos: Multi-phase consensus protocol
- PBFT: Byzantine fault-tolerant consensus
- Viewstamped Replication: Primary-backup with view changes
- Zab: ZooKeeper atomic broadcast protocol
#### Synchronous Replication

Synchronous Replication Process

- Client sends write request to coordinator
- Coordinator forwards write to all replicas
- All replicas acknowledge write completion
- Coordinator acknowledges to client
- Write is now visible to all reads
### Strong Consistency Systems

#### Traditional RDBMS

- Relational Database Approach
    - ACID transactions guarantee consistency
    - Two-phase locking ensures serializability
    - WAL (Write-Ahead Logging) for durability
    - Distributed transactions via 2PC
    - Strong consistency within transaction boundaries

Examples : PostgreSQL with synchronous replication, MySQL Cluster (NDB), Oracle RAC, SQL Server AlwaysOn, Google Spanner (globally distributed).
#### Distributed Strong Consistency Systems

Specialized Systems:

- `Apache HBase`: Strong consistency for row operations
- `etcd`: Strongly consistent key-value store
- Apache ZooKeeper: Coordination service with strong consistency
- TiDB: Distributed SQL with strong consistency
- CockroachDB: Distributed SQL with serializable isolation

Use Cases : Configuration Management, Service Discovery, Leader Election, Distributed Locking, Financial Transactions
### Strong Consistency Trade-offs

Performance Costs:

- Higher latency: Coordination overhead
- Lower throughput: Synchronization bottlenecks
- Reduced availability: Sensitive to node failures
- Geographic limitations: Cross-region coordination expensive
- Scalability constraints: Coordination doesn't scale linearly

Optimization Strategies

- Batching: Group operations to amortize coordination cost
- Read replicas: Offload reads to reduce coordinator load
- Partitioning: Reduce coordination scope
- Caching: Cache frequently accessed data
- Local operations: Minimize cross-node coordination

------

## Eventual Consistency

Eventual consistency guarantees that if no new updates are made to a given data item, eventually all accesses to that item will return the last updated value. The system will become consistent over time, but not immediately.

### Eventual Consistency Characteristics

#### Basic Properties

*"Given enough time and no new updates, all nodes will eventually have the same data"*

Eventual Consistency Guarantees :

- Convergence: All replicas will eventually converge
- No time bound: No guarantee on when convergence occurs
- Temporary inconsistency: Different nodes may see different values
- Update propagation: Changes eventually reach all nodes
- Conflict resolution: Mechanisms to handle concurrent updates
#### Conflict Scenarios

Common Conflict Situations

- Concurrent updates: Multiple clients update same data
- Network partitions: Updates on different sides of partition
- Offline updates: Mobile clients updating while disconnected
- Geographic distribution: Updates in different regions
- System failures: Updates during node outages

Resolution Requirements

- Deterministic resolution: Same conflicts resolve same way
- Commutative operations: Order independence when possible
- Associative merging: Consistent regardless of merge order
- Idempotent operations: Safe to apply multiple times
- Semantic preservation: Business meaning maintained
### Eventual Consistency Implementation

#### Anti-Entropy Mechanisms

Convergence Techniques:

- Gossip protocols: Peer-to-peer information exchange
- Merkle trees: Efficient difference detection
- Version vectors: Track causal relationships
- Read repair: Fix inconsistencies during reads
- Background repair: Periodic consistency checks
- Hinted handoff: Store updates for offline nodes
#### Conflict Resolution Strategies

Resolution Approaches:

- Last-write-wins: Use timestamps to resolve conflicts
- Multi-value: Store all conflicting values
- Application resolution: Let application decide
- CRDT operations: Conflict-free data types
- Custom merge functions: Domain-specific resolution
- Human intervention: Manual conflict resolution


```
Vector Clock Example:
Node A: [A:2, B:1, C:0] - A has seen 2 of its own operations, 1 from B
Node B: [A:1, B:3, C:1] - B has seen 1 from A, 3 of its own, 1 from C
Concurrent if neither vector dominates the other
```

### Eventual Consistency Systems

#### NoSQL Databases

Eventually Consistent Systems:

- Amazon DynamoDB: Tunable consistency levels
- Apache Cassandra: Eventual consistency by default
- `Riak`: Configurable consistency with eventual default
- CouchDB: Multi-master replication with conflict resolution
- MongoDB: Eventual consistency with read preferences
#### Web-Scale Systems

Large-Scale Eventually Consistent Systems:

- DNS: Global name resolution system
- CDN: Content delivery networks
- Social media feeds: Facebook timeline, Twitter feed
- E-commerce catalogs: Product information
- Web caches: Browser and proxy caches
- Email systems: Message delivery across servers

Characteristics:

- Massive scale: Billions of operations
- Global distribution: Worldwide deployment
- High availability: Always responsive
- Acceptable inconsistency: Business tolerates temporary differences
- User experience: Availability more important than perfect consistency
### Eventual Consistency Challenges

#### Application Complexity

Programming Challenges:

- Handling stale reads: Data may be outdated
- Conflict resolution: Application must handle conflicts
- User experience: Managing user expectations
- Testing complexity: Non-deterministic behavior
- Debugging difficulty: Race conditions and timing issues

Design Patterns:

- Read-your-writes: Users see their own updates immediately
- Monotonic reads: Users don't see data go backward in time
- Causal consistency: Related operations maintain order
- Session consistency: Consistency within user session
- Compensating transactions: Undo operations when conflicts detected
#### Business Logic Adaptation

Business Process Considerations:

- Idempotent operations: Safe to execute multiple times
- Commutative operations: Order independence
- Convergent operations: Multiple executions lead to same state
- Compensation logic: Ability to undo operations
- Conflict detection: Recognize when conflicts occur

Examples:

- Shopping cart: Adding items is commutative
- Like counts: Increment operations are commutative
- Collaborative editing: Operational transformation
- Financial transactions: Require careful conflict resolution
- Inventory: May require compensation for overselling

------

## Weak Consistency

Weak consistency provides minimal guarantees about when data will be visible across the system. It prioritizes availability and performance over consistency, offering the weakest ordering guarantees.
### Weak Consistency Models

#### Basic Weak Consistency

Properties :

- Minimal ordering: Few guarantees about operation order
- Best effort: System tries to maintain some consistency
- High performance: Optimized for speed and availability
- Application responsibility: Apps must handle inconsistency
- Eventually consistent: May converge over time

Characteristics

- Reads may return any value that was ever written
- No guarantees about seeing latest writes
- Different nodes may see different orders of operations
- Suitable for use cases where perfect consistency not required
- Extremely high performance and availability

#### Release Consistency

Release Consistency Models

- Acquire operations: Gain access to shared data
- Release operations: Finish access to shared data
- Ordinary operations: Regular reads and writes
- Ordering guarantees: Only between acquire/release pairs
- Programming model: Similar to memory barriers

Use Cases : Shared Memory Systems, Distributed Computing frameworks, Lock-Based Synchronization, Message Passing Systems, Parallel Processing Applications, etc.
### Weak Consistency Applications

There are mainly two application for weak-consistency

- High Performance Systems
- Caching Systems
#### Performance-Critical Systems

Examples of Use Cases :

- Gaming systems: Player position updates
- Real-time analytics: Streaming data processing
- IoT systems: Sensor data collection
- Financial trading: High-frequency trading systems
- Live streaming: Video/audio distribution
- Social media: Activity feeds and counters

Characteristics of such systems are : Volume over Accuracy, Approximate Results, Low Latency, Fault Tolerance, Eventual Consistency.
#### Caching Systems

Cache Consistency Models

- Write-through: Updates cache and storage synchronously
- Write-back: Updates cache immediately, storage later
- Write-around: Bypasses cache for writes
- Cache-aside: Application manages cache explicitly
- Refresh-ahead: Proactively refresh expiring entries
### Weak Consistency Benefits & Challenges

Benefits :

- ultra low latency, high through put, high availability, geographic scalability, resource efficiency.
- Linear scalability, No Co-ordination Bottlenecks, Partition Tolerance, Elastic Scaling, Cost Effective

Challenges

- Uncertainty handling, Conflict resolution, manage user experience, Testing Complexity, Monitoring Difficulty

Mitigation Strategies

- Graceful degradation: Degrade functionality, not availability
- Approximate results: Provide best-effort answers
- Error recovery: Handle inconsistent state gracefully
- User feedback: Inform users about data freshness
- Compensation: Correct errors when detected

------

## Session Consistency

Session consistency provides consistency guarantees within the context of a single client session, ensuring that a client's view of the data is consistent with their own operations while allowing inconsistency across different sessions.

Main Use Case is maintaining User Profiles in applications, apps, etc.
### Session Consistency Guarantees

#### Read Your Writes

In Read Your Writes Consistency, user see their changes immediately, scope of the change is limited to the current session. Any reads following writes see the updates. There is no global ordering.

Implementation :

- Session affinity: Route client to same server
- Client-side versioning: Track version numbers
- Write tracking: Remember what client has written
- Monotonic read consistency: Don't go backward in time
- Causal consistency: Maintain cause-effect relationships
#### Monotonic Read Consistency

In Monotonic Read Consistency, later reads see newer or same data. There is no time-travel. Applicable only within the client session.

Benefits of this are : Predictable user experience, user doesn't see data going backwards. Easy to implement and compatible with caching.
### Session Consistency Implementation

#### Client-Side Techniques

Client Side Implementation Patterns

- Version tracking: Client remembers last seen version
- Session tokens: Include version in session identifier
- Sticky routing: Route to servers with latest data
- Local caching: Cache data seen by client
- Causal context: Track causally related operations

Server Side Implementation Patterns

- Session state: Maintain per-session metadata
- Version vectors: Track causal relationships
- Read preferences: Allow clients to specify requirements
- Write concerns: Ensure writes meet client requirements
- Conflict detection: Identify when guarantees violated
#### System Design Patterns

Architecture Patterns

- Session affinity: Load balancer routes to same server
- Read-after-write routing: Special handling for recent writes
- Client libraries: Embed consistency logic in client
- Proxy layer: Intermediate consistency management
- Database features: Built-in session consistency support

Examples : 

- MongoDB: Causal consistency in client sessions
- CosmosDB: Session consistency level option
- DynamoDB: Consistent reads within session
- Cassandra: Session consistency through client drivers
- Redis: Session consistency via connection affinity
### Session Consistency vs Other Models

| Consistency Model | Scope      | Guarantees                | Complexity | Performance |
| ----------------- | ---------- | ------------------------- | ---------- | ----------- |
| **Strong**        | Global     | All operations ordered    | High       | Lowest      |
| **Session**       | Per-client | Client operations ordered | Medium     | Medium      |
| **Eventual**      | Global     | Eventually converges      | Medium     | High        |
| **Weak**          | Minimal    | Best effort               | Low        | Highest     |

------

## Choosing the Right Consistency Model

### Decision Framework

#### Business Requirements Analysis

Key Questions:

- Data importance: How critical is data consistency?
- User experience: What do users expect?
- Business impact: What happens with inconsistent data?
- Regulatory needs: Are there compliance requirements?
- Performance requirements: What are latency/throughput needs?
- Scale requirements: How large will the system be?
- Geographic distribution: Is global deployment needed?

Decision Matrix:

- Financial data: Strong consistency required
- User profiles: Session consistency usually sufficient
- Analytics data: Eventual consistency often acceptable
- Caching data: Weak consistency for performance
- Configuration data: Strong consistency for reliability
- Social media: Eventual consistency for scale

#### Technical Considerations

Implementation Factors:

- Team expertise: Complexity vs capability
- Operational overhead: Monitoring and debugging
- Technology constraints: Platform capabilities
- Performance budget: Latency and throughput targets
- Availability requirements: Uptime expectations
- Cost considerations: Infrastructure and development costs
- Maintenance burden: Long-term operational costs
### Hybrid Approaches

#### Multi-Level Consistency

LayeredConsistency Strategies:

- Core data: Strong consistency for critical operations
- User data: Session consistency for personal information
- Analytics: Eventual consistency for aggregations
- Cache layers: Weak consistency for performance
- Derived data: Eventual consistency for computed values

Benefits:

- Optimized per data type
- Balanced performance and consistency
- Reduced complexity where possible
- Cost optimization
- Flexibility for changing requirements

#### Consistency Evolution

![](assets/Pasted%20image%2020251230123005.png)

------

## Conclusion

### Key Takeaways

1. **Consistency is a spectrum**: Many levels between strong and weak consistency
2. **Business requirements drive choice**: Technical capabilities must align with business needs
3. **Trade-offs are fundamental**: Consistency, availability, and performance are interconnected
4. **Session consistency is often ideal**: Good balance for interactive applications
5. **Hybrid approaches work**: Different data types can use different consistency models

#### Implementation Guidelines

**For Strong Consistency**:

- Use for critical business data where correctness is paramount
- Implement proper consensus algorithms or synchronous replication
- Plan for reduced availability during partitions
- Monitor performance impact and optimize coordination overhead
- Test failure scenarios and recovery procedures

**For Eventual Consistency**:

- Design conflict resolution strategies from the beginning
- Implement monitoring for convergence and conflicts
- Educate users about temporary inconsistencies
- Use CRDTs or other conflict-free approaches where possible
- Plan for operational complexity of debugging

**For Session Consistency**:

- Implement client-side version tracking
- Design session affinity or read-after-write routing
- Balance session state management overhead
- Monitor session consistency violations
- Provide clear guarantees to application developers

#### Common Pitfalls

- **Choosing consistency too early**: Start with requirements, not technology
- **Underestimating complexity**: Weaker consistency often means more complex applications
- **Ignoring user experience**: Consistency affects how users perceive the system
- **Not testing edge cases**: Consistency violations often occur in failure scenarios
- **Over-engineering**: Don't use stronger consistency than actually needed