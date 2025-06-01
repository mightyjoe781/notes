# Dsa Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: dsa
This is part 1 of 1 parts

---

## File: dsa/additional/bit1.md

# Bit Manipulation

Bit manipulation enables direct work with the binary representation of numbers. It optimizes performance and solves problems involving sets, parity, power-of-two checks, and other applications.

## XOR

XORs have 2 important property other than commutative & associativity

- Identity Element: $A \oplus 0 = A$
- Self - Inverse : $A \oplus A = 0$

[All about XOR](https://accu.org/journals/overload/20/109/lewin_1915/)

## Basic Bit Operations

* Check if `ith` bit is set

````c++
if (n & (1 << i)) {
  // i-th bit is set
}
````

- set the `ith` bit : `n |= (1 << i)`
- clear the `ith` bit : `n &= ~(1 << i)`
- toggle the `ith` bit : `n ^= (1 << i)`
- Count total set Bits (Hamming Weight)

````c++
int count = 0;
for (int i = 0; i < 32; ++i)
    if (n & (1 << i)) ++count;
````

````c++
int count = __builtin_popcount(n);        // GCC / Clang
int countll = __builtin_popcountll(n);    // For long long
````

- count trailing zeroes (rightmost 0s) : `int tz = __builtin_ctz(n);`
- count leading zeroes : `int lz = __builtin_clz(n);`

- Get Rightmost set bit :
  - Used for iterating over subsets

````c++
// bit manipulation
int r = n & -n  // Two's complement trick
// OR
int r = n & (~n + 1)  // Explicit two's complement
````

- Remove Rightmost set bit : `n = n & (n-1)`
  - Useful for counter number of set bits : (Kernighan’s Algorithm)
- Reverse Bits (Manually)

````c++
unsigned int reverseBits(unsigned int n) {
    unsigned int rev = 0;
    for (int i = 0; i < 32; ++i)
        rev = (rev << 1) | ((n >> i) & 1);
    return rev;
}
````

- Iterate over all subsets of a Bitmask. Useful in DP on subsets

````c++
int mask = ...;
for (int sub = mask; sub; sub = (sub - 1) & mask) {
    // process sub
}
````

- XOR Trick : Detect Single Number
  - Find the number that appears odd number of times

````c++
int xor_all = 0;
for (int a : arr) xor_all ^= a;
````

- Swap without temporary variable
  - avoid in production, not readable, not safe with references to same memory

````c++
a ^= b;
b ^= a;
a ^= b;
````

- Check power of two

````c++
bool isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
````

- Difference Bits Sum Pairwise
  - Efficiently calculates total XOR difference over all pairs

````c++
long long total = 0;
int n = A.size();
for (int i = 0; i < 32; ++i) {
    int count = 0;
    for (int x : A)
        if (x & (1 << i)) count++;
    total += 2LL * count * (n - count);
}
````

- Binary String Representation

````c++
bitset<32> bs(n);
cout << bs.to_string() << "\n";
````

- Turn Off Last Consectuive Set Bits : `x = x & (x + 1);`
- Turn On Last Zero Bit : `x = x | (x + 1);`
- Log Base 2 : `int highestSetBit = 31 - __builtin_clz(n);  // Position of MSB (0-indexed)`
- Parity (Even or Odd Number of Set Bits) : `bool evenParity = __builtin_parity(n) == 0;`

## Builtins

| **Functionality**                   | **C++ Built-in**          | **Python Equivalent (or Alternative)**                  |
| ----------------------------------- | ------------------------- | ------------------------------------------------------- |
| **Count 1s in binary (popcount)**   | `__builtin_popcount(x)`   | bin(x).count('1') or x.bit_count() (Python 3.10+)       |
| **Count 1s in 64-bit int**          | `__builtin_popcountll(x)` | bin(x).count('1') or x.bit_count() (works for int)      |
| **Count trailing zeroes**           | `__builtin_ctz(x)`        | len(bin(x & -x)) - 3 or use custom function (see below) |
| **Count leading zeroes (32-bit)**   | `__builtin_clz(x)`        | 32 - x.bit_length()                                     |
| **Parity (even/odd 1s)**            | `__builtin_parity(x)`     | bin(x).count('1') % 2                                   |
| **Check if power of 2**             | N/A                       | x > 0 and (x & (x - 1)) == 0                            |
| **Get lowest set bit**              | N/A                       | x & -x                                                  |
| **Remove lowest set bit**           | N/A                       | x & (x - 1)                                             |
| **Reverse bits manually**           | N/A (manual loop)         | Use a loop, or: int('{:032b}'.format(x)[::-1], 2)       |
| **Highest set bit position (log2)** | `31 - __builtin_clz(x)`   | x.bit_length() - 1                                      |

### Python Custom Helper Functions

````c++
def count_trailing_zeroes(x):
    return (x & -x).bit_length() - 1 if x != 0 else 32

def count_leading_zeroes(x, bits=32):
    return bits - x.bit_length() if x != 0 else bits

def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0
````

### Summary

````c++
// Correct bit manipulation operations
bool checkBit(int n, int i) { return n & (1 << i); }
int setBit(int n, int i) { return n | (1 << i); }
int clearBit(int n, int i) { return n & ~(1 << i); }
int toggleBit(int n, int i) { return n ^ (1 << i); }
int getRightmostSetBit(int n) { return n & -n; }
int clearRightmostSetBit(int n) { return n & (n - 1); }
````

## Problems on Bit Manipulation

- **Single Number (Leetcode 136)** – XOR trick (A ^ A = 0)
- **Single Number II (Leetcode 137)** – Bit count per position, modulo 3 trick
- **Sum of XOR of all pairs** – Count set bits at each position, pairwise XOR contribution
- **Counting Bits (Leetcode 338)** – DP using n & (n - 1) to count set bits
- **Reverse Bits (Leetcode 190)** – Bit shifting and reconstruction
- **Hamming Distance (Leetcode 461)** – popcount(a ^ b)
- **Number of 1 Bits (Leetcode 191)** – Hamming weight, __builtin_popcount, loop-based
- **Power of Two (Leetcode 231)** – (n > 0 && (n & (n - 1)) == 0)
- **Power of Four (Leetcode 342)** – Power of two + only one bit set at even position
- **Bitwise AND of Numbers Range (Leetcode 201)** – Common prefix by bit shifting
- **Subsets Generation** – Bitmask subset loop: (sub - 1) & mask
- **Maximum XOR of Two Numbers in an Array (Leetcode 421)** – Trie + greedy on MSBs
- **Total Hamming Distance (Leetcode 477)** – Bitwise count at each position
- **Missing Number (Leetcode 268)** – XOR from 0 to n with array
- **Binary Watch (Leetcode 401)** – Count set bits, generate valid times
- **Complement of Base 10 Integer (Leetcode 1009)** – Flip bits up to MSB
- **Find Rightmost Set Bit** – x & -x, used in subset iteration, masks, etc.


---

## File: dsa/additional/bit2.md

# Bitmask DP

Bitmask DP is useful when the state of a problem involves subsets (e.g. selected elements, visited nodes). Since subsets of n elements can be represented using integers from 0 to 2ⁿ - 1, we can model states with bitmasks.

## Subset Generation

To iterate over **all subsets** of a set of size n:

````c++
for (int mask = 0; mask < (1 << n); ++mask) {
    // mask represents a subset
    for (int i = 0; i < n; ++i) {
        if (mask & (1 << i)) {
            // i-th element is in the subset
        }
    }
}
````

To iterate over all subset of a specific mask

````c++
int mask = ...;
for (int sub = mask; sub; sub = (sub - 1) & mask) {
    // sub is a subset of mask
}
````

Very useful in optimization problems with subsets (e.g., TSP, Set Cover).

## Bitmask DP Template

````c++
int dp[1 << N]; // Stores answers for all subsets

for (int mask = 0; mask < (1 << N); ++mask) {
    for (int i = 0; i < N; ++i) {
        if ((mask >> i) & 1) continue; // skip if i already in mask
        int newMask = mask | (1 << i);
        dp[newMask] = min(dp[newMask], dp[mask] + cost[mask][i]); // Update based on problem
    }
}
````

## Example Problems

### Traveling Salesman Problem (TSP)

- Problem: Find the minimum cost path that visits every city once and returns to the origin.
- State:
  - mask = cities visited so far
  - i = current city
- Recurrence: `dp[mask][i] = min(dp[mask][i], dp[mask ^ (1 << i)][j] + dist[j][i]) // for all j ≠ i`
- Base case: `dp[1 << i][i] = cost from 0 to i`

````c++
n = 4
INF = float('inf')
dp = [[INF] * n for _ in range(1 << n)]
dp[1][0] = 0  # Start at city 0

for mask in range(1 << n):
    for u in range(n):
        if not (mask & (1 << u)):
            continue
        for v in range(n):
            if mask & (1 << v):
                continue
            new_mask = mask | (1 << v)
            dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + cost[u][v])

# Final answer: return to city 0
res = INF
for u in range(1, n):
    res = min(res, dp[(1 << n) - 1][u] + cost[u][0])

print(res)
````

### Count Number of Ways to Partition into K Subsets

- Problem: Partition a set of n elements into exactly k non-empty subsets
- Use Bell numbers or bitmask DP with memoization over (mask, k) where:
  - mask = unpicked elements
  - k = subsets left

### Minimum Incompatibility

- [Problem Link](https://leetcode.com/problems/minimum-incompatibility/)
- Need to partition array into k subsets of size n / k, minimizing incompatibility (max - min of each subset)
- Precompute all valid subsets of size n/k and their incompatibility
- Use Bitmask DP:
  - dp[mask] = min incompatibility for subset mask
  - Transition: combine valid group with remaining mask

### Max AND Sum of Array

- [Problem Link](https://leetcode.com/problems/maximum-and-sum-of-array/)
- You are given a list of nums and you have k slots, each can take up to 2 numbers.
- Use Bitmask DP:
  - State: mask of which numbers used
  - Value: max AND sum you can get
  - Transition: try placing a number in each slot (0..k-1) with 2 capacity

## Bitmask Utility Tricks

- Set/Unset/Toggle Bit

````c++
mask | (1 << i)    // set i-th bit
mask & ~(1 << i)   // unset i-th bit
mask ^ (1 << i)    // toggle i-th bit
````

- Count Set Bits

````c++
__builtin_popcount(mask)    // Count 1's in binary (GCC/Clang)
````

- Iterate Subsets of a Mask

````c++
for (int sub = mask; sub; sub = (sub - 1) & mask)
````

## Common Scenarios to Use Bitmask DP

- Permutation with cost (e.g., assignment, TSP)
- Subset selection with constraints (e.g., compatibility, minimal sum)
- Dynamic Programming on graph states (e.g., Hamiltonian path)
- Partitioning problems where sets are mutually exclusive

### Practice Problems

| **Problem**                                                  | **Key Idea**                         |
| ------------------------------------------------------------ | ------------------------------------ |
| [Leetcode 847 - Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | Bitmask BFS on visited nodes         |
| [Leetcode 1349 - Maximum Students Taking Exam](https://leetcode.com/problems/maximum-students-taking-exam/) | Bitmask DP with row states           |
| [Leetcode 1659 - Maximize Grid Happiness](https://leetcode.com/problems/maximize-grid-happiness/) | DP + Bitmask Compression             |
| [AtCoder DP Contest - Problem O “Matching”](https://atcoder.jp/contests/dp/tasks/dp_o) | Count perfect matchings with bitmask |
| [Leetcode 689 - Maximum Sum of 3 Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/) | Sliding window + bitmask dp          |

---

## File: dsa/additional/geometry1.md

# Computational Geometry

## Orientation of 3 Points

Given 3 points determine if three points A, B, C

- Clockwise
- Counter Clockwise
- Collinear

Formulae : `val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x)*(c.y - b.y)`

- val = 0 : collinear
- val > 0 : clockwise
- val < 0 : counter-clockwise

## Area Calculations

### Triangle Area

- Using determinant

````python
double triangle_area(Point a, Point b, Point c) {
    return abs((a.x*(b.y - c.y) + b.x*(c.y - a.y) + c.x*(a.y - b.y)) / 2.0);
}
````

### Polygon Area - Shoelace Formula

- For a polygon with vertices in order $p_0$, $p_1$, ..., $p_{n-1}$, use

````python
double polygon_area(vector<Point> &pts) {
    int n = pts.size();
    double area = 0;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        area += (pts[i].x * pts[j].y) - (pts[j].x * pts[i].y);
    }
    return abs(area) / 2.0;
}
````

## Distance

- Between Two Points

- Euclidean Distance

````python
double dist(Point a, Point b) {
    return sqrt((a.x - b.x)*(a.x - b.x) + (a.y - b.y)*(a.y - b.y));
}
````

* point to Line `(Ax + By + C = 0)`

````python
double point_line_distance(Point p, double A, double B, double C) {
    return abs(A*p.x + B*p.y + C) / sqrt(A*A + B*B);
}
````

- Point to Segment
- Use projection method or brute-force checking

````python
double dist_point_to_segment(Point p, Point a, Point b) {
    double len2 = dist(a, b)*dist(a, b);
    if (len2 == 0.0) return dist(p, a);
    double t = ((p.x - a.x)*(b.x - a.x) + (p.y - a.y)*(b.y - a.y)) / len2;
    t = max(0.0, min(1.0, t));
    Point proj = {a.x + t*(b.x - a.x), a.y + t*(b.y - a.y)};
    return dist(p, proj);
}
````

## Dot & Cross Product

### Dot Product

- $a.b = |a||b| \cos \theta$
- Sign tells about angle
  - `> 0` : acute
  - `< 0` : obtuse
  - `= 0` : orthogonal

````python
double dot(Point a, Point b) {
    return a.x * b.x + a.y * b.y;
}
````

### Cross Product

- $a \times b = a.x * b.y - a.y * b.x$
- Useful for area, orientation, convex hulls

````python
double cross(Point a, Point b) {
    return a.x * b.y - a.y * b.x;
}
````

## Angle between vectors

````python
double angle(Point a, Point b) {
    return acos(dot(a, b) / (hypot(a.x, a.y) * hypot(b.x, b.y)));
}
````

Result is in **radians**. Use `angle * 180.0 / M_PI` to convert to degrees.

## Floating-point precision issues & techniques

- Avoid comparing floats directly, use abs(a - b) < EPS where EPS ~ 1e-9
- Prefer integers where possible (e.g., cross product or Shoelace)
- Use long double for better precision if needed
- Normalize angles or vectors before comparing

---

## File: dsa/additional/geometry2.md

# Points, Lines, Polygons

## Line Representations

### Standard

- A line: $Ax + By+ C = 0$. Used in analytical geometry
- $A = y_2 - y_1$
- $B = x_1 - x_2$
- $C = -(A*x_1 + B*y_1)$

### Parametric

- A point on line: $P = A + t* (B -A)$, where $A, B$ are two points on the line and $t \in \real$

## Line and Segment Intersection

Check if two segments $p1p2$ and $q1q2$ intersect

- Orientation Test: Use oreintation function on all combinations
  - o1 = orientation(p1, p2, q1)
  - o2 = orientation(p1, p2, q2)
  - o3 = orientation(q1, q2, p1)
  - o4 = orientation(q1, q2, p2)
  - If o1 != o2 && o3 != o4 → segments intersect.
- Collinear Case
  - Check if one point lies on the other segment using bounding box

````python
bool onSegment(Point p, Point q, Point r) {
    return q.x <= max(p.x, r.x) && q.x >= min(p.x, r.x) &&
           q.y <= max(p.y, r.y) && q.y >= min(p.y, r.y);
}
````

## Point in Triangle & Point in Polygon

### Point in Triangle

Use **Barycentric Coordinates** or check if point lies on the **same side** of each triangle edge.

````python
bool point_in_triangle(Point a, Point b, Point c, Point p) {
    double A = triangle_area(a, b, c);
    double A1 = triangle_area(p, b, c);
    double A2 = triangle_area(a, p, c);
    double A3 = triangle_area(a, b, p);
    return abs((A1 + A2 + A3) - A) < EPS;
}
````

### Point in Polygon

#### Ray Casting Algorithm

- Shoot a ray from the point to the right.
- Count how many times it intersects with polygon edges.
- If odd → inside, else outside.

#### Winding Number

- Based on angle the polygon wraps around the point.
- Winding number ≠ 0 ⇒ point is inside.

````python
// Ray-casting method
bool isInside(vector<Point> &polygon, Point p) {
    int n = polygon.size(), cnt = 0;
    for (int i = 0; i < n; i++) {
        Point a = polygon[i], b = polygon[(i+1)%n];
        if (a.y > b.y) swap(a, b);
        if (p.y > a.y && p.y <= b.y && 
            (b.y - a.y) * (p.x - a.x) < (b.x - a.x) * (p.y - a.y))
            cnt ^= 1;
    }
    return cnt;
}
````

## Convex vs Concave Polygon

- A polygon is **convex** if all internal angles < 180°.
- All cross products of consecutive edges should have the **same sign**.

````python
bool isConvex(vector<Point>& poly) {
    int n = poly.size();
    int sign = 0;
    for (int i = 0; i < n; i++) {
        Point a = poly[i];
        Point b = poly[(i+1)%n];
        Point c = poly[(i+2)%n];
        int cp = cross({b.x - a.x, b.y - a.y}, {c.x - b.x, c.y - b.y});
        if (cp != 0) {
            if (sign == 0)
                sign = (cp > 0 ? 1 : -1);
            else if ((cp > 0 ? 1 : -1) != sign)
                return false;
        }
    }
    return true;
}
````

## Polygon Perimeter & Area

### Perimeter

````python
double polygon_perimeter(vector<Point> &pts) {
    double perim = 0;
    int n = pts.size();
    for (int i = 0; i < n; i++) {
        perim += dist(pts[i], pts[(i + 1) % n]);
    }
    return perim;
}
````

### Area (Shoelace Method)

````python
double polygon_area(vector<Point> &pts) {
    int n = pts.size();
    double area = 0;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        area += (pts[i].x * pts[j].y) - (pts[j].x * pts[i].y);
    }
    return abs(area) / 2.0;
}
````

## Convexity Detection

Check if **all turns** between consecutive triplets are either all **left** (CCW) or all **right** (CW) as shown in isConvex() function.

## Closest Pair of Points (Divide & Conquer)

Find closest pair in $O(n log n)$ time:

1. Sort points by x-coordinate
2. Recursively solve for left and right halves
3. Combine step: consider only points within $d$ distance of mid-line
4. Sort those by $y$ and check distance within a vertical strip

````python
import math

def dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def closest_pair_rec(px, py):
    n = len(px)
    if n <= 3:
        return min(
            (dist(px[i], px[j]) for i in range(n) for j in range(i + 1, n)),
            default=float('inf')
        )

    mid = n // 2
    mid_x = px[mid][0]

    left_px = px[:mid]
    right_px = px[mid:]

    left_py = list(filter(lambda p: p[0] <= mid_x, py))
    right_py = list(filter(lambda p: p[0] > mid_x, py))

    d_left = closest_pair_rec(left_px, left_py)
    d_right = closest_pair_rec(right_px, right_py)
    d = min(d_left, d_right)

    strip = [p for p in py if abs(p[0] - mid_x) < d]

    # Check at most 6 neighbors ahead in y-sorted strip
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            d = min(d, dist(strip[i], strip[j]))

    return d

def closest_pair(points):
    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    return closest_pair_rec(px, py)
````



---

## File: dsa/additional/geometry3.md

# Convex Hull

The **Convex Hull** of a set of points is the smallest convex polygon that contains all the points. It’s like stretching a rubber band around the outermost points.

## Graham Scan

**Idea**: Sort points by polar angle w.r.t. lowest point (y-coordinate, then x), then walk through the sorted list, maintaining a stack of convex points.

Steps:

- Choose the point P0 with the lowest y-coordinate (and leftmost if tie).
- Sort the rest of the points by polar angle with P0.
- Traverse sorted points:
  - For each point, check if it makes a **left turn**.
  - Pop from the stack if not (right turn).
  - Push otherwise.

````python
def graham_scan(points):
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    points.sort()
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]  # Avoid duplicating the endpoints
````

## Andrew’s Monotone Chain

**Similar to Graham Scan**, but avoids sorting by angle—just sort by x/y and construct **lower and upper hulls** separately.

````python
def monotone_chain(points):
    points = sorted(set(points))
    def build_half(points):
        hull = []
        for p in points:
            while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
                hull.pop()
            hull.append(p)
        return hull

    lower = build_half(points)
    upper = build_half(reversed(points))
    return lower[:-1] + upper[:-1]
````

## Gift Wrapping (Jarvis March)

**Idea**: Start from the leftmost point, then at each step choose the most counterclockwise point.

- Time Complexity : $O(nh)$, $h$ is the number of points on the convex hull.
- Good when $h$ is small like ~ $ \log n$
- Easy to understand

## Application

### Rotating Calipers

**Use Cases**:

- Diameter of convex polygon.
- Closest pair on convex hull.
- Width of convex polygon.
- Minimum/maximum enclosing rectangles.

**Idea**: Two antipodal points move around the hull while maintaining orientation.

### Diameter of Convex Polygon

Using **Rotating Calipers**, we can find the pair of points with the maximum distance (farthest apart) in a convex polygon in linear time.

````python
def convex_polygon_diameter(hull):
    n = len(hull)
    if n == 2:
        return dist(hull[0], hull[1])
    j, max_dist = 1, 0
    for i in range(n):
        while True:
            d = dist(hull[i], hull[j])
            d_next = dist(hull[i], hull[(j + 1) % n])
            if d_next > d:
                j = (j + 1) % n
            else:
                break
        max_dist = max(max_dist, dist(hull[i], hull[j]))
    return max_dist
````

### Minkowski Sum (Basics)

The **Minkowski Sum** of two polygons A and B is formed by adding each point of A to every point of B.

- Used in collision detection, motion planning.
- If A and B are convex and sorted, their Minkowski sum can be constructed in O(n + m).

````python
def minkowski_sum(poly1, poly2):
    result = []
    for p1 in poly1:
        for p2 in poly2:
            result.append((p1[0] + p2[0], p1[1] + p2[1]))
    return convex_hull(result)
````



---

## File: dsa/additional/geometry4.md

# Advanced Geometry Algorithms

## Line-Sweep for Segment Intersection

**Goal**: Detect if any two line segments intersect or count total intersections.

Idea:

- Sweep a vertical line across the plane.
- Maintain a balanced BST of active segments ordered by their y-coordinates.
- At each **event** (segment start/end or intersection), update BST and check neighboring segments for intersections.

Time Complexity : $O((n+k) \log n)$ , $n$ = number of segments, $k = $ number of intersections

Key Concepts

- Events are sorted by `x` co-ordinate
- Use Comparator to maintain segment order in BST

Applications

- Geometry Kernels
- Map Overlays
- Graphics (clipping)

## Half-Plane Intersection (Brief Overview)

**Goal**: Find the intersection of multiple half-planes (bounded regions).

Idea

- Each inequality (e.g., ax + by + c <= 0) represents a half-plane.
- Sort half-planes by angle and use deque to maintain valid intersection area.
- Use orientation checks to keep only feasible intersections.

Applications

- Feasible region finding in LP
- Visibility problems
- Polygon clipping

Time Complexity : $O(n \log n)$

## Convex Hull Trick (DP Optimization)

- **Used for**: Efficient queries on minimum/maximum value of a set of linear functions at some x.

Requirements

- Lines added in order of decreasing/increasing slope.
- Queries are in increasing/decreasing order (for amortized O(1)), or binary search if arbitrary.

Useful when solving:

````python
dp[i] = min(dp[j] + a[i]*b[j]) or max(...)
````

Implementation

- Maintain a deque of candidate lines.
- Remove lines that are no longer optimal using slope comparisons (cross-product or intersection).



Time Complexity

- Amortized O(1) per query with monotonic insert/query
- O(log n) using binary search

## Tangents from a point to a circle

Goal: Given a point P and circle (center C, radius R), find tangent points on the circle.

Cases

- If |PC| < R: No tangent
- If |PC| = R: One tangent (point lies on the circle)
- If |PC| > R: Two tangents

Steps

1. Compute distance $d = |P - C|$
2. Angle between center-to-point line and tangent = $\theta = a \cos \frac{R}{d}$
3. Use rotation and trigonometry to find tangent points

Application

- Visibility problems
- Shortest path avoiding circle
- Light simulation

## Polygon Triangulation (Overview)

**Goal**: Break a simple polygon into non-overlapping triangles.

Key Algorithms

- **Ear Clipping** (Greedy, O(n²))
  - Repeatedly remove “ears” (triangles with no other vertex inside)
- **Sweep Line / Monotone Polygon Partitioning** (Optimal, O(n log n))

Applications

- Rendering (graphics pipeline)
- Physics (mesh simplification)
- Area computation, centroid calculation

## Polygon Cutting & Union (Overview)

Cutting

- Given a polygon and a line, split it into two parts.
- Requires handling intersection points with polygon edges.
- Important in **constructive solid geometry** and **boolean ops**.

Union (Boolean Operations on Polygons)

- Compute union, intersection, or difference of polygons.
- Based on **Weiler–Atherton**, **Greiner–Hormann**, or **Bentley–Ottmann**.

Applications

- CAD
- GIS (geospatial data)
- Game dev / simulation engines

---

## File: dsa/additional/math1.md

# Number Theory

## GCD, LCM & Primes

### Euclidean Algorithm

- GCD (Greatest Common Divisor) : largest number that divides both `a` and `b`
- Approach : `gcd(a, b) = gcd(b, a % b)`
- Time: $O(\log \min(a, b))$

````c++
# recursive
int gcd(int a, int b) {
  return b == 0 ? a : gcd(b, a % b);
}

# iterative
int gcd(int a, int b) {
  while(b)
    a %= b, swap(a, b);
 	return a;
}
````

* Properties
  * $\gcd({a,0}) = a$
  * $\gcd(a, b) = \gcd(b, a\%b)$
  * $\gcd (a, b, c) = \gcd(\gcd(a, b), c)$
  * $\gcd(a, b) * lcm(a, b) = a * b$


### Extended Euclidean Algorithm

- Goal : Find $x, y$ such that $ax + by = gcd(a, b)$
- Useful for:
  - Finding modular inverse when $\gcd (a, m) = 1$
  - Solving Linear Diophantine Equations

````python
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1
````

### Applications of GCD (e.g., LCM tricks, reductions)

- LCM : smallest number that is a multiple of both a and b
- Approach : `LCM(a, b) = (a * b) // gcd(a, b)`
- Reduce $\frac{a}{b}$ to lowest terms, divide both by gcd(a, b)
- Problems
  - Rope cutting into equal parts
  - Synchronizing Cycles (LCM)

### Prime Numbers

* A prime number is a number greater than 1 that has no positive divisors other than 1 and itself.
* 2 is the only prime-even number
* If n is not prime, then it has a factor $ \lt= \sqrt{n}$
* There are infinitely many prime numbers
* Naive Implementation take $O(n\sqrt n)$ time

````python
def prime_factors(n):
    i = 2
    while i*i <= n:
        while n % i == 0:
            print(i, end=' ')
            n //= i
        i += 1
    if n > 1:
        print(n)
````

* Applications

  * Cryptography (RSA, etc)

  * Number theory Problems

  * Factorization, divisibility problems

### Count & Sum of Divisors

Let $n = p_1^{e_1} *p_2^{e_2} * ... *p_k^{e_k}$

- #Divisors = $(e_1 + 1) * (e_2 + 1)* ... *(e_k + 1)$
- Sum of Divisors = $((p_1^{(e_1 + 1)}-1)*(p_2^{(e_2 + 1)}-1))*...$

````python
def count_divisors(n):
    cnt = 1
    i = 2
    while i * i <= n:
        power = 0
        while n % i == 0:
            power += 1
            n //= i
        cnt *= (power + 1)
        i += 1
    if n > 1:
        cnt *= 2
    return cnt
````

### Square-Free Numbers

A number is square-free if no prime appears more than once in its factorization.

- 10 : (2, 5) - square free number
- 18 : (3, 3, 2) - not a square free number

Calculate using spf (implemented below) or trial division

## Sieve Techniques

### Sieve of Eratosthenes

* Sieve of Eratosthenes generates primes in $O(n \log \log n)$ 

````c++
// sieve implmentation to generate primes
vector<int> sieve(int N) {
		int i, a[N];
  	for(i = 2; i < N; i++) a[i] = 1;	// set entire array
    for(i=2;i<N;i++) 
        if(a[i])	//takes jumps of j to remove every multiple
            for(int j=i;j*i<N;j++) a[i*j]=0;
    return a;
}
````

### Segmented Sieve

- Used to find primes $[L, R]$ where $R$ is large ( <= 1e12)
- Steps
  - Precompute all primes up to $\sqrt R$ using simple sieve
  - Create a boolean array of size $R-L+1$
  - Mark all multiples of precomputed primes in the range

### Sieve for Smallest/Largest Prime Factors

Useful for fast factorization

````python
N = 10**6
spf = [0] * (N+1)

def compute_spf():
    for i in range(2, N+1):
        if spf[i] == 0:
            for j in range(i, N+1, i):
                if spf[j] == 0:
                    spf[j] = i
````

### Prime Distribution & Number Theorems

- $\pi (n)$ = number of primes $\le n \approx n / \log(n)$ Prime Number Theorem
- There are infinite primes (proved by contradiction - Euclid)

## Diophantine Equations

### Linear Diophantine Equations

**Form:** $ax + by = c$

**Solution exists if:** $\gcd(a, b)$ divides $c$

Find one solution using extended Euclid, then use:

````python
x = x0 + (b/g)*t  
y = y0 - (a/g)*t
````

### Integer Solution using GCD

- If g = gcd(a, b) divides c, then solutions exist.

- Scale extended Euclid’s output to match c/g.

### Application in Modular Inverse

- $a^{(-1)} \mod m$ exists if and only if $\gcd(a, m) == 1$
- Use extended Euclidean algorithm to find it.

````python
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None  # No inverse
    return x % m
````



---

## File: dsa/additional/math2.md

# Modular Arithmetic & Exponentiation

## Core Concepts

$$
\frac{A}{B} = Q\text{ remainder }R
$$

Here, A : dividend, B : divisor, Q : quotient, R : remainder. Sometimes we only wish to calculate the remainder only. For that purpose we use modulo operator. (%)

$A \mod{B} = R$

A *modulo* B is *equal* to R. Here B is referred as the **modulus**.
$$
A \mod{B} = (A + K.B) \mod{B} \text{ for any integer } K
$$

### Congruence Modulo

$$
A \equiv B \mod {C}
$$

Above expression says A is **congruent** to B modulo C.
A common way of expressing two values are in the same **equivalence class**.

e.g. 26 $\equiv$ 11 (mod 5).

- 26 mod 5 = 1
- 11 mod 5 = 1

Both 26 and 11 belong to equivalence class for 1.

### Equivalence Relations

Note following relations.

- $A \equiv B (mod\ C) \\$
- $A \ mod \ C = B \ mod \ C \\$
- C | (A - B)  : ( The | symbol means divide, or is a factor of)
- A  = B + K. C (where K is some integer)

Congruence Modulo is an Equivalence Relation. Follows equivalence property.

- A $\equiv$ A (mod C) (Reflexive)
- if A $\equiv$ B (mod C) then B $\equiv$ A (mod C) (Symmetric)
- if A $\equiv$ B (mod C) and B $\equiv$ D (mod C) then A $\equiv$ D (mod C) (Transitive)

### Quotient Remainder Theorem

Given any integer A, and a positive integer B, there exist unique integers Q and R such that
$$
A = B * Q + R \text{ where } 0 \le R < B
$$
From this form actually imerges **A mod B = R**.

### Modular Properties

- Modular Addition
  - (A + B) mod C = (A mod C + B mod C) mod C
- Modular Subtraction
  - (A - B) mod C = (A mod C - B mod C) mod C
- Modular Multiplication
  - (A * B) mod C = (A mod C * B mod C) mod C
- Modular Exponentiation
  - $A^{B}$ mod C = $(A \mod C)^{B}$ mod C
- Extension of Product property above
  - $(A * B * C)$ mod D = ( ( A mod D) (B mod D) (C mod D) ) mod D

### Modular Exponentiation (Binary Exponentiation)

- How can we calculate $A^B$ mod C quickly when B is a power of 2.
- We can utilize : $A^2$ mod C = ((A mod C) (A mod C))mod C

How about when B is not perfect power of 2 ? i.e. $5^{117}$ mod 19.

- divide B into powers of 2 by writing it in binary
  - 117 : 1110101 in binary = $2^0 + 2^2 + 2^4 + 2^5 + 2^6$ = (1 + 4 + 16 + 32 + 64)
  - $5^{117}$ mod 19 = $(5*5^4*5^{16}*5^{32}*5^{64})$ mod 19


- Calculate mod C of powers of two $\le$ B

- Use modular multiplication properties to combine the calculated mod C values

````python
def mod_exp(a, b, m):
    result = 1
    a %= m
    while b:
        if b & 1:
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1
    return result
````

- RSA, Diffie Hellman
- Competitive Programming Constraints $(1e9+7)$

### Modular Inverse

Inverse : A number multiplied by its inverse gives 1

- Modular Inverse of A (mod C) is A ^ -1.
- (A * A^-1) $\equiv$ 1 (mod C) or equivalent (A * A^-1) mod C = 1.
- Only the numbers coprime to C (numbers that share no prime factors with C) have a modular inverse. (mod C)

Implementation

Find x such that (a * x) % m == 1

1. If m is prime: use **Fermat’s Little Theorem**

   ⇒ a^(m-2) % m

2. If gcd(a, m) == 1: use **Extended Euclidean Algorithm**

````python
def modinv(a, m):
    g, x, _ = extended_gcd(a, m)
    return x % m if g == 1 else None
````

### Modular Division

- To compute: (a / b) % m, use inverse: `(a / b) % m = (a * b^(-1)) % m`
- b must be coprime with m

### Fast Exponentiation Techniques 

Variants:

- **Recursive**: cleaner but risk of stack overflow
- **Iterative**: preferred for tight loops
- **Matrix Exponentiation**: for Fibonacci/DP transitions in O(log n)
- **Modular Exponentiation**: use when modulus is large (1e9+7)



## Theorems & Advanced Techniques

### Fermat’s Little Theorem

If p is prime and a not divisible by p, then:

````python
a^(p−1) ≡ 1 (mod p)
⇒ a^(p−2) ≡ a^(-1) (mod p)
````

Usage:

- Modular inverse when mod is prime
- Simplifying power expressions in mod

### Euler’s Theorem

If a and m are coprime:

````python
a^φ(m) ≡ 1 (mod m)
⇒ a^(φ(m)-1) ≡ a^(-1) (mod m)
````

Works for non-prime m, using **Euler’s Totient $\phi(m)$**

### Wilson’s Theorem

For prime p: `(p−1)! ≡ −1 (mod p)`

Theoretical Interests, rarely used in implementation directly

### Euler’s Totient Function ($\phi (n)$)

$\phi(n)$ = Number of integers <= n that are coprime with n

If $n = p_1^{e_1} *p_2^{e_2} * ... *p_k^{e_k}$ (prime factorization)

````python
φ(n) = n * (1 - 1/p1) * (1 - 1/p2) * ... * (1 - 1/pk)
````

Efficient Implementation

````python
def phi(n):
    res = n
    i = 2
    while i*i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            res -= res // i
        i += 1
    if n > 1:
        res -= res // n
    return res
````

### Chinese Remainder Theorem (CRT)

Solve

````python
x ≡ a1 mod m1  
x ≡ a2 mod m2  
...  
````

Where m1, m2, ... are **pairwise coprime**

- Solution exists & is unique modulo M = m1*m2*...
- Combine equations step by step using extended Euclid

### Modular Arithmetic in Primes vs Non-Primes

| **Feature**         | **Prime Modulus**         | **Non-Prime Modulus**    |
| ------------------- | ------------------------- | ------------------------ |
| Inverses Exist      | If gcd(a, p) = 1 → always | Only if gcd(a, m) = 1    |
| Fermat’s Theorem    | ✅                         | ❌                        |
| Use Euler’s Theorem | ❌                         | ✅                        |
| Simplifications     | Easier (unique fields)    | Harder, may lack inverse |

- Prefer Primes like $1e9+7$ or $998244353$ for programming


---

## File: dsa/additional/math3.md

# Combinatorics & Probability

## Permutation & Combinations

- Permutation (`nPr`) : Number of ways to arrange `r` objects out of `n` distinct objects, order matters.

$$
nPr = \frac{n!}{(n-r)!}
$$

- Combination (nCr) : Number of ways to choose `r` objects out of `n` distinct objects, order doesn’t matter

$$
nCr = \frac{n!}{r!(n-r)!}
$$

## Pascal’s Triangle

- A triangular array where each number is sum of two directly above it
- The `nth` row corresponds to coefficient of $(a+b)^n$
- Properties
  - $\binom{n}{r} = \binom{n-1}{r-1} + \binom{n-1}{r}$
- Symmetry: $\binom{n}{r} = \binom{n}{n-r}$

## Binomial Theorem

- Expansion of $(a + b)^n$

$$
(a+b)^n = \Sigma^{n}_{r=0} \binom{n}{r} a^{n-r} b^r
$$

- Coefficient are binomial coefficient from Pascal’s Triangle

## Stars & Bars

- Technique to find the number of solution to : $x_1 + x_2 + ...+ x_k = n$, $x_i \ge 0$
- Number of solution is : $\binom{n+k-1}{k-1}$
- If $x_i > 0$, then number of solution is : $\binom{n-1}{k-1}$

## Inclusion - Exclusion Principle

- To find the size of the union of sets



## Derangements

- Permutation where no element appears in its original position
- Number of derangements of n objects, denote as $!n$

$$
!n = n!\Sigma^{n}_{k=0} \frac{(-1)^k}{k!}
$$

## Bell, Catalan, Stirling Numbers

- Bell Numbers : Number of ways to partition a set of n elements
- Catalan Number : Number of ways to correctly match parentheses, number of rooted binary trees, etc

$$
C_n = \frac{1}{n+1} \binom{2n}{n}
$$

- Stirling Numbers of the Second Kind: Number of ways to partition $n$ elements into $k$ non-empty subsets

$$
S(n, k)
$$

## Probabilities

### Conditional Probability

$$
P(A|B) = \frac{P(A\cap B)}{P(B)} \text{ if P(B) > 0}
$$



### Bayes’ Theorem

$$
P(H|E) = \frac{P(H)P(E|H)}{P(E)} = \frac{P(H)P(E|H)}{P(H)P(E|H) + P(\overline H)P(E|\overline H)}
$$

- Bayes theorem plays a central role in probability. It improves probability estimates based on evidence.
- Nice Video : [Link](https://www.youtube.com/watch?v=HZGCoVF3YvM)

|                                                              |
| ------------------------------------------------------------ |
| ![image-20250520101004237](./math3.assets/image-20250520101004237.png) |

### Expected Value

- For discrete random Variable $X$

$$
E[X] = \Sigma x_i P(X=x_i)
$$



### Linearity of Expectation

- For any random variables $X, Y$:

$$
E[X+Y] = E[X] + E[Y]
$$



- Holds even if $X, Y$ are dependent

## Radomized Techniques

Discussed in more detail in simulation section

* Monte Carlo Algorithms: Use randomness to get approximate solutions with some probability of error. 
* Las Vegas Algorithms: Always give correct solutions but runtime is random.

## Probabilistic DP & Sampling

- Use probability distributions to handle states in dynamic programming.
- Sampling methods (e.g., Markov Chain Monte Carlo) to estimate quantities when exact computation is hard.

---

## File: dsa/additional/math4.md

# Advanced Math Topics

## Pell’s Equation (Basic Form)

Form:
$$
x^2 - D y^2 = 1
$$

- A special type of Diophantine Equation
- Has integer solution only for non-square D

Approach:

- Use a continued fraction to find its minimal solution
- Once smalled solution $(x_1, y_1)$ is known rest can be generated using

$$
x_{k+1} + y_{k+1}\sqrt D = (x_1 + y_1\sqrt D)^{k+1}
$$

- Used in Number theory problems, math olympiads etc.

## Mobius Function & Inversion Principle

Definition: For integer $n$ define
$$
\mu(n) = \begin{cases}
1 & \text{if } n = 1 \\
(-1)^k & \text{if n is a product of k distinct prime} \\
0 & \text{If n has squared prime factors}
\end{cases}
$$
Properties:

- Used in **inclusion-exclusion**, number-theoretic transforms.
- Appears in **Dirichlet convolution**:

$$
f(n) = \Sigma_{d|n} g(d) \implies g(n) = \Sigma_{d|n} \mu(d) f(\frac{n}{d})
$$

- **Use Case**: Inverting divisor sums, e.g., recovering $\phi(n)$ from sum over divisors.

## Integer Partitions (Combinatorial DP)

Number of ways to write n as sum of positive numbers (order doesn’t matter)

$P(n)$ = partition function

Example

- 4 has 5 partition : 4, 3+1, 2+2, 2+1+1, 1+1+1+1

````python
def partition_count(n):
    dp = [1] + [0] * n
    for i in range(1, n+1):
        for j in range(i, n+1):
            dp[j] += dp[j - i]
    return dp[n]
````

- Used in: DP optimization, partition-related number theory problems.

## Base Conversions & Number Representations

- **Binary**: base 2
- **Octal**: base 8
- **Decimal**: base 10
- **Hexadecimal**: base 16

Conversion Technique

- Decimal → base b: repeated division by b
- Base b → decimal: weighted sum by powers of b

Two’s Complement: Signed binary representation

## Continued Fractions (Optional, for theory-heavy contests)

$$
\text{Definition} = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 + \dots}}
$$

Used in :

- Solving Pell’s Equation
- Approximating Irrational with rational
- Analyzing number properties (e.g. irrationality of $e, \pi$)

Application

- Minimal Solution for Pell’s Equation
- Rational Approximation of $\sqrt D, \pi, e$

---

## File: dsa/additional/matrix1.md

# Matrix Problems

## Matrix Traversal

- SSince travel is possible from any (i, j) position in eight directions, use a direction vector to solve the problem of traversing the matrix efficiently.

### DFS

````c++
vector<vector<int>> dirs = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};

void dfs(vector<vector<int>>& grid, int i, int j, vector<vector<int>>& vis) {
  vis[i][j] = true;
  for(auto dir: dirs) {
    int x = i + dir[0];
    int y = j + dir[1];
    
    if(x < 0 || y < 0 || x >= grid.size() || y >= grid[0].size())
      	continue;
    if(vis[x][y])
      	continue;
    dfs(grid, x, y, vis);
  }
}
````

### BFS

````c++
vector<vector<int>> dirs = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
queue<pair<int, int>> q;
q.push({sr, sc});

while(!q.empty()) {
  auto const &[i, j] = q.front(); q.pop();
	vis[i][j] = true;
  for(auto dir: dirs) {
    int x = i + dir[0];
    int y = j + dir[1];
    
    if(x < 0 || y < 0 || x >= grid.size() || y >= grid[0].size())
      	continue;
    if(vis[x][y])
      	continue;
    q.push({x, y});
  }
}
````

### Spiral

````c++
vector<int> spiralOrder(vector<vector<int>>& matrix) {
    if(matrix.empty()) return {};
    int m = matrix.size(), n = matrix[0].size();
    int top = 0, bottom = m - 1;
    int left = 0, right = n - 1;
    vector<int> result;

    while (top <= bottom && left <= right) {
        // Traverse from left to right
        for (int j = left; j <= right; j++) {
            result.push_back(matrix[top][j]);
        }
        top++;

        // Traverse downwards
        for (int i = top; i <= bottom; i++) {
            result.push_back(matrix[i][right]);
        }
        right--;

        if (top <= bottom) {
            // Traverse from right to left
            for (int j = right; j >= left; j--) {
                result.push_back(matrix[bottom][j]);
            }
            bottom--;
        }

        if (left <= right) {
            // Traverse upwards
            for (int i = bottom; i >= top; i--) {
                result.push_back(matrix[i][left]);
            }
            left++;
        }
    }
    return result;
}
````

A more elegant python solution is to rotate array and consume first row.

````python
def spirallyTraverse(self, matrix):
    result = []
    while matrix:
        result += matrix.pop(0)
        matrix = list(zip(*matrix))[::-1]
    return resul
````

### Zig-Zag

- Pretty Intuitive Traversal



## Matrix Rotation & Transformation

- **Rotation by 90 degrees (clockwise)**
  - For an $n \times n$ matrix \(M\), the element at position $(i, j)$ moves to $(j, n-1-i)$
  - Common approach:
    - **Transpose** the matrix: swap `M[i][j]` with `M[j][i]`
    - **Reverse each row**.
- Rotation by 90 degrees (counter clockwise)
  - Transpose the Matrix
  - Reverse each columns
  - or do the reverse each row, then transpose
- General Transformations
  - Translation
  - Scaling 
  - Rotation by angle $\theta$

## Prefix 2D Sum



````c++
int m = matrix.size();
int n = matrix[0].size();
vector<vector<int>> prefix(m, vector<int>(n, 0));

for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
        int top = (i > 0) ? prefix[i-1][j] : 0;
        int left = (j > 0) ? prefix[i][j-1] : 0;
        int diag = (i > 0 && j > 0) ? prefix[i-1][j-1] : 0;
        prefix[i][j] = matrix[i][j] + top + left - diag;
    }
}
````

