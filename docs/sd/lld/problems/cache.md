# Design LRU Cache

## Requirements

- `get(key)` → return value if present, move to MRU position, else return `None`
- `put(key, value)` → insert/update; if at capacity, evict the LRU item first
- Fixed capacity set at init
- Thread-safe for concurrent reads/writes
- Both operations O(1)

## Core Insight: Why DLL + HashMap

A plain list or dict alone can't give you O(1) on both axes:

|Structure|get|put / evict|
|---|---|---|
|Dict only|O(1)|O(n) to find LRU|
|List only|O(n) to find key|O(1) evict from tail|
|**DLL + HashMap**|**O(1)**|**O(1)**|

The HashMap gives you O(1) node lookup. The DLL gives you O(1) reordering and eviction. They're useless without each other here.

## Class Structure

Three classes: `Node`, `DLL`, `LRUCache`.

**Node** is just a container - key + value + two pointers. Keep the key on the node because when you evict the tail, you need to delete from the map, and you can't do that without the key.

**DLL** manages the sentinel head/tail pattern - head = most recent, tail = least recent. Sentinels eliminate all the null-check edge cases in pointer manipulation.


![](assets/Pasted%20image%2020251214184402.png)

### DLL Internals

Initial state and after insertions:

![](assets/Pasted%20image%2020251214185517.png)

All four DLL operations are O(1) - they only touch adjacent pointers. 

The one piece that _would_ be O(n) is "find the node to reorder" - that's exactly what the HashMap in `LRUCache` solves.

- **`add_first(node)`** - splice after HEAD  
- **`remove(node)`** - unlink from wherever it sits (needs both prev/next valid, hence sentinels)  
- **`move_to_front(node)`** - remove + add_first (every GET does this)  
- **`remove_last()`** - unlink `tail.prev` and return it (eviction path in PUT)

### LRUCache

Fields: `size: int`, `map: dict[key → Node]`, `dll: DLL`, `lock: threading.Lock`

**`get(key)`**: check map → move_to_front → return value  
**`put(key, value)`**:

- Key exists: update value in-place, move_to_front
- Key new + at capacity: remove_last from DLL, delete that key from map, then insert new
- Key new + under capacity: just insert

**`remove(key)`**: unlink from DLL, delete from map

![](assets/Pasted%20image%2020251214185629.png)

#### Thread Safety

A single `threading.Lock` guarding the entire operation is correct here - both get and put do two things atomically (map access + DLL reorder). A read-write lock won't help much because even `get` mutates the DLL.

> **Important missing detail**: The `lock` and `dll` fields shouldn't be inside `@dataclass` without `field(default_factory=...)`. Both are class-level instances - if declared as bare class variables (not instance fields), all instances share the same DLL and lock. In the code below, `dll` and `lock` are defined outside `__post_init__` which is a subtle bug. Fix: use `__post_init__` or `field(default_factory=DLL)` pattern.

## Design Extension Point

The problem hints at this: if you need multiple eviction policies (LRU, LFU, MRU, etc.), define a `CachePolicy` Protocol:

```python
class CachePolicy(Protocol):
    def get(self, key: Hashable) -> object | None: ...
    def put(self, key: Hashable, value: object) -> None: ...
    def remove(self, key: Hashable) -> None: ...
```

`LRUCache`, `LFUCache`, etc. implement this. The caller holds a `CachePolicy` reference and never knows which strategy it's using.

## Python Supplement


