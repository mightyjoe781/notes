# Pathfinding at Scale - From BFS to Contraction Hierarchies

*How "shortest route from New York to San Francisco" goes from a brute-force impossibility (~10^200 years of compute) to a sub-millisecond Google Maps query.*

## The Scale Problem

The North American road network has ~64 million intersections, which works out to roughly 10^220 possible routes between two points. Checking a billion routes per second would still take over 10^200 years. Yet Google/Apple Maps answers in a few seconds end-to-end - and the actual routing engine underneath needs to run in **under a millisecond**, because it isn't just answering you - it's answering millions of concurrent queries on a finite fleet of servers.

## BFS - shortest path when every edge is equal

Model the road network as a graph - intersections/cities are nodes, roads are edges. [BFS](../dsa/graphs/ch2.md) explores every node one hop away, then two hops away, and so on - guaranteed to find the shortest path **as long as every edge has the same weight**. Real roads have different lengths, so equal-weight BFS isn't enough on its own - you need a way to account for distance. That gap is exactly what Dijkstra's algorithm closes.

## Dijkstra's Algorithm (1956)

Famous origin story - Edsger Dijkstra invented it in **20 minutes**, without pen or paper, on a café terrace in Amsterdam, while looking for a problem simple enough to demo the ARMAC computer to non-technical people. The original framing was literally "what's the shortest way to travel from Rotterdam to Groningen?"

Core idea - track the **cost** (cheapest known distance from the source) to every node. Start the source at 0 and everything else at infinity, then repeatedly:

1. Pick the unexplored node with the lowest known cost
2. *Relax* each of its edges - if reaching a neighbour through this node is cheaper than the neighbour's current known cost, update it
3. Mark the node explored

It's correct because expanding strictly in cost order means that by the time you pop the target, you've already explored every path that could possibly be cheaper - there's nothing left to beat it. It's BFS generalized from "explore in hop order" to "explore in cost order."

