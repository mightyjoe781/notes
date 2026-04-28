# Fail2ban

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Scans log files for failed login attempts and bans offending IPs using iptables/nftables. Commonly used to protect SSH.

### Installation

```bash
sudo apt install fail2ban
sudo systemctl enable --now fail2ban
```

### Configuration

Never edit `jail.conf` directly - it gets overwritten on upgrades. Use `jail.local`:

```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Key settings in `[DEFAULT]`:

```ini
[DEFAULT]
ignoreip = 127.0.0.1/8 192.168.1.0/24   # never ban these IPs
bantime  = 1h                             # how long to ban (use -1 for permanent)
findtime = 10m                            # window for counting failures
maxretry = 5                              # failures before ban
banaction = ufw                           # use ufw instead of iptables directly
```

Enable SSH jail:

```ini
[sshd]
enabled  = true
port     = 2222          # match your SSH port
maxretry = 3
bantime  = 24h
```

```bash
sudo systemctl restart fail2ban
```

### Commands

```bash
# Status
sudo fail2ban-client status              # list active jails
sudo fail2ban-client status sshd        # jail details (banned IPs, stats)

# Ban / Unban
sudo fail2ban-client set sshd banip 203.0.113.5
sudo fail2ban-client set sshd unbanip 203.0.113.5

# Reload config
sudo fail2ban-client reload

# Test a filter against a log file
sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
```

### Custom Jail (Nginx)

```ini
# /etc/fail2ban/jail.local

[nginx-http-auth]
enabled  = true
port     = http,https
filter   = nginx-http-auth
logpath  = /var/log/nginx/error.log
maxretry = 5

[nginx-limit-req]
enabled  = true
port     = http,https
filter   = nginx-limit-req
logpath  = /var/log/nginx/error.log
maxretry = 10
```

### Custom Filter

```ini
# /etc/fail2ban/filter.d/myapp.conf
[Definition]
failregex = ^<HOST> .* "POST /login" 401
ignoreregex =
```

```ini
# /etc/fail2ban/jail.local
[myapp]
enabled  = true
port     = http,https
filter   = myapp
logpath  = /var/log/myapp/access.log
maxretry = 10
bantime  = 1h
```

### Tips

- Check `sudo fail2ban-regex` to verify your filter works before enabling
- Use `bantime = -1` for permanent bans on known malicious IPs
- Combine with `ufw`: set `banaction = ufw` in `[DEFAULT]`
- Set `ignoreip` to include your own IP to avoid locking yourself out
- View banned IPs: `sudo iptables -L f2b-sshd -n`

### See Also

- [UFW](ufw.md) for general firewall rules
- [SSH](ssh.md) for hardening SSH config
