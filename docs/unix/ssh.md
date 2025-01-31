# SSH

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

Secure Shell (SSH) configuration for remote access and security.

***Warning:*** Always test SSH changes in a **second terminal** before disconnecting!

## Basic Configuration

Edit `/etc/ssh/sshd_config`

````bash
# Change default port
Port 23415
# Disable root login
PermitRootLogin no
# Allow specific users
AllowUsers smk deploy
# Key authentication only
PasswordAuthentication no
````

````bash
# Reload SSH
sudo systemctl reload ssh
````

## Key-Based Authentication

````bash
# Generate ED25519 key (client)
ssh-keygen -t ed25519 -C "smk@vps" -f ~/.ssh/vps_key

# Copy public key to server
ssh-copy-id -i ~/.ssh/vps_key.pub smk@your-server -p 23415

# SSH config shortcut (~/.ssh/config)
Host vps
  HostName your-server.com
  User smk
  Port 23415
  IdentityFile ~/.ssh/vps_key
  IdentitiesOnly yes
````

## Security Hardening

````bash
# Edit /etc/ssh/sshd_config
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 3
LoginGraceTime 1m
````

## Fail2Ban Setup

````bash
sudo apt install fail2ban
sudo cp /etc/fail2ban/jail.{conf,local}
````

Edit `/etc/fail2ban/jail.local`:

````bash
[sshd]
enabled = true
port = 23415
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 1h
ignoreip = 127.0.0.1/8
````

````bash
sudo systemctl restart fail2ban
````

## Useful Commands

````bash
# SSH tunnel
ssh -L 8080:localhost:80 vps

# SCP file transfer
scp -P 23415 file.txt vps:/path/

# Check active sessions
ss -tnp | grep 'ssh'
````

## Troubleshooting

````bash
# Check SSH status
sudo systemctl status ssh

# Test config syntax
sshd -t

# Verbose connection test
ssh -vvv vps

````



#### Reference: Full `~/.ssh/config` Setup

````yaml
Host *
Protocol 2
Compression no
StrictHostKeyChecking no
#-------- GIT COMMITS ----------
Host github gh github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

#-------- Proxy Example ---------
# Host smk.minetest.ca 1.1.1.1
    ProxyCommand ssh -xaqW%h:22195 minetest.in

# -------- Proxy SSH Example --------
Host bsdimp.com 1.1.1.1
    User smk
    HostName bsdimp.com
    Port 8798
    IdentityFile ~/.ssh/id_ed25519
    ProxyCommand ssh -xaqW%h:8792 minetest.in

# -------- remote ssh config --------
Host code
    HostName 1.1.1.1
    Port 22199
    User code
    IdentityFile ~/.ssh/smk.prvkey
    # useful for keeping vscode connected
    ServerAliveInterval 60
    ServerAliveCountMax 20
    # localhost forwarding settings
    ForwardAgent yes
    ExitOnForwardFailure no
    LogLevel QUIET
    LocalForward 3000 localhost:3000
    LocalForward 3001 localhost:3001
    LocalForward 4321 localhost:4321
    LocalForward 5000 localhost:5000
    LocalForward 8000 localhost:8000
    LocalForward 8385 localhost:8384

# ------------ Example SSH for FreeBSD ------
Host freebsd-vm
    HostName 192.168.69.3
    Port 22
    User smk
    IdentityFile /Users/smk/.ssh/id_ed25519
    RemoteCommand /compat/debian/bin/bash
    RequestTTY force
    SetEnv BASH_ENV=".bash_debian"

````

