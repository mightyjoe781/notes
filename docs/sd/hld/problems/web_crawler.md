# Designing a Web Crawler

Motive : Tracking, Capacity Estimation, Extensibility, Sheer Scale, Working Backwards

Starting with the seed URLs, crawl all the links that come our way. Process the text and create an inverted index

word $\to$ list of documents
Relevance is out of scope, HTTP pages only

### Crawling Basics

*spiders* are used to crawl website.
spider start with seed URL, download the pages, extract the links within them
and iterate in BFS order.

Example - Scrapy : we can also quickly code our own

Instead of storing from top, let's work backwards.

### Storage of Reverse Index

For each word we need to store list of documents (URLs) containing them.
Huge number of words, huge list of documents ~ screams massive scale of data
Access is key based (given word, give me list of doc)

KV database like Dynamo DB.


`apple : [doc1, doc23, ....]`
`banana : [...]`

### Estimating size of Reverse Index

Assume : every webpage is assigned a 32 byte identifier, there are 1,000,000,000 webpages and there are 1,000,000 words, with on average each word is present in 1% of pages

Size of inverted index = 1,000,000 x (8 (avg word lenght) + 10,000, 000 x 32)
Size of inverted index = 8 MB  + 32 x 10, 000, 000, 000, 000 B
Size of inverted index = 8 MB + 32 x 10 TB = 320 TB

Possible Optimization : Compression, Champion List

Instead of storing all pages where word `w` is present we only store the `popular` or `significant` ones only.

### Search Engine using Reverse Index

Search engine will use this reverse Index to provide relevant results. How search engines determines relevance is out of scope for this system. TF-IDF

> Term Frequency-Inverse Document Frequency, a statistical measure used in search engines and information retrieval to evaluate the importance of a word in a document relative to a collection of documents.

![](assets/Pasted%20image%2020250908114910.png)
### Extracting words from webpages

Assume we have webpages stored *somewhere* we have to continuously read them, parse them, strip off style/script and tokenize and update the inverted index.

Given the amount of data to be processed is HUGE, one machine will not be able to do this. But where would we store the web pages ?

Given web pages are just blob files (not actively queried), we can store them on S3 (blob store).
But how do we know which one are new ones ? In S3 the folders will be arranges/partitioned by time

`s3://the-internet/2023/01/mm/yyyy/<batch of webpage>1.zip`

This makes it easy to read folders that interests us and also keep track of them.

![](assets/Pasted%20image%2020250908114746.png)


### How webpages get into S3 ?

Crawlers craw the pages, but can they directly put them on S3 ?
Doing a lot of microwrites (one per page) on S3 is slow and time consuming so we process them in a batch.

Crawlers hence write the crawled page on local disk and a small daemon packs them up, zip it and upload to s3.

![](assets/Pasted%20image%2020250908115539.png)

Crawler crawls and stores data on local disk.
Daemon packs and upload to S3 `[at specific location - partitioned by time]`and  Delete file from HDD.

### How crawler crawls efficiently ?

Yes, we know crawler start with the seed URLs and all, but given there are distributed server they should have a DB

All servers running crawlers co-ordinate through a common DB (URL DB).
URL DB is responsible for assigning a uniquer id to each URL is responsible to hold stats about recent crawling amount of data is huge, hence we need it to be sharded and KV based access is fine.

Dynamo DB with domain as hash key seems fine.

![](assets/Pasted%20image%2020250908120140.png)

schema

| uid                     |     |
| ----------------------- | --- |
| url                     |     |
| last_crawled_at         |     |
| recent_crawls: `[ ...]` |     |
Periodically crawling stats are archived to a blob storage to keep the database optimal

What if we stumble upon same URL multiple times in a short time window, say 1 week.

### Per domain Configuration

We need a per-domain cool down period for crawling.
Whenever the crawler stumbles upon a link (url), *separate configuration*

1. it extracts the domain
2. loads the domain configuration
3. checks the last crawled at
4. decides to crawl or not

No need to have another DB. We can store this info in URL.

per domain config, status, reputation, rank, meta details like name, icon, etc.

### Performance Optimization

We can leverage Bloom Filter to check for pages, *not recently crawled* and this would help us save a ton of DB calls.
We save recently crawled pages in Bloom Filter and it is periodically reconstructed.

### Priority Crawling

There are some website that are frequently crawled and should fast index.
Handling these requires us to have a parallel setup of crawlers segregated by priority.

![](assets/Pasted%20image%2020250908120720.png)
### Periodic Crawling

Crawling is not a one time activity, the pages/website needs to be frequently crawled for 1. newer pages, 2. updated information

- define a generic crawl frequency
- let user request for reindexing through sitemap submission

We need *job* that finds domains eligible for a re-index & a way for explicit reindexing.

![](assets/Pasted%20image%2020250908121051.png)


### Storage Improvement

Entire internet is filled with duplicate content (~28%) so we can reduce our storage (not processing) by the same fraction by not storing duplicate data.

Approach 1 : Match web pages (super expensive, huge pages)
Approach 2 : Match hash (two page with same content will have same hash + hash are very small (256/512 bits)).
Risk of collision but mostly insignificant.

### How crawlers guarantee no job overlap ?

In order guarantee uniform work distribution we can make a set of servers responsible for a set of domains

This looks like a problem of *data ownership* ~ consistent hashing.
Certainly not the the only way though, fault tolerance !

![](assets/Pasted%20image%2020250908121557.png)


### Exercise

- Write a small scrapper/crawler using scrapy
- ingest data in Elastic Search
- Query the data and play around with it
- try to not process the same webpage twice, within 5 minutes
- implement consistent hashing
- run 5 instances of crawler and ensure they do not overlap
