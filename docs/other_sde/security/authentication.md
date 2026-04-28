# Authentication

Authentication is the process of verifying the identity of users, systems, or entities attempting to access resources.

- **Authentication**: "Who are you?" — verifying identity
- **Authorization**: "What can you do?" — determining permissions

Key principles: identity validation, session management, scalability, and user experience.

## Single Sign-On (SSO)

SSO allows users to authenticate once and gain access to multiple applications without re-entering credentials. It centralizes authentication management and is widely used in production and enterprise systems.

**Benefits:**

- Improved user experience — fewer passwords to manage
- Centralized security policies, easier to administer
- Unified audit trail from a single auth source

**Challenges:**

- Single point of failure
- A compromised credential grants access to all connected systems
- Vendor lock-in

SSO implementation patterns: SAML, OIDC, Enterprise SSO.

### SAML (Security Assertion Markup Language)

**Components:**

- **Identity Provider (IdP)**: Authenticates users and issues assertions
- **Service Provider (SP)**: Consumes assertions and grants access
- **Assertions**: XML-based security tokens containing user information

A SAML assertion is an XML document issued by the IdP that asserts facts about a user to the SP.

**SAML Assertion Flow:**

![](assets/Pasted%20image%2020251229181926.png)

Use cases: enterprise applications, B2B integrations, federated identity across organizations.

### OIDC (OpenID Connect)

**Components:**

- **OpenID Provider (OP)**: Issues ID tokens after authentication
- **Relying Party (RP)**: Application requesting authentication
- **ID Token**: JWT containing user identity information
- **UserInfo Endpoint**: Additional user profile data

![](assets/Pasted%20image%2020251229182522.png)

The diagram above shows the Authorization Code flow. OIDC defines additional flows not covered here.

Both SAML and OIDC follow a similar pattern — the key differences are in the token format (XML vs JSON) and how claims are returned.

**OIDC advantages over SAML:**

- Built on OAuth 2.0
- JSON-based (simpler than XML)
- Better mobile and API support
- Standardized discovery mechanisms

### Enterprise SSO Patterns

**Active Directory Federation Services (ADFS):**

- Microsoft's enterprise SSO solution
- Integrates with Active Directory
- Supports SAML, WS-Federation, OAuth

**LDAP (Lightweight Directory Access Protocol):**

- Directory-based authentication
- Centralized user store
- Common in enterprise environments

**Kerberos:**

- Network authentication protocol
- Ticket-based authentication
- Strong security for internal networks

### SSO Considerations

#### Session Management

Session strategies include global sessions, local sessions, or a hybrid of both.

Session lifecycle:

- Establishment
- Refresh
- Termination
- Timeout

#### Security Considerations

**SAML:**

- Assertion encryption: protect sensitive user data
- Signature verification: ensure assertion integrity
- Replay attack prevention: time-based validation
- Audience restriction: limit token scope

**OIDC:**

- Token validation: verify signature and claims
- HTTPS enforcement: protect token transmission
- State parameter: prevent CSRF attacks
- Nonce validation: prevent replay attacks

## Multi-Factor Authentication (MFA)

MFA requires users to provide multiple forms of evidence to verify identity, significantly improving security beyond passwords alone.

### Authentication Factors

#### Knowledge Factor (Something You Know)

- Passwords
- PINs
- Security questions
- Passphrases

#### Possession Factor (Something You Have)

- Mobile devices (SMS, authenticator apps)
- Hardware tokens
- Smart cards
- Digital certificates

#### Inherence Factor (Something You Are)

- Fingerprints
- Facial recognition
- Voice recognition
- Iris scanning
- Behavioral biometrics (typing patterns, gait)

#### Contextual Factor

- Location (geographic or network-based)
- Known device characteristics
- Time-based validation
- Risk assessment via behavioral analysis

### MFA Implementation Patterns

#### TOTP (Time-based One-Time Passwords)

**Characteristics:**

- Based on HMAC-SHA1 and current time (RFC 6238)
- Codes valid for 30–60 second windows
- Requires time synchronization between client and server

**Flow:**

1. Shared secret established during enrollment
2. User generates a code via authenticator app
3. Server independently generates the expected code
4. Codes are compared
5. Used tokens are marked to prevent replay

**Popular TOTP apps:** Google Authenticator, Microsoft Authenticator, Authy, 1Password

#### SMS-Based Authentication

**Flow:**

1. User enters username and password
2. System sends a verification code via SMS
3. User enters the code
4. System validates and grants access

**Security considerations:**

- SIM-swapping attacks
- SMS interception at the network level
- Delivery reliability issues
- International delivery limitations

**Alternatives:** voice call delivery, push notifications, in-app codes

#### Hardware Security Keys

**FIDO Standards:**

- **FIDO U2F**: Universal 2nd Factor
- **FIDO2/WebAuthn**: Passwordless authentication standard
- **CTAP**: Client to Authenticator Protocol

**Benefits:**

