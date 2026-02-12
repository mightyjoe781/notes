# Bloom Filters

*Membership testing with false positives*

A Bloom filter is ==a space-efficient, probabilistic data structure that quickly checks if an element might be in a set==, offering fast "definitely not in set" (true negative) or "possibly in set" (potential false positive) answers, but never a "definitely in set"


Good Explanation Videos :

- [Spanning Tree](https://www.youtube.com/watch?v=kfFacplFY4Y)
- [Byte Byte Go](https://www.youtube.com/watch?v=V3pzxngeLqw)
- [mCoding](https://www.youtube.com/watch?v=qZNJTh2NEiU)

It was conceived by *Burton Howard Bloom* in 1970. [Paper](http://www.dragonwins.com/domains/getteched/bbc/literature/Bloom70.pdf), [Scalable Bloom Filters](https://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf)

Use Cases:

- Cache Filtering (avoid DB hits)
- URL de-duplication
- Spam Detections
- Distributed Systems, Membership checks

## Algorithm Description

- Create a Bloom Filter (a bit array for of size $m$), with $k$ hash functions
- Add(x)
    - Hash element `x` with `k` hash functions
    - Each Hash gives an index
    - Set those bits to 1
- Contains(x)
    - Hash the same with `k` functions
    - If all bits are 1 ~ maybe present (false positive)
    - If any bits are 0 ~ definitely not present

## False Positive Probability

$$
\Sigma_t Pr(q=t)(1-t)^k \cong (1 - E[q])^k = (1 - [1 - \frac{1}{m}]^{kn})^k \cong (1 - e^{\frac{-kn}{m}})^k
$$

- `m` = number of bits
- `n` = number of elements
- `k` = number of hash functions

Optimal Number of Hashes : $k=\frac{m}{n} \ln 2$

Generally, based on error rate Redis will swap out the algorithm for a more optimal one.

|**Bits per element**|**False positive rate**|
|---|---|
|10 bits|~1%|
|5 bits|~3%|
|20 bits|~0.01%|
## Code Examples

### Python

```bash
pip install pybloom-live
```

```python
from pybloom_live import BloomFilter

bf = BloomFilter(capacity=1000000, error_rate=0.01)

bf.add("user1")

if "user1" in bf:
    print("Maybe present")
```

### Redis

```redis
BF.RESERVE key 0.01 1000000
BF.ADD key user1
BF.EXISTS key user1
```

More : [Link](https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/)

## Limitation of Bloom Filters

Biggest Limitation is that you cannot delete items.

Bloom filters typically exhibit better performance and scalability when inserting items. Cuckoo filters are quicker on check operations and also allow deletions.

Use Cases of Cuckoo Filters

- Targeted ad campaigns (advertising, retail)
- Discount code/coupon validation (retail, online shops)

## Cuckoo Filters

A Cuckoo filter is an array of buckets, storing fingerprints of the values in one of the buckets at positions decided by the two hash functions. A membership query for item `x` searches the possible buckets for the fingerprint of `x`, and returns true if an identical fingerprint is found. A cuckoo filter's fingerprint size will directly determine the false positive rate.

### Redis Cuckoo Filters

```
> CF.RESERVE bikes:models 1000
OK
> CF.ADD bikes:models "Smoky Mountain Striker"
(integer) 1
> CF.EXISTS bikes:models "Smoky Mountain Striker"
(integer) 1
> CF.EXISTS bikes:models "Terrible Bike Name"
(integer) 0
> CF.DEL bikes:models "Smoky Mountain Striker"
(integer) 1
```

[More on Cuckoo Filters](https://redis.io/docs/latest/develop/data-types/probabilistic/cuckoo-filter/)