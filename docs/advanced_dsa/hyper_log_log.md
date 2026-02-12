# Hyper Log Log

*Cardinality Estimation*

Given a very large stream of elements: Estimate the number of **distinct elements**, without storing them all.

[Hyper Log Log Video Explanation](https://youtu.be/lJYufx0bfpw?si=nBIU1DCxkz-zkzmj)

The algorithm divides the stream in `m` independent substreams and keeps the maximum length of a seen `00...1` prefix of each substream. Then, it estimates the final value by taking the mean value of all substreams.

We often use *hash functions* to each element in the original multiset to obtain multiset of uniformly distributed random numbers with same cardinality as original multiset.

StackOverFlow Example : [Link](https://stackoverflow.com/questions/12327004/how-does-the-hyperloglog-algorithm-work)
Original Flajolet-Marting Algorithm : [Link](https://en.wikipedia.org/wiki/Flajolet%E2%80%93Martin_algorithm)
LogLog Paper : [Link](https://www.ic.unicamp.br/%7Ecelio/peer2peer/math/bitmap-algorithms/durand03loglog.pdf)
Hyper LogLog Paper : [Link](https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf)

When this algorithm becomes important, when we want to count/approximate the number of distinct elements in a very large dataset, We might need to store data same as cardinality of dataset.

HyperLogLog uses significantly less memory, trading off for accuracy.

The HyperLogLog algorithm is able to estimate cardinalities of > $10^9$ with a typical accuracy (standard error) of 2%, using 1.5 kB of memory


HyperLogLog has 3 main operations

- Add : add a new element to set
- Count : obtain cardinality of the set
- Merge : obtain union of two sets

[HyperLogLog Redis Docs](https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/)

Use Cases :

- How many unique visits has this page had on this day?
- How many unique users have played this song?
- How many unique users have viewed this video?

## Algorithm Overview

- Hash each element to a uniform random bit string
- Split hash into
    - Register index (first p bits)
    - Remaining bits used to count leading zeroes
- Track the maximum number of leading zeroes seen per register
- Combining registers using harmonic mean

### Usage Example Python

NOTE: This library has bias from HLL+

```
pip install hyperloglog
```

```python
import hyperloglog

h = hyperloglog.HyperLogLog(0.01)  # 1% error

for i in range(1000000):
    h.add(str(i))

print(len(h))
```

### Usage Example Redis

```bash
## Add element
PFADD page:visits user1 user2 user3

## count the elements
PFCOUNT page:visits

## Merge operation
PFMERGE combined page:visits page:visits2
```

```python
import redis

r = redis.Redis()

r.pfadd("page:visits", "user1", "user2")
count = r.pfcount("page:visits")

print(count)
```