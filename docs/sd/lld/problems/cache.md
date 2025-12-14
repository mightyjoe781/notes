# Design a LRU Cache

## Requirements

- The LRU cache should support the following operations:
    - put(key, value): Insert a key-value pair into the cache. If the cache is at capacity, remove the least recently used item before inserting the new item.
    - get(key): Get the value associated with the given key. If the key exists in the cache, move it to the front of the cache (most recently used) and return its value. If the key does not exist, return -1.
- The cache should have a fixed capacity, specified during initialization.
- The cache should be thread-safe, allowing concurrent access from multiple threads.
- The cache should be efficient in terms of time complexity for both put and get operations, ideally $O(1)$.

## Class Diagram

- Implementing a cache with property of LRU (Least Recently Used) requires implementing a DLL (Doubly Linked List)
- Usually a list/map is not a cut out for this, if you try to optimize `put` operation then your `get` will become expensive and vice-versa
- For implementing this we will have two structures : *Node* and *DLL*, both will be used by *Cache* class which will be implementing the main program for us to use.
- Note : This problem could be extended by providing multiple caching policies like LFU, LRU, etc. In such scenarios we should declare an interface for *Cache* and implement multiple caching strategies for such cache class.

![](assets/Pasted%20image%2020251214184402.png)

![](assets/Pasted%20image%2020251214185517.png)

- Cache class could look like following : 

![](assets/Pasted%20image%2020251214185629.png)

Example Code Snippets for above classes

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    key: Any
    value: Any
    prev: Node | None = field(default=None)
    next: Node | None = field(default=None)

```

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

```python lru_cache.py
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


~ Driver Class to validate functionality

```python
from lru_cache import LRUCache


class LRUCacheDemo:
    @staticmethod
    def main():
        cache = LRUCache(3)

        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        # Accessing 'a' makes it the most recently used
        print(cache.get("a"))  # 1

        # Adding 'd' will cause 'b' (the current LRU item) to be evicted
        cache.put("d", 4)

        # Trying to get 'b' should now return None
        print(cache.get("b"))  # None


if __name__ == "__main__":
    LRUCacheDemo.main()
```