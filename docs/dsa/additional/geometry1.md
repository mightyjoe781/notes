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
def triangle_area(a, b, c):
    return abs((a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1])) / 2.0)
````

### Polygon Area - Shoelace Formula

- For a polygon with vertices in order $p_0$, $p_1$, ..., $p_{n-1}$, use

````python
def polygon_area(pts):
    n = len(pts)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    return abs(area) / 2.0
````

## Distance

- Between Two Points

- Euclidean Distance

````python
import math

def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])
````

* point to Line `(Ax + By + C = 0)`

````python
def point_line_distance(p, A, B, C):
    return abs(A*p[0] + B*p[1] + C) / math.sqrt(A*A + B*B)
````

- Point to Segment
- Use projection method or brute-force checking

````python
def dist_point_to_segment(p, a, b):
    len2 = dist(a, b) ** 2
    if len2 == 0:
        return dist(p, a)
    t = ((p[0]-a[0])*(b[0]-a[0]) + (p[1]-a[1])*(b[1]-a[1])) / len2
    t = max(0.0, min(1.0, t))
    proj = (a[0] + t*(b[0]-a[0]), a[1] + t*(b[1]-a[1]))
    return dist(p, proj)
````

## Dot & Cross Product

### Dot Product

- $a.b = |a||b| \cos \theta$
- Sign tells about angle
    - `> 0` : acute
    - `< 0` : obtuse
    - `= 0` : orthogonal

````python
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]
````

### Cross Product

- $a \times b = a.x * b.y - a.y * b.x$
- Useful for area, orientation, convex hulls

````python
def cross(a, b):
    return a[0]*b[1] - a[1]*b[0]
````

## Angle between vectors

````python
def angle(a, b):
    return math.acos(dot(a, b) / (math.hypot(a[0], a[1]) * math.hypot(b[0], b[1])))
````

Result is in **radians**. Use `angle * 180.0 / math.pi` to convert to degrees.

## Floating-point precision issues & techniques

- Avoid comparing floats directly, use abs(a - b) < EPS where EPS ~ 1e-9
- Prefer integers where possible (e.g., cross product or Shoelace)
- Use long double for better precision if needed
- Normalize angles or vectors before comparing