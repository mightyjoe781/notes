# Advanced Trees: Selecting the Optimal Structure

A range-query problem usually boils down to two questions: **what kind of updates does it need** (none, point, or range), and **what is the combine function** (sum, min/max/gcd, k-th smallest, ...)? 

The answers narrow the choice down to one of the structures below.

## Comparison Table

| **Data Structure**                              | **Point Update** | **Point Query** | **Range Update** | **Range Query** | **Time Complexity (Update / Query)** | **Space**  | **Common Use Cases**                                              |
| ----------------------------------------------- | ---------------- | --------------- | ---------------- | --------------- | ------------------------------------ | ---------- | ----------------------------------------------------------------- |
| **[Sparse Table](../additional/sparse.md)**     | ❌                | ✅               | ❌                | ✅ (idempotent)  | - / O(1)                             | O(n log n) | RMQ, range GCD/AND/OR/XOR on a static array                       |
| **[Fenwick Tree (Classic)](fenwick.md)**        | ✅                | ❌*              | ❌                | ✅ (prefix)      | O(log n) / O(log n)                  | O(n)       | Prefix sums, XORs, frequency counts                               |
| **Fenwick Tree (Dual)**                         | ❌                | ✅               | ✅                | ❌               | O(log n) / O(log n)                  | O(n)       | Range add + point read, simulation of cumulative effects          |
| **Fenwick Tree (2-BIT)**                        | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(n)       | Full support for sum range queries with range updates             |
| **[Segment Tree](segment.md)**                  | ✅                | ✅               | ❌                | ✅               | O(log n) / O(log n)                  | O(4n)      | RMQ, range sum/min/max/gcd with point updates                     |
| **Segment Tree + Lazy**                         | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(4n)      | Full range queries + range updates, e.g., add 5 over [l..r]       |
| **Sparse Segment Tree**                         | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(k log n) | Sparse values over large domains (e.g., up to 1e9)                |
| **Persistent Segment Tree**                     | ❌ (new ver)      | ✅ (old ver)     | ❌ (immutable)    | ✅ (prev ver)    | O(log n) / O(log n)                  | O(n log n) | Time-travel queries, undo/rollback, version control               |
| **[Sqrt Decomposition](sqrt_decomposition.md)** | ✅                | ✅               | ✅* (limited)     | ✅               | O(√n) / O(√n)                        | O(n)       | Simpler implementation for mid-size n, not time-critical problems |
| **Wavelet Tree**                                | ❌                | ✅ (rank)        | ❌                | ✅ (freq)        | O(log n) / O(log n)                  | O(n log n) | K-th smallest, rank/select, frequency queries in a range          |

- Fenwick Tree (Classic) supports point query only by computing `prefix(i) - prefix(i-1)`; it is not a direct $O(1)$ lookup like an array.

## Decision Flow

1. **Is the array static (no updates at all)?**
   - Combine function is idempotent (min/max/gcd/and/or) → **[Sparse Table](../additional/sparse.md)**, $O(1)$ query after $O(n \log n)$ build.
   - You only need sums → a plain prefix-sum array, no tree needed.
2. **Do you only need point updates + range sum?** → **[Fenwick Tree](fenwick.md)** - simplest to code, smallest constant factor.
3. **Do you need range updates AND range queries** (e.g. "add 5 to `[l,r]`", "sum of `[l,r]`")? → **[Segment Tree with lazy propagation](segment.md)**, or a **dual/2-BIT Fenwick** if the combine function is sum.
4. **Is the combine function not idempotent and not a simple sum** (e.g. merging `(max, count)` pairs, or matrix multiplication for Fibonacci-style recurrences)? → **[Segment Tree](segment.md)** - the combine function is the only thing that changes.
5. **Pressed for time, or the query pattern is irregular** (e.g. answering queries in a specific offline order)? → **[Sqrt Decomposition](sqrt_decomposition.md)** - asymptotically worse but far simpler to get right.
6. **Values span a huge range (up to 1e9) but updates are sparse?** → **Sparse/Dynamic Segment Tree** - allocate nodes lazily instead of a fixed-size array.
7. **Need to query a past version of the array, or undo updates?** → **Persistent Segment Tree** - each update creates $O(\log n)$ new nodes instead of mutating in place.
8. **Need "k-th smallest" or "count of elements ≤ x" in a range?** → **Merge Sort Tree** (simple, $O(\log^2 n)$) or **Wavelet Tree** / **order-statistics Fenwick** for $O(\log n)$.

## Other Structures Worth Knowing

These don't fit neatly into the table above but build directly on the same ideas.

### Merge Sort Tree

A segment tree where every node stores a **sorted copy** of the elements in its range (built bottom-up like merge sort). A range query binary-searches each of the $O(\log n)$ relevant nodes.

- Query: "how many elements in `[l, r]` are $\leq x$?" → $O(\log^2 n)$.
- No updates (rebuilding a sorted node is expensive) - use a **Fenwick of sorted lists** or a **BIT on values** if updates are required.

### Order-Statistics Fenwick (BIT on Values)

Index the Fenwick tree by **value** instead of array position. Each update marks "value `v` is present"; prefix sums then answer "how many values $\leq v$ have been inserted so far?".

- Classic use: counting inversions, "count of smaller elements after self".
- Requires coordinate compression if values are large.

### Persistent Segment Tree

Every update creates a new root and only the $O(\log n)$ nodes on the path to the changed leaf - all other nodes are shared with the previous version.

- Enables answering "what did the array look like after the $k$-th update?" in $O(\log n)$.
- Combine with coordinate compression for "k-th smallest in `arr[l..r]`" by treating each version as a prefix-count Fenwick/segment tree over values.

### 2D Fenwick / 2D Segment Tree

Extend the same recursive idea one dimension further: a Fenwick tree of Fenwick trees, or a segment tree of segment trees.

- Point update + 2D range sum in $O(\log n \cdot \log m)$ - common for "sum of submatrix" with updates.
- Memory grows to $O(nm)$ (or $O(nm \log n \log m)$ for the segment tree version), so prefer 2D Fenwick when only sums are needed.

### Mo's Algorithm

An **offline** technique: sort all queries by block of `l` (block size $\sqrt n$) and by `r` within each block, then answer them by sliding a `[l, r]` window and incrementally adding/removing elements.

- Turns many range queries into $O((n + q)\sqrt n)$ total work, even when the combine function has no nice algebraic structure (e.g. "number of distinct elements in `[l, r]`").
- Requires that all queries are known in advance (offline).

## Quick Reference

| Need | Reach for |
| --- | --- |
| Static array, idempotent query | [Sparse Table](../additional/sparse.md) |
| Point update, range sum | [Fenwick Tree](fenwick.md) |
| Range update, range sum | Fenwick (range-update trick) or [Segment Tree + Lazy](segment.md) |
| Range update/query, arbitrary associative combine | [Segment Tree](segment.md) |
| Huge value range, sparse updates | Sparse/Dynamic Segment Tree |
| Query past versions / rollback | Persistent Segment Tree |
| k-th smallest / count ≤ x in range | Merge Sort Tree, Wavelet Tree, or order-statistics Fenwick |
| 2D range sum with updates | 2D Fenwick |
| Offline queries, no algebraic structure | Mo's Algorithm |
| Simple to code, $O(\sqrt n)$ acceptable | [Sqrt Decomposition](sqrt_decomposition.md) |
