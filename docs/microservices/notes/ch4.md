## Communicating Between Microservices

#### Microservice Communication Patterns

If microservices communicate directly with each other, you may get tangled dependencies, cascading failures, and poor performance (multiple hops per request).

If you encounter a "too many hops" problem in your architecture, it's likely a sign of a misplaced service boundary.

A better approach: allow microservices to communicate via an **Event Bus** for asynchronous communication. For frontend applications, use an **API Gateway** to interact with microservices. The API Gateway can handle authentication in one place and creates a single controlled entry point for external traffic into internal services.

We could also use the **BFF (Backend for Frontend)** pattern — a dedicated API layer tailored for each type of client (web, mobile, etc.).

#### Synchronous Communication

Making a direct call to a microservice and waiting for a response.

Performance is critical in synchronous communication.

**HTTP** is preferred: it is the industry standard, works across all programming languages, provides standard error codes, and supports caching and proxies. Payloads are typically JSON.

**RESTful APIs** represent information as "resources" and use standard HTTP methods:

- `GET` — retrieve a resource
- `POST` — create a resource
- `PUT` — replace a resource
- `PATCH` — partially update a resource
- `DELETE` — remove a resource

Use appropriate HTTP status codes and `Content-Type` headers.

**gRPC** is an alternative worth considering for internal service-to-service communication — it offers strong typing via Protocol Buffers and better performance than JSON/HTTP for high-throughput scenarios.

#### Asynchronous Communication

Placing an order is a good example: take payment, request additional stock, ship to customer. We can accept the order immediately and let the user track progress asynchronously.

**Asynchronous communication via messaging** is a powerful design pattern. A microservice publishes a message to an Event Bus. The second microservice does not need to be online at the time — messages queue up in the bus. When the second service comes back online, it processes the queued messages.

Another advantage is scaling: if the first service produces many messages, you can scale out the second service independently so multiple instances process the queue in parallel.

Two important message types:

- **Commands**: Directed at a specific microservice (e.g., `PlaceOrder`)
- **Events**: Broadcast to all interested microservices (e.g., `OrderShipped`) — only the concerned services respond

> **Book Recommendation**: *Enterprise Integration Patterns* by Gregor Hohpe & Bobby Woolf

#### Resilient Communication Patterns

In a microservices system:

- **Expect transient errors** — services will be temporarily unavailable
- **Beware of cascading failures** — one slow service can block others
- **Implement retries with exponential back-off** (e.g., using [Polly](https://github.com/App-vNext/Polly) in .NET — or the first-party [`Microsoft.Extensions.Http.Resilience`](https://learn.microsoft.com/en-us/dotnet/core/resilience/) wrapper introduced in .NET 8 — or [resilience4j](https://resilience4j.readme.io/) in Java)
- **Circuit Breaker**: Sits between client and service; after a threshold of failures, it "opens" and fast-fails requests to prevent further overload
- **Caching can improve resilience**: Use cached data as a fallback when a dependency is unavailable
- **Message Brokers** are inherently resilient: they queue messages for offline services, manage re-delivery on failure, and route undeliverable messages to a dead-letter queue

> **Note**: Messages may be received out of order or delivered more than once. Always implement **idempotent message handlers**.

#### Service Discovery

Microservices need addresses to reach each other. Hardcoding IP addresses is not viable — hosts are taken offline for maintenance and updates, and containers are ephemeral.

Use a **Service Registry** to maintain the current addresses of all services. You don't need to build your own:

- **PaaS platforms** (Azure App Service, AWS ECS): built-in DNS per service
- **Kubernetes**: built-in DNS and load balancing for internal traffic via Services and Ingress
- **Service meshes** (e.g., Istio, Linkerd): provide advanced service discovery, load balancing, and observability
