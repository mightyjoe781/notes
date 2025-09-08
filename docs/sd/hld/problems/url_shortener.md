# Designing URL Shorteners

Motive : Understand partitioning, Sharding & Out of box solutions

Statement : Design a URL Shortener that generates pseudo-random human readable short URLs. Upon Visiting takes you to original website.

Why ? easy to share in Messaging Apps.
~ 100 M URL/month
~ no support for custom alias.

### How to shorten a URL ?

Approach 1 : Hash the URL

- SHA 256 are 256 bits long ~ 15 B
- 16 B short url are not short. (`url.sml/abcedfghij...16 chars`)
- Two URLs can have the same hash.

Approach 2: Integer ID as short

- if URL stored in DB is at ID : 1337
- very short but predictable (`url.sml/1337`)
- someone can easily scrape all shortened URLs

Approach 3: Custom Encoding

- Total unique characters in short url = $(a-z) + (A-Z) + (0-9) = 62$ chars ~ $2^6$
- we define a map that maps each of 6 bits to a character

| BITS   | char |
| ------ | ---- |
| 000001 | a    |
| 000002 | b    |
| ....   |      |

- Our encoding scheme : user is storing some URL and when we stored it in the DB, ID that was assigned 79.
- 79 ~ url but what is sent to user is `sml.url/bp`
- 79 ~ `100011111`
- left padding ~ (000001)(001111) ~ bp
- But this is still predictable, Shuffle the map for each bits of characters to make it difficult to predict.

| BITS   | chars |
| ------ | ----- |
| 000001 | q     |
| 000002 | x     |
| ....   |       |

* But if one fires so back to back request one would know the pattern and would be able to reverse engineer the custom encoding, so instead of picking sequential ID, we pick random ones. This will form the crux of our approach !

### Storage

we store mapping b/w short URLs and actual URL in database.
Schema :

| urls       |               |
| ---------- | ------------- |
|            |               |
| short_code | url           |
| bpqAzq     | https://..... |
| a2Am6      | https://..... |
NOTE: short-code are not derived from the URL.

Given our access pattern is just KV based, we can store these in any KV store that is partitioned by short_code.

We can pick any KV store or even relation DB to hold this.
Amount of data = 100 M x (8(code) + 120(url))
per month = 128 x 100 M = 12.8 GB

Storage is not the concern, we shard to handle load.

### What happens when someone visits `url.sml/bp` ?

When someone visit the URL, the request comes to our API server we get the actual url from the shard, we return 301 redirect with this URL. (this would ensure user is redirected to actual URL)
But before returning 301 status code, we emit an event to register the analytics.


![](assets/Pasted%20image%2020250907194206.png)

### Caching ?

Newly published URLs are more likely to see hits, we cache the short urls that are *new* or *hit* popular. ~ reduces load on DB, improves latency.

- Visualisation for end user : we leverage aggregation of stats DB to render fancy visualisation for the user.

![](assets/Pasted%20image%2020250907194441.png)

NOTE: stats DB is sharded by user who created the url. Aggregation are mostly per user and we leverage Grafana to render them.

### How is short code/url generated ?

- if we go one by one ... easy to predict the next one
- generating random integer is prone to collision
    - hence we have to do it uniquely pseudo random
- only one machine should not be handling this ~ too much load on one machine
- 100M/30 ~ 3 M per day ~ 125k per hour ~ 2k per minute (averge) ~ peak will be way worse traffic

We leverage partitioning, sharding and transactions to achieve this !!

We setup a few database servers having a job to issue one random integer (unique, non-repeating, making it difficult to guess and reverse engineer the logic) atomically (no matter how request hit the database at once there will be no collisions)

#### Ticket Server
On a smaller scale (one DB handles this) (0-1000) say we partition it in 4 ranges.

| start | end  | current |
| ----- | ---- | ------- |
| 0     | 250  | 0       |
| 250   | 500  | 250     |
| 500   | 750  | 500     |
| 750   | 1000 | 750     |
current : the value that will be returned when the value is hit that range.

![](assets/Pasted%20image%2020250907195320.png)

1. user wants short url
2. API server picks ticket server, server knows *available range ids* (configurable)
3. API server selects one range at random
4. API server
    1. select the *current of the range*
    2. increments current by 1 if *end != current*


| id  | start | end  | current     |
| --- | ----- | ---- | ----------- |
| 1   | 0     | 250  | 0           |
| 2   | 250   | 500  | _250_ ~ 251 |
| 3   | 500   | 750  | 500         |
| 4   | 750   | 1000 | 750         |


**TXN**
```sql
SELECT * FROM ranges
    WHERE id = ?
UPDATE ranges SET current = current + 1
    WHERE id = ?
```

if range is exhausted, server remove the range (id) from its in-mem store (table).

#### COMMIT
Because we are picking one random range, we see a pseudorandom order within range the order is sequential .
Now once we have the *random id*, we can encode the store mapping of store url & original in urls db

We take max ids we would support say *4 Billions* at 100 M per month consumption will take 40 months ~ 3 years to exhaust the range.
If we want to support more, we increase *int* to 64 bits. giving us range till $2^{64}$ ~ 1.84 x $10^{19}$
and it would take

$$
2^{64} = \frac{1.84 \times 10^{19}}{100 \times 10^6} = 1.84 \times 10^{11} \text { months } \equiv 15.33 \times 10^9 years = 15 \text{ Billion years}
$$

Our 64 bit numbers ~ 66 bit ~ 11 char (encoded)
But if we want to restrict the short code length just reduce the bit. Also, instead of starting from 0, lets do it from 100,000 to have short code of length at least 3.

Say, we use code in length of min 3 to max 8

$$
3 \text{ chars} = 3 \times 6 = 18 \text { bits} = 2^{18}
$$

$$
8 \text{ chars} = 8 \times 6 = 48 \text { bits} = 2^{48} = 5.62 \times 10^{14}
$$

So to select a good number we have go a range of numbers :
Say we want each range to exhaust in 1 year. so, it generates 100 M x 12 = 1200 M urls ~ $1.2 \times 10^9$ integers.

$$
\text{Total Range } = \frac{5.62 \times 10 ^{14}}{1.2 \times 10^9} \sim 4.5 \times 10 ^ 5 \sim 500,000 \text{ ranges}
$$


Now we have a range in millions
- 100k - 1200 M
- 1200M - 2400 M
- 2400 M - 3600 M

if one DB becomes a bottle neck, we spin up a new DB and move some ranges there. Now API server will pick one ticket server at random.


![](assets/Pasted%20image%2020250907201145.png)

Exercise

- implement the encoding schema we discussed
- explore analytics we can capture and how during short urls hit
- explore how exactly we share analytics data
