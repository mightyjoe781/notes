# Freebsd Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: freebsd
This is part 1 of 1 parts

---

## File: freebsd/absfreebsd/ch12.md

## 12. The Z File System

Even though we are keen to improve our hardware every 5 years, but still we are using a 40 years old filesystem. While those architectures have been improved and made robust but they are still same basic architecture and prone to errors.

ZFS combines existing well-understood principles into a single cohesive, well-engineered whole with design that can be updated with new hashing or data trees or indexing algorithms without losing backwards compatibility.

ZFS is almost an operating system on its own, or perhaps a special-purpose database. Usually a install of ZFS-based FreeBSD is preferred and automatically handles prerequisties like, setting `zfs_load=YES` in `loader.conf` and `zfs_enable=YES` in `rc.local`.

ZFS has 3 main components : datasets, pools, and virtual devices.

### Datasets

A *database* is defined as a named chunk of ZFS data. ZFS includes snapshots, block devices for virtualization and iSCSI targets, clones and more, all of those are datasets. `zfs(8)` is used to manage all ZFS datasets. Execute `zfs list` to view all existing datasets.



---

## File: freebsd/absfreebsd/ch9.md

## 9. Securing your System

Securing your system means ensuring that your computer’s resources are used only by authorized people for authorized purposes. Even if you have no important data on system, you still have valuable CPU time, memory, and bandwidth.

Many folks who think their systems were too unimportant for anyone to bother breaking into found themselves an unwitting relay for an attack that disabled a major corporation. See Botnets.

Generally, OS are not broken into; the program running on OS are. Even the most paranoiac, secure-by-default OS in the world can’t protect badly written programs from themselves. Occasionally, one of those program can interact with OS in a way as to actually compromise OS. The most well-know of these are *buffer overflows*, where an intruder’s program is dumped straight into CPU’s execution space and the OS runs it. FreeBSD has undergone extensive auditing to eliminate buffer overflows as wells as myraid other well-understood security issues, but that’s no guarantee that they have been eradicated.

FreeBSD provides many tools to help secure your system against attacker, both internal and external. While no one of these tools are sufficient, all are desirable. Treat everything you learn about system security as a tool in a kit, not as the answer to all your problems.

### Who is the Enemy ?

#### Script Kiddies

Script Kiddies are not sysadmins and they are not skilled. They download attack points and work on a point-and-click basis and go look for vulnerability. To defend against : just keep your software up-to-date and follow good computing practices.

#### Disaffected Users

A organization’s employees are people most likely to know where the security gaps are, to feel that the rules don’t apply to them, and to have the time to spend breaking your security. You might have all patched and downright misanthropic firewall installed, but if anyone who knows the password is *Current93* can dial the back rook modem, you’re in trouble.

To stop people like these is simply not to be sloppy. Don’t leave projects insecurely half-finished or half-documented. When someone leaves the company, disable his account, change all administrative passwords, inform all employees of that person’s departure, and remind them not to share confidential information with that person. 

#### Botnets

Botnets are more numerous than either of the above. They are machines compromised by malware and controlled from a central point. Botnets can include millions of machines. The malware authors control the botnets and use them for anything from searching for more vulnerable hosts to sending spam or breaking into secure sites. Most botnets are composed of Windows and Linux Machines, But there is no reason why FreeBSD OS can’t be assimilated into botnets.

Fortunately, botnet defense is much like script kiddie defense; keeping your software patched and following good computing practices goes a long way.

#### Motivated Skilled Attackers

The most dangerous group - skilled attackers are competent system admins, security researchers, penetration specialists, and criminals who want access to your specific resources. Computer penetration is a lucrative criminal field these days, especially if the victim has resources that can be used for DDOS attacks or mass spam transmission. If one of these people *really* wants to break into your network, he’ll probably get there.

If you can make the intruder’s break-in plan resemble a Hollywood script no matter how much he knows about your network, your security is probably pretty good.

### FreeBSD Security Announcements

The FreeBSD Project includes volunteers who specialize in auditing source code and watching for security issues with both the base operating system and add-on software. These developers maintain a very low-volume mailing list, FreeBSD-security-notifications@FreeBSD.org, and subscribing is a good idea. While you can monitor other mailing lists for general announcements, the security notifications list is a single source forFreeBSD-specific information. To subscribe to the security notifications mailing list, see the instructions on http://lists.freebsd.org/. The FreeBSD security team releases advisories on that mailing list as soon as they’re available.

### User Security

FreeBSD has a variety of ways to allow users to do their work without giving them free rein on the system.

#### Creating User Accounts

FreeBSD uses standard UNIX user management programs such as `passwd(1)`, `pw(8)`, and `vipw(8)`. FreeBSD also includes a friendly interactive user-adding program, `adduser(8)`. Only *root* may add users, of course.

![image-20220329002843030](ch9.assets/image-20220329002843030.png)

The username is the name of account. FreeBSD lets you choose a numerical user ID (UID). FreeBSD starts numbering UIDs at 1,000; while you can change this, all UIDs below 1000 are reserved for system use. Just press enter to take next available UID.

![image-20220329003048086](ch9.assets/image-20220329003048086.png)

The user’s default group is important. The FreeBSD default of having each user in their own group is usually the sensible way for most setups. Any of big thick books on system administration offers several grouping schemes.

