# systemd

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

Although some folks hate systemd :). I am more keen on solving my problem rather than getting into that debate. I still use init on my freeBSD instances.

Since I occasionally encounter system running systemd, I think there is no hard in getting familiar with it.

### Basic Commands

````bash
# start a service
sudo systemctl start servicename

# stop a service
sudo systemctl stop servicename

# restart a service
sudo systemctl restart servicename

# reload a service
sudo systemctl reload servicename

# enable a service
sudo systemctl enable servicename

# disable a service
sudo systemctl disable servicename

# check service status
sudo systemctl status servicename
````

#### Sytem Management

````bash
sudo systemctl reboot
sudo systemctl poweroff
sudo systemctl suspend
systemctl status
````

### Creating a Custom Service

Create `/etc/systemd/system/myservice.service`

````ini
[Unit]  
Description=My Custom Service  
After=network.target  

[Service]  
ExecStart=/usr/bin/myscript.sh  
Restart=on-failure  

[Install]  
WantedBy=multi-user.target  
````



````bash
# reload daemon
sudo systemctl daemon-reload
# enable the service
sudo systemctl start myservice  
sudo systemctl enable myservice
````

### Timers (Cron Alternatives)

Create a timer file : `/etc/systemd/system/mytimer.timer`

````ini
[Unit]  
Description=Run My Script Daily  

[Timer]  
OnCalendar=daily  
Persistent=true  

[Install]  
WantedBy=timers.target  
````

Create a Service File : `/etc/systemd/system/mytimer.service`

````ini
[Unit]  
Description=My Timer Service  

[Service]  
ExecStart=/usr/bin/myscript.sh
````

````bash
sudo systemctl enable mytimer.timer
sudo systemctl start mytimer.timer
````

### Debugging 

````bash
# view logs
journalctl -u servicename

# follow logs
journalctl -u servicename -f

# filter by time
journalctl --since "2023-10-01" --until "2023-10-02"
````

### Best Practies

* Limit Service Permissions: Use `User` and `Group` directives in service files

  ````ini
  [Service]  
  User=nobody  
  Group=nogroup
  ````

* Sandbox Services: Use `ProtectSystem` and `ProtectHome`

  ````ini
  [Service]  
  ProtectSystem=full  
  ProtectHome=true  
  ````

* Disable Unused services: `sudo systemctl disable servicename`

* Automate Service Restarts: Use `Restart=always` in service files

  ````ini
  [Service]  
  Restart=always  
  ````

* Identify rogue services during boottime: `systemd-analyze blame`

### Example Service to Send Pushover Notification on Server Reboot

Edit : `/etc/systemd/system/multi-user.target.wants/reboot_ntf.service`

````ini
[Unit]
Description=ntf reboot script
After=network-online.target
Wants=network-online.target
[Service]
ExecStart=/bin/bash -c 'sleep 2 && /usr/local/bin/ntf send -t REBOOT minetest.in just rebooted! > /var/log/reboot_ntf.log 2>&1'
Type=oneshot
RemainAfterExit=true
Environment=HOME=/root/
[Install]
WantedBy=multi-user.target
````

