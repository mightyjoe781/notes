# High Throughput Systems

## LSM Trees

### Attempting to better Bitcask

Bitcask does

- append only files (no disk seek during write)
- in memory index (quick lookup)

Core Idea : Attempt to make writes faster

So can we write directly to RAM ? instead of disk ? that would make writes faster.

Another question is why are we trying to this ? Usually all products eventually start by solving small problem or niche in the already existing sea of solutions and then expand to compete against them. Ex - Duck DB started as a small scale analytics solutions.

Niche where this works in real-time data, which requires a very high write throughputs, e.g. sensors, IOT, clickstream, logging, location updates data, etc.

![](assets/Pasted%20image%2020250919090931.png)

Because we are writing directly to RAM, this gives you higher write throughput ! (but at the cost of Durability)

Excellent for high *ingestion* volumes.

Reads : You need RAM first, If key is present (latest values) return it. Or else fallback to disk for searching the key, but if its not in disk then return NOT Found.

If key is in memory it has to be the most recent value. *Tiered Storage*

#### Periodic Flush

Every `t` minutes in-memory buffer is flushed to the disk at once.
Where should we flush ?

- existing file
    - file too long
    - flush too long
- new file every flush ?
    - faster and efficient
    - flush everything in one shot

#### Get Key

Every flush creates a new file *SSTable* (in-memory & disk). It writes index and data in same file.
*SSTable* ~ sorted string table.

![](assets/Pasted%20image%2020250919101112.png)

GET (k) flow :
    lookup in memory if key is there, return the value or else start from the latest file on disk
    check if key is present, if yes return value, if no, then keep on checking in backwards in older files. if key is not found return *NOT_FOUND*

We do not need to go through each file, we check the indexes to see if the key present in the file.

#### SS Tables

![](assets/Pasted%20image%2020250919102217.png)

#### Merge and Compaction

Large number of files (immutable) on disk ---> Merge and compaction

Merging of SS table would take $O(n)$ time because data is already sorted !

Worst Case : k files on the disk, you look through all of them to realise key does not exists. Can we optimize this ?

![](assets/Pasted%20image%2020250919102917.png)

What if we have a way to know if key exists or not ?

*Set* -> becomes inefficient at scale. A better data structure which is space efficient ?
*Bloom Filters*

- return Yes (with uncertainty)
- return No (with certainty that it is not present)

### Bloom Filters

![](assets/Pasted%20image%2020250919103638.png)

Above bloom filters can be included in our design now. Another reason we can't use set is because its size will grow/change, and managing its space in our current layout becomes a challenge due to our append only design, while BLOOM filters will be fixed in size and can be allocated in memory as well easily or onto disk.

![](assets/Pasted%20image%2020250919103800.png)

#### How to handle data loss ?
Append all update/delete operations in *WAL* file (write-ahead-log)
This WAL file is truncated on every flush. (*configurations*)

If we are writing to disk every write, how is it faster than Bitcask ?
If we need zero data loss, we have to have WAL

How is it better than Bitcask ?
Keys are disk bound and not memory bound, we get comparable write amplification while being disk bound.

Whole uses LSM ? *RocksDB, LevelDB, BadgerDB* (why not redis) ?
Use cases: Bidding (4 min, bid then persistence, redis key expires and data is gone), Adtech

Some piece of data in memory and some on disk.

![](assets/Pasted%20image%2020250919110030.png)

LSM outperform everything where you want a quickly access for recently inserted keys at scale as LSM is stored in memory before being flushed in the disk.
Redis even though provides persistence, but requires everything to be stored in memory. LSM outshine Redis in recency data access and size bound memory.

## Designing Video Processing Pipeline

Requirements

- video upload
- video processing
- video distribution

#### Need of transcoding

Recorded Video is in a certain format, say `.mov`. But, client device may not support this format.
Each video/audio will have *bitrates*

- high bitrate $\propto$ quality
- high bitrate requires higher processing power and faster internet speed

But all devices (users) won't have. Hence we have to *transcode* (convert into various resolution, bitrate, format)

Visit : https://howvideo.works/ 

For a smoother UX while watching video,

- higher resolution video when internet is good, battery is good, device is good
- when network fluctuates, we should switch between resolution & bitrates.

Two components :
**Containers** : A file format that stores multimedia data, including audio, video, and metadata.  Format `.mp4`, `.avi`, etc
**Codec** : A method or algorithm used to compress and decompress audio/video data. `h.264`, `vpq`, `hevc`. 

![](assets/Pasted%20image%2020250919231336.png)

*Use ffmpeg to transcode*.
*Janus*, *WebRTC*, *TURN servers*, *100ms* website, etc are great sources of content.

Now that we know transcoding is essential, we put it in our design.

### Transcoding

- Workflow Management - Airflow, Luigi
- Event Driven - Kafka

#### Workflow Management Tool

![](assets/Pasted%20image%2020250919231819.png)

Use Case would be managing workflow of video upload here. Rather than getting into managing multiple Kafka we will use specialized tools for workflows.

![](assets/Pasted%20image%2020250919232030.png)

#### Should we transcode all videos ? No

Similar to *on-demand* image optimisation, we do on-demand transcoding. Live streaming & Low sub videos.
Feed is captured in live and in a batch of small buffers (10 seconds) and transcoded in real-time and server using CDN, that is why live streams run 30 seconds behind the live event.

#### Caching (CDN) is expensive

Hence we do not cache all videos, only the videos that are worthy to be cached.

#### Full Architecture

![](assets/Pasted%20image%2020250919233814.png)



Exercises

- implement your own bloom filter