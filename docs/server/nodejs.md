### Serve `node.js` apps by `https`

The best way to serve "node.js" apps by "https" (as opposed to "http") is probably as follows.

The advantages of this approach are significant:

* You  can  run an app as an ordinary user but serve it using  "https" regardless (despite port 443 being a privileged port).

* "nginx" and the app won't conflict.  Instead, they'll work together. "nginx" will take care of the "https" part for the app.

* You  don't  need to  deal with SSL certs or  "https" code at the app level.

a. Write  an old-fashioned "http"-based "node.js" app.  I.e. Don't use "https" or certs at the "node.js" level.

b. The app should listen to IPV4 address 127.0.0.1 and use an unprivileged port; i.e., a port in the 1,000s.

c. Serve the app. For example:

    node app.js

d. On the  same box,  confirm that the app can be accessed locally using "lynx". For example:

    lynx http://127.0.0.1:5000/

Substitute the appropriate "node.js" app port for 5000.

e. Set  up an  "http"-only  server using "nginx" and a  "server" block similar to the following.

    server {
        listen 80;
        server_name ~^moo\.cow\.milk$;
    access_log /var/log/nginx/moo_cow_milk_access.log main;
    error_log  /var/log/nginx/moo_cow_milk_error.log  info;
    
    location / {
        proxy_set_header   X-Forwarded-For $remote_addr;
        proxy_set_header   Host $http_host;
        proxy_pass         http://127.0.0.1:5000;
    }
    }
Modify "moo\.cow\.milk" to match a domain name  you control which points to the current box.

Substitute the appropriate "node.js" app port number for 5000.

f. Restart "nginx":

    sudo service nginx restart

If everything is working, the  following command should now be able to access  the  "node.js" app using the indicated domain, "http", and the default "http" TCP port (80):

    lynx http://moo.cow.milk/

Substitute the appropriate domain name for "moo.cow.milk".

g. If  you don't already have SSL cert files for the domain name used, obtain them at this point.

Integrate the appropriate SSL settings and code into the "nginx" "server" block that you created previously.

The  procedures  used for this step are  beyond the scope of this discussion.  However, the final version of the "nginx" server block might look something like this:



    server {
        listen 80;
        listen 443 ssl;
        server_name ~^moo.cow.milk$;
    access_log /var/log/nginx/moo_cow_milk_access.log main;
    error_log  /var/log/nginx/moo_cow_milk_error.log  info;
    
    ssl_certificate     /var/letse/farmer/certificates/moo.cow.milk.crt ;
    ssl_certificate_key /var/letse/farmer/certificates/moo.cow.milk.key ;
    
    location ^~ /.well-known/acme-challenge/ {
        default_type "text/plain";
        root /var/www/tmp;
        allow all;
    }
    
    location = /.well-known/acme-challenge/ {
        return 404;
    }
    
    location / {
        proxy_set_header   X-Forwarded-For $remote_addr;
        proxy_set_header   Host $http_host;
        proxy_pass         http://127.0.0.1:5000;
    }
    
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    
    add_header Strict-Transport-Security max-age=15768000;
    }
h. Restart "nginx":

    sudo service nginx restart

If everything is working, the  following command should now be able to access the  "node.js" app using the indicated domain, "https", and the default "https" TCP port (443):

    lynx https://moo.cow.milk/

Substitute the appropriate domain name for "moo.cow.milk".

Chromium and other major browsers should be able to access the indicated URL as well.

