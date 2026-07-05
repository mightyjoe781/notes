---
title: Process
description: How a process is laid out in memory - program vs process, the stack (frames, base/stack pointers, return addresses), the data section, the heap, pointers, and memory leaks.
tags:
  - concept
---

# Process

It is important to be aware that in reality we don't really need OS, in-fact some of the low-latency application directly communicate with Kernel.

## Program vs Process

Program ~ often actual executive on the file-system with extension, and when the program is executed we call it a process.

Simply, Process is a program in motion.

**Program**

- Code is compiled and linked for a CPU
    - Compiling is generating object files for a specific CPU from source code.
    - There are two types of linking : Static, Dynamic.
    - mold linker
- Produces executable file program
- Only works on that CPU architecture
- At rest it follows an executable file format
- Lives on Disk


![236](assets/Pasted%20image%2020260609212218.png)

![ELF File Example](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/ELF_Executable_and_Linkable_Format_diagram_by_Ange_Albertini.png/1280px-ELF_Executable_and_Linkable_Format_diagram_by_Ange_Albertini.png)

**Process**

- Stack Grows down, and heap grows up
- When a program is run, we get a process
- Process lives in Memory
- Uniquely identified with an id and scoped to the namespace
- Instruction pointer/program counter
- Process Control Block (PCB) ~ metadata about the actual process, tells about the pointers, page tables, id, etc. Reading from PCB is cheap, but writing is costly.
    - Process State ~ Running, waiting, etc
    - Process ID, and parent ID
    - CPU registers & Program Counter. (Saved/Restored when swapping process out of CPU)
    - CPU Scheduling Information
    - Memory-Management Information
    - Accounting Information
    - I/O Status Information

Example : Program vs Process

![399](assets/Pasted%20image%2020260609214105.png)

Producing Machine Code

![415](assets/Pasted%20image%2020260609214210.png)

| Process In Memory                                                                                                        | Program Example                                    |
| ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| ![Process in Memory](https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/images/Chapter3/3_01_Process_Memory.jpg) | ![423](assets/Pasted%20image%2020260609225832.png) |

NOTE : A local variable like `c=4` lives in the stack segment.

- The CPU runs instructions via the **fetch-decode-execute cycle**: fetch the instruction at the address in the program counter, decode it, execute it, then advance the program counter.

### State of a Process

![Diagram of Process State](https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/images/Chapter3/3_02_ProcessState.jpg)

### Demo

- Create a process & Use GNU Debugger to investigate it.

```bash

uname -S # Kernel Name
uname -a

vim test.c # use the above code
gcc -S test.c -o test.s # default is machine code

cat test.s # assembly code

gcc -g test.c -o test # symbols

gdb test

# ideally you should set a breakpoint before executing, using `start`
# `info registers` to inspect register values

```

## The Stack

![278](assets/Pasted%20image%2020260610100435.png)

- Each function call gets its own **frame** (also called an activation record) on the stack, holding that function's local variables
- The active function is the one whose frame is at the top of the stack (`function3`, here, since it was called last)
- The stack grows from high memory addresses down to low memory addresses
- Stack space is limited (and fixed per-thread) - deep/unbounded recursion causes a *stack overflow*

**Stack Pointer**

![](assets/Pasted%20image%2020260610101058.png)

- The Stack Pointer (SP) is a CPU register that always points to the top (lowest address) of the stack
- **Allocating** space (pushing) moves SP to a *lower* address
- **Deallocating** space (popping) moves SP back to a *higher* address
- Popping doesn't erase or zero out the old data - it's simply left behind in memory until something else is pushed and overwrites it. There's no garbage collector for the stack; the moving SP is the only thing that marks what's "valid"

**Base Pointer**

![436](assets/Pasted%20image%2020260610101416.png)

- SP keeps moving as a function pushes/pops temporaries, so it's not a stable way to refer to a local variable
- The Base Pointer (BP), aka the Frame Pointer, is a second CPU register that stays fixed for the lifetime of a function's frame, giving a stable reference point
- Variables are then addressed as offsets from BP, e.g. `a` is at `bp`, `b` is at `bp-4`, `c` is at `bp-8`

**Nested Calls**

