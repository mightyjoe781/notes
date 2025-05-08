## Backup VPS using rclone

Cheap VPS offers often do not include backups, so users must take backups on their devices. The best solution for users with cheap VPS plans lacking backup facilities is to purchase cloud storage and create a backup script that sends backups to the cloud vendor.

This approach makes the cloud drive function like a portable storage device, where regular VPS backups are stored.

### Sync Script with pcloud

* This setup uses `rclone` configured to use `pcloud` remote.

#### Create a filter for backup

````txt
# === System configuration files ===
+ /etc/**
- /etc/mtab
- /etc/resolv.conf
- /etc/hostname
- /etc/hosts
- /etc/adjtime

# === SSH keys and user data ===
- /root/.cache/**
- /home/*/.cache/**
- .npm/**
- .cargo/**/target/**
- .vscode-server/**
- node_modules/**
- target/**
- tmp/**
+ /root/**
+ /home/**

# === Web servers and web apps ===
+ /var/www/**
+ /etc/nginx/**
+ /etc/letse/**

# === Databases and important services ===
# + /var/lib/mysql/**
# + /var/lib/postgresql/**
# + /var/lib/redis/**

# === Mail systems ===
+ /var/mail/**
# + /var/spool/mail/**
# + /etc/postfix/**
# + /etc/dovecot/**

# === Special services ===
+ /opt/smkbin/**

# === Logs (optional) ===
# + /var/log/**

# === SSH and Sudo ===
+ /etc/ssh/**
+ /etc/sudoers.d/**
+ /etc/sudoers

# === Default deny everything else ===
- *
````

#### Installing Dependencies

````bash
# pre-requisites
sudo apt-get install rclone
````

#### Assuming rclone is setup with a remote

* Below script assumes you a remote named `pcloud` 

````bash
#!/bin/bash
# /*
# * --------------------------------------------------------------------
# * @file    pcloud_sync
# * @brief   A simple sync util for pcloud
# * @author  smk (smk@freebsd.org)
# * @version 20221129
# * @license BSD3
# * @bugs    No known bugs
# * --------------------------------------------------------------------
# */

set -e
set -o pipefail

SERVER=$(hostname -s)
REMOTE="pcloud:vps_bkp/${SERVER}"
RCLONE_BIN=/opt/smkbin/rclone

MYDIR="/"
FILTER="/root/.dotfiles/conf/filter.txt"
VERBOSE=""	# Add verbose -v as needed
LOG="/tmp/rclone_log.txt"

WHOAMI=`whoami`
if [ "@$WHOAMI" \!= "@root"    ]; then
    echo Error: Must be run as root
    exit 1
fi

pushd ${MYDIR}

echo "Performing Sync to ${REMOTE}"
# Borg Handles Archiving VPS State, so just sync latest dir state
nice ${RCLONE_BIN} sync / ${REMOTE}/latest --filter-from ${FILTER} ${VERBOSE} --skip-links --update --use-server-modtime &>> ${LOG}
echo "Done"

popd
````

#### Further Steps

- Run this script monthly using crond or a systemd script according to the required backup frequency.
- An example cron job I use sends mobile notifications directly using `ntf`.

````bash
0 2 * * 6 /usr/local/bin/ntf -t WEEKLY_PCLOUD_SYNC done /root/bin/pcloud_sync.sh
````

* [https://github.com/wolfv6/rclone_jobber/tree/master](https://github.com/wolfv6/rclone_jobber/tree/master) : `rclone_jobber` is a script for backup.

### Borg - Snapshots

* WIP