# Design SplitWise

## Requirements

### Solution Requirements

- End-to-end working solution
- For storage, we have to maintain a DB (MySQL)
- We should be exposing REST APIs for interacting with the system

### Functional Requirements

- Users should be able to create group
- Users should be able to create or be part of an expense where other group members are involved
- To add an expense, we might equally split the expense among all, or there can be percentage based split
- Users are able to see the transactions required to be done for settling up a group
- Support for history
- Support for adding or removing users from group
- Users should be able to get all their expenses

NOTES:

- The problem to find min. number of txns to settle up is going to be NP hard problem
- We can have multiple solutions
- Solution # 1
    - sort all the people in order, A B C D.
    - Now A can ask B either to pay off extra or give back money and leave the group (on view).
    - Now problem is solving settlements for B C D
    - same continues until 2 people are left in the group with equal amount of money.
- Solution # 2 ~ reduce the number of txn, greedy solution
    - Find the person who needs to get the most, who has to pay most.
    - Maintain two heaps to divide all the people on basis of the amount owed.
    - Settling 1 person completely, then again we can match both heap.
- We can have a strategy pattern for different settlement strategies.

