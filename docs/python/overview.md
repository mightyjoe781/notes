# Python Libraries Overview

Quick reference for Python's built-in data structure and algorithm libraries. Each section covers the most useful tools with the key patterns you'll reach for most often.

---

## `collections` - Specialized Container Types

[Documentation](https://docs.python.org/3/library/collections.html)

| Type | Use case |
|---|---|
| `deque` | O(1) append/pop from both ends; bounded buffer |
| `Counter` | Multiset / frequency counting |
| `defaultdict` | Dict that auto-creates missing keys |
| `OrderedDict` | Dict with order-aware equality and `move_to_end` |
| `namedtuple` | Lightweight immutable record with named fields |
| `ChainMap` | Layered lookup across multiple dicts (scope chains) |
| `UserDict` / `UserList` | Safe base classes when subclassing dict/list |

```python
from collections import deque, Counter, defaultdict, namedtuple

# deque as a bounded recent-items buffer
buf = deque(maxlen=5)
buf.extend(range(10))   # keeps [5, 6, 7, 8, 9]

# Counter
freq = Counter("abracadabra")
freq.most_common(3)     # [('a', 5), ('b', 2), ('r', 2)]

# defaultdict - no KeyError on missing keys
graph = defaultdict(list)
graph['a'].append('b')

# namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
p.x, p._asdict()
```

---

## `heapq` - Min-Heap Priority Queue

[Documentation](https://docs.python.org/3/library/heapq.html)

Python's heap is a **min-heap** implemented as a plain list. For a max-heap, negate values.

```python
import heapq

heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
heapq.heappop(heap)         # 1

# k smallest / largest
heapq.nsmallest(3, [5, 1, 4, 2, 3])   # [1, 2, 3]
heapq.nlargest(2, [5, 1, 4, 2, 3])    # [5, 4]

# heapify in-place: O(n)
data = [5, 1, 4, 2, 3]
heapq.heapify(data)

# Priority queue pattern: (priority, item)
tasks = []
heapq.heappush(tasks, (2, 'low priority'))
heapq.heappush(tasks, (1, 'high priority'))
heapq.heappop(tasks)  # (1, 'high priority')
```

---

## `bisect` - Sorted List Binary Search

[Documentation](https://docs.python.org/3/library/bisect.html)

Maintains a sorted list in O(log n) search + O(n) insert. Use when you need a sorted sequence with infrequent inserts.

```python
import bisect

nums = [1, 3, 5, 7, 9]
bisect.bisect_left(nums, 5)     # 2  - index where 5 would be inserted (leftmost)
bisect.bisect_right(nums, 5)    # 3  - index after existing 5s

bisect.insort(nums, 4)          # insert 4 in sorted order -> [1, 3, 4, 5, 7, 9]

# Grade lookup pattern
breakpoints = [60, 70, 80, 90]
grades = 'FDCBA'
def grade(score):
    return grades[bisect.bisect(breakpoints, score)]

grade(55)   # 'F'
grade(85)   # 'B'
```

---

## `itertools` - Iterator Building Blocks

[Documentation](https://docs.python.org/3/library/itertools.html)

All return lazy iterators. Combine them to build efficient pipelines without materializing intermediate lists.

### Infinite iterators

| Function | Description |
|---|---|
| `count(start, step)` | 0, 1, 2, … (unbounded) |
| `cycle(it)` | Repeats iterable indefinitely |
| `repeat(x, n)` | Repeats `x` exactly `n` times (or forever) |

### Filtering / slicing

| Function | Description |
|---|---|
| `islice(it, stop)` | Lazy slice |
| `takewhile(pred, it)` | Yield while predicate is true |
| `dropwhile(pred, it)` | Skip while predicate is true, then yield rest |
| `filterfalse(pred, it)` | Yield items where predicate is false |
| `compress(it, selectors)` | Yield items where selector is truthy |

### Combining

| Function | Description |
|---|---|
| `chain(*its)` | Concatenate iterables |
| `chain.from_iterable(it)` | Flatten one level |
| `zip_longest(*its, fillvalue)` | Zip, padding shorter iterables |
| `product(*its, repeat)` | Cartesian product |
| `permutations(it, r)` | All r-length permutations |
| `combinations(it, r)` | All r-length combinations (no repeat) |
| `combinations_with_replacement(it, r)` | Combinations with repeat |
| `pairwise(it)` | Successive overlapping pairs (3.10+) |

### Aggregating

| Function | Description |
|---|---|
| `accumulate(it, func)` | Running totals (or any binary func) |
| `groupby(it, key)` | Group consecutive elements by key |
| `starmap(func, it)` | `map` where each item is unpacked as args |
| `tee(it, n)` | Split one iterator into n independent iterators |

```python
import itertools, operator

# Running sum, min, max
list(itertools.accumulate([3, 1, 4, 1, 5], operator.add))   # [3, 4, 8, 9, 14]
list(itertools.accumulate([3, 1, 4, 1, 5], min))             # [3, 1, 1, 1, 1]

# Flatten nested list
nested = [[1, 2], [3, 4], [5]]
list(itertools.chain.from_iterable(nested))                  # [1, 2, 3, 4, 5]

# Cartesian product
list(itertools.product('AB', repeat=2))  # [('A','A'),('A','B'),('B','A'),('B','B')]

# groupby - input MUST be sorted by key
data = sorted([('a', 1), ('b', 2), ('a', 3)], key=lambda x: x[0])
for k, g in itertools.groupby(data, key=lambda x: x[0]):
    print(k, list(g))
```

---

## `functools` - Higher-Order Functions

[Documentation](https://docs.python.org/3/library/functools.html)

| Tool | Description |
|---|---|
| `lru_cache(maxsize)` | Memoize function results; `maxsize=None` for unbounded |
| `cache` | Unbounded `lru_cache` (3.9+) |
| `cached_property` | Lazy property cached in instance dict |
| `reduce(func, it, init)` | Left fold over iterable |
| `partial(func, *args)` | Freeze some arguments of a function |
| `total_ordering` | Auto-fill comparison methods from `__eq__` + one of `__lt__/le/gt/ge` |
| `singledispatch` | Function overloading based on first argument type |

```python
from functools import lru_cache, reduce, partial
import operator

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

# reduce
reduce(operator.mul, range(1, 6))   # 120 (5!)

# partial
double = partial(operator.mul, 2)
double(7)   # 14
```

---

## `array` - Typed Compact Sequences

[Documentation](https://docs.python.org/3/library/array.html)

Use instead of `list` when storing millions of uniform numeric values. Stores values directly (not references), so far more memory-efficient.

```python
from array import array
from random import random

# 'd' = double (float64), 'i' = signed int, 'B' = unsigned byte
floats = array('d', (random() for _ in range(10**6)))

# Fast binary file I/O
with open('data.bin', 'wb') as f:
    floats.tofile(f)

floats2 = array('d')
with open('data.bin', 'rb') as f:
    floats2.fromfile(f, 10**6)
```

Common typecodes: `'b'` int8, `'B'` uint8, `'h'` int16, `'i'` int32, `'l'` int64, `'f'` float32, `'d'` float64.

---

## `queue` - Thread-Safe Queues

[Documentation](https://docs.python.org/3/library/queue.html)

| Class | Description |
|---|---|
| `Queue(maxsize)` | FIFO; blocks when full/empty |
| `LifoQueue(maxsize)` | LIFO (stack) |
| `PriorityQueue(maxsize)` | Min-heap priority queue |
| `SimpleQueue` | Unbounded FIFO; no `task_done`/`join` |

```python
from queue import PriorityQueue

pq = PriorityQueue()
pq.put((2, 'medium'))
pq.put((1, 'high'))
pq.put((3, 'low'))
pq.get()    # (1, 'high')
```

---

## `math` - Mathematical Functions

[Documentation](https://docs.python.org/3/library/math.html)

```python
import math

math.isqrt(17)          # 4  - integer square root (fast primality testing)
math.gcd(12, 8)         # 4
math.lcm(4, 6)          # 12  (3.9+)
math.comb(10, 3)        # 120 - C(n, k)
math.perm(10, 3)        # 720 - P(n, k)
math.log2(1024)         # 10.0
math.floor / math.ceil
math.inf                # float infinity
math.fsum([0.1]*10)     # 1.0  - exact float sum
```

---

## `operator` - Operators as Functions

[Documentation](https://docs.python.org/3/library/operator.html)

Useful with `functools.reduce`, `itertools.starmap`, `sorted(key=...)`:

```python
from operator import add, mul, itemgetter, attrgetter, methodcaller

# itemgetter - fast key/index access (returns callable)
get_name = itemgetter('name')
get_name({'name': 'Alice', 'age': 30})  # 'Alice'

# sort list of tuples by index 1
data = [('b', 2), ('a', 1), ('c', 3)]
sorted(data, key=itemgetter(1))         # [('a',1), ('b',2), ('c',3)]

# attrgetter - for objects
from operator import attrgetter
sorted(people, key=attrgetter('last_name', 'first_name'))
```

---

## `sortedcontainers` - Fast Sorted Structures (3rd party)

[Documentation](https://grantjenks.com/docs/sortedcontainers/) · `pip install sortedcontainers`

Pure Python, ~10× faster than manual bisect maintenance. Essential when you need a mutable sorted collection.

| Class | Description |
|---|---|
| `SortedList` | Sorted list with O(log n) add/discard |
| `SortedDict` | Dict with keys iterable in sorted order |
| `SortedSet` | Set with sorted iteration |

```python
from sortedcontainers import SortedList

sl = SortedList([5, 1, 3, 2, 4])
sl.add(0)               # SortedList([0, 1, 2, 3, 4, 5])
sl.irange(2, 4)         # iterator over [2, 3, 4]
sl.bisect_left(3)       # 2
```
