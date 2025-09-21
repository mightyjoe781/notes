# Interview Guide

Machine Coding

- problem statement -> Algorithm (easy)
- we have to implement a working (imp) solution that handles the code base in a graceful and extendible way.
- focus on SOLID, OOPs and Design Patterns

Where to find questions ~ 

- search LeetCode reviews for SDE 2 rounds
    - Management Systems
    - Game Related Problems (ticktactoe, chess, card games)
    - Infra Questions -> Designing Cache, a logger, Distributed Queue, etc
    - Product -> SplitWise, BookMyShow (booking flow), E-commerce

If problem is to be coded in the interview itself, you are expected to write a Day-0 problem solution. 
But if the problem is given as take-home assignment then you are expected to provide very high level of design implementation, tests and understanding.

Steps to Approach the Problem

- Requirements
    - Feature Requirements
    - Non Feature Requirements -> Solution Requirements
        - Are we expected to produce running code.
        - Focus on Entities and other classes.
        - How you want data to be handled ? Local DB, Remote DB, etc ?
        - Mode of running expected ~ CLI, REST APIs

We are expected to produce a running code + cli/rest api + db interaction - in memory/sql anything.

Any DB query interaction should happen via repository pattern (repository layer).

![](assets/Pasted%20image%2020250921233038.png)



