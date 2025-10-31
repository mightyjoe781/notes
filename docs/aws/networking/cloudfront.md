# AWS CloudFront

## Overview

- Content Delivery Network (CDN)
- Improves read performance, content is cached at the edge
- 225+ Point of Presence globally (215+ Edge Locations & 13 Regional Edge Cache)
- Protect again Network & Application layer attacks like DDOS
- Integration with AWS Shield, AWS WAF, and Route 53
- Can expose external HTTPS and can talk to internal HTTP Backends
- Supports Websocket Protocol

### Edge Locations & Regional Edge Caches

![](assets/Pasted%20image%2020251029142459.png)

Edge Locations

- Serve content quickly directly to users
- Cache more popular content

Regional Edge caches

- serve content to edge location
- cache less popular content that might suddenly find popularity
- Larger cache than Edge location (objects remain longer)
- Improve performance, reduce load on your origins
- Dynamic content doesn't pass through it (directly to origin)

### CloudFront Components

- Distribution
    - Identified by a domain (e.g. abcdef.cloudfront.net)
    - You can use this distribution domain name to access the website
    - You can also use Route53 CNAME (non-root) or Alias (root & non-root) which points to distributions domain name
- Origin
    - where actual content resides (server, s3 buckets, etc)
- Cache Behavior
    - Cache Configurations (e.g. Object Expiration, TTL, Cache invalidation)

## CloudFront - Origins

- S3 Bucket
    - for distributing files
    - for uploading files to S3 (using cloudfront as ingress)
    - Enhanced security with CloudFront Origin Access Control (OAC)
- Media Store Container & Media Package Endpoint
    - To deliver video on demand (VDO) or live streaming video using AWS Media Services
- VPC Origin
    - for applications hosted in VPC private subnets
    - ALB/NLB/EC2 Instances
- Custom Origin (HTTP)
    - API Gateway
    - S3 bucket configured as a website
    - Any HTTP backend you want
### CloudFront Origins - S3 as a origin

![](assets/Pasted%20image%2020251029142954.png)

### CloudFront - ALB or EC2 as an origin : Using VPC Origins

![](assets/Pasted%20image%2020251029143111.png)

- Allows you to deliver content from your applications hosted in your VPC private subnets (no need to expose them on the Internet)
- Deliver traffic to private:
    - ALB
    - NLB
    - EC2 Instances

NOTE:

![](assets/Pasted%20image%2020251029143224.png)

### CloudFront - Multiple Origin

![](assets/Pasted%20image%2020251029143333.png)

- To route to different kind of origins based on the content type
- Based on path pattern:
    - `/images/*`
    - `/api/*`
    - `/*`

### CloudFront - Origin Groups

- To increase high-availability and do failover
- Origin Group: one primary and one secondary origin
- If the primary origin fails, the second one is used

![](assets/Pasted%20image%2020251029144558.png)

## CloudFront - Origin Custom Headers

 - Add custom headers to requests CloudFront sends to your origin
 - Can be customized for each origin
 - Supports custom and S3 origins
 - Use cases:
     - Identify which requests coming from CloudFront or a particular distribution
     - Control access to content (configure origin to respond to requests only when they include a custom header)
 - Specific HTTP headers added based on the viewer request
     - Viewer’s Device Type Headers (User-Agent)
     - Viewer’s Location Headers (IP)
     - Viewer’s Request Protocol & HTTP Version

## CloudFront Origin Security

![](assets/Pasted%20image%2020251029144954.png)

- Prevent direct access to files in your S3 buckets (only access through CloudFront)
- First, create an Origin Access Control and associate it with your distribution (previously known as OAI)
- Second, edit your S3 bucket policy so that only OAC has permission

### CloudFront - restrict Access to Application ~ Load Balancers & Custom Origins

- Prevent direct access to your ALB or Custom Origins (only access through CloudFront)
- First, configure CloudFront to add a Custom HTTP Header to requests it sends to the ALB
- Second, configure the ALB to only forward requests that contain that Custom HTTP Header
- Keep the custom header name and value secret!

![](assets/Pasted%20image%2020251029145103.png)

### Using AWS WAF & Security Manager

![](assets/Pasted%20image%2020251029145139.png)

## CloudFront & HTTPS

- Viewer Protocol Policy
    - HTTP & HTTPS
    - Redirect HTTP to HTTPS
    - HTTPS Only
- Origin Protocol Policy (HTTP or S3)
    - HTTP Only (default for S3 static sites)
    - HTTPS Only
    - Or Match Viewer

NOTE:

