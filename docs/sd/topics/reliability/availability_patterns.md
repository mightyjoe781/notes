# High Availability Patterns

*Ensuring systems remain operational and accessible with minimal downtime, typically measured in "nines" of uptime.*

## Overview

High Availability (HA) is about designing systems that remain operational despite failures. It's measured by uptime percentages and directly impacts user experience and business revenue.

### Availability Levels (SLA Standards)

- **99% (Basic)**: 3.65 days downtime/year - Acceptable for internal tools
- **99.9% (Standard)**: 8.77 hours downtime/year - Typical web applications
- **99.95% (High)**: 4.38 hours downtime/year - E-commerce, SaaS platforms
- **99.99% (Very High)**: 52.6 minutes downtime/year - Banking, critical systems
- **99.999% (Extreme)**: 5.26 minutes downtime/year - Emergency services, trading

### Key Principles

1. **Eliminate Single Points of Failure**: Every component should have redundancy
2. **Detect Failures Quickly**: Fast detection enables rapid response
3. **Automate Recovery**: Human intervention introduces delays
4. **Design for Graceful Degradation**: Partial functionality > complete failure
5. **Test Everything**: Regular failure testing validates HA design

### Cost vs Availability Trade-off

```
Availability Level | Relative Cost | Use Cases
99%                | 1x            | Internal tools, development
99.9%              | 3x            | Standard web apps, blogs
99.99%             | 10x           | E-commerce, business apps
99.999%            | 50x+          | Financial, emergency systems
```

------

## Active-Passive vs Active-Active

### Active-Passive Configuration

**Definition**: One primary system handles all traffic while backup systems remain on standby, ready to take over during failures.

#### How It Works

1. **Primary** handles all requests and data writes
2. **Passive** systems monitor primary health
3. **Failover** occurs when primary fails
4. **Failback** may occur when primary recovers

#### Types of Active-Passive

**Cold Standby**:

- Backup systems are powered off or minimal state
- **Recovery Time**: 10-30 minutes
- **Cost**: Lowest
- **Use Case**: Non-critical systems, development environments

**Warm Standby**:

- Backup systems running but not processing traffic
- **Recovery Time**: 1-5 minutes
- **Cost**: Medium
- **Use Case**: Standard business applications

**Hot Standby**:

- Backup systems fully operational, synchronized
- **Recovery Time**: 30 seconds - 2 minutes
- **Cost**: High
- **Use Case**: Critical business systems

#### Implementation Pattern

```
Load Balancer Configuration:
Primary: Server-A (Weight: 100, Health Check: ON)
Backup:  Server-B (Weight: 0, Health Check: ON)

Failover Logic:
if (primary.health_check == FAIL) {
    backup.weight = 100
    primary.weight = 0
    alert_operations_team()
}
```

#### Benefits of Active-Passive

- **Simple Architecture**: Easy to understand and implement
- **Data Consistency**: Single write source eliminates conflicts
- **Cost Effective**: Only one system actively consuming resources
- **Predictable Performance**: Known capacity limitations

#### Drawbacks of Active-Passive

- **Resource Waste**: Passive systems idle most of the time
- **Capacity Limitations**: Total capacity limited to single system
- **Failover Time**: Always some downtime during transition
- **Geographic Limitations**: Typically within same data center

### Active-Active Configuration

**Definition**: Multiple systems simultaneously handle traffic and share the load, providing both high availability and improved performance.

#### How It Works

1. **Multiple active** systems process requests simultaneously
2. **Load balancer** distributes traffic across all systems
3. **Automatic failover** when any system fails
4. **Seamless scaling** by adding more active systems

#### Types of Active-Active

**Shared Nothing Architecture**:

```
User Requests → Load Balancer → [Server-A, Server-B, Server-C]
                                      ↓         ↓         ↓
                                  Database  Database  Database
                                  Shard-1   Shard-2   Shard-3
```

**Shared Database Architecture**:

```
User Requests → Load Balancer → [Server-A, Server-B, Server-C]
                                      ↓         ↓         ↓
                                    Shared Database Cluster
```

**Geographic Active-Active**:

```
US Users → US Data Center (Active)
EU Users → EU Data Center (Active)
APAC Users → APAC Data Center (Active)
```

#### Implementation Challenges

