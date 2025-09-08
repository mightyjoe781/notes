# Design e-commerce product listing

Motive : Understanding how a system is built and taking a structures approach in building one. Understanding core-infra components and how they fit.

Problem Statement:

For a small shop (100 items) design a system through which the shop owner can

* add a new product
* update/delete existing product
* list all the products on the websites
* customers should be able to quickly access the catalog

NOTE: Payment is out of scope for this discussion.

Storage :

- not huge data, only 100 rows
- there seems to be a structure, we can go with SQL DB
- 100 x 1KB ~ 100 KB data
- `product` table to hold all the catalog.

Serving the data :

* simple REST based HTTP webserver is fine
* we will need many (handle large request)
* hence put a load balancer

Load Balancer will have DNS like `api.mstore.com`

![](assets/Pasted%20image%2020250906182036.png)

* Classic Three tier architecture: user, compute, storage. Often represented as follows

![](assets/Pasted%20image%2020250906182516.png)

* End user will not directly interact with backend, needs the frontend service.
*  In read world we will need an admin UI as well for adding products to listing.

![](assets/Pasted%20image%2020250906182902.png)

* Load on catalog frontend service, backend service and storage would require load balancer and multiple servers. For Admin UI we can get by using 1 server.
* From the design we can understand that load is read heavy, we add multiple Read Replicas, and keep a master Replica (primarily for write).
* To Keep read traffic to replica, we will manage that in the backend service, using multiple database connection pools.
* Can we add cache to read ? Definitely but it comes with the cost of Cache invalidation as admin is updating the database. But we are handling read requests using Read Replicas.

![](assets/Pasted%20image%2020250906183806.png)


Exercise

* Design DB Schema for this system
* Write a simple backend API service exposing APIs
* Setup DB Replication
* Move read APIs to read from Replica

