## Setting up VSCode for RCE on M1 

This method assumes you have working QEMU machine running on M1. Following steps prepare vm for running VSCode Remote Extension which is useful in case you wish to use debugger and run commands easily.

NOTE : this doesn’t work for ssh to root because vscode assumes its in linuxulator root

[Resource](https://gist.github.com/mateuszkwiatkowski/ce486d692b4cb18afc2c8c68dcfe8602)

### Enable linuxulator and install linux Userland

````bash
sysrc linux_enable="YES"
service linux start
pkg install linux_base-c7

# check installation
/compat/linux/usr/bin/uname -a

# more : https://docs.freebsd.org/en/books/handbook/linuxemu/
````

### Enable bash config files

````bash
# add following .profile for the user you want to ssh
export PATH="/compat/linux/usr/sbin:/compat/linux/usr/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin"
````

### SSH Config Block

````txt
Host freebsd-vm-root
    HostName 192.168.64.5
    Port 22
    User root
    IdentityFile /Users/smk/.ssh/id_ed25519
    RemoteCommand /compat/linux/usr/bin/bash
    # RequestTTY force
    # SetEnv PATH="/compat/linux/usr/sbin:/compat/linux/usr/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin"
````

### On Host

- Add your public ssh keys in `.ssh/authorized_keys`
- Add your user to sudoers