- S3 bucket `static websites` doesn't support HTTPS
- You must use a valid SSL/TLS certificate between CloudFront and your origin (can't use self-signed certs)

### Alternate Domain Names

![](assets/Pasted%20image%2020251029145807.png)

- Use your own domain name instead of the domain assigned by CloudFront to your distribution
- You must have a valid SSL/TLS Certificate from an authorized CA that covers:
    - Your domain name
    - All Alternate Domain Names you added to your distribution
- You can use wildcards in Alternate Domain Names (e.g., `*.example.com`)

### CloudFront SSL Certs

- Default CloudFront Certificate (`*.cloudfront.net`)
- Custom SSL Certificate
    - When using your domain name
    - CloudFront can serve HTTPS requests using
        - (Server Name Indication) SNI
        - Dedicated IP Address in Each Edge Location (expensive)
    - You can use
        - Certs provided by ACM
        - 3rd party certificates uploaded to ACM or IAM certs store
    - Certs must be created/imported in US East (N. Virginia) Region
- Ability to specify a Security Policy (min. SSL/TLS protocol & ciphers to use)

### End-to-End Encryption : CloudFront, ALB, EC2

- CloudFront
    - Origin protocol policy: HTTPS Only
    - Install an SSL / TLS certificate on your custom origin
    - The origin certificate must include either the Origin domain field (configured in CloudFront) or the domain in the “Host” header if it’s forwarded to Origin
    - Does not work with self-signed certificate
- Application Load Balancer
    - Use a certificate provided by AWS Certificate Manager or imported into ACM
- EC2 Instance
    - ACM is not supported on EC2
    - Can use a third-party SSL certificate (any domain name)
    - Can use a self-signed certificate (ALB does not verify the certificate itself)

## CloudFront Geo Restrictions

### CloudFront - Restrict Content Geographically

- Prevent users in specific locations from accessing your content/distribution
- CloudFront Geo Restriction
    - Restrict access at the country level (country determined using a 3rd party GeoIP database)
    - Allow list – allow access only if is from one of the approved countries
    - Block list – prevent access if users in one of the countries on a blacklist of banned countries
    - Applied to an entire CloudFront distribution
- Use case: Copyright Laws to control access to content

## CloudFront Functions & Lambda@Edge
### CloudFront - Customization At The Edge

- Many modern applications execute some form of the logic at the edge
- Edge Function:
    - A code that you write and attach to CloudFront distributions
    - Runs close to your users to minimize latency
    - Doesn’t have any cache, only to change requests/responses
    - CloudFront provides two types: CloudFront Functions & Lambda@Edge
- Use cases:
    - Manipulate HTTP requests and responses
    - Implement request filtering before reaching your application
    - User authentication and authorization
    - Generate HTTP responses at the edge
    - A/B Testing
    - Bot mitigation at the edge
- You don’t have to manage any servers, deployed globally

![](assets/Pasted%20image%2020251029150849.png)
### CloudFront Functions

![](assets/Pasted%20image%2020251029151032.png)

- Lightweight functions written in JavaScript
- For high-scale, latency sensitive CDN customizations
- Sub-ms startup times, millions or requests/second
- RuN at Edge Locations
- Process-based Isolation
- Used to change Viewer requests and responses
- Native feature

### Lambda@Edge

- Lambda functions written in NodeJS or Python
- Scales to 1000s of requests/second
- Runs at the nearest Regional Edge Cache
- VM-based isolation
- Used to change CloudFront requests and responses:
    - Viewer Request – after CloudFront receives a request from a viewer
    - Origin Request – before CloudFront forwards the request to the origin
    - Origin Response – after CloudFront receives the response from the origin
    - Viewer Response – before CloudFront forwards the response to the viewer
- Author your functions in one AWS Region (us-east-1), then CloudFront replicates to its locations

Example using CloudFront Functions with Lambda@Edge

![](assets/Pasted%20image%2020251029151153.png)

Example using Lambda@Edge only

![](assets/Pasted%20image%2020251029151302.png)

## AWS Global Accelerator

Problem : An application is deployed in a region, but consumers are present everywhere in the globe.

![](assets/Pasted%20image%2020251029153120.png)

- Unicast IP : one server holds one IP address
- Anycast IP : all servers hold the same IP address and client is routed to nearest one

- Leverage the AWS internal network to route to your application.
- 2 Anycast IP are created for your application, and send traffic directly to Edge location.
- Edge locations send the traffic to your application
- Works with Elastic IP, EC2, ALB, NLB, public or private
- Consistent Performance
    - Intelligent routing to lowest latency and fast regional failover
    - No issue with client cache
    - Internal AWS Network
- Security (DDOS Protections)
- Health Checks

![](assets/Pasted%20image%2020251029153341.png)

- CloudFront
    - Improves performance for both cacheable content (such as images and videos)
    - Dynamic content (such as API acceleration and dynamic site delivery)
    - Content is served at the edge
- Global Accelerator
    - Improves performance for a wide range of applications over TCP or UDP
    - Proxying packets at the edge to applications running in one or more AWS Regions.
    - Good fit for non-HTTP use cases, such as gaming (UDP), IoT (MQTT), or Voice over IP
    - Good for HTTP use cases that require static IP addresses
    - Good for HTTP use cases that required deterministic, fast regional failover