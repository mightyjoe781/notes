---
title: Process Management
description: Processes vs threads, PCBs/TCBs, fork and copy-on-write, context switching and TLB flushes, scheduling algorithms, and concurrency primitives like mutexes and semaphores.
tags:
  - concept
---

# Process Management

## Process vs Thread

### Process

![295](assets/Pasted%20image%2020260611232027.png)

- A process is an instance of a program - see [process.md](process.md) for the full breakdown of a process's address space (stack, heap, data, code)
- Each process has its own dedicated code, stack, heap, and data section - it's isolated from every other process
- It also has its own *context* in the CPU: the program counter (`pc`), link register (`lr`), stack pointer, and other registers that describe exactly where execution currently is
- The kernel needs to remember this context when the process isn't actively running on a core. That's the job of the **Process Control Block (PCB)** - it lives in kernel memory and holds the saved registers (`pc`, `lr`, etc.), so the process can be paused and resumed later without losing its place

### Process Control Block

- The kernel needs metadata about every process it manages - this is what the PCB stores
- PCB contains:
    - PID, process state, program counter, registers
    - Process control info (running/stopped, priority)
    - Page table (virtual memory to physical memory mapping)
    - Accounting info (CPU/memory usage)
    - Memory management info (pointers to code/stack/heap regions)
    - I/O info (file descriptors)
    - IPC info - semaphores, mutexes, shared memory, message queues

### Kernel Process Table

![353](assets/Pasted%20image%2020260611232749.png)

- The kernel needs a quick way to go from "which process is this?" to "where is its metadata?"
- The **process table** is exactly that: a mapping from PID to PCB, kept in kernel space
- In the diagram, PID `100` maps to the PCB at address `0x222222` (currently `running`, with its saved `pc`), and PID `200` maps to the PCB at `0x333333` (currently `stopped`). Each PCB in turn describes that process's own address space (code/data/heap/stack)
- Because this table lives in kernel space, user-space code can't read or tamper with it directly - it has to go through system calls (e.g. `/proc` on Linux is a window into parts of it)

### Thread

![453](assets/Pasted%20image%2020260611233358.png)

