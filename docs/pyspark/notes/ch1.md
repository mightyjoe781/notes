# What is Apache Spark ?

Apache Spark is a *unified computing engine* and *set of libraries for parallel data processing* on computer clusters.

Spark supports multiple programming languages (Python, Java, Scala, and R)

## Apache Spark’s Philosophy

- **Unified** : Spark’s key goal is to offer a unified platform for writing big data applications. Spark supports wide range of data analytics tasks, ranging from simple data loading and SQL queries to ML and streaming computation, over the same computing engine and with a *consistent and composable* set of APIs.
- **Computing Engine** : Spark carefully limits its scope to a computing engine. Spark handles loading data from storage systems and performing computation on it, not permanent storage as the end itself. This allows using it with variety of storage systems like **Azure Storage**, S3, distributed file systems such as **Apache Hadoop**, Key-Value stores like Cassandra and message buses like **Apache Kafka**. Moving data is expensive that is why Spark focuses on performing computation over the data, no matter where it resides.
  - It differs from Apache Hadoop in the way that Hadoop stores data as well as does computation(MapReduce) which were tightly coupled.

- **Libraries** : which builds on its design as a unified engine to provide a unified API for common data analysis tasks. Spark supports both standard libraries that ship with the engine as well as wide array of external libraries published as third-party packages by open-source communities. Spark includes libraries for SQL and structured data (Spark SQL), machine learning (MLlib), stream processing (Spark Streaming and new Structured Streaming), and graph analytics (GraphX).

## Context: The Big Data Problem

- As technology progressed computers became very powerful and throughout years there were multiple applications which improved in speed without any code changes. But all of them were still designed to run single-core. This trend stopped around 2005 when performance plateued due to hard physical limits so industry moved toward multi-core CPUs but application will be required to change in order to faster which set stage for **programming models** such as Apache Spark.
- On top of that storage became cheaper and its storage/collection kept increasing so processing it required large, parallel computation often not on one machine but bunch of machines (clusters).

## History of Spark

- Apache Spark began at UC Berkeley in 2009 as the Spark research project, which was first published the following year in a paper entitled [“Spark: Cluster Computing with Working Sets”](https://www.usenix.org/legacy/event/hotcloud10/tech/full_papers/Zaharia.pdf) by Matei Zaharia, Mosharaf Chowdhury, Michael Franklin, Scott Shenker, and Ion Stoica of the UC Berkeley AMPlab.
- Even though Hadoop MapReduce was dominant programming engine at that time and had its share of problems which Spark tried to Tackle.
- In addition, Zaharia had also worked with Hadoop users at UC Berkeley to understand their needs for the platform—specifically, teams that were  doing large-scale machine learning using iterative algorithms that need to make **multiple passes over the data** and loading it on clusters multiple times. MapReduce engine made it both challenging and inefficient to build large applications.

- To address this problem, the Spark team first designed an API based on functional programming that could succinctly **express multistep applications**. The team then implemented this API over a new engine that could perform efficient, in-memory data sharing across computation steps.The team also began testing this system with both Berkeley and external users.  
- Another use case they worked on was interactive data science and ad hoc queries. By simply plugging the Scala interpreter into Spark, the project could provide a highly usable interactive system for running queries on hundreds of machines.
- Later team focused on a “standard library” approach and worked on making its APIs more composable.

## The present and Future of Spark

Spark has been around for a number of years but keeps on growing with interesting projects within ecosystem that keeps pushing boundaries of its application. A new high-level streaming engine, Structured Streaming was introduced in 2016. 

This solved problems for massive-scale data challenges, from tech companies like Uber and Netflix using Spark’s streaming and ML tools, to NASA, CERN and Broad Institute of MIT and Harvard applying Spark to scientific data analysis.

## Running Spark (Pyspark)

https://spark.apache.org/downloads.html

Using Pyspark requires the Spark JARs. The Python packaging for Spark is not intended to replace all of the other use cases.

- Install JARs (pip does that for you)

Alternately use a Docker image which is much easier to use.

````bash
virtualenv .venv
source .venv/bin/activate
pip install pyspark

# Launching Spark # may need to be prefixed with # ./bin/pyspark
pyspark

# Launching Scala Console
spark-shell

# Launching SQL Console
spark-sql
````

````bash
# Clean approach for system wide installation
# NOTE: for mac
brew install openjdk@11 scala python
pip install pyspark

brew install jupyter
# Launch Jupyter
jupyter notebook
````

Let’s create a spark session and test

````python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('example').getOrCreate()

data = [("Java", "20000"), ("Python", "100000"), ("Scala", "3000")]
columns = ["launguage", "user_count"]

df = spark.createDataFrame(data).toDF(*columns)
df.show()
````

