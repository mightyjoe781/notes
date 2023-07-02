## GSoC

This page documents the GSoC journey for the project that I will be doing with Warner Losh.

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
  - Setup freebsd server and build systems on Racknerd VPS
  - Read basics of lua and design of the project (module systems)
  - Decide the syntax and how to process inputs from users
- Week 2 (4 Jun)
  - Write combination.lua which calculates and parses regex strings in format : `<arch>-<file-system>-<boot-partition>-<encryption>`
  - Write `optparse` for the `main.lua` file
  - Write `parser.lua` for parsing the `input.conf` more correctly
- [Week 3 (12 Jun)](week/week3.md)

  - Setup ntfy on Warner’s Server
  - Build freebsd-src tree on server

  - setup development workflow
- Week 4 (19 Jun)
  - complete build.lua script
  - Above required a lot of designing and rewrite of previous script

- Week 5 (26 Jun) [WIP]
  - Smoke test for at least one of architecture combo : amd64:amd64-gpt-ufs-none


- Week 6 (3 July)
  - design and complete test.lua script.
  - review how to concisely report all build runs.
  - A reasonable amount of coding part should be done by now
- Week 7 (10 July) - MidTerm Evaluations
- Week 8 (17 July)
- Week 9 (24 July)
- Week 10 (31 July)
- Week 11 (7 Aug)
- Week 12 (14 Aug)
- Week 13 (21 Aug) - Final Evaluations

### Important Links

- Github : [Link](https://github.com/mightyjoe781/freebsd-src/tree/bootloader-smk)