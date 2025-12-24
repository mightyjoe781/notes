# Load Balancers

**What are Load Balancers ?**

Load balancers are critical components in distributed systems that distribute incoming requests across multiple backend servers. 

They act as a **single point of contact** for clients while hiding the complexity of multiple servers behind them.

![](../../hld/beginner/assets/Pasted%20image%2020251221204406.png)

**Key Benefits**

- **Scalability** - Enable horizontal scaling by adding/removing servers without client knowledge
- **High Availability** - Prevent single points of failure by routing around unhealthy servers
- **Performance** - Distribute load to prevent server overload and reduce response times
- **Flexibility** - Allow maintenance and updates without service interruption

![](../../hld/beginner/assets/Pasted%20image%2020251221205436.png)

**Request-Response Flow**

1. Client sends request to load balancer's static IP/DNS
2. Load balancer selects an appropriate backend server using configured algorithm
3. Load balancer forwards request to selected server
4. Backend server processes request and returns response
5. Load balancer forwards response back to client

## Layer 4 vs Layer 7 Load Balancing

### Layer 4 (Transport Layer) Load Balancing

- operates on TCP/UDP Level - makes routing based on IP Addresses and Port Numbers only
- Use Cases
    - High-throughput applications requiring minimal latency
    - Non-HTTP protocols (databases, gaming servers, VoIP)
    - When you need maximum performance and don't need *content-based routing*
    - Faster and doesn't read the content, so its more private.

### Layer 7 (Application Layer) Load Balancing

* Operates on HTTP/HTTPs level - can inspect and make decision based on application content
* Use Cases
    * Microservice Architecture requiring path based routing
    * A/B testing and canary deployments
    * API Gateways requiring authentication and rate limiting
    * Content-Based Routing

| Aspect               | Layer 4                  | Layer 7                  |
| -------------------- | ------------------------ | ------------------------ |
| Performance          | Higher (less processing) | Lower (high processing)  |
| Routing Intelligence | IP/Port Only             | Full Application Context |
| SSL Handling         | Pass-through             | Can terminate & Inspect  |
| Caching              | Not Possible             | Can Cache Responses      |
| Protocol Support     | Any TCP/UDP              | Primarily HTTP/HTTPS     |
| Complexity           | Simple                   | Complex                  |

## Load Balancing Algorithms

### Round Robin

* distributes the load iteratively (uniformly) across all servers
* best for homogenous servers with similar processing capabilities

````python
class RoundRobinBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0
    
    def get_server(self):
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server
````

### Weighted Round Robin

* distribute the load iteratively but as per weights
* best for heterogeneous environments with servers of different capacities

````python
class WeightedRoundRobinBalancer:
    def __init__(self, servers_with_weights):
        self.servers = []
        # Create list with servers repeated based on weights
        for server, weight in servers_with_weights:
            self.servers.extend([server] * weight)
        self.current_index = 0
    
    def get_server(self):
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server
````

### Least Connections

- pick server with least connection from the balancer. Used when response time has a big variance (analytics, file upload)

````python
class LeastConnectionsBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.connection_counts = {server: 0 for server in servers}
    
    def get_server(self):
        return min(self.connection_counts, key=self.connection_counts.get)
    
    def on_request_start(self, server):
        self.connection_counts[server] += 1
    
    def on_request_end(self, server):
        self.connection_counts[server] -= 1
````

### Least Response Time

* Combines connection count with average response time.
* Algorithm : Routes to server with `(active_connections * average_response_time)` minimum value.

### IP Hash

* has of some attributes (ip, user id, url) determines which serve to pick
* Ensures session is persistent without sticky sessions, but can create uneven distribution if clients are behind a NAT

### Consistent Hashing

* best for session-stick applications, caching

### Resource Based (Dynamic)

* Routes based on real-time server resource utilization (CPU, memory, disk I/O).
* Implementation requires monitoring agents on each server reporting metrics to the load balancer.

## Active-Active vs Active-Passive

### Active-Active Configuration

All load balancers handle traffic simultaneously

Implementation Pattern

* DNS Round Robin - Multiple A records for the same domain
* BGP Anycast - Same IP announced from multiple locations
* Clustered Load Balancers - shared state between multiple LB instances

### Active-Passive Configuration

One load balancer handles traffic while others remain on standby

Implementation

* Virtual IP (VIP) Floating - IP address moves between servers
* Heartbeat Monitoring - Passive monitors active health
* Automatic Promotion - Standby becomes active on failure detection

| Aspect               | Active-Active              | Active-Passive          |
| -------------------- | -------------------------- | ----------------------- |
| Management           | Complex Synchronisation    | Simple                  |
| Resource Utilization | Full 100% Usage            | Waste                   |
| Point of Failure     | None, Multiple Entry Point | Single Point of Failure |
| Throughput           | High                       | Low                     |

## Health Checks

### HTTP Health Checks

* Monitor real request/response patterns to detect failures

````python
# we implement a health check which only activates when failures cross certain threshold
class PassiveHealthCheck:
    def __init__(self, failure_threshold=3, timeout_threshold=5.0):
        self.failure_threshold = failure_threshold
        self.timeout_threshold = timeout_threshold
        self.server_stats = {}
    
    def record_response(self, server, response_time, success):
        if server not in self.server_stats:
            self.server_stats[server] = {'failures': 0, 'successes': 0}
        
        if success and response_time < self.timeout_threshold:
            self.server_stats[server]['successes'] += 1
            self.server_stats[server]['failures'] = 0  # Reset failure count
        else:
            self.server_stats[server]['failures'] += 1
    
    def is_server_healthy(self, server):
        stats = self.server_stats.get(server, {'failures': 0})
        return stats['failures'] < self.failure_threshold
