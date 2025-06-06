### VPS Setup Redacted (smk)

Assuming you got root password from some vnc console in freshly installed VPS. Let’s setup.

### Setup Locale

````bash
# create locale file
echo "export LC_ALL=C" > /etc/profile.d/lc_all.sh
exec bash
````

````c++
# relogin and check
locale
````

### Upgrade System

````bash
apt update
apt upgrade
# to upgrade the distro
apt-get dist-upgrade
````

### Install Basic Tools

````bash
apt-get install sudo stow vim net-tools
````

### Add user & grant sudo

````bash
user=smk
adduser $user
# grant sudo
usermod -a $user -G sudo
# add basic authorized keys
cd /home/$user
mkdir -p .ssh
chmod 700 .ssh
echo "YOUR_KEY" > .ssh/authorized_keys
chown -R $user:$user /home/$user

# try now ssh thru this user
````

### SUDO without password

Create a file named `90-cloud-init-users`.

````bash
touch 90-cloud-init-users
chmod 440 90-cloud-init-users
````

Put following text in it.

````bash
root ALL=(ALL) NOPASSWD:ALL
smk ALL=(ALL) NOPASSWD:ALL
````

now copy this file to `/etc/sudoers.d`

***Warning :*** This step if not done properly can brick the box!

Also do not edit the file once its in directory. This may also brick the box. Safest way is to edit is somewhere else and then copy result into the directory in question

### Harden Security

````bash
# disable root login with password
# vi /etc/ssh/sshd_config

Port 23415
PasswordAuthentication no
````

````bash
service sshd restart
````

This sets up our box in safe state to use. Disable RootLogin as well if you want extra security.

### Setting up fail2ban

Alternate: https://github.com/skeeto/endlessh?tab=readme-ov-file

````bash
sudo apt install fail2ban sendmail-bin sendmail
# you can edit this .local because it overrides the default conf
cp /etc/fail2ban/fail2ban.conf /etc/fail2ban/fail2ban.local
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# to view your chain traffic drop configuration
iptables -L f2b-sshd -v -n --line-numbers
# to delete a rule applied to an IP address
iptables -D chain rulenum
````

````bash
# some jail settings all things are pretty well documented and we care about these
# https://www.linode.com/docs/guides/using-fail2ban-to-secure-your-server-a-tutorial/
ignoreip = 127.0.0.1/8 123.45.67.89
bantime  = 600
findtime = 600
maxretry = 3

# to check status
fail2ban-client status
````

<hr>
### Setup DNS

TODO : Add domain setup steps here before

NOTE : if your domain hostname is set but domain doesn’t point the server then you will always get an error regarding resolv.conf referring to host not found. To fix make sure hostname domain actually points the server you are setting up a dns.

````bash
# install dnsmasq
sudo apt-get install dnsmasq

# replace the default DNS generated by solus VM in Racknerd
echo "nameserver 127.0.0.1" > /tmp/resolv.conf
cp /tmp/resolv.conf /etc/resolv.conf
# lock the file, you can't edit it unless you do chattr -i
chattr +i /etc/resolv.conf

# note backup contens of resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
````

````bash
# put the following text in /etc/dnsmasq.conf
echo "all-servers
cache-size=10000
log-queries
interface=lo
no-resolv

address=/bacon.eggs/2.3.4.5

server=208.67.220.220           # OpenDNS
server=8.8.8.8                  # Google
server=1.1.1.1" > /tmp/dnsmasq.conf

cp /tmp/dnsmasq.conf /etc/dnsmasq.conf
````

````bash
sudo service dnsmasq restart
````

`dnsmasq` is a caching DNS server. To flush the cache, restart the `dnsmasq` service.

````bash
# check if this is resolved correctly
nslookup bacon.eggs
````

### Setup Hostname

````bash
DOMAIN=somedomain.com
hostname $DOMAIN
echo     $DOMAIN > /etc/hostname
````

<hr>
### Generate `dhparam.pem`

