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
- If odd -> inside, else outside.

![](assets/Pasted%20image%2020260215010916.png)

To find whether a point $(x_p, y_p)$ intersects an edge after raycasting given by pair $[(x_1, y_1), (x_2, y_2)]$ would be intersection if $y_1 \le y_p \le y_2$

![](assets/Pasted%20image%2020260215011159.png)

Another situation could be point could be on the right side of the edge in that there won't be any edge, to find the location of point, we can following diagram.

![](assets/Pasted%20image%2020260215011732.png)

So we realize second condition

$$
x_p < x_1 + \frac{y_p - y_1}{y_2 - y1} * (x_2 - x_1)
$$

```python

def is_inside(edges, xp, yp):
    cnt = 0
    for edge in edges:
        (x1, y1), (x2, y2) = edge
        if (yp < y1) != (yp < y2) and xp < x1 + ((yp-y1)/(y2-y1))*(x2-x1):
            cnt += 1
    return cnt%2 == 1

```

Full Code for Simulation : [Gist Link](https://gist.github.com/inside-code-yt/7064d1d1553a2ee117e60217cfd1d099)
Video for Explanation : [Video Link](https://www.youtube.com/watch?v=RSXM9bgqxJM)
#### Winding Number

- Based on angle the polygon wraps around the point.
- Winding number $\ne 0 \implies$ point is inside.

````c++
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

[Video Explanation](https://www.youtube.com/watch?v=ldHA8UcQI9Q)

Find closest pair in $O(n log n)$ time:

1. Sort points by x-coordinate
2. Recursively solve for left and right halves
3. Combine step: consider only points within $d$ distance of mid-line
4. Sort those by $y$ and check distance within a vertical strip

*Karatsuba Algorithm*

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

## Find Fixed-Radius neighbors of a point

[Video Explanation](https://www.youtube.com/watch?v=w4Dosp2U74Y)


## k-d Trees

Improving above problem.