# Designing Twitter Trends

Motive : To understand how *many* components are needed to build at scale.

Twitter Trends is a page/screen where people find what's happening

![](assets/Pasted%20image%2020250907155650.png)

We display Image of the top trend, and articles about each trend based on popularity.

## Input to the System

In order to build Twitter Trends, we need all the recent tweets (almost realtime).
Hence, we push tweets (as soon as they are published) in a persistent, high-throughput (350,000 tweets/min) message stream ~ Kafka
Tweets DB could be Cassandra

![](assets/Pasted%20image%2020250907160326.png)

### News Clustering

Group similar news stories in to clusters. There are various clustering algorithms that can be applied, like *k-means* + *tfidf*
We have to prepare data for clustering.

![](assets/Pasted%20image%2020250907160819.png)

#### Process of Clustering

The clustering algorithm uses the crawled data and extracts feature vectors to cluster the articles. (stores them in Elastic Search mapped to our taxonomy). Supervised or Semi-supervised Learning.

Clusters we got are ranked as per recency & size.

Each cluster then picks

- Top Articles (media house, popularity) -> Used while rendering
- Reference Image (image from top article)
- Keywords (common keywords from articles)

### News clustering Service

The clusters, along with Metadata (top articles, keyword, top images) are stored in a database and *is used to serve the trends page* through News Clustering Service

For any `trend` the News Clustering service is contacted to fetch the meta and top articles to render.

![](assets/Pasted%20image%2020250907161716.png)

Given a *query* find the matching clusters *(used by trends, search, and discover features of the application)*

### Find What's Trending

Trending *entities* are computed (not just hashtags) for a domain, location and topic. E.g. We see WPL, IND vs AUS trending and not just hashtags.

In order to find what's trending, we have to

- prepare the data
- extract domain, entity and aggregate
- score and rank

If we consider every tweet to find, what's trending then it become easy to game the system. Hence its important to filter out *spam* (replies, low quality tweets, tweets with sensitive content, etc)

![](assets/Pasted%20image%2020250907162537.png)

Thus the candidate database now holds in a given time range, the entities that are popular along with their scores.

## Serving the Trending

![](assets/Pasted%20image%2020250907163132.png)

Instead of looking at one huge diagram, its better to look at one small subsystem at a time and explore it in depth

Final Data structure for Trends Database : `<time_window, location, trend>`
Each trend will contain

 - entity
 - domain
 - metadata (top tweet, top articles, statistics)

Exercise

- create a complete diagram of this system
- explore clustering algorithms
- pick a text/new clustering problem on kaggle
