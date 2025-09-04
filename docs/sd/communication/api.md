# API Design Patterns

### REST (Representation State Transfer)

**Core Principles:**

- Stateless communication
- Resource-based URLs
- Standard HTTP methods (GET, POST, PUT, DELETE)
- JSON/XML data format
- Cacheable responses

**Advantages:**

- Simple and widely understood
- Excellent caching support (HTTP caching)
- Great tooling and debugging support
- Platform and language agnostic
- Mature ecosystem

**Disadvantages:**

- Over-fetching and under-fetching data
- Multiple round trips for related data
- Versioning challenges
- No built-in real-time support

**Best Use Cases:**

- Public APIs
- CRUD operations
- Web services with simple data requirements
- When caching is critical

````python
# REST API Example
# GET /api/users/123
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "posts": [
    {"id": 1, "title": "Hello World"},
    {"id": 2, "title": "API Design"}
  ]
}
````

### GraphQL

**Core Principles:**

- Single endpoint
- Query language for APIs
- Client specifies exactly what data it needs
- Strong type system
- Introspection capabilities

**Advantages:**

- Eliminates over-fetching and under-fetching
- Single request for complex data
- Strong typing and schema validation
- Excellent developer experience
- Real-time subscriptions

**Disadvantages:**

- Complex caching (no HTTP caching)
- Query complexity analysis needed
- Steeper learning curve
- Potential for expensive queries

**Best Use Cases:**

- Mobile applications (bandwidth optimization)
- Complex data relationships
- Rapid frontend development
- When you need flexible data fetching

````python
# GraphQL Query Example
query {
  user(id: 123) {
    name
    email
    posts(limit: 5) {
      title
      createdAt
    }
  }
}
````

### gRPC (Google Remote Procedure Call)

**Core Principles:**

- Protocol Buffers (protobuf) for serialization
- HTTP/2 transport
- Strongly typed contracts
- Code generation from schema
- Streaming support

**Advantages:**

- High performance and efficiency
- Strong typing and code generation
- Bidirectional streaming
- Multiple language support
- Compact binary format

**Disadvantages:**

- Limited browser support
- Binary format (not human-readable)
- Steeper learning curve
- Less tooling compared to REST

**Best Use Cases:**

- Microservices communication
- High-performance applications
- Real-time streaming
- Internal APIs where performance matters

````python
// Protocol Buffer Definition
service UserService {
  rpc GetUser(UserRequest) returns (UserResponse);
  rpc StreamUsers(Empty) returns (stream UserResponse);
}

message UserRequest {
  int32 user_id = 1;
}

message UserResponse {
  int32 id = 1;
  string name = 2;
  string email = 3;
}
````

| **Feature**         | **REST**  | **GraphQL**   | **gRPC**  |
| ------------------- | --------- | ------------- | --------- |
| **Performance**     | Good      | Good          | Excellent |
| **Caching**         | Excellent | Complex       | Limited   |
| **Learning Curve**  | Easy      | Medium        | Hard      |
| **Browser Support** | Excellent | Excellent     | Limited   |
| **Real-time**       | WebSocket | Subscriptions | Streaming |
| **Tooling**         | Mature    | Growing       | Limited   |

## API Versioning

### URL Path Versioning

* Most common and straightforward approach

````python
# Examples
GET /api/v1/users
GET /api/v2/users
GET /api/v3/users
````

**Advantages:**

- Clear and explicit
- Easy to implement
- Good for major changes

**Disadvantages**: URL pollution, Multiple endpoints to maintain

### Header Versioning

Version is specified in Headers

````python
# Request Header
GET /api/users
Accept: application/vnd.api+json;version=1

# Or custom header
API-Version: 2.0
````

**Advantages:**

- Clean URLs
- Content negotiation support
- Flexible versioning

**Disadvantages**: Less visible, Harder to test manually

### Query Parameter Versioning

* Version passed as query parameter

````python
GET /api/users?version=1.0
GET /api/users?v=2
````

**Advantages:**

