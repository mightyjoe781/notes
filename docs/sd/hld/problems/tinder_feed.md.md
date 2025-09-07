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

