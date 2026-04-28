# SSH

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Secure Shell. Encrypted remote login, file transfer, and port forwarding.

!!! warning
    Always test SSH config changes from a second terminal before closing your current session.

### Key-Based Authentication

```bash
# Generate ED25519 key (preferred)
ssh-keygen -t ed25519 -C "comment" -f ~/.ssh/my_key

# Copy public key to server
ssh-copy-id -i ~/.ssh/my_key.pub user@server
# or manually:
# cat ~/.ssh/my_key.pub >> ~/.ssh/authorized_keys   (on server)

# Connect
ssh -i ~/.ssh/my_key user@server
```

### ~/.ssh/config

Define aliases and per-host settings:

```
Host myserver
    HostName 203.0.113.10
    User deploy
    Port 2222
    IdentityFile ~/.ssh/my_key
    IdentitiesOnly yes

Host github
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

Host *
    Protocol 2
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Then just `ssh myserver` instead of the full command.

### Server Hardening

Edit `/etc/ssh/sshd_config`:

```
Port 2222                            # change default port
PermitRootLogin no
PasswordAuthentication no            # keys only
PubkeyAuthentication yes
AllowUsers deploy alice
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
```

```bash
sudo sshd -t                         # test config syntax
sudo systemctl reload ssh
```

### Port Forwarding / Tunnels

```bash
# Local forward: access remote service locally
# Visit localhost:8080 to reach server:80
ssh -L 8080:localhost:80 myserver

# Local forward to a different host
ssh -L 5432:db.internal:5432 jumphost

# Remote forward: expose local port on remote server
ssh -R 9000:localhost:3000 myserver

# Dynamic SOCKS proxy
ssh -D 1080 myserver
# then configure browser to use SOCKS5 proxy at localhost:1080

# Keep tunnel open (no shell)
ssh -fNT -L 8080:localhost:80 myserver
```

### Jump Hosts (ProxyJump)

```bash
# Connect to internal server through a bastion
ssh -J bastion user@internal.host

# In ~/.ssh/config
Host internal
    HostName 10.0.0.5
    User app
    ProxyJump bastion

Host bastion
    HostName bastion.example.com
    User jump
    IdentityFile ~/.ssh/bastion_key
```

### File Transfer

```bash
# SCP (simple, single files or directories)
scp file.txt myserver:/tmp/
scp -P 2222 file.txt user@host:/path/
scp -r ./dir myserver:/backup/

# SFTP (interactive)
sftp myserver
# then: ls, get file, put file, cd, lcd, quit
```

### Useful Commands

```bash
# Check active SSH sessions
ss -tnp | grep ssh
who

# SSH agent (avoid typing passphrase repeatedly)
eval $(ssh-agent)
ssh-add ~/.ssh/my_key
ssh-add -l                           # list loaded keys
```

### Troubleshooting

```bash
ssh -vvv myserver                    # verbose debug output
sudo sshd -t                         # validate config
sudo systemctl status ssh
sudo journalctl -u ssh -f
```

| Issue | Likely cause |
|---|---|
| `Permission denied (publickey)` | wrong key, wrong user, `authorized_keys` permissions |
| Connection refused | SSH not running, wrong port, firewall |
| Timeout | firewall blocking, server unreachable |
| `WARNING: REMOTE HOST IDENTIFICATION` | server key changed, update `~/.ssh/known_hosts` |

### Tips

- `ssh -o StrictHostKeyChecking=no` disables host key check (use only in automation/trusted environments)
- Add `ForwardAgent yes` to pass your local keys to the remote host for onward SSH
- Use `~.` to force-disconnect a hung SSH session
- `LocalForward` in `~/.ssh/config` persists tunnels without extra flags

### See Also

- [UFW](ufw.md) for firewall rules
- [Fail2ban](fail2ban.md) for blocking brute-force attempts
- Also: mosh (mobile shell, UDP-based, handles roaming), autossh (auto-reconnecting SSH tunnel)
