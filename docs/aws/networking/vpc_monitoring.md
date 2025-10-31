# VPC traffic Monitoring, Troubleshooting and Analysis

## Traffic Monitoring

### VPC Flow Logs

- Capture information about IP traffic going in/out of your interfaces:
    - VPC Flow Logs
    - Subnet Flow Logs
    - Elastic Network Interface Flow Logs
- Helps monitor & troubleshoot connectivity issues
- Flow logs data can go to S3/CloudWatch Logs/ Kinesis Data Firehose
- Captures network information from AWS managed interface too : ELB, RDS, ElastiCache, Redshift, Amazon WorkSpaces
- There is no impact to network performance for enabling VPC flow logs.

### Publishing VPC flow logs

![](assets/Pasted%20image%2020251025204547.png)

### VPC Flow Logs default format

- `<version> <account-id> <interface-id> <srcaddr> <dstaddr> <srcport> <dstport> <protocol> <packets> <bytes> <start> <end> <action> <log-status>`
- Supported flow logs version 2, 3, 4, 5. Default is 2
- Action : Success/failure due to SG/NACL
- can be used for analytics on usage patterns, or malicious behaviour
- Can be customized

Examples of Log Query

```txt
# find out rejects on a particular ENI
stats sum(packets) as packetsTransferred by srcAddr, dstAddr
| sort packetsTransferred desc
| limit 15

# list of IP addresses trying to connect to specific IP or CIDR
fields @timestamp, srcAddr, dstAddr
| sort @timestamp desc
| limit 5
| filter srcAddr like “xxx.xxx.xxx.xxx"
```

#### How to troubleshoot SG vs NACL issue ?

- Action Field can help with this
- For incoming requests
    - Inbound Reject : NACL or SG
    - Inbound Accept : outbound REJECT: NACL
- For outgoing request
    - Outbound REJECT: NACL or SG
    - Outbound ACCEPT: inbound REJECT: NACL

### Flow Logs limitation

- Amazon VPC Flow Logs do not record
    - To and from VPC-native DNS services
    - Amazon EC2 metadata service
    - Dynamic Host Configuration Protocol (DHCP) services
    - Windows license activation server

### Other traditional Tools for Network Monitoring

- Packet Capture
    - Wireshark
- traceroute
- telnet
- nslookup
- ping
    - NOTE: ping uses ICMP
    - ICMP should be allowed explicitly through Security Groups

## Traffic Mirroring

- Copy network traffic from an elastic network interface of Amazon EC2 instances
- Send the traffic to out-of-band security and monitoring appliances for Content inspection or threat monitoring or for troubleshooting
- How to set up Traffic Mirroring (via AWS VPC console)
    - Create the Mirror Target
    - Define the Traffic Filter
    - Create Mirror Session

### VPC Traffic Mirroring - ENI as Target

![](assets/Pasted%20image%2020251025210153.png)
### VPC Traffic Mirroring - NLB as Target

![](assets/Pasted%20image%2020251025210205.png)

### VPC Traffic Mirroring Filters

![](assets/Pasted%20image%2020251025210254.png)

### Important Notes

- Mirrors the traffic flowing in/out of VPC and routes it to network analysis tools to detect the potential network & security anomalies
- Mirror source is ENI
- Mirror target could be another ENI or Network Load Balancer (UDP - 4789)
- Mirror Filter – To capture only the traffic you are interesting in
    - Filter the traffic by specifying Protocols, Source/Destination port ranges, and CIDR Blocks
    - Define rules (numbered) to send the traffic to respective destination
- The traffic mirror source and the traffic mirror target (monitoring appliance) can be in the same VPC or they can be in a different VPC connected via intra- Region VPC peering or a transit gateway
- Source and Destination can be in different AWS accounts

## VPC Traffic Analysis

![](assets/Pasted%20image%2020251025233016.png)
### VPC Reachability Analyzer

![](assets/Pasted%20image%2020251025233300.png)

- Connectivity testing between the source resource and a destination resource
- Produces hop-by-hop details of the virtual network path
- Points out the blocking components when traffic is not reachable
- Does not send real packets. It uses network configurations to find out if network is reachable

Use Cases

- Troubleshoot connectivity issues by network configuration
- Automate the verification of connectivity after network configuration changes

#### VPC Reachability Analyzer output

![](assets/Pasted%20image%2020251025233341.png)
### Network Access Analyzer

![](assets/Pasted%20image%2020251025233453.png)

- Identify un-intended network access to the AWS resources
    - Isolated network segments
    - Internet accessibility
    - Trusted network paths
    - Trusted network access
- Specify network access scope and analyze if it meets your compliance.