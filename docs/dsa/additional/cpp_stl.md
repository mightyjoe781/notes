# C++ STL for DSA

> These tricks are C++-specific. They don't change the algorithm - they remove boilerplate so you can focus on the logic. Mirrors [Python Standard Library for DSA](python_stdlib.md) for cross-reference.

## Containers

### vector - dynamic array

```cpp
#include <vector>

vector<int> v(n);          // size n, zero-initialized
vector<int> v(n, -1);      // size n, filled with -1
vector<vector<int>> grid(m, vector<int>(n, 0)); // 2D grid

v.push_back(x);
v.pop_back();
v.back(); v.front();
v.size();                  // size_t - cast to int when subtracting
```

**Gotcha**: `v.size()` returns `size_t` (unsigned). `v.size() - 1` underflows to a huge number when `v` is empty - check `!v.empty()` first or cast: `(int)v.size() - 1`.

### deque - BFS, sliding window

```cpp
#include <deque>

deque<int> dq;
dq.push_back(x); dq.push_front(x);
dq.pop_back();   dq.pop_front();
dq.front(); dq.back();
```

### pair / tuple - composite keys, return multiple values

```cpp
#include <utility>
#include <tuple>

pair<int, int> p = {1, 2};
p.first; p.second;

auto [a, b] = p;           // structured bindings (C++17)

tuple<int, int, int> t = {1, 2, 3};
auto [x, y, z] = t;
```

---

## unordered_map / unordered_set - hash map/set, O(1) average

```cpp
#include <unordered_map>
#include <unordered_set>

unordered_map<int, int> freq;
freq[x]++;                       // auto-creates with value 0

if (freq.count(x)) { ... }       // membership check
if (freq.find(x) != freq.end()) { ... }

unordered_set<int> seen;
seen.insert(x);
seen.erase(x);
```

**Gotcha**: `unordered_map` operator `[]` **inserts** the key if missing (with default value). Use `.count()` or `.find()` for read-only lookups to avoid accidental insertions.

### map / set - ordered, O(log n)

```cpp
#include <map>
#include <set>

map<int, int> m;          // sorted by key
set<int> s;               // sorted, unique

s.insert(x);
auto it = s.lower_bound(x);  // first element >= x
auto it2 = s.upper_bound(x); // first element > x

// kth smallest with order statistics: use policy tree (GNU PBDS)
```

---

## queue / stack / priority_queue

### queue - BFS

```cpp
#include <queue>

queue<int> q;
q.push(x); q.pop();
q.front(); q.back();
```

### stack - DFS, monotonic stack

```cpp
#include <stack>

stack<int> st;
st.push(x); st.pop();
st.top();
```

### priority_queue - heap (max-heap by default)

```cpp
#include <queue>

priority_queue<int> pq;                          // max-heap
priority_queue<int, vector<int>, greater<int>> pq; // min-heap

pq.push(x); pq.pop(); pq.top();

// pair-based: (priority, value)
priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
```

---

## algorithm

### sort - with custom comparator

```cpp
#include <algorithm>

sort(v.begin(), v.end());
sort(v.begin(), v.end(), greater<int>());        // descending

// custom comparator
sort(v.begin(), v.end(), [](int a, int b) {
    return a > b;
});

// sort pairs by second element
sort(v.begin(), v.end(), [](pair<int,int>& a, pair<int,int>& b) {
    return a.second < b.second;
});
```

### binary search - lower_bound / upper_bound

```cpp
#include <algorithm>

// requires sorted range
auto it = lower_bound(v.begin(), v.end(), x);  // first element >= x
auto it = upper_bound(v.begin(), v.end(), x);  // first element > x

int idx = lower_bound(v.begin(), v.end(), x) - v.begin();

// Longest Increasing Subsequence - O(n log n)
vector<int> tails;
for (int x : nums) {
    auto it = lower_bound(tails.begin(), tails.end(), x);
    if (it == tails.end()) tails.push_back(x);
    else *it = x;
}
// tails.size() is the LIS length
```

### accumulate, min/max element, count

```cpp
#include <numeric>

int sum = accumulate(v.begin(), v.end(), 0);

// prefix sums
vector<int> prefix(n + 1, 0);
partial_sum(v.begin(), v.end(), prefix.begin() + 1);

*max_element(v.begin(), v.end());
*min_element(v.begin(), v.end());
count(v.begin(), v.end(), x);
```

### permutations

```cpp
#include <algorithm>

sort(v.begin(), v.end());          // must start sorted for all perms
do {
    // process v
} while (next_permutation(v.begin(), v.end()));
```

### reverse, unique

```cpp
reverse(v.begin(), v.end());

// remove consecutive duplicates (call sort first for full dedup)
sort(v.begin(), v.end());
v.erase(unique(v.begin(), v.end()), v.end());
```

---

## numeric helpers

```cpp
#include <numeric>
#include <climits>
#include <cmath>

__gcd(a, b);                 // built-in gcd (also gcd() in <numeric>, C++17)
lcm(a, b);                    // <numeric>, C++17

INT_MAX; INT_MIN;             // <climits>
LLONG_MAX; LLONG_MIN;

sqrt(n); pow(a, b);
```

---

## Bit manipulation builtins (GCC)

```cpp
__builtin_popcount(x);        // number of set bits (int)
__builtin_popcountll(x);      // for long long
__builtin_clz(x);             // count leading zeros
__builtin_ctz(x);             // count trailing zeros - position of lowest set bit
```

---

## Quick Reference

| Problem type | Tool |
| --- | --- |
| Top K / priority queue | `priority_queue` |
| BFS / sliding window | `deque`, `queue` |
| Frequency / anagram / window | `unordered_map` |
| Ordered keys / order statistics | `map`, `set` |
| Binary search / LIS | `lower_bound`, `upper_bound` |
| Custom sort comparator | `sort` with lambda |
| GCD, LCM, integer limits | `<numeric>`, `<climits>` |
| Prefix sums | `partial_sum` |
| Brute force orderings | `next_permutation` |
| Dedup sorted range | `unique` + `erase` |
| Popcount / bit tricks | `__builtin_*` |

Power combo for medium-hard problems: `unordered_map` + `priority_queue` + `lower_bound` + lambda comparators.
