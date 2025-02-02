# OpenSSL

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

````bash
sudo apt update
sudo apt install openssl
````

### Common Usage

#### Generate a Private Key

````bash
# RSA Key
openssl genpkey -algorithm RSA -out private.key

# EC Key
openssl ecparam -genkey -name secp384r1 -out ec.key
````

#### Generate a CSR (Certificate Signing Request)

````bash
openssl req -new -key private.key -out request.csr
````

#### Create a self-signed Certificate

````bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
````

#### Convert Certificate Formats

````bash
# PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der

# DER to PEM
openssl x509 -inform DER -in cert.der -out cert.pem
````

#### Verify a Certificate

````bash
# verify details
openssl x509 -in cert.pem -text -noout

# verify cert chain
openssl verify -CAfile ca.crt cert.pem
````

#### Encrypt and Decrypt Files

````bash
# encrypt a file
openssl enc -aes-256-cbc -salt -in file.txt -out file.enc

# decrypt a file
openssl enc -d -aes-256-cbc -in file.enc -out file.txt
````

### Advanced Usage

#### Create a PKCS#12 Bundle

````bash
# bundle cert and key
openssl pkcs12 -export -in cert.pem -inkey key.pem -out bundle.p12

# extract from pkcs#12
openssl pkcs12 -in bundle.p12 -out cert.pem -nodes
````

#### Generate DH (Diffie-Hellman) Params file

````bash
openssl dhparam -out dhparam.pem 2048
````

### Example

#### Block unwanted DNS resolution by port scanners

Issue a fake certificate with `example.com` to prevent Censys like services to resolve domain names from nginx-default redirects.

````bash
# 100 yrs self-signed valid certificate
sudo openssl req -x509 -nodes -days 36500 -newkey rsa:2048 \
  -keyout /etc/ssl/nginx/self-signed.key \
  -out /etc/ssl/nginx/self-signed.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN=example.com"
````

Edit `/etc/nginx/sites-available/default`

````nginx
## save following contents to /etc/nginx/sites-available/default
# this prevent domain name leak and default forwarding from ip
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	root /var/www/html;
  
	# Add index.php to the list if you are using PHP
	index index.html index.htm index.nginx-debian.html;
	server_name _;

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
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

### Resources

* https://www.feistyduck.com/library/openssl-cookbook/

### Tips

* Automate Cert Generation : Use Scripts to automate CSR and certificate generation
* Use *Let’s Encrypt* : provides free SSL/TLS certificates
* Monitor Cert Expiry: Use tools like `certbot renew` or `cron` to automate renewal
