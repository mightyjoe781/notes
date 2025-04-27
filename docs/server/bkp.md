## Backup VPS using rclone

Cheap VPS Offers often do not include backups, so user are at their devices to take backups. A best solution for users which have cheap vps with no backup facilities is to buy cloud storage and create their own backup script that sends the backups to that vendor.

So your cloud drive becomes like a take anywhere stick, where you keep regular backups of your VPS.

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

- You could run this script montly using `crond` or a `systemd` scripts as suited backup frequency.
- Example cron I use, which use `ntf` to send mobile notification directly.

````bash
0 2 * * 6 /usr/local/bin/ntf -t WEEKLY_PCLOUD_SYNC done /root/bin/pcloud_sync.sh
````

* [https://github.com/wolfv6/rclone_jobber/tree/master](https://github.com/wolfv6/rclone_jobber/tree/master) : `rclone_jobber` is a scripts for backup

### Borg - Snapshots

* WIP