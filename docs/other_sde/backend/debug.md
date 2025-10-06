# Debugging


## Tier 1 Analysis DevTools

- `Ctrl + Shift + I` : Open Chrome Developer Tools
- Switch to Network Tab
    - Preserver Log ~ preserves log following redirects
    - Disable Cache ~ remote unnecessary caching
- Select a Request to view more details like
    - Request
    - Response
    - Waterfall

Request Waterfall Diagram

![](assets/Pasted%20image%2020251006075622.png)

Broadly divided in three parts

- Resource Scheduling
- Connection Start
- Request/Response

Example : 

![](assets/Pasted%20image%2020251006081018.png)

Documentation : https://developer.chrome.com/docs/devtools/network/reference

#### Identifying Slow Processing Request

Waiting for server response ~ time we wait for server to process and return response, once it has received the request. If server is slow in terms of creating the response, this time will indicate this.
Example ~ server sleeps for 2 seconds before replying

#### Identifying Slow Network Speed & Download/Streaming Issue

Content Download ~ will very upon size of content sent from server, post processing (after we wait for server response). Now server can send this content very slowly increasing content download time.
Example ~ server sends that response content-length is 14 bytes, but sleeps in between every 5 bytes.

#### Identifying Slow Connection Establishment

Initial Connection : This indicates how much time it takes to setup the initial connection, a good example of this is lets say in accept queue is full, and server makes you wait before it gets a space for your connection to be put in the accept queue.

One Mac you can use `netstat -Lan` to see accept queue and backlogs.
on Linux ~ `ss -ltn`

#### Identify slow DNS/TLS

Use VPN to simulate this scenario.

Example Code : https://github.com/hnasr/backend-analysis-course/tree/main/thecwebserver-code

## Tier 2 : MITM Proxy

- Popular Tools
    - Fiddler
    - Burpsuite
    - MITM proxy (`brew install mitmproxy`)

```bash

mitmproxy --listen-host 127.0.0.1 -p 8181

# mitmproxy -b ip_address -p port

curl http://localhost:8080 # doesn't respect proxy by default

curl -x http://localhost:8181 http://example.com

curl -x http://localhost:8181 https://example.com # fails
# because we don't trust mitmproxy's root certificate to be same as example.com :)

# correct way is to download and use mitmproxy Certificate Authority

# https://docs.mitmproxy.org/stable/concepts/certificates/

sudo security add-trusted-cert -d -p ssl -p basic -k /Library/Keychains/System.keychain ~/.mitmproxy/mitmproxy-ca-cert.pem

## now try again

curl -x http://localhost:8181 https://example.com
```

Try above things with `mitmweb` : A web frontend for above cli application.

Try setting up proxy on mobile by connecting  mobile to the same wifi and configuring the proxy.
## Tier 3 : Wireshark

Wireshark is industry recognised tool for inspecting the data at interface level. There is nothing hidden from Wireshark.

To configure wireshark to inspect to encrypted SSL traffic use following commands to export a encryption key from curl, and load the same key back in Wireshark to allow decrypting of the packets.

```bash
export SSLKEYLOGFILE=/Users/smk/home/wireshark/tlskey
```

```text
# open wireshark
# Preferences
# TLS > Master Secret Path
```

Ideally ISP can't see the encrypted packets, only way they block domain, using server name indication headers, where server names are listed.

