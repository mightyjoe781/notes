# OpenSSL

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Swiss-army knife for TLS/SSL: generate keys, create certificates, inspect and convert cert formats, encrypt files.

### Installation

```bash
sudo apt install openssl
openssl version
```

### Generate Keys

```bash
# RSA (2048 or 4096 bit)
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out private.key

# ECDSA (smaller, faster - recommended)
openssl ecparam -genkey -name secp384r1 -out ec.key

# View key info
openssl rsa -in private.key -text -noout
openssl ec -in ec.key -text -noout
```

### Self-Signed Certificate

```bash
# Key + self-signed cert in one command
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes \
  -subj "/C=US/ST=State/L=City/O=Org/CN=example.com"

# With Subject Alternative Names (required by modern browsers)
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes \
  -subj "/CN=example.com" \
  -addext "subjectAltName=DNS:example.com,DNS:www.example.com"
```

### Certificate Signing Request (CSR)

```bash
# Generate CSR from existing key
openssl req -new -key private.key -out request.csr \
  -subj "/CN=example.com/O=My Org/C=US"

# View CSR content
openssl req -in request.csr -text -noout
```

### Inspect Certificates

```bash
# View cert details
openssl x509 -in cert.pem -text -noout

# Check expiry date
openssl x509 -in cert.pem -noout -enddate

# Verify cert chain
openssl verify -CAfile ca.crt cert.pem

# Check remote server certificate
openssl s_client -connect example.com:443 -showcerts </dev/null

# Check cert and key match (modulus must be same)
openssl x509 -noout -modulus -in cert.pem | md5sum
openssl rsa -noout -modulus -in key.pem | md5sum
```

### Convert Formats

```bash
# PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der

# DER to PEM
openssl x509 -inform DER -in cert.der -out cert.pem

# Create PKCS#12 bundle (cert + key)
openssl pkcs12 -export -in cert.pem -inkey key.pem -out bundle.p12

# Extract from PKCS#12
openssl pkcs12 -in bundle.p12 -out cert.pem -nodes

# PEM to PKCS#7
openssl crl2pkcs7 -nocrl -certfile cert.pem -out cert.p7b
```

### Encrypt and Decrypt Files

```bash
# Encrypt with AES-256
openssl enc -aes-256-cbc -pbkdf2 -salt -in plaintext.txt -out encrypted.bin

# Decrypt
openssl enc -d -aes-256-cbc -pbkdf2 -in encrypted.bin -out plaintext.txt
```

### Diffie-Hellman Params

```bash
openssl dhparam -out dhparam.pem 2048
```

### Hashing

```bash
openssl dgst -sha256 file.txt
openssl dgst -sha256 -sign key.pem -out sig.bin file.txt   # sign
openssl dgst -sha256 -verify pub.pem -signature sig.bin file.txt  # verify
```

### Tips

- Use `Let's Encrypt / certbot` for public-facing sites instead of self-signed certs
- Always add `-nodes` when generating test keys to skip passphrase (for automation)
- Use `-days 36500` for long-lived internal certs (100 years)
- Modern TLS: prefer TLSv1.2 / TLSv1.3, avoid SSLv3/TLSv1.0
- Check if a port is open with TLS: `openssl s_client -connect host:443`

### See Also

- [Nginx](nginx.md) for SSL/TLS termination
- [SSH](ssh.md) for key-based auth
- Also: [certbot](https://certbot.eff.org) for Let's Encrypt automation, cfssl (Cloudflare PKI toolkit), step-cli
