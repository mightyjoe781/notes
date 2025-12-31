# API Design Principles

> _What does a great API look like, and why should we care about the APIs we build?_

> A thoughtfully designed API can be a game changer - it directly shapes the developer experience and determines how easily others can build on top of it.

Few examples of such *clean, consistent, developer-first* APIs comes from Stripe, Twilio, Plaid, GitHub, Slack, Shopify, SendGrid etc.

What makes these APIs stand out is following

- Consistency : Same naming, same patterns everywhere
- Predictability : You can guess the next endpoint
- Clear Error Models : Structured errors, not strings
- Good Default : Sensible pagination, limits, retries
- Strong Documentation : Examples > Explanations
- Backwards Compatibility : Versioning without surprise
- Developer Empathy : Designed for Humans, not machines

Good Video on API Design : [Link](https://www.youtube.com/watch?v=IEe-5VOv0Js)

- APIs should be *Approachable, Flexible, Composable*.
- Example of Stripe API Release Process

![](assets/Pasted%20image%2020251216003034.png)

- API Design Patterns
    - Avoid Industry Jargon
    - Nested Structures : introduces structure with extensionability
    - Properties as Enums: prefer enums rather than booleans
    - Reflect API Request in Response
    - Polymorphic Objects : Use type field to define the type of object we gonna receive.
    - Express changes with verbs : `/v1/payment_intents/:id/capture` or `/v1/invoices/:id/mark_uncollectible`
    - Timestamp parameter names `<verb>_at`
    - Gated Features

![](assets/Pasted%20image%2020251216003550.png)

Other Few Important Concepts in reference of robust APIs is *Pagination, Idempotency Key, etc.*

## Design Principles for APIs

### URL Path Versioning

- Most common and straightforward approach, flexible to update your code without breaking backward compatibility for consumers.

```python
# Examples
GET /api/v1/users
GET /api/v2/users
GET /api/v3/users
```

- Only disadvantages are maintenance and nudging consumers to start using latest endpoints.
- Other ways to represent same could be using query params or headers to avoid URL pollution.

```python
# Request Header
GET /api/users
Accept: application/vnd.api+json;version=1

# Or custom header
API-Version: 2.0
```

```python
# Query Params versioning
GET /api/users?version=1.0
GET /api/users?v=2
```

```python
# versioning embedded in Content Type, HTTP Standard
# Request
Accept: application/vnd.company.app-v2+json

# Response
Content-Type: application/vnd.company.app-v2+json
```

- Some of the best practices for API Migration are
    - Semantic Versioning : https://semver.org/
    - Backward Compatibility
    - Deprecation Strategy: Clearly communicate timelines
    - Documentation and changelog along with migration guides.

```python
# Deprecation Header Example
GET /api/v1/users
Response Headers:
Warning: 299 - "Deprecated API Version. Migrate to v2 by 2024-12-31"
Sunset: Wed, 31 Dec 2024 23:59:59 GMT
```

### Rate Limiting & Throttling

- Examples of algorithm, Token Bucket Algorithm, Sliding Window, Fixed Window.
- Usually we should return the response back to user before they hit rate limits.
- Rate Limiting Strategies
    - Per-User
    - API Key-Based
    - Global Rate Limits

```python
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 30

X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1703409000

{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Too many requests. Please retry after 30 seconds."
  }
}
```

Implementation of Token Bucket Algorithm

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


### Idempotency

- Usually its only required for `POST` and `PATCH` operations, rest all operation are (should be) repeatable and don't act on database etc.
- Generally as a Thumb rule it should be generated client side (UI) because client is supposed to track it, and send it with the request to Backend.
- Idea is that client might send multiple send requests, some user clicks UI multiple times, but we should process it once. Very common in payments and ordering services.

```python
POST /payments HTTP/1.1
Host: api.example.com
Content-Type: application/json
Idempotency-Key: 7f8c2c8a-9e7f-4b5b-a912-44b6dcb1b3d2

{
  "user_id": "u123",
  "amount": 5000,
  "currency": "INR"
}
```


From server response could be like following

```python
# first request
HTTP/1.1 201 Created
Content-Type: application/json
Idempotency-Key: 7f8c2c8a-9e7f-4b5b-a912-44b6dcb1b3d2

{
  "payment_id": "pay_98765",
  "status": "success"
}

# second/multiple requests
HTTP/1.1 200 OK
Content-Type: application/json
Idempotency-Key: 7f8c2c8a-9e7f-4b5b-a912-44b6dcb1b3d2
Idempotent-Replayed: true

{
  "payment_id": "pay_98765",
  "status": "success"
}
```

### Pagination

- There are multiple ways to implement pagination.
    - Limit & Offset
        - Server Side Cursor
        - Client Side Cursor
    - Next Page Token
- Usually when we want to allow user to jump around pages in random order we use Limit & Offset, If we want user to proceed only to next page in order we use next page token based pagination.
- We can combine both as well, see in Pagination Patterns Section

```python

### Limit Offset
REQUEST /api/v1/users?limit=100&offset=0

RESPONSE:
{
    "data": [(..)],
    "page_no": 2,
    "total_pages": 50,
    "data_length": 100
}

### Next Page Token
REQUEST /api/v1/users

RESPONSE:

{
    "data": [(...)],
    "has_more": true,
    "next_page_token": "token123125"
}

```

| Method           | Example                              | Pros                                   | Cons                         |
| ---------------- | ------------------------------------ | -------------------------------------- | ---------------------------- |
| **Offset-based** | `GET /posts?page=2&limit=20`         | Easy to implement, familiar            | Issues with data changes     |
| **Cursor-based** | `GET /posts?cursor=abc123&limit=20`  | Consistent results, real-time friendly | More complex implementation  |
| **Key-based**    | `GET /posts?since_id=12345&limit=20` | Efficient for time-ordered data        | Limited to specific ordering |

### Request/Response Patterns

#### Standard HTTP Status Code

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

```json
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


### Simple API Gateway Implementation

- NOTE : This is just representative

```python
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
```


Resources : 

- [Postman Blog on Stripe APIs](https://blog.postman.com/how-stripe-builds-apis/)