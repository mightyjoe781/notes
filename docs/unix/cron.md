# cron

allows users to schedule the execution.

### Installation

````bash
sudo apt update && sudo apt install cron
sudo systemctl enable cron
````

Cron is mostly installed in all the systems and consists of two things

* `cron` or `crond` : daemon
* `crontab` : command interface for interacting with daemon

### Cron Syntax

````bash
*    *    *    *    *   /home/user/bin/somecommand.sh
|    |    |    |    |            |
|    |    |    |    |    Command or Script to execute
|    |    |    |    |
|    |    |    | Day of week(0-6 | Sun-Sat)
|    |    |    |
|    |    |  Month(1-12)
|    |    |
|    |  Day of Month(1-31)
|    |
|   Hour(0-23)
|
Min(0-59)
````

`*`: matches all values, so above script runs every minute

### Usage

* add crontab entry

````bash
crontab -e
````

NOTE: crontab entries do not source `~/.bashrc` so always use full script path and environment variable. Either hardcode or source in the executing script

NOTE: Make sure your script is executible

* cron logs

  ````bash
  tail -f /var/log/cron
  ````

  

### Example crons entries

* Use https://crontab.guru to validate your cron

If you want to run four times a day between Monday and Friday, you can use the *step operator* ( **/** ) and the *range operator* ( **-** ).

````bash
0 */6 * * Mon-Fri /home/user/somejob.sh
````

#### **Run Every Hour at Minute 15**

```
15 * * * * /path/to/script.sh 
```

#### **Run Every Day at 2 AM**

````bash
0 2 * * * /path/to/script.sh
````

#### **Run Every Sunday at 3 PM**

````bash
0 15 * * 0 /path/to/script.sh
````

#### **Run Every Month on the 1st at 4 AM**

````bash
0 4 1 * * /path/to/script.sh
````

### Advanced Features

#### Environment Variable

````bash
SHELL=/bin/bash  
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
* * * * * /path/to/script.sh
* * * * * /path/to/script.sh >> /var/log/script.log 2>&1
````

#### Special Strings

Use predefined schedules:

- `@reboot`: Run at startup.
- `@daily`: Run once a day.
- `@weekly`: Run once a week.
- `@monthly`: Run once a month.
- `@yearly`: Run once a year.

````bash
@daily /path/to/script.sh
````

### Pro Tips

**Use `cron.d` for System Jobs**: Place system-wide cron jobs in `/etc/cron.d/`