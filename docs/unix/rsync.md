# rsync

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Fast incremental file transfer. Only copies changed parts of files; works locally and over SSH.

### Installation

```bash
sudo apt install rsync
```

### Basic Usage

```bash
# Local copy (trailing slash on source = copy contents, not the directory itself)
rsync -av src/ dst/                  # copy contents of src into dst
rsync -av src  dst/                  # copy src directory into dst/src

# Dry run - preview what would change
rsync -avn src/ dst/

# Delete files in dst that no longer exist in src
rsync -av --delete src/ dst/

# Remote: push to server
rsync -av src/ user@server:/dst/

# Remote: pull from server
rsync -av user@server:/src/ dst/

# Use specific SSH port
rsync -av -e "ssh -p 2222" src/ user@server:/dst/
```

### Common Flags

| Flag | Description |
|---|---|
| `-a` | archive mode: `-rlptgoD` (recursive, preserve links/perms/times/owner/group) |
| `-v` | verbose |
| `-z` | compress during transfer |
| `-n` | dry run |
| `-P` | show progress + resume partial transfers (`--partial --progress`) |
| `--delete` | remove destination files not in source |
| `--exclude PATTERN` | skip matching files |
| `--exclude-from FILE` | read exclusions from file |
| `--checksum` | compare by checksum instead of size+time |
| `--bwlimit=KBPS` | limit bandwidth |
| `--backup` | keep copies of overwritten files |
| `--backup-dir DIR` | directory for backup copies |
| `--link-dest DIR` | hard-link unchanged files from DIR (for incremental backups) |

### Exclude Patterns

```bash
rsync -av --exclude='*.log' src/ dst/
rsync -av --exclude={'*.log','*.tmp','node_modules/'} src/ dst/

# Exclude file
echo '*.log' > .rsyncignore
echo 'node_modules/' >> .rsyncignore
rsync -av --exclude-from='.rsyncignore' src/ dst/
```

### Incremental Backups with --link-dest

```bash
# First backup
rsync -av --link-dest=/backups/latest src/ /backups/$(date +%F)/

# Update "latest" symlink
ln -sfn /backups/$(date +%F) /backups/latest
```

Each daily backup uses hard links for unchanged files, so it takes nearly no extra space but appears as a full copy.

### Common Examples

```bash
# Sync a website
rsync -avz --delete ./site/ user@server:/var/www/html/

# Backup home directory (exclude cache)
rsync -av --exclude='.cache/' ~ /mnt/backup/

# Mirror with progress
rsync -avzP src/ user@server:/dst/

# Cron backup job
0 2 * * * rsync -az --delete /data/ /backup/data/ >> /var/log/rsync.log 2>&1
```

### Tips

- Always do a dry run first with `-n` before using `--delete`
- The trailing slash on source matters: `src/` copies contents, `src` copies the directory
- Use `-z` on slow connections, omit it on fast LAN/local transfers (CPU overhead not worth it)
- Combine with `ssh-agent` for passwordless remote syncing in cron

### See Also

- [Compression](compression.md) for archiving before transfer
- Also: rclone (like rsync for cloud storage: S3, GCS, Dropbox), borgbackup (dedup + encryption), restic
