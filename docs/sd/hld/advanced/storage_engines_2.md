# Storage Systems II

## Word Dictionary without using any DB

Requirements

    scalable (storage (portable) and API servers (resposne time can be high))

- No traditional database, Be creative
- words and meanings are updated weekly (though a changelog)
- lookup is always a singular word
- dictionary is 1TB big, and has 170,000 words.

### Storage

Because we cannot use a traditional DB, let's be creative and use S3 (network attached filesystem) - raw file system.

Approach 1 : 170k words, each word in a separate file

```txt
s3://word-dict/a/apple.txt
            .../america.txt
            ....
            .../z/zoo.txt
```

Folder for each character.
Lookup : `get_word(w)` -> create s3 path, goto s3, read the file return the meaning.

But this approach breaks a major requirement. *Portability*

Approach 2: Storing all words & meanings in one file. Simplest format would be CSV
The file will be 1TB big. Now, how would the lookup word ?
Traversing complete dictionary is not a good choice. *Too slow and expensive*

Making lookups faster:
A universal strategy to make lookups faster - *Indexing*
index.data & data.dat

![](assets/Pasted%20image%2020250917211217.png)

This could be stored as a separate file. but with some smart choices we can divide the file logically.

What is the size of index.dat ?

Total words 171476
Avg Words length 4.7

Total index size : 2.6 MB

$$
size = 15.7 \times 171476 \sim 2692173.2 \sim 2.6 MB
$$

Since index is very small in size & can be stored in memory, flow would be like this

API server on boot

- loads the index file in memory
- upon receiving a req
- lookup in index (memory)
- find offset
- goto s3 and read the entry
- return the memory

![](assets/Pasted%20image%2020250917214912.png)


#### Updating the dictionary

updates are *changelog*

Procedure

- spinup a new server
- download the dictionary locally
- download the changelog
- merge in $O(n)$, create a new dict & index locally
- upload the new dictionary on S3 & new index

#### How is merge O(n)

Dictionary is sorted. Index is sorted

Merge -> merging of two sorted list.

![](assets/Pasted%20image%2020250917214633.png)

#### Where to upload the new dictionary

Same location ? `s3//word-dictionary/data.dat & index.dat`
NOTE: servers have already loaded the old index built for old dictionary data

User might see garbage data in response during replacement, how will we make transition smooth for users

#### Transitions

1. Periodic refresh of server's idnex
2. Reactive : Use a redis pub sub to send events to the servers serving the dictionary
3. Parallel Setup
    1. upload index and data to a new path, keep a `meta.json`
    2. `meta.json` will point to new location where file is uploaded.

![](assets/Pasted%20image%2020250917214923.png)

New data & index files are uploaded to new path on S3 and `meta.json` file changed
Old server continues serving old data. New server will load new `meta.json` & serve from new files.

![](assets/Pasted%20image%2020250917223334.png)
#### Solving portability

Two files index and data not portable, let's merge !
How to where index ends and data starts ? Adding a separator or predefined size of bytes.
Adding a separator is not a good choice, we solve this problem using header.

![](assets/Pasted%20image%2020250917222136.png)

Header stores

- offset of index, data
- meta information ~ total words + versions

![](assets/Pasted%20image%2020250917222143.png)

*New Flow*

- API server loads header (fixed width)
- API server loads the index
- API server starts serving the requests

#### Real world applications

- multi - tiered storage
    - historical orders on S3
    - latest orders in MySQL
- Without loosing an ability to query the data store historical data on S3

Athena
DataLake

## Superfast DB KV

Requirements : superfast reads, writes, deletes, persitence

SSD are more closer to memory rather than magnetic disks, both in terms of cost and speed.
Each hard disk has sector and data is read based on offsets across sectors.

![](assets/Pasted%20image%2020250917230428.png)

Log - Structured Storage

Data stored files

- append-only
- sequential writes
- no random updates

No disk seeks during writes

What we get ? High write throughput (even on HDD)
The SSD doesn't give similar gain


**Simple Design** : Single files of KV pairs

![](assets/Pasted%20image%2020250917231928.png)

PUT (k, v) -> append to this file (lighting fast operations)

DEL (k) -> delete operation is also a *PUT* with special value (-1) (representational)
DEL(k) = PUT(K, -1)

#### How one entry in file looks like ?

![](assets/Pasted%20image%2020250917232240.png)

When reading one entry from file, do we know how much to read. We cannot read *until newline*, not optimal
*Because key and value are of variable length*

![](assets/Pasted%20image%2020250917232248.png)

We read KS2 (4 bytes) VS2(4 bytes) and then read
KS2 bytes for key
VS2 bytes for values

#### Solving Integrity

![](assets/Pasted%20image%2020250917232732.png)

Finding corrupt entries : CRC -> first thing we flush

![](assets/Pasted%20image%2020250917232724.png)

#### Faster GET(k)

To get O(1) GET we use *Index*.
We create an in-memory Hash Table

![](assets/Pasted%20image%2020250917233018.png)

GET(k) -> pointed queries

- Hash Table lookup
- disk seek
- disk read

limitation : index to fit in memory

#### When file grows too big ?

Solution : rotate the file every *t* bytes.
We create new file and old file is made *immutable*


![](assets/Pasted%20image%2020250917233227.png)

#### Changes in our in-memory index

![](assets/Pasted%20image%2020250917233700.png)

We have a lot of files, can we optimize ?

We merge & compact.
All immutable files are merged(stale entries skipped) & compact(deleted entries skipped)

![](assets/Pasted%20image%2020250917233832.png)

Because files are merged offset changes, we have to update index atomically !

Limitations of the DB : Keys must fit in memory
Strength of this DB : O(1) reads, writes, deletes

- High throughput, low latency
- I/O stauration
- Easy Backups

What we just designed is *Bitcask*

![](assets/Pasted%20image%2020250917234340.png)

Most efficient KV database, used by uber in production as backend for Riak, Each node of Riak has an instances of Bitcask running

Riak ~ wrapper on top of Bitcask, helps in distributed features for Bitcask.


Exercise

- implement Riak/Bitcask
- read the paper on bitcask