**Data Consistency**:

- **Read Replicas**: Eventually consistent reads
- **Write Conflicts**: Requires conflict resolution strategies
- **Distributed Transactions**: Complex coordination needed

```python
# Example: Conflict Resolution Strategy
def resolve_write_conflict(local_data, remote_data):
    if local_data.timestamp > remote_data.timestamp:
        return local_data  # Last-write-wins
    elif local_data.version > remote_data.version:
        return local_data  # Version-based resolution
    else:
        return merge_data(local_data, remote_data)  # Custom merge
```

**Session Management**:

- **Sticky Sessions**: Route user to same server
- **Shared Session Storage**: Redis/Memcached for session data
- **Stateless Design**: No server-side session dependencies

#### Benefits of Active-Active

- **No Wasted Resources**: All systems actively serving traffic
- **Better Performance**: Load distributed across multiple systems
- **Instant Failover**: No downtime when systems fail
- **Horizontal Scaling**: Easy to add capacity
- **Geographic Distribution**: Closer to users worldwide

#### Drawbacks of Active-Active

- **Complex Architecture**: Harder to design and maintain
- **Data Synchronization**: Consistency challenges
- **Higher Costs**: All systems must be fully operational
- **Monitoring Complexity**: More moving parts to track

### Choosing Between Active-Passive and Active-Active

| Factor                 | Active-Passive              | Active-Active             |
| ---------------------- | --------------------------- | ------------------------- |
| **Complexity**         | Low                         | High                      |
| **Cost**               | Lower                       | Higher                    |
| **Performance**        | Limited by single system    | Better load distribution  |
| **Failover Time**      | 30s - 5min                  | Instant                   |
| **Data Consistency**   | Simple                      | Complex                   |
| **Geographic Support** | Limited                     | Excellent                 |
| **Best For**           | Simple apps, cost-sensitive | High-traffic, global apps |

------

## Geographic Distribution

### What is Geographic Distribution?

Deploying systems across multiple geographic locations to improve availability, performance, and disaster resilience.

### Geographic Distribution Strategies

#### 1 Multi-Region Deployment

**Regional Architecture Pattern**:

```
Global DNS (Route 53, CloudFlare)
├── US-East Region (Primary)
│   ├── Load Balancers
│   ├── Application Servers  
│   ├── Database (Master)
│   └── Cache Cluster
├── US-West Region (Secondary)
│   ├── Load Balancers
│   ├── Application Servers
│   ├── Database (Read Replica)
│   └── Cache Cluster
└── EU-West Region (Secondary)
    ├── Load Balancers
    ├── Application Servers
    ├── Database (Read Replica)
    └── Cache Cluster
```

**Benefits**:

- **Reduced Latency**: Users connect to nearest region
- **Disaster Recovery**: Natural protection against regional outages
- **Compliance**: Data residency requirements
- **Load Distribution**: Traffic spread across regions

#### 2 Content Delivery Networks (CDN)

**CDN Architecture**:

```
Origin Servers (US-East)
       ↓
Global CDN Edge Locations
├── US-West: Static assets, API cache
├── Europe: Static assets, API cache  
├── Asia: Static assets, API cache
└── Australia: Static assets, API cache
```

**What to Cache**:

- ✅ Static assets (images, CSS, JS)
- ✅ API responses (with TTL)
- ✅ Video/media content
- ❌ User-specific data
- ❌ Real-time data
- ❌ Sensitive information

#### 3 DNS-Based Geographic Routing

**Routing Strategies**:

**Latency-Based Routing**:

```python
# Route user to lowest latency region
user_location = get_user_location(ip_address)
regions = [
    {"name": "us-east", "latency": measure_latency(user_location, "us-east")},
    {"name": "eu-west", "latency": measure_latency(user_location, "eu-west")},
    {"name": "ap-south", "latency": measure_latency(user_location, "ap-south")}
]
best_region = min(regions, key=lambda r: r["latency"])
```

**Geolocation-Based Routing**:

```
User Location → Target Region
US/Canada    → us-east-1
Europe       → eu-west-1  
Asia Pacific → ap-southeast-1
South America → sa-east-1
```

**Health Check Routing**:

```
if (region.health_check == "HEALTHY"):
    route_to_region(region)
else:
    route_to_failover_region(region.failover)
```

