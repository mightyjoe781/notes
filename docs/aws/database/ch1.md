## AWS Global Infrastructure



The components of AWS Global Infra are:

- Availability Zones (AZs)
- Regions
- Edge Locations
- Regional Edge Caches
- Local Zones
- Wavelength Zones
- Outposts

**Availability Zones (AZs)**

- Physical data-centers of AWS
- Multiple Physical data-centers close enough together form one Availability Zone
- Each AZ will have at least nearby sister AZ(probably in nearby city) which is connected via very low latency private fibre optic (used by many AWS Services to replicate data : Read up synchronous and asynchronous replication)
    - Note Both AZ will be separate power resources and network connectivity
    - This is all because of resilience and availability purpose.
- Making use of 2 AZs in one Region ensures your infra remains stable, available, and resilient even in worse times

**Region**

- Collection of AZs that are located geographically close to each other
- Every Region works independently of others and will have atleast 2 AZs
- Having global regions allows organisation to comply with local laws to store data
- Use mulitple region if you are a global organisation and downtime may cost money
- Currently there 32 Regions and 102 AZs. (Note : this number may have changed)
- Note : not all services are available in every region. IAM and CloudFront are global Services
- AWS GovCloud is a region only available to approved US Companies
- Naming convention of region : region-direction-number

![image-20230219124734176](ch1.assets/image-20230219124734176.png)

NOTE : AWS maps these AZ letters to different AZs for different AWS Accounts for ensuring even distribution of resources across all AZs within a Region.

**Edge Locations :**

- AWS Sites deployed in Major Cities and highly populated areas across the globe.
- Outnumber AZs
- Utilised for services such as CloudFront and Lambda to cache data and reduce latency for end-users by using Edge Locations as CDN.

**Regional Edge Cache**

- These Edge Location sit between your CloudFront Origin servers and the Edge Locations.
- Large Cache-width than each of individual Edge Locations
- Data is retained at Regional Edge Cache while it expires at Edge Locations

**Local Zones**

- 2022 : Amazon launches first 16 Local Zones
- Local Zone : a new type of infrastructure deployment designed to place core AWS Compute, Storage, Networking & Database services near highly populated areas.
- All Local Zones will be connected to a parent Region, allowing seamless connection between other AWS Services.
- Available in 33 metropolitan areas (19 more planned)

**Wavelength Zones**

- Similar to Local Zones but differs how it connects to its parent Region i.e. 5G mobile broadband networks and re deployed within the data centers of large telecommunication providers.
- AWS Wavelength Zones are available through Verizon in US, KDDI in Japan, SK Telecom in South Korea, Vodafone in UK/Germany & Bell in Canada

**Outposts**

- brings capabilites of AWS Cloud to your on-premises data center, includes same hardware used by AWS in their data centres
- allows users to use native AWS services, including the same tools and APIs you would use when running your infra within AWS.
- available as 1U or 2U rack-mountable servers, or as 42U racks that can be scaled to 96 racks
- provides PrivateLink Gateway endpoints to securely and privately connect to other services and resources such as DynamoDB
- aws will patch and update those servers
