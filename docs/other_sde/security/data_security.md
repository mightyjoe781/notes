# Data Security

Data security protects information throughout its lifecycle — from creation and storage to transmission and disposal — through encryption, access controls, and privacy-preserving techniques.

**Key principles:**

- **Confidentiality**: data accessible only to authorized parties
- **Integrity**: data accuracy maintained; unauthorized modification prevented
- **Availability**: data accessible when needed by authorized users
- **Privacy**: protection of personally identifiable information (PII)
- **Compliance**: adherence to regulations (GDPR, HIPAA, SOX)

### Data Classification

**Levels:**

- Public: intended for public consumption
- Internal: for internal organizational use only
- Confidential: sensitive, requires protection
- Restricted: highly sensitive, strict access controls

**Classification factors:**

- Sensitivity: impact of unauthorized disclosure
- Regulatory obligations
- Business value
- Presence of PII or sensitive personal data

---

## Encryption at Rest

Encryption at rest protects stored data from unauthorized access when systems are powered off, stolen, or compromised at the storage level.

### Storage Encryption Types

#### Full Disk Encryption (FDE)

- Encrypts the entire disk including the OS
- Transparent to the operating system (auto encryption/decryption)
- Minimal performance overhead with hardware acceleration
- Key typically tied to user authentication

**Technologies:** BitLocker, FileVault (macOS), LUKS, self-encrypting drives (SEDs)

Common use cases: work laptops, mobile devices, encrypted backups.

#### File-Level Encryption

- Selectively encrypts specific files or folders
- Supports different keys per file
- Encryption tied to file permissions
- Minimal impact on the rest of OS operation

**Examples:** EFS (Windows), EncFS, eCryptfs, cloud storage encryption

#### Database Encryption

**Transparent Data Encryption (TDE):**

- Database engine handles encryption automatically
- Encrypts data pages on disk
- Minimal application changes required
- CPU overhead for encryption/decryption

**Column-Level Encryption:**

- Encrypts specific sensitive columns
- Supports different keys per column
- Application must handle encrypted data explicitly
- Encrypted columns are not easily searchable

| Database       | TDE Support      | Column Encryption | Key Features            |
| -------------- | ---------------- | ----------------- | ----------------------- |
| **MySQL**      | Yes (Enterprise) | Yes               | AES-256, key rotation   |
| **PostgreSQL** | Yes (extensions) | Yes               | Multiple cipher support |
| **Oracle**     | Yes              | Yes               | Advanced key management |
| **SQL Server** | Yes              | Always Encrypted  | Client-side encryption  |
| **MongoDB**    | Yes              | Yes               | Field-level encryption  |

### Encryption Algorithms and Standards

#### Symmetric Encryption — AES

- Key sizes: 128, 192, 256 bits
- Fast encryption/decryption with hardware support (AES-NI)
- No known practical attacks

**Modes of operation:**

- **ECB**: simple, not recommended
- **CBC**: requires an initialization vector
- **CTR**: stream cipher mode, parallelizable
- **GCM**: authenticated encryption (preferred for most uses)
- **XTS**: designed for disk encryption

#### Key Derivation

- **PBKDF2**: widely supported, configurable iterations
- **scrypt**: memory-hard, resistant to GPU attacks
- **Argon2**: winner of the Password Hashing Competition; recommended for new systems
- **bcrypt**: adaptive, widely used for password hashing

Key stretching benefits: computationally expensive to brute-force, salt prevents rainbow table attacks, work factor is adjustable over time.

### Cloud Storage Encryption

#### Server-Side Encryption (SSE)

- **SSE-S3**: Amazon S3 managed keys
- **SSE-KMS**: AWS Key Management Service
- **SSE-C**: customer-provided keys
- Transparent to applications; encryption handled by the cloud provider

#### Client-Side Encryption (CSE)

- Data encrypted on the client before upload
- Keys never leave the customer environment (zero-knowledge)
- Cloud provider cannot decrypt data
- Requires encryption libraries in the application

**Patterns:**

- Envelope encryption: encrypt data with a data key; encrypt that key with a master key
- Hybrid encryption: combine symmetric and asymmetric encryption
- Key versioning: support key rotation while remaining backward-compatible

### Encryption Best Practices

- Use established libraries — do not implement crypto yourself
- Use cryptographically secure random number generators for key generation
- Store keys separately from encrypted data
- Rotate encryption keys regularly
- Securely delete old keys and temporary plaintext

---

## Encryption in Transit

Encryption in transit protects data as it moves between systems, preventing eavesdropping and man-in-the-middle attacks.

### Transport Layer Security (TLS)