### 4 Data Replication Across Regions

#### Cross-Region Database Strategies

**Master-Slave Cross-Region**:

```
US-East (Master)     →  Async Repl  →  EU-West (Slave)
US-East (Master)     →  Async Repl  →  APAC (Slave)
```

- **Pros**: Simple, consistent writes
- **Cons**: Cross-region latency for writes

**Multi-Master Cross-Region**:

```
US-East (Master) ←→ Sync Repl ←→ EU-West (Master)
       ↓                              ↓
   Async Repl                    Async Repl
       ↓                              ↓
   APAC (Slave)                  LatAm (Slave)
```

- **Pros**: Low write latency in multiple regions
- **Cons**: Conflict resolution complexity

**Event Sourcing + CQRS**:

```
Command Side (Writes):
Region A → Event Stream → Replicated to All Regions

Query Side (Reads):  
Region A, B, C → Local Read Models (Eventually Consistent)
```

### Geographic Distribution Challenges

#### 5 Network Partitions

**Split-Brain Problem**: Regions can't communicate but both remain active

**Solutions**:

- **Quorum Systems**: Require majority consensus
- **Witness/Arbiter**: Third region breaks ties
- **Graceful Degradation**: Accept reduced functionality

#### 6 Data Consistency Across Regions

**Consistency Models**:

```
Strong Consistency    → Synchronous replication → High latency
Eventual Consistency  → Asynchronous replication → Low latency  
Session Consistency   → Read your own writes → Good UX
```

**Implementation Pattern**:

```python
def write_with_consistency_level(data, consistency="eventual"):
    if consistency == "strong":
        return sync_write_to_all_regions(data)  # Slow but consistent
    elif consistency == "session":
        return write_with_session_affinity(data)  # Good UX
    else:
        return async_write_with_eventual_consistency(data)  # Fast
```

------

## Disaster Recovery

### What is Disaster Recovery?

The process of preparing for and recovering from catastrophic events that could cause extended system outages.

### Disaster Recovery Metrics

**Recovery Time Objective (RTO)**: Maximum acceptable downtime

- **Tier 1**: RTO < 1 hour (Critical systems)
- **Tier 2**: RTO < 4 hours (Important systems)
- **Tier 3**: RTO < 24 hours (Standard systems)
- **Tier 4**: RTO < 72 hours (Non-critical systems)

**Recovery Point Objective (RPO)**: Maximum acceptable data loss

- **RPO = 0**: No data loss acceptable (sync replication)
- **RPO < 15 min**: Minimal data loss (frequent backups)
- **RPO < 1 hour**: Acceptable for most businesses
- **RPO < 24 hours**: Acceptable for non-critical data

### Disaster Recovery Strategies

#### Cold Site Recovery

**Definition**: Backup facility with basic infrastructure but no active systems.

**Characteristics**:

- **RTO**: 24-72 hours
- **RPO**: 4-24 hours
- **Cost**: Lowest
- **Complexity**: Low

**Process**:

1. Declare disaster
2. Ship/restore equipment to cold site
3. Restore data from backups
4. Redirect traffic to cold site

#### Warm Site Recovery

**Definition**: Backup facility with partial infrastructure and recent data.

**Characteristics**:

- **RTO**: 2-12 hours
- **RPO**: 1-4 hours
- **Cost**: Medium
- **Complexity**: Medium

**Process**:

1. Detect disaster
2. Complete system setup at warm site
3. Restore latest data backups
4. Test systems and redirect traffic

#### Hot Site Recovery

**Definition**: Fully operational backup facility with real-time or near-real-time data.

**Characteristics**:

- **RTO**: 15 minutes - 2 hours
- **RPO**: 0-15 minutes
- **Cost**: Highest
- **Complexity**: High

**Process**:

1. Automatic failover triggers
2. DNS switches to hot site
3. Verify system operation
4. Monitor and adjust capacity

### Backup Strategies

#### The 3-2-1 Backup Rule

- **3** copies of critical data
- **2** different storage media types
- **1** offsite/cloud backup

#### Backup Types and Schedule

**Full Backup** (Weekly):

```
Sunday: Full backup of entire system
Size: 100% of data
Time: 4-8 hours
```

**Incremental Backup** (Daily):

