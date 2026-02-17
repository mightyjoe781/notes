# Advanced Algorithms

NOTE: Following algorithms are way too advanced for implementation, you are better off using some library implementing these algorithms. Its important to understand what problems these algorithms are solving efficiently.
Most of the algorithm are often implemented in the solutions of System Design Problems.

## Content

Core Probabilistic & Approximate Data Structures (*Space-Accuracy Trade-Off*)

- [Bloom Filters](bloom_filters.md) : Membership testing with false positives
- [Count-Min Sketch](count-min_sketch.md) : Frequency estimation in Data Streams
- [Hyper Log-Log](hyper_log_log.md) : Cardinality Estimation


Tree Based Indexing & Spatial Data Structures (*Hierarchical partitioning*)

- [Trie](../dsa/strings/ch3.md) : Prefix Based Lookup
- [B-Tree](btree.md) : Disk friendly ordered indexing
- [Quad Tree](quadtree.md) : 2D Spatial Partitioning
- [GeoHashing](geohashing.md) : Spatial Indexing using String Prefixes


Storage & Synchronization Structures (*Efficient Persistence & Comparisons*)

- [LSM Tree](lsm.md) : Write-optimized Storage Engines
- [Merkle Tree](merkle_tree.md) : Efficient Data Integrity & Sync
- [Rsync Algorithm](rsync_algo.md) : Delta based file synchronization


Hashing, Distribution & Rate Control (*Load Distribution & Control*)

- Consistent Hashing : Stable sharding with minimum reshuffling
- Token Bucket : Rate Limiting & Traffic Shaping
- Hierarchical Timing Wheels : Efficient time management at scale


Distributed Consensus & Coordination (*Agreement under failure*)

- Raft
- Paxos

Collaborative & Conflict Resolution Algorithms (*Eventually consistent collaboration*)

- Operational Transformation (OT) : Real-time collaborative editing
- Conflict-Free Replicated Data Types (CRDTs) : Convergent state without coordination