- Simple implementation
- Easy to test
- Optional parameter support

Disadvantages: Can be ignored easily, Mixed with other parameters

### Content Type Versioining

Version embedded in content type.

```http
# Request
Accept: application/vnd.company.app-v2+json

# Response
Content-Type: application/vnd.company.app-v2+json
```

**Advantages:**

- RESTful approach
- Follows HTTP standards
- Content negotiation

Disadvantages: Complex to implement, Limited tooling support

### Versioning Best Practices

1. Semantic Versioning: Use MAJOR.MINOR.PATCH format
2. Backward Compatibility: Maintain older versions for transition period
3. Deprecation Strategy: Clearly communicate timeline for version sunset
4. Documentation: Maintain clear changelog and migration guides

```python
# Deprecation Header Example
GET /api/v1/users
Response Headers:
Warning: 299 - "Deprecated API Version. Migrate to v2 by 2024-12-31"
Sunset: Wed, 31 Dec 2024 23:59:59 GMT
```

## Rate Limiting & Throttling

#### Token Bucket Algorithm

Most flexible and commonly used.

```python
import time
from threading import Lock

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = Lock()
    
    def consume(self, tokens=1):
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def _refill(self):
        now = time.time()
        tokens_to_add = (now - self.last_refill) * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

# Usage
bucket = TokenBucket(capacity=100, refill_rate=10)  # 10 tokens per second
if bucket.consume(1):
    # Process request
    pass
else:
    # Rate limited
    pass
```

#### Sliding Window Algorithm

More accurate but memory intensive

````python
import time
from collections import deque

class SlidingWindow:
    def __init__(self, window_size, max_requests):
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = deque()
    
    def allow_request(self):
        now = time.time()
        # Remove old requests outside window
        while self.requests and self.requests[0] < now - self.window_size:
            self.requests.popleft()
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
````

#### Fixed Window Algorithm

Simple but has burst Issues

````python
import time

class FixedWindow:
    def __init__(self, window_size, max_requests):
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = 0
        self.window_start = time.time()
    
    def allow_request(self):
        now = time.time()
        if now - self.window_start >= self.window_size:
            # Reset window
            self.window_start = now
            self.requests = 0
        
        if self.requests < self.max_requests:
            self.requests += 1
            return True
        return False
````

#### Other Rate Limiting Strategies

* Per-User Rate Limiting
* API Key-based Rate Limiting
* Global Rate Limiting

#### Rate Limiting Headers

Standard headers to communicate rate limit status

````python
# Response Headers
X-RateLimit-Limit: 1000        # Maximum requests allowed
X-RateLimit-Remaining: 999     # Requests remaining in window
X-RateLimit-Reset: 1640995200  # Unix timestamp when limit resets
Retry-After: 3600              # Seconds to wait before retry
````

## Authentication & Authorization

### JWT

**What is JWT?** A stateless authentication mechanism where user information is encoded in a cryptographically signed token. The token contains all necessary information to verify the user's identity and permissions.

**JWT Structure:** `Header.Payload.Signature`

- **Header**: Algorithm and token type
- **Payload**: User claims (ID, roles, expiration)
- **Signature**: Cryptographic verification

**Key Characteristics:**

- **Stateless**: No server-side session storage required
- **Self-contained**: All user info embedded in token
- **Tamper-proof**: Cryptographically signed
- **Portable**: Works across different domains/services

**When to Use JWT:**

- Microservices architecture (stateless communication)
- Single Page Applications (SPA)
- Mobile applications
- API-to-API communication
- Cross-domain authentication

**JWT vs Session Tokens Trade-offs:**

| **Factor**      | **JWT**                          | **Session Tokens**              |
| --------------- | -------------------------------- | ------------------------------- |
| **Scalability** | ✅ Stateless, horizontal scaling  | ❌ Requires shared session store |
| **Revocation**  | ❌ Hard to revoke before expiry   | ✅ Easy instant revocation       |
| **Size**        | ❌ Large payload in every request | ✅ Small session ID              |
| **Security**    | ❌ All data in client-side token  | ✅ Sensitive data server-side    |
| **Performance** | ✅ No database lookup             | ❌ Database lookup per request   |

