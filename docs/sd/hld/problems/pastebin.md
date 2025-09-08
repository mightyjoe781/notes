# Design Pastebin (Github Gist)

Motive : Not storing derivables, cost effective design

Requirements : Pastebin is an online platform that allows you to
- store any text file (content)
- share it with anyone (publicly or secretly)
- set an expiration for auto deletion
- URL generated for a paste is unique
- file stored can be long (but not huge) 10 MB max
- one who created the paste can edit it as well

### Where should we store the file ?

We have two options : Database or Blob store like S3
To decide which one, let's crunch some numbers

Max. size per file = 10 MB
Say # writes = 10 M per month
Total storage req = 10 M x 10MB = 100 TB (per month)

*Bandwidth Requirement Calculations*
Typical write to read = 1 : 50
Total data read = 5 PB (per month)
Since data is huge & per file size is long enough, there is no rationale to store this on a database.

### Storage
We store files on S3 and metadata on Relational DB
Schema : store

| uid  | name  | createdAt | Visibility          | owner_id |
| ---- | ----- | --------- | ------------------- | -------- |
| (36) | (120) | (4)       | (4) (PUBLIC/SECRET) | (4)      |

$$
10 \ M \times (36 + 120 + 12) = 10\ M \times 168 = 1680 \ MB = 1.6 \ GB
$$

Handle-able by simple relational database : We could also go with KV store like Dynamo DB.
### API and Compute
For uploading and accessing the files we need API servers.
One will not be enough, hence we add many behind a Load Balancer

![](assets/Pasted%20image%2020250907230459.png)

NOTE: we did not store S3 path in relational DB (Meta DB)
On S3, we configure our bucket : *gist-paste*
When user $1729$ uploads the file with UUID: $7128356$

1. File is sent by user to API server on HTTP Post
2. API server gets the file
3. API server generates a random UUID
4. API server uploads file to S3 at `s3://gist-paste/1729/7128356`
5. API server makes an entry in meta db
6. API server returns response

| uid     | name    | createdAt | Visibility | owner_id |
| ------- | ------- | --------- | ---------- | -------- |
| 7128356 | abc.txt | -         | PUBLIC     | 1729     |

Name is just display file on UI, NOTE: Avoid storing something that can be derived in the database.

![](assets/Pasted%20image%2020250907231126.png)
### URL of the File
The url through which we would access the file would be : `https://gist.github.com/7128356`

Read request flow is straight forward,
S3 path created from entry.

NOTE: If files are too big, you can send a presigned URLs to user to upload the files, making the upload responsibility of the User's browser, rather than uploading through your service.
### Cache
There might be some files that are frequently accessed, so should we cache them to improve user perceived latency ?
We are for sure tempted to do so ? but is it worth it ?

- cache stores in RAM
- pretty expensive

*Frequently ->* how much ?
If the frequency is not *huge*, it does not make sense to cache the file. As a one word answer
I would rather prefer to server 10 request from S3, than add an expensive cache and maintain it.

But be open to understanding user behaviour and access pattern

### Expiration
Owner of the file can set expiration to a file, post which it becomes inaccessible and eventually deleted.

We add *expiration* column, when file is accessed, we first check expiration time, if beyond return 404 else fetch and return.

Run a simple cleanup job that cleans up expired file from meta db and s3.


![](assets/Pasted%20image%2020250907231852.png)

### Fault Tolerance
Take periodic backup of MetaDB and store it on S3
This would help us with disaster recovery ? recovering from data loss
### Analytics

Whenever a file is accessed, the API server captures the request metadata and stores it on *elastisearch* for end-user analytics.

- Elastisearch : good for recent analytics
- Aggregation and Visuatlization

Given analytics data is huge & we may not query it beyond 6 months. Archive to save space.

![](assets/Pasted%20image%2020250907232635.png)
### Exercise

- capture request data (ip, region, user-agent, etc) and dump it in Elastic Search
- build visualisation on top of it with *Kibana*
- Write a small cleanup job that periodically deletes the data from Relational DB