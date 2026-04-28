# Cron

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Schedule recurring commands. The `crond` daemon checks every minute and runs matching jobs.

### Cron Syntax

```
*    *    *    *    *   /path/to/command
|    |    |    |    |
|    |    |    |    +-- Day of week (0-7, Sun=0 or 7, or Mon-Sun)
|    |    |    +------- Month (1-12)
|    |    +------------ Day of month (1-31)
|    +----------------- Hour (0-23)
+---------------------- Minute (0-59)
```

Operators:

| Operator | Meaning | Example |
|---|---|---|
| `*` | every | `* * * * *` - every minute |
| `,` | list | `0 8,12,18 * * *` - at 8am, 12pm, 6pm |
| `-` | range | `0 9-17 * * *` - every hour 9am-5pm |
| `/` | step | `*/15 * * * *` - every 15 minutes |

### Managing Crontabs

```bash
crontab -e                           # edit current user's crontab
crontab -l                           # list current user's crontab
crontab -r                           # remove current user's crontab
sudo crontab -u alice -e             # edit another user's crontab

# System crontabs (include username field)
/etc/crontab
/etc/cron.d/                         # drop-in files
/etc/cron.hourly/ /etc/cron.daily/ /etc/cron.weekly/ /etc/cron.monthly/
```

### Special Strings

```bash
@reboot     /path/to/script.sh       # run once at startup
@hourly     /path/to/script.sh       # equivalent to 0 * * * *
@daily      /path/to/script.sh       # equivalent to 0 0 * * *
@weekly     /path/to/script.sh       # equivalent to 0 0 * * 0
@monthly    /path/to/script.sh       # equivalent to 0 0 1 * *
```

### Common Examples

```bash
# Every 5 minutes
*/5 * * * * /usr/local/bin/check.sh

# Every day at 2:30am
30 2 * * * /usr/local/bin/backup.sh

# Every Monday at 9am
0 9 * * 1 /usr/local/bin/report.sh

# Every weekday (Mon-Fri) at 8am
0 8 * * 1-5 /usr/local/bin/sync.sh

# First day of every month at midnight
0 0 1 * * /usr/local/bin/monthly.sh

# Every 6 hours
0 */6 * * * /usr/local/bin/fetch.sh

# Capture output to log
0 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

### Environment Gotchas

Cron runs with a minimal environment - `$PATH` is short and `~/.bashrc` is not sourced.

```bash
# Set PATH at the top of crontab
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Or use full paths in scripts
0 2 * * * /usr/bin/python3 /home/alice/scripts/backup.py

# Or source environment in a wrapper
0 2 * * * bash -l -c '/path/to/script.sh'
```

### Viewing Logs

```bash
grep CRON /var/log/syslog            # Debian/Ubuntu
journalctl -u cron                   # systemd systems
tail -f /var/log/cron                # RHEL/CentOS
```

### Tips

- Use [crontab.guru](https://crontab.guru) to validate expressions
- Make scripts executable: `chmod +x /path/to/script.sh`
- Always redirect output: `cmd >> /var/log/cmd.log 2>&1` or jobs silently fail
- Consider `systemd timers` for better logging and dependency control
- Use `flock` to prevent overlapping runs: `0 * * * * flock -n /tmp/job.lock job.sh`

### See Also

- [Systemd Timers](systemd.md) for more powerful scheduling with logging