````

* Advantages: No additional network overhead, reflect real user experience.
* Disadvantages: Reactive only, may take time to detect issues.

### Active Health Check

* Proactively send test requests to verify server health

````python
import asyncio
import aiohttp

class ActiveHealthCheck:
    def __init__(self, check_interval=30, check_path='/health'):
        self.check_interval = check_interval
        self.check_path = check_path
        self.server_health = {}
    
    async def check_server_health(self, server_url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{server_url}{self.check_path}",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        self.server_health[server_url] = True
                        return True
        except Exception as e:
            print(f"Health check failed for {server_url}: {e}")
        
        self.server_health[server_url] = False
        return False
    
    async def monitor_servers(self, servers):
        while True:
            tasks = [self.check_server_health(server) for server in servers]
            await asyncio.gather(*tasks)
            await asyncio.sleep(self.check_interval)
````

Common Health Check Endpoints

* Basic: `GET /health` -> `200 OK`
* Detailed : Returns JSON with system status, dependencies, version
* Deep : Checks database connectivity, external service availability

### Application-Level Health Checks

* Verify application functionality beyond basic connectivity.
* Example assume we have few services connected to `/health` endpoint : Postgres, & Redis.

```json
{
    "checks": {
        "database": "healthy",
        "cache": "healthy",
        "dns": "degraded"
    },
    "status": "degraded"
}
```


### Phi Accrual Failure Detector Algorithm

$\phi$ : suspicion level of failure.
$P_{fail}$ : is the probability that the node has failed based on observed heartbeat intervals.


$$
\phi = -\log_{10}(1-P_{fail})
$$

NOTE: if $\phi$ exceeds some threshold, node is suspected to have failed.

Now Health Check Frequency can be adjusted based on phi values. Ex- if low phi is detected then checks can be less frequent or else we can increase checks.

Applications : Systems like Cassandra & Zookeeper, and other distributed systems use it for failure detection.

## Failover Mechanisms
### Circuit Breaker Pattern

![](../../hld/beginner/assets/Pasted%20image%2020251221205200.png)

* Prevents cascading failures by temporarily stopping requests to failed service.

````python
# Sample Example Python Code
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Blocking requests
    HALF_OPEN = "half_open" # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
````

### Graceful Degration

* provide reduced functionality when some servers are unavailable

````python
class GracefulDegradationBalancer:
    def __init__(self, primary_servers, fallback_servers):
        self.primary_servers = [s for s in primary_servers if self.is_healthy(s)]
        self.fallback_servers = [s for s in fallback_servers if self.is_healthy(s)]
    
    def get_server(self):
        if self.primary_servers:
            return self.select_from_primary()
        elif self.fallback_servers:
            return self.select_from_fallback()
        else:
            raise Exception("No healthy servers available")
    
    def select_from_primary(self):
        # Use preferred load balancing algorithm
        return self.round_robin_select(self.primary_servers)
    
    def select_from_fallback(self):
        # Might use simpler logic for degraded mode
        return self.fallback_servers[0]
````

## Other Topics on Load Balancer
### Popular Load Balancer Solutions

Hardware Load Balancers

- **F5 BIG-IP**: Enterprise-grade with advanced features
- **Citrix NetScaler**: High-performance application delivery
- **A10 Networks**: Scalable application delivery controllers

Software Load Balancers

- **NGINX**: Popular reverse proxy and load balancer
- **HAProxy**: High-performance TCP/HTTP load balancer
- **Apache HTTP Server**: Basic load balancing capabilities

Cloud Load Balancers

- **AWS ELB/ALB/NLB**: Elastic Load Balancing services
- **Google Cloud Load Balancer**: Global and regional options
- **Azure Load Balancer**: Layer 4 and Layer 7 options

### Load Balancer Considerations

Performance Requirements

* High Throughput  -> Layer 4, Active-Active
* Low Latency -> Layer 4, Least Connections
* Content-Based Routing -> Layer 7, Weighted Round Robin

Infrastructure Complexity

* Simple -> Round Robin, Active-Passive
* Microservices -> Layer 7, Hash-Based Routing
* Multi-Region -> Active-Active with health checks

Operation Requirements

* Session Persistence -> IP Hash or Sticky Session
* Rolling Deployments -> Weighted algorithms with health checks
* Disaster Recovery -> Active-Passive with automated failovers

### Best Practices

1. **Always implement comprehensive health checks** - Both active and passive monitoring
2. **Use circuit breakers** - Prevent cascading failures in distributed systems
3. **Monitor key metrics** - Response times, error rates, server utilization
4. **Plan for failover scenarios** - Test failover procedures regularly
5. **Consider geographic distribution** - Use multiple load balancers across regions
6. **Implement gradual rollouts** - Use weighted routing for safe deployments
7. **Log and audit** - Track routing decisions for troubleshooting
8. **Security considerations** - Implement DDoS protection and rate limiting

### Further Reading

- [AWS Application Load Balancer Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/)
- [NGINX Load Balancing Guide](https://nginx.org/en/docs/http/load_balancing.html)
- [HAProxy Configuration Manual](http://cbonte.github.io/haproxy-dconv/)
- [Google Cloud Load Balancing Concepts](https://cloud.google.com/load-balancing/docs/load-balancing-overview)

Advanced Load Balancing Features

* Session Persistence (Sticky Sessions)
* Geo-based Load Balancing
