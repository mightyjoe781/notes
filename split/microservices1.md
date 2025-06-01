# Microservices Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: microservices
This is part 1 of 1 parts

---

## File: microservices/index.md

## Microservices

- [Fundamentals Notes](notes/index.md)

---

## File: microservices/notes/ch1.md

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

---

## File: microservices/notes/ch2.md

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

---

## File: microservices/notes/ch3.md

## Building Microservices

 

#### Hosting Microservices

- Development : Developers wants to debug the application locally.
- Staging : Testers want to try out the application in a production like environment.
- Production : We also need to host application for end users.

Hosting Options :

1. Virtual Machines
   - Traditional approach is Virtual Machines with one VM per microservice. But it can be costly and if we try to put more microservices on same VM then there maybe Operation challanges. Service discovery is another problem to deal with in VMs.

2. Platform as a Service

   - Automatic scale-out, DNS address for each microservices

   - Load Balacing builtin

   - Security, Monitoring

   - Serverless

3. Containers

   - Portable : Run anywhere

   - Easily run locally

   - Docker compose

#### Demo : Running Microservices Locally in Containers

Development Environment Setup : 

- Install Docker Desktop
- Clone eShopOnContainers source code
- Enable the WSL2 based engine in Docker Desktop [Optional : Windows]
- Configure Windows firewall rules (using supplied PowerShell script) [Optional : Windows].

Clone the repo : 

```bash
git close https://github.com/dotnet-architecture/eShopOnContainers
```

To build the application execute : `docker-compose build`

To run application : `docker-compose up`

Navigate : `host.docker.internal:5100`

#### Creating a New Microservices

- Source Control repository per microservice because avoids tight coupling between services.
- Continous integration build and run automated tests

#### Testing Microservices

Types of Tests

- Unit Tests : Operate at Code level and Fast to run. TDD : Test Driven Development and High code coverage on buisiness application.
- Service-Level Tests :  Test a single service in isolation and use mocked collaborators.
- End to end Tests : Production like environment and can be fragile.

#### Mircoservices Templates

*Consider using a mircoservice template or exemplar.*

Standardizing Microservices : 

- Logging : Consistent and Sending it to centralized location.
- Health Checks : Each microservice is able to check its health and status
- Configuration : Accessing secrets and configuration
- Authentication : Middleware which sets up standard approach for providing security
- Build Script : Use standard build scripts be it makefile or docker-compose.ymls

Benefits of Service Templates

- Reduced time to create a new microservice
- Consistent Tooling (but still allow for best tool for job)
- Increased developer production
- Ability to run the microservice in isolation

- Run in context of full application - Locally (eg Docker Compose) or Connect to shared services.

---

## File: microservices/notes/ch4.md

## Communicating Between Microservices

#### Microservice Communication Patterns

If microservices communicate directly with each other then there may be some tangled dependencies and casacading failures and poor performance (multiple hops for request).

If there is a hopping problem in your architecture then it might be possible that you may have a misplaced boundry in your architecture.

Better to allow Mircoservices to communicate via Event Bus allows synchronised communications. For frontend application we can use an API gateway to interact with microservices. We could separate and implement Authentication on API gateway and creates a single place for flow of external traffic into internal services.

![image-20220717121541176](ch4.assets/image-20220717121541176.png)

We could also use BFF (Backend for Frontend Approach) to communicate to Microservices.

#### Synchronous Communication

Making a direct call to microservice and waiting for it to return response.

Performance is very important in synchronous communication !

HTTP is preferred : Industry standard, Easily used by any programming language, standard error codes, Caching and proxies. Payload for HTTP service is usually JSON or XML.

RESTful APIs : Represent information as “resources”, Use standard HTTP methods like

- GET to retrieve
- POST to create
- PUT to update

HTTP status codes and Media type headers (Content-Type).

#### Asynchronous Communication

Process of Placing an order can be a good example : Take payment, order additional stock, ship to customer. We can accept the order and let them track the order.

Asynchronous Communication via Messaging can be very useful design. If one microservice communicates with Even Bus and sends out a message to bus. It doesn’t require second microservice to present/online, messages can queue up in bus and when second service comes up online, it can pick up queued messages.

Another advantage is the scaling, say first Service send out a lots of messages then to process the messages effieciently we can scale up the second service and multiple instances can then take up the queued messages.

There are several types of messages, two important of them are 

- Commands : directed to a microservices
- Events : announce to all microservices and only concerned microservices respond.

Books Recommendation : Enterprise Integration Pattern by Gregor Hohpe & Bobby Woolf

#### Resilient Communication Patterns

In microservices

- Expect trasient errors!
- Beware of cascading failures
- Implement retries with back-off (e.g. using Polly in .NET)
- Circuit Breaker (sits in client and server) 
- *Caching can improve resilience* : Fallback mechanism
- Message Brokers are useful and they are resilient, they queue messages for microservices, It can catch up later. They can also manage re-deliveries and dead-letter after mulitple failure.
- NOTE : Messages maybe recieived out of order, or may be recieved multiple times (Have indempotent handlers!).

