## Impression Counting

### Point in Polygon : *RayCasting*

If a particular point lies in the polygon.

![](assets/Pasted%20image%2020250921110719.png)

Use-Cases

- location based reminders
- navigations
- airport rides
- Pokemon Go

### Impression Counting

One of the most used system out there and it finds its application across.

- Linked In - count views on the post
- YouTube - count views on the video
- Google Search - count impressions on a search result
- Reddit - count views on a post
- Google Adsense - count impressions on an Ad
- Instagram - count views on the photo

Problem : Not everyone reacts, so how to measure engagement.

AdTech firms wants to render the graph that shows how was the campaign
Total number of unique visitors in last `n` time units
NOTE: `n` is given as an input at runtime.

Requirements :

- realtime/near-realtime ~ each user counted once in a time window
- No aggregates ~ count can be a close approximate
- same rules to filter out unwanted events

#### On the fly counting

*Count distinct users* on a post (Ad) from `04/01/2022` to `08/01/2022` 10:00AM

![](assets/Pasted%20image%2020250921115339.png)

NOTICE : combining both ranges, requires *Union* rather *Summation*

#### Input

Stream of views on videos/ads/etc
Given a stream of elements, find count of distinct elements in a given time window

[ A, A, B, C, A, B, C, A, D, A, B, C, A] = 4 distinct users

#### Naive Solution

Hashset of user_ids grouped by time : precomputed due to aggregation

```txt
20220401_1200 = [a, b, c, d, e, f]
20220401_1300 = [a, c, d, w, x]
20220401_1400 = [c, d, e, f]
```

Total unique users : set of union(`20220401_1200, 20220401_1300, 20220401_1400`) = 10 views

This is taxing on CPU and memory !! Takes time to compute granularity is critical.

At smaller scale, this approach works well but at massive scale this is not sustainable.
user_id is int ~ 4 bytes
1 M people view an Ad /minute ~ Total Storage ~ 4 MB
Say we want to compute total unique visitor in last 1 hours ~ 60x4MB ~ 240 MB of data for 1 Ad for 1 hour.
There are one thousands of customer who want to see their ad campaign is performing.

5000 x 240MB = 1200GB!!!

At scale, this needs to efficient,
let's approximate : *Cardinality Estimation Problem* ~ Efficiently approximate the cardinality of resultant sets after `n` unions

#### Hyperloglog ~ Flajolet Martin Algorithm

In this design, we use this as a Black Box. How much memory are we saving ?
4MB in set -> 12KB in HLL

Thats almost of `0.15%` of the space

Operations on HLL,
Redis gives you this data structure out of the Box.

- Add an element to HLL ~ PFADD ~ O(1)
- count of element of HLL ~ PFCOUNT ~ O(1)
- Merge N HLLs ~ PFMERGE ~ O(N)

You cannot delete from HLL (similar to Bloom Filter) ~ This is lossy in nature.
 
```txt
p1: 20220401_1200 = HLL[a, b, c, d, e, f]
p2: 20220401_1300 = HLL[a, c, d, w, x]
p3: 20220401_1400 = HLL[c, d, e, f]
```

Total Unique Visitors

temp_total = `PFMERGE(p1: 20220401_1200, p2: 20220401_1300, p3: 20220401_1400)`
Create a new HLL by merging, return the `PFCOUNT(temp_total)`

Total Views between20220401_1200 & 20220401_1359

`temp_hll = PFMERGE(pl:20220401_1200, 20220401_1359)`
`return PFCOUNT(temp_hll)`

#### Architecture

Input : Kafka with view events of a user
If user made `n` views in 1 min window, count as 1

![](assets/Pasted%20image%2020250921124951.png)

- 0 views if user sees own video
- min watch time ~ 5 minutes
- 10 views in 1 min count as 0

![](assets/Pasted%20image%2020250921125044.png)

Events always move forward in time.
For each event, counting consumers read from kafka and ingest it in corresponding HLL of the post. 

Each post each minute : p1: 20220401_1200 = HLL[--]
command - > PFADD p1: 20220401_1200 user_123

#### Querying
We have a separate set of machines that queries the HLL from Redis and responds

![](assets/Pasted%20image%2020250921125219.png)

Depending on the request, the analytics engine hits the redis, merges the relevant HLLs, computes the cardinality and return the response *PFMERGE* and *PFCOUNT*

#### Does it work at scale ?
YouTube has millions of videos, millions of users and billions of events.
Keeping them all on Redis is very costly.

- we cannot keep entire data in Redis
- Only Redis know HLLs

Keep last 30min/1hour data in Redis (events always move forward)
Keep older data in cheap KV storage (Data is anyways immutable)

![](assets/Pasted%20image%2020250921125652.png)

