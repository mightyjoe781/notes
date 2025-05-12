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