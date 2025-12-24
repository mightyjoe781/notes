# Authorization Patterns

*Comprehensive guide to authorization mechanisms and access control patterns for secure system design.*

## Overview

Authorization determines what authenticated users can access and what actions they can perform. It's the second critical component of security after authentication, controlling resource access based on policies, roles, and attributes.

### Authorization vs Authentication

- **Authentication**: Establishes identity ("Who are you?")
- **Authorization**: Controls access ("What can you do?")
- **Access Control**: Enforcement mechanism for authorization decisions

### Key Authorization Principles

- **Principle of least privilege**: Grant minimum necessary access
- **Defense in depth**: Multiple layers of access control
- **Separation of duties**: Distribute critical operations across multiple roles
- **Need-to-know basis**: Access only to required information
- **Regular access reviews**: Periodic permission audits

### Authorization Models Overview

- **Discretionary Access Control (DAC)**: Owner controls access
- **Mandatory Access Control (MAC)**: System enforces access policies
- **Role-Based Access Control (RBAC)**: Access based on user roles
- **Attribute-Based Access Control (ABAC)**: Dynamic access based on attributes

------

## Role-Based Access Control (RBAC)

### RBAC Fundamentals

RBAC assigns permissions to roles rather than individual users, simplifying access management by grouping users with similar access needs into roles.

### RBAC Core Components

#### Roles

**Role Definition:**

- **Job function**: Roles reflect organizational responsibilities
- **Permission sets**: Collections of related permissions
- **Hierarchical structure**: Roles can inherit from other roles
- **Separation of concerns**: Distinct roles for different functions

**Common Role Examples:**

- **Admin**: Full system access and configuration
- **Manager**: Department-level access and user management
- **Employee**: Standard user access to assigned resources
- **Guest**: Limited read-only access to public resources
- **Service Account**: Automated system access

#### Permissions

**Permission Granularity:**

- **Coarse-grained**: High-level operations (read, write, delete)
- **Fine-grained**: Specific actions (update_profile, approve_invoice)
- **Resource-specific**: Permissions tied to specific resources
- **Operation-based**: Actions users can perform

**Permission Categories:**

- **Data permissions**: Access to specific data types
- **Functional permissions**: Access to application features
- **Administrative permissions**: System configuration and management
- **API permissions**: Access to specific endpoints or services

#### Role Assignments

**Assignment Strategies:**

- **Direct assignment**: User directly assigned to role
- **Group-based assignment**: Users inherit roles through group membership
- **Automatic assignment**: Rules-based role assignment
- **Temporary assignment**: Time-limited role access

### RBAC Implementation Patterns

#### Flat RBAC Model

**Characteristics:**

- **Simple role structure**: No role hierarchy
- **Direct user-role assignment**: Straightforward mapping
- **Easy to understand**: Clear permission boundaries
- **Limited scalability**: Can become complex with many roles

**Use Cases:**

- Small organizations
- Simple applications
- Clear job function boundaries
- Limited permission requirements

#### Hierarchical RBAC Model

**Role Hierarchy Benefits:**

- **Permission inheritance**: Child roles inherit parent permissions
- **Reduced redundancy**: Common permissions defined once
- **Organizational alignment**: Reflects company structure
- **Simplified management**: Easier role maintenance

**Hierarchy Example:**

```
CEO
├── VP Engineering
│   ├── Engineering Manager
│   │   ├── Senior Engineer
│   │   └── Junior Engineer
│   └── DevOps Manager
│       ├── Senior DevOps
│       └── DevOps Engineer
└── VP Sales
    ├── Sales Manager
    │   ├── Senior Sales Rep
    │   └── Sales Rep
    └── Sales Support
```

#### Constrained RBAC Model

**Separation of Duties (SoD):**

- **Static SoD**: Conflicting roles cannot be assigned to same user
- **Dynamic SoD**: Conflicting roles cannot be active simultaneously
- **Conflict resolution**: Policies for handling role conflicts

