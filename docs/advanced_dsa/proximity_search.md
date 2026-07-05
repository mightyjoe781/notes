---
title: Proximity Search & Geospatial Indexes - Custom Trees vs Encoded Keys
description: Survey of how spatial indexes evolved from Quadtree/KD-Tree/R-Tree to encoded-key approaches like Geohash/S2/H3, and when to reach for each.
tags:
  - concept
---

# Proximity Search & Geospatial Indexes

*Why "find everything near me" breaks indexes that answer "find everything between age 20 and 30" trivially - and how the industry got from brute-force scans to Geohash/S2/H3.*

## The Core Problem

A B-Tree answers `age BETWEEN 20 AND 30` in one seek because **1D sort order preserves 1D closeness** - 20 sits next to 21 sits next to 22, all on the same disk page.

Location is two numbers, `(lat, lng)`, and what actually matters is straight-line distance. Indexing `lat` and `lng` separately just gives you a horizontal strip and a vertical strip of the Earth - their intersection is still millions of rows you'd have to check by hand.

The real issue: **flattening 2D into 1D rips apart neighborliness**. Two cabs five blocks apart in Manhattan are neighbours in space, but sort purely by longitude and every cab between the Bronx and Staten Island gets crammed into the index between them - a block apart on the street, millions of rows apart in the database.

Every production system - Postgres, Elasticsearch, Redis, MongoDB, Uber - converges on one of two fixes:

1. **Build a custom tree** shaped like a B-Tree (balanced, page-sized nodes, on-disk friendly) but tuned for space → Quadtree → KD-Tree → BKD-Tree → R-Tree
2. **Encode `(lat, lng)` into a single sortable integer** and reuse the boring, 50-years-tuned B-Tree you already have → Geohash → S2 → H3

Both camps chase the same prize: *a balanced tree of disk pages you can range-scan.*

## Camp 1 - Custom Spatial Trees

### Quadtree (Finkel & Bentley, 1974)

See [Quad Tree](quadtree.md) for the full algorithm and implementation. The foundational idea - recursively split a 2D region into 4 quadrants until every leaf holds a manageable number of points, then descend one level at a time (compare query point to the cell's midpoint, pick a quadrant, recurse, check neighbouring leaves at the boundary).

- Adapts to density - Manhattan ends up as a deep tree, an empty lake stays a single cell
- **Weakness**: splits always happen at the *geometric midpoint*, not where data actually sits. A dense cluster keeps getting bisected over and over, so query latency depends on *where* you're looking - Manhattan is deep and slow, Vermont is shallow and fast. No predictable worst case, and the regions you care most about are the slowest.
- **Weakness**: it's a pointer structure - nodes live at arbitrary memory addresses. Fine when the whole tree fits in RAM (cheap pointer chasing), but a database can't assume that. Once it spills to disk, every hop is a likely-random page read.
- Still used where the structure stays in memory: Google Maps tile systems, game-engine collision detection

### KD-Tree (Bentley, 1975)

Binary cousin of the quadtree - instead of splitting both axes at once into 4 quadrants, alternate **one dimension per level** (split on `x` at level 0, `y` at level 1, back to `x`, ...). Splitting at the median keeps it balanced, and it was the workhorse for nearest-neighbour search for decades.

- Same disk problem as quadtrees - pointer-heavy, no clean mapping onto fixed-size pages, great in memory and painful off it

### BKD-Tree ("Block KD-Tree")

The disk-friendly fix for KD-Trees - instead of one point per node, pack points into blocks sized to a disk page, and bulk-build the whole tree once from a batch of data.

- Elasticsearch's geo fields are backed by a BKD-Tree under the hood
- Trade-off: it's essentially write-once / built-for-immutable-segments, which makes it a poor fit for workloads with heavy, constant updates (e.g. Uber's drivers moving every second)

### R-Tree (Guttman, 1984)

First spatial index designed specifically *for a database*. Guttman set out to solve two things quadtrees and KD-Trees hadn't:

1. **Shapes** - real geo data isn't just points. A highway is a line, a country or a delivery zone is a polygon. You can't meaningfully drop a polygon into a quadtree cell.
2. **Disk layout** - he wanted the spatial analog of a B-Tree: balanced, every leaf at the same depth, every node sized to a disk page, splits/merges on insert/delete the same way a B-Tree rebalances.

The trick - wrap every object in its **Minimum Bounding Rectangle (MBR)**, axis-aligned to lat/lng. A point is a zero-area rectangle, a highway a long thin one, a country a big one. Nearby rectangles get grouped into larger enclosing rectangles, all the way up to the root - giving predictable depth and one disk page per node.

- **Trade-off**: unlike quadtree cells, MBRs can *overlap*. If a query point lands inside two bounding rectangles at once, you must descend both subtrees - a bad insertion strategy produces heavy overlap and tanks performance.
- The workhorse of production spatial indexes: Postgres/PostGIS, SQLite, Oracle Spatial all run an R-Tree variant under the hood
- **R\*-Tree** (Germany, 1990): a smarter insertion heuristic that minimises overlap; almost every modern R-Tree implementation is built on top of this insertion strategy

