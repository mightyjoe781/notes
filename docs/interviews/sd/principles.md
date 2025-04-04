
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
