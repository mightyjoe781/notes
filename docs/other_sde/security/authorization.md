# Authorization

Authorization determines what authenticated users can access and what actions they can perform. It is the second critical security component after authentication, controlling resource access based on policies, roles, and attributes.

**Key principles:**

- Least privilege: grant only the minimum necessary access
- Defense in depth: multiple layers of access control
- Separation of duties: distribute critical operations across roles
- Need-to-know: access only to required information
- Regular access reviews: periodic permission audits

**Authorization models:**

- **DAC** (Discretionary Access Control): owner controls access
- **MAC** (Mandatory Access Control): system enforces access policies
- **RBAC** (Role-Based Access Control): access based on user roles
- **ABAC** (Attribute-Based Access Control): dynamic access based on attributes

## Role-Based Access Control (RBAC)

RBAC is the industry standard. It assigns permissions to roles rather than individual users, simplifying access management by grouping users with similar needs.

### RBAC Core Components

#### Role

- Reflects a job function or organizational responsibility
- A named collection of related permissions
- Can inherit from parent roles (hierarchical)
- Should have clear separation of concerns

**Common examples:** Admin, Manager, Employee, Guest, Service Account

#### Permissions

**Granularity:**

- Coarse-grained: high-level operations (read, write, delete)
- Fine-grained: specific actions (`update_profile`, `approve_invoice`)
- Resource-specific: permissions tied to particular resources
- Operation-based: what actions a user can perform

**Categories:** data, functional, administrative, API

#### Role Assignment Strategies

- **Direct assignment**: user explicitly assigned to a role
- **Group-based**: users inherit roles through group membership
- **Automatic**: rules-based role assignment
- **Temporary**: time-limited role access

### RBAC Implementation Patterns

Three models:

- **Flat RBAC**: simple structure, no hierarchy
- **Hierarchical RBAC**: child roles inherit parent permissions
- **Constrained RBAC**: conflicting roles cannot be simultaneously assigned or active

#### Flat RBAC

- Simple, direct user-to-role mapping
- Easy to understand and audit
- Becomes unwieldy with many roles
- Best for small organizations or applications with clear job function boundaries

#### Hierarchical RBAC

- Child roles inherit parent permissions
- Reduces redundancy by defining common permissions once
- Mirrors organizational structure

![](assets/Pasted%20image%2020251229192730.png)

#### Constrained RBAC

**Separation of Duties (SoD):**

- **Static SoD**: conflicting roles cannot be assigned to the same user
- **Dynamic SoD**: conflicting roles cannot be active in the same session

**Examples:**

- Finance: separate roles for expense approval and payment processing
- Development: separate roles for code authoring and deployment
- Admin: separate roles for user creation and permission assignment

### RBAC Architecture Patterns

#### Centralized RBAC

A central authorization service acts as the single source of truth:

1. **Policy Decision Point (PDP)**: evaluates access requests
2. **Policy Information Point (PIP)**: provides contextual data
3. **Policy Enforcement Point (PEP)**: enforces decisions
4. **Policy Administration Point (PAP)**: manages policies

**Trade-offs:** consistent policies and centralized auditing, but introduces network latency and a potential single point of failure.

#### Distributed RBAC

- Services cache role and permission data locally
- Authorization decisions are made independently per service
- Reduced latency, but requires synchronization

**Synchronization strategies:**

- Event-driven: push policy changes to services
- Pull-based: periodic synchronization
- Hybrid: critical changes pushed, routine changes pulled

### RBAC Best Practices

**Role design:**

- Align roles to actual business functions
- Grant minimum necessary permissions per role
- Define clear boundaries between roles
- Review roles periodically

**Common mistakes:**

- Role explosion: too many fine-grained roles
- Permission creep: roles accumulating unnecessary permissions
- Overlapping roles: multiple roles with redundant permissions
- Generic roles that don't reflect actual needs

**Permission naming:**

- Use `resource:action` format (`user:read`, `invoice:approve`)
- Group related permissions by namespace
- Use consistent, standardized action names

## Attribute-Based Access Control (ABAC)

ABAC makes authorization decisions based on attributes of users, resources, actions, and environment context, providing fine-grained and dynamic access control.