**TLS versions:**

- TLS 1.0/1.1: deprecated, vulnerable
- TLS 1.2: widely supported; secure with correct configuration
- TLS 1.3: recommended; improved security and reduced handshake latency

#### Certificate Types

- **DV (Domain Validated)**: basic domain ownership verification
- **OV (Organization Validated)**: extended organization verification
- **EV (Extended Validation)**: highest validation level
- **Wildcard**: covers multiple subdomains
- **SAN (Subject Alternative Name)**: multiple domains in one certificate

#### TLS Configuration Best Practices

**Cipher suite selection:**

- Use Perfect Forward Secrecy (PFS) via ephemeral key exchange (ECDHE)
- Strong encryption: AES-256-GCM, ChaCha20-Poly1305
- Secure hashing: SHA-256 or better
- Disable: RC4, 3DES, MD5, anonymous ciphers

**Security headers:**

- **HSTS**: force HTTPS connections
- **OCSP stapling**: efficient certificate status checking
- **Secure cookie flags**: `HttpOnly`, `Secure`, `SameSite`

### Application-Level Encryption

#### End-to-End Encryption (E2E)

- Data is encrypted on the sender's device
- Server stores ciphertext without holding decryption keys
- Only the recipient can decrypt
- Provider has zero knowledge of plaintext

**Protocols:** Signal Protocol, Double Ratchet, Noise Protocol Framework

#### API Encryption

- HTTPS: standard for web API encryption
- Message-level encryption: encrypt specific fields within a message
- JWE (JSON Web Encryption): encrypted JWT payloads
- Application-specific encryption schemes where needed

### Database Connection Encryption

**Database SSL/TLS support:**

- MySQL: SSL/TLS with certificate validation
- PostgreSQL: SSL modes from `require` to `verify-full`
- Oracle: native network encryption and SSL
- SQL Server: forced encryption with certificate validation
- MongoDB: TLS/SSL for client and replica set communication

**Connection security levels:**

- Encrypted: basic encryption, no certificate validation
- Authenticated: verify server certificate
- Mutually authenticated: both client and server present certificates
- Certificate pinning: pin expected server certificates

### Microservices Communication Security

#### mTLS (Mutual TLS)

- Services authenticate each other via certificates
- All inter-service communication is encrypted
- Certificates rotated automatically

#### Service Mesh Security

- Automatic mTLS managed by the mesh (e.g., Istio, Linkerd)
- Service identity and authentication built in
- Communication policies enforced centrally
- Encrypted traffic observable for monitoring

#### Message Queue Encryption

- Transport encryption: TLS on the connection
- Message encryption: encrypt the payload itself
- Key distribution: securely share encryption keys

**Examples:**

- Apache Kafka: SSL/TLS with SASL authentication
- RabbitMQ: TLS connections and message-level encryption
- Amazon SQS: server-side encryption with KMS
- Azure Service Bus: TLS and message-level encryption

---

## Key Management

Effective key management is critical. Weak key management renders strong encryption useless.

### Key Management Lifecycle

#### Key Generation

- Use cryptographically secure random number generators
- Select appropriate key sizes for the required security level
- Ensure keys are unique and not reused

**Key types:**

- Symmetric keys: same key for encryption and decryption
- Asymmetric key pairs: public/private
- KEK (Key Encryption Keys): used to encrypt other keys
- DEK (Data Encryption Keys): used to encrypt actual data

#### Key Distribution

- Manual: physical delivery
- Automated: secure key exchange protocols
- Key agreement: Diffie-Hellman, ECDH
- PKI: certificate-based distribution
- Key wrapping: encrypt keys with KEKs

#### Key Storage

**HSMs (Hardware Security Modules):**

- Tamper-resistant hardware
- Hardware random number generation
- Cryptographic operations performed inside the module
- FIPS 140-2 Level 3/4 compliant

**Software storage:** OS keystores, application keystores, cloud key management services

#### Key Rotation

**Benefits:** limits exposure window if a key is compromised, meets compliance requirements, supports forward secrecy

**Strategies:**

- Time-based: rotate on a schedule
- Usage-based: rotate after a threshold of operations
- Event-based: rotate after a security incident
- Gradual: support multiple key versions during transition

### Cloud Key Management Services

#### AWS KMS

- Customer Managed Keys (CMKs) for envelope encryption
- Data keys generated for encrypting data directly
- Fine-grained key policies and CloudTrail audit logging
- Multi-region key replication
- Direct encryption up to 4 KB; envelope encryption for larger data

#### Azure Key Vault

- Keys, secrets, and certificates in one service
- HSM-backed key protection
- RBAC-based access control