**JWT Best Practices:**

- Keep access tokens short-lived (15-30 minutes)
- Use refresh tokens for session management
- Store securely (httpOnly cookies for web, secure storage for mobile)
- Include minimal necessary claims
- Implement token blacklisting for critical operations

**Refresh Token Pattern:** Two-token system where short-lived access tokens handle API requests, and long-lived refresh tokens generate new access tokens. This balances security (quick revocation) with user experience (no frequent re-authentication).

### OAuth 2.0

- An authorization framework that enables applications to obtain limited access to user accounts. It separates the role of the client from the resource owner by requiring authorization from the resource owner.

**Core Concepts:**

- **Resource Owner**: User who owns the data
- **Client**: Application requesting access
- **Authorization Server**: Issues access tokens
- **Resource Server**: Hosts protected resources

**OAuth 2.0 Flows (Grant Types):**

#### Authorization Code Flow

**Best for:** Web applications with server-side backend **Security Level:** Highest **Flow:**

1. Client redirects user to authorization server
2. User authorizes and gets redirected back with authorization code
3. Client exchanges code for access token (server-to-server)
4. Client uses access token to access resources

**Why secure?** Client secret never exposed to browser; authorization code is single-use and short-lived.

#### Client Credentials Flow

**Best for:** Server-to-server communication **Use case:** Microservices, background jobs, system integrations **Flow:** Direct exchange of client credentials for access token **Security:** No user context; service-level authorization only

#### Implicit Flow (Deprecated)

**Previously for:** Single Page Applications **Why deprecated?** Access token exposed in browser URL **Modern alternative:** Authorization Code Flow with PKCE

#### PKCE (Proof Key for Code Exchange)

**Purpose:** Secure OAuth for public clients (mobile apps, SPAs) **How it works:**

- Client generates random code verifier
- Sends SHA256 hash (code challenge) with authorization request
- Proves ownership during token exchange with original verifier

**OAuth 2.0 vs SAML vs OpenID Connect:**

- **OAuth 2.0**: Authorization framework
- **OpenID Connect**: Identity layer on top of OAuth 2.0
- **SAML**: XML-based federation protocol for enterprises

**OAuth 2.0 Design Decisions:**

- **Scopes**: Define permission granularity (read, write, admin)
- **Token Storage**: Authorization server responsibility
- **Client Registration**: Static vs dynamic client registration
- **Token Introspection**: Active token validation endpoint

### RBAC

* An access control method where permissions are associated with roles, and users are assigned to roles. 
* Instead of granting permissions directly to users, you assign roles that contain collections of permissions.

**Core Components:**

- **Users**: Individual entities requiring access
- **Roles**: Named collections of permissions (e.g., "Editor", "Admin")
- **Permissions**: Specific actions on resources (e.g., "users:read", "posts:create")
- **Resources**: Objects being protected (users, posts, files)

````python
User → Role → Permission → Resource
Alice → Editor → posts:create → Blog Posts
Bob → Admin → users:delete → User Accounts
````

#### RBAC Variations

#### Flat RBAC

Simple role assignment without hierarchy

```
Roles: [Guest, User, Moderator, Admin]
Each role has distinct permissions
```

#### Hierarchical RBAC

Roles inherit permissions from lower-level roles

```
Admin (inherits all)
  ↓
Moderator (inherits User + moderation)
  ↓
User (inherits Guest + user actions)
  ↓
Guest (read-only)
```

#### Constrained RBAC

Adds separation of duties and constraints

- **Mutual Exclusion**: User cannot have conflicting roles
- **Cardinality**: Limit number of users per role
- **Prerequisites**: Role A required before Role B

**RBAC vs ABAC (Attribute-Based Access Control):**