### Querying Submatrix Sum

````python
      (r1, c1)
         +---------------+
         |               |
         |     SUM       |
         |               |
         +---------------+
                         (r2, c2)
          
          
total = P[r2][c2]
if r1 > 0: total -= P[r1-1][c2]
if c1 > 0: total -= P[r2][c1-1]
if r1 > 0 and c1 > 0: total += P[r1-1][c1-1]
````

### Application

- Image Processing
- Histogram or Heatmap Analysis
- DP Optimization on 2D Grids

## Binary Search in Sorted Matrix

- Naive Method is to put all numbers in a vector then sort and search.

````python
def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False

    n, m = len(matrix), len(matrix[0])
    low, high = 0, n * m - 1

    while low <= high:
        mid = (low + high) // 2
        row, col = divmod(mid, m)
        mid_val = matrix[row][col]

        if mid_val == target:
            return True
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return False
````

## Pathfinding in Grids

### Dijkstra

````python
import heapq

def dijkstra(grid, start, goal):
    n, m = len(grid), len(grid[0])
    dist = [[float('inf')] * m for _ in range(n)]
    dist[start[0]][start[1]] = 0
    pq = [(0, start[0], start[1])]  # (cost, x, y)
    
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]

    while pq:
        cost, x, y = heapq.heappop(pq)
        if (x, y) == goal:
            return cost
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<m and grid[nx][ny] != -1:
                new_cost = cost + grid[nx][ny]
                if new_cost < dist[nx][ny]:
                    dist[nx][ny] = new_cost
                    heapq.heappush(pq, (new_cost, nx, ny))
    return -1
````

### A*

**Use When:** You want Dijkstra + **heuristics** (e.g., Euclidean or Manhattan distance)

**Guarantees:** Optimal + faster than Dijkstra (if heuristic is admissible)

````python
def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def astar(grid, start, goal):
    n, m = len(grid), len(grid[0])
    open_set = [(0 + manhattan(*start, *goal), 0, start[0], start[1])]  # (f = g + h, g, x, y)
    g_score = [[float('inf')] * m for _ in range(n)]
    g_score[start[0]][start[1]] = 0
    
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]

    while open_set:
        f, g, x, y = heapq.heappop(open_set)
        if (x, y) == goal:
            return g
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<m and grid[nx][ny] == 0:
                ng = g + 1
                if ng < g_score[nx][ny]:
                    g_score[nx][ny] = ng
                    f_score = ng + manhattan(nx, ny, *goal)
                    heapq.heappush(open_set, (f_score, ng, nx, ny))
    return -1
````

## Matrix Exponentiation

https://codeforces.com/blog/entry/67776

- Powerful technique that can be used compute the terms of linear recurrence relations efficiently.
- General Recurrence relation looks like : $f_n = \Sigma^{k}_{i=1} c_i * f_{n-i}$, where $c_i$ could be zero, implying no dependence on that term.
- Let’s consider simple case of $f_n = \Sigma^{k}_{i=n} c_k * f_{n-k}$
- Consider this matrix

$$
T = \begin{bmatrix}
    0 & 1 & 0 & 0 & \dots  \\
    0 & 0 & 1 & 0 & \dots \\
    \vdots & \vdots & \vdots & \vdots & \vdots \\
    c_{k} & c_{k-1} & c_{k-2} & \dots  & c_{1}
\end{bmatrix}
$$



- And the $k * 1$ column vector $F$

$$
F = \begin{bmatrix}
    f_0 \\
    f_1 \\
    f_2 \\
    \vdots \\
    f_{k-1}
\end{bmatrix}
$$

$$
C = T * F = \begin{bmatrix}
    f_1 \\
    f_2 \\
    f_3 \\
    \vdots \\
    f_{k}
\end{bmatrix}
$$

- Its straightforward to see first $k-1$ entries of $C = T * F$. The $k^{th}$ entry is just the calculation of recurrence relation using the past *k* values of the sequence.So, when we obtain $C=T*F$, the first entry gives $f_1$. It is easy to see that $f_n$ is the first entry of the vector: $C_n = T^n * F$(Here $T^n$ is the matrix multiplication of T with itself *n* times).
- Example Matrix for Finbonacci sequence

$$
T = \begin{bmatrix}
    0 & 1 \\
    1 & 1 \\
\end{bmatrix}
$$

- Main Crux of Problem is getting the $T$ matrix
- Problem: Let’s write T, F matrix for $f_n = 2 * f_{i-1} + 3 * f_{i-2} + 4 * f_{i-3}$
- Solution for $f_n = 2 * f_{i-1} + 3 * f_{i-2} + 5$

$$
C = T * F = \begin{bmatrix}
    0 & 1 & 0 \\
    3 & 2 & 5 \\
    0 & 0 & 1
\end{bmatrix} * \begin{bmatrix}
    f_0 \\
    f_1 \\
    1
\end{bmatrix}
$$

- $n^{th}$ term will still be first entry of $C = T^n * F$
- To calculate $T^n$, use the concept of binary exponentiation to calculate it in $O(\log(n))$

## Binary Exponentiation

- This requires two function, one to multiply matrices, and second to perform exponentiation

````python
def mat_mult(A, B, mod=None):
    n = len(A)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res[i][j] += A[i][k] * B[k][j]
                if mod:
                    res[i][j] %= mod
    return res
  
def mat_pow(mat, power, mod=None):
    n = len(mat)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]  # Identity matrix
    while power > 0:
        if power % 2 == 1:
            result = mat_mult(result, mat, mod)
        mat = mat_mult(mat, mat, mod)
        power //= 2
    return result

# finbonacci in O(log n)
def fib(n):
    if n == 0:
        return 0
    base = [
        [1, 1],
        [1, 0]
    ]
    res = mat_pow(base, n - 1)
    return res[0][0]
````

---

## File: dsa/additional/mitmt.md

# Meet-in-the-Middle Technique

- Meet in the Middle is a divide-and-conquer technique, used to reduce complexity of exponential search problems
- Typically when n < 40, where brute force is $O(2^n)$ but we can reduce it by $O(2^{\frac{n}{2}})$
- Especially useful in subset problems, Knapsack, XOR-sum
- We split the input into two halves, solving independently, and combining results
- When to Apply MITM ?
  - While dealing with subset or permutation problems where n is too large for brute force
  - There is **no polynomial-time algorithm**, but a smarter brute-force can be done
  - Splitting data leads to **independent subproblems**

- Steps
  - Split the problem in two halves
  - Enumerate all solution for both halves
  - Combine both using binary search, hashing or two-pointer techniques

## Subset Sum Problem

- given $n \le40$ elements and target sum $S$
- Naive approach of enumeration $2^n$ is too slow
- MITM
  - split into two halves A and B
  - Generate subset sums of both halves : sumA , sumB
  - for each sum in sumA, check if `target-sum` exists in sumB (using binary_search or hashing)
- Time : $O(2^{\frac{n}{2}}) * \log(2^{\frac{n}{2}})$

````python
from bisect import bisect_left

def subset_sum(arr, target):
    n = len(arr)
    half = n // 2
    A, B = arr[:half], arr[half:]

    def get_sums(sub):
        sums = []
        for i in range(1 << len(sub)):
            s = 0
            for j in range(len(sub)):
                if i & (1 << j):
                    s += sub[j]
            sums.append(s)
        return sums

    sa = get_sums(A)
    sb = get_sums(B)
    sb.sort()

    for x in sa:
        if bisect_left(sb, target - x) < len(sb) and sb[bisect_left(sb, target - x)] == target - x:
            return True
    return False
````

## Equal Sum Partition

* Given an array `arr`, determine if it can be partitioned into two subsets with equal sum
* MITM
  * total sum must be even
  * split array into two halves
  * Generate all subset sums for each half
  * Use hashing/binary search to check if any combination sums to `total_sum//2`

````python
def can_partition(arr):
    total = sum(arr)
    if total % 2 != 0:
        return False
    target = total // 2

    n = len(arr)
    half = n // 2
    A = arr[:half]
    B = arr[half:]

    def gen_sums(nums):
        sums = []
        for i in range(1 << len(nums)):
            s = 0
            for j in range(len(nums)):
                if i & (1 << j):
                    s += nums[j]
            sums.append(s)
        return sums

    sumA = gen_sums(A)
    sumB = gen_sums(B)
    setB = set(sumB)

    for sa in sumA:
        if (target - sa) in setB:
            return True
    return False
````

## XOR-based problems (split approach)

- MITM works well for XOR Problems where DP or naive recursion is too slow
- Problem: Count number of subsets where XOR = target
- Steps
  - Split Array
  - Generate all XORs of subsets in both halves
  - Count how many `a xor b == target` using hashmap for one side

````python
from collections import Counter

def count_subsets_xor(arr, target):
    def gen_xors(nums):
        res = []
        for i in range(1 << len(nums)):
            xor = 0
            for j in range(len(nums)):
                if i & (1 << j):
                    xor ^= nums[j]
            res.append(xor)
        return res

    half = len(arr) // 2
    A, B = arr[:half], arr[half:]
    xorsA = gen_xors(A)
    xorsB = gen_xors(B)
    counterB = Counter(xorsB)

    count = 0
    for xa in xorsA:
        count += counterB[xa ^ target]
    return count
````

## 0-1 Knapsack

- Given n items (where n is large) each with a weight `w[i]` and value `v[i]`, and a total capacity `W`, find the max total value we can obtain without exceeding the weight `W`
- Standard DP : $O(n*W)$, which could be quite large when either W or `n` is large
- MITM Steps
  - Split into two halves A and B
  - Generate all subsets of each half with
    - total weight `w`
    - total value `v`
  - For one half, **prune dominated pairs**  (where a subset has both higher weight and lower value)
  - For each subset in one half, find best possible complement in other (with total weight <= W) using binary search

````python
from bisect import bisect_right

def knapsack_mitm(weights, values, max_weight):
    n = len(weights)
    half = n // 2
    A = list(zip(weights[:half], values[:half]))
    B = list(zip(weights[half:], values[half:]))

    def generate_subsets(items):
        subsets = []
        for i in range(1 << len(items)):
            tw = tv = 0
            for j in range(len(items)):
                if i & (1 << j):
                    tw += items[j][0]
                    tv += items[j][1]
            if tw <= max_weight:
                subsets.append((tw, tv))
        return subsets

    sa = generate_subsets(A)
    sb = generate_subsets(B)

    # Prune dominated pairs in sb
    sb.sort()
    pruned_sb = []
    max_val = -1
    for w, v in sb:
        if v > max_val:
            pruned_sb.append((w, v))
            max_val = v

    sb_weights = [w for w, v in pruned_sb]
    sb_values = [v for w, v in pruned_sb]

    ans = 0
    for wa, va in sa:
        remaining = max_weight - wa
        idx = bisect_right(sb_weights, remaining) - 1
        if idx >= 0:
            ans = max(ans, va + sb_values[idx])

    return ans
````

## Double Binary Search

Double Binary Search is used when the **search space is 2D**, or when we must binary search on **both the answer** and **some parameter/condition** inside a decision function. It’s common in optimization problems where:

- The answer isn’t directly numeric, but depends on a function.
- You need to search in a matrix-like domain.

Classical Problems

* Minimum Maximum Distance : Given n points, place k stations such that the **maximum distance** from any point to a station is minimized. 
  * Involves two Binary Search, one of the distance `D`
  * for each `D`, binary search or greedy check if `k` police station can be placed
* Binary Search in Sorted Matrix : Binary Search in two dimensions, could be reduced to one dimension
* Aggressive Cows/Router Placement

## A* Optimization Variant

A* Search is an optimization over Dijkstra’s Algorithm using **heuristics** to guide search. It is used to **speed up shortest-path search** (like in pathfinding).

- `f(n) = g(n) + h(n)`
  - `g(n)` = cost from start to node `n`
  - `h(n)` = estimated cost from node n to goal (heuristic)
  - A* selects the node with smallest `f(n)`

- When using MITM in **graph traversal** or **state space search**, especially when both forward and backward searches are possible, **bidirectional A\*** is a powerful optimization.

- You can simulate A* from both **start and goal** simultaneously, and **meet in the middle**.

````python
# template code
# Pseudocode sketch
A_star_forward(start, goal)
A_star_backward(goal, start)

# Combine states where forward and backward searches meet
for state in visited_forward:
    if state in visited_backward:
        update answer with g1(state) + g2(state)
````

- This helps **cut the search space from exponential to square root** of total size — classic MITM optimization.

---

## File: dsa/additional/simulation.md

# Simulation & Randomized Algorithms

## Game Simulation Problems

* Simulate step-by-step execution of a game scenario or interaction according to predefined rules.
* Example
  * Grid Based Movement
  * Turn-Based Movement
  * Collision Handling
  * Entity Interaction (e.g. player/enemy/item)
* Common Patterns
  * Discrete Time Steps: Update the game state at each tick/turn. Minetest actually has globalstep timer you can utilise.
  * Grid Representation : models position of player, walls, obstacles
  * Entity Queue
  * State Tracking 
  * Rule Engine
* Techniques
  * BFS/DFS for movement (zombie spread, virus simulation)
  * PriorityQueue for ordering actions
  * Coordinate compression or hashing for large boards
  * Bitmasks or flags for power-ups, abilities

### Problems

