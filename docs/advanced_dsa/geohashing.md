# Geohashing

Excellent way to reduce one type of problem (proximity search) to another, seemingly unrelated one (string prefix matching), allowing databases to re-use their regular index datastructures on these fancy new co-ordinates.

It usually maps `(lat, lng)` to a string.

![](assets/Pasted%20image%2020260216141202.png)

Division along x and y axes are interleaved between bit string. So for every vertical division we give left side a zero and right side a one. And for every horizontal division upper part is given again zero and bottom part is given a one.

We repeatedly divide into two halves producing Binary Path

```
L R L T R T ...
0 1 0 1 1 0 ...
```

This is called as a Z-order Curve (Morton Encoding), nearby points ends up in similar patterns.

Since these binary string could be quite large we encode them using *base32*, starting from the left, the *high-bits*

```
00111 01011 00000
    7    11     0
    
-> "7c0"

```

An important observation is two quadrant which are close share a common prefix. Example `0000` and `0001`, but not necessarily other way around.

Examples :

```
Mount Everent -> tuvz4p0f7
Nearby Point -> tuvz4p0fe
Far Point     -> u4pruydqqv
```

## Python Implementation

```python

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"

def geohash_encode(lat, lon, precision=9):
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]

    bits = []
    even = True

    while len(bits) < precision * 5:
        if even:
            mid = sum(lon_range) / 2
            if lon > mid:
                bits.append(1)
                lon_range[0] = mid
            else:
                bits.append(0)
                lon_range[1] = mid
        else:
            mid = sum(lat_range) / 2
            if lat > mid:
                bits.append(1)
                lat_range[0] = mid
            else:
                bits.append(0)
                lat_range[1] = mid

        even = not even

    # Convert bits => base32
    hash_str = ""
    for i in range(0, len(bits), 5):
        chunk = bits[i:i+5]
        value = 0
        for b in chunk:
            value = (value << 1) | b
        hash_str += BASE32[value]

    return hash_str

# decode function
def geohash_decode(hash_str):
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    even = True

    for char in hash_str:
        value = BASE32.index(char)

        for mask in [16,8,4,2,1]:
            bit = value & mask

            if even:
                mid = sum(lon_range)/2
                if bit:
                    lon_range[0] = mid
                else:
                    lon_range[1] = mid
            else:
                mid = sum(lat_range)/2
                if bit:
                    lat_range[0] = mid
                else:
                    lat_range[1] = mid

            even = not even

    lat = sum(lat_range)/2
    lon = sum(lon_range)/2
    return lat, lon

```

Searching nearby points becomes now, without any geometry.

```sql
SELECT * WHERE geohash LIKE 'tuvz4p%'
```

## Proximity Search Algorithm

Step 1 : Choose Precision

Radius -> prefix length

```
~ 5km -> length 5
~ 150km -> length 7
```

Step 2 : Get center Hash

```
h = geohash(point)
prefix = h:[:length]
```

Step 3: Also query neighbors, because edges exists

```
+----+----+----+
| NW | N  | NE |
+----+----+----+
| W  | X  | E  |
+----+----+----+
| SW | S  | SE |
+----+----+----+
```

We query 9 cells

### Neighbor Computation

```python
# decode -> move -> re-encode
def neighbor(lat, lon, dlat, dlon, precision=7):
    return geohash_encode(lat+dlat, lon+dlon, precision)
```

In production systems use lookup tables to speed up.

### Conclusion

Use Cases

- Redis GEO ~ radius search
- Elasticsearch ~ Geo Indexing
- Uber ~ driver matching
- Maps ~ nearby places
- Games ~ area queries

Strengths

- Fast range queries
- Uses Normal Indexes
- Compact Storage
- Easy Sharding

Limitations

- Distortion near poles
- Cells rectangular, not circular
- Requires Neighbour search
- Not Exact distance

## GeoHashing in Real Systems

Why do we even need to improve this further ? In general queries in real life are circular in nature. Example - Find all restaurants within 500m.

But Geohash due to its nature returns all points inside grid cells, and we must remove points which are not inside circle.

![](assets/Pasted%20image%2020260216143146.png)

### 1. Candidate Selection

- Compute GeoHash Prefix
- Query DB using prefix index
- Also Query 8 neighbors

This reduces the search from millions to maybe 100 results.

### 2. Accurate Distance (Haversine)

Now we compute real Earth Distances. Since Earth is spherical(almost :) we can use Haversine formula

```python
from math import radians, sin, cos, sqrt, atan2

EARTH_RADIUS = 6371000  # meters

def haversine(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return EARTH_RADIUS * c
```

Final Query Pipeline

```python
def nearby_points(center, points, radius):
    lat, lon = center

    # Step 1: rough filter
    prefix = geohash_encode(lat, lon, precision=7)
    candidates = [p for p in points if p.hash.startswith(prefix)]

    # Step 2: accurate filter
    result = []
    for p in candidates:
        if haversine(lat, lon, p.lat, p.lon) <= radius:
            result.append(p)

    return result
```

This is similar to how Redis/Uber/ElasticSearch Geo Queries work

Choosing Geohash Precision Automatically

|**Radius**|**Geohash Length**|
|---|---|
|< 5 km|5|
|< 1 km|6|
|< 150 m|7|
|< 40 m|8|
|< 5 m|9|

Geohash is based on Z-order curve, which has locality problems. Sometimes Close points may have very different hashes. Near cell broken clusters.

So world moved beyond Geohash

### S2 (Google)

Earth is projected on the cube -> subdivided.

- Shape : Squares on Sphere
- Better locality
- Uniform area

Used by:

- Google Maps
- BigQuery GIS
- Pokemon Go
### H3

Hexagonal Grid on Sphere

- Shape: Hexagons
- Uniform Neighbors
- Best Clustering

Used By

- Uber ride matching
- Grab
- Lyft
- Modern Geo Analytics


### Final Conclusion

Geospatial search pipeline is not just geohashing, its just a first stage accelerator.

- Spatial Index (Geohash/s2/h3)
- candidate set
- Haversine Filter
- Exact Results

### Resources

Further Reading

- https://medium.com/@sylvain.tiset/breaking-down-location-based-algorithms-r-tree-geohash-s2-and-h3-explained-a65cd10bd3a9
- https://cloud.google.com/blog/products/data-analytics/best-practices-for-spatial-clustering-in-bigquery
- https://eugene-eeo.github.io/blog/geohashing.html
- https://www.uber.com/en-IN/blog/h3/