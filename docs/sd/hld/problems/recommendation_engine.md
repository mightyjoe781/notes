# Design a Recommendation Engine

Motive : Understand ML System, plug and play, Graph DBs in ML systems.

Recommendation Engines are heart and soul of consumer platforms.

- Youtube
- Amazon
- Spotify

Depending on what the platform is the *feature* changes but overall architecture remains similar.

Lets take a concrete example :
Say we are designing Recommendation engine for Amazon, Recommend products that people would buy

### Naive Approach

Recommended the most popular items. Simple, quick and dirty.

- most popular items are same for all
- there is no personalization
- would recommend item you already bought or is out of budget or irrelevant

You have never made a purchase > 10k Rs, but amazon keeps recommending a 1.5Lakh Laptop

### ML Approach 1 : Content Filtering (Exploitation)

Show me products similar to ones I shopped. Can be expended to *videos*, *songs*, *searches*
Above technique works well for some niche use cases

- recommending similar books, songs, videos, creators.

How to implement ?

Cluster the *content* (title, description, type, tags) such that similar ones falls closer when user sees/watches/consumers one, we pick few more from this cluster and add to recommendation section.

![](assets/Pasted%20image%2020250908090838.png)


When user transacts or is on a product page we hit the recommendation service and fetch the recommendation.

![](assets/Pasted%20image%2020250908090936.png)

#### Cosine Similarity
Convert the product into vector in *n* dimensional space, where `n` = features like *tokens, price, categories, etc.*
Product A and B are more similar than A and C. We know
$$
\cos(0) = 1 \text{ and } \cos (90) = 0
$$

$$
similarity = \cos(\theta)
$$
Two products are similar if $\theta \to 0$ i.e. $\cos(\theta) \to 1$ (approaches)
We can also use other distances Euclidean to quantify similarity.

### ML Approach 2 : Collaborative Filtering (Exploration)

Collaborative Filtering Clusters users and recommends things that other similar user bough

- A *bought* iPhone
- A *similar* to B
- B *could buy* iPhone (recommendation)

Core Idea : Of all the missing edges, which one has maximum probabilities of occurring.

![](assets/Pasted%20image%2020250908091246.png)

Instead of recommending similar items, collaborative opts explorations. This approach helps to spice up recommendations
- suggest new books
- suggest new shows
- suggest new articles
- suggest new products

Basically What is new ?

#### How to implement ?

1. Cluster the users
2. Replicate purchase history into another storage
3. train and predict

![](assets/Pasted%20image%2020250908092058.png)

#### Querying Candidate User

1. Pick a few users from the cluster *at random*
2. pick top n similar users to a particular user
3. if cluster is small enough pick all

#### Query Candidate Items

For each candidate user find items that they purchase but our user A didn't.
Simple Query for a Graph Database.

#### Predicting
For each of the candidate item, 
predict how much would user *find it interesting* (rate the product)
as a factor of how similar they are.

If *u* and *v* are very similar they will give similar rating.
Now arrange the prediction in descending order and get top *n* entries.

#### Serving Recommendations

Recommendation Database is a simple KV store that holds
`user_id` -> `[product1, product2, ....]`

Simple scoring and ranking job runs on top of Graph DB generating recommendation for each user (as mentioned above)

![](assets/Pasted%20image%2020250908093032.png)

This is async recommendation generator.
#### Serving Recommendation & Triggering Proactively

We want recommendation to be re-generated when they *exhaust*.
This can be a simple event from frontend, pushed to Kafka.

![](assets/Pasted%20image%2020250908093252.png)

#### Similar Systems

Movie Recommendation Systems, Article Recommendation Systems
Recommendation in Feed (twitter, instagram, tik-tok)

#### Exercise
- understand clustering
- understand collaborative filtering
- solve one clustering question on Kaggle
- solve one collaborative filtering question on Kaggle
- setup neo4j and populate with random data to fire query like
    - give me items that are not bought by me but are bought by all of my friends