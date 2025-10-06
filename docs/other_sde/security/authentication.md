# Authentication




# Token-based Authentication

Token-based authentication uses cryptographically signed tokens to verify user identity and maintain session state across stateless HTTP requests.

## JWT

- JSON Web Token
- Completely Stateless
- 3 Parts 
    - **Header**: Algorithm and token type information
    - **Payload**: Claims about the user and session
    - **Signature**: Cryptographic verification of token integrity
- Signature Encryption can be symmetrical or asymmetrical
- Symmetrical require same key to generate JWT and validate
- Asymmetrical private Key creates the JWT, public key validates

Example : https://www.jwt.io/

![](assets/Pasted%20image%2020251006225843.png)

JWT Format : `<claims>.<payload>.<signature>`

```jwt
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30
```

### JWT Based Auth

Symmetric Key

![](assets/Pasted%20image%2020251006232323.png)

![](assets/Pasted%20image%2020251006232332.png)

### JWT Claims

Standard Claims:

- `iss` (Issuer): Token issuing authority
- `sub` (Subject): User identifier
- `aud` (Audience): Intended token recipients
- `exp` (Expiration): Token expiration time
- `iat` (Issued At): Token creation time
- `nbf` (Not Before): Token validity start time

Custom Claims:

- User roles: Authorization information
- Permissions: Specific access rights
- Tenant ID: Multi-tenant identification
- Session data: Application-specific information

### JWT Security Considerations

Token Security Best Practices:

- Short expiration times: Limit token validity window
- Secure storage: HttpOnly cookies or secure storage
- HTTPS enforcement: Protect token transmission !! most common attacks
- Signature verification: Always validate token integrity
- Algorithm restrictions: Whitelist allowed algorithms

Common JWT Vulnerabilities:

- Algorithm confusion: None algorithm attacks
- Key confusion: RSA/HMAC algorithm substitution
- Token replay: Reusing valid tokens maliciously
- Information disclosure: Sensitive data in payload
### Refresh Tokens

- Once Stolen we can't do anything
- So we must make it short-lived
- But can't force users to login every 15 minutes
- Need a way to get new JWT every 15 minutes

![](assets/Pasted%20image%2020251006233110.png)

### Asymmetric JWT

Symmetric Keys are difficult to share in Microservices Architecture making them unsuitable for a firm level operations.
Usually we deploy IdP servers (Identity Providers). These servers handle issuing of the token and have the private keys. Any client ask for token from these servers and then can use that token to query another microservice, which can either decrypt the token and verify signature using public keys of auth servers, or can request IdP servers to validate the token.

![](assets/Pasted%20image%2020251006233627.png)

### Token Management Patterns

#### Token Storage Strategies

Client-Side Storage Options:

| Storage Method   | Security | Persistence  | XSS Vulnerability |
| ---------------- | -------- | ------------ | ----------------- |
| Local Storage    | Low      | High         | High              |
| Session Storage  | Low      | Medium       | High              |
| HttpOnly Cookies | High     | Configurable | Low               |
| Memory Only      | High     | Low          | Low               |

Server-Side Storage:

- Database storage: Persistent token management
- Cache storage: Fast token validation
- Distributed cache: Scalable token sharing
- Token introspection: Centralized validation

#### Token Validation Patterns

Local Validation:

- Signature verification: Cryptographic validation
- Claims validation: Expiration and audience checks
- No network calls: Fast validation process
- Suitable for: Stateless microservices

Remote Validation:

- Token introspection: Server-side validation
- Real-time revocation: Immediate token invalidation
- Network dependency: Requires connectivity
- Suitable for: High-security applications

#### Token Lifecycle Management

**Token Issuance:**

1. User authentication
2. Token generation with appropriate claims
3. Token signing with secure key
4. Token delivery to client
5. Token storage (server-side tracking if needed)

**Token Refresh:**

1. Access token expiration detection
2. Refresh token presentation
3. Refresh token validation
4. New access token generation
5. Optional refresh token rotation

**Token Revocation:**

1. Logout or security event
2. Token blacklisting or database update
3. Cleanup of related sessions
4. Notification to relevant services

### Stateless vs Stateful Authentication

#### Stateless Authentication

Characteristics:

- No server-side session storage
- Token contains all necessary information
- Horizontal scalability
- Reduced server memory usage

Implementation Considerations:

- Token size: Balance information vs payload size
- Secret management: Secure key distribution
- Revocation complexity: Immediate invalidation challenges
- Clock synchronization: Time-based claims validation

#### Stateful Authentication

Characteristics:

- Server-side session storage
- Token references server-side data
- Centralized session management
- Easier revocation and updates

Implementation Considerations:

- Storage scaling: Session store performance
- High availability: Session replication
- Memory usage: Session data size
- Cleanup processes: Expired session removal

### Pros vs Cons

| Pros                                                                                                                                       | Cons                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stateless<br>Great for APIs<br>Secure<br>Carry useful info (username)<br>Can store info that derive UX<br>No need for centralized database | Sharing Secrets in Microservices<br>Key management<br>Very tricky to consume correctly<br>Storage of Refresh tokens<br>Token Revocation and Control<br>Insecure implementation (e.g none alg) |