- Phishing-resistant (domain-bound)
- No shared secrets (public key cryptography)
- Works offline
- Cross-platform standardization

**Key types:** USB (YubiKey, Google Titan), NFC, Bluetooth, Lightning/USB-C

#### Biometric Authentication

**Implementation considerations:**

- Template storage: local vs cloud
- Liveness detection: prevent spoofing
- Accuracy metrics: false accept/reject rates
- Privacy: biometric data handling regulations

**Challenges:**

- Irrevocability: compromised biometrics cannot be changed
- Template attacks and presentation attacks (spoofing)
- Environmental factors (lighting, positioning)

MFA implementations should support backup codes (pre-generated single-use codes), multiple registered authenticators, and account recovery procedures.

## Token-Based Authentication

Token-based authentication uses cryptographically signed tokens to verify identity and maintain session state across stateless HTTP requests.

### JWT (JSON Web Token)

- Completely stateless
- Three parts: `<header>.<payload>.<signature>`
    - **Header**: algorithm and token type
    - **Payload**: claims about the user and session
    - **Signature**: cryptographic integrity verification
- Symmetric signing: same key signs and validates
- Asymmetric signing: private key signs, public key validates

Reference: https://jwt.io/

![](assets/Pasted%20image%2020251006225843.png)

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30
```

### JWT-Based Auth

**Symmetric key flow:**

![](assets/Pasted%20image%2020251006232323.png)

![](assets/Pasted%20image%2020251006232332.png)

### JWT Claims

**Standard claims:**

- `iss` — Issuer
- `sub` — Subject (user identifier)
- `aud` — Audience (intended recipients)
- `exp` — Expiration time
- `iat` — Issued at
- `nbf` — Not before

**Custom claims:**

- User roles and permissions
- Tenant ID (multi-tenant systems)
- Application-specific session data

### JWT Security Considerations

**Best practices:**

- Short expiration times
- Store in HttpOnly cookies (preferred over localStorage)
- Always use HTTPS
- Always verify the signature
- Restrict allowed signing algorithms

**Common vulnerabilities:**

- Algorithm confusion (`alg: none` attacks)
- RSA/HMAC algorithm substitution
- Token replay
- Sensitive data in the payload (it is only base64-encoded, not encrypted)

### Refresh Tokens

Short-lived access tokens limit the impact of theft, but logging users out every 15 minutes is impractical. Refresh tokens solve this:

- Access token expires quickly (e.g., 15 minutes)
- Refresh token is longer-lived and stored securely
- Client exchanges the refresh token for a new access token silently

![](assets/Pasted%20image%2020251006233110.png)

### Asymmetric JWT in Microservices

Symmetric keys are difficult to distribute safely across many services. The standard solution is a dedicated **Identity Provider (IdP)**:

- IdP holds the private key and issues tokens
- Services verify tokens using the IdP's public key
- Alternatively, services can call the IdP to validate tokens

![](assets/Pasted%20image%2020251006233627.png)

### Token Storage Strategies

| Storage Method   | Security | Persistence  | XSS Vulnerability |
| ---------------- | -------- | ------------ | ----------------- |
| Local Storage    | Low      | High         | High              |
| Session Storage  | Low      | Medium       | High              |
| HttpOnly Cookies | High     | Configurable | Low               |
| Memory Only      | High     | Low          | Low               |

**Server-side storage options:** database, cache, distributed cache, token introspection

### Token Validation Patterns

**Local validation:**

- Verify signature and claims (expiration, audience)
- No network calls — fast
- Suitable for stateless microservices

**Remote validation (introspection):**

- Server-side validation with real-time revocation support
- Requires network connectivity
- Suitable for high-security applications

## Stateless vs Stateful Authentication

### Stateless Authentication

- No server-side session storage
- Token contains all necessary information
- Horizontally scalable
- Lower server memory usage
- Revocation is complex (tokens remain valid until expiry)

### Stateful Authentication

- Server stores session data
- Token is a reference to server-side data
- Easier revocation and session updates
- Requires session store scaling and high availability

## Authentication Architecture Patterns

### Centralized Authentication Service

Responsibilities:

- Credential verification
- Token issuance and validation
- Session management
- Security policy enforcement

Integration patterns:

- API gateway integration (single auth entry point)
- Service-to-service tokens (machine-to-machine)
- Token propagation (user context passed between services)
- Authorization delegation (service-specific permissions)

### Distributed Authentication (JWT-based)

- Self-contained tokens — no central validation needed per request
- Each service independently validates tokens
- Reduced latency
- Consistent key management via shared signing keys or public key distribution

### Security Best Practices

- Enforce password strength requirements
- Account lockout on repeated failures (brute-force protection)
- Audit logging for all authentication events
- Rate limiting on login endpoints
- Fail-safe defaults (deny on error)

**Common pitfalls:**

- Predictable session IDs
- Incomplete logout (sessions not fully cleaned up)
- Tokens leaked in logs or error messages
- Timing attacks that reveal valid usernames
- Insufficient authorization checks after authentication
