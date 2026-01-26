# Implementation Problems

Following problems often appear in design interviews due to application in wide range of scenarios in practical real-life.

## Sliding Window Maximum

Given an array nums and window of size k, return the max of each sliding window

Applications

* Real-time data analysis
* Maximum in Streaming Data
* Temperature Monitoring, Sensor logs

Key idea : Use a *Monotonic Deque*

- Values in `deque` are in *decreasing order*
- Front of `deque` = max of current window

````python

from collections import deque
def maxSlidingWindow(nums, k):
    dq, res = deque(), []
    
    for i in range(len(nums)):
        # remove out of window indices
        if dq and dq[0] <= i - k:
            dq.popleft()
        
        # maintain decreasing monotonic deque constraint
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # window formed
        if i >= k - 1:
            res.append(nums[dq[0]])
            
    return res

````

NOTE: Time complexity is $O(2n) \cong O(n)$
## Stock-Span Problem

Problem Link - 901 - [Link](https://leetcode.com/problems/online-stock-span/description/)

This is a straightforward problem similar to 739: Daily Temperature.

Push every pair of `<price, result>` to a stack, pop lower price from the stack and accumulate the count.

One price will be pushed once and popped once. So `2*N` times stack operation and `N` times calls.

```python

class StockSpanner:

    def __init__(self):
        self.stk = []
        

    def next(self, price: int) -> int:
        res = 1
        while self.stk and self.stk[-1][0] <= price:
            res += self.stk.pop()[1]
        self.stk.append([price, res])
        return res

```

## The Celebrity Problem

A celebrity is a person who is known by everyone else at the party but does not know anyone in return. Given a square matrix M of size N x N where `M[i][j]` is 1 if person i knows person j, and 0 otherwise, determine if there is a celebrity at the party. Return the index of the celebrity or -1 if no such person exists. 

This is very famous and standard problem.

![](assets/Pasted%20image%2020260112114454.png)


## LRU Cache

Properties of LRU Cache

- `GET(Key)` ~ return the value of key exists, else -1 & moves the accessed node top of LRU element tracking system because we just accessed it.
- `PUT(Key)` ~ updates the value if exists or else adds it given that space is present, if its not present then removes the LRU element at the end of the list

We need a data structure to quickly access the tail-head of the element. We could use a DLL, or `deque` for this purpose, but to serve $O(1)$ get queries we will need additional map.

In Python we can use OrderedDict as well, for this implementation.

```python

from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)  # Mark as recently used
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove LRU item

```

But in other languages or without using library we have to use this implementation.

```python

from dataclasses import dataclass, field
from typing import Optional

from models.node import Node


class DLL:
    def __init__(self):
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_first(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_to_front(self, node: Node) -> None:
        self.remove(node)
        self.add_first(node)

    def remove_last(self) -> Optional[Node]:
        if self.tail.prev == self.head:
            return None
        last: Node = self.tail.prev
        self.remove(last)
        return last


```


```python

# Thread Safe Cache

import threading
from dataclasses import dataclass, field
from typing import Dict, Hashable, Mapping, Optional

from models.dll import DLL
from models.node import Node


@dataclass
class LRUCache:
    size: int
    map: Dict[Hashable, Node] = field(default_factory=dict)
    dll = DLL()
    lock = threading.Lock()

    def get(self, key: Hashable) -> Optional[object]:
        with self.lock:
            if key not in self.map:
                return None
            node = self.map[key]
            self.dll.move_to_front(node)
            return node.value

    def put(self, key: Hashable, value: object) -> None:
        with self.lock:
            if key in self.map:
                node = self.map[key]
                node.value = value
                self.dll.move_to_front(node)
            else:
                if len(self.map) == self.size:
                    lru = self.dll.remove_last()
                    if lru is not None:
                        del self.map[lru.key]
                new_node = Node(key, value)
                self.dll.add_first(new_node)
                self.map[key] = new_node

    def remove(self, key: Hashable) -> None:
        with self.lock:
            if key not in self.map:
                return
            node = self.map[key]
            self.dll.remove(node)
            del self.map[key]


```

## LFU Cache

Important Features

- Evict Least frequently used element
- Order by frequency
- Multiple DLLs, one per frequency

Its a multi-dimensional problem, requiring frequency and recency

```python

@dataclass
class Node:
    key: object
    value: object
    freq: int = 1
    prev: Optional["Node"] = None
    next: Optional["Node"] = None
    
class DLL:
    def __init__(self):
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_first(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def remove_last(self):
        if self.tail.prev == self.head:
            return None
        last = self.tail.prev
        self.remove(last)
        return last

    def is_empty(self):
        return self.head.next == self.tail   


```


LFU Cache State

```python

import threading
from dataclasses import dataclass, field
from typing import Dict, Hashable, Optional

@dataclass
class LFUCache:
    capacity: int
    key_map: Dict[Hashable, Node] = field(default_factory=dict)
    freq_map: Dict[int, DLL] = field(default_factory=dict)
    min_freq: int = 0
    lock = threading.Lock()
    
    def get(self, key: Hashable) -> Optional[object]:
        with self.lock:
            if key not in self.key_map:
                return None

            node = self.key_map[key]
            self._increase_freq(node)
            return node.value
            
    def put(self, key: Hashable, value: object) -> None:
        if self.capacity == 0:
            return

        with self.lock:
            if key in self.key_map:
                node = self.key_map[key]
                node.value = value
                self._increase_freq(node)
                return

            if len(self.key_map) == self.capacity:
                self._evict()

            node = Node(key, value)
            self.key_map[key] = node

            self.freq_map.setdefault(1, DLL()).add_first(node)
            self.min_freq = 1
            
    def _increase_freq(self, node: Node):
        freq = node.freq
        self.freq_map[freq].remove(node)

        if freq == self.min_freq and self.freq_map[freq].is_empty():
            self.min_freq += 1

        node.freq += 1
        self.freq_map.setdefault(node.freq, DLL()).add_first(node)
        
    def _evict(self):
        dll = self.freq_map[self.min_freq]
        node = dll.remove_last()

        if node:
            del self.key_map[node.key]

```