#### Google Cloud KMS

- Key rings to organize related keys
- Key versions for rotation support
- IAM integration and Cloud Audit Logs
- Cloud HSM for hardware-backed protection

### Key Management Best Practices

- Separation of duties: require multiple parties for critical key operations
- Least privilege: minimize who can access which keys
- Key escrow: maintain secure backups of critical keys
- Secure deletion: properly destroy old keys
- Audit logging: record all key access and operations
- Regular audits and disaster recovery planning

---

## Data Anonymization and Masking

Data anonymization and masking protect privacy by removing or obscuring PII while preserving data utility for legitimate purposes.

### Privacy Regulations

**GDPR:**

- Requires lawful basis for processing
- Consent management
- Privacy by design
- Privacy impact assessments
- Breach notification within 72 hours

**CCPA:**

- Consumer rights: right to know, delete, opt-out
- Restrictions on selling personal data

**HIPAA:**

- Protects PHI (Protected Health Information)
- Administrative, physical, and technical safeguards required
- Business associate agreements for third-party data handling

### Data Anonymization Techniques

#### Statistical Anonymization

**K-Anonymity:**

- Each record is indistinguishable from at least k−1 other records
- Achieved through generalization (replacing specific values with ranges) and suppression (removing identifying attributes)

```
Original:
Age | Zip Code | Salary
25  | 12345    | $50,000
26  | 12346    | $55,000
27  | 12347    | $60,000

3-Anonymous:
Age Range | Zip Prefix | Salary Range
25-27     | 123**      | $50,000-$60,000
25-27     | 123**      | $50,000-$60,000
25-27     | 123**      | $50,000-$60,000
```

**L-Diversity:**

- Addresses homogeneity attacks on k-anonymous data
- Each equivalence class must have at least l distinct values for sensitive attributes

**T-Closeness:**

- Sensitive attribute distribution within each group must match the overall distribution
- Stronger protection than l-diversity but more complex to implement

#### Differential Privacy

- Formal mathematical guarantee of privacy
- Calibrated random noise added to query results
- Privacy budget limits total information leakage across queries

**Implementation approaches:**

- Local differential privacy: noise added on the client side
- Global differential privacy: noise added on the server side
- Federated learning: train models without centralizing raw data
- Synthetic data generation: create privacy-preserving datasets

### Data Masking Techniques

#### Static Data Masking

Applied to data at rest (e.g., production data copied to non-production environments):

- Consistent masking: same input always produces the same masked output
- Referential integrity maintained across tables
- Format preserved (same type and structure)
- Irreversible: original values cannot be recovered

**Methods:** substitution, shuffling, numeric variance, date shifting

#### Dynamic Data Masking

Applied at query time:

- Role-based: different masking rules per user role
- Context-aware: masking based on query context
- Implemented at database level, application layer, or via proxy

### Tokenization

Replaces sensitive data with a non-sensitive token. The mapping is stored in a secure token vault.

**Characteristics:**

- Format-preserving: tokens match the original data format
- Consistent: same value always maps to the same token
- Irreversible without the vault

| Aspect             | Tokenization                     | Encryption                     |
| ------------------ | -------------------------------- | ------------------------------ |
| **Reversibility**  | Irreversible without token vault | Reversible with key            |
| **Format**         | Preserves original format        | May change format              |
| **Performance**    | Fast lookup                      | Crypto overhead                |
| **Key management** | Centralized token vault          | Distributed key management     |
| **Compliance**     | Often removes data from scope    | Data remains in compliance scope |

### Synthetic Data Generation

**Use cases:** development/testing, analytics, ML model training, cross-organization data sharing

**Statistical methods:**

- Parametric models: generate data based on statistical distributions
- Non-parametric models: use empirical distributions
- Copula-based generation: preserve correlation structures
- Bootstrap sampling

**ML methods:**

- GANs (Generative Adversarial Networks): generate realistic synthetic data
- VAEs (Variational Autoencoders): learn data distributions for generation

### Implementation Strategies

#### Data Discovery and Classification

- Pattern matching (regex) to identify PII
- ML-based classification
- Database schema and content scanning
- Data lineage tracking

**Classification dimensions:** sensitivity level, data type (PII/PHI/financial), regulatory scope, processing requirements (retention, anonymization, encryption)

#### Privacy Engineering

**Privacy by design:**

- Integrate privacy into system design from the start
- Strongest privacy settings as the default
- Transparency about privacy practices

**Privacy impact assessments:**

- Identify privacy risks in data processing
- Develop risk mitigation strategies
- Validate compliance
- Monitor continuously
