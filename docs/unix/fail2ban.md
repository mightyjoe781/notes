# fail2ban

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

### Installation

````bash
sudo apt update
sudo apt install fail2ban
````

````bash
# check fail2ban service
systemctl status fail2ban.service
````

### Setup

* Create a local configuration : `jail.local`

````bash
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
````

* Edit Configuration file `/etc/fail2ban/jail.local`

````ini
[DEFAULT]  
ignoreip = 127.0.0.1/8 192.168.1.0/24  
bantime = 600  
findtime = 600  
maxretry = 3 
````

* Enable Jails

````ini
[sshd]  
enabled = true  
````

````bash
systemctl enable fail2ban
````

### Commands

* Check Status

  ````bash
  fail2ban-client status
  ````

* Unban an IP

  ````bash
  fail2ban-client set sshd unbanip 192.168.1.100
  ````

* Ban an IP Manually

  ````bash
  fail2ban-client set sshd banip 192.168.1.100  
  ````

* Reload Configuration

  ````bash
  fail2ban-client reload
  ````

### Advanced Use-Cases

* Create a custom filter in `/etc/fail2ban/filter.d/`

  ````ini
  [custom-filter]  
  enabled = true  
  filter = custom-filter  
  action = iptables[name=Custom, port=http, protocol=tcp]  
  logpath = /var/log/custom.log  
  maxretry = 3  
  bantime = 600
  ````

* Email Notifications: Configure mail alerts in `jail.local`

  ````ini
  [DEFAULT]  
  destemail = admin@example.com  
  sender = fail2ban@example.com  
  action = %(action_mwl)s 
  ````

### Example Configurations

#### Securing MailCow Mailserver

Create a new filter : ` /etc/fail2ban/filter.d/mailcow.conf`

````ini
[Definition] 
failregex = LOGIN authenticator failed for .+ \[<HOST>\]:.* 
            NOQUEUE: reject: RCPT from \[<HOST>\].* Auth failure: 535 

````

Add `[mailcow]` jail in `/etc/fail2ban/jail.conf`

````ini
[mailcow] 
enabled = true 
port = smtp, submission, imap, imaps, pop3, pop3s 
filter = mailcow 
logpath = /opt/mailcow-dockerized/mailcow.conf 
maxretry = 3 
bantime = 3600
````

#### Securing Nextcloud with Fail2Ban

Create a new filter : ` /etc/fail2ban/filter.d/nextcloud.conf`

````ini
[Definition] 
failregex = Login failed.*REMOTE_ADDR=<HOST>
````

Add `[nextcloud]` jail in `/etc/fail2ban/jail.conf`

````ini
[nextcloud] 
enabled = true 
port = http, https 
filter = nextcloud 
logpath = /path/to/nextcloud.log 
maxretry = 3 
bantime = 3600
````

#### 