![476](assets/Pasted%20image%2020260610101535.png)

When `main` calls `func1`:

- `main` pauses, and `func1` becomes the active frame - both `bp` and `sp` move to point into `func1`'s frame
- When `func1` returns, `sp` moves back up by the size of `func1`'s frame (here, 8 bytes for `x` and `y`), freeing that space
- `bp` also needs to move back to where it was for `main` - but where was that? `bp` itself doesn't remember its old value, so it must be saved somewhere before being overwritten

This is solved by saving the old `bp` on the stack itself, as part of the new frame:

![453](assets/Pasted%20image%2020260610102015.png)

1. `main` calls `func1`
2. The CPU allocates `func1`'s frame by moving `sp` down (here `bp`, `x`, and `y` together need 12 bytes)
3. The *old* `bp` (still pointing at `main`'s frame) is pushed onto the stack first
4. `bp` is now safely updated to point at the start of `func1`'s frame
5. `func1` runs using `x` and `y`, addressed relative to the new `bp`
6. When `func1` returns: read the saved old `bp` value back into `bp` (restoring `main`'s frame pointer), then move `sp` back up by 12 bytes to deallocate `func1`'s frame
7. `main` is active again - but at what instruction should it resume?

**Return Address**

![397](assets/Pasted%20image%2020260610102225.png)

- Restoring `bp` tells the CPU *whose* frame is active again, but not *where in `main`'s code* to continue executing
- So, alongside the old `bp`, the **return address** - the address of the instruction in `main` right after the `call` to `func1` - is also pushed onto the stack when `func1` is called
- On return, this value is popped back into the Program Counter (PC), so execution resumes exactly where `main` left off
- On many architectures the return address is first placed in a dedicated **link register** by the `call` instruction, and only pushed onto the stack if `func1` itself needs to make further calls (otherwise it can return directly from the link register)
## Process Execution with Stack

**Stack Overflow**

- The stack has a fixed size limit, set per-process/per-thread (it can usually be raised via `ulimit -s` or compiler/linker flags, but not made unbounded)
- If too many frames pile up, the stack pointer runs past this limit and the program crashes with a stack overflow. Common causes:
    - Unbounded or infinite recursion (each call adds a new frame, with nothing to stop it)
    - Very large local variables (e.g. a huge array declared inside a function), which can overflow the stack even with shallow call depth

**Why this matters: function call overhead at scale**

Every function call has a real cost - pushing the return address and old `bp`, moving `sp`, and later restoring everything on return. This is usually negligible, but it adds up when a function is called millions of times per second in a hot path. In hot loops, "cleaner" code with many small layered function calls can trade real throughput for readability, unless the compiler can inline things back away.

## Data Section

![402](assets/Pasted%20image%2020260610150620.png)

The full layout of a process's address space, from low to high addresses: **Text/Code** (the program's instructions), **Data** (this section), **Heap**, and finally the **Stack** (growing downward from the top).

- Stores **global and static variables** - i.e. variables whose lifetime is the entire program, not tied to any single function's frame
- Has two parts:
    - Read-only (e.g. string literals, `const` globals)
    - Read-write (regular global/static variables)
- Fixed size, decided at compile/link time - just like the code section
- Accessible from all functions (unlike stack locals, which are scoped to their frame)
- Memory is generally fetched from RAM into cache in chunks (cache lines, commonly 64 bytes), not one variable at a time - so variables declared near each other are more likely to land in the same cache line and be "free" to access once the first one is fetched

Looking at the assembly for a program like this shows that fetching `A` actually pulls in `B` as well, since they sit next to each other in the data section within the same cache line:

```c
int A = 10;
int B = 20;

int main() {
    int C = A + B;
    return 0;
}
```

## The Heap

![343](assets/Pasted%20image%2020260610152114.png)

- Used for **dynamic allocation** - memory requested at runtime, whose size isn't known at compile time
- Grows from low addresses to high addresses (upward), opposite to the stack - so they grow toward each other
- Memory here persists until it's **explicitly freed** (or the process exits) - unlike stack memory, which is automatically reclaimed when a function returns
- Accessible from any function, as long as it has a pointer to it
- A program can't allocate heap memory itself - `malloc`, `free`, `new`, etc. are library calls that ultimately ask the kernel for memory (see Program Break, below)
- This is also where memory leaks happen, since nothing automatically reclaims it

### Pointers

![411](assets/Pasted%20image%2020260610152517.png)

- A pointer is just a variable that stores a memory **address** - the address of the first byte of whatever it points to
- A pointer itself can live anywhere - stack, data section, or heap - regardless of where the memory it *points to* lives
- The pointer's *type* (`int *`, `char *`, ...) tells the compiler how many bytes to read/write starting from that address

```c
#include <stdlib.h>

int main() {
    int *ptr = malloc(sizeof(int));

    *ptr = 10;
    *ptr += 1;
    free(ptr);

    return 0;
}
```

**Memory Leaks**

- A memory leak happens when heap memory is never freed and nothing points to it anymore, so it can't be freed either
- Common cause: the only pointer to a heap allocation lived in a stack variable, and that function returned without calling `free` - the pointer is gone, but the allocation isn't
- Languages address this differently:
    - C/C++: manual `malloc`/`free` (or RAII via destructors in C++)
    - Reference counting (e.g. CPython): free memory once its reference count hits zero
    - Garbage collection (e.g. Go, Java, JS): a separate process periodically finds and frees unreachable memory

**Dangling Pointers**

![356](assets/Pasted%20image%2020260610154044.png)

- A dangling pointer is a pointer that still holds the address of memory that has already been freed
- Using or freeing it again leads to undefined behavior - crashes, corruption, or (in security contexts) exploitable bugs
- In the diagram: `fun2` holds `*b = 0x333333`, frees that heap block, and returns. `fun1`'s `*a` still points at `0x333333` (the same, now-freed block) - if `fun1` reads through `*a` or calls `free(a)` again, that's a use-after-free / double-free

### Performance

- The stack has "free" memory management - allocation/deallocation is just moving `sp`, no bookkeeping needed
- Stack variables for a frame are allocated together and tend to be accessed together, which plays well with the CPU cache (good locality)
- The heap, by contrast, is effectively a pile of allocations made at arbitrary times and possibly scattered across memory - access patterns are far less predictable, so heap-heavy code tends to see more cache misses
- A common real-world optimization in performance-sensitive C code (e.g. kernel networking code, databases) is reordering struct fields so that fields accessed together are placed in the same cache line - shrinking the number of cache lines touched per operation

**Escape Analysis**

- A compiler optimization where the compiler proves a value never "escapes" the function it's created in (no pointer to it is returned or stored elsewhere)
- If so, it can be allocated on the stack instead of the heap, even though it was written as if it were heap-allocated - avoiding allocation overhead and GC pressure entirely
- Used by Go and the JVM (Java)

**Program Break**

- The "program break" (or "break") is the address marking the current end of the heap (the boundary between the heap and unmapped memory)
- `brk()` / `sbrk()` are the system calls that move this boundary up or down - this is how the heap actually grows or shrinks
- `malloc`/`free` are typically implemented on top of `brk`/`sbrk` (or `mmap` for very large allocations) - they manage a pool of memory obtained this way and hand out chunks of it

## Resources

- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/3_Processes.html
- [Operating Systems: Three Easy Pieces - Process chapters](https://pages.cs.wisc.edu/~remzi/OSTEP/) - free textbook covering processes, the process API, and limited direct execution
- [cpu.land - Putting the "You" in CPU](https://cpu.land/) - an excellent walkthrough of what happens when a program runs: processes, the stack, syscalls, and scheduling
- [Computer Systems: A Programmer's Perspective (CS:APP) - "Bryant & O'Hallaron"](https://csapp.cs.cmu.edu/) - the canonical reference for how programs are translated, linked, and executed, including the stack/heap/data layout covered above
- [x86 Disassembly / Calling Conventions - Wikibooks](https://en.wikibooks.org/wiki/X86_Disassembly/Calling_Conventions) - details on stack frames, `bp`/`sp`, and return addresses across architectures
- Cost Times
    - Register Access - 1ns
    - L1 Cache - 2ns
    - L2 Cache - 7ns
    - L3 Cache - 15ns
    - Main Memory - 100ns
    - SSD - 150 us
    - HDD - 10 ms