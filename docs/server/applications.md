### Setting up some more Applications

#### Installing `golang`

````bash
#!/bin/bash -e
mkdir -p /opt/
cd       /opt/
rm -fr go golang
GOBALL=go1.18.linux-amd64.tar.gz

wget -c https://dl.google.com/go/$GOBALL
tar zxf $GOBALL
rm      $GOBALL
mv     go golang

mkdir -p                   /opt/smkbin/
ln -nsf /opt/golang/bin/go /opt/smkbin/
````

#### Build Google Drive CLI tool

Note : Allow a few minutes. Nothing will be printed until this part is nearly done.

````bash
#!/bin/bash -e
export GOPATH=/tmp/gobuild
GOPROG=$GOPATH/bin/drive

rm -fr     $GOPATH
go get -u github.com/odeke-em/drive/cmd/drive

strip      $GOPROG
upx --lzma $GOPROG
mkdir -p           /opt/smkbin/
mv         $GOPROG /opt/smkbin/
rm -fr     $GOPATH
````

#### Build `lego` tool (supersedes `certbot`)

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
upx --lzma $GOPROG
mv         $GOPROG /opt/smkbin/
rm -fr     $GOPATH
````

#### `nomodeset`

Some Xorg video drivers require a kernel feature known as `nomodeset`. If you learn that this is the case for your box, you can set this feature up as follows.

(a) Edit the `/etc/default/grub`

(b) Look for a line similar to the following

`GRUB_CMDLINE_LINUX_DEFAULT=“quiet splash resume=...”`

(c) Insert the word nomodeset before the word quiet. Put a space between the two words. Save and exit.

(d) Execute the command `update-grub`.

#### Optional Step : Install TexLive

This step may take from several minutes up to an hour and will add several GB of files. However, if you would like a full-featured industrial-strength system, TexLive is a useful part of picture.

`apt-get install texlive-full`

#### Optional Step : Initial virtualization setup

Note : Only use in physical hardware or dedicated servers, Skip for a normal VPS.

````bash
#!/bin/bash -e
apt-get install \
    qemu-kvm qemu-system qemu-utils \
    bridge-utils \
    virtinst libvirt-daemon libvirt-daemon-system virt-manager
````

#### Optional Step : Install Palemoon

Skip this step for headless servers unless you plan to use VNC [and you want this web browser as well].

````bash
#!/bin/bash -e
apt-get install libdbus-glib-1-2
````

````bash
#!/bin/bash -e
cd /opt || exit 1
rm -fr  palemoon

wget -O palemoon.tar.xz https://linux.palemoon.org/\
datastore/release/\
palemoon-unstable-latest.linux-x86_64.tar.xz

tar Jxf palemoon.tar.xz
rm -fr  palemoon.tar.xz
ln -nsf ../palemoon/palemoon smkbin/
````

Run `palemoon` as an ordinary user.

Turn off “Always perform this check”.

User View -> Toolbars -> Customize to put Zoom controls, History and Bookmarks on the links toolbar.

Install extensions using the XPI files provided with this documentation file.

#### Install `youtube-dl`

````bash
#!/bin/bash -e
TARGET=/opt/smkbin/youtube-dl
rm -fr     $TARGET
curl -L \
https://yt-dl.org/downloads/latest/youtube-dl \
        -o $TARGET
chmod a+rx $TARGET
````

#### Restore `/var/letse/`.

If you have a saved copy of the directory tree "/var/letse", restore it to the current box. Otherwise, create the directory.

#### Generate `dhparam.pem`

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

#### Set up `node`, `npm` and `yarn`

````bash
#!/bin/bash -e
apt-get install curl software-properties-common
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
apt-get update
apt-get install gcc g++ make nodejs
LINK="https://dl.yarnpkg.com/debian"

curl -sL $LINK/pubkey.gpg | sudo apt-key add -
echo "deb $LINK/ stable main" | \
    sudo tee /etc/apt/sources.list.d/yarn.list

apt-get update
apt-get -y install yarn
````

#### Fix `joe` setup

````bash
#!/bin/bash -e
DOTJOE=/root/setupdoc/files/dotjoe.tgz
cd /etc/skel && tar zxf $DOTJOE
cd /root     && tar zxf $DOTJOE

cd /home
for x in *
do
    cd /home/$x && tar zxf $DOTJOE && chown -R $x.$x .joe
done
````

#### Add more PHP feature

````bash
#!/bin/bash -e
apt-get install \
    libmcrypt-dev  \
    php-apcu       php-bcmath     php-cli        php-common     \
    php-curl       php-dev        php-fpm        php-gd         \
    php-imagick    php-intl       php-json       php-ldap       \
    php-mbstring   php-mysql      php-pear       php-readline   \
    php-redis      php-smbclient  php-soap       php-sqlite3    \
    php-xml        php-xmlrpc     php-zip

pecl channel-update    pecl.php.net
pecl install channel://pecl.php.net/mcrypt-1.0.2
````