**Constraint Examples:**

- **Financial controls**: Separate roles for expense approval and payment
- **Development controls**: Separate roles for code development and deployment
- **Administrative controls**: Separate roles for user creation and permission assignment

### RBAC Architecture Patterns

#### Centralized RBAC

**Central Authorization Service:**

- **Single source of truth**: All authorization decisions centralized
- **Consistent policies**: Uniform access control across systems
- **Simplified auditing**: Central logging and monitoring
- **Performance considerations**: Network latency for authorization calls

**Implementation Approach:**

1. **Policy Decision Point (PDP)**: Evaluates access requests
2. **Policy Information Point (PIP)**: Provides contextual information
3. **Policy Enforcement Point (PEP)**: Enforces authorization decisions
4. **Policy Administration Point (PAP)**: Manages policies and rules

#### Distributed RBAC

**Distributed Authorization:**

- **Local caching**: Cache role and permission data locally
- **Eventual consistency**: Accept temporary inconsistencies
- **Service autonomy**: Services make independent authorization decisions
- **Reduced latency**: No network calls for authorization

**Synchronization Strategies:**

- **Event-driven updates**: Push changes to distributed services
- **Pull-based refresh**: Periodic synchronization
- **Hybrid approach**: Critical changes pushed, routine changes pulled

### RBAC Best Practices

#### Role Design Guidelines

**Effective Role Modeling:**

- **Business alignment**: Roles reflect actual job functions
- **Minimal privilege**: Each role has minimum necessary permissions
- **Clear boundaries**: Distinct responsibilities between roles
- **Regular review**: Periodic assessment of role relevance

**Common Role Design Mistakes:**

- **Role explosion**: Too many fine-grained roles
- **Permission creep**: Roles accumulate unnecessary permissions
- **Overlapping roles**: Multiple roles with similar permissions
- **Generic roles**: Roles that don't reflect actual needs

#### Permission Management

**Permission Lifecycle:**

- **Creation**: Define new permissions as features develop
- **Assignment**: Associate permissions with appropriate roles
- **Review**: Regular assessment of permission necessity
- **Retirement**: Remove obsolete permissions

**Permission Naming Conventions:**

- **Resource-action format**: `user:read`, `invoice:approve`
- **Namespace organization**: Group related permissions
- **Consistent terminology**: Standardized action names
- **Hierarchical structure**: Support permission inheritance

------

## Attribute-Based Access Control (ABAC)

### ABAC Fundamentals

ABAC makes authorization decisions based on attributes of users, resources, actions, and environment context, providing fine-grained and dynamic access control.

### ABAC Components

#### Attributes

**Subject Attributes (User):**

- **Identity attributes**: User ID, email, department
- **Role attributes**: Current roles and responsibilities
- **Clearance attributes**: Security clearance level
- **Contextual attributes**: Current location, device type

**Resource Attributes:**

- **Classification**: Public, internal, confidential, secret
- **Owner**: Resource creator or responsible party
- **Creation date**: When resource was created
- **Sensitivity**: Data sensitivity level

**Action Attributes:**

- **Operation type**: Read, write, update, delete
- **Risk level**: Low, medium, high risk operations
- **Audit requirement**: Operations requiring audit trails

**Environment Attributes:**

- **Time**: Current time, business hours
- **Location**: Geographic location, network zone
- **Risk context**: Current threat level
- **System state**: Maintenance mode, emergency status

#### Policies

**Policy Structure:**

```
IF (subject.department == "Finance" AND 
    resource.classification == "Financial" AND 
    action == "read" AND 
    environment.time WITHIN business_hours)
THEN PERMIT
ELSE DENY
```

**Policy Categories:**

- **Access policies**: Basic resource access rules
- **Obligation policies**: Required actions after access granted
- **Advice policies**: Recommendations for access decisions
- **Delegation policies**: Rules for delegating permissions

