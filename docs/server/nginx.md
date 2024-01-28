### Nginx

This part  assumes  that you know the  basics of  "nginx" setup.  If this isn't the case, you can skip this step until later.

`setupdoc/files/` includes a tarball named "nginx-base.tar.gz".  The tarball contains a directory tree named `nginx/`.

Execute:

    service nginx stop

Replace the directory tree `/etc/nginx/` with the `nginx/` directory tree in the tarball.

Replace the `.conf` files in `/etc/nginx/ with  similar files named after domains that you control and have pointed  to the current box.

 Edit the files and make the appropriate changes.

If you don't already have certs in `/var/letse/`  for all of the domains that you use, disable the use of SSL in the associated `.conf` files.

Edit  the script file `/etc/nginx/local/runletse*.pl`.  Make the appropriate changes.

Execute this command to restart "nginx":

    service nginx restart

If errors occur, do this:

    systemctl status nginx.service >& /tmp/nginx.err

Review  the contents of `/tmp/nginx.err`.  If possible,  correct the indicated problems and try to start "nginx" again.

#### Step: Set up automated SSL certs renewal

NOTE: requires lego to be installed from [here](applications.md)

Create  a text file  named "/etc/cron.weekly/renew-letse"  with  the following contents:

````bash
#!/bin/bash -e
cd /etc/nginx/local/ || exit 1
perl runletse.pl > /tmp/renew-letse.log 2>&1 &
exit 0
````

Make the file executable. I.e.:

`chmod 755 /etc/cron.weekly/renew-letse`