- A thread is a *lightweight* process - it runs inside an existing process rather than getting a brand-new address space
- Threads of the same process share the code, heap, and data sections, and they share the same PCB-level resources (page table, open file descriptors, etc.)
- What's *not* shared is the stack and the CPU context (`pc`, registers) - each thread gets its own stack, carved out of the same virtual address space as the other threads' stacks
- Because all of a process's threads live in the same virtual memory, switching between them doesn't require changing the page table mapping - this is the key reason thread switches are cheaper than process switches (see [TLB flush](#tlb-flush) below)

### Thread Control Block (TCB)

- Just as the kernel keeps a PCB per process, it keeps a **Thread Control Block (TCB)** per thread
- TCB contains:
    - TID, thread state, program counter, registers
    - Thread control info (running/stopped, priority)
    - Accounting/management info (e.g. pointer to this thread's stack)
    - A pointer back to the parent PCB, so the thread can find the shared resources (code, heap, data, page table) it doesn't have its own copy of

### Kernel Thread Table

![412](assets/Pasted%20image%2020260611234512.png)

- Just like the process table, the kernel keeps a **thread table** - a mapping from `(PID, TID)` to TCB, kept in kernel space for quick lookup
- In the diagram, both TID `1001` and TID `1002` belong to PID `100`, each with its own TCB (`0x222222` and `0x333333`) holding its own saved registers and state (`running` vs `stopped`)
- Both TCBs point back to the same PCB (`100`), which is where the shared code, heap, data, and page table live
- Notice that thread 1's stack and thread 2's stack sit side-by-side within the same process's virtual address space (alongside the main process stack), rather than each thread getting an entirely separate address space the way a process would

### Shared Memory

- Multiple processes (not just threads of the same process) can share memory too, via `mmap` with a shared mapping
- The key idea: each process keeps its *own* virtual memory and page table, but a region of those virtual addresses is mapped to the *same* physical pages - so writes by one process are visible to the other. See [memory.md - Shared Memory](memory.md#shared-memory) for the full picture of virtual vs. physical memory in this setup
- Databases use this heavily - e.g. Postgres's **shared buffers** are a region of shared memory that every Postgres backend process maps into its own address space, so they're all looking at the same cached pages without copying data between processes

### Postgres Processes

![331](assets/Pasted%20image%2020260611234656.png)

- Postgres uses a **multi-process** architecture: each client connection gets its own dedicated backend process (forked from the postmaster), rather than a thread within one big server process
- These backend processes are isolated from each other (separate address spaces, separate page tables), but they all attach to the same shared memory region - this is where the shared buffer cache and WAL records live, as shown in the diagram, alongside background workers like the autovacuum workers and WAL senders
- This design gives strong isolation (a crashing backend can't corrupt another backend's memory directly) at the cost of higher per-connection memory overhead and more expensive context switches between backends compared to thread switches
- Whether Postgres should move to a thread-based model is a long-running discussion in the Postgres community. As of 2024-2025 there's an active proposal and mailing-list thread, ["Let's make PostgreSQL multi-threaded"](https://www.postgresql.org/message-id/31cc6df9-53fe-3cd9-af5b-ac0d801163f4@iki.fi) by Heikki Linnakangas, with [LWN coverage discussing the tradeoffs](https://lwn.net/Articles/934940/) (lower per-connection memory, but a huge amount of code that currently assumes "one backend = one process" would need auditing for thread-safety)

### Fork

- `fork()` creates a new process by duplicating the calling process
- The child needs its *own* virtual memory - it can't simply share the parent's page table outright, since each process must be able to modify its own memory independently
- The kernel makes this cheap via **Copy-on-Write (CoW)**: parent and child initially share the same physical pages (marked read-only), and a page is only copied when either side actually writes to it. See [memory.md - Copy-on-Write](memory.md#virtual-memory) for the full mechanism and the Redis snapshotting example
- This is also why `fork()`-based snapshotting (like Redis's RDB/AOF rewrite) is cheap: the child mostly just reads pages that never change from its point of view

### Python CoW bug

- A good illustration of how CoW interacts badly with reference counting: every Python object - including singletons like `None`, `True`, and `False` - carries a refcount that's incremented and decremented as the object is used
- After a `fork()` (e.g. in a pre-fork web server like Gunicorn), parent and child share those CoW pages - but as soon as either process touches an object's refcount, that page gets copied, even though the *value* of the object hasn't logically changed
- Because `None`/`True`/`False` are touched constantly, this could quietly defeat CoW sharing across many forked workers, each ending up with its own private copy of pages that should have stayed shared
- This is part of the motivation behind CPython 3.12+ making these objects "immortal" (refcount frozen, never written) - see [cpu.md - CPython's immortal None/True/False](cpu.md#cpu-architecture) for the full story

## Context Switching

### CPU Process

- The CPU itself has no concept of a "process" - it just executes whatever instructions the program counter points it at, using whatever registers are currently loaded
- The OS is what gives meaning to "this CPU is running process X": it loads that process's saved registers (`pc`, `sp`, `bp`, etc.) into the CPU, including the pointer to that process's page table (`ptbr` - page table base register)
- This loaded state - registers plus `ptbr` - is collectively called the **context**
- Once loaded, the CPU just keeps executing instructions from wherever `pc` points, oblivious to which "process" that corresponds to

### Context Switch

- To switch from running one process to another, the OS performs a **context switch**: save the current context, then load the new one
- **Save**: write the current CPU registers back into the outgoing process's PCB (a memory write)
- **Load**: read the incoming process's saved registers from its PCB into the CPU (a memory read)
- This includes `pc`, `bp`, `sp`, `lr`, `ptbr`, and more

![](assets/Pasted%20image%2020260612112311.png)

The CPU is executing process 100's instructions. Many registers are involved, but the diagram shows just `pc` and `ptbr` for simplicity. `ptbr` (page table base register) points to the physical address of the page table that maps process 100's virtual addresses to physical memory; `pc` holds the virtual address of the instruction currently executing.

![](assets/Pasted%20image%2020260612112512.png)

The OS periodically interrupts the running process to check whether a context switch is needed - typically via a timer interrupt (a Programmable Interval Timer or High Precision Event Timer firing every few milliseconds). When it decides to switch away from process 100, process 100's current register state (`pc=4012`, etc.) is saved into its PCB, and process 100 moves to the *ready* state.

This timer interrupt is also the answer to "how does the kernel get to run at all, if it's not a process being scheduled like everything else?" - the timer fires unconditionally, on a hardware interrupt, which forces the CPU into kernel mode and starts executing the scheduler's interrupt handler regardless of what was running a moment ago.

![](assets/Pasted%20image%2020260612112730.png)

The OS then loads process 200's PCB into the CPU's registers (`pc=8008`, `ptbr=0x444444`). Process 200 is now in the *running* state. Because `ptbr` changed - process 200 has a different page table than process 100 - the TLB must also be flushed (see below).

### TLB flush

- The TLB caches recent virtual-to-physical address translations so the CPU doesn't have to walk the page table on every memory access
- Those cached translations are only valid for *one* process's page table - processes can't share virtual-to-physical mappings, since the same virtual address means something different in each process's address space
- So on a context switch between two different processes, the TLB has to be flushed - the next several memory accesses will all miss the TLB and pay the cost of a full page-table walk, which is slow
- Threads of the same process don't have this problem: they share the same page table (same `ptbr`), so switching between threads of one process doesn't require a TLB flush - this is a major reason thread switches are cheaper than process switches

From this, process switches are inherently more expensive than thread switches - which is exactly the tradeoff at the heart of the Postgres processes-vs-threads discussion above.

### TLB ASID

![355](assets/Pasted%20image%2020260612113735.png)

- Modern ARM and Intel CPUs avoid full TLB flushes on every context switch by tagging each TLB entry with an **Address Space ID (ASID)** alongside the virtual address
- Each process is assigned an ASID (a small number, typically up to 255 distinct values depending on the architecture)
- A TLB lookup now matches on *both* the virtual address and the ASID - so entries belonging to a previously-running process can stay in the TLB without being usable by the new process, and don't need to be evicted just because a context switch happened
- If the new process's translations are still in the TLB (e.g. it ran recently and got switched back to quickly), this avoids the page-table-walk penalty entirely

**When does a context switch happen?**

- The scheduler decides a different process/thread should run (see Scheduling Algorithms below)
- Preemptive multitasking - the OS interrupts a running process that's used up its time slice
- The running process blocks on I/O and can't make progress until it returns

### Preemptive Multitasking

![Preemptive Multi-tasking](https://media.geeksforgeeks.org/wp-content/uploads/20260130174207229367/preemptive_scheduling_vs_non_preemptive_scheduling.webp)

- Some processes would happily run forever if left alone (e.g. a tight CPU-bound loop) - the OS must be able to switch them out regardless of whether they "want" to give up the CPU
- **Preemptive** scheduling means the OS can forcibly suspend a running process via a timer interrupt, after it's been given a fixed **time slice** (quantum) to run
- This is in contrast to *cooperative* scheduling, where a process voluntarily yields control - older systems like Windows 3.1 worked this way, and a single misbehaving application that never yielded could freeze the entire system, since nothing could forcibly take the CPU back from it (see [introduction.md - Scheduling](introduction.md#scheduling)). Preemptive scheduling, enforced by the timer-interrupt mechanism described above, fixes this by guaranteeing the OS regains control on a fixed schedule no matter what the running process does

### Scheduling Algorithms

- The scheduler decides which process/thread runs on which CPU core, and for how long
- This is a deep area - entire research careers are built on scheduling algorithms, because a *general-purpose* scheduler that's fair across wildly different workloads (interactive, batch, real-time) is genuinely hard to get right
- One useful heuristic: threads belonging to the same process benefit from being scheduled on the same core (or nearby cores sharing a cache), since they share memory and can reuse cached data - scheduling them on distant cores adds cache-coherency traffic (see [cpu.md](cpu.md) on NUMA and cache coherence)

Some classic algorithms:

- **First Come First Served (FCFS)** - run processes in arrival order; simple, but a long process at the front makes everything behind it wait (convoy effect)
- **Shortest Job First (SJF)** - run whichever process needs the least remaining CPU time next; optimal for average wait time, but requires knowing (or estimating) run times in advance, and can starve long jobs
- **Round Robin** - give each process a fixed time slice in turn, cycling through the ready queue; fair and simple, and the basis for most modern time-sharing schedulers (e.g. Linux's CFS is a more sophisticated descendant of this idea)

## Concurrency

### CPU time is precious

- CPU cores are a shared, finite resource - the goal of scheduling and concurrency is to keep them as busy as possible doing useful work
- A useful question for any workload: can this one task be split into multiple concurrent pieces, so that while one piece is waiting (e.g. on I/O), another piece can use the CPU?

### CPU Bound vs IO Workload

- **CPU-bound** workloads spend most of their time actually computing: encryption, compression, database query planning, sorting, protocol parsing (HTTP/2, QUIC framing). These want to avoid starving other CPU-bound work of core time
- **I/O-bound** workloads spend most of their time waiting on something external: database queries, network reads/writes, file reads/writes. These want to avoid blocking the CPU while waiting - the CPU should be free to do other work during that wait

### Multi-threaded vs Multi-Process

- **Multi-process**: spin up multiple separate processes, each isolated with its own address space. Example: nginx, Postgres (see [Postgres Processes](#postgres-processes) above)
- **Multi-threaded**: one parent process spins up multiple threads that share its memory. Example: MySQL, Node's `libuv` thread pool

**Concurrency vs Parallelism**

![Concurrency vs Parallelism](https://i.ytimg.com/vi/RlM9AfWf1WU/maxresdefault.jpg)

- **Concurrency** is about *structure*: multiple tasks are in progress at the same time, making progress by interleaving - even on a single core, a scheduler can switch between tasks fast enough that they appear to run simultaneously
- **Parallelism** is about *execution*: multiple tasks are physically running at the same instant, on different cores
- A single thread can handle many concurrent tasks (e.g. an event loop interleaving many I/O-bound requests), without any parallelism at all

### Concurrency Issues

- Concurrency introduces correctness challenges that don't exist in single-threaded code:
    - Two threads reading and writing the same variable without coordination (a thread-safety / data-race problem)
    - Two processes writing to the same shared memory region without coordination

![159](assets/Pasted%20image%2020260612121422.png)

This diagram shows a classic race condition. Two threads, T1 and T2, both want to increment a shared variable `a` (starting at `a = 1`):

- T1 reads `a = 1`, computes `a + 1 = 2`
- T2 *also* reads `a = 1` (before T1 has written back), computes `a + 1 = 2`
- T1 stores `a = 2`, then T2 stores `a = 2`

The two increments were meant to add up to `a = 3`, but because both threads read the *same* stale value before either wrote back, one increment is silently lost and `a` ends up at `2`. This is why `a++` is not atomic, and why concurrent access to shared state needs explicit synchronization (mutexes, atomics, etc.) - the topic of the next sections.

### Mutexes

- A **mutex** (mutual exclusion lock) is a binary lock: either held or free
- Thread 1 acquires the mutex - succeeds, since it was free
- Thread 2 tries to acquire the same mutex - it's already held, so Thread 2 blocks (waits)
- Thread 1 makes its change to the shared data, then releases the mutex
- Thread 2 immediately unblocks, acquires the mutex, and makes its own change

### Mutexes Gotchas

- A mutex has **ownership** - whichever thread locked it is the one responsible for unlocking it
- If a thread terminates (crashes, or exits) while still holding a mutex, that mutex can remain locked forever, with no one left to unlock it
- This is one of the classic causes of **deadlock** - other threads waiting on that mutex will block indefinitely

### Semaphores

- A **semaphore** is a more general synchronization primitive than a mutex - it's a counter, not just a binary lock, so it can also be used for mutual exclusion (a semaphore initialized to 1 behaves like a mutex)
- **Signal** (aka `post`/`release`) atomically increments the counter; **Wait** (aka `acquire`) atomically decrements it
- `Wait` blocks if the counter is already `0` - there's nothing available to "take" yet
- Unlike a mutex, there's no ownership requirement: any thread with access to the semaphore can signal or wait on it, regardless of which thread (if any) last touched it. This makes semaphores useful for things like bounding the number of concurrent workers, or signaling between producer/consumer threads

## When do you use threads?

Threads are lightweight processes, processes are programs in motion, and programs are static, on-disk, compiled binaries in a specific executable format.

We try to avoid threads where possible, due to the safety, complexity, shared-state management, and locking issues they introduce. However, there are cases where threads genuinely thrive and their use is clearly beneficial.

So when do you reach for threads? If your task has one or more of these properties:

1. It blocks on I/O
2. It's heavily CPU-bound
3. It's a large volume of small, individually-cheap tasks

In any of these cases, it's favorable to offload the task to a thread. Let's look at each.

#### IO blocking task

When you read from or write to disk, depending on how you do it and which kernel interface you use, the operation might be *blocking*: the process performing the I/O won't execute any more code until the read/write completes.

This is why many logging implementations do their actual writes on a secondary thread (the way Node's `libuv` does) - that thread blocks on the I/O, but the main process/thread can carry on with its work.

If you can do file I/O asynchronously instead - e.g. with `io_uring` - you don't technically need a separate thread for this.

Note the distinction with file I/O specifically: socket I/O is typically handled asynchronously already, via `epoll`/`select` and similar readiness-based APIs, without needing a dedicated thread per connection.

#### Heavy CPU bound

The second use case is when a task needs a lot of CPU time, which would otherwise starve or block the rest of the process from doing its normal work. Offloading that task to a thread lets it run on a different core, so the main process can keep making progress on its original core.

#### Large volume of small tasks

The third use case is when you have a large number of small tasks and a single process can't deliver enough throughput on its own. A classic example is accepting incoming connections: a single process can only `accept()` so fast, so under a massive number of connecting clients, spinning up multiple threads to accept and process connections increases overall throughput. (You'd typically also enable port/socket reuse here, to avoid an accept-mutex bottleneck across those threads.)

## References

- [Operating Systems: Three Easy Pieces - Scheduling chapters](https://pages.cs.wisc.edu/~remzi/OSTEP/) - free textbook covering process scheduling (FCFS, SJF, Round Robin, MLFQ) and the mechanics of context switching
- [The Little Book of Semaphores](https://greenteapress.com/wp/semaphores/) - a free, thorough treatment of mutexes, semaphores, and classic synchronization problems
- [Computer Systems: A Programmer's Perspective (CS:APP)](https://csapp.cs.cmu.edu/) - covers processes, context switching, and concurrent programming with threads
- ["Let's make PostgreSQL multi-threaded"](https://www.postgresql.org/message-id/31cc6df9-53fe-3cd9-af5b-ac0d801163f4@iki.fi) - the active mailing-list proposal to move Postgres from a multi-process to a multi-threaded architecture
- [PostgreSQL reconsiders its process-based model (LWN.net)](https://lwn.net/Articles/934940/) - good overview of the tradeoffs in that proposal
- [ARM TLB and ASID overview](https://developer.arm.com/documentation/102142/latest/) - background on how Address Space IDs let the TLB cache translations from multiple processes at once
