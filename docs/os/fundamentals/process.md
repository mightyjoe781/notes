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

NOTE : Here `c=4` will be put in stack, 

- Fetch Load Execute cycle.

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

# ideally you should set breakpoint before exectuing using start
# info registers to validate binary

```

## The Stack



## Resources

- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/3_Processes.html
- Cost Times
    - Register Access - 1ns
    - L1 Cache - 2ns
    - L2 Cache - 7ns
    - L3 Cache - 15ns
    - Main Memory - 100ns
    - SSD - 150 us
    - HDD - 10 ms