### ABAC Components

#### Attributes

**Subject (user):** identity, role, clearance level, location, device type

**Resource:** classification (public/internal/confidential/secret), owner, sensitivity

**Action:** operation type (read/write/delete), risk level, audit requirement

**Environment:** time, geographic location, threat level, system state

#### Policies

```
IF (subject.department == "Finance" AND
    resource.classification == "Financial" AND
    action == "read" AND
    environment.time WITHIN business_hours)
THEN PERMIT
ELSE DENY
```

**Policy categories:** access policies, obligation policies (required actions post-grant), advice policies, delegation policies

### ABAC Implementation Patterns

#### XACML (eXtensible Access Control Markup Language)

**Architecture components:**

- **PAP** (Policy Administration Point): creates and manages policies
- **PDP** (Policy Decision Point): evaluates access requests
- **PEP** (Policy Enforcement Point): enforces decisions
- **PIP** (Policy Information Point): provides attribute values

**Request flow:**

1. User attempts resource access
2. PEP intercepts the request
3. PIP gathers relevant attributes
4. PDP evaluates applicable policies
5. Decision returned: PERMIT, DENY, or INDETERMINATE
6. PEP enforces the decision

#### Policy Languages

- **XACML**: XML-based standard
- **Cedar**: Amazon's policy language
- **Rego**: Open Policy Agent's policy language
- **Custom DSLs**: domain-specific policy languages

**Example (Cedar-style):**

```
permit (
    principal in Group::"FinanceTeam",
    action == Action::"ViewReport",
    resource in Folder::"QuarterlyReports"
) when {
    context.time >= time("09:00:00") &&
    context.time <= time("17:00:00") &&
    context.location == "Corporate"
};
```

### ABAC Use Cases

**Dynamic access control:**

- Time-based: different permissions during business hours
- Location-based: geographic restrictions
- Device-based: different permissions per device type
- Risk-based: dynamic permissions based on current risk level

**Example scenarios:**

- Healthcare: doctor access to patient records based on assignment
- Financial services: trading permissions based on market conditions
- Government: clearance-based access to classified information
- Enterprise: project-based access to confidential documents

**Fine-grained control:**

- Document sharing: author can read/write; reviewers can comment only
- API access: rate limiting based on user tier and resource type
- Feature flags: beta features available to specific user segments

## OAuth 2.0 Flow Patterns

OAuth 2.0 is an authorization framework that enables applications to obtain limited access to user accounts by delegating authentication to the account provider.

### OAuth 2.0 Roles

- **Resource Owner**: entity that owns the protected resource (typically the user)
- **Client**: application requesting access (web app, mobile app, SPA)
- **Authorization Server**: authenticates the resource owner and issues tokens (e.g., Google OAuth, Auth0, Okta)
- **Resource Server**: hosts protected resources; validates access tokens

### OAuth 2.0 Grant Types

#### Authorization Code Grant

**Use case:** server-side web applications with a secure backend

![](assets/Pasted%20image%2020251229193437.png)

**Flow:**

1. Client redirects user to the authorization server
2. User authenticates and grants permission
3. Authorization server redirects back with an authorization code
4. Client exchanges the code for an access token (server-to-server)
5. Client uses the access token to access resources

**Security characteristics:**

- Authorization code is never exposed to the user agent
- Client authentication required for token exchange
- PKCE recommended for additional security
- Suitable for confidential clients

#### Implicit Grant

**Use case:** single-page applications (legacy — deprecated)

- Access token returned directly in the URL fragment
- No client authentication possible
- Replaced by Authorization Code + PKCE in OAuth 2.1

#### Client Credentials Grant

**Use case:** machine-to-machine communication

![](assets/Pasted%20image%2020251229193800.png)

**Flow:**

1. Client authenticates with the authorization server
2. Authorization server validates client credentials
3. Authorization server issues an access token
4. Client uses the token to access resources

No user interaction. Client acts on its own behalf (not on behalf of a user — see On-Behalf-Of flow for that). Suitable for backend services and APIs.

#### Resource Owner Password Credentials Grant

