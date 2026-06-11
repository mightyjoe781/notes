# Introduction

If application programmers had to understand the detailed workings of every hardware component attached to a modern computer, and manage all of those components optimally themselves, no code would ever get written.

For this reason, every computer includes a layer of software called the **operating system**. It provides a simpler, cleaner model of the computer and manages all of its resources.

The program a user interacts with is called the **shell** when it's text-based, and the **graphical user interface (GUI)** when it's graphical. Note that the GUI itself is *not* part of the operating system, although it relies on the operating system to function.

The operating system runs in two privilege modes:

- **Kernel mode** - has complete access to all hardware and can execute any instruction the machine is capable of
- **User mode** - only a subset of machine instructions is available; instructions that directly affect I/O or other privileged hardware are strictly forbidden

Major examples of operating systems include Windows, Linux, FreeBSD, and macOS.

Operating systems are huge, complex, and long-lived. They are very hard to write, and once one has been written, its owner is loath to throw it out and start again - which is part of why decades-old design decisions still echo through modern systems.

### What is an Operating System ?

The architecture (instruction set, memory organization, I/O, and bus structure) of most computers, at the machine-language level, is primitive and awkward to program directly - especially I/O.

Instead, a **disk driver** deals with the hardware directly and provides a simple interface to read and write disk blocks, without exposing those low-level details. The OS contains many such drivers for controlling its I/O devices.

This kind of abstraction is the key to managing all this complexity. Good abstractions turn a nearly impossible task into two manageable ones: first, defining and implementing the abstraction; second, using that abstraction to solve the problem at hand.

The operating system's real "customers" are application programmers - it hides the differences between hardware implementations and gives programmers a clean, consistent platform to build on.

**OS as a Resource Manager**

Resource management means **multiplexing** (sharing) resources, in two different ways: in time, and in space.

- **Time multiplexing** - different programs or users take turns using a resource. Deciding *which* program gets the resource, and for how long, is one of the operating system's prime tasks (this is scheduling)
- **Space multiplexing** - instead of taking turns, each consumer gets *part* of the resource simultaneously. E.g. main memory is divided up among several running programs so each can be resident at the same time. This is not as simple as it sounds - there are many caveats around fairness, protection, and so on

### History of Operating System

Take the following section as a guide, not as the last word.

The first true digital computer was designed by the English mathematician Charles Babbage (1791-1871). Most of his time was spent developing the Analytical Engine, which he never got working properly - it was purely mechanical, and the technology of his day couldn't produce the wheels, gears, and cogs to the precision he needed. The Analytical Engine didn't have an operating system :P

- **The First Generation (1945-55) - Vacuum Tubes**

  Soon after World War II, a number of universities started building their own digital computers - some binary, some using vacuum tubes, some programmable, but all very primitive and slow even for the simplest calculations. In these early days, a single group of people designed, built, programmed, operated, and maintained each machine. All programming was done in absolute machine language, or worse, by wiring up electrical circuits via thousands of cables on plugboards. Operating systems were unheard of.

- **The Second Generation (1955-65) - Transistors and Batch Systems**

- **The Third Generation (1965-80) - ICs and Multiprogramming**

- **The Fourth Generation (1980-Present) - Personal Computers**

- **The Fifth Generation (1990-Present) - Mobile Computers**

### Computer Hardware Review



### The Operating System Zoo

### Operating System Concepts

### System Calls

### Operating System Structure

### World According to C

### Research on Operating Systems

### Outline of Rest of the Notes

### Metric Units

### Summary
