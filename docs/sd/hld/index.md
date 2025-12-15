# High-Level Design


## Basics

- [Introduction to System Design](intro.md)
- [Databases and Scaling](db.md)
- [Caching and Optimization](cache.md)
- [Messaging and Streaming Systems](streaming.md)
- [Load Balancing and Fault Tolerance](load.md)
- [Communication and Protocols](communication.md)
- [Big Data and Applications](big_data.md)
  
## Real-world System Designs

- [Designing an E-commerce Product Listing](problems/ecommerce.md)
- [Designing an API Rate Limiter](problems/rate_limiter.md)
- [Designing and Scaling Notification Systems](problems/notification_system.md)
- [Designing a Realtime Abuse Detection System](./problems/abuse_masker.md)
- [Designing a Tinder-like Feed](problems/tinder_feed.md)
- [Designing Twitter Trends](problems/twitter_trends.md)
- [Designing a URL Shortener](problems/url_shortener.md)
- [Designing GitHub Gists / Pastebin](./problems/pastebin.md)
- [Designing a Fraud Detection System](problems/fraud_detection.md)
- [Designing a Recommendation Engine](problems/recommendation_engine.md)
- [Designing a Web Crawler](problems/web_crawler.md)

## Advanced Topics

- [Foundational Concepts](./advanced/foundational_1.md)
    - Online Offline Indicator

- Databases
    - [Relational Databases](./advanced/relational_database.md)
        - Relational Databases & Pessimistic locking
        - Designing : KV store on relational DB
    - [Non-Relational Databases](./advanced/non_relational_database.md)
        - Non-Relational Databases

- Distributed Systems
    - [Distributed Systems](./advanced/distributed_systems.md)
        - Designing Load Balancer
        - Remote and Distributed Locks
        - Synchronizing Consumers
    - [Distributed ID Generators](./advanced/distributed_id_generators.md)
        - Distributed ID generator
        - Monotonically increasing IDs
        - Central ID generation service
        - Snowflake : Twitter

- Building Large-Scale Social Networks
    * [Building Social Network](./advanced/social_network.md)
        * Instagram's Architecture
        * Uploading photos at Scale
    * [Building Social Network 2](./advanced/social_network_2.md)
        * Designing Gravatar
        * On-demand Image Optimization
        * Tagging Photos
        * Designing Notification Badge

- Storage Systems
    - [Storage Engines - I](./advanced/storage_engines.md)
        - Designing a Distributed Cache
        - ETL & Tiered Storage
    - [Storage Engines - II](./advanced/storage_engines_2.md)
        - Word Dictionary without using any DB
        - Superfast DB KV

- High Throughput System Design
    - [High Throughput Systems - I](./advanced/high_throughput.md)
        - Multi-Tiered Storage
        - Designing S3
    - [High Throughput Systems - II](./advanced/high_throughput_2.md)
        -  LSM Trees
        - Designing Video Processing Pipeline

- Information Retrieval Systems
    - [Building Search Engines and Retrieval Systems](./advanced/search_engines.md)
        - Designing Recent Searches
        - Designing : Cricbuzz's Text Commentary
        - Designing : Super Simple text Based Search Engine

- Advanced System Design Techniques
    - [Adhoc System Design](./advanced/ad_hoc.md)
        - Distributed Task Scheduler
        - Message Brokers on DB
        - YouTube Views Counter
        - Flash Sale
    - [Algorithmic System Design - I](./advanced/algorithmic_design.md)
        - Impression Counting
        - Remote File Sync
    - [Algorithmic System Design - II](./advanced/algorithmic_design_2.md)
        - Geo-Proximity
        - User Affinity Service

Resources :