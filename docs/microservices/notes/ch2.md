## Architecting Microservices

#### Evolving Towards Microservices

Augment a monolith

- Add new microservices

Decompose a monolith

- Extract Microservices

You don’t need to get started with microservices, Its hard to get service boundaries right. Its better to let it evolve a little bit before switching to microservices.

Definig Microservice responsibilities

- Public Interface

#### Microservices Own Their Own Data

Microservices are independently deployable which ultimately requires them to own their own data. All microservices should not share data from a single pool, instead each of microservices have their own data store.

If a microservices wants to access data store of another microservice, it needs to interact with the public API of that microservice that owns data.

Some limitation comes with this issues.

- Database Joins are no longer possible
- Single Transactions are not possible and distributed transaction are very complex.
- Eventual Consistency : All transaction and database will come to consistent state eventually if service boundries are defined carefully.

Mitigating Data Ownership Limitation.

- Define service boundaries well, Minimize need to aggregate data
- Caching : improved performance and availability, no need to communicate again and again with other microservices

#### EShopOnContainers Architecture

![img](https://github.com/dotnet-architecture/eShopOnContainers/raw/dev/img/eShopOnContainers-architecture.png)

Notice how Catalog and ordering microservices are mysql database but it doesn’t need to share resources. Basket Microservice uses Redis cache.

Two microservices eventually have issues of duplicating data. Direct database join between two microservices is might not be a problem as it seemed to be. Consider ordering and catalog microservices. It may seem ordering and catalog may have duplication of products and prices, but in actually in reality we only care about the time we ordered something is different from what catalog shows. So data is in reality consistent and we use denormalization to reach consistent states after an order goes through.

#### Components of a Microservice

Microservices is not a single service running on simple one host. If we scale out then there are multiple replica’s of microservices running on multiple hosts. A microservices may have scheduler that requires to perform some kind of data maintenance. 

So in reality a single microservices has many components and together they form a closed microservice in which component can communicate to each other only if they belong to same microservice.

Microservices should have a clear defined public interface and its data can only be accessed thorugh that public interface.\

#### Microservices are Independently Deployable

*Miroservices can be upgraded without their clients need to upgrade.*

This requires care and never push breaking changes to public interface. To achieve this we use Microservices Contracts like :

- Make additive changes : New endpoints and properties on DTOs
- Introduce version 2 API : Version 1 client must still be supported
- Easily forgotten in development. (Upgrade both at same time).

Avoiding Upgrade Issues

- Team ownership of microservices (Add new feature, then deploy updated microservices, update clients then)
- Create automated tests (Ensure older clients are supported, run as part of a CI build process).
- Beware of shared Codebase, results in tightly coupled client and services.

#### Identifying Microservices Boundries

Getting it wrong can be costly : Poor performance, Hard to change

Start from existing monolith system :

- Identify loosely coupled components
- Identify database seams

A helpful guideline is : *Organize microservices around business capabilities*.

Domain Driven design (Courses by Vladimir are quire good) can be utilised here :

- Identify “bounded contexts”
- Break up large domains
- Microservices do not share models
- “Ubiquitous language”
- Sketch on paper to get more idea about potential problems

Pitfalls in Microservice Boundaries : 

- Don’t turn every noun into a microservices
- Anemic CRUD microservices
- Thin wrappers around databases
- Logic distributed Everywhere
- **Avoid circular dependency**
- Avoid chatty communication (too much communication among microservices, takes a toll on performance and can be costly).

#### EShopOnContainers Service Boundries

There are 3 microservices : Catalog, Basket and Ordering microservices.

These are 3 distinct parts of shopping experience. It helps in resilience, scalability. Catalog is very large datasets and focus on flexible querying (MySQL). Basked service is short-lived data and redis cache is good. Ordering reqruires to always required to write new data and its very vital and highly sensitive data. Identify requires Authentication database.