```
Monday-Saturday: Only changed data since last backup
Size: 5-15% of data  
Time: 30-60 minutes
```

**Differential Backup** (Alternative):

```
Daily: All changes since last full backup
Size: Grows throughout week
Time: 1-3 hours
```

#### Cloud Backup Strategy

```python
# Multi-tier backup strategy
backup_tiers = {
    "hot": {
        "location": "primary_region_ssd",
        "retention": "7_days",
        "rto": "minutes",
        "cost": "high"
    },
    "warm": {
        "location": "secondary_region_hdd", 
        "retention": "30_days",
        "rto": "hours",
        "cost": "medium"
    },
    "cold": {
        "location": "glacier_storage",
        "retention": "7_years", 
        "rto": "hours_to_days",
        "cost": "low"
    }
}
```

### Database Disaster Recovery

#### Database Backup Strategies

**Point-in-Time Recovery**:

```
Daily Full Backup + Transaction Log Backups
Recovery Process:
1. Restore latest full backup
2. Apply transaction logs up to desired point
3. Verify data integrity
```

**Cross-Region Database Replication**:

```
Primary Region:
├── Master Database (Read/Write)
├── Local Read Replicas (Read Only)
└── Backup to S3 (Daily)

DR Region:  
├── Cross-Region Read Replica (Read Only)
├── Automated Promotion Process
└── Independent Backup System
```

#### Database Failover Process

```python
def database_failover_process():
    steps = [
        "1. Stop application writes to primary",
        "2. Verify replica is caught up", 
        "3. Promote replica to master",
        "4. Update application connection strings",
        "5. Resume application traffic",
        "6. Monitor for issues"
    ]
    
    # Automated failover for RTO < 5 minutes
    # Manual failover for complex scenarios
```

### Application-Level Disaster Recovery

#### Stateless Application Recovery

```
DR Deployment Process:
1. Infrastructure as Code → Deploy in DR region
2. Container Images → Pull from registry  
3. Configuration → Environment-specific configs
4. Load Balancer → Update DNS to DR region
5. Monitoring → Deploy monitoring stack
```

#### Stateful Application Recovery

```
Additional Steps for Stateful Apps:
1. Data Recovery → Restore from backups
2. Session Recovery → Restore user sessions  
3. Cache Warming → Pre-populate caches
4. Gradual Traffic → Slowly increase load
5. Validation → Verify application functionality
```

### Testing Disaster Recovery

#### Types of DR Testing

**Tabletop Exercises** (Monthly):

- Walk through DR procedures on paper
- Identify gaps in documentation
- Train team on processes

**Partial Testing** (Quarterly):

- Test specific components
- Restore backups to test environment
- Validate RTO/RPO metrics

**Full DR Testing** (Annually):

- Complete failover to DR site
- Run production workload
- Measure actual RTO/RPO

#### DR Testing Checklist

```
Pre-Test:
□ Document current system state
□ Notify stakeholders of test
□ Prepare rollback procedures
□ Set up monitoring and logging

During Test:
□ Follow DR procedures exactly
□ Document all steps and timing
□ Note any deviations or issues  
□ Measure RTO/RPO achievement

Post-Test:
□ Restore to normal operations
□ Document lessons learned
□ Update DR procedures
□ Schedule follow-up improvements
```

------

## Implementation Best Practices

### Monitoring and Alerting for HA

#### Health Check Design

```
Service Health Checks:
├── Shallow (< 100ms)
│   ├── Process running?
│   ├── Port responding?
│   └── Basic connectivity?
├── Deep (< 5s)
│   ├── Database connectivity?
│   ├── External dependencies?
│   └── Critical workflows?
└── Business Logic (< 30s)
    ├── End-to-end transaction?
    ├── Data consistency checks?
    └── Performance benchmarks?
```

#### Alerting Strategy

```
Alert Severity Levels:
Critical (Page immediately):
├── Service completely down
├── RTO/RPO SLA breached  
├── Security incident
└── Data corruption detected

Warning (Investigate within 1 hour):
├── Degraded performance
├── Failover events
├── High error rates
└── Capacity approaching limits

Info (Review during business hours):  
├── Planned maintenance
├── Backup completions
├── Performance trends
└── Capacity planning alerts
```

