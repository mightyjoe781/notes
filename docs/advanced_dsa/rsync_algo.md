# Rsync Algorithm
*Delta based file synchronization*

Often people confuse this with Merkle Trees, which in reality both serve different purpose.

Merkle Trees actually compute difference or prove integrity quickly but Rsync is more about efficiently copying changed file.

So often they work in conjunction, not alternatives of each other.

*rsync answers: “How do I transform file A into file B with minimal bytes?”*
*It computes a delta patch using rolling checksums.*

File Systems like ZFS *send/receive* combines both ideas.

More can be read here [Link](https://rsync.samba.org/tech_report/)

