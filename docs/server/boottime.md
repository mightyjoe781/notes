### Regarding `rc.local`

`/etc/rc.local` is a `bash` script that Linux executes at boot time. So it is a convenient place to put your own startup commands.



However, there are a few rules to remember. Failure to follow these rules is very likely to brick your box :

- You need to double-check the script and, ideally, test a copy before updating the master copy in "/etc/".  Syntax errors or other problems with the script are  very likely to brick your box.

- If the script executes potentially blocking operations,  they should  be  executed as  background processes.  Execution  of blocking  operations  in the  foreground  is  very likely  to brick your box.

- The script should be guaranteed to make it to the end and to exit there as follows : `exit 0`

- The script probably needs to be executable, though this isn’t confirmed for all distros. To make is executable, do `chmod 755 /etc/rc.local`

- Processes that will use network, such as `node.js` apps, need to wait until the network comes up before doing setup operations.

  We are going to install a script named `wait-ipv4.pl`. If that script is properly configured, you can simply call it to pause the startup process of such processes until the network is ready to go

  If you are not able to configure `wait-ipv4.pl` properly, or if you would like to be on safe side, a `sleep 60` command should provide sufficient delay

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

