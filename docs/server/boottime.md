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

