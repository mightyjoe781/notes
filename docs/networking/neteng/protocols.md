# Popular Networking Protocols

## DNS

### Why DNS ?

- People. can't remember IPs
- A domain is a text points to an IP or a collection of IPs
- Additional layer of abstraction is good
- IP can change while the domain remain
- We can serve the closest IP to a client requesting the same domain
- Load Balancing
### DNS

- A new addressing system means we need a mapping. Meet DNS
- If you have an IP and you need the MAC, we use ARP
- If you have an name and you need the IP, we use DNS
- Built on top of UDP
- Port 53
- Many records (MX, TXT, A, CNAME)

### How DNS works

- DNS resolver - frontend and cache
- ROOT server - Hosts IPs of TLDs
- Top level domain server ~ Hosts IPs of the ANS
- Authoritative Name Server ~ Hosts the IP of the target server

![](assets/Pasted%20image%2020251001001559.png)

### DNS Packet

![](assets/Pasted%20image%2020251001000855.png)
RFC : https://datatracker.ietf.org/doc/html/rfc1035
### Notes about DNS

- Why so many layers ?
- DNS is not encrypted by default
- Many attacks against DNS (DNS hijacking/DNS poisoning)
- DoT / DoH attempts to address this

### DNS Commands

```bash
nslookup notes.minetest.in

nslookup -type=a minetest.in

nslookup -type=ns minetest.in

nslookup minetest.in 1.1.1.1

dig minetest.in mx
```

## TLS

### HTTP

![](assets/Pasted%20image%2020251001081708.png)

### HTTPS

![](assets/Pasted%20image%2020251001081735.png)

### Why TLS

- We encrypt with symmetric key algorithm (fast)
- We need to exchange the symmetric key
- Key exchange uses asymmetric key (PKI)
- Authenticate the server
- Extension (SNI, preshared, 0RTT)

### TLS 1.2

![](assets/Pasted%20image%2020251001082626.png)

- Heartbleed Openssl Bug ~ People managed to get the Private Key, effectively they could decrypt anything. https://www.heartbleed.com/
- It lacks forward secrecy, people can harvest data now, and decrypt later when they get hands on private key, they can decrypt older data.

### Diffie Hellman

Diffie-Hellman : https://www.youtube.com/watch?v=85oMrKd8afY
Elliptic Curve DHE

- Let's not share symmetric key at all,
- Let's only share parameters (certificates) enough to generate it
- Each party generates the same key
- Party one generate `X` number (private)
    - Also generates `g` and `n` (public, random and prime)
- Party two generates `Y` number (private)

![](assets/Pasted%20image%2020251001085358.png)


- Party 1 sends `g` and `n` to Party 2
- Anyone can sniff those values , fine.
- now both has `g` and `n`

- Party 1 takes `g` to the power of `X` `%n`
    - `g^X %n` is now a public value
    - cannot be broken to get `X`
- Party 2 does same with Y
    - `g^Y %n` is now a public value
    - cannot be broken to get Y
- Both party shares the new values

At each end

- Party 1 takes `Y` value and raises it to X
    - $(g^y \mod n)^x = g^{xy} \mod n$
- Party 2 takes `X` value and raises it to `Y`
    - $(g^x \mod n)^y = g^{xy} \mod n$
- Both now has the same value : $g^{xy} \mod n$
- This is the used as a seed for the key, and can be used to generate symmetric key.

#### MITM

- above strategy solves secrecy problem
- but if someone intercepts and puts their own DH Keys >
- MITM replaces Y's parameter with their own
- X doesn't know that happened (its just numbers)

#### Solution

- We bring back public key encryption
- But only to sign the entire DH message
- With certificates

## Certificates

- We need a way to proof authenticity
- Generate a pair of public/private key
- Put a public key in a certificate
- Put the website name in the certificate
- Sign the certificate with the private
- x509

![](assets/Pasted%20image%2020251001093140.png)

- Certificates can be *self-signed*
    - The private key signing the cert belong to the public key
    - Usually untrusted and used for testing/local
- Certificate can sign *other certificates*
    - Creating a trust chain
    - Issuer name is who issued it
    - Lets Encrypt
- Ultimately a ROOT cert is found
    - ROOT certs are always self signed
    - They are trusted by everyone
    - Installed with OS root (certificate store)

#### Certificate Verification

![](assets/Pasted%20image%2020251001093358.png)

Client receives the full chain, wants to verify A.com cert signature which as been signed by
CA public key issuer, so it gets the CA and gets the CAPUB to verify, but also it needs to
trust the CA cert so it, verifies that by getting the RootTrust public key and verifies it, but the
RootTrust is self signed so it looks up its local cert store. If it is there it is trusted. Else
rejected.

### TLS 1.3

![](assets/Pasted%20image%2020251001083155.png)


### More on TLS

- More stuff is sent in TLS Handshake
- TLS extensions
    - ALPN
    - SNI
- Cipher Algorithms
- Key generation Algorithms
- Key Size
- Digital Signature Algorithms
- Client side Certificates



How to send a Secret Message : https://www.youtube.com/watch?v=I6Unxb-PFhs