### ABAC Implementation Patterns

#### XACML (eXtensible Access Control Markup Language)

**XACML Architecture:**

- **Policy Administration Point (PAP)**: Creates and manages policies
- **Policy Decision Point (PDP)**: Evaluates access requests
- **Policy Enforcement Point (PEP)**: Enforces decisions
- **Policy Information Point (PIP)**: Provides attribute values

**XACML Request Flow:**

1. **Access request**: User attempts resource access
2. **PEP intercepts**: Enforcement point captures request
3. **Attribute gathering**: PIP provides relevant attributes
4. **Policy evaluation**: PDP evaluates applicable policies
5. **Decision response**: PERMIT, DENY, or INDETERMINATE
6. **Enforcement**: PEP enforces the decision

#### Policy Languages

**Common Policy Languages:**

- **XACML**: XML-based standard policy language
- **Cedar**: Amazon's policy language for authorization
- **Rego**: Open Policy Agent's policy language
- **Custom DSLs**: Domain-specific policy languages

**Policy Example (Cedar-style):**

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

### ABAC vs RBAC Comparison

| Aspect                  | RBAC                        | ABAC                          |
| ----------------------- | --------------------------- | ----------------------------- |
| **Complexity**          | Simple to moderate          | High complexity               |
| **Flexibility**         | Limited by predefined roles | Highly flexible               |
| **Performance**         | Fast role-based lookups     | Slower policy evaluation      |
| **Management**          | Easier role management      | Complex policy management     |
| **Scalability**         | Role explosion issues       | Scales with policy complexity |
| **Context awareness**   | Limited context             | Rich contextual decisions     |
| **Implementation cost** | Lower                       | Higher                        |

### ABAC Use Cases

#### Dynamic Access Control

**Contextual Authorization:**

- **Time-based access**: Different permissions during business hours
- **Location-based access**: Access restrictions based on geographic location
- **Device-based access**: Different permissions for different device types
- **Risk-based access**: Dynamic permissions based on risk assessment

**Example Scenarios:**

- **Healthcare**: Doctor access to patient records based on assignment
- **Financial services**: Trading permissions based on market conditions
- **Government**: Clearance-based access to classified information
- **Enterprise**: Project-based access to confidential documents

#### Fine-Grained Permissions

**Granular Control Examples:**

- **Document sharing**: Author can read/write, reviewers can comment only
- **Database access**: Different query permissions based on data sensitivity
- **API access**: Rate limiting based on user tier and resource type
- **Feature access**: Beta features available to specific user segments

------

## OAuth 2.0 Flow Patterns

### OAuth 2.0 Fundamentals

OAuth 2.0 is an authorization framework that enables applications to obtain limited access to user accounts by delegating authentication to the account provider.

### OAuth 2.0 Roles

#### Core Roles

**Resource Owner:**

- **Definition**: Entity that owns the protected resource (typically the user)
- **Capabilities**: Can grant access to protected resources
- **Examples**: End users, system accounts

**Client:**

- **Definition**: Application requesting access to protected resources
- **Types**: Confidential clients, public clients
- **Examples**: Web applications, mobile apps, SPA applications

**Authorization Server:**

- **Definition**: Server that authenticates the resource owner and issues access tokens
- **Responsibilities**: Token issuance, refresh, and revocation
- **Examples**: Google OAuth, Auth0, Okta

**Resource Server:**

- **Definition**: Server hosting protected resources
- **Capabilities**: Accepts and validates access tokens
- **Examples**: API servers, microservices

### OAuth 2.0 Grant Types

#### Authorization Code Grant

**Use Case:** Server-side web applications with secure backend

**Flow Steps:**

1. **Client redirects user** to authorization server
2. **User authenticates** and grants permission
3. **Authorization server redirects back** with authorization code
4. **Client exchanges code** for access token (backend)
5. **Client uses access token** to access resources

