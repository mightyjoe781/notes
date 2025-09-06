## GSoC

This page documents the GSoC journey for the project that I will be doing with Warner Losh.

[Debug Notes](debug.md)

[Setup Notes](setup.md)

### Short Description

FreeBSD supports multiple architectures, file systems, and  disk-partitioning schemes. Currently, there is a script named  full-test.sh located in src/tools/boot/ that creates several of these  environments but does not test all of them. The proposed idea is to  rewrite the script in a language such as Python or Lua, which would  allow for testing of all the architecture combinations supported in the  first and second-tier support, and provide a report on any broken  combinations and expected functionality. Additionally, providing Linux  Boot support using Linux EFI shim(EDK) II for amd64 and arm64. If time  permits, further exploration could be done to integrate the script into  the existing build infrastructure (either Jenkins or Github Actions) to  generate a comprehensive summary of the test results.

### Design Discussion

- WIP [Need to write this section]

### Deliverables

- There exists one single main.lua script when invoked will test all  the possible arch-interface-file_system-encryption combination 
- Figuring out sane defaults for all config combination : Lots of Work \0-0/ :P 
- You could provide a config.lua to run custom tests rather than sane defaults 
- Try to integrate the script in the existing FreeBSD Infra (If time permits) 

### Important Dates

- May 29th: Start of coding 
    - You'll be doing this in the first week 
- June 5th: Week 2 
    - You plan to do this in the second week 
- July 10th - July 14th: Mid-term Evaluations #1 
- August 21st - August 28th: Final-term Evaluations #2 
- September 5th: End of coding (soft) 
    - You may wish to use this time to complete documentation etc 
- Nov 6th: End of coding (hard) 

### Weekly Check-in

- [Week 1 (29 May) ](week/week1.md)
    - Successfully deployed a FreeBSD server and established build sytem on Racknerd VPS
    - Acquired foundation knowledge of Lua programming and explored the design principles of the project, include module systems.
    - Deliberated and finalized the syntax for the project, as well as devised a robust approach to process user inputs effectively and efficiently.
- Week 2 (4 Jun)
    - Developed `combination.lua`, a script that computes and parses regex strings in the specified format: `<arch>-<file-system>-<boot-partition>-<encryption>`
    - Implemented `optparse` for the `main.lua` file, enabling efficient command-line option parsing and handling.
    - Created `parser.lua` to significantly improve accuracy of parsing of `input.conf` ensuring correct and reliable data extraction.
- [Week 3 (12 Jun)](week/week3.md)
    - Configured `ntfy` on Warner’s Server to enable seamless notifications for build events.
    - Successfully build the `freebsd-src` on the server, ensuring smooth and error-free process.

    - Established a streamlined development workflow, optimizing collaboration and productivity.
- Week 4 (19 Jun)
    - Successfully finalized the `build.lua` script, incorporating extensive design and significant rewrites of the previous code.
    - Achieved comprehensive functionality through careful planning and meticulous execution.
- [Week 5 (26 Jun)](week/week5.md)
    - Successfully configured luarocks on FreeBSD Server.

    - Conducted a smoke test on the “amd64:amd64-gpt-ufs-none” architecture combination to ensure smooth functionality.


- Week 6 (3 July)
    - Wrote `test.lua` script, ensuring its successful design and completion.
    - Evaluated and streamlines the consicise reporting process for all build runs.
    - substantially progressed with the coding tasks, meeting expected milestones.
- Week 7 (10 July) - MidTerm Evaluations [Week Off Work]
- Week 8 (17 July)

    - Enhacned code styling and resolved potential design issues to improve overall script.
    - Conducted in-depth testing to ensure robutstness of script and addressing several small issues.

- [Week 9 (24 July)](week/week9.md)
    - Start working on externalising as much as freebsd related stuff to a `freebsd-util` script while generalising the functionality of `build` script.
    - Above decision will allow me to easily integrate support for all remaining architectures.
    - Start working on collecting qemu recipes for different architectures.
  
- Week 10 (31 July)

    - first script end to end works correct

- Week 11 (7 Aug)

    - all amd64 combination work correctly
    - encountered issues in running arm64 on qemu Synchronous Exception Faults

- Week 12 (14 Aug)

    - fixing up issues in various parts of the script
    - fixing a critical overwrite flaw in the script

- Week 13 (21 Aug) - Final Evaluations

    - all arm64 combination work correctly


Extension for 4 weeks


- Week 14 (28 Aug)

    - trying to get the riscv64 boot up using openSBI
- Week 15 (4 Sept)

    - riscv64-zfs-gpt-none(encryption) & riscv64-ufs-gpt-none(encryption) works fine and builds successfully.
- Week 16 (11 Sept)

    - blocked due to not able to get the arm sd image to extract correctly
    - consulted with kyle evans with suggestion to look at mounting the partitions of image
- Week 17 (18 Sept) [Kinda Busy week]
- Week 18 (25 Sept)

    - will work on creating a custom image for arm image and host it somewhere.

### Meeting Notes

- ̛amd64 -> aarch64 -> riscv (gpt only ufs/zfs with opens) -> armv7(ufs with gpt/mbr works, check for zfs) -> powerpc64 (ufs/zfs on openfirmware) -> i386 -> powerpc32

### Important Links

- Github : [Link](https://github.com/mightyjoe781/freebsd-src/tree/bootloader-smk)