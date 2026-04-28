# tar / gzip / zstd

[:octicons-arrow-left-24:{ .icon } Back](index.md)

`tar` bundles files into archives. Compression (`gzip`, `bzip2`, `zstd`, `xz`) reduces size.

### Quick Reference

| Task | Command |
|---|---|
| Create `.tar.gz` | `tar -czf archive.tar.gz dir/` |
| Extract `.tar.gz` | `tar -xzf archive.tar.gz` |
| Create `.tar.zst` | `tar -cf archive.tar.zst --zstd dir/` |
| Extract `.tar.zst` | `tar -xf archive.tar.zst --zstd` |
| List contents | `tar -tf archive.tar.gz` |
| Extract to dir | `tar -xzf archive.tar.gz -C /path/` |

### tar

```bash
# Common flags
# -c  create
# -x  extract
# -t  list contents
# -f  specify filename (always last before filename)
# -v  verbose
# -z  gzip compression
# -j  bzip2 compression
# -J  xz compression
# --zstd  zstd compression

# Create archive
tar -cf archive.tar file1 file2 dir/
tar -czf archive.tar.gz dir/         # with gzip
tar -cjf archive.tar.bz2 dir/        # with bzip2
tar -cf archive.tar.zst --zstd dir/  # with zstd

# Extract
tar -xf archive.tar
tar -xzf archive.tar.gz
tar -xf archive.tar.gz -C /tmp/      # extract to specific directory

# List contents without extracting
tar -tf archive.tar.gz

# Exclude patterns
tar -czf archive.tar.gz dir/ --exclude='*.log' --exclude='node_modules'

# Extract specific files
tar -xzf archive.tar.gz dir/file.txt
tar -xzf archive.tar.gz --wildcards '*.txt'

# Append to existing archive
tar -rf archive.tar newfile.txt

# Combine with find
find . -name "*.py" | tar -czf python_files.tar.gz -T -
```

### gzip

```bash
gzip file.txt                        # compress (replaces original)
gzip -k file.txt                     # compress, keep original
gzip -d file.txt.gz                  # decompress
gunzip file.txt.gz                   # same as gzip -d

gzip -9 file.txt                     # maximum compression
gzip -1 file.txt                     # fastest compression

zcat file.txt.gz                     # view without decompressing
zcat file.txt.gz | grep "error"

# Compress multiple files
gzip *.log

# Check integrity
gzip -t archive.tar.gz
```

### zstd (Zstandard)

Faster than gzip with better compression. Good for large files and real-time use.

```bash
zstd file.txt                        # compress (creates file.txt.zst)
zstd -k file.txt                     # keep original
zstd -d file.txt.zst                 # decompress
unzstd file.txt.zst                  # same as zstd -d

zstd -19 file.txt                    # maximum compression (slow)
zstd -1 file.txt                     # fastest
zstd -T0 file.txt                    # multi-threaded (use all cores)

# Stream compress / decompress
cat large.log | zstd > large.log.zst
zstdcat large.log.zst | grep "error"
```

### Comparison

| Tool | Speed | Ratio | Best for |
|---|---|---|---|
| `gzip` | medium | good | universal compatibility |
| `bzip2` | slow | better | small files, text |
| `xz` | very slow | best | distribution packages |
| `zstd` | very fast | excellent | large files, real-time |
| `lz4` | fastest | low | streaming, speed-critical |

### Tips

- Use `.tar.gz` for cross-platform compatibility (universally supported)
- Use `zstd` for local backups and fast transfers on modern systems
- `pigz` is a parallel gzip drop-in: `tar -cf - dir/ | pigz -p 4 > archive.tar.gz`
- Use `tar -P` to preserve absolute paths (use carefully - can overwrite system files on extract)

### See Also

- [rsync](rsync.md) for incremental file sync/backup
- Also: zip/unzip (Windows-compatible), 7z (high compression), zlib (library)