**Security Characteristics:**

- **Authorization code** never exposed to user agent
- **Client authentication** required for token exchange
- **PKCE extension** recommended for additional security
- **Suitable for** confidential clients

#### Implicit Grant

**Use Case:** Single-page applications (legacy pattern)

**Flow Steps:**

1. **Client redirects user** to authorization server
2. **User authenticates** and grants permission
3. **Authorization server redirects back** with access token in URL fragment
4. **Client extracts token** from URL fragment
5. **Client uses access token** to access resources

**Security Considerations:**

- **Access token exposed** in URL fragment
- **No client authentication** possible
- **Deprecated** in OAuth 2.1
- **Replaced by** Authorization Code + PKCE

#### Client Credentials Grant

**Use Case:** Machine-to-machine communication

**Flow Steps:**

1. **Client authenticates** with authorization server
2. **Authorization server validates** client credentials
3. **Authorization server issues** access token
4. **Client uses access token** to access resources

**Characteristics:**

- **No user interaction** required
- **Client acts on own behalf** not on behalf of user
- **Suitable for** backend services, APIs
- **Requires** client authentication

#### Resource Owner Password Credentials Grant

**Use Case:** Highly trusted applications (legacy pattern)

**Flow Steps:**

1. **User provides credentials** directly to client
2. **Client forwards credentials** to authorization server
3. **Authorization server validates** and issues access token
4. **Client uses access token** to access resources

**Security Concerns:**

- **Client handles user credentials** directly
- **Risk of credential exposure**
- **Deprecated** in favor of other flows
- **Only for** highly trusted applications

### Modern OAuth 2.0 Patterns

#### Authorization Code + PKCE

**PKCE (Proof Key for Code Exchange):**

- **Code verifier**: Cryptographically random string
- **Code challenge**: SHA256 hash of code verifier
- **Challenge method**: S256 or plain
- **Verification**: Authorization server verifies challenge matches verifier

**Enhanced Security:**

- **Protection against** code interception attacks
- **Suitable for** public clients (mobile apps, SPAs)
- **Recommended for** all OAuth 2.0 clients
- **Required in** OAuth 2.1

#### Device Authorization Grant

**Use Case:** Input-constrained devices (smart TVs, IoT devices)

**Flow Steps:**

1. **Device requests** device code from authorization server
2. **Authorization server returns** device code and user code
3. **Device displays** user code and verification URL
4. **User visits URL** on another device and enters user code
5. **User authenticates** and grants permission
6. **Device polls** for access token
7. **Authorization server issues** access token when authorized

### OAuth 2.0 Security Best Practices

#### Token Security

**Access Token Protection:**

- **Short expiration times**: Typically 1 hour or less
- **Minimal scope**: Principle of least privilege
- **Secure transmission**: Always use HTTPS
- **Secure storage**: HttpOnly cookies or secure storage APIs

**Refresh Token Security:**

- **Longer validity**: Days to months
- **Rotation**: Issue new refresh token with each use
- **Binding**: Tie to specific client instance
- **Revocation**: Immediate invalidation capability

#### Client Security

**Confidential Client Security:**

- **Client authentication**: Strong client credentials
- **Secret rotation**: Regular client secret updates
- **Secure storage**: Protect client secrets
- **Certificate-based authentication**: Enhanced security

**Public Client Security:**

- **PKCE mandatory**: Always use PKCE for public clients
- **Dynamic client registration**: Avoid hardcoded credentials
- **App attestation**: Verify app integrity
- **Certificate pinning**: Prevent man-in-the-middle attacks

### OAuth 2.0 Implementation Patterns

#### API Gateway Integration

**Gateway-based Authorization:**

- **Centralized token validation**: Gateway validates all tokens
- **Token introspection**: Real-time token validation
- **Scope enforcement**: Gateway enforces token scopes
- **Rate limiting**: Per-token rate limiting

**Benefits:**

