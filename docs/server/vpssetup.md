## Developer VPS Box Setup

Credits : Robert Kiraly

#### Overview

This text file documents one possible approach to the setup of a Debian 10 developer’s box.

This is a flexible guide as opposed to a single fixed procedure. The assumption is that the user is a developer who is able to decide which steps to take and how to tweak them.

This guide can be used to create boxes that operate in an optimum manner and are fully-loaded with useful software (including non-Debian extras).

>Unless you are an expert, this guide should not be used with existing boxes, especially in cases where bricking would be a serious issue.
>
>Due to oddities in how some VPS hosts set up boxes on their end, there is a possibility that use of this guide will lead to inability to boot VPSes.

------

This guide can be used in the following contexts :

- The box may be a server but this is not required
- The box may be headless or it may run XOrg
- Some features are for AMD64 system only
- However, Raspberry Pi’s may work
- CPU: 2x2 or above
- RAM: 8GB or above
- Disk: 40 GB or above (SSD or better is recommended)
- Distro should be based on Debian 10

The box may be a local PC, a dedi box, or a VPS. We’ve tried to allow for all three possibilities, but correction may be needed.

Debian `Sid` and/or `Testing` branches may work as well as `Buster`. However, tweaks may be needed.

Ubuntu branches from the same period as “Buster” may work, to a lesser extent.

If the goal is a headless box, GUI software such as LibreOffice should obviously be skipped. Image and/or other multimedia libraries may be installed regardless.

------

You should have recieved a directory tree named “setupdoc/” with this file. The directory tree should like this

```txt
setupdoc/setupdoc.txt	# This page
setupdoc/files/				# A subdirectory with multiple files
```

`setupdoc/` should be place in `/root` on the box that you would like to setup.

The steps documented here should be executed as superuser except where otherwise indicated.

------

Examples of packages and/or features installed : 

| Utility    | Use                                     |
| ---------- | --------------------------------------- |
| bzip2      | Faster replacement for standard version |
| dnsmasq    | Faster DNS                              |
| drive      | Google drive CLI client                 |
| go         | Recent Version                          |
| gzip       | Faster replacement for standard version |
| lego       | Faster replace for `certbot`            |
| qemu-*     | QEMU [for physical boxes only]          |
| softoffice | Working copy of LibreOffice 7           |
| texlive    | Typesetting system                      |

.NET SDK

`rjkbin/*` : OldCoder utility scripts.

````bash
# OldCoder scripts provided:

# cls           - Clear screen
# cmptree       - Byte-compare two directory trees
# cptime        - Copy file or directory timestamp
# debak         - Delete backup files in current directory
# debaktree     - Delete backup files in current tree
# deext         - Echoes arguments with filename extensions removed
# detab         - Detabs files using a 4-space column width
# epoch         - Display timestamp of a directory or file
# largest       - List largest files in a directory tree
# md5all        - Output MD5 sums for a directory tree
# md5tree       - Relatively powerful MD5 sum manager
# newest        - List newest files in a directory tree
# oldest        - List oldest files in a directory tree
# runhtpdate    - (root only) sync server time by HTTP
# setdos        - Set newlines to DOS format
# setunix       - Set newlines to UNIX format
# tardate       - Set timestamp of a tarball or ZIP file
# trimws        - Trim white space from end of text lines
````

#### Upgrade Debian Strech to Buster

If the box is running Stretch, upgrade it to Buster as shown below. Other skip this step.

````bash
#!/bin/bash -e
sed -e 's/stretch/buster/g' \
    -i /etc/apt/sources.lst || exit 1

apt-get update
apt-get upgrade
apt-get dist-upgrade
````

Reboot the box,Login and become superuser again. Check distro version again.

```bash
cat /etc/os-release
```

Remove unnecessary packages

```bash
apt-get autoremove
```

#### Distribution Upgrade

These commands update files. They may upgrade the distro within its series (for example: from 10.1 to 10.8) but not to next series. That type of upgrade is a separate process

````bash
#!/bin/bash -e
apt-get update
apt-get dist-upgrade
````

#### Installing Basic Packages

Atleast install these packages.

````bash
sudo apt-get install dnsutils joe lynx pbzip2 pigz rlwrap
````

#### Installing a number of packages

````bash
#!/bin/bash -e
cd /root/setupdoc/files/
apt-get install `cat *-dpkg.lst`
````

#### Check `/etc/shells`

If the text file `/etc/shells` doesn’t already contain the following line, add the line : `/bin/bash`

Note : If `dropbear` seems to be accepting connections but produces error messages, this issue may be the problem.

#### Modify `/etc/fstab` entry for root filesystem

**NOTE : This step is only for physical boxes and/or dedis. Skip it for VPSes.**