1. Periodically (10seconds) HLLs are copied from Redis to DynamoDB
2. HLLs are always updated in Redis
3. If key doesn't exist in Redis it is brought from DynamoDB
4. For analytics query all relevant HLLs are brought in Redis & then cardinality is computed.
## Remote File Sync

Say, you are building Dropbox

![](assets/Pasted%20image%2020250921135811.png)

When a file is uploaded to Dropbox cloud from one of your device, it needs to be

- uploaded efficiently
- synced efficiently

Challenge 1 : how to build resumable upload & downloads ?
Challenge 2 : how will clients know about new changes ?

![](assets/Pasted%20image%2020250921141144.png)

Chunking a file makes it better for parallel upload and resumable

File is broken into chunks of 4MB and each chunk is called as *block*
Each block is then passed through a Hash Function spitting out a *hash* (identifier)

File representation : A file is represented as a series of hash called as Blocklist.
`video.avi -> [h1, h2, h3, h4]`

Blocks are stored on Blob Storage (S3) with identifier hash
e.g. `s3://my-dropbox/<acc_id>/<block_hash>`

#### Blocks DB
Namespace ~ Account ID
Hash ~ Block Hash
Block ~ Actual Block

This simple table will help us identify if a block exists in an account, if yes we can obtain the content.

How is a file information hold in DB. 
File is a list of block hashes.
#### File Metadata DB
Namespace ID ~ Account Id
Relative path ~ /video.avi
BlockList ~ h1, h2, h3, h4
Version ID ~ monotonically increasing across an account

#### How upload works

Client talks to metaserver and says it wants *commit* the file *video.avi* having block hashes *h1,h2,h3,h4*. Metaserver checks Blocks DB and informs none of the blocks exists.

Client then talks to Blockserver and uploads two chunks (blocks) at a time and waits for an ACK. It repeats this until all blocks are uploaded.

Client re-commits the file and this time the file is saved.

![](assets/Pasted%20image%2020250921142714.png)

The file is saved implies and entry in file metadata DB.

#### What if a file changed ?
Say, now a few bytes of the file changed so client tries to commit the file and sees the blocks are [`h1, h2, h3', h4]

The file is saved implies an entry in the file metadata DB

| version | namespace | relative_path | blocklist       |
| ------- | --------- | ------------- | --------------- |
| 1       | my-drive  | /video.avi    | h1, h2, h3, h4  |


![](assets/Pasted%20image%2020250921161850.png)

Client finds out (from metadata) that `h3'` is missing, it uploads the 4 MB block to Blocks DB and re-commits and this time it succeeds

| version | namespace | relative_path | blocklist       |
| ------- | --------- | ------------- | --------------- |
| 1       | my-drive  | /video.avi    | h1, h2, h3, h4  |
| 2       | my-drive  | /video.avi    | h1, h2, h3', h4 |
| 3       | my-drive  | /photo.jpg    | h5, h6          |

#### How client knows what changed

We need a way to *sequentialize* the updates and every client can maintain till which update it has the changes.

- this looks oddly similar to checkpoints in Kafka, Kinesis. Can we get some inspiration ?
- *VersionID*

Version ID ~ Every-time any update happening in a namespace the version ID is incremented.

| version | namespace | relative_path | blocklist       |
| ------- | --------- | ------------- | --------------- |
| 1       | my-drive  | /video.avi    | h1, h2, h3, h4  |
| 2       | my-drive  | /video.avi    | h1, h2, h3', h4 |
| 3       | my-drive  | /photo.jpg    | h5, h6          |
| 4       | my-drive  | /notes.txt    | h7, h8          |
| 5       | my-drive  | /photo.jpg    | h6'             |

Client can now say, I am at `2`, any new changes ?
Metaserver can then forward all updates to the client post 2.

#### Multi-version

| version | namespace | relative_path | blocklist       |
| ------- | --------- | ------------- | --------------- |
| 1       | my-drive  | /video.avi    | h1, h2, h3, h4  |
| 2       | my-drive  | /video.avi    | h1, h2, h3', h4 |
| 3       | my-drive  | /photo.jpg    | h5, h6          |
| 4       | my-drive  | /notes.txt    | h7, h8          |
| 5       | my-drive  | /photo.jpg    | h6'             |
| 6       | my-drive  | /video.avi    | h1, h2, h3, h4  |
We can very easily re-construct and old version of a file.

h1, h2, h3', h4(v2 of video) ---> h1, h2, h3, h4 (v1 of video)

Since server holds reference to $h_3$ . The file can be reconstructed easily.


Similar Systems

- google drive & multi-versioning
- slack, teams, etc. even whatsapp.
- only where we need "updates"


Exercise

- read and implement RayCasting
- read about AB Testing in Social Media, read netflix blog
- read segment trees implementation, hyper-log-log (probabilistic data structure)
- read about differential synchronisation
- implement operational transformations