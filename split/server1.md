# Server Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: server
This is part 1 of 1 parts

---

## File: server/applications.md

### Setting up some more Applications

#### Installing `golang`

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
curl -sL https://deb.nodesource.com/setup_21.x | sudo bash -
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



---

## File: server/bkp.md

## Backup VPS using rclone

Cheap VPS offers often do not include backups, so users must take backups on their devices. The best solution for users with cheap VPS plans lacking backup facilities is to purchase cloud storage and create a backup script that sends backups to the cloud vendor.

This approach makes the cloud drive function like a portable storage device, where regular VPS backups are stored.

### Sync Script with pcloud

* This setup uses `rclone` configured to use `pcloud` remote.

#### Create a filter for backup

````txt
# === System configuration files ===
+ /etc/**
- /etc/mtab
- /etc/resolv.conf
- /etc/hostname
- /etc/hosts
- /etc/adjtime

# === SSH keys and user data ===
- /root/.cache/**
- /home/*/.cache/**
- .npm/**
- .cargo/**/target/**
- .vscode-server/**
- node_modules/**
- target/**
- tmp/**
+ /root/**
+ /home/**

# === Web servers and web apps ===
+ /var/www/**
+ /etc/nginx/**
+ /etc/letse/**

# === Databases and important services ===
# + /var/lib/mysql/**
# + /var/lib/postgresql/**
# + /var/lib/redis/**

# === Mail systems ===
+ /var/mail/**
# + /var/spool/mail/**
# + /etc/postfix/**
# + /etc/dovecot/**

# === Special services ===
+ /opt/smkbin/**

# === Logs (optional) ===
# + /var/log/**

# === SSH and Sudo ===
+ /etc/ssh/**
+ /etc/sudoers.d/**
+ /etc/sudoers

# === Default deny everything else ===
- *
````

#### Installing Dependencies

````bash
# pre-requisites
sudo apt-get install rclone
````

#### Assuming rclone is setup with a remote

* Below script assumes you a remote named `pcloud` 

````bash
#!/bin/bash
# /*
# * --------------------------------------------------------------------
# * @file    pcloud_sync
# * @brief   A simple sync util for pcloud
# * @author  smk (smk@freebsd.org)
# * @version 20221129
# * @license BSD3
# * @bugs    No known bugs
# * --------------------------------------------------------------------
# */

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

#### Further Steps

- Run this script monthly using crond or a systemd script according to the required backup frequency.
- An example cron job I use sends mobile notifications directly using `ntf`.

````bash
0 2 * * 6 /usr/local/bin/ntf -t WEEKLY_PCLOUD_SYNC done /root/bin/pcloud_sync.sh
````