A login class specifies what level of resource the user has access to.

The *shell* is command line environment. While system default is /bin/sh, I prefer tcsh.

The home directory is where the user’s files reside on disk. The user and the user’s primary group own this directory. You can set custom permissions on the directory if you want, probably so that other users can’t view this user’s directory.

#### Configuring Adduser : /etc/adduser.conf

Creating new users on some Unix systems requires you to manually edit `/etc/passwd`, rebuild the password database, edit `/etc/group`, create a home directory, set permission on that directory, install dotfiles, and so on.

`/etc/adduser.conf` lets you set requirements as defaults while retaining the high degree of automation. To create `adduser.conf`, run `adduser -c` and answer the questions.

#### Editing Users

FreeBSd includes several tools for editing accounts, the simplest are `passwd(1)`, `chpass(1)`, `vipw(8)`, and `pw(8)`. These work on tightly interrelated files `/etc/master.passwd`, `/etc/passwd`, `/etc/spwd.db` and `/etc/pwd.db`.

`/etc/master.passwd` is authoritative source of user account information and includes user passwords in encrypted form.

Any time any standard user management program changes the account information in `/etc/master.passwd`, FreeBSD runs `pwd_mkdb(8)` to update other three files.

**Changing a Password**

Use `passwd(1)` to change passwords.

![image-20220329004438328](ch9.assets/image-20220329004438328.png)

**Changing Accoutns with chpass(1)**

if you use `chpass`, you will get an editro with following text : 

![image-20220329004548626](ch9.assets/image-20220329004548626.png)

If you use `chpass <username>` as root you will get even more options to modify.

**The Big Hammer : vipw(8)**

`vpiw` helps edit multiple user at a time. A FreeBSD system considers `/etc/master.passwd` in case of conflicts with other password files.

Each line in `/etc/master.passwd` is a single account record containing 10 colon-sepearated fields. These fields are the following : 

Username;Encrypted Password, UserID, Group ID, User’s Class, Password Expiration; Account Expiration; Personal Data; User’ Home Directory; User’s Shell.

**Removing a User**

The `rmuser(8)` program deletes user accounts.

**Scripting with `pw(8)`**

Very useful command to lock users and while account is locked, account is active, nobody can log in to it.

`pw lock xistence`

`pw unlock xistence`

### Shells and /etc/shells

The *shell* is the program that provides the user’s command prompt. The file `/etc/shells` contains a list of all legitimate user shells. If you compile your own shell without using a FreeBSD port, you must list the shsell by its complete path in `/etc/shells`.

The FTP daemon won’t allow a user to login via FTP if his shell isn’t listed in `/etc/shells`

### root, Groups, an Management

#### The root Password

Certain actions require absolute control of the system, including manipulating core system files such as the kernel, device drivers, and authentication systems. Such activities are designed to be performed by root.

To use the root password, you can either login as root at console login prompt or, if you’re a member of group wheel, log in as yourself and use the switch user command `su(1)`. It logs who uses it and can be used on a remote system.

One of the simplest ways to reduce the need for root access is the proper use of the groups.

#### Groups of Users

- A *group* is a way to classify users with similar administrative functions.
- A *sysadmin* can define a group *webmasters*, and add accounts of people with privilages to edit web-related files or create a group *email* and add email administrators to that group.
- To check your group type `id` on a console.

**/etc/group**

- The file `/etc/group` contains all group information except for the user’s primary group (which is defined with user account in `/etc/master.passwd`).

- Each line is four colon-delimited fields : the group name, group password, the group ID number, and a list of members.

  Example entry : `wheel:*:0:root,mwlucas,xistence`

- Second field group password, turned out to be a big nightmare. Modern Unix-like systems don’t do anything with group password, but field remains because old program expect to find something in this space. Asterisk is just a placeholder.

**Changing group Memberships**

- Just simply add user’s name into the list of member in `/etc/group` of respective group you want to add user to.

**Creating Group**

- For creating you only need a name for the group and a group ID. Technically, you don’t need a member for the group; some programs run as members of a group, and FreeBSD uses group permissions to control those programs similar to users.
- GIDs are generally assigned as next number in list but can be arbitrary number between 0 and 65535.

#### Using Groups to Avoid Root

#### System Accounts

- FreeBSD reserves some user account names for integrated programs. e.g. nameserver runs under the user account bind and group bind. If an intruter compromises the nameserver, she can access the system only with privileges of the user bind.
- Don’t have user log in as these users. They are not setup as interactive accounts by design.
- Create a separate user and group to own program files. That way, our hypothetical intruder can’t even edit the files used by DNS server, minimizing potential damage.
- Similarly database should not be allowed to edit its own config files.

#### Administrative Group Creation

Simplest way to create a group that owns files is to employ `adduser` to make a user that owns them and then to utilize that user’s primary group as the group for the files. Because we already have a user called `bind`, we will create an administrative user `dns`. Username isn’t important, but you can choose a name that everyone will recognise.

Give you administrative user a shell of `nologin`, which sets a shell of `/sbin/nologin`. This prevents anyone from actually loggin in as the administrative user.

Do not add this administrative user to any other groups. Under no circumstances add this user to a privileged group, such as wheel !

Every user needs a home directory. For an administrative user, a home directory of `/nonexistent` works well. This user’s files are elsewhere in the system, after all.

