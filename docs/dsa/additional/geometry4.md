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