# nginx

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

````bash
# dependencies
sudo apt install curl gnupg2 ca-certificates lsb-release debian-archive-keyring

# nginx signing key to verify installation
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null

# verify key
gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg

# optional: add nginx stable to sources in apt repo
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list
    
# installing
sudo apt update
sudo apt install nginx
````

### Setup

Edit `/etc/nginx/nginx.conf`

````nginx
# add in http block
http {
  	# default options
  	...
    # modified options
    add_header X-Frame-Options "SAMEORIGIN";
    include /etc/nginx/sites-available/default;
    include /etc/nginx/conf.d/*.conf;
}

````

Create a `/etc/nginx/local/common.conf`

````nginx
#---------------------------------------------------------------------
# Start of "common.conf".

#---------------------------------------------------------------------
# SSL settings.

# The  "dhparam.pem" file is  created using a script  that is provided
# separately.

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;

#---------------------------------------------------------------------
# Strict Transport Security.

# If  you've  got a site  that needs to support  "http"  as opposed to
# "https", you'll need to set that site up differently.

    add_header Strict-Transport-Security max-age=15768000;

#---------------------------------------------------------------------
# PHP.

location ~ \.php8?$ {
    location ~ \..*/.*\.php8$ { return 404; }
    root $docdir;
    try_files $uri =404;
#   fastcgi_pass 127.0.0.1:9000;
    fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME
    $document_root$fastcgi_script_name;
    include fastcgi_params;
}

#---------------------------------------------------------------------
# Misc. safety measures and/or tweaks.

location / {
    root $docdir;
    index index.php index.html index.htm;
}

location ~* ^.+.(jpg|jpeg|gif|css|png|js|ico|xml)$ {
    root $docdir;
    access_log off;
}

location ~ /\.ht {
    deny all;
}
# add other services like censys to stop them from scanning
if ($http_user_agent ~* (IndeedBot)) {
    return 403;
}

# if ($bad_referer) {
#     return 444;
# }

location ~ /.well-known {
    allow all;
}

# To allow POST on static pages
error_page 405 =200 $uri;

#---------------------------------------------------------------------
# End of "common.conf".
````

Create a default server blocks in 

````nginx
# Virtual Host configuration for example.com
#
# You can move that to a different file under sites-available/ and symlink that
# to sites-enabled/ to enable it.
#
server {
	listen 80;
	listen [::]:80;

	server_name example.com;

	root /var/www/example.com;
	index index.html;

	location / {
		try_files $uri $uri/ =404;
	}
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    server_name _;

    ssl_certificate /etc/nginx/ssl/self-signed.crt;
    ssl_certificate_key /etc/nginx/ssl/self-signed.key;

    access_log /var/log/nginx/default_ssl_access.log;
    error_log /var/log/nginx/default_ssl_error.log;

    return 444;  # Drop the connection
}
````



Create `minetest.in.conf` in `/etc/nginx/conf.d/`

````nginx
# detect http[s]://www. access to server and redirect to http[s]://minetest.in
server {
    listen 80;
  	listen 443;
		# detect http[s]://www. access to server
    server_name ~^www\.minetest\.in$;

    access_log /var/log/nginx/minetest_access.log main ;
    error_log  /var/log/nginx/minetest_error.log  info ;

    ssl_certificate     /var/letse/smk/certificates/minetest.in.crt ;
    ssl_certificate_key /var/letse/smk/certificates/minetest.in.key ;
	
  	# forward to https
    return 301 $scheme://minetest.in$request_uri;
}
# handle http/https
server {
    listen 80;
    listen 443 ssl;
    server_name ~^minetest\.in$;

    access_log /var/log/nginx/minetest_access.log main ;
    error_log  /var/log/nginx/minetest_error.log  info ;

    ssl_certificate     /var/letse/smk/certificates/minetest.in.crt ;
    ssl_certificate_key /var/letse/smk/certificates/minetest.in.key ;

    location ^~ /.well-known/acme-challenge/ {
        default_type "text/plain";
        root /var/www/tmp;
        allow all;
    }

    location = /.well-known/acme-challenge/ {
        return 404;
    }

    set $docdir /var/www/minetest.in;
    include /etc/nginx/local/common.conf;
    root $docdir;
}
````

### Examples

#### Serving Static Content

````bash
server {
    location / {
        root /data/www;
    }

    location /images/ {
        root /data;
    }
}
````

#### Simple Proxy Server

````nginx
server {
    location / {
        proxy_pass http://localhost:8080/;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
````

#### Simple FastCGI Proxying

````bash
server {
    location / {
        fastcgi_pass  localhost:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param QUERY_STRING    $query_string;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
````

### Resources

* https://nginx.org/en/docs/beginners_guide.html

* [Server Nginx Setup Guide 1](../server/nginx.md)
* [Server Nginx Setup Guide 2](../server/nginx2.md)