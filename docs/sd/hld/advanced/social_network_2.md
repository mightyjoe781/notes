# Social Network

#### How images are served

`https://media.minetest.in/static/img/resume.png`

Folder Structure : `site/static/img/<file>.png`

Once the request hits the server

- reads the URL
- reads the file from the server at the path/reads the file from s3
- sends the response

```python
# demonstration of how we can dynamically generate image for github
@app.route('/raw/<path>')
def raw_handler(path):
    raw_b = s3.read(path, BUCKET)
    return raw_b
```

`http://localhost:5000/raw/users/smk.jpg` : This acts as proxy for s3, similar to how static tries to find the image in the disk.

## Designing Gravatar

Gravatar is your single embeddable URL for profile picture.

`https://gravatar.com/{hash(email)}` -> security PII
`hash("smk@minetest.in") = 0eafd172`
and above can be rendered

`<img src= "https://gravatar.com/0eafd172" />`
renders the current profile picture

- user can upload multiple pictures
- user can mark one as active
- active one should be returned as part of the response.


If derivable is a complicated calculation and it is run in *where* clause will be catastrophic as query will not able to utilise indexes.

Lets write our API server : *api.gravatar.com*
Uploading Photo

![](assets/Pasted%20image%2020250915093400.png)

Prepare for upload :

- user requests photo upload service for a new upload
- photo upload service generates a random id
- photo upload service generates signed URL for : `s3://gravatar-images/{user_id}/{random_photo_id}`
- photo upload service sends signed URL to user

Upload Photo

- user uploads photo to s3

Making entry in gravatar

- make POST request to add photo to gravatar

![](assets/Pasted%20image%2020250915093924.png)

#### Render the active photo

`https://api.gravatar.com/photos/{hash}`

- get hash from URL
- get active photo id from the database

```sql
SELECT * from photos join USERS
where USER.hash = {hash} and IS_ACTIVE = True
```

- read the file from s3 : `https://gravatar_images/{user_id}/{photo_id}`
- return the resposne

But in frontend we can use CDN to make it render
`<img src = https://api.gravatar.com/photos/0eafd172 />`


### Marking photo as Active

| id    | user_id | is_active |
| ----- | ------- | --------- |
| 7abe  | 729     | false     |
| 8ab   | 729     | false     |
| cdae  | 729     | True      |
| e7215 | 729     | false     |

How will you mark one photo as active ?
Discuss, how its better to store `active_image_id` on the users table and just find this image directly from that table rather then performing complex join queries.


So, we have got everything working at : `https://api.gravatar.com/photos/0eafd172`

But we want `https://api.gravatar.com/{hash}`

Let's use CDN to serve it

Configure  `gravitar.com -> api.gravatar.com/photos (origin)`
`https://api.gravatar.com/hash -> https://api.gravatar.com/photos/`
We get, speed and scale of CDN & ease of use for users.

![](assets/Pasted%20image%2020250915100400.png)


## On-demand Image Optimization

Just like how CDN accepts query params we will accept query params which will indicate the transformations.
Let's say image : 1024 x 1024, but we want to render it as an icon : 32 x 32

`< img src = "https://gravatar.com/h1?w=32" />`

Here `w = 32` represents the transformation done on the image.

URL driven image manipulations

`https://edge.smk.minetest.in/img/smk.png?w=240`

CDNs give this feature out of the box. This is what CDN does internally.

- reads the URL
- if it has the file, return
- if not read the file from origin
- transform as per the given transformation
- cache the file locally
- return the response.

CPU intensive ! Cannot be done asynchronously, large servers (size & numbers)

We use services like *PIL* or `ImageMagik` libraries to do transformations, on the images.

## Tagging Photos

Questions

- Who can tag (Authorization)
- Max limit of people tag in a photo
- Notifications & throttling
- self-removal
- face recognition & suggestions (SLA)
- profile/activity (DB)
- Feed

![](assets/Pasted%20image%2020250915083904.png)

Relative Positioning of the tag

$$
location = (\frac{320}{720},\frac{120}{720})
$$
allows us to handle multiple devices on-demand transformation of the image. `LTRB/xywh`

schema : *post_tags*

| post_id | user_id | location |
| ------- | ------- | -------- |

Services to interact with : 

- search
- face detection
- location
- notification
- RBAC (Authorized to tag ?)

Key component for extensibility : *Kafka*

`PHOTO_TAG` event will have many consumers like search, notification, analytics, profile etc.

## Designing Notification Badge

We need to inform users about presence of new message (not unread/unacknowledged)
User can have 100s of unread messages but the number `3` indicates there are 3 people 

Messaging System

![](assets/Pasted%20image%2020250915091020.png)

Problem 1 : find when message is not delivered ?
that is when you will `cnt++`

*Websockets* know if a user is connected or not (also maybe an online/offline indicator), we use to find the undelivered messages.

![](assets/Pasted%20image%2020250915091301.png)

#### ON_MSG_UNSENT

Kafka becomes input to our systems

Each event would contain

```json
{
    "src": "A",
    "dest": "B",
    "msg": "..."
}
```

We want number of unread messages from Unique users
`user_id : {u1, u2, ...}`


![](assets/Pasted%20image%2020250915092920.png)

Auxiliary Database helps us take load off original redis cluster by becoming a writing sink for Kafka Workers.
In case if this Auxiliary Database goes down we can redirect entire traffic to cluster for direct writes.

## Building a Notification System

- combine message stream with message broker to get high throughput systems.