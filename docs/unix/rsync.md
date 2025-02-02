# rsync

 [:octicons-arrow-left-24:{ .icon } Back](index.md) 

### Installation

````bash
apt update
apt install rsync

# verify
rsync --version
````

### Basic Usage

#### Copy Files

````bash
rsync -av /src/ /dst/
# -a : archive mode
# -v : verbose
````

#### Dry Run

````bash
rsync -av --dry-run /source/ /destination/ 
````

#### Delete Extraneous Files

````bash
rsync -av --delete /source/ /destination/
````

#### Copy to Remote Server

````bash
rsync -av /source/ user@remote:/destination/
````

#### Copy from Remote Server

````bash
rsync -av user@remote:/source/ /destination/
````

#### Use SSH

````bash
rsync -av -e ssh /source/ user@remote:/destination/
````

### Exclude Files

````bash
rsync -av --exclude='*.log' /source/ /destination/
rsync -av --exclude={'*.log','*.tmp'} /source/ /destination/

# using exclude files
echo '*.log' > exclude.txt  
echo '*.tmp' >> exclude.txt  
rsync -av --exclude-from='exclude.txt' /source/ /destination/ 
````

### Tips

#### Automate Backups

````bash
# cron to schedule regular backups
0 2 * * * rsync -av /source/ /backup/ 
````

#### Use `--backup` for Versioning

````bash
# keep copies of overwritten files
rsync -av --backup --backup-dir=backup-$(date +%F) /source/ /destination/ 
````

#### Combine with Tar

````bash
# compress files before syncing
tar czf - /source/ | rsync -av -e ssh - user@remote:/destination/backup.tar.gz
````

### Example

#### rsync using ssh remote

````bash
#!/bin/sh
mkdocs build && rsync -avz --delete site/ smkroot:/var/www/notes/
exit 0
````