Lastly, let `adduser(8)` disable the account. While the shell prevents logins, an extra layer of defense won’t hurt.

To change the file’s owner and group, use `chown(1)`

`chown dns:dns rndc.key`

#### Interesting Default Groups

````
audit  : Users who can access audit(8) information
authpf : Users who can authenticate to the PF packet filter
bin 	 : Group owner of general system programs
bind   : Group for the BIND DNS server software
daemon : Used by various system services, such as the printing system
_dhcp  : DHCP client operations
dialer : Users who can access serial ports; useful for modems and tip(1)
games  : Owner of game files
guest  : System guests (almost never used)
hast   : Files used by hastd(8)
kmem   : Programs that can access kernel memory, such as fstat(1), netstat(1), and so on
mail   : Owner of the mail system
mailnull:Default group for sendmail(8) or other mail server
man    : Owner of uncompressed man pages
network: Owner of network programs like ppp(8)
news   :Owner of the Usenet News software (probably not installed)
nobody : Primary group for unprivileged user nobody, intended for use by NFS
nogroup: Group with no privileges, intended for use by NFS
operator:Users that can access drives, generally for backup purposes
_pflogd: Group for PF logging
proxy  : Group for FTP proxy in PF packet filter
smmsp  : Group for Sendmail submissions
sshd   : Owner of the SSH server (see Chapter 20)
staff  : System administrators (from BSD’s college roots, when users were
staff, faculty, or students)
sys    : Another system group
tty    : Programs that can write to terminals, like wall(1)
unbound: Files and programs related to the unbound(8) DNS server
uucp   : Group for programs related to the Unix-to-Unix Copy Protocol
video  : Group that can access DRM and DRI video devices
wheel  : Users who may use the root password
www Web: server programs (not files)
_ypldap: Files needed by the LDAP-backed YP server ypldap(8)
````

### Tweaking User Security

#### Restricting Login Ability

FreeBSD checks `/etc/login.access` for rules that forbid logins from users. This file has no rules by default, meaning everyone who provides valid password and username has no restrictions.

The `/etc/login.access` has three colon-delimited fields.

- (+) grants or (-) denies the right to login
- list of users or groups
- list of connection sources

Usage of `ALL` or `ALL EXCEPT` is allowed to make simple but expressive rules.

For example, to allow only members of wheel group to login from system console.

```
+:wheel:console
```

NOTE : There is a problem with this rule, although it allows wheel users to login from console, but if there is a user named Bert who is no wheel, but if he tries to login, no rule denies him access.

Correct Rule should be.

````
+:wheel:console
-:ALL :consoles
````

or similar rule using `ALL EXCEPT`

```
-:ALL EXCEPT wheel: console
```

Change the default from “allow access” to “deny access” by adding a final rule.

```
-:ALL:ALL
```

**Hostnames**

```
-:ALL EXCEPT WHEEL:fileserver.mycompany.com
```

Users in the wheel group can login from the fileserver, but nobody else can.

**Host Addresses and Networks**

Host addresses work like hostnames except they are immune to DNS failures or spoofing.

```
-:ALL EXCEPT wheel : 203.0.11.345
```

A network number is truncated IP Address, like this : 

```
-:ALL EXCEPT wheel : 203.0.113.
```

**LOCAL**

Anyone who owns a block of IP addresses can give their addresses any desired reverse DNS. The `LOCAL` restriction is best avoided.

**ALL and ALL EXCEPT**

```
-:ALL EXCEPT wheel: ALL EXCEPT 203.0.113.128 203.0.113.44
```

**Tie It All Together**

The point of these rules is to build a login policy that matches your real-world policies. If you provide generic services but only allow your sysadmin to log on remotely, a one-line `login.access` prevents any other users from loggin in.

Generally this configuration is quite used at several ISPs

````
-:ALL EXCEPT wheel: console
-:ALL EXCEPT wheel dns webmasters: ALL
````

This allows sysadmins to login via console and allow web teams and DNS teams to login remotely.

#### Restricting System Usage

You can provide more specific controls with login classes `/etc/login.conf`.

**Class Definitions**

The default `login.conf` starts with the default class, the class used by accounts without any class and gives unlimited access to system resources.

Each class definition consists 

---

## File: freebsd/absfreebsd/index.md

## Absolute FreeBSD

- Chapter 1. Getting More Help
- Chapter 2. Before You Install
- Chapter 3. Installing
- Chapter 4. Start me up! The Boot Process
- Chapter 5. Read this before you break something else
- Chapter 6. Kernel Games
- Chapter 7. The Network
- Chapter 8. Configuring Network
- [Chapter 9. Securing you System](ch9.md)
- Chapter 10. Disks, Partitions, and GEOM
- Chapter 11. The UNIX File System
- [Chapter 12. The Z File System](ch12.md)
- Chapter 13. Foreign File System
- Chapter 14. Exploring /etc
- Chapter 15. Making your System Useful
- Chapter 16. Customizing Software with Ports
- Chapter 17. Advanced Software Management
- Chapter 18. Upgrading FreeBSD
- Chapter 19. Advanced Security Features
- Chapter 20. Small System Services
- Chapter 21. System Performance and Monitoring
- Chapter 22. Jails
- Chapter 23. The Fringe of FreeBSD
- Chapter 24. Problem Reports and Panics

---

