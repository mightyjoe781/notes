# Debugging

## Tier 1: Browser DevTools

- `Ctrl + Shift + I`: Open Chrome Developer Tools
- Switch to the Network tab
    - Preserve Log: preserves log across redirects
    - Disable Cache: removes cached responses
- Select a request to view details:
    - Request
    - Response
    - Waterfall

Request Waterfall Diagram

![](assets/Pasted%20image%2020251006075622.png)

Broadly divided into three parts:

- Resource Scheduling
- Connection Start
- Request/Response

Example:

![](assets/Pasted%20image%2020251006081018.png)

Documentation: https://developer.chrome.com/docs/devtools/network/reference

#### Identifying Slow Server Processing

**Waiting for server response** — time between the request being received and the first byte of the response. A slow server (e.g., one that sleeps before replying) will inflate this metric.

#### Identifying Slow Network / Download Issues

**Content Download** — time taken to receive the response body after the server starts sending. A slow server that trickles data (e.g., sleeps between chunks) will show a long content download time.

#### Identifying Slow Connection Establishment

**Initial Connection** — time to complete the TCP handshake. If the accept queue is full, the server makes the client wait before the connection is accepted.

- macOS: `netstat -Lan` — view accept queue and backlog
- Linux: `ss -ltn`

#### Identifying Slow DNS / TLS

Use a VPN to simulate high-latency DNS or TLS scenarios.

Example Code: https://github.com/hnasr/backend-analysis-course/tree/main/thecwebserver-code

## Tier 2: MITM Proxy

Popular tools:

- Fiddler
- Burp Suite
- mitmproxy (`brew install mitmproxy`)

```bash
mitmproxy --listen-host 127.0.0.1 -p 8181

curl http://localhost:8080

curl -x http://localhost:8181 http://example.com

curl -x http://localhost:8181 https://example.com
```

HTTPS interception fails by default because the client does not trust mitmproxy's certificate. Install the mitmproxy CA certificate to fix this:

```bash
sudo security add-trusted-cert -d -p ssl -p basic -k /Library/Keychains/System.keychain ~/.mitmproxy/mitmproxy-ca-cert.pem

curl -x http://localhost:8181 https://example.com
```

Reference: https://docs.mitmproxy.org/stable/concepts/certificates/

`mitmweb` provides a browser-based UI for the same functionality. The proxy can also intercept mobile traffic by connecting the device to the same Wi-Fi and configuring it to use the proxy.

## Tier 3: Wireshark

Wireshark inspects traffic at the network interface level. To decrypt TLS traffic, export the session keys from curl and load them into Wireshark:

```bash
export SSLKEYLOGFILE=/tmp/wireshark/tlskey
```

In Wireshark: **Preferences → TLS → (Pre)-Master-Secret log filename** → point to the key file.

ISPs can see the Server Name Indication (SNI) header in TLS handshakes even though the payload is encrypted, which is how domain-level blocking works.
