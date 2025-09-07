# Designing Realtime Abuse Masker

Motive : Not everything is a service.

Statement : Say, one video live stream is powered by one server. All participants part of that stream (max 100) are connected to the same server. In this stream people can send the text messages (broadcast). We want to ensure abuses are masked like `s***` or `f***`

### Understanding Architecture

![](assets/Pasted%20image%2020250907083608.png)

* Live Stream of a creator is captured over RTMP
* participants are connected to the server over websockets
* participants can send message to all

### How socket.io works ?

Socket IO has notion of rooms, Simple Socket IO process is running on server. We want to create a `room` for this live stream. Participants join the room.

#### Abuse Dictionary

Assume that we have a list of words (*abuses*) stored in a text file on Blog Storage like S3 (at a path).
Hence, when the live stream server starts up

* downloads the abuse file
* loads it in memory ~ how and which data structure.

#### Masking the Abuse

Given all the messages will go through the same server, we have to find some logic that efficiently detects and masks.

Approach 1 : Tokenize and Lookup

* load all abuses in a dictionary (hash set)
* tokenize incoming text message
* for each word, check if it is in abuse dict
* if yes : mask and update the token
* if no : copy the token

This is a simple approach but not efficient.

* Tokenize (text to list of tokens requires extra space)
* string look up is expensive

Approach 2 : Trie

We can build a trie out of abuses and in just $O(n)$ traversal mask the abuses.
For each character in text we iterate through trie everytime we get `_`, `,`, ... etc we reset our trie iteration (to the top).

if the abuse is found an next char is EOS or non-alphabet, we mask and write the new string. Else the word copied as is. The final string is then sent/broadcasted to every participant.

How this fits in the system ? 
We typically think of databases and all to hold and query but that is very slow for this plus no database exposes trie, So what should we do ?

### Really poor way to design this system

Have a *abuse masker* service that exposes an HTTP endpoint accepting text and returns masked version of it. The web service will have the trie loaded in memory.

![](assets/Pasted%20image%2020250907085245.png)

NOTE : Not everything needs to be a *service* . It would add network latency.
Setting up TCP connection will take (3 way handshake) and teardown will require 2 way teardown. For persistent connection we will incur network I/O.

Hence, create a config in S3 that load every time server boots up

![](assets/Pasted%20image%2020250907091308.png)

#### Configuring Abuse List

We need a way to update the list of abuses (internal team)

- we need a UI where abuses are listed
- we should update the abuses and push them to s3

We can create an Abuse Admin Service to take care of this.

![](assets/Pasted%20image%2020250907092044.png)

