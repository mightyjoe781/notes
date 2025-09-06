## Storage 

### Amazon S3

#### Overview

- Amazon S3 is a fully manage object based storage service that is highly available, highly durable, cost effective and widely accessible.
- Smallest Size : 0KB, Largest Size : 5TB
- Each object uploaded does not conform to file structure level heirarchy like OS, instead its storage as object with flat address space and located by unique url.
- Its a regional service. [Resource](https://cloudacademy.com/blog/aws-global-infrastructure)
- To locate a specific file within the bucket we use keys and to access that object via internet we use object url. Bucket url and object key makes up the object url.

#### Storage Classes

1. S3 Standard : 
2. S3 INT (Intelligent Tiering) : for both frequent and infrequent access (use when frequency is not known)
3. S3 S-IA (Standard Infrequent Access) :
4. S3 Z-IA (One zone and Infrequent Access) :
5. S3 Glacier : Long term archival storage solution
6. S3 G-DA (Glacier Deep Archive) : same as S3 Glacier with min 12 hours retrieval time.

All 4 above services offer **High Throughput**, **low latency**, **SSL to encrypt data during transit**, **lifecycle rules to automate data storage management**.

S3 has Highest availability of 99.99% and Eleven 9s durability. S3 INT, S3 S-IA have similar availability and durability. S3 Z-IA have such durability and availability only for a region.

**Lifecycle Rules** : You are able to set and configure specific criteria which can automatically move your data from one storage class to another or delete it. (to save cost we can move around data not in use to other cheaper classes).

Intelligent Tiering is based on principle : *more frequently accessed data is more faster to access*. Within the same class there are two tiers : Frequent Access and Infrequent Access, thoughout the life cycle data keeps moving around according to its demand.

Glacier Services do not offer graphical user interface and its a two step process to setup to move data into glacier.

1. Create your valut as a container for your archives
2. Move your data into the Glacier vault using the available APIs or SDKs

Access to data is costly depending on how urgently you need the data : expedited (under 250mb available in 5 minutes) , standard (any size, 3-5 hours) and bulk (PB of data, 5-12 hours) options.



### S3 Management Features

#### Versioning

- Versioning is maintained automatically completely by AWS if enabled (not enabled by default) but once enabled can’t be disabled only paused/suspended.
- Version ID is used to maintain versions. Deleted versioned files can be seen when show/hide is toggled with version called *Delete Marker*.
- If you enable versioning on an existing bucket in Amazon S3, how are the unmodified objects already in them labeled? : Null

#### Server Access Logging

- Logs are collected every hour and there is no hard and fast rule that every request is logged, sometimes specific logs may not be available.
- You will need to configure Target bucket (used to store the logs, should be same zone as source bucket) and target prefix for management. You can also configure this while bucket creation.
- If you using AWS Console then Log Delievery Groups are automatically added to Access Control List of the target bucket. But if you are utilizing some API/SDK you will need to manually add access to ACL.
- Log Naming Standard : \<Target Prefix\>YYYY-MM-DD-HH-MM-SS-UniqueString/
- Entries in logs are as : BucketOwner Bucket TimeStamp RemoteIPAddress Requester Operation Key RequestURI HTTPStatus ErrorCode ByteSent ObjectSize TotalTime(ms) TurnAroundTime Referer User-Agent VersionID HostID Cipher Suite AuthHeader TLS Version

#### Object Level Logging

- Closely related to AWS Cloudtrail and logs DeleteObject, GetObject, PutObject requests. It also logs Identity of the caller, timestamp and source IP address.
- Can be configured at Bucket level or AWS Cloudtrail Console.

#### Transfer Acceleration

- Amazon Front is a CDN (Content Delievery Network) greatly increased transfer speeds between client to S3 or vice-versa.
- There is a cost associated with Transfer Acceleration per GB according to Edge region.
- NOTE : your bucket name always should be DNS complaint and should not contain any periods to utlize this feature.
- Trasfer Acceleration doesn’t Support GET Server, PUT bucket, DELETE Bucket and Cross-region copies using PUT Object Copy

### Amazon S3 Security

#### Using Policies to Control Access

- Identity Based Policies : Attached to IAM identity requiring access, using IAM permission policies, either in-line or managed.
    - Assoiciated to a User or role or group
    - We can control access with **conditions** [Resource](https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazons3.html)
- Resource Based Policy : policy is associated with a resource
    - Forms : Access Control Lists and Bucket Policies
    - Need to define who will be allowed/denied access
    - Written in JSON or use AWS policy generator
    - permissions are controlled with **principals**
- IAM Policies are desired in case to centrally manage access and you have several roles to assign rather than 1 bucket/policy, Can control access for more than one service at a time. (max allowed policy size : 2Kb is size for users, 5Kb for groups, 10Kb for roles)
- Bucket Policies : controls S3 buckets and its objects, Used to maintain security policies within S3 alone. Can grant cross-account access without having to create and assume roles using IAM (max allowed policy size : 20Kb)

Both are not mutually exclusive and used together. In case of information conlict : principal of Least-Priviledged is utilised : if there is even single deny, any authorized request will be denied.

#### S3 Access Control List

- ACLs allows control of access to bucket, and specific objects within a bucket by groupings and AWS accounts
- can set different permissions per object
- ACLs do not follow same JSON format as the policies defined by IAM and bucket policies
- More Granular Control, can be applied at Bucket Level or Object Level.

- Permissions : LIST, WRITE, BUCKET ACL READ, BUCKET ACL WRITE

#### Cross Origin Resource Sharing (CORS) with S3

CORS allows specific resouces on a web page to be requested from a different domain than its own.

This allows to build client-side web application and then, if required, you can utilise CORS support to access resouce stored in S3.

Policy(JSON) is evaluated on three fold rules

1. Requestors *Origin* header matches and entry made in *Allowed Origins* element
2. The method used in request is matched in Allowed methods
3. The headers used in Access-Control Request Headers within a preflight request matches a value in the *Allowed Header* element.

### Amazon S3 Encryption

- SSE-S3 (Server Side Encryption with S3 managed keys)
    - minimal configuration, upload all data and S3 will manage everything
    - AWS will manage all encryption keys
- SSE-KMS (Server Side Encryption with KMS managed keys)
    - allows S3 to use Key Management Service to generate data encryption keys
    - gives greater flexibility of key diabled, rotate and apply access controls.
- SSE-C (Server Side Encryption with customer provided keys)
    - provide you master keys
    - S3 will manage encryption
- CSE-KMS (Client Side Encryption with KMS managed keys)
    - uses key management service to generate data encryption keys
    - KMS is called upon viathe client, not S3
    - encryption happends on client side and encrypted data send to S3
- CSE-C (Client Side Encryption with customer managed keys)
    - utlise your keys
    - use an AWS SDK client to encrypt data before sending to AWS for storage

### Best Techniques to Optimize S3 Performance

1. TCP Window Scaling
2. TCP Selective Acknowledgement
3. Scaling S3 Request Rates
4. Integration of Amazon CloudFront

