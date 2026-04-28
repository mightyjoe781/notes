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
| `-O` | save with remote filename |
| `-s` | silent (no progress bar) |
| `-v` | verbose (request and response headers) |
| `-I` | fetch headers only (HEAD request) |
| `-L` | follow redirects |
| `-u user:pass` | basic auth |
| `-k` | skip TLS certificate verification |
| `-w "%{http_code}"` | print response code |
| `--compressed` | request gzip-compressed response |
| `-x proxy:port` | use proxy |

### Basic Requests

```bash
# GET
curl https://example.com/api/users

# Follow redirects, show response code
curl -Ls -o /dev/null -w "%{http_code}" https://example.com

# HEAD - check if URL exists
curl -I https://example.com

# POST with JSON body
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'

# POST form data
curl -X POST https://example.com/login \
  -d "username=alice&password=secret"

# PUT
curl -X PUT https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Updated"}'

# DELETE
curl -X DELETE https://api.example.com/users/1

# With Bearer token
curl https://api.example.com/me \
  -H "Authorization: Bearer eyJhbGci..."

# With API key header
curl https://api.example.com/data \
  -H "X-API-Key: abc123"
```

### File Operations

```bash
# Download file
curl -O https://example.com/file.tar.gz

# Download and rename
curl -o myfile.tar.gz https://example.com/file.tar.gz

# Download with progress bar
curl --progress-bar -O https://example.com/large.iso

# Resume interrupted download
curl -C - -O https://example.com/large.iso

# Upload file (multipart form)
curl -F "file=@/path/to/local/file.txt" https://example.com/upload

# Upload raw binary
curl -X PUT --data-binary @file.bin https://example.com/upload
```

### Debugging

```bash
# Verbose - shows request and response headers
curl -v https://example.com

# Show only response code
curl -s -o /dev/null -w "%{http_code}" https://example.com

# Measure timing
curl -s -o /dev/null -w "
  dns:   %{time_namelookup}s
  conn:  %{time_connect}s
  ttfb:  %{time_starttransfer}s
  total: %{time_total}s
" https://example.com

# Write response and headers to files separately
curl -s -D headers.txt -o body.json https://api.example.com
```

### Config and Aliases

```bash
# ~/.curlrc - default options
--silent
--show-error
--location

# Useful aliases
alias curljson='curl -H "Content-Type: application/json" -H "Accept: application/json"'
alias curltime='curl -s -o /dev/null -w "total: %{time_total}s\n"'
```

### Tips

- Use `-s --show-error` in scripts: no progress bar but errors still print
- Pipe to `jq` for readable JSON: `curl -s api.example.com | jq .`
- `curl -K credentials.txt` reads flags from a file (keep secrets out of shell history)
- For large downloads consider `wget -c` or `aria2c` (parallel chunks)

### See Also

- [OpenSSL](openssl.md) for TLS certificate generation
- Also: httpie (`http`), wget (simpler downloads), aria2 (parallel downloads), xh (fast httpie alternative)
