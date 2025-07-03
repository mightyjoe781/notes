# Load Balancing and Fault Tolerance

## Load Balancers

* One of the most important component in distributed system that makes it easy to scale horizontally
* load Balancer is the only point of contact
* Every Load Balancer has either
  * Static IP
  * static DNS Name
* load balancer hides the #server that are *behind* it allowing us to add *as many servers* as possible without client knowing about it
* Request Response Flow
  * Client already has IP/domain of load balancer
  * client makes API call and it comes to load balancer
  * load balancer picks one server and makes the same request
  * load balancer gets the response from the server
  * load balancer responds back to the client

### Load Balancing Algorithms

#### Round Robin

* distribute the load iteratively (uniform)

#### Weighted Round Robin

* distribute the load iteratively but as per weights

#### Least Connection

* pick server with least connection from the balancer. Used when response time has a big variance (analytics)

#### Hash Based Routing

* 

### Key Advantages of Load Balancers

* Scalability - servers can be scaled up and scaled down without User ever knowing.
* Availability - crashing of one server doesn’t affect entire infra, load balancer can route traffic to healthy nodes

## Circuit Breakers

* circuit breakers prevent *cascading failure*
* Example
  * User request comes to a feed service
  * Feed service pulls some info from recommendation system/Trending System
  * Recommendation and trending btoh relies on Profiles service
  * Recommendation and trending depends on Post Service
  * Post Service depends on Post Service
* There are lots of services that depend on profile service, if profile DB is overwhelmed (shuts down) and transitively all dependents on it are affected causing “Timeout”
* Two major affects
  * complete outage
  * unresponsiveness
* Idea : if recommendation service works without profile service, and returns some default feed. Then recommendation service becomes *circuit breaker* and stops cascading fialures

* How to Implement ?
  * A common database holds the settings for each breaker
  * services before making calls to each other checks the config (cahce the config to avoid checking the DB)
* In case of the outage, the circuit is tripped and DB updated, services will periodically check and stop sending requests to affected services

## Data Redundancy and Recovery

* API servers are *stateless* but databases are *stateful*
* API servers going down is fine because it can be respawned but thats no the cash if disk crashes
* A good system always takes care of such catastrophic situation
* The only way to protect against loss of data to create multiple copies of it - *Data Redudancy*
* Backup & Restore
  * Daily backup of data (incremental)
  * weekly complete backup
  * storing one copy across region (Disaster Recovery)
  * When something goes wrong, just restore the last backup
  * almost always easiest thing to do

### Continous Redundancy

* Setup Replica of the database and writes go to both DB (sync/async)
  * API server writes to both Database
  * API writes to one and is copied to other async
* If master database goes down, writes can be redirected to slave database replica which is temporarily promoted to master and handles writes.

## Leader Election for Auto-Recovery

* If there are bunch of nodes serving traffic, then if any of the node goes down, then a *orchrestration* service should bring up another replica of that node.
  * No human intervention involved
  * Minimal Time - outage
* But above scenario always keeps happening as orchestration might be down, how do we keep orchestration correctly ? orchestrator for orchestrators :(
* We keep two orchestration called as Orch leader, Orch workers. (Master-Slave Topology)
* If any of the worker figures out that orch leader is down, orch slave is promoted to master orchestration by the workers by consensus algorithms.
* Read up more on various Consensus Algorithms