See [Shortest Path - Dijkstra's Algorithm](../dsa/graphs/ch4.md) for the full algorithm and implementation.

- On a city-sized query it runs in ~100ms - genuinely fast
- On the *full* North American network, a well-tuned Dijkstra averages **~7 seconds per query**, often touching most of the 64M nodes
- Google needs roughly **7,000x** that speed

## A* - Dijkstra with a compass (1968)

The problem with Dijkstra at scale - it explores *equally in every direction*, including straight away from the destination.

The fix - add a **heuristic**, an estimate of the remaining distance from a node to the target (e.g. straight-line/Haversine distance), and explore nodes in order of `cost-so-far + heuristic` instead of just `cost-so-far`. Visually, picture the heuristic as height - the search becomes a landscape that slopes up the further you get from the goal, and the algorithm naturally avoids climbing it.

- On a Newark -> Central Park Zoo query, A* checked ~7,000 nodes vs Dijkstra's ~65,000 - roughly a 10x cut, when optimizing for raw **distance**
- **Catch**: optimize for **travel time** instead, and the heuristic (straight-line distance / max speed) becomes a severe underestimate. A* then explores *more* nodes (3x more in one benchmark, vs Dijkstra's +10%) and pays for an expensive sqrt in every heuristic evaluation - "[for travel time] A* loses against a well-tuned Dijkstra"
- Where it shines - game-engine pathfinding (Minecraft mobs run an A* variant with extra penalties for lava/hazards) and maze solving, where "as the crow flies" is a good proxy for "as the road goes"

## Bidirectional Dijkstra

Run two searches at once - forward from the source, backward from the target - and stop when their frontiers meet in the middle.

- A single search covers roughly a circle of area `πR²` for a target distance `R`. Two searches meeting at the midpoint each only need to cover about half that, `½πR²` (sometimes better, depending on the graph's shape)
- Carnegie Hall -> Wall Street - plain Dijkstra explored ~7,200 nodes; bidirectional explored ~2,600 - about 3x fewer
- Still doesn't encode anything about *road-network structure* - a twisty back street and an interstate with the same edge weight get searched with equal enthusiasm. "They still do things you wouldn't conceive as a good idea - like checking if there's a shorter path by driving through an In-N-Out drive-through and out the other side."

## Manual Road Hierarchies (1990s in-car GPS)

The human intuition - real trips meander on local roads, merge onto a highway for the long stretch, then meander again near the destination. Early GPS units encoded this by hand:

1. Surveyors tagged every road with a class - narrow road → local major road → express highway
2. The router ran bidirectional Dijkstra restricted to the *lowest* road class within a hand-tuned "candidate area" first
3. If the target wasn't found, it widened the candidate area and moved up to the next road class, repeating until the two searches met

- **Problem**: the candidate-area size is a guess. Too small, and a faster route made of local roads gets passed over for a longer highway detour; too large, and you're effectively back to plain Dijkstra
- Required armies of surveyors manually classifying roads - it could never scale to "map the entire world"

## Contraction Hierarchies - automate the hierarchy

Same intuition - prefer "important" roads - but **derive importance automatically from the graph's structure**, while still *guaranteeing* the true shortest path (no hand-tuned candidate areas, no risk of missing a better local route).

### Phase 1 - Rank every node by importance (slow, infrequent pre-processing)

A node is important if it sits on a **small cut** that roughly splits the graph in half - like the single bridge connecting two similarly-sized towns: nearly every cross-town trip has to pass through it. Find these cuts recursively (**nested dissection**):

- The ~102 nodes that split North America into East and West (loosely tracing the Mississippi River) get the *highest* rank
- Recursively cut each half again - the next cuts trace the Appalachians/Potomac on the East and the Rockies/Colorado River on the West - and rank those next
- Keep splitting and ranking until all 64M+ nodes have a rank

On the North American graph this pre-processing took roughly **1h40m**, and it barely needs to be redone - only when the road network itself changes (new bridges, permanent closures).

### Phase 2 - Patch in shortcuts (so low-rank routes aren't lost)

A search that only ever climbs the hierarchy would miss shortest paths that dip through low-ranked nodes - e.g. a pair of cheap local roads that genuinely beats a highway detour. The fix - walk from the lowest-ranked node upward; whenever a node connects to two higher-ranked neighbours (a "lower triangle"), add a **shortcut edge** directly between those neighbours carrying the combined cost. This:

- Guarantees the search never *needs* to drop below its current rank to find the true shortest path - any such path is already pre-baked into a shortcut
- Means the exact node ranking doesn't have to be perfect - any valid split-and-rank ordering works, because anything the ranking "misses" gets patched back in as a shortcut (more shortcuts ↔ sloppier ranking is fine, just costs more storage/search)
- Has to be recomputed whenever edge *weights* change (live traffic, new speed limits) - this step has to stay cheap (~1s on North America with parallelization), unlike Phase 1

Splitting the pipeline this way - rank once (expensive, rare) vs. re-weight often (cheap, frequent) - is exactly what makes this a **customizable contraction hierarchy**.

### Phase 3 - Query (bidirectional Dijkstra, but only ever moving "up")

Run bidirectional Dijkstra where both searches are restricted to nodes of strictly increasing rank. The two frontiers naturally converge near the top of the hierarchy - the handful of major cuts (e.g. the Mississippi crossings) - having explored almost nothing else.

- Result on North America - query time drops to **~200 microseconds** (tunable down to ~100µs), exploring on average just **~1,450 nodes** - about **35,000x** faster than Dijkstra and a ~44,000x smaller search space
- San Francisco → Montreal - plain Dijkstra explores roughly the whole continent's worth of nodes; the contraction hierarchy touches only ~1,236, clustered around the source, the destination, and the major cuts in between

## The pre-processing vs. query-time trade-off

Plot pre-processing time on one axis and query time on the other:

- **Full lookup table** (precompute every shortest path between every pair of nodes) - near-instant queries, but building it would take more than a decade of single-core compute and ~8 petabytes of storage (16x all of Wikipedia) - and huge chunks would need rebuilding on every road change
- **Plain Dijkstra** - zero pre-processing, ~7 seconds per query
- **Contraction hierarchies** - the sweet spot in between - a chunk of (infrequent, parallelizable) pre-processing buys sub-millisecond queries

## Evolution Recap

```
BFS  (shortest path, unweighted - explore in hop order)
  -> Dijkstra, 1956            (weighted graphs - explore in cost order, provably shortest)
    -> A*                      (heuristic-guided Dijkstra - lean the search toward the goal)
      -> Bidirectional Dijkstra (search from both ends, meet in the middle, ~half the area)
        -> Manual road hierarchies, 1990s GPS  (hand-tagged road classes + candidate areas)
          -> Contraction Hierarchies            (auto-rank nodes via nested dissection + shortcut edges)
            -> Customizable Contraction Hierarchies (decouple expensive ranking from cheap re-weighting, so live traffic stays fast)
```

Notice that every step is still, at its core, Dijkstra - explore the frontier in cost order, relax edges, never miss a cheaper path. As Mikkel Thorup put it, "all theoretical developments in single-source shortest paths have been based on Dijkstra's algorithm." A 70-year-old, 20-minute café invention is still the engine room of Google Maps.

## Further Reading / Watching

- [How Does Google Maps Calculate the Shortest Route? - Veritasium x 2swap (YouTube)](https://www.youtube.com/watch?v=kS-CGkiPetQ) - the source for this walkthrough; covers Dijkstra's origin story, A*, bidirectional search, manual road hierarchies, and customizable contraction hierarchies, with real benchmark numbers on the North American road network
