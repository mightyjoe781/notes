# curl

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Command-line HTTP client. Essential for testing APIs, downloading files, and scripting HTTP workflows.

### Installation

```bash
sudo apt install curl
```

### Common Options

| Flag | Description |
|---|---|
| `-X METHOD` | HTTP method (GET, POST, PUT, DELETE, PATCH) |
| `-H "Header: val"` | add request header |
| `-d "data"` | request body (implies POST) |
| `-o file` | save output to file |
| `-O` | save with remote filename (from URL path) |
| `-s` | silent (no progress bar) |
| `-v` | verbose (full connection detail, TLS handshake) |
| `-I` | fetch headers only (HEAD request) |
| `-i` | include response headers in output |
| `-L` | follow redirects |
| `-u user:pass` | basic auth |
| `-k` | skip TLS certificate verification |
| `-w "%{http_code}"` | print response code |
| `--compressed` | request gzip-compressed response |
| `-x proxy:port` | use proxy |

---

### Basic Requests

```bash
# GET - returns raw HTML or JSON
curl https://example.com

# Headers only
curl -I https://example.com
# HTTP/2 200
# content-type: text/html

# Follow redirects (useful when HTTP redirects to HTTPS)
curl -L http://example.com

# Verbose - shows TLS handshake, headers, everything
curl -v https://example.com

# Skip TLS verification (self-signed certs, local dev)
curl -k https://self-signed.example.com
```

---

### Save Output to File

```bash
# Save to named file
curl -o page.html https://example.com

# Save using filename from URL path
curl -O https://example.com/index.html    # saves as index.html

# Resume interrupted download
curl -C - -O https://example.com/large.iso
```

---

### Multiple URLs and Globbing

```bash
# Hit two URLs in one command
curl https://api.example.com/users/1 https://api.example.com/users/2

# Range glob - hits /users/1 through /users/5
curl https://api.example.com/users/[1-5]

# List glob
curl https://api.example.com/users/{alice,bob,carol}
```

---

### APIs

```bash
# POST with form data (default when using -d)
curl -d "name=Alice&age=30" https://api.example.com/users
# returns: {"status": "created"}

# POST with JSON body
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "age": 30}'

# PUT
curl -X PUT https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Updated"}'

# DELETE
curl -X DELETE https://api.example.com/users/1

# With Bearer token
curl https://api.example.com/me \
  -H "Authorization: Bearer eyJhbGci..."
```

---

### Host and DNS Manipulation

Useful for testing locally before DNS propagates or behind load balancers.

```bash
# Fake the Host header (app expects a specific hostname)
curl http://127.0.0.1 -H "Host: example.com"

# Override DNS resolution (connect to localhost but act as if it's example.com)
curl https://example.com --resolve example.com:443:127.0.0.1

# Connect to a specific backend host (useful behind LBs)
curl https://example.com --connect-to example.com:443:backend-1.internal:443
```

---

### Other Protocols

curl supports protocols beyond HTTP.

```bash
# Test if a TCP port is open (useful when telnet isn't available)
curl telnet://localhost:4317
# Connected to localhost.

# Dictionary lookup
curl dict://dict.org/d:dog

# Send email via SMTP
curl smtp://mail.example.com \
  --mail-from sender@example.com \
  --mail-rcpt recipient@example.com \
  --upload-file email.txt
```

---

### Debugging

```bash
# Show only response code
curl -s -o /dev/null -w "%{http_code}" https://example.com
# 200

# Measure timing
curl -s -o /dev/null -w "
  dns:   %{time_namelookup}s
  conn:  %{time_connect}s
  ttfb:  %{time_starttransfer}s
  total: %{time_total}s
" https://example.com

# Save response body and headers to separate files
curl -s -D headers.txt -o body.json https://api.example.com
```

---

### File Uploads

```bash
# Multipart form upload
curl -F "file=@/path/to/file.txt" https://example.com/upload

# Raw binary upload
curl -X PUT --data-binary @file.bin https://example.com/upload
```

---

### Tips

- `curl http://example.com` defaults to HTTP and won't follow a redirect to HTTPS - add `-L`
- `-k` is safe for local dev/testing; never use it against production endpoints
- Use `-s --show-error` in scripts: suppresses progress bar but still prints errors
- `-v` shows the TLS handshake step-by-step - first place to look when SSL fails
- Pipe to `jq` for readable JSON: `curl -s api.example.com | jq .`
- `curl -K credentials.txt` reads flags from a file (keeps secrets out of shell history)

### See Also

- [jq](jq.md) - parse and filter JSON responses
- [OpenSSL](openssl.md) for TLS certificate generation
- Also: httpie (`http`), wget (simpler downloads), xh (fast httpie alternative)
