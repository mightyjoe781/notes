# Load Balancers

**What are Load Balancers**

Load balancers are critical components in distributed systems that distribute incoming requests across multiple backend servers. 

They act as a **single point of contact** for clients while hiding the complexity of multiple servers behind them.

**Key Benefits**

- **Scalability** - Enable horizontal scaling by adding/removing servers without client knowledge
- **High Availability** - Prevent single points of failure by routing around unhealthy servers
- **Performance** - Distribute load to prevent server overload and reduce response times
- **Flexibility** - Allow maintenance and updates without service interruption

**Request-Response Flow**

1. Client sends request to load balancer's static IP/DNS
2. Load balancer selects an appropriate backend server using configured algorithm
3. Load balancer forwards request to selected server
4. Backend server processes request and returns response
5. Load balancer forwards response back to client

(todo: put a digram here for load balancer)

### Layer 4 vs Layer 7 Load Balancing

**Layer 4 (Transport Layer) Load Balancing**

- operates on TCP/UDP Level - makes routing based on IP Addresses and Port Numbers only
- Use Cases
  - High-throughput applications requiring minimal latency
  - Non-HTTP protocols (databases, gaming servers, VoIP)
  - When you need maximum performance and don't need content-based routing

**Layer 7 (Application Layer) Load Balancing**

* Operates on HTTP/HTTPs level - can inspect and make decision based on application content
* Use Cases
  * Microservice Architecture requiring path based routing
  * A/B testing and canary deployments
  * API Gateways requiring authentication and rate limitting
  * Content-Based Routing

**Comparison Table**

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

### Weighted Round Robin

### Least Connections

### Least Response Time

### IP Hash

### Consistent Hashing



## Active-Active vs Active-Passive

### Active-Active Configuration

### Active-Passive Configuration





## Health Checks

### HTTP Health Checks

### TCP Health Checks

### Application-Level Health Checks

## Failover Mechanisms

### Automatic Failover

### Circuit Breaker Pattern

## Advanced Load Balancing Features

### Session Persistence (Sticky Sessions)

### Geo-based Load Balancing

## Popular Load Balancer Solutions

### 