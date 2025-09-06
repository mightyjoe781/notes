# Segment Trees

* **Segment Tree** with **lazy propagation** to efficiently handle range updates and range minimum queries (RMQ).
* Segment trees provide fast $O(\log n)$ queries and updates, making them ideal for dynamic array problems.
* to get RSQ in Segment Tree
    * In build function replace : `st[p] = min(st[2*p], st[2*p+1]);` with `st[p] = st[2*p] + st[2*p+1];`
    * In query function : `min(query(...), query(...));`  with `query(...left...) + query(...right...);`
    * In update function : `st[p] = st[2*p] + st[2*p+1];`


| **Operation**    | **Fenwick Tree** | **Segment Tree** |
| ---------------- | ---------------- | ---------------- |
| **Point Update** | ✅ O(log n)       | ✅ O(log n)       |
| **Range Query**  | ✅ O(log n)       | ✅ O(log n)       |
| **Range Update** | ❌*               | ✅ (needs lazy)   |
| **Point Query**  | ❌*               | ✅                |

## Segment Tree (without Lazy Propagation)

* Only Point Updates are available

````c++
#include <bits/stdc++.h>
using namespace std;

class SegmentTree {
    int n;
    vector<int> st;
  
    int l(int p) { return  p<<1; }
    int r(int p) { return (p<<1)+1; }
  
    void build(const vector<int>& A, int p, int l, int r) {
        if (l == r)
            st[p] = A[l];
        else {
            int m = (l + r) / 2;
            build(A, l(p), l, m);
            build(A, r(p), m+1, r);
            st[p] = min(st[l(p)], st[r(p)]);
        }
    }

    int query(int p, int l, int r, int i, int j) {
        if (j < l || i > r) return INT_MAX;
        if (i <= l && r <= j) return st[p];
        int m = (l + r) / 2;
        return min(query(l(p), l, m, i, j), query(r(p), m+1, r, i, j));
    }
		
  
  	// notice its a point update
    void update(int p, int l, int r, int idx, int val) {
        if (l == r)
            st[p] = val;
        else {
            int m = (l + r) / 2;
            if (idx <= m) update(l(p), l, m, idx, val);
            else          update(r(p), m+1, r, idx, val);
            st[p] = min(st[l(p)], st[r(p)]);
        }
    }

public:
    SegmentTree(const vector<int>& A) {
        n = A.size();
        st.assign(4*n, 0);
        build(A, 1, 0, n-1);
    }

    int query(int i, int j) { return query(1, 0, n-1, i, j); }
    void update(int idx, int val) { 
      if (idx < 0 || idx >= n) return;  // Add this check
      update(1, 0, n-1, idx, val); 
		}
};
````



## Segment Tree with Lazy Propagation (Optimal)

```c++
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

class SegmentTree {                              // OOP style
private:
  int n;                                         // n = (int)A.size()
  vi A, st, lazy;                                // the arrays

  int l(int p) { return  p<<1; }                 // go to left child
  int r(int p) { return (p<<1)+1; }              // go to right child

  int conquer(int a, int b) {
    if (a == -1) return b;                       // corner case
    if (b == -1) return a;
    return min(a, b);                            // RMQ
  }

  void build(int p, int L, int R) {              // O(n)
    if (L == R)
      st[p] = A[L];                              // base case
    else {
      int m = (L+R)/2;
      build(l(p), L  , m);
      build(r(p), m+1, R);
      st[p] = conquer(st[l(p)], st[r(p)]);
    }
  }

  void propagate(int p, int L, int R) {
    if (lazy[p] != -1) {                         // has a lazy flag
      st[p] = lazy[p];                           // [L..R] has same value
      if (L != R)                                // not a leaf
        lazy[l(p)] = lazy[r(p)] = lazy[p];       // propagate downwards
      else                                       // L == R, a single index
        A[L] = lazy[p];                          // time to update this
      lazy[p] = -1;                              // erase lazy flag
    }
  }

  int RMQ(int p, int L, int R, int i, int j) {   // O(log n)
    propagate(p, L, R);                          // lazy propagation
    if (i > j) return -1;                        // infeasible
    if ((L >= i) && (R <= j)) return st[p];      // found the segment
    int m = (L+R)/2;
    return conquer(RMQ(l(p), L  , m, i          , min(m, j)),
                   RMQ(r(p), m+1, R, max(i, m+1), j        ));
  }

  // notice range updates
  void update(int p, int L, int R, int i, int j, int val) { // O(log n)
    propagate(p, L, R);                          // lazy propagation
    if (i > j) return;
    if ((L >= i) && (R <= j)) {                  // found the segment
      lazy[p] = val;                             // update this
      propagate(p, L, R);                        // lazy propagation
    }
    else {
      int m = (L+R)/2;
      update(l(p), L  , m, i          , min(m, j), val);
      update(r(p), m+1, R, max(i, m+1), j        , val);
      int lsubtree = (lazy[l(p)] != -1) ? lazy[l(p)] : st[l(p)];
      int rsubtree = (lazy[r(p)] != -1) ? lazy[r(p)] : st[r(p)];
      st[p] = (lsubtree <= rsubtree) ? st[l(p)] : st[r(p)];
    }
  }

public:
  SegmentTree(int sz) : n(sz), st(4*n), lazy(4*n, -1) {}

  SegmentTree(const vi &initialA) : SegmentTree((int)initialA.size()) {
    A = initialA;
    build(1, 0, n-1);
  }

  void update(int i, int j, int val) { update(1, 0, n-1, i, j, val); }

  int RMQ(int i, int j) { return RMQ(1, 0, n-1, i, j); }
};
```

