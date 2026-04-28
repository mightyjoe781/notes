# UFW (Uncomplicated Firewall)

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Frontend for iptables. Simpler syntax for managing common firewall rules on Linux.

!!! warning
    Always allow your SSH port before enabling UFW or you will lock yourself out.

### Installation

```bash
sudo apt install ufw
sudo systemctl enable ufw
```

### Initial Setup

```bash
# 1. Allow necessary ports first
sudo ufw allow 22/tcp                # SSH (change if using non-default port)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 2. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw default deny routed        # drop forwarded packets

# 3. Review and enable
sudo ufw show added
sudo ufw --force enable
sudo ufw status verbose
```

### Allow and Deny Rules

```bash
# By port/protocol
sudo ufw allow 8080/tcp
sudo ufw deny 8080/tcp

# By service name (from /etc/services)
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# By application profile
sudo ufw allow 'Nginx Full'          # HTTP + HTTPS
sudo ufw app list                    # show available profiles

# From specific IP or range
sudo ufw allow from 192.168.1.100
sudo ufw allow from 192.168.1.0/24 to any port 5432
sudo ufw deny from 10.0.0.5

# On specific interface
sudo ufw allow in on eth0 to any port 80

# Rate limiting (brute-force protection)
sudo ufw limit 22/tcp
```

### Managing Rules

```bash
sudo ufw status numbered             # list rules with numbers
sudo ufw delete 3                    # delete rule by number
sudo ufw delete allow 80/tcp         # delete by specification
sudo ufw insert 1 allow from 203.0.113.0/24  # insert at position 1

sudo ufw disable
sudo ufw enable
sudo ufw reload
sudo ufw reset                       # clear all rules (use with caution)
```

### Status and Reporting

```bash
sudo ufw status                      # enabled/disabled + active rules
sudo ufw status verbose              # includes default policies
sudo ufw status numbered
sudo ufw show listening              # listening ports and their rules
sudo ufw show added                  # pending rules not yet active
sudo ufw show raw                    # underlying iptables rules
```

### Logging

```bash
sudo ufw logging on                  # enable logging
sudo ufw logging medium              # low, medium, high, full
sudo tail -f /var/log/ufw.log
```

### Common Setups

#### Web server

```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw default deny incoming
sudo ufw --force enable
```

#### Database server (allow only app server)

```bash
sudo ufw allow from 10.0.1.50 to any port 5432 proto tcp  # PostgreSQL
sudo ufw allow from 10.0.1.50 to any port 6379 proto tcp  # Redis
sudo ufw default deny incoming
sudo ufw --force enable
```

### Tips

- Use `ufw limit 22/tcp` to auto-block IPs with too many failed SSH attempts
- Check `/etc/ufw/applications.d/` to see or add custom app profiles
- `ufw allow in on lo` ensures loopback traffic is allowed if needed
- `ufw show listening` helps identify services that need rules

### See Also

- [Fail2ban](fail2ban.md) for rate-limiting and ban-on-failure
- [SSH](ssh.md) for hardening SSH access
- Also: iptables (underlying tool), nftables (modern replacement for iptables), firewalld
