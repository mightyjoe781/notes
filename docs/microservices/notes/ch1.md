## Introducing Microservices

#### What are Microservices

*An architectural style where autonomous, independently deployable services collaborate to form an application.*

#### The Problem of Monoliths

*Monoliths :* 

- Single Process
- Single Codebase
- Single Host
- Single databse
- Consistent Technology

Benefits are Simplicity, One Codebase (easy to find errors), single Deployments. Monoliths are not wrong approach but they are sometimes are not desirable for example.

- Monoliths works well for small application
- Problem of scaling (Horizontal Scaling often not possible, Vertical scaling is expensive, whole application needs to scaled)
- Increasing Complexity
- Modular Monoliths often becomes very dependent on each other.
- Difficult to Deploy (Risky, Requires downtime).
- Wedded to legacy technology.

Distributed Monoliths divided in to multiple services which share same database is not same as Microservices.

#### The Benefits of Microservices

- Small Services ( Can be owned by a team)
- Easier to Understand, Rewritten
- Adopt new technology
- Standardize where it makes sense
- Loose Coupling allows individual deployment, Lower risk, minimize downtime.
- Frequent Updates
- Scale services individually and Cost Effect
- Adapt rapidly and Easier to Reuse

#### The Challenges of Microservices

- Developer Productivity, How easy can we make it for devs to be productive working on system.
- Complex Interaction, Take care to avoid inefficient, chatty communication between microservices
- Automated Deployments are must
- Monitoring is needed because a centralized place to check logs and monitor for problems.

#### Introducing the Demo Application

Use this link [Repo](https://github.com/dotnet-architecture/eShopOnContainers).

E-commerce is well known problem statement. Main focus would be on learning Microservices.