Execute the following command and wait for it to finish. For a high-end box, use 4096 here instead of 2048. Don’t try to use 4096 on a low-end or medium-level box.

````bash
openssl dhparam -out dhparam.pem 2048 >& /tmp/dhparam.log
````

Subsequent to completion, check the output and confirm that no errors occurred.

`cat /tmp/dhparam.log`

Then : 

````bash
mkdir -p       /etc/ssl/certs/
rm    -fr      /etc/ssl/certs/dhparam.pem
mv dhparam.pem /etc/ssl/certs/
````

This is required for setting up ssl certs for websites.

### Setup Ngnix

````bash
# install nginx
sudo apt-get install nginx
# visit your domain/ip that points to box and you should be greeted with nginx page
````

````
# generate a 100 yr dummy certs
# creating dummy certs to be used to hide domain reference from ip scans
sudo openssl req -x509 -nodes -days 36500 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/self-signed.key \
  -out /etc/nginx/ssl/self-signed.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN=example.com"
````

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

More on this Page : [Pre-requiste](#Installing lego) 

See Also : 

* [Setting up Nginx](nginx.md)
* [Setting up Static Site on Nginx](nginx2.md)
* [Setting up a dynamic site on Nginx](nginx3.md)

<hr>
### Setting up source paths

````bash
#!/bin/bash -e
mkdir -p /opt/minetest/mtbin
mkdir -p /opt/smkbin
````

Create a text file `/etc/profile.d/smkbin.sh` containing : 

NOTE : Don’t use `#!/bin/bash -e` here.

````bash
for dir in \
	/opt/minetest/mtbin \
	/opt/minetest/smkbin \
	/opt/smkbin
do
	if [ -d $dir ]; then PATH=$dir:$PATH; fi
done
````

This file needs to be readable, but it doesn’t need to be executable.

Make this available for root as well.

##### Edit `secure_path` setting in `etc/sudoers` to prepend directories from preceding scripts which exists. Note use `visudo` to edit the file.

```
secure_path="/opt/minebest/mtbin:/opt/smkbin:/usr/local/sbin:..."
```

Log-out and back in. You can now add useful scripts and tools to the two new directories.


### Application

#### Installing golang

````bash
#!/bin/bash -e
mkdir -p /opt/
cd       /opt/
rm -fr go golang
GOBALL=go1.21.6.linux-amd64.tar.gz

wget -c https://dl.google.com/go/$GOBALL
tar zxf $GOBALL
rm      $GOBALL
mv     go golang

mkdir -p                   /opt/smkbin/
ln -nsf /opt/golang/bin/go /opt/smkbin/
````

#### Installing lego

````bash
apt-get install binutils make git
````

````bash
#!/bin/bash -e
export GOPATH=/tmp/gobuild
GOPROG=$GOPATH/lego/dist/lego

rm -fr     $GOPATH
mkdir -p   $GOPATH
cd         $GOPATH

git clone https://github.com/go-acme/lego.git
cd lego
make build

strip      $GOPROG
# upx --lzma $GOPROG # for some reason upx is not packaged for bookworm
mv         $GOPROG /opt/smkbin/
rm -fr     $GOPATH
````

#### Set up `node`, `npm` and `yarn`

NOTE: Installs python3, gcc, g++ as well

````bash
#!/bin/bash -e
apt-get install curl software-properties-common -y
curl -sL https://deb.nodesource.com/setup_21.x | sudo bash -
apt-get update
apt-get install gcc g++ make nodejs -y
LINK="https://dl.yarnpkg.com/debian"

curl -sL $LINK/pubkey.gpg | sudo apt-key add -
echo "deb $LINK/ stable main" | \
    sudo tee /etc/apt/sources.list.d/yarn.list

apt-get update
apt-get -y install yarn
````

### Installing Docker on VPS

````bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
````

````bash
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
````

````bash
sudo apt-get install docker-ce
````

````bash
# managing docker as non root user
$USER=smk
sudo groupadd docker
sudo usermod -aG docker $USER
# refresh group
newgrp docker
# test docker run hello-world

# NOTE : fix .docker dir due to previous root runs if you get config errors
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R
````



### Installing PHP (Optional)

````bash
apt install php-common libapache2-mod-php php-mysql php-curl
````

NOTES: Manually building binary : [link](https://www.php.net/manual/en/install.unix.debian.php)

#### Add more PHP feature

NOTE : If nginx is not booting up due to port bind already in use, most likely its apache2 running disable it.

````bash
sudo systemctl disable apache2
sudo systemctl stop apache2
sudo service nginx start
````

````bash
#!/bin/bash -e
apt-get install \
    libmcrypt-dev  \
    php-apcu       php-bcmath     php-cli        php-common     \
    php-curl       php-dev        php-fpm        php-gd         \
    php-imagick    php-intl       php-json       php-ldap       \
    php-mbstring   php-mysql      php-pear       php-readline   \
    php-redis        php-soap       php-sqlite3    \
    php-xml        php-xmlrpc     php-zip
# note : php-smbclient is not working
pecl channel-update    pecl.php.net
pecl install channel://pecl.php.net/mcrypt-1.0.2
````

### Installing ntf

````bash
# refer https://github.com/hrntknr/ntf
sudo curl -L https://github.com/hrntknr/ntf/releases/download/v1.0.1/ntf-x86_64-unknown-linux-gnu -o /usr/local/bin/ntf
sudo chmod +x /usr/local/bin/ntf
echo -e 'backends: ["pushover"]\npushover: {"user_key": "t0k3n"}' > ~/.ntf.yml
ntf send test
ntf send -t BOX_SAYS_HELLO hello from box
````

### Alert on Reboot using ntf (systemd: don’t hate me)

````bash
touch /lib/systemd/system/reboot_ntf.service
echo "[Unit]
Description=ntf reboot script
After=network-online.target
Wants=network-online.target
[Service]
ExecStart=/bin/bash -c 'sleep 2 && /usr/local/bin/ntf send -t REBOOT minetest.in just rebooted! > /var/log/reboot_ntf.log 2>&1'
Type=oneshot
RemainAfterExit=true
Environment=HOME=/root/
[Install]
WantedBy=multi-user.target" > /lib/systemd/system/reboot_ntf.service

sudo systemctl enable reboot_ntf.service
sudo systemctl restart reboot_ntf.service
sudo chmod 644 /lib/systemd/system/reboot_ntf.service

# To create a generic service
# systemctl enable reboot_ntf.service
````

## Create a Backup (rclone-pcloud Setup)

#### Installing rclone

````bash
sudo apt-get install unzip -y
curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
unzip rclone-current-linux-amd64.zip
cd rclone-*-linux-amd64

# copy the binary
sudo cp rclone /opt/smkbin
sudo chown root:root /opt/smkbin/rclone
sudo chmod 755 /opt/smkbin/rclone

# install man page
sudo mkdir -p /usr/local/share/man/man1
sudo cp rclone.1 /usr/local/share/man/man1/
sudo mandb

# configure rclone
rclone config

# remote config for headless server : https://rclone.org/remote_setup/
# NOTE : choose advance config because pcloud has two regions
# so pass all default except region select it correctly

# testing if rclone works for remote name : pcloud
rclone lsd pcloud:
````

#### Backup Script

* [Backup using rclone](bkp.md)

````bash
#!/bin/bash
set -e
set -o pipefail

SERVER=$(hostname -s)
REMOTE="pcloud:vps_bkp/${SERVER}"
RCLONE_BIN=/opt/smkbin/rclone

MYDIR="/"
FILTER="/root/.dotfiles/conf/filter.txt"
VERBOSE=""	# Add verbose -v as needed
LOG="/tmp/rclone_log.txt"

WHOAMI=`whoami`
if [ "@$WHOAMI" \!= "@root"    ]; then
    echo Error: Must be run as root
    exit 1
fi

pushd ${MYDIR}

echo "Performing Sync to ${REMOTE}"
# Borg Handles Archiving VPS State, so just sync latest dir state
nice ${RCLONE_BIN} sync / ${REMOTE}/latest --filter-from ${FILTER} ${VERBOSE} --skip-links --update --use-server-modtime &>> ${LOG}
echo "Done"

popd
````

### Create a cron job

````bash
# you could wrap above script in ntfy and then setup a cron job
# open crontab file
crontab -e

# crontab for monthly execution
#0 0 1 * * /opt/smkbin/pcloud-bkp or
0 0 1 * * ntf -t MONTHLY_BACKUP done /opt/smkbin/pcloud-bkp
````

### Installing portainer & dockge

````bash
# using any one is fine
sudo mkdir -p /home/docker/dockge
sudo mkdir -p /home/docker/portainer
````

Create `compose.yml` in the portainer directory

````yaml
# be careful when setting up proxy_pass as it decides the uri_scheme traffic will be served on
# use https://127.0.0.1:6789/ if that is mapped inside container to 9443

version: "3.3"
services:
  portainer-ce:
    ports:
      - 8000:8000
      # - 6789:9000 : Note use this for serving portainer on HTTP
      - 9443:9443	# This is for HTTPS port
    container_name: portainer
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    image: portainer/portainer-ce:latest
volumes:
  portainer_data: {}
networks: {}
````

#### Setting up dockge

````yaml
version: "3.8"
services:
  dockge:
    image: louislam/dockge:1
    restart: unless-stopped
    ports:
      - 5678:5001
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./data:/app/data
      - /home/docker/dockge:/home/docker/dockge
    environment:
      # Tell Dockge where to find the stacks
      - DOCKGE_STACKS_DIR=/home/docker/dockge
````

### Installing Postgresql & pg-admin

````bash
sudo apt-get update && sudo apt-get install postgresql postgresql-contrib

# note by default postgres is not exposed to anyone outside localhost
# and it should be left this way, don't use connection from outside the box
# verify above by accessing /etc/postgresql/x.x/main/pg_hba.conf
local all postgres peer local all all peer host all all 127.0.0.1/32 md5 host all all ::1/128 md5

# neither root nor smk can access the psql (its good that way)
sudo su - postgres
psql
# create user for yourself
CREATE USER smk WITH PASSWORD 'your_password';
CREATE DATABSE test_db;
GRANT CONNECT ON DATABASE test_db TO smk;
GRANT USAGE ON SCHEMA public TO smk;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO smk;
# we granted everything to smk, but be careful to grant to other users
\q # to quit

# as user smk try to login
psql -h localhost -U smk -d test_db
````

````yml
# yaml for db
version: '3.8'

services:
  postgres:
    image: postgres:latest
    container_name: example-database
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: smk
      POSTGRES_PASSWORD: example-database-password
    ports:
      - "5433:5432"
    networks:
      - pg-network
    volumes:
      - pg-data:/var/lib/postgresql/data
      - ./initdb/:/docker-entrypoint-initdb.d/

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pg-admin
    environment:
      PGADMIN_DEFAULT_EMAIL: smk@minetest.in
      PGADMIN_DEFAULT_PASSWORD: admin_password_probably
    ports:
      - "5678:80"
    networks:
      - pg-network

networks:
  pg-network:

volumes:
  pg-data:
  
# create a script initdb/init-user-db.sh
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER "$POSTGRES_USER" WITH PASSWORD '$POSTGRES_PASSWORD';
  CREATE DATABASE "$POSTGRES_DB" WITH OWNER "$POSTGRES_USER";
  GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
EOSQL
````

### Installing JupyterHub

````bash
docker run -d -p 5678:8000 --name jupyterhub jupyterhub/jupyterhub jupyterhub
# enter in container
docker exec -it jupyterhub bash
# then :
adduser test
````

### Setting up ZNC



### Setting up ngircd

