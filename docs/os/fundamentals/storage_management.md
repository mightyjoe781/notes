# Storage Management

## Persistent Storage

### Persistence

- RAM is fast but **volatile** - if power is lost, its contents are gone
- Many use cases need data to survive a reboot or power loss, so the OS also manages **persistent** storage devices
- Common technologies: magnetic tape, HDD (magnetic disk), SSD (flash), and newer persistent-memory devices

### HDD

![226](assets/Pasted%20image%2020260612183521.png)

A hard disk drive stores data on spinning magnetic **platters**, read/written by a **head** that moves across **tracks**. The diagram above labels the key geometric concepts:

- **(A) Track** - one of the concentric rings on the platter
- **(B) Geometrical sector** - a pie-slice wedge cutting across all tracks
- **(C) Disk sector** - the intersection of a track and a geometrical sector; this is the actual unit the disk reads/writes
- **(D) Cluster** - a group of sectors treated as a unit (more on this in the File Systems section below)

Traditionally, the OS addressed disks using the **CHS** (Cylinder/Head/Sector) scheme - it had to know the physical geometry of the drive (how many cylinders, heads, and sectors per track) to compute where a given piece of data lived.

![Disk Sector|466](https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/images/Chapter10/10_01_DiskMechanism.jpg)

### LBA

![](assets/Pasted%20image%2020260612184133.png)

CHS addressing tightly coupled software to a drive's exact physical layout, which made it hard for manufacturers to change that layout without breaking compatibility. **Logical Block Addressing (LBA)** solves this:

- The entire disk is presented to the OS as one flat array of numbered blocks (LBAs `1..N` in the diagram)
- The OS just asks for "LBA 3" - it has no idea (and doesn't need to know) which physical cylinder, head, and sector that corresponds to
- The **disk controller** does the translation from LBA to the real physical location (e.g. "LBA 3 -> Cylinder *yellow*, Head 2, Sector C" in the diagram)
- This adds a small translation overhead, but lets the manufacturer change the physical layout (or even the storage technology entirely, as with SSDs below) without the OS or applications needing to change

### SSD

- SSDs store data using **NAND flash** technology, organized into:
    - **Physical pages** - the smallest unit that can be *read or written* (commonly 4 KiB or 16 KiB)
    - **Physical blocks** - a collection of pages, and the smallest unit that can be *erased*
- The SSD controller maintains the **Flash Translation Layer (FTL)**, which maps each logical block address (LBA) the OS uses to a physical page on the flash chip

![](assets/Pasted%20image%2020260612184538.png)

In the diagram, LBAs `1`-`8` are mapped through the FTL to physical pages spread across two physical blocks (`A`-`D` and `E`-`H`) - e.g. LBA 1 maps to page A, LBA 7 maps to page G, and so on. Note that this mapping doesn't need to be sequential or contiguous - the FTL is free to place any LBA on any physical page.

#### SSD Write

![](assets/Pasted%20image%2020260612185206.png)

Say we want to write to LBA 1 for the first time:

- The FTL finds a free physical page - here, page A - and writes the 4 KiB of data for LBA 1 into it
- The FTL records the mapping `LBA 1 -> page A`

Now suppose we want to *update* LBA 1 with new content. Flash doesn't support in-place updates - a page can't simply be overwritten with new data. Instead, the FTL does a "remove and add":

#### SSD Write - Update

![](assets/Pasted%20image%2020260612185226.png)

- The FTL writes the new data for LBA 1 into a *different*, free page - here, page B
- The mapping is updated: `LBA 1 -> page B`
- The old page A is marked **invalid** - it still physically holds the old data, but nothing points to it anymore, and it can't be reused until it's erased. Crucially, a single page can't be erased on its own - only an entire *block* can be erased

#### SSD Write - More Update

![](assets/Pasted%20image%2020260612185427.png)

As writes continue, this pattern repeats: LBA 1 gets remapped again, this time to page D, leaving A and B (and now C) invalid within their block. Meanwhile pages E-H in the second block are being used to store LBAs 6, 7, and 8.

#### SSD Write - More Updates

![483](assets/Pasted%20image%2020260612185719.png)

One more update to LBA 1 remaps it to a page in the *second* block (here, page E). At this point, the first block (A-D) has every one of its pages marked invalid - none of them are referenced by any LBA anymore. The whole block is now eligible to be **erased and reused**, since erase operates on whole blocks.

#### SSD Write Garbage Collection

![446](assets/Pasted%20image%2020260612185828.png)

This reclaiming process is **garbage collection (GC)**:

- The controller picks a block that's entirely (or mostly) invalid
- It erases that block, making all of its pages free again
- Only *then* can a new write (e.g. another update to LBA 1) be placed into one of those freshly-erased pages

#### SSD Write Amplification

![](assets/Pasted%20image%2020260612185854.png)

If a block being garbage-collected still has a *few* valid pages on it (pages still referenced by some LBA), the controller has to first copy those valid pages elsewhere before it can erase the block. This means a single logical write from the OS can trigger the controller to internally read, copy, and erase far more data than the original write - this is **write amplification**. It's a key reason SSD performance and lifespan depend heavily on how full the drive is and how the FTL's GC is tuned.

### Wear Leveling

- Each NAND cell can only be erased/programmed a limited number of times before it wears out (its **write endurance**)
- Not all data is updated equally often:
    - **Cold pages** - written once and rarely or never touched again (e.g. installed program files)
    - **Hot pages** - rewritten constantly (e.g. filesystem metadata, database WAL)
- Without intervention, the physical cells backing hot pages would wear out and fail long before the cells backing cold pages

![](assets/Pasted%20image%2020260612190212.png)

The diagram illustrates the underlying problem: if the "hot" portion of the drive is small relative to its total capacity, that small portion absorbs a disproportionate share of all writes/erases (the "used" region), while the rest sits comparatively idle ("waste" from a wear perspective) - the hot cells wear out first and that part of the SSD becomes unusable well before the drive's nominal capacity is exhausted.

#### Over Engineering

![](assets/Pasted%20image%2020260612191710.png)

SSDs address this with **wear leveling**, backed by an **over-provisioned (OP)** area - extra physical capacity that isn't exposed as user-addressable LBAs:

- The controller periodically identifies cold pages and moves them into the over-provisioned area
- It then erases the block that held those cold pages
- That freshly-erased block can now absorb hot writes, spreading wear more evenly across *all* the physical cells rather than concentrating it on a few

### Defragmentation

Traditional defragmentation - rearranging file data so it's physically contiguous - helps HDDs, because it reduces how far the head has to seek between reads. It does **not** help SSDs: there's no seek penalty to save, and the extra reads/writes/erases caused by defragmentation just consume write endurance and accelerate wear, for no real benefit.

### Mismatch block to page size

![616](assets/Pasted%20image%2020260612191826.png)

The LBA size the OS uses doesn't have to match the SSD's physical page size - e.g. LBAs might be 4 KiB while a physical page is 8 KiB. When that happens, a single physical page ends up holding parts of *multiple* LBAs at different byte offsets within it (in the diagram, LBA 1 sits at the start of page A while LBA 2 sits partway through it, at roughly the 50% offset). This complicates the FTL's bookkeeping and can mean that updating one LBA forces the controller to read, modify, and rewrite a page that also holds unrelated data from a neighboring LBA - another source of write amplification.

## File Systems

- A **file system** is an abstraction layered on top of raw block storage
- Users and applications think in terms of files and directories, not raw LBAs - the file system translates between the two
- Reading or writing a file ultimately translates into reading/writing one or more blocks
- This translation also enables **caching**: once a block is read, it can be kept in memory and reused (see OS Page Cache below)
- To store any data, a file must be allocated at least one block (which itself maps to one or more LBAs)

**Examples of File Systems**

- FAT (FAT16, FAT32)
- NTFS
- APFS
- EXT4
- XFS
- btrfs

**Some Terminology**

![364](assets/Pasted%20image%2020260612215019.png)

The diagram shows how three different "block" concepts can relate to each other - here, one 2048-byte filesystem block spans two 1024-byte LBAs, and four such LBAs together span one 4096-byte PBA:

- **PBA (Physical Block Address)** - internal to the drive; also called the physical sector size
- **LBA (Logical Block Address)** - exposed to the OS; also called the logical sector size
- **File system block size** - the minimum unit the *file system* reads/writes in
- In general: 1 PBA maps to one or more LBAs, and 1 file system block maps to one or more LBAs

You can inspect a device's logical and physical sector sizes with:

```bash
lsblk -o NAME,PHY-SEC,LOG-SEC
```

### FAT32

**FAT (File Allocation Table)** is one of the simplest file system designs:

- The FAT is, at its core, an array of integers
- The *index* into the array is an LBA (traditionally called a logical sector)
- The *value* stored at that index is the **next** LBA in the file's chain - or a special marker for "end of chain"

![](assets/Pasted%20image%2020260612215917.png)

In the diagram, the file `test.txt` starts at LBA 6. To read the whole file:

1. Go to LBA 6 - the FAT entry there says the next LBA is `2`
2. Go to LBA 2 - the FAT entry there says the next LBA is `3`
3. Go to LBA 3 - the FAT entry there is `E` (end of chain) - there's no more data

So reading `test.txt` means reading LBAs 6, 2, and 3, in that order - even though they aren't contiguous on disk.

Although FAT32 entries are 32 bits wide, only **28 bits** are actually usable for addressing:

- The remaining bits are reserved for flags - end-of-chain markers, "dirty"/free indicators, and other bookkeeping
- With the historical LBA size of 512 bytes, 28 bits of addressing gives $2^{28} \times 512 \text{ bytes} \approx 128 \text{ GiB}$ of addressable space
- That's far too small for modern drives, so FAT32 uses a trick to address more space without widening the table entries: **clustering**

#### Clustering

A **cluster** is a fixed-size logical grouping of consecutive LBAs (blocks), and the FAT table operates on *clusters* rather than individual LBAs:

- E.g. with 512-byte LBAs, 8 LBAs grouped together make a 4 KiB cluster
- Cluster 0 covers LBAs 0-7, cluster 1 covers LBAs 8-15, and in general cluster `C` covers LBAs `C*8` through `C*8+7`
- Since each FAT entry now refers to a whole cluster instead of a single LBA, the same 28-bit address space covers a much larger disk - on the order of 1 TB instead of ~128 GB

![](assets/Pasted%20image%2020260612220439.png)

The diagram mirrors the earlier FAT example, but at the cluster level: `test.txt` starts at cluster 6, whose entry points to cluster 3, whose entry is `E` (end of chain). To actually read the file, the file system converts those cluster numbers back to LBA ranges - cluster 6 is LBAs 48-55, and cluster 3 is LBAs 24-31 (using `cluster * 8` from the example above).

### Cluster Size Tradeoffs

![](assets/Pasted%20image%2020260612220938.png)

Cluster size is a tradeoff:

- **Larger clusters** let the same number of FAT entries address more total disk space
- But every file's size gets rounded up to a whole number of clusters - if a file only uses part of its last cluster, the rest is wasted. This is **internal fragmentation**, illustrated in the diagram as the "used" portion of a cluster versus the "waste" left over, space that can't be used by any other file

### Blocks Everywhere

![](assets/Pasted%20image%2020260612221129.png)

When you format a file system, you choose a file system block size - which must be a multiple of (and typically no smaller than) the underlying LBA size, commonly 1024, 2048, or 4096 bytes. The diagram shows three different ratios between file system block size, LBA size, and PBA size:

- **4096 -> 512 -> 512** - one 4096-byte FS block maps cleanly to 8 LBAs, and each LBA maps 1:1 to a PBA. Everything lines up
- **4096 -> 1024 -> 2048** - one FS block maps to 4 LBAs of 1024 bytes, but each *physical* sector (PBA) is 2048 bytes, so each PBA actually backs 2 LBAs
- **4096 -> 1024 -> 4096** - one FS block again maps to 4 LBAs of 1024 bytes, but here a single 4096-byte PBA backs *all 4* of those LBAs at once

The second and third cases are where a **torn write** (aka torn page) becomes possible: if the OS only writes one of the LBAs that share a PBA, and power is lost before the underlying physical sector write completes, the drive can end up with a sector containing a mix of old and new data spanning multiple logical blocks.

### OS Page Cache

- Blocks read from disk are cached in memory by the OS - this is the **page cache**
- Each cached block number is mapped to a virtual memory page; in many setups, one file system block corresponds to one (or fits within one) VM page
- **Reads** check the page cache first; only on a miss does the OS go to disk - and the result is then stored in the cache for next time
- **Writes** go to the page cache first; the OS writes the dirty page back to disk later (or immediately, if asked to)

**OS Page Cache (Cached Read)**

![](assets/Pasted%20image%2020260612221753.png)

The user wants to read block 3. The OS checks the page cache, finds block 3 already cached (a **hit**), and copies its contents directly to the user's buffer - no disk access needed.

**OS Page Cache (Cache Miss)**

![](assets/Pasted%20image%2020260612221836.png)

The user wants to read block 7. The OS checks the page cache and finds it's *not* there (a **miss**). It translates block 7 to its underlying LBAs (here, LBAs 56-63), reads them from disk, populates the page cache with the result, and then returns the data to the user.

**OS Page Cache (Write)**

![](assets/Pasted%20image%2020260612221938.png)

The user writes to block 7. The OS writes the new data into the page cache (marking that page **dirty**/buffered) and returns immediately - the write to disk happens later, when the OS flushes dirty pages, or whenever `fsync()` is explicitly called.

This buffering is exactly why databases call `fsync()` so aggressively: a write being "done" from the application's point of view (it returned successfully) doesn't mean it's actually durable yet - it may still only exist in the page cache, with no guarantee it survives a crash until `fsync()` forces it out to disk.

A famous real-world example of `fsync()` cost: in 2008, Firefox 3 was found to call `fsync()` (via SQLite, for its history/bookmarks database) on every page load. On Linux's ext3 in `data=ordered` mode, `fsync()` on one file flushes *all* dirty data for that entire file system - so a user copying a large file in the background could cause Firefox to visibly freeze for tens of seconds on an unrelated `fsync()` call. See [Mike Shaver's "fsyncers and curveballs"](http://shaver.off.net/diary/2008/05/25/fsyncers-and-curveballs/) and the [LWN writeup](https://lwn.net/Articles/283745/).

A more recent example of *noticing* unexpected overhead in this neighborhood: the [2024 XZ Utils backdoor (CVE-2024-3094)](https://en.wikipedia.org/wiki/XZ_Utils_backdoor) was discovered by PostgreSQL developer Andres Freund after he noticed SSH logins were using more CPU than expected and were about 500ms slower than normal - a small, measurable anomaly that led him to trace a supply-chain attack hidden inside `liblzma`. The lesson in both cases is the same: small, "shouldn't matter" latency anomalies are sometimes hiding something significant underneath.

### Page cache woes

- **Benefit**: faster reads, and multiple processes reading the same file share one cached copy (e.g. two applications reading the same shared library only need it cached once)
- **Risk**: because writes land in the page cache first, a crash between "write accepted" and "write flushed to disk" can corrupt application-level structures that span multiple blocks - e.g. a database page that's only partially written to disk (a torn page, as mentioned above)

### File Modes

A file must be **opened** before it can be used, and the mode it's opened with affects how the page cache is involved. Some examples:

- `O_APPEND` - all writes go to the end of the file
- `O_DIRECT` - bypasses the page cache entirely; reads/writes go straight to/from the device
- `O_SYNC` - every write is flushed to durable storage before returning (safe, but slow)

Many databases expose a tunable (e.g. Postgres's `wal_sync_method`) that controls exactly which of these mechanisms is used for flushing the write-ahead log, trading durability guarantees against throughput.

### Partitions

![330](assets/Pasted%20image%2020260612223053.png)

- A disk is exposed as one big array of LBAs (logical sectors)
- A **partition** is a contiguous range of that array - it starts at one LBA and ends at another, providing logical segmentation of the disk
- In the diagram, an SSD's LBA space is divided into partitions P1, P2, and P3, each spanning its own range of LBAs
- Each partition can hold its own file system, and each file system can use its own block size (cluster size)

### Partition Alignment

![](assets/Pasted%20image%2020260612223306.png)

This diagram (from the classic ["Aligning filesystems to an SSD's erase block size"](https://azrael.digipen.edu/~mmead/www/Courses/CS180/linux-on-4kb-sector-disks.pdf) discussion of 4 KiB-sector "Advanced Format" disks) shows why partition *starting offset* matters:

- **Proper alignment** (top) - a 4 KiB data structure (e.g. a file system block) lines up exactly with a single physical sector
- **Improper alignment** (bottom) - the same 4 KiB structure straddles two physical sectors

If a partition starts at a misaligned LBA, every file system block built on top of it can end up straddling two physical sectors this way. A single logical write then requires the drive to read-modify-write *two* physical sectors instead of one - extra work on every write, for the lifetime of that partition.

### Moving File Systems

![](assets/Pasted%20image%2020260612223427.png)

File system choice has a measurable effect on tail latency, not just throughput. Allegro's engineering team found that their Kafka brokers on **ext4** had p999 produce-latency spikes up to several seconds, largely caused by ext4's journal commit behavior interacting with metadata updates under load. After migrating their Kafka brokers to **XFS**, they measured an 82% reduction in producer latency outliers above their SLO. See [Allegro's "Unlocking Kafka's Potential: Tackling Tail Latency with eBPF"](https://blog.allegro.tech/2024/03/kafka-performance-analysis.html).

## What really happens in a file IO?

### POSIX

POSIX (Portable Operating System Interface) is a set of standardized APIs designed to ensure compatibility between different Unix-like operating systems, including Linux. It defines:

- System calls and library functions for tasks like file management, process control, and I/O
- Shell command behavior and scripting standards
- Interface consistency, enabling applications to be portable across compliant systems

In Linux, POSIX compliance ensures that programs written against these interfaces run reliably across different Unix-like environments.

```c
// POSIX API examples
#include <unistd.h>

ssize_t read(int fd, void buf[.count], size_t count);
ssize_t write(int fd, const void buf[.count], size_t count);

int fsync(int fd);
int fdatasync(int fd);
```

**Read Example**

Consider reading an entire file, `test.dat`, which is 5000 bytes, on a system where:

- Logical sector size = 4096 bytes, physical sector size = 4096 bytes
- Page size = 4096 bytes
- File system block size = 4096 bytes (so 1 file system block = 1 LBA/sector)

5000 bytes therefore spans **two** file system blocks: one full 4096-byte block, plus a second block holding the remaining 904 bytes.

**Read File Blocks**

![](assets/Pasted%20image%2020260613000806.png)

1. The application issues a `read()` on the file
2. The OS reads the file's metadata (its block-allocation chain, e.g. a FAT-style chain as described above) and follows it from the start to find which blocks make up the file - in the diagram, `test.dat` starts at block 6, whose entry points forward, ending the chain at block 3. So the file's data lives in blocks 6 and 3 (these still need to be translated to LBAs)

**Check the page cache**

- The OS checks its page cache for blocks 6 and 3
- Suppose block 3 is already cached, but block 6 is not
- For the cached block, the OS can serve the data immediately; for the uncached block, it has to go to the disk controller

**Read from disk controller**

- The OS sends a read command for block 6's underlying LBA(s) to the disk controller
- Since 1 block = 1 LBA here, this is simply "read LBA 6, length 1"
- The disk controller translates that LBA to its physical block address (PBA) and returns the data
- The OS stores the result in the page cache

**Return to user**

- The OS now has both blocks' data: a full 4096 bytes from block 6, and the cached 904 bytes from block 3
- Since the user only asked for 5000 bytes total, the OS copies exactly that much from its buffers into the user's buffer and returns success

This walkthrough shows just how many layers sit between a single `read()` call and the actual bytes coming off a disk: translating the POSIX call to file system blocks, translating those blocks to LBAs, checking (and populating) the page cache, and only then - if necessary - going all the way down to the disk controller and the physical media.

## Resources

- [Operating Systems: Three Easy Pieces - Persistence chapters](https://pages.cs.wisc.edu/~remzi/OSTEP/) - free textbook covering disks, SSDs, RAID, file systems, and crash consistency
- ["Coding for SSDs" series (Codecapsule)](https://codecapsule.com/2014/02/12/coding-for-ssds-part-1-introduction-and-table-of-contents/) - a deep, approachable series on SSD internals: pages, blocks, the FTL, garbage collection, wear leveling, and write amplification
- [Mike Shaver - "fsyncers and curveballs"](http://shaver.off.net/diary/2008/05/25/fsyncers-and-curveballs/) and the [LWN writeup](https://lwn.net/Articles/283745/) - the Firefox 3 / ext3 `fsync()` story referenced above
- [Theodore Ts'o - "Don't fear the fsync!"](https://thunk.org/tytso/blog/2009/03/15/dont-fear-the-fsync/) - a clear explanation of what `fsync()` actually guarantees and why it matters for durability
- [XZ Utils backdoor (CVE-2024-3094) - Wikipedia](https://en.wikipedia.org/wiki/XZ_Utils_backdoor) - the supply-chain attack discovered via an unexplained SSH latency increase
- [Allegro Tech - "Unlocking Kafka's Potential: Tackling Tail Latency with eBPF"](https://blog.allegro.tech/2024/03/kafka-performance-analysis.html) - the ext4 -> XFS migration referenced above
- [Aligning filesystems to an SSD's erase block size](https://azrael.digipen.edu/~mmead/www/Courses/CS180/linux-on-4kb-sector-disks.pdf) - the partition/sector alignment discussion referenced above
- [memory.md](memory.md) - for how virtual memory pages, the MMU, and page tables relate to the OS page cache discussed here