## File: freebsd/freebsd_m1.md

## FreeBSD Development Environment on M1 Macs



I was a GSoC (Google Summer of Code) student in year 2023 and it was very interesting summer to spend working with Warner Losh on Designing CI Boot Loader Test Harness for different FreeBSD Architectures. Main Idea of project was to write several qemu recipes for pretty much most of first tier architectures in FreeBSD, and somehow make the script user friendly enough so people can drive it via a config, later this config can integrated on FreeBSD CI systems to remove the possibility of shipping broken Bootloader.

WiFi support on FreeBSD has been a lot shaky mostly due to manufactures not sharing specs to their WiFi Hardware. I had a old laptop that I used to install FreeBSD and work little bit on, but without a WiFi in this modern day, it was a difficult developer experience.

Later Warner arranged a Jail running on his bare metal server rack for me to connect via ssh. This was a temporary arrangement for me to proceed with the summer. And I always wanted to develop things locally. I tried various methods to get VSCode running on FreeBSD remotely but could not make it work. Finally for the entire summer project I was working on my local and pushing my changes to git, then logging into the server via ssh, and pulling in the changes from git. A long tiring process.

After this struggle I was keen on finding the solution for this problem so I found this article online by John Grafton (https://www.jrgsystems.com/) who seems to share similar interest in MacBook developement Environments as me. So I set out to emulate his development environment across my M1. Following Steps are more of personal note for me to remember what I did to make this work.

### 1. Creating a FreeBSD QEMU VM

[Reference](https://gist.github.com/ctsrc/a1f57933a2cde9abc0f07be12889f97f)

1. Installing X-Code
2. Installing Homebrew and QEMU
3. Download pre-build EDKII OVMF EFI image for QEMU
4. Prepare pflash for non-volatile variable store, such as screen-resolutions etc.
5. Download FreeBSD arm64 image
6. Decompress VM image
7. Grow Image Size
8. Run QEMU using this script

#### Installing X-code

```
xcode-select --install
```

#### Installing Homebrew and QEMU

````bash
brew install qemu wget
rehash
qemu-system-aarch64 --version
````

#### Download pre-build EDKII OVMF EFI image for QEMU

[Link](https://gist.github.com/niw/4f1f9bb572f40d406866f23b3127919b/raw/f546faea68f4149c06cca88fa67ace07a3758268/QEMU_EFI-cb438b9-edk2-stable202011-with-extra-resolutions.tar.gz) : Please Check references if link doesn’t work

#### Prepare pflash for non-volatile variable store, such as screen-resolutions etc.

````bash
mkdir ~/qemu-vm/
cd ~/qemu-vm/
tar xvf ~/Downloads/QEMU_EFI-cb438b9-edk2-stable202011-with-extra-resolutions.tar.gz
dd if=/dev/zero of=pflash0.img bs=1m count=64
dd if=/dev/zero of=pflash1.img bs=1m count=64
dd if=QEMU_EFI.fd of=pflash0.img conv=notrunc
dd if=QEMU_VARS.fd of=pflash1.img conv=notrunc
````

#### Download FreeBSD arm64 image

````
wget https://ftp2.uk.freebsd.org/pub/FreeBSD/releases/VM-IMAGES/14.0-RELEASE/aarch64/Latest/FreeBSD-14.0-RELEASE-arm64-aarch64.raw.xz
````

#### Decompress VM image

````bash
mv ~/Downloads/FreeBSD-14.0-RELEASE-arm64-aarch64.raw.xz .
unxz -k FreeBSD-14.0-RELEASE-arm64-aarch64.raw.xz
````

#### Grow Image Size

````bash
qemu-img resize -f raw FreeBSD-14.0-RELEASE-arm64-aarch64.raw +60G
````

#### Run QEMU using this script

````bash
echo "
qemu-system-aarch64 \
  -M virt \
  -accel hvf \
  -cpu host \
  -smp 4 \
  -m 8192M \
  -drive file=pflash0.img,format=raw,if=pflash,readonly=on \
  -drive file=pflash1.img,format=raw,if=pflash \
  -device virtio-gpu-pci \
  -display default,show-cursor=on \
  -device qemu-xhci \
  -device usb-kbd \
  -device usb-tablet \
  -device intel-hda \
  -device hda-duplex \
  -drive file=FreeBSD-14.0-RELEASE-arm64-aarch64.raw,format=raw,if=virtio,cache=writethrough \
  -serial mon:stdio \
  -audiodev none,id=hdac \
  -nic vmnet-shared \
  -nographic
" >> freeBSD.run
chmod +x freeBSD.run
````

### 2. Setting up NFS on M1

[Reference](https://www.jrgsystems.com/posts/2023-09-08-developing-freebsd-on-macos/)

1. Write Exports File
2. Enable nfsd on M1
3. Checking nfsd is working correctly

#### Write Exports File

````txt
### /etc/exports on MacBook
/System/Volumes/Data/smk -ro -alldirs 192.168.64.2
# Note this represents the IP which will be able to access the NFS hosted at 192.168.64.1
# to know the IP of your qemu machine, you have to run ifconfig on it and add it here
````

#### Enable nfsd on M1

````bash
nfsd start
# note any changes to nfsd exports file will require you to execute following command
# nfsd update

# more information about nfsd in man page
````

#### Checking nfsd is working correctly

````bash
# from the host (M1), by default it looks at localhost
showmount -e
# another way is use finder and type : <Ctrl>-k
# and type in this url : nfs://192.168.64.1:/System/Volumes/Data/Users/smk/personal

# from the client (FreeBSD)
showmount -e 192.168.64.1
# if this doesn't work then mostly IP is not whitelisted in exports file
````

### 3. Post Setup

1. Mounting Local FreeBSD folder inside the QEMU-VM
2. Build World and Build Kernel (Probably will need it :)

#### Mounting Local FreeBSD src folder inside the QEMU-VM

````bash
mount -v -t nfs 192.168.64.1:/System/Volumes/Data/Users/smk/personal/gsoc/fbsd /usr/src

# to unmount it 
umount -a -t nfs,nullfs

# a more correct way to automatically mount this would be to either write this in fstab file or maybe a one line bash script
````

#### Build World and Build Kernel (Probably will need it :)

````bash
make -j `sysctl -n hw.ncpu` -DWITHOUT_SYSTEM_COMPILER buildworld buildkernel

# look at ntfy build notification :) cause it takes around 1:40hrs to execute both command on M1(MBP13) with above specs on VM
````

For any issues you can mail me at : smk@FreeBSD.org

---

## File: freebsd/freebsd_m1_vscode.md

## Setting up VSCode for RCE on M1 

This method assumes you have working QEMU machine running on M1. Following steps prepare vm for running VSCode Remote Extension which is useful in case you wish to use debugger and run commands easily.

NOTE : this doesn’t work for ssh to root because vscode assumes its in linuxulator root

**NOTE : This setup can’t run `make buildworld buildkernel` becuase while changing `.profile` we change priority of many binaries. To run buildworld or buildkernel disable path export in `.profile`**

NOTE : its possible you are connecting to wrong host, as it might very on system restarts. Use `ifconfig` to check ip to ssh.

NOTE : try to attach to debugger over network and nfsd

NOTE : Sometimes dhcp doesn’t work properly on m1 host, usually due to system upgrades and reboots. execute this if your qemu machine doesn’t get an ipv4 address on host. since we run vm in host mode, bootpd offers the DHCP lease

````bash
# add bootpd to firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/libexec/bootpd
# allow bootpd to run thru firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblock /usr/libexec/bootpd
````

[Resource](https://gist.github.com/mateuszkwiatkowski/ce486d692b4cb18afc2c8c68dcfe8602)

### On Host Machine Setup User

- Create a user

````bash
# execute
adduser
# follow thru default for most of options but make sure to add user to wheel user group
````

- Add your public ssh keys in `.ssh/authorized_keys`

````bash
# become user & add your public key to authorized_keys
su - smk
mkdir .ssh
touch .ssh/authorized_keys
chmod 700 .ssh
echo "YOUR_KEY" >> .ssh/authorized_keys
````

Enable sshd service (if not enabled)

````bash
# add this line to /etc/rc.conf
echo "sshd_enable=YES" >> /etc/rc.conf

# or alternatively use
# sysrc sshd_enable="YES"

reboot
service sshd restart

# to watch login logs for debug
tail -f /var/log/auth.log

# from you mac
ssh <user>@<ip> -i <identity_file>
````

- Add your user to sudoers

````bash
# install sudo
pkg install sudo wget curl

# always use visudo to edit sudoers file or else system can brick
visudo

# uncomment any one of these lines, based on preference
# %wheel ALL=(ALL:ALL) ALL
# %wheel ALL=(ALL:ALL) NOPASSWD: ALL

su - smk
sudo whoami
# should be root
````

### Enable linuxulator and install linux Userland

````bash
sysrc linux_enable="YES"
service linux start
pkg install linux_base-c7

# check installation
/compat/linux/usr/bin/uname -a
# sometimes first install don't work fine until reboot
reboot

# more : https://docs.freebsd.org/en/books/handbook/linuxemu/
````

### Enable bash config files

````bash
# add following .profile for the user you want to ssh
export PATH="/compat/linux/usr/sbin:/compat/linux/usr/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin"

# note on next login make sure .profile is loaded and echo $PATH is same as what you set
# only login shells load .profile so its possible it may not be set when ssh freebsd-vm is used, check this is loaded on vscode terminal
````

### SSH Config Block

````txt
Host freebsd-vm
    HostName 192.168.64.5
    Port 22
    User smk
    IdentityFile /Users/smk/.ssh/id_ed25519
    RemoteCommand /compat/linux/usr/bin/bash
    RequestTTY force
````

### On VSCode

- Now install `remote ssh` plugin on VS-Code
- Make sure this is enabled : `remote.SSH.enableRemoteCommand": true`
- `<cmd>+<shift>+p` and look for remote ssh : connect to host : freebsd-vm
- `<cmd>+<shift>+p` and look for preferences : open remote settings (freebsd-vm)
- Add following config specifying shell you wish to enable : 

````json
{
    "terminal.integrated.defaultProfile.linux": "bash"
}
````

- Reconnect to host and you got a shell yay



ping on discord or connect via smk@freebsd.org | smk@minetest.in if you face any trouble


---

## File: freebsd/gsoc/debug.md

# Debug Notes

## notes on script design



## nfs attach script

````bash
# notes - follow freebsd-m1 setup page
echo "mount -v -t nfs 192.168.64.1:/System/Volumes/Data/Users/smk/personal/gsoc/fbsd/tools/boot/bootloader_test /root/freebsd-src/tools/boot/bootloader_test" >> mount.sh
chmod +x mount.sh
# later configure to execute on bootup
````

- There is an issue when mounting entire freebsd-src from Mac. Seems like its attaching in a read-only mode which interferes with `buildworld`, `buildkernel` steps
- There is another issue while running `amd64` builds from `arm64` qemu running requires to build toolchain

````bash
# building toolchain
cd freebsd-src
# assumes buildworld and buildkernel is done
make -j `sysctl -n hw.ncpu` TARGET=amd64 TARGET_ARCH=amd64 toolchain
# optionally could use : toolchains to build everything
````



## notes on amd64

- really already been solved by warner

## notes on arm64

- Check nfs attach script section’s 2nd portion

## notes on riscv

default boot mode for my script is using opensbi

````bash
# install opensbi & optionally u-boot
pkg install opensbi u-boot-qemu-riscv64
````

## notes on armv7

This image is always released as IMG file, which could be tricky to handle in bootloader_tests script which is a lua script.

- Decided to convert `.img` into `.iso`

How do we get all the files ?

````bash
# uncompress the xz
xz -k FreeBSD-13.2-RELEASE-arm-armv7-GENERICSD.img.xz

# then create a virtual device with this uncompressed image
mdconfig -a -t vnode -f FreeBSD-13.2-RELEASE-arm-armv7-GENERICSD.img -u 0
# this should mount the virtual device as md0 & confirm it as
mdconfig -l
ls /dev/md0*		# output should be md0, md0s1, md0s2, md0s2a

# lets find out file-system of each of them
file FreeBSD-13.2-RELEASE-arm-armv7-GENERICSD.img
fstyp /dev/md0s2a			# this should be required ufs partition

# mounting
mount -t ufs /dev/md0s2a /mnt/armv7

# cleanup: unmount & delete virtual device
unmount /mnt/armv7
mdconfig -d -u 0

# reference
# discord discussions & https://gist.github.com/yzgyyang/4965d5673b5c79c644a695dd75fa8e05
# https://www.freebsddiary.org/iso-mount.php
# https://www.cs.ait.ac.th/~on/technotes/archives/2013/12/11/mount_a_file_system_image_in_freebsd/index.html
````

Creating ISO

````bash
# install cdutils
pkg install sysutils/cdrtools

# in qemu cd-writer needs to configured so rather let's write the folder into iso
# method-1 directly make iso from /mnt/armv7
mkisofs -o FreeBSD-13.2-RELEASE-arm-armv7-bootonly.iso /mnt/armv7

# method-2 cause big image :(
cp -r /mnt/armv7 ~/data_src/armv7
mkisofs -o FreeBSD-13.2-RELEASE-arm-armv7-bootonly.iso ~/data_src/armv7

# if not in qemu
cdrecord dev=md0 imagefile.iso

# reference : https://docs.freebsd.org/en/books/handbook/disks/#creating-cds
````

````bash
# armv7 requires
pkg install sysutils/u-boot-qemu-arm
````



## notes on powerpc64

adalava, dbaio, jhibbits on efnet:#powerpc64

- There is no `loader.efi`, freebsd-doesn’t support efi boot



## notes on CI process

## notes on parallelisation of tests

## notes on python port


---

## File: freebsd/gsoc/index.md

## GSoC

This page documents the GSoC journey for the project that I will be doing with Warner Losh.

[Debug Notes](debug.md)

[Setup Notes](setup.md)

### Short Description

FreeBSD supports multiple architectures, file systems, and  disk-partitioning schemes. Currently, there is a script named  full-test.sh located in src/tools/boot/ that creates several of these  environments but does not test all of them. The proposed idea is to  rewrite the script in a language such as Python or Lua, which would  allow for testing of all the architecture combinations supported in the  first and second-tier support, and provide a report on any broken  combinations and expected functionality. Additionally, providing Linux  Boot support using Linux EFI shim(EDK) II for amd64 and arm64. If time  permits, further exploration could be done to integrate the script into  the existing build infrastructure (either Jenkins or Github Actions) to  generate a comprehensive summary of the test results.

### Design Discussion

- WIP [Need to write this section]

### Deliverables

- There exists one single main.lua script when invoked will test all  the possible arch-interface-file_system-encryption combination 
- Figuring out sane defaults for all config combination : Lots of Work \0-0/ :P 
- You could provide a config.lua to run custom tests rather than sane defaults 
- Try to integrate the script in the existing FreeBSD Infra (If time permits) 

### Important Dates

- May 29th: Start of coding 
  - You'll be doing this in the first week 
- June 5th: Week 2 
  - You plan to do this in the second week 
- July 10th - July 14th: Mid-term Evaluations #1 
- August 21st - August 28th: Final-term Evaluations #2 
- September 5th: End of coding (soft) 
  - You may wish to use this time to complete documentation etc 
- Nov 6th: End of coding (hard) 

### Weekly Check-in

- [Week 1 (29 May) ](week/week1.md)
  - Successfully deployed a FreeBSD server and established build sytem on Racknerd VPS
  - Acquired foundation knowledge of Lua programming and explored the design principles of the project, include module systems.
  - Deliberated and finalized the syntax for the project, as well as devised a robust approach to process user inputs effectively and efficiently.
- Week 2 (4 Jun)
  - Developed `combination.lua`, a script that computes and parses regex strings in the specified format: `<arch>-<file-system>-<boot-partition>-<encryption>`
  - Implemented `optparse` for the `main.lua` file, enabling efficient command-line option parsing and handling.
  - Created `parser.lua` to significantly improve accuracy of parsing of `input.conf` ensuring correct and reliable data extraction.
- [Week 3 (12 Jun)](week/week3.md)
  - Configured `ntfy` on Warner’s Server to enable seamless notifications for build events.
  - Successfully build the `freebsd-src` on the server, ensuring smooth and error-free process.

  - Established a streamlined development workflow, optimizing collaboration and productivity.
- Week 4 (19 Jun)
  - Successfully finalized the `build.lua` script, incorporating extensive design and significant rewrites of the previous code.
  - Achieved comprehensive functionality through careful planning and meticulous execution.
- [Week 5 (26 Jun)](week/week5.md)
  - Successfully configured luarocks on FreeBSD Server.

  - Conducted a smoke test on the “amd64:amd64-gpt-ufs-none” architecture combination to ensure smooth functionality.


- Week 6 (3 July)
  - Wrote `test.lua` script, ensuring its successful design and completion.
  - Evaluated and streamlines the consicise reporting process for all build runs.
  - substantially progressed with the coding tasks, meeting expected milestones.
- Week 7 (10 July) - MidTerm Evaluations [Week Off Work]
- Week 8 (17 July)

  - Enhacned code styling and resolved potential design issues to improve overall script.
  - Conducted in-depth testing to ensure robutstness of script and addressing several small issues.

- [Week 9 (24 July)](week/week9.md)
  - Start working on externalising as much as freebsd related stuff to a `freebsd-util` script while generalising the functionality of `build` script.
  - Above decision will allow me to easily integrate support for all remaining architectures.
  - Start working on collecting qemu recipes for different architectures.
  
- Week 10 (31 July)

  - first script end to end works correct

- Week 11 (7 Aug)

  - all amd64 combination work correctly
  - encountered issues in running arm64 on qemu Synchronous Exception Faults

- Week 12 (14 Aug)

  - fixing up issues in various parts of the script
  - fixing a critical overwrite flaw in the script

- Week 13 (21 Aug) - Final Evaluations

  - all arm64 combination work correctly


Extension for 4 weeks


- Week 14 (28 Aug)

  - trying to get the riscv64 boot up using openSBI
- Week 15 (4 Sept)

  - riscv64-zfs-gpt-none(encryption) & riscv64-ufs-gpt-none(encryption) works fine and builds successfully.
- Week 16 (11 Sept)

  - blocked due to not able to get the arm sd image to extract correctly
  - consulted with kyle evans with suggestion to look at mounting the partitions of image
- Week 17 (18 Sept) [Kinda Busy week]
- Week 18 (25 Sept)

  - will work on creating a custom image for arm image and host it somewhere.

### Meeting Notes

- ̛amd64 -> aarch64 -> riscv (gpt only ufs/zfs with opens) -> armv7(ufs with gpt/mbr works, check for zfs) -> powerpc64 (ufs/zfs on openfirmware) -> i386 -> powerpc32

### Important Links

- Github : [Link](https://github.com/mightyjoe781/freebsd-src/tree/bootloader-smk)

---

## File: freebsd/gsoc/setup.md



# Setup

## Cloud VMs





## M1 Mac VMs

## Quick setup arm64-VM

````bash
# install packages 
pkg install git opensbi qemu-8.1.1 ntfy lua54 lua54-luarocks vim tmux

# lua packages
luarocks54 install posix luacheck

# clone the freebsd-src repo
git clone https://github.com/mightyjoe781/freebsd-src && cd freebsd-src

# own object and src dir
chown smk:wheel /usr/src /usr/obj
# make buildworld buildkernel
make -j `sysctl -n hw.ncpu` -DWITHOUT_SYSTEM_COMPILER buildworld buildkernel
make -j `sysctl -n hw.ncpu` TARGET=amd64 TARGET_ARCH=amd64 toolchain

# save mount script
mkdir -p ~/freebsd-src/tools/boot/bootloader_test
echo "mount -v -t nfs 192.168.64.1:/System/Volumes/Data/Users/smk/personal/gsoc/fbsd/tools/boot/bootloader_test /root/freebsd-src/tools/boot/bootloader_test" >> mount.sh
chmod +x mount.sh


# run a basic test
lua54 main.lua -a amd64:amd64 -f ufs -i gpt -e none
````





---

### Notes

amd64, arm64, riscv, armv7, powerpc/64

Running qemu with script
qemu-system-riscv64: Unable to find the RISC-V BIOS "/usr/local/share/opensbi/lp64/generic/firmware/fw_jump.elf"

- make toolchain

### Armv7

- Image is not there
- Mount Issues were there
- compressed.tgz for now its fine, later decide where to host the resources

### Open Items

- Explore python for running test parallel
- move towards CI side of things 

### powerpc & powerpc64

- finding correct Recipe 
- Powerpc64 with openfirmware

-----

115049 -- security code



---

## File: freebsd/gsoc/week/week3.md

## Week 3

Timeline : 12 Jun

### Setup ntfy

`ntfy` is very useful notification application and its open-source. Using ntfy you can send notification via any push notification services like pushover.

- Purchase one-time pushover service at 5$.
- Setup ntfy.

````bash
sudo pkg install ntfy
````

I used my old `ntfy.yml` by sending it to server directly from my server. (Assuming that server has been setup properly locally in `conf` file.)

```bash
scp prismo:~/.config/ntfy/ntfy.yml gsoc:~/.config/ntfy/ntfy.yml
```

### Build FreeBSD Source Tree

Useful Resources : 

- https://klarasystems.com/articles/freebsd-developer-workstation-setup/

````bash
# Install my source tree
git clone git@github.com:mightyjoe781/freebsd-src.git --branch bootloader-smk fbsd-smk
cd fbsd-smk

# maybe you will need sudo for this
chown smk:smk /usr/src /usr/obj

# assuming ntfy is setup correctly lets build tree with env
ntfy done make -j `sysctl -n hw.ncpu` -DWITHOUT_SYSTEM_COMPILER buildworld buildkernel


# Warner wanted one kernel for arm64 for override
mkdir -p $HOME/stand-test-root/override/arm64-aarch64
sudo -E make installkernel DESTDIR=$HOME/stand-test-root/override/arm64-aarch64 TARGET=arm64
````

### Setup Development Workflow

- Following tooling seems to work fine for me these days. Its adapted from my own server to work in freebsd servers.

````bash
# my setup works for only bash for now
# first get my dotfiles
git clone https://github.com/mightyjoe781/.dotfiles

# install required tools
sudo pkg install stow tmux vim neovim

# go in .dotfiles
cd .dotfiles
# i think i changed this so i don't need this but doesn't hurt to copy
cp ~/.dotfiles/bash/.bashrc ~

# ignore pushd and popd errors in FreeBSD
chmod +x install
./install

# this should stow most of required stuff
# .bashrc.d way of setting up things i learned from ghoti :P
cp -r ~/.dotfiles/bash/.bashrc.d ~
cp ~/.dotfiles/vim/.vimrc ~

# Open vim and execute :PlugInstall
# need to work on making tmux working panels
````

### build.lua module progress

- There are two ways build.lua works atm, depending on linuxboot flag (wait did I ever decide how to enable it oops)
  - LinuxBoot
  - FreeBSD Boot
- This week FreeBSD Boot should be in atleast complete shape to keep up with timelines, Next week could take up configuring `test.lua` for running those FreeBSD trees using `qemu`
- Later that I can work on bringing the Linux Kernel Boot working (wait that reminds me of extra custom kernel warner hosted)
- 
- 

### ToDo

- This setup seems to have the VSCode Remote Extension working, but i do not wish to destroy my current jail following some random gist :P. but that is what jail is for (another smk shouts from corner lol) 
  https://gist.github.com/mateuszkwiatkowski/ce486d692b4cb18afc2c8c68dcfe8602
- Let’s try to focus on testing via qemu and completing the build script for this week.



---

## File: freebsd/gsoc/week/week5.md

## Week 5

Timeline (26 Jun)

### Installing Luarocks on Freebsd

```
pkg install lua54-luarocks
```

Installing posix

```
luarocks54 install posix
```



---

## File: freebsd/implement/index.md

### Design and Implementation of FreeBSD 4.4

#### I : Overview

Chapter 1 : History and Goals

Chapter 2 : Design Overview of FreeBSD

Chapter 3 : Kernel Services

#### II : Processes

Chapter 4 : Process Management

Chapter 5 : Security

Chapter 6 : Memory Management

#### III : I/O System

Chapter 7 : I/O System Overview

Chapter 8 : Devices

Chapter 9 : The Fast Filesystem

Chapter 10 : The Zettabyte Filesystem

Chapter 11 : The Network Filesystem

#### IV : Interprocess Communication

Chapter 12 : Interprocess Communication

Chapter 13 : Network-Layer Protocols

Chapter 14 : Transport-Layer Protocols

#### V : System Operation

Chapter 15 : System Startup and Shutdown





---

## File: freebsd/index.md

## FreeBSD

### Notes

- [First Install/Setup](install.md)
- [FreeBSD Development Environment on M1](freebsd_m1.md)
- [FreeBSD Development Environment on M1 - VSCode Remote Extension](freebsd_m1_vscode.md)
- [Absolute FreeBSD](absfreebsd/index.md)
- [Design and Implementation of FreeBSD 4.4](implement/index.md)

### GSoC

- [GSoC Journey](gsoc/index.md) [To Document :)]

### Books

- Absolute FreeBSD
- Design and Implementation of FreeBSD 4.4

### Resources

- [FreeBSD Handbook](https://docs.freebsd.org/en/books/handbook/)

---

## File: freebsd/install.md

## Installing FreeBSD



## Settingup FreeBSD Install

### Updating Installation

### Setting up pkg

### Installing important pkgs

### Setting up ports

### Setting up jails

### Setting up linuxulator

### Setting up poudrie


---

## File: freebsd/new_file.md

### 1. Device Drivers

2. ### Creating Documentation

3. ### Automated Testing

4. ### Code Analysis

5. ebpf interpretor : dtrace hooks

6. ### Capsicumization of the base system

7. 

---

