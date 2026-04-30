## Building Microservices

#### Hosting Microservices

- **Development**: Developers want to debug the application locally
- **Staging**: Testers want to try out the application in a production-like environment
- **Production**: Host the application for end users

Hosting Options:

1. **Virtual Machines**
   - Traditional approach: one VM per microservice. Can be costly. Placing multiple microservices on one VM introduces operational challenges. Service discovery is another problem to solve.

2. **Platform as a Service (PaaS)**
   - Automatic scale-out
   - DNS address per microservice
   - Built-in load balancing
   - Security and monitoring included
   - Serverless options available

3. **Containers**
   - Portable: run anywhere
   - Easy to run locally
   - Orchestrate with Docker Compose or Kubernetes

#### Running Microservices Locally in Containers

Development Environment Setup:

- Install Docker Desktop
- Clone the reference application source code
- Enable the WSL2-based engine in Docker Desktop (Windows only)
- Configure Windows firewall rules via the supplied PowerShell script (Windows only)

> **Note**: The original `dotnet-architecture/eShopOnContainers` repository has been archived. The updated reference app is at [dotnet/eShop](https://github.com/dotnet/eShop).

Clone the repo:

```bash
git clone https://github.com/dotnet/eShop
```

Build the application:

```bash
docker compose build
```

Run the application:

```bash
docker compose up
```

Navigate to the URL printed by `docker compose up` (typically `http://localhost:<port>`) to access the app. Check the repo README for the current port, as it differs from the original eShopOnContainers (which used port 5100).

> **Note**: `docker-compose` (with hyphen) is the legacy standalone CLI. Docker v2 bundles `docker compose` (no hyphen) as a plugin — prefer the new form.

#### Creating a New Microservice

- Use a **separate source control repository per microservice** to avoid tight coupling between services
- Set up a **continuous integration build** that runs automated tests on every push

#### Testing Microservices

Types of tests:

- **Unit Tests**: Operate at the code level; fast to run. TDD (Test-Driven Development) gives high code coverage on business logic.
- **Service-Level Tests**: Test a single service in isolation using mocked collaborators.
- **End-to-End Tests**: Run in a production-like environment; can be fragile and slow.

#### Microservice Templates

*Consider using a microservice template or exemplar to standardize new services.*

Standardizing microservices across:

- **Logging**: Consistent format, sent to a centralized location
- **Health Checks**: Each microservice exposes a health/status endpoint
- **Configuration**: Standard approach for accessing secrets and config (e.g., environment variables, secret stores)
- **Authentication**: Middleware that sets up a standard security approach
- **Build Script**: Consistent build scripts (Makefile, `docker compose`, etc.)

Benefits of service templates:

- Reduced time to create a new microservice
- Consistent tooling across teams (while still allowing the best tool for the job)
- Increased developer productivity
- Ability to run the microservice in isolation
- Ability to run in the context of the full application — locally (e.g., Docker Compose) or connected to shared services
