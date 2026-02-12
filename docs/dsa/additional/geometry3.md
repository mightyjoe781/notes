# Convex Hull

The **Convex Hull** of a set of points is the smallest convex polygon that contains all the points. It’s like stretching a rubber band around the outermost points.

![](assets/Pasted%20image%2020260212083041.png)

Applications in Study Polynomials, Matrix Eigenvalues, Thermodynamics, Quantum Physics, Ethology, etc.
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
- Good when $h$ is small like ~ $\log n$
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