```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Hashable, Protocol
import threading


# --- Protocol for extensibility (if multi-policy needed) ---
class CachePolicy(Protocol):
    def get(self, key: Hashable) -> object | None: ...
    def put(self, key: Hashable, value: object) -> None: ...


# --- Node: store key too, needed when evicting from DLL back to map ---
@dataclass
class Node:
    key: Hashable
    value: object
    prev: Node | None = field(default=None, repr=False)
    next: Node | None = field(default=None, repr=False)


# --- DLL: sentinel head/tail eliminates all null-check edge cases ---
class DLL:
    def __init__(self) -> None:
        self.head = Node(None, None)   # MRU sentinel
        self.tail = Node(None, None)   # LRU sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_first(self, node: Node) -> None:
        """Splice node right after HEAD (mark as most recently used)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node   # order matters: fix forward link first
        self.head.next = node

    def remove(self, node: Node) -> None:
        """Unlink node; sentinels mean prev/next are always valid."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_to_front(self, node: Node) -> None:
        self.remove(node)
        self.add_first(node)

    def remove_last(self) -> Node | None:
        """Evict LRU node; return None if list is empty (only sentinels)."""
        if self.tail.prev is self.head:
            return None
        last = self.tail.prev
        self.remove(last)
        return last


# --- The tricky part: dll and lock must be per-instance, not class-level ---
@dataclass
class LRUCache:
    capacity: int
    _map: dict[Hashable, Node] = field(default_factory=dict, init=False)
    _dll: DLL = field(default_factory=DLL, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def get(self, key: Hashable) -> object | None:
        with self._lock:
            if (node := self._map.get(key)) is None:
                return None
            self._dll.move_to_front(node)
            return node.value

    def put(self, key: Hashable, value: object) -> None:
        with self._lock:
            if key in self._map:
                node = self._map[key]
                node.value = value
                self._dll.move_to_front(node)
            else:
                if len(self._map) == self.capacity:
                    evicted = self._dll.remove_last()
                    if evicted:
                        del self._map[evicted.key]  # why we store key on Node
                new_node = Node(key, value)
                self._dll.add_first(new_node)
                self._map[key] = new_node

# Deliberately left as exercise:
# - LFUCache using the same CachePolicy Protocol
# - TTL expiry (hint: store timestamp on Node, lazy eviction on get)
# - Async variant with asyncio.Lock
```

---
## Further Reading & Exercises

### Directly Relevant

- _Designing Data-Intensive Applications_ - Chapter 11 (caching patterns, eviction policies in distributed systems context)
- Python `functools.lru_cache` source - see how the stdlib does it with a circular DLL in pure Python: [https://github.com/python/cpython/blob/main/Lib/functools.py](https://github.com/python/cpython/blob/main/Lib/functools.py)
- Python threading docs - Lock vs RLock vs Semaphore tradeoffs: [https://docs.python.org/3/library/threading.html](https://docs.python.org/3/library/threading.html)
- _Introduction to Algorithms (CLRS)_ - Chapter 10 (linked list operations, sentinel nodes)
- "Caching at Scale" - Meta engineering blog on how LRU variants work in Memcached/TAO

### Exercises

**Easy** - Add a `peek(key)` method that returns the value without updating recency. Does the lock strategy change?

**Medium** - Add TTL support. Each entry expires after `ttl_seconds`. Decide: do you expire eagerly (background thread) or lazily (on access)? Implement lazy expiry first. Where does the expiry timestamp live?

**Hard (design decision, no single right answer)** - Implement `LFUCache` using the same `CachePolicy` Protocol. LFU needs to track access frequency AND recency within the same frequency bucket. Two reasonable designs: (a) a min-heap of `(frequency, last_access_time, key)` tuples, or (b) a hashmap of frequency → DLL of nodes at that frequency. Argue which is better for your workload. What's the time complexity of each?

### Related Problems

- **LFU Cache** - same HashMap+DLL skeleton, but you need a second map from frequency → DLL bucket; the core challenge transfers directly
- **Design a Cache with TTL (Expiring Map)** - same eviction logic, adds a time dimension; forces you to decide where the clock lives
- **Thread-Safe Bounded Queue** - same pattern of "lock wraps a compound data structure mutation"; identical reasoning about why you can't split read and write into separate locks

### Connection to HLD

- **CDN / Edge Cache design** - LRU is the local eviction policy inside each PoP node; the HLD problem is about which PoP to route to and how to handle cache misses cascading to origin
- **Database Buffer Pool** (e.g., InnoDB) - buffer pool uses a variant of LRU with a "young/old" split to prevent full-table scans from flushing hot pages; same core structure, smarter eviction heuristic
- **Distributed Cache (Redis/Memcached)** - at HLD level you're partitioning keys across nodes (consistent hashing); at node level, each shard runs its own LRU eviction