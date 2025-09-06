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