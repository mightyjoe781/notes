## Backup of VPS using rclone

Cheap VPS Offers often do not include backups, so user are at their devices to take backups. A best solution for users which have cheap vps with no backup facilities is to buy cloud storage and create their own backup script that sends the backups to that vendor.

So your cloud drive becomes like a take anywhere stick, where you keep regular backups of your VPS.

### Backup Script with pcloud

#### Installing Dependencies

````bash
# pre-requisites
sudo apt-get install pv rclone
````

#### Assuming rclone is setup with a remote

Below scripts assumes that remote `smk` has already been setup then ends up creating a folder with `vps_bkp/bkp_ddmm` on the cloud provider you have.

````bash
REMOTE_NAME="smk:vps_bkp"
RCLONE_BIN=/home/smk/bin/go/bin/rclone

WHOAMI=`whoami`
if [ "@$WHOAMI" \!= "@root"    ]; then
    echo Error: Must be run as root
    exit 1
fi

cd /

# backup_dirs=("etc" "home" "root" "var" "usr/local/bin" "usr/local/sbin" "srv" "opt")
backup_dirs=("etc" "home" "root" "var" "srv" "opt")
bkp_dir="bkp_`date +"%m%d"`"
mkdir -p /tmp/${bkp_dir}

for i in ${!backup_dirs[@]}; do
    echo "Starting tar of /${backup_dirs[$i]} ..."
    # tar -cz -f /tmp/${bkp_dir}/${backup_dirs[$i]}.tgz -C ${backup_dirs[$i]} .
    tar cf - /${backup_dirs[$i]} -P | pv -s $(du -sb /${backup_dirs[$i]} | awk '{print $1}') | gzip > /tmp/${bkp_dir}/${backup_dirs[$i]}.tgz
    echo "Done tar of /${backup_dirs[$i]}"
done

echo "Created backups at : /tmp/${bkp_dir}"
echo "----------------BKP------------------"
du -sh /tmp/${bkp_dir}/* | sort -h

echo "--------------- RCLONE ---------------"
${RCLONE_BIN} copy /tmp/${bkp_dir} ${REMOTE_NAME}/${bkp_dir} -P -v


echo "--------------- Cleanup --------------"
rm -rf /tmp/${bkp_dir}
````

#### Further Steps

- You could run this script montly using `crond` or a `systemd` scripts as suited backup frequency.