> **Mental model**: Quadtree → adaptive *grid*. KD-Tree → adaptive *split*. R-Tree → bounding *boxes of objects*.

## Camp 2 - Encoded Keys (collapse 2D into one sortable integer)

Skip the custom tree entirely. Turn `(lat, lng)` into a single number where *numerically close integers are geographically close*, drop it into a plain B-Tree / sorted structure, and range scans just work.

### Geohash (Niemeyer, 2008)

See [GeoHashing](geohashing.md) for the full encode/decode algorithm, the 3x3-neighbour trick, and the Haversine post-filter pipeline.

The framing worth carrying over from this angle - a geohash isn't really a string, it's a **stack of bits** (5 bits per base32 character, with lat/lng bits interleaved via a Z-order/Morton curve). Read those same bits as an integer and you keep the exact same sort order:

- Redis stores it as a 52-bit integer inside a sorted set - `GEOADD` computes the integer, and a radius query is just `ZRANGEBYSCORE`, i.e. a range scan over geohash integers
- Postgres can store the very same bits as text and prefix-scan it (`WHERE geohash LIKE 'dr5ru%'`)

Both representations sort identically - "one of the most elegant reductions of a hard problem (proximity search) into one you've already solved (string-prefix / integer-range matching) that you'll find in production."

- **Weakness**: treats lat/lng as if they sit on a flat rectangle. The Earth isn't flat - a degree of longitude is ~111km at the equator and ~0km at the poles, so a geohash cell is a fat square at the equator and a thin sliver near the poles.

### S2 (Google, ~2011)

Fixes the flat-Earth distortion - wrap the sphere in a cube, project the Earth onto its 6 flat faces, and subdivide each face into cells that stay roughly equal-area anywhere on the globe. Every location gets a hierarchical **64-bit S2 cell ID** - truncate it for a coarser parent cell, exactly like a geohash prefix.

- Powers MongoDB's `2dsphere` index
- Correctly handles polygons that cross the antimeridian - a flat geohash-style index would treat such a polygon as stretching all the way around the globe; S2 knows better

### H3 (Uber, open-sourced ~2018)

Same hierarchical-integer idea, but tiles the globe in **hexagons** instead of squares.

- A square has two *kinds* of neighbour - 4 edge-adjacent and 4 corner-adjacent (and the corner ones sit further away). That asymmetry makes "everyone within N cells" queries and heatmaps messy.
- A hexagon has exactly 6 neighbours, **all equidistant** - clean math for the analytics Uber runs constantly (dispatch, surge pricing)
- You don't sort the hexagons themselves - H3 walks the hex grid in a deterministic order (a space-filling curve) and assigns increasing integer IDs along that walk, preserving "numerically close ⇒ geographically close"
- 16 resolutions, 64-bit hierarchical IDs (continent-sized cells down to ~1m²); zero out the tail of an ID to get its parent cell
- Production flow: driver pings → converted to an H3 cell (e.g. ~200m resolution) → rider opens app → look up their cell → expand to the 6 neighbours → look for drivers → widen the ring if the net comes back empty

## Choosing - Custom Tree vs Encoded Key

| | **Custom Tree** (R-Tree, BKD-Tree) | **Encoded Key** (Geohash, S2, H3) |
|---|---|---|
| Handles | Points, lines, polygons - exact geometry (`intersects?`, `contains?`) | Mostly points |
| Requires | A real spatial extension (PostGIS, ES geo mapping) | Any DB with a B-Tree / sorted structure - nothing extra |
| Writes | Expensive - R-Tree rebalancing, BKD built in batches; a poor fit for constantly-moving data | Dirt cheap - a moving driver is just one integer update on an index the DB already tunes for |
| Precision | Exact | Approximate - boundary artifacts mean you query a ring of neighbour cells and post-filter by real distance (e.g. Haversine) |
| Used by | Postgres/PostGIS, SQLite, Oracle Spatial (R-Tree variants); Elasticsearch (BKD-Tree) | Redis (Geohash → 52-bit int); MongoDB `2dsphere` (S2); Uber/Grab/Lyft (H3) |

**Rule of thumb**: need shapes and exact geometry → reach for a custom tree, but mind the write throughput. Have points at scale with heavy writes (drivers, pings, check-ins) → reach for an encoded key (Geohash / S2 / H3).

## Further Reading / Watching

- [Proximity Search & Geospatial Indexes - HelloInterview (YouTube)](https://www.youtube.com/watch?v=dQXdSxn7d1g) - the source walkthrough this note is built from; ties Quadtree → KD-Tree → BKD-Tree → R-Tree and Geohash → S2 → H3 into one coherent evolution story

## See Also

- [Quad Tree](quadtree.md) - the foundational custom spatial tree this survey opens with
- [GeoHashing](geohashing.md) - the full encode/decode algorithm behind the encoded-key camp
- [Algorithmic Design - Geo-Proximity and GeoHash](../sd/hld/advanced/algorithmic_design_2.md) - these ideas applied to a real geo-proximity architecture
