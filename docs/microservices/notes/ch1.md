## Introducing Microservices

#### What are Microservices

*An architectural style where autonomous, independently deployable services collaborate to form an application.*

#### The Problem of Monoliths

*Monoliths:*

- Single Process
- Single Codebase
- Single Host
- Single Database
- Consistent Technology

The benefits of monoliths are simplicity, a single codebase (easy to find errors), and single deployments. Monoliths are not the wrong approach, but they are sometimes not desirable. For example:

- Monoliths work well for small applications
- Scaling is problematic (horizontal scaling is often not possible, vertical scaling is expensive, the whole application must be scaled)
- Increasing complexity over time
- Modular monoliths often become tightly coupled
- Difficult to deploy (risky, requires downtime)
- Locked into legacy technology

A distributed monolith — multiple services that share the same database — is not the same as microservices.

#### The Benefits of Microservices

- Small services (can be owned by a single team)
- Easier to understand and rewrite
- Freedom to adopt new technology per service
- Standardize where it makes sense
- Loose coupling allows individual deployment, lower risk, and minimal downtime
- Frequent, independent updates
- Scale services individually and cost-effectively
- Adapt rapidly and easier to reuse

#### The Challenges of Microservices

- **Developer productivity**: How easy can we make it for developers to work on the system?
- **Complex interactions**: Take care to avoid inefficient, chatty communication between microservices
- **Automated deployments**: Manual deployments don't scale across many services
- **Centralized monitoring**: A single place to check logs and monitor for problems is essential

#### Introducing the Demo Application

The course uses an e-commerce application as its reference architecture. The original demo repo (`dotnet-architecture/eShopOnContainers`) has been archived; the updated reference application is available at [dotnet/eShop](https://github.com/dotnet/eShop).

E-commerce is a well-known problem domain. The main focus is on learning microservices concepts.
