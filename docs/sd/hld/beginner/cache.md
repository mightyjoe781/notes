# Caching and Optimization

> There are only two hard things in computer science: cache invalidation and naming things. - Phil Karlton

## What is Caching

* caches are anything that helps you avoid an expensive *network I/O*, *disk I/O* or a computation.
    * API call to get profile information
    * reading specific line from a file
    * doing multiple table joins
* Frequently accessed data is stored in a temporary location. The API server first checks the cache. If the item is not present, it fetches it from the actual database and stores it in the cache.
* Cache are faster and expensive(loaded in memory). Cache is not a breaking point in a design, it helps improve the design.
* Caches are just *glorified hash tables*
* Examples include
    * Google News
    * Auth Tokens
    * Live Stream

## Populating and Scaling a Cache

![](assets/Pasted%20image%2020251221195711.png)

* cache is put in between API server and database
* Lazy Population (most popular)
    * Read first goes to cache, if data exists return it, or else fetch from db, store in cache, and then return
    * Ex - Caching Blogs, (multiple joins involved)
* Eager Population
    * Writes go to both database and cache in the request call. Ex - live cricket score
    * Proactively push data to cache, because you anticipate the need. Ex - Twitter Celebrity Problem

## Caching at Different Levels

* Caching can placed at everywhere, but it comes with a cost of stale data and invalidation. Caching is ideally a very difficult problem to solve perfectly, you only need to approximate your use-case solution.

### Client Side Caching

* storing frequently accessed data on client side. Ex - browser, mobile devices, etc
* cache near constant data (e.g. images, ui components, user information)
* it should be okay serving cached info (stale)
* invalidation by time (expiry)

Massive Performance boost, as we need not make any requests to backend

### Content Delivery Networks (CDN)

* CDNs are a set of servers distributed across the world, used for caching
* request from a user goes to geographically nearest CDN server and user gets a quick response.
* Example - this site is hosted in Dublin, and ideally would be slower to load from India, but a CDN for a user in India will make it fast. For this site, I am using Cloudflare CDN.
* CDN does lazy cache population!

### Remote Cache (Redis)

* Centralized cache that we most commonly use (Redis). Multiple API servers use it to store frequently accessed data.
* Every key stored should have an expiration date(memory leak)
* Size of cache is relatively very small as compared to a database

### Database Caching

* Instead of computing total post by users every time, we store `total_posts` as column and update it once in a while (saves an expensive DB computation)
* This often involves re-evaluating the data model.


NOTE:

* There are other places like load Balancer where we can use cache.
* We can cache some data at every single component, and it should be used sparingly because make sure that staleness of the data doesn’t affect the speed of your component.
* Cache Invalidation is really hard to solve problem.



