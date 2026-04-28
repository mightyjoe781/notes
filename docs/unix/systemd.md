# systemd

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Init system and service manager for Linux. Manages services, timers, mounts, and more.

### Service Management

```bash
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx          # reload config without full restart

sudo systemctl enable nginx          # start on boot
sudo systemctl disable nginx
sudo systemctl is-enabled nginx

sudo systemctl status nginx          # detailed status with recent log lines
systemctl list-units --type=service  # list all loaded services
systemctl list-units --failed        # list failed units
```

### System Control

```bash
sudo systemctl reboot
sudo systemctl poweroff
sudo systemctl suspend
systemctl status                     # overall system status
systemd-analyze blame                # boot time per service (slow startup debug)
systemd-analyze critical-chain       # critical path to reach default.target
```

### Creating a Custom Service

Create `/etc/systemd/system/myapp.service`:

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/server
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal

# Security hardening
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now myapp   # enable and start immediately
```

### Service Type Reference

| Type | Use case |
|---|---|
| `simple` | process stays in foreground (default) |
| `forking` | process forks and parent exits (traditional daemons) |
| `oneshot` | runs once and exits (like a cron job) |
| `notify` | process signals readiness via sd_notify |
| `idle` | like simple but waits until other jobs finish |

### journalctl - Log Viewing

```bash
journalctl -u nginx                  # logs for specific service
journalctl -u nginx -f               # follow (tail -f equivalent)
journalctl -u nginx -n 50            # last 50 lines
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx --since "2024-01-01" --until "2024-01-02"
journalctl -p err                    # filter by priority: emerg,alert,crit,err,warning,notice,info,debug
journalctl --disk-usage              # how much disk journals use
journalctl --vacuum-size=500M        # reduce journal to 500M
journalctl -b                        # logs since last boot
journalctl -b -1                     # logs from previous boot
journalctl -k                        # kernel messages only
```

### Timers (Cron Alternative)

Create `/etc/systemd/system/backup.timer`:

```ini
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Create `/etc/systemd/system/backup.service`:

```ini
[Unit]
Description=Run Daily Backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

```bash
sudo systemctl enable --now backup.timer
systemctl list-timers                # list all active timers
```

OnCalendar examples:

```
daily           # 00:00:00 every day
hourly          # every hour
weekly          # Monday 00:00:00
Mon 09:00       # every Monday at 9am
*-*-* 02:30:00  # every day at 2:30am
```

### Tips

- `systemctl cat nginx` shows the active unit file
- `systemctl edit nginx` creates an override without modifying the original
- `journalctl -f -u app1 -u app2` tails multiple services simultaneously
- Use `Restart=always` with `RestartSec=5s` for auto-recovering services
- `systemd-run --on-calendar="..." /path/to/script` runs a one-off timer without creating a unit file

### See Also

- [Cron](cron.md) for traditional scheduling
- Also: `ps`, `top`, `htop` for process monitoring; `ss` for socket inspection
