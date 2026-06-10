# Introduction

## Why OS ?

![](assets/Pasted%20image%2020260607083421.png)

A computer is made up of multiple components - CPU, SSD, RAM, network cards, graphics cards, mouse, keyboard, etc.

An operating system is **software** that helps *manage* these resources. Specs for different types of CPUs and their operational methods are quite different. The OS ensures that these vastly different components work in unison, often utilizing *drivers* provided by the manufacturer or generic *drivers*.

- Applications talk to the OS
- Most OSs are general purpose

### Scheduling

All applications compete for CPU time to run themselves; the OS handles the task of scheduling and allocating each application/process its share of time to run, while also managing resources.

Ex - Windows 3.1 used cooperative scheduling, where an application could block the CPU; preemptive scheduling came later.

- Scheduling is critical
- People do PhDs on this topic - building a general-purpose scheduler is very difficult; building a predictable one is possible
- Fair share of resources to all processes
    - CPU/Memory/IO
- Some applications, like InnoDB, allow tunable IOPS, letting other processes get a larger share of the available I/O operations

### Hardware abstraction

- OS APIs abstract the hardware: POSIX
- Your app will work on any hardware*
- Occasional breaking changes (64-bit/32-bit)

### Can you build your app without an OS?

- Yes, but it's very difficult. For example, the kernel decides how something like a socket is stored and handled, and this behavior can be changed at the kernel level - and that can make things slower.
- A good real-world case: Google found that Linux servers with many NVMe drives took too long to reboot because the kernel issued shutdown commands to each SSD synchronously, one at a time; they fixed it by making SSD shutdown asynchronous. See [Google proposes shutdown changes to speed up Linux reboots](https://www.phoronix.com/news/Google-Linux-Too-Many-NVMe).

### Why this matters

- An OS shouldn't be a black box - understanding it helps you build more efficient apps
- Ex - Python's `None` is a singleton, and CPython tracks it via reference counting; every comparison, default argument, or assignment that touches `None` bumps its refcount, and at scale that constant churn adds measurable overhead. This got bad enough that CPython 3.12+ made `None`, `True`, `False` and a few other commonly used objects "immortal" - their refcount is frozen so it's never incremented or decremented. Knowing how the runtime manages memory underneath helps you spot why something this innocuous-looking can show up in a profiler. See [CPython Reference Counting and Garbage Collection Internals](https://blog.codingconfessions.com/p/cpython-garbage-collection-internals).
- Understanding the OS helps you appreciate and understand what's required further - it builds the foundation for grasping how the languages, runtimes, and tools you use every day actually behave

## System Architecture

- A system has resources: CPU, memory, storage, network, etc.
- The kernel is the OS's core component
- The kernel manages these resources
- The OS includes more than the kernel - it also ships tools for usability (shells, GUIs, utilities)

### CPU

- Central Processing Unit
- Consists of multiple cores
- Earlier CPUs had a single core dedicated to running tasks one at a time; nowadays we have multiple cores on the same chip, running tasks in parallel
- Each core runs at a clock speed
- Executes machine-level instructions
- Has fast caches (L1/L2/L3) to avoid going to slower main memory
- Cache coherence - keeping each core's view of cached data consistent - is one of the hardest problems to solve. See [Cache coherency primer](https://fgiesen.wordpress.com/2014/07/07/cache-coherency/).

### Memory

- Memory access is slow; Apple has done interesting work bringing memory onto the same package as the CPU (unified memory architecture) to cut that latency
- Random Access Memory (RAM) - unlike disks, reading from it doesn't require a physical seek
- Fast but volatile - databases use a Write-Ahead Log (WAL) to persist data safely despite this
- Stores process state and data while the process runs
- Limited - a scarce resource
- Virtual memory is an abstraction that hides physical memory's complexity from applications
- Slower than CPU cache

### Storage

- Persistent storage - stores data long-term, surviving reboots/power loss
- HDD (magnetic) wears down gradually over time; SSDs have a fixed lifespan with a definite erase cycle - to write data you must find an empty page, invalidate the old page, and write the new data
- Slower than memory

### Network

- Network Interface Controller (NIC)
- TCP/IP Offload Engine - moves protocol processing off the CPU and onto the NIC
- Communicates with other hosts
- Protocol implementation follows standards published as RFCs - see the [TCP/IP tutorial (RFC 1180)](https://datatracker.ietf.org/doc/html/rfc1180) for an overview

### Kernel

- Core of the OS
- Focused on core OS tasks
- Manages resources
- The OS is more than the kernel
    - GUI, command-line tools, UI, and other tooling
    - E.g. `top` is a tool that displays running processes
    - Distros are largely about this extra tooling layered on top of the kernel

### File System

- Storage is mostly exposed as blocks of bytes (a block store)
- We like to work with files, not raw blocks
- A file system is an abstraction over that block store
- It defines how files are organized and stored on disk
- btrfs, ext4, fat32, NTFS, tmpfs

#### HDD

- An HDD consists of platters, heads, tracks, and sectors
- Traditionally the OS addressed disks using the CHS method
    - Cylinder/Head/Sector
- Geometric sector vs. logical disk sector
- The OS *knows* the physical layout of the HDD

#### LBA

- Later, OSes moved to a new addressing scheme: LBA
- Logical Block Addressing
- The entire disk is exposed as a single array of blocks
- The disk controller handles the translation from logical block to physical location
- Adds a small translation overhead, but lets manufacturers change the physical disk layout without breaking compatibility

#### Partitions

- Disks are exposed as one big array of LBAs (logical sectors)
- Partitions start at one LBA and end at another
- Provides logical segmentation
- E.g. Partition 1 spans LBA 1 - LBA 4
- Each partition can have its own file system
- Each file system can use a different block size (clusters)

### Program vs Process

- A program is the compiled executable
- A process is an instance of a program
- A process is "a program in motion"
- Executable file formats: PE (e.g. `postgres.exe` on Windows), ELF on Linux

### Process Management

- The kernel manages processes
- Schedules processes onto a CPU
- Switches from one process to another (context switching)
- Grants processes access to resources like storage

### User Space vs Kernel Space

- User space (e.g. addresses `0x00000000`-`0xC0000000` on 32-bit Linux)
    - browser
    - postgres
- Protected kernel space
    - kernel code
    - device drivers
    - TCP/IP stack
- A user process can't execute kernel-space instructions directly - it has to switch into kernel mode (via a system call) to get the kernel to do that work for it
- This separation is meant to be strictly isolated, though `io_uring` blurs the line a bit by sharing ring buffers between user and kernel space. That extra surface area has caused real problems: Google ended up restricting `io_uring` across its products after it became a major source of security vulnerabilities. See [Google limiting io_uring use due to security vulnerabilities](https://www.phoronix.com/news/Google-Restricting-IO_uring).

### Device Drivers

- Drivers are software that live in the kernel
- They manage hardware devices
- NVMe, keyboard, NIC, etc.
- Interrupt Service Routine (ISR) - runs immediately in response to a hardware interrupt

### System Calls

- The way to jump from user mode to kernel mode
- The user makes a system call
- E.g. `read()`, `write()`, `malloc()`
- Involves a mode switch - important for isolation, but expensive

## Further reading

- [Google proposes shutdown changes to speed Linux reboots](https://www.phoronix.com/news/Google-Linux-Too-Many-NVMe) - the NVMe synchronous-shutdown bug mentioned above, and how Google fixed it
- [CFS: Completely fair process scheduling in Linux](https://opensource.com/article/19/2/fair-scheduling-linux) - a good accessible look at how Linux's default scheduler tries to give every process its fair share of CPU time
- [CPython Reference Counting and Garbage Collection Internals](https://blog.codingconfessions.com/p/cpython-garbage-collection-internals) - covers the `None` refcount story above and how CPython 3.12+ made it (and a few others) "immortal" to cut the overhead
- [cpu.land - Putting the "You" in CPU](https://cpu.land/) - an awesome, accessible walkthrough of what actually happens when you run a program: processes, system calls, memory, interrupts, and program loading
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) - free, widely-used OS textbook covering virtualization (CPU/memory), concurrency, and persistence
- [The Linux Kernel documentation](https://www.kernel.org/doc/html/latest/) - the primary source for how the Linux kernel actually implements scheduling, memory management, file systems, etc.
- [Modern Operating Systems by Andrew S. Tanenbaum](https://www.pearson.com/en-us/subject-catalog/p/modern-operating-systems/P200000003229) - a classic, broad textbook covering OS fundamentals across processes, memory, file systems, and I/O