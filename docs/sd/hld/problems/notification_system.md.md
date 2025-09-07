# Notification System

Motive : Designing an extensible system and reading unsaid requirements.

Objective : Design a notification service that sends *notifications* to users across channels.
The system needs to be horizontally scalable and should support a very high fan-out.

Instead of directly jumping to send *millions* of notifications, lets start with simple service.

## Notification Template

* We need a UI and simple backend to create notification template that will be configured by some internal team.
* number of notification templates will not be huge & will fit on a single machine. Hence, we start with relational OB

![](assets/Pasted%20image%2020250906230723.png)

When any team/product wants to send notification
* create a template using the Notification Control Service
* Specify the variables
* note the ID of the defined the template

## Notification Channels

User can be notified via multiple channels

* email
* android push notification
* apple push notification
* SMS

For each of the above channels there are providers that expose APIs. We invoke them programmatically to send notification at the *very instant*

Some Examples : SES, Mailgun, One Signal, Twilio, Msg91, Pushover, etc.

So, the servers that will send/trigger the actual notification will have to configure their SDKs/libraries.

NOTE : The API Calls are expensive network calls with high latencies, one machine will not be able to make million of concurrent calls.

### Simple Notification Flow (one user)

![](assets/Pasted%20image%2020250906231535.png)

* PM creates a Notification Template
* PM triggers notification, the control service notifies all subscribers instantly.

What if PM wants to trigger thousands of notifications at the same time ? Wants Robustness, so doesn't rely on providers timing out.

![](assets/Pasted%20image%2020250906232947.png)

This architecture solves *retries* does not overwhelm notification service, and the API service is installed on Workers which sends the notification.
Making the architecture asynchronous, gives us retries. If one of the worker fails to send message, it will appear in the queue again, and picked by another worker.

#### Bulk Notification :
Above architecture works well when we have moderate traffic and notification are triggered one by one.
A typical usecase : notify `everyone`
User Experience : PM submits a job to notify everyone and we need to take care of everything else.

Approach 1 : Control server iterates

* iterating through million rows might hog the resources of the control service preventing it to serve other requests

Approach 2 : Control server delegates iteration

![](assets/Pasted%20image%2020250906233319.png)

SQS1 : Notification Emitter
SSQ2 : User iterator, and anything that requires some processing.

### Important Notification

Some notifications are more important than others. e.g. Appointment Reminders >>> Marketing Push

In out current architecture, one marketing campaign will keep executors busy and all other notifications will starve in the queue.
To solve this : Instead of having one Notification Emitter Queue, have multiple queues with priority queue (p1, p2, p3) & each having its own set of workers.

![](assets/Pasted%20image%2020250906234942.png)
Horizontal Scalability - add more queues, add more workers
Load Isolation and avoiding starvations.

Duplicate Notification ?

It is really irritating to receive marketing notifications and it is the worst if we receive multiple of the same campaign.

To ensure we do not accidentally send multiple notification from same campaign we keep track in the a database (KV store is fine)

$$
\begin{split}
100 M \times (4B + 4B) = 800 MB \\
5 \text{ campaign} \sim 4 GB
\end{split}
$$



![](assets/Pasted%20image%2020250906235816.png)

Add Bloom Filters to check whether a specific user is notified already and it will save size of the database from GBs to MBs.

Notification Tracker DB

* light weight & shard-able
* in-memory with periodic persistence
* bloom filter support a plus (space efficient)

Exercise

* Try implementing Bloom Filters on your own.