- [LC 1275: Find Winner on a Tic Tac Toe Game](https://leetcode.com/problems/find-winner-on-a-tic-tac-toe-game/)
- [LC 794: Valid Tic Tac Toe State](https://leetcode.com/problems/valid-tic-tac-toe-state/)
- [LC 1496: Path Crossing](https://leetcode.com/problems/path-crossing/)
- [LC 847: Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)

## Event Based Simulation

* Instead of updating the simulation at every time unit, only process **important events** that change the system. This improves efficiency.
* Idea
  * Maintain a priority queue of events
  * Each event is represented as `(timestamp, event_data)`
  * process events in *chronological order*
  * Each event may generate new future events
* Use Cases
  * systems where actions are sparse in time
  * Real-Time Simulations
  * Traffic/Server Processing Simulation
  * Collision Detection
  * Network Models

````python
import heapq

event_queue = []
heapq.heappush(event_queue, (event_time, event_type, data))

while event_queue:
    time, evt_type, evt_data = heapq.heappop(event_queue)
    
    if evt_type == "MOVE":
        # simulate movement, add next move
        heapq.heappush(event_queue, (time + dt, "MOVE", new_data))
    elif evt_type == "COLLISION":
        # resolve collision
        pass
````

- Check simulation Implementation : https://leetcode.com/problems/minimum-time-to-repair-cars/editorial/

## Cellular Automata (e.g Conway’s Game of Life)

- Deterministic grid-based models used to simulate complex systems using simple local rules.
- **Cellular Automaton (CA)**: A discrete model made up of a regular grid of cells, each in a finite state (e.g., alive/dead or 0/1). The state of each cell evolves based on a fixed rule depending on the states of neighboring cells.
- Neighborhood
  - Moore : 8 neighbours
  - Von Neuman : 4 neighbours (no diagonal)

**Conway’s Game of Life**

A famous 2D cellular automaton invented by John Conway

**Rules**

Each cell is either alive (1) or dead(0) and evolves per these rules

- **Underpopulation**: Any live cell with fewer than 2 live neighbors dies.
- **Survival**: Any live cell with 2 or 3 live neighbors lives on.
- **Overpopulation**: Any live cell with more than 3 live neighbors dies.
- **Reproduction**: Any dead cell with exactly 3 live neighbors becomes alive.

````python
import os
import time

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def game_of_life(board):
    rows, cols = len(board), len(board[0])
    
    def count_live_neighbors(r, c):
        directions = [(-1, -1), (-1, 0), (-1, 1), 
                      (0, -1),         (0, 1), 
                      (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and abs(board[nr][nc]) == 1:
                count += 1
        return count

    # Update in place with markers
    for r in range(rows):
        for c in range(cols):
            live_neighbors = count_live_neighbors(r, c)
            if board[r][c] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                board[r][c] = -1  # alive -> dead
            elif board[r][c] == 0 and live_neighbors == 3:
                board[r][c] = 2   # dead -> alive

    # Final state update
    for r in range(rows):
        for c in range(cols):
            board[r][c] = 1 if board[r][c] > 0 else 0

    return board

start = [
    [0, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 1, 0, 1]
]

for i in range(10):
    clear_console()
    print(f"Generation {i+1}")
    start = game_of_life(start)
    for row in start:
        print(" ".join(map(str, row)))
    time.sleep(2)
````

- Resources : John Conway Interview : [Link](https://www.youtube.com/watch?v=xOCe5HUObD4)

## Random Walks & Probabilistic Modelling

- A **random walk** is a process where an object randomly moves in space (line, grid, graph), often used to model physical or stochastic processes like diffusion, stock prices, or Brownian motion.
- Each step is chosen **randomly** from allowed directions.
- Can be 1D, 2D, or nD.
- Often studied for **expected behavior**, like return-to-origin probability or average distance from start.

**Examples** 

- **1D Random Walk**: Step left or right with equal probability.
- **2D Grid**: Move in 4/8 directions randomly.
- **Markov Chains**: Use transition matrices to describe probabilistic state changes.

**Applications**

- Modeling population movement, chemical diffusion
- Estimating mathematical constants (e.g. Pi)
- Physics (Brownian motion)
- PageRank Algorithm
- Monte Carlo simulations

````python
# Estimate average distance after n steps of a 2D walk.
import random
def random_walk_2D(n):
    x = y = 0
    for _ in range(n):
        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        x += dx
        y += dy
    return (x**2 + y**2) ** 0.5
````

## Monte-Carlo Simulations

- Estimates value using randomness (statistical sampling)
- Use-Cases
  - Pi-estimation using random point in square/circle
  - Probabilistic integral approximation
- Usually steps involved are:
  - Simulate random input based on some distribution
  - Count/Measure successful outcomes
  - Estimate with `success/ total trials`
- Pi-Estimation Using Monte Carlo Method
- The idea is to randomly generate points inside a unit square and count how many fall inside the quarter circle of radius 1. The ratio approximates π/4.

````python
import random

def estimate_pi(num_samples=1_000_000):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x * x + y * y <= 1:
            inside_circle += 1

    return (inside_circle / num_samples) * 4

# Example usage
print("Estimated π:", estimate_pi())
````

- Probabilistic integral approximation
- Estimate definite integrals by sampling random points in the domain.

$$
\int^b_a f(x) dx \sim (b-a).\frac{1}{N} \Sigma^{N}_{i=1} f(x_i)
$$



````python
import random
import math

# Function to integrate
def f(x):
    return math.sin(x)  # ∫₀^π sin(x) dx = 2

def monte_carlo_integral(f, a, b, num_samples=100000):
    total = 0
    for _ in range(num_samples):
        x = random.uniform(a, b)
        total += f(x)
    return (b - a) * (total / num_samples)

# Example usage
result = monte_carlo_integral(f, 0, math.pi)
print("Estimated ∫ sin(x) dx from 0 to π:", result)
````

## Las Vegas Algorithms

- These are dual to Monte-Carlo Simulation
- Las Vegas Algorithm
  - Always give correct answer
  - Runtime is probabilistic
- Examples
  - Randomized Quicksort : Uses randomness to select pivot (Las Vegas — correctness guaranteed)
  - Perfect Hashing : Repeatedly tries seeds to find a collision-free assignment of keys.
- Randomized Quicksort : we randomly choose the pivot each time — the correctness is guaranteed, but performance depends on the pivot quality.

````python
import random

def randomized_quicksort(arr):
    if len(arr) <= 1:
        return arr

    # Las Vegas: randomly choose a pivot
    pivot_index = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_index]

    # Partitioning
    less = [x for i, x in enumerate(arr) if x < pivot and i != pivot_index]
    equal = [x for x in arr if x == pivot]
    greater = [x for i, x in enumerate(arr) if x > pivot and i != pivot_index]

    return randomized_quicksort(less) + equal + randomized_quicksort(greater)

# Example usage
arr = [7, 2, 1, 6, 8, 5, 3, 4]
sorted_arr = randomized_quicksort(arr)
print("Sorted:", sorted_arr)
````

## Random Sampling Algorithm

### Reservoir Sampling

- Randomly pick `k` items from a stream of unknown size
- Time : $O(n)$, Space : $O(k)$
- Formula: Replace element with $i-th$ element with probability $k/i$

````python
import random

def reservoir_sampling(stream, k):
    res = stream[:k]
    for i in range(k, len(stream)):
        j = random.randint(0, i)
        if j < k:
            res[j] = stream[i]
    return res
````

## Randomized Algorithms

- Use randomness to achieve simplicity or performance
- Can be faster or memory efficient
- Las-Vegas & Monte Carlo are two broad types

### Randomized Quicksort/Quickselect

**QuickSort**:

- Pick pivot randomly → reduces chance of worst case

**QuickSelect**:

- Find k-th smallest element with expected O(n) time

### Treaps (Randomized BST)

- Combines BST + Heap
- Each node has a key and random priority
- Maintains BST by key and Heap by priority

**Advantages**:

- Balanced with high probability
- Easy to implement split/merge operations

### Randomized Hashing

- Add randomness to hash functions to reduce collision
- E.g., Polynomial Rolling Hash with random base/mod

**Use Case**:

- Hashing strings in rolling hashes
- Prevent collision attacks in contests

## Hashing & Randomization for Collision Detection

Use **hash functions** (with randomness) to detect collisions efficiently in large datasets or data streams. Randomization helps reduce the chance of adversarial inputs causing worst-case behavior.

### Use Cases

- **Plagiarism detection**: Hash substrings (e.g., Rabin-Karp)
- **Data integrity**: Quick comparison via hashes
- **Hash tables**: Reduce collisions by randomizing the hash function
- **Bloom Filters**: Probabilistic set membership with hash functions

### Randomization

- Randomly select hash seeds or mod values.
- Use **universal hashing**: ensures low collision probability even with bad input.

### Techniques

- Rabin-Karp substring matching
- Zobrist hashing (used in game states)
- Randomly seeded polynomial hashing

````python
# Rabin-Karp
def rabin_karp(text, pattern, base=256, mod=10**9+7):
    n, m = len(text), len(pattern)
    pat_hash = 0
    txt_hash = 0
    h = 1

    for i in range(m-1):
        h = (h * base) % mod

    for i in range(m):
        pat_hash = (base * pat_hash + ord(pattern[i])) % mod
        txt_hash = (base * txt_hash + ord(text[i])) % mod

    for i in range(n - m + 1):
        if pat_hash == txt_hash and text[i:i+m] == pattern:
            return i  # match found
        if i < n - m:
            txt_hash = (base * (txt_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            txt_hash = (txt_hash + mod) % mod  # handle negative values
    return -1
````

## Probabilistic Primality Testing (Miller-Rabin)

Determining whether a number is **prime**, especially large numbers, in an efficient and probabilistic way.

- A **Monte Carlo algorithm**: May give false positives, but with low probability.
- Much faster than deterministic primality tests.
- Based on Fermat’s little theorem.

Concept

* For an odd number n > 2 write : ` n - 1 = 2^s *d`
* Then randomly choose bases `a` and check : `a^d % n == 1 or a^{2^r * d} % n == n-1 for some r in [0, s-1]`. If this fails for any `a`, `n` is composite. If it passes for all `a`, **it’s probably prime**

````python
import random

def is_probably_prime(n, k=5):
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

    # Write n-1 = 2^s * d
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite
    return True  # Probably Prime
````

## State Compression in Simulation

Idea: Encode complex states (grid, position, moves left, etc) into integers or bitmasks

Why ? Reduces memory and improves cache usages

Examples

- `3x3` board can be represented in 9 bits
- Compress states as (x, y, moves_left) into a tuple/int

---

## File: dsa/additional/sparse.md

# Sparse Tables & Range Queries

- A **Sparse Table (ST)** is a **static data structure** used to answer **idempotent range queries** (like min, max, GCD, LCM, XOR, etc.) in **O(1)** time after **O(n log n)** preprocessing.
- Use Cases
  - RMQ
  - Range GCD/LCM
  - Range XOR/AND/OR
  - LCA (Lowest Common Ancestor)
  - Binary Lifting/kth ancestor queries
- This topic is very crucial for competitive coding. Interviews often prefer Segment Trees over these due to their dynamic nature.
- Time Complexity
  - Preprocessing : $O(n \log n)$
  - Query: $O(1)$ for idempotent functions
- Concept:
  - Precompute answers for all intervals of length $2^j$ for all positions.
  - For a function `f` (idempotent) e.g. min, gcd : ` s[i][j] = f(st[i][j-1], st[i + 2^(j-1)][j-1])`
  - Query over the range `[L, R]` becomes

````python
j = log2(R - L + 1)
answer = f(st[L][j], st[R - 2^j + 1][j])
````

### RMQ Example

````python
def build_sparse_table(arr):
    from math import log2, floor
    n = len(arr)
    k = floor(log2(n)) + 1
    st = [[0] * k for _ in range(n)]

    for i in range(n):
        st[i][0] = arr[i]

    j = 1
    while (1 << j) <= n:
        i = 0
        while i + (1 << j) <= n:
            st[i][j] = min(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])
            i += 1
        j += 1
    return st

def query(st, L, R):
    from math import log2, floor
    j = floor(log2(R - L + 1))
    return min(st[L][j], st[R - (1 << j) + 1][j])
````

### Min/Max Example

````python
import math

def build_sparse_table_max(arr):
    n = len(arr)
    max_log = math.floor(math.log2(n)) + 1
    st = [[0] * max_log for _ in range(n)]

    for i in range(n):
        st[i][0] = arr[i]

    for j in range(1, max_log):
        for i in range(n - (1 << j) + 1):
            st[i][j] = max(st[i][j-1], st[i + (1 << (j-1))][j-1])

    return st

def query_max(l, r, st):
    j = math.floor(math.log2(r - l + 1))
    return max(st[l][j], st[r - (1 << j) + 1][j])
  
arr = [1, 3, 2, 7, 9, 11, 3, 5]

st = build_sparse_table_max(arr)

print(query_max(2, 5, st))  # Output: 11
print(query_max(0, 3, st))  # Output: 7
print(query_max(4, 7, st))  # Output: 11
````

### Binary Lifting & Sparse Tables

- Binary lifting is used in tree problems to quickly jump $2^k$ levels in $O(\log N)$
- Preprocess `parent[node][k] = parent[parent[node[k-1]][k-1]`
- Usage
  - Kth Ancestor Query
  - Lowest Common Ancestor (LCA)

### LCA using Sparse Tables (Euler Tour)

- Flatten tree using Euler Tour
- Store depth and first occurrence
- Use RMQ on depth over the Euler array using Sparse Table

````python
import math

class LCA_SparseTable:
    def __init__(self, n, tree):
        self.n = n
        self.tree = tree
        self.euler = []
        self.depth = []
        self.first_occurrence = [-1] * n
        self.visited = [False] * n

        self._dfs(0, 0)  # Root at 0
        self._build_sparse_table()

    def _dfs(self, node, d):
        self.visited[node] = True
        self.first_occurrence[node] = len(self.euler)
        self.euler.append(node)
        self.depth.append(d)

        for neighbor in self.tree[node]:
            if not self.visited[neighbor]:
                self._dfs(neighbor, d + 1)
                self.euler.append(node)
                self.depth.append(d)

    def _build_sparse_table(self):
        m = len(self.depth)
        k = math.floor(math.log2(m)) + 1
        self.st = [[0] * k for _ in range(m)]

        for i in range(m):
            self.st[i][0] = i  # Store index in depth[]

        for j in range(1, k):
            for i in range(m - (1 << j) + 1):
                left = self.st[i][j - 1]
                right = self.st[i + (1 << (j - 1))][j - 1]
                self.st[i][j] = left if self.depth[left] < self.depth[right] else right

    def lca(self, u, v):
        left = self.first_occurrence[u]
        right = self.first_occurrence[v]
        if left > right:
            left, right = right, left

        j = math.floor(math.log2(right - left + 1))
        left_index = self.st[left][j]
        right_index = self.st[right - (1 << j) + 1][j]
        return self.euler[left_index if self.depth[left_index] < self.depth[right_index] else right_index]
````



## Idempotent Function & Their Stability

Only idempotent function work efficiently
$$
f(f(a, b), b) = f(a, b)
$$

- Examples :
  - `min` , `max`
  - `gcd` , `lcm`
  - `XOR`, `AND`, `OR` (XOR is associative but not idempotent, it works)



### Comparison with Segment Tree

| **Feature**       | **Sparse Table**   | **Segment Tree**   |
| ----------------- | ------------------ | ------------------ |
| Query Time        | O(1) (idempotent)  | O(log n)           |
| Update Time       | ❌ (static only)    | ✅ O(log n)         |
| Space             | O(n log n)         | O(4n)              |
| Suitable for      | Static arrays      | Dynamic updates    |
| Common Operations | min, max, GCD, etc | All (with updates) |



### NOTE

**Hybrid Approaches**

- For large inputs, use block partitioning ($\sqrt n$ blocks) combined with Sparse Table for fast queries
- Examples : sqrt decomposition + ST for fast preprocessing & quick queries

**Offline Queries with Sparse Table**

- Useful in offline query prolems (given queries beforehand)
- Sort queries and answer with Sparse Table in O(1)
- Common Usecases
  - Mo’s Algorithm
  - Offline RMQ queries

---

## File: dsa/array/ch1.md

# Two Pointer

* Useful for handling sorted data or searching for pairs, triplets, or subarrays that meet specific conditions
* The core idea is to use two indices that move through the data structure at different speeds or in different directions to narrow the search space.

| Problem Type                        | Description                                                  | Movement Strategy                          |
| ----------------------------------- | ------------------------------------------------------------ | ------------------------------------------ |
| Pair with target sum                | Find two elements summing to a target value in a sorted array | Move left/right pointers inward            |
| Remove duplicates from sorted array | Remove duplicates in-place and return new length             | Slow and fast pointer moving forward       |
| Partition array                     | Rearrange elements based on a pivot                          | Left and right pointers moving inward      |
| Check palindrome                    | Check if a string is palindrome                              | Left and right pointers moving inward      |
| Triplets with zero sum              | Find all unique triplets that sum to zero                    | Fix one pointer, use two pointers for rest |

## Framework to Solve Problems

- Determine if the two-pointer technique applies.

  - Is the array or string sorted? Can it be sorted without violating constraints?
  - Are pairs, triplets, or subarrays required?
  - Can two loops be replaced by two pointers? NOTE: Extra Information by sorted constraint allows us to skip every pair check.

- Initialize the pointers
  - Usually, `l = 0` and `r = n-1` for pairs
  - For windows, `l` and `r` start at `0`

- Pointer moving conditions
  - If `sum` or `constraint` is more, move `r` to reduce it
  - If `sum` or `constraint` is less, move `l` to reduce it
  - For partitioning problems, swap elements and move pointers accordingly

- Stop Conditions : When pointers cross or meet, terminate

## Examples

* Remove Duplicates from Sorted Array In-Place

````c++
int removeDuplicates(vector<int>& nums) {
    if (nums.empty()) return 0;
    int slow = 0;
    for (int fast = 1; fast < nums.size(); fast++) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}
````

* Partition Array Around a Pivot

````c++
void partitionArray(vector<int>& nums, int pivot, int n) {
    int l = 0, r = n - 1;
    while (l <= r) {
        if (nums[l] < pivot) {
            l++;
        } else {
            swap(nums[l], nums[r]);
            r--;
        }
    }
}
````

## Problems

* [2 Sum with sorted Input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)
* [3 Sum](https://leetcode.com/problems/3sum/description/) : we can sort without violating constraint
* [(125) Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)


---

## File: dsa/array/ch2.md

# Sliding Window

All sliding window problems share a basic concept: slide a sub-array (window) linearly from left to right over the original array of \(n\) elements.

## Common Problem Types

1. **find the smallest sub-array size**(smallest window length) such that sum of the sub-array is greater or equal to a certain constant S in O(n).
2. **find the smallest sub-array size**(smallest window length) such that elements inside the sub-array contains all integers in range [1..K].
3. **find the maximum sum** of a certain sub-arry with static size K.
4. **Find the minimum element** in every sub-array of size \(K\) — a classic problem solved efficiently using a deque.

## Solutions

- **Variable Size Window with Sum Constraint**
   - Maintain a window that **grows** by adding elements at the back (right pointer) and **shrinks** by removing elements from the front (left pointer) as long as the running sum meets or exceeds the target \(S\).
   - Continuously update the smallest window length satisfying the condition like `running sum >= S`

- **Variable Size Window with Frequency Constraints**
   - Expand the window until it contains **all required elements** (e.g., all integers in \([1..K]\)).
   - Use a frequency map to track counts of elements inside the window.
   - Shrink the window from the left while maintaining the constraint to find the minimal window.

- **Fixed Size Window for Maximum Sum**
   - Initialize the window with the first \(K\) elements and compute their sum.
   - Slide the window forward by removing the element at the front and adding the next element at the back.
   - Keep track of the maximum sum encountered.

- **Fixed Size Window for Minimum Element (Using Deque)**
   - Use a **deque** to maintain elements in ascending order within the current window.
   - For each new element:
   - Pop elements from the back of the deque while they are larger than the current element to maintain sorting.
   - Add the current element along with its index.
   - Remove elements from the front if they fall outside the current window.
   - The front of the deque always contains the minimum element for the current window.

- this is challenging especially if n is quite large. To get O(n) solution use deque to model the window. this time we maintain that the window is sorted in ascending order, that is front element of deque is minimum. However this changes ordering of elements in the array. To keep track of whether an element is in window or not, we need to remember index of each element too. See example below

````c++
// Type-1
// finding windows with sum == target
int subarraySum(vector<int>& nums, int k) {
    int res = 0, sum = 0;
  	// growing window
    for(int l = 0, r = 0; r < nums.size(); r++) {
        sum += nums[r];
      	// shrinking window
        while(sum > k && l < nums.size()) {
            sum-=nums[l];
            l++;
        }
      	// assess the condition to answer
        if(sum == k)
            res++;
    }
    return res;
}
````

````c++
// Type-4: Minimum in every subarray of size K using deque
void SlidingWindow(int A[], int n, int K) {
    // pair<int,int> represents (value, index)
    deque<pair<int, int>> window;  // maintain ascending order in window
    
    for (int i = 0; i < n; i++) {
        // Remove elements larger than current from the back
        while (!window.empty() && window.back().first >= A[i])
            window.pop_back();
        
        window.push_back({A[i], i});
        
        // Remove elements out of current window from front
        while (window.front().second <= i - K)
            window.pop_front();
        
        // Output minimum for windows starting from index K-1
        if (i + 1 >= K)
            printf("%d\\n", window.front().first);
    }
}
````

## Problems

* [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)
* [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)
* [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)


---

## File: dsa/array/ch3.md

# Prefix Sums & Difference Arrays

Prefix sums and difference arrays are fundamental tools to efficiently handle range queries and range updates on arrays. They help reduce time complexity from $(O(n \times q))$ to $(O(n + q))$ for many problems involving cumulative computations.

## Prefix Sums

### Concept

* Prefix sum array stores cumulative sums of elements up to each index
* For an array `A` of length `n`, prefix sums array `P` is defined as

```python
P[0] = A[0]
for i in range(1, n):
  P[i] = P[i-1] + A[i]
```

* To calculate sum in range `A[l...r]`

```python
def range_sum(P, l, r):
  if l == 0: return P[r]
  return P[r] - P[l-1]
```

* Applications
  * Efficient Range Sum Queries
  * Counting Elements satisfying conditions in ranges
  * Solving problems involving sum of subarrays

## Difference Arrays

### Concept

* A difference array *D* for an array A stores the difference between consecutive elements
* Allows efficient Range Updates: increment all elements in range `[l..r]` by a value `val` in O(1)
* After all updates, original array can be reconstructed by prefix sum of *D*

````python
D[0] = A[0]
for i in range(1, n):
  D[i] = A[i] - A[i-1]
````

### Range Update

* To add a `val` to `A[l...r]`
  * increment `D[l]` by `val`
  * decrement `D[r+1]` by `val` if `r + 1 < n`

```python
D[l] += val
if r + 1 < D.size():
  D[r+1] -= val
```

* Reconstruction
  * Prefix sum array of difference array is exactly same as original array

## Problems

Prefix Sum

* Subarray Sum Equals K (560)
* Range Sum Queries (303)
* [Equilibrium Index](https://www.geeksforgeeks.org/problems/equilibrium-point-1587115620/1)
* Maximum Subarray Sum : Kadane’s Algorithm
* Minimum Size Subarray Sum: Prefix sum with sliding window/binary search
* Counting Zero-Sum Subarrays (325) : Track occurrences of prefix sums using hash maps to count subarrays summing to zero

Difference Array

* Range Updates with Add/Subtract
* **Car Pooling Problem** (1094) : Model pickups/drop-offs using difference arrays
* **Corporate Flight Bookings** (1109) : Apply seat reservations to flight segments and output final seat counts. Difference arrays handle bulk updates efficiently
* Range Addition (370)
* Meeting Room II 

Hybrid Problems

* Product of Array Except Self (238)
* Longest Turbulent Subarray (978)
* Find Pivot Index (724)



---

## File: dsa/array/ch4.md

# Subarrays & Subsequences

* core concepts in problems related to array and string problems
* Its important to understand the difference between them

## Subarrays

* A **subarray** is a contiguous part of an array.
* Formed by selecting a continuous segment `(A[l..r])` where `(0 <= l <= r < n)`

* number of subarrays in an array of `n` size : `n(n+1)/2`
* order of element is preserved and contiguous
* sliding window & prefix sums are important tools to solve subarray related problems

### Common Problems

* Maximum Sum Subarray (Kadane’s Algorithm)
* Counting Subarrays with Certain sum or property
* Longest Subarray with Constraint

### Examples

```c++
// Kadane's Algorithm
int maxSubArray(vector<int>& nums) {
	int n = nums.size(), i ,res = INT_MIN;
	int prev = 0, curr;
  for(i = 1; i <= n; i++){
      curr = max(prev + nums[i-1], nums[i-1]);
      res = max(res,curr);
      prev = curr;
  }
  return res; 
}

// Alternate Implementation
int maxSubArray(vector<int>& nums) {
	int n = nums.size(), i ,res = INT_MIN;
	int sum = 0;
  for(i = 0; i <= n; i++){
		sum += nums[i];
    res = max(res, sum);
    if(sum < 0) sum = 0; // when sum drops negative we will not find better solution by adding more numbers, better to reset
  }
  return res; 
}

// NOTE: Both Implementation works regardless of negative numbers
```

## Subsequences

* sequence derived from the array by deleting zero or more elements without changing the order of remaining elements
* not necessarily contiguous

* number of subsequences in an array of size `n` is `2^n`
* usually these problems are optimally solvable by using DP

### Common Problems

* Longest Increasing Subsquence (LIS)
* Counting subsequences with certain properties
* Subsequences sum problems

```c++
// Example with DP
int lengthOfLIS(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, 1);
    int maxLength = 1;
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[i] > nums[j]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
        maxLength = max(maxLength, dp[i]);
    }
    return maxLength;
}
```

### Problems

Subarrays

Pre-requisite : Prefix and Sliding Window

* Longest Subarray with Given Sum
* Count of Subarrays with Given Sum
* Subarray with Max Product
* Subarray with `k` Distinct Elements
* Longest Ascending(or Descending) Subarray
* Longest Palindromic Subarray
* Fixed-Length Max/Min Subarray

Subsequences

Pre-requsite : Recursion, DP

* LIS (Longest Increasing Subsequence)
* LCS (longest common Subsequences)
* Count Subsequences with Given Property
* Subsequence Matching
* Distinct Subsequences


---

## File: dsa/dp/ch1.md

# 1D DP

### Climbing Stairs

[Problem Link](https://leetcode.com/problems/climbing-stairs/)

* If a person stands at the bottom, he has choice of taking 1 or 2 steps, and he wants to reach to the top (`n th` stairs)
* This problem can easily be modeled using following recursion: `f(n) = f(n-1) + f(n-2)` , which is coincidently fibonacci sequence.
* Solving the above recursion using traditional recursion will result in a time limit exceeded error on any sufficiently capable platform. This problem requires determining the number of ways to solve it, not the specific ways themselves.
* But for solving above problem efficiently we might need to Memoization to store already calculated answers, 

* Splits
  * $x_1$ : ways to reach top floor using 1st floor
  * $x_2$ : ways to reach top floor using 2nd floor
* Recursion : `f(n) = f(n-1) + f(n-2)`
* Base cases: `f(1) = 1, f(2) = 2`

````c++
int climbStairsHelper(int n, vector<int>& dp){
    // base case
    if(n == 1) return 1;
    if(n == 2) return 2;

    // recursive step
    // check the table
    if(dp[n] != -1)
        return dp[n];

    // if not solved
    // solve now and store in table
    dp[n] = climbStairsHelper(n-1,dp) + climbStairsHelper(n-2,dp);
    return dp[n];
}
int climbStairs(int n) {
    vector<int> dp(n+1,-1);
    return climbStairsHelper(n,dp); 
}
````

Recurrence: $O(n^2)$, Memoization: $O(n)$

Now we could have solved same problem from smallest solution to largest then, we don’t even have to check anything. `dp[n]` would simply be the answer

````c++
int climbStairs(int n) {
    if(n == 1) return 1;
    vector<int> dp(n+1,-1);
    dp[1] = 1;
    dp[2] = 2;
    for(int i = 3; i < n+1; i++)
        dp[i] = dp[i-1]+dp[i-2];
    return dp[n];
}
````

Further Optimization can be done upon recognising that we are using only 2 variables to store states. (State Compression)

### House Robber

- [Problem Link](https://leetcode.com/problems/house-robber/)
- Notice how robber can’t rob two adjacent houses. Determing houses he will rob to get maximum money
- Now problem is no longer enumeration (where we could do choice of picking/leaving elements). Here we are given optimization problem and answer is one final answer.
- We can state the problem as, optimal solution either contains $x$ or it does not.
- Say optimal solution is $[H_i, H_j, H_k...]$ we can see that if $H_1$ is part of solution or it is not. dividing problem into two sets.
- Original Problem : $P(A, 0, n-1)$
- Subproblems
  - $p_1$ : $M(H_1) + P(A, 2, n-1)$  // including the H1
  - $p2$ : $P(A, 1, n-1)$ // doesn’t include H1
- Recurrence : $P(A, 0, n-1) = [M(H_1) + P(A, 2, n-1)] + [P(A, 1, n-1)]$
- Above Recurrence, in correct dimensions : $P(A, 0) = max{A(0) + P(A, 2), P(A, 1)}$
- Base Cases: while solving for last 2 elements its nothing but $max{A(n-1), A(n-2)}$ or we can last element `A(n-2)`
- Order of filling could be either direction, problem just flips to prefix in that case.

````c++
//<data-type of ans> f(<Subproblem representation>,<DP table>)
int robHelper(vector<int>& nums,int start,vector<int>& dp){
    int n = nums.size();
    // base cases
    if(start == n-1)
        return nums[n-1];
    if(start == n)
        return 0;
    // check the dp table
    if(dp[start] != -1)
        return dp[start];
    // recursive call
    dp[start] = max(nums[start]+robHelper(nums,start+2,dp),
                    robHelper(nums,start+1,dp));
    return dp[start];  }
int rob(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n+1,-1);
    return robHelper(nums,0,dp); }

````

**Second Approach**

````c++
int rob(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n+1,-1);
    dp[n] = 0, dp[n-1] = nums[n-1];
    for(int i = n-2; i >= 0; i--)
        dp[i] = max(nums[i]+dp[i+2], dp[i+1]);
    return dp[0]; 
}
````

**Second Approach (State Space Optimization)**

````c++
int rob(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(2,-1);
    
    dp[n%2] = 0, dp[(n-1)%2] = nums[n-1];
    for(int i = n-2; i >= 0; i--)
        dp[i%2] = max(nums[i]+dp[(i+2)%2], dp[(i+1)%2]);
    return dp[0%2];
}
````

Solution of Climbing Stairs using this approach : http://p.ip.fi/a6qS

### Problems

* [House Robber II](https://leetcode.com/problems/house-robber-ii/) : Try similar problem with constraint changed.

### Decode Ways

[Problem Link](https://leetcode.com/problems/decode-ways/description/)

* Clearly problem is a counting problem, and we don’t want to enumerate
* DnC Criteria should make solution mutually exclusive and exhaustive
  * $s_1$ : set of all words made by considering only 1st character
  * $s_2$ : set of all words made by considering first 2 characters
* Let’s connect with original subproblem, hint: Suffix Array
* Original Problem: $P(S, 0)$
  * $s_1$ : $P(S, 1)$
  * $s_2$ : $P(S, 2)$
* Recurrence Relation: $P(s, 0) = P(s, 1) + P(s, 2)$
* NOTE: $s_2$ can be pruned while solving the problem as numbers greater than 26 are invalid.

**Bottom Up Solution**

````c++
int numDecodings(string s) {
    int n = s.size();
    vector<int> dp(n);
    dp[n-1] = (s[n-1] == '0') ? 0 : 1;

    for(int i = n-2; i >= 0; i--){
        dp[i] = 0;
        // 2 cases
        // single digit
        if(s[i] != '0')
            dp[i] += dp[i+1];

        // double digit
        if(s[i] =='1' || (s[i] == '2' && s[i+1] <= '6')){
            if(i == n-2)
                dp[i] += 1;
            else 
                dp[i] += dp[i+2];
        }
    }
    return dp[0]; 
}
````

**Simplified Code**

````c++
int numDecodings(string s) {
    int n = s.size();
    vector<int> dp(n+1, 0);
    dp[n] = 1;
    dp[n-1] = (s[n-1] == '0') ? 0 : 1;

    for(int i = n-2; i >= 0; i--){
        if(s[i] != '0')
            dp[i] += dp[i+1];
        if(s[i] =='1' || (s[i] == '2' && s[i+1] <= '6'))
            dp[i] += dp[i+2];
    }
    return dp[0];
}
````

## Advanced 1D DP Problems

* These problems either have Nested Loops, or more than 1 degree of freedom but in a limited capacity (second dimension is small enough to enumerate) 

### Longest Increasing Subsequence (LIS)

- [Problem Link](https://leetcode.com/problems/longest-increasing-subsequence/)

Up until we have looked at subarrays, subsequences are different that subarray, they follow the order they appear in, but not necessarily contigous

1. Modelling the Problem: We have to find $res = max\{s_i\}$, where $s_i$ : Length of LIS ending at $i$
2. Now to find $s_i$ : Length of LIS ending at $i$, we assume that at any $j$, (where $j < i$) If $A[i] > A[j]$ we can extend teh subsequence by 1
3. Recurrence : $S_i = 1 + max_{j \le i} S_j$ and $A[i] > A[j]$
4. Checking DP, Prefix Array with dimension 1, size <- n
5. Base case : `dp[0] = 1`

````c++
int lengthOfLIS(vector<int>& nums) {
    int n = nums.size(),i,j, res = 1;
    vector<int> dp(n,1);

    for(i = 1; i < n; i++){
        // compute dp[i]
        for(j = i-1; j >= 0; j--)
            if(nums[i] > nums[j])
                dp[i] = max(dp[i],1+dp[j]);
        res = max(res,dp[i]);
    }     return res;  
}
````

* Solve Longest Arithmetic Subsequence After this problem

### Word Break

- [Problem Link](https://leetcode.com/problems/word-break/)

All possible splits can be calculated and some will be valid, and some will not be valid. We can have splits at `0, 1, 2, ..., n-1` giving $s_1, s_2, ..., s_n$

given : `catsanddog`, we could split at `[1, 4, 7]` or `[3, 6, 8]` and more...

- Model Problem: $S$ : set of all possible splits
- DnC Criteria: we can mark first split at `0, 1, 2...`, split at some position is i would be $s_i$ , these splits will be mutually exclusive and exhaustive in nature
- We can prune the solution and validate each subproblem as
  - $s_1$ : $A[1...n-1]$ s.t. all words are in dictionary
  - $s_2$ : A[2 ... n-1]
  - Suffix Strings
- We should have split s.t. all words `[0 ... i-1]` for $s_i$ are in dictionary
- Representation : $res = OR\{w[0 ..i-1] \in D \text{ \& } S_i\}$
- $S = w_1 | w_2 | w_3 | ...$
- $D = \{w_1, w_2, w_1w_2\}$
- Order to fill : in backwards, for $j < i$

````c++
bool wordBreak(string s, vector<string>& wordDict) {
    unordered_set<string> dict(wordDict.begin(), wordDict.end());
    int i, j, n = s.size();
    vector<bool> dp(n+1,false);
    dp[n] = true;
    string temp = "";
    for(i = n-1; i >= 0 ; i--){
        //compute s_i
        temp = "";
        for(j = i; j <n; j++){
            temp += s[j];
            if(dict.find(temp) == dict.end())
                continue;
            dp[i] = dp[i] || dp[j+1];

            if(dp[i])
                break;
        }
    }     return dp[0]; 
}
````

* Word - Break II 


---

## File: dsa/dp/ch2.md

# 2D DP

### Best Time to Buy & Sell Stocks with Txn Fee

* [Best Time to Buy and Sell Stocks with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) : might look like above problems but its not because we can sell at will.
* Cue to DP : Maximize profit (try DP!)
* DnC criteria : think about all possible txn, so we can buy on 6th day and sell on 1st day $(b_6, s_1)$, like that there could be many element of the set. Now problem is finding subproblem which provide us mutually exclusive & exhaustive sets.
* We could purchase on first day and don’t buy on first day. Let’s try to related the subproblem to original problem
* Purchase on 0th day
  * $s_1$ : max profite you can make from $D[1... n-1]$, assuming first thing we do is sell $[S_i, (B_j S_k), (B_iS_m)....]$
* Don’t purchase on 0th day
  * $s_2$ : max profit that you can make from $D[1...n-1]$, assuming you start with a buy
* Here we can notice that that there are two degree of freedom making this problem 2D DP

* We will need 2 variable, 1 representing suffix sum & second represent the operation (buy/sell)
* Representation: $f(D, 0, 1, fee)$
  * $s_1$ : $f(D, 1, 0, fee)$
  * $s_2$ : $f(D,1, 1, fee)$
* NOTE: purchase can be represented as negative profit.
* $f(D, 0, 1) = max(-D[0] + f(D,1, 0), f(D, 1, 1))$
* but here there is no way to solve $f(D, 1, 0)$ ? We will need to write another recurrence for it
* $f(D, 0, 0) = max(D[0] + f(D, 1, 1) - fee, f(D, 1, 0))$
* We will have two arrays tracking
  * `n(buy)` : all suffix arrays
  * `n(sell)` : all prefix arrays

````c++
int maxProfit(vector<int>& prices, int fee) {
    int n = prices.size();
    vector<vector<int>> dp(n,vector<int>(2,0));

    // base case
    // 0-> sell
    // 1-> buy
    dp[n-1][0] = prices[n-1] - fee;
    dp[n-1][1] = max(0,-prices[n-1]);

    for(int i = n-2; i >= 0; i--){
            dp[i][0] = max(prices[i] - fee + dp[i+1][1] , dp[i+1][0]);
            dp[i][1] = max(dp[i+1][1], -prices[i]+dp[i+1][0]);
    }

    return dp[0][1];
}
````

### Longest Arithmetic Subsequence

* Nested, 2D DP
* [Problem Link](https://leetcode.com/problems/longest-arithmetic-subsequence/)

1. Modelling the Problem: We have to find $res = max\{s_i\}$, where $s_i$ : length or largest Arithmetic Subsequence ending at $i$
2. Now to find $s_i$ : Assume $j$ for every $j < i$ s.t. common difference `d = A[i] - A[j]` is same.
3. Notice how this requires us to track common difference as well, converting this problem into a 2 DP Problem
4. Dimensions - Prefix Array, Common Difference
5. Data Structure -> use `unordered_map<int,int> `: key -> cd , value -> length of longest chain.

````c++
int longestArithSeqLength(vector<int>& A) {
    int n = A.size(), i, j, cd, res = 0;
    vector<unordered_map < int, int >> dp(n);

    for(i = 0; i < n; i++){
        // compute dp[i]
        for(j = 0; j < i; j++){
            cd = A[i] - A[j];
            if(dp[j].find(cd) == dp[j].end())
                dp[i][cd] = 2;
            else
                dp[i][cd] =  1+dp[j][cd];

            res = max(res,dp[i][cd]); }
    }     return res;  }

````

Above gives TLE : one quick fix is the line after calculating cd , second way using a vector of 1000 size because its possible to get small common  difference .

Maps were giving TLE because , maps are not always O(1) , instead its average case performance.

````c++
int longestArithSeqLength(vector<int>& A) {
    int n = A.size(), i, j, cd, res = 0;
    vector<vector<int>> dp(n, vector<int> (1001,0));

    for(i = 0; i< n; i++){
        // compute dp[i]
        for(j = 0; j < i; j++){
            cd = A[i] - A[j];
            dp[i][cd+500] = max(2,1+dp[j][cd+500]);
            res = max(res,dp[i][cd+500]);
        }
    }     return res; 
}
````

### Target Sum

* [Problem Link](https://leetcode.com/problems/target-sum/description/)
* Subset DP, 2 D DP, Counting Problem
* DnC Criteria : Split the set into 2 components, set $s_1$ contains the sum with $A[0]$ in positive sign while another set $s_2$ with $A[0]$ in negative sign
  * $s_1$ : number of ways to make `target-A[0]` from `A[1...n]`
  * $s_2$ : number of ways to make `target+A[0]` from `A[1...n]`

* Recurrence : $P(A, 0, target) = P(A, 1, target-A[0]) + P(A, 1, target + A[0])$
* Size of DP Array : $n(2 + (\Sigma{A[i] + 1}))$
* To understand the order of filling the table, try to put some value on above recurrence
* Base Case : `n-1` row where the `1` where `target == A[n-1]` otherwise `0`, or using n

````c++
int findTargetSumWays(vector<int>& nums, int target) {
    int n = nums.size(), i, j;
    vector<vector<int>> dp(n+1, vector<int> (2001,0));
    // sum = 0
    // -1000 to 1000 => [0,2000]
    // 0 to 1000
    dp[n][1000] = 1;

    for(i = n-1; i >= 0; i--){
        for( j = -1000; j <= 1000; j++){
            // two cases
            // +ve sign
            if(j+1000-nums[i] >= 0)
                dp[i][j+1000] += dp[i+1][j+1000-nums[i]];

            // -ve sign
            if(j+1000+nums[i] <= 2000)
                dp[i][j+1000] += dp[i+1][j+1000+nums[i]];
        }
    }     return dp[0][target+1000]; 
}
````

* A further state space optimization is possible here by using a 2x(2001) size array

### Edit Distance

* [Problem Link](https://leetcode.com/problems/edit-distance/)
* Famous Problem Commonly Asked in Interviews
* Here, `dp[i][j]` refers to minimum operation needed to convert `s1[0...i]` into `s2[0...j]`
* Given the operations
  * If `s1[i] == s2[j]` then `dp[i][j] = dp[i-1][j-1]`
  * If `s1[i] != s2[j]`
    * `dp[i][j] = dp[i-1][j-1] + 1` : replace operation
    * `dp[i][j] = dp[i][j-1]+1 ` : insertion operation
    * `dp[i][j] = dp[i-1][j]+1 ` : delete operation
    * `dp[i][j]` is minimum of above operation.
* order of filling from top to down and left to right
* Base Case : to  transform [a] into [ab….] if there is a in second word then $n-1$ deletion otherwise $n$. Simpler base case is by shifting everything by one. :)
* we add a row above the table and column of left side too. just to make the base case simpler.

````c++
int minDistance(string word1, string word2) {
    int m = word1.length(),n = word2.length(),i,j;
    vector<vector<int>> dp(m+1, vector<int> (n+1,0));
    // base cases
    for(i = 0 ; i <= n ; i++) dp[0][i] = i;
    for(j = 0 ; j <= m ; j++) dp[j][0] = j;
    // actual DP implemenation
    for(int i = 1 ; i <= m ; i++)
        for(int j = 1 ; j<= n ; j++)
            if(word1[i-1] == word2[j-1]) 
                dp[i][j] = dp[i-1][j-1];
            else
                dp[i][j] = 1 + min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
	return dp[m][n]; 
}
````



### Distinct Subsequences



---

## File: dsa/dp/ch3.md

# Knapsack

## Bounded Knapsack

### Coin Change

* Very Famous & Standard Problem
* Trying to solve this problem greedily fails, Proof by contradiction
  * Example - `[1, 15, 25]` coins, to get a total sum of 30, we will need 1 denomination of 25, and 6 denomination of `1`, A total of 6 coins
  * But optimal solution is to use 2 denomination of 15.
* Split Criteria is we can divide the problem into two subproblems where we take `0` denomination of first coin, other solution is we take more than zero denomination of the first coin
  * $s_1$ : Excluding first coin : $P(A, 1, target)$
  * $s_2$ : Including first coin : $P(A, 0, target-A[0])$ 
* Recurrence : $P(A, 0, target) = min {P(A, 1, target), 1 + P(A, 0, target - A[0])} $
* Clearly its a 2-dimensional DP with a size of `n * (target + 1)`
* Base Case
  * `dp[n][0] = 0`
  * `dp[n][1...target] = INT_MAX` (NOTE: since we are taking min at each step, `INT_MAX` will eventually be replaced)


**Recursive Solution**

````c++
// recursive solution
#include <vector>
#include <climits>
using namespace std;

int coinChangeHelper(const vector<int>& coins, int i, int target, vector<vector<int>>& dp) {
    // base cases
    if (target == 0) return 0;
    if (target < 0 || i >= coins.size()) return INT_MAX;

    if (dp[i][target] != -1)
        return dp[i][target];

    int skip = coinChangeHelper(coins, i + 1, target, dp);
    int take = coinChangeHelper(coins, i, target - coins[i], dp);
    if (take != INT_MAX) take += 1;

    return dp[i][target] = min(skip, take);
}

int coinChange(const vector<int>& coins, int target) {
    int n = coins.size();
    vector<vector<int>> dp(n, vector<int>(target + 1, -1));
    int res = coinChangeHelper(coins, 0, target, dp);
    return (res == INT_MAX ? -1 : res); // -1 if not possible
}
````

**Tabulation Solution**

- From the recurrence we can observe that we can fill 2D Table by filling bottom row, and a column somewhere behind the current element. Bottom to Top & Left to Right.

````c++
int coinChange(vector<int>& coins, int amount) {
    int n = coins.size(), i, j;
    vector<vector<int>> dp(n+1, vector<int>(amount+1,INT_MAX));

    dp[n][0] = 0;
    for(i = n-1; i>= 0; i--){
        for(j = 0; j <= amount; j++){
            dp[i][j] = dp[i+1][j];
            if(j-coins[i] >= 0 && dp[i][j-coins[i]] != INT_MAX)
                dp[i][j] = min(dp[i][j], 1+dp[i][j-coins[i]]);
        }
    }    
  	return dp[0][amount] == INT_MAX ? -1: dp[0][amount];
}
````

* Notice how, `[i]` in the recurrence doesn’t change, that means that it can be state optimized, because we only need one previous row not the entire table.
* [Example Solution](https://algo.minetest.in/Practice_DP/DP_4/)

Further Optimization on Space State could be done using only 1 dimensional table, since states does not depend on some far away row.

````c++
int coinChange(vector<int>& coins, int amount) {
    int n = coins.size(), i, j;
    vector<int> dp(amount+1,INT_MAX);
    dp[0] = 0;
    for(i = n-1; i>= 0; i--)
        for(j = 0; j <= amount; j++)
            if(j-coins[i] >= 0 && dp[j-coins[i]] != INT_MAX)
                dp[j] = min(dp[j], 1+dp[j-coins[i]]);
    return dp[amount] == INT_MAX ? -1: dp[amount];
}
````

**Follow Up**

- Now Try to solve the same problem using following split criteria

  * $s_1$ : picking 1st coin & finding solution

  * $s_2$ : picking 2nd coin & finding solution

  * ...

  * $s_n$

- Recurrence : $P(target) = 1 + \min_{0 \le i \le n}{P(target - A[i])}$
- Base Case:
  - P(0) = 0 (No coins needed to make amount 0)
  - If target < 0, return INT_MAX to signify impossible state

````c++
int coinChangeHelper(const vector<int>& coins, int target, vector<int>& dp) {
    // base cases
    if (target == 0) return 0;
    if (target < 0) return INT_MAX;

    if (dp[target] != -1)
        return dp[target];

    int ans = INT_MAX;
    for (int i = 0; i < coins.size(); ++i) {
        int res = coinChangeHelper(coins, target - coins[i], dp);
        if (res != INT_MAX)
            ans = min(ans, 1 + res);
    }
    return dp[target] = ans;
}

int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, -1);
    int res = coinChangeHelper(coins, amount, dp);
    return res == INT_MAX ? -1 : res;
}
````

Tabulation of Above Method

````c++
int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;

    for (int j = 1; j <= amount; ++j) {
        for (int i = 0; i < coins.size(); ++i) {
            if (j - coins[i] >= 0 && dp[j - coins[i]] != INT_MAX)
                dp[j] = min(dp[j], 1 + dp[j - coins[i]]);
        }
    }
    return dp[amount] == INT_MAX ? -1 : dp[amount];
}
````

### Rod Cutting

## UnBounded Knapsack

### Integer Knapsack (0/1)

* Its quite similar to coin change, but we have to take items such that we get maximum value and capacity less than the max capacity
* Given
  * Items : $I_1 I_2 ...I_n$
  * Value : $v_1, v_2...v_n$
  * Capacity: $c_1, c_2...c_n$
* Criteria: Solving the problem based on whether we get max capacity by including or excluding the first element in the set.
  * $s_1$ : solving knapsack including the item1
  * $s_2$ : solving knapsack including the item2
* Recurrence : $P(A, i, cap) = \max\{v_i + P(A, i+1, cap-c_i), P(A, i+1, cap)\}$

**Tabulation Strategy**

Fill the DP table from the bottom-up:

- Start from i = n-1 down to 0
- Iterate through cap = 0 to W

Order of filling table looks like:

````
Item ⬇️ vs Capacity ➡️ (0...W)
````

### Fractional Knapsack

* Only difference as compared to above problem is that we are now allowed to take fractional parts of an item. We have to maximize the value given total capacity
* Given
  * Items: Each with `value[i], weight[i]`
  * Partial Items can be taken
  * Capacity : `W`
* This is not a DP Problem, Here greedy will work because we can calculate `value[i]/weight[i]` for each item, giving us the optimal choice to pick items.
* Sort the above transformed array and take as much as till `W` is reached.

### Server Problem (0/1) Knapsack

- You have:
  - A list of task sizes: tasks[i] (integers)
  - A **single integer capacity**: C (capacity of **server 0**)
- You need to:
  - **Generate all possible subsets** of tasks (tasks cannot be split).
  - For each subset, compute the **sum of its tasks**.
  - Find the **maximum total task size ≤ C** (that is, the most work server 0 can process **without exceeding** its capacity).
- You’re not required to assign the rest of the tasks or consider other servers.

* Converting to Knapsack
  * Items = tasks
  * Weight = task size
  * Value = same as weight
  * Maximize total weight ≤ capacity C

````c++
int maxSubsetSumWithinLimit(const vector<int>& tasks, int capacity) {
    vector<bool> dp(capacity + 1, false);
    dp[0] = true;  // zero sum is always achievable

    for (int task : tasks) {
        for (int c = capacity; c >= task; --c) {
            dp[c] = dp[c] || dp[c - task];
        }
    }

    for (int i = capacity; i >= 0; --i) {
        if (dp[i]) return i;
    }

    return 0; // no subset possible (should not happen with dp[0] = true)
}
````

- If n is up to **40** and capacity can be up to **1e9 or more**, use **meet-in-the-middle**

### Equal Partition

---

## File: dsa/dp/ch4.md

# Grid DP

### Minimum Path Sum

* [Problem Link](https://leetcode.com/problems/minimum-path-sum/)
* Direction Constraint : down, right only
* We have to minimize the sum along a valid path from `(0,0)` to `(m-1, n-1)`
* Split criteria: Two sets of problems, where we can either take the down or right cell
  * $s_1$ : Min. Path Sum given first step is right step, then solving problem for $P(0, 1)$
  * $s_2$ : Min. Path Sum given first step is right step, then solving problem for $P(1, 0)$
* All matrices are suffix matrix for the original matrix
* Recurrence: $P(0, 0) = min\{P(0, 1), P(1, 0)\} + A[0][0]$
* Its a two dimensional DP, $m*n$
* Base Cases : declare extra column & row with the value `INT_MAX`
* Order to fill the table, bottom to top & right to left

````c++
int minPathSum(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size() ,i ,j ;
    vector< vector<int>> dp(m+1,vector<int>(n+1,INT_MAX));
    dp[m][n-1] = dp[m-1][n] = 0;
    // bottom to top , R to L
    for(i = m-1; i>=0; i--)
        for(j = n-1; j>=0; j--)
            dp[i][j] = grid[i][j] + min(dp[i+1][j],dp[i][j+1]);
    return dp[0][0]; 
}
````

**Space State Optimization**

````c++
int minPathSum(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size() ,i ,j ;
    vector<int> dp(n+1,INT_MAX);
    dp[n-1] = 0;
    // bottom to top , R to L
    for(i = m-1; i>=0; i--)
        for(j = n-1; j>=0; j--)
            dp[j] = grid[i][j] + min(dp[j+1],dp[j]);
    return dp[0]; 
}
````

### Dungeon Game

* [Problem Link](https://leetcode.com/problems/dungeon-game/description/)
* Find a path where the health of knight doesn’t go below zero, 
* Split Criteria
  * $H_1$ : Initial min. Health of knight for rescuing in the box `(0, 1)` to `(m-1, n-1)`
  * $H_2$ : Initial min. Health of knight for rescuing in the box `(1, 0)` to `(m-1, n-1)`
* By definition $H_1 > 0$ & $H_2 > 0$, so `dp[0][0] = val`, so both subproblems will become `H1` is `-6` & `H2` is `-5`, assuming initial health as `val-6` and `val-5` respectively, and it is guaranteed that one path will lead to solution by problem constraint
* Base Case
  * bottom row : $H_1 = \max(H_1 - val, 1)$
  * right column : $H_2 = \max(H_2 - val, 1)$
* Order of filling : B to L & R to L

````c++
int calculateMinimumHP(vector<vector<int>>& dungeon) {
    int m = dungeon.size(), n = dungeon[0].size(), i , j;
    vector<vector<int>> dp(m,vector<int> (n,INT_MAX));
    
    dp[m-1][n-1] = max(1-dungeon[m-1][n-1],1);
    
    for( i = m-1; i >= 0; i--){
        for(j = n-1; j >= 0; j--){
            if(i+1 < m)
                dp[i][j] = min(dp[i][j],
                               dp[i+1][j] - dungeon[i][j]);
            if(j+1 < n)
                dp[i][j] = min(dp[i][j],
                               dp[i][j+1] - dungeon[i][j]);
            dp[i][j] = max(1,dp[i][j]);
        }
    }    
  	return dp[0][0];
}
````

### Unique Paths

* https://leetcode.com/problems/unique-paths/description/

### Frog Jump

* [Problem Link](https://leetcode.com/problems/frog-jump/)
* Split Criteria: at each step we could jump to `k` , `k+1`, `k-1`
* Representation : $P(S_i,k)$ : can we reach the last stone starting from $s_i$ assuming the last jump made was `k`
* Recurrence : $P(s_i, k) = P(s_j, k-1) || P(s_l, k) || P(s_m, k+1)$
* where $s_j = s_i + k - 1$, $s_l = s_i + k$ , $s_m = s_i +k+1$, s : represents the indices
* Size : nxn, max possible jump is `n+1`, order of filling : bottom to top

**TLE Solution**

````c++
bool canCross(vector<int>& stones) {
    if(stones[1]!=1)
        return false;
    int n = stones.size(), i ,j;
    unordered_map<int,int> m;
    vector<vector<bool>> dp(n,vector<bool>(n+1,false));
    // populate the map
    for(i = 0; i <n; i++){
        m[stones[i]] = i;
        dp[n-1][i+1] = true;
    }
    // DP table
    for(i = n-2; i >= 1; i--){
        for(j = 1; j <= n; j++){
            // 3 casese
            if(j > 1 && m.find(stones[i]+j-1) != m.end())
                dp[i][j] = dp[i][j] || dp[m[stones[i]+j-1]][j-1];
            // j
            if(m.find(stones[i]+j) != m.end())
                dp[i][j] = dp[i][j] || dp[m[stones[i]+j]][j];

            // j+1
            if(m.find(stones[i]+j+1) != m.end())
                dp[i][j] = dp[i][j] || dp[m[stones[i]+j+1]][j+1];
        }
    }     
  	return dp[1][1]; 
}
````

* Above solution can be improved by observing that for all the `k` stones we don’t need to store last possible sum
* we need only few `k` values:
* Bottom Up -> always computing all subproblems, Top-Down -> computes only the needed subproblem

**Top-Down Solution Passes**

````c++
bool canCrossHelper(unordered_map<int,int>& m, vector<vector<int>> &dp ,int i, int j , vector<int>& stones){
    int n = stones.size();
    // base case
    if( i == n-1) return true;
    // dp step 
    if(dp[i][j]!= -1) return dp[i][j];
    int t1 = 0, t2=0, t3 = 0;
    // 3 casese
    if(j > 1 && m.find(stones[i]+j-1) != m.end())
        t1 = canCrossHelper(m,dp,m[stones[i]+j-1],j-1,stones);
    // j
    if(m.find(stones[i]+j) != m.end())
        t2 = canCrossHelper(m,dp,m[stones[i]+j],j,stones);
    // j+1
    if(m.find(stones[i]+j+1) != m.end())
        t3 = canCrossHelper(m,dp,m[stones[i]+j+1],j+1,stones);

    dp[i][j] = t1 || t2 || t3;
    return dp[i][j];
}
bool canCross(vector<int>& stones) {
    if(stones[1]!=1)
        return false;
    int n = stones.size(), i ,j;
    unordered_map<int,int> m;
    vector<vector<int>> dp(n,vector<int>(n+1,-1));
    // populate the map
    for(i = 0; i <n; i++){
        m[stones[i]] = i;
    }    
  	return canCrossHelper(m,dp,1,1,stones);
}
````

## Palindrome DP

### Longest Palindromic Subsequences

* [Problem Link](https://leetcode.com/problems/longest-palindromic-subsequence/)
* Check Stone Game Problem : [Link](ch5.md)
* Hint : Recurrence : 
  * Equal : $P(0, n-1) = 2 + P(1, n-2)$
  * Not Equal : $P(0, n-1) = max\{P(1, n-1), P(0, n-2)\}$


````c++
int longestPalindromeSubseq(string s) {
    int n = s.size(), len, i;
    vector<vector<int>> dp(n,vector<int>(n,0));

    // length wise
    for(len = 1; len <= n; len++)
        for(i = 0; i+len-1 < n; i++)
            if(len == 1)
                dp[i][i] = 1;
    		else {
        	// s[i][i+len-1]
        if(s[i] == s[i+len-1])
            dp[i][i+len-1] = 2+(i+1> i+len-2?0:dp[i+1][i+len-2]);
        else
            dp[i][i+len-1] = max(dp[i+1][i+len-1],dp[i][i+len-2]);
    }  
  	return dp[0][n-1]; 
}
````

### Min Cuts for Pal

* [Link](https://leetcode.com/problems/palindrome-partitioning-ii/description/)


---

## File: dsa/dp/ch5.md

# Game DP

### Stone Game

- [Problem Link](https://leetcode.com/problems/stone-game/)
- NOTE: Game’s Outcome is Deterministic !
- The problem's constraints state that both players play optimally. Alex, starting the game, can lock a particular index set (odd or even). Therefore, she knows which index set has the greater sum. Conclude that Alex always wins.
- Solution : `return true;`
- Split Criteria:
  - Original Subproblem : Alex goes first, whether Alex Wins/Losses given `A[0...n-1]`
  - Subsets : Lee goes first, whether Alex wins/losses given `A[1, ... n-1]`
  - If Alex chooses `A[n-1]` , then second config becomes Lee goes first, whether Alex wins/losses given `A[0...n-2]`

- There are 3 dimension to this DP, Its of general subarray type
- 2D Subproblems
- Representation :
  - $p_1$ : $P1(A, i, j)$ Assuming alex goes first
  - $p_2$ : $P2(A, i, j)$ Assuming lee goes first
  - Actual Problem will Alex win if P1 or P2
  - $P1(A, i, j) = P2(A, i+1, j) || P2(A, i, j-1)$

- Problem statement needs to expanded as wee need to keeps score to decide who wins
  - $P1(A,i,j)$ <- Alex - lee score for A[i….j] Assuming Alex goes first
  - $P2(A,i,j)$ <- Alex - lee score for A[i…j] Assuming lee goes first
  - $P1(A,i,j) = max \{A[i] + p_2(A,i+1,j) , A[j] + p2(A,i,j-1) \}$
  - $P2(A,i,j) = max \{  p_1(A,i+1,j)-A[i] , p(A,i,j+1)-A[j] \}$
  - $P(A,i,j)$ : whoever is going first <- $max(S_1 - S_2)$;

- Difference between scores of P1 and P2 assuming P1 goes first.
  - $P(A,i,j) = max \{A[i] - P(A,i+1,j) , A[j] - P(A,i,j-1) \}$

- Repeated Subproblems
- Order to Fill Table
  - Top to Down & left to right, since `i<=j`, we just populate lower triangular matrix

- Base Case: We can fill principle diagonal before using `i=j` we can do `A[i]`

````c++
bool stoneGame(vector<int>& piles) {
    int n = piles.size(), i, j;
    vector<vector<int>> dp(n,vector<int>(n,0));
    // diagonal
    for(i = 0; i <n ; i++) dp[i][j] = piles[i];

    for(i = n-2; i >= 0; i--)
        for( j = i+1; j <n; j++)
            dp[i][j] = max(piles[i]-dp[i+1][j],
                           piles[j] - dp[i][j-1]);
    return dp[0][n-1] > 0; 
}
````

- NOTE : this table can be filled diagonally as well :)

### Predict Winner

### Nim Game

## Interval DP

### Burst Balloons

* [Problem Link](https://leetcode.com/problems/burst-balloons/)
* From the problem we can understand clearly there is an order of popping balloons, which will given you most sum. This is similar to there are multiple path but only 1 is optimal (could be more),
* Problem Space : All permutations of bursting balloons
* Subproblem : $s_1$ : the permutation in which balloon $B_1$ is burst at the end
  * Similarly for $s_2$ , $s_3$, .. $s_n$

* Do not burst the balloon in the middle, as it will remove information about nearby balloons, preventing further query resolution. The balloons are not independent. Select the last balloon to ensure that a balloon exists on the left side.
* Let’s say we burst $B_i$ last
  * then solution becomes : $(B_0 ...B_{i-1}) + (B_{j+1} ... B_{n-1}) + 1 *B_i * 1$

* Recurrence : $dp(i, j) = max_{i \le k \le j} dp(i, k-1) + dp(k-1, j) + A[k]$
* Note: Solution is $O(n^3)$

````c++
int maxCoins(vector<int>& nums) {
    int n = nums.size(), len, i, k, left=1, right=1, left_term, right_term;
    vector<vector<int>> dp(n,vector<int> (n,0));
    // dp
    for(len = 1; len <= n; len++){
        for(i = 0; i+len-1 < n; i++){
            // nums[i][i+len-1]
            for(k = i; k <= i+len-1; k++){
                left = right = 1;
                if(i-1 >= 0) left = nums[i-1];
                if(i+len-1+1 < n) right = nums[i+len-1+1];
                left_term = right_term = 0;
                if(k-1 >= 0) left_term = dp[i][k-1];
                if(k+1 < n) right_term = dp[k+1][i+len-1];
                dp[i][i+len-1] = max(dp[i][i+len-1],
                                     left_term+right_term+
                                     left*nums[k]*right);
            }
        }
    }     
  	return dp[0][n-1]; 
}
````

### Minimum Deletions to make Palindrome

- Problem: Find the minimum number of deletions required to make string palindrome
- Key Insight: The problem could be formulated as a range DP over substrings, where goal is to minimize deletions in the substring `s[i...j]`
- Subproblem: `dp[i][j]` : represents the min deletions required to make substring `s[i...j]` a palindrome
- Base Case
  - If `i == j`, substring of lenght 1 is already a palindrome, return 0
  - if `i > j`, empty substring, so shoudl be zero
  - Transition : if `s[i] == s[j]` then problem is same as solving `dp[i+1][j-1]`
- There are two possibilities to get answer, either delete left character or right character & get minimum

````c++
def minDeletions(s):
    n = len(s)
    dp = [[0]*n for _ in range(n)]

    for i in range(n-1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] if i+1 <= j-1 else 0
            else:
                dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])

    return dp[0][n-1]The question of whether machines can think is about as relevant as the question of whether submarines can swim" Edsger Dijkstra
````

### Matrix Chain Multiplication


---

## File: dsa/dp/ch6.md

# DP on Trees

Used when input is a **tree (acyclic connected graph)** and we need to calculate DP states at each node, often in a **bottom-up (post-order)** or **top-down (rerooting)** fashion.

## Post-order DFS (Bottom Up Tree DP)

We process children first, then compute the parent’s result using children’s DP.

````c++
vector<int> adj[N];
int dp[N];

void dfs(int node, int parent) {
    for (int child : adj[node]) {
        if (child == parent) continue;
        dfs(child, node);
        dp[node] += dp[child];  // Combine child results
    }
    dp[node] += value[node];  // Include current node’s own value
}
````

## Common Patterns

### Subtree Size

````c++
int size[N];

void dfs(int u, int p) {
    size[u] = 1;
    for (int v : adj[u]) {
        if (v == p) continue;
        dfs(v, u);
        size[u] += size[v];
    }
}
````

### Longest Path (Diameter of Tree)

````c++
int diameter = 0;

int dfs(int u, int p) {
    int max1 = 0, max2 = 0;
    for (int v : adj[u]) {
        if (v == p) continue;
        int d = dfs(v, u);
        if (d > max1) {
            max2 = max1;
            max1 = d;
        } else if (d > max2) {
            max2 = d;
        }
    }
    diameter = max(diameter, max1 + max2);
    return max1 + 1;
}
````

## Tree Rerooting (Top-Down Tree DP)

We compute `dp[root]`, then update `dp[child]` by “rerooting” at each child using the parent’s value.

````c++
void dfs1(int u, int p) {
    for (int v : adj[u]) {
        if (v == p) continue;
        dfs1(v, u);
        dp[u] += dp[v] + size[v];
    }
}

void dfs2(int u, int p) {
    for (int v : adj[u]) {
        if (v == p) continue;
        dp[v] = dp[u] - size[v] + (total_nodes - size[v]);
        dfs2(v, u);
    }
}
````

### Problems

**Easy to Medium**

- [**337. House Robber III**](https://leetcode.com/problems/house-robber-iii/) - Classic DP on binary tree. Decide to rob or not rob each node.*(2 states per node: include or exclude)*
- [**110. Balanced Binary Tree**](https://leetcode.com/problems/balanced-binary-tree/) - Simple bottom-up recursion to calculate subtree height.
- [**104. Maximum Depth of Binary Tree**](https://leetcode.com/problems/maximum-depth-of-binary-tree/) - Base DFS post-order depth calculation.
- [**124. Binary Tree Maximum Path Sum**](https://leetcode.com/problems/binary-tree-maximum-path-sum/) - Compute the max path sum going through each node using child contributions.

**Medium to Hard**

- [**979. Distribute Coins in Binary Tree**](https://leetcode.com/problems/distribute-coins-in-binary-tree/) - Pass extra coins up/down tree using post-order traversal.
- [**834. Sum of Distances in Tree**](https://leetcode.com/problems/sum-of-distances-in-tree/) - Tree rerooting technique (top-down DP after bottom-up DP).
- [**968. Binary Tree Cameras**](https://leetcode.com/problems/binary-tree-cameras/) - 3-state DP: covered with camera, covered without camera, not covered.
- [**543. Diameter of Binary Tree**](https://leetcode.com/problems/diameter-of-binary-tree/) -  Standard diameter logic using two max child depths.


---

## File: dsa/dp/ch7.md

# Digit DP

Digit DP is used to count or optimize over **numbers within a range** that satisfy certain properties.

### State Parameters

| **Parameter** | **Meaning**                                |
| ------------- | ------------------------------------------ |
| pos           | Current digit index                        |
| tight         | Whether we’re restricted by upper bound    |
| leading_zero  | Are we still skipping leading 0s           |
| sum / mask    | Any custom condition (sum of digits, etc.) |



### DP Template

````c++
int dp[20][2][2];  // pos, tight, leading_zero

int dfs(int pos, bool tight, bool leading_zero, string &num) {
    if (pos == num.size()) return /* base case */;
    
    if (dp[pos][tight][leading_zero] != -1) return dp[pos][tight][leading_zero];

    int res = 0;
    int limit = tight ? (num[pos] - '0') : 9;

    for (int d = 0; d <= limit; d++) {
        bool new_tight = (tight && d == limit);
        bool new_leading = (leading_zero && d == 0);
        res += dfs(pos + 1, new_tight, new_leading, num);
    }

    return dp[pos][tight][leading_zero] = res;
}
````

**Example: Count numbers with digit sum divisible by k**

````c++
int k;

int dfs(int pos, int sum, bool tight, string &num) {
    if (pos == num.size()) return (sum % k == 0);

    if (dp[pos][sum][tight] != -1) return dp[pos][sum][tight];

    int res = 0;
    int limit = tight ? (num[pos] - '0') : 9;

    for (int d = 0; d <= limit; d++) {
        res += dfs(pos + 1, (sum + d) % k, tight && (d == limit), num);
    }

    return dp[pos][sum][tight] = res;
}
````

To count in range `[L, R]`

````c++
int count(string x) {
    memset(dp, -1, sizeof dp);
    return dfs(0, 0, true, x);
}

int answer = count(R) - count(L - 1);
````

### Common Use Cases

- Count numbers with no repeated digits
- Count numbers with alternating digits
- Count palindromes in a range
- Sum of digits of all numbers in a range

### Problems

Digit DP is often implicit in “count how many numbers” problems involving digit constraints.

**Easy to Medium**

- [**902. Numbers At Most N Given Digit Set**](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/) - Classic Digit DP, counting numbers ≤ N from a set of digits.
- [**233. Number of Digit One**](https://leetcode.com/problems/number-of-digit-one/) - Count number of ‘1’s from 1 to N.
- [**357. Count Numbers with Unique Digits**](https://leetcode.com/problems/count-numbers-with-unique-digits/) - Use bitmask to ensure digit uniqueness.
- [**600. Non-negative Integers without Consecutive Ones**](https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/) - Count integers with no two consecutive 1s in binary representation.

**Medium to Hard**

- [**1012. Numbers With Repeated Digits**](https://leetcode.com/problems/numbers-with-repeated-digits/) - Complement count of numbers with all unique digits using digit DP.
- [**1397. Find All Good Strings**](https://leetcode.com/problems/find-all-good-strings/) - Hard variant combining digit DP and KMP automaton.
- [**6285. Count Beautiful Substrings I**](https://leetcode.com/problems/count-beautiful-substrings-i/) - Newer problem involving constraints on digit patterns.

---

## File: dsa/dp/intro.md

# Dynamic Programming

Key skill to master DP is ability to determine the problem *states* and to determine the relationship or *transitions* between current problems and their sub-problems.

Identify problems related to Dynamic Programming by determining whether the problem can be solved by counting solutions rather than enumeration or involve Optimization. Often, pruning is necessary to obtain the answer within time limits.

If the problem cannot be solved using another technique, dynamic programming must be applied.

### Types of DP Problems

| **Type**               | **Dimension** | **Core Idea / State**                 | **Common Examples**                          | **Techniques**                        |
| ---------------------- | ------------- | ------------------------------------- | -------------------------------------------- | ------------------------------------- |
| **1D DP**              | 1             | Linear state (i)                      | Fibonacci, Climbing Stairs, House Robber     | Simple recurrence, prefix/suffix      |
| **2D DP**              | 2             | Two indices (i, j)                    | LCS, Edit Distance, 0/1 Knapsack             | Nested loops, memo/table              |
| **Grid DP**            | 2 (grid)      | Grid position (i, j) with movement    | Unique Paths, Min Path Sum                   | Directional traversal (right/down)    |
| **Subset DP**          | 2             | Subsets + indices                     | Subset Sum, Target Sum, Count Subsets        | Choose/Skip, Include/Exclude          |
| **Unbounded Knapsack** | 2             | Repeat items, unlimited use           | Coin Change (ways/least), Rod Cutting        | Iterate items, inner loop on total    |
| **Bounded Knapsack**   | 2             | Use each item once                    | 0/1 Knapsack, Equal Partition                | Reverse loops to avoid reuse          |
| **Bitmask DP**         | ≥2            | Set of visited items (mask, pos)      | TSP, Count Valid Words, Assignment Problem   | Bitmasking, memoization               |
| **Tree DP**            | Varies        | DP on tree nodes, subtree aggregation | Tree Diameter, Max Weight Independent Set    | DFS, post-order, rerooting            |
| **Interval DP**        | 2             | Range-based (i to j)                  | Matrix Chain Multiplication, Burst Balloons  | Nested intervals, greedy partition    |
| **Palindrome DP**      | 2             | String substrings                     | Longest Palindromic Subseq, Min Cuts for Pal | Expand from center / DP on substrings |
| **Digit DP**           | Varies        | Positional digits with constraints    | Count ≤ N with X digits, Sum of digits       | pos, tight, leading_zero, memo        |
| **Game DP / Minimax**  | 2+            | Optimal moves between players         | Stone Game, Predict Winner, Nim Game         | Minimax, turn-based state             |
| **Memoization**        | Any           | Recursion + Caching                   | Decode Ways, Unique Paths, Partition Memo    | Top-down recursion + unordered_map    |
| **Tabulation**         | Any           | Bottom-up DP table                    | Most DP problems (as iterative solutions)    | Fill from base cases up               |


---

## File: dsa/dsu.md

# DSU

## Union-Find (Simple)

````c++
class UnionFind {
private:
  vector<int> p;
public:
  UnionFind(int N) {
    p.assign(N, 0); 
    for (int i = 0; i < N; ++i) 
      p[i] = i;
  }

  int findSet(int i) { return (p[i] == i) ? i : (p[i] = findSet(p[i])); }
  bool unionSet(int i, int j) {
    int x = findSet(i), y = findSet(j);
    if(x == y) return false;
    p[x] = y;
    return true;
  }
};
````



## Union-Find (Fastest Implementation)

````c++
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

class UnionFind {                                // OOP style
private:
  vi p, rank, setSize;                           // vi p is the key part
  int numSets;
public:
  UnionFind(int N) {
    p.assign(N, 0); for (int i = 0; i < N; ++i) p[i] = i;
    rank.assign(N, 0);                           // optional speedup
    setSize.assign(N, 1);                        // optional feature
    numSets = N;                                 // optional feature
  }

  int findSet(int i) { return (p[i] == i) ? i : (p[i] = findSet(p[i])); }
  bool isSameSet(int i, int j) { return findSet(i) == findSet(j); }

  int numDisjointSets() { return numSets; }      // optional
  int sizeOfSet(int i) { return setSize[findSet(i)]; } // optional

  bool unionSet(int i, int j) {
    if (isSameSet(i, j)) return false;           // i and j are in same set
    int x = findSet(i), y = findSet(j);          // find both rep items
    if (rank[x] > rank[y]) swap(x, y);           // keep x 'shorter' than y
    p[x] = y;                                    // set x under y
    if (rank[x] == rank[y]) ++rank[y];           // optional speedup
    setSize[y] += setSize[x];                    // combine set sizes at y
    --numSets;                                   // a union reduces numSets
    return true;
  }
};
````

## Applications

* Cycle Detection in Graphs
* Connected Components
* Applications in Network Connectivity

Implementation of Above Application can be found in Graph Section.

---

## File: dsa/graphs/ch1.md

# Graph Properties and Types

Major Application of Graph includes *Maps, Hypertext, Circuits, Schedules, Transactions, Matching, Networks, Program Structure(Compiler).*

## Glossary

***Definition** :* A **graph** is a set of **vertices** and a set of **edges** that connect pairs of distinct vertices ( with at most one edge connecting any pair of vertices ).

$V$: # of vertices/nodes, $E$: number of edges/links

Above definition puts two restrictions on graphs

1. Disallow duplicate edges (*Parallel edges, and a graph that contains them multigraph*)
2. Disallows edges that connect to itself (*Self-Loops*)

***Property 1:*** *A graph with $V$ vertices has at most $V(V-1)/2$ edges.*

When there is a edge connecting two vertices, we say that the vertices are *adjacent* to one another and edges *incident* on it. 

Degree of Vertex: Number of edges incident on it. $v-w$ represents edge from $v$ to $w$ and $w-v$ represents edge from $w$ to $v$.

A *subgraph* is a subset of graph's edges (and associated vertices) that constitutes a graph.

**Same graph represented 3-ways**

![image-20210106085726344](./graphs.assets/image-20210106085726344.png)

A graph is defined by its vertices and its edges, not the way that we choose to draw it.

A *planar graph* is one that can be drawn in the plane without any edges crossing. Figuring out whether a graph is planar or not is a fascinating problem itself. For some graphs drawing can carry information like vertices corresponding points on plane and distance represented by edges are called as *Euclidean graphs.*

Two graphs are *isomorphic* if we can change the vertex labels on one to make its set of edges identical to the other. (Difficult Computation Problem since there are $V!$ possibilities).

**Definition 2: ** *A **path** in a graph is a sequence of vertices in which each successive vertex(after the first) is adjacent to its predecessor in the path.* In a **simple path**, the vertices and edges are distinct. A *cycle* is a path that is simple except that the first and final vertices are the same.

Sometimes we refer *cyclic paths* to refer to a path whose first and last vertices are same; and we use term *tour* to refer to a cyclic path that includes every vertex.

Two simple paths are *disjoint* if they have non vertices in common other than, possibly, their endpoints.

![image-20210106120526277](./graphs.assets/image-20210106120526277.png)

**Definition 3:** A graph is ***connected graph*** if there is a path from every vertex to every other vertex in the graph. A graph that is not connected consists of a set of ***connected components***, which are maximal connected subgraphs.

**Definition 4 :** A acyclic connected graph is called a **tree**. A set of trees is called a **forest**. A **spanning tree** of a connected graph is a subgraph that contains all of that graph's vertices and is a single tree.

A **spanning forest** of a graph is a subgraph that contains all of that graph's vertices and is a forest.

A graph $G$ with $V$ vertices is a tree if and only if it satisfies any of the following four conditions.

- $G$ has $V-1$ edges and no cycles.
- $G$ has $V-1$ edges and is connected
- Exactly one simple path connects each pair of vertices in $G$
- $G$ is connected, but removing any edge disconnects it

Graphs with all edges present are called *complete graphs.*

*Complement of a graph $G$ has same set of vertices as complete graph but removing the edges of $G$*.

Total number of graphs with $V$ vertices is $2^{V(V-1)/2}$. A complete subgraph is called a *clique*.

*density* of graph is average vertex degree or $\frac{2E}{V}$. A *dense graph* is a graph whose density is proportional to $V$. A *sparse graph* is a graph whose complement is dense.

A graphs is dense if $E \propto V^2$ and sparse otherwise. Density of graphs helps us choose a efficient algorithm for processing the graph.

When analysing graph algorithms, we assume $\frac V E$  is bounded above by a small constant, so we can abbreviate expression such as $V(V+E)\approx VE$.

A *bipartite graph* is a graph whose vertices we can divide into two sets such that all edges connect a vertex in one set with a vertex in the other set. Its quite useful in matching problem. Any subgraph of bipartite graph is bipartite.

![image-20210106121534465](./graphs.assets/image-20210106121534465.png)

Graphs defined above are all *undirected graphs*. In *directed graphs*, also know as *digraphs*, edges are one-way. pair of vertices are in form of ordered pairs.

First vertex in digraph is called as *source* and final vertex is called as *destination*.

We speak of *indegree and outdegree* of a vertex ( the #edges where it is destination and #edges where it is source respectively)

A *directed cycle* in a digraph is a cycle in which all adjacent vertex pairs appear in the order indicated by (directed) graph edges

A *directed acyclic graph (DAG)* is digraph that has no directed cycles.

In *weighted graphs we associate numbers (weights) with each edge, denoting cost or distance.*

## Graph Representation

### Edge List

An **edge-list representation** of a graph is a way of representing the edges of a graph as a list of pairs (or tuples) of vertices. Each pair corresponds to an edge in the graph, indicating a connection between two vertices.

* For a **directed graph**, each pair (u, v) in the list represents a directed edge from vertex u to vertex v.

* For an **undirected graph**, each pair (u, v) in the list represents an undirected edge between vertices u and v. (Note: Duplicate or reverse entries, such as (u, v) and (v, u), are often avoided since they represent the same edge.)

This representation is well-suited for **sparse graphs** where the number of edges is much smaller compared to the number of possible edges.

### Adjacency Matrix

An *adjacency-matrix* representation of a graph is matrix of Boolean values, with entry in row and column defined to be 1 if there is an edge connecting vertex and vertex in the graph, and to be 0 otherwise.

This representation is well suited for dense graphs.

NOTE: this matrix will be symmetric for undirected graphs.

![image-20210106152530456](./ch1.assets/image-20210106152530456.png)

````c++
vector<vector<int>> build_adj_matrix(vector<vector<int>> edges, int n) {
    // Assume input: edges = [(u1, v1), (u2, v2), ...], n vertices/nodes
    vector<vector<int>> adj(n, vector<int>(n, 0)); // Create an n x n matrix initialized to 0

    for (auto &[u, v] : edges) {
        adj[u][v] = 1; // From u to v
        adj[v][u] = 1; // From v to u (for undirected graph)
    }

    return adj; // Return the adjacency matrix
}
````

### Adjacency List

Preferred when graphs are not dense, where we keep track of all vertices connected to each vertex on a linked list that is associated with that  vertex. We maintain a vector of lists so that, given a vertex, we can  immediately access its list; we use linked lists so that we can add new  edges in constant time.

Primary advantage is space-efficient structure while disadvantage is time proportional to  for removing a specific edges.

````c++
vector<vector<int>> build_adj_list(vector<vector<int>> edges, int n) {
    // Assume input: edges = [(u1, v1), (u2, v2), ...], n vertices/nodes
    vector<vector<int>> adj(n); // Create an adjacency list with n empty lists

    for (auto &[u, v] : edges) {
        adj[u].push_back(v); // Add v to the adjacency list of u
        adj[v].push_back(u); // Add u to the adjacency list of v (for undirected graph)
    }

    return adj; // Return the adjacency list
}
````

Cost Comparison of these representations

![image-20210106201409694](./ch1.assets/image-20210106201409694.png)

## Simple, Euler and Hamilton Paths

**Simple Path :** Given two vertices, is there a simple path in the graph that connects them ?

* Property: We can find a path connecting two given vertices in a graph in linear time.

**Hamilton Path :** Given two vertices, is there a simple path connecting them that visits every vertex in the graph exactly once ? If the path is from a vertex back to itself, this problem is known as the Hamilton Tour.

* Property: *A recursive search for a Hamilton tour could take exponential time.*

**Euler Path :** Is there a path connecting two given vertices that uses each edge in the graph exactly once ? The path need not be simple - vertices may be visited multiple times. If the path is from a vertex back to itself, we have a Euler tour problem. or Is there a cyclic path that uses each edge in the graph exactly once ?

* *Property :* A graph has an Euler tour if and only if it is connected and all its vertices are of even degree.
* *Corollary :* A graph has an Euler path if an only if it is connected and exactly two of its vertices are of odd degree.
* Property: We can find an Euler tour in a graph, if one exists, in linear time.

## Suggested Reading

[Graph Processing Problems](https://algo.minetest.in/5-Graph_Algorithms/17-Graph-Properties_and_Types/8_Graph-Processing_Problems/)


---

## File: dsa/graphs/ch2.md

# Graph Traversal

## DFS

- traverses graph in 'depth-first' manner
- Time Complexity
  - $O(V+E)$ : Adjacency List
  - $O(V^2)$ : Adjacency Matrix

```c++
const UNVISITED = -1;
const VISITED = 1;

vector<int> dfs_num;				// initially all set to unvisited

void dfs(int u) {
  dfs_num[u] = VISITED;
  for(auto v:adj[u]) {
    if(dfs_num[v] == UNVISITED)
       dfs(v);
  } }
```

[GFG DFS Problem](https://www.geeksforgeeks.org/problems/depth-first-traversal-for-a-graph/1)

[Clone Graph](https://leetcode.com/problems/clone-graph/)

## BFS

- traverses graph in 'breadth-first' manner
- Time Complexity
  - $O(V+E)$ : Adjacency List
  - $O(V^2)$ : Adjacency Matrix

````c++
// inside int main() -- no recursion
  vi d(V,INF); d[s] = 0;					// distance from source s to s is 0
  queue<int> q; q.push(s);

  while(!q.empty()) {
    int u = q.front(); q.pop();
    for(auto v:adj[u]) {
      if(d[v] == INF) {
        d[v] = d[u] + 1;
        q.push(v);
 } } }
````

[GFG BFS Problem](https://www.geeksforgeeks.org/problems/bfs-traversal-of-graph/1)

## Connected Components

- Can be done using Union-Find and BFS also.

````c++
// inside int main()---this is the DFS solution
numCC = 0;
  dfs_num.assign(V, UNVISITED); // sets all vertices’ state to UNVISITED
  for (int i = 0; i < V; i++) // for each vertex i in [0..V-1]
  	if (dfs_num[i] == UNVISITED) // if vertex i is not visited yet
  	printf("CC %d:", ++numCC), dfs(i), printf("\n"); // 3 lines here!
````

https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/description/

## Flood Fill - Labeling/Coloring the Connected Components

This version actually counts the size of each component and colors it.

````c++
int dr[] = {1,1,0,-1,-1,-1, 0, 1}; // trick to explore an implicit 2D grid
int dc[] = {0,1,1, 1, 0,-1,-1,-1}; // S,SE,E,NE,N,NW,W,SW neighbors
int floodfill(int r, int c, char c1, char c2) { // returns the size of CC
  if (r < 0 || r >= R || c < 0 || c >= C) return 0; // outside grid
  if (grid[r][c] != c1) return 0; // does not have color c1
  int ans = 1; // adds 1 to ans because vertex (r, c) has c1 as its color
  grid[r][c] = c2; // now recolors vertex (r, c) to c2 to avoid cycling!
  for (int d = 0; d < 8; d++)
    ans += floodfill(r + dr[d], c + dc[d], c1, c2);
  return ans; // the code is neat due to dr[] and dc[]
}
````

NOTE: this direction traversal can be simple using `vector<vector<int>> dirs` to represent directions to traverse in.

## Cycle Detection
Approach should be based on Graph Type:

* Undirected Graph - *DFS with parent tracking*, *Union-Find*
* Directed Graph - Kahn’s Algorithm, *DFS with recursion Stack*

### DFS on Undirected Graph

**Key Idea**: During DFS, if you encounter a visited vertex that is not the parent of the current vertex (back-edge), a cycle exists.

````c++
bool dfs(int v, int parent, vector<vector<int>> &adj, vector<bool> &visited) {
    visited[v] = true;
    for (int neighbor : adj[v]) {
        if (!visited[neighbor]) {
            if (dfs(neighbor, v, adj, visited))
                return true;
        } else if (neighbor != parent) // back-edge
            return true; // Cycle detected
    }
    return false;
}

bool hasCycleUndirected(vector<vector<int>> &adj, int n) {
    vector<bool> visited(n, false);
    for (int i = 0; i < n; ++i)
        if (!visited[i])
            if (dfs(i, -1, adj, visited))
                return true;
    return false;
}
````

### UNION-FIND TO Detect CyCLES

* NOTE: This is a simplified implementation of Union-Find. Refer [Better Union-Find](ch5.md)

````c++
class UnionFind {
    
public:
    vector<int> p;
    UnionFind(int n) {
        p.resize(n);
        for(int i = 0; i < n; i++)
            p[i] = i;
    }
    int find(int x) {
        if(p[x] != x)
            return p[x] = find(p[x]);	// path compression
        return x;
    }
    bool unite(int x, int y) {
        int px = find(x);
        int py = find(y);
        if(px == py)
            return false;
        p[px] = py;
        return true;
    }
};

// inside main function
bool isCycle(int n, vector<vector<int>>& edges) {
    UnionFind uf(n);
    for(auto e: edges) {
        if(!uf.unite(e[0], e[1]))
            return true;
    }
    return false;
}
````



### Kahn’s Algorithm

* NOTE: Same algorithm with minor changes, can be used to give Topological Order.

````c++
bool hasCycleKahn(vector<vector<int>> &adj, int n) {
    vector<int> inDegree(n, 0);

    // Calculate in-degree
    for (int i = 0; i < n; ++i)
        for (int neighbor : adj[i])
            inDegree[neighbor]++;

  	// put zero-indegree nodes in on queue
    queue<int> q;
    for (int i = 0; i < n; ++i)
        if (inDegree[i] == 0)
            q.push(i);

    int count = 0; // Number of processed nodes
    while (!q.empty()) {
        int v = q.front(); q.pop();
        count++;

        for (int neighbor : adj[v]) {
            inDegree[neighbor]--;
            if (inDegree[neighbor] == 0)
                q.push(neighbor);
        }
    }
    return count != n; // Cycle exists if not all vertices are processed
}
````

### DFS on Directed Graph

we need to keep track of path we used to come to a node. Without recStack, the algorithm cannot identify back edges properly, which are a key indicator of cycles in a directed graph.

In a directed graph, a **back edge** points from a node to one of its ancestors in the current DFS path.

Here visited only keeps track of nodes that have been explored, for example if you again run dfs on different node but come across a node that is visited doesn’t mean it is forming a cycle but rec Stack keeps track of that.

````c++
1 → 2 → 3 → 4
    ↘   ↗
      5
  
// above graph lets say traverses straight from 1->2->3->4->5, marks everything visited.
// when branching again happens at 2, we see wait 3 is marked visited, this should not happen there fore its important to keep track of current path.

bool dfsDirected(int v, vector<vector<int>> &adj, vector<bool> &visited, vector<bool> &recStack) {
    visited[v] = true;
    recStack[v] = true;

    for (int neighbor : adj[v]) {
        if (!visited[neighbor]) {
            if (dfsDirected(neighbor, adj, visited, recStack))
                return true;
        } else if (recStack[neighbor]) {
            return true; // Cycle detected
        }
    }

    recStack[v] = false;
    return false;
}

bool hasCycleDirected(vector<vector<int>> &adj, int n) {
    vector<bool> visited(n, false);
    vector<bool> recStack(n, false);
    for (int i = 0; i < n; ++i)			// check all nodes
        if (!visited[i])
            if (dfsDirected(i, adj, visited, recStack))
                return true;
    return false;
}
````

### Bipartite(or 2/bi-colorable) Graph Check

````c++
bool isBipartite(vector<vector<pair<int, int>>>& adj, int s, int V) {
    queue<int> q;
    vector<int> color(V, -1); // -1 means unvisited
    color[s] = 0; // Start coloring the first node
    q.push(s);
		bool isBipartite = true;
  
    while (!q.empty() && isBipartite) {
        int u = q.front(); q.pop();
        for (auto& v : adj[u]) {
            int neighbor = v.first;
            if (color[neighbor] == -1) { // Unvisited node
                color[neighbor] = 1 - color[u]; // Alternate color
                q.push(neighbor);
            } else if (color[neighbor] == color[u]) {
                isBipartite = false; // Conflict found
                break;
            }
        }
    }
    return isBipartite; // Successfully colored
}
````

### K-Colorable Problem

* general k-Colorable problem is difficult to solve
* DFS/BFS ~ can work for 25 nodes at max
* If a problem can be expressed as a **digital circuit or logic gates**, it can be expressed in **Boolean algebra**, which can be reduced to **SAT (Boolean satisfiability)**, and from there, can often be transformed into a **graph k-coloring** problem (could be come complex).

## Problems on DFS/BFS

| **Problem**                                                                                      | **Concept**                     | **Approach**                                                                                                                                                                                                                          |
|--------------------------------------------------------------------------------------------------|---------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Number of Provinces](https://leetcode.com/problems/number-of-provinces/)                        | DFS on adjacency matrix         | Calculate connected components using a custom DFS implementation. Iterate through unvisited nodes, recursively traverse neighbors via adjacency matrix.                                                                              |
| [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/description/)                    | BFS for shortest path           | Use BFS starting from all rotten oranges simultaneously. Simulate the rotting process and track total and rotten orange counts to determine if any fresh oranges remain disconnected.                                               |
| [Flood Fill](https://leetcode.com/problems/flood-fill/)                                          | BFS / Flood Fill                | Perform BFS to change connected cells to the new color. Use the original color to track visited cells instead of a separate array.                                                                                                  |
| [Course Schedule](https://leetcode.com/problems/course-schedule/description/)                   | Topological Sort (Kahn’s Algo)  | Use Kahn's Algorithm for topological sorting. Challenge: Solve using a DFS approach by detecting cycles in the graph.                                                                                                               |
| [01 Matrix](https://leetcode.com/problems/01-matrix/description/)                                | Modified BFS                    | Initialize BFS from all 0-value cells with a queue storing `{i, j, distance}`. Increment distances during BFS traversal.                                                                                                            |
| [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/description/)              | Boundary DFS/BFS                | Traverse the board boundary and mark connected `O` regions. Any unmarked `O` regions are captured. Ensure comparisons are done on the board's characters.                                                                           |
| [Number of Enclaves](https://leetcode.com/problems/number-of-enclaves/description/)              | Boundary BFS/DFS                | Start BFS from boundary `1`s, marking reachable land cells. Count unmarked `1`s for enclosed regions.                                                                                                                              |
| [Word Ladder](https://leetcode.com/problems/word-ladder/)                                        | BFS with transformation         | Generate all possible transformations of each word in BFS. Use unordered maps to check validity and track visited words.                                                                                                           |
| [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/)                                  | BFS with path reconstruction    | Solve using BFS for shortest path. Use parent tracking for reconstructing paths. Avoid DFS as it explores all paths and may result in TLE.                                                                                         |
| [Is Graph Bipartite](https://leetcode.com/problems/is-graph-bipartite/description/)              | BFS/DFS with color assignment   | Check bipartiteness using BFS/DFS. Assign colors alternately and ensure there are no conflicts. Handle disconnected components by applying the algorithm to all nodes.                                                              |

#### Number of Distinct Islands

This problem requires identifying the shapes of the encountered island. The way to approach this problem is creating a **canonical hash** for the dfs we perform on each island.

Problem: https://leetcode.com/problems/number-of-distinct-islands/

Given a 2D array grid 0’s and 1’s island as a group of 1’s representing land connected by 4-neighbors.

Count number of distinct islands. An island is considered to be same  as another if and only if one island can be translated (and not  rotated/reflected) to equal the other.

Hmm make a island into a string xD and then store it in the map (kind of like serialization) , now for each island check before whether its  stored in map then its not distinct and don’t count it in result.

Now how to serialize : Create a traversal strings representing traversal DRLU representing the down,right,left,up!

````c++
  vector<vector<int>> dirs = {{0, 1, 'R'}, {1, 0, 'U'}, {-1, 0, 'L'}, {0, -1, 'D'}};
  void dfs(vector<vector<int>>& grid, int i, int j, vector<vector<bool>>& visited,string& island){
      visited[i][j] = true;

      for(auto dir: dirs){
          // neighbors
          int x = i + dir[0];
          int y = j + dir[1];

          if(x < 0 || y < 0 || x >= grid.size()||
          y >= grid[0].size()||visited[x][y] || grid[x][y] == 0)
              continue;

          island += dir[2];
          dfs(grid, x, y, visited, island);      
      }
      island+="#";
  }
  int numDistinctIslands(vector<vector<int>>& grid){
      int m = grid.size(), n = grid[0].size(), i, j;
      unordered_set<string> islands;
      vector<vector<bool>> visited(m,vector<bool>(n,false));

      for(i = 0; i< m; i++){
          for(j = 0; j < n; j++)
              if(grid[i][j] == 1 && !visited[i][j]){
                  string island_pattern = "";
                  dfs(grid, i, j, visited, island_pattern);
                  islands.insert(island_pattern);
              }
      }
      return (int) islands.size();
  }
````



---

## File: dsa/graphs/ch3.md

# Digraphs and DAGs

## Definitions

**Definition:** *A **digraph** is a set of **vertices** plus a set of **directed edges** that connect ordered pairs of vertices (with no duplicate edges). We say that an edge goes **from** its vertex **to** its second vertex*

**Definition:** *A **directed path** in a digraph is a list of vertices in which there is a (directed) digraph edge connecting each vertex in the list to its successor in the list. We say that a vertex $t$ is reachable from a vertex $s$ if there is a directed path from $s$ to $t$*.

***sink*** has outdegree 0. and **source** has indegree of 0.

* NOTE: We can easily calculate indegree/outdegree, and find source/sink in linear time and space.

**Definition:** *A **directed acyclic graph (DAG)** is digraph with no directed cycles.*

**Definition:** *A digraph is **strongly connected** if every vertex is reachable from every vertex.*

![image-20241223165121302](./ch3.assets/image-20241223165121302.png)

## DFS in Digraphs

In digraphs, there is a one-to-one correspondence between tree links and graph edges, and they fall into four distinct classes :

- Those representing a recursive call (tree edges)
- Those from a vertex to an ancestor in its DFS tree (back edges)
- Those from a vertex to a descendent in its DFS tree (down edges)
- Those from a vertex to another vertex that is neither an ancestor nor a descendent in its DFS tree (cross edges)

![image-20241223165518350](./ch3.assets/image-20241223165518350.png)

## Reachability and Transitive Closure

**Definition:** *The **transitive closure** of a digraph is a digraph with same vertices but with an edge from s to t in the transitive closure if and only if there is a directed path  from s to t in the given digraph.*

![image-20241223170949138](./ch3.assets/image-20241223170949138.png)

Transitive Closure can be calculated by using $C = A *A^2$ where $A$ is adjacency matrix representation.

We can build transitive closure as

````c++
for(i = 0; i< V; i++)
    for( s = 0 ; s < V; s++)
        for( t = 0; t <V; t++)
            if(A[s][i] && A[i][t]) A[s][t] = 1;
````

**Property:** With Warshall’s algorithm, we can compute the transitive closure of a digraph in time proportional to $V^3$.

A better improvement would be to move `A[s][i]` outside of for loop in a if condition.

There are two important problem which imply us to find better solution to this method.

* (all-pair shortest path)for each pair of vertices, a directed path with minimal number of edges
* solving transitive-closure problem efficiently solves boolean matrix multiplication problem.

NOTE: above problem is just special case of *Floyd’s* Algorithm which finds shortest path in a weighted graph.

## DAGs

* generally used to solve scheduling problem.

**Definition:** *A **binary DAG** is a directed acyclic graph with two edges leaving each node, identified  as the left edge and the right edge, either or both of which may be  null.*

![image-20241223171344720](./ch3.assets/image-20241223171344720.png)

NOTE: only difference between a binary DAGs and Binary tree is that a node can have more than 1 parent.

## Topological Sorting

Goal of topological sorting is to process the vertices of DAG s.t. every vertex is processed before all the vertices to which it points.

**Topological Sort (relabel)** Given a DAG, relabel its vertices such that every directed edge points from a lower-numbered vertex to a higher-number one.

**Topological Sort (rearrange)** Given a DAG, rearrange its vertices on a horizontal line such that all the directed edges points from left to right.

![image-20241223183626572](./ch3.assets/image-20241223183626572.png)

`for(i = 0; i < V; i++) tsI[ts[i]] = i;` defines a relabeling in the vertex-indexed vector.

NOTE: The vertex order produced by a topological sort is not unique.

### DFS Topological Sort

**Property:** *Postorder numbering in DFS yields a reverse topological sort for any DAG.*

````c++
void dfs(int v, vector<vector<int>>& adj, vector<bool>& visited, vector<int>& order) {
    visited[v] = true;
    for (int neighbor : adj[v]) {
        if (!visited[neighbor]) {
            dfs(neighbor, adj, visited, order);
        }
    }
    order.push_back(v); // Add to order after visiting all neighbors (Post-order)
}

vector<int> topologicalSort(int V, vector<vector<int>>& adj) {
    vector<bool> visited(V, false);
    vector<int> order;
    // Perform DFS for each unvisited node
    for (int i = 0; i < V; i++)
        if (!visited[i])
            dfs(i, adj, visited, order)

    // Reverse to get topological sort order
    reverse(order.begin(), order.end());
    return order;
}
````

### Kahn’s Topological Sort

* create a indegree vector while creating graph
* put all the sources onto the queue
* then run BFS from those sources and keep decrementing the indegree as you explore the graph.

````c++
vector<int> kahnTopologicalSort(int numVertices, vector<vector<int>>& edges) {
    // Create adjacency list and indegree vector
    vector<vector<int>> graph(numVertices);
    vector<int> inDegree(numVertices, 0);

    // Populate the graph and indegree vector
    for (auto& edge : edges) {
        graph[edge[0]].push_back(edge[1]); // Directed edge from edge[0] to edge[1]
        inDegree[edge[1]]++;
    }

    // Initialize the queue with nodes having indegree 0
    queue<int> q;
    for (int i = 0; i < numVertices; i++)
        if (inDegree[i] == 0)
            q.push(i);

    vector<int> result; // To store the topological order

    // Process nodes in the queue
    while (!q.empty()) {
        int curr = q.front();
        q.pop();
        result.push_back(curr);

        // Reduce indegree of neighbors by 1
        for (int neighbor : graph[curr]) {
            inDegree[neighbor]--;
            if (inDegree[neighbor] == 0) {
                q.push(neighbor);
            }
        }
    }

    // If all nodes are processed, return the topological order
    if ((int)result.size() == numVertices) {
        return result;
    }

    // If there is a cycle, return an empty vector
    return {};
}
````

## Problems

### Example Problems with Links

| **Problem** | **Concept** | **Approach** |
|-------------|-------------|--------------|
| [Topological Sort](https://practice.geeksforgeeks.org/problems/topological-sort/1) | Standard Topological Sorting. | Use DFS with a stack or Kahn’s Algorithm. |
| [Detect Cycle in a Directed Graph](https://practice.geeksforgeeks.org/problems/detect-cycle-in-a-directed-graph/1) | Cycle Detection in a Directed Graph. | Use recursion stack in DFS or Kahn’s Algorithm to detect cycles. |
| [Course Schedule](https://leetcode.com/problems/course-schedule/) | Check if courses can be completed. | Use Topological Sort to detect cycles. |
| [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Find course completion order. | Use Topological Sort to get a valid order. |
| [Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) | Identify nodes not leading to a cycle. | Reverse the graph, apply Topological Sort on reversed edges, and find nodes with 0 indegree. |
| [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | Determine character order from word precedence. | Construct a graph from word order, apply Topological Sort to find the order. Handle cycles or ambiguity cases. |

### Alien Dictionary

We can represent the problem as directed graph. Now if there is a cycle or self loops then its invalid.

Vertices will be unique characters from the words. After the construction of graph we have to return topological sort of the graph!

Now should we make graph explicitly. Yes indeed because topological sort requires the neighbors but we can't have neighbors through given structure of input and will cost $O(n^2)$ to every letter.

We used the unordered_set just to quickly check whether there is a edge already there.

````c++
class Solution {
public:
  string alienOrder(vector<string>& words) {
      // construct the graph
      // nodes - letters
      // a->b iff a < b
      // Adjacency list.
      unordered_map<char, unordered_set<char>> graph;
      int n = words.size();
      string res = "";
      unordered_map<char, int> indegree;
      // preprocessing step for intializing to empty value
      // if there is some vertex that doesn't get processed 
      // while graph construction i.e. stand alone vertices
      for(int i = 0; i < n; i++){
          for(int k = 0; k < words[i].size(); k++) {
              if(graph.find(words[i][k]) == graph.end()) {
                  graph[words[i][k]] = {};
                  indegree[words[i][k]] = 0;
              }
          }
      }
      // Graph Construction.
      for(int i = 0; i < n; i++){
          for(int j = i+1; j < n; j++){
              // equal words...
              if(words[i] == words[j])
                  continue;

        int k = 0, l = 0;
              while(k < words[i].size() && l < words[j].size()
                   && words[i][k] == words[j][l]){
                  k++;l++;
              }
              // words[j] is a prefix of words[i].
              if(l == words[j].size())
                  return "";

              if(k == words[i].size())
                  continue;

              if(graph[words[i][k]].find(words[j][l]) == 
                                         graph[words[i][k]].end()) {
                  // undirected graph!
                   graph[words[i][k]].insert(words[j][l]);
                  indegree[words[j][l]]++;
              }

          }
      }
      // Topological sort
      queue<char> q;

      // Initialize the queue
      for(const auto& entry:indegree){
          if(entry.second == 0)
              q.push(entry.first);
      }
      while(!q.empty()){
          char ch = q.front();
          q.pop();
          res += ch;
          for(const auto& nbrs: graph[ch]){
              indegree[nbrs]--;
              if(indegree[nbrs] == 0)
                  q.push(nbrs);
          }
      }
      return res.size() == graph.size() ? res : "";
  }
};
````

Improvements : We need to check only consecutive words to create graph.

Because graph captures transitive relation by the fact input is sorted in alien dictionary implying word $ a, b, c$ in order mean $a < b$ and $ b < c$ but that directly implies $ a < c $.

---

## File: dsa/graphs/ch4.md

# Shortest Path

**Definition:** *A **shortest path** between two vertices s and t in a network(weighted digraphs) is a directed simple path from s to t with property that no other such path has a lower weight*.

**Source-sink shortest path** Given a start vertex s and a finish vertex t, find a shortest path in graph from s to t. s-source vertex and t-sink vertex.

**Single-source shortest path** Given a start vertex s, find the shortest path from s to each other vertex in graph.

**All-pairs shortest path** Find the  shortest path connecting each pair of vertices in the graph, we  sometimes use the term *all shortest * to refer to this set of $V^2$ paths.

## Underlying Principle

We apply repeatedly two operations

*Edge relaxation* Test whether travelling along a given edges gives a new shortest path to its destination vertex.

*Path relaxation* Test whether traveling through a given vertex gives a new shortest path connecting two other given vertices.

````c++
if(wt [w] > wt[v] + e->wt()) {	
  wt[w] = wt[v] + e->wt(); // edge-relaxation
  spt[w] = e; // path-relaxation
}
````

**Property:** *If a vertex x is on a shortest  path from s to t, then that path consists of a shortest path from s to x followed by a shortest path from x to t.*

### Dijkstra’s Algorithm (SPSP)

**Property 2:** *Dijkstra’s algorithm solves the single-source shortest-paths* *problem in networks that have **nonnegative weights**.*

Dijkstra’s original implementation, which is suitable for dense  graphs, is precisely like Prim’s MST algorithm. Specifically we simple  change the assignment of priority P from `p=e->wt()` (edge wt) to `p=wt[v]+e->wt()` ( distance from the source to edge’s destination)

**Property 3** *With Dijkstra’s algorithm, we can find any SPT in a dense network in linear time.*

**Property 4** *For all networks and all priority functions, we can compute a spanning tree with PFS in time proportional to the time required for V insert , V delete the minimum , and E decrease key operations in a priority queue of size at most V.*

**Property 5** *With a PFS implementation of Dijkstra’s algorithm that uses  a heap for the priority-queue implementation, we can compute any SPT in time proportional to E lg V.*

````c++
int dijkstra(int V, vector<vector<int>>& edges, int src) {
    // Construct the graph as an adjacency list
    vector<vector<pair<int, int>>> graph(V + 1); // {weight, destination}
    vector<bool> vis(V + 1, false);
    vector<int> dis(V + 1, INT_MAX);
    //$ vector<int> p(int,-1);
    int processed = 0;

    for (const auto& e : edges) {
        graph[e[0]].push_back({e[2], e[1]}); // {weight, destination}
    }

    // Min-heap: stores {distance, vertex}
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;

    // Initialize source node
    pq.push({0, src});
    dis[src] = 0;

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if (vis[u])
            continue;

        vis[u] = true;
        processed++;

        // Relax neighbors
        for (const auto& [w, v] : graph[u]) {
            if (!vis[v] && d + w < dis[v]) {
                dis[v] = d + w;
                //$ p[v] = u;
                pq.push({dis[v], v});
            }
        }
    }

    // Return the maximum shortest distance or -1 if not all vertices are reachable
    return processed == V ? *max_element(dis.begin() + 1, dis.end()) : -1;
}
````

A variant of above algorithm can be used to print the path as well. Uncomment lines `//$`

````c++
vector<int> restore_path(int s, int d, vector<int>& p) {
    vector<int> path;
    for(int v = d; v!=s; v=p[v])
        path.push_back(v);
    path.push_back(s);
    // reverse the path do correct the ordering
    reverse(path.begin(),path.end());
    return path;
}
````

## Floyd-Warshall Algorithm (APSP)

````c++
void floydWarshall(int V, vector<vector<int>>& edges) {
    // Initialize distance matrix
    vector<vector<int>> dis(V, vector<int>(V, INT_MAX));

    // Set diagonal to 0 (distance to itself)
    for (int i = 0; i < V; i++) 
        dis[i][i] = 0;

    // Populate initial distances from edges
    for (const auto& e : edges) 
        dis[e[0]][e[1]] = e[2]; // edge from u to v with weight w

    // Floyd-Warshall algorithm
    for (int k = 0; k < V; k++) {         // Intermediate vertex
        for (int u = 0; u < V; u++) {     // Source vertex
            for (int v = 0; v < V; v++) { // Destination vertex
                if (dis[u][k] != INT_MAX && dis[k][v] != INT_MAX)
                    dis[u][v] = min(dis[u][v], dis[u][k] + dis[k][v]);
            }
        }
    }
}
````

## Bellman Ford Algorithm

- Used to find the shortest path from a source node to all other nodes in a **graph**, even if there are negative edge weights.

* **Key Features**:
  * Works for both **directed** and **undirected** graphs.
  * Handles **negative edge weights**, unlike Dijkstra’s algorithm.
  * Can also detect **negative weight cycles** in the graph.
  * Time Complexity: $O(V \times E)$, where V is the number of vertices and E is the number of edges.

````c++
vector<int> bellmanFord(int V, int E, vector<Edge>& edges, int source) {
    // Initialize distances from the source
    vector<int> dist(V, INT_MAX);
    dist[source] = 0;

    // Relax edges V-1 times
    for (int i = 1; i < V; ++i) {
        for (const auto& edge : edges) {
            int u = edge.u;
            int v = edge.v;
            int w = edge.weight;

            // If the distance to the destination vertex is greater
            // through the current edge, update the distance
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }

    // Check for negative weight cycles
    for (const auto& edge : edges) {
        int u = edge.u;
        int v = edge.v;
        int w = edge.weight;

        // If the distance can still be minimized, it means there's a negative cycle
        if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
            cout << "Graph contains negative weight cycle!" << endl;
            return {};  // Return an empty vector to indicate a negative cycle
        }
    }

    return dist;  // Return the shortest distances from the source
}
````

### Other Applications

#### Solving SSSP Problem on Small Weighted Graph

If we have the APSP information we also know the SSSP information.

Printing Shortest Path

A common issue encountered by programmers who use four-liner Floyd Warshall’s without understanding how it works is when they are asked to print shortest paths too. In BFS/Dijkstra’s/ Bellman Ford’s algorithm we just need to remember the shortest paths spanning tree by using a 1D vector to store parent information for each vertex. In Floyd Warshall’s we need to store a 2D parent matrix. The modified code is as

````c++
for(int i = 0; i < V; i++)
  for(int j = 0; j < V; j++)
    p[i][j] = i; // initialize the parent matrix
for(int k = 0; k < V; k++)
  for(int i = 0; i < V; i++)
    for(int j = 0; j < V; j++)
      if(adj[i][k] + adj[k][j] < adj[i][j) {
        adj[i][j] = adj[i][k] + adj[k][j];
        p[i][j] = p[k][j];
      }
//------------------------------------------------------
void printPath(int i, int j) {
  if(i!=j) printPath(i,p[i][j]);
  printf(" %d", j);
}
````

#### Transitive Closure (Warshall’s Algorithm)

Given a graph, determine if vertex i is connected to j, directly or indirectly. This variant uses bitwise operators which are much faster than arithmatic operators.

Initially set entire adj to 1 if i connected to j otherwise 0.

After running Floyd’s Algorithm we can check if any two vertices are connected by check adj matrix

````c++
for(int k = 0; k < V; k++)
  for(int i = 0; i < V; i++)
    for(int j = 0; j < V; j++)
      adj[i][j] != (adj[i][k] & adj[k][j]);
````

#### Minimax and Maximin

We have seen the minimax(and maximin) path problem earlier. The solution using Floyd Warshall’s is shown below. First intialize `adj[i][j]` to be the weight of edge (i,j). This is default minimax cost for two vertices that are directly connected. For pair i-j without any direct edge, set `adj[i][j] = INF`. Then we try all possible intermediate vertex k. The minimax cost `adj[i][j]` is minimum of either (itself) or (the maximum between `adj[i][k]] or adj[k][j]`) However this approach works only for  V $\le$ 400.

````c++
for (int k = 0; k < V; k++)
	for(int i = 0; i < V; i++)
		for(int j = 0; j < V; j++)
			adj[i][j] = min(adj[i][j], max(adj[i][k],adj[k][j]))
````

#### Finding the Cheapest/Negative Cycle

We know Bellman Ford will terminate after O(VE) steps regardless of the type of input graph, same is the case with Floyd Warshall it terminates in $O(V^3)$.

To solve this problem, we intially set the main diagonal of the adj matrix to a very large value, i.e. `adj[i][i] = INF`, which now mean shortest cyclic paht weight strating from vertex i goes thru up to V-1 other intermediate vertices and return back to i. If `adj[i][i]` is no longer INF for any $i \in [0…V-1]$, then we have a cycle. The smallest non-negative `adj[i][j]` $\forall i \in [0…V-1]$ is the cheapest cycle.

If `adj[i][j]` < 0 for any $i \in [0…V-1]$, then we have a negative cycle because if we take this cyclic path one more time, we will get even shorter `shortest` path.

#### Finding the Diameter of a Graph

The diameter is maximum shortest path distance between any pair, just find the i and j s.t. its maximum of the matrix adj.

#### Finding the SCCs of a Directed Graph

Tarjan’s algorithm can be used to identify SCCs of a digraph. However code is bit long. If input graph is small, we can also identify the SCCs of graph in $O(V^3)$ using Warshall’s transitive closure algorithm and then use the following check.

 To find all the members of SCC that contains vertex i check all other vertices $V\in [0…V-1]$. If `adj[i][j] && adj[j][i]` is true, then vertex i and j belong to same SCC.

## Summary

| Algorithm      | Graph Type          | Complexity            | Special Features                         |
| -------------- | ------------------- | --------------------- | ---------------------------------------- |
| BFS            | Unweighted          | \(O(V + E)\)          | Layer-by-layer exploration               |
| Dijkstra       | Weighted (Non-Neg.) | \(O((V + E) \log V)\) | Priority queue-based; greedy approach    |
| Bellman-Ford   | Weighted (Neg.)     | \(O(V \times E)\)     | Handles negative weights; detects cycles |
| Floyd-Warshall | Small Graphs/APSP   | \(O(V^3)\)            | Solves all-pairs shortest paths          |

## Problems

1. https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph-having-unit-distance/1 NOTICE few things, first there is no need to track visited since in undirected grpah it processes layer by layer, its a special case of floyd warshal which is special case PFS.
2. https://www.geeksforgeeks.org/problems/shortest-path-in-undirected-graph/1 NOTICE NOW we need visited array to for safeguard and efficiency. Try removing it and see memory comparisons.
3. https://www.geeksforgeeks.org/problems/implementing-dijkstra-set-1-adjacency-matrix/1 for fun try to use set for this approach to implement dijkstras

| **Aspect**               | **Priority Queue**                              | **Set**                                                                 |
|--------------------------|-------------------------------------------------|-------------------------------------------------------------------------|
| **Insertion Time**        | \( $O(\log N)$ \)                               | \( $O(\log N)$ \)                                                      |
| **Update Time**           | Not supported directly; push new value instead | \( $O(\log N)$ \): Remove old value, insert new value                  |
| **Deletion Time**         | \( $O(\log N)$ \)                             | \( $O(\log N)$ \)                                                      |
| **Ease of Implementation**| Simple (standard libraries like `priority_queue`)| More complex, as updates require additional operations                 |
| **Duplicates**            | Allows duplicates                               | Does not allow duplicates                                              |
| **Space Usage**           | May grow larger due to duplicate entries        | Minimal, as it keeps only one instance of each node                    |
| **Efficiency in Practice**| Generally faster due to less overhead           | Slightly slower for the same operations due to extra bookkeeping       |

4. https://leetcode.com/problems/shortest-path-in-binary-matrix/ Now it maybe tempting to store all distances but the quesiton only ask for a specific target, so try to optimize space without using matrix to store all distances.
5. https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/ The best solution would be to keep track of number of ways in an array ways and increment each time your traverse priority queue.

6. https://leetcode.com/problems/path-with-minimum-effort/description/ This problem requires to drive dijkstra in the direction where the abs difference encountered so far is minimum, so our priority function changes here.

7. https://leetcode.com/problems/network-delay-time/description/ This is straightforward question find all distances and then find the longest distance from the dist array.

8. https://www.geeksforgeeks.org/problems/minimum-multiplications-to-reach-end/1 This problem does have any graph structure and we don’t actually need to create the graph, its an application of PFS (doesn’t really matter as PFS function is not obvious). Think of it as a graph with 1e5 nodes and you are traversing using multiplication rules.

9. https://leetcode.com/problems/cheapest-flights-within-k-stops/ Cheapest flight with K stops, this is important question look at DFS solution presented as well.

````c++
    int dfs(vector<vector<pair<int,int>>> &graph, vector<vector<int>> &vis, int i, int dst, int k) {
        if(i == dst){
            return 0;
        }
        if(k < 0) {
            return INT_MAX;
        }
        if(vis[i][k] != 0) {
            return vis[i][k];
        }

        int cost = INT_MAX;
        for(auto nbr: graph[i]) {
            int next = nbr.first;
            int weight = nbr.second;
            int subproblem = dfs(graph, vis, next, dst, k - 1);
            if (subproblem != INT_MAX) {
                cost = min(cost, weight + subproblem);
            }
        }
        return vis[i][k] = cost;

    }
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        // looks like a weighted graph with bfs
        // vector<vector<pair<int,int>>> graph(n);
        unordered_map<int, vector<pair<int,int>>> graph;


        // construct graph
        for(auto f : flights) {
            graph[f[0]].push_back({f[1],f[2]});
        }

        // ----------- bfs ----------
        queue<pair<int,int>> q;
        vector<int> dist(n+1, INT_MAX);
        dist[src] = 0;
        q.push({src,0});
        while(!q.empty() && k >= 0) {
            // travel all current level nodes - level order traversal
            int n = q.size();
            for(int i = 0; i < n; i++) {
                auto t = q.front(); q.pop();
                // do edge relaxation from all neighbors
                for(auto nbr: graph[t.first]) {
                    if(t.second + nbr.second < dist[nbr.first]) {
                        dist[nbr.first] = t.second + nbr.second;
                        q.push({nbr.first, dist[nbr.first]});
                    }
                }
            }
            k--;
        }
        return dist[dst] >= INT_MAX ? -1 : dist[dst];

        // ----------- dfs -----------
        // vector<vector<int>> vis(n, vector<int>(k + 2, 0)); // Initializing vis with -1
        // start from src and do bfs till k dist or destination
        // int result = dfs(graph, vis, src, dst, k);
        // return result == INT_MAX ? -1 : result;
        
    }
````

10. https://www.geeksforgeeks.org/problems/distance-from-the-source-bellman-ford-algorithm/1 Use bellman ford
11. https://www.geeksforgeeks.org/problems/distance-from-the-source-bellman-ford-algorithm/1 Use floyd warshal
12. https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/description/ Use floyd warshall and do post processing on resulting matrix as per conditions presented.
13. https://leetcode.com/problems/swim-in-rising-water/ Use dijkstra to solve and select a path which does not have max element present in it.

---

## File: dsa/graphs/ch5.md

# Minimum Spanning Trees

Given a connected, undirected, and weighted graph G, select a subset $E' \in G $ such that graph G is (still) connected and weight of selected edge E' is minimal !!

To satisfy connectivity criteria

- we need at least V-1 edges that form a tree and this tree must span all $V \in G$.

- MST can be solved with several well known algorithms
  - Prim's
  - Krushkal's

Application of MSTs

* Network Design : Minimize cost of laying cable networks
* Clustering and Machine Learning to remove expensive edges in tree
* TSP (Travelling Saleman Problem): used for approximation solution
* Pathfinding Algorithms in Games often use MST.

## Prim’s Algorithm

This algorithm takes a starting vertex and flags it as taken and enqueues a pair of information into a priority queue. The weight `w` and the other end point `u` of edge 0->u that is not taken yet.

These pairs are sorted in the priority queue based on increasing weight, and if tie, by increasing vertex number. Then Prim's algorithm greedily selects pair (w,u) in front of priority queue which has the minimum weight w - if the end point of this edge - which is u has not been taken before. ( to prevent cycle).

- O(process each edge once x cost of enqueue/dequeue) = $O(E \log E)$ = $O(E \log V)$

````c++
int primsMST(int V, vector<vector<pair<int, int>>>& adj) {
    vector<bool> visited(V, false);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
    int mstWeight = 0;
    pq.push({0, 0});  // Start with node 0, weight 0
    while (!pq.empty()) {
        auto [w, u] = pq.top(); pq.pop();
        if (visited[u]) continue;
        visited[u] = true;
      	// take weight and process adjacent edges
        mstWeight += w;
        for (auto& [v, wt] : adj[u]) {
            if (!visited[v]) {
                pq.push({wt, v});
            }
        }
    }
    return mstWeight;
}
````

## Krushkal’s Algorithm

This algorithm first sorts E edges based on non-decreasing weight. Then greedily try to add each edge into MST as long as such addition doesn't form a cycle. This check can be done using lightweight Union-Find Disjoint Sets implementation.

- Runtime O(sorting + trying to add each edge x Cost of Union-Find)
- $O(E \log E + E \times (\approx 1)) = O(E\log E) = O(E \log {V^2} = O(E\log V))$

````c++
bool compareEdges(const Edge& a, const Edge& b) {
    return a.weight < b.weight;
}

int kruskalMST(int V, vector<Edge>& edges) {
    sort(edges.begin(), edges.end(), compareEdges);
    DSU dsu(V);
    int mstWeight = 0;

    for (auto& edge : edges) {
        if (dsu.unite(edge.u, edge.v)) {
            mstWeight += edge.weight;
        }
    }

    return mstWeight;
}
````

## Union-Find (Fastest Implementation)

````c++
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

class UnionFind {                                // OOP style
private:
  vi p, rank, setSize;                           // vi p is the key part
  int numSets;
public:
  UnionFind(int N) {
    p.assign(N, 0); for (int i = 0; i < N; ++i) p[i] = i;
    rank.assign(N, 0);                           // optional speedup
    setSize.assign(N, 1);                        // optional feature
    numSets = N;                                 // optional feature
  }

  int findSet(int i) { return (p[i] == i) ? i : (p[i] = findSet(p[i])); }
  bool isSameSet(int i, int j) { return findSet(i) == findSet(j); }

  int numDisjointSets() { return numSets; }      // optional
  int sizeOfSet(int i) { return setSize[findSet(i)]; } // optional

  bool unionSet(int i, int j) {
    if (isSameSet(i, j)) return false;           // i and j are in same set
    int x = findSet(i), y = findSet(j);          // find both rep items
    if (rank[x] > rank[y]) swap(x, y);           // keep x 'shorter' than y
    p[x] = y;                                    // set x under y
    if (rank[x] == rank[y]) ++rank[y];           // optional speedup
    setSize[y] += setSize[x];                    // combine set sizes at y
    --numSets;                                   // a union reduces numSets
    return true;
  }
};
````

## Famous Variants of MST Applications

- ##### 'Maximum' Spanning Tree

The solution for this is very simple : Modify Kruskal's algorithm a bit, we no simply sort the edges based on non-increasing weight.

- ##### 'Minimum' Spanning Subgraph

In this variant, we do not start with a clean slate. Some edges in the given graph have already been fixed and must be taken as part of the solution. These default edges may form a non-tree in the first place. Our task is to continue selecting the remaining edges (if necessary) to make the graph connected in the least cost way. The resulting Spanning Subgraph may not be a tree and even if its a tree, it may not be the MST. That's why we put term 'Minimum' in quotes and use the term 'subgraph' rather than `tree`.

After taking into account all the fixed edges and their cost we can continue running Kruskal's algorithm on the remaining free edges until we have a spanning subgraph (or spanning tree).

- ##### Minimum 'Spanning Forest'

In this variant, we want to form a forest of K connected components (k subtrees) in the least cost way where K is given beforehand.

To get the minimum spanning forest is simple. Run Kruskal's algorithm as normal, but as soon as the number of connected components equals to the desired pre-determined number K, we can terminate the algorithm.

- ##### Second Best Spanning Tree

A solution for this variant is a modified Kruskal's: sort the edges in $O(E\log E) = O(E\log V)$ then find MST using Kruskal's in $O(E)$. Next for each edge in the MST, temporarily flag it so that it can't be chosen, then try to find MST again in $O(E)$ but now excluding that flagged edge. Note that we do not have to resort the edges at this point. The best spanning tree found after this process is the second best ST.

O(sort the edges once + find the original MST + find the second best ST) = $O(E\log V + E + VE) = O(EV)$

- ##### Minimax (and Maximin)

The minimax path problem is a problem of finding he minimum of maximum edge weight among all possible paths between two vertices i to j. The cost of a path from i to j is determined by maximum edge weight along this path. Among all these possible paths from i to j, pick the one with the minimum max-edge weight.

The problem can be modeled as MST problem. With a rationale that path with low individual edge weights even if the path is longer in terms of number of vertices/edges involved, then having the MST of given weighted graph is correct step. The MST is connected thus ensuring a path between any two vertices. The minimax path solution is thus the max edge weight along the unique path between vertex i and j in this MST.

The overall complexity is O(build MST + one traversal on the resulting tree.)  As E = V-1 in a tree, any traversal is just O(V).

Total Complexity : O(E log V + V) = O(E log V)

## Problems

1. https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1 implement prim’s algorithm with negative weights to simulate min-heap.
2. https://www.geeksforgeeks.org/problems/disjoint-set-union-find/1 Recursive Find Implementation
3. https://www.geeksforgeeks.org/problems/minimum-spanning-tree/1 Same Problem and use simplified UFs and unpack adjacency graph into edges, make sure to use undirected edges only once.
4. https://leetcode.com/problems/number-of-operations-to-make-network-connected/ Use Union-Find to find out the components in the graph, rest can be simple calculations around that.
5. https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/  This solution is complicated better to read discussion on the platform.
6. https://leetcode.com/problems/accounts-merge/description/ In this problem you basically have to track owners separately and try to build union set on strings (emails) and then print those back with owner.
7. https://leetcode.com/problems/number-of-islands-ii/ This problem makes u think of 2d array as flattened array list to simplify the UnionFind implementation, so there is a trade off :)
8. https://leetcode.com/problems/swim-in-rising-water/ This time we will use MST to solve this problem.


---

## File: dsa/graphs/ch6.md

# Other Algorithms

### Graph Edges Property Check via DFS Spanning Tree

* Running DFS on a connected graph generates a DFS spanning tree (or spanning forest if the graph is disconnected). With the help of one more vertex state: EXPLORED = 2 (visited but not yet completed) on top of VISITED (visited and completed), 

* we can classify graph edges into three types:
  * Tree edge: The edge traversed by DFS, i.e. an edge from a vertex currently with state: EXPLORED to a vertex with state: UNVISITED.

  * Back edge: Edge that is part of a cycle, i.e. an edge from a vertex currently with state: EXPLORED to a vertex with state: EXPLORED too. This is an important application of this algorithm. Note that we usually do not count bi-directional edges as having a ‘cycle’ (We need to remember dfs_parent to distinguish this, see the code below).

  * Forward/Cross edges from vertex with state: EXPLORED to vertex with state: VISITED.


![image-20241224185858479](./ch6.assets/image-20241224185858479.png)

````c++
void graphCheck(int u) { 
    // DFS for checking graph edge properties
    dfs_num[u] = EXPLORED;  // Color u as EXPLORED instead of VISITED

    for (int j = 0; j < (int)AdjList[u].size(); j++) {
        ii v = AdjList[u][j]; 
        if (dfs_num[v.first] == UNVISITED) {  // Tree Edge, EXPLORED -> UNVISITED
            dfs_parent[v.first] = u;          // Parent of this child is me
            graphCheck(v.first);
        }
        else if (dfs_num[v.first] == EXPLORED) {  // EXPLORED -> EXPLORED
            if (v.first == dfs_parent[u]) {
                // To differentiate between these two cases
                printf("Two ways (%d, %d) - (%d, %d)\n", u, v.first, v.first, u);
            } else {
                // The most frequent application: check if the graph is cyclic
                printf("Back Edge (%d, %d) (Cycle)\n", u, v.first);
            }
        }
        else if (dfs_num[v.first] == VISITED) {
            printf("Forward/Cross Edge (%d, %d)\n", u, v.first); // EXPLORED -> VISITED
        }
    }
    dfs_num[u] = VISITED;  // After recursion, color u as VISITED (DONE)
}

// Inside int main()
dfs_num.assign(V, UNVISITED);
dfs_parent.assign(V, 0);  // New vector
for (int i = 0; i < V; i++)
    if (dfs_num[i] == UNVISITED)
        printf("Component %d:\n", ++numComp), graphCheck(i); // 2 lines in 1!
````



### Bridges

Use Cases:

* **Network Analysis:** Detecting critical connections in a communication or transport network.
* **Graph Reliability:** Determining edges whose removal disconnects parts of the graph.
* **Geography:** Identifying vulnerable bridges in road networks.

Properties:

* **Definition:** Edges whose removal increases the number of connected components.
* Found in **undirected graphs**.
* Calculated by comparing discovery and low-link values during DFS.
* **O(V + E):** Same DFS-based approach as articulation points.

````c++
void findBridges(int u, int parent, vector<int>& disc, vector<int>& low, vector<vector<int>>& adj,
                 int& time, vector<pair<int, int>>& bridges) {
    disc[u] = low[u] = ++time;

    for (int v : adj[u]) {
        if (disc[v] == -1) { // v is not visited
            findBridges(v, u, disc, low, adj, time, bridges);

            low[u] = min(low[u], low[v]);

            if (low[v] > disc[u]) {
                bridges.push_back({u, v});
            }
        } else if (v != parent) { // Back edge
            low[u] = min(low[u], disc[v]);
        }
    }
}

void bridges(int n, vector<vector<int>>& adj) {
    vector<int> disc(n, -1), low(n, -1);
    vector<pair<int, int>> bridges;
    int time = 0;

    for (int i = 0; i < n; i++) {
        if (disc[i] == -1) {
            findBridges(i, -1, disc, low, adj, time, bridges);
        }
    }

    for (auto& bridge : bridges) {
        cout << bridge.first << " - " << bridge.second << endl;
    }
}
````

### Articulation Point

Use Cases:

* Network Design: Identifying critical routers or servers in a network.
* Graph Reliability: Understanding the impact of removing key nodes.
* Ecosystems: Determining species critical to the stability of ecological networks.

Properties:

* **Definition:** Nodes whose removal increases the number of connected components in a graph.
* Found in **undirected graphs**.
* Depends on **DFS traversal** and comparing discovery and low-link values.
* **O(V + E)**: Each vertex and edge is visited once during the DFS.

````c++
void findArticulationPoints(int u, int parent, vector<int>& disc, vector<int>& low,
                            vector<bool>& isArticulation, vector<vector<int>>& adj, int& time) {
    disc[u] = low[u] = ++time;
    int children = 0;

    for (int v : adj[u]) {
        if (disc[v] == -1) { // v is not visited
            children++;
            findArticulationPoints(v, u, disc, low, isArticulation, adj, time);

            low[u] = min(low[u], low[v]);

            // Check articulation point condition
            if (parent == -1 && children > 1) isArticulation[u] = true;
            if (parent != -1 && low[v] >= disc[u]) isArticulation[u] = true;
        } else if (v != parent) { // Back edge
            low[u] = min(low[u], disc[v]);
        }
    }
}

void articulationPoints(int n, vector<vector<int>>& adj) {
    vector<int> disc(n, -1), low(n, -1);
    vector<bool> isArticulation(n, false);
    int time = 0;

    for (int i = 0; i < n; i++) {
        if (disc[i] == -1) {
            findArticulationPoints(i, -1, disc, low, isArticulation, adj, time);
        }
    }

    for (int i = 0; i < n; i++) {
        if (isArticulation[i]) cout << i << " ";
    }
}
````

## Strongly Connected Components

An SCC is defined as such: If we pick any pair of vertices u and v in the SCC, we can find a path from u to v and vice versa.

![image-20241224184825089](./ch6.assets/image-20241224184825089.png)

### Tarjan’s Algorithm

* **SCCs:** Find SCCs in directed graphs.
* **Circuit Analysis:** Identify strongly connected sub-circuits.
* **Optimization:** Used in solving 2-SAT problems in linear time.

Properties:

* Uses **DFS** to compute discovery and low-link values.
* Maintains a stack to identify the nodes in the current SCC.
* Operates on **directed graphs**.
* **O(V + E):** Each node and edge is processed once during DFS.

````c++
void tarjanDFS(int u, int& time, vector<vector<int>>& adj, vector<int>& disc, vector<int>& low,
               stack<int>& st, vector<bool>& inStack) {
    disc[u] = low[u] = ++time;
    st.push(u);
    inStack[u] = true;

    for (int v : adj[u]) {
        if (disc[v] == -1) { // v is not visited
            tarjanDFS(v, time, adj, disc, low, st, inStack);
            low[u] = min(low[u], low[v]);
        } else if (inStack[v]) { // Back edge
            low[u] = min(low[u], disc[v]);
        }
    }

    if (low[u] == disc[u]) { // Root of SCC
        while (true) {
            int v = st.top();
            st.pop();
            inStack[v] = false;
            cout << v << " ";
            if (v == u) break;
        }
        cout << endl;
    }
}

void tarjansSCC(int n, vector<vector<int>>& adj) {
    vector<int> disc(n, -1), low(n, -1);
    vector<bool> inStack(n, false);
    stack<int> st;
    int time = 0;

    for (int i = 0; i < n; i++) {
        if (disc[i] == -1) {
            tarjanDFS(i, time, adj, disc, low, st, inStack);
        }
    }
}
````

### Kosaraju Algorithm

Use Cases:

* **Strongly Connected Components (SCCs):** Identifying clusters in directed graphs.
* **Dependency Analysis:** Resolving dependencies in package management systems.
* **Circuits:** Finding self-contained sub-circuits in electrical networks.

Properties:

* **Steps:** Two-pass DFS:
  * First pass: Record finishing times of nodes.
  * Second pass: Perform DFS on the reversed graph in decreasing order of finishing times.
* Operates on **directed graphs**.
* **O(V + E):** First DFS, graph reversal, and second DFS each take linear time.

````c++
void dfs(int u, vector<vector<int>>& adj, vector<bool>& visited, stack<int>& st) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v, adj, visited, st);
        }
    }
    st.push(u);
}

void reverseDFS(int u, vector<vector<int>>& revAdj, vector<bool>& visited) {
    visited[u] = true;
    cout << u << " "; // Print SCC
    for (int v : revAdj[u]) {
        if (!visited[v]) {
            reverseDFS(v, revAdj, visited);
        }
    }
}

void kosaraju(int n, vector<vector<int>>& adj) {
    stack<int> st;
    vector<bool> visited(n, false);

    // Step 1: Fill the stack with finish times
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            dfs(i, adj, visited, st);
        }
    }

    // Step 2: Reverse the graph
    vector<vector<int>> revAdj(n);
    for (int u = 0; u < n; u++) {
        for (int v : adj[u]) {
            revAdj[v].push_back(u);
        }
    }

    // Step 3: Process vertices in order of decreasing finish time
    fill(visited.begin(), visited.end(), false);
    while (!st.empty()) {
        int u = st.top();
        st.pop();
        if (!visited[u]) {
            reverseDFS(u, revAdj, visited);
            cout << endl;
        }
    }
}
````



| **Algorithm**           | **Use Case**                        | **Graph Type** | **Property**                             | **Time Complexity** |
| ----------------------- | ----------------------------------- | -------------- | ---------------------------------------- | ------------------- |
| **Articulation Points** | Critical nodes in undirected graphs | Undirected     | Nodes whose removal increases components | O(V + E)            |
| **Bridges**             | Critical edges in undirected graphs | Undirected     | Edges whose removal increases components | O(V + E)            |
| **Kosaraju's**          | SCCs in directed graphs             | Directed       | Two-pass DFS with graph reversal         | O(V + E)            |
| **Tarjan's**            | SCCs in directed graphs             | Directed       | Single DFS with stack-based SCCs         | O(V + E)            |

---

## File: dsa/hash/ch1.md

# Hash Maps & Frequency Counting

To count element frequencies effectively, hash map (dictionary) are used by storing elements as keys and counts as values.

* Updates/Insertion/Lookup : Avg Time $O(1)$ 

* Hash Maps are already implemented in modern programming languages
  * C++ : `map` or `unordered_map` or `set` or `unordered_set`
  * Python: `dict` , `OrderedDict`

* Use cases
  * Anagram Detection
  * First Unique Character in String
  * Find all elements appearing >= n/3 times

* NOTE: More on Hashing will be discussed in Searching/Sorting Portions

### Collision Handling

| **Method**          | **Technique**              | **Use Case**             |
| ------------------- | -------------------------- | ------------------------ |
| **Chaining**        | Linked List in Each Bucket | High collision scenarios |
| **Open Addressing** | Linear/Quadratic Probing   | Memory optimization      |
| **Double Hashing**  | Secondary Hash Functions   | Reduced clustering       |

### Hash Functions

* Properties of a Good Hash Function
  * Prime number modulus reduces collisions
  * Cryptographic hashes (SHA) for security
  * Simple mod/bitmask for speed

## Usage

### Python

````python
# Creating a dictionary
employee = {"name": "Alice", "age": 30, "role": "Engineer"}

print(employee["name"])  # Output: Alice

# Adding or updating values
employee["department"] = "IT"
employee["age"] = 31

# Checking for a key
if "salary" in employee:
    print(employee["salary"])
else:
    print("No salary info")

# Iterating over keys and values
for key, value in employee.items():
    print(f"{key}: {value}")
    
# safe access
print(employee.get("email", "Not available"))  # Output: Not available
````

### STL

````c++
int main() {
    unordered_map<int, string> hashmap;

    // Inserting key-value pairs
    hashmap.insert({1, "Value 1"});
    hashmap[2] = "Value 2";
    hashmap[3] = "Value 3";

    // Accessing values
    cout << "Key 2: " << hashmap[2] << endl;

    // Checking if a key exists
    if (hashmap.find(4) != hashmap.end()) {
        cout << "Key 4 found!" << endl;
    } else {
        cout << "Key 4 not found!" << endl;
    }

    // Removing a key-value pair
    hashmap.erase(2);

    // Iterating over key-value pairs
    for (const auto& pair : hashmap) {
        cout << "Key: " << pair.first << ", Value: " << pair.second << endl;
    }
    return 0;
}
````



### Problems

* Top K frequent Elements
* Sort Characters by Frequency
* First Unique Character


---

## File: dsa/heaps/ch1.md

# Priority Queue & HeapSort

*A priority queue is a data structure of items with keys that supports two basic operation*

* insert a new item
* remove the item with the largest key

Applications

* Simulation Systems (keys ~ event times)
* Job scheduling (keys ~ priority)
* Numerical computation ( keys ~ computation errors )

NOTE: [Linear Implementation](https://algo.minetest.in/3-Sorting/9-Priority_Queues_and_Heapsort/2-Heap_Data_Structure/) , [Tree Implementation](https://algo.minetest.in/3-Sorting/9-Priority_Queues_and_Heapsort/3-Algorithms_on_heap/)

The PQ algorithms on heaps all work by first making a simple  modification that could violate the heap condition and them traversing  the and restoring the heap condition everywhere. This is known as ***Heapifying*** or ***fixing*** the heap.

There are 2 possibilities

1. Priority of some node is increased : To fix it node should swim up the tree
2. Priority of some node in decreased : To fix it node should swim down the tree

## STL & Python Usage

### Python (heapq) — Min-Heap by Default

| **Operation**          | **Function**                  | **Notes**                       |
| ---------------------- | ----------------------------- | ------------------------------- |
| Create heap            | heapq.heapify(list)           | Converts a list into a heap     |
| Insert item            | heapq.heappush(heap, item)    | Adds an item                    |
| Remove min             | heapq.heappop(heap)           | Pops the smallest item          |
| Peek min               | heap[0]                       | Doesn’t remove                  |
| Replace                | heapq.heapreplace(heap, item) | Pops min & pushes item (faster) |
| Push-Pop               | heapq.heappushpop(heap, item) | Push then pop (more efficient)  |
| Merge sorted iterables | heapq.merge(*iterables)       | Useful for external sorting     |

* heapq is a **min-heap** → use **negative values** for max-heap behavior
* No built-in support for 
  * Updating/removing arbitrary elements (requires rebuild)
  * Custom comparators (use Tuple Keys)
* Not thread-safe (`queue.PriorityQueue` is used for threading)

### C++ (std::priority_queue) — Max-Heap by Default

| **Operation** | **Function**      | **Notes**             |
| ------------- | ----------------- | --------------------- |
| Create heap   | priority_queue<T> | Max-heap by default   |
| Insert item   | pq.push(item)     | Adds an item          |
| Remove max    | pq.pop()          | Pops the largest item |
| Peek max      | pq.top()          | Doesn’t remove        |
| Check empty   | pq.empty()        |                       |
| Size          | pq.size()         |                       |

* for min-heap : `priority_queue<int, vector<int>, greater<int>> minHeap;`

````c++
// custom comparator
struct Task {
    int priority;
    string name;
    bool operator<(const Task& other) const {
        return priority < other.priority;  // max-heap
    }
};
priority_queue<Task> pq;
````

* use locks if needed for threading

### Problems

* Implement a Priority Queue using Heap
* Heap Sort (Concept)
* Build a Max Heap from an Array

---

## File: dsa/heaps/ch2.md

# Applications

## Real-time Top-K Elements

### Concept

* Maintain the top `K` largest or smallest elements from a stream or dataset in real-time
* Use a *min-heap* of size `K` to track top `K` largest elements

### Use Cases

* Streaming data analytics
* Real-time Leaderboards
* Online Recommendation System

### Complexity

* Each insertion/deletion operation takes $O(\log K)$
* Efficient for large data streams where $K << N$

### Problems

* Kth Largest Element in an Array
* Top K Frequent Elements
* K Closest Points to Origin

## Median Maintenance

* Maintain the median of a dynamic data stream efficiently
* Use two-heaps
  * A max-heap for the lower half of the numbers
  * A min-heap for the upper half of the numbers
* Balancing the heaps ensures
  * The max-heap size is equal to or one more than the min-heap size
  * Median is either the top of the max-heap (odd cnt) or average of tops of both heaps (even cnt)

### Use Cases

* Real-time Statistics
* Running median in Sensor Data
* Financial Analytics

## Heap-based Sorting & Merging

### HeapSort

* Use a *max-heap* to sort an array in-place
* Steps
  * Build a *max-heap* from input array
  * Repeatedly extract the maximum element and place it at the end
  * Heapify the reduced heap
* Time Complexity: $O(n \log n)$
* Space Complexity: $O(1)$ (in-place)

### Merge K Sorted Lists/Array

* Use a *min-heap* to efficiently merge K sorted list
* Steps
  * Insert the first element of each list into the min-heap
  * Extract the smallest element from the heap and add it to the merged output.
  * Insert the next element from the extracted element’s list into the heap.
  * Repeat until all elements are processed.
* Time Complexity: $O(N \log K)$

### Problems

* Meeting Rooms II (Minimum Number of Meeting Rooms) : (253)

### Use Cases

* External Sorting
* Merging logs or streams
* Database Query Language

---

## File: dsa/index.md

# DSA

## Data Structures

- Array

  * [Two Pointer](array/ch1.md)
  * [Sliding Window](array/ch2.md)
  * [Prefix Sums & Difference Arrays](array/ch3.md)
  * [Subarrays & Subsequences](array/ch4.md)


- Linked List

  * [Basics of Linked List](ll/ch1.md)
  * [Linked List Techniques](ll/ch2.md)


* Stack & Queues

  * [Stack Operations & Applications](stknq/ch1.md)
  * [Queue & Deque Implementations](stknq/ch2.md)
  * [Expression Evaluation & Parsing](stknq/ch3.md)
  * [Monotonic Stacks & Sliding Window Maximum](stknq/ch4.md)


* Heaps & Priority Queues

  * [Min-Heaps & Max-Heaps](heaps/ch1.md)
  * [Applications](heaps/ch2.md)


* [Disjoint Set Union (DSU)(Union-Find)](dsu.md)

* [Hash Maps & Frequency Counting](hash/ch1.md)



## Sorting

* [Elementary Sorting Strategies](sorting/ch1.md)
* [Quicksort](sorting/ch2.md)
* [Mergesort](sorting/ch3.md)
* [Priority Queues & Heapsort](heaps/ch1.md)
* Counting Sort, Radix Sort & Bucket Sort
* Special Sorting Techniques



## Search

* [Binary Search](search/binary_search.md)
* [Search in Rotated/Sorted Array](search/ch2.md)
* [Binary Search Trees (BSTs) Operations](trees/ch1.md)
* Hashing Based Search Methods
* Radix Search & Trie-based Search (Optional)



## Recursion

* [Simple Recursion](recursion/ch1.md)
* [Combinatorics & Permutations](recursion/ch2.md)
* [String Recursion](recursion/ch3.md)
* [Backtracking](recursion/ch4.md)



## Problem Solving Paradigm

- [Complete Search (Brute Force)](paradigm/complete.md)
- [Divide & Conquer](paradigm/dnc.md)
- [Greedy Algorithms & Strategies](paradigm/greedy.md)
- [Dynamic Programming Patterns](dp/intro.md)
  - [1D DP](dp/ch1.md)
  - [2D DP](dp/ch2.md)
  - [Unbounded & Bounded (0/1) Knapsack](dp/ch3.md)
  - [Grid & Palindrome DP](dp/ch4.md)
  - [Game & Interval DP](dp/ch5.md)
- Advanced DP Problems
  - [Bitmask DP](additional/bit2.md)
  - [DP on Trees](dp/ch6.md)
  - [Digit DP](dp/ch7.md)



## Trees

* [Binary Trees & Binary Search Trees (BST)](trees/ch1.md)
* [Problems on Binary Trees](trees/ch2.md)
* [Tries](strings/ch3.md)

Optional Topics in Trees

* [Suffix Trees](strings/ch4.md)
* [Fenwick Trees (Binary Indexed Trees)](trees/ch3.md)
* [Segment Trees & Lazy Propagation](trees/ch4.md)
* [Sqrt Decomposition Techniques](trees/ch5.md)
* [Heap](trees/ch6.md)
* Advanced Trees: AVL, Red-Black Trees


## Graph

* [Graph Properties and their Types](graphs/ch1.md)
* [Graph Traversal (DFS/BFS)](graphs/ch2.md)
* [Digraphs & DAGs (Topological Sorting)](graphs/ch3.md)
* [Shortest Paths](graphs/ch4.md) (Dijkstra, Bellman-Ford, Floyd-Warshall)
* [Minimum Spanning Trees](graphs/ch5.md) (Kruskal, Prim)
* Network Flow Algorithm (Ford-Fulkerson, Edmond-Karp) (Optional)
* [Other Algorithms](graphs/ch6.md) (SCC, Bridges, Articulation Points)



## Strings

* [Basic String Processing](strings/ch1.md)
* [String Matching](strings/ch2.md) (KMP, Rabin-Karp, Z-Algorithm)
* [Trie Data Structures & Application](strings/ch3.md)
* [Suffix Tree & Suffix Arrays](strings/ch4.md) (Optional)
* [String Processing with DP](strings/ch5.md)
* [String Tasks](strings/ch6.md)
* [Compression & Encoding Techniques](strings/ch7.md)



## Additional Topics

* Mathematics
  * [Mathematics & Number Theory](additional/ch1.md)
  * [Modular Arithmetic & Exponentiation](additional/ch2.md)
  * [Combinatorics & Probability](additional/math3.md)
  * [Advanced Math Topics](additional/math4.md) (Optional)
* Binary Manipulation
  * [Bit Manipulation](additional/bit1.md)
  * [Subset Generation & Bitmask DP](additional/bit2.md)


* [Matrix](additional/matrix1.md)
* [Simulation & Randomized Algorithms](additional/simulation.md)
* [Meet-in-the-Middle Technique](additional/mitmt.md)
* [Sparse Tables & Range Queries](additional/sparse.md)
* Geometry
  * [Computational Geometry](additional/geometry1.md)
  * [Points, Lines, Polygons](additional/geometry2.md)
  * [Convex Hull & Line Intersection](additional/geometry3.md)
  * [Advanced Geometry Algorithms](additional/geometry4.md)


---

## File: dsa/ll/ch1.md

# Linked List

### Key Concepts

* Types of Linked List
  * Singly Linked List
  * Doubly Linked List
  * Circular Linked List
* Advantages over arrays
  * Dynamic Size
  * Efficient Insertion/Deletion
* Disadvantages
  * No Random Access
  * Extra Memory for Pointers

## Implementation

```c++
// compact implementation
struct Node { Item item; Node *next;}
typedef Node *link;

// usage
link x = new Node; // or Node *x = new Node;
```

```c++
// constructor implementation
struct Node{
    Item item , Node *next;
    Node( Item x; Node *t){
        item = x ; next = t;
    };
}
typedef Node *link;

// usage
link t = new Node(x, t);	// or Node *x = new Node(x, t);
```

## Basic Operation

### Access

````c++
// dereferencing the link
(*x).item // of type item
(*x).next	// of type link

// short-hand in cpp
x->item
x->next
````

### Deletion

````c++
// using temporary variable
t = x->next; x->next = t->next; // NOTE: Java GC can collect it later, but in C++ it needs to deleted.

// more simpler
x->next = x->next->next;
````

### Insertion

````c++
// inserting node t into the list at position following node x
t->next = x->next; x->next = t;
````

### Traversal

````c++
for(link t = x; t != 0; t = t->next)
  	cout << t->item << endl;
````

### Reversal

* Maintain a pointer `r` to the portion of the list already processed , and a pointer `y` to the portion of the list not yet seen.
* Then save a pointer to the node following `y` in `t`, change `y`’s link to point to `r`, and then move `r` to `y` and `y` to `t`,

````c++
link reverse(link x) {
  link t, y = x, r = 0;
  while(y != 0) {
    t = y->next; y->next = r; r = y; y = t;
  }
  return r;
}
````

## Doubly Linked List

* Its not asked very commonly, but its better understand it.

````c++
// constructor implementation
struct Node{
    Item item , Node *next, Node *prev;
    Node( Item x; Node *t, Node *p){
        item = x ; next = t; prev = p;
    };
}
typedef Node *link;

// deletion for node t
t->next->prev = t->prev;
t->prev->next = t->next;

// insertion, requires updating four nodes
// insert t after x
t->next = x->next;
x->next->prev = t;
x->next = t;
t->prev = x;
````

## Problems

* Merge Two Sorted List (21)
* Remove Nth Node from End (19)
* Remove Linked List Element (203)
* Intersection of Two Linked List (160)
* Josephus Problem (Linked List Variant)


---

## File: dsa/ll/ch2.md

# Linked List Techniques

## Fast & Slow Pointer Techniques

* Optimize traversal using two pointers moving at different speeds.
* Detects cycles, Start of Cycle, mid of list
* Finds Nth Node from End
* Palindrome Checks

````c++
ListNode* middleNode(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

````

Application

* AST Analysis by Compilers to detect recursive & errornous constructs
* Game Development, cycle detection to avoid resource hogging
* Networking Routing Loops

### Problems

* Palindrome Linked List (234)
* Linked List Cycle Detection (141)
* Find Cycle Entry Point (142)

## Recursive Linked List Problems

* these problems usually involve backtracking, divide & Conquer

````c++
ListNode* reverseList(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* newHead = reverseList(head->next);
    head->next->next = head;
    head->next = nullptr;
    return newHead;
}
````

### Problems

* Linked List Palindrome (Recursive Solution)
* Swap Nodes in Pair (24)
* Reverse Node in `k-Groups` (25)

## Cycle Detection & List Manipulation

* Advanced operation involving cycles or structural changes

### Problems

* Reorder List (143) : Combine Cycle Detection with Reversal 
* Flatten a Multilevel DLL (430)
* Partition List (86)
* Odd Even Linked List (328)

---

## File: dsa/paradigm/complete.md

# Complete Search

- aka brute force or recursive backtracking
- in this method we traverse entire search space to obtain solution and during search we are allowed to prune
- Develop this solution only if
- - clearly no other algorithm available
  - better algorithms are overkill for input size
- Remember *‘KISS’* - Keep it Short and Simple
- If there exists a better solution you will get a TLE
- This method can be used as a verifier for small instances

## Iterative Complete Search

- Problem UVa 725 - Division (Two Nested Loops)
- Problem UVa 441 - Lotto (Many Nested Loops)
- Problem UVa 11565 - Simple Equations ( Loops + Pruning)
- Problem UVa 11742 - Social Constraints( Permutations)
- Problem UVa 12455 - Bars (Subsets)

## Recursive Complete Search

- UVa 750 8 Queens Chess Problem
- This code basically checks for all different possibilities of proper non conflicting solution and checks whether given pair is part of the  placement or not. It recursively does backtracking to save time.

````c++
#include <cstdlib>
#include <cstdio>
#include <cstrings>
using namespace std;

int row[8] , TC , a , b, lineCounter;

bool place(int r,int c){
    for (int prev=0; prev<c ; prev++)
        if(row[prev] == r || (abs(row[prev]-r) == abs(prev - c)))
            return false;
    return true;
}
void backtrack(int c){
    if(c==8 && row[b] == a){
        printf("%2d		%d", ++lineCounter , row[0]+1);
        for(int j=1;j<8; j++) printf(" %d",row[j] +1);
        printf("\n");     }
    for (int r =0; r< 8 ; r++)
        if(place(r,c)){
            row[c] = r; backtrack(c+1);
        }
}

int main(){
    scanf("%d",&TC);
    while(TC--){
        scanf("%d %d", &a,&b); a--;b--; //switching to zero basesd indexing
        memset(row,0,sizeof row); lineCounter = 0;
        printf("SOLN		COLUMN\n");
        printf(" # 		1 2 3 4 5 6 7 8\n\n");
        backtrack(0);	//generates all possible 8! candidates
        if (TC) 
          printf("\n");            
    } 
}
````

### Tips:

- Filtering v/s Generating
- Prune Infeasible Search Space Early
- Utilize Symmetries
- Pre-Computation
- Try solving problem backwards
- Optimize your Source Code
- Use Better Data Structures & Algorithms

### Problems

-  [Subsets - Generate all subsets of a set](https://leetcode.com/problems/subsets/) - recursive backtracking to explore include/exclude choices  
-  [Permutations - Generate all permutations of a list](https://leetcode.com/problems/permutations/) - recursive swapping to generate permutations  
-  [Permutations II - Permutations with duplicates](https://leetcode.com/problems/permutations-ii/) - recursive backtracking with sorting and pruning duplicates  
-  [Combination Sum - Find combinations summing to target](https://leetcode.com/problems/combination-sum/) - recursive backtracking allowing repeated elements  
-  [Combination Sum II - Combinations without duplicates](https://leetcode.com/problems/combination-sum-ii/) - recursive backtracking with sorting and skipping duplicates  
-  [Letter Combinations of a Phone Number - Phone digit to letter combos](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) - recursive backtracking building combinations digit by digit  
-  [Generate Parentheses - All valid parentheses combinations](https://leetcode.com/problems/generate-parentheses/) - recursive backtracking tracking counts of open/close parentheses  
-  [Word Search - Search word in 2D board](https://leetcode.com/problems/word-search/) - DFS with backtracking and visited tracking  
-  [N-Queens - Place N queens without conflicts](https://leetcode.com/problems/n-queens/) - recursive backtracking with conflict checks on columns and diagonals  
-  [N-Queens II - Count distinct N-Queens solutions](https://leetcode.com/problems/n-queens-ii/) - recursive backtracking counting solutions  
-  [Palindrome Partitioning - Partition string into palindromes](https://leetcode.com/problems/palindrome-partitioning/) - recursive backtracking with palindrome checks  
-  [Restore IP Addresses - Generate valid IP address combinations](https://leetcode.com/problems/restore-ip-addresses/) - recursive backtracking choosing valid segments  
-  [Combination Sum III - Combination sum with fixed number of elements](https://leetcode.com/problems/combination-sum-iii/) - recursive backtracking with pruning on sum and count  
-  [Subsets II - Subsets with duplicates](https://leetcode.com/problems/subsets-ii/) - recursive backtracking with sorting and duplicate skipping  
-  [All Paths From Source to Target - List all paths in DAG](https://leetcode.com/problems/all-paths-from-source-to-target/) - DFS with path tracking and backtracking  
-  [Find All Anagrams in a String - Find all anagram start indices](https://leetcode.com/problems/find-all-anagrams-in-a-string/) - sliding window with frequency counting  
-  [Permutations (Iterative) - Generate permutations without recursion](https://leetcode.com/problems/permutations/) (variant) - iterative backtracking using explicit stack or loops  


---

## File: dsa/paradigm/dnc.md

# Divide & Conquer

- Divide the original problem into sub-problems-(usually half)
- Find (sub)-solutions for each of these sub-problems-which are now easier
- If needed combine the sub solutions to get a complete solution for the main problem.

***Divide and Conquer to find the maximum***

* function divides array into two halves and then finds the maximum

````c++
Item max(Item a[],int l, int r){
    if (l==r) return a[l];
    item m = (l+r)/2;
    Item u = max(a,l,m);
    Item v = max(a,m+1,r);
    if(u>v) return u; else return v;
}
````

* *Property* - A recursive function that divides a problem of size N into two independent (non empty) parts that it solves recursively calls itself less than N times.
* If parts are one of size k and one size `N-k`

$$
T_N = T_k + T_{N-k} + 1, for N \ge 1 \text{ with } T_1 = 0
$$

* Solution : $T_N = N - 1$ is immediate by induction

***Towers of Hanoi***

given 3 pegs and N disks that fit onto the pegs.  Disks differ in  size and are initially arranged on one of the pegs, in order from  largest(disk N) at the bottom to smallest (disk1) at the top.

The task is to move the stack of disks to the right one position(peg), while obeying the following rules

1. only one disk mat be shifted at a time
2. no disk may be placed on top of smaller one

*The recursive divide-and-conquer algorithm for the towers of Hanoi problem produces a solution that has $2^{N^{-1}}$ moves.*

* $T_N = 2 T_{N-1} + 1, for N \ge \text{ with } T_1 = 1$

***Solution to the towers of Hanoi problem***

````c++
void hanoi(int N,int d){
    if(N==0) return;
    hanoi(N-1,-d);
    shift(N,d);
    hanoi(N-1,-d);
}
````

there is a  correspondence with n-bit numbers is a simple algorithm  for the task. We can move the pile one peg to right by iterating the  following two steps until done:

1. Move the small disk to right if n is odd (left if n is even)
2. Make the only legal move not involving the small disk.

## Uncommon Usages of Binary Search

### The Ordinary Usage

- canonical usage is searching a item in static sorted array.
- complexity is $O(\log n)$
- pre-requisite for performing a binary search can also be found in other uncommon data structures like-root-to-leaf path of a tree (not necessarily binary nor complete ) that satisfies *min heap property* .

### Binary Search on Uncommon Data Structures

### Bisection Method

* also known as binary search on answer space

| Problem Name                                | Problem Number | Description                                                  |
| ------------------------------------------- | -------------- | ------------------------------------------------------------ |
| **Capacity To Ship Packages Within D Days** | 1011           | Binary search on the ship capacity range to find the minimum capacity to ship all packages within D days. |
| **Koko Eating Bananas**                     | 875            | Binary search on the eating speed to find the minimum speed to finish piles within H hours. |
| **Split Array Largest Sum**                 | 410            | Binary search on the largest sum allowed to split the array into m subarrays. |
| **Minimum Time to Complete Trips**          | 2187           | Binary search on time to find the minimum time to complete all trips given multiple buses. |

* All these problems rely on a simple concept. Consider a solution space from 0 to 100000. Usually, a solution exists at some point X within this range, such that every number greater than X is also a solution. Finding X becomes a problem solvable using binary search.

````c++
# gas station problem
#define EPS 1e-9

bool can(double f){	//simulation portion
    //return true if jeep reaches to its goal 
    //return false otherwise
}
//inside int main
// Binary Search the answer, then simulate
double lo =0.0, hi=1000.0, mid =0.0 ans =0.0;
while(fabs(hi-lo)>EBS){
    mid = (lo+hi)/2.0;
    if(can(mid)) { ans = mid ; hi = mid;}
    else 			lo=mid;
}
 printf("%.31f\n",ans);
````



---

## File: dsa/paradigm/greedy.md

# Greedy Algorithms & Strategies

* an algorithm that make the locally optimal choice at each step with the  hope of eventually reaching the globally optimal solution.

* a problem to be solved using greedy must exhibit these two property

  * It has optimal sub structures
  * It has the greedy property (difficult to prove in time -critical environment)

* **Coin Change**

  * Problem Statement:

    Given a target amount $( V )$ cents and a list of $( n ) $ coin denominations, represented as coinValue[i] (in cents) for coin types $ i \in [0..n-1] $, determine the minimum number of coins required to represent the amount \( V \). Assume an unlimited supply of coins of each type.

    Example: For \( n = 4 \) and coinValue = {25, 10, 5, 1} cents, to represent \( V = 42 \) cents, apply the greedy algorithm by selecting the largest coin denomination not exceeding the remaining amount: \( 42 - 25 = 17 \), \( 17 - 10 = 7 \), \( 7 - 5 = 2 \), \( 2 - 1 = 1 \), \( 1 - 1 = 0 \). This requires a total of 5 coins and is optimal.

  - The Problem has two properties

    - Optimal sub-structures

      These are

      - To represent 17 cents we use 10+5+1+1
      - To represent 7 cents we use 5+1+1

    - Greedy property- Given every amount V,we can greedily subtract the  largest coin denomination which is not greater than this amount V. It  can be proven that using any other strategies will not lead to an  optimal solution, at least for this set of coin denominations.

  - However **this greedy doesn’t always work** for all sets of coin denominations e.g.  cents. To make 6 cents with this set will fail optimal solution.

- **UVa - 11292 Dragon of Loowater (Sort the input first)**
  - This is a bipartite matching problem but still can be solved.
  - we match(pair) certain knights to dragon heads in maximal fashion. However, this problem can be solved greedily
  - Each dragon head must be chopped by a knight with the shortest height  that is at least as tall as the diameter’s of the dragon’s head.
  - However input is arbitrary order. Sorting Cost : $O(n \log n + m \log m)$, then to get answer $O(min(n, m))$

````c++
gold = d = k = 0; // array dragon and knight sorted in non decreasing order
while(d<n && k<m){
    while(dragon[d]> knight[k] && k<m) k++; //find required knight
    if(k==m) break;		//no knight can kill this dragon head,doomed
    gold+= knight[k]; // the king pays this amount of gold
    d++;k++;	//next dragon head and knight please
}

if(d==n) printf("%d\n",gold);		//all dragon heads arer chopped
else printf("Loowater is doomed!\n");
````

* Other classical Examples
  * Kruskal’s (and Prim’s) algorithm for the minimum spanning tree (MST)
  * Dijkstra’s (SSSP)
  * Huffman Code
  * Fractional Knapsacks
  * Job Scheduling Problem
* More on [Greedy](https://algo.minetest.in/CP3_Book/3_Problem_Solving_Paradigms/#greedy)

## Problems

* **Station Balance(Load Balancing)- UVa 410**
* **Watering Grass- UVa 10382**-(**Interval Covering**)

---

## File: dsa/recursion/ch1.md

# Recursion

* A recursion program is one that calls itself with a *termination* condition
* Ex - Trees are defined recursively
* **Definition-** A *recursive algorithm* is one that solves a program by solving one or more smaller instances of the same problem. ~ (Divide & Conquer Rule)
* Its always possible to convert recursive program into a non-recursive-one, sometimes it might not be obvious

***Factorial function (recursive implementation)***

````c++
int factorial(int N){
    if (N == 0) return 1;
    return N*factorial(N-1);
}
````

A care should be taken while writing programs related to recursion

* they must explicitly solve a basis case
* each recursive call must involve smaller values of the arguments

***A questionable recursive program***

````c++
int puzzle(int N)
{
    if (N == 1) return 1;
    if (N % 2 == 0)
        return puzzle(N/2);
    else return puzzle(3 * (N+1));	// unbounded N
}
````

***Euclid’s algorithm***

````c++
int gcd(int m,int n ){
    if(n==0) return m;
    return gcd(n,m%n);
}
````

***Recursive program to evaluate prefix expressions***

````c++
char *a; int i;		// passed globally, rather than parameters
int eval(){
    int x=0;
    while(a[i] == " ") i++;
    if(a[i] == "+")
    {	i++; return eval() + eval();}
    if(a[i] == "*")
    {	i++; return eval() * eval();}
    while((a[i]>="0")&&( a[i]<="9"))
        x=10*x+(a[i++]-'0');
    return x;
}
````

***Examples of recursive functions for linked lists***

- `count` - It counts number of nodes on the list.
- `traverse` - calls `visit` for each node on the list from beginning to end.
- `traverseR` - It calls `visit` for every node but in reverse order.
- `remove` - Removes all nodes from a given item value from the list.

````c++
int count(link x)
{
    if(x==0) return 0;
    return 1 + count(x->next);
}
void traverse(link h, void visit(link)){
    if(h==0) return ;
    visit(h);
    traverse(h->next,visit);
}
void traverseR(link h, void visit(link)){
    if(h==0) return;
    traverseR(h->next,visit);
    visit(h);
}
void remove(link& x,Item v)
{
    while(x!=0 && x->item == v)
    {	link t = x ; x = x->next ; delete t;}
    if (x!=0) remove(x->next,v);
}
````

#### Call by value

Memory Layout

* Stack (local function data : arguments & inside data)
* Heap (dynamic like malloc, new)
* Global (global variable, code)

Flow of execution

* Main
* Stack is allocated for every function

#### Call by Reference

* Change the value at calls
  * Explicit return types (use struct to create a new data type)
  * Implicit Return type
* Space Optimized: don’t need extra memory declaration in memory stack

### Problem Types

Note: This is a broad classification. Some types will be discussed in later sections, while others will be covered in their respective sections due to prerequisite topics.

| **Type**                      | **Keywords / Pattern**                          | **Examples**                                        |
| ----------------------------- | ----------------------------------------------- | --------------------------------------------------- |
| **Basic Recursion**           | Simple function calls, base + recursive step    | Factorial, Fibonacci, Power(x, n)                   |
| **Backtracking**              | Try all possibilities, undo step, constraints   | N-Queens, Sudoku Solver, Permutations               |
| **Combinatorics**             | Generate combinations, subsets, partitions      | Subsets, Combination Sum, Phone Number Letter Comb  |
| **Permutations**              | All orderings, visited flags                    | All permutations of string/array, Anagrams          |
| **Divide & Conquer**          | Split input, solve subproblems, merge result    | Merge Sort, Quick Sort, Binary Search               |
| **Tree Recursion**            | Binary tree traversal, multiple recursive calls | DFS, Tree Diameter, Max Depth of Tree               |
| **Graph Traversal**           | Recursively visit nodes/edges, visited map      | DFS on Graph, Islands Count, Connected Components   |
| **Recursion + Memoization**   | Reuse overlapping subproblems                   | Fibonacci (Top-down), Climbing Stairs               |
| **String Recursion**          | Substring generation, character decisions       | Palindrome Partitioning, Generate Valid Parentheses |
| **Recursion with Return**     | Return values from children, accumulate results | Path Sum in Tree, Sum of Subsets                    |
| **Recursion with Parameters** | Track path, state                               | Subsequence with sum K, Combinations with k size    |
| **Recursion Tree Analysis**   | T(n) = 2T(n/2) + n, or similar                  | Understanding time complexity                       |

## Time Complexity Analysis

* A very straight forward method to solve recursion complexity is using Back Substitution method (write-out recurrence)

$$
f(n) = f(n-1) + f(n-2)\\
f(n) = f(n-2) + f(n-3) + f(n-3) + f(n-4)\\
f(n) = f(n-2) + 2 f(n-3) + f(n-4) ... f(n)\\
f(n) = f(1) + O(2^n)
$$

* Tree Method
  * Imagine the tree
  * Sum up the work at each level
* Subsets Problem : $O(2^n)$
* Combination Problem: $O(2^{max(n, k)}) = O(2^n)$

- A recursion Visualizer : https://recursion.vercel.app/


---

## File: dsa/recursion/ch2.md

# Combinatorics & Permutations

* Note that all problems listed here are enumeration problems requiring the generation of all possible solution combinations. If the problems involved calculating a single value instead of actual solutions, they would become dynamic programming problems. In such cases, optimizations like memoization can reduce complexity.

## Subsets

* NOTE: Subsets don’t have any specific order
* To solve this problems lets divide the solution set using some criteria where both solutions are
  * Disjoint ($c_1 \text{ and } c_2 = \phi $)
  * Universal ($c_1 \text{ or } c_2 = U$)
* we can interpret solution set as : $c_1$ solution that includes first element in the subset, $c_2$ solution that doesn’t include the first element
* Solution for `[2, 3, 5]` becomes
  * $c_1$ : number of subset of `[3, 5]`
  * $c_2$ : any subsets of `[3, 5]` and append `2` to it
* Solution is based on Suffix Array
* Recurrence : `f(arr, 0, n-1) = f(arr, 1, n-1)` $\text{ or }$ `f(arr, 1, n-1) + {arr[0]}`
* Base Case: `f(arr, n-1, n-1) = { {}, {arr[n-1]}}`

````c++
vector<vector<int>> f(vector<int>& nums, int i, int r) {
  // Base Case
  if(i == r) {
    return {{}, {nums[r]}}
  }
  // Recursive Step
  // Get C2
  vector<vector<int>> c1 = f(nums, i+1, r);
  
  // Get C1
  vector<vector<int>> c2 = c1;
  for(int j = 0; j < c2.size(); j++)
    	c1[j].push_back(nums[i]);
  
  // combine both solution
  vector<vector<int>> res = c2;
  for(int j = 0; j < c1.size(); j++) {
    res.push_back(c1[j]);
  }
  return res;
}

vector<vector<int>> subsets(vector<int>& nums) {
  return f(nums, 0, nums.size() - 1);
}
````

* more space optimal approach is to track current recursion calls using `contribution` arr.

````c++
void f(vector<int>& nums, int i, int end, vector<int> contri, vector<vector<int>> & res){
    if(i == end){
        res.push_back(contri);
        
        contri.push_back(nums[end]);
        res.push_back(contri);
        return;
    }
    
    // Recursive
    // C2.
    f(nums,i+1,end, contri,res);
    
    // C1.
    // Contribution at this step is nums[i], ideally should be passed as reference
   	contri.push_back(nums[i]);
    f(nums,i+1,end, contri, res);
}
vector<vector<int>> subsets(vector<int>& nums){
    vector<vector<int>> res;
    
    // Implicit return
    f(nums, 0, nums.size()-1, {}, res);
    return res;
}
````

## Combination

Given an array = `[1, 2, 3, 4]` and `k=2`

Solution Set would be : `{[1,2] , [2,3], [3,4], [1,4] , [2,4], [1,3] }`

- Divide : Above problem can be divided into two chunks such that they contain `1` in c_1 and doesn’t contain `1` in c_2
- Represent : Suffix Array
- $c_2$ : all possible `k` sized subsets of `P(A[1...n-1], k)`
- $c_1$ : all possible `k-1` sized subsets of `P(A[l...n-1]) + [A[0]]` (`A[0]` is appended to solution)
- Recursion: `P(A, 0, n-1, k) = P(A, 1, n-1, k) + (P(A, 1, n-1, k-1)..A[0])`
- Base Case
  - `s > e`
    - `k = 0` : `{{}}`
    - `k > 0` : no solution
  - `s <= e`
    - `k = 0` : `{{}}`

````c++
vector<vector<int>> f(int start, int end, int k){
    // Base Case.
    if(k == 0)
        return {{}};
    if(start > end)
        return {};
    
    // Recursive Step
    // C2
    // Doesn't include the first element
    vector<vector<int>> c2 = f(start+1,end,k);

    // C1
    // Include the first element
    vector<vector<int>> temp = f(start+1, end, k-1);

    // Append the first element
    vector<vector<int>> c1 = temp;
    for(int i = 0; i < temp.size(); i++)
        c1[i].push_back(start+1);

    // Merge
    // Res is c1 U c2
    vector<vector<int>> res = c2;
    for(int i = 0 ; i < c1.size(); i++)
        res.push_back(c1[i]);
    return res;
}
vector<vector<int>> combine(int n, int k) {
    return f(0,n-1,k);
}
````

````c++
// space optimized solution
void f(int start, int end, int k, vector<int>& contri, vector<vector<int>> & res ){
    // Base Case.
    if(k == 0){
        res.push_back(contri);
        return ;
    }
    if(start > end)
        return ;

    // Recursive Step
    // C2. Doesn't include the first element
    f(start+1,end,k, contri, res);

    // C1. Include the first element
    contri.push_back(start+1);
    f(start+1, end, k-1,contri, res);
  	// restore recursion stack
  	contri.pop_back();		// notice now its even better then previous solutions
}
vector<vector<int>> combine(int n, int k) {
    vector<vector<int>> res;
    f(0,n-1,k,{},res);
    return res;
}
````

## Combination Sum

Representation : Suffix Array

* Divide
  * $c_1$ : not including first element :
  * $c_2$ : contains atleast one instance of first element
* Subproblems
  * $c_1$ : `P(A, 1, n-1, sum)`
  * $c_2$ : `P(A, 0, n-1, sum - A[0])` , same as original problem with one copy consumed
* Recurrence: `P(A, 0, n-1, sum)  = P(A, 1, n-1, sum) & P(A, 0, n-1, sum - A[0])`
* Base Cases
  * if `A` becomes empty
    * `sum > 0` : `{}`
    * `sum = 0` : `{{}}` | result
    * `sum < 0` : `{}`
  * `sum <= 0`
    * `sum == 0`: `{{}}` | result
    * `sum < 0` : `{}`

````c++
void f(vector<int>& arr, int start, int end, int target, vector<int>& contri, vector<vector<int>>& res){
    //Base Setps
    if(target == 0) {
        res.push_back(contri);
        return;
    }
    if(target < 0 || start > end)
        return;
    
    //solve c2
    //not including first element
    f(arr,start+1,end,target,contri,res);
    //solve c1 include first element atleast once
    contri.push_back(arr[start]);
    f(arr,start, end, target-arr[start],contri, res);
    contri.pop_back();
}
vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    vector<vector<int>> res;
    vector<int> contri;
    f(candidates, 0, candidates.size()-1,target, contri, res);
    return res;
}
````

* Above solution can be pruned further: `if (rem < k) return;` i.e. `if(end-start+1 < k) return;`

### Combination Sum - II

[LeetCode Link](https://leetcode.com/problems/combination-sum-ii/description/)

* NOTE: Only change is finite consumption of numbers. So out $c_2$ from previous solution changes as follows.

````c++
void f(vector<int>& candidates, int start, int end, int target,vector<int>& contri, vector<vector<int>>& res){
    //base step
    if(target == 0) {
        res.push_back(contri);
        return;
    }

    if( target < 0 || start > end) return;
    //recursive step

    //Not include the smallest ele. at all
    //find the first occurence of number > ar[start]
    int j = start + 1;
    while(j <= end && candidates[j] == candidates[start]) j++;

    f(candidates, j, end, target , contri , res);
    contri.push_back(candidates[start]);
    f(candidates,start + 1, end, target - candidates[start], contri, res);
    contri.pop_back();
}
vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
    vector<int> contri;
    vector<vector<int>> res;
    vector<int> suffix(candidates.size(),0);
    sort(candidates.begin(), candidates.end());
    f(candidates, 0 , candidates.size() -1 , target, contri, res);
    return res;
}
````

### Letter Combination of a Phone Number

[Leetcode Link](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

Given string digit from `2-9`, return all possible letter combination that could represent the numbers.

* So for a digit `3`: there could be 3 possibility `d, e, f`
* Problem reduces to precisely same as suffix array.

````c++
vector<string> digitToAlphabet;
void initializeMap(){
    digitToAlphabet.resize(10);
    digitToAlphabet[2] = "abc";
    digitToAlphabet[3] = "def";
    digitToAlphabet[4] = "ghi";
    digitToAlphabet[5] = "jkl";
    digitToAlphabet[6] = "mno";
    digitToAlphabet[7] = "pqrs";
    digitToAlphabet[8] = "tuv";
    digitToAlphabet[9] = "wxyz";
}
void f(string& digits, int start, string& contri, vector<string>& res){

    //Base Case
    if(start == digits.size()){
        res.push_back(contri);
        return;
    }

    // recursion
    for(int i=0; i< digitToAlphabet[digits[start] -'0'].size(); i++){
        contri.push_back(digitToAlphabet[digits[start] - '0'][i]);
        f(digits,start+1,contri,res);
        contri.pop_back();
    }
}
vector<string> letterCombinations(string digits) {
    if(digits.size() == 0) return vector<string>();
    vector<string> res;
    string contri;
    initializeMap();
    f(digits,0,contri,res);
    return res;
}

````

## Permutation

* This is somewhat what represent a `1D` DP. Representation of Solution using Suffix Array usually leads to constraint in 1 dimension.
* Ex - `[1, 2, 3]` Split Criteria : ?
  * `n` chunks of solutions, as
  * begins with 1 `{[1,3,2], [1,2,3]}`
  * begins with 2 `{[2,1,3], [2,3,1]}`
  * begins with 3 `{[3,1,2], [3,2,1]}`
* Subproblem : permutation calculation of the subarray removing that item. These are subsequences not suffix array problem.
* Representation:
  * Keeping a visited array will be helpful to represent the subproblems.
  * Or we can always send the element not to be included to be swapped with  the first element and that way we have a continuous suffix array as a subproblem

##### Keeping visited array (Optimized) 

````c++
void f(vector<int>& nums, vector<bool>& visited, vector<int>& contri, vector<vector<int>>& res){
    //Base Step
    //When everything is visited
    int i;
    for(i=0; i <nums.size(); i++){
        if(!visited[i])
            break;
    }
    if(i == nums.size()){
        res.push_back(contri);
        return;
    }
    //Recursive Step
    //Iterate over all possibilities for current position
    for( i = 0; i< nums.size(); i++)
    {
        //consider the ones that aren't visited
        if(!visited[i]) {
            //Passdown the contri
            //Try for this elt at the current position
            contri.push_back(nums[i]);
            visited[i] = true;
            f(nums,visited,contri, res);
            contri.pop_back(); // important step
            visited[i] = false;
        } 
    }
}
vector<vector<int>> permute(vector<int>& nums) {
    vector<bool> visited(nums.size(),false);
    vector<vector<int>> res;
    vector<int> contri;
    f(nums, visited, contri, res);
    return res;
}
````

Base Case Pruning

````c++
if(contri.size() == nums.size()){
    res.push_back(contri);
    return;
}
````

##### Swapping based solution (creates explicit suffix array)

````c++
void f(vector<int>& nums,int j, vector<int>& contri, vector<vector<int>>& res){
    //Base Step
    //When everything is visited
    if(j == nums.size()){
        res.push_back(contri);
        return;
    }

    //Recursive Step
    //Iterate over all possibilities for current position
    for(int i = j; i< nums.size(); i++)
    {
        //consider the ones that aren't visited
        //Passdown the contri
        //Try for this elt at the current position
        contri.push_back(nums[i]);
        swap(nums[j],nums[i]);
        f(nums,j+1,contri, res);
        //undo operation to maintain tree validity
        contri.pop_back();
        swap(nums[j],nums[i]);
    }
}
vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> res;
    vector<int> contri;
    f(nums, 0, contri, res);
    return res;
}
````

### Permutation Sequence

[k-th Permutation Sequence](https://leetcode.com/problems/permutation-sequence/description/)

* Naively Listing all permutations and then finding `kth` will give TLE in this case.
* We will perform DFS, and try to search that solution
* Ex - `[1, 2, 3]`
* Possibilities = `(123, 132,213, 231, 312,321)` and we have to give `kth` solution.
* There are 3 chunks, chunks including 1, 2, 3 as first number respectively
* now say its a ordered list, then we can easily say chunk size and the chunk in which this `k-th` number will lie would be

$$
\text{chunk id} = \frac{k-1}{(n-1)!}
$$

* then calculate offset how far this item is away from that `chunk_id`
* hmmm can we do that recursively ! yes :D

````c++
int fact(int n){
    int i, res = 1;
    for(i = 1; i<= n; i++)
        res = res * i;
    return res;
}
//Return the pos and unvisited number
int getNumber(vector<int>& visited, int pos){
    int count = 0;
    for(int i = 1; i<= 9; i++){
        if(visited[i]) continue;
        count++;
        if(count == pos)
            return i;
    }
    //NF-won't reach here
    return -1;
}
string getPermutation(int n, int k) {
    int i,chunk_id, pos, curr_digit;
    int copy_n = n;
    vector<int> visited(10,0); 
    string res = "";
    for( i = 1; i <= copy_n; i++){
        chunk_id = (k-1)/fact(n-1); 
        // get corresponding digit
        pos = chunk_id +1;
        curr_digit = getNumber(visited, pos);
        res = res + to_string(curr_digit);

        // mark visited
        visited[curr_digit] = 1;
        // update k and n;
        k = k - (chunk_id*fact(n-1));
        n--;
    }
    return res;
}
````



---

## File: dsa/recursion/ch3.md

# String Recursion

## Palindrome Partitioning

[Leetcode Link](https://leetcode.com/problems/palindrome-partitioning/)

* Given a string `s`, partition `s` such that every substring of the partition is a substring, Enumerate all such solutions

Split Strategy

* divide into `n` chunks
* set of solution where first partition `a` : `a | a | b`
* set of solution where first partition `aa` : `a a | b`
* set of solution where first partition `aab` : $\phi$ // prefix is not a palindrome

Subproblem

* $c_i$ : All the palindrome partition of elements of array after $i$ and then append palindrome before $c_i$

* 1 D Subproblem, its a suffix array problem

````c++
bool isPalindrome(string& s){
    int start= 0, end = s.size()-1;
    while(start <= end){
        if(s[start] != s[end])
            return false;
        start++,end--;
    }
    return true;
}
void f(string& s, int start, vector<string>& contri, vector<vector<string>>& res){
    //Base case
    if(start == s.size()){
        res.push_back(contri);
        return;
    }

    //Try all possibilities of putting up the partition
    string part;
    for(int j = start; j < s.size(); j++){
        // s[start .. j] is the first partition
        part = s.substr(start, j-start+1);

        if(!isPalindrome(part))
            continue;
        contri.push_back(part);
        f(s,j+1, contri, res);
        contri.pop_back(); // clear parent call! important
    }
}
vector<vector<string>> partition(string s) {
    vector<vector<string>> res;
    vector<string> contri;
    f(s,0,contri,res);
    return res;
}

````



## Word Search

[Leetcode Link](https://leetcode.com/problems/word-search/description/)

* Problem based on 2D Matrix DFS, standard pattern

````c++
vector<vector<int>> dirs = {{1,0}, {-1,0} , {0,1} , {0,-1}};
bool f(vector<vector<char>>& board, int start_i, int start_j,vector<vector<bool>>& visited, string& word, int pos){
    // 4 possibilities
    if(pos == word.size())
        return true;
    int m = board.size() , n =board[0].size();
    bool res = false;
    for(int i = 0; i < dirs.size(); i++){
        int x = start_i + dirs[i][0];
        int y = start_j + dirs[i][1];

        //check if its valid
        if(x<0 || x>=m || y <0  || y>=n) continue;
        if(visited[x][y] || board[x][y] != word[pos]) continue;
        visited[x][y] = true;
        res = res||f(board, x, y, visited, word, pos+1);
        visited[x][y] = false;

    }
    return res;
}
bool exist(vector<vector<char>>& board, string word) {
    int m = board.size(), n = board[0].size();
    bool res = false;
    vector<vector<bool>> visited(m,vector<bool>(n,false));
    for(int i = 0; i<m; i++)
        for(int j = 0; j < n ; j++)
            if(board[i][j] == word[0]){
                visited[i][j] = true;
                res = res || f(board,i,j,visited, word, 1);
                visited[i][j] = false;
            }

    return res;
}
````

## Generate valid Parenthesis


---

## File: dsa/recursion/ch4.md

# Backtracking

## N-Queens Problem

[Leetcode Link](https://leetcode.com/problems/n-queens/)

Enumeration Problem

Problem can be restated as putting 1 queen into each row such that they don’t conflict.

Split into chunks

* `n` queens can be put in `n` rows
* for each row we have `n` possible columns

$c_1$ : List of valid configuration s.t. first cell is `[0, 0]` and rest of solution is `Mat[1..n-1][0..n-1]`

$c_2$ : List of valid configuration st.t first cell is `[0, 1]`

$c_3$ : List of valid configuration st.t first cell is `[0, 2]`

Subproblem instance

$c_1$ : take `(0, 0)` as occupied and then find out all valid configuration for `n-1` queens and append `(0, 0)` to it

Representation of problem : `f(n*n Matrix, n-1)`

````c++
bool existsInCol(vector<string>& mat, int col, int n){
    for(int i = 0; i <n ; i++){
        if(mat[i][col] == 'Q')
            return true;
    }
    return false;
}
bool existsInDiag(vector<string>& mat, int curr_row, int curr_col, int type, int n){
    //type == 1 principal diagonal (positive slope)
    //type == 2 secondary diagonal (negative slope)

    //Go up
    int factor = (type == 1)? 1 : -1;

    int i = curr_row, j = curr_col;
    while( i>=0 && j<n && j >= 0){
        if(mat[i][j] == 'Q')
            return true;
        i--;
        j+=factor;
    }
    //Go down
    return false;
}
void f(vector<string>& mat, int  rem, vector<string>& contri, vector<vector<string>>& res,int n){

    // Base step
    if(rem == 0)
    { res.push_back(contri); return;}
    //recursive step
    //c1 to c_N
    //try n-rem row
    int i;
    for(i = 0; i < n; i++){
        //check if this is a valid position
        // check if possible in curr col
        if(!existsInCol(mat,i,n) &&
           !existsInDiag(mat,n-rem,i,1,n)&&
           !existsInDiag(mat,n-rem,i,2,n)){
            mat[n-rem][i] = 'Q';
            contri[n-rem][i] = 'Q';
            f(mat,rem-1,contri,res,n);
            mat[n-rem][i] = '.';
            contri[n-rem][i] ='.';

        }
    }

}
vector<vector<string>> solveNQueens(int n) {
    vector<vector<string>> res;
    vector<string> mat(n, string(n,'.'));
    vector<string> contri(n,string(n,'.'));
    f(mat,n,contri,res,n);
    return res;

}
````

## Sudoko Solver


---

## File: dsa/search/binary_search.md

# Binary Search

Binary search is a powerful algorithm for locating an element or solving optimization problems within a search space where the data meets specific criteria. The following is a concise summary and framework for applying binary search effectively:

Key Concepts

1. **Search Space:** 
   * A set of elements, such as indices, numbers, or a conceptual range, that can be ordered or partitioned. Examples include sorted arrays, monotonic functions, and intervals.

2. **Predicate (p(x))**: 
   * A boolean function (true/false) applied to items in the search space.
   * The predicate determines the behavior of the elements:
     * `F*T*`: false, false, false, true, true (transition from F to T).
     * `T*F*`: true, true, true, false, false (transition from T to F).
3. Applicability of Binary Search:
   * Binary Search is applicable if:
     * The search space is monotonic w.r.t. the predicate.
     * For `F*T*`: All F precede T.
     * For `T*F*`: All T precede F.
4. Goals of Binary Search:
   * Find the last F or the first T in `F*T*`.
   * Find the last T or the first F in `T*F*`.

## Framework to Solve Binary Search Problem

1. **Define the Search Space:**
   * Decide whether it is a range ([lo, hi]) or a collection (like an array).

2. **Define the Predicate (p(x)):**
   * Write a condition that transitions at a key point.

Example: For a sorted array and a target x, use p(x) = (arr[mid] >= target) for ``F*T*`.

3. **Decide the Goal:**
   * Find **first T**, **last F**, **last T**, or **first F** based on the problem.

4. **Write Binary Search:**
   * Use the appropriate loop (while(lo < hi) or while(lo <= hi)) and mid-point calculation:
     * low_mid: mid = lo + (hi - lo) / 2 (default).
     * high_mid: mid = lo + (hi - lo + 1) / 2 (if focusing on higher mid).

## Pseudo Codes

### For `F*T*` (Find Last F/First T)

````c++
int lastF(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;  // Use high_mid
        if (p(mid))
            hi = mid - 1;  // Move left
        else
            lo = mid;      // Move right
    }
    return (!p(lo)) ? lo : -1;  // Check and return
}
````

````c++
int firstT(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;  // Use low_mid
        if (p(mid))
            hi = mid;      // Move left
        else
            lo = mid + 1;  // Move right
    }
    return (p(lo)) ? lo : -1;  // Check and return
}
````

### For `T*F*` (Find Last T/First F)

````c++
int lastT(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;  // Use high_mid
        if (p(mid))
            lo = mid;      // Move right
        else
            hi = mid - 1;  // Move left
    }
    return (p(lo)) ? lo : -1;  // Check and return
}
````

````c++
int firstF(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;  // Use low_mid
        if (p(mid))
            lo = mid + 1;  // Move right
        else
            hi = mid;      // Move left
    }
    return (!p(lo)) ? lo : -1;  // Check and return
}
````

### **Tips to Remember**

1. **Predicate**: Design it to divide the search space into `F*T*` or `T*F*`.

2. **Mid Calculation**:
   * **low_mid**: lo + (hi - lo) / 2 (default for most cases).
   * **high_mid**: lo + (hi - lo + 1) / 2 (if skipping mid element is required).

3. **Focus**: Adjust lo or hi based on whether you move left or right.

4. **Post-Loop Check**: Always verify the result before returning to avoid off-by-one errors.

Binary Search simplifies problems when you clearly define the search space and the predicate.

### Overflow Safe Binary Search Template

````c++
int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;  // Overflow-safe
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
````

### Further Study

[Divide & Conquer](../paradigm/dnc.md)

---

## File: dsa/search/ch2.md

# Problems on Sorting



### Problem

* [Sort Colors](https://leetcode.com/problems/sort-colors) : Dutch National Flag

---

## File: dsa/sorting/ch1.md

# Elementary Sorting Techniques

Below are all Elementary Sorting Techniques for Educational Purposes only, These are rarely used in production.

## Selection Sort

* Exchanges : $N-1$
* Comparisons : $N^2$
* Comparisons dominate runtime
* Not Stable
* Takes same time irrespective of already sorted array
* outperforms more sophisticated methods in one important application; it is the method for sorting files with huge item and small keys. `(cost of moving > cost of making comparisons)`

````c++
void selection(vector<int> arr, int l , int r){
    for(int i = l ; i <r ; i++){
        int min  = i;
        for(int j = i+1 ; j <=r ; j++)
            if(arr[j] < arr[min]) min = j ;
        swap(arr[i], arr[min]);
    }
}
````

## Bubble Sort

* Exchanges : Upto $N^2$
* Comparison: $N^2$
* Stable
* **Inefficient for large datasets** due to high number of swaps, rarely used in practice
* Not Memory Efficient, but in-place
* Adaptive : Useful In scenarios where data is almost already sorted.

````c++
// compexch: compare and exchange if necessary
template <typename T>
void compexch(T& a, T& b) {
    if (b < a) {
        std::swap(a, b);
    }
}
````

````c++
// assuming compexch is implemented
void bubble(vector<int> arr , int l , int r){
    for(int i = l; i < r; i++)
        for(int j = r ; j > i; j--)
            compexch(arr[j-1], arr[j]);
}
````

## Insertion Sort

* Exchanges: Upto $N^2$
* Comparison: $N^2$
* Stable
* Adaptive
* Efficient for small datasets or partially sorted data
* Used in practice for small data and as a final stage in more complex sorts like TimSort or Hybrid sorts
* The **sentinel optimization** ensures that the inner loop never checks bounds `(j > l)`, improving efficiency.

````c++
void insertion(vector<int> a, int l, int r) {
    // Sentinel placement: move the smallest item to the beginning
    for (int i = r; i > l; --i) compexch(a[i - 1], a[i]);

    // Insertion sort with sentinel
    for (int i = l + 2; i <= r; ++i) {
        Item v = a[i];
        int j = i;
        while (v < a[j - 1]) {
            a[j] = a[j - 1];
            --j;
        }
        a[j] = v;
    }
}
````

## Shell Sort

* Not Stable
* More on Shell Sort : [Link](https://algo.minetest.in/3-Sorting/6-Elementary_Sorting_Methods/6-Shell_sort/)

````c++
template <typename Item>
void shellsort(Item a[], int l, int r) {
    int h;

    // Generate initial maximum gap (using Knuth's sequence: 1, 4, 13, 40, ...)
    for (h = 1; h <= (r - l) / 9; h = 3 * h + 1);

    // Decrease the gap and perform gapped insertion sort
    for (; h > 0; h /= 3) {
        for (int i = l + h; i <= r; ++i) {
            Item v = a[i];
            int j = i;

            // Gapped insertion sort
            while (j >= l + h && v < a[j - h]) {
                a[j] = a[j - h];
                j -= h;
            }

            a[j] = v;
        }
    }
}
````



---

## File: dsa/sorting/ch2.md

# Quicksort

* Quicksort is most widely used sorting algorithm than any other algorithm.

* Invented in 1960 by C.A.R. Hoare.

  - easy to implement
  - resource efficient in many cases

* features

  - in-place
  - $N \log{N}$ on avg case

* drawbacks

  - Not stable

  - $N^2$ in worst case
  - fragile ( any small mistake in implementation can go un-noticed and cause bad performance)

* STL library uses `qsort` function.

* Performance of the quicksort is highly dependent on the input.

![image-20201020142048564](https://algo.minetest.in/1-The_Basic_Algorithm.assets/image-20201020142048564.png)

````c++
// Partition function
template <typename Item>
int partition(Item a[], int l, int r) {
    int i = l - 1, j = r;
    Item v = a[r];
    for (;;) {
        while (a[++i] < v);         // move i right
        while (v < a[--j]) if (j == l) break; // move j left
        if (i >= j) break;
        swap(a[i], a[j]);           // swap a[i] and a[j]
    }
    swap(a[i], a[r]);               // place pivot at its final position
    return i;                       // return pivot index
}

// Quicksort main function
template <typename Item>
void quicksort(Item a[], int l, int r) {
    if (r <= l) return;
    int i = partition(a, l, r);
    quicksort(a, l, i - 1);
    quicksort(a, i + 1, r);
}
````

* Dynamic Characterstics
  * Nearly ordered files perform worst.
  * Because they have many partitions.

## Quick-Select

* Finding `k-th` smallest number in a set of numbers
* Can be used to find median without sorting
* Time Complexity : $O(N)$ in avg case, $O(N^2)$ in worst case

````c++
// Recursive
template <typename Item>
void quickselect(Item a[], int l, int r, int k) {
    if (r <= l) return;
    int i = partition(a, l, r);
    if (i > k) quickselect(a, l, i - 1, k);
    else if (i < k) quickselect(a, i + 1, r, k);
}
````

````c++
// Iterative Approach
template <typename Item>
void quickselect(Item a[], int l, int r, int k) {
    while (r > l) {
        int i = partition(a, l, r);
        if (i > k) r = i - 1;
        else if (i < k) l = i + 1;
        else break;
    }
}
````



---

## File: dsa/sorting/ch3.md

# Mergesort

* Biggest Advantage is guaranted runtime : $O(N \log{N})$ (Independent of Input)
* Requires Additional Space : $O(N)$ (disadvantage)
* Guaranted Runtime can become liability. Some linear sorts can take take advantage of array properties.
* Stable (NOTE: Quicksort & Heapsort are not)
* Choice for Sorting Linked List
* Proper Example of Divide & Conquer

## Two-Way Merging

````c++
// two-way merging: given two ordered files (a, b), merge them into one (c)
template <class Item>
void mergeAB(Item c[], Item a[], int N, Item b[], int M){
    for(int i = 0, j = 0, k = 0; k < (M+N); k++){
        if(i == N){ c[k] = b[j++]; continue;}
        if(j == M){ c[k] = a[i++]; continue;}
        c[k] = (a[i] < b[j]) ? a[i++] : b[j++];
    }
}
````

## Inplace Merge

* Stable

````c++
// merge without sentinels, copy second array aux in reverse back to back with the first (putting aux in bitonic order)
template <class Item>
void merge(Item a[], int l, int m, int r){
    int i , j;
    static Item aux[maxN];
    for(i = m+1; i > l; i--) aux[i-1] = a[i-1];
    for(j = m; j < r ; j++) aux[r+m-j] = a[j+1];
    for(int k = l; k <= r ; k++)
				if(aux[j] < aux[i]) 
          a[k] = aux[j--]; 
  			else a[k] = aux[i++];
}
````

````c++
// top-down merge sort
template <class Item>
void mergesort(Item a[],int l , int r)
{
    if(r <= l ) return;
    int m = (r+l)/2 ;
    mergesort(a,l,m);
    mergesort(a,m+1,r);
    merge(a,l,m,r);
}
````

````c++
// bottom-up merge sort
template <class Item>
void mergesortBU(Item [a],int l, int r){
    for(int m = l; m <= r-l ; m = m+m )
        for(int i = l; i <= r-m; i += m+m)
            merge(a, i, i+m-1, min(i+m+m-1, r));
}
````

* NOTE: MergeSort can be improved by adding additional check to sort smaller partition using *insertion sort*

## Linked List Merge Sort

````c++
// merge
link merge(link a, link b ){
    node dummy(0); link head = &dummy, c= head;
    while((a!=0) && (b!=0))
        if(a->item < b->item)
        {c->next = a; c= a; a = a->next;}
    	else
        {c->next = b ;c= b ; b= b->next;}
    c->next = (a==0) ? b :a;
    return head->next;
}
// bottom-up
link mergesort(link t){
    QUEUE<link> Q(max);
    if(t == 0 || t->next == 0) return t;
    for(link u = 0 ; t != 0 ; t = u)
    {u = t->next ; t->next = 0; Q.put(t);}
    t = Q.get();
    while(!Q.empty())
    {Q.put(t); t = merge(Q.get(),Q.get());}
    return t;
}

// top-down
link mergesort(link c){
    if( c==0 || c->next == 0) return c;
    //splits link pointed by c into two lists a, b
    //then sorting two halves recursively
    //and finally merging them
    link a = c, b = c->next;
    while((b!=0) && (b->next!= 0))
    { c = c->next; b = b->next->next;}
    b = c->next; c->next = 0;
    return merge(mergesort(a),mergesort(b));
}
````



---

## File: dsa/sorting/ch4.md

# Special Sorting Techniques

NOTE: Its good to know these techniques rather than understanding in great detail.

## Batcher’s Odd-Even Mergesort

Batcher’s Odd-Even Mergesort is a comparison-based parallel sorting algorithm, known for its deterministic structure and regular data access patterns, making it highly suitable for hardware implementation like on GPUs, FPGAs, and sorting networks.

Implementation - [Link](https://algo.minetest.in/3-Sorting/11-Special_purpose_sorting_methods/1-Batchers_OddEven/)

## External Sorting

External sorting is a class of sorting algorithms that can handle massive amounts of data. External sorting is required when the data being sorted do not fit into the main memory of a computing device (usually RAM) and instead they must reside in the slower external memory, usually a disk drive. Thus, external sorting algorithms are external memory algorithms and thus applicable in the external memory model of computation. 

More - [Algo Site](https://algo.minetest.in/3-Sorting/11-Special_purpose_sorting_methods/3-External_Sorting/)  [Wiki Article](https://en.wikipedia.org/wiki/External_sorting)

## Parallel MergeSort

Paper - [Parallel Merge Sort](https://www.sjsu.edu/people/robert.chun/courses/cs159/s3/T.pdf)

## Counting Sort

Counting Sort is a non-comparison-based linear-time sorting algorithm suitable for integers in a fixed range. It works by counting the frequency of each unique element, then calculating prefix sums to determine positions in the output array.

* No Comparisons
* Time Complexity : $O(n+k)$ where n is the number of elements, and k is the range of input.
* Space : $O(k)$
* Ideal for **bucket-based grouping**, **radix sort**, or **histogram generation**.

## Radix Sort

**Radix Sort** is a **non-comparison** sorting algorithm that sorts numbers digit by digit, starting either from the least significant digit (**LSD**) or most significant digit (**MSD**), using a **stable sort** (like Counting Sort) at each digit level.

[Full Chapter in Detail](https://algo.minetest.in/3-Sorting/10-Radix_Sorting/)

## Bucket Sort

**Bucket Sort** distributes elements into several buckets, then sorts each bucket (typically using **insertion sort**) and concatenates them.

* Use it when Inputs are **uniformly distributed floating-point numbers in [0, 1)**
* You want **average-case linear time**
* Data is spread out over a range and simple sorting within chunks is faster

````python
def bucket_sort(arr):
    n = len(arr)
    buckets = [[] for _ in range(n)]

    for num in arr:
        index = int(num * n)
        buckets[index].append(num)

    for i in range(n):
        buckets[i].sort()

    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result
````


---

## File: dsa/stknq/ch1.md

# Stack Operations & Application

*A stack is a linear data structure that follows the Last-In First-Out (LIFO) principle.*

**Basic Stack Operations**

* Push - *Insert and element on top of the stack*
* Pop - *Remove the top element from the stack*
* Peek/Top - *View the top element without removing it*
* isEmpty - *Check whether stack is empty*

## Application of Stack

* Function Call Management
  * Every function call is pushed to the *call* stack and popped when it returns
* Expression Evaluation and Conversion
  * Infix to Postfix/Prefix Conversion
  * Postfix Expression Evaluation
* Undo Mechanisms in Editors and Apps
  * Each operation is pushed onto a stack, `undo` just pops the last action
* Syntax Parsing
  * Used in Compilers to parse Expressions, Match Brackets, and More
* Backtracking
  * Pathfinding, Maze Solving, Puzzle Solving (DFS uses stack)
* Memory Management
  * Stacks are use for **stack frame** in program execution

## STL & Python Usage

Python (`builtin` or `collections.deque`)

| **Operation** | **Using list**  | **Using deque**                                        |
| ------------- | --------------- | ------------------------------------------------------ |
| Create stack  | stack = []      | `from collections import deque` then `stack = deque()` |
| Push          | stack.append(x) | stack.append(x)                                        |
| Pop           | stack.pop()     | stack.pop()                                            |
| Peek          | stack[-1]       | stack[-1]                                              |
| Check empty   | not stack       | not stack                                              |

NOTE: `deque` is faster and preferred for large-scale stack operations

C++ (`std::stack`)

| **Operation** | **Function** | **Notes**                    |
| ------------- | ------------ | ---------------------------- |
| Create stack  | stack<T> s   | T is the data type           |
| Push          | s.push(x)    | Adds x to top                |
| Pop           | s.pop()      | Removes top element          |
| Peek          | s.top()      | Returns top without removing |
| Check empty   | s.empty()    | Returns true if empty        |
| Size          | s.size()     | Returns number of elements   |

- To use a different container: `stack<int, vector<int>> s; or stack<int, deque<int>> s;`

### Problems

* Valid Parentheses (20)
* Min Stack (155)
* String Reversal
* Basic Calculator
* Longest Valid Parentheses
* Decode String
* Remove K Digits

---

## File: dsa/stknq/ch2.md

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

---

## File: dsa/stknq/ch3.md

# Expression Evaluation & Parsing

### Expression Types

* Infix : `a + b * c`
* Postfix (RPN): `a b c * +`
* Prefix: `+ a * b c`

### Stack - Based Evaluation

* Convert Infix into Postfix using Stack (Shunting Yard Algorithm)
* Evaluate Postfix using stack:
  * If operand - `push`
  * If operator `pop two operands, evaluate, push result`

### Problems

* Evaluate Reverse Polish Notation (150)
* Infix to Postfix Convertor
* Basic Caculator
* Expression Parsing 


---

## File: dsa/stknq/ch4.md

# Techniques

## Monotonic Stack

*A monotonic stack is a stack that maintains elements in increasing or decreasing order*

Applications

* Next Greater Element
* Largest Rectangle in Histogram
* Stock Span Problem
* Daily Temperature

### Next Greater Element

````python
# Next Greater Element
nums = [2, 1, 2, 4, 3]
stack = []
res = [-1] * len(nums)
for i in range(len(nums)):
    while stack and nums[i] > nums[stack[-1]]:
        idx = stack.pop()
        res[idx] = nums[i]
    stack.append(i)
````

## Sliding Window Maximum

Given an array nums and window of size k, return the max of each sliding window

Applications

* Real-time data analysis
* Maximum in Streaming Data
* Temperature Monitoring, Sensor logs

````python
from collections import deque
def maxSlidingWindow(nums, k):
    dq, res = deque(), []
    for i in range(len(nums)):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
````



---

## File: dsa/strings/ch1.md

# Basic String Processing

### Application of String Processing

- Information Processing
- Genomics
- Communication Books
- Programming Systems

**Rules of the Game**

For clarity there are several assumptions and definitions that we will make use of ahead.

- *Characters* : A `String` is a sequence of characters. Characters are of type `char`.
- *Immutability* : String objects are immutable. Their values doesn't change while assigning statements and as arguments and return values.
- *Indexing* : Operation to extract a specified character from a string.
- *Length* : Size of the string
- *Substring* : extract a specified substring operation. We expect a constant time implementation of this.
- *Concatenation* : Creating a new string by appending one string to another.
- *Character Arrays* : We can alternately use an array of character as direct abstraction for string.

Main point to focus here is understanding the efficiency of each operation.

Not all languages provide same implementation of String for e.g. in C it may take linear time to determine the length of String.

## Basic Problem Categorization in String Processing

* Searching and Matching
  * Pattern Matching
  * Exact Match
  * Approximate Match
* Transformation
  * Reversal
  * Substitution
* Parsing and Tokenization
  * Splitting
  * Parsing
* Dynamic String Construction
  * Concatenation
  * Building Substrings
* Structural Analysis

## C++/Python Strings

| Feature                  | Python                               | C++                                       |
| ------------------------ | ------------------------------------ | ----------------------------------------- |
| **String Mutability**    | Immutable strings (must create new)  | Mutable with std::string or char[].       |
| **Indexing**             | 0-based; supports negative indexing. | 0-based; no negative indexing.            |
| **Length**               | O(1) via len().                      | O(1) via string.size().                   |
| **Substring Extraction** | O(1) with slicing (s[start:end]).    | O(n), substr() creates a copy.            |
| **Concatenation**        | O(n) due to creation of new strings. | O(n) via + or append().                   |
| **Character Arrays**     | Not used, strings directly used.     | Commonly used with char[] or std::string. |

## Common String Operations

### Checking Palindrome

* Python : `s == s[::-1]` (Read about python slices)
* C++ : use std::reverse() and compare

### Converting Case

* Python : `s.upper(), s.lower()`
* C++: Use `transform()` from `<algorithms>`

### Sorting Characters:

* Python: `sorted(s)` returns a list
* C++: `sort(s.begin(), s.end())`

### Counting Frequency

* Python: `collections.Counter(s)` or `s.count(ch)`
* C++: Use a frequency array for faster processing

### NOTES on String Efficiency

* Avoid concatenation in loops
  * in python `join()` is faster
  * Use `ostringstream` or `stringstream ` in C++ for efficient appending
* Use Substrings Sparingly
  * python slices are efficient
  * but avoid using `substr` in C++ to avoid copy overhead
* Precompute lengths
  * repeated calls to `len` or `size` are unnecessary, better to cache in a variable.

## Problems

1. https://leetcode.com/problems/roman-to-integer/description/ 
2. https://leetcode.com/problems/string-to-integer-atoi/ painful to process question :)
3. https://leetcode.com/problems/encode-and-decode-strings/description/
4. https://leetcode.com/problems/string-compression/description/


---

## File: dsa/strings/ch2.md

# String Matching

## Library Solution

Modern programming languages provide library solutions for basic string matching. These solutions are highly optimized and can be used directly for simple problems

### C++

C++ offers several built-in functions in the <string> library for string matching:

* `find()`: Returns the index of the first occurrence of a substring.
* `substr()`: Extracts a portion of the string.

````c++
string text = "hello world";
string pattern = "world";
size_t pos = text.find(pattern);
if (pos != string::npos) {
    cout << "Pattern found at index " << pos << endl;
} else {
    cout << "Pattern not found" << endl;
}
````

### Python

Python simplifies string matching with built-in methods:

* `find()`: Returns the index of the first occurrence of a substring or -1 if not found.
* `in` **operator**: Checks for substring presence.

````c++
text = "hello world"
pattern = "world"
if pattern in text:
    print(f"Pattern found at index {text.find(pattern)}")
else:
    print("Pattern not found")
````

## String Hashing

String hashing is a preprocessing technique that converts a string into a numeric value (hash). This value allows efficient comparisons of substrings.

Algorithm

* Choose a **base** (e.g., 31) and a **modulus** (e.g., $10^9+7$).

* Compute the hash of the string using the formula:

  $$H[i] = (H[i-1] \cdot \text{base} + \text{char}[i]) \mod \text{modulus}$$

* Use **prefix hashes** to compute substring hashes efficiently.

````c++
vector<long long> compute_hash(string s, int base, int mod) {
    vector<long long> hash(s.size() + 1, 0);
    long long power = 1;
    for (int i = 0; i < s.size(); i++) {
        hash[i + 1] = (hash[i] * base + (s[i] - 'a' + 1)) % mod;
        power = (power * base) % mod;
    }
    return hash;
}
````

## Rabin-Karp

The Rabin-Karp algorithm uses hashing to find all occurrences of a pattern in a text.

Algorithm

* Precompute the hash of the pattern and the initial substring of the text of the same length.
* Slide over the text:
  * If the hashes match, verify the strings.
  * Recompute the hash for the next substring in O(1)
* Complexity: O(N + M) on average.
* Things to consider while implementation
  * Always verify with string comparison after hash match
  * Consider double hashing for critical applications
  * Birthday Paradox - The **Birthday Paradox** refers to the counterintuitive probability result that in a group of just 23 people, there is about a 50% chance that at least two people share the same birthday. Shows the vulnerability of hash functions to collisions, leading to the "birthday attack" where finding two inputs that hash to the same output is easier than expected.


````c++
bool rabin_karp(string text, string pattern) {
    int n = text.size(), m = pattern.size();
    int base = 31, mod = 1e9 + 7;
    long long pattern_hash = 0, text_hash = 0, power = 1;

    for (int i = 0; i < m; i++) {
        pattern_hash = (pattern_hash * base + (pattern[i] - 'a' + 1)) % mod;
        text_hash = (text_hash * base + (text[i] - 'a' + 1)) % mod;
        if (i > 0) power = (power * base) % mod;
    }

    for (int i = 0; i <= n - m; i++) {
      
      	// Always verify with string comparison after hash match (left as to-do)
        if (pattern_hash == text_hash && text.substr(i, m) == pattern)
            return true;
        if (i < n - m) {
            text_hash = (text_hash - (text[i] - 'a' + 1) * power) % mod;
            text_hash = (text_hash * base + (text[i + m] - 'a' + 1)) % mod;
            if (text_hash < 0) text_hash += mod;
        }
    }
    return false;
}
````

## Z-Function

The Z-function computes an array where Z[i] is the length of the longest substring starting from i that matches the prefix of the string.

Applications

* Pattern Matching (Exact Match) : concatenate P and T : `P + '$' + T`, compute Z-function for such string. If $Z[i] \geq \text{length of } P$ , the pattern occurs starting at $i - (\text{length of } P + 1$) 
* Finding Periods in Strings
* Counting Unique Substrings
* String Compression

Algorithm

* Initialize Z[0] = 0 .
* Maintain a window [L, R] that matches the prefix.
* For each i :
  * If $i \leq R$, use previously computed values.
  * Otherwise, compute Z[i] directly
* Complexity: O(N)

````c++
vector<int> compute_z(string s) {
    int n = s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;

    for (int i = 1; i < n; i++) {
        if (i <= r) z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}
````

## Prefix Function (KMP) Algorithm

The Knuth-Morris-Pratt (KMP) algorithm avoids redundant comparisons by precomputing a prefix function(lps).

Algorithm

* Compute the prefix function:
  *  $\text{pi}[i]$ is the length of the longest prefix that is also a suffix for the substring ending at i .
* Use $\text{pi}[]$ to skip unnecessary comparisons
* Complexity: O(N + M).

````c++
vector<int> compute_prefix_function(string pattern) {
    int m = pattern.size();
    vector<int> pi(m, 0);

    for (int i = 1, j = 0; i < m; i++) {
        while (j > 0 && pattern[i] != pattern[j]) j = pi[j - 1];
        if (pattern[i] == pattern[j]) j++;
        pi[i] = j;
    }
    return pi;
}
````

````c++
// using above function to perform KMP Search
int strStr(string haystack, string needle) {
    int n = needle.size();
    if (n == 0) return 0;

    vector<int> lps = compute_prefix_function(needle);

    // Perform the KMP search
    int i = 0; 
    j = 0; 
    while (i < haystack.size()) {
        if (haystack[i] == needle[j]) {
            i++;
            j++;
        }
        if (j == n) {
            return i - n; // Pattern found at index (i - n)
        }
        if (i < haystack.size() && haystack[i] != needle[j]) {
            if (j > 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }

    return -1; // Pattern not found
}
````



---

## File: dsa/strings/ch3.md

# Trie

A **Trie** (pronounced “try”) is a tree-like data structure used to store a dynamic set of strings. Each node in the Trie represents a single character, and strings are represented as paths from the root to a leaf node. It is mainly used for:

* Word search (exact match)

* Prefix search (words starting with a prefix)

Its commong use-cases are

* Auto-Complete
* Spell Checker
* Longest Prefix Matching

![Trie](./ch3.assets/1050.png)

````c++
class Trie {
public:
    Trie() { root = new TrieNode(); }

    // Insert a word into the Trie
    void insert(const string& word) {
        TrieNode* tmp = root;
        for (char c : word) {
            int i = c - 'a';
            if (tmp->next[i] == nullptr)
                tmp->next[i] = new TrieNode();
            tmp = tmp->next[i];
        }
        tmp->end = true;
    }

    // Check if a word exists in the Trie
    bool search(const string& word) {
        TrieNode* tmp = root;
        for (char c : word) {
            int i = c - 'a';
            if (tmp->next[i] == nullptr) return false;
            tmp = tmp->next[i];
        }
        return tmp->end;
    }

    // Check if any word starts with the given prefix
    bool startsWith(const string& prefix) {
        TrieNode* tmp = root;
        for (char c : prefix) {
            int i = c - 'a';
            if (tmp->next[i] == nullptr) return false;
            tmp = tmp->next[i];
        }
        return true;
    }

private:
    struct TrieNode {
        vector<TrieNode*> next;
        bool end;
        TrieNode() : next(26, nullptr), end(false) {}
    };

    TrieNode* root;
};
````



---

## File: dsa/strings/ch4.md

# Suffix Tree

* A suffix tree is a compressed trie containing all the suffixes of the given text as their keys and positions in the text as their values.
* Allows particularly fast implementations of many important string operations
* The Suffix tree for a text `X` of size `n` from an alphabet of size `d` 
  * stores all the `n(n-1)/2` suffixes of `X` in `O(n)` space.
  * can be constructed in `O(dn)` time
  * supports arbitrary pattern matching and prefix matching queries in `O(dm)` time, where `m` is length of the pattern

Example - Given a string `banana$` create its suffix tree. NOTE: `$` : represents string termination.

Generating the suffixes by hand would give us following : `banana$, anana$, nana$, ana$, na$, a$ , $`

Construct a trie for the data, which is a space-intensive method to represent it as a tree. Instead, create a suffix tree from the data.

| ![image-20250515114245532](./ch4.assets/image-20250515114245532.png) |
| ------------------------------------------------------------ |
| Above representation is not efficient in terms of space, we can represent a suffix as shown below. |
| ![image-20250515113825221](./ch4.assets/image-20250515113825221.png) |
| The number in the leaf refers to the index into `s` where the suffix represented by the leaf begins. |

* Actual algorithm work in following way, To add a new suffix to tree, we walk down the current tree, until we come to a place where the path leads off of the current tree.
* This could happen at anywhere in tree, middle of the edge, or at an already existing node,
  * In first cast we split the edge in two and add a new node with branching factor of 2 in the middle
  * second case simply add a new edge from an already existing node.
* Thus number of node in the tree is O(n) (NOTE: Naive construction above is still $O(N^2)$ which can be optimized)
* NOTE: Ukkonen’n Algorithm (linear time) for creating suffix tree. [Link](https://en.wikipedia.org/wiki/Ukkonen's_algorithm)

# Suffix Array

* **in practice**, people rarely implement full **suffix trees**, especially not Ukkonen’s algorithm
* In a practical scenario : Suffix Array + LCP Array = Practical Suffix Tree Substitute
* A suffix array is simply a sorted list of all suffixes of the string. Taking previous example.

````c++
Suffixes:         Sorted Order:
0: banana$        6: $
1: anana$         5: a$
2: nana$          3: ana$
3: ana$           1: anana$
4: na$            0: banana$
5: a$             4: na$
6: $              2: nana$
````

* Suffix Array would be : `[6, 5, 3, 1, 0, 4, 2]`
* LCP Array is Longest Common Prefix : It tells the length of the common prefix between consecutive suffixes in the sorted suffix array. Here LCP = `[0, 1, 3, 0, 0, 2, 0]`

| **Feature**                | **Suffix Tree**          | **Suffix Array + LCP**                        |
| -------------------------- | ------------------------ | --------------------------------------------- |
| **Construction Time**      | O(n) with Ukkonen’s algo | O(n log n) or O(n) with tricks                |
| **Space Usage**            | High (nodes, pointers)   | Low (arrays only)                             |
| **Ease of Implementation** | Very hard                | Easy to moderate                              |
| **Pattern Matching**       | O(m)                     | O(m log n)                                    |
| **Use in Practice**        | Rarely used directly     | Common (bioinformatics, search engines, etc.) |

## Suffix Array Implementation

* Build Suffix Array in $O(n \log n)$
* Build LCP Array using Kasai’s algorithm in $O(n)$
* Supports
  * Pattern Matching
  * Longest Repeated Substring
  * Count of distinct substring

````c++
#include <bits/stdc++.h>
using namespace std;

class SuffixStructure {
private:
    string s;
    int n;
    vector<int> sa, rank, lcp;

    void buildSA() {
        sa.resize(n);
        vector<int> tmp(n), cnt(max(256, n));
        iota(sa.begin(), sa.end(), 0);
        rank.resize(n);
        for (int i = 0; i < n; ++i) rank[i] = s[i];

        for (int k = 1; k < n; k <<= 1) {
            auto cmp = [&](int i, int j) {
                if (rank[i] != rank[j]) return rank[i] < rank[j];
                int ri = (i + k < n) ? rank[i + k] : -1;
                int rj = (j + k < n) ? rank[j + k] : -1;
                return ri < rj;
            };
            sort(sa.begin(), sa.end(), cmp);

            tmp[sa[0]] = 0;
            for (int i = 1; i < n; ++i)
                tmp[sa[i]] = tmp[sa[i - 1]] + cmp(sa[i - 1], sa[i]);
            rank = tmp;
        }
    }

    void buildLCP() {
        lcp.resize(n);
        vector<int> inv(n);
        for (int i = 0; i < n; ++i) inv[sa[i]] = i;

        int k = 0;
        for (int i = 0; i < n; ++i) {
            if (inv[i] == 0) continue;
            int j = sa[inv[i] - 1];
            while (i + k < n && j + k < n && s[i + k] == s[j + k]) k++;
            lcp[inv[i]] = k;
            if (k) k--;
        }
    }

public:
    SuffixStructure(const string &str) : s(str + "$"), n(str.size() + 1) {
        buildSA();
        buildLCP();
    }

    // Find if pattern exists in O(m log n)
    bool contains(const string &pattern) {
        int l = 0, r = n - 1;
        while (l <= r) {
            int m = (l + r) / 2;
            string suffix = s.substr(sa[m], pattern.size());
            if (suffix == pattern) return true;
            else if (suffix < pattern) l = m + 1;
            else r = m - 1;
        }
        return false;
    }

    // Longest repeated substring
    string longestRepeatedSubstring() {
        int len = 0, pos = 0;
        for (int i = 1; i < n; ++i) {
            if (lcp[i] > len) {
                len = lcp[i];
                pos = sa[i];
            }
        }
        return s.substr(pos, len);
    }

    // Number of distinct substrings
    long long countDistinctSubstrings() {
        long long total = 1LL * n * (n - 1) / 2; // sum of lengths of all suffixes
        long long repeated = accumulate(lcp.begin(), lcp.end(), 0LL);
        return total - repeated;
    }

    // Getters
    vector<int> getSA() { return sa; }
    vector<int> getLCP() { return lcp; }
};
````

## Problems

| **Problem**                                                  | **Problem Type**       | **Optimal with**        | **Notes**                                                    |
| ------------------------------------------------------------ | ---------------------- | ----------------------- | ------------------------------------------------------------ |
| [#336. Palindrome Pairs](https://leetcode.com/problems/palindrome-pairs/) | Substring checks       | Trie / Suffix tree idea | Though typically solved with tries, suffix structures help in understanding efficient string lookups. |
| [#472. Concatenated Words](https://leetcode.com/problems/concatenated-words/) | Substring parsing      | Trie / DP               | Suffix tree logic helps if asked to optimize DP further.     |
| [#920. Number of Music Playlists](https://leetcode.com/problems/number-of-music-playlists/) | Rare use case          | DP + Combinatorics      | Suffix trees aren’t a fit here, but LCP might be used to optimize substring checks. |
| [#1044. Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/) | **Direct application** | **Suffix Array + LCP**  | This is the **clearest modern Suffix Tree replacement problem** on LeetCode. |
| [#1153. String Compression II](https://leetcode.com/problems/string-compression-ii/) | Optimization           | DP + Preprocessing      | Advanced string structure can help, but not common in brute-force. |
| [#1326. Minimum Number of Taps to Open to Water a Garden](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/) | Interval covering      | Segment Tree            | Not suffix-related, but string segment problems sometimes align with this. |
| [#1178. Number of Valid Words for Each Puzzle](https://leetcode.com/problems/number-of-valid-words-for-each-puzzle/) | Bitmask / Trie         | Trie / hashing          | Again, tries are more practical here.                        |

### Summary

* Most of technical interviews will not ask for Suffix Tree/Suffix Array unless you are going for competitive coding, in that case Suffix Array + LCP would be enough to answer most of the questions

---

## File: dsa/strings/ch5.md

# String Processing with DP

- String DP problems usually involve breaking a string into smaller parts and solving subproblems based on those. It includes:
  - Subsequence & substring analysis
  - Palindromes
  - Pattern matching
  - Partitioning
  - Edit distances

### Core Concepts

- Substrings vs Subsequences
  - **Substring**: Continuous sequence (e.g. "abc" in "abcd").
  - **Subsequence**: Can skip characters but maintain order (e.g. "acd" in "abcd").
- State Design
  - Most problems are defined using:
  - `dp[i][j]` → answer for the substring `s[i..j]`
  - `dp[i][j]` → answer for prefixes/suffixes
  - `dp[i]` → answer for prefix of length `i`
- Recurrence Patterns
  - Try partitioning the string at every k, solving for `i..k` and `k+1..j`.
  - Use memoization to avoid recomputing overlapping subproblems.

### Classic Patterns

- Longest Common Subsequence (LCS)

````c++
if s1[i-1] == s2[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
````

- Longest Palindromic Subsequence

````c++
if s[i] == s[j]:
    dp[i][j] = 2 + dp[i+1][j-1]
else:
    dp[i][j] = max(dp[i+1][j], dp[i][j-1])
````

- Longest Palindromic Substring

````c++
dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]
````

- Edit Distance

````c++
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1]
else:
    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
````

### Advance Patterns

- Palindrome Partitioning
- State
  - `is_pal[i][j]` = True/False for checking palindromes
  - `dp[i]` = min cuts for `s[0..i]`

````c++
if is_pal[j][i]:
    dp[i] = min(dp[i], 1 + dp[j-1])
````

- Count Distinct Subsequences
  - **Problem**: Count how many times t occurs as a subsequence of s
  - State: `dp[i][j]` = ways to form `t[0..j-1]` using `s[0..i-1]`

````c++
if s[i-1] == t[j-1]:
    dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
else:
    dp[i][j] = dp[i-1][j]
````



---

## File: dsa/strings/ch6.md

# String Tasks

String tasks involve manipulation, analysis, and transformation of strings. These are frequently encountered in contests and technical interviews.

### Character Counting & Frequency Maps

- Useful for **anagrams**, **palindromes**, or finding **most/least frequent characters**.
- Use Counter (Python) or arrays (int[26] for lowercase letters).

````python
from collections import Counter
freq = Counter(s)
````

### Prefix / Suffix Processing

- Compute **prefix sums**, **hashes**, or match substrings from the start or end.
- s.startswith("abc"), s.endswith("xyz") (Python methods)

### Palindrome Checks

- Reverse and compare: s == s[::-1]
- Efficient check for substrings using 2 pointers or dynamic programming.

### Lexicographical Comparisons

- Compare strings as numbers or words: "abc" < "abd" → True
- Useful for finding minimal/maximal rotations or rearrangements.

### Sliding Window on Strings

- For substring problems like finding the smallest/biggest/first substring with some property.
- Time: O(n) with hashmap or frequency arrays.

Example: Longest substring without repeating characters.

### String Hashing (Rabin-Karp)

- Compute hash of substrings in O(1) using prefix hash arrays.
- Useful for **duplicate substrings**, **pattern matching**, or **string equality checks**.

### Z-Algorithm / Prefix Function (KMP)

- Efficient pattern matching.
- Find all occurrences of a pattern in a text in O(n + m).

### Minimum / Maximum Operations

- Turn string to palindrome, make all chars equal, reduce to one character, etc.
- Usually involves DP or greedy strategies.

````python
s.split(), s.replace(), re.findall()
````

### String Rewriting / Parsing

- Tokenize by space, delimiter, regex.
- Replace substrings, compress sequences, etc.

---

## File: dsa/strings/ch7.md

# Compression & Encoding Techniques

These are used in both practical applications (like ZIP files, web protocols) and algorithm problems (e.g. Run-Length Encoding, Huffman Coding).

## Run-Length Encoding

- Replace repeating characters with a count.

````python
Input: "aaabbc"
Output: "a3b2c1"
````

````python
def rle(s):
    res = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        res.append(s[i] + str(j - i))
        i = j
    return ''.join(res)
````

## Huffman Coding

**Idea:**

- Variable-length encoding based on character frequency (used in compression algorithms like ZIP, JPEG).

**Steps:**

1. Count frequency of each character.
2. Build a **min-heap** to construct a **binary tree**.
3. Traverse the tree to assign binary codes.

**Properties:**

- Prefix-free codes (no code is prefix of another).
- Greedy algorithm.

Useful in:

- Data compression
- Encoding tasks

## Trie-Based Compression

- Tries (prefix trees) efficiently store sets of strings with common prefixes.
- Space-efficient for autocomplete, spell-checkers, or dictionary encoding.

## Burrows-Wheeler Transform (BWT)

Used in compression (e.g. bzip2) and bioinformatics.

- Rearranges the string into a form more amenable to compression.
- Requires suffix array or rotations.

## Dictionary Encoding (LZW)

- Replaces repeating substrings with dictionary indices.
- Used in image compression (GIF) and data formats.

---

## File: dsa/trees/ch1.md

# Trees

* Trees are heirarchical data structures consisting of nodes connected by edges.
* Each tree has a root node, and zero or more child nodes forming a *parent-child* relationship without cycles.

## Types of Trees

| Tree Type                    | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| **Binary Tree**              | Each node has at most two children (left and right).         |
| **Binary Search Tree (BST)** | A binary tree where left child < parent < right child, enabling efficient search operations. |
| **Balanced Trees**           | Trees maintaining height balance for efficient operations (e.g., AVL, Red-Black trees). |
| **Heap**                     | Complete binary tree satisfying heap property (min-heap or max-heap). |
| **Trie (Prefix Tree)**       | Tree used for storing strings, where each node represents a character, enabling fast prefix queries. |
| **Fenwick Tree (BIT)**       | Binary Indexed Tree for efficient prefix sum queries and updates. |
| **Segment Tree**             | Tree structure to efficiently answer range queries and updates on arrays. |
| **N-ary Tree**               | Each node can have any number of children, generalizing binary trees. |
| **Suffix Tree**              | Compressed trie of all suffixes of a string, used in string processing. |

## Implementation

````c++
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};
````

## Tree Traversal

| Traversal Type  | Description                      | Order of Processing                    |
| --------------- | -------------------------------- | -------------------------------------- |
| **Preorder**    | Visit root, traverse left, right | Root → Left → Right                    |
| **Inorder**     | Traverse left, visit root, right | Left → Root → Right                    |
| **Postorder**   | Traverse left, right, visit root | Left → Right → Root                    |
| **Level Order** | Traverse level by level (BFS)    | Top to bottom, left to right per level |

### Traversal Implementation

````c++
void preorder(TreeNode* root) {
    if (!root) return;
  	cout << root->val << " ";
    preorder(root->left);
    preorder(root->right);
}

void inorder(TreeNode* root) {
    if (!root) return;
    inorder(root->left);
    cout << root->val << " ";
    inorder(root->right);
}

void postorder(TreeNode* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    cout << root->val << " ";
}

void levelOrderTraversal(TreeNode* root) {
    if (!root) return;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* node = q.front(); q.pop();
        cout << node->val << " ";
        if (node->left) q.push(node->left);
        if (node->right) q.push(node->right);
    }
}
````

## Binary Search Trees

* NOTE: Inorder traversal of the BST returns a sorted list

````c++
#include <iostream>
using namespace std;

class BST {
private:
    struct Node {
        int key;
        Node *left, *right;
        Node(int k) : key(k), left(nullptr), right(nullptr) {}
    };

    Node* root;

    // Recursive search
    Node* search(Node* node, int key) {
        if (node == nullptr || node->key == key)
            return node;
        if (key < node->key)
            return search(node->left, key);
        else
            return search(node->right, key);
    }

    // Recursive insert
    void insert(Node*& node, int key) {
        if (node == nullptr) {
            node = new Node(key);
            return;
        }
        if (key < node->key)
            insert(node->left, key);
        else
            insert(node->right, key);
    }

public:
    BST() : root(nullptr) {}

    // Public API
    void insert(int key) { insert(root, key); }
    bool search(int key) { return search(root, key) != nullptr; }
};
````



---

## File: dsa/trees/ch2.md

## Problems on Binary Trees & BST



| Types                         | Pattern                                         | Examples                                         |
| ----------------------------- | ----------------------------------------------- | ------------------------------------------------ |
| **Recursion with Return**     | Return values from children, accumulate results | Path Sum in Tree, Sum of Subsets                 |
| **Recursion with Parameters** | Track path, state                               | Subsequence with sum K, Combinations with k size |

| Problem Type                       | Description                                         | Example Questions          |
| ---------------------------------- | --------------------------------------------------- | -------------------------- |
| **Basic Traversals**               | Implement preorder, inorder, postorder, level order | Leetcode 94, 144, 102      |
| **Lowest Common Ancestor (LCA)**   | Find lowest shared ancestor of two nodes            | Leetcode 236, 1650         |
| **Balanced Tree Check**            | Check if tree height difference is bounded          | Leetcode 110               |
| **Validate BST**                   | Check if a binary tree satisfies BST property       | Leetcode 98                |
| **Serialize & Deserialize**        | Convert tree to string and back                     | Leetcode 297               |
| **Diameter of Binary Tree**        | Longest path between any two nodes                  | Leetcode 543               |
| **Path Sum**                       | Check if path with given sum exists                 | Leetcode 112, 113          |
| **Construct Tree from Traversals** | Rebuild tree from preorder/inorder/postorder        | Leetcode 105, 106          |
| **Trie Operations**                | Insert, search, prefix queries                      | Leetcode 208               |
| **Fenwick & Segment Trees**        | Range queries and updates                           | Range sum, minimum queries |



## Problems

### Binary Tree Maximum Path Sum

- [Problem Link](https://leetcode.com/problems/binary-tree-maximum-path-sum/)
- We have to find a path in the binary tree, that gives the max sum
- Maximum at a node could be following
  - Node’s value
  - Node’s value + max. sum from left subtree
  - Node’s value + max. sum from right subtree
  - Node’s Value + max. sum including both subtree

````c++
int maxSum = INT_MIN;
int solve(TreeNode* node) {
    if(!node)
        return 0;
    int left = max(solve(node->left), 0);
    int right = max(solve(node->right), 0);
    int rooted = node->val + left + right;

    maxSum = max(maxSum, rooted); // no need to check other 3 condition

    return node->val + max(left, right);
}
int maxPathSum(TreeNode* root) {
    solve(root);
    return maxSum;
}
````







**Most Commonly Asked Interview Questions**

| Question Name                                     | Description                       | Difficulty |
| ------------------------------------------------- | --------------------------------- | ---------- |
| Binary Tree Inorder Traversal                     | Recursive and iterative traversal | Easy       |
| Validate Binary Search Tree                       | Check BST property                | Medium     |
| Lowest Common Ancestor of a Binary Tree           | Find LCA without BST property     | Medium     |
| Serialize and Deserialize Binary Tree             | Convert tree to string and back   | Hard       |
| Maximum Depth of Binary Tree                      | Find height of tree               | Easy       |
| Balanced Binary Tree                              | Check if tree is height-balanced  | Medium     |
| Construct Binary Tree from Preorder and Inorder   | Build tree from traversals        | Medium     |
| Trie: Implement Insert and Search                 | Basic trie implementation         | Medium     |
| Range Sum Query - Mutable (Segment Tree, Fenwick) | Handle dynamic range queries      | Hard       |

## Selecting Optimal Tree

| **Data Structure**          | **Point Update** | **Point Query** | **Range Update** | **Range Query** | **Time Complexity (Update / Query)** | **Space**  | **Common Use Cases**                                         |
| --------------------------- | ---------------- | --------------- | ---------------- | --------------- | ------------------------------------ | ---------- | ------------------------------------------------------------ |
| **Fenwick Tree (Classic)**  | ✅                | ❌*              | ❌                | ✅ (prefix)      | O(log n) / O(log n)                  | O(n)       | Prefix sums, XORs, frequency counts                          |
| **Fenwick Tree (Dual)**     | ❌                | ✅               | ✅                | ❌               | O(log n) / O(log n)                  | O(n)       | Range add + point read, simulation of cumulative effects     |
| **Fenwick Tree (2-BIT)**    | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(n)       | Full support for sum range queries with range updates        |
| **Segment Tree**            | ✅                | ✅               | ❌                | ✅               | O(log n) / O(log n)                  | O(4n)      | RMQ, range sum/min/max/gcd with point updates                |
| **Segment Tree + Lazy**     | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(4n)      | Full range queries + range updates, e.g., add 5 over [l..r]  |
| **Sparse Segment Tree**     | ✅                | ✅               | ✅                | ✅               | O(log n) / O(log n)                  | O(k log n) | Sparse values over large domains (e.g., up to 1e9)           |
| **Persistent Segment Tree** | ❌ (new ver)      | ✅ (old ver)     | ❌ (immutable)    | ✅ (prev ver)    | O(log n) / O(log n)                  | O(n log n) | Time-travel queries, undo/rollback, version control          |
| **Sqrt Decomposition**      | ✅                | ✅               | ✅* (limited)     | ✅               | O(√n) / O(√n)                        | O(n)       | Simpler implementation for mid-size n, not time-critical problems |
| **Wavelet Tree**            | ❌                | ✅ (rank)        | ❌                | ✅ (freq)        | O(log n) / O(log n)                  | O(n log n) | K-th smallest, rank/select, frequency queries in a range     |

---

## File: dsa/trees/ch3.md

# Range Updates & Queries

## Fenwick Tree (Binary Indexed Trees)

- Supports efficient prefix sums (range sum queries from index 1 to \(j\)) and point updates.
- Internally stores cumulative frequencies in a vector ⁠ft.





## Simple Implementation

````c++
#include <vector>
using namespace std;

class FenwickTree {
private:
    vector<long long> ft;

    int LSOne(int s) { return s & -s; }

public:
    FenwickTree(int n) {
        ft.assign(n + 1, 0); // 1-based indexing
    }

    // Point update: add v to index i
    void update(int i, long long v) {
        while (i < (int)ft.size()) {
            ft[i] += v;
            i += LSOne(i);
        }
    }

    // Prefix sum query: sum[1..i]
    long long rsq(int i) {
        long long sum = 0;
        while (i > 0) {
            sum += ft[i];
            i -= LSOne(i);
        }
        return sum;
    }

    // Range sum query: sum[i..j]
    long long rsq(int i, int j) {
        return rsq(j) - rsq(i - 1);
    }
};
````



## Complete Implementation 

```c++
#include <bits/stdc++.h>
using namespace std;

#define LSOne(S) ((S) & -(S))                    // the key operation

typedef long long ll;                            // for extra flexibility
typedef vector<ll> vll;
typedef vector<int> vi;

class FenwickTree {                              // index 0 is not used
private:
  vll ft;                                        // internal FT is an array
public:
  FenwickTree(int m) { ft.assign(m+1, 0); }      // create an empty FT

  void build(const vll &f) {
    int m = (int)f.size()-1;                     // note f[0] is always 0
    ft.assign(m+1, 0);
    for (int i = 1; i <= m; ++i) {               // O(m)
      ft[i] += f[i];                             // add this value
      if (i+LSOne(i) <= m)                       // i has parent
        ft[i+LSOne(i)] += ft[i];                 // add to that parent
    }
  }

  FenwickTree(const vll &f) { build(f); }        // create FT based on f

  FenwickTree(int m, const vi &s) {              // create FT based on s
    vll f(m+1, 0);
    for (int i = 0; i < (int)s.size(); ++i)      // do the conversion first
      ++f[s[i]];                                 // in O(n)
    build(f);                                    // in O(m)
  }

  ll rsq(int j) {                                // returns RSQ(1, j)
    ll sum = 0;
    for (; j; j -= LSOne(j))
      sum += ft[j];
    return sum;
  }

  ll rsq(int i, int j) { return rsq(j) - rsq(i-1); } // inc/exclusion

  // updates value of the i-th element by v (v can be +ve/inc or -ve/dec)
  void update(int i, ll v) {
    for (; i < (int)ft.size(); i += LSOne(i))
      ft[i] += v;
  }

  int select(ll k) {                             // O(log m)
    int p = 1;
    while (p*2 < (int)ft.size()) p *= 2;
    int i = 0;
    while (p) {
      if (k > ft[i+p]) {
        k -= ft[i+p];
        i += p;
      }
      p /= 2;
    }
    return i+1;
  }
};


```







## Range Update Point Query & Range Query

* Supports **range updates** & **point queries**
* Uses a Fenwick Tree internally but updates the Fenwick Tree in a way that a range update is simulated by two point updates.

````c++
class RUPQ {                                     // RUPQ variant
private:
  FenwickTree ft;                                // internally use PURQ FT
public:
  RUPQ(int m) : ft(FenwickTree(m)) {}
  void range_update(int ui, int uj, ll v) {
    ft.update(ui, v);                            // [ui, ui+1, .., m] +v
    ft.update(uj+1, -v);                         // [uj+1, uj+2, .., m] -v
  }                                              // [ui, ui+1, .., uj] +v
  ll point_query(int i) { return ft.rsq(i); }    // rsq(i) is sufficient
};

class RURQ  {                                    // RURQ variant
private:                                         // needs two helper FTs
  RUPQ rupq;                                     // one RUPQ and
  FenwickTree purq;                              // one PURQ
public:
  RURQ(int m) : rupq(RUPQ(m)), purq(FenwickTree(m)) {} // initialization
  void range_update(int ui, int uj, ll v) {
    rupq.range_update(ui, uj, v);                // [ui, ui+1, .., uj] +v
    purq.update(ui, v*(ui-1));                   // -(ui-1)*v before ui
    purq.update(uj+1, -v*uj);                    // +(uj-ui+1)*v after uj
  }
  ll rsq(int j) {
    return rupq.point_query(j)*j -               // optimistic calculation
           purq.rsq(j);                          // cancelation factor
  }
  ll rsq(int i, int j) { return rsq(j) - rsq(i-1); } // standard
};
````



---

## File: dsa/trees/ch4.md

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



---

## File: dsa/trees/ch5.md

# Sqrt Decomposition

* Divides the array into blocks of size roughly $\sqrt{n}$.
* Each block stores the minimum value of that block.
* Lazy array stores pending updates for each block.

Range Updates

* If the update range is within a single block, apply updates directly to elements and rebuild that block
* If the update range spans multiple blocks:
  * Update partial blocks at the edges directly.
  * For full blocks in between, store lazy updates and update block minimum directly.

Range Minimum Query

* If query range is within a single block, check elements directly.
* Otherwise, check partial blocks at edges and use stored block minimum or lazy values for full blocks in between.

````c++
#include <bits/stdc++.h>
using namespace std;

class SqrtDecomposition {
private:
    int n, blockSize, numBlocks;
    vector<int> A;          // original array
    vector<int> blocks;     // stores minimum of each block
    vector<int> lazy;       // lazy updates for each block

    void applyLazy(int block) {
        if (lazy[block] != INT_MAX) {
            int start = block * blockSize;
            int end = min(n, start + blockSize);
            for (int i = start; i < end; i++) {
                A[i] = lazy[block];
            }
            blocks[block] = lazy[block];
            lazy[block] = INT_MAX;
        }
    }

    void rebuildBlock(int block) {
        int start = block * blockSize;
        int end = min(n, start + blockSize);
        int mn = INT_MAX;
        for (int i = start; i < end; i++) {
            mn = min(mn, A[i]);
        }
        blocks[block] = mn;
    }

public:
    SqrtDecomposition(const vector<int> &initialA) {
        A = initialA;
        n = (int)A.size();
        blockSize = (int)sqrt(n);
        numBlocks = (n + blockSize - 1) / blockSize;
        blocks.assign(numBlocks, INT_MAX);
        lazy.assign(numBlocks, INT_MAX);

        for (int i = 0; i < numBlocks; i++) {
            rebuildBlock(i);
        }
    }

    // Range update: set all elements in [l, r] to val
    void rangeUpdate(int l, int r, int val) {
        int startBlock = l / blockSize;
        int endBlock = r / blockSize;

        if (startBlock == endBlock) {
            applyLazy(startBlock);
            for (int i = l; i <= r; i++) {
                A[i] = val;
            }
            rebuildBlock(startBlock);
        } else {
            // Partial first block
            applyLazy(startBlock);
            int startBlockEnd = (startBlock + 1) * blockSize - 1;
            for (int i = l; i <= startBlockEnd; i++) {
                A[i] = val;
            }
            rebuildBlock(startBlock);

            // Full blocks in between
            for (int b = startBlock + 1; b < endBlock; b++) {
                lazy[b] = val;
                blocks[b] = val;
            }

            // Partial last block
            applyLazy(endBlock);
            int endBlockStart = endBlock * blockSize;
            for (int i = endBlockStart; i <= r; i++) {
                A[i] = val;
            }
            rebuildBlock(endBlock);
        }
    }

    // Range minimum query [l, r]
    int rangeMinQuery(int l, int r) {
        int startBlock = l / blockSize;
        int endBlock = r / blockSize;
        int mn = INT_MAX;

        if (startBlock == endBlock) {
            applyLazy(startBlock);
            for (int i = l; i <= r; i++) {
                mn = min(mn, A[i]);
            }
        } else {
            // Partial first block
            applyLazy(startBlock);
            int startBlockEnd = (startBlock + 1) * blockSize - 1;
            for (int i = l; i <= startBlockEnd; i++) {
                mn = min(mn, A[i]);
            }

            // Full blocks in between
            for (int b = startBlock + 1; b < endBlock; b++) {
                if (lazy[b] != INT_MAX) {
                    mn = min(mn, lazy[b]);
                } else {
                    mn = min(mn, blocks[b]);
                }
            }

            // Partial last block
            applyLazy(endBlock);
            int endBlockStart = endBlock * blockSize;
            for (int i = endBlockStart; i <= r; i++) {
                mn = min(mn, A[i]);
            }
        }
        return mn;
    }
};
````



---

## File: dsa/trees/ch6.md

# Heap

## Simple Max-Heap Implementation

````c++
#include <vector>
#include <iostream>
using namespace std;

class MaxHeap {
private:
    vector<int> heap;

    int parent(int i) { return (i - 1) / 2; }
    int left(int i)   { return 2 * i + 1; }
    int right(int i)  { return 2 * i + 2; }

    // Swim Up (Heapify Up)
    void swim(int i) {
        while (i > 0 && heap[parent(i)] < heap[i]) {
            swap(heap[i], heap[parent(i)]);
            i = parent(i);
        }
    }

    // Sink Down (Heapify Down)
    void sink(int i) {
        int n = heap.size();
        while (left(i) < n) {
            int j = left(i);
            if (right(i) < n && heap[right(i)] > heap[j])
                j = right(i); // pick the larger child
            if (heap[i] >= heap[j])
                break;
            swap(heap[i], heap[j]);
            i = j;
        }
    }

public:
    MaxHeap() {}

    MaxHeap(const vector<int>& arr) {
        heap = arr;
        for (int i = (int)heap.size() / 2 - 1; i >= 0; --i)
            sink(i); // heapify
    }

    void insert(int val) {
        heap.push_back(val);
        swim((int)heap.size() - 1);
    }

    int getMax() {
        return heap.empty() ? -1 : heap[0];
    }

    void removeMax() {
        if (heap.empty()) return;
        heap[0] = heap.back();
        heap.pop_back();
        sink(0);
    }

    void printHeap() {
        for (int x : heap)
            cout << x << ' ';
        cout << '\n';
    }
};
````

### Summary of Operations

| **Operation**       | **Method**   | **Complexity** |
| ------------------- | ------------ | -------------- |
| Insert item         | insert(val)  | O(log n)       |
| Remove max          | removeMax()  | O(log n)       |
| Peek max            | getMax()     | O(1)           |
| Build heap from arr | MaxHeap(arr) | O(n)           |

### Min - Heap Implementation

To convert Max-Heap Implementation into a Min-Heap one

* In `swim()` : change `<` to `>`
* In `sink()` : change `>` to `<`

---

