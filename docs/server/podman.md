### Installing Podman (under Debian 10)

Skip this section unless you're running Debian 10.

Note:  We use "buster-backports" on Debian 10 to get a newer version of `libseccomp2`.

````bash
U1=https://download.opensuse.org/repositories/devel
U2=/kubic:/libcontainers:/stable/Debian_10
U3=devel:kubic:libcontainers:stable.list

cat << END >> /etc/apt/sources.list
deb http://deb.debian.org/debian buster-backports main
END

cat << END >> /etc/apt/sources.list.d/$U3
deb $U1:$U2/ /
END

curl -L $U1:$U2/Release.key | sudo apt-key add -
sudo apt-get update
sudo apt-get -y -t buster-backports install libseccomp2
sudo apt-get -y install podman
````

#### Step: Install "podman" (under Ubuntu 18.04).

Skip this section unless you're running Ubuntu 18.04.

````bash
MOO=https://download.opensuse.org/repositories/devel:\
/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}
echo $MOO

echo "deb $MOO/ /" | \
sudo tee /etc/apt/sources.list.d/\
devel:kubic:libcontainers:stable.list

curl -L $MOO/Release.key | sudo apt-key add -

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install podman
````

Instructions  online  say to  do this next,  but it doesn't  seem to work.  We think it's because  this part is intended  for cases where non-root users are going to use "podman".

````bash
systemctl --user restart dbus
````

Suggestion: At this point, reboot the system instead.

------

#### Some notes on “Podman”

You can use `podman` to pull and run a copy of Ubuntu LTS as follows:

````bash
podman image pull ubuntu
podman run --interactive --tty --name sally ubuntu
````

Ctrl + D to exit.

The preceding block will leave you with a stored image named `ubuntu` and a stored container named `sally`. To run `sally` again :

````bash
podman restart sally
podman attach sally
````

Ctrl + D to exit.

------

#### To list `podman` containers :

`podman container list --all`

`podman` lacks a simple way to rename containers. This approach is cumbersome but should work.

````bash
podman stop    sally            # Stop   old  container
                                # Use container to create image
podman commit  sally jessie-image
podman rm      sally            # Delete old container
                                # Create new container
podman run --interactive --tty --name jessie jessie-image
podman image rm jessie-image    # Optional: Delete new image
# Control-D to exit
````

To run container again

````bash
podman restart jessie
podman attach jessie
````

Control-D to exit

#### Exporting a `podman` container to a tarball

````bash
podman stop    jessie
podman export  jessie | gzip -c -9 > jessie-image.tar.gz
````

You can use a tarball of this type to create a new image:

````bash
podman import  jessie-image.tar.gz new-jessie-image \
     -c CMD=/bin/bash \
     -c WORKDIR=/tmp \
     -c ENV=PATH=/usr/local/sbin:/usr/local/bin:\
/usr/sbin:/usr/bin:/sbin:/bin
````

Note: The tarball doesn't preserve  meta-information such as what to do with the image when you run it.However, settings related to that can  be  specified during the image creation step as illustrated above.

So, an alternate and clumsier way  to rename  a container is as follows:

````bash
podman stop    jessie           # Stop   "jessie" container
                                # Create "jessie" tarball
podman export  jessie | gzip -c -9 > jessie-image.tar.gz
                                # Use the tarball to create an image
podman import  jessie-image.tar.gz laura-image \
     -c CMD=/bin/bash \
     -c WORKDIR=/tmp \
     -c ENV=PATH=/usr/local/sbin:/usr/local/bin:\
/usr/sbin:/usr/bin:/sbin:/bin
                                # Delete "jessie" tarball
rm             jessie-image.tar.gz
podman rm      jessie           # Delete "jessie" container
                                # Create "laura"  container
podman run --interactive --tty --name laura laura-image
````

Control-D to exit