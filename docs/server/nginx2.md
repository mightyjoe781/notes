### Nginx Quickly Setup a Static Website

NOTE : This guide assumes you have working nginx configuration and auto-renewal scripts setup correctly.

#### Step 1 : Register a Child Domain on your Domain Provider

Add one CNAME entry with following information to setup `prismo.minetest.in`

- Type : CNAME
- Host : prismo
- Value : `minetest.in.` (Notice the `.` at the end)
- TTL : 5min

Now wait for 2 minutes and try pinging to `prismo.minetest.in` to check if your domain has propogated to your server or not. Usually this is very fast now a days.

Now execute : `nslookup prismo.minetest.in` to check domain propogation.

Accessing `prismo.minetest.in` should throw 502 if nginx is correctly configured.

#### Step 2 : Setup nginx conf for `prismo.minetest.in`

- Create a simple `index.html` file with some content in `/var/www/prismo`
- We will use simple configs one by one.

Basic Config-1 : filename : `prismo.minetest.in.conf` in `/etc/nginx/conf.d/`

````nginx
server {
    listen 80;
    server_name ~^(www\.|)prismo\.minetest\.in$;

    access_log /var/log/nginx/prismo.minetest_access.log main;
    error_log  /var/log/nginx/prismo.minetest_error.log  info;
}
````

Save above configuration and run `service nginx restart` . This should give welcome message that nginx is configured correctly.

Basic Config-2 : same file

````nginx
server {
    listen 80;
    server_name ~^(www\.|)prismo\.minetest\.in$;

    access_log /var/log/nginx/prismo.minetest_access.log main;
    error_log  /var/log/nginx/prismo.minetest_error.log  info;
		# this is a redirect rule to https
    return 301 https://prismo.minetest.in$request_uri;
}

#---------------------------------------------------------------------

server {
    listen 443 ssl;
    server_name ~^prismo\.minetest\.in$;

    access_log /var/log/nginx/prismo_error.log main;
    error_log  /var/log/nginx/prismo_error.log  info;
		# NOTE Keep these commented out for now until we obtain certs from runlets perl script.
    # ssl_certificate     /var/letse/smk/certificates/prismo.minetest.in.crt ;
    # ssl_certificate_key /var/letse/smk/certificates/prismo.minetest.in.key ;

    location ^~ /.well-known/acme-challenge/ {
        default_type "text/plain";
        root /var/www/tmp;
        allow all;
    }

    location = /.well-known/acme-challenge/ {
        return 404;
    }

    set $docdir /var/www/prismo;
    include /etc/nginx/local/common.conf;
    root $docdir;

# Add any useful rewrite rules below.
#
}
````

Now save this config and again access `prismo.minetest.in` . You will get a certificate warning and proceed with above setup to check if your html page is rendered properly or not.

You could render your html page on `http` if you move setdirectory directives in http config portion. And note certs are commented out because they do not exist yet !

Confirm : If your http is redirected to https and page loads correctly, ignore secure website warnings for now.

#### Step 3: Generating certs for the above domain

NOTE: nginx must be up for perl script solver to work

Now if you have recieved bundle of scripts from this website then there should be a `runlets` perl script, Its basically a certificate solver and generates certificate for our domain.

Add your new domain `prismo.minetest.in` and run the script. Wait for it to resolve and generate certificate.

Uncomment certs line from above script and execute `service nginx restart` again. If there is no specific error from nginx then you have setup everything correctly and use a browser to navigate to `http://prismo.minetest.in` and it should redirect to `https://prismo.minetest.in` with valid certs.

#### Step 4 : Adding your website

Now you can drop in your static website to `/var/www/prismo/` directory tree and nginx will take care of rest.

As usual setup I generally have a folder for static files locally and I create a deploy script file with two commands, one generates the static files/builds website and another rsyncs that into the server.

Example npm build website.

````bash
#!/bin/sh
npm run build && rsync -avz --delete build/ mtboxroot:/var/www/prismo/
exit 0
````

Note here `mtboxroot` is derived from the `.ssh/config` file.