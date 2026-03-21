# Social Network (Part 2)

## How Images Are Served - The Proxy Pattern

Before CDNs became universal, teams served static files one of two ways: directly off disk, or via a server-side proxy that read from object storage and forwarded the bytes to the client.

```python
@app.route('/raw/<path>') 
def raw_handler(path): 
    raw_b = s3.read(path, BUCKET) 
    return raw_b
```

`https://media.minetest.in/raw/users/smk.jpg` - this route acts as a **transparent proxy** for S3. The client never knows it's talking to S3; it just sees a normal HTTP endpoint. 

This is the same pattern that Django's `STATIC_URL` uses when it maps `/static/img/resume.png` to a folder on disk - the server reads the file and writes it to the response.

**Why you'd still do this today**: access control. If you need to check permissions before serving a file (e.g. "is this user allowed to see this document?"), a proxy lets you gate the read. Pre-signed URLs can't do conditional per-request auth - they're open to anyone who holds them for their lifetime.

**Why it doesn't scale**: the API server is now in the critical path of every byte transferred. Every concurrent image load consumes a worker thread and network bandwidth twice (once inbound from S3, once outbound to client).

For anything beyond low traffic, move to CDN + pre-signed URLs.

## Designing Gravatar

Gravatar is a globally shared profile picture service. The core idea: **one canonical URL per person**, derived deterministically from their email, embeddable anywhere.

```
hash("smk@minetest.in") = 0eafd172 

<img src="https://gravatar.com/0eafd172" /> # security or PII requirements
```

The hash serves two purposes: it's deterministic (same email always yields the same URL), and it avoids exposing the raw email address (PII) in the URL. MD5 is what Gravatar historically used, but its collision and preimage weaknesses mean modern implementations would use SHA-256 truncated.

`<img src= "https://gravatar.com/0eafd172" />` renders the current profile picture.

#### Data Model

A user can upload multiple photos and mark one as active. The naive schema puts an `is_active` boolean on the `photos` table:

| id    | user_id | is_active |
| ----- | ------- | --------- |
| 7abe  | 729     | false     |
| 8ab   | 729     | false     |
| cdae  | 729     | **true**  |
| e7215 | 729     | false     |


Lets write our API server : *api.gravatar.com*

#### Upload Flow

![](assets/Pasted%20image%2020250915093400.png)

Identical to Instagram's pattern: 

1. **Prepare**: client calls Photo Upload Service → receives a pre-signed S3 URL for `s3://gravatar-images/{user_id}/{random_photo_id}` 
2. **Upload**: client PUT directly to S3 (no proxy through your servers) 
3. **Register**: client calls `POST /photos` to create the DB record

![](assets/Pasted%20image%2020250915093924.png)

#### Serving the Active Photo

```
GET https://api.gravatar.com/photos/{hash}
```

- get hash from URL,
- get active photo id from the database

```sql
SELECT * from photos join USERS
where USER.hash = {hash} and IS_ACTIVE = True
```

**Construct S3 path**

- read the file from s3 : `https://gravatar_images/{user_id}/{photo_id}`
- return the resposne

**Proxy Read from S3 directly**

But in frontend we can use CDN to make it render : `<img src = https://api.gravatar.com/photos/0eafd172 />`

#### Marking photo as Active

| id    | user_id | is_active |
| ----- | ------- | --------- |
| 7abe  | 729     | false     |
| 8ab   | 729     | false     |
| cdae  | 729     | True      |
| e7215 | 729     | false     |

**The problem with `is_active` as a column**: marking a new photo active requires a transaction that sets the old row to `false` and the new row to `true`. 

Under concurrent writes, this can fail or produce two active photos. It also forces a full-table scan or index scan on `is_active` per user.

#### CDN Configuration

The final URL Gravatar exposes is `gravatar.com/{hash}` — clean, short, embeddable. Behind the scenes:

- API works as expected at following URL : `https://api.gravatar.com/photos/0eafd172`
- Requirement : `https://api.gravatar.com/{hash}`


gravatar.com/{hash}

  - CDN (origin: api.gravatar.com/photos)
  - api.gravatar.com/photos/{hash}
  - DB lookup → S3 read → response


![](assets/Pasted%20image%2020250915100400.png)

