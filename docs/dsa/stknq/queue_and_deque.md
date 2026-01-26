# Queue & Deque Implementations

A Queue follows First-In First-Out (FIFO), while a Deque (Double-Ended Queue) allows insertion and removal from both ends.

**Basic Operation**

| **Queue**  | **Deque**                   |
| ---------- | --------------------------- |
| enqueue(x) | push_front(x), push_back(x) |
| dequeue()  | pop_front(), pop_back()     |
| peek()     | front(), back()             |
| isEmpty()  | empty()                     |

### Python

* Queue & Deque : `collections.deque`

````python
from collections import deque
q = deque()
q.append(x)      # enqueue
q.popleft()      # dequeue

dq = deque()
dq.appendleft(x) # push front
dq.append(x)     # push back
dq.pop()         # pop back
dq.popleft()     # pop front
````

### C++ STL

````cpp
#include <queue>
queue<int> q;
q.push(x);       // enqueue
q.pop();         // dequeue

#include <deque>
deque<int> dq;
dq.push_front(x);
dq.push_back(x);
dq.pop_front();
dq.pop_back();
````

## Applications

* Queues : OS Scheduling, BFS traversal, Buffers
* Deques: Sliding Window Problems, Palindrome Checks, Task Scheduler

### Problems

* Implement Queue Using Stacks (232) : Simulate a FIFO queue using two stacks
* Implement Stack Using Queues : Simulate a LIFO stack using 2 queues
* Circular Queue (622) : Implementation
* Double-Ended Queue : Implementation
* Reverse First K Elements of a Queue
* Task Scheduler
* Design Hit Counter
* Rotten Oranges
* LRU Cache