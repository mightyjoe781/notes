# Books Notes - Part 1
Generated on: 2025-06-01 14:11:13
Topic: books
This is part 1 of 1 parts

---

## File: books/designing_data_intensive_applications/ch1.md

# Reliable, Scalable and Maintainable Applications

- Many modern applications are *data-intensive* rather than *compute-intensive*.
- A data-intensive application is typically built around standard building blocks providing common needed functionality like
  - Store data so that they, or another application can find it later (databases)
  - Remember the result of expensive operation to speed up reads (caches)
  - allow users to search data by keyword or filter in various ways (search indexes)
  - send a message to another process, to be handled asynchronously (stream processing)
  - periodically crunch a large amount of accumulated data (batch processing)
- If above building blocks sound obvious because these *data systems* are successful abstraction.

## Thinking about Data Systems

- Databases, queues, and caches are typically seen as different tools due to their varied access patterns and use cases, but ultimately, they all store data for some time.
- Tools like Apache Kafka (a message queue with database durability) and Redis (both a datastore and message queue) blur these distinctions further.
- Modern applications have diverse requirements that a single tool often cannot meet. Tasks are typically divided to be processed efficiently by different data systems, working in harmony with application code to handle large data volumes.

Designing a new data system involves solving these key problems:

- Ensuring data remains correct and complete, even if internal issues arise.
- Maintaining good performance for clients, even when parts of the system degrade.
- Scaling to handle increased load.
- Designing a user-friendly and functional API for the service.

External factors influencing the design process include:

- The skills and experience of the team.
- Dependencies on legacy systems and technical debt.
- The delivery timescale.
- The organization’s risk tolerance and regulatory constraints.

## Reliability

- In a typical software setting, reliability involves ensuring that:
  - The application performs its expected functionality.
  - The application can tolerate user mistakes and unexpected usage.
  - The performance is good under expected load and data volumes.
  - The system prevents unauthorized access and abuse.
- Faults are issues that can occur within a system. A fault-tolerant or resilient system can cope with these issues, though this doesn't guarantee handling every possible fault.
- Failure occurs when the entire system stops working, whereas faults are deviations in individual components from their specifications. Since eliminating all faults is impossible, designing fault-tolerant systems is usually best.
- One approach to designing fault-tolerant systems is to create deliberate faults and observe the system's reactions, as exemplified by Netflix's Chaos Monkey.
- While tolerating faults is generally preferred, there are cases, such as cybersecurity attacks, where prevention is better than cure.

### Kinds of Faults

#### Hardware Faults

- **Hardware Failures and Redundancy**: Hardware faults like hard disk crashes, RAM failures, power outages, and network issues are common in large datacenters. To mitigate these, redundancy techniques such as RAID configurations, dual power supplies, and backup power systems are used to keep machines running uninterrupted for years.
- **Increasing Demand and Fault Rates**: As data volumes and computing demands grow, the use of larger numbers of machines increases the rate of hardware faults. Cloud platforms, like AWS, often experience unannounced virtual machine outages due to their design for flexibility and elasticity over single-machine reliability.
- **Shift to Software Fault-Tolerance**: Modern systems are increasingly designed to tolerate entire machine losses using software fault-tolerance techniques alongside or instead of hardware redundancy. This allows for operational advantages like rolling upgrades, enabling system patches without requiring downtime.

#### Software Errors

- Hardware faults are generally random and independent (one disk failture is not related to other), some weak correlation might exists due to environmental factors like temperature
- Systematic error are harder to predict and correlated across nodes causing widespread system failures. Examples include software bugs (linux leap year bug), resource-hogging processes, dependency issues, and cascading failures.
- There are no quick fixes, but several small strategies can help:
  - Careful assumption and interaction analysis, thorough testing, process isolation, crash recovery, and continuous monitoring.
  - Implement self-checks to verify system guarantees and raise alerts for discrepancies.

#### Human Erros

- Humans are prone to errors; configuration mistakes by operators are a major cause of outages, more so than hardware faults.
- **Strategies for Reliable Systems**:
  - **Error Minimization**: Design systems with user-friendly abstractions, APIs, and admin interfaces that encourage correct usage.
  - **Decoupling**: Separate high-risk actions from critical operations; provide sandbox environments for safe experimentation with real data.
  - **Thorough Testing**: Use comprehensive automated and manual testing, from unit tests to integration tests, to cover rare corner cases.
  - **Recovery Mechanisms**: Ensure quick recovery from errors by enabling fast rollbacks, gradual code deployment, and tools for data recomputation.
  - **Detailed Monitoring**: Implement performance metrics and error rate monitoring to detect early warning signals and diagnose issues.
  - **Management and Training**: Apply good management practices and training to improve human reliability.

### How important is Reliability

- **Reliability Beyond Critical Systems**:
  - Reliable operation is important for all applications, not just critical ones like nuclear power or air traffic control.
  - Business application bugs can lead to lost productivity, legal issues, and significant revenue losses during outages.
  - Users depend on applications to safely store important data; losing such data can be devastating.
- **Balancing Reliability and Costs**:
  - Sometimes, reliability might be sacrificed to reduce development or operational costs, such as for prototype products or low-margin services.
  - It's crucial to be conscious and deliberate about when and why reliability is being compromised.

## Scalability

*Scalability* is described as a system’s ability to cope with increased load. Its often useful to talk about questions like : if system grows in a particular way, what are our options for coping with growth. How to add more compute to handle additional load

## Maintainability

---

## File: books/designing_data_intensive_applications/index.md

# Designing Data Intensive Applications

Author : Martin Kleppmann

- Foundations of Data Systems
  - [Reliable, Scalable, and Maintainable Application](ch1.md)
  - [Data Models and Query Languages](ch2.md)
  - [Storage and Retrieval](ch3.md)
  - [Encoding and Evolution](ch4.md)
- Distributed Data
  - Replication
  - Partitioning
  - Transactions
  - The trouble with Distributed Systems
  - Consistency and Consensus
- Derived Data
  - Batch Processing
  - Stream Processing
  - Future of Data Systems

---

## File: books/index.md

# Library

## Books

- [Designing Data-Intensive Applications](designing_data_intensive_applications/index.md)
- [The Pragmatic Programmer Notes](https://media.minetest.in/the_pragmatic_programmer_notes.pdf)

---