### Automation for High Availability

#### Automated Failover Decision Tree

```python
def automated_failover_logic():
    if primary_health_check_fails():
        if consecutive_failures >= FAILURE_THRESHOLD:
            if secondary_is_healthy():
                trigger_failover()
                alert_operations_team("Automated failover initiated")
            else:
                alert_operations_team("CRITICAL: Both primary and secondary failed")
        else:
            log_warning("Primary health check failed, monitoring...")
```

#### Infrastructure as Code for DR

```yaml
# Example: Terraform for multi-region deployment
regions:
  primary: us-east-1
  secondary: us-west-2
  
resources:
  - load_balancers: 2 (one per region)
  - app_servers: 6 (3 per region)  
  - databases: master/replica across regions
  - monitoring: CloudWatch + DataDog
  - dns: Route53 with health checks
```

### Cost Optimization for HA

#### Right-sizing HA Infrastructure

```
Cost Optimization Strategies:
├── Reserved Instances for steady-state capacity
├── Spot Instances for non-critical workloads
├── Auto-scaling for variable loads
├── Cold storage for long-term backups
└── Cross-region data transfer optimization
```

#### HA Cost Analysis

```
Monthly HA Costs Breakdown:
├── Infrastructure: 60-70%
│   ├── Servers/containers
│   ├── Load balancers  
│   └── Storage
├── Data Transfer: 15-25%
│   ├── Cross-region replication
│   └── CDN costs
├── Monitoring/Tools: 10-15%
│   ├── APM tools
│   └── Log aggregation
└── Human Resources: 5-10%
    ├── On-call engineers
    └── DR testing time
```

------

## Choosing the Right HA Pattern

### Decision Framework

| Business Requirement   | Recommended Pattern                    | Typical RTO  | Typical RPO |
| ---------------------- | -------------------------------------- | ------------ | ----------- |
| **Personal Website**   | Single region + backups                | 2-4 hours    | 24 hours    |
| **Small Business App** | Active-Passive in single region        | 5-15 minutes | 1 hour      |
| **E-commerce Site**    | Active-Active + CDN                    | 1-5 minutes  | 15 minutes  |
| **Financial Trading**  | Multi-region Active-Active             | < 30 seconds | < 1 minute  |
| **Global SaaS**        | Multi-region + Geographic distribution | < 1 minute   | < 5 minutes |

### Architecture Evolution Path

**Phase 1: Basic HA**

- Load balancer + multiple app servers
- Database with read replicas
- Basic monitoring and alerts

**Phase 2: Regional HA**

- Active-Passive across availability zones
- Automated failover
- Regular backup testing

**Phase 3: Geographic HA**

- Multi-region deployment
- CDN for global performance
- Cross-region data replication

**Phase 4: Advanced HA**

- Active-Active across regions
- Chaos engineering
- Advanced disaster recovery automation

------

## Conclusion

### Key Takeaways

1. **Start Simple**: Begin with single-region HA, then expand geographically
2. **Measure Everything**: Track RTO, RPO, and availability metrics continuously
3. **Test Regularly**: Disaster recovery plans are worthless without testing
4. **Automate Recovery**: Human intervention introduces delays and errors
5. **Balance Cost vs Requirements**: Higher availability comes with exponential costs

### Common Pitfalls to Avoid

- **Over-engineering**: Building for 99.999% when 99.9% is sufficient
- **Ignoring Network Partitions**: Assuming networks are always reliable
- **Untested DR Plans**: Plans that work on paper but fail in practice
- **Single Region Dependencies**: Hidden dependencies that aren't geographically distributed
- **Manual Processes**: Relying on human intervention during outages

### Implementation Checklist

- [ ] Define RTO and RPO requirements for each system component
- [ ] Identify and eliminate single points of failure
- [ ] Implement appropriate redundancy (Active-Passive vs Active-Active)
- [ ] Set up geographic distribution based on user base
- [ ] Create comprehensive disaster recovery procedures
- [ ] Implement automated failover where possible
- [ ] Set up monitoring, alerting, and health checks
- [ ] Schedule regular DR testing and improvements
- [ ] Document all procedures and train the team
- [ ] Plan for cost optimization and capacity management

Remember: High availability is not just about technology—it requires process, people, and continuous improvement to be truly effective.