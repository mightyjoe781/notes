---
title: More OS Concepts
description: Compilers and linkers, interpreted languages and JIT compilation, garbage collection, kernel/user mode switching, and virtualization vs containerization.
tags:
  - concept
---

# More OS Concepts

## Compilers and Linkers

### Machine Code

- Programs ultimately run as **machine code** - raw binary instructions the CPU executes directly
- Machine code is specific to a CPU's instruction set (e.g. x86-64, ARM64)
- Different CPU families use different instruction sets - see [cpu.md](cpu.md) for the RISC vs. CISC distinction

### Assembly

- Assembly is the closest human-readable representation of machine code - roughly a 1:1 mapping to instructions
- It's still tied to a specific CPU architecture (an x86 assembly program won't run on ARM)
- Easier to write than raw machine code, but still far more tedious and error-prone than a high-level language

### High-Level Languages

- High-level languages (HLLs) are far more convenient to write in - they provide abstractions that hide most of the CPU-specific detail
- That convenience comes at a cost: the code still has to be turned into machine code for a specific CPU before it can run
- Two steps are involved: **compiling** turns source code into machine code (as object files), and **linking** combines those object files into a runnable executable

### Compiling

- A compiler turns source code into **object files** containing machine code
- Each source file typically produces its own object file
- Object files aren't runnable on their own - they're missing things like the final addresses of functions defined in *other* object files, or in libraries
- They need to be **linked** together to produce an executable
- Examples: `gcc`, `clang`, `rustc`

### Linking

A **linker** takes all the object files (and any libraries) a program needs and combines them into a single executable - resolving references between them (e.g. a call in `file1.o` to a function defined in `file2.o`) and laying out the final binary.

![](assets/Pasted%20image%2020260613165412.png)

The diagram shows the general shape of this process: each source file is compiled (via an assembler, in this simplified view) into its own object file, and the linker combines all of those object files - together with any program libraries - into one executable file.

![](assets/Pasted%20image%2020260613165419.png)

This second diagram shows the full pipeline for a single source file, including the **preprocessor** step that runs before compilation (handling `#include`, macros, etc. in C/C++):

1. **Preprocessor** - expands includes and macros, producing preprocessed source code
2. **Compiler** - turns the preprocessed source into object code
3. **Linker** - combines the object code with any required libraries into the final executable

