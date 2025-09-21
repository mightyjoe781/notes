# Algorithmic Design


## Geo-Proximity

What made Tinder, Ola, Uber, Swiggy, Zomato, Google Store, Facebook nearby friends, Yulu, ZoomCar possible ?

*Geo Proximity* : How do you efficiently findout who and what is *near-you*

Problem Statement :
Find people who are within `k` km radius

![](assets/Pasted%20image%2020250921164045.png)

Why is it soo.. hard to find geo proximity ?
### Core Idea : Divide & Conquer

![](assets/Pasted%20image%2020250921175017.png)

Split in half everytime & assign left = 0, right = 1, top = 0, bottom 1

- zoom in ... more bits in the right
- zoom out ... remove bits from the right

Edge case : same points near maybe far in GeoHash

### GeoHash

Convert two dimensional (lat, long) into a single dimension point giving you an ability to quickly check *nearby*

![](assets/Pasted%20image%2020250921175424.png)

On one dimension you can very efficiently find out who's near you using Range Queries (efficiently done using Segment Trees)

Geohash converts 2D to 1D and then we can use a bunch of methods for range queries.

KNN Speedup
Dimensionality Reduction

0001000100 ... 32 bit numbers are not Human Readable. So, Geohash changed the base to 32 and instead of halving every time, it broke the geo in 32 blocks

![](assets/Pasted%20image%2020250921175651.png)

All geo locations can be represented by a base 32 string and closer the points closer the geohash

Check if these two points are closer - *qrzkst* and *qrzksx*

Data structure that is meant to solve prefix matching problem efficiently is *Trie, BK Trees, Edit Distance*

Zippr, did something similar in India, Every address gets a unique code (not GeoHash) but something memorizable.

Even Google Maps has an 8-char Human Readable string for each location (*Landmark*)

This algorithm is so simple that we can find nearest points using a simple SQL query

```sql
-- find all people in bengaluru
select * from people
where substr(geohash, 5)
like 'tdrlv%'
```

You can also use a trie to find the nearest people, load all people & geohash in a trie. Traverse through the trie for tdrlv and all child of this node are people in Bengaluru

Also, you need not use GeoHash from scratch. GeoSpatial databases solve this for you!
*e.g. Redis, ElasticSearch, MongoDB*

You insert/update (lat, long) and say, give me point in 5km radius from a (lat, long)

Alex Xu  ~ Video on Proximity Service

![](assets/Pasted%20image%2020250921171340.png)

#### Availability and low latency over consistency

Key Design Decisions
Redis for storing and querying data

- in-memory fast
- suppports geo-queries
- multi-master, multi-replica setup

Data is sharded and stored on exclusive master each master has a set of replicas following it
![](assets/Pasted%20image%2020250921172632.png)


Challenge : *EVAL Command*

filtering of drivers on constraint happen through EVAL command. Redis doesn't execute EVAL on replicas.
Why ? because EVAL can contain command that could update the data.
How ? If we fire EVAL on replica it responds with MOVED <master_ip>

![](assets/Pasted%20image%2020250921172452.png)

But *Gojek* wanted EVAL on replica for fitlering drivers

- They raised an issue with Redis Team and proposed *EVAL_RO* command
- They updated *go_redis* to enable this command to execute on Replicas.

#### Availability with low latency
Instead of firing *GEOSEARCH* on one node/replica, they split the query into smaller queries and fired in parallel on multiple nodes.

- even if one node is slow, other nodes repsond
- parallel execution makes computing quicker
- send partial response if SLA breached.

![](assets/Pasted%20image%2020250921173336.png)

#### HOT Shard Problem

Splitting queries into smaller regions addresses hot-sharded (to some extent)
But key step to ensure this is 

shard the data in such a way that peak load regions and low traffic regions are mixed well

Manual Allocation would have been done here by ADS service, because native Redis's sharding has no business context !

#### Impact
600k writes/minutes
200k reads/minutes

Truly horizontally scalable (add more nodes to handle more load) system. Highly available and low latency.


Also such Divide & Conquer strategy is used in *Anamoly Detection* using *Isolation Forest* Algorithm very similar to geohash's approach.

## User-Affinity Service

On a social media, you can follow someone how to model this at scale ?

Potential : `nxn` cardinality ~ every user following every other

GraphDB ? seems an obvious choice.
most social networks do this ~ e.g. Koo India

But isn't it an overkill ? Are we using any sophisticated algorithm ?

Few reasons why it might not be the best choice

- we are not using any sophisticated algorithm
- managing a graph DB is painful
- managing or using a graph DB is expensive
- plug pagination is very tricky in graph DB

Can we do better ?

Requirements

- use relational DB
- pagination should extremely efficient (no matter how deep you scroll the performance should be same)
- counting followers and followings should be accurate & quick
- very quickly find A follows B ?
- very fast writes

![](assets/Pasted%20image%2020250921181712.png)
when A follows B we make an entry in the table with `src = A` and `dest=B`.
We want to render the 
- people who follow B
- people B follows

Query

```sql
-- followers of B
select * from edges where dest = B

-- following of B
select * from edges where src = B
```

Challenges

- To answer both queries efficiently (expensive) we need to index both the columns
- how will you grow beyond one DB node

Say, we shard and *src* is the partitioning key

Say, we have 4 shards and 4 users A, B, C, D and each user is on one shard.

![](assets/Pasted%20image%2020250921185336.png)

- calculating followers of B is calculated over multiple shard and then aggregated,
- calculating who B follows, is simple and calculated from one shard

We need somehow have both, follow and following on the same shard !
i.e. if we shard by src we want to ensure we have to never query on dest.

Solution :

- store A Follows B
- ans B is followed by A

For each follow create 2 entries with relation.
![](assets/Pasted%20image%2020250921185705.png)

![](assets/Pasted%20image%2020250921190047.png)

```sql
-- followers of B
select * from edges
where src = B and 
state = "followed_by"

-- people B follows
select * from edges
where src = B and 
state = "follows"

```

#### Twitter -> Flock DB

We moved both queries to `src`, now no need of dest index and we can shard the dataset on `src`

Stores graph as set of Edges <- GraphDB on Relational DB

| col       | type  | description                        |
| --------- | ----- | ---------------------------------- |
| source_id | int64 | nodes connected by edge            |
| dst_id    | int64 | nodes connected by edge            |
| position  | int64 | cursor, sorting criteria           |
| state     | int8  | positive, negative, archived, etc. |

for following graph, position = timestamp.

When edge deleted -> change state -> restoration possible

Primary Key : source_id, state, position
Unique Index : (source_id, destination_id, state)

Data is partitioned by node so any query would not require cross partition execution

Pagination is done *position* and not Limit/Offset
-> any page of result equally fast

src = B

| src | dest | state      | position |
|-----|------|------------|----------|
| B   | C    | Follows    | 100      |
| B   | D    | Follows    | 200      |
| B   | F    | Follows    | 250      |
| B   | A    | Follows    | 500      |
| B   | A    | Followed By| 50       |
| B   | C    | Followed By| 70       |
| B   | D    | Followed By| 102      |
|     |      |            | 200      |
|     |      |            | 300      |

```sql
select * from edges where src = B, state = follows and order by position ASC
```

Since above table is always sorted due to constraints on the table, we get a very neat paginated API.Rather than using limit/offset we are using how database stores the data.

So we get the following benefits from above structure

- range based partitions
- horizontally scalable

Resource ~ 

- B-Trees in DB