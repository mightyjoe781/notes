# Os Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: os
This is part 1 of 1 parts

---

## File: os/ch1.md

# Introduction

If application programmers had to understand the detailed workings of every hardware component attached to a modern computer and manage these components while using them optimally, no code would ever be written.

For this reason, every computer includes a layer of software called the operating system. It provides a simpler, cleaner model of the computer and manages all resources.

The program with which users interact is called the shell when it is text-based and the graphical user interface (GUI) when it is graphical. Note that the GUI is not part of the operating system, although it relies on the operating system to function.

Operating System runs in two modes.

- Kernel mode : It has complete access to all hardware and can execute any instruction the machine is capable of executing.

- User mode : In this mode subset machine instruction is available. control instruction which directly affect I/O are strictly forbidden.

Major examples of OS are Windows, Linux, FreeBSD and OS X.

Operating systems are huge, complex and long-lived. They are very hard to write and having written one, the owner is loath to throw it out and start again.

### What is an Operating System ?

The architecture (instruction set, memory organization, i/o, and bus structure) of most coputer at machine-language level is primitive and awkward to program, especially I/O.

Instead **disk driver**, deals with harware and provides an interface to read and write disk blocks, without getting into the details. OS contains many drivers for controlling I/O devices.

This abstraction is the key to managing all this complexity. Good abstractions turn a nearly impossible task into two manageables ones. The first defining and implementing the abstractions. The second is using these abstraction to solve the problem at hand.

Operating system's real customers are the application programmers because it hides different hardware implementation and provides a good application programmer.

**OS as a Resource Manager**

Resource management includes multiplexing (sharing) resources in two different ways : in time and in space. When a resource is time multiplexed, different programs or users take turn using it. Deciding which program to given resource and for how long is the one of the prime tasks of Operating System.

The second kind of multiplexing is space multiplexing. Instead of the customers taking turns, each one gets part of the resource. For e.g. main memory of the computer is divided up among several running programs, so each one can be resident at the same time. This is not as simple task as it seems there are many caveats like fairness, protection and so on.

### History of Operating System

Take the following section as a guide not as a last world.

The first true digital computer was designed by the English mathematician Charge Babbage (1792-1871). Although most of his time was spent developing Analytical Engine which he never got it working properly cause it was purely mechanical and the technology of his day could not produce required wheels, gears and cogs to high precision that he needed. Analytical Engine didn’t had an OS :P

- The First Generation (1945-55) : Vaccum Tubes

  Soon after World War II, lot of Universities started building their own digital computers, some were binary, some used vaccum tubes, some were programmable, but very primitive and took lot of time to do simplest calculation. In these early days a single group of people designed, built, programmed, operated and maintained each machine. All programming was done in absolute machine language or worse, by wiring up electrical circuits by connecting thousands of cables to plugboards. Operating Systems were unheard of.

- The Second Generation (1955-65) : Transistors and Batch Systems

- The Third Generation (1965-80) : ICs and Multiprogramming

- The Fourth Generation (1980-Present) : Personal Computers

- The Fifth Generation (1990-Present) : Mobile Computers

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


---

## File: os/index.md

### **OS**

- [Chapter 1. Introduction](ch1.md)



---

