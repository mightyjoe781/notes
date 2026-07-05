---
title: CPU
description: How a CPU core is built and works - ALU/CU/registers/MMU/caches, NUMA, RISC vs CISC, the instruction life-cycle, pipelining, hyper-threading, and SIMD.
tags:
  - concept
---

# CPU

## CPU Components and Architecture

**Basic Components**

![](assets/Pasted%20image%2020260611104823.png)

A single CPU core, at a high level, is built from a handful of pieces stacked together:

- **ALU** (Arithmetic Logic Unit) - does the actual arithmetic and logic operations
- **CU** (Control Unit) - fetches, decodes, and orchestrates execution of instructions
- **Registers** - the core's small, ultra-fast working storage, sitting between the CU/ALU and the rest of the memory hierarchy
- **MMU** (Memory Management Unit) - translates virtual addresses (used by registers/instructions) into physical addresses
- **Caches (L1, L2, L3)** - progressively larger, slower layers between the core and main memory

The diagram shows the typical flow: the CU/ALU work with values in **registers**; when a register needs data from memory, the request goes down through the **MMU** (for address translation) and into the cache hierarchy (**L1**, then further out to **L2**).

**Multiple Cores**

![](assets/Pasted%20image%2020260611104811.png)

- A modern **processor** (chip) contains multiple **cores**, each a near-complete copy of the components above (its own ALU, CU, registers, MMU, and L1)
- **L2** is often per-core too (as shown here), though on some processors it's shared between a small group of cores
- **L3** is shared across *all* cores on the processor - it's the last level of cache before falling back to main memory

**Full Memory Hierarchy**

![](assets/Pasted%20image%2020260611105220.png)

