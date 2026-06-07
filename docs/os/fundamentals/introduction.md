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


## Further reading

- [Google proposes shutdown changes to speed Linux reboots](https://www.phoronix.com/news/Google-Linux-Too-Many-NVMe) - the NVMe synchronous-shutdown bug mentioned above, and how Google fixed it
- [CFS: Completely fair process scheduling in Linux](https://opensource.com/article/19/2/fair-scheduling-linux) - a good accessible look at how Linux's default scheduler tries to give every process its fair share of CPU time
- [CPython Reference Counting and Garbage Collection Internals](https://blog.codingconfessions.com/p/cpython-garbage-collection-internals) - covers the `None` refcount story above and how CPython 3.12+ made it (and a few others) "immortal" to cut the overhead