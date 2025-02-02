# tar/gzip/zstd

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

## tar (tape archive)

used to bundle files into a single archive

### Basic Usage

#### 1. Create and Archive

````bash
tar -cvf archive.tar file1 file2
````

* `-c`: create archive
* `-v`: verbose output
* `-f`: specify archive filename

#### 2. Extract an Archive

````bash
tar -xvf archive.tar
````

* `-x`: Extract files
* files are extracted into current directory by default

#### 3. List Archive Contents

````bash
tar -tvf archive.tar
````

### Common Scenarios

1. Extract to a Specific Directory

   ````bash
   tar -xvf archive.tar -C /path/to/dir
   ````

2. Create and archive from a Directory

   ````bash
   tar -cvf archive.tar /path/to/dir
   ````

3. Exclude file

   ````bash
   tar -cvf archive.tar --exclude="*.log" /path/to/dir
   ````

4. Extracting only `txt` files

   ````bash
   tar -xvf archive.tar --wildcards "*.txt"
   ````

5. Combine with `find` archive specific files

   ````bash
   find . -name "*.txt" | tar -cvf archive.tar -T -
   ````

## gzip

Compress files using `.gz` format

### Basic Usage

#### 1. Compress a file

````bash
gzip file.txt
````

#### 2. Decompress a file

````bash
gzip -d file.txt.gz
````

#### 3. Compress and Archive

````bash
tar -czvf archive.tar.gz file1 file2
````

#### 4. Extract `.tar.gz`

````bash
tar -xzvf archive.tar.gz
````

#### 5. View Compressed files without extraction

````bash
zcat file.txt.gz
````

* Use `gunzip` as an alias for `gzip -d`

## Zstd (Z Standard)

A modern compression tool with better speed and ratios

### Basic Usage

#### 1. Compress a File

````bash
zstd file.txt
````

#### 2. Decompress a File

````bash
zstd -d file.txt.zst
````

#### 3. Compress and Archive

````bash
tar -cvf archive.tar.zst --zstd file1 file2
````

#### 4. Extract `.tar.zst`

````bash
tar -xvf archive.tar.zst --zstd
````

You can adjust compression level : `zstd -19 file.txt`

Use `unzstd` as alias for `zstd -d`

### Comparison between gzip and zstd

| Tool   | Speed  | Compression Ratio | Common Use Cases           |
| ------ | ------ | ----------------- | -------------------------- |
| `gzip` | Medium | Good              | General-purpose            |
| `zstd` | Fast   | Excellent         | Modern systems, large data |

#### Notes

* take a look at `pigz` (parallel implementation of gzip)