Configure the CDN to cache responses with a TTL short enough that photo changes propagate reasonably fast (e.g. 5–15 minutes). On cache miss, the CDN calls the origin, which does the DB + S3 resolution. On cache hit, the CDN serves directly - zero origin load for popular hashes.
## On-demand Image Optimization

Different clients need different image dimensions. A 1024×1024 photo uploaded by a user should render as a 32×32 icon in a notification, 240×240 in a profile card, and full-size in a lightbox. Storing all variants up front is wasteful. 

On-demand transformation solves this.

```
<img src="https://gravatar.com/0eafd172?w=32" />
```


The `w=32` query parameter instructs the CDN (or a transformation proxy) to resize the image to 32px wide before serving.

The CDN flow:

1. Check cache for `{hash}?w=32` - hit → return immediately
2. Miss → fetch original from origin
3. Resize using an image processing library (PIL, ImageMagick, libvips)
4. Cache the resized variant keyed by `{hash}?w=32`
5. Return to client

**Why this is CPU-intensive**: resizing is synchronous, blocking, and proportional to image dimensions. 

A 4K → 32px downscale is fast; a 4K → 3840px crop with sharpening is not. This is why CDN edge nodes are large, numerous, and cache aggressively - the compute happens once per variant per edge location, then the cache absorbs all subsequent requests.

**Common transformation parameters**:

- `w` / `h` - width/height (maintain aspect ratio if only one specified)
- `q` - quality (JPEG compression, 1-100)
- `f` - format conversion (e.g. `f=webp`)
- `fit` - crop mode (cover, contain, fill)

Services like Imgix, Cloudinary, and Cloudflare Images offer this as a managed product. For self-hosted, `libvips` is substantially faster than ImageMagick for most operations.
## Tagging Photos

Photo tagging is richer than it looks. Before designing anything, scope the requirements:

- **Who can tag**: Only the post owner? Anyone? Friends only? → RBAC decision
- **Max tags per photo**: Instagram caps at 20. Unbounded tags create abuse vectors and UI problems.
- **Self-removal**: Can a tagged user remove their own tag without the post owner's consent? (Instagram: yes)
- **Notifications**: Tag creates a notification to the tagged user. Throttle if someone is tagged 500 times in an hour.
- **Face recognition**: Suggested tags based on face detection. This is async - runs after upload, has its own SLA (can be seconds to minutes), and results feed back as suggestions, not confirmed tags.
- **Feed & profile impact**: Being tagged in a photo may surface it on your profile/activity. This is a write to downstream systems.


![](assets/Pasted%20image%2020250915083904.png)

#### Tag Schema

A tag is a relationship between a post, a user, and a position within the image:

```
post_tags
  post_id   UUID  (FK → posts)
  user_id   UUID  (FK → users)
  location  JSONB -- { "x": 0.44, "y": 0.17, "w": 0.12, "h": 0.12 }
```

Relative Positioning of the tag

$$
location = (\frac{320}{720},\frac{120}{720})
$$
allows us to handle multiple devices on-demand transformation of the image. `LTRB/xywh`

**Location as normalised coordinates**: rather than storing absolute pixel coordinates, store position as a fraction of the image's dimensions (0.0–1.0). `(320/720, 120/720)` for a 720px-wide image.

This means the tag position is valid regardless of which resolution variant is rendered - you don't need to recalculate for the 32px icon vs the 1024px full view. Common formats: LTRB (left-top-right-bottom) or XYWH (x, y, width, height).

#### Event Driven Extensibility

When a tag is created, many downstream systems care: search index (now the tagged user is associated with this post), notifications (send a push/email), analytics, profile activity feed, face recognition feedback loop.

Rather than calling each system synchronously from the tag endpoint, publish a `PHOTO_TAG` event to Kafka:

`PHOTO_TAG` event will have many consumers like search, notification, analytics, profile etc.

```json
{
  "post_id": "...",
  "tagged_user_id": "...",
  "tagged_by_user_id": "...",
  "location": { "x": 0.44, "y": 0.17 },
  "timestamp": "..."
}
```

Each downstream system is an independent Kafka consumer group. Adding a new consumer (say, a moderation pipeline) requires zero changes to the tag service. This is the **open/closed principle** applied to distributed systems - the tag service is closed for modification but open for extension via new consumers.
## Notification Badge - Unread Message Count