Putting it all together: each core has its own L1 (and often L2), all cores share an L3, and beyond L3 sits **main memory (RAM)**, connected via a shared **bus**. Each step out from the core - L1 -> L2 -> L3 -> RAM - is larger but significantly slower (see the latency numbers under [L Caches](#l-caches) below).

### NUMA - Non-Uniform Memory Access

![](assets/Pasted%20image%2020260611105400.png)

- In multi-socket / multi-die systems, each group of cores has its own "local" memory controller and DIMM (e.g. Cores 1-2 are local to `DIMM1`, Cores 3-4 are local to `DIMM2`)
- A core *can* access memory attached to a different DIMM (e.g. Core 4 reading from `DIMM1`), but that access has to cross an interconnect (**DSM**, Distributed Shared Memory) to reach the remote memory controller
- This makes memory access **non-uniform**: a "local" access (Core 3/4 -> `DIMM2`) is fast, while a "remote" access (Core 4 -> `DIMM1`) is slower and can also be delayed if the remote memory controller is busy serving its own local cores
- As a developer/operator, this is why **NUMA-aware** placement matters: pinning a process's memory allocations and the threads that use them to the same NUMA node (e.g. via `numactl` on Linux) keeps accesses local and avoids the cross-interconnect penalty
- Trade-off: NUMA gives you more aggregate memory bandwidth (each node has its own path to its DIMMs), at the cost of inconsistent latency depending on *where* data and the accessing core happen to be
- Apple's M-series chips (e.g. M1 Ultra, which is physically two dies connected together) are a notable case where the interconnect between the two halves was made fast and high-bandwidth enough that the system behaves close to a single uniform pool of memory, hiding most of the NUMA effect from software

### ALU

- Arithmetic Logic Unit
- Arithmetic `+-/*`
- Logic XOR/OR/AND
- Core of compute

We use half-adders (XOR and AND), full-adders (2 half-adders, connected to OR).

### CU

- Control Unit
- Fetches Instruction
- Decodes Instruction
- Executes Instruction

### Registers

- Small, ultra-fast storage units, typically **32-bit or 64-bit** wide, sitting directly inside the CPU core - the fastest storage in the whole system (faster than even L1 cache)
- There are several specialized registers, alongside general-purpose ones:
    - **PC** (Program Counter) - address of the next instruction to execute
    - **IR** (Instruction Register) - holds the instruction currently being decoded/executed
    - **SP** (Stack Pointer) / **BP** (Base Pointer) - covered in the [stack notes](process.md#the-stack)
- **General-purpose registers** - used by the ALU for arithmetic/logic and to hold intermediate values

**Why register/cache width matters: optimized `memchr()`**

A good real-world illustration of why operating on more bytes at once matters: the Linux kernel's `memchr()` (used to find a byte within a block of memory) traditionally compared one byte at a time. A patch reworked it to load and compare a full **machine word** (8 bytes on a 64-bit CPU) at once using bitwise tricks to detect whether the target byte is present anywhere in that word - only falling back to a byte-by-byte scan once the right word is found. For long searches, this made `memchr()` close to **4x faster**, since the CPU does 8x fewer comparison/branch iterations for the same amount of data. See [Optimized memchr() Implementation For The Linux Kernel Up To ~4x Faster](https://www.phoronix.com/news/Linux-Kernel-Faster-memchr).

### MMU

- Memory Management Unit - sits between the core's registers and the cache/memory hierarchy
- Responsible for translating **virtual addresses** (used by every instruction) into **physical addresses** (used by the actual RAM)
- Caches recent translations in the **TLB** (Translation Lookaside Buffer) so most accesses don't need a full page-table walk (see [memory notes](memory.md#page-tables))
- Because the TLB caches *virtual -> physical* mappings, and that mapping is per-process (each process has its own page table), the TLB entries from one process are meaningless - and potentially a security issue - for another. So the **TLB must be flushed on a context switch** to a different process's address space (modern CPUs use tagged TLBs with an address-space ID to avoid flushing in some cases)

### L Caches

- L1, L2, and L3 form a hierarchy of progressively larger but slower caches between the core and main memory. Not all levels are guaranteed to exist on every CPU, and L2 may be per-core or shared depending on the processor
- **L1** - local to its core, ~1ns, ~128KB
    - Split into two: **L1D** (data) and **L1I** (instructions) - having separate caches lets the CU fetch the next instruction and load/store data in the same cycle, since they don't contend for the same cache
- **L2** - local to its core (sometimes shared by a small group of cores), ~5ns, ~256KB-2MB. Unified (holds both data and instructions)
- **L3** - shared across *all* cores on the processor, ~15ns, ~64MB (some AMD chips ship L3 in the gigabytes via 3D-stacked cache). Also unified
- **Main Memory** - ~50-100ns, far larger but shared and contended across all cores
- Every memory read is cached at every level it passes through on the way back to the core, so subsequent accesses to the same (or nearby, same cache-line) data are much faster
- **Cache invalidation** is one of the hardest problems here: when one core writes to a memory location, any copies of that line cached by *other* cores become stale and must be invalidated or updated (see [Cache coherency primer](https://fgiesen.wordpress.com/2014/07/07/cache-coherency/) from the [introduction notes](introduction.md))
- Some smaller/embedded CPUs only have L1 and a shared L2, with no L3 at all

**Why this matters: CPython's "immortal" `None`/`True`/`False`**

CPython uses reference counting for garbage collection - every time a value like `None` is assigned, compared, or passed as a default argument, its refcount is incremented or decremented. `None`, `True`, `False`, and small integers are extremely "hot" - referenced constantly across virtually all Python code. Every refcount bump is a *write* to that object's memory, and on a multi-core system, a write from one core invalidates that cache line in every other core's cache (the cache-coherency problem above). For objects this frequently touched, that constant cross-core invalidation traffic adds real overhead. CPython 3.12+ made these objects **"immortal"** - their refcount is frozen and never modified - which removes this constant-write/invalidation churn entirely. See [CPython Reference Counting and Garbage Collection Internals](https://blog.codingconfessions.com/p/cpython-garbage-collection-internals).

### CPU Architecture

CPUs are broadly designed around one of two philosophies for their instruction sets:

- **RISC** - Reduced Instruction Set Computer
    - Simple instructions, each doing one task, generally completing in a single cycle
    - Lower power, more predictable timing (easier to pipeline - see below)
    - ARM (and RISC-V)
- **CISC** - Complex Instruction Set Computer
    - A single instruction can do a lot of work (e.g. read memory, compute, write memory) but takes multiple cycles
    - More power-hungry, less predictable timing
    - x86 (Intel/AMD)

### CISC vs RISC - Example

Take `a = a + b`, where `a` and `b` are values in memory:

- **CISC** - one instruction can do it all:
    - `ADD a, b` - the CPU itself reads both memory locations, adds them, and writes the result back to `a`
- **RISC** - the same operation is broken into explicit steps, each a separate instruction:
    - `LDR r0, a` - load `a` into register `r0`
    - `LDR r1, b` - load `b` into register `r1`
    - `ADD r0, r1` - add them, result in `r0`
    - `STR r0, a` - store `r0` back to `a`

RISC trades instruction *count* for instruction *simplicity* - more instructions, but each one is small, fast, and easy for the CPU to pipeline.

### CPU Clock

- The clock speed is how many cycles the CPU performs per second, e.g. **3 GHz = 3 billion cycles/second**
- For a simple RISC design where most instructions complete in one cycle, this is roughly 3 billion instructions/second
- For CISC, where a single instruction can take multiple cycles, the actual instruction throughput is lower than the raw clock rate would suggest
- In practice, every instruction also has fetch/decode overhead on top of execution - **pipelining** (see below) is what allows the CPU to overlap these stages across instructions instead of paying the full cost serially for each one

**Display CPU Info (macOS)**

- Show cache sizes: `sysctl -a | grep cachesize`
- Show number of physical cores: `sysctl -n hw.physicalcpu`
- Show CPU architecture: `uname -m`

## Instruction Life-Cycle

Every instruction the CPU executes goes through the same five stages. Let's walk through executing `sub sp, sp, #12` (shrink the stack pointer by 12, allocating space for a new stack frame - see the [stack notes](process.md#the-stack)), with the program counter (`pc`) currently pointing at address `640`.

**1. Fetch** (MMU + caches)

![](assets/Pasted%20image%2020260611114238.png)

- The CU asks for the instruction at the address in `pc` (`640`)
- This is a virtual address, so it goes through the **MMU** to get translated to a physical address
- The CPU checks its caches for that address - on a miss, it goes all the way to RAM, which returns a full **64-byte cache line** (the burst, covered in the [memory notes](memory.md)) containing that instruction and several neighboring ones
- That cache line is loaded into **L1i** (and L2), so nearby instructions are now cached for free

**2. Decode** (CU)

![](assets/Pasted%20image%2020260611114428.png)

- The CU reads the fetched instruction (`640: sub sp, sp, #12`) from L1i - a **cache hit**
- Instructions are stored as **opcodes** (binary encodings) that the CU translates into the control signals the ALU and registers understand - here, the `sub` opcode is decoded into the gate-level logic that will perform a subtraction

**3. Execute** (ALU)

![](assets/Pasted%20image%2020260611114720.png)

- The CU fetches the operand values from the relevant registers - here, the current value of `sp` (`100`)
- The ALU performs the operation: `sp - 12 = 88`
- The ALU only computes the result; it doesn't read or write registers/memory itself

**4. Write-back** (CU + registers)

![](assets/Pasted%20image%2020260611114909.png)

- The CU takes the ALU's result (`88`) and writes it back into the `sp` register
- (For instructions like `ldr`/`str`, this stage - or an extra "Memory Access" stage between Execute and Write-back - is where the actual memory read/write happens)

**5. Fetch next instruction**

![](assets/Pasted%20image%2020260611115903.png)

- `pc` is incremented to `644`, and the cycle repeats
- Since `644` was part of the same 64-byte cache line fetched in step 1, this is another **cache hit** in L1i - fast!

**What if the next instruction is a function call?**

- A function call (e.g. `bl _malloc`) jumps to a completely different address, which is very likely **not** in the 64 bytes already cached
- This causes a **cache miss** on fetch - the CPU has to stall while a new cache line is loaded from a higher cache level or RAM
- This is one of the costs behind the "function call overhead" discussed in the [process notes](process.md#why-this-matters-function-call-overhead-at-scale) - jumping around to many small functions means more instruction-cache misses, on top of the stack-frame setup/teardown cost
- **Inlining** - the compiler copies a small function's body directly into its caller instead of emitting a `call`, avoiding both the jump (and its cache-miss risk) and the stack-frame overhead entirely

> Two related topics worth knowing about, even though they're not detailed here yet: **branch prediction** (the CPU guesses which way an `if`/conditional jump will go and speculatively fetches/executes down that path, to avoid stalling the pipeline while the condition is computed) and **speculative execution** more broadly. The Spectre/Meltdown vulnerabilities (2018) showed that the *side effects* of this speculative work (e.g. what ends up in the cache) can leak data even when the speculated instructions are later discarded - a good entry point if you want to dig deeper.

## Pipelining and Parallelism

### CPU mostly idle

- In the instruction life-cycle above, only **one** stage (Fetch, Decode, Execute, or Write-back) is doing useful work on any given cycle - the rest of the CPU's stage hardware sits idle
- **Pipelining** fixes this: while instruction 1 is being *decoded*, the CPU can already start *fetching* instruction 2. While instruction 1 *executes*, instruction 2 can be *decoded*, and so on
- The diagram shows the difference: without pipelining, instruction 2 doesn't start until instruction 1 has gone through all four stages. With pipelining, each stage's hardware is kept busy on a different instruction every cycle, dramatically increasing overall throughput (instructions completed per second) even though any single instruction still takes the same number of stages/cycles to complete

![](assets/Pasted%20image%2020260611115903.png)

This idea isn't unique to CPUs - **HTTP/1.1 pipelining** applies the same principle to network requests: instead of waiting for each response before sending the next request, the client sends multiple requests back-to-back without waiting, overlapping the "in flight" time of each request.

![HTTP Pipelining](https://upload.wikimedia.org/wikipedia/commons/1/19/HTTP_pipelining2.svg)

### Parallelism

![](assets/Pasted%20image%2020260611120259.png)

- Pipelining overlaps the *stages* of instructions on a single core - it doesn't let two instructions execute at the exact same instant
- True **parallelism** requires multiple cores: an application splits a big task into multiple processes or threads, and the OS scheduler assigns each one to run on its own CPU core, so they execute genuinely simultaneously
- Without multiple cores (left side), a "big task" runs as one sequential unit on one CPU. With multiple cores (right side), the task is split into independent processes that run truly concurrently

### Hyper-Threading

![](assets/Pasted%20image%2020260611120352.png)

- Without hyper-threading, a single physical core can only run one process/thread at a time - a second process has to **queue** and wait its turn (left side)
- **Hyper-Threading** (Intel's name for simultaneous multithreading, SMT) lets a single physical core present itself to the OS as **two (or more) logical cores/hardware threads**
- Each logical core gets its **own copy of certain registers** (e.g. `pc`, general-purpose registers) so the OS can schedule a separate thread onto each one - but they **share** the underlying execution resources: the ALU, CU, and caches
- This works because a single thread rarely keeps every part of the core busy (recall "CPU mostly idle" above) - while one logical thread is stalled (e.g. waiting on a cache miss), the core's execution units can make progress on the other logical thread's instructions
- It's not "free" parallelism like adding a real core - if both logical threads need the ALU at the same instant, one has to wait. But it improves overall utilization of an otherwise-idle core

### SIMD

- **S**ingle **I**nstruction, **M**ultiple **D**ata - one instruction performs the same operation on several values at once, by loading them into a wide **vector register**
- Instead of issuing 4 separate `add` instructions (one pair of operands each), a single SIMD instruction operates on all 4 pairs simultaneously
- Useful anywhere the same simple operation is applied across large arrays of data: graphics/gaming (transforming vertices, pixels), audio/video processing, and database engines (e.g. scanning columns or comparing keys in B-tree nodes)
- Examples: ARM NEON, x86 SSE/AVX

```
# Traditional - 4 instructions
Add a1, b1
Add a2, b2
Add a3, b3
Add a4, b4

# SIMD - 1 instruction
Add [a1, a2, a3, a4], [b1, b2, b3, b4]
```

## Resources

- [cpu.land - Putting the "You" in CPU](https://cpu.land/) - an excellent walkthrough of what happens when a program runs: processes, the stack, sys-calls, and scheduling
- [What Every Programmer Should Know About Memory](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf) - Ulrich Drepper's paper, with a deep dive into cache hierarchies, cache-line behavior, and NUMA
- [Cache coherency primer](https://fgiesen.wordpress.com/2014/07/07/cache-coherency/) - a good explanation of why cache invalidation across cores is hard
- [Optimized memchr() Implementation For The Linux Kernel Up To ~4x Faster](https://www.phoronix.com/news/Linux-Kernel-Faster-memchr) - the word-at-a-time `memchr()` story referenced above
- [CPython Reference Counting and Garbage Collection Internals](https://blog.codingconfessions.com/p/cpython-garbage-collection-internals) - covers the immortal `None`/`True`/`False` story
- [Computer Systems: A Programmer's Perspective (CS:APP)](https://csapp.cs.cmu.edu/) - covers CPU architecture, pipelining, and the memory hierarchy in depth
- [Modern Microprocessors - A 90 Minute Guide!](https://www.lighterra.com/papers/modernmicroprocessors/) - a widely-read, accessible guide to pipelining, superscalar execution, and RISC vs CISC
- [How CPU efficient is your app](https://www.youtube.com/watch?v=BTD5I1BMx2Q)