1. Replace default for root filesystem with : `noatime,errors=remount=ro`
2. Execute:

````bash
#!/bin/bash -e
cd /etc
cp -ai fstab fstab.000
nano   fstab
````

#### Setup `dnsmasq`

````bash
#!/bin/bash -e
apt-get install dnsmasq
````

Replace `/etc/dnsmasq.conf` and `etc/resolv.conf` with the copies provided in `setupdoc/files`. Then execute : 

````bash
#!/bin/bash -e
chattr +i /etc/resolv.conf
service dnsmasq restart
````

Note : Subsequently, you won’t be able to edit `/etc/resolv.conf` unless you run `chattr -i` on the file first. After edits, run `chattr +i` on the file again.

To confirm dnsmasq is working, execute this command ; 

```bash
nslookup bacon.eggs
```

`dnsmasq` is a caching DNS server. To flush the cache, restart the `dnsmasq` service.

#### Generate a keypair for your server-side user accounts

````bash
#!/bin/bash -e
rlwrap ssh-keygen -t rsa -b 2048
````

Do *not* specify  a password for the keypair.  Additionally, specify box-specific names such as `pi.pubkey` and `pi.prvkey`. The `.prvkey` file goes on your ssh client boxes. The `.pubkey` file should be appended to `$HOME/.ssh/authorized_keys` for your user account on the server box.

If you're using `dropbear` instead of `openssh`, skip this part.

Step:  If you're using `openssh`,  edit  `/etc/ssh/sshd_config`  and set:

````
MaxStartups 75
UseDNS no
````

Then execute: service sshd restart

#### Create directories for utilities

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

##### Edit `secure_path` setting in `etc/sudoers` to prepend directories from preceding scripts which exists.

```
secure_path="/opt/minebest/mtbin:/opt/smkbin:/usr/local/sbin:..."
```

Log-out and back in.

If you log-in as an ordinary user, execute the following command to become the superuser

`sudo bash`

You can now add useful scripts and tools to the two new directories.

#### Set `LC_ALL`

Create a text file `/etc/profile.d/lc_all.sh` containing:

```
export LC_ALL=C
```

File needs to be readable, but not executable.

#### Set a timezone

To list possible time zones, do this : `timedatectl list-timezones`

For Kolkata timezone in India : `timedatectl set-timezone Asia/Kolkata`

#### Replace `gzip` and `bzip2` with faster version

We need to save the old versions as some programs may need then

````bash
if [ \! -L /bin/gzip ]; then
    mv /bin/gzip{,.000}
    ln -s `which pigz`   /bin/gzip
fi

if [ \! -L /bin/bzip2 ]; then
    mv /bin/bzip2{,.000}
    ln -s `which pbzip2` /bin/bzip2
fi
````

These two special version are faster for new files, but not neccessarily for existing files.

#### Adding a ordinary user

At this point, add atleast one ordinary user. To do so, execute `rlwrap adduser` once for each user.

Initially only account name and passwords are important. Other fields can be left empty. The account name needs to be lower-case.

Execute following block for each new-user, Substitute the appropriate name for “sally”

````bash
THEM=sally
HOUSE=/home/$THEM
chmod 700 $HOUSE
mkdir -p  $HOUSE/.ssh
chmod 700 $HOUSE/.ssh
touch     $HOUSE/.ssh/authorized_keys
chown -R  $THEM:$THEM $HOUSE
````

When time permits, you (as admin) or each individual user should append  each individual user's public key to the following file.  Substitute the appropriate account name for "sally" in each case. `/home/sally/.ssh/authorized_keys`

Execute the following command once for each user who should have `sudo` access : `usermod -a sally -G sudo`.

#### Optional : Enable `sudo` w/o password

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

now copy this file to `etc/sudoers.d`

***Warning :*** This step if not done properly can brick the box!

Also do not edit the file once its in directory. This may also brick the box. Safest way is to edit is somewhere else and then copy result into the directory in question

#### Set hostname

If possible, at this point,  you should point the  IPV4 for some domain that you control to the Debian box. Note: This doesn't apply if the box isn't on the WAN.

If you have a domain and point it as indicated, set the hostname for the box as follows:

````bash
DOMAIN=somedomain.com           # Replace with appropriate domain
hostname $DOMAIN
echo     $DOMAIN > /etc/hostname
````

#### Harden Security

````bash
# vi /etc/ssh/sshd_config

# note these are important, as vps almost every few minutes gets attacked by botnets
# changing port decreases attack surface
# disabling password auth decreases risk of guessing password
# note : you may not worry if you screw up your keys, you can always vnc into the vm from
# cloud providers console and login and fix your box

Port 23415
PasswordAuthentication no

# after that run service sshd restart
````

