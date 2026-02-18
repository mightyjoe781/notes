# Rsync Algorithm
*Delta based file synchronization*

Often people confuse this with Merkle Trees, which in reality both serve different purpose.

Merkle Trees actually compute difference or prove integrity quickly but Rsync is more about efficiently copying changed file.

So often they work in conjunction, not alternatives of each other.

*rsync answers: “How do I transform file A into file B with minimal bytes?”*
*It computes a delta patch using rolling checksums.*

File Systems like ZFS *send/receive* combines both ideas.

More can be read here [Link](https://rsync.samba.org/tech_report/)
Good Explanation for the algorithm Here : [Youtube video](https://www.youtube.com/watch?v=X3Stha8pxXc)

The rsync algorithm efficiently computes which parts of a source file match some part of an existing destination file. These parts need not be sent across the link; all that is needed is a reference to the part of the destination file. Only parts of the source file which are not matched in this way need to be sent verbatim. The receiver can then construct a copy of the source file using the references to parts of the existing destination file and the verbatim material.

