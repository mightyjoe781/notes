## Securing Microservices

Not all data is equally sensitive. For example, the Catalog Service is largely public, while the Ordering Service contains highly sensitive financial data and requires strict protection.

#### Encrypting Data in Transit

Encryption must be present in transit. Use standard, well-vetted algorithms — never implement your own encryption scheme.

For HTTP, use **TLS (Transport Layer Security)** with valid certificates. Certificates can be managed by:

- Your cloud provider (e.g., AWS Certificate Manager, Azure-managed certificates)
- The [**lego**](https://go-acme.github.io/lego/) CLI tool — an ACME client for Let's Encrypt, written in Go
- cert-manager (for Kubernetes environments)

#### Encrypting Data at Rest

Data stored on disk also needs encryption. This requires:

- Proper encryption key management (e.g., AWS KMS, Azure Key Vault, HashiCorp Vault)
- Encrypted backups

#### Authentication

*We need to know who is calling our service.*

HTTP authentication options:

| Method | Notes |
|---|---|
| **Basic Auth** (username & password) | Requires every microservice to manage credential storage — not recommended |
| **API Key** | Simple client identification; requires client lifecycle management |
| **Client Certificate** | Strong mutual TLS (mTLS); complex to manage at scale |

The recommended approach is to use a dedicated **Identity Server** with industry-standard protocols: **OAuth 2.0** and **OpenID Connect**.

How it works:
1. The client authenticates with the Identity Server
2. The Identity Server issues a short-lived **access token** (JWT)
3. Every request from the client to a microservice includes the token
4. Microservices validate the token without managing credentials themselves

Common Identity Server implementations: [Keycloak](https://www.keycloak.org/), [Auth0](https://auth0.com/), [Duende IdentityServer](https://duendesoftware.com/products/identityserver), or cloud-native options like AWS Cognito and Azure Entra ID.

> **Recommended reading**: *OAuth 2.0 in Action* by Justin Richer & Antonio Sanso

#### Authorization

*Authentication establishes who the caller is; authorization limits what they can do.*

Authorization frameworks:

- Make decisions based on **roles** or **claims** in the access token
- Consider carefully what each caller type should be permitted to do

**Role-based access control (RBAC)** helps prevent the [confused deputy problem](https://en.wikipedia.org/wiki/Confused_deputy_problem) — where a service with elevated privileges is tricked into performing unauthorized actions on behalf of a less-privileged caller.

#### Securing the Network

Place all microservices inside a **virtual network (VNet/VPC)** and block direct public access. Expose services only through an **API Gateway** that:

- Accepts requests from the public network
- Enforces authentication and authorization at the edge
- Acts as a single point of entry, hardened with a firewall and DDoS protection

#### Defense in Depth

*Don't rely on a single layer of security.*

Apply multiple overlapping layers:

- Encryption in transit (TLS)
- Encryption at rest
- Short-lived access tokens
- Virtual network isolation and allowlists
- API Gateway as the single public entry point

Additional defensive measures:

- **Penetration testing**: Performed by security experts; get their recommendations
- **Automated security testing**: Prove that APIs correctly reject unauthorized callers (e.g., with tools like OWASP ZAP)
- **Attack detection**: Detect port scanning, SQL injection attempts; alert and respond quickly
- **Auditing**: Maintain a complete, tamper-resistant record of who did what and when
