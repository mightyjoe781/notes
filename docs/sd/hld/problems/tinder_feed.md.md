# Designing Tinder Feed

Motive : playing with location and keeping things efficient.

Statement : Design Feed for Tinder and feature to swipe left or right. For great user experience, a user should not be shown a profile that he/she already swiped.
Feed Criteria

* Proximity : near the better
* Common Interest : shared interest

## Capture Proximity

User's device app continuously emits (lat, long) to our backend, we store this information in a database

* that support geo-spatial queries (generating feed)
* can be horizontally scaled through sharding ~ (handle huge incoming load)


![](assets/Pasted%20image%2020250907135938.png)

Amount of data is not the concern but the query to store and get is ! Hence we are sharding the database.

## Capturing Common Interests

1. Ask user to provide those details (profile information)
2. Capture the details with social login : google/facebook/twitter (connect for scraping profiles)

![](assets/Pasted%20image%2020250907141240.png)

Now that we have the interest information and current location we can generate feed for users.
Behaviour : generate feed when user is about to exhaust the current one.

* frontend (app) will make an API call to trigger population of the feed.
* maintain a feed counter in backend and check everytime user swipes.

### Feed Database

Feed database can potentially explode ($n \times n$) and will require decent storage. For each user, the DB holds feed items. Fetch feed item ~ profile information that user has not seen before

Approach 1 :
Store `<user_id, candidate_id, created_at >`
we can partition by user_id, and order by created_at.
But whenever we are returning, we have to fetch profile info in real time and send it to user (additional n/w call).

Approach 2 :
Store : `<user_id, candidate_profile, created_at >`
we require a significant storage + risk of serving stale data, but we avoid making call to profile service on runtime.

In either case, you should never store feed of a user is "`list`" (say Mongo DB)

* it will bloat up the document size on mongo db
* expensive serialization and deserialization
* iteration is difficult

### Feed Generator

- should be async, because it is time consuming
- should be triggered by frontend

![](assets/Pasted%20image%2020250907143126.png)

### Storing Swipes

People swipe left or right to indicate interest.
We do not need a separate DB to hold this info and we leverage Feed Database and just add `is_intrested` in each item

NOTE: You don't have to create a new DB for everything

When A swipes B,
- mark `is_interested` in feed item
- check `<b, a>` in feed DB
- if entry doesn't exist or `is_interested = false` do nothing
- else : create a match (in match DB)

`<user_a, user_b, match_id>` : Match DB Schema, here `match_id` will be used by messaging service and all messages are for a *match*

![](assets/Pasted%20image%2020250907143643.png)

#### Ensuring no-repetition

- when A registers a *swipe* for B
- A should never see B again in the feed
- while generating the feed, we have to check for past swipes & add only if new profiles are there

Since here we need a definite no, approximate yes, it is fine ~ classic use case of Bloom Filter
Use Redis + Periodic persist to store swipe information. Bloom filter is considered before adding any item in feed database.

![](assets/Pasted%20image%2020250907144052.png)

