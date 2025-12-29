# Authentication

Authentication is the process of verifying the identity of users, systems, or entities attempting to access resources. Modern applications require robust authentication patterns that balance security, usability, and scalability.

What is difference between Authentication & Authorization

- Authentication: "Who are you?" - Verifying identity
- Authorization: "What can you do?" - Determining permissions

Key principles involved in Authentication are identity validation & management, session management, scalability and user experience.

## Single Sign-On (SSO)

SSO allows users to authenticate once and gain access to multiple applications or services without re-entering credentials. It improves user experience while centralizing authentication management.

This is very common form of authentication used in Production Systems and Corporate Systems.

Some benefits of SSO are

- Improved user experience due to avoiding remembering multiple passwords.
- Centralized security policies which are easy to administer.
- Enhanced Security along with full audit trail from one auth source.

Challenges of using SSO

- Single Point of Failure
- Potential Cascading Security Flaw, hacking one of the credentials, gets you all the access.
- Vendor Lock-in, dependence on SSO provider

There are multiple SSO Implementation Patterns

- SAML
- OIDC
- Enterprise SSO Patterns

### SAML (Security Assertion Markup Language)

SAML Components:

- Identity Provider (IdP): Authenticates users and issues assertions
- Service Provider (SP): Consumes assertions and grants access
- Assertions: XML-based security tokens containing user information

A SAML assertion is an XML document issued by an Identity Provider (IdP) that asserts facts about a user to a Service Provider (SP).

SAML Assertion Flow,

![](assets/Pasted%20image%2020251229181926.png)

Use Cases for SAML Assertion are : Enterprise Applications, B2B integrations, Federated Identity across Organizations, etc.

### OIDC

Components of OIDC Authentication

- OpenID Provider (OP): Issues ID tokens after authentication
- Relying Party (RP): Application requesting authentication
- ID Token: JWT containing user identity information
- UserInfo Endpoint: Additional user profile information

![](assets/Pasted%20image%2020251229182522.png)

NOTE: Above diagram is for code_authorization_flow in oidc, there are many more authentication patterns which are not covered here :)

Notice how both (SAML and OIDC) are quite similar in the pattern of authentication, only the claims and identities are returned in different ways and formats.

Main Advantage that OIDC Provides are its simplicity.

- Built on OAuth 2.0 foundation
- JSON-based (simpler than XML)
- Better mobile and API support
- Standardized discovery mechanisms

### Enterprise SSO Patterns

**Active Directory Federation Services (ADFS):**

- Microsoft's enterprise SSO solution
- Integrates with Active Directory
- Supports SAML, WS-Federation, OAuth

**Lightweight Directory Access Protocol (LDAP):**

- Directory-based authentication
- Centralized user store
- Common in enterprise environments

**Kerberos:**

- Network authentication protocol
- Ticket-based authentication
- Strong security for internal networks

### SSO Important Considerations

#### Session Management

There could be multiple session strategy for maintaining a session, Global Session, Local Session, combination of both.

Session Lifecycle

- Session Establishment
- Session Refresh
- Session Termination
- Session timeout

#### Security Consideration

SAML

- Assertion encryption : protect sensitive user data
- signature verification : Ensure assertion integrity
- Replay attack prevention: Time-based validation
- Assertion audience restriction: Limit token scope

OIDC

- Token validation: Verify signature and claims
- HTTPS enforcement: Protect token transmission
- State parameter: Prevent CSRF attacks
- Nonce validation: Prevent replay attacks

## Multi-Factor Authentication

Multi-Factor Authentication requires users to provide multiple forms of evidence to verify their identity, significantly enhancing security beyond password-only authentication.

### Authentication Factors

#### Knowledge Factor (Something You Know)

- **Passwords**: Traditional text-based secrets
- **PINs**: Numeric personal identification numbers
- **Security questions**: Personal information verification
- **Passphrases**: Longer, sentence-like passwords
#### Possession Factor (Something you have)

- **Mobile devices**: SMS, authenticator apps
- **Hardware tokens**: Physical security keys
- **Smart cards**: Chip-based authentication devices
- **Digital certificates**: Cryptographic credentials

#### Inherence Factor (Something you are)