- **Simplified services**: Services don't handle token validation
- **Consistent enforcement**: Uniform authorization across APIs
- **Centralized logging**: Single point for access logs
- **Policy management**: Central authorization policies

#### Microservices Authorization

**Token Propagation Patterns:**

- **Token relay**: Forward original token between services
- **Token exchange**: Exchange tokens for service-specific tokens
- **Service-to-service tokens**: Separate tokens for internal communication

**Service Mesh Integration:**

- **Automatic token injection**: Sidecar proxy handles tokens
- **mTLS for service communication**: Encrypted service-to-service communication
- **Policy enforcement**: Mesh enforces authorization policies

### OAuth 2.0 Extensions

#### OpenID Connect Integration

**ID Token Addition:**

- **Authentication layer**: Built on top of OAuth 2.0
- **User identity**: ID token contains user information
- **Standard claims**: Predefined user attributes
- **Token validation**: Additional validation requirements

#### Token Exchange (RFC 8693)

**Token Exchange Use Cases:**

- **Service delegation**: Exchange user token for service token
- **Token adaptation**: Convert between token formats
- **Scope reduction**: Obtain tokens with reduced scope
- **Context modification**: Add context to existing tokens

------

## Authorization Architecture Patterns

### Centralized Authorization

#### Authorization Service Architecture

**Components:**

- **Policy engine**: Evaluates authorization policies
- **Policy repository**: Stores authorization rules
- **Decision cache**: Caches frequent authorization decisions
- **Audit service**: Logs authorization events

**Benefits:**

- **Consistent policies**: Single source of truth for authorization
- **Centralized management**: Easier policy administration
- **Audit trail**: Complete authorization logging
- **Policy evolution**: Easier to update authorization logic

**Challenges:**

- **Single point of failure**: Authorization service availability critical
- **Performance impact**: Network latency for authorization calls
- **Scalability concerns**: All services depend on authorization service

### Distributed Authorization

#### Service-Level Authorization

**Patterns:**

- **Embedded authorization**: Each service handles its own authorization
- **Shared libraries**: Common authorization logic across services
- **Event-driven updates**: Push policy changes to services
- **Local caching**: Cache authorization data locally

**Trade-offs:**

- **Performance**: Faster local authorization decisions
- **Autonomy**: Services independently manage authorization
- **Consistency**: Potential for policy divergence
- **Complexity**: Distributed policy management

### Hybrid Authorization Patterns

#### Multi-Layer Authorization

**Authorization Layers:**

1. **Network layer**: Firewall and network access control
2. **Gateway layer**: API gateway authorization
3. **Service layer**: Service-specific authorization
4. **Data layer**: Database-level access control

**Defense in Depth:**

- **Multiple checkpoints**: Authorization at multiple layers
- **Fail-safe defaults**: Deny access by default
- **Redundant controls**: Backup authorization mechanisms
- **Audit everywhere**: Comprehensive authorization logging

------

## Key Takeaways

1. **Choose the right model**: RBAC for role-based organizations, ABAC for dynamic contexts
2. **Start simple**: Begin with RBAC and evolve to ABAC if needed
3. **Principle of least privilege**: Grant minimal necessary access
4. **Regular access reviews**: Periodically audit and update permissions
5. **Defense in depth**: Implement authorization at multiple layers
6. **Monitor and audit**: Track all authorization decisions and changes
7. **Plan for scale**: Design authorization systems for distributed architectures

### Common Authorization Mistakes

- **Overprivileged roles**: Roles with unnecessary permissions
- **Missing authorization checks**: Unprotected resources or operations
- **Client-side authorization**: Relying on client-side access control
- **Hardcoded permissions**: Authorization logic embedded in code
- **Insufficient auditing**: Poor visibility into access patterns

> **Remember**: Authorization is about controlling what authenticated users can do. Design authorization systems that match your organizational structure and security requirements while maintaining good performance and user experience.