| **RBAC**                    | **ABAC**                    |
| --------------------------- | --------------------------- |
| Role-based decisions        | Attribute-based decisions   |
| Simple, easy to understand  | Complex, highly flexible    |
| Good for stable hierarchies | Good for dynamic contexts   |
| “What is your role?”        | “What are your attributes?” |

**When to Use RBAC:**

- Clear organizational hierarchy
- Relatively stable permission structure
- Need for simple administration
- Compliance requirements (SOX, HIPAA)

**RBAC Implementation Considerations:**

- **Role Explosion**: Too many fine-grained roles become unmanageable
- **Role Mining**: Analyzing existing permissions to create roles
- **Temporal Constraints**: Time-based role activation
- **Context Awareness**: Location, time, device-based access control

**Permission Design Patterns:**

```
Resource:Action format
- users:read, users:create, users:update, users:delete
- posts:publish, posts:moderate
- billing:view, billing:manage

Hierarchical permissions
- api:* (all API permissions)
- api:users:* (all user-related permissions)
- api:users:read (specific permission)
```

**Multi-Tenancy Considerations:**

- **Tenant Isolation**: Roles scoped to specific tenants
- **Cross-Tenant Roles**: System admin across all tenants
- **Role Templates**: Reusable role definitions across tenants

### Selecting a Right Auth Method

| **Use Case**     | **Recommended Method**       | **Reason**                 |
| ---------------- | ---------------------------- | -------------------------- |
| Single Page Apps | OAuth 2.0 + JWT              | Stateless, secure, good UX |
| Mobile Apps      | OAuth 2.0 + JWT              | Native integration, secure |
| Server-to-Server | OAuth 2.0 Client Credentials | No user context needed     |
| Legacy Systems   | API Keys                     | Simple integration         |
| High Security    | OAuth 2.0 + mTLS             | Mutual authentication      |
| Microservices    | JWT with service mesh        | Stateless, distributed     |

## Common API Design Patterns

### Request/Response Patterns

#### Standard HTTP Status Codes

```python
# Success responses
200 OK           # Successful GET, PUT, PATCH
201 Created      # Successful POST
204 No Content   # Successful DELETE

# Client error responses  
400 Bad Request      # Invalid syntax
401 Unauthorized     # Authentication required
403 Forbidden        # Insufficient permissions
404 Not Found        # Resource doesn't exist
409 Conflict         # Resource conflict
422 Unprocessable    # Validation errors

# Server error responses
500 Internal Server Error  # General server error
502 Bad Gateway           # Upstream server error
503 Service Unavailable   # Temporary overload
```

#### Error Response Format

```python
# Standardized error response
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "request_id": "req_12345"
  }
}
```

#### Pagination Patterns

```python
# Offset-based pagination
GET /api/users?limit=20&offset=40

# Cursor-based pagination (better for large datasets)
GET /api/users?limit=20&cursor=eyJpZCI6MTIzfQ

# Response format
{
  "data": [...],
  "pagination": {
    "total": 1000,
    "limit": 20,
    "offset": 40,
    "has_next": true,
    "next_cursor": "eyJpZCI6MTQ0fQ"
  }
}
```

### API Gateway Patterns

````python
class APIGateway:
    def __init__(self):
        self.services = {}
        self.rate_limiter = RateLimiter()
        self.auth = AuthService()
    
    def register_service(self, path_prefix, service_url):
        self.services[path_prefix] = service_url
    
    async def handle_request(self, request):
        # 1. Rate limiting
        if not self.rate_limiter.allow_request(request.client_ip):
            return Response(status=429, body="Rate limit exceeded")
        
        # 2. Authentication
        try:
            user = await self.auth.authenticate(request)
            request.user = user
        except AuthError:
            return Response(status=401, body="Unauthorized")
        
        # 3. Route to service
        service_url = self.find_service(request.path)
        if not service_url:
            return Response(status=404, body="Service not found")
        
        # 4. Proxy request
        response = await self.proxy_request(service_url, request)
        
        # 5. Add common headers
        response.headers['X-Request-ID'] = request.request_id
        response.headers['X-Response-Time'] = str(request.duration)
        
        return response
````

