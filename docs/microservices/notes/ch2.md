## Architecting Microservices

#### Evolving Towards Microservices

Augment a monolith:

- Add new microservices alongside the existing system

Decompose a monolith:

- Extract microservices incrementally

You don't need to start with microservices. It's hard to get service boundaries right. It's better to let the domain evolve a little before switching to microservices.

Defining microservice responsibilities:

- Public Interface

#### Microservices Own Their Own Data

Microservices are independently deployable, which requires them to own their own data. Microservices should not share data from a single pool; each microservice has its own data store.

If a microservice needs data from another microservice, it must interact through that service's public API.

Some limitations come with this approach:

- Database joins are no longer possible
- Single transactions are not possible; distributed transactions are very complex
- **Eventual consistency**: All data will converge to a consistent state eventually, provided service boundaries are defined carefully

Mitigating data ownership limitations:

- Define service boundaries well to minimize the need to aggregate data across services
- **Caching**: Improves performance and availability; reduces repeated inter-service calls

#### eShopOnContainers Architecture

The reference architecture uses separate data stores per microservice. The Catalog and Ordering microservices use a relational database (MySQL/SQL Server) independently — they do not share resources. The Basket microservice uses Redis cache.

On apparent data duplication: consider the Ordering and Catalog microservices. It may seem that both duplicate product and price data, but in practice we only care about the price at the time an order was placed — not the current catalog price. This is intentional denormalization for consistency.

> **Note**: The original `dotnet-architecture/eShopOnContainers` repository has been archived. The updated reference app is at [dotnet/eShop](https://github.com/dotnet/eShop).

#### Components of a Microservice

A microservice is not a single service running on one host. When scaled out, there are multiple replicas running across multiple hosts. A microservice may also include a scheduler for background data maintenance tasks.

In practice, a single microservice has many internal components. These components communicate freely with each other, but the microservice as a whole exposes only a well-defined public interface. Its data can only be accessed through that public interface.

#### Microservices are Independently Deployable

*Microservices can be upgraded without requiring their clients to upgrade.*

This requires care — never push breaking changes to a public interface. To achieve this, follow microservice contract conventions:

- **Make additive changes**: New endpoints, new optional properties on DTOs
- **Introduce a v2 API**: v1 clients must still be supported during the transition
- Don't fall into the trap of upgrading both client and service simultaneously in development

Avoiding upgrade issues:

- Team ownership of microservices (add the new feature, deploy the updated service, then update clients)
- Create automated contract tests (ensure older clients are still supported; run as part of CI)
- Beware of shared codebases — they result in tightly coupled clients and services

#### Identifying Microservice Boundaries

Getting boundaries wrong is costly: poor performance, hard to change.

Starting from an existing monolith:

- Identify loosely coupled components
- Identify database seams

A helpful guideline: *Organize microservices around business capabilities*.

Domain-Driven Design (DDD) can be applied here:

- Identify "bounded contexts"
- Break up large domains
- Microservices do not share models
- Use a "ubiquitous language" within each service
- Sketch on paper to discover potential boundary issues early

Pitfalls in microservice boundaries:

- Don't turn every noun into a microservice
- Avoid anemic CRUD microservices — thin wrappers around a database with no logic
- Avoid logic distributed everywhere across many tiny services
- **Avoid circular dependencies**
- Avoid chatty communication (excessive inter-service calls hurt performance and increase costs)

#### eShopOnContainers Service Boundaries

There are three core microservices: Catalog, Basket, and Ordering.

These represent three distinct parts of the shopping experience, each with different data characteristics:

- **Catalog**: Large dataset, optimized for flexible querying (relational DB)
- **Basket**: Short-lived session data, well-suited for Redis cache
- **Ordering**: Write-heavy, highly sensitive financial data requiring durability
- **Identity**: Authentication and user management database
