# Homomorphic Encryption


## What is Encryption ?

- Symmetric Encryption
    - Uses a single secret key for both encrypting and decrypting data.
    - Key distribution is risky; if key is stolen, security is compromised.
- Asymmetric Encryption
    - Uses a pair of keys: a public key to encrypt data and a private key to decrypt. One key locks the data, the other unlocks it.
    - Slower than symmetric encryption; more complex.

Good Video : https://www.youtube.com/watch?v=I6Unxb-PFhs
## Why we can't always Encrypt ?

- Database Queries can only be performed on plain text
- Analysis, Indexing, Tuning
- Application must read data to process it
- TLS Termination Layer 7 Reverse Proxies and Load Balancing
## Homomorphic Encryption

- Ability to perform arithmetic operations on encrypted data
- No need to decrypt!
- You can query a database that is encrypted !
- Layer 7 Reverse Proxies don't have to terminate TLS, can route traffic based on rules without decrypting traffic
- Database can index and optimize without decrypting data
- Only drawback is its too slow atm (takes 3 minutes to fetch 100 records)

FHE toolkit by IBM : https://github.com/IBM/fhe-toolkit-linux
