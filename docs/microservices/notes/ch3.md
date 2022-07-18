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