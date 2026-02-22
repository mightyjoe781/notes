# Consensus Algorithm

Consensus Algorithms are used to gain agreement between network of nodes in a distributed system.

A consensus algorithm  must have following three property

- Agreement : every correct process must agree on the same value
- Validity : values agreed upon must have been proposed by another process termination.
- Termination : A value will eventually be decided by every correct process


### CAP Theorem

- Consistency
- Availability
- Partition Tolerance

More on CAP Here : [CAP](../sd/topics/consistency/cap.md)

CAP Theorem Constraints

- In the presence of a network partition, you must choose between
    - Consistency: Reject requests to maintain data consistency
    - Availability: Accept requests but risk data inconsistency
- When no partition exists
    - Both consistency and availability can be maintained
    - The trade-off becomes irrelevant

So a consensus algorithm must handle different types of failures,

- Fail-Stop
- Network Partition
- Fail-recover
- Byzantine Failure

### Byzantine Failure

[Video Explanation](https://www.youtube.com/watch?v=Bvj72wN0OVk)



Conditions on Generals 

- Only direct message is possible
- Two of them are traitors

We should find a strategy that every honest general will follow.

Input : YES/NO for every honest general

![](assets/Pasted%20image%2020260218120638.png)

Output : YES/NO for every honest general.

Task : All honest generals output the same answer.

![](assets/Pasted%20image%2020260218120759.png)
![](assets/Pasted%20image%2020260218120819.png)

There are two solution to it.

### Leader Selection

Leader can take the votes from all the nodes and return the majority opinion to everyone.

![](assets/Pasted%20image%2020260218121202.png)

Only Flaw is if we select a bad node as leader, it can send out wrong results.

![](assets/Pasted%20image%2020260218121228.png)

### Local Algorithm

Everybody sends their opinion to everyone their opinion, and each of the nodes agrees on the most frequent value.

![](assets/Pasted%20image%2020260218121655.png)

Only issue is that if we still have bad nodes which send corrupt data (say yes to some, and no to some) we will not be able to reach consensus.

A simple solution is to combine these patterns and select three nodes and run the voting 3 times.

Coming back to leader based protocol, since we know there are at most 2 leaders, we can select three leaders and run consensus.

Let's say we select following three.

![](assets/Pasted%20image%2020260218122140.png)

At least one of these 3 generals is honest,

Still there is a problem, what happens if general-3 sends random majority junk value to everyone, and no consensus is decided,

![](assets/Pasted%20image%2020260218122313.png)

A simple solution is to lock the leader once a majority is reached.

![](assets/Pasted%20image%2020260218122412.png)

During agreement if we get leaders opinion along with local opinion, if majority of the votes lean towards one of the value then we go with local opinion (rogue generals can't skew the decision) but if there is a tie, its almost alway better to go with leader's opinion

```
for leader_id in [1, 2, 3]:
    send my opinion to everybody
    if I am the leader: # Leader-based algo
        my opinion <- majority opinion
        broadcast my opinion
    count YES and NO messages # Local algo
    if YES >= 10 or NO >= 10:
        my opinion <- local opinion
    else:
        my opinion <- leader opinion
```
## Raft

Replicated and Fault Tolerant Algorithm

It is a *leader-based*, understandable protocol designed for managing replicated logs in fault-tolerant distributed systems.

[Martin Kleppmann Lecture](https://www.youtube.com/watch?v=uXEYuDwm7e4)

[Best Site for Explanation](https://raft.github.io/)

- **Leader Election:** Nodes are either Leaders, Followers, or Candidates. If a follower receives no communication (heartbeat) from a leader, it becomes a candidate, increases its "term," and requests votes to become the new leader

- **Log Replication:** The leader receives client requests, writes them to its log, and forces followers to replicate these entries.

- **Safety & Quorums:** A majority of nodes (quorum) must agree on log entries before they are committed. This ensures that if any node fails, the system can still function, provided a majority remains.

- **Log Consistency:** If a follower's log diverges from the leader, the leader forces the follower to duplicate its own log.

Amazing Visualization : https://thesecretlivesofdata.com/raft/

### Raft in Real Life

`etcd (coreOS/CNCF)`

- Probably the most widely used Raft implementation.
- Production-grade.
- Used by Kubernetes for cluster state storage.

`HashiCorp Raft`

