---
title: Memory
description: How RAM works - DRAM internals, reading and writing memory, virtual memory (paging, page tables, shared memory, swapping), and DMA.
tags:
  - concept
---

# Memory

- RAM is the OS's "scratch pad" - we don't ultimately care about *what* is sitting in it (it's volatile, gone on power loss), but it's fast, so we trade durability for speed and rely on disk for anything that needs to survive

## Anatomy of Memory

### Memory

- Stores data while it's in use
- **Volatile** - loses its contents when power is lost
    - RAM - Random Access Memory
- **Non-volatile** - retains contents without power
    - ROM - Read Only Memory

**Static RAM**

- SRAM
- Complex and expensive, but fast
    - 1 bit -> 1 flip-flop -> ~6 transistors
- A flip-flop holds its state as long as power is supplied (no refresh needed)
- Used in CPU caches (L1/L2/L3), and some SSD controllers
- Access time is constant/fast - no extra steps needed to read a bit

**Dynamic RAM**

- DRAM
- Abundant and cheap, but slower
    - 1 bit -> 1 capacitor + 1 transistor
- A capacitor stores a bit as a charge, but that charge leaks over time
- Needs to be **refreshed** periodically (the charge re-written) or the data is lost
- Reading is also slow because **reading a DRAM cell is destructive** - sensing the charge drains the capacitor, so the value has to be sensed, then immediately written back (recharged) before the next access

**Asynchronous DRAM**

![](assets/Pasted%20image%2020260610173513.png)

- The CPU and RAM run on independent clocks, so they're not synchronized with each other
- The CPU issues a read and then has to *wait* for RAM to respond, without knowing exactly which RAM clock cycle the response will land on
- This causes wasted clock cycles on both sides while waiting for the other to catch up, plus extra cycles lost to refresh - making async DRAM relatively slow

**Synchronous DRAM**

![](assets/Pasted%20image%2020260610173708.png)

- SDRAM
- The RAM's clock is synchronized with the CPU's (memory bus) clock
- Both sides know exactly when data will be ready, so there's no guessing/waiting - no wasted cycles

**Double Data Rate**

![](assets/Pasted%20image%2020260610173823.png)

- DDR SDRAM
- A clock signal has a rising edge ("up-tick") and falling edge ("down-tick") per cycle
- Regular SDRAM transfers data once per cycle (on one edge); DDR transfers data on *both* edges
- Result: two transfers per clock cycle, doubling effective bandwidth without raising the clock frequency

**DDR4 SDRAM**

![](assets/Pasted%20image%2020260610173939.png)

- The **prefetch buffer** size determines how many bits are transferred per pin for a single memory access
- DDR4 has 64 data pins, with an 8-bit prefetch buffer per pin
- 64 pins x 8 bits = 64 bytes transferred per access - this is called a **burst**
- This lines up nicely with the CPU's cache line size (commonly 64 bytes), which is the minimum amount of data the CPU typically wants to fetch at once

**DDR5 SDRAM**

![](assets/Pasted%20image%2020260610174347.png)

- Splits the module into two independent **channels** of 32 pins each, which can be accessed in parallel for two different addresses
- Each channel has a 16-bit prefetch buffer per pin
- Per channel: 32 pins x 16 bits = 64 bytes - so each channel still delivers a 64-byte burst, but two channels can now serve two requests concurrently

### DRAM Internals

A 64-bit physical memory address is decoded into several components that together identify exactly which physical storage cell(s) to access - this decoded form is the **DRAM address**:

- **DIMM** - which physical memory module
- **Bank** - an independent array within the DIMM; different banks can be operated on somewhat independently
- **Row** - a row of cells within a bank
- **Column** - a specific cell (or group of cells) within a row
- **Cell** - the actual capacitor storing 1 bit

**Opening a row**

![](assets/Pasted%20image%2020260610175046.png)

- A bank contains many rows (e.g. ~32K)
- A row contains many columns (e.g. ~1024)
- Each column maps to one or more cells (e.g. 16 or 32 bits wide)
- Before any column in a row can be read or written, that **row must be "opened"** - its contents are sensed and loaded into a row of **sense amplifiers** shared by the bank. This acts as a row-sized cache/buffer.
- A bank can only have **one row open at a time**
- If the next access is to a different row in the same bank, the currently open row must first be **closed** - its (possibly modified) contents are written back from the sense amplifiers to the row, *then* the new row is opened. This close-then-open cycle is slow.
- Writes also go to the sense amplifiers first, and are flushed back to the row when it's closed
- Because of this, having **many banks** helps - different banks can have different rows open simultaneously, so accesses that hit different banks don't pay the close/open penalty

## Reading and Writing from and to Memory

### Read

![](assets/Pasted%20image%2020260610180603.png)

- The CPU wants to execute the instruction at address `640` (the value currently in the program counter, `pc`), so it asks RAM for the contents at that address
- RAM doesn't return just the 4 (or however many) bytes for that one instruction - because of the burst behavior covered above, it returns the full **64-byte burst** containing that address
- Those 64 bytes get loaded into the CPU's caches (L1/L2/L3), so the *next* several instructions (and any nearby data) are likely already in cache when needed
- This round trip - RAM to CPU cache - takes roughly **50-100ns**

### Write

![](assets/Pasted%20image%2020260610181112.png)

- To write `22` into `*ptr` (address `1024`), the CPU sends a write request: address `1024`, value `22`, size 4 bytes
- The CPU can't directly "set" a capacitor's charge from across the bus - the memory controller drives the write, and includes error-checking (e.g. ECC on supporting hardware) to detect/correct bit errors introduced by the imperfect, leaky nature of DRAM cells
- Note in the diagram: the stack frames (`main`, `malloc`) are at high addresses and grow down, while the heap allocation (`*ptr`) is at a low address and grows up - matching the "stack grows down, heap grows up" layout from the [process notes](process.md)

### NOTE about alignment

![](assets/Pasted%20image%2020260610181215.png)

- Most CPUs read/write memory most efficiently when a value's address is a multiple of its size - this is **alignment**. E.g. a 4-byte `int` should sit at an address divisible by 4, an 8-byte `double` at an address divisible by 8
- The compiler enforces this by inserting **padding** bytes between struct fields so each field starts at a properly aligned offset
- **Field order matters**: in the first `struct Foo` (`char`, `double`, `short`, `int`), the `double` needs 8-byte alignment, so 7 padding bytes are inserted after the `char`. More padding follows after `short`. Total size: 24 bytes.
- Simply reordering the fields from largest to smallest (`char`, `short`, `int`, `double` in the second example) lets the compiler pack them with far less padding - in this layout, only 1 byte of padding is needed (after `char`), shrinking the struct considerably
- This is the same idea referenced in the [process notes](process.md) about reordering struct fields for cache-line efficiency: less padding means more useful data per cache line

## Virtual Memory

### Limitations of Physical Memory

Working with raw physical memory directly creates several problems:

- **Fragmentation** - free memory ends up scattered in unusable chunks
- **Shared Memory** - no easy way for multiple processes to safely share the same memory
- **Isolation** - nothing stops one process from reading/writing another's memory
- **Large Programs** - a program larger than physical memory has nowhere to "overflow" to

**Fragmentation**

![400](assets/Pasted%20image%2020260610183031.png)

- Memory is handed out to processes in blocks
- Over time, as processes start and stop and request different-sized blocks, free memory becomes fragmented - there may be enough *total* free memory, but not in one contiguous piece
- Two flavors: **external** and **internal** fragmentation

**External Fragmentation**

![357](assets/Pasted%20image%2020260610183157.png)

- Free memory exists, but in small non-contiguous gaps between allocated blocks
- A new request that needs one large contiguous block (the purple process) can fail even though the *sum* of free space would be enough
- Common with **variable-sized** allocation schemes, e.g. segmentation

**Internal Fragmentation**

![335](assets/Pasted%20image%2020260610183224.png)

- Memory is handed out in **fixed-size blocks** - if a process only needs part of a block, the rest is wasted
- That wasted space is *inside* an allocated block, so the OS has no way to give it to another process, even though it's unused
- The bigger the fixed block size, the more is wasted on average per allocation

### Virtual Memory and Fragmentation

![](assets/Pasted%20image%2020260610221757.png)

- The fix: use small, fixed-size blocks called **pages** (commonly 4KB) - small enough to keep internal fragmentation low, fixed-size so there's no external fragmentation in the traditional sense
- Each process gets its own **virtual address space**, divided into virtual pages
- Each virtual page is mapped to some physical page frame in RAM - the physical frames backing a process don't need to be contiguous at all, since the mapping handles the indirection
- This mapping is stored per-process in a **page table**
- It's a many-to-one relationship in the sense that physical memory (one shared resource) is divided up and mapped from many different processes' virtual address spaces

**Page Tables**

![](assets/Pasted%20image%2020260610222204.png)

- Every memory access from a process now needs an extra **translation** step: virtual address -> physical address
- The page table holds this virtual-page -> physical-frame mapping
- Each process has its own page table, so the same virtual address in two different processes can (and usually does) map to different physical memory
- The page table itself lives in memory; the CPU keeps a pointer to the *current* process's page table in a register called the **PTBR** (Page Table Base Register), and swaps it on every context switch
- In practice, page tables store compact **page numbers** rather than full addresses (since pages are fixed-size and aligned, only the page number needs to be looked up - the offset within the page stays the same)

**Shared Memory**

![304](assets/Pasted%20image%2020260610222334.png)

- Without virtual memory, sharing is hard: if you spin up 5 processes running the same program, you'd naively need 5 separate copies of that program's code in physical memory - mostly duplicate data
- This wastes RAM proportional to the number of running instances

**Shared Memory and Virtual Memory**

![](assets/Pasted%20image%2020260610222656.png)

- With virtual memory, the code only needs to exist **once** in physical memory
- Each process's virtual pages for that code (e.g. `A.P2` and `B.P1` in the diagram) are mapped to the *same* physical frame
- Each process still believes it has its own private copy - it has no visibility into the fact that the underlying physical memory is shared

**Shared Libraries**

- This is exactly how shared libraries work in practice
- Most processes link against common libraries (e.g. `libc`)
- The OS loads each library's code into physical memory once, and maps it into the virtual address space of every process that uses it
- You can see a process's actual mappings via `/proc/[pid]/maps` on Linux

**Use Cases for Shared Memory**

- Multi-process / multi-threaded applications sharing data
- Database shared buffer pools (e.g. Postgres's shared buffers, accessible by all backend processes)
- Reverse proxies / web servers (e.g. nginx worker processes sharing config/cache)
- `fork()` - a child process initially shares all of the parent's pages
- **Copy-on-Write (CoW)** - after a `fork()`, parent and child share the same physical pages (marked read-only); only when one of them *writes* to a page does the kernel copy that page so each gets its own version. This makes `fork()` cheap even for processes with large memory footprints.

> Redis persistence is a good real-world use of this: when Redis needs to write a snapshot (RDB) or rewrite its append-only file, it `fork()`s a child process. Thanks to CoW, that fork is nearly instant and doesn't duplicate the dataset in memory - the child just reads the (unchanging, from its point of view) shared pages and writes them to disk, while the parent keeps serving writes to its own copies of any pages that get modified in the meantime.

**Isolation**

- Without virtual memory, a process's pointers/addresses *are* physical addresses - nothing stops a process from constructing an address that points into another process's (or the kernel's) memory
- Virtual memory fixes this: each process gets its own full virtual address space, almost all of which is unmapped
- A process simply has **no way to express** a physical address directly - every address it uses is virtual, and only valid if its page table happens to map it to something

**Isolation with Virtual Memory**

- Process A's virtual address `1000` and Process B's virtual address `1000` are translated independently via their own page tables, and typically point to *completely different* physical addresses
- One process cannot read or corrupt another's memory by guessing addresses, because there's no shared addressing scheme to exploit

**Swapping**

![](assets/Pasted%20image%2020260610223833.png)

- Physical memory (RAM) is limited - if too many processes are running, their combined working sets might not fit
- Because every process already goes through the virtual-to-physical translation layer, the kernel has a convenient point to intercept this: it can move some pages that aren't currently in use out to disk (the **swap** area), freeing up physical frames for active processes
- The page table entry for a swapped-out page is marked invalid; if the process tries to access it again, this triggers a **page fault**, and the kernel reads the page back in from disk before resuming the process
- This lets the system keep running (slowly, for swapped processes) instead of simply failing to start new processes when RAM is full

**Limitations of Virtual Memory**

All of this flexibility isn't free:

- **Extra translation layer** - the CPU can't use virtual addresses directly; every memory access needs a virtual -> physical lookup
- **More bookkeeping** - page tables themselves consume memory and need to be maintained per-process
- **Page faults** - a miss in the page table (e.g. a swapped-out page) requires a trap into the kernel to resolve, which is a relatively expensive mode switch
- **More complex hardware** - CPUs need a Memory Management Unit (MMU) to do translation, and a **TLB** (Translation Lookaside Buffer) to cache recent virtual->physical translations so most accesses don't have to walk the full page table
- **TLB misses** - if a translation isn't cached in the TLB, the CPU has to walk the page table in memory to find it, adding latency to what would otherwise be a single memory access

## DMA

### Peripherals Read (without DMA)

![](assets/Pasted%20image%2020260610224356.png)

- Without DMA, every byte transferred between a peripheral and RAM has to pass *through* the CPU
- E.g. keyboard -> CPU -> RAM, or network card -> CPU -> RAM
- The CPU has to actively copy each chunk of data itself, which means it can't do other useful work during the transfer
- This is fine for tiny, infrequent transfers (a keypress), but becomes a real bottleneck for large/frequent transfers (disk I/O, network packets) - the CPU spends cycles babysitting a copy instead of computing

### DMA (Direct Memory Access)

![](assets/Pasted%20image%2020260610224647.png)

- A separate **DMA controller** sits between RAM and peripherals, and can move data directly between them **without the CPU being involved in the actual transfer**
- The flow: the CPU programs the DMA controller once (source, destination, length), then the controller performs the transfer on its own; the CPU is free to do other work and is only **interrupted once the transfer completes**
- This frees up the CPU for large transfers - it pays a small one-time setup cost instead of being tied up for the whole transfer

**Notes about DMA**

- DMA transfers use **physical addresses**, not virtual ones
- The DMA controller traditionally has no concept of virtual memory and doesn't go through the MMU - it just reads/writes physical RAM directly
- Because of this, memory that's the target of a DMA transfer (e.g. a kernel buffer for an in-flight disk read) **must not be swapped out** while the transfer is in progress - the physical address has to remain valid and stable
- **IOMMU** - an MMU for I/O devices. It lets devices use "virtual" device-addresses that get translated to physical addresses, which restores some of virtual memory's benefits (isolation, not needing physically-contiguous buffers) for DMA-capable devices

**O_DIRECT**

- An important flag/option for file systems and databases
- Normally, file reads/writes go through the OS **page cache** - an extra copy in kernel memory
- `O_DIRECT` bypasses this cache: data is transferred (via DMA) straight between the disk and the application's user-space buffer
- Databases (e.g. Postgres, MySQL/InnoDB) often use this because they manage their *own* caching (e.g. the buffer pool) and don't want data double-buffered in both the OS page cache and their own cache

**Pros and Cons**

Pros:

- Efficient, high-throughput transfers for large I/O
- CPU is freed from managing the byte-by-byte copy
- Avoids unnecessary virtual-memory translation/management for the transfer itself

Cons:

- Added hardware complexity (DMA controller, IOMMU)
- Security concerns - a device with raw physical-memory access can potentially read/write memory it shouldn't (see DMA attacks below)
- Setup/initialization overhead per transfer - not worth it for tiny transfers
- Not used for things like keyboard/mouse interrupts: the data volume is so small that the CPU handling it directly is simpler and effectively just as fast

**DMA Attacks**

- Because DMA-capable devices can read/write physical memory directly and historically bypass the MMU, a malicious or compromised peripheral can access memory it has no business touching - including secrets like encryption keys or credentials sitting in RAM
- This is the basis of real-world attacks via hot-pluggable, DMA-capable ports like FireWire and Thunderbolt: an attacker plugs in a malicious device and uses DMA to read or modify the host's memory, sometimes even while the screen is locked
- IOMMUs (above) are a key mitigation - they let the OS restrict which physical memory regions a given device is allowed to access via DMA, rather than granting unrestricted access

## Resources

- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/8_MainMemory.html
- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/9_VirtualMemory.html
- [What Every Programmer Should Know About Memory](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) - Ulrich Drepper's classic, in-depth paper covering DRAM internals, CPU caches, and virtual memory
- [Operating Systems: Three Easy Pieces - Address Spaces / Paging / Swapping chapters](https://pages.cs.wisc.edu/~remzi/OSTEP/) - free textbook with very approachable chapters on virtual memory, paging, TLBs, and swapping
- [Gallery of Processor Cache Effects](https://igoro.com/archive/gallery-of-processor-cache-effects/) - hands-on examples of how memory layout/alignment affects real-world performance
- [DMA attack - Wikipedia](https://en.wikipedia.org/wiki/DMA_attack) - background on FireWire/Thunderbolt DMA attacks and IOMMU mitigations