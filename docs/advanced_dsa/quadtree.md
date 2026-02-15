# QuadTree

*Where in space should this belong?*

A quadtree is a *tree data structures* in which each internal node has exactly four children. They are two dimensional analog of *octrees* and are most often used to partition a two-dimensional space by recursively subdividing it into four quadrants or regions.

Generally Leaf Cell represents a *unit of interesting spatial information*

![](assets/Pasted%20image%2020260216003043.png)

Types of quadtree

- Region quadtree : represents *a partition of space* in two dimensions by decomposing the region into four equal quadrants, and so on with each leaf node containing data corresponding to a specific subregion.
    - Examples : Image Compression, Occupancy Grids, Terrain, etc.
- Point quadtree : adaptation of *Binary Tree* used to represent two-dimensional point data. It shares the features of all quadtree but is a true tree as the center of subdivision always on a point. It is often very efficient in comparing 2D, ordered data points, usually operating in $O(\log n)$ time.
    - Surpassed by *k-d trees* as tools for generalized binary tree.
    - Examples: Game Engines, GIS Systems, Physics Engines, etc.
- Loose QuadTree (Industry Favorite) : Nodes slightly overlap boundaries, prevents objects crossing boundaries from bouncing between nodes and heavily used in collision detection engines.

Use Cases

- Image representation
- Image Processing
- Mesh Generation
- Spatial Indexing, Point location queries, and range queries
- Collision Detection
- Maximum disjoint sets

## Python Implementation

![](assets/Pasted%20image%2020260216003122.png)

A Point-Region Quadtree with point data. Bucket Capacity 1

Minimal Usable Implementation

```python

class Rect:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h

    def contains(self, p):
        return (self.x <= p[0] < self.x+self.w and
                self.y <= p[1] < self.y+self.h)

    def intersects(self, other):
        return not (other.x > self.x+self.w or
                    other.x+other.w < self.x or
                    other.y > self.y+self.h or
                    other.y+other.h < self.y)
```

Full Implementation

```python

class QuadTree:
    CAPACITY = 4

    def __init__(self, boundary):
        self.boundary = boundary
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w/2, self.boundary.h/2
        self.nw = QuadTree(Rect(x, y, w, h))
        self.ne = QuadTree(Rect(x+w, y, w, h))
        self.sw = QuadTree(Rect(x, y+h, w, h))
        self.se = QuadTree(Rect(x+w, y+h, w, h))
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < QuadTree.CAPACITY:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        return (self.nw.insert(point) or self.ne.insert(point) or
                self.sw.insert(point) or self.se.insert(point))
                
    def query(self, range_rect, found=None):
        if found is None:
            found = []

        if not self.boundary.intersects(range_rect):
            return found

        for p in self.points:
            if range_rect.contains(p):
                found.append(p)

        if self.divided:
            self.nw.query(range_rect, found)
            self.ne.query(range_rect, found)
            self.sw.query(range_rect, found)
            self.se.query(range_rect, found)

        return found
        
```
### Important Point

- QuadTree -> adaptive grid
- k-d tree -> adaptive split
- R-tree -> bounding boxes of objects

### Real-Life Examples

- Minecraft => Chunk Visibility
- Physics Engines => Collision Broad Phase
- Maps (Google Maps) => Tile Indexing
- Image Compression => Region Compression
- Games => Object Culling