The notification badge shows **the number of unique senders** with undelivered messages - not the raw message count. Receiving 50 messages from one person shows `1`, not `50`. This is a distinct counting problem.

Messaging System

![](assets/Pasted%20image%2020250915091020.png)

#### What "undelivered" means

A message is undelivered if it was sent while the recipient was **not connected via WebSocket**. WebSocket connections are stateful - the server knows exactly who is online. 

If user B is offline when A sends a message, that message is undelivered and should increment B's badge count.

A sends message → Messaging Service
- Is B connected via WebSocket?
    - YES → deliver directly, no badge increment
    - NO  → publish ON_MSG_UNSENT event to Kafka

![](assets/Pasted%20image%2020250915091301.png)

#### ON_MSG_UNSENT

Kafka becomes input to our systems.

```json
{
  "src": "user_A",
  "dest": "user_B",
  "msg_id": "...",
  "timestamp": "..."
}
```

The badge number is the cardinality of the set of unique senders with undelivered messages to a given user. In Redis this maps naturally to a **Set** per user:

```
Key: unread_senders:{user_B}
Value: Set { "user_A", "user_C", ... }
Badge count = SCARD unread_senders:{user_B}
```

When B opens the conversation with A, remove A from the set: `SREM unread_senders:{user_B} user_A`.

![](assets/Pasted%20image%2020250915092920.png)

Direct writes from Kafka consumers to Redis works at moderate scale. At high throughput, the Redis cluster becomes a write bottleneck. 

The mitigation is an **auxiliary DB** (e.g. a write-optimised DynamoDB or Cassandra table) that acts as the primary write sink for Kafka workers - Redis serves reads and is updated asynchronously from the auxiliary DB.

**Fallback**: if the auxiliary DB goes down, Kafka workers can redirect directly to Redis. The latency increases but the system stays functional. This is a simple circuit-breaker pattern on the worker side.

## Building a Notification System

The general shape of a high-throughput notification system:

Event Source (tag, message, like, comment)

-  Kafka topic (partitioned by destination user_id)
- Notification Workers (fan-out per user)
- Delivery channels: WebSocket (online), Push (mobile), Email (offline)

Partitioning by `dest_user_id` ensures all notifications for a given user are processed by the same worker, enabling in-order delivery and per-user rate limiting without distributed coordination.

**Rate limiting**: a user who gets 1000 notifications in 10 seconds (spam, viral post) should not receive 1000 push notifications. Apply a per-user token bucket at the worker level before dispatching to delivery channels.

## Further Reading

**On Image Processing**

- _libvips_ documentation — particularly the "Why is libvips quick" page. Explains pipeline-based processing vs load-modify-save and why it uses a fraction of the memory ImageMagick does.
- Cloudinary's engineering blog — covers lazy transformation pipelines, CDN integration, and format negotiation (WebP/AVIF).

**On Distributed Counters and Sets**

- Redis documentation on HyperLogLog - if you need approximate unique counts at extreme scale (billions of users), HyperLogLog trades exactness for constant memory.
- _"Counting at Scale"_ - Stripe's engineering blog post on their counter architecture. Covers batching, approximate vs exact counts, and when each is appropriate.

**On Notification Systems**

- Slack's engineering post _"Building Slack's Real-Time Messaging Infrastructure"_ - covers WebSocket fan-out, presence detection, and the tradeoffs between push and pull delivery.
- _"How Facebook Scales its Notifications Infrastructure"_ - Meta engineering blog. Covers the move from pull-based polling to push, and the Kafka-based fan-out architecture they settled on.
- _"The Tail at Scale"_ - Jeff Dean & Luiz André Barroso (Google, 2013). Foundational paper on latency distribution in large systems. Notification delivery SLAs are directly impacted by the patterns described here.

**On Event-Driven Design**

- _"The Log: What every software engineer should know about real-time data's unifying abstraction"_ - Jay Kreps. The Kafka consumer group model for extensible notification fan-out comes directly from the principles here.
- _"Designing Event-Driven Systems"_ - Ben Stopford (free PDF, Confluent). Chapter on event-driven microservices covers the tagging extensibility pattern in depth.