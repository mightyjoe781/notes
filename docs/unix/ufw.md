# ufw

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

NOTE: Do not copy paste these commands except you understand each of them.

### Installation

````bash
apt -y install ufw
systemctl enable ufw
````

### Setup

````bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22195
ufw allow from <EDGE_NODE_IP> to any port 8000	# connect edge agents to portainer

ufw default reject incoming
ufw default allow outgoing
ufw default deny routed

ufw show added
ufw show listening
````

After reviewed. Activate your firewall

````bash
ufw --force enable
ufw status verbose
````

### Chain Default Action

````bash
ufw [--dry-run] default allow|deny|reject [incoming|outgoing|routed]
````

#### Safe Mode (Allow all chain)

````bash
ufw default allow incoming
ufw default allow outgoing
ufw default allow routed
````

#### Recommended

````bash
ufw default reject incoming
ufw default allow outgoing
ufw default deny routed	# drop forward chain
````

### Firewall Rules

#### Rule Syntax

````bash
ufw [rule]
  [delete] [insert NUM] [prepend]
  allow|deny|reject|limit
  [in|out [on INTERFACE]]
  [log|log-all]
  [proto PROTOCOL]
  [from ADDRESS [port PORT | app APPNAME ]]
  [to ADDRESS [port PORT | app APPNAME ]]
  [comment COMMENT]
````

#### Abbreviated allow syntax using Port/Protocol

````bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
````

#### Abbreviated allow syntax using Service Name

````bash
ufw allow ssh
ufw allow http
ufw allow https
````

Check service name from `/etc/services` and replace port/protocol with it.

````bash
cat /etc/services | head -35 | tail -10
````

#### Abbreviated allow syntax using UFW Application Profile

````bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
````

````bash
# check available app profiels
ufw app list

# app profile info
ufw app info <appname>

# app profiles directory : /etc/ufw/applications.d/
````

#### Full allow incoming connection syntax

````bash
## using port/protocol
ufw allow in proto tcp to any port 22## using service name
ufw allow in to any port ssh## using application profile
ufw allow in to any app OpenSSH
````

#### Allow incoming connection from specific source

- **Network Interface**: add `in on <interface>` after `ufw`
- **Source IP/CIDR**: add `from <IP/CIDR>` after `ufw allow`

````bash
## specific incoming interface
ufw allow in on eth0 proto tcp to any port 22
ufw allow in on eth0 to any port ssh## specific source ip
ufw allow from 192.168.1.0/24 proto tcp to any port 22
ufw allow from 172.16.1.10 proto tcp to any port 80
ufw allow from 172.16.1.10 proto tcp to any port 443## or both
ufw allow in on eth0 from 192.168.1.0/24 to any port 22
````

### Show Report

#### Report Syntax

````bash
ufw show raw
ufw show builtins|before-rules|user-rules|after-rules|logging-rules
ufw show listening
ufw show added
````

#### Show listening ports along with firewall rules

````bash
ufw show listening
````

NOTE: if some service doesn’t have any rules then default chain action is executed.

#### Show added rules

````bash
ufw show added
````

### Control your Firewall

- `ufw enable` — Activate ufw by adding all ufw iptables rules
- `ufw disable` — Remove all ufw iptables rules
- `ufw reload` — Reload config (e.g. `/etc/default/ufw` `/etc/ufw/*` )

### Status — Check UFW Status

Syntax: `ufw status [verbose|numbered]`