* [https://github.com/wolfv6/rclone_jobber/tree/master](https://github.com/wolfv6/rclone_jobber/tree/master) : `rclone_jobber` is a script for backup.

### Borg - Snapshots

* WIP

---

## File: server/boottime.md

### Regarding `rc.local`

`/etc/rc.local` is a `bash` script that Linux executes at boot time. So it is a convenient place to put your own startup commands.



However, there are a few rules to remember. Failure to follow these rules is very likely to brick your box :

- Double-check the script and test a copy before updating the master copy in `/etc/`. Syntax errors or other issues with the script can render the system inoperable.

- If the script executes potentially blocking operations, execute them as background processes. Running blocking operations in the foreground will likely cause the system to become unresponsive.

- The script must complete execution and exit with the command `exit 0`.

- The script must be executable, although this requirement is not confirmed for all distributions. To make it executable, run `chmod 755 /etc/rc.local`.

- Processes that will use network, such as `node.js` apps, need to wait until the network comes up before doing setup operations.

  Install the script named `wait-ipv4.pl`. If configured properly, call the script to pause the startup of processes until the network is ready.

  If configuring `wait-ipv4.pl` is not possible or to ensure safety, use the command sleep 60 to provide a sufficient delay.

  > Neither `wait-ipv4.pl` nor `sleep 60` should be executed by `/etc/rc.local` in the foreground. These commands are for use in background processes only.

### Setup some boot-time operations

Create the directory `/opt/boot/`, copy `setupdoc/files/boot-net-programs.sh` into the directory and make the copy executable. For example.

````bash
#!/bin/bash -e
mkdir -p /opt/boot/
cd
cp -p setupdoc/files/boot-net-programs.sh /opt/boot/
chmod 755  /opt/boot/boot-net-programs.sh
````

Edit `/opt/smkbin/wait-ipv4.pl`. Confirm that the settings of `$IFACE` and `$IPCONFIG` are correct for the current box. To get the information needed to do so, Use `ifconfig |grep up` and then `which ipconfig`

Edit the script that you installed above. Modify it to use similar code to start network-related process that are not handled by other means.

Create an initial version of `/etc/rc.local` that looks like this

````bash
#!/bin/bash
/opt/boot/boot-net-programs.sh >& /dev/null &
exit 0
````

Important : **Do not** use `#!/bin/bash -e` above

Make file executable : `chmod 755 /etc/rc.local`



---

## File: server/cpan.md

### Install CPAN modules using `cpanm`

If  the  new box is going to be used for Perl development,  you should
install a set of CPAN modules. There are two ways to do this:

​	(a) Install them from the distro repos

​	(b) Build   them from source

(a) is faster and  more reliable.  However, the distro repos don't in-
clude a full set of modules.  Additionally, repo copies of modules may
be outdated.

We may  document (a) at a later date.  This  revision of this document
discusses (b).

Advisories:

​	(c) This procedure may take up to an hour or longer
​	(d) Some builds may fail. See below for a work-around.

If a build of a given module fails due to a  test failure,  one  work-
around  is to disable testing for that module.  To do that,  replace a
command of the form:

      cpanm Foo::Bar
with:
      `cpanm --notest Foo::Bar`

If builds fail for other reasons, consult a developer.

To proceed:

      bash -e /root/setupdoc/files/addcpan.sh

Note that:

  (a) This must be done as "root"
  (b) Internet access is required
  (c) The work-around discussed above may be required

#### CPAN documentation

To  see what a given CPAN module does,  execute the command  "perldoc"
followed by a space and the module name. For example:

    perldoc Algorithm::FastPermute

#### CPAN Examples

##### CPAN example:  Print a sorted list of all  unique permutations of an array. Skip redundant lines.

````perl
use strict   ;
use Carp     ;
use warnings ;

use Algorithm::FastPermute ('permute');

my @array = qw (dog cat woof meow woof cow milk);
my %list  = ();
permute { $list {"@array\n"} = 1; } @array;
for (sort keys %list) { print; }
````

##### CPAN example: Download a file from the Web and store it locally.

````perl
use strict   ;
use Carp     ;
use warnings ;

use LWP::Simple;

die "Error: Download failed\n"
    unless getstore ("https://google.com/", "/tmp/google.html");
print "File downloaded\n";
````



##### CPAN example: Compute and display an MD5 sum.  The output is consistent with that produced by "md5sum -b".

````perl
use strict   ;
use Carp     ;
use warnings ;

use Digest::MD5 qw (md5_hex);

my $data   = "moo\n";
my $md5sum = md5_hex ($data)  ;
print "MD5 sum is: $md5sum\n" ;
````



---

## File: server/guide.md

### A talk with OldCoder aka Robert Kiraly

#### Study: What should a Linux FOSS developer learn?

Q. Suppose that  somebody is interested in Linux FOSS development  for startup  or employment purposes.  Or just to be able to create or participate in FOSS projects.  What should a related course of study  include?

A. I'll assume that this is  about  building a broad foundation as opposed to a focus on a specialty.

The answers are:

-   Code Languages
-   Data Languages
-   Source Code Management
-   Build Systems
-   Standard Servers
-   Containers and Virtual Machines

These topics are discussed in the following sections.

#### Code Languages

This is a summary of my own languages experience from 2012:

> Perl, Python, PHP. Standard but
> you 'C', I also Lisp
> FORTRAN rocks and TeX rolls
> It's fun to assemble
>
> JavaScript, Forth, Pascal, Bash
> Bash is a smash
> People should not trash
> Bash is a smash
>
> Tcl/Tk: people disrespect it a bit
> but with me it's a hit
> Java is not JavaScript
> Lua how'ja Dua
>
> Octave and Matlab not the same
> Close enough there's no shame
> SQL What the Hell
> Several versions

I'd recommend the following to new developers in 2021:

Learn 'C' (not C++), Perl 5, Python 3, PHP 7 and 8,  JavaScript  (both traditional and "node.js"), Lua and Tcl (they might go well together), and Bash. Later on, Go (Google's replacement for C++).

Java is a good teaching language. I'm referring to Java, the pure language,  as opposed to JNI.  Java is the modern Pascal.  It's so strict that, if a student is able to get a program to  build,  it's likely to run.

I don't  recommend  focusing on Java or going  too deep into the  Java ecosystem.

The Java ecosystem is like the  MS-Windows world:  It's a foreign city actually,  a city on another planet -- where everything down to the plumbing is different.  You'd visit the city and learn the new culture and  myriad different ways of doing things only if you planned to live there.

Learn  enough C++ to  be able to patch C++ programs based on 'C' knowledge.

Avoid Rust and Ruby.  Reasons for dislike of C++, Rust, and Ruby are a separate discussion.

If  you work at a Windows house,  you'll want to  pick up both DOS CLI and PowerShell.

If possible,  avoid the major  MS languages and frameworks  such as C# and .NET. The reason is the same as discussed above in connection with Java.

At some Windows houses,  you'll be able to work in Linux-like environments and use "gcc", Perl, and other FOSS languages much as though you were using Linux.

#### Data Languages

Be familiar with SQL, JSON, YAML, and XML.  Plus HTML 5 and CSS 3  for webdev. Note that HTML 5 is a type of XML.  Learn  enough  CSS 3  that you're able to write responsive web pages.

You should be familiar with CSV  but that one is really just a trivial format.

#### Source Code Management

Learn "git".  There are  other systems of this type,  but "git" is the one to start with.

#### Build Systems

You  don't need to  learn to work  *in* a  build system;  i.e., how to write build scripts.  However, you do need to learn how to use them to build programs.

The two most  important build systems are  "autotools"  (also known as "autohell") and "meson-ninja".  "cmake" is a candidate for  3rd place.

"autotools" was  dominant for years.  It  was,  and remains, horrible. Different releases are incompatible.  A tool  that's designed  to help with this (autoupdate) doesn't work.  The system as a whole is as slow as molasses  and often breaks for reasons that  are difficult to debug and fix.

In response to this,  "meson" and "ninja" have arisen.  This is a pair of programs  that  work together  to build programs  quickly and efficiently.

"cmake"  was an earlier attempt  to escape  the  horror that is "auto-tools".  I don't like "cmake"  because it's often  unable to find libraries and what to do about this isn't clear.

We'll discuss the three systems in greater detail further down.

#### Standard Servers

1. A developer should have a fair understanding of what DNS is and how
   it works. For basic development boxes,  "dnsmasq" is the recommended DNS server.
   Setup instructions are provided elsewhere in this document. For more advanced use cases, it may be  necessary  to set  up "named". "named" is beyond the scope of this discussion.

2. It's also important to be familiar with web server setup. 

   A web server is, of course, any server that supports the "http" and/or "https" protocols. There are many such servers. The ability to do this is, for example, a standard part of most Perl, Python, and PHP installations.

   The two most important web server programs -- i.e., programs dedicated to the purpose -- are "nginx" (aka Engine X) and Apache 2.

   Apache 2 isn't  bad.  However, it's complicated and resource-intensive compared to "nginx".  The recommendation is  to use "nginx" instead of Apache 2 where possible. 

   In some cases,  FOSS software packages require Apache 2.  It should be possible, in a subset of the cases,  to run "nginx" as the primary web server and to relay  requests for Apache 2 pages to a copy of Apache 2 running behind the scenes.

3. FWIW: As of 2021,  "nginx" and Apache 2 are basically tied in terms of market share.

4. "nginx's" features include:

    * Uses much less RAM than Apache 2
    * Much faster than Apache 2
    * Reverse proxy with caching
    * Mail proxy (supports TLS, SMTP, POP3, and IMAP)
    * IPV6
    * Load balancing

5. A third FOSS  web server  that is  worth mentioning is  "lighttpd".
  "lighttpd" is also known as "Lighty"  (a name that is certainly easier
  to pronounce).

  "Lighty's" claims to fame are as follows:

  - It's both  venerable and maintained.  The program  dates back to
    2003 but a new release was made in 2021.
  * It's lightweight and quite fast.

  "nginx" is  recommended for general use cases,  but "Lighty" is useful
  for some purposes.

6. A Linux FOSS developer should know how to configure SSH both on the
  client side and on the server side.

  There are two major SSH server programs: OpenSSH and Dropbear. OpenSSH setup is discussed elsewhere in this document.  Dropbear notes will be added.

  On the client side, the primary SSH configuration file is "$HOME/.ssh/config". Notes related to that file will be added.

7. An understanding of SSH key pairs is advisable. A few notes related
to key pairs are included elsewhere in this document.

#### Virtual Machines

In the modern FOSS world,  an understanding of  containers and virtual machines is a must.

A virtual machine (or VM) is simply a PC or other computer that  isn't real. I.e, it isn't hardware by itself. It consists partly or entirely of software.

In the classical form,  a virtual machine is a program that interprets machine instructions and  thereby fools  an application into believing that it's running on a compatible machine. The machine doesn't actually exist.

The game device emulators that  started to appear in the 1990s -- MAME is an important example -- were of this type.

It can be more complicated these days.  In some cases, a virtual machine may have access to the underlying real machine's hardware. The access is, however, controlled.

A "VPS" is simply a  virtual machine that is rented out,  usually on a monthly or annual basis.  Typically, it offers WAN access and a static WAN IPV4. So, it's useful for server hosting purposes.

#### Containers

Virtual machines  require lots of resources to run.  Containers  are a lightweight alternative.

A container looks, to some extent, like a virtual machine.  It has its own operating system and filesystem.  So,  for example, you can have a Debian PC and boot a container on the  PC that runs  Fedora instead of Debian.

Terminology: The OS that runs a virtual machine or container is referred to as the "host OS" or simply as the "host". The OS that runs on a virtual machine  or in a container is referred to as the "guest OS" or simply as the "guest".

Containers are more limited than virtual machines in two key respects: (a) There is no virtual hardware. (b) The same kernel needs to be used by the host OS and the guest OS.

So, a guest running on a Linux host must run Linux and the two Linuxes must be the same in terms of kernel and machine type.

The trade-off is that containers are essentially zero cost in terms of resources -- i.e., disk space, RAM, and CPU -- except for  the resources that a guest OS  actually uses. No machine per se is emulated,  so there is no cost for that.

Additionally,  containers don't need to emulate entire OSes.  They can be set up so as  to perform specific tasks such as running one type of server.

##### Container Software

Important container tools include "docker", "lxd", "podman", and "kubernetes".

You probably wouldn't  seek to learn  "kubernetes" without a reason to do so. It's powerful but complicated.

"docker" was a must-know for a few years. However, there's an alternative named "podman" now that may be a better option.  "podman" is discussed elsewhere in this document.

"lxd" is  useful but not a must-know presently for the generalist developer.

#### VM Software

The most important  FOSS virtual machine systems are QEMU and Virtual Box OSE.

QEMU is the one to focus on.

VirtualBox OSE has a polished and friendly GUI.  However, it's part of a commercial  package and  license issues are  a problem  in some contexts.

Additionally, VirtualBox OSE is highly fragile, it requires Qt5 (which is problematic in multiple respects),  and it can be nearly impossible to build.

QEMU is very simple to use for simple use cases.  It also doesn't have as many license issues.

For more  advanced use cases -- for example, those involving complicated network setups -- QEMU commands can  require some effort to figure out.

You'll want to learn to use a system called SPICE with QEMU.  SPICE is needed to get "copy and paste" working between host and guest.  It implements other features as well.

Some  developers use a framework named "libvirt" to set up QEMU operations. I prefer direct control of things and to avoid extra  layers of machinery where possible.  So, QEMU commands  can be complicated but I prefer  to write  them than  to deal with  the machinery introduced by "libvirt".

There's a tool named "vagrant" that is sometimes used to manage remote VMs from the command line.  I like  "vagrant"  but  it's difficult  to build, so I've dropped it.

#### CMS Recommendations

Drupal: Not advised for individuals or small organizations.

Drupal could be thought of as a powerful analogue to WordPress. It has impressive features and  is  a respected CMS.  However,  it's huge and complicated.  A  startup or small business that uses Drupal might find itself trapped in technical debt.

Joomla: Not advised for individuals or small organizations.

Joomla is a competitor to Drupal.  It offers  similar advantages relative to WordPress.  I don't see a clear winner between Joomla and Drupal. Some  reviewers feel that Joomla is more polished, but Drupal may offer features to balance this.

WordPress:  WordPress is O.K. for non-tech would-be CEOs. It isn't for developers who'd like to do things quickly and efficiently. Especially not CLI developers.

Don't deprecate WordPress.  It fills a niche and does it well. A large part of the Web  is  on WordPress.  However,  it's bulky,  awkward and clumsy to  work with.  Additionally, the resulting websites are slower than what you get with lightweight approaches.

This said, for a small startup or business, WordPress is probably preferable to Drupal or Joomla.

Jekyll:  You  can  use  Jekyll "to host [static] sites right from your GitHub repositories".  That's a nice feature.  However, there are some negatives:

* It's written in, and requires, Ruby. That isn't a plus.

* Its use  case  is,  to  some  extent,  integration with Github (even
though Github isn't required).

* It involves more of an ecosystem than I like to see for this type of
application.  I prefer software that doesn't require  as  much commit-
ment.

* It's slow for large sites.

Hugo: Hugo offers a number of pluses:

* It's 35 times faster than Jekyll. Repeat, 35 times.

* Hugo is a compiled Go application -- hence the name Hugo -- and this
means  both  speed  and  fewer  problems  related  to fiddling with an
interpreter.

* Hugo is easier to set up than Jekyll is.

* It supports more data languages than Jekyll does.

* Like Jekyll, files are stored as text as opposed to database.

* Like Jekyll, a development server is provided.

* Hugo can generate and/or post-process CSS and JS code.

* It supports menus, XML sitemaps, and RSS/ATOM feeds.

* It can import Jekyll sites.

Hugo is obviously a winner in this space. There are only two arguments
against it that I can see:

* It's for static sites only as opposed to dynamic sites.

* I prefer  something  simpler for basic use cases.  This brings us to the final options below.

Lightweight tools: I prefer lightweight site-creation tools.

I use both  (a) my own site language translator,  "Haggis",  and (b) a markdown to  HTML translator that I've started  to write.  Haggis supports dynamic pages. The MD to HTML translator is static-only but very easy to use.

There are publicly released FOSS projects in the same space. For example, review Pico:

      https://picocms.org/

Pico supports static sites out of the box.  Additionally, if you don't mind learning a related  framework named  "Twig",  you can add dynamic content.

For basic use cases, these tools are good because  they're simple  and easy  to  use,  they don't require a commitment  to an ecosystem,  and they're often easy to tweak.

Four recommendations:

* Try Pico for static sites and sites that need a small amount of dyn-
amic content.

* Try Hugo for static sites that need more "oomph".

* For sites that are primarily  dynamic in nature,  it might be better
to skip CMS and  work in one of the following: Perl 5, Python 3, PHP 7
or 8, or "node.js".

* If you  need a dynamic site quickly and  a matching template site in
your preferred language isn't available,  WordPress is acceptable as a
fallback option.

#### Use of `autohell`

The sources  for an "autohell"-based FOSS program may include a "configure"  script written in Bash.  To use such a script, one typically executes it as follows:

    mkdir -p /opt/moocow
    bash ./configure \
        --prefix=/opt/moocow           \
        --disable-dependency-tracking  \
        --enable-shared=yes            \
        --enable-static=no

This procedure,  ideally,  creates  a "Makefile" which  can be used to build and  install the program.  Additional option switches may or may not be required.

The sources  may include a "configure.ac" file instead of "configure". In this case, one must use "configure.ac" to create "configure",  then use "configure" to create "Makefile".

The  procedure  used to go from  "configure.ac" to "configure"  varies from program to program. Sometimes, the following command will work:

    autoreconf -fi

Scripts with names such as "autogen", "autogen.sh", or "bootstrap" may be  provided.  These  scripts  typically  will create  "configure" for you.

In some cases, these  scripts may run "configure" automatically  after "configure" is created. In the latter case, the developer must provide the required "configure" switches to these scripts instead of to "configure".

If  a FOSS project is old,  its existing  "configure"  script  may not work.  In such cases,  one hopes that "configure.ac"  is also provided and  uses "configure.ac" to rebuild "configure".  That procedure often fails with obscure error messages.

With luck, "autotools" will disappear soon. It won't be missed.

#### Use of `meson-ninja`

"meson-ninja" projects  are easy to build  except for  one tricky part that we'll come back to. One proceeds as follows:

a. Python 3 is required and must be accessible by PATH.

b. Install dependencies.

c. Go to the appropriate source directory.  This is the directory that contains "meson.build". Execute a script similar to the following:

    mkdir -p /opt/moocow
    rm -fr build
    mkdir  build
    meson  build -D prefix=/opt/moocow
    
    cd build
    if [ \! -f build.ninja ]; then exit 1; fi
    meson configure
    ninja || ninja
    ninja install

That's it, in many cases, except for the tricky part mentioned before. You may need to add more option switches to the "meson build" command. The tricky part  is  determining  the  format  of the option switches.
Sometimes, you'll need to specify "true" or "false" to enable or disable a feature. Other times, you'll need to specify "enabled" or "disabled" instead.

To  find out the  option switches that are supported  for a particular program and whether to use "true-false" or "enabled-disabled" instead, look  for a file named "meson_options.txt" and  review the contents of that file.

Some examples:

* This is my "meson build" command for "tracker-sparql"

    ````bash
    meson build \
        -D prefix=/opt/moocow \
        -D network_manager=disabled
    ````

* A build of "libvirt" is more complicated:

    ````bash
    meson build \
        -D prefix=/opt/moocow   \
        -D docs=enabled         \
        -D driver_qemu=enabled  \
        -D fuse=enabled         \
        -D libnl=enabled        \
        -D libpcap=enabled      \
        -D no_git=true
    ````

`meson-ninja` problem : 

There is one problem with  "meson-ninja" that makes it impossible to use for some purposes: The "meson-ninja" developers  chose  to  make the build system strip one type of information, "rpath", from executables at "install" time. This was insanity. However, the following simple patch to "meson" fixes the problem:

````python
--- meson-0.57.0.old/mesonbuild/minstall.py
+++ meson-0.57.0/mesonbuild/minstall.py
@@ -319,7 +319,8 @@
 
     def fix_rpath(self, *args: T.Any, **kwargs: T.Any) -> None:
         if not self.dry_run:
-            depfixer.fix_rpath(*args, **kwargs)
+            # depfixer.fix_rpath (*args, **kwargs)
+            print ("meson: rpath changes at install time disabled")
 
     def set_chown(self, *args: T.Any, **kwargs: T.Any) -> None:
         if not self.dry_run:
````

#### Use of `cmake`

"cmake" is used as follows:

a. "cmake" must be accessible by PATH.

b. Install dependencies.

c. Go to the appropriate source directory.  This is highest-level directory that contains a "CMakeLists.txt" file. Execute a script similar to the following:

````bash
mkdir build
cd    build
cmake \
    -DCMAKE_BUILD_TYPE=RELEASE          \
    -DCMAKE_INSTALL_PREFIX=/opt/moocow  \
    -DCMAKE_INSTALL_LIBDIR=lib          \
    ..
make && make install
````

This is obviously simple.  The problem is that,  if a  problem such as not being able to find a library occurs, it may be difficult to figure out and fix.

---

## File: server/index.md

### Server Setup



- [VPS Box](vpssetup.md) Basic Setup
- [smk’s VPS Setup](vps_setup_smk.md)
- [Application Setup](applications.md)
- [Bootup Scripts](boottime.md)
- [Nginx](nginx.md)
- [Nginx Static Site](nginx2.md)
- [Serving node.js apps](nodejs.md)
- [squid](squid.md) proxy
- [Podman Installation](podman.md)
- [Host sortable download Links](mypaste.md)
- [CPAN Modules](cpan.md) (for perl developers)
- [ZNC Setup](znc.md) 
- [Setting up Rclone](rclone.md)
- [Backup VPS with Pcloud](bkp.md)
- [A general talk with OldCoder](guide.md)

---

## File: server/mypaste.md

### Mypaste : sortable download links

This step is  for developers and is optional.  It  requires  a working
"nginx" website with PHP 7 support.  "Apache" isn't presently support-
ed for this purpose.

The following tarball  contains a directory tree that includes an "in-
dex.php" file in the top-level directory:

    /root/setupfiles/mypaste.tgz

Unpack the tarball somewhere in the website  directory tree.  Then add
files  (any that you'd like to distribute) to the  top-level directory
of the tree that you just unpacked.

If  the new tree is  accessed via the  Web,  "index.php" will  display
download links for the files that you add.

"sortable"  means that  the list of download links can be sorted based
on  any of  several  attribute columns  (filename,  modification date,
etc.).

Subdirectories are supported.

For credits,  license information, and other details, see the code and
comments in the "index.php" file.

You may or may not wish to "chown" the directory tree as follows (mod-
ify the path shown here appropriately):

    chown -R www-data.www-data /var/www/mypaste/

If  you'd like to  use this feature to  distribute files both publicly
and privately, use two separate copies of the directory tree,  one for
public files and one for private files.

---

## File: server/nginx.md

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

---

## File: server/nginx2.md

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

---

## File: server/nodejs.md

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



---

## File: server/podman.md

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

---

## File: server/rclone.md

## RCLONE

Rclone is a command-line program to manage files on cloud storage. Its feature rich and cross platform, excellent for writing scripts which stays longer than locking with a specific cloud vendors cli solution.

Users call rclone *The Swiss army knife of cloud storage*, and *Technology indistinguishable from magic*.

What I like about rclone is that is vendor lockin proof and we can apply encryption, compression, chunking, hashin and joining all costly operation for free. rclone works on all OS, be it linux, windows or freeBSD.

### Installing rclone

````bash
# on macOS
brew install rclone
# on linux
sudo apt-get install rclone
````

**[Note] : If you are using rclone and same config on various system, try to remain on same version of rclone.**

### Setup rclone

````bash
rclone config
````

- you will need to setup a remote for each cloud vendor you wish to add.
- proceed with some remote name then select your cloud vendor.
- then you will need to authenticate your rclone using token to access cloud vendor’s storage.
  - GUI System : If you have some browser, then u can use auto generate token and follow the link provided by cli
  - Headless System : In case of headless system since there is no browser what you will need to create token on some another system and add it to the headless system.



---

## File: server/squid.md

### Routing browsing through a `squid` proxy

If you wish,  you  can use your Debian server  to change your apparent country in web browsers.

One  reason to do  this would be to access content  that is restricted based on location. This will  only work,  though,  if your server's IP address  is  located in a country or region  for which  such access is permitted.

To do this, proceed as follows:

a. Determine  the  IPV4 address of the connection  that  you'd like to relocate.  One way to  do this is to go to Google  and enter  "What is my IP address?"  Another way is  to visit the following website.  Note that the URL in question uses "http" and not "https":

    http://showip.net/

b. Execute:

    sudo apt-get install squid

c. Edit the text file "/etc/squid.conf". Find this part:

    #Default:
    # forwarded_for on

Add the following setting right after that:

    forwarded_for delete

Find this part:

    #Default:
    # Deny, unless rules exist in squid.conf.

Add the following part right after that:

    acl moocow src 111.222.333.444
    http_access allow moocow

Replace 111.222.333.444 with the IPV4 address that you identified previously.

Note: You should see the following right after the new lines:

    # Recommended minimum Access Permission configuration:
    #
    # Deny requests to certain unsafe ports
    http_access deny !Safe_ports

d. sudo service squid restart

Allow 5 minutes for the preceding command to complete.

e. Install a proxy management add-on in your web browser.  Or, in some browsers, you may be able to edit network settings directly. In either case, set up your connection, or a proxy profile, as follows:

    Proxy host: 123.456.123.456
    Proxy port: 3128
    Use this proxy for all protocols
    No Proxy For: localhost; 127.0.0.1

Replace 123.456.123.456 with the IPV4 or hostname for your box.

If the last 2 settings aren't offered, proceed without them.

f. Clear your browser cache,  restart your browser,  and check the ap-
parent IPV4 address.

g. If your  client-side  IPV4  address changes,  you'll need to update "squid.conf" accordingly. Subsequently, execute:

    sudo service squid restart

Note, again, that this may take up to 5 minutes.

h. "squid"  offers  multiple benefits in addition  to location change. It's advised that you read about the program.

i. Never run "squid" without the edits discussed above.  If you do so, 100s of people  will flood in to use your proxy and you'll be held responsible for whatever they do.

---

## File: server/vps_setup_smk.md

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



---

## File: server/vpssetup.md

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



---

## File: server/znc.md

### ZNC Setup : Never miss an IRC message

---

