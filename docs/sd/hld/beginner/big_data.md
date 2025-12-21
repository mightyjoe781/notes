# Big Data

>    Big data is not about data size, it’s about extracting value.

When one machine is not enough to process the data, we distribute processing over several machines and combine their results to get final result.

This process in fundamental in all kinds of Big Data Processing, useful in extracting insights from the data, train Machine Learning Models, move data across databases and much more.

When too much data needs to be processed quickly we use Big Data Tools, done on commodity hardwares and readily available by various cloud vendors.

### Example Word Frequency

Given a 1 TB text dataset find frequency of each word.

Approach 1 : Simple

- load data on one machine [disk]
- read it character by character
- when space is encountered, update the in-mem hash table, increase count.

This is a simple approach that runs in $O(n)$ time approx., But because one machine is doing this it will take a long time. We can parallelize it using threads.

Approach 2 : Threads

* Parallelize the code
* Each thread can handle a chunk of the file
* we can wait for all threads to join and compute total sum from cnt of thread.

But what if the dataset is not 1TB but 100TB ?

* this file will not fit in single machine, even if it did, it would be very slow to compute this threads are bounded by timeshare provided by each CPU, limited computation capability of the underlying hardware.

* Instead of one machine, we can distribute the workload across (often smaller) machines and utilize their parallelism to compute the result.

Approach 3 : Distributed Computing

* More computers, more cpu, more processing
* Idea: Split the file into `partitions`, distribute the partition across all servers and let each server compute word frequency independently and send the result to the cluster co-ordinator which merges the result and returns final answer

![](assets/Pasted%20image%2020251221211833.png)

Challenges with this approach

* What about failures 
* What about completions

Big Data Tools manages the complexity for us, leaving business logic to users. Ex- Spark, Snowflake

* distribute across machines
* knowing which machines are doing what
* retry in case of failures
* reprocessing in case of partial or failed jobs
* cleaning up the resources once entire job is completed.

Examples:

* combine user, order, payments and logistics DBs and put the result in AWS Redshift.
* When any activity is happening, events are streamed to kafka. In realtime enrich the events and put them in analytic DB to track in realtime.


