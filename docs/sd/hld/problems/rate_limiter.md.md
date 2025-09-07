# Design Rate Limiter

Motive: understanding that more boxes $\ne$ better system. Understanding scaling decisions.

Requirements :
Systems break down under tremendous load and we need to ensure that doesn't happen.

Design a rate limiter, that

- limit the number of requests in a given period
- allows developers to configure threshold at a granular level
- does not add a massive additional overhead

Rate Limiter

- First line of defense, Any incoming request is first consulted against rate limiter.
- If we are under limits, allow connection, or else reject with status code `429`

Where does it fit ?

* There are 2 different ways to put a Rate Limiter
    * If you have proxy sitting in front of Backend Service then it can handle the rate limitting
    * Backend Service can track the throughput and communicate with rate limiter service to manage connections.

![](assets/Pasted%20image%2020250906190654.png)

## Understanding Rate Limiter

Rate Limiter needs track `#` requests in a given period. Hence we need a database to hold the count, but which one ?

* for every incoming request we would update the db
* for every incoming request we would read from the db (aggregate)
* we need ability to `clock` the time

Say, we rate limit per user

* we can store # request in a period
* once the period is over we reset the counter

Resetting the counter ~ expiring the key :

* KV Store  + Expiration -> Redis
* Redis also provides fast in-memory writes with periodic persistence.

Checking and updating

* we let the service (HTTP) Endpoint that talks to rate limiter database
* we let the services directly talk to rate limiter DB (saves network hop, but exposes critical internal details)

We could have added entire Backend service for Rate Limiter but it will add extra overhead of maintaining infrastructure and network hops.

![](assets/Pasted%20image%2020250906191830.png)

## Scaling the rate limiter

Given the services are directly talking to Rate Limiter Database
Scaling Rate limiter = scaling the database.

* Should we scale vertically ? Yes
* Should we add read replicas ? No ! traffic is not read heavy
* Should we shard the database ? Yes
    * Any function in backend service will extract user_id from token
    * check rate-limiter Db if good then proceed otherwise block

We can easily shard the database to handle more load. And store the redis servers by storing the configuration on the s3, and logic to handle the selection of the redis server would be handled by the library.

![](assets/Pasted%20image%2020250906192514.png)

## Admin Console

It is better to have a small admin console (frontend/backend), that is used by developers to reset counters & debug when things go wrong.

The service will also provide observability on infrastructure and report things like `#keys` or `#request` blocked, cpu/memory load, etc.

#### Exercise

* Read and Implement : Leaky Bucket, Fixed Window and Sliding window algorithm using Redis.