#### Service Discovery

To microservices requires an address to read the messages. We don’t want to hardcode ip addresses because microservices and vms can be taken ofline time to time for maintenance and update.

We use **Service Registry** to maintain the address of all the VMs, and you don’t need to create your own service registry, you could use a DNS if you have PaaS (Platform as a Service) or you use Container orchestration (Kubernetes have built in DNS which handles/load balancing handlers for managing internal traffic).

---

## File: microservices/notes/ch5.md

## Securing Microservices

Not all data is sensitive. For eg Catalog Service is not sensitive while Ordering Service is highly sensitive data and requires encryption.

#### Encrypting Data

Encryption should be present in transit. Use standard algorithms and never try to write your own encrytion schemes. For HTTP we use Transport Layer Security and SSL certificates. We usually need to manage Certificates, which could be done by Cloud Service provider or we can use LEGO tool for certificates.

 Also data needs to Encrypted at rest. Disk Encryption requires a proper key management and requires encrypted backups.

#### Authentication

*We need to know who is calling our service.*

with HTTP we have many options, auth header can have main option is 

- Basic Authentication (username & password) : Only issue is Requires all microservices requires password storage.
- API Key : key/client and requires client management
- Client certificate : public-key cryptography but require very complex management.

Better Approach is use an Identity Server and use industry standard protocols:  OAuth 2.0 & OpenID Connect.

Recommendation : Getting Started with OAuth2.0 (Scott Brady).

Once identity server verifies client auth info, it provides access token (Short lived) to client. Then every request from client to microservice will contain this token and makes life easy for microservices by not making them manage authentication.

#### Authorization

*If authenticated then limit what they can do, role based management.*

Authorization Frameworks : 

- Makes decisions based on “roles”
- consider carefully what callers should be allowed to do

![image-20220717194653437](ch5.assets/image-20220717194653437.png)

Role based authentication systems helps fight the problem of confused deputy.

#### Securing the Network

Always put all microservices inside a virtual network and don’t allow others access them. Implement an API Gateway that accepts requests from public network and passes on incoming request to Microservices.

This allows us to have single point of entry and configured with Firewall and guarded with DDOS defense.

![image-20220717195103400](ch5.assets/image-20220717195103400.png)

#### Defense in Depth

*Avoid relying on single layer of security.*

- Encryption in transit
- Access tokens
- Virtual Networks and whitelists for network security.

Apply multiple layers of protection to remove the possibility of breach.

Additional Defensive Measures : 

- Penetration testing : performed by infosec experts and get their advice.
- Automated security testing : prove APIs reject unauthorized callers
- Attack detection : port scanning, sql-injection detects and react quickly when you are under attack.
- Auditing : know exactly who did what and when.



---

## File: microservices/notes/ch6.md

## Delivering Microservices

#### Automated Deployments

In monoliths usually deployment is manual process, but microservices are deployed frequently and there are bunch of them, so manual process is not feasible.

Microservices requires Automated Deployments : 

- Reliable and repeatable 
- frequent deployments
- Continous Integration
- Release Pipelines : Build -> Unit Tests -> Deploy Microservices -> Service Tests -> Deploy to QA -> End-to-end test -> Release gate -> Deploy to Production

#### Deployment Environments

Development : Debug Code

QA : End-to end test, manual testing, Pen testing, Performance testing

Production : per-customer, per-region

It is helpful to parameterize your deployments. Common way is json/yaml config files which explain whats different about environments.

Cloud Infrastructure Deployment, Terraform or Azure ARM Templates.

Base template + environment-specific override

#### Artifact Registries

- Store Build artificats
- Deploy latest or previous version
- Docker Container Images
- Deploy to Kubernetes : (yaml config files, desired state)

#### Independent Upgrades

*Upgrading one microservice should not require microservices to be upgraded.*

Upgrade Strategies : 

- Stop v1, start v2 : short period of unavailability 
- blue-green swap : run v1 & v2 simultaneously and swap traffic from v1 to v2 using load balancer (minimal downtime).
- rolling upgrade : there are several v1 instances running, removing one by one v1 instances and replacting with v2 (kubernetes is useful).

#### Monitoring Microservices

What should we monitor ?

Host Metrices 

- CPU percentages
- Memory Usage
- Configure alerts

Application Metrices

- HTTP requests
- Errors (401, 500)
- Queue Length (scale out or DDOS)
- Dead-letter queue
- Health checks

Logs

- Aggregated
- Standardize log output 
- Kibana
- Application Insights

*Take advantage of builtin monitoring and observability capabilities of your microservices hosting platform.*

### Recommended Reading : ORILEY’s Building Microservices by Sam Newman

---

## File: microservices/notes/index.md

## Microservices

### Content

1. [Introduction to Microservices](ch1.md)
2. [Architecting Microservices](ch2.md)
3. [Building Microservices](ch3.md)
4. [Communicating Between Microservices](ch4.md)
5. [Securing Microservices](ch5.md)
6. [Delivering Microservices](ch6.md)

---

