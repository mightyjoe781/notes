# Python Standard Library for DSA

> These tricks are Python-specific. They don't change the algorithm - they remove boilerplate so you can focus on the logic.

## itertools

### product - grid neighbors, brute force enumeration

````python
from itertools import product

# 8-directional neighbors
for dx, dy in product([-1, 0, 1], repeat=2):
    if dx == dy == 0:
        continue

# All border cells of an m x n grid (for multi-source BFS)
from itertools import chain
for x, y in chain(
    product(range(m), [0, n-1]),
    product([0, m-1], range(1, n-1))
):
    queue.append((x, y))

# Brute force over 2^k binary choices
for choices in product([0, 1], repeat=k):
    ...
````

### chain - multi-source BFS, merging iterables

````python
from itertools import chain

# Seed BFS from multiple sources at once
for node in chain(boundary_nodes, special_nodes):
    queue.append(node)
````

### combinations / permutations - enumeration

````python
from itertools import combinations, permutations

for a, b in combinations(nums, 2):      # O(n^2) pairs, no repeats
    ...

for a, b, c in combinations(nums, 3):  # 3Sum brute force
    ...

for perm in permutations(chars):        # all orderings
    ...
````

### combinations_with_replacement - multisets

````python
from itertools import combinations_with_replacement

for combo in combinations_with_replacement(coins, k):
    if sum(combo) == target:
        ...
````

### accumulate - prefix sums, running aggregates

````python
from itertools import accumulate
import operator

prefix = list(accumulate(nums))                    # prefix sums
prefix_prod = list(accumulate(nums, operator.mul)) # prefix products
running_max = list(accumulate(nums, max))
````

### groupby - run-length encoding, interval grouping

````python
from itertools import groupby

# NOTE: input must be sorted first
for key, group in groupby("aaabbbcc"):
    print(key, len(list(group)))  # a 3, b 3, c 2
````

### islice - generator slicing, sliding window

````python
from itertools import islice

first_k = list(islice(some_generator, k))

from collections import deque
window = deque(islice(it, k), maxlen=k)
````

---

## collections

### deque - BFS, sliding window

````python
from collections import deque

q = deque([(0, 0)])
q.appendleft(x)   # O(1) prepend
q.popleft()       # O(1) dequeue
````

### defaultdict - adjacency lists, frequency maps

````python
from collections import defaultdict

graph = defaultdict(list)
freq = defaultdict(int)
freq[x] += 1  # no KeyError
````

### Counter - frequency, anagram, sliding window

````python
from collections import Counter

c = Counter(nums)
c.most_common(k)   # top k elements
c1 & c2            # min counts (intersection)
c1 | c2            # max counts (union)
c1 - c2            # difference (anagram checks)
````

**Key trick**: Counter subtraction silently drops zeros and negatives. This makes `not (need - window)` a clean "window fully satisfies need" check - used in minimum window substring and similar problems.

````python
need = Counter("abc")
window = Counter()

# as you expand/shrink the window:
window[char] += 1

if not (need - window):   # True when window covers all of need
    ...                   # shrink from left
````

### OrderedDict - manual LRU cache

````python
from collections import OrderedDict

od.move_to_end(key)
od.popitem(last=False)  # O(1) pop from front
````

---

## heapq

Python only has min-heap. Negate values for max-heap.

````python
import heapq

heapq.heapify(arr)                    # O(n) in-place
heapq.heappush(h, (priority, val))
heapq.heappop(h)

heapq.heappush(h, -val)              # max-heap trick

heapq.nlargest(k, nums)              # O(n log k)
heapq.nsmallest(k, nums)

for val in heapq.merge(*sorted_lists):  # merge k sorted lists lazily
    ...
````

### heappushpop / heapreplace - fused operations

````python
heapq.heappushpop(h, val)   # push then pop smallest - one O(log n) call
heapq.heapreplace(h, val)   # pop then push - faster, skips size check
                             # raises IndexError on empty heap
````

Use `heapreplace` to maintain a fixed-size heap of k elements (e.g. k largest):

````python
if len(h) < k:
    heapq.heappush(h, val)
elif val > h[0]:
    heapq.heapreplace(h, val)
````

### Tuple tiebreaker - avoid TypeError on non-comparable items

When two heap entries have the same priority, Python tries to compare the next element. If items aren't comparable (e.g. dicts, lists, custom objects), it raises `TypeError`.

````python
import itertools
counter = itertools.count()

heapq.heappush(h, (priority, next(counter), item))  # counter always breaks ties
````

### Lazy deletion - remove arbitrary elements

Python heaps have no `remove`. The pattern is a tombstone set - mark elements as deleted and skip them on pop.

````python
heap, dead = [], set()

heapq.heappush(heap, val)
dead.add(val_to_remove)      # "delete" by marking

def pop_valid(heap, dead):
    while heap and heap[0] in dead:
        dead.discard(heapq.heappop(heap))
    return heapq.heappop(heap) if heap else None
````

Comes up in: sliding window maximum with heap, task scheduling, dynamic top-K.

---

## bisect

Binary search without writing it from scratch.

````python
import bisect

bisect.bisect_left(arr, x)   # leftmost insertion index
bisect.bisect_right(arr, x)  # rightmost insertion index
bisect.insort(arr, x)        # insert maintaining sort order

# count elements in [lo, hi]
bisect.bisect_right(arr, hi) - bisect.bisect_left(arr, lo)

