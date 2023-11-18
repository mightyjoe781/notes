## Setting up VSCode for RCE on M1 

This method assumes you have working QEMU machine running on M1. Following steps prepare vm for running VSCode Remote Extension which is useful in case you wish to use debugger and run commands easily.

NOTE : this doesn’t work for ssh to root because vscode assumes its in linuxulator root

NOTE : try to attach to debugger over network and nfsd

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
````

### SSH Config Block

````txt
Host freebsd-vm
    HostName 192.168.64.5
    Port 22
    User root
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