**Use case:** highly trusted first-party applications (legacy — deprecated)

![](assets/Pasted%20image%2020251229194023.png)

- User provides credentials directly to the client
- Client forwards credentials to the authorization server
- High risk of credential exposure; deprecated in favor of other flows

### Modern OAuth 2.0 Patterns

#### Authorization Code + PKCE

Reference: https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce

**PKCE (Proof Key for Code Exchange):**

- **Code verifier**: cryptographically random string generated by the client
- **Code challenge**: SHA-256 hash of the code verifier
- **Verification**: authorization server checks that the challenge matches the verifier at token exchange time

Protects against authorization code interception. Mandatory for public clients (mobile apps, SPAs); recommended for all OAuth 2.0 clients; required in OAuth 2.1.

#### Device Authorization Grant

Reference: https://auth0.com/docs/get-started/authentication-and-authorization-flow/device-authorization-flow

**Use case:** input-constrained devices (smart TVs, IoT)

**Flow:**

1. Device requests a device code from the authorization server
2. Authorization server returns a device code and a user code
3. Device displays the user code and verification URL
4. User visits the URL on another device and enters the user code
5. User authenticates and grants permission
6. Device polls for an access token
7. Authorization server issues the token once authorized

### OAuth 2.0 Security Best Practices

**Access token protection:**

- Short expiration (typically ≤ 1 hour)
- Minimal scope (least privilege)
- Always use HTTPS
- Store in HttpOnly cookies or secure storage APIs

**Refresh token security:**

- Longer validity (days to months)
- Rotation: issue a new refresh token on each use
- Bind to specific client instance
- Support immediate revocation

**Confidential clients:**

- Strong client authentication
- Rotate client secrets regularly
- Protect secrets in secure storage

**Public clients:**

- Always use PKCE
- Use dynamic client registration where possible
- Consider app attestation and certificate pinning

### OAuth 2.0 Implementation Patterns

#### API Gateway Integration

- Gateway validates all tokens centrally (introspection or local validation)
- Gateway enforces token scopes and rate limits
- Services are simplified — no token validation logic required
- Centralized access logs and policy management

#### Microservices Authorization

**Token propagation patterns:**

- **Token relay**: forward the original token between services
- **Token exchange**: exchange for a service-specific token (RFC 8693)
- **Service-to-service tokens**: separate tokens for internal communication

**Service mesh integration:**

- Sidecar proxy handles token injection automatically
- mTLS for encrypted service-to-service communication
- Mesh enforces authorization policies

### OAuth 2.0 Extensions

#### OpenID Connect Integration

OIDC adds an authentication layer on top of OAuth 2.0:

- **ID token**: JWT containing user identity information
- **Standard claims**: predefined user attributes
- Additional token validation requirements

#### Token Exchange (RFC 8693)

Use cases:

- Delegation: exchange a user token for a service-specific token
- Token format conversion
- Scope reduction: obtain a token with narrower permissions
- Context modification: add context to an existing token

---

## Authorization Architecture Patterns

### Centralized Authorization

A dedicated authorization service as the single source of truth:

**Components:** policy engine, policy repository, decision cache, audit service

**Benefits:** consistent policies, centralized management, complete audit trail, easier policy updates

**Challenges:** single point of failure, network latency on every authorization check, scalability bottleneck

### Distributed Authorization

**Patterns:**

- Embedded authorization: each service handles its own logic
- Shared libraries: common authorization code across services
- Event-driven policy updates: push changes to all services
- Local caching: cache authorization data per service

**Trade-offs:** faster local decisions and service autonomy, but risk of policy divergence and distributed management complexity.

### Multi-Layer Authorization

**Authorization layers:**

1. Network layer: firewall and network ACLs
2. Gateway layer: API gateway authorization
3. Service layer: service-specific authorization
4. Data layer: database-level access control

Defense in depth: deny by default, redundant controls, audit at every layer.

### Common Authorization Mistakes

- Overprivileged roles with unnecessary permissions
- Missing authorization checks on resources or operations
- Client-side authorization (can be bypassed)
- Hardcoded permissions in application code
- Insufficient auditing and visibility into access patterns