# Longest Increasing Subsequence - O(n log n)
tails = []
for x in nums:
    pos = bisect.bisect_left(tails, x)
    if pos == len(tails):
        tails.append(x)
    else:
        tails[pos] = x
# len(tails) is the LIS length
````

---

## functools

### lru_cache / cache - top-down DP memoization

````python
from functools import lru_cache, cache

@lru_cache(maxsize=None)
def dp(i, j, remaining):
    ...

@cache          # Python 3.9+ - cleaner alias for lru_cache(maxsize=None)
def dp(i, j):
    ...
````

**Clearing the cache** - critical in competitive programming when the same function is called across multiple test cases. Stale cache from a previous test case will return wrong answers silently.

````python
dp.cache_clear()          # wipe all cached results
dp.cache_info()           # CacheInfo(hits=..., misses=..., maxsize=..., currsize=...)
````

If your solution is wrapped in a loop over test cases:

````python
for _ in range(t):
    dp.cache_clear()      # must reset before each test case
    print(solve())
````

### reduce - fold over collections

````python
from functools import reduce
import operator
from math import gcd

reduce(operator.or_, list_of_sets)   # union of all sets
reduce(operator.and_, list_of_sets)  # intersection
reduce(gcd, nums)                    # GCD of entire array
````

### cmp_to_key - custom sort comparator

````python
from functools import cmp_to_key

# Largest number problem: "3" vs "30" -> compare "330" vs "303"
def cmp(a, b):
    return (a + b > b + a) - (a + b < b + a)

nums.sort(key=cmp_to_key(cmp))
````

---

## math

````python
import math

math.gcd(a, b)
math.lcm(a, b)       # Python 3.9+
math.isqrt(n)        # integer square root, no float errors
math.comb(n, k)      # n choose k
math.perm(n, k)      # nPk
math.inf             # cleaner than float('inf')
math.log2(n)         # tree height, bit length
````

---

## string module

````python
import string

string.ascii_lowercase   # 'abcdefghijklmnopqrstuvwxyz'
string.ascii_uppercase   # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
string.ascii_letters     # all 52 letters
string.digits            # '0123456789'
string.punctuation       # all punctuation chars
````

**Common patterns:**

````python
# 26-slot frequency array indexed by letter
freq = [0] * 26
for c in s:
    freq[ord(c) - ord('a')] += 1

# char classification (no import needed)
c.isalpha()   # a-z, A-Z
c.isdigit()   # 0-9
c.isalnum()   # a-z, A-Z, 0-9
c.islower() / c.isupper()

# char <-> index
ord(c) - ord('a')   # 0-based index for lowercase
chr(ord('a') + i)   # index back to char
````

---

## operator

Useful as first-class functions instead of lambdas.

````python
import operator

sorted(pairs, key=operator.itemgetter(1))    # sort by index
sorted(objs, key=operator.attrgetter('val')) # sort by attribute
reduce(operator.add, nums)
````

---

## Built-in tricks

### Matrix transpose

````python
transposed = list(zip(*matrix))   # rows become columns, O(mn)
````

Useful for rotating a grid, checking columns as rows, or diagonal traversal.

### sys.setrecursionlimit

Python's default recursion limit is 1000. Any recursive DP on n = 10^4 will crash with `RecursionError` without this.

````python
import sys
sys.setrecursionlimit(10**6)
````

Set it once at the top of your solution.

---

## sortedcontainers (third-party, standard in competitive programming)

`bisect` gives you the index but `list.insert` / `list.remove` are O(n). `SortedList` gives true O(log n) insert and delete with O(log n) index access.

````python
from sortedcontainers import SortedList

sl = SortedList()
sl.add(x)           # O(log n)
sl.remove(x)        # O(log n) - raises ValueError if not found
sl.discard(x)       # O(log n) - safe remove
sl[k]               # O(log n) - k-th smallest
sl.bisect_left(x)   # same semantics as bisect module
sl.bisect_right(x)
````

Use cases: sliding window median, count of smaller numbers after self, order statistics on a dynamic set.

````python
# sliding window median example structure
window = SortedList()
window.add(nums[i])
if i >= k:
    window.remove(nums[i - k])
median = window[k // 2] if k % 2 else (window[k//2 - 1] + window[k//2]) / 2
````

---

## Quick Reference

| Problem type | Tool |
| --- | --- |
| Alphabet sets / char classification | `string` module + `str` methods |
| Top K / priority queue | `heapq` |
| BFS / sliding window | `collections.deque` |
| Frequency / anagram / window | `collections.Counter` |
| LRU cache | `collections.OrderedDict` |
| Binary search / LIS | `bisect` |
| Top-down DP memoization | `functools.lru_cache` |
| Custom sort comparator | `functools.cmp_to_key` |
| GCD, nCk, integer sqrt | `math` |
| Graph / grouping | `collections.defaultdict` |
| Grid neighbors, brute force | `itertools.product` |
| Multi-source BFS seeding | `itertools.chain` |
| Prefix sums / running aggregates | `itertools.accumulate` |
| Enumerate subsets of size k | `itertools.combinations` |
| Brute force orderings | `itertools.permutations` |
| Run-length encoding / grouping | `itertools.groupby` |
| Sliding window median / order stats | `sortedcontainers.SortedList` |
| Heap with arbitrary deletion | lazy deletion + tombstone set |
| Matrix transpose | `zip(*matrix)` |
| Recursive DP on large n | `sys.setrecursionlimit` |
| Multi-test-case memoization | `dp.cache_clear()` |

Power combo for medium-hard problems: `lru_cache` + `defaultdict` + `heapq` + `bisect`.