- **Fingerprints**: Biometric finger scanning
- **Facial recognition**: AI-based face analysis
- **Voice recognition**: Speech pattern analysis
- **Iris scanning**: Eye pattern recognition
- **Behavioral biometrics**: Typing patterns, gait analysis

#### Contextual Factor

- **Location**: Geographic or network-based verification
- **Device characteristics**: Known device identification
- **Time-based**: Authentication within expected time windows
- **Risk assessment**: Behavioral pattern analysis

### MFA Implementation Patterns

#### Time-based One-Time Passwords (TOTP)

**TOTP Characteristics:**

- **Algorithm**: Based on HMAC-SHA1 and current time
- **Validity**: Typically 30-60 second windows
- **Synchronization**: Requires time sync between client and server
- **Standard**: RFC 6238 specification

**TOTP Implementation Flow:**

1. Shared secret established during enrollment
2. User generates code using authenticator app
3. Server generates expected code using same algorithm
4. Codes compared for authentication
5. Used tokens marked to prevent replay

**Popular TOTP Applications:**

- Google Authenticator
- Microsoft Authenticator
- Authy
- 1Password

#### SMS-based Authentication

**SMS MFA Process:**

1. User enters username and password
2. System sends verification code via SMS
3. User enters received code
4. System validates code and grants access

**SMS Security Considerations:**

- **SIM swapping attacks**: Attacker takes control of phone number
- **SMS interception**: Network-level message capture
- **Delivery reliability**: Network and carrier dependencies
- **International limitations**: Cross-border delivery issues

**SMS Alternatives:**

- Voice calls for code delivery
- Push notifications to registered devices
- In-app notifications

#### Hardware Security Keys

**FIDO (Fast Identity Online) Standards:**

- **FIDO U2F**: Universal 2nd Factor authentication
- **FIDO2/WebAuthn**: Passwordless authentication standard
- **CTAP**: Client to Authenticator Protocol

**Hardware Key Benefits:**

- **Phishing resistance**: Domain-bound authentication
- **No shared secrets**: Public key cryptography
- **Offline capability**: No network dependency
- **Standardization**: Cross-platform compatibility

**Hardware Key Types:**

- **USB keys**: YubiKey, Google Titan
- **NFC keys**: Near-field communication enabled
- **Bluetooth keys**: Wireless connectivity
- **Lightning/USB-C**: Mobile device compatibility

#### Biometric Authentication

**Biometric Implementation Considerations:**

- **Template storage**: Local vs cloud storage
- **Liveness detection**: Prevent spoofing attacks
- **Accuracy metrics**: False accept/reject rates
- **Privacy protection**: Biometric data handling

**Biometric Challenges:**

- **Irrevocability**: Cannot change compromised biometrics
- **Template attacks**: Reverse engineering attempts
- **Presentation attacks**: Spoofing with fake biometrics
- **Environmental factors**: Lighting, positioning effects

Often these MFA generation methods force users to create backup codes (pre-generated single-use codes), and user should register multiple authenticators.

A good application should allow user to have account recovery procedures.

## Token-based Authentication

Token-based authentication uses cryptographically signed tokens to verify user identity and maintain session state across stateless HTTP requests.

### JWT

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

## Authentication Architecture Patterns

### MicroServices Authentication

#### Centralized Authentication Service

Authentication Service Responsibilities:

- User credential verification
- Token issuance and validation
- Session management
- Security policy enforcement

Service Integration Patterns:

- API Gateway integration: Central authentication point
- Service-to-service authentication: Machine-to-machine tokens
- Token propagation: Pass user context between services
- Authorization delegation: Service-specific permissions

#### Distributed Authentication

JWT-based Distributed Authentication:

- Self-contained tokens: No central validation needed
- Service independence: Each service validates tokens
- Reduced latency: No network calls for validation
- Consistent key management: Shared signing keys

### Security Best Practices

#### General Authentication Security

Implementation Guidelines:

- Password policies: Strength requirements and rotation
- Account lockout: Brute force protection
- Audit logging: Authentication event tracking
- Rate limiting: Prevent automated attacks
- Secure defaults: Fail-safe security configurations

Common Security Pitfalls:

- Weak session management: Predictable session IDs
- Inadequate logout: Incomplete session cleanup
- Token exposure: Logging or error message leaks
- Timing attacks: Information disclosure through response times
- Privilege escalation: Insufficient authorization checks