Several linker implementations exist with different performance characteristics - `ld` (the traditional GNU linker), `gold`, `lld` (LLVM's linker), and the newer [mold](https://github.com/rui314/mold), which focuses heavily on link speed via parallelism:

![mold-times](https://github.com/rui314/mold/raw/main/docs/chart.svg)

### Executable file formats

Once linked, the executable follows a platform-specific file format:

- **PE** (Portable Executable) - Windows (e.g. `postgres.exe`)
- **ELF** (Executable and Linkable Format) - Linux
- **Mach-O** - macOS

### Interpreted Languages

A compiled program is tied to a specific CPU/OS combination - it won't run anywhere else without recompiling. **Interpreted languages** (Python, JavaScript, Java/JVM bytecode, etc.) solve "write once, run anywhere" differently:

- A **runtime** (e.g. `python.exe`, the JVM, Node) is compiled separately for each OS/CPU combination
- Your source code (`hello.py`) doesn't need to be recompiled - it runs unchanged on top of whichever runtime is installed
- E.g. `python hello.py` works the same way on Windows and Linux, because it's the *runtime* that's platform-specific, not your script

This is also why a compiled *binary* generally keeps working on the same OS over time (unless the kernel/OS-level APIs it depends on change) - but an *interpreted* program can stop working on a newer runtime if that runtime drops support for something your code relies on.

**Why are interpreted languages slower?**

- The runtime has to repeatedly figure out what each line/instruction *means* before doing it - effectively re-deciding "if I see `+`, do this; if I see a function call, do that" every time it's encountered
- Many runtimes mitigate this by compiling source down to **bytecode** ahead of time (a compact, simpler instruction format for the runtime's own interpreter), rather than re-parsing source text on every execution - but it's still an extra layer of interpretation compared to native machine code

### JIT (Just-In-Time Compilation)

Everything described as "compiling" so far happens **ahead of time (AOT)**, before the program runs. JIT compilation instead happens *while the program is running*:

- The runtime notices code being interpreted repeatedly (a "hot" function/loop)
- It compiles that code directly to native machine code on the fly
- That machine code is placed in an executable region of memory (typically on the heap, with the page's permissions marked executable)
- The CPU's program counter is pointed at the compiled code instead of going through the interpreter

JIT compilation can make code faster *without changing languages* - the same source, running on a JIT-enabled runtime, can end up executing as native machine code for its hot paths.

### Garbage Collection

- Memory management is tricky to get right manually - forgetting to free memory leaks it; freeing it too early causes dangling-pointer bugs (see [process.md](process.md))
- Some languages manage memory automatically via **garbage collection (GC)**: Go, Python, Java
- Others require manual management: C, C++ (though C++ mitigates this with RAII/destructors)
- A garbage collector is part of the language runtime - it tags and tracks every object, and periodically finds and frees objects that are no longer reachable
- This bookkeeping isn't free - GC can introduce pauses or latency spikes, especially under memory pressure

A real-world example of this tradeoff: Linkerd's original service-mesh proxy (Linkerd 1.x) ran on the JVM (Scala), and like any JVM application it was subject to garbage-collection pauses - a GC pause in the proxy shows up as added latency on every request passing through it, since the proxy sits on the network path between services. This was one of the motivations for **Linkerd2's proxy being rewritten in Rust** - a language with no garbage collector, where memory is managed deterministically at compile time - to get predictable, low tail latency in a component that sits in the hot path of every request.

## Kernel vs User Mode Switching

![294](assets/Pasted%20image%2020260613174906.png)

- Every process's virtual address space is split into two regions: a **user** region and a **kernel** region (in the diagram, addresses `0x00000000`-`0xC0000000` are user space, and `0xC0000000`-`0xFFFFFFFF` are kernel space)
- The kernel portion is mapped to the **same** physical memory in every process - since the kernel itself doesn't change between processes, it's efficient to map it directly rather than maintain a separate copy of those mappings per process
- The user portion maps to *different* physical memory per process, translated via that process's own page table (see [memory.md - Virtual Memory](memory.md#virtual_memory) and the TLB discussion in [process_management.md](process_management.md#tlb_flush))
- The page table is what makes both of these mappings work - kernel addresses resolve the same way for every process, while user addresses resolve differently per process

### Modes

![384](assets/Pasted%20image%2020260613175026.png)

- The CPU itself has two privilege modes: **user mode** and **kernel mode**
- In **user mode**, user code executes, and it can only access the user portion of the address space - any attempt to read/write/jump into the kernel region is blocked by the hardware (the red X in the diagram)
- In **kernel mode**, kernel code executes - this is where system calls and device drivers run - and it can access *both* the kernel and user regions
- This separation is what makes the kernel/user boundary a real security boundary, not just a convention: user-mode code is physically incapable of touching kernel memory without the CPU switching modes first

### Kernel mode Switch Cost

Switching from user mode to kernel mode (e.g. to service a system call) isn't free - it's similar in spirit to a context switch, but within the same process:

- The kernel has its own dedicated stack and code, separate from the process's user-space stack
- When a process invokes a system call (e.g. `read()`), or a page fault occurs, the CPU switches into kernel mode
- The CPU saves the current base pointer and return address onto the **kernel stack**
- All of the user-mode register state is saved to memory
- The kernel looks up which system call was requested (via the syscall number) and dispatches to the right handler
- Kernel-mode code then runs on the kernel stack, with its own accounting/runtime statistics tracked separately from the process's user-mode execution time

This is the underlying cost behind the general advice to minimize syscalls in hot paths - each one involves this save/restore/dispatch dance, on top of whatever work the syscall itself does.

## Virtualization & Containerization

### One Machine, One OS

Traditionally, one physical machine ran one operating system at a time. This is limiting if you want to run multiple OSes - the options are:

- Run one OS at a time, switching which one boots (multi-boot)
- Run multiple OSes *simultaneously* - via virtual machines or containers

### Multiple native OS

![](assets/Pasted%20image%2020260613180748.png)

The simplest form of "multiple OSes on one machine" is **multi-boot**: several full OS installations, each with its own kernel, sit side by side directly on the hardware, but only **one is active at a time** - switching means rebooting into a different one. This gives high isolation (each OS has the entire machine to itself while running), but no two OSes are ever running concurrently.

### Virtualization

![](assets/Pasted%20image%2020260613180741.png)

**Virtualization** runs multiple full OSes *concurrently* on one machine:

- A **base OS** (with its own kernel and tools) runs directly on the hardware
- A **hypervisor** (software) runs on top of that base OS
- The hypervisor manages multiple **guest OSes** ("Full OS1/2/3"), each completely unaware of the others
- The hypervisor proxies guest system calls/hardware access down to the base kernel, and can enforce CPU/memory limits per VM
- This gives strong isolation - each guest behaves as if it has its own machine - but at the cost of redundancy: each guest OS duplicates an entire kernel and userland
- Examples: VMware, VirtualBox

### Containerization

![](assets/Pasted%20image%2020260613180735.png)

**Containers** take a different approach - instead of each "guest" having its own kernel, **all containers share the host's kernel**:

- Containers ("Container1/2/3") sit directly on top of the base OS tools and base kernel - there's no per-container kernel
- Isolation between containers is provided by **namespaces** (each container gets its own view of mounts, processes, network interfaces, etc.)
- Resource limits are enforced by **cgroups** (CPU/memory limits per container)
- Much less overhead than virtualization, since there's no duplicated kernel - but isolation is weaker (a kernel vulnerability can potentially be exploited across container boundaries)
- Example: Docker

**Namespaces**

A kernel feature providing per-process isolated views of various global resources:

- **Mount namespace** - isolates the filesystem mount table, so a container sees its own root filesystem
- **PID namespace** - isolates the process ID space, so a container can have its own "PID 1"
- **Network namespace** - isolates network interfaces, routing tables, etc.

**cgroups (control groups)**

A kernel feature for limiting and accounting resource usage - assigning a maximum share of CPU and memory to a group of processes, so that one container can't starve the others on a shared host.

**What happens when a new container starts**

- New namespaces are created for the container
- The container can only see what's explicitly mounted into it - typically a directory on the host is exposed as the container's root filesystem, and it can't see anything outside that
- The OS tools the container needs are loaded into that filesystem (e.g. Ubuntu's `apt-get`, `ifconfig`, etc.)
- Then the actual application process is started (e.g. `node`)
- Naively, each container would need its **own full copy** of all those base OS tools - which would multiply disk usage across every container running the same base image. **OverlayFS** solves this:
    - The base OS image layer is mounted **read-only** and **shared** across containers
    - Each container gets a thin, container-specific **writable layer** on top, which only stores the *changes* that container makes
    - This is the layering mechanism behind Docker images

**Network**

Each new container gets its own network namespace, so by default it can't see the host's network interfaces at all. Docker typically creates a virtual network that all containers on a host join; each container gets its own virtual NIC, its own MAC address, and is assigned an IP via DHCP on that virtual network.

**Processes**

A container can spawn any number of processes, but - thanks to the PID namespace - it can only *see* its own processes. Multiple containers can each have a process with PID 1 inside their own namespace, even though the host kernel sees each of those as a distinct, globally-unique PID outside any namespace.

## Resources

- [Computer Systems: A Programmer's Perspective (CS:APP)](https://csapp.cs.cmu.edu/) - covers the full compile/assemble/link pipeline and linking in detail
- [mold - a modern, fast linker](https://github.com/rui314/mold) - the linker referenced above, with benchmarks against `ld`/`gold`/`lld`
- [Operating Systems: Three Easy Pieces - Virtual Machines / Concurrency chapters](https://pages.cs.wisc.edu/~remzi/OSTEP/) - covers virtualization, kernel/user mode, and system call mechanics
- [Linux 6.8 Network Optimizations Can Boost TCP Performance For Many Concurrent Connections By ~40% (Phoronix)](https://www.phoronix.com/news/Linux-6.8-Networking) - Google's contribution reorganizing core networking structs for better cache-line utilization, mentioned as a real example of struct-layout optimization (see also [process.md - Performance](process.md#performance))
- [ByteDance Working To Make It Faster: Kexec Booting The Linux Kernel (Phoronix)](https://www.phoronix.com/news/Bytedance-Faster-Kexec-Reboot) - ByteDance's work reducing kernel `kexec` reboot time from ~500ms to ~15ms across their fleet
- [Timeouts, retries, and backoff with jitter (AWS Builders' Library)](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) - a thorough, widely-cited treatment of how to set timeouts and retries correctly in distributed systems
- [A Postgres failure caused by a Cisco router](https://medium.com/@hnasr/a-postgres-failure-caused-by-a-cisco-router-3d285f739a4e) - a real incident where a router's TCP idle-connection timeout (default 1 hour on Cisco routers) silently dropped "idle" Postgres connections, fixed via TCP keepalives (`tcp_keepalives_idle`, etc.)
- [socket_management.md - Send and Receive Buffers](socket_management.md#send_and_receive_buffers) - covers zero-copy I/O, referenced here as the "Zero Copy" topic
- [Docker overlay filesystem driver docs](https://docs.docker.com/storage/storagedriver/overlayfs-driver/) - details on the OverlayFS layering described above

## See Also
- [Docker Containers](../../docker/containers.md)
- [Docker Networking](../../docker/networking.md)
- [Docker Storage](../../docker/storage.md)
