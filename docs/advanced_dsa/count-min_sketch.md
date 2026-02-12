# Count-min Sketch

*Frequency estimation in Data Streams*

It uses a sub-linear space at the expense of over-counting some events due to collisions. It consumes a stream of events/elements and keeps estimated counters of their frequency.

It is very important to know that the results coming from a Count-Min sketch lower than a certain threshold (determined by the error_rate) should be ignored and often even approximated to zero. So Count-Min sketch is indeed a data-structure for counting frequencies of elements in a stream, but it's only useful for higher counts. Very low counts should be ignored as noise.


[An Improved Data Stream Summary](http://dimacs.rutgers.edu/~graham/pubs/papers/cm-full.pdf)

Use Cases

- Product (retail, online shops) ~ What was the sales volume (on a certain day) for a product ?
- Use one Count-Min sketch created per day (period). Every product sale goes into the CMS. The CMS give reasonably accurate results for the products that contribute the most toward the sales. Products with low percentage of the total sales are ignored.

## Code Examples

```
> CMS.INITBYPROB bikes:profit 0.001 0.002
OK
> CMS.INCRBY bikes:profit "Smokey Mountain Striker" 100
(integer) 100
> CMS.INCRBY bikes:profit "Rocky Mountain Racer" 200 "Cloudy City Cruiser" 150
1) (integer) 200
2) (integer) 150
> CMS.QUERY bikes:profit "Smokey Mountain Striker" "Rocky Mountain Racer" "Cloudy City Cruiser" "Terrible Bike Name"
3) (integer) 100
4) (integer) 200
5) (integer) 150
6) (integer) 0
> CMS.INFO bikes:profit
7) width
8) (integer) 2000
9) depth
10) (integer) 9
11) count
12) (integer) 450
```

### Sizing the Count-Min Sketch

Even though the Count-Min sketch is similar to Bloom filter in many ways, its sizing is considerably more complex. The initialisation command receives only two sizing parameters, but you have to understand them thoroughly if you want to have a usable sketch.

-  `error` parameter will determine the width `w` of your sketch and the probability will determine the number of hash functions (depth `d`). The error rate we choose will determine the threshold above which we can trust the result from the sketch. $\text{threshold} = \text{error} \times \text{total\_count}$
- `probability` in this data structure represents the chance of an element that has a count below the threshold to collide with elements that had a count above the threshold on all sketches/depths thus returning a min-count of a frequently occurring element instead of its own.


See Also :

- [Top-K](https://redis.io/docs/latest/develop/data-types/probabilistic/top-k/)

