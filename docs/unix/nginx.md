# Nginx

[:octicons-arrow-left-24:{ .icon } Back](index.md)

High-performance web server and reverse proxy. Also used for load balancing, SSL termination, and static file serving.

### Installation

```bash
sudo apt install nginx
sudo systemctl enable --now nginx
nginx -v                             # check version
```

### File Layout

| Path | Purpose |
|---|---|
| `/etc/nginx/nginx.conf` | main config |
| `/etc/nginx/sites-available/` | server block definitions |
| `/etc/nginx/sites-enabled/` | symlinks to active configs |
| `/etc/nginx/conf.d/` | additional configs (auto-included) |
| `/var/log/nginx/access.log` | access log |
| `/var/log/nginx/error.log` | error log |
| `/var/www/html/` | default web root |

### Core Commands

```bash
nginx -t                             # test config syntax
sudo nginx -s reload                 # reload config without downtime
sudo systemctl restart nginx         # full restart
sudo tail -f /var/log/nginx/error.log
```

### Server Blocks

#### Static site

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

#### Redirect HTTP to HTTPS

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

#### HTTPS with SSL

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

#### Reverse proxy to upstream app

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Serve static files and proxy API

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/app;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Load Balancing

```nginx
upstream backend {
    least_conn;                       # or: round_robin (default), ip_hash
    server 10.0.0.1:3000;
    server 10.0.0.2:3000;
    server 10.0.0.3:3000 backup;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### Security Headers

```nginx
server {
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
    add_header Content-Security-Policy "default-src 'self'";

    # Hide nginx version
    server_tokens off;
}
```

### Rate Limiting

```nginx
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
        }
    }
}
```

### Useful Config Snippets

```nginx
# Gzip compression
gzip on;
gzip_types text/plain application/json application/javascript text/css;
gzip_min_length 1024;

# Cache static assets
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# Block access to dotfiles
location ~ /\. {
    deny all;
}

# Custom error pages
error_page 404 /404.html;
error_page 500 502 503 504 /50x.html;
```

### Let's Encrypt / Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
sudo certbot renew --dry-run               # test auto-renewal
```

### Tips

- Always run `nginx -t` before reloading - a bad config will fail silently on `reload`
- Use `include /etc/nginx/snippets/ssl.conf;` to share SSL settings across vhosts
- Enable sites: `ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/`
- `access_log off;` in static asset locations reduces disk I/O

### See Also

- Also: Caddy (auto HTTPS, simpler config), Traefik (dynamic config for containers), HAProxy (high-performance load balancing), Apache
