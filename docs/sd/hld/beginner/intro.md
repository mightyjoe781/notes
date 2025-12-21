# Introduction to System Design

## What is System Design ?

![](assets/Pasted%20image%2020251221191055.png)

* A set of requirements which requires defining :
    * Architecture
    * Components
    * Modules
* It deals with how above 3 pieces interact with each other, cumulatively solving the problem at hand.

## Framework for Designing a System

* Pattern for solving a system design problem goes something like :
    * Break down problem statement into *solvable* sub-problem (divide & conquer)
    * Decide *key components and responsibilities*
    * Declare *boundaries* of each component
    * Understand *Key Challenges* in scaling your solution
    * Make architecture *fault-tolerant* and *available*

* Approaching System Design Problems
    * Understand the problem statement
    * Break it down into components
        * Be mindful of the components and start with components you know
    * Dissect each component
        * A Feed System might have - generator, aggregator & web server
    * For each sub-component look into
        * Database & Caching
        * Scaling & Fault Tolerance
        * Async Processing (Delegation)
        * Communication
    * Add more sub-components if needed
        * Understand the scope of each component
        * In above example of A Feed System, A Feed Generator could be made up of Post Service, Recommendation System, Follow Service which all connect together, and put data in feed database.

## How do you Evaluate a System ?

* Every system can be improved *infinitely* & you should have a better idea when to stop
* Follow these points
    * Break system into components
    * Each Component has a clear set of responsibility(Exclusive)
    * For Each Component have Clear technical details on database, caching, scaling, fault-tolerance, async processing, communication
* Make sure Each Component in Isolation is
    * Scalable - horizontally scalable
    * Fault-Tolerant - Plan for recovery in case of a failure
    * Available - Component function even when some component fails