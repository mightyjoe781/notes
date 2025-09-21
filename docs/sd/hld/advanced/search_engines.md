# Designing Recent Searches

Let's say your insights teams come to you solve the following problems

- 50% of users tap on Search Bar within the first 5 seconds
- 30% of all searches happen through recent searches
- Suggest each user 10 most recent searches

Key Points : Bounded data, Unbounded data, Time

How would above key points affect our design ? Is stale data okay ? What about cross-device consistency ?

We want to store all search queries & optimize for 10 most recent searches.

### Storage

 We want to store Search Queries made by the users. (No Relations)

- large volume of data
- high write throughput
- access is always per user level

Hence we go for a partitioned NoSQL DB. e.g. MongoDB, Elastic Search.

![](assets/Pasted%20image%2020250920154240.png)

- when user searches something we take the search query and put it in this partitioned DB

Decision 1

- should the write from API to DB happen SYNC or ASYNC

Decision 2

- if we do it ASYNC  ... SQS or Kafka ? Also delay to get the record in the databases.
- if we do it SYNC ... will our DB handle the load ?

NOTE: *Search is one of the most hit APIs always !*

Decision 3

- one record per query per user ?
- one record per user

There are two ways to store it

1. user_id -> [q1, q2, ....] ~ will become expensive as queries pile up
2. [q1, ts, user, device, os, browsers etc] , [q2], ....[qn] ... individual documents


Unbounded data should not be stored in the way 1st point shows up. Most correct way would be to use 2nd point where each data point should be stored for individual user.

Let's think about the user Behaviour

- 50% of users tap on Search Bar within the first 5 seconds
    - High read requests, recent searches to be updated near realtime preload it for the user
- 30% of all searches happen through Recent Searches
    - high write ingestion

Because the delay (search query -> persistence) should be ZERO

1. Let's do a synchronous write
2. Because READ and WRITE heavy system -> in-memory store with pre-computed results

Advantage we get if we do read/write from memory is that is provides quick look-ups and No disk or separate index required.

In one of the partition of your DB if indexed, read throughput would not be best, see the example.

![](assets/Pasted%20image%2020250920155116.png)

Hence, we *SYNC* write to in-memory store and our partitioned DB.
You can also do an *ASYNC* write but it will not have a significant gain in performance and there will be some delay.

$$
API \to KAFKA \to DB
$$
But doing *ASYNC* will be good for extensibility!

![](assets/Pasted%20image%2020250920155805.png)

Our in-memory store *Redis* will have

- `u1 = ["sachin", "sehwag" ...]` -> recent 10 search queries (pre-computed)
- Here this will be fast reads, no processing and it will be same across all devices.
### Cost Optimisation

- redis will NOT store all queries for a user, instead will store the recent 10
- we may never access the historical queries for a user. So we archive any data that is older than 6 months

![](assets/Pasted%20image%2020250920160204.png)

- Saves huge amount of money & compute
- This has to be a product call on if they do not want to show at all or with higher latency. 

One key UX : 50% of users tap on Search Bar within the first 5 seconds
What is recent searches are not in Redis cluster ?

- if we go to DB & fetch -> will take time, poor UX
- can we pre-warm the data ?

UX : as soon as user clicks on the search bar the recent queries should be already available to be rendered.


![](assets/Pasted%20image%2020250920161603.png)


# Designing : Cricbuzz's Text Commentary

Requirements

- user should see live text commentary
- cost efficient architecture
- good user experience


![](assets/Pasted%20image%2020250920173853.png)

Cost Optimization : Archival, Short Polling
Durability : *retry*
Good UX : Direct update in Redis, Fetch from redis (for latest commentary)

![](assets/Pasted%20image%2020250920180509.png)

# Designing : Super Simple text Based Search Engine

### Text Based Search Engines

Information Need -> Find most *relevant* documents from the corpus. JSON, web_pages, text documents.

#### Simplest Search

Search Query (`q`) : Go through documents one-by-one and see if it `matches`. $O(n)$, not scalable and substring checks.

How can we make search efficient ? lookup faster ? -> *indexing*

We create `inverted index` on our corpus

$$
w_i = [d_a, d_b, ...]
$$
Here, $w$ represent the word we are searching for, and $d$ documents where the word has appeared.

#### Relevance Techniques

- weighted score : diff weights to diff fields (title, descriptions, footnotes)
- fuzzy search : BK trees, typos
    - lat -> bat, cat
    - search words 1 (tolerance) edit distance away from lat
- Spell Correction : HOUPE -> House and then search
- Synonymic Expansion : HOME = HOURE, match docs having either of the words.
- Phonetic : Metaphone, Soundex
    - word -> root word & stored
    - Insight : people do not know the word they are looking for but they remember the sound,
    - so their typos closely resemble the word.
    - Arnold Swarzenger/Swarzeneger/Schwarzeneger (Fuzzy is not optimal to solve it)
- Query Segmentation 
    - people forget `space`. e.g.` mcdonalds`, `mc donalds`


*Christopher Manning : Introduction to IR*
