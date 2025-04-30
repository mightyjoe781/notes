# Big Data Processing

* When one machine is not enough to process the data, we divide & conquer
* Companies use it to process massive amounts of data and extract insights out of it, train ML models, move data across database, ETL, etc.
* All these fancy processing on commodity hardware

### Count Word Frequency

* Given a 1 TB text dataset find frequency of each work
* Approach 1 : load data on a machine, read character by character, update the counter. But its slow.
* Approach 2 : Implement parallel processing but you are still limited by space & cpu constraints
* Approach 3 : We can easily distribute this tasks to multiple machines, and later on just sum up each individual results.

Spark(Big-Data Tool) provides a co-ordinator which actually co-ordinates all the nodes.

More : [Spark Architecture](https://notes.minetest.in/pyspark/notes/ch15/)

