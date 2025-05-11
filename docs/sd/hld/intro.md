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