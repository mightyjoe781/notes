# Pyspark Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: pyspark
This is part 1 of 1 parts

---

## File: pyspark/index.md

# Pyspark

Credits : Following notes are learnings from *Spark: The Definitive Guide by Bill Chambers and Matei Zaharia*

- Overview of Big Data and Spark
   1. [What is Apache Spark ?](notes/ch1.md)
   2. [A Gentle Introduction to Spark](notes/ch2.md)
   3. [A Tour of Spark’s Toolset](notes/ch3.md)
- Structured APIs - DataFrames, SQL And Datasets
   1. [Structured API Overview](notes/ch4.md)
   2. [Basic Structured Operations](notes/ch5.md)
   3. [Working With Different Types of Data](notes/ch6.md)
   4. [Aggregations](notes/ch7.md)
   5. [Joins](notes/ch8.md)
   6. [Data Sources](notes/ch9.md)
   7. [Spark SQL](notes/ch10.md)
   8. [Datasets](notes/ch11.md)

Till this its probably enough to learn 80% of pyspark and people can head dive into the pyspark easily.

- Low-Level APIs
  1. [Resilient Distributed Datasets](notes/ch12.md)
  2. [Advanced RDDs](notes/ch13.md)
  3. [Distributed Shared Variables](notes/ch14.md)

This shoud be performed practically with a running spark cluster and probably book is best place to read this.

- Production Applications
  1. [How Spark Runs on a Cluster](notes/ch15.md)
  2. [Developing Spark Applications](notes/ch16.md)
  3. [Deploying Spark](notes/ch17.md)
  4. [Monitoring and Debugging](notes/ch18.md)
  5. [Performance Tuning](notes/ch19.md)

You should take a look at *Apache Flink* as well for Streaming Solutions.

- Streaming
  1. [Stream Processing Fundamentals](notes/ch20.md)
  2. [Structured Streaming Basics](notes/ch21.md)
  3. [Event Time And Stateful Processing](notes/ch22.md)
  4. [Structured Streaming in Production](notes/ch23.md)

For Running Machine Learning Workloads on Spark. There is a dedicate guide for ML on the site.

- Advanced Analytics and Machine Learning
  1. [Advanced. Analytics and Machine Learning Overview](notes/ch24.md)
  1. [Preprocessing and Feature Engineering](notes/ch25.md)
  1. [Classification](notes/ch26.md)
  1. [Regression](notes/ch27.md)
  1. [Recommendation](notes/ch28.md)
  1. [Unsupervised Learning](notes/ch29.md)
  1. [Graph Analytics](notes/ch30.md)
  1. [Deep Learning](notes/ch31.md)
- Ecosystem
  1. [Language Specifics: Python (pyspark) and R (SparkR and Sparklyr)](notes/ch32.md)
  1. [Ecosystem and Community](notes/ch33.md)

## Books

- [Learning Spark 2.0](https://pages.databricks.com/rs/094-YMS-629/images/LearningSpark2.0.pdf)

---

## File: pyspark/notes/ch1.md

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



---

## File: pyspark/notes/ch10.md

# Spark SQL

- Spark SQL can run SQL queries against views or tables organized into databases.
- We can define UDFs and analyze query plans in order to optimize their workload
- If some of data manipulation are Spark SQL and others are in DataFrames, they still compile to same underlying code.

## What is SQL

- Structured Query Language is domain-specific language for expressing relational operations over data.
- SQL is everywhere, and even though tech pundits prophesized its death, its an extremely resilient data tool that many businesses depend on.
- Spark implements a subset of ANSI SQL 2003

## Big Data and SQL: Apache Hive

- Before Spark, Hive was de facto big data SQL access layer.
- developed at Facebook
- It helped propel Hadoop into different industries because analysts could run SQL Queries.

## Big Data and SQL: Spark SQL

- With Spark 2.0 release, its authors created a superset of Hive’s support, writing a native SQL parser that supports both ANSI-SQL as well as HiveQL queries.
- SQL analysts can now take advantage of Spark’s computation abilities by  plugging into the Thrift Server or Spark’s SQL interface, whereas data engineers and scientists can use Spark SQL where appropriate in any data flow. This unifying API allows for data to be extracted with SQL, manipulated as a DataFrame, passed into one of Spark MLlibs’ large-scale machine learning algorithms, written out to another data source, and everything in between.

### Spark’s Relationship to Hive

- Spark SQL has a great relationship with Hive because it can connect to Hive metastores. The Hive metastore is the way in which Hive maintains table information for use across sessions.

#### The Hive Metastore

- To connect to Hive metastore, there are several properties required
  - Metastore version
  - Metstore jars
  - Shared Prefixes: Proper Class prefixes in order to communicate with different databases

## How to run Spark SQL Queries

Spark SQL Interfaces :

### Spark SQL CLI

````bash
./bin/spark-sql
# ./bin/spark-sql --help
````

### Spark Programmatic SQL Interface

`````sql
spark.sql("SELECT 1 + 1").show()	# return a dataframe executed lazily
`````

### SparkSQL Thrift JDBC/ODBC Server

- Spark provides JDBC interface by which a remote program can connect to Spark driver in order to execute Spark SQL queries.
- We can connect business softwares lik Tableau to Spark.

````bash
# start JDBC/ODBC server
./sbin/start-thriftserver.sh

# starting with some hive metastore
./sbin/start-thriftserver.sh \
  --hiveconf hive.server2.thrift.port=<listening-port> \
  --hiveconf hive.server2.thrift.bind.host=<listening-host> \
  --master <master-uri>
  ...
````

To test connection to this server

````bash
./bin/beeline
beeline> !connect jdbc:hive2://localhost:10000
````

## Catalog

- highest level of abstraction for storage of metadata about the data stored in your tables as well other helpful things like databases, tables, functions, and views
- The catalog is available in the `org.apache.spark.sql.catalog.Catalog` package

## Tables

- Tables are logically equivalent to a DataFrame in that they are structure of data against which you run commands.
- NOTE: Spark 2.x, *tables* always contain data. There is no notion of temporary table, only a view, which doesn't contain data. This is important because if you go to drop a table, you can risk losing the data when doing so.

### Spark Managed Tables

- Tables store two pieces of information : data and metadata about itself.
- Spark can manage the metadata for a set of files as well as data about tables.
- When you define a table from files on disk, you are defining an unmanaged table. When you use `saveAsTable` on a DataFrame, you are creating a managed table for which Spark will track of all of the relevant information.
- Finding tables in a database : `show tables IN databaseName`

### Creating Tables

- Spark has unique capability of reusing the entire Data Source API within SQL

````sql
CREATE TABLE flights (
  DEST_COUNTRY_NAME STRING, ORIGIN_COUNTRY_NAME STRING, count LONG)
USING JSON OPTIONS (path '/data/flight-data/json/2015-summary.json')
````



````sql
-- tables with column comments

CREATE TABLE flights_csv (
  DEST_COUNTRY_NAME STRING,
  ORIGIN_COUNTRY_NAME STRING COMMENT "remember, the US will be most prevalent",
  count LONG)
USING csv OPTIONS (header true, path '/data/flight-data/csv/2015-summary.csv')

-- creating table from a query
CREATE TABLE flights_from_select USING parquet AS SELECT * FROM flights
````

````sql
-- controlling layout of data
CREATE TABLE partitioned_flights USING parquet PARTITIONED BY (DEST_COUNTRY_NAME)
AS SELECT DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME, count FROM flights LIMIT 5
````

### Creating External Tables

- spark is completely compatible with Hive SQL

````sql
CREATE EXTERNAL TABLE hive_flights (
  DEST_COUNTRY_NAME STRING, ORIGIN_COUNTRY_NAME STRING, count LONG)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LOCATION '/data/flight-data-hive/'

-- on an select query
CREATE EXTERNAL TABLE hive_flights_2
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/data/flight-data-hive/' AS SELECT * FROM flights
````

### Inserting into Tables

```sql
-- standard sql syntax
INSERT INTO flights_from_select
  SELECT DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME, count FROM flights LIMIT 20

-- partition spec for putting data in specific partition
INSERT INTO partitioned_flights
  PARTITION (DEST_COUNTRY_NAME="UNITED STATES")
  SELECT count, ORIGIN_COUNTRY_NAME FROM flights
  WHERE DEST_COUNTRY_NAME='UNITED STATES' LIMIT 12
```

### Describing Table Metadata

````sql
DESCRIBE TABLE flights_csv

SHOW PARTITIONS partitioned_flights
````

### Refreshing Table Metadata

````sql
# refreshes all cached entries associated with table
REFRESH table partitioned_flights

# collects new partition information
MSCK REPAIR TABLE partitioned_flights
````

### Dropping Tables

*Dropping a managed table deletes the data in the table, so you need to be very careful when doing this.*

````sql
DROP TABLE flights_csv;

DROP TABLE IF EXISTS flights_csv;
````

- for unmanaged tables (Hive), no data will be removed but we will no longer be able to refer to this data by table name.

### Caching Tables

```sql
CACHE TABLE flights
UNCACHE TABLE flights
```

## Views

- View specifies a set of transformations on top of an existing table - basically saved query plans which can be convenient for organizing or reusing your query logic.
- Views can be global, set to a database or per session

### Creating Views

````sql
CREATE VIEW just_usa_view AS
  SELECT * FROM flights WHERE dest_country_name = 'United States'
  
-- views limited to current session
CREATE TEMP VIEW just_usa_view_temp AS
  SELECT * FROM flights WHERE dest_country_name = 'United States'
  
-- global temp view
CREATE GLOBAL TEMP VIEW just_usa_global_view_temp AS
  SELECT * FROM flights WHERE dest_country_name = 'United States'
````

````sql
SHOW TABLES
````

````sql
-- overwriting views
CREATE OR REPLACE TEMP VIEW just_usa_view_temp AS
  SELECT * FROM flights WHERE dest_country_name = 'United States'
````

Execution plan of Views and DataFrames

````sql
val flights = spark.read.format("json")
  .load("/data/flight-data/json/2015-summary.json")
val just_usa_df = flights.where("dest_country_name = 'United States'")
just_usa_df.selectExpr("*").explain


-- sql
EXPLAIN SELECT * FROM just_usa_view 	-- or
EXPLAIN SELECT * FROM flights WHERE dest_country_name = 'United States'
````

### Dropping Views

- dropping a view doesn’t remove any data

```sql
DROP VIEW IF EXISTS just_usa_view;
```

## Databases

- tools for organizing tables
- if not defined spark uses default databases

````sql
SHOW DATABASES

-- Creating Databases
CREATE DATABASE some_db

-- setting the DataBase
USE some_db

-- list all tables in db
SHOW tables

SELECT * FROM flight	-- fail with table/view not found

-- query from other database
SELECT * FROM default.flights

-- check current database
SELECT current_database()

-- switching database
USE default;

-- dropping a database
DROP DATABASE IF EXISTS some_db;
````

## Select Statements

- ANSI SQL requirements of SELECT works

````sql
SELECT [ALL|DISTINCT] named_expression[, named_expression, ...]
    FROM relation[, relation, ...]
    [lateral_view[, lateral_view, ...]]
    [WHERE boolean_expression]
    [aggregation [HAVING boolean_expression]]
    [ORDER BY sort_expressions]
    [CLUSTER BY expressions]
    [DISTRIBUTE BY expressions]
    [SORT BY sort_expressions]
    [WINDOW named_window[, WINDOW named_window, ...]]
    [LIMIT num_rows]

named_expression:
    : expression [AS alias]

relation:
    | join_relation
    | (table_name|query|relation) [sample] [AS alias]
    : VALUES (expressions)[, (expressions), ...]
          [AS (column_name[, column_name, ...])]

expressions:
    : expression[, expression, ...]

sort_expressions:
    : expression [ASC|DESC][, expression [ASC|DESC], ...]
````

### Conditional SQL Operations

- SQL changes based on some condition i.e. `case...when...then...end`

````sql
SELECT
  CASE WHEN DEST_COUNTRY_NAME = 'UNITED STATES' THEN 1
       WHEN DEST_COUNTRY_NAME = 'Egypt' THEN 0
       ELSE -1 END
FROM partitioned_flights
````

## Advanced Topics

### Complex Types

- Incredibly powerful feature that does not exist in standard SQL.

#### Structs

- more akin to maps, providing a way of creating or querying nested data in Spark.

````sql
CREATE VIEW IF NOT EXISTS nested_data AS
  SELECT (DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME) as country, count FROM flights
````

````sql
SELECT * FROM nested_data
SELECT country.DEST_COUNTRY_NAME, count FROM nested_data	-- notice dot syntax\

-- selection all subvalues from a struct
SELECT country.*, count FROM nested_data
````

#### Lists

- `collect_list` function, which creates a list of values.

````sql
SELECT DEST_COUNTRY_NAME as new_name, collect_list(count) as flight_counts,
  collect_set(ORIGIN_COUNTRY_NAME) as origin_set
FROM flights GROUP BY DEST_COUNTRY_NAME

SELECT DEST_COUNTRY_NAME, ARRAY(1, 2, 3) FROM flights

-- accessing using python like syntax
SELECT DEST_COUNTRY_NAME as new_name, collect_list(count)[0]
FROM flights GROUP BY DEST_COUNTRY_NAME

-- converting array's back to rows using explode
-- new view
CREATE OR REPLACE TEMP VIEW flights_agg AS
  SELECT DEST_COUNTRY_NAME, collect_list(count) as collected_counts
  FROM flights GROUP BY DEST_COUNTRY_NAME
  
-- explode
SELECT explode(collected_counts), DEST_COUNTRY_NAME FROM flights_agg
````

### Functions

````sql
-- list of functions
SHOW FUNCTIONS

-- system/user functions
SHOW SYSTEM FUNCTIONS
SHOW USER FUNCTIONS

-- filtering functions
SHOW FUNCTIONS "s*";

SHOW FUNCTIONS LIKE "collect*"
````

### Subqueries

- Queries within other queries
- In Spark, there are two fundamental subqueries.
  - Correlated Subqueries : some information from outer scope of the query
  - Uncorrelated subqueries : no information from the outer scope
- Each of these query can return on (scalar subquery) or more values. Spark supports predicate subqueries, allowing filtering based on views.

#### Uncorrelated predicate subqueries

````sql
-- composed of two uncorrelated queries
-- top 5 country destinations
SELECT dest_country_name FROM flights
GROUP BY dest_country_name ORDER BY sum(count) DESC LIMIT 5
+-----------------+
|dest_country_name|
+-----------------+
|    United States|
|           Canada|
|           Mexico|
|   United Kingdom|
|            Japan|
+-----------------+

-- we can put this query inside another filter
SELECT * FROM flights
WHERE origin_country_name IN (SELECT dest_country_name FROM flights
      GROUP BY dest_country_name ORDER BY sum(count) DESC LIMIT 5)
````

#### Correlated predicate subqueries

- allows to use information from the outer scope in inner query
- `EXISTS` just checks for some existence in the subquery and returns true if there is a value.

````sql
-- to check if there is flight to take you back home, round way trip
SELECT * FROM flights f1
WHERE EXISTS (SELECT 1 FROM flights f2
            WHERE f1.dest_country_name = f2.origin_country_name)
AND EXISTS (SELECT 1 FROM flights f2
            WHERE f2.dest_country_name = f1.origin_country_name)
````

#### Uncorrelated scalar queries

```sql
SELECT *, (SELECT max(count) FROM flights) AS maximum FROM flights
```

## Miscellaneous Features

### Configurations

| Property Name                                  | Default            | Meaning                                                      |
| ---------------------------------------------- | ------------------ | ------------------------------------------------------------ |
| `spark.sql.inMemoryColumnarStorage.compressed` | `true`             | When set to true, Spark SQL automatically selects a compression codec for each column based on statistics of the data. |
| `spark.sql.inMemoryColumnarStorage.batchSize`  | 10000              | Controls the size of batches for columnar caching. Larger batch sizes can improve memory utilization and compression, but risk `OutOfMemoryError`s (OOMs) when caching data. |
| `spark.sql.files.maxPartitionBytes`            | 134217728 (128 MB) | The maximum number of bytes to pack into a single partition when reading files. |
| `spark.sql.files.openCostInBytes`              | 4194304 (4 MB)     | The estimated cost to open a file, measured by the number of bytes that  could be scanned in the same time. This is used when putting multiple  files into a partition. It is better to overestimate; that way the  partitions with small files will be faster than partitions with bigger  files (which is scheduled first). |
| `spark.sql.broadcastTimeout`                   | 300                | Timeout in seconds for the broadcast wait time in broadcast joins. |
| `spark.sql.autoBroadcastJoinThreshold`         | 10485760 (10 MB)   | Configures the maximum size in bytes for a table that will be broadcast to all  worker nodes when performing a join. You can disable broadcasting by  setting this value to -1. Note that currently statistics are supported  only for Hive Metastore tables for which the command `ANALYZE TABLE COMPUTE STATISTICS noscan` has been run. |
| `spark.sql.shuffle.partitions`                 | 200                | Configures the number of partitions to use when shuffling data for joins or aggregations. |

### Setting Configuration Values in SQL

````sql
SET spark.sql.shuffle.partitions=20
````



---

## File: pyspark/notes/ch11.md

# Datasets

- foundational type of Structured APIs and strictly JVM language feature that work only in Scala or Java.
- using datasets we define objects that each row in Dataset consist of. In Scala this will be a case class object that essentially defines a schema that you can use, and in Java, you will define a Bean.
- To efficiently support domain-specific objects, a special concept called an “Encoder” is required. The encoder maps the domain-specific type T  to Spark’s internal type system.

## When to Use Datasets

- since Datasets are costly and come with performance penalty, then why use them at all ? Reasons to use :
  - When the operation(s) cannot be expressed using DataFrame Manipulations
  - When we want or need type-safety, and willing to trade performance for it
- e.g. A large set of business logic that needs to encoded in one specific function
- Another use it to reuse a variety of transformations of entire rows between single-node workloads and Spark workloads

## Creating Datasets

- manual operation, requires prior knowledge of schema ahead of time

### In Java: Encoders

````java
import org.apache.spark.sql.Encoders;

public class Flight implements Serializable{
  String DEST_COUNTRY_NAME;
  String ORIGIN_COUNTRY_NAME;
  Long DEST_COUNTRY_NAME;
}

Dataset<Flight> flights = spark.read
  .parquet("/data/flight-data/parquet/2010-summary.parquet/")
  .as(Encoders.bean(Flight.class));
````

### In Scala : Case Classes

- `case class` is a regular class with characterstics
  - immutable
  - Decomposable through pattern matching
  - allows for comparison based on structure instead of reference
  - easy to use and manipulate

````scala
case class Flight(DEST_COUNTRY_NAME: String,
                  ORIGIN_COUNTRY_NAME: String, count: BigInt)

val flightsDF = spark.read
  .parquet("/data/flight-data/parquet/2010-summary.parquet/")
val flights = flightsDF.as[Flight]
````

## Actions

It is important to understand actions like `collect`, `take` and `count` apply to whether we are using Datasets or DataFrames

````scala
flights.show(2)

+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|            Romania|    1|
|    United States|            Ireland|  264|
+-----------------+-------------------+-----+
````

## Transformations

- transformations are similar to a dataframe.

### Filtering

````scala
def originIsDestination(flight_row: Flight): Boolean = {
  return flight_row.ORIGIN_COUNTRY_NAME == flight_row.DEST_COUNTRY_NAME
}

flights.filter(flight_row => originIsDestination(flight_row)).first()
````

### Mapping

````scala
// manipulate our dataset to extract one value from each row
// effectively similar to select on DataFrame

val destinations = flights.map(f => f.DEST_COUNTRY_NAME)	// Dataset of Type String
````

## Joins

- joins are also similar, but dataset also provide more sophisticated method `joinWith`
- `joinWith` is roughly equal to a co-group (in RDD terminology), basically nested Datasets inside of one.

````scala
case class FlightMetadata(count: BigInt, randomData: BigInt)

val flightsMeta = spark.range(500).map(x => (x, scala.util.Random.nextLong))
  .withColumnRenamed("_1", "count").withColumnRenamed("_2", "randomData")
  .as[FlightMetadata]

val flights2 = flights
  .joinWith(flightsMeta, flights.col("count") === flightsMeta.col("count"))

flights2.selectExpr("_1.DEST_COUNTRY_NAME")
flights2.take(2)
// Array[(Flight, FlightMetadata)] = Array((Flight(United States,Romania,1),...
````

## Grouping and Aggregations

- all previous discussion of `groupBy`, `rollup` and `cube` still apply

````scala
flights.groupBy("DEST_COUNTRY_NAME").count()

flights.groupByKey(x => x.DEST_COUNTRY_NAME).count()
````



---

## File: pyspark/notes/ch12.md

# Resilient Distributed Datasets (RDDs)

- Almost in all scenarios you must prefer Spark’s Structured APIs.
- Only in some cases we might need Spark’s low-level APIs, especially RDDs, the Spark Context, and distributed *shared variables* like accumulators and broadcast variables.

## What Are the Low-Level APIs

There are two sets of low-level APIs

- manipulating distributed data (RDDs)
- distributing and manipulating shared variables (broadcast variables and accumulators)

#### When to Use Low-Level APIs

You should use low-level APIs in following 3 situations

- You need a functionality that is not provided by higher-level APIs, maybe controls over data placement across cluster
- Maintain some legacy codebase written using RDDs
- Custom shared variable manipulation

We might need to drop down to these APIs to use some legacy code, implement custom data partitioner, or update and track shared variables over pipeline. These tools give more-fine grained control at the *expense of safeguarding yourself from shooting in your foot.*

#### How to Use the Low-Level APIs

A `SparkContext` is entry point for low-level APIs and can be accessed throught the `SparkSession`

## About RDDs

- All code (DataFrames, Datasets, ..) we run eventually compiles down to RDDs
- RDD represents an immutable, partitioned collection of records that can be operated on in parallel. In DataFrames each record was a row containing fields of type schema but here it could be any arbitrary Java, Python, objects.
- They come at cost of implementing everything from scratch and optimizing yourself.
- The RDD API is similar to the `Dataset`, which we saw in the  previous part of the book, except that RDDs are not stored in, or  manipulated with, the structured data engine.

### Types of RDDs

- Therre are lots of subclass of RDD. Generally you are going to use mainly two : `generic` RDD type or `key-value` RDD (provides aggregation by key).
- RDD is characterized by 5 main properties
  - A list of partition
  - A function for computing each split
  - A list of dependencies on other RDDs
  - Optionally, `Partitioner` for key-value RDDs (mostly the reason to use RDDs)
  - Optionally, a list of preffered location on which to compute each split.
- RDDs provide all Spark Paradigms like *transformations*, *lazy evaluations*, *actions*. However there is no concept of *Rows* in RDDs, individual records are just objects.
- NOTE: Python loses substancial amount of performance when using RDDs, as effectively similar to running UDFs row by row. In python there are now raw objects instead, serialize data to Python process, operate to it in Python and deserialize data back again for JVM.

### When to Use RDDs

- for vast variety of use cases, DataFrames will be more effecient, more stable and expressive.
- You should not manually create RDDs (unless very specific need), they trade off partitioning power for optmisations that are in Structured APIs

### Datasets and RDDs of Case Classes

- difference between RDDs of Case Classes and Datasets? : The difference is that Datasets can still take advantage of the wealth  of functions and optimizations that the Structured APIs have to offer.

## Creating RDDs

#### Interoperating Between DataFrames, Datasets, and RDDs

````python
# in Scala: converts a Dataset[Long] to RDD[Long]
spark.range(500).rdd

# in Python
spark.range(10).rdd
spark.range(10).rdd.toDF()	# back to DF


# extracting data from Row Type
# Scala: spark.range(10).toDF().rdd.map(rowObject => rowObject.getLong(0))
spark.range(10).toDF("id").rdd.map(lambda row: row[0])
````

#### From Local Collection

````python
myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple".split(" ")
words = spark.sparkContext.parallelize(myCollection, 2)

# naming it so its visible in Spark UI
words.setName("myWords")
words.name() # myWords
````

#### From Data Sources

- NOTE: RDDs do not have notion of Data Sources APIs like DataFrames, they primarily define their dependency structures and lists of partitions.

````python
spark.sparkContext.textFile("/some/path/withTextFiles")
spark.sparkContext.wholeTextFiles("/some/path/withTextFiles")
````

## Manipulating RDDs

You manipulate RDDs in much the same way that you manipulate DataFrames. As mentioned, the core difference being that you manipulate raw Java or Scala objects instead of Spark types. There is also a dearth of “helper” methods or functions that you can draw upon to simplify calculations.

## Transformation

### Distinct

````python
# Remove duplicates from RDDs
words.distinct().count()
````

### filter

````python
# This function returns a Boolean type to be used as a filter function.
def startsWithS(individual):
  return individual.startswith("S")
words.filter(lambda word: startsWithS(word)).collect()
````

### map

````python
# map the current word to the word, its starting letter, and whether the word begins with “S.”
words2 = words.map(lambda word: (word, word[0], word.startswith("S")))

# filter
words2.filter(lambda record: record[2]).take(5)
# returns tuple ("Spark", "S" ,true") , ...
````

#### flatMap

````python
# Sometimes, each current row should return multiple rows
# flatMap requires that the ouput of the map function be an iterable that can be expanded

words.flatMap(lambda word: list(word)).take(5)
````

### sort

````python
words.sortBy(lambda word: len(word) * -1).take(2)
````

### Random Splits

````python
fiftyFiftySplit = words.randomSplit([0.5, 0.5])	# returns an array of RDDs
````

## Actions

### reduce

````python
# reduce an RDD of any kind of value to one value
spark.sparkContext.parallelize(range(1, 21)).reduce(lambda x, y: x + y) # 210

# get longest word in set of words
def wordLengthReducer(leftWord, rightWord):
  if len(leftWord) > len(rightWord):
    return leftWord
  else:
    return rightWord

words.reduce(wordLengthReducer)
````

Because the `reduce` operation on the partitions is not deterministic, you can have either  “definitive” or “processing” (both of length 10) as the “left” word.  This means that sometimes you can end up with one, whereas other times  you end up with the other.

### count

````python
words.count()
````

### countApprox

````python
# This is an approximation of the count method we just looked at, but it must execute within a timeout (and can return incomplete results if it exceeds the timeout).

val confidence = 0.95
val timeoutMilliseconds = 400
words.countApprox(timeoutMilliseconds, confidence)
````

### countApproxDistinct

There are two implementations of this, both based on streamlib’s  implementation of “HyperLogLog in Practice: Algorithmic Engineering of a State-of-the-Art Cardinality Estimation Algorithm.”

````python
# In the first implementation, the argument we pass into the function is the relative accuracy
words.countApproxDistinct(0.05)
# second, you specify the relative accuracy based on two parameters: one for “regular” data and another for a sparse representation.
words.countApproxDistinct(4, 10)
````

### countByValue

````python
# counts the number of values in a given RDD
words.countByValue()
````

- However, it counts by finally loading the result set into the memory of the driver. You should use this method only if the resulting map is  expected to be small because the entire thing is loaded into the  driver’s memory

### countByValueApprox

````python
# similar to above with confidence interval [0,1]
words.countByValueApprox(1000, 0.95)
````

### first

````python
words.first()
````

### max and min

```python
spark.sparkContext.parallelize(1 to 20).max()
spark.sparkContext.parallelize(1 to 20).min()
```

### take

`take` and its derivative methods take a number of values from your RDDs. This works by first scanning one partition and then using the results  from that partition to estimate the number of additional partitions  needed to satisfy the limit.

There are many variations on this function, such as `takeOrdered`, `takeSample`, and `top`.

````python
words.take(5)
words.takeOrdered(5)
words.top(5)
val withReplacement = true
val numberToTake = 6
val randomSeed = 100L
words.takeSample(withReplacement, numberToTake, randomSeed)
````

## Saving Files

Saving files means writing to plain-text files. With RDDs, you cannot actually “save” to a data source in the conventional sense. You must iterate  over the partitions in order to save the contents of each partition to  some external database.

### saveAsTextFile

````scala
words.saveAsTextFile("file:/tmp/bookTitle")
// we can use a compression codec as well

// in Scala
import org.apache.hadoop.io.compress.BZip2Codec
words.saveAsTextFile("file:/tmp/bookTitleCompressed", classOf[BZip2Codec])
````

### Sequence Files

Spark originally grew out of the Hadoop ecosystem, so it has a fairly tight integration with a variety of Hadoop tools. A `sequenceFile` is a flat file consisting of binary key–value pairs. It is extensively used in MapReduce as input/output formats.

````scala
words.saveAsObjectFile("/tmp/my/sequenceFilePath")
````

### Hadoop Files

There are a variety of different Hadoop file formats to which you can save.  These allow you to specify classes, output formats, Hadoop  configurations, and compression schemes.

## Caching

Same principles apply for caching RDDs as for DataFrames and Datasets. We can either cache or persist an RDD

````python
words.cache()
````

We can specify a storage level as any of the storage levels in the singleton object: `org.apache.spark.storage.StorageLevel`, which are combinations of memory only; disk only; and separately, off heap.

````python
words.getStorageLevel()
````

## Checkpointing

One feature not available in the DataFrame API is the concept of *checkpointing*. Checkpointing is the act of saving an RDD to disk so that future  references to this RDD point to those intermediate partitions on disk  rather than recomputing the RDD from its original source.

similar to caching except that it’s not stored in memory, only disk.  This can be helpful when performing iterative computation, similar to  the use cases for caching:

````python
spark.sparkContext.setCheckpointDir("/some/path/for/checkpointing")
words.checkpoint()
````

## Pipe RDDs to System Commands

With `pipe`, you can return an RDD created by piping elements to forked external processes. The resulting RDD is computed by executing the given process once per  partition. All elements of each input partition are written to a process’s stdin as lines of input separated by a newline. The resulting partition consists of the process’s stdout output, with each line of stdout resulting in one element of the output partition. A process is invoked even for empty partitions.

The print behavior can be customized by providing two functions.

```python
words.pipe("wc -l").collect()
```

### mapPartitions

- spark operates on a per-partition basis when it comes to actually executing code. Notice return signature of `map` function on an RDD is actually `MapPartitionsRDD`. `map` is just a row-wise alias for `mapPartitions` which makes it possible for you to map an individual partition.

````python
# example creates the value “1” for every partition in our data, and the sum of the following expression will count the number of partitions we have
words.mapPartitions(lambda part: [1]).sum() # 2
````

This allows us to perform something on an entire subdataset of yours. Ex - we could pipe this though some machine learning algorithm and train an individual model for that company’s portion of the dataset.

```python

def indexedFunc(partitionIndex, withinPartIterator):
  return ["partition: {} => {}".format(partitionIndex,
    x) for x in withinPartIterator]
words.mapPartitionsWithIndex(indexedFunc).collect()
```

### foreachPartition

`foreachPartition` simply iterates over all the partitions of the data without any return value. Good for writing all partitions to database.

````scala
words.foreachPartition { iter =>
  import java.io._
  import scala.util.Random
  val randomFileName = new Random().nextInt()
  val pw = new PrintWriter(new File(s"/tmp/random-file-${randomFileName}.txt"))
  while (iter.hasNext) {
      pw.write(iter.next())
  }
  pw.close()
}
````

### Glom

`glom` takes every partition in your dataset and converts them to arrays. Useful if we are going to collect the data to the driver and want to have an array for each partition. However, this can cause serious stability issues because if you have  large partitions or a large number of partitions, it’s simple to crash  the driver.

````scala
# in Python
spark.sparkContext.parallelize(["Hello", "World"], 2).glom().collect()
# [['Hello'], ['World']]
````



---

## File: pyspark/notes/ch13.md

# Advanced RDDs

- Here we focus on advanced RDD operation and focuses on key-value RDDs, a powerful data manipulation abstraction.

````python
myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple"\
  .split(" ")
words = spark.sparkContext.parallelize(myCollection, 2)
````

## Key-Value Basics (Key-Value RDDs)

- Many `<someoperation>ByKey` methods rely on data to be in key-value format.

````python
# easiest to create key-value pairs
words.map(lambda word: (word.lower(), 1)))
````

### keyBy

````python
# creating key-value pairs using keyBy
keyword = words.keyBy(lambda word: word.lower()[0])
````

### Mapping over Values

- After creating key-value pairs, we can manipulate them, If we have tuple, Spark will assume that the first element is key, the second is the value. When in this format, you can explicitly choose to map-over the values and ignore keys.

````python
keyword.mapValues(lambda word: word.upper()).collect()
````

We can flatMap over row’s values as well.

````python
keyword.flatMapValues(lambda word: word.upper()).collect()
````

### Extracting Keys and Values

````python
keyword.keys().collect()
keyword.values().collect()
````

### lookup

````python
keyword.lookup("s")	# ['Spark', 'Simple']
````

### sampleByKey

there are two ways to sample an RDD by a set of keys. We can do it via an approximation or exactly. Both operations can do so with or without replacement as well as sampling by a fraction by a given key. This is done via simple random sampling with one pass over the RDD, which produces a sample of size  that’s approximately equal to the sum of `math.ceil(numItems * samplingRate)` over all key values

````python
import random
distinctChars = words.flatMap(lambda word: list(word.lower())).distinct()\
  .collect()
sampleMap = dict(map(lambda c: (c, random.random()), distinctChars))
words.map(lambda word: (word.lower()[0], word))\
  .sampleByKey(True, sampleMap, 6).collect()
````

## Aggregation

- we can do aggregation on plain RDDs or on PairRDDs, depending on method we are using

````python
chars = words.flatMap(lambda word: word.lower())	# exploded words
KVcharacters = chars.map(lambda letter: (letter, 1))
def maxFunc(left, right):
  return max(left, right)
def addFunc(left, right):
  return left + right
nums = sc.parallelize(range(1,31), 5)
````

After above we can use `countByKey` which counts the items per each key

````python
KVcharacters.countByKey()
````

### Understanding Aggregation Implementations

There are several ways to create your key–value PairRDDs; however, the implementation is actually quite important for job stability.

#### groupByKey

````python
KVcharacters.groupByKey().map(lambda row: (row[0], reduce(addFunc, row[1])))\
  .collect()
# note this is Python 2, reduce must be imported from functools in Python 3
````

You might think `groupByKey` with a map over each grouping is best way to sum up the counts for each key. However mostly this is wrong approach, fundamental issues here is that executor must hold *all* values for a given key in memory before applying the function to them. We can have `OutOfMemoryErrors`

There is preferred approch mentioned below.

#### reduceByKey

performing a simple count, a much more stable approach is to perform the same `flatMap` and then just perform a `map` to map each letter instance to the number one, and then perform a `reduceByKey` with a summation function in order to collect back the array.

This implementation is much more stable because the reduce happens  within each partition and doesn’t need to put everything in memory.  Additionally, there is no incurred shuffle during this operation;  everything happens at each worker individually before performing a final reduce.

````python
KVcharacters.reduceByKey(addFunc).collect


# Array((d,4), (p,3), (t,3), (b,1), (h,1), (n,2),
...
# (a,4), (i,7), (k,1), (u,1), (o,1), (g,3), (m,2), (c,1))
````

### Other Aggregation Methods

#### aggregate

- This function requires a null and start value and then requires you to specify two different functions. First for aggregates within partitions, and second aggregates across partitions. Start value is used at both levels

````python
nums.aggregate(0, maxFunc, addFunc)
````

NOTE: It might have performance implications as it performs final aggregations on the driver.

````python
# use tree based implemetations for avoiding OutOfMemoryError
depth = 3
nums.treeAggregate(0, maxFunc, addFunc, depth)
````

#### aggregateByKey

````python
# instead of partition we aggregate by key
KVcharacters.aggregateByKey(0, addFunc, maxFunc).collect()
````

#### combineByKey

````python
# Combiner operates on a given key and merges the values according to some function. It 
# then goes to merge the different outputs of the combiners to give us our result.
def valToCombiner(value):
  return [value]
def mergeValuesFunc(vals, valToAppend):
  vals.append(valToAppend)
  return vals
def mergeCombinerFunc(vals1, vals2):
  return vals1 + vals2
outputPartitions = 6
KVcharacters\
  .combineByKey(
    valToCombiner,
    mergeValuesFunc,
    mergeCombinerFunc,
    outputPartitions)\
  .collect()
````

#### foldByKey

`foldByKey` merges the values for each key using an associative function and a neutral  “zero value,” which can be added to the result an arbitrary number of  times, and must not change the result (e.g., 0 for addition, or 1 for  multiplication)

````python
KVcharacters.foldByKey(0, addFunc).collect()
````

## CoGroups

`CoGroups` give ability to gorup together up to three key-value RDDs together in Scala and two in Python. This joins the given values by key.

This is effectively just a group-based join on an RDD. When doing this,  you can also specify a number of output partitions or a custom  partitioning function to control exactly how this data is distributed  across the cluster

````python
import random
distinctChars = words.flatMap(lambda word: word.lower()).distinct()
charRDD = distinctChars.map(lambda c: (c, random.random()))
charRDD2 = distinctChars.map(lambda c: (c, random.random()))
charRDD.cogroup(charRDD2).take(5)
````

## Joins

### Inner Join

````python
# in Python
keyedChars = distinctChars.map(lambda c: (c, random.random()))
outputPartitions = 10
KVcharacters.join(keyedChars).count()
KVcharacters.join(keyedChars, outputPartitions).count()
````

- Other type of Joins
  - fullOuterJoin
  - leftOuterJoin
  - rightOuterJoin
  - cartesian

### zips

The final type of join isn’t really a join at all, but it does combine two RDDs, so it’s worth labeling it as a join. `zip` allows you to “zip” together two RDDs, assuming that they have the same length. This creates a `PairRDD`. The two RDDs must have the same number of partitions as well as the same number of elements

````python
numRange = sc.parallelize(range(10), 2)
words.zip(numRange).collect()

# Output
[('Spark', 0),
 ('The', 1),
 ('Definitive', 2),
 ('Guide', 3),
 (':', 4),
 ('Big', 5),
 ('Data', 6),
 ('Processing', 7),
 ('Made', 8),
 ('Simple', 9)]
````

## Controlling Partitions

With RDDs, you have control over how data is exactly physically distributed  across the cluster. Some of these methods are basically the same from  what we have in the Structured APIs but the key addition (that does not  exist in the Structured APIs) is the ability to specify a partitioning  function (formally a custom `Partitioner`, which we discuss later when we look at basic methods).

### coalesce

`coalesce` effectively collapses partitions on the same worker in order to avoid a shuffle of the data when repartitioning.

````python
words.coalesce(1).getNumPartitions() # 1
````

### repartition

The `repartition` operation allows you to repartition your data up or down but performs a shuffle across nodes in the process. Increasing the number of partitions can increase the level of parallelism when operating in map- and filter-type operations

````python
words.repartition(10) // gives us 10 partitions
````

### repartitionAndSortWithinPartitions

This operation gives you the ability to repartition as well as specify the ordering of each one of those output partitions.

### Custom Partitioning

Custom partitioners are not available in the Structured APIs because  they don’t really have a logical counterpart. They’re a low-level, implementation detail that can have a significant effect on whether your jobs run successfully.

The canonical example to motivate custom partition for this operation is PageRank whereby we seek to control the layout of the data on the  cluster and avoid shuffles. In our shopping dataset, this might mean  partitioning by each customer ID.

In short, the sole goal of custom partitioning is to even out the  distribution of your data across the cluster so that you can work around problems like data skew.

````python
df = spark.read.option("header", "true").option("inferSchema", "true")\
  .csv("/data/retail-data/all/")
rdd = df.coalesce(10).rdd

df.printSchema()
````

Spark has two built-in Partitioners that you can leverage off in the RDD API, a `HashPartitioner` for discrete values and a `RangePartitioner`. These two work for discrete values and continuous values, respectively. Spark’s Structured APIs will already use these, although we can use the same thing in RDDs:

```python
def partitionFunc(key):
  import random
  if key == 17850 or key == 12583:
    return 0
  else:
    return random.randint(1,2)

keyedRDD = rdd.keyBy(lambda row: row[6])
keyedRDD\
  .partitionBy(3, partitionFunc)\
  .map(lambda x: x[0])\
  .glom()\
  .map(lambda x: len(set(x)))\
  .take(5)
```

See the count of results in each partition. The second two numbers will  vary, because we’re distributing them randomly (as you will see when we  do the same in Python) but the same principles apply

## Custom Serialization

- Issue of Kryo serialisation. Any object that you hope to parallelize must be serializable.
- The default serialization can be quite slow. Spark can use the Kryo  library (version 2) to serialize objects more quickly. Kryo is  significantly faster and more compact than Java serialization (often as  much as 10x), but does not support all serializable types and requires  you to register the classes you’ll use in the program in advance for  best performance.
- You can use Kryo by initializing your job with a SparkConf and setting the value of `"spark.serializer"` to `"org.apache.spark.serializer.KryoSerializer"` (we discuss this in the next part of the book). This setting configures the serializer used for shuffling data between worker nodes and  serializing RDDs to disk. The only reason Kryo is not the default is  because of the custom registration requirement, but we recommend trying  it in any network-intensive application.

````scala
// To register your own custom classes with Kryo, use the registerKryoClasses method in scala
val conf = new SparkConf().setMaster(...).setAppName(...)
conf.registerKryoClasses(Array(classOf[MyClass1], classOf[MyClass2]))
val sc = new SparkContext(conf)
````






---

## File: pyspark/notes/ch14.md

# Distributed Shared Variables

- second kind of low-level API in Spark exposes two distributed shared variables: *brodcast varaibles* and *accumulators*. We can use these in UDFs that have special properties when running on a cluster.

## Broadcast Variables

- Broadcast Variables are way you can share an **immutable** value **efficiently** across the cluster without encapsulating that variable in function closure(e.g. in `map`).
- When we use a variable in a closure, it must be deserialized on the worked node many times. Moreover, if you use the same variable in multiple Spark actions and jobs, it will be re-sent to the workers with every job instead of once.
- Broadcast variables are shared, immutable variables that are cached on  every machine in the cluster instead of serialized with every single task.
- Standard use case is to pass around a large lookup table tha fits in memory on the executors and use that in a function

````python
my_collection = "Spark The Definitive Guide : Big Data Processing Made Simple"\
  .split(" ")
words = spark.sparkContext.parallelize(my_collection, 2)

# to supplement list of words with extra information
supplementalData = {"Spark":1000, "Definitive":200,
                    "Big":-300, "Simple":100}

# broadcasting this structure across Spark and referencing it
suppBroadcast = spark.sparkContext.broadcast(supplementalData)
suppBroadcast.value	# reference

# now we can transform our RDD using this value.
words.map(lambda word: (word, suppBroadcast.value.get(word, 0)))\
  .sortBy(lambda wordPair: wordPair[1])\
  .collect()
````

## Accumulators

- way of updating a value inside of a variety of transformations and propagating value to driver node in an efficient and fault-tolerant way.
- Accumulators provide a mutable variable that a Spark cluster can safely update on a per-row basis. You can use these for debugging purposes (say to track the values of a certain variable per partition in order to  intelligently use it over time) or to create low-level aggregation.
- For accumulator updates performed inside ***actions** only*, Spark guarantees that each task’s update to the accumulator will be applied only once, meaning that restarted tasks will not update the value. In ***transformations***, you should be aware that each task’s update can be  applied more than once if tasks or job stages are reexecuted.

- accumulator updates are not guaranteed to be executed when made within a lazy transformation like `map()`.

````python
# read the parquet file
flights = spark.read\
  .parquet("/data/flight-data/parquet/2010-summary.parquet")

# in accumulator to count number of flights from or to china
# this is an unnamed accumulator	# not visible in Spark UI
accChina = spark.sparkContext.accumulator(0)

# declaring a named accumulator for showing in Spark UI
# Scala
val accChina = new LongAccumulator
val accChina2 = spark.sparkContext.longAccumulator("China")
spark.sparkContext.register(accChina, "China")
# end

def accChinaFunc(flight_row):
  destination = flight_row["DEST_COUNTRY_NAME"]
  origin = flight_row["ORIGIN_COUNTRY_NAME"]
  if destination == "China":
    accChina.add(flight_row["count"])
  if origin == "China":
    accChina.add(flight_row["count"])
# iterate over every row in flights database    
flights.foreach(lambda flight_row: accChinaFunc(flight_row))

accChina.value # 953
````

#### Custom Accummulators

Although Spark does provide some default accumulator types, sometimes you might  want to build your own custom accumulator. In order to do this you need  to subclass the `AccumulatorV2` class.

````scala
// in Scala
import scala.collection.mutable.ArrayBuffer
import org.apache.spark.util.AccumulatorV2

val arr = ArrayBuffer[BigInt]()

class EvenAccumulator extends AccumulatorV2[BigInt, BigInt] {
  private var num:BigInt = 0
  def reset(): Unit = {
    this.num = 0
  }
  def add(intValue: BigInt): Unit = {
    if (intValue % 2 == 0) {
        this.num += intValue
    }
  }
  def merge(other: AccumulatorV2[BigInt,BigInt]): Unit = {
    this.num += other.value
  }
  def value():BigInt = {
    this.num
  }
  def copy(): AccumulatorV2[BigInt,BigInt] = {
    new EvenAccumulator
  }
  def isZero():Boolean = {
    this.num == 0
  }
}
val acc = new EvenAccumulator
val newAcc = sc.register(acc, "evenAcc")
````

````scala
// in Scala
acc.value // 0
flights.foreach(flight_row => acc.add(flight_row.count))
acc.value // 31390
````



---

## File: pyspark/notes/ch15.md

# How Spark Runs On A Cluster

## The Architecture of a Spark Application

Review from Chapter 2

- *The Spark Driver* : controller of the execution of spark Application and maintains all the state of Spark Clusters. Interfaces with cluster manager in order to actually get physical resouces and launch executors.
- *The Spark Executors* : processes that perform the tasks assigned by Spark driver and report their state(success/failure) and results.
- *The cluster Manager* : Maintains cluster of machines that will run your Spark Application. Somewhat confusingly, a cluster manager will have its own `driver` and `worker` abstractions which are actually tied to physical machines rather than `process` in Spark.

To run a Spark application, we request resources from cluster manager to run it. Depending on config, this can include a place to run the Spark driver or might be just resources for the executor for our Spark Applications. Over the course of Spark Application execution, the cluster manager will be responsible for managing the underlying machines that our application is running on.

Spark currently supports 3 cluster managers : Apache Mesos, and Hadoop YARN.

### Execution Modes

- determine resources are physically located when we run our application.
- Circle represents daemon processes running on and managing each of individual worker nodes. Rectangles are actual processes running that are submitted.

1. Cluster Mode

Most common way to run Spark Application. User submits a pre-compiled JAR, Python Script, or R script to a cluster Manager. The cluster manager then launches the driver process on a worker node inside the cluster, in addition to the executor processes.

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_1502.png)

2. Client Mode : Same as cluster mode except that Spark driver remains on client machine that submitted the application. This means that the client machine is responsible for maintaining the Spark driver process, and the cluster manager maintains the executor  processses. These machines are commonly referred to as *gateway machines* or *edge nodes*.

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_1503.png)

3. Local Mode : It runs entire Spark Application on a single machine. It achieves parallelism through threads. Common way to learn Spark, test application but not for production application.

## The Life Cycle of a Spark Application (Outside Spark)

### Client Request

- Client submits a pre-compiled JAR/library making request to cluster manager driver. Explicitly asking for resources for *Spark driver process only*. Cluster manager places driver onto a node in cluster. Client exits and application is now on cluster.

### Launch

- Now driver process begins running user code. This code must include *SparkSession* that initialises a Spark Cluster (e.g. driver +executors).
- SparkSession communicates with cluster manager asking to launch Spark executor processes across cluster. These cluster and their numbers are configured based on command-line args during `spark-submit`
- Cluster manager launches executor processes on cluster and send relevent information about their location to driver process.

### Execution

- Now we have a “Spark Cluster,” Spark goes about its merry way executing code. Now driver and executor processes communicate among themselves executing code, moving data. The driver schedules tasks on each worker and workers respond with results and status.

### Completion

- After Spark Application completes, driver exits with either success or failures. The cluster manager shuts down executors in that Spark cluster for the driver. Now we can ask cluster manager about success or failure of Spark Application.

## The Life Cycle of a Spark Application (Inside Spark)

### The SparkSession

- first step of any Spark Application. In many interactive modes this is done automatically but in an application we must do it manually.

````python
# use newer builder method, more robustly instantiates Spark and SQL contexts ensuring
# no context conflict.

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local").appName("Word Count")\
    .config("spark.some.config.option", "some-value")\
    .getOrCreate()
````

### The SparkContext

- A `SparkContext` object within the `SparkSession` represents the connection to spark cluster.This class is how you communicate with some of Spark’s lower-level APIs, such as RDDs. It is commonly stored as the variable `sc` in older examples and documentation. Through a `SparkContext`, you can create RDDs, accumulators, and broadcast variables, and you can run code on the cluster.

````python
from pyspark import SparkContext
sc = SparkContext.getOrCreate()
````

### Logical Instruction

- Spark code consists of transformations and actions. How we build (SparkSQL, RDDs, ML) it its upto us. Understanding how we take declarative instructions like DataFrames and convert them into physical execution plans is an important step to  understanding how Spark runs on a cluster

````python
df1 = spark.range(2, 10000000, 2)
df2 = spark.range(2, 10000000, 4)
step1 = df1.repartition(5)
step12 = df2.repartition(6)
step2 = step1.selectExpr("id * 5 as id")
step3 = step2.join(step12, ["id"])
step4 = step3.selectExpr("sum(id)")

step4.collect() # 2500000000000
````

`step4.explain()`

````txt
== Physical Plan ==
*HashAggregate(keys=[], functions=[sum(id#15L)])
+- Exchange SinglePartition
   +- *HashAggregate(keys=[], functions=[partial_sum(id#15L)])
      +- *Project [id#15L]
         +- *SortMergeJoin [id#15L], [id#10L], Inner
            :- *Sort [id#15L ASC NULLS FIRST], false, 0
            :  +- Exchange hashpartitioning(id#15L, 200)
            :     +- *Project [(id#7L * 5) AS id#15L]
            :        +- Exchange RoundRobinPartitioning(5)
            :           +- *Range (2, 10000000, step=2, splits=8)
            +- *Sort [id#10L ASC NULLS FIRST], false, 0
               +- Exchange hashpartitioning(id#10L, 200)
                  +- Exchange RoundRobinPartitioning(6)
                     +- *Range (2, 10000000, step=4, splits=8)
````

### A Spark Job

- In general there should be one spark job for one action. Actions always return results. Each job breaks into series of stages, the number of which depends on shuffle operations need to take place
- Above job is:
  - Stage 1 with 8 Tasks
  - Stage 2 with 8 Tasks
  - Stage 3 with 6 Tasks
  - Stage 4 with 5 Tasks
  - Stage 5 with 200 Tasks
  - Stage 6 with 1 Task

### Stages

- group of tasks that can be executed together to compute the same operations on multiple machines. Generally Spark tries to pack as much work as possible into same stage, but the engine starts new stages after operations called shuffles.
- A Shuffle represents physical repartitioning of data. For example - sorting a DataFrame, or grouping data that was loaded from a file by key.
- First two stages in above example corresponds to range
- Stage3, 4 perform on each of those DataFrames and end of stage represents the join (a shuffle)
- Suddenly, we have 200 tasks. This is because of a Spark SQL configuration. The `spark.sql.shuffle.partitions` default value is 200, which means that when there is a shuffle  performed during execution, it outputs 200 shuffle partitions by  default.
- A good rule of thumb is that the number of partitions should be larger than the number of executors on your cluster, potentially by multiple  factors depending on the workload. If you are running code on your local machine, it would behoove you to set this value lower because your  local machine is unlikely to be able to execute that number of tasks in  parallel.

### Tasks

- Stages in spark consists of tasks. Each task corresponds to a combination of blocks of data and a transformation that will run on a single executor.
- A task is just a unit of computation applied to a unit of data (the partition). Partitioning your data into a greater number of partitions means that more can be executed in parallel.

## Execution Details

Tasks and Stages have important property. First, Spark automatically *pipelines* stages and tasks that can be done together, such as `map` followed by another `map`. Second, for all shuffle operation, Spark writes the data to stable storage, and can reuse it across multiple jobs.

### Pipelining

An important part of what makes Spark an “in-memory computation tool” is  that unlike the tools that came before it (e.g., MapReduce), Spark  performs as many steps as it can at one point in time before writing  data to memory or disk. One of the key optimizations that Spark performs is *pipelining*, which occurs at and below the RDD level.

With pipelining, any sequence of operations that feed data directly into each other, without needing to move it across nodes, is collapsed into a single stage of tasks that do all the operations together. 

### Shuffle Persistence

When Spark needs to run an operation that has to move data *across* nodes, such as a reduce-by-key operation (where input data for each key needs to first be brought together from many nodes), the engine can’t perform pipelining anymore, and instead it performs a cross-network shuffle.

Spark always executes shuffles by first having the “source” tasks (those sending data) write *shuffle files* to their local disks during their execution stage. Then, the stage that does the grouping and reduction launches and runs tasks that fetch their corresponding records from each shuffle file and performs that computation (e.g., fetches and processes the data for a specific range  f keys). Saving the shuffle files to disk lets Spark run this stage later in time than the source stage (e.g., if there are not enough executors to run both at the same time), and also lets the engine re-launch reduce tasks on failure without rerunning all the input tasks.

One side effect you’ll see for shuffle persistence is that running a new job over data that’s already been shuffled does not rerun the “source” side of the shuffle. Because the shuffle files were already written to disk earlier, Spark knows that it can use them to run the later stages  of the job, and it need not redo the earlier ones. In the Spark UI and logs, you will see the pre-shuffle stages marked as “skipped”. This automatic optimization can save time in a workload that runs multiple jobs over the same data, but of course, for even better performance you can perform your own caching with the DataFrame or RDD `cache` method, which lets you control exactly which data is saved and where.

---

## File: pyspark/notes/ch16.md

# Developing Spark Application

## Writing Spark Applications

Spark Applications are combination of two things : a Spark Cluster and your code.

#### Writing Python Applications

Spark doesn’t have a build concept, just write Python scripts to simple execute against the cluster.

To facilitate code reuse, its common to package multiple Python files into egg or ZIP files of Spark code. To include those files use `--py-files` argument of `spark-submit` to add `.py`, `.zip` or .`egg` files to be distributed with applications.

````python
from __future__ import print_function
# entry point
if __name__ == '__main__':
    from pyspark.sql import SparkSession
    # always share this inside your application rather than instantiating it with every python class.
    spark = SparkSession.builder \
        .master("local") \
        .appName("Word Count") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    print(spark.range(5000).where("id > 500").selectExpr("sum(id)").collect())
````

Running the application : `$SPARK_HOME/bin/spark-submit --master local pyspark_template/main.py`

## Testing Spark Applications

### Strategic Principles

#### Input data resilience

- Being resilient to different kinds of input data is something that is quite fundamental to how you write your data pipelines. Data changes with business requirements, so design your application to handle some degree of change in input data or otherwise handle failures gracefully.

#### Business logic resilience and evolution

- do robust logical testing with realistic data to ensure that you are actually getting what you want.
- Don’t try writing bunch of “Spark Unit Tests” that just test Spark’s functionality, instead focus on testing business logic.

#### Resilience in output and atomicity

- Output Structure of your pipeline is what you expect. This means you will need to gracefully handle ouput schema resolution. Most of the times your Spark pipeline will be feeding other Spark pipelines.

### Tactical Takeaways

The highest value approach is to verify that your business logic is correct by employing proper unit testing and to ensure that you’re  resilient to changing input data or have structured it so that schema evolution will not become unwielding in the future.

#### Managing SparkSessions

- Testing your Spark code using a unit test framework like JUnit or ScalaTest is relatively easy because of Spark’s local mode

- perform dependency injection as much as possible when managing SparkSessions in your code.
- initialize the `SparkSession` only once and pass it around to relevant functions and classes at runtime in a way that makes it easy  to substitute during testing.

#### Which Spark API to Use ?

Right API depends on your team and its needs: some teams and  projects will need the less strict SQL and DataFrame APIs for speed of  development, while others will want to use type-safe Datasets or RDDs.

### Connecting to Unit Testing Frameworks

To unit test your code, we recommend using the standard frameworks in your langage (e.g., JUnit or ScalaTest), and setting up your test harnesses  to create and clean up a SparkSession for each test.

### Connecting to Data Sources

You should make sure your testing code does not connect to production data sources, so that developers can easily run it in isolation if these data sources change.

One easy way to make this happen is to have all your business logic  functions take DataFrames or Datasets as input instead of directly  connecting to various sources; after all, subsequent code will work the  same way no matter what the data source was.

## The Development Process

First, maintain a scratch space, such as an interactive notebook or some equivalent thereof and then as you build key components and algorithms, move them to a more permanent location like a library or package.

When running on your local machine, the `spark-shell` and its various language-specific implementations are probably the best way to develop applications. For the most part, the shell is for interactive applications, whereas `spark-submit` is for production applications on your Spark cluster.

## Launching Applications

- Most Common way to submit application is through `spark-submit`

````python
./bin/spark-submit \
  --class <main-class> \
  --master <master-url> \
  --deploy-mode <deploy-mode> \
  --conf <key>=<value> \
  ... # other options
  <application-jar-or-script> \
  [application-arguments]
````

- Always favour cluster mode to reduce latency between the executors and the driver.

- To enumerate all options yourself, run `spark-submit` with `--help`.

#### Application Launch Examples

````bash
./bin/spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master spark://207.184.161.138:7077 \
  --executor-memory 20G \
  --total-executor-cores 100 \
  replace/with/path/to/examples.jar \
  1000
  
# or

./bin/spark-submit \
  --master spark://207.184.161.138:7077 \
  examples/src/main/python/pi.py \
  1000
````

## Configuring Applications

Majority of configuration fall into following categories

- Application properties
- Runtime environment
- Shuffle behavior
- Spark UI
- Compression and serialization
- Memory management
- Execution behavior
- Networking
- Scheduling
- Dynamic allocation
- Security
- Encryption
- Spark SQL
- Spark streaming
- SparkR

Spark provides three location to configure system :

- Spark properties control most application parameters and can be set by using a `SparkConf` object
- Java system properties
- Hardcoded configuration files

You can find several templates under `/conf` dir of Spark Home. You can configure logging through `log4j.properties`

### SparkConf

The `SparkConf` manages all of our application configurations. You create one via the `import` statement, as shown in the example that follows.

````python
from pyspark import SparkConf
conf = SparkConf().setMaster("local[2]").setAppName("DefinitiveGuide")\
  .set("some.conf", "to.some.value")
````

````python
./bin/spark-submit --name "DefinitiveGuide" --master local[4] ...
````

### Application Properties

- properties set either from spark-submit or while creating application.

| Property name                | Default | Meaning                                                      |
| ---------------------------- | ------- | ------------------------------------------------------------ |
| `spark.app.name`             | (none)  | The name of your application. This will appear in the UI and in log data. |
| `spark.driver.cores`         | `1`     | Number of cores to use for the driver process, only in cluster mode. |
| `spark.driver.maxResultSize` | `1g`    | Limit of total size of serialized results of all partitions for each Spark action (e.g., collect). Should be at least `1M`, or `0` for unlimited. Jobs will be aborted if the total size exceeds this limit. Having a high limit can cause `OutOfMemoryError`s in the driver (depends on `spark.driver.memory` and memory overhead of objects in JVM). Setting a proper limit can protect the driver from `OutOfMemoryError`s. |
| `spark.driver.memory`        | `1g`    | Amount of memory to use for the driver process, where `SparkContext` is initialized. (e.g. `1g`, `2g`). Note: in client mode, this must not be set through the `SparkConf` directly in your application, because the driver JVM has already started at that point. Instead, set this through the `--driver-memory` command-line option or in your default properties file. |
| `spark.executor.memory`      | `1g`    | Amount of memory to use per executor process (e.g., `2g`, `8g`). |
| `spark.extraListeners`       | (none)  | A comma-separated list of classes that implement `SparkListener`; when initializing `SparkContext`, instances of these classes will be created and registered with Spark’s  listener bus. If a class has a single-argument constructor that accepts a `SparkConf`, that constructor will be called; otherwise, a  zero-argument constructor will be called. If no valid constructor can be found, the `SparkContext` creation will fail with an exception. |
| `spark.logConf`              | `FALSE` | Logs the effective `SparkConf` as INFO when a `SparkContext` is started. |
| `spark.master`               | (none)  | The cluster manager to connect to. See the list of allowed master URLs. |
| `spark.submit.deployMode`    | (none)  | The deploy mode of the Spark driver program, either “client” or “cluster,”  which means to launch driver program locally (“client”) or remotely  (“cluster”) on one of the nodes inside the cluster. |
| `spark.log.callerContext`    | (none)  | Application information that will be written into Yarn RM log/HDFS audit log when  running on Yarn/HDFS. Its length depends on the Hadoop configuration `hadoop.caller.context.max`.size. It should be concise, and typically can have up to 50 characters. |
| `spark.driver.supervise`     | `FALSE` | If true, restarts the driver automatically if it fails with a non-zero  exit status. Only has effect in Spark standalone mode or Mesos cluster  deploy mode. |

More description available at : https://spark.apache.org/docs/latest/configuration.html

Runtime Properties : configure the runtime environment of your application

Execution Properties : finer-grained control on actual execution.

Configuring Memory Management : There are times when you might need to manually manage the memory options to try and optimize your applications.

Configuring Shuffle Behaviour : We’ve emphasized how shuffles can be a bottleneck in Spark jobs because of  their high communication overhead. Therefore there are a number of  low-level configurations for controlling shuffle behavior.

### Environment Variables

We can configure Spark settings through environment variables, which are read from the `conf/spark-env.sh`

Following variables can be set :

- `JAVA_HOME` : Location where Java is installed (if it’s not on your default PATH).
- `PYSPARK_PYTHON` : Python binary executable to use for PySpark in both driver and workers (default is `python2.7` if available; otherwise, `python`). Property `spark.pyspark.python` takes precedence if it is set.
- `PYSPARK_DRIVER_PYTHON` : Python binary executable to use for PySpark in driver only (default is `PYSPARK_PYTHON`). Property `spark.pyspark.driver.python` takes precedence if it is set.
- `SPARKR_DRIVER_R` : R binary executable to use for SparkR shell (default is R). Property `spark.r.shell.command` takes precedence if it is set.
- `SPARK_LOCAL_IP` : IP address of the machine to which to bind.
- `SPARK_PUBLIC_DNS` : Hostname your Spark program will advertise to other machines.

### Job Scheduling within an Application

- Witing a given Spark Application, multiple parllel job can be run simulatenously as if they were submitted from separate thread. Spark’s scheduler is fully thread-safe and supports this use case to enable applications that server multiple requests.
- By default scheduler runs in FIFO fashion. If the jobs at the head of the queue don’t need to use the entire  cluster, later jobs can begin to run right away, but if the jobs at the  head of the queue are large, later jobs might be delayed significantly.
- It is also possible to configure fair sharing between jobs. Under fair sharing, Spark assigns tasks between jobs in a round-robin fashion so that all jobs get a roughly equal share of cluster resources. This means that short jobs submitted while a long job is running can begin receiving resources right away and still achieve good response times  without waiting for the long job to finish. This mode is best for multiuser settings.
- To enable the fair scheduler, set the `spark.scheduler.mode` property to `FAIR` when configuring a `SparkContext`.
- The fair scheduler also supports grouping jobs into pools, and setting  different scheduling options, or weights, for each pool. This can be  useful to create a high-priority pool for more important jobs or to  group the jobs of each user together and give users equal shares  regardless of how many concurrent jobs they have instead of giving jobs  equal shares. This approach is modeled after the Hadoop Fair Scheduler.

````python
sc.setLocalProperty("spark.scheduler.pool", "pool1")
````



---

## File: pyspark/notes/ch17.md

# Deploying Spark

We will look at fundamental differences between different types of cluster managers.

## Where to Deploy Your Clusters to Run Spark Applications

There are two high-level options for deploying Spark Cluster: On-premise or public cloud.

### On-Premise Cluster Deployments

- On Premise clusters are sometimes reasonable options for companies already having their own data centres. Although you get full hardware control from this but also becomes challenging to handle clusters of dynamic size. Data Analytics workloads are usually often elastic.
- Secondly many On Premises systems are build around their own storage system like Hadoop file system or scalable key-value store (Cassandra) requiring a lot of extra effort to have replication and extra recovery.
- All of Spark’s cluster managers allow multiple concurrent application but YARN and Mesos have better supports for dynamic sharing and additionally support non-spark workloads.

### Spark in Cloud

- With onset of giants like AWS, Azure, GCP providing fully managed dynamic machines to handle elastic workloads makes them suitable for Spark.
- You should always choose AWS S3, Azure Blob Storage, GCS and sping up resources dynamically for each workload effectively decoupling *storage and compute.*
- Another advantage is public clouds include low-cost, georeplicated storage that makes it easier to manage large amounts of data. 

## Cluster Managers

Spark supports following clusters manager : standalone clusters, Hadoop YARN, and Mesos.

### Standalone Clusters

- lightweight platform built specifically for Apache Spark workloads. Using it, we can run multiple Spark Applications on the same cluster. Provides simple interfaces for scaling workloads.
- Main disadvantage of using it that you can only run Spark.

#### Starting a standalone cluster

- It requires provisioning the machine for doing so. 
- Manual starting cluster by hand : `$SPARK_HOME/sbin/start-master.sh` : this runs master on  a `spark://HOST:PORT` URI. You can also find master’s web UI, which is [*http://master-ip-address:8080*](http://master-ip-address:8080) by default
- Start the worker nodes by logging into each machine and connecting at : `$SPARK_HOME/sbin/start-slave.sh <master-spark-URI>`

#### starting cluster using a script

You can configure cluster launch scripts that can automate the launch of standalone clusters. To do this, create a file called *conf/slaves* in your Spark directory that will contain the hostnames of all the  machines on which you intend to start Spark workers, one per line. If this file does not exist, everything will launch locally. When you go to actually start the cluster, the master machine will access each of the  worker machines via Secure Shell (SSH).

After we setup this file we can start and stop cluster using simple scripts in `sbin`

- `$SPARK_HOME/sbin/start-master.sh`
- `$SPARK_HOME/sbin/start-slaves.sh`
- `$SPARK_HOME/sbin/start-slave.sh`
- `$SPARK_HOME/sbin/start-all.sh`
- `$SPARK_HOME/sbin/stop-master.sh`
- `$SPARK_HOME/sbin/stop-slaves.sh`
- `$SPARK_HOME/sbin/stop-all.sh`

#### Standalone cluster configurations

- helps control everything from what happens to old files on each worker for terminated application to the worker’s core and memory resources.

#### Submitting applications

- we can submit application using `spark://` of master UI or directly on master node itself using `spark-submit`

### Spark on YARN

- Hadoop YARN is a framework for job scheduling and cluster resource management. Even though Spark is often misclassfied as a part of Hadoop Ecosystem, in reality. Spark has little to do with Hadoop.
- Spark natively supports YARN and doesn’t require Hadoop itself.
- You can run spark jobs on Hadoop’s YARN by specifying the master as the YARN in the `spark-submit` command line arguments. Just like with standalone mode, there are multiple knobs to tune it according to what you would like cluster to do.

#### Submitting Application

When submitting applications to YARN, the core difference from other deployments is that `--master` will become `yarn` as opposed the master node IP, as it is in standalone mode. Instead,  Spark will find the YARN configuration files using the environment  variable `HADOOP_CONF_DIR` or `YARN_CONF_DIR`.

### Configuring Spark on YARN Applications

#### Hadoop Configurations

If you plan to read and write from HDFS using Spark, you need to include two Hadoop configuration files on Spark’s classpath: *hdfs-site.xml*, which provides default behaviors for the HDFS client; and *core-site.xml*, which sets the default file system name. The location of these  configuration files varies across Hadoop versions, but a common location is inside of */etc/hadoop/conf*. 

To make these files visible to Spark, set `HADOOP_CONF_DIR` in *$SPARK_HOME/spark-env.sh* to a location containing the configuration files or as an environment variable when you go to `spark-submit` your application.

#### Application properties for YARN

There are a number of Hadoop-related configurations and things that come up that largely don’t have much to do with Spark, just running or securing YARN in a way that influences how Spark runs.

### Spark on Mesos

- Mesos was created by many of original authors of Spark
- Apache Mesos abstracts CPU, memory, storage, and other compute resources away from machines (physical or virtual), enabling fault-tolerant and  elastic distributed systems to easily be built and run effectively.
- Mesos intends to be datacenter scale-cluster manager that manages not just short lived application like Spark, but long-running applications like we application and other interfaces.
- Mesos is the heaviest-weight cluster manager, simply because you might  choose this cluster manager only if your organization already has a  large-scale deployment of Mesos, but it makes for a good cluster manager nonetheless.
- Mesos deprecated fine-grained mode and exclusively supports coarse-grained mode meaning that each Spark executor runs as a sinlge Mesos task.

#### Submitting applications

- you should favor cluster mode when using Mesos. Client mode requires lot of configurations in `spark-env.sh` to work with Mesos.

```
export MESOS_NATIVE_JAVA_LIBRARY=<path to libmesos.so>
```

```
export SPARK_EXECUTOR_URI=<URL of spark-2.2.0.tar.gz uploaded above>
```

Now when starting applicatioin against the cluster

````scala
import org.apache.spark.sql.SparkSession
val spark = SparkSession.builder
  .master("mesos://HOST:5050")
  .appName("my app")
  .config("spark.executor.uri", "<path to spark-2.2.0.tar.gz uploaded above>")
  .getOrCreate()
````

#### Application Scheduling

Spark Application runs executor processes independently. Cluster maangers provide for scheduling across Spark Application. Within each Spark Application, multiple jobs may be running concurrently if they were submitted by different threads. Spark includes a *fair scheduler* to schedule resources within each application.

If multiple users need to share your cluster and run different Spark Applications, there are multiple ways to manage resources like static partitioning of resources manually or dynamic allocation can be turned on the let applications scale up and down dynamically based on their current number of pending tasks.

NOTE : for using Dynamic allocation enable following options : `spark.dynamicAllocation.enabled` and `spark.shuffle.service.enabled`

## Misc. Considerations

- Number and Type of Applications: YARN is great for HDFS based applications. Its not great as compute and storage is tightly coupled. Mesos improves on this bit conceptually and supports multiple types of application but it require pre-provisioning machines and requires buy-in at a much larger scale. Spark Standalone is best choice for running only Spark Workloads, its lightweight and relatively simpler to manage.
- Spark Versions : If you want to manage multiple spark version then you will need to handle it yourselves as there no easy solution.
- Logging : These are more “out of box” for YARN or Mesos and might need some tweaking if you are using standalone
- Maintaining a Metastore : in order to maintain metadata about your stored dataset, such as table catalog. Maintaining an Apache Hive metastore, might be something that’s worth doing to facilitate more productive, cross-application referencing to the same datasets
- Spark’s external Shuffle Service: typically spark stores shuffle blocks on a local disk on that node. An external shuffle service allows storing shuffle blocks so that they are available to all executors meaning we can arbitrarily kill executors and still have their shuffle outputs.

---

## File: pyspark/notes/ch18.md

# Monitoring and Debugging

NOTE: This chapter is better explored using a Spark UI

## Monitoring Landscape

Components we can monitor :

- Spark Application and Jobs: Debug using Spark UI and Spark Logs.
- JVM : Executors are run in individual JVM. Use tools like *jstack*, *jmap*, *jstat* and *jvisualvm* etc to profile Spark Jobs.
- OS/Machine : We can monitor machines for CPU, Network and I/O using tools like *dstat*, *iostat*, *iotop*
- Cluster: Monitor using Cluster Manager like YARN, Mesos or standalone cluster. Popular tools include *Ganglia* and *Prometheus*.

## What to Monitor ?

We usually monitor two things : *processes* running your application (CPU usage, memory usage, etc.), and *query* execution inside it (e.g. jobs and tasks).

### Driver and Executor Processes

- We should keep an eye on driver because state of application resides here. If you could only monitor one machine : always monitor driver but understanding state of executors is also important for individual Spark jobs.
- Spark has configurable metrics system based on *Dropwizard Metrics Library*. Its configured via a configuration file that Spark expects at `$SPARK_HOME/conf/metrics.properties` or defined via `spark.metrics.conf`

### Queries, Jobs, Stages and Tasks

- Spark provides ability to dive into queries, job, stages, and tasks. This allows to know exactly what’s eating up all the resources in case users run catersian joins :)

## Spark Logs

- Usually with Scala and Java, Spark automatically provides logs out of box, but with python it requires `py4j` to integrate to Spark’s Java-based logging library. Using `logging` module or simple print statements will still print results to standard errors, however its hard to find.

````python
# set spark log level
spark.sparkContext.setLogLevel("INFO")
````

## Spark UI

- visual way to monitor application while they are running as well as metrics about Spark Workloads, at the Spark and JVM level.
- Every `SparkContext` running launches a web UI, by default on port 4040, that displays useful information about the application. When you run Spark in local mode, for example, just navigate to [*http://localhost:4040*](http://localhost:4040) to see the UI when running a Spark Application on your local machine.

Open a new spark-shell and run this code and trace it in UI

````python
spark.read\
  .option("header", "true")\
  .csv("/data/retail-data/all/online-retail-dataset.csv")\
  .repartition(2)\
  .selectExpr("instr(Description, 'GLASS') >= 1 as is_glass")\
  .groupBy("is_glass")\
  .count()\
  .collect()
````

Notice the aggregate statistics about this query:

```
Submitted Time: 2017/04/08 16:24:41
Duration: 2 s
Succeeded Jobs: 2
```

Open the Jobs Menu

The first stage has eight tasks. CSV files are splittable, and Spark  broke up the work to be distributed relatively evenly between the  different cores on the machine. This happens at the cluster level and  points to an important optimization: how you store your files. The  following stage has two tasks because we explicitly called a repartition to move the data into two partitions. The last stage has 200 tasks  because the default shuffle partitions value is 200.

### Spark REST API

you can also access Spark’s status and metrics via a REST API. This is is available at [*http://localhost:4040/api/v1*](http://localhost:4040/api/v1) and is a way of building visualizations and monitoring tools on top of Spark itself.

### Spark UI History Server

Normally, the Spark UI is only available while a SparkContext is running, so how  can you get to it after your application crashes or ends? To do this, Spark includes a tool called the Spark History Server that  allows you to reconstruct the Spark UI and REST API, provided that the  application was configured to save an *event log*.

To use the history server, you first need to configure your application  to store event logs to a certain location. You can do this by by  enabling `spark.eventLog.enabled` and the event log location with the configuration `spark.eventLog.dir`. Then, once you have stored the events, you can run the history server  as a standalone application, and it will automatically reconstruct the  web UI based on these logs. Some cluster managers and cloud services  also configure logging automatically and run a history server by  default.

## Debugging and Spark First Aid

Common Problem and their solutions

### Spark Jobs Not Starting

This issue can arise frequently, especially when you are just getting started with a fresh deployment or environment.

#### Signs and Symptoms

- Spark jobs don’t start
- Spark UI doesn’t show any nodes on the cluster except the driver
- Spark UI seems to be reporting incorrect information.

#### Potential treatments

- Occurs due to application’s resource demands are not configured properly and Spark makes assumptions about networks, file system and other resources. Most likely configured something incorrectly, and now the node that runs the driver can’t talk to executor, maybe your forgot to specify what IP and port is open or didn’t open correct one.
- Ensure machines can communicate properly with one another on ports that you expect
- Ensure Spark resource configurations are correct and that cluster manager is setup correctly for Spark. Try running a simple application first to see if that works. One common issue maybe that you requested more memory per executor than the cluster manager has free to allocate.

### Errors Before Execution

- While developing a new application and have previously run code on this cluster, but now some new code won’t work.

#### Signs and Symptoms

- Commands don’t run at all and output error messages
- Check Spark UI and no jobs, stages or tasks seem to run.

#### Potential Treatments

- Take a look at error message to make sure nothing is wrong with your code such as Incorrect file path or column name
- Double check to verify that cluster has the network connectivity between driver, workers, and the storage systems.
- There might be issues with libraries or class paths that are causing the wrong version of a library to be loaded for accesing storage.

### Errors During Execution

#### Signs and Symptoms

- One spark job runs successfully on cluster but next one fails
- A step in multistep query fails
- Difficult to parse error message

#### Treatments

- Check if data is in correct format as expected. Sometimes upstream data may change causing unintended consequences in application
- If an error pop quickly even before tasks are launched, then its most likely an *analysis exception* while planning the query. Either misspelled columns are referenced or column, view, or table doesn’t exits
- Read stack trace for more clues on the problem.
- Its also possible your own code is failing and Spark will just ouput the excepted error from the program and task will be marked as failed on Spark UI.

### Slow Tasks or Stragglers

#### Signs and Symtoms

- Spark stages seem to execute until there are only a handful of tasks left. Those tasks then take a long time.
- These slow tasks show up in the Spark UI and occur consistently on the same dataset(s).
- These occur in stages, one after the other.
- Scaling up the number of machines given to the Spark Application  doesn’t really help—some tasks still take much longer than others.
- In the Spark metrics, certain executors are reading and writing much more data than others.

#### potential treatments

Most often the source of this issue is that your data is partitioned unevenly into DataFrame or RDD partitions. When this happens, some executors might need to work on much larger amounts of work than others.

- Try increasing the number of partitions to have less data per partition
- Try repartitioning by another combination of columns.
- Try increasing the memory allocated to your executors if possible.
- Monitor the executor that is having trouble and see if it is the same  machine across jobs; you might also have an unhealthy executor or  machine in your cluster—for example, one whose disk is nearly full.
- Check whether your user-defined functions (UDFs) are wasteful in their object allocation or business logic. Try to convert them to DataFrame code if possible.
- Ensure that your UDFs or User-Defined Aggregate Functions (UDAFs) are running on a small enough batch of data. Oftentimes an aggregation can pull a lot of data into memory for a common key, leading to that executor having to do a lot more work than other
- Turning on *speculation* (Discussed below)
- Another common issue can arise when you’re working with Datasets. Because Datasets perform a lot of object instantiation to convert records to Java objects for UDFs, they can cause a lot of garbage collection.

### Slow Aggregations

#### Signs and symptoms

- Slow tasks during a `groupBy` call.
- Jobs after the aggregation are slow, as well.

#### Potential Treatments

Unfortunately, this issue can’t always be solved. Sometimes, the data in your job just has some skewed keys, and the operation you want to run  on them needs to be slow.

- Increase number of partitions before aggregation to reduce number of different keys processed in each task.
- Increase executor memory as this can help handle the case if a single key has lots of data allowing less spillage to disk.
- If tasks after aggregation are slow means your dataset is still unbalanced, try a `repartition` call to partition it randomly.
- Try to prune filters and `SELECT` statements to collect the data that you actually need. Spark’s query optimizer does this for structured APIs automatically.
- Ensure null values are represented correctly and not using `“ ”` or `“EMPTY”`. Spark can optimize nulls early in job if possible.
- Some aggregations are inherently slower than others. For isntance, `collect_list` and `collect_set` are very slow aggregation functions because they *must* return all the matching objects to the driver, and should be avoided in performance-critical code.

### Slow Joins

Joins and aggregations are both shuffles, so they share some of the same general symptoms as well as treatments.

#### Signs and symptoms

- A join stage seems to be taking a long time. This can be one task or many tasks.
- Stages before and after the join seem to be operating normally.

#### Potential treatments

- Many joins can be optimized (manually or automatically) to other types of joins.
- Experimenting with different join orderings can really help speed up jobs, especially if some of those joins filter out a large amount of  data; do those first.
- Partitioning a dataset prior to joining can be very helpful for reducing data movement across the cluster, especially if the same  dataset will be used in multiple join operations. It’s worth experimenting with different prejoin partitioning. Keep in mind, again, that this isn’t “free” and does come at the cost of a shuffle.
- Slow joins can also be caused by data skew. There’s not always a lot you can do here, but sizing up the Spark application and/or increasing the size of executors can help, as described in earlier sections.
- Gather data using `filter` and `select` that you actually need.
- Represent `null` values correctly.
- Sometimes Spark can’t properly plan for a broadcast join if it doesn’t know any statistics about the input DataFrame or table. If you know that one of the tables that you are joining is small, you can try  to force a broadcast, or use Spark’s statistics collection commands to let it analyze the table.

### Slow Reads/Writes

Slow I/O can be difficult to diagnose, especially with networked file systems.

#### Signs and Symptoms

- Slow reading of data from a distributed file system or external system.
- Slow writes from network file systems or blob storage.

#### Potential Treatments

- Turning on speculation (set `spark.speculation` to `true`) can help with slow reads and writes. This will launch additional tasks  with the same operation in an attempt to see whether it’s just some transient issue in the first task. Speculation is a powerful tool and works well with consistent file systems. However, it can cause duplicate data writes with some eventually consistent cloud services, such as Amazon S3, so check whether it is supported by the storage system connector you are using.
- Ensuring sufficient network connectivity can be important—your Spark  cluster may simply not have enough total network bandwidth to get to your storage system.
- For distributed file systems such as HDFS running on the same nodes as Spark, make sure Spark sees the same hostnames for nodes as the file  system. This will enable Spark to do locality-aware scheduling.

### Driver OutOfMemoryError or Driver Unresponsive

This is usually serious issue as it crashes Spark Application. It happens due to collecting too much data back to driver, making it run out of memory

#### Signs and Symptoms

- Spark Application is unresponsive or crashed.
- `OutOfMemoryError`s or garbage collection messages in the driver logs.
- Commands take a very long time to run or don’t run at all.
- Interactivity is very low or non-existent.
- Memory usage is high for the driver JVM.

#### Potential Treatments

- Your code should not call `collect` on a very large dataset
- Avoid doing broadcast join where the data to be broadcast is too big.
- A long-running application generated a large number of objects on the driver and is unable to release them. Java’s *jmap* tool can be useful to see what objects are filling most of the memory of your driver JVM by printing a histogram of the heap.
- Increase the driver’s memory allocation if possible to make it work with more data
- Issues with JVMs running out of memory can happen if you are using  another language binding, such as Python, due to data conversion between the two requiring too much memory in the JVM.
- If you are sharing a SparkContext with other users, ensure that people aren’t trying to do something that might be causing large amounts of memory allocation in the driver 

### Executor OutOfMemoryError or Executor Unresponsive

Many Spark Applications can recover from this automatically depending on the issue.

#### Signs and Symptoms

- `OutOfMemoryError`s or garbage collection messages in the executor logs. You can find these in the Spark UI.
- Executors that crash or become unresponsive.
- Slow tasks on certain nodes that never seem to recover.

#### Potential treatments

- Try increasing the memory and number of executors
- Try increasing PySpark worker size via relevant Python configurations
- Look for garbage collection error messages in the executor logs. Some of the tasks that are running, especially if you’re using UDFs, can be creating lots of objects that need to be garbage collected. Repartition  your data to increase parallelism, reduce the amount of records per  task, and ensure that all executors are getting the same amount of work.
- Ensure nulls are handled correctly
- Try using fewer UDFs and more of Spark’s structured operations
- Use Java montioring tools like *jmap* to get a histogram of heap memory usage on your executors
- If executors are being placed on nodes that also have other workloads running on them, such as a key-value store, try to isolate your Spark jobs from other jobs.

### Unexpected Nulls in Results

#### Signs and symptoms

- Unexpected `null` values after transformations.
- Scheduled production jobs that used to work no longer work, or no longer produce the right results.

#### Potential treatments

- It’s  possible that your data format has changed without adjusting  your business logic. This means that code that worked before is no longer valid.
- Use an accumulator to try to count records or certain types, as well as parsing or processing errors where you skip a record. This can be helpful because you might think that you’re parsing data of a certain  format, but some of the data doesn’t. Most often, users will place the accumulator in a UDF when they are parsing their raw data into a more controlled format and perform the counts there. This allows you to count valid and invalid records and then operate accordingly after the fact.
- Ensure that your transformations actually result in valid query plans. Spark SQL sometimes does implicit type coercions that can cause confusing results. 

For instance, the SQL expression `SELECT 5*"23"` results in 115 because the string “25” converts to an the value 25 as an integer, but the expression `SELECT 5 * " "` results in `null` because casting the empty string to an integer gives `null`. Make sure that your intermediate datasets have the schema you expect them to (try using `printSchema` on them), and look for any `CAST` operations in the final query plan.

### No Space Left on Disk Errors

#### Signs and symptoms

- You see “no space left on disk” errors and your jobs fail.

#### Potential treatments

- Add more disk space by sizing up the nodes or attaching external storage from cloud.
- If there is a limit on storage, Repartition can help not to have skewed nodes with large storage.
- Try experimenting with different storage configurations like log retain or rolling, etc.

### Serialization Errors

#### Signs and symptoms

- You see serialization errors and your jobs fail.

#### Potential treatments

- This is very uncommon when working with the Structured APIs, but you  might be trying to perform some custom logic on executors with UDFs or  RDDs and either the task that you’re trying to serialize to these  executors or the data you are trying to share cannot be serialized. This often happens when you’re working with either some code or data that cannot be serialized into a UDF or function, or if you’re working with  strange data types that cannot be serialized. If you are using (or  intend to be using Kryo serialization), verify that you’re actually registering your classes so that they are indeed serialized.
- Try not to refer to any fields of the enclosing object in your UDFs when creating UDFs inside a Java or Scala class. This can cause Spark to try to serialize the whole enclosing object, which may not be possible. Instead, copy the relevant fields to local variables in the same scope as closure and use those.

---

## File: pyspark/notes/ch19.md

# Performance Tuning

## Indirect Performance Enhancements

### Design Choices

- Although its an obvious way to optimize performance, often we don’t prioritize this step. It helps in writing better Spark applications which run stable and consistent manner.

#### Scala vs Java vs Python vs R

- Its nearly impossible to choose one over other, but depends on use cases.
- If we want to perform some single-node machine learning after performing a large ETL job, run ETL as SparkR and then use R’s massive machine learning ecosystem to run single-node machine learning algorithms.
- Spark’s Structured API are consistent across language in terms of stability and speed.
- When you start delving in RDDs or UDFs, then R or Python are not best choice simple because how its executed, additionally its hard to provide type guarantees

#### DataFrames vs SQL vs Datasets vs RDDs

- Across all languages, DataFrames, Datasets and SQL are equivalent, however while using UDFs R or Python will take a hit on performance due to serialisation. 
- Although everything boils down to RDDs Spark’s optimization engine will write “better” RDD code than you can manually.

### Object Serialization in RDDs

- When working with custom data type you should use *Kyro* for serialisation because its more compact and more efficient than Java’s default serialisations. However you will need to register classes that you will be using in your application.
- You can use Kryo serialization by setting `spark.serializer` to `org.apache.spark.serializer.KryoSerializer`. You will also need to explicitly register the classes that you would like to register with the Kryo serializer via the `spark.kryo.classesToRegister` configuration.

### Cluster Configurations

#### Cluster/Application Sizing and Sharing

- This boils down to a resource sharing and scheduling problem, however there are lot of options for how we want to share resources at cluster level or application level

#### Dynamic Allocation

- Application can give resources back to the cluster if they are no longer used, and request them again later when there is demand
- This feature is disabled by default and available on all coarse-grained cluster managers, that is standalone mode, YARN mode, or Mesos coarse-grained mode.
- set `spark.dynamicAllocation.enabled` to `true` for enabling this feature

### Scheduling

- We can take advantage of running Spark jobs in parallel with scheduler pools or help Spark applications run in parallel with something like dynamic allocation or setting `max-executor-cores`
- Scheduling optimizations do involve some research and experimentation, and unfortunately there are not super-quick fixes beyond setting `spark.scheduler.mode` to `FAIR` to allow better sharing of resources across multiple users, or setting `--max-executor-cores`, which specifies the maximum number of executor cores that your  application will need. Specifying this value can ensure that your  application does not take up all the resources on the cluster.

### Data at Rest

- More often Data we write, in a large organisation is accessed by multiple parties and we should make sure that our data is efficient while reading.
- This involves settling for a storage system, data format and taking advantage or data partitioning in some storage formats.

#### File-based long-term data storage

- There are many file formats available, one simple best practice is to use most efficient storage format possible
- Generally prefer structured, binary types to store data, especially when you will be accessing it frequently. CSVs are slow to parse, and can cause problem when reading multiple files. You should use Apache Parquet
- Parquet stores data in binary files with column-oriented storage and also tracks statistics about each file that make it possible to quickly skip data not needed for query.

#### Splittable file types and compression

- Make sure your file types is splittable, allowing different tasks can read different parts of file in parallel. File types like malformed JSON types require read on single machine reducing parallelism
- Main place splittability comes in is compression formats. A ZIP or Tar can’t be split. If files compressed using gzip, bzip2 or lz4 are generally splittable if the are written by Hadoop or Spark.
- Make sure multiple files should not be very small, neither too large. Prefer several files on few hundred megabytes.

#### Table Partitioning

- Table partitioning refers to storing files in separate directories based on a key, such as the date field in the data. Storage managers like Apache Hive support this concept, as do many of Spark’s built-in data sources.
- Partitioning allows Spark to skip many irrelevant files when it only requires data with a specific range of keys.
- NOTE tho, don’t prefer partition if it increases granularity as it can split data in multiple files, which is not ideal.

#### Bucketing

- Bucketing allows Spark to `pre-partition` data according to how joins or aggregation are likely to be performed by readers.
- This improves performance and stability because data can be consistently distributed across partitions as opposed to skew distribution.
- If join is done on a column immediately after read, we can se bucketing to ensure data is well partitioned according to those values, saving shuffle before join.

#### The number of files

- Having lots of small files is going to make the scheduler work much harder to locate the data and launch all of the read tasks increasing the network and scheduling overhead of the job.
- Having fewer large files eases the pain off the scheduler but it will also make tasks run longer. In this case, though, you can always launch more tasks than there are input files if you want more parallelism—Spark will split each file across multiple tasks assuming you are using a splittable format.
- To control how many records go into each file, you can specify the `maxRecordsPerFile` option to the write operation.

#### Data Locality

- Data locality basically specifies a preference for certain nodes that hold certain data, rather than having to exchange these blocks of data over the network.
- If you run your storage system on the same nodes as Spark, and the system supports locality hints, Spark will try to schedule tasks close to each input block of data.

#### Statistics Collection

- Spark has a cost based query optimizer that plans queries based on the properties of the input data when using the Structured APIs. This will require storing *statistics* about your tables.
- There are two types of statistics: table-level and Column level
- Statistics collection is available only on named tables, not on arbitrary DataFrames or RDDs.

````sql
# table-level statistics
ANALYZE TABLE table_name COMPUTE STATISTICS

# column-level statistics
ANALYZE TABLE table_name COMPUTE STATISTICS FOR
COLUMNS column_name1, column_name2, ...
````

### Shuffle Configurations

- Spark’s External Shuffle service allows other nodes to read shuffle data from remote machines even when executor on those machines are busy (garbage collection). This comes at the cost of complexity and maintenance.
- Optimize number of concurrent connection per executor (usually good defaults)
- for RDD job, serialisation has large impact on shuffle, always use *Kyro*
- Optimize number of partition to aim few tens of megabytes of data per output partition in your shuffle

### Memory Pressure and Garbage Collections

- Garbage collection hits performance when there are large number of objects in memory.
- One strategy to avoid above situation is to use Structured APIs as they reduce memory pressure because JVM objects are never realized and Spark SQL simply performs computation on internal formats

#### Measuring Impact of Garbage Collection

- Find out how frequently garbage collection happens and amount it takes.
- Change Spark’s JVM Options using `spark.executor.extraJavaOptions` to `-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps`

#### Garbage Collection tuning

- Understand how memory is organized in JVM
  - Java Heap Space is divided into : Young and Old. The Young generation is meant to hold short-lived objects whereas the  Old generation is intended for objects with longer lifetimes.
  - The Young generation is further divided into three regions: Eden, Survivor1, and Survivor2.
- Simplified description of garbage collection procedure
  - When Eden is full, a minor garbage collection is run on Eden and objects that are alive from Eden and Survivor1 are copied to Survivor2.
  - The Survivor regions are swapped.
  - If an object is old enough or if Survivor2 is full, that object is moved to Old.
  - Finally, when Old is close to full, a full garbage collection is  invoked. This involves tracing through all the objects on the heap, deleting the unreferenced ones, and moving the others to fill up unused  space, so it is generally the slowest garbage collection operation.
- Gather garbage collection statistics to determine whether it is being  run too often. If a full garbage collection is invoked multiple times  before a task completes, it means that there isn’t enough memory  available for executing tasks, so you should decrease the amount of  memory Spark uses for caching (`spark.memory.fraction`).
- If there are too many minor collections but not many major garbage collections, allocating more memory for Eden would help. You can set the size of the Eden to be an over-estimate of how much memory each task will need. If the size of Eden is determined to be *E*, you can set the size of the Young generation using the option `-Xmn=4/3*E`. (The scaling up by 4/3 is to account for space used by survivor regions, as well.)
- Try the G1GC garbage collector with `-XX:+UseG1GC`. It can  improve performance in some situations in which garbage collection is a  bottleneck and you don’t have a way to reduce it further by sizing the  generations. Note that with large executor heap sizes, it can be  important to increase the G1 region size with `-XX:G1HeapRegionSize`.

## Direct Performance Enchancements

### Parallelism

- First thing to speedup a stage is to increase degree of parallelism. At least 2-3 tasks per CPU core in your cluster if the stage processes a large amount of data.
- set this via the `spark.default.parallelism` property as well as tuning the `spark.sql.shuffle.partitions` according to the number of cores in your cluster.

### Improved Filtering

- Move filters to earliest part of Spark job. Sometimes filters are pushed into data sources themselves and this means we can avoid reading/writing data is irrelevant to end result.
- Enabling Partitioning and Bucketing helps achieve this

### Repartitioning and Coalescing

- Repartition calls can incur a shuffle. However it optimize overall execution by balacing data across the cluster.
- Generally shuffle least amount of data possible, If reducing number of overall partitions in a DataFrame or RDD, first try `coalesce` method, which will not perform a shuffle but rather merge partitions on the same node into one partition.
- The slower `repartition` method will also shuffle data across the network to achieve even load balancing. Repartitions can be  particularly helpful when performing joins or prior to a `cache` call.

#### Custom Partitioning

If your jobs are still slow or unstable, you might want to explore performing custom partitioning at the RDD level. This allows you to  define a custom partition function that will organize the data across the cluster to a finer level of precision than is available at the DataFrame level. 

### User-Defined Functions

- generally avoiding UDFs is a good optimization :)
- UDFs are expensive because they force representing data as objects in JVM and sometimes do this multiple times per record in query. Use structured APIs as much possible.

### Temporary Data Storage (Caching)

- NOTE: Although caching sounds cool it incurs serialization, deserialization, and storage cost. So use it with caution and not too much
- In applications that reuse the same datasets over and over, most useful optimizations is caching. Caching will place a DataFrame, table, or RDD into temporary storage (either memory or disk) across the executors in your cluster, and make subsequent reads faster.
- Caching is a lazy operation, meaning that things will be cached only as they  are accessed. The RDD API and the Structured API differ in how they actually perform caching
- Caching an RDD involves actual data (bits/bytes) When this is accesed again Spark returns proper data. This is done using RDD reference.
- Structured API caching is done based on *physical plan*. This means that we effectively store the physical plan as our key (as  opposed to the object reference) and perform a lookup prior to the execution of a Structured job
- there are different storage levels to cahce data : *MEMORY_ONLY, MEMORY_AND_DISK, MEMORY_ONLY_SER (Java/Scala), MEMORY_AND_DISK_SER(Java/Scala), DISK_ONLY, MEMORY_ONLY_2, MEMORY_AND_DISK_2 (2 means replication), OFF_HEAP(Experimental)*
- 

### Joins

- Joins are common operation and biggest optimization opportunity is simply understanding joins :)
- Equi-joins are easiest for Spark to optimize, therefore should be preffered.
- Simple things like trying to use filtering ability of inner joins by changing join ordering can yield large speedups.
- Broadcast join hints can help Spark make intelligent planning decisions when it comes to creating query plans.
- Avoid cartesian joins or even full outer joins as they often low-hanging fruit for optimization and stability because they can optimized into different filtering style joins when we look at entire data flow.
- Collecting statistics before join always help Spark
- Bucketing helps Spark avoid large shuffle when joins are performed

### Aggregations

- there are not too many ways that you can optimize specific aggregations  beyond filtering data before the aggregation having a sufficiently high  number of partitions.
- If you’re using RDDs, controlling exactly how these aggregations are performed (e.g., using `reduceByKey` when possible over `groupByKey`) can be very helpful and improve the speed and stability of your code.

### Broadcast Variables

- The basic premise is that if some large piece of data will be used  across multiple UDF calls in your program, you can broadcast it to save  just a single read-only copy on each node and avoid re-sending this data with each job.

- Broadcast variables may be useful to save a lookup table or a machine  learning model. You can also broadcast arbitrary objects by creating  broadcast variables using your SparkContext, and then simply refer to  those variables in your tasks

---

## File: pyspark/notes/ch2.md

# A Gentle Introduction to Spark



## Spark’s Basic Architecture

- Often times a single machine is not powerful enough to perform huge amounts of computations and data processing.
- A cluster or group of computers, pools the resources of many machines giving us abstration of single compute machine which is managed and co-ordinated by Spark.

- clusters are managed by cluster managers like Spark’s stand-alone cluster manager, YARN or Mesos. We submit our Spark Applications to these cluster managers which grant resources to our application to perform the task at hand.

### Spark Applications

- Spark Applications consist of a *driver* process and a set of *executor* processes.
- Driver Node runs your `main()` function, sits on a node in a cluster, and is responsible for three things
  - maintaining information about spark application
  - responding to user program or input
  - analyzing, distributing and scheduling work across executors
- Executors actually carry out the work assigned by driver and submit it back.

## Spark’s Language APIs

- Spark API enables us to run Spark Code in various programming Languages
  - Scala : Spark is primarily written in spark, making it spark’s default language.
  - Java : supports Scala, and Java is required for some special cases.
  - Python : supports nearly all constructs that Scala supports.
  - SQL : Spark supports a subset of ANSI SQL 2003 Standard.
  - R : Spark has 2 commonly used R libraries: Spark core (SparkR) and another as R community driven package (sparklyr)

## Spark’s APIs

There are two fundamental set of APIs: the low-level “unstructured” APIs, and the higher-level structured APIs.

### Starting Spark

- Spark Application is controlled through a driver process called the SparkSession. SparkSession Instance is the way to Spark executes user-defined manipulations across the cluster.
- Type `spark` and notice it builds a default session.
- Run : `myRange = spark.range(1000).toDF("number")`

### DataFrames

- most common Structured API and simply represents a table of data with rows and columns. The list that defines the columns and types within those columns is called the **schema**.
- Spark DataFrame can span thousands of computers. Either for computational reasons or storage limit reasons.
- Spark DataFrames can be converted to Python or R Dataframes but limits their capability of spanning multiple machines.

### Partitions

- To allow every executor to perform work in parallel, spark breaks data into chunks called as *partitions*
- A *partition* is a collection of rows that sit on one physical machines in your cluster.
- NOTE: you should not manipulate partitions manually as part of Spark’s highly optimized plans it will manage this as a compute engine.

## Transformations

- In Spark, core data structures are *immutable*.
- This seems strange but then how will you change a df ? These operations are called *transformations*

````python
divisBy2 = myRange.where("number % 2 = 0")
````

- Notice that these return no output because it is an abstract transformation, and Spark will not act on transformation until we call an action. They are more used for expressing business logic.
- Types of Transformation
  - Narrow Dependencies : Each input partition will contribute to only one output partition.
  - Wide Dependencies : Inpute partitions contributing to many output partitions. (Shuffle)
- With narrow transformations, Spark will automatically perform an operation called *pipelining*, meaning that if we specify multiple filters on DataFrames, they’ll all  be performed in-memory. The same cannot be said for shuffles.

|                    Narrow Transformations                    |                     Wide Transformations                     |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_0204.png) | ![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_0205.png) |

### Lazy Evaluation

- Spark waits until we actually require to execute the graph of computation instructions (*plan of transformation*)
- By waiting Spark compiles a plan from raw DataFrame transformations to a streamlined physical plan that will run as efficiently as possible across clusters.
- This provides immense benefit because spark can optimize data flow across clusters (expensive). An example of this is something called *predicate pushdown* on DataFrames.

## Actions

- Transformations allow us to build up our logical transformation plan. To trigger the computation, we run an action.

````python
divisBy2.count() # count action
````

- Three kinds of actions
  - actions to view data in console.
  - actions to collect data to native objects in respective language.
  - actions to write to output data sources.

- Here first we ran filter transformation (narrow transformation) then an aggregation (wide transformation) performing counts on a per partition basis and collecting results which we can view on spark UI at `http://localhost:4040`

## End-to-End Example

Resource Repo : https://github.com/databricks/Spark-The-Definitive-Guide/tree/master

Dataset : flight_data

````python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('example').getOrCreate()

DATA_DIR = "../Spark-The-Definitive-Guide"

# spark supports read/write from large number of data sources
# we will use a DataFrame reader from SparkSession
flightData2015 = spark.read\
                    .option("inferSchema", "true")\
                    .option("header", "true")\
                    .csv(f"{DATA_DIR}/data/flight-data/csv/2015-summary.csv")
````

- To get schema information, Spark only reads in a little bit of data and then attempts to parse the types in those rows according to types in Spark. We could also pass schema when reading dataset.
- Each of these DataFrames (in Scala and Python) have a set of columns with an unspecified number of rows. The reason the number of rows is  unspecified is because reading data is a transformation, and is  therefore a lazy operation. Spark peeked at only a couple of rows of  data to try to guess what types each column should be.

````python
flightData2015.sort("count").explain()

# Output
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- Sort [count#19 ASC NULLS FIRST], true, 0
   +- Exchange rangepartitioning(count#19 ASC NULLS FIRST, 200), ENSURE_REQUIREMENTS, [plan_id=33]
      +- FileScan csv [DEST_COUNTRY_NAME#17,ORIGIN_COUNTRY_NAME#18,count#19] Batched: false, DataFilters: [], Format: CSV, Location: InMemoryFileIndex(1 paths)[file:/Users/smk/dev/spark/Spark-The-Definitive-Guide/data/flight-data/..., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<DEST_COUNTRY_NAME:string,ORIGIN_COUNTRY_NAME:string,count:int>
````

- Nothing happens when we call sort because its just a transformation. Notice how spark makes the plan to execute it. Explain can be called on any DataFrame Object to see its lineage.
- Notice sort, exchange and FileScan, it is there because the sort of our data is actually a wide transformation because rows will need to compared with one another.
- Note by default spark outputs 200 shuffle partitions, reduce it to 5

````python
spark.conf.set("spark.sql.shuffle.partitions", "5")
flightData2015.sort("count").take(2)
````

- *The logical plan of transformations that we build up defines a lineage for  the DataFrame so that at any given point in time, Spark knows how to  recompute any partition by performing all of the operations it had  before on the same input data. This sits at the heart of Spark’s  programming model—functional programming where the same inputs always  result in the same outputs when the transformations on that data stay  constant.*
- We do not manipulate the physical data; instead, we configure physical  execution characteristics through things like the shuffle partitions  parameter

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_0209.png)

### DataFrames and SQL

We can make any DataFrame into a table or view

````python
flightData2015.createOrReplaceTempView("flight_data_2015")

# now we can query this view
sqlWay = spark.sql("""
SELECT DEST_COUNTRY_NAME, count(1)
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
""")

dataFrameWay = flightData2015\
  .groupBy("DEST_COUNTRY_NAME")\
  .count()

sqlWay.explain()
dataFrameWay.explain()

# Note How physical plan comes same, because of spark optimization

spark.sql("SELECT max(count) from flight_data_2015").take(1)
# in Python
from pyspark.sql.functions import max

flightData2015.select(max("count")).take(1)
````

````python
# Using SparkSQL
maxSql = spark.sql("""
SELECT DEST_COUNTRY_NAME, sum(count) as destination_total
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
ORDER BY sum(count) DESC
LIMIT 5
""")

maxSql.show()

# Using DataFrames
from pyspark.sql.functions import desc

flightData2015\
  .groupBy("DEST_COUNTRY_NAME")\
  .sum("count")\
  .withColumnRenamed("sum(count)", "destination_total")\
  .sort(desc("destination_total"))\
  .limit(5)\
  .show()

# Tip : check plan of above query try to understand
````



---

## File: pyspark/notes/ch20.md

# Stream Processing Fundamentals

- Why streaming ? More often we find ourselves performing a long computation but we want something of value while computation is going on e.g. report about customer activity or a new machine learning model.
- In 2012, the project incorportaed Spark Streaming and its DStreams API. DAPIs enable stream processing using high-level functional operators like `map` and `reduce`.
- Hundreds of orgs now use DStreams in production for large real-time application, often processing terabytes of data per hour.M uch like the Resilient Distributed Dataset (RDD) API, however, the  DStreams API is based on relatively low-level operations on Java/Python objects that limit opportunities for higher-level optimization.
- Thus in 2016 Spark added Structured Streaming, built directly on DataFrames that supports both rich optimizations and significantly simple integration with other DataFrame and Dataset code.
- If you are interested in DStreams, many other books cover that API,  including several dedicated books on Spark Streaming only, such as *Learning Spark Streaming* by Francois Garillot and Gerard Maas (O’Reilly, 2017).
- Much as with RDDs versus DataFrames, however, Structured Streaming offers a superset of the majority of the functionality of DStreams, and  will often perform better due to code generation and the Catalyst optimizer.

## What is Steam Processing

- act of continuously adding new data to compute a result. In stream processing, input data in unbounded and has no beginning or end, simply forms a series of events that arrive at the stream processing system (e.g. credit card transactions, clicks on a website, IOT devices)
- User/Applications can compute various queries over this stream and output multiple versions of the results as it runs, or keep it upto date in and external “sink” system such as a key-value store.
- In Batch processing often results are computed once on static data.
- Although stream and batch sound like different strategies, in practice both are often employed together. e.g. streaming application often need to join input data against a dataset written periodically by a batch job, and output of streaming jobs often files or tables that are queried in batch jobs.

### Stream Processing Use Cases

#### Notifications and Alerting

- given some series of events, a notification or alert should be triggered if some sort of event or series of events occur.
- it doesn’t limit to autonomous or pre-programmed decision making, but rather notifying with a counterpart of some action to be taken on the fly

#### Real-time reporting

- Real-time dashboarding
- monitoring some resource, load, uptime, etc.

#### Incremental ETL

- reduce latency companies must endure while retrieving information into a data warehouse.
- Spark batch jobs are often used for ETL Workloads, Using Structured Streaming these jobs can incorporate new data withing seconds, enabling users to query it faster downstream.
- NOTE: here data needs to processed exactly once in a fault tolerant manner.

#### Update data to serve in real time

- compute data that gets server interactively by another application
- ouput of web analytics product such as Google Analytics might continuosly track visits to each page and use a streaming system to keep up to date these counts

#### Real time decision making

- analyzing new inputs and responding to them automatically using business logic.  An example is credit card transaction fraud detection.

#### online machine learning

- training a model on a combination of streaming and historical data from multiple users.

### Advantages of Stream Processing

- enables *lower latency* - when application needs to respond quickly (*minutes, seconds, milliseconds*)
- more efficient in updating a result than repeated batch jobs, because of automatic incrementalizes the computation.

### Challanges of Stream Processing

- Assumes folowing output events from sensor

````
{value: 1, time: "2017-04-07T00:00:00"}
{value: 2, time: "2017-04-07T01:00:00"}
{value: 5, time: "2017-04-07T02:00:00"}
{value: 10, time: "2017-04-07T01:30:00"}
{value: 7, time: "2017-04-07T03:00:00"}
````

- Notice, how last packet came out of order and later than others, responding to a specific event (`5`) is much easier as compared to specific sequence of values in stream (`2->5->10`)
- Solving above problem require stream have memory of past (state). If sensor output million records, it might become a nightmare.
- Summarize
  - Processing out-of-order data based on application timestamps (also called *event time*)
  - Maintaining large amounts of state
  - Supporting high-data throughput
  - Processing each event exactly once despite machine failures
  - Handling load imbalance and stragglers
  - Responding to events at low latency
  - Joining with external data in other storage systems
  - Determining how to update output sinks as new events arrive
  - Writing data transactionally to output systems
  - Updating your application’s business logic at runtime

## Stream Processing Design Points

### Record-at-a-Time v/s Declarative APIs

- simplest way to design a streaming API is to pass each event to application and let it react usin custom logic, this approach seems useful when application wants to have full control over data processing.
- however downside is most of the above complications are now application’s problem!. You need to maintain states, responding to failures etc.
- Newer streaming system provide *declarative APIs*, where application specify what to compute but not how to compute in response to each new event and how to recover on failures. e.g. Spark’s original DStream lib used to do that offering `map`, `reduce` and `filter` on streams.

### Event Time vs Processing Time

for systems with declarative APIs second problem is does the system natively supports event time ? Event time is idea of processing data based on timestamps inserted into each record at the source, as opposed to time when record is received (*processing time*).

- When using event times, records may come at different times and out of order (network latency), If system derives important information/patterns from order of information then you may be in big trouble.
- If application only processes local events only we may not sophisticated event-time processing.

Because of this, many declarative systems, including Structured  Streaming, have “native” support for event time integrated into all  their APIs, so that these concerns can be handled automatically across  your whole program.

### Continuous vs Micro-Batch Execution

*latency* determines usage of one over other. Continous Execution provide low latency (at least when input rate is low) while Micro-Batching does take some time to execute.

As input rate of data scales we are better off using Micro-Batching to avoid overhead of per-record processing.

Micro Batches can wait to accumulate small batches of input data (500ms worth of data) then each bacth can be processed parallely on a cluster of machines and we can often obtain high throughput per node because of batch systems optimizations.

## Spark’s Streaming APIs

Spark has two APIs for streaming

### The DStream API

- original API of spark since 2012 release. Many companies use it in production. Interactions with RDD code, such as joins with static data, are also natively supported in Spark Streaming.
- DStreams has several limitations tho
  - Based purely on Java/Python objects and functions, as opposed to riched concept of structured tables in DataFrames and Datasets which limits the engine’s oppotunity to perform optimizations
  - API is purely based on processing time-to handle event-time operations
  - DStreams can only operate in a micro-batch fashion and exposes the duration of micro batches in some parts of its API, making it difficult to support alternative execution modes

### Structured Streaming

- higher level streaming API formed from Spark’s Structured API
- Available on all supported languages
- Native support for event time data, all of its the windowing operators automatically support it.
- Structured Streaming doesn’t use a separate API from DataFrames.
- As another example, Structured Streaming can output data to standard  sinks usable by Spark SQL, such as Parquet tables, making it easy to  query your stream state from another Spark applications



---

## File: pyspark/notes/ch21.md

# Structured Streaming Basics

- Structured Streaming is a stream processing framework built on Spark SQL engine which uses existing DataFrames API simplifying writing streaming code.
- Structured Streaming ensures end-to-end, exactly once processing as well as fault tolerance through checkpointing and write ahead logs.

## Core Concepts

- spark aims to simplify stream processing and avoids too much complex terminologies.

### Transformation and Actions

- same concept of transformation and actions from DataFrames APIs.
- some of transformation will have a few restrictions on some type of queries that cannot be incrementalize yet.

### Input Sources

- several input sources are supported
  - Apache Kafka 0.10
  - Files on distributed file system like HDFS or S3
  - A socket source for testing.

### Sinks

- several output sources are supported
  - Apache Kafka 0.10
  - Almost any file format
  - A foreach sink for running arbitary computation on the records
  - A console sink for testing
  - A memory sink for debugging

### Output Modes

- defines how data is written on the sink i.e. append or update
- The supported output modes are
  - *Append* : only add new records to the ouput sink
  - *Update* : Update changed records in place
  - *Complete* : Rewrite the full output

### Triggers

- when data is output  - by default Structured Streaming will look for new input records as soon as it finished processing the last group of input data, giving lowest latency for new results.
- However this behaviour can lead to many small ouput writes when sink is set of files. We can trigger based on processing time.

### Event-Time Processing

- *Processing data based on timestamps included in the record that may arrive out of order*

#### Event Time Data

- Event-Time : *time fields are embedded in data*. Processing is based on time of generation of data.
- Expressing event-time processing is simple in Structured Streaming.  Because the system views the input data as a table, the event time is  just another field in that table, and your application can do grouping,  aggregation, and windowing using standard SQL operators.
- Structured Streaming automatically optimizes when it knows a column is an event-time field based on *watermark* controls

### Watermarks

- *feature* of Structured Streaming that allows to specify how late they expect to see data in event time.
- We can also set how long to remember the old data, when to ouput a result for a particular time window.

## Structured Streaming in Action

- Data that we are using is sensor readings at high frequency : https://github.com/databricks/Spark-The-Definitive-Guide/tree/master/data

````python
static = spark.read.json("/data/activity-data/")
dataSchema = static.schema
static.printScehma()
root
 |-- Arrival_Time: long (nullable = true)
 |-- Creation_Time: long (nullable = true)
 |-- Device: string (nullable = true)
 |-- Index: long (nullable = true)
 |-- Model: string (nullable = true)
 |-- User: string (nullable = true)
 |-- _corrupt_record: string (nullable = true)
 |-- gt: string (nullable = true)
 |-- x: double (nullable = true)
 |-- y: double (nullable = true)
 |-- z: double (nullable = true)
````

Let’s create streaming version of this data

````python
streaming = spark.readStream.schema(dataSchema).option("maxFilesPerTrigger", 1)\
  .json("/data/activity-data")

# just like DataFrame APIs, streaming DF creation and execution is also lazy.
# defining transformations

activityCounts = streaming.groupBy("gt").count()

# NOTE: since this code running in local set shuffle partitions to 5 
spark.conf.set("spark.sql.shuffle.partitions", 5)

# specify action to start the query on an output sink

activityQuery = activityCounts.writeStream.queryName("activity_counts")\
  .format("memory").outputMode("complete")\
  .start()

# terminate the query to prevent the driver from exiting while query is stil running
# activityQuery.awaitTermination()


# Now in antoher Spark Session we can see all active streams
spark.streams.active	# Return UUIDs, and we can select the stream, but we already that in variable

````

- Now that this stream is running, we can experiment with the results by  querying the in-memory table it is maintaining of the current output of  our streaming aggregation. This table will be called `activity_counts`, the same as the stream.

````python
from time import sleep
for x in range(5):
    spark.sql("SELECT * FROM activity_counts").show()
    sleep(1)
````

## Transformations on Streams

- limitation arise from transformation in stream are actually logical, `sort` doesn’t make sense in streams that are not aggregated, you cannot perform multi-level aggregation without Stateful Processing

### Selection and Filtering

- All select and filter transformation & All individual column manipulations are supported.

````python
from pyspark.sql.functions import expr
simpleTransform = streaming.withColumn("stairs", expr("gt like '%stairs%'"))\
  .where("stairs")\
  .where("gt is not null")\
  .select("gt", "model", "arrival_time", "creation_time")\
  .writeStream\
  .queryName("simple_transform")\
  .format("memory")\
  .outputMode("append")\
  .start()
````

### Aggregations

- we could specify exotice aggregations like cube on the phone model and activity and average x,y,z of sensors.

````python
deviceModelStats = streaming.cube("gt", "model").avg()\
  .drop("avg(Arrival_time)")\
  .drop("avg(Creation_Time)")\
  .drop("avg(Index)")\
  .writeStream.queryName("device_counts").format("memory")\
  .outputMode("complete")\
  .start()
````

### Joins

````python
historicalAgg = static.groupBy("gt", "model").avg()
deviceModelStats = streaming.drop("Arrival_Time", "Creation_Time", "Index")\
  .cube("gt", "model").avg()\
  .join(historicalAgg, ["gt", "model"])\
  .writeStream.queryName("device_counts").format("memory")\
  .outputMode("complete")\
  .start()
````

## Input and Output

Documentations : http://spark.apache.org/docs/latest/structured-streaming-programming-guide.html



### Source and Sinks

#### File Source and Sink

- simplest source is file source. We have seen Parquet, text, JSON, and CSV
- Only difference between using file source/sink and Spark’s static file source is that with streaming, we can control how many file we read during each trigger vis `maxFilesPerTrigger` option.

#### Kafka source and sink

- Kafka is a distributed publish and subscribe system for data.
- Each record on Kakfa consists of a Key, Value and Timestamp. Topics consist of immutable sequences of records for which teh position of a record in a sequence is called an offset. Reading data is called *subscribing* to a topic, writing data is called as *publishing* to a topic.
- Spark allows you to read from Kafka with both batch and streaming DataFrames.

### Reading from a Kafka Source

To read, you first need to choose one of the following options: `assign`, `subscribe`, or `subscribePattern`

- Assign : Fine grained way of specify not just topic but also the topic partitions from which we would like `{"topicA":[0,1],"topicB":[2,4]}`
- subscribe and subscribePattern are ways of subscribing to one or more topics either specifying a list of topics or via a pattern

Secondly, we specify `kafka.bootstrap.servers` that Kafka provides to connect to the service.

Other options we can choose :

- `startingOffsets` and `endingOffsets` : The start point when a query is started, either `earliest`, which is from the earliest offsets; `latest`, which is just from the latest offsets; or a JSON string specifying a starting offset for each `TopicPartition`. This applies only when a new Streaming query is started, and that  resuming will always pick up from where the query left off. Newly  discovered partitions during a query will start at earliest. The ending  offsets for a given query.
- `failOnDataLoss` : Whether to fail the query when it’s possible that data is lost (e.g.,  topics are deleted, or offsets are out of range). This might be a false alarm. You can disable it when it doesn’t work as you expected. The default is `true`.
- `maxOffsetsPerTrigger` : total number of offsets to read in given triggers

````python
df1 = spark.readStream.format("kafka")\
  .option("kafka.bootstrap.servers", "host1:port1,host2:port2")\
  .option("subscribe", "topic1")\
  .load()
# Subscribe to multiple topics
df2 = spark.readStream.format("kafka")\
  .option("kafka.bootstrap.servers", "host1:port1,host2:port2")\
  .option("subscribe", "topic1,topic2")\
  .load()
# Subscribe to a pattern
df3 = spark.readStream.format("kafka")\
  .option("kafka.bootstrap.servers", "host1:port1,host2:port2")\
  .option("subscribePattern", "topic.*")\
  .load()
````

Each row in the source will have the following schema:

- key: binary
- value: binary
- topic: string
- partition: int
- offset: long
- timestamp: long

### Writing to a Kafka Sink

````python
df1.selectExpr("topic", "CAST(key AS STRING)", "CAST(value AS STRING)")\
  .writeStream\
  .format("kafka")\
  .option("kafka.bootstrap.servers", "host1:port1,host2:port2")\
  .option("checkpointLocation", "/to/HDFS-compatible/dir")\
  .start()
df1.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")\
  .writeStream\
  .format("kafka")\
  .option("kafka.bootstrap.servers", "host1:port1,host2:port2")\
  .option("checkpointLocation", "/to/HDFS-compatible/dir")\
  .option("topic", "topic1")\
  .start()
````

#### Foreach Sink

- similar to `foreachPartitions` in Dataset API, allowing arbitrary operation to be computed on a per-partition basis, in parallel.
- To use `foreach` sink we need to implement `ForeachWriter` interface, which contains `open`, `process`, and `close`
- NOTE:
  - writer must be Serializable, as it were a UDF or Dataset Map Function
  - three methods(`open`, `process`, and `close`) will be called on each executor
  - writer must do all its initialization, like opening connections or starting transactions using only in the `open` method.
- Because the Foreach sink runs arbitrary user code, one key issue you  must consider when using it is fault tolerance. If Structured Streaming  asked your sink to write some data, but then crashed, it cannot know  whether your original write succeeded. Therefore, the API provides some  additional parameters to help you achieve exactly-once processing.
- First, the `open` call on your `ForeachWriter` receives two parameters that uniquely identify the set of rows that need to be acted on. The `version` parameter is a monotonically increasing ID that increases on a per-trigger basis, and `partitionId` is the ID of the partition of the output in your task

````scala
//in Scala
datasetOfString.write.foreach(new ForeachWriter[String] {
  def open(partitionId: Long, version: Long): Boolean = {
    // open a database connection
  }
  def process(record: String) = {
    // write string to connection
  }
  def close(errorOrNull: Throwable): Unit = {
    // close the connection
  }
})
````

#### Sources and sinks for testing

Spark also includes several test sources and sinks that you can use for  prototyping or debugging your streaming queries (these should be used  only during development and not in production scenarios

*Socket Source*

```python
socketDF = spark.readStream.format("socket")\
  .option("host", "localhost").option("port", 9999).load()
```

Now netcat the port

````bash
nc -lk 9999
````

*console sink*

```
activityCounts.format("console").write()
```

*memory sink*

```
activityCounts.writeStream.format("memory").queryName("my_device_table")
```

### How Data is Output (Modes)

- Append Mode : when new rows are added to result table, they will be output to sink based on trigger we specify. Ensures that each row is ouput once assuming a fault-tolerant sink
- Complete Mode: outputs entire state of the result table to output sink, usefule when working with statful data where all rows change over time or the sink we are writing doesn’t support row-level updates
- Update Mode: only the rows that are different from previous write are written out. Sink must support row-level updates for this to work. If query doesn’t have aggregation its similar to append mode.

There are three modes of output but when to use which one ?

If your query just does a `map` operation, Structured Streaming will not allows complete mode, because this would require it to remember all inputs since start of the job and rewrite whole ouput table.

### When Data is Output (Triggers)

To control when data is output to our sink, we set a *trigger*. By default, Structured Streaming will start data as soon as the  previous trigger completes processing. You can use triggers to ensure  that you do not overwhelm your output sink with too many updates or to  try and control file sizes in the output.

#### Processing time trigger

````bash
activityCounts.writeStream.trigger(processingTime='5 seconds')\
  .format("console").outputMode("complete").start()
````

Trigger is fired at every five seconds

#### Once Trigger

- useful in production/development : in dev, we can test application on just one trigger worth of data at a Time, in prod we can use it to run job manually at low rate.

````bash
activityCounts.writeStream.trigger(once=True)\
  .format("console").outputMode("complete").start()
````



## Streaming Dataset API

- Note Structured Streaming is not limite to DataFrame API for streaming, we can use Datasets to perform same computation in a type safe manner.

````scala
// in Scala
case class Flight(DEST_COUNTRY_NAME: String, ORIGIN_COUNTRY_NAME: String,
  count: BigInt)
val dataSchema = spark.read
  .parquet("/data/flight-data/parquet/2010-summary.parquet/")
  .schema
val flightsDF = spark.readStream.schema(dataSchema)
  .parquet("/data/flight-data/parquet/2010-summary.parquet/")
val flights = flightsDF.as[Flight]
def originIsDestination(flight_row: Flight): Boolean = {
  return flight_row.ORIGIN_COUNTRY_NAME == flight_row.DEST_COUNTRY_NAME
}
flights.filter(flight_row => originIsDestination(flight_row))
  .groupByKey(x => x.DEST_COUNTRY_NAME).count()
  .writeStream.queryName("device_counts").format("memory").outputMode("complete")
  .start()
````



---

## File: pyspark/notes/ch22.md

# Event-Time And Stateful Processing

## Event Time

- NOTE: Spark’s DStream API doesn’t support processing information wrt event-time
- There are two relevant times:
  - Event Time : time that is embedded in data itself. The challenge here is that event data can be late or out of order. This  means that the stream processing system must be able to handle  out-of-order or late data.
  - Processing Time : time at which stream processing system actually recieves data. Usually less important. This can’t ever be out of order because its a property of streaming system at a certain time.
- Order of the series of events in the processing system does not guarantee an ordering in event time. Computer networks are unreliable. That means that events can be dropped, slowed down, repeated, or be sent without issue. 

## Stateful Processing

- Stateful processing is only necessary when you need to use or update intermediate information (state) over longer periods of time (in either a microbatch or a record-at-a-time approach). This can happen when you are using event time or when you are performing an aggregation on a key, whether that involves event time or not.
- spark handles all the complexity entailing stateful processing for you. We just need to specify the logic. Spark storest state in a state *store*.

## Arbitrary Stateful Processing

- sometimes  we need fine grained control on what state should be stored, how its updated and when it should be removed, either explicitly or via a time-out.
- Some scenario where it might be used
  - We would like to record information about user sessions on an ecommerce site. Track what user visits over the course of this session in order to provide recommendation in real time during next time.
  - Report on errors in the web application but only if five events occurs during a user’s session. Count-based windows that emit result if five events of some type occur.
  - Deduplicate records over time requires tracking every record that you see before deduplication it.

## Event-Time Basics

````python
# contd. from previous chapter
spark.conf.set("spark.sql.shuffle.partitions", 5)
static = spark.read.json("/data/activity-data")
streaming = spark\
  .readStream\
  .schema(static.schema)\
  .option("maxFilesPerTrigger", 10)\
  .json("/data/activity-data")

streaming.printSchema()
````

- Notice how this dataset has `Creation_Time` defining event time, whereas the `Arrival_Time` defines when an event hit our servers somewere upstream.

## Windows on Event Time

First step is to convert timstamp column into proper Spark SQL timestamp type.

````python
withEventTime = streaming\.selectExpr(
  "*",
  "cast(cast(Creation_Time as double)/1000000000 as timestamp) as event_time")
````

### Tumbling Windows

- count the number of occurences of an event in a given window.

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_2202.png)

- we perform aggregation of keys over a window of time. but we operate data recieved since the last trigger.

- for dataset we will use 10 min windows.

````python
from pyspark.sql.functions import window, col
withEventTime.groupBy(window(col("event_time"), "10 minutes")).count()\
  .writeStream\
  .queryName("pyevents_per_window")\
  .format("memory")\
  .outputMode("complete")\
  .start()
````

- we’re writing out to the in-memory sink for debugging, so we can query it with SQL after we have the stream running

````python
spark.sql("SELECT * FROM events_per_window").printSchema()
# or
# SELECT * FROM events_per_window

root
 |-- window: struct (nullable = false)
 |    |-- start: timestamp (nullable = true)
 |    |-- end: timestamp (nullable = true)
 |-- count: long (nullable = false)
````

- Note: how previous window is actually a `struct` (a complex type). Using this we can query this `struct` for start and end time of a particular window
- Of importance is the fact that we can also perform an aggregation on  multiple columns, including the event time column. Just like we saw in  the previous chapter, we can even perform these aggregations using  methods like `cube`

````python
from pyspark.sql.functions import window, col
withEventTime.groupBy(window(col("event_time"), "10 minutes"), "User").count()\
  .writeStream\
  .queryName("pyevents_per_window")\
  .format("memory")\
  .outputMode("complete")\
  .start()
````

### Sliding Windows

- decouple window from the starting time of the window

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_2203.png)

- we run a sliding window through which we look at an hour increment, but we’d like to know state every 10 minutes

````python
from pyspark.sql.functions import window, col
withEventTime.groupBy(window(col("event_time"), "10 minutes", "5 minutes"))\
  .count()\
  .writeStream\
  .queryName("pyevents_per_window")\
  .format("memory")\
  .outputMode("complete")\
  .start()

# SELECT * FROM events_per_window
````

### Handling Late Data with Watermarks

- all previous examples we didn’t define how late we expect to see data, meaning spark will wait forever for data because we didn’t specify watermark, or a time at which we don’t expect to see any more data.
- we must define watermark in order to age-out data in the stream, so that we don’t overwhelm the system over a long period of time. DStream did not have this way to handle data and lost events may appear on other processing bacthes.

````python
from pyspark.sql.functions import window, col
withEventTime\
  .withWatermark("event_time", "30 minutes")\
  .groupBy(window(col("event_time"), "10 minutes", "5 minutes"))\
  .count()\
  .writeStream\
  .queryName("pyevents_per_window")\
  .format("memory")\
  .outputMode("complete")\
  .start()

# SELECT * FROM events_per_window
````

## Dropping Duplicates in a Stream

- multiple publish of data multiple times is common in IoT application and deduplication require high coordination, so its very important task.
- Structured Streaminng makes it easy to take message system that provide at least once semantics, and convert them into exactly-once by dropping duplicate message as they come in, based on arbitrary keys. To de-duplicate data, Spark  will maintain a number of user specified keys and ensure that duplicates are ignored.

````python

from pyspark.sql.functions import expr

withEventTime\
  .withWatermark("event_time", "5 seconds")\
  .dropDuplicates(["User", "event_time"])\
  .groupBy("User")\
  .count()\
  .writeStream\
  .queryName("pydeduplicated")\
  .format("memory")\
  .outputMode("complete")\
  .start()
````

## Arbitrary Stateful Processing

- While performing stateful processing, we might want to do following
  - create a window based on counts of a given key
  - emit an alert if there is a number of events within a certain time frame
  - Maintain user sessions of an undetermined amount of time and save those sessions to perform analysis on later
- Effectively we will want to two things
  - Map over groups in your data, operate on each group of data, and generate at most a single row for each group. `mapGroupsWithState` API
  - Map over groups in your data, operate on each group of data, and generate one or more rows for each group. `flatMapGroupsWithState` 

### Time-Outs

- Time we should wait before timing-out some intermediate state. global parameter across all groups that is configured on a per-group basis.
- Time-outs can be either based on processing time or event time.
- While using timeouts, check for time-out first before processing values using `state.hasTimedOut` or checking if values iterator is empty.
- We can set timeout duration using `GroupState.setTimeoutDuration`. The time-out will occur when the clock advances by set duration.
  - Time-out will never occur before the clock time has advanced by D ms
  - Time will occur eventually when there is a trigger in the query(after Dms). So there is no strict upper bound on when time-out would occur.
- Since time-out is based on clock-time, it is affected by system clock and timezone variations
- When using a time-out based on event time, the user also must specify the event-time watermark in query using watermarks. When set, data older than the watermark is filtered out. As the developer, you can set the timestamp that the watermark should reference by setting a time-out timestamp using the `GroupState.setTimeoutTimestamp(...)` API
- there is a no strict upper bound on the delay when the time-out actually occurs. The watermark can advance only when there is data in the  stream, and the event time of the data has actually advanced

### Output Modes

NOTE:`mapGroupsWithState` supports update mode only while `flatMapGroupsWithState` supports `append` and `update` mode.

Both are still experimental features in 3.5.1 Spark. Check documentation for more information.

### mapGroupWithState

- We can control arbitrary state by creating it, updating it over time, and removing it using following things
  - Three class definitions: an input definition, a state definition, and optionally an output definition.
  - A function to update state based on a key, an iterator of events and a previous state.
  - A time-out parameter.
- Ex - Simply update keys based on certain amount of state in sensor data.So keys for grouping here are grouping(mapping on) is a user and activity combination (first and last timestamp)

````scala
// input, state and output definitions
case class InputRow(user:String, timestamp:java.sql.Timestamp, activity:String)
case class UserState(user:String,
  var activity:String,
  var start:java.sql.Timestamp,
  var end:java.sql.Timestamp)

// set up the function that defines how you will update your state based on a given row
def updateUserStateWithEvent(state:UserState, input:InputRow):UserState = {
  if (Option(input.timestamp).isEmpty) {
    return state
  }
  if (state.activity == input.activity) {

    if (input.timestamp.after(state.end)) {
      state.end = input.timestamp
    }
    if (input.timestamp.before(state.start)) {
      state.start = input.timestamp
    }
  } else {
    if (input.timestamp.after(state.end)) {
      state.start = input.timestamp
      state.end = input.timestamp
      state.activity = input.activity
    }
  }

  state
}

// define a function defining the way state is updated based on an epoch of rows
import org.apache.spark.sql.streaming.{GroupStateTimeout, OutputMode, GroupState}
def updateAcrossEvents(user:String,
  inputs: Iterator[InputRow],
  oldState: GroupState[UserState]):UserState = {
  var state:UserState = if (oldState.exists) oldState.get else UserState(user,
        "",
        new java.sql.Timestamp(6284160000000L),
        new java.sql.Timestamp(6284160L)
    )
  // we simply specify an old date that we can compare against and
  // immediately update based on the values in our data

  for (input <- inputs) {
    state = updateUserStateWithEvent(state, input)
    oldState.update(state)
  }
  state
}
````

````scala
// usually you should set a time-out for a given group's state (its omitted here)
// Querying above Stream
import org.apache.spark.sql.streaming.GroupStateTimeout
withEventTime
  .selectExpr("User as user",
    "cast(Creation_Time/1000000000 as timestamp) as timestamp", "gt as activity")
  .as[InputRow]
  .groupByKey(_.user)
  .mapGroupsWithState(GroupStateTimeout.NoTimeout)(updateAcrossEvents)
  .writeStream
  .queryName("events_per_window")
  .format("memory")
  .outputMode("update")
  .start()
````

````sql
SELECT * FROM events_per_window order by user, start

+----+--------+--------------------+--------------------+
|user|activity|               start|                 end|
+----+--------+--------------------+--------------------+
|   a|    bike|2015-02-23 13:30:...|2015-02-23 14:06:...|
|   a|    bike|2015-02-23 13:30:...|2015-02-23 14:06:...|
...
|   d|    bike|2015-02-24 13:07:...|2015-02-24 13:42:...|
+----+--------+--------------------+--------------------+
````

####  Example : Count-Based Windows

- usually window operations revolve around a start and end time and counting or summing up in that window. Sometimes we may wish to create windows based on counting only regardless of state and event times, and perform some aggregation on that window.
- Example : Output average reading of each device periodically creating a window based on count of events and outputting it each time it has 500 events for that device

````scala
// input, state and output definitions
case class InputRow(device: String, timestamp: java.sql.Timestamp, x: Double)
case class DeviceState(device: String, var values: Array[Double],
  var count: Int)
case class OutputRow(device: String, previousAverage: Double)

// update function
def updateWithEvent(state:DeviceState, input:InputRow):DeviceState = {
  state.count += 1
  // maintain an array of the x-axis values
  state.values = state.values ++ Array(input.x)
  state
}

// function that updates states across a series of input rows
mport org.apache.spark.sql.streaming.{GroupStateTimeout, OutputMode,
  GroupState}

def updateAcrossEvents(device:String, inputs: Iterator[InputRow],
  oldState: GroupState[DeviceState]):Iterator[OutputRow] = {
  inputs.toSeq.sortBy(_.timestamp.getTime).toIterator.flatMap { input =>
    val state = if (oldState.exists) oldState.get
      else DeviceState(device, Array(), 0)

    val newState = updateWithEvent(state, input)
    if (newState.count >= 500) {
      // One of our windows is complete; replace our state with an empty
      // DeviceState and output the average for the past 500 items from
      // the old state
      oldState.update(DeviceState(device, Array(), 0))
      Iterator(OutputRow(device,
        newState.values.sum / newState.values.length.toDouble))
    }
    else {
      // Update the current DeviceState object in place and output no
      // records
      oldState.update(newState)
      Iterator()
    }
  }
}
````

````scala
// run stream
import org.apache.spark.sql.streaming.GroupStateTimeout

withEventTime
  .selectExpr("Device as device",
    "cast(Creation_Time/1000000000 as timestamp) as timestamp", "x")
  .as[InputRow]
  .groupByKey(_.device)
  .flatMapGroupsWithState(OutputMode.Append,
    GroupStateTimeout.NoTimeout)(updateAcrossEvents)
  .writeStream
  .queryName("count_based_device")
  .format("memory")
  .outputMode("append")
  .start()
````

````sql
SELECT * FROM count_based_device

+--------+--------------------+
|  device|     previousAverage|
+--------+--------------------+
|nexus4_1|      4.660034012E-4|
|nexus4_1|0.001436279298199...|
...
|nexus4_1|1.049804683999999...|
|nexus4_1|-0.01837188737960...|
+--------+--------------------+
````

### flatMapGroupsWithState

- rather than having a single key with at most one output, a single key may have many outputs providing more flexibility as compared to `mapGroupWithState`
- Things we need to define remain same as we defined with `mapGroupWithState`

#### Example : Sessionization

- Sessions are simply unspecified time windows with a series of events that occur.
- We want to record these different events in an array in order to compare these sessions to other sessions in the future.
- In a session, you will likely have arbitrary logic to maintain and update your state over time as well as certain actions to define when state ends (like a count) or a simple time-out.
- Often times there will be a session ID that we can use making it easier, lets create sessions on the fly here since there is no session ID

````scala
// input, state, and output
case class InputRow(uid:String, timestamp:java.sql.Timestamp, x:Double,
  activity:String)
case class UserSession(val uid:String, var timestamp:java.sql.Timestamp,
  var activities: Array[String], var values: Array[Double])
case class UserSessionOutput(val uid:String, var activities: Array[String],
  var xAvg:Double)

// a function to change state
def updateWithEvent(state:UserSession, input:InputRow):UserSession = {
  // handle malformed dates
  if (Option(input.timestamp).isEmpty) {
    return state
  }

  state.timestamp = input.timestamp
  state.values = state.values ++ Array(input.x)
  if (!state.activities.contains(input.activity)) {
    state.activities = state.activities ++ Array(input.activity)
  }
  state
}


// method to work on epoch of rows
import org.apache.spark.sql.streaming.{GroupStateTimeout, OutputMode,
  GroupState}

def updateAcrossEvents(uid:String,
  inputs: Iterator[InputRow],
  oldState: GroupState[UserSession]):Iterator[UserSessionOutput] = {

  inputs.toSeq.sortBy(_.timestamp.getTime).toIterator.flatMap { input =>
    val state = if (oldState.exists) oldState.get else UserSession(
    uid,
    new java.sql.Timestamp(6284160000000L),
    Array(),
    Array())
    val newState = updateWithEvent(state, input)

    if (oldState.hasTimedOut) {
      val state = oldState.get
      oldState.remove()
      Iterator(UserSessionOutput(uid,
      state.activities,
      newState.values.sum / newState.values.length.toDouble))
    } else if (state.values.length > 1000) {
      val state = oldState.get
      oldState.remove()
      Iterator(UserSessionOutput(uid,
      state.activities,
      newState.values.sum / newState.values.length.toDouble))
    } else {
      oldState.update(newState)
      oldState.setTimeoutTimestamp(newState.timestamp.getTime(), "5 seconds")
      Iterator()
    }

  }
}
````

```scala
// create a query
import org.apache.spark.sql.streaming.GroupStateTimeout

withEventTime.where("x is not null")
  .selectExpr("user as uid",
    "cast(Creation_Time/1000000000 as timestamp) as timestamp",
    "x", "gt as activity")
  .as[InputRow]
  .withWatermark("timestamp", "5 seconds")
  .groupByKey(_.uid)
  .flatMapGroupsWithState(OutputMode.Append,
    GroupStateTimeout.EventTimeTimeout)(updateAcrossEvents)
  .writeStream
  .queryName("count_based_device")
  .format("memory")
  .start()
```

````sql
SELECT * FROM count_based_device

+---+--------------------+--------------------+
|uid|          activities|                xAvg|
+---+--------------------+--------------------+
|  a|  [stand, null, sit]|-9.10908533566433...|
|  a|   [sit, null, walk]|-0.00654280428601...|
...
|  c|[null, stairsdown...|-0.03286657789999995|
+---+--------------------+--------------------+
````

- Notice how session that have number of activities in them have higher x-axis gyroscope value than ones that ahve fewer activities

---

## File: pyspark/notes/ch23.md

# Structured Streaming in Production

- Structured Streaming was marked as production-ready in Apache Spark 2.2.0, meaning that this release has all the features required for production use and stabilizes the API.

## Fault Tolerance and Checkpointing

- failure recovery is a important operational concern, faults are inevitable like losing connection to a cluster, schema changes or intentional restart.
- Structured Streaming allows recovering an application by just restarting it. To do this enable checkpointing and write-ahead logs, both of which are handled automatically by the engine.
- We must configure a query to write to a *checkpoint location* on a reliable file system which is used for periodic saving of all relevant progress information as well as current intermediate state values to the checkpoint location.

````python
static = spark.read.json("/data/activity-data")
streaming = spark\
  .readStream\
  .schema(static.schema)\
  .option("maxFilesPerTrigger", 10)\
  .json("/data/activity-data")\
  .groupBy("gt")\
  .count()
query = streaming\
  .writeStream\
  .outputMode("complete")\
  .option("checkpointLocation", "/some/python/location/")\
  .queryName("test_python_stream")\
  .format("memory")\
  .start()
````

## Updating Your Application

- checkpointing helps us with information about stream processed thus far and what intermediate state it may be storing but it has small catch - we might reason our old checkpoint when we update our streaming application. Make sure that update is not a breaking change to avoid such situations.

### Updating your streaming application code

- Structured Streaming allows certain types of chagnes to application code between restarts. 
  - you can change UDFs as long as they have same type signature.
  - adding a new columns is also not a breaking change for checkpoint directory.
- If you update your streaming application to add new aggregation key or fundamental changes to query itself, Spark cannot construct the required state for query using checkpoint directory.

### Updating Your Spark Version

- Structured Streaming applications should be able to restart from an old checkpoint directory across patch version upgrades to spark. (2.2.0 -> 2.2.1 -> 2.2.2).
- Checkpoint format is designed to forward-compatible, so the only way it breaks due to critical bug fixes. Check Spark notes before upgrading.

### Sizing and Rescaling your Applications

- Ideally, cluster should be big enough to comfortable handle bursts above your data rate. The metrics you should be monitoring for are :
  - Input rate is much higher than processing rate (elaborated or momentarily)
  - You can dynamically add executors to your application. When it comes time you can scale-down your application same way.
- These change usually require a restart of application or stream with a new configuration. For example `spark.sql.shuffle.partitions` can not be updated while a stream is currently running.

## Metrics and Monitoring

- Mostly Metric and Monitoring for streaming application is same as general spark applications, but there are more specifics to help you beter understand state of your application.
- There are two key APIs you can leverage to query the status of a streaming query

### Query Status

- It answers : “What processing is my stream performing right now”. This is reported in the `status` field of the query object returned by `startStream`

````bash
query.status

{
  "message" : "Getting offsets from ...",
  "isDataAvailable" : true,
  "isTriggerActive" : true
}
````

### Recent Progress

````bash
query.recentProgress

# Scala Version
Array({
  "id" : "d9b5eac5-2b27-4655-8dd3-4be626b1b59b",
  "runId" : "f8da8bc7-5d0a-4554-880d-d21fe43b983d",
  "name" : "test_stream",
  "timestamp" : "2017-08-06T21:11:21.141Z",
  "numInputRows" : 780119,
  "processedRowsPerSecond" : 19779.89350912779,
  "durationMs" : {
    "addBatch" : 38179,
    "getBatch" : 235,
    "getOffset" : 518,
    "queryPlanning" : 138,
    "triggerExecution" : 39440,
    "walCommit" : 312
  },
  "stateOperators" : [ {
    "numRowsTotal" : 7,
    "numRowsUpdated" : 7
  } ],
  "sources" : [ {
    "description" : "FileStreamSource[/some/stream/source/]",
    "startOffset" : null,
    "endOffset" : {
      "logOffset" : 0
    },
    "numInputRows" : 780119,
    "processedRowsPerSecond" : 19779.89350912779
  } ],
  "sink" : {
    "description" : "MemorySink"
  }
})
````

- *Input rate and processing rate*
- *Batch Duration* : all streaming systems utilize batching to operate at any reasonable throughput. Structured Streaming achieves both.

### Spark UI

The Spark web UI, covered in earlier topics, also shows tasks, jobs, and data processing metrics for Structured  Streaming applications. On the Spark UI, each streaming application will appear as a sequence of short jobs, one for each trigger.

## Alerting

## Advanced Monitoring with the Streaming Listener

- we can use status and query Progress APIs to output monitoring events into your organization’s monitoring platform (Prometheus, etc.). There is also a lower-level but more powerful way to observe an application’s execution using `StreamingQueryListener` class
- This class will allow you to receive asynchronous updates from the streaming query in roder to automatically output this information to other systems and implement robust monitoring and alerting mechanisms.

````scala
val spark: SparkSession = ...

spark.streams.addListener(new StreamingQueryListener() {
    override def onQueryStarted(queryStarted: QueryStartedEvent): Unit = {
        println("Query started: " + queryStarted.id)
    }
    override def onQueryTerminated(
      queryTerminated: QueryTerminatedEvent): Unit = {
        println("Query terminated: " + queryTerminated.id)
    }
    override def onQueryProgress(queryProgress: QueryProgressEvent): Unit = {
        println("Query made progress: " + queryProgress.progress)
    }
})
````

- the following code for a `StreamingQueryListener` that will  forward all query progress information to Kafka. You’ll have to parse  this JSON string once you read data from Kafka in order to access the  actual metrics

````scala
class KafkaMetrics(servers: String) extends StreamingQueryListener {
  val kafkaProperties = new Properties()
  kafkaProperties.put(
    "bootstrap.servers",
    servers)
  kafkaProperties.put(
    "key.serializer",
    "kafkashaded.org.apache.kafka.common.serialization.StringSerializer")
  kafkaProperties.put(
    "value.serializer",
    "kafkashaded.org.apache.kafka.common.serialization.StringSerializer")

  val producer = new KafkaProducer[String, String](kafkaProperties)

  import org.apache.spark.sql.streaming.StreamingQueryListener
  import org.apache.kafka.clients.producer.KafkaProducer

  override def onQueryProgress(event:
    StreamingQueryListener.QueryProgressEvent): Unit = {
    producer.send(new ProducerRecord("streaming-metrics",
      event.progress.json))
  }
  override def onQueryStarted(event:
    StreamingQueryListener.QueryStartedEvent): Unit = {}
  override def onQueryTerminated(event:
    StreamingQueryListener.QueryTerminatedEvent): Unit = {}
}
````

---

## File: pyspark/notes/ch24.md

# Advanced Analytics and Machine Learning Overview

Beyond large-scale SQL analysis and streaming, Spark also provides support for statistics, machine learning, and graph analytics. These encompass a set of workloads that we will refer to as advanced analytics.

## A Short Primer on Advanced Analytics

- Advanvced Analytics refers to techniques solving core problems of deriving insights and making predictions or recommendation based on data.
- Commong Tasks involve :
  - Supervised Learning, including Classification and Regression, where gol is to predict a label for each data point based on various features
  - Recommendation Engines to suggest products to user’s based on behaviour
  - Unsuperivised leraning, including clustering, anomaly detection and topic modelling, which goal is discover structure in data.
  - Graph Analytic tasks such as searching for patterns in a social network.
- Great Resources
  - [*An Introduction to Statistical Learning*](http://www-bcf.usc.edu/~gareth/ISL/) by Gareth James, Daniela Witten, Trevor Hastie, and Robert Tibshirani. We refer to this book as “ISL.”
  - [*Elements of Statistical Learning*](https://web.stanford.edu/~hastie/ElemStatLearn/) by Trevor Hastie, Robert Tibshirani, and Jerome Friedman. We refer to this book as “ESL.”
  - [*Deep Learning*](http://www.deeplearningbook.org/) by Ian Goodfellow, Yoshua Bengio, and Aaron Courville. We refer to this book as “DLB.”

### Supervised Learning

- goal : using historical data that already has labels, train a model to predict values of those labels based on various features of data points.
- This training process usually proceeds through an iterative optimization algorithm such as gradient descent, starting with basic model and improving it by configuring internal parameters during each training iteration.

#### Classification

- act of training an algorithm to predict a dependent variable that is *categorical*
- Most common case is *Binary Classifier*, where resulting model makes prediction that a item belongs to one of two groups. Eg. selecting a spam mail.
- If we have more that two categories we call it *multiclass classification*
- Use Cases
  - Predicting Diseases: Historical data of behaviour and physiological attributes of set of patients.
  - Classifying Images
  - Predicting Customer Churn : predicting which customer is likely to stop using a service
  - Buy or won’t buy

#### Regression

- In classification, dependent variable was discrete. In regression we try to predict a continous variable (real number)
- Typical Examples:
  - Predicting Sales
  - Predicting Height
  - Predicting Number of Viewers of a Show

### Recommendation

- By studying people’s explicit preferences (ratings, etc) or implicit ones (tracking, etc) for various products or items to make recommendations
- Common use case for Spark and well suited for Big Data
- Examples:
  - Movie Recommendations
  - Product Recommendations

### Unsupervised Learning

- act of trying to find patterns or discover underlying structure in a given set of data.
- Examples:
  - Anomaly Detection
  - User Segmentation
  - Topic Modelling

### Graph Analytics

- study of structures in which we specify vertices(objects) and edges(relationships)
- E.g. Vertices maybe users and products and edges represent purchase.
- Examples:
  - Fraud Prediction : Read Capital One Bank’s fraud detection network case
  - Anomaly Detection
  - Classification : classify items based on graph connections
  - Recommendations : Pagerank

### The Advanced Analytics Process

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_2401.png)

Overall Process involves following steps (with variations sometimes)

- #### Data Collection

  - Gathering data is the first task, Spark is good at collecting data from variety of data sources

- #### Data Cleaning

  - We need to clean and inspect collected data. We perform *exploratory data analysis* (EDA).
  - We discard the data we don’t require and proceed with a clean data.

- #### Feature Engineering

  - We convert clean data into suitable format for machine learning algorithms.
  - Its a very important step
  - It includes tasks like *normalizing data*, *adding variables to represent interactions of other variables*, *manipulating categorical variables*, *convert to proper format to train*
  - In spark all variable usually have to be input of vectors of double.

- #### Training Models

  - train the model to predict the correct output, given some input.
  - During the training process, the parameters inside of the model will change according to how well the model performed on the input data.
  - The output of the training process is what we call a model

- #### Model Tuning and Evaluation

  - We usually split training data into Train-Test Split and use Test data to evaluate model performance
  - Depending on requirements we tune the model (hyperparameter tuning) to help us achieve require efficiency

- #### Leveraging Model and/or insights

  - After running the model through the training process and ending up with a well-performing model, you are now ready to use it! Taking your model to production can be a significant challenge in and of itself.

## Spark’s Advanced Analytics Toolkit

### What is MLlib ?

- MLlib is a package built on Spark, provides interfaces for gathering and cleaning data, feature engineering and feature selection, training and tuning large-scale supervised and unsupervised machine learning models, and using those models in production.
- Actually there are two packages : `org.apache.spark.ml` includes interface for use with DataFrames. Lower-level package, `org.apache.spark.mllib` includes interface for low-level RDDs APIs. (NOTE: now its in maintenance mode and only recieves bug fixes)

### When and Why should you use MLlib (vs scikit-learn, TensorFlow, or foo package)

- There are several tools for performing machine learning tasks on single machine. When we hit scalibility issues with data we can take advantage of Spark’s ability.
- Two use cases :
  - Spark for preprocessing and feature generation ot reduce time to prepare data.
  - Input data or model size becomes too inconvinient to use on one machine making distributed machine learning simple.
- There are few caveats tho :
  - Spark does not provide a built-in way to serve low-latency predictions  from a model, so you may want to export the model to another serving  system or a custom application to do that
  - Spark is not as efficient in training Deep Learning models.
    - Deep learning models benefit heavily from random access to elements of datasets to perform shuffling. RDDs are designed for streaming not random access
    - Spark Tasks are generally stateless and retryable but deep learning models are stateful.
    - Deep learning is not infinitely scalable, as it affects model convergence. (Spark 3.1 tries to solve to do resource aware scheduling)

## High-Level MLlib Concepts

- MLlib have several fundamental `structural` types : `transformer`, `estimator`, `evaluators` and `pipelines`.

![image](./ch24.assets/spdg_2402.png)

- Transformers: functions that convert raw data in some way. E.g. converting a categorical data into numerical values that can be used in MLlib.
- *Estimators* : one of two things, first a kind of transformer that is initialized with data. Normalization requires two passes over data. (generating initialisor and applying over data), sometimes algorithms that allow users to train a model from data are also called as estimators
- An *evaluator* allows us to see how a given model performs according to criteria we specify  like a receiver operating characteristic (ROC) curve. After we use an  evaluator to select the best model from the ones we tested, we can then  use that model to make predictions.
- each of the transformations, estimations, and evaluations one by one, but together in steps referred as *stages* in a *pipeline*.

#### Low-level data types

- Whenever we pass a set of features into ML model, we must do it as a vector that consists of type `Double`
- Vector can sparse or dense. To create sparse vector specify total size and the indices and values of the non-zero elements. To create a dense vector, we specify an array of all values.
- Sparse is best format when majority of values are zero as this is more compressed representation

````python
from pyspark.ml.linalg import Vectors
denseVec = Vectors.dense(1.0, 2.0, 3.0)
size = 3
idx = [1, 2] # locations of non-zero elements in vector
values = [2.0, 3.0]
sparseVec = Vectors.sparse(size, idx, values)
````

## MLlib in Action

````python
df = spark.read.json("/data/simple-ml")
df.orderBy("value2").show()
````

````text
+-----+----+------+------------------+
|color| lab|value1|            value2|
+-----+----+------+------------------+
|green|good|     1|14.386294994851129|
...
|  red| bad|    16|14.386294994851129|
|green|good|    12|14.386294994851129|
+-----+----+------+------------------+
````

- Above dataset consists of categorical label with good or bad, a categorical variable (color) and two numeric variables. Assume color represents medical health rating. Other two are some numerical measurement.
- Let’s train a classification model which can predict binary variable the label from other values

### Feature Engineering with Transformers

- To conform columns to our requirement for transformer we will use `RFormula`. Declarative language for specify machine learning transformation and is quite simple to understand
- Basic RFormula operators are:
  - `~` : Separate target and terms
  - `+` : Concat terms; “+ 0” means removing the intercept (this means that the *y*-intercept of the line that we will fit will be 0)
  - `-` : Remove a term; “- 1” means removing the intercept (this means that the *y*-intercept of the line that we will fit will be 0—yes, this does the same thing as “+ 0”
  - `:` : Interaction (multiplication for numeric values, or binarized categorical values)
  - `.` : All columns except the target/dependent variable

```python
from pyspark.ml.feature import RFormula
supervised = RFormula(formula="lab ~ . + color:value1 + color:value2")

fittedRF = supervised.fit(df)
preparedDF = fittedRF.transform(df)
preparedDF.show()


+-----+----+------+------------------+--------------------+-----+
|color| lab|value1|            value2|            features|label|
+-----+----+------+------------------+--------------------+-----+
|green|good|     1|14.386294994851129|(10,[1,2,3,5,8],[...|  1.0|
...
|  red| bad|     2|14.386294994851129|(10,[0,2,3,4,7],[...|  0.0|
+-----+----+------+------------------+--------------------+-----+
```

- Notice the column features. RFormula inspects our data during the fit call and ouput an object that will transfom our data according to `RFormulaModel`
- Let’s train the model

````python
# train-test split
train, test = preparedDF.randomSplit([0.7, 0.3])


# Linear Regression Estimator
from pyspark.ml.classification import LogisticRegression
lr = LogisticRegression(labelCol="label",featuresCol="features")
````

- Before training model let’s inspect parameters : also gives idea about options available in for each particular model

````python
print(lr.explainParams())
# fit the linear-regressor
fittedLR = lr.fit(train)

# let's perform prediction using following code snippet
fittedLR.transform(train).select("label", "prediction").show()
+-----+----------+
|label|prediction|
+-----+----------+
|  0.0|       0.0|
...
|  0.0|       0.0|
+-----+----------+
````

- Next is evaluation of model and calculate performance metrics like true positive rate, false negative rate, etc.

### Pipelining Our Workflow

Note that it is essential that instances of transformers or models are *not* reused across different pipelines. Always create a new instance of a model before creating another pipeline.

````python
train, test = df.randomSplit([0.7, 0.3])

# create base stages in our pipeline

rForm = RFormula()
lr = LogisticRegression().setLabelCol("label").setFeaturesCol("features")

from pyspark.ml import Pipeline
stages = [rForm, lr]
pipeline = Pipeline().setStages(stages)
````

### Training and Evaluation

````python
# train on multiple model variation based on hyperparameter tuning

from pyspark.ml.tuning import ParamGridBuilder
params = ParamGridBuilder()\
  .addGrid(rForm.formula, [
    "lab ~ . + color:value1",
    "lab ~ . + color:value1 + color:value2"])\
  .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0])\
  .addGrid(lr.regParam, [0.1, 2.0])\
  .build()

# we will be training 12 different versions of same model and Evaluate using area
# Under ROC

from pyspark.ml.evaluation import BinaryClassificationEvaluator
evaluator = BinaryClassificationEvaluator()\
  .setMetricName("areaUnderROC")\
  .setRawPredictionCol("prediction")\
  .setLabelCol("label")

````

- use TrainValidationSplit, which will simply perform an arbitrary random split of our data into two different groups, or CrossValidator, which performs K-fold cross-validation by splitting the dataset into k non-overlapping, randomly partitioned folds

````python
from pyspark.ml.tuning import TrainValidationSplit
tvs = TrainValidationSplit()\
  .setTrainRatio(0.75)\
  .setEstimatorParamMaps(params)\
  .setEstimator(pipeline)\
  .setEvaluator(evaluator)

tvsFitted = tvs.fit(train)

evaluator.evaluate(tvsFitted.transform(test)) // 0.9166666666666667
````

### Persisting and Applying Models

- saving to disk, for later use or use in some other model

````python
tvsFitted.write.overwrite().save("/tmp/modelLocation")
````

## Deployment Patterns

![image](./ch24.assets/spdg_2405.png)

- Train ML models offline and then supply it with offline data. Spark is suited for this kind of deployments
- Train models offline and then put results into a database (a key-value store). This is well suited for recommendation but poorly for something like classification or regression where we can’t look up a value for a given user but must calculate based on input
- Train ML algorithm offline, persist models to disk and then use that for serving. This is not a low-latency solution if you use Spark for the serving  part, as the overhead of starting up a Spark job can be high, even if  you’re not running on a cluster. Additionally this does not parallelize  well, so you’ll likely have to put a load balancer in front of multiple  model replicas and build out some REST API integration yourself.
- Manually convert distributed model to one that can run more quickly on single machine, This works well when there is not too much manipulation of raw data in Spark and can be hard to maintain over time.
- Train your ML models online and use it online, This is possible when used in conjunction with Structured Streaming, but can be complex for some models.



---

## File: pyspark/notes/ch25.md

# Preprocessing and Feature Engineering

## Formatting Models According to your Use Case

- general structure for each advanced analytics task in MLlib.
  - In most cases of classification and regression algorithms, Organise data into column of type `Double` to represent the label and a column of type `Vector` (dense/sparse) to represent features
  - In case of recommendation, get data into a columns of users, a column of items and a column of ratings
  - In case of unsupervised learning a column of type `Vector` is needed to represent features.
  - In the case of graph analytics, DataFrame of vertices and a DataFrame of edges.
- NOTE: Following are all synthetic datasets we are going to use

````python
sales = spark.read.format("csv")\
  .option("header", "true")\
  .option("inferSchema", "true")\
  .load("/data/retail-data/by-day/*.csv")\
  .coalesce(5)\
  .where("Description IS NOT NULL")	# NOTE we filtered nulls here.
fakeIntDF = spark.read.parquet("/data/simple-ml-integers")
simpleDF = spark.read.json("/data/simple-ml")
scaleDF = spark.read.parquet("/data/simple-ml-scaling")
````

- best way to achieve the required structure is to use transformer.

## Transformers

- Transformers are functions that convert raw data in some way. This might be to create a new interaction variable (from two other variables), to  normalize a column, or to simply turn it into a `Double` to be input into a model.
- The `Tokenizer` is an example of a transformer. It tokenizes a string, splitting on a  given character, and has nothing to learn from our data; it simply applies a function. Will discuss in upcoming chapter in detail.

````scala
import org.apache.spark.ml.feature.Tokenizer
val tkn = new Tokenizer().setInputCol("Description")
tkn.transform(sales.select("Description")).show(false)

+-----------------------------------+------------------------------------------+
|Description                        |tok_7de4dfc81ab7__output                  |
+-----------------------------------+------------------------------------------+
|RABBIT NIGHT LIGHT                 |[rabbit, night, light]                    |
|DOUGHNUT LIP GLOSS                 |[doughnut, lip, gloss]                    |
...
|AIRLINE BAG VINTAGE WORLD CHAMPION |[airline, bag, vintage, world, champion]  |
|AIRLINE BAG VINTAGE JET SET BROWN  |[airline, bag, vintage, jet, set, brown]  |
+-----------------------------------+------------------------------------------+
````

## Estimators for Preprocessing

- An *estimator* is necessary when a transformation you would like  to perform must be initialized with data or information about the input  column (often derived by doing a pass over the input column itself)
- Examples, scaling values in column to have mean zero and unit variance
- In effect, an estimator can be a transformer configured according to your particular input data. In simplest terms, you can either blindly apply a transformation (a “regular” transformer type) or perform a transformation based on your data (an estimator type).

````scala
import org.apache.spark.ml.feature.StandardScaler
val ss = new StandardScaler().setInputCol("features")
ss.fit(scaleDF).transform(scaleDF).show(false)

+---+--------------+------------------------------------------------------------+
|id |features      |stdScal_d66fbeac10ea__output                                |
+---+--------------+------------------------------------------------------------+
|0  |[1.0,0.1,-1.0]|[1.1952286093343936,0.02337622911060922,-0.5976143046671968]|
...
|1  |[3.0,10.1,3.0]|[3.5856858280031805,2.3609991401715313,1.7928429140015902]  |
+---+--------------+------------------------------------------------------------+
````

### Transformer Properties

- All transformers require you to specify, at a minimum, the `inputCol` and the `outputCol`
- all transformers have different parameters that you can tune

## High-Level Transformers

### RFormula

- `RFormula` is easiest transformer to use when we have `conventionally` formatted data. It is borrowed from R to make transformations easier.
- With this transformer, values can be either numerical or categorical and you do not need to extract values from strings or manipulate them in  any way. The `RFormula` will automatically handle categorical inputs (specified as strings) by performing something called *one-hot encoding*.
- 
- Basic RFormula operators are:
  - `~` : Separate target and terms
  - `+` : Concat terms; “+ 0” means removing the intercept (this means that the *y*-intercept of the line that we will fit will be 0)
  - `-` : Remove a term; “- 1” means removing the intercept (this means that the *y*-intercept of the line that we will fit will be 0—yes, this does the same thing as “+ 0”
  - `:` : Interaction (multiplication for numeric values, or binarized categorical values)
  - `.` : All columns except the target/dependent variable
- `RFormula` also uses default columns of `label` and `features` to label

````python
from pyspark.ml.feature import RFormula

supervised = RFormula(formula="lab ~ . + color:value1 + color:value2")
supervised.fit(simpleDF).transform(simpleDF).show()

+-----+----+------+------------------+--------------------+-----+
|color| lab|value1|            value2|            features|label|
+-----+----+------+------------------+--------------------+-----+
|green|good|     1|14.386294994851129|(10,[1,2,3,5,8],[...|  1.0|
| blue| bad|     8|14.386294994851129|(10,[2,3,6,9],[8....|  0.0|
...
|  red| bad|     1| 38.97187133755819|(10,[0,2,3,4,7],[...|  0.0|
|  red| bad|     2|14.386294994851129|(10,[0,2,3,4,7],[...|  0.0|
+-----+----+------+------------------+--------------------+-----+
````

### SQL Transformers

- Any `SELECT` statement from SQL is a valid transformation, only change is that instead of table we will use `THIS` keyword.

````python
from pyspark.ml.feature import SQLTransformer

basicTransformation = SQLTransformer()\
  .setStatement("""
    SELECT sum(Quantity), count(*), CustomerID
    FROM __THIS__
    GROUP BY CustomerID
  """)

basicTransformation.transform(sales).show()

-------------+--------+----------+
|sum(Quantity)|count(1)|CustomerID|
+-------------+--------+----------+
|          119|      62|   14452.0|
...
|          138|      18|   15776.0|
+-------------+--------+----------+
````

### Vector Assembler

- Very important tool, will be used in all pipelines
- Helps concatenate all features into one big vector that we can pass into an estimator
- Typically last step of a machine learning pipeline and takes as input a number of columns of `Boolean`, `Double`, or `Vector`

````python
from pyspark.ml.feature import VectorAssembler
va = VectorAssembler().setInputCols(["int1", "int2", "int3"])
va.transform(fakeIntDF).show()

+----+----+----+--------------------------------------------+
|int1|int2|int3|VectorAssembler_403ab93eacd5585ddd2d__output|
+----+----+----+--------------------------------------------+
|   1|   2|   3|                               [1.0,2.0,3.0]|
|   4|   5|   6|                               [4.0,5.0,6.0]|
|   7|   8|   9|                               [7.0,8.0,9.0]|
+----+----+----+--------------------------------------------+
````

## Working with Continuous Features

Continous features are just values on a number line. There are two common transformers for continuous features.

First convert continuous features into categorical features via bucketing or we can scale and normalise features according to several different requirements.

NOTE: these transformers will work on only `Double` type.

````python
contDF = spark.range(20).selectExpr("cast(id as double)")
````

### Bucketing

- We can bin a continous range by binning (bucketing) using `Bucketizer`
- We can specify bucket creation via an array or list of `Double` values. E.g. Bucketing weight ranges using buckets like `overweight`, `average` or `underweight`. 
- To specify a bucket, define its border like setting splits to `5.00`, `10.00`, `250.0` on our `contDF` will fail because it doesn’t cover all possible input ranges.
  - Min value in your splits must be less than minimum in your DF
  - Max value in your splits must be greater than maximum in your DF
  - Specify at a minimum three values in the splits array, which creates 2 buckets
- Another option to cover all ranges can be `scala.Double.NegativeInfinity` or `scala.Double.PositiveInfinity`, while in python `float('inf')` or `float('-inf')`
- To handle `null` or `NaN` values, you must specify `handleInvalid` parameter as certain value.

````python
from pyspark.ml.feature import Bucketizer
bucketBorders = [-1.0, 5.0, 10.0, 250.0, 600.0]
bucketer = Bucketizer().setSplits(bucketBorders).setInputCol("id")
bucketer.transform(contDF).show()

+----+---------------------------------------+
|  id|Bucketizer_4cb1be19f4179cc2545d__output|
+----+---------------------------------------+
| 0.0|                                    0.0|
...
|10.0|                                    2.0|
|11.0|                                    2.0|
...
+----+---------------------------------------+
````

- Another way to split based on percentiles in your data using `QuantileDiscretizer`
- For instance, the 90th quantile is the point in your data at which 90% of the data is below that value. You can control how finely the buckets  should be split by setting the relative error for the approximate  quantiles calculation using `setRelativeError`.

````python
from pyspark.ml.feature import QuantileDiscretizer
bucketer = QuantileDiscretizer().setNumBuckets(5).setInputCol("id")
fittedBucketer = bucketer.fit(contDF)
fittedBucketer.transform(contDF).show()

+----+----------------------------------------+
|  id|quantileDiscretizer_cd87d1a1fb8e__output|
+----+----------------------------------------+
| 0.0|                                     0.0|
...
| 6.0|                                     1.0|
| 7.0|                                     2.0|
...
|14.0|                                     3.0|
|15.0|                                     4.0|
...
+----+----------------------------------------+
````

More advanced bucketing techniques like `LHS(locality sensitive hashing)` are also available in MLlib.

### Scaling and Normalizing

- Usually preffered when our data has multiple columns but based on different scale. E.g. Weight(in kgs) and Height(in feet). If we don’t scale or normalise, algorithm will becomes less sensitive to variations in heights because height values are much lower than weight values.
- In MLlib we always apply normalisation to columns of type `Vector`. MLlib looks across all rows in a given column (of type `Vector`) and then treat every dimension in those vectors as its own particular column. Applying scaling or normalization function on each dimension separately.

### Standard Scaler

- Standardizes a set of features to have zero mean and a standard deviation of `1`.
- flag `withStd` will scale the data to unit standard deviation, `withMean` (false default) will center data prior to scaling it.
- NOTE: Centering can be very expensive on sparse vectors because it generally  turns them into dense vectors, so be careful before centering your data.

````python
from pyspark.ml.feature import StandardScaler
sScaler = StandardScaler().setInputCol("features")
sScaler.fit(scaleDF).transform(scaleDF).show()

+---+--------------+------------------------------------------------------------+
|id |features      |StandardScaler_41aaa6044e7c3467adc3__output                 |
+---+--------------+------------------------------------------------------------+
|0  |[1.0,0.1,-1.0]|[1.1952286093343936,0.02337622911060922,-0.5976143046671968]|
...
|1  |[3.0,10.1,3.0]|[3.5856858280031805,2.3609991401715313,1.7928429140015902]  |
+---+--------------+------------------------------------------------------------+
````

#### MinMaxScaler

- scale values in a vector (component wise) to a proportional values on a scale from a given min value to max value.
- If you specify the minimum value to be 0 and the maximum value to be 1, then all the values will fall in between 0 and 1

````python
from pyspark.ml.feature import MinMaxScaler
minMax = MinMaxScaler().setMin(5).setMax(10).setInputCol("features")
fittedminMax = minMax.fit(scaleDF)
fittedminMax.transform(scaleDF).show()

+---+--------------+-----------------------------------------+
| id|      features|MinMaxScaler_460cbafafbe6b9ab7c62__output|
+---+--------------+-----------------------------------------+
|  0|[1.0,0.1,-1.0]|                            [5.0,5.0,5.0]|
...
|  1|[3.0,10.1,3.0]|                         [10.0,10.0,10.0]|
+---+--------------+-----------------------------------------+
````

#### MaxAbsScaler

- scales data by dividing each value by maximum absolute value in this feature.
- All values end up between -1 and 1. NOTE: this transformer doesn’t shift or center data at all.

````python
from pyspark.ml.feature import MaxAbsScaler
maScaler = MaxAbsScaler().setInputCol("features")
fittedmaScaler = maScaler.fit(scaleDF)
fittedmaScaler.transform(scaleDF).show()

+---+--------------+----------------------------------------------------------+
|id |features      |MaxAbsScaler_402587e1d9b6f268b927__output                 |
+---+--------------+----------------------------------------------------------+
|0  |[1.0,0.1,-1.0]|[0.3333333333333333,0.009900990099009901,-0.3333333333333]|
...
|1  |[3.0,10.1,3.0]|[1.0,1.0,1.0]                                             |
+---+--------------+----------------------------------------------------------+
````

#### ElementwiseProduct

- scale each value in a vector by an arbitrary value.
- Naturally the dimensions of the scaling vector must match the dimensions of the vector inside the relevant column

````python
from pyspark.ml.feature import ElementwiseProduct
from pyspark.ml.linalg import Vectors
scaleUpVec = Vectors.dense(10.0, 15.0, 20.0)
scalingUp = ElementwiseProduct()\
  .setScalingVec(scaleUpVec)\
  .setInputCol("features")
scalingUp.transform(scaleDF).show()

+---+--------------+-----------------------------------------------+
| id|      features|ElementwiseProduct_42b29ea5a55903e9fea6__output|
+---+--------------+-----------------------------------------------+
|  0|[1.0,0.1,-1.0]|                               [10.0,1.5,-20.0]|
...
|  1|[3.0,10.1,3.0]|                              [30.0,151.5,60.0]|
+---+--------------+-----------------------------------------------+
````

#### Normalizer

- The normalizer allows us to scale multidimensional vectors using one of several power norms, set through the parameter “p”
- For example, we can use the Manhattan norm (or Manhattan distance) with p = 1, Euclidean norm with p = 2, and so on

````python
from pyspark.ml.feature import Normalizer
manhattanDistance = Normalizer().setP(1).setInputCol("features")
manhattanDistance.transform(scaleDF).show()

+---+--------------+-------------------------------+
| id|      features|normalizer_1bf2cd17ed33__output|
+---+--------------+-------------------------------+
|  0|[1.0,0.1,-1.0]|           [0.47619047619047...|
|  1| [2.0,1.1,1.0]|           [0.48780487804878...|
|  0|[1.0,0.1,-1.0]|           [0.47619047619047...|
|  1| [2.0,1.1,1.0]|           [0.48780487804878...|
|  1|[3.0,10.1,3.0]|           [0.18633540372670...|
+---+--------------+-------------------------------+
````

## Working with Categorical Features

- most common categorical task is indexing
- Indexing converts a categorical variable in a column to a numerical one
- In general, you should re-index every categorical variable when pre-processing just for the sake of consistency

### StringIndexer

- maps strings to different numerical IDs, it also creates metadata attached to DataFrame that specify what inputs correspond to what outputs.

````python
# in Python
from pyspark.ml.feature import StringIndexer
lblIndxr = StringIndexer().setInputCol("lab").setOutputCol("labelInd")
idxRes = lblIndxr.fit(simpleDF).transform(simpleDF)
idxRes.show()

+-----+----+------+------------------+--------+
|color| lab|value1|            value2|labelInd|
+-----+----+------+------------------+--------+
|green|good|     1|14.386294994851129|     1.0|
...
|  red| bad|     2|14.386294994851129|     0.0|
+-----+----+------+------------------+--------+
````

- we can apply StringIndexer to columns that are not strings, in that case, they will be converted to strings before being indexed

- String Indexer is an estimator that must be fit on the input data meaning it must see all inputs to select a mapping of inputs to IDs.
- If `StringIndexer` is trained on `a`, `b`, `c` but you feed `d` as input, it will throw error, a way to handle this is set `setHandleInvalid` as `skip`.

````python
valIndexer.setHandleInvalid("skip")
valIndexer.fit(simpleDF).setHandleInvalid("skip")
````

### Converting Indexed Values Back to Text

- Use `IndexToString` to convert indexed values back to Text.

````python
from pyspark.ml.feature import IndexToString
labelReverse = IndexToString().setInputCol("labelInd")
labelReverse.transform(idxRes).show()

+-----+----+------+------------------+--------+--------------------------------+
|color| lab|value1|            value2|labelInd|IndexToString_415...2a0d__output|
+-----+----+------+------------------+--------+--------------------------------+
|green|good|     1|14.386294994851129|     1.0|                            good|
...
|  red| bad|     2|14.386294994851129|     0.0|                             bad|
+-----+----+------+------------------+--------+--------------------------------+
````

### Idexing in Vectors

- `VectorIndexer` is a helpful tool for working with categorical variables that are already found inside of vectors in your dataset.
- It will automaticallyy find categorical features inside of input vectors and convert them to categorical features with zero-based category indices.
- By setting `maxCategories` to 2 in our `VectorIndexer`, we are instructing Spark to take any column in our vector with two or  less distinct values and convert it to a categorical variable. 

````python
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.linalg import Vectors
idxIn = spark.createDataFrame([
  (Vectors.dense(1, 2, 3),1),
  (Vectors.dense(2, 5, 6),2),
  (Vectors.dense(1, 8, 9),3)
]).toDF("features", "label")
indxr = VectorIndexer()\
  .setInputCol("features")\
  .setOutputCol("idxed")\
  .setMaxCategories(2)
indxr.fit(idxIn).transform(idxIn).show()

+-------------+-----+-------------+
|     features|label|        idxed|
+-------------+-----+-------------+
|[1.0,2.0,3.0]|    1|[0.0,2.0,3.0]|
|[2.0,5.0,6.0]|    2|[1.0,5.0,6.0]|
|[1.0,8.0,9.0]|    3|[0.0,8.0,9.0]|
+-------------+-----+-------------+
````

### One-Hot Encoding

- common transformation after indexing categorical variables, as after encoding colors lets say we have `blue` for `1` and `green` for `2`, then it appears to have greater value than other color, but for us these might be independent.
- To avoid this, we use `OneHotEncoder`, which will convert each distinct value to a Boolean flag (1 or 0) as a component in a vector.

````python
from pyspark.ml.feature import OneHotEncoder, StringIndexer
lblIndxr = StringIndexer().setInputCol("color").setOutputCol("colorInd")
colorLab = lblIndxr.fit(simpleDF).transform(simpleDF.select("color"))
ohe = OneHotEncoder().setInputCol("colorInd")
ohe.transform(colorLab).show()

+-----+--------+------------------------------------------+
|color|colorInd|OneHotEncoder_46b5ad1ef147bb355612__output|
+-----+--------+------------------------------------------+
|green|     1.0|                             (2,[1],[1.0])|
| blue|     2.0|                                 (2,[],[])|
...
|  red|     0.0|                             (2,[0],[1.0])|
|  red|     0.0|                             (2,[0],[1.0])|
+-----+--------+------------------------------------------+
````

## Text Data Transformer

- Text is always a tricky input because it often requires lots of manipulation to map to a format easier to train ML models.
- There are two types of text : free-from text and string categorical variables

### Tokenizing Text

- Tokenization is process of converting free-form text into lits of `tokens` or individual words. Easiest way to do this is using `Tokenizer` class.

````python
from pyspark.ml.feature import Tokenizer
tkn = Tokenizer().setInputCol("Description").setOutputCol("DescOut")
tokenized = tkn.transform(sales.select("Description"))
tokenized.show(20, False)

+-----------------------------------+------------------------------------------+
|Description                        DescOut                                    |
+-----------------------------------+------------------------------------------+
|RABBIT NIGHT LIGHT                 |[rabbit, night, light]                    |
|DOUGHNUT LIP GLOSS                 |[doughnut, lip, gloss]                    |
...
|AIRLINE BAG VINTAGE WORLD CHAMPION |[airline, bag, vintage, world, champion]  |
|AIRLINE BAG VINTAGE JET SET BROWN  |[airline, bag, vintage, jet, set, brown]  |
+-----------------------------------+------------------------------------------+
````

- regular expression based Tokenizer

````python
from pyspark.ml.feature import RegexTokenizer
rt = RegexTokenizer()\
  .setInputCol("Description")\
  .setOutputCol("DescOut")\
  .setPattern(" ")\
  .setToLowercase(True)
rt.transform(sales.select("Description")).show(20, False)

+-----------------------------------+------------------------------------------+
|Description                        DescOut                                    |
+-----------------------------------+------------------------------------------+
|RABBIT NIGHT LIGHT                 |[rabbit, night, light]                    |
|DOUGHNUT LIP GLOSS                 |[doughnut, lip, gloss]                    |
...
|AIRLINE BAG VINTAGE WORLD CHAMPION |[airline, bag, vintage, world, champion]  |
|AIRLINE BAG VINTAGE JET SET BROWN  |[airline, bag, vintage, jet, set, brown]  |
+-----------------------------------+------------------------------------------+
````

- Another way using is to matching output values with the provided pattern instead of using for split(gaps)

````python
from pyspark.ml.feature import RegexTokenizer
rt = RegexTokenizer()\
  .setInputCol("Description")\
  .setOutputCol("DescOut")\
  .setPattern(" ")\
  .setGaps(False)\
  .setToLowercase(True)
rt.transform(sales.select("Description")).show(20, False)
````

### Removing common Words

- Common operation after tokenization is to filter stop words, common words which do not have any relevance in many kinds of analysis and should be removed. Like `the`, `and`, and `but`. Spark already has this list.

````python
# in Python
from pyspark.ml.feature import StopWordsRemover
# supported languages for stopwords are “danish,” “dutch,” “english,” “finnish,” “french,” 
# “german,” “hungarian,” “italian,” “norwegian,” “portuguese,” “russian,” “spanish,” 
# “swedish,” and “turkish”
englishStopWords = StopWordsRemover.loadDefaultStopWords("english")
stops = StopWordsRemover()\
  .setStopWords(englishStopWords)\
  .setInputCol("DescOut")
stops.transform(tokenized).show()

+--------------------+--------------------+------------------------------------+
|         Description|             DescOut|StopWordsRemover_4ab18...6ed__output|
+--------------------+--------------------+------------------------------------+
...
|SET OF 4 KNICK KN...|[set, of, 4, knic...|                [set, 4, knick, k...|
...
+--------------------+--------------------+------------------------------------+
````

### Creating Word Combinations

- After tokenization and filtering stop words, It is usually of interest to look few words together. Word Combinations are techincally called as *n-grams*
- An *n*-gram of length 1 is called a *unigrams*; those of length 2 are called *bigrams*, and those of length 3 are called *trigrams* and so-on
- Order of *n-gram* matters. The goal when creating *n*-grams is to better capture sentence  structure and more information than can be gleaned by simply looking at  all words individually.

Example:

- The bigrams of “Big Data Processing Made Simple” are:
  - “Big Data”
  - “Data Processing”
  - “Processing Made”
  - “Made Simple”
- While the trigrams are:
  - “Big Data Processing”
  - “Data Processing Made”
  - “Procesing Made Simple”

````python
from pyspark.ml.feature import NGram
unigram = NGram().setInputCol("DescOut").setN(1)
bigram = NGram().setInputCol("DescOut").setN(2)
unigram.transform(tokenized.select("DescOut")).show(False)
bigram.transform(tokenized.select("DescOut")).show(False)

Bigrams Output
+------------------------------------------+------------------------------------
DescOut                                    |ngram_6e68fb3a642a__output       ...
+------------------------------------------+------------------------------------
|[rabbit, night, light]                    |[rabbit night, night light]      ...
|[doughnut, lip, gloss]                    |[doughnut lip, lip gloss]        ...
...
|[airline, bag, vintage, world, champion]  |[airline bag, bag vintage, vintag...
|[airline, bag, vintage, jet, set, brown]  |[airline bag, bag vintage, vintag...
+------------------------------------------+------------------------------------
````

### Converting Words into Numerical Representation

- next task is to count instances of words and word combinaiton for use in our models, we include binary counts of a word in a given document.
- Essentially, we’re measuring whether or not each row contains a given  word. This is a simple way to normalize for document sizes and occurrence counts and get numerical features that allow us to classify  documents based on content.
- We can count words using a `CountVectorizer` or reweigh them according to prevalence of a given word in all the documents using TF-IDF transformation.
- A `CountrVectorizer` operates on our tokenized data and does two operation
  - During the `fit` process, it finds the set of words in all the documents and then counts the occurrences of those words in those documents.
  - It then counts the occurrences of a given word in each row of the DataFrame column during the transformation process and outputs a vector with the terms that occur in that row.
- Conceptually this tranformer treats every row as a *document* and every word as a *term* and the total collection of all terms as the *vocabulary*. These are all tunable parameters, meaning we can set the minimum term frequency (`minTF`) for the term to be included in the vocabulary (effectively removing rare words from the vocabulary); minimum number of documents a term must appear in (`minDF`) before being included in the vocabulary (another way to remove rare  words from the vocabulary); and finally, the total maximum vocabulary size (`vocabSize`). 
- By default the `CountVectorizer` will output the counts of a term in a document. To just return whether or not a word exists in a document, we can use `setBinary(true)`.

````python
from pyspark.ml.feature import CountVectorizer
cv = CountVectorizer()\
  .setInputCol("DescOut")\
  .setOutputCol("countVec")\
  .setVocabSize(500)\
  .setMinTF(1)\
  .setMinDF(2)
fittedCV = cv.fit(tokenized)
fittedCV.transform(tokenized).show(False)

+---------------------------------+--------------------------------------------+
DescOut                           |countVec                                    |
+---------------------------------+--------------------------------------------+
|[rabbit, night, light]           |(500,[150,185,212],[1.0,1.0,1.0])           |
|[doughnut, lip, gloss]           |(500,[462,463,492],[1.0,1.0,1.0])           |
...
|[airline, bag, vintage, world,...|(500,[2,6,328],[1.0,1.0,1.0])               |
|[airline, bag, vintage, jet, s...|(500,[0,2,6,328,405],[1.0,1.0,1.0,1.0,1.0]) |
+---------------------------------+--------------------------------------------+
````

#### Term frequency-inverse document frequency

- Another way to approach the problem of converting text into a numerical  representation is to use term frequency–inverse document frequency
- *TF–IDF* measures how often a word occurs in each document, weighted according to how many documents that word occurs in. The result is that words that occur in a few documents are given more weight than words that occur in many documents. E.g. words like a, an, the are given less weight as compared to word like `streaming`

````python
tfIdfIn = tokenized\
  .where("array_contains(DescOut, 'red')")\
  .select("DescOut")\
  .limit(10)
tfIdfIn.show(10, False)

+---------------------------------------+
DescOut                                 |
+---------------------------------------+
|[gingham, heart, , doorstop, red]      |
...
|[red, retrospot, oven, glove]          |
|[red, retrospot, plate]                |
+---------------------------------------+

# applying TF-IDF on above Df which has red on every line
from pyspark.ml.feature import HashingTF, IDF
tf = HashingTF()\
  .setInputCol("DescOut")\
  .setOutputCol("TFOut")\
  .setNumFeatures(10000)
idf = IDF()\
  .setInputCol("TFOut")\
  .setOutputCol("IDFOut")\
  .setMinDocFreq(2)

idf.fit(tf.transform(tfIdfIn)).transform(tf.transform(tfIdfIn)).show(10, False)

# ~ Output ~ Notice red is given very low weight.
(10000,[2591,4291,4456],[1.0116009116784799,0.0,0.0])
````

### Word2Vec

- Word2Vec is a deep learning–based tool for computing a vector representation of a set of words. The goal is to have similar words close to one another in this vector space, so we can then make generalizations about the words  themselves. 
- This model is easy to train and use, and has been shown to be useful in a number of natural language processing applications, including entity recognition, disambiguation, parsing, tagging, and machine translation.
- Word2Vec is notable for capturing relationships between words based on  their semantics. For example, if v~king, v~queen, v~man, and v~women  represent the vectors for those four words, then we will often get a  representation where v~king − v~man + v~woman ~= v~queen. To do this,  Word2Vec uses a technique called “skip-grams” to convert a sentence of  words into a vector representation (optionally of a specific size). It  does this by building a vocabulary, and then for every sentence, it  removes a token and trains the model to predict the missing token in the "*n*-gram” representation. Word2Vec works best with continuous, free-form text in the form of tokens.

````python
from pyspark.ml.feature import Word2Vec
# Input data: Each row is a bag of words from a sentence or document.
documentDF = spark.createDataFrame([
    ("Hi I heard about Spark".split(" "), ),
    ("I wish Java could use case classes".split(" "), ),
    ("Logistic regression models are neat".split(" "), )
], ["text"])
# Learn a mapping from words to Vectors.
word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol="text",
  outputCol="result")
model = word2Vec.fit(documentDF)
result = model.transform(documentDF)
for row in result.collect():
    text, vector = row
    print("Text: [%s] => \nVector: %s\n" % (", ".join(text), str(vector)))
    
Text: [Hi, I, heard, about, Spark] =>
Vector: [-0.008142343163490296,0.02051363289356232,0.03255096450448036]

Text: [I, wish, Java, could, use, case, classes] =>
Vector: [0.043090314205203734,0.035048123182994974,0.023512658663094044]

Text: [Logistic, regression, models, are, neat] =>
Vector: [0.038572299480438235,-0.03250147425569594,-0.01552378609776497]
````

## Feature Manipulation

- following algorithms and tools are automated means to either expand feature vector or reduce dimensionality of features

### PCA

- Principal Components Analysis (PCA) is a mathematical technique for finding the  most important aspects of our data (the principal components). It changes the feature representation of our data by creating a new set of features (“aspects”). Each new feature is a combination of the original  features.
- https://en.wikipedia.org/wiki/Principal_component_analysis
- Using PCA, we can find the most important combinations of features and  only include those in our machine learning model. PCA takes a parameter  𝘬, specifying the number of output features to create. Generally, this  should be much smaller than your input vectors’ dimension.

````python
from pyspark.ml.feature import PCA
pca = PCA().setInputCol("features").setK(2)
pca.fit(scaleDF).transform(scaleDF).show(20, False)

+---+--------------+------------------------------------------+
|id |features      |pca_7c5c4aa7674e__output                  |
+---+--------------+------------------------------------------+
|0  |[1.0,0.1,-1.0]|[0.0713719499248418,-0.4526654888147822]  |
...
|1  |[3.0,10.1,3.0]|[-10.872398139848944,0.030962697060150646]|
+---+--------------+------------------------------------------+
````

### Interaction

- In some cases, you might have domain knowledge about specific variables in your dataset.
- For example, you might know that a certain interaction between the two  variables is an important variable to include in a downstream estimator. 
- The feature transformer `Interaction` allows you to create an interaction between two variables manually. It just multiplies the  two features together—something that a typical linear model would not do for every possible pair of features in your data.

### Polynomial Expansion

- Polynomial expansion is used to generate interaction variables of all the input  columns. With polynomial expansion, we specify to what degree we would  like to see various interactions. For example, for a degree-2 polynomial, Spark takes every value in our feature vector, multiplies it by every other value in the feature vector, and then stores the results as features.
- For instance, if we have two input features, we’ll get four output  features if we use a second degree polynomial (2x2). If we have three  input features, we’ll get nine output features (3x3).

````python
from pyspark.ml.feature import PolynomialExpansion
pe = PolynomialExpansion().setInputCol("features").setDegree(2)
pe.transform(scaleDF).show()

+---+--------------+-----------------------------------------------------------+
|id |features      |poly_9b2e603812cb__output                                  |
+---+--------------+-----------------------------------------------------------+
|0  |[1.0,0.1,-1.0]|[1.0,1.0,0.1,0.1,0.010000000000000002,-1.0,-1.0,-0.1,1.0]  |
...
|1  |[3.0,10.1,3.0]|[3.0,9.0,10.1,30.299999999999997,102.00999999999999,3.0... |
+---+--------------+-----------------------------------------------------------+
````

## Feature Selection

- Often, you will have a large range of possible features and want to select a smaller subset to use for training.
- This process is called feature selection. There are a number of ways to evaluate feature importance  once you’ve trained a model but another option is to do some rough  filtering beforehand. Spark has some simple options for doing that, such as `ChiSqSelector`

### ChiSqSelector

- `ChiSqSelector` leverages a statistical test to identify  features that are not independent from the label we are trying to  predict, and drop the uncorrelated features. It’s often used with  categorical data in order to reduce the number of features you will  input into your model, as well as to reduce the dimensionality of text  data (in the form of frequencies or counts)
- Since this method is based on the Chi-Square test, there are several  different ways we can pick the “best” features. The methods are `numTopFeatures`, which is ordered by *p*-value; `percentile`, which takes a proportion of the input features (instead of just the top N features); and `fpr`, which sets a cut off *p*-value.

````python
from pyspark.ml.feature import ChiSqSelector, Tokenizer
tkn = Tokenizer().setInputCol("Description").setOutputCol("DescOut")
tokenized = tkn\
  .transform(sales.select("Description", "CustomerId"))\
  .where("CustomerId IS NOT NULL")
prechi = fittedCV.transform(tokenized)\
  .where("CustomerId IS NOT NULL")
chisq = ChiSqSelector()\
  .setFeaturesCol("countVec")\
  .setLabelCol("CustomerId")\
  .setNumTopFeatures(2)
chisq.fit(prechi).transform(prechi)\
  .drop("customerId", "Description", "DescOut").show()
````

## Advanced Topics

### Persisting Transformer

- once we have used an estimator to configure a transformer, it can be helpful to write it to disk and simply load when needed.

````python
# save
fittedPCA = pca.fit(scaleDF)
fittedPCA.write().overwrite().save("/tmp/fittedPCA")

# load
from pyspark.ml.feature import PCAModel
loadedPCA = PCAModel.load("/tmp/fittedPCA")
loadedPCA.transform(scaleDF).show()
````

## Writing a Custom Transformer

Writing a custom transformer can be valuable when you want to encode some of  your own business logic in a form that you can fit into an ML Pipeline,  pass on to hyperparameter search, and so on. In general you should try  to use the built-in modules (e.g., `SQLTransformer`) as much as possible because they are optimized to run efficiently

- A simple tokenizer example

````scala
import org.apache.spark.ml.UnaryTransformer
import org.apache.spark.ml.util.{DefaultParamsReadable, DefaultParamsWritable,
  Identifiable}
import org.apache.spark.sql.types.{ArrayType, StringType, DataType}
import org.apache.spark.ml.param.{IntParam, ParamValidators}

class MyTokenizer(override val uid: String)
  extends UnaryTransformer[String, Seq[String],
    MyTokenizer] with DefaultParamsWritable {

  def this() = this(Identifiable.randomUID("myTokenizer"))

  val maxWords: IntParam = new IntParam(this, "maxWords",
    "The max number of words to return.",
  ParamValidators.gtEq(0))

  def setMaxWords(value: Int): this.type = set(maxWords, value)

  def getMaxWords: Integer = $(maxWords)

  override protected def createTransformFunc: String => Seq[String] = (
    inputString: String) => {
      inputString.split("\\s").take($(maxWords))
  }

  override protected def validateInputType(inputType: DataType): Unit = {
    require(
      inputType == StringType, s"Bad input type: $inputType. Requires String.")
  }

  override protected def outputDataType: DataType = new ArrayType(StringType,
    true)
}

// this will allow you to read it back in by using this object.
object MyTokenizer extends DefaultParamsReadable[MyTokenizer]
````

````scala
val myT = new MyTokenizer().setInputCol("someCol").setMaxWords(2)
myT.transform(Seq("hello world. This text won't show.").toDF("someCol")).show()
````



---

## File: pyspark/notes/ch26.md

# Classification

Documentation : https://spark.apache.org/docs/latest/ml-classification-regression.html

## Use Cases

- predicting potential credit default risk while lending (Binary Classification)
- categorizing news posts or article based on their content
- using sensors based data on a smart watch to determine physical activity

## Types of Classification

#### Binary Classification

- only two labels to predict, example: detecting whether an email is spam or not

#### Multiclass Classification

- choose a label from multiple labels, example: facebook predicting people in a given photo, meterological prediction for weather

#### Multilabel Classification

- choose mutilple labels, exmaple: predict a book’s genre from the text of book, could belong to multiple genre

## Classification Models in MLlib

- Spark has several models available for performing binary and multiclass classification out of the box.
  - [Logistic regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#logistic-regression)
    - [Binomial logistic regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#binomial-logistic-regression)
    - [Multinomial logistic regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#multinomial-logistic-regression)
  - [Decision tree classifier](https://spark.apache.org/docs/latest/ml-classification-regression.html#decision-tree-classifier)
  - [Random forest classifier](https://spark.apache.org/docs/latest/ml-classification-regression.html#random-forest-classifier)
  - [Gradient-boosted tree classifier](https://spark.apache.org/docs/latest/ml-classification-regression.html#gradient-boosted-tree-classifier)
  - [Multilayer perceptron classifier](https://spark.apache.org/docs/latest/ml-classification-regression.html#multilayer-perceptron-classifier)
  - [Linear Support Vector Machine](https://spark.apache.org/docs/latest/ml-classification-regression.html#linear-support-vector-machine)
  - [One-vs-Rest classifier (a.k.a. One-vs-All)](https://spark.apache.org/docs/latest/ml-classification-regression.html#one-vs-rest-classifier-aka-one-vs-all)
  - [Naive Bayes](https://spark.apache.org/docs/latest/ml-classification-regression.html#naive-bayes)
  - [Factorization machines classifier](https://spark.apache.org/docs/latest/ml-classification-regression.html#factorization-machines-classifier)
  
- Spark does not support making multilabel predictions natively. In order to train a multilabel model, you must train one model per label and combine them manually

### Model Scalability

- Model scalability is a very important metric while choosing a model, Spark performs good on large-scale machine learning models but there on a single-node workloads there are number of tools that will outperform spark.

| Model                  | Features count  | Training examples | Output classes                  |
| ---------------------- | --------------- | ----------------- | ------------------------------- |
| Logistic regression    | 1 to 10 million | No limit          | Features x Classes < 10 million |
| Decision trees         | 1,000s          | No limit          | Features x Classes < 10,000s    |
| Random forest          | 10,000s         | No limit          | Features x Classes < 100,000s   |
| Gradient-boosted trees | 1,000s          | No limit          | Features x Classes < 10,000s    |

Data for classification models

````python
bInput = spark.read.format("parquet").load("/data/binary-classification")\
  .selectExpr("features", "cast(label as double) as label")
````

## Logistic Regression

- very popular regression methods for classification. It is linear method that combines individual features with specific weights that combined to get a probability of belonging to a class.
- Weights represents the importance of a features

### Model Hyperparameters

- `family` : can be multinomial (two or more distinct labels) or binary (only two labels)
- `elasticNetParam` : A float value `(0, 1)` which specifies the mix of L1 and L2 regularization according to elastic net regularization. L1 regularization will create sparsity in model because features weights will become zero (that are little consequence to output). L2 regularization doesn’t create sparsity because corresponding weights for a particular features will only be driven towards zero, but will never reach zero.
- `fitIntercept` : Boolean value, determines whether to fit the intercept or the arbitrary number that is added to the linear combination of inputs and weights of the model. Typically you will want to fit the intercept if we haven’t normalized our training data.
- `regParam` : A value >= 0. that determines how much weight to give to regularization term in objective function. Choosing a value here is again going to be a function of noise and dimensionality in our dataset.
- `standardization` : Boolean Value deciding whether to standardize inputs before passing them into the models.

### Training Parameters

- `maxIter` : Total number of iterations over the data before stopping. Default is 100.
- `tol` : specifies a threshold by which changes in parameters show that we optimized our weights enough, and can stop iterating. It lets the algorithm stop before maxIter iteration. Default is : `1e-6`
- `weightCol` : name of weight column used to weigh certain rows more than other

### Prediciton Parameters

- `threshold` : A `Double` in the range 0 to 1. This parameter is probability threshold for when a given class should be predicted. You can tune this parameter to your requirements to balance between false positives and false negatives. For instance, if a mistake prediction is very costly, set this to very high value.
- `thresholds` : This parameter lets you specify an array of threshold values for each class when using multiclass classification.

### Example

- To get all params

````python
from pyspark.ml.classification import LogisticRegression
lr = LogisticRegression()
print lr.explainParams() # see all parameters
lrModel = lr.fit(bInput)
````

- once model is trained we can get information about model by taking a look at intercepts and coefficients. The coefficients correspond to the individual feature weights while the intercept is the value of the italics-intercept.

````python
print(lrModel.coefficients)
print(lrModel.intercept)
````

For a multinomial model (the current one is binary), `lrModel.coefficientMatrix` and `lrModel.interceptVector` can be used to get the coefficients and intercept. These will return `Matrix` and `Vector` types representing the values or each of the given classes.

### Model Summary

Logistic regression provides a model summary that gives you information about the final, trained model.

Using the summary, we can get all sorts of information about the model itself including the area under the ROC curve, the f measure by threshold, the precision, the recall, the recall by thresholds, and the ROC curve. Note that for the area under the curve, instance weighting is not taken into account, so if you wanted to see how you performed on the values you weighed more highly, you’d have to do that manually.

## Decision Trees

- more friendly and interpretable models for performing classification because similar to decision models that resembles human decision use.

![Decision Trees for Classification: A Machine Learning Algorithm | Xoriant](https://www.xoriant.com/sites/default/files/uploads/2017/08/Decision-Trees-modified-1.png)

- In short you create a big decision tree to predict the outcomes, this model supports multiclass classifications as well.
- Although this model is good start, it does come at a cost. It can overfit data *extremely quickly*. Unrestrained this decision tree will create a pathway from start based on every training example.
- This is bad because then the model won’t generalize to new data (you  will see poor test set prediction performance). However, there are a  number of ways to try and rein in the model by limiting its branching  structure (e.g., limiting its height) to get good predictive power.

### Model Hyperparameters

- `maxDepth`: specifies max depth in order to avoid overfitting dataset
- `maxBins`: In decision trees, continuous features are converted into categorical features and `maxBins` determines how many bins should be created from continous features. More bins gives a higher level of granularity. The value must be greater than or equal to 2 and greater than or equal to the number of categories in any categorical feature in your dataset. The default is 32
- `impurity` : To build a “tree” you need to configure when the model should branch. Impurity represents the metric to determine whether or not model should splits at a particular leaf node. This parameter can be set to either be “entropy” or “gini” (default), two commonly used impurity metrics
- `minInfoGain` : this param determines the minimum information gain that can be used for a split. A higher value can prevent overfitting. This is largely something that needs to be determines from testing out different variations of the decision tree model. Ddefault : 0
- `minInstancePerNode` : This parameter determines the minimum number of training instances that need to end in a particular node. Think of this as another manner of  controlling max depth. We can prevent overfitting by limiting depth or we can prevent it by specifying that at minimum a certain number of training values need to end up in a particular leaf node. If it’s not met we would “prune” the tree until that requirement is met. A higher value can prevent overfitting. The default is 1, but this can be any  value greater than 1.

### Training Parameters

- `checkpointInterval` : Checkpointing is a way to save the model’s work over the course of training so that if nodes in cluster crash for some reason, we don’t lose our work. This parameter needs to be set together with a `checkpointDir` (a directory to checkpoint to) and with `useNodeIdCache=true`

### Prediction Parameters

- There is only one prediction parameters for decision trees : `thresholds`

````python
from pyspark.ml.classification import DecisionTreeClassifier
dt = DecisionTreeClassifier()
print dt.explainParams()
dtModel = dt.fit(bInput)
````

## Random Forest and Gradient-Boosted Trees

- This method is an extension of decision tree which trains multiple trees on varying subsets of data. Each of those trees become expert in a particular domain relevant to subset picked and we combine them to get a concensus. These methods help preventing overfitting.
- Random forests and gradient-boosted trees are two distinct methods for combining decision trees. In random forests we simply train lots of trees and then average their response to make a prediction. With gradient-boosted trees, each tree makes a weighted prediction. They have largely same parameters stated below.
- One current limitation is that gradient-boosted trees currently only support binary labels. There are several popular tools for learning tree-based models. For example, the [XGBoost](https://xgboost.readthedocs.io/en/latest/) library provides an integration package for Spark that can be used to run it on Spark.

### Model Hyperparameters

Both support all same model hyperparameters as decision trees.

#### Random forest only

- `numTrees` : total number of trees to train
- `featureSubsetStrategy` : determines how many features should be considered for splits. This can be a variety of different values including “auto”, “all”, “sqrt”, “log2”, or a number “n.” When your input is “n” the model will  use n * number of features during training.

#### Gradient-boosted trees (GBT) only

- `lossType`: loss function for gradient-boosted trees to minimize during training. Currently, only logistic loss is supported.
- `maxIter` : Total number of iterations over the data before stopping. Changing this  probably won’t change your results a ton, so it shouldn’t be the first parameter you look to adjust. The default is 100.
- `stepSize` : This is the learning rate for the algorithm. A larger step size means  that larger jumps are made between training iterations. This can help in the optimization process and is something that should be tested in  training. The default is 0.1 and this can be any value from 0 to 1.

#### Training Parameters

- `checkpointInterval`

### Prediction Parameters

- Have same prediction parameters as decision trees.

Examples

````python
# RF Tree
from pyspark.ml.classification import RandomForestClassifier
rfClassifier = RandomForestClassifier()
print rfClassifier.explainParams()
trainedModel = rfClassifier.fit(bInput)

# GBT Tree
from pyspark.ml.classification import GBTClassifier
gbtClassifier = GBTClassifier()
print gbtClassifier.explainParams()
trainedModel = gbtClassifier.fit(bInput)
````

## Naive Bayes

- Naive Bayes classifiers are a collection of classifiers based on Bayes’ theorem. The core assumption behind the models is that all features in your data are independent of one another. Naturally, strict independence is a bit naive, but even if this is violated, useful models can still be produced.
- Naive Bayes classifiers are commonly used in text or document classification, although it can be used as a more general-purpose classifier as well.
- There are two different model types: 
  - either a *multivariate Bernoulli model*, where indicator variables represent the existence of a term in a document; 
  - or the *multinomial model*, where the total counts of terms are used.
- One important note when it comes to Naive Bayes is that all input features must be non-negative.

### Model Hyperparameters

- `modelType`: Either “bernoulli” or “multinomial”
- `weightCol` : Allows weighing different data points differently.

### Training Parameters

- `smoothing` : This determines the amount of regularization that should take place using [additive smoothing](https://en.wikipedia.org/wiki/Additive_smoothing). This helps smooth out categorical data and avoid overfitting on the  training data by changing the expected probability for certain classes.  The default value is 1.

### Prediction Parameters

Naive Bayes shares the same prediction parameter, `thresholds`

````python
from pyspark.ml.classification import NaiveBayes
nb = NaiveBayes()
print nb.explainParams()
trainedModel = nb.fit(bInput.where("label != 0"))
````

## Evaluators for Classification and Automating Model Tuning

- Evaluator on its doesn’t help too much, unless we use it in a pipeline, we can automate a grid search of our various parameters of models and transformers - trying all combinations of parameters to see which ones perform best.
- For classification, there are two evaluators, and they expect two  columns: a predicted label from the model and a true label. 
- For binary  classification we use the `BinaryClassificationEvaluator`.  This supports optimizing for two different metrics “areaUnderROC” and  areaUnderPR.” 
- For multiclass classification, we need to use the `MulticlassClassificationEvaluator`, which supports optimizing for “f1”, “weightedPrecision”, “weightedRecall”, and “accuracy”.

## Detailed Evaluation Metrics

MLlib  also contains tools that let you evaluate multiple classification  metrics at once. Unfortunately, these metrics classes have not been  ported over to Spark’s DataFrame-based ML package from the underlying  RDD framework. Check documentation for more information

There are 3 different Classifications metrics we can use

- Binary classification metrics
- Multiclass classification metrics
- Multilabel classification metrics

````python
from pyspark.mllib.evaluation import BinaryClassificationMetrics
out = model.transform(bInput)\
  .select("prediction", "label")\
  .rdd.map(lambda x: (float(x[0]), float(x[1])))
metrics = BinaryClassificationMetrics(out)

print metrics.areaUnderPR
print metrics.areaUnderROC
print "Receiver Operating Characteristic"
metrics.roc.toDF().show()
````

## One-vs-Rest Classifier

- There are some MLlib models that don’t support multiclass classification. In these cases, users can leverage a one-vs-rest classifier in order to perform multiclass classification given only a binary classifier.
- The intuition behind this is that for every class you hope to predict,  the one-vs-rest classifier will turn the problem into a binary classification problem by isolating one class as the target class and  grouping all of the other classes into one.
- One-vs-rest is implemented as an estimator. For the base classifier it  takes instances of the classifier and creates a binary classification  problem for each of the 𝘬 classes. The classifier for class *i* is trained to predict whether the label is *i* or not, distinguishing class *i* from all other classes.
- Predictions are done by evaluating each binary classifier and the index of the most confident classifier is output as the label.
- See spark documentation for more.

## Multilayer Perceptron

The multilayer perceptron is a classifier based on neural networks with a configurable number of layers (and layer sizes). We will discuss it in 3 chapters ahead


---

## File: pyspark/notes/ch27.md

# Regression

- regression is a logical extension of classification. Regression is act of predictin a real number(cont. variable) from a set of features (represented as numbers).
- regression can be much harder as there are infinite possible output values, we try to optimize some error metric between true value and predicted value.

## Use Cases

- predicting moview turnout from initial responses like trailer watches, social shares etc.
- predicting company revenue from bunch of business parameters
- predicting crop yield based on weather

## Regression Models in MLlib

- [Linear regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#linear-regression)
- Generalized linear regression
  - [Available families](https://spark.apache.org/docs/latest/ml-classification-regression.html#available-families)
- [Decision tree regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#decision-tree-regression)
- [Random forest regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#random-forest-regression)
- [Gradient-boosted tree regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#gradient-boosted-tree-regression)
- [Survival regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#survival-regression)
- [Isotonic regression](https://spark.apache.org/docs/latest/ml-classification-regression.html#isotonic-regression)
- [Factorization machines regressor](https://spark.apache.org/docs/latest/ml-classification-regression.html#factorization-machines-regressor)

### Model Scalability

| Model                         | Number features | Training examples |
| ----------------------------- | --------------- | ----------------- |
| Linear regression             | 1 to 10 million | No limit          |
| Generalized linear regression | 4,096           | No limit          |
| Isotonic regression           | N/A             | Millions          |
| Decision trees                | 1,000s          | No limit          |
| Random forest                 | 10,000s         | No limit          |
| Gradient-boosted trees        | 1,000s          | No limit          |
| Survival regression           | 1 to 10 million | No limit          |

Data used in examples:

````python
df = spark.read.load("/data/regression")
````

## Linear Regression

- Linear Regression assumes that a linear combination of your input features results along with an amount of Gaussian error in output.
- Model Hyperparameters, Training Parameters are same as previous module or refer documentation.

```python
from pyspark.ml.regression import LinearRegression
lr = LinearRegression().setMaxIter(10).setRegParam(0.3).setElasticNetParam(0.8)
print lr.explainParams()
lrModel = lr.fit(df)
```

### Training Summary

The residuals are simply the weights for each of the features that we  input into the model. The objective history shows how our training is  going at every iteration. The root mean squared error is a measure of  how well our line is fitting the data, determined by looking at the  distance between each predicted value and the actual value in the data.  The R-squared variable is a measure of the proportion of the variance of the predicted variable that is captured by the model.

````python
summary = lrModel.summary
summary.residuals.show()
print(summary.totalIterations)
print(summary.objectiveHistory)
print(summary.rootMeanSquaredError)
print(summary.r2)
````

## Generalized Linear Regression

- standard linear regression is actually part of family of algorithms called generalized linear regression.
- Spark has two implementation of this algorithm, one is optimized for large set of features and other is more general includes support for more algorithms, doesn’t scale to large number of features.
- Generalized forms allow you to select your own noise function and support link function that specifies relationship between linear predictor and mean of distribution function.

| Family   | Response type | Supported links         |
| -------- | ------------- | ----------------------- |
| Gaussian | Continuous    | Identity*, Log, Inverse |
| Binomial | Binary        | Logit*, Probit, CLogLog |
| Poisson  | Count         | Log*, Identity, Sqrt    |
| Gamma    | Continuous    | Inverse*, Idenity, Log  |

### Model Hyperparameters

- `fitIntercept` and `regParam`
- `family` : description of error function to be used.
- `link` : name of link function which provides relationship between linear predictor and mean of distribution function.
- `solver`: algorithm to be used for optimization. currently only supports `irls `(iteratively reweighted least squares)
- `variancePower` : variance function of the Tweedie distribution, characterizes relationship between the variance and mean of the distribution. Supports : `0(default)` and `[1, Infinity)`
- `linkPower`: The index in the power link function for the Tweedie family.

### Training Parameters

- same as logistic regression.

### Prediction Parameters

- `linkPredictionCol`: A column name that will hold the output of our link function for each prediction.

````python
from pyspark.ml.regression import GeneralizedLinearRegression
glr = GeneralizedLinearRegression()\
  .setFamily("gaussian")\
  .setLink("identity")\
  .setMaxIter(10)\
  .setRegParam(0.3)\
  .setLinkPredictionCol("linkOut")
print glr.explainParams()
glrModel = glr.fit(df)
````

### Training Summary

- common success metric

  - R squared : The coefficient of determination; a measure of fit.

  - The residuals : The difference between the label and the predicted value.

## Decision Trees

- decision tree as applied to regression work similar to classification with only difference that they output a single number per leaf node instead of a label.
- Simply, rather than training coefficients to model a function, decision tree regression simply creates a tree to predict numerical outputs
- This is of significant consequence because unlike generalized linear  regression, we can predict nonlinear functions in the input data. This  also creates a significant risk of overfitting the data, so we need to  be careful when tuning and evaluating these models.

### Model Hyperparameters

- same as decision tree in classification except
- `impurity`: represents the metric (information gain) for whether or not the model should split at a particular leaf node with a particular value or keep it as is. The only metric currently supported for regression trees is “variance.”

### Training Parameters

- same as classification

### Example

````python
from pyspark.ml.regression import DecisionTreeRegressor
dtr = DecisionTreeRegressor()
print dtr.explainParams()
dtrModel = dtr.fit(df)
````

## Random Forests and Gradient Boosted Trees

- both follow same basic concept as the decision tree, rather than training one tree we train many trees and then averages
- In the random forest model, many de-correlated trees are trained and  then averaged. With gradient-boosted trees, each tree makes a weighted  prediction
- both have same model hyperparameters and training parameters as classification models except for purity measure.
- training parameters supports `checkpointInterval`

````python
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.regression import GBTRegressor
rf =  RandomForestRegressor()
print rf.explainParams()
rfModel = rf.fit(df)
gbt = GBTRegressor()
print gbt.explainParams()
gbtModel = gbt.fit(df)
````

## Advanced Methods

### Survival Regression (Accelerated Failure Time)

- statistician use survival analysis to understand survival rate of individuals, typically in controlled experiments.
- Spark implements the accelerated failure time model, which, rather than  describing the actual survival time, models the log of the survival  time. This variation of survival regression is implemented in Spark  because the more well-known Cox Proportional Hazard’s model is  semi-parametric and does not scale well to large datasets.
- By contrast, accelerated failure time does because each instance (row)  contributes to the resulting model independently. Accelerated failure  time does have different assumptions than the Cox survival model and  therefore one is not necessarily a drop-in replacement for the other. See [L. J. Wei’s paper](http://bit.ly/2rKxqcW) on accelerated failure time for more information.

### Isotonic Regression

- defines a piecewise linear function that is monotonically increasing.
- if your data is going up and to the right in a given plot, this is an appropriate model.

## Evaluators and Automating Model Tuning

- same core model tuning functionality similar to classification. We specify evaluator, pick a metric to optimize for and then train pipeline to perform that parameter tuning on our park.
- `RegressionEvaluator` allows us to optimize for a number of common regression success metrics. Just like the classification evaluator,  `RegressionEvaluator` expects two columns, a column representing the prediction and another representing the true label. The supported metrics to optimize for are the root mean squared error (“rmse”), the mean squared error (“mse”), the r2 metric (“r2”), and the mean absolute error (“mae”).

````python
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.regression import GeneralizedLinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
glr = GeneralizedLinearRegression().setFamily("gaussian").setLink("identity")
pipeline = Pipeline().setStages([glr])
params = ParamGridBuilder().addGrid(glr.regParam, [0, 0.5, 1]).build()
evaluator = RegressionEvaluator()\
  .setMetricName("rmse")\
  .setPredictionCol("prediction")\
  .setLabelCol("label")
cv = CrossValidator()\
  .setEstimator(pipeline)\
  .setEvaluator(evaluator)\
  .setEstimatorParamMaps(params)\
  .setNumFolds(2) # should always be 3 or more but this dataset is small
model = cv.fit(df)
````

## Metrics

we can also access a number of regression metrics via the `RegressionMetrics` object.

````python
from pyspark.mllib.evaluation import RegressionMetrics
out = model.transform(df)\
  .select("prediction", "label").rdd.map(lambda x: (float(x[0]), float(x[1])))
metrics = RegressionMetrics(out)
print("MSE: " + str(metrics.meanSquaredError))
print("RMSE: " + str(metrics.rootMeanSquaredError))
print("R-squared: " + str(metrics.r2))
print("MAE: " + str(metrics.meanAbsoluteError))
print("Explained variance: " + str(metrics.explainedVariance))
````



---

## File: pyspark/notes/ch28.md

# Recommendation

- by observing people’s explicit preferences or implicit preferences, we can predict recommendation on what one user may like based on similarity among users

## Use Cases

- Movie Recommendation by Netflix, Amazon, and HBO etc.
- Course Recommendations

In spark, there is Alternating Least Squares (ALS) algorithms which uses a technique called *collaborative* filtering, which makes recommendations based only on which items users interacted with in past.

It doesn’t require any additional features about users or the time. It supports several ALS variants.

## Collaborative Filtering with Alternating Least Squares

- ALS find a *k-dimensional* feature vector for each user user and item such that dot product of both approximates user’s rating for that item.
- It only requires input dataset of existing ratings between user-item pairs, with three columns: UserID, ItemID, and a rating column.
- NOTE: rating can be explicit - a numerical rating we aim to predict directly or implicit (based on user interaction)
- ALS suffers from *cold start* problem in Recommendation Systems. https://en.wikipedia.org/wiki/Cold_start_(recommender_systems)
- In terms of scaling it scales to million and billions of ratings.

### Model Hyperparameters

- `rank` (default 10) : dimension of feature vectors learned for users and items. This is tuned thru experimentation. Value of rank is proportional to fitting of data.
- `alpha` : when training of implicit feedback, alpha set a baseline confidence for preference. default is 1 and should be driven based on experimentation
- `regParam` : control regularization to prevent overfitting. default 0.1
- `implicitPrefs` Boolean value, training of implicit data or not.
- `nonnegative` : Boolean value, this parameter configures the model to place non-negative constraint on least-squares problem, and only return non-negative feature vectors.default is `false`

### Training Parameters

The groups of data that are distributed around the cluster are called *blocks*. Determining how much data to place in each block can have a significant impact on the time it takes to train the algorithm

A good rule of thumb is to aim for approximately one to five million ratings per block.

- `numUserBlocks` : determines how many blocks to split users into. default 10
- `numItemBlocks` : determines how many blocks to split items into. default 10
- `maxIter` : Total iteration over the data before splitting. Changing this probably won’t change results a ton. default 10
- `checkpointInterval` : Checkpointing allows you to save model state during training to more  quickly recover from node failures. You can set a checkpoint directory  using `SparkContext.setCheckpointDir`.
- `seed` : Specifying a random seed can help you replicate your results.

### Prediction Parameters

- defines how a trained model should actually make predictions
- There is one parameter : the cold start strategy (`coldStartStrategy`) determines how model should predict for users or items that did not appear in training set.
- The cold start challenge commonly arises when you’re serving a model in  production, and new users and/or items have no ratings history, and  therefore the model has no recommendation to make. It can also occur  when using simple random splits as in Spark’s `CrossValidator` or `TrainValidationSplit`, where it is very common to encounter users and/or items in the evaluation set that are not in the training set.
- By default, Spark will assign `NaN` prediction values when it encounters a user and/or item that is not present in the actual model.  This can be useful because you design your overall system to fall back  to some default recommendation when a new user or item is in the system. However, this is undesirable during training because it will ruin the  ability for your evaluator to properly measure the success of your  model. This makes model selection impossible. Spark allows users to set  the `coldStartStrategy` parameter to `drop` in order to drop any rows in the DataFrame of predictions that contain `NaN` values. The evaluation metric will then be computed over the non-`NaN` data and will be valid. `drop` and `nan` (the default) are the only currently supported cold-start strategies.

### Example

````python
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
ratings = spark.read.text("/data/sample_movielens_ratings.txt")\
  .rdd.toDF()\
  .selectExpr("split(value , '::') as col")\
  .selectExpr(
    "cast(col[0] as int) as userId",
    "cast(col[1] as int) as movieId",
    "cast(col[2] as float) as rating",
    "cast(col[3] as long) as timestamp")
training, test = ratings.randomSplit([0.8, 0.2])
als = ALS()\
  .setMaxIter(5)\
  .setRegParam(0.01)\
  .setUserCol("userId")\
  .setItemCol("movieId")\
  .setRatingCol("rating")
print(als.explainParams())
alsModel = als.fit(training)
predictions = alsModel.transform(test)

# output top k-recommendations for each user or movie
alsModel.recommendForAllUsers(10)\
  .selectExpr("userId", "explode(recommendations)").show()
alsModel.recommendForAllItems(10)\
  .selectExpr("movieId", "explode(recommendations)").show()
````

## Evaluators for Recommendation

- when covering cold-start strategy we can set up an automatic model evaluator working with ALS.
- recommendation problem is really just a kind of regression problem. since we are prediction rating for given users we want to optimize for reducing the toatl difference between our user’s rating and the true values.
- We can use same Regression Evaluator nad place this in a pipeline to automate training process. When we also set cold-strategy to `drop` instead of `NaN` and then switch back to `NaN` when it comes time to actually make prediction in production systems.

````python
from pyspark.ml.evaluation import RegressionEvaluator
evaluator = RegressionEvaluator()\
  .setMetricName("rmse")\
  .setLabelCol("rating")\
  .setPredictionCol("prediction")
rmse = evaluator.evaluate(predictions)
print("Root-mean-square error = %f" % rmse)
````

## Metric

- Recommendation results can be measured using both the standard regression metrics and some recommendation-specific metrics

### Regression Metrics

````python
from pyspark.mllib.evaluation import RegressionMetrics
regComparison = predictions.select("rating", "prediction")\
  .rdd.map(lambda x: (x(0), x(1)))
metrics = RegressionMetrics(regComparison)
````

### Ranking Metrics

A `RankingMetric` allows us to compare our recommendations with an actual set of ratings (or preferences) expressed by a given user. `RankingMetric` does not focus on the value of the rank but rather whether or not our  algorithm recommends an already ranked item again to a user. This does  require some data preparation on our part.

````python
from pyspark.mllib.evaluation import RankingMetrics, RegressionMetrics
from pyspark.sql.functions import col, expr
perUserActual = predictions\
  .where("rating > 2.5")\
  .groupBy("userId")\
  .agg(expr("collect_set(movieId) as movies"))
````

- At this point, we have a collection of users, along with a truth set of  previously ranked movies for each user. Now we will get our top 10  recommendations from our algorithm on a per-user basis.
- We will see then the top 10 recommendations show up in our truth set or not.

````python
perUserPredictions = predictions\
  .orderBy(col("userId"), expr("prediction DESC"))\
  .groupBy("userId")\
  .agg(expr("collect_list(movieId) as movies"))
````

- Now we have two DataFrames, one of predictions and another the  top-ranked items for a particular user. We can pass them into the `RankingMetrics` object.

````python
perUserActualvPred = perUserActual.join(perUserPredictions, ["userId"]).rdd\
  .map(lambda row: (row[1], row[2][:15]))
ranks = RankingMetrics(perUserActualvPred)

# now observe the metrics
ranks.meanAveragePrecision
ranks.precisionAt(5)
````

## Frequent Pattern Mining

- *Frequent pattern mining*, sometimes referred to as *market basket analysis*, looks at raw data and finds association rules.
- For instance, given a large number of transactions it might identify  that users who buy hot dogs almost always purchase hot dog buns. 
- This  technique can be applied in the recommendation context, especially when  people are filling shopping carts (either on or offline).

---

## File: pyspark/notes/ch29.md

# Unsupervised Learning

- Unsupervised learning is used less often because its usually little harder to apply and measure success. These challenges can become exacerbated at scale.
- For instance, clustering in high-dimensional space can create odd clusters simply because of the properties of high-dimensional spaces, something referred to as *the curse of dimensionality*. https://en.wikipedia.org/wiki/Curse_of_dimensionality
- Dimensionality increase corresponds to increase in sparsity of features and comes with noise in data.
- Model can hone in noise instead of true features.
- *unsupervised learning* is trying to discover patterns or derive a concise representation of the underlying structure of a given dataset.

## Use Cases

- Finding Anomalies in data
- Topic Modelling to predict text and its context.

## Model Scalability

| Model               | Statistical recommendation | Computation limits               | Training examples |
| ------------------- | -------------------------- | -------------------------------- | ----------------- |
| *k*-means           | 50 to 100 maximum          | Features x clusters < 10 million | No limit          |
| Bisecting *k*-means | 50 to 100 maximum          | Features x clusters < 10 million | No limit          |
| GMM                 | 50 to 100 maximum          | Features x clusters < 10 million | No limit          |
| LDA                 | An interpretable number    | 1,000s of topics                 | No limit          |

Data we will operate on

````python
from pyspark.ml.feature import VectorAssembler
va = VectorAssembler()\
  .setInputCols(["Quantity", "UnitPrice"])\
  .setOutputCol("features")

sales = va.transform(spark.read.format("csv")
  .option("header", "true")
  .option("inferSchema", "true")
  .load("/data/retail-data/by-day/*.csv")
  .limit(50)
  .coalesce(1)
  .where("Description IS NOT NULL"))

sales.cache()
````

## k-means

- one of the most popular clustering algorithms, in this method we take `k` clusters and assign datapoints to the clusters. The unassigned points are assigned based on their proximity (Euclidean distance) to previously assigned points
- As assignment happens, all points are assigned to a particular centroid, and a new centroid is computed. We repeat this process for finite iteration until convergence.
- It often a good idea to perform multiple runs of k-means starting with different intializations. Choosing the right value of k is important.

### Model Hyperparameters

- `k` : number of clusters that you would like to end up with.

### Training Parameters

- `initMode` : algorithm that determines starting point of centroids. Supports options are `random` and `k-means||` (default). The later is parallelized variant of `k-means` method.
- `initSteps` : number of steps for k-`mean||` initialization mode. must be greater than 0, default 2
- `maxIter` : total number of iteration over the data before stopping. Changing this probably doesn’t affect the outcomes too much. default 20
- `tol` : threshold by which changes in centroids show that we optimized our model enough to stop iteration. default - 0.0001

### Example

````python
from pyspark.ml.clustering import KMeans
km = KMeans().setK(5)
print km.explainParams()
kmModel = km.fit(sales)
````

### k-Means Metrics Summary

- k-means includes a summary class that we can use to evaluate our model.
- It includes info about clusters created and their relative sizes, we usually try to minimize the set of sum of squared error, subject to given number k of clusters

````python
summary = kmModel.summary
print(summary.clusterSizes) # number of points
kmModel.computeCost(sales)
centers = kmModel.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)
````

## Bisecting k-means

- variant of k-means. difference is instead of clustering points by starting `bottom-up` and assigning bunch of different groups in the data, this is a `top-down` clustering method.
- Starts with simple 1 group and then groups data in smaller groups to end up with k clusters

### Mode Hyperparameters

`k` : number of clusters to end up with

### Training Parameters

- `minDivisibleClusterSize` : min. number of points or min. proportions of points of a divisible cluster. default is 1, meaning that there must be at least one point in each cluster.
- `maxIter` : same as above

````python
from pyspark.ml.clustering import BisectingKMeans
bkm = BisectingKMeans().setK(5).setMaxIter(5)
bkmModel = bkm.fit(sales)
````

### Bisecting k-means Summary

````python
# in Python
summary = bkmModel.summary
print summary.clusterSizes # number of points
kmModel.computeCost(sales)
centers = kmModel.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)
````

## Gaussian Mixture Models

- GMM are another popular clustering algorithm, in GMM each cluster of data should be less likely to have data at the edge of cluster and much higher probability of having data in center.

### Model Hyperparameters

- `k` : number of clusters

### Training Parameters

- `maxIter`
- `tol`

### Example

````python
from pyspark.ml.clustering import GaussianMixture
gmm = GaussianMixture().setK(5)
print gmm.explainParams()
model = gmm.fit(sales)
````

### Gaussian Mixture Model Summary

````python
summary = model.summary
print model.weights
model.gaussiansDF.show()
summary.cluster.show()
summary.clusterSizes
summary.probability.show()
````

## Latent Dirichlet Allocations

- *Latent Dirichlet Allocation* (LDA) is a hierarchical clustering model typically used to perform topic  modelling on text documents. LDA tries to extract high-level topics from a series of documents and keywords associated with those topics. It then interprets each document as having a variable number of contributions from multiple input topics.
- There are two implementation of LDA
  - Online LDA
  - Expectation Maximization (used for large input vocabulary)
- To input our text data into LDA, we’re going to have to convert it into a numeric format. You can use the `CountVectorizer` to achieve this.

### Model Hyperparameters

- `k`
- `docConcentration` 
  - Concentration parameter (commonly named “alpha”) for the prior placed on documents’ distributions over topics (“theta”). This is the  parameter to a Dirichlet distribution, where larger values mean more  smoothing (more regularization).
  - If not set by the user, then `docConcentration` is set  automatically. If set to singleton vector [alpha], then alpha is  replicated to a vector of length k in fitting. Otherwise, the `docConcentration` vector must be length 𝘬.
- `topicConcentration` : The concentration parameter (commonly named “beta” or “eta”) for the  prior placed on a topic’s distributions over terms. This is the  parameter to a symmetric Dirichlet distribution. If not set by the user, then `topicConcentration` is set automatically.

### Training Parameters

- `maxIter`
- `optimizer` : determines whether use EM or online training oftimization. default is online
- `learningDecay` : Learning rate, set as an exponential decay rate. This should be between  (0.5, 1.0] to guarantee asymptotic convergence. The default is `0.51` and only applies to the online optimizer.
- `learningOffset` : A (positive) learning parameter that downweights early iterations.  Larger values make early iterations count less. The default is `1,024.0` and only applies to the online optimizer.
- `optimizeDocConcentration` : Indicates whether the `docConcentration` (Dirichlet parameter for document-topic distribution) will be optimized during training. The default is `true` but only applies to the online optimizer.
- `subsamplingRate` : The fraction of the corpus to be sampled and used in each iteration of  mini-batch gradient descent, in range (0, 1]. The default is `0.5` and only applies to the online optimizer.
- `seed`
- `checkpointInterval`

### Prediction Parameters

- `topicDistributionCol` : The column that will hold the output of topic mixture distribution for each document

### Example

````python
# prepare data
from pyspark.ml.feature import Tokenizer, CountVectorizer
tkn = Tokenizer().setInputCol("Description").setOutputCol("DescOut")
tokenized = tkn.transform(sales.drop("features"))
cv = CountVectorizer()\
  .setInputCol("DescOut")\
  .setOutputCol("features")\
  .setVocabSize(500)\
  .setMinTF(0)\
  .setMinDF(0)\
  .setBinary(True)
cvFitted = cv.fit(tokenized)
prepped = cvFitted.transform(tokenized)

# apply LDA
from pyspark.ml.clustering import LDA
lda = LDA().setK(10).setMaxIter(5)
print lda.explainParams()
model = lda.fit(prepped)

# describing models
model.describeTopics(3).show()
cvFitted.vocabulary
````



---

## File: pyspark/notes/ch3.md

# A Tour of Spark’s Toolset

## Running Production applications with `spark-submit`

- Using `spark-submit` we can send our code to a cluster and launch it. We can specify resources you application as well.
- `spark-submit` is not language bound, write your application in any supported languages by spark.

````python
./bin/spark-submit --class org.apache.spark.examples.SparkPi --master local ./examples/jars/spark-examples_2.11-2.2.0.jar 10
````

## Datasets: Type-Safe Structured APIs

- Datasets is a type-safe version of Structured APIs for writing statically typed code in Java and Scala, it is not available ini Python and R because they are dynamically typed.
- Dataframes are a distributed collection of objects of type `Row` that can hold various types of tabular data. Dataset API allows users to assign, Java/Scala class to the records within a DataFrame and manipulate it as a collection of typed objects,
- Datasets class is parameterized with type of object contained in it. `Dataset<T>` in Java and `Dataset[T]` in Scala.
- NOTE: One of the advantage of Datset is when you `collect` or `take` return type is not `Row` but the object type that you put in it.

## Structured Streaming

- Operations performed in Batch Mode using Spark’s structured APIs can be run in streaming fashion reducing latency and allowing incremental processing.
- One advantage is we can extract data out of streaming solution without almost any code change. We can prototype our application in batch mode and quickly switch over to streaming.

- We will play with retail data example

````python
# Static DataFrame
staticDataFrame = spark.read.format("csv")\
  .option("header", "true")\
  .option("inferSchema", "true")\
  .load("/data/retail-data/by-day/*.csv")

staticDataFrame.createOrReplaceTempView("retail_data")
staticSchema = staticDataFrame.schema

# Because data is time-series data, we might go along grouping and aggregating our data.
from pyspark.sql.functions import window, column, desc, col
staticDataFrame\
  .selectExpr(
    "CustomerId",
    "(UnitPrice * Quantity) as total_cost",
    "InvoiceDate")\
  .groupBy(
    col("CustomerId"), window(col("InvoiceDate"), "1 day"))\
  .sum("total_cost")\
  .show(5)

# because of local machine change shuffles to 5
spark.conf.set("spark.sql.shuffle.partitions", "5")
````

- The window function will include all data from each day in the aggregation. It’s simply a window over the time–series column in our data. This is a helpful tool for manipulating date and timestamps because we can specify our requirements in a more human form (via intervals)

````python
# Streaming Version of Above data
streamingDataFrame = spark.readStream\
    .schema(staticSchema)\
    .option("maxFilesPerTrigger", 1)\
    .format("csv")\
    .option("header", "true")\
    .load("/data/retail-data/by-day/*.csv")

purchaseByCustomerPerHour = streamingDataFrame\
  .selectExpr(
    "CustomerId",
    "(UnitPrice * Quantity) as total_cost",
    "InvoiceDate")\
  .groupBy(
    col("CustomerId"), window(col("InvoiceDate"), "1 day"))\
  .sum("total_cost")

purchaseByCustomerPerHour.writeStream\
    .format("memory")\
    .queryName("customer_purchases")\
    .outputMode("complete")\
    .start()
````

- streaming actions are a bit different from conventional static action because we are goind to be populating the data somewhere instead of just calling something like count (doesn’t make sense on stream anyways).
- The action we will use will output to an in-memory table that we will update(opeartion like max, sum) after each *trigger*. Here trigger is reading a specific file.
- when we start the stream we can run queries against it to debug what our results look like if we were to write this to production sink.

```python
spark.sql("""
  SELECT *
  FROM customer_purchases
  ORDER BY `sum(total_cost)` DESC
  """)\
  .show(5)
```

## Machine Learning & Advanced Analytics

- Another ability of Spark is to perform large-scale machine learning with a built-in library of machine learning algorithms called MLlib.
- MLlib allows for preprocessing, munging, training of models, and making  predictions at scale on data. You can even use models trained in MLlib  to make predictions in Strucutred Streaming.
- Example

````python
from pyspark.sql.functions import date_format, col
preppedDataFrame = staticDataFrame\
  .na.fill(0)\
  .withColumn("day_of_week", date_format(col("InvoiceDate"), "EEEE"))\
  .coalesce(5)

# Train-Test Split : TODO : use API to do train-test split
trainDataFrame = preppedDataFrame.where("InvoiceDate < '2011-07-01'")
testDataFrame = preppedDataFrame.where("InvoiceDate >= '2011-07-01'")

# We will use StringIndexer Transformer to convert days of week into indices
from pyspark.ml.feature import StringIndexer
indexer = StringIndexer()\
  .setInputCol("day_of_week")\
  .setOutputCol("day_of_week_index")

# Now we should encode this using One-Hot-Encoder
from pyspark.ml.feature import OneHotEncoder
encoder = OneHotEncoder()\
  .setInputCol("day_of_week_index")\
  .setOutputCol("day_of_week_encoded")

# above transformation will result in set of columns that we will "assemble" into a vector. All ML algorithms in Spark take as input a Vector Type, which must be a set of numerical values.
from pyspark.ml.feature import VectorAssembler
vectorAssembler = VectorAssembler()\
  .setInputCols(["UnitPrice", "Quantity", "day_of_week_encoded"])\
  .setOutputCol("features")

# create a pipeline
from pyspark.ml import Pipeline

transformationPipeline = Pipeline()\
  .setStages([indexer, encoder, vectorAssembler])

# let's fit the transformation model
fittedPipeline = transformationPipeline.fit(trainDataFrame)

# let's transform the training data
transformedTraining = fittedPipeline.transform(trainDataFrame)

# NOTE : At this point, it’s worth mentioning that we could have included our model training in our pipeline. We chose not to in order to demonstrate a use case for caching the data.

transformedTraining.cache()	# put a copy of intermediately transformed dataset in memory which can be useful for hyper-parameter tuning

# train the model
from pyspark.ml.clustering import KMeans
kmeans = KMeans()\
  .setK(20)\
  .setSeed(1L)
````

- There are always two types for every algorithm in MLlib’s DataFrame API. They follow the naming pattern of `Algorithm`, for the untrained version, and `AlgorithmModel` for the trained version. In our example, this is `KMeans` and then `KMeansModel`.
- Estimators in MLlib’s DataFrame API share roughly the same interface  that we saw earlier with our preprocessing transformers like the `StringIndexer`. This should come as no surprise because it makes training an entire pipeline (which includes the model) simple.

````python
kmModel = kmeans.fit(transformedTraining)

# we can find compute cost
kmModel.computeCost(transformedTraining)

transformedTest = fittedPipeline.transform(testDataFrame)

kmModel.computeCost(transformedTest)
# we can keep on improving this model more using hyper-parameter tuning
````

## Lower-Level APIs

- Spark includes a number of lower-level primitives to allow for arbitrary Java and Python object manipulation via Resilient Distributed Datasets(RDDs)
- Virtually everything in Spark is built on top of RDDs
- RDDs are lower level than DataFrames because they reveal physical execution characteristics (like partitions) to end users.
- We can use RDDs to parallelize raw data we have in memory on the driver machine

```python
spark.sparkContext.parallelize([Row(1), Row(2), Row(3)]).toDF()
```

## SparkR

- SparkR is a tool for running R on Spark. It follows the same principles as all of Spark’s other language bindings. To use SparkR, you simply import it into your environment and run your code. It’s all very similar to the  Python API except that it follows R’s syntax instead of Python.

## Spark’s Ecosystem and Packages

- One of the best parts about Spark is the ecosystem of packages and tools  that the community has created. Some of these tools even move into the  core Spark project as they mature and become widely used. As of this  writing, the list of packages is rather long, numbering over 300—and  more are added frequently. You can find the largest index of Spark  Packages at [spark-packages.org](https://spark-packages.org/), where any user can publish to this package repository. There are also  various other projects and packages that you can find on the web; for  example, on GitHub.


---

## File: pyspark/notes/ch30.md

# Graph Analytics

- *Graph analytics* is the process of analyzing these relationships.

- Graphs are a natural way of describing relationships and many different  problem sets, and Spark provides several ways of working in this analytics paradigm.

- Spark has long contained an RDD-based library for performing graph  processing: GraphX. This provided a very low-level interface that was  extremely powerful, but just like RDDs, wasn’t easy to use or optimize.

- However, some of the developers of Spark (including some of the original authors of GraphX) have recently created a next-generation graph analytics library on Spark: GraphFrames.

[GraphFrames](http://graphframes.github.io/index.html) is currently [available as a Spark package](http://spark-packages.org/package/graphframes/graphframes), an external package that you need to load when you start up your Spark  application, but may be merged into the core of Spark in the future. For the most part, there should be little difference in performance between the two (except for a huge user experience improvement in GraphFrames). There is some small overhead when using GraphFrames, but for the most  part it tries to call down to GraphX where appropriate; and for most,  the user experience gains greatly outweigh this minor overhead.

````shell
./bin/spark-shell --packages graphframes:graphframes:0.5.0-spark2.2-s_2.11
````

````python
bikeStations = spark.read.option("header","true")\
  .csv("/data/bike-data/201508_station_data.csv")
tripData = spark.read.option("header","true")\
  .csv("/data/bike-data/201508_trip_data.csv")
````

## Building a Graph

- Example building a directed graph. graph will point from source to destination location

````python
stationVertices = bikeStations.withColumnRenamed("name", "id").distinct()
tripEdges = tripData\
  .withColumnRenamed("Start Station", "src")\
  .withColumnRenamed("End Station", "dst")
````

````python
# building graphframe object
from graphframes import GraphFrame
stationGraph = GraphFrame(stationVertices, tripEdges)
stationGraph.cache()
````

````python
# in Python
print "Total Number of Stations: " + str(stationGraph.vertices.count())
print "Total Number of Trips in Graph: " + str(stationGraph.edges.count())
print "Total Number of Trips in Original Data: " + str(tripData.count())

# Total Number of Stations: 70
# Total Number of Trips in Graph: 354152
# Total Number of Trips in Original Data: 354152
````

## Querying a Graph

````python
from pyspark.sql.functions import desc
stationGraph.edges.groupBy("src", "dst").count().orderBy(desc("count")).show(10)

+--------------------+--------------------+-----+
|                 src|                 dst|count|
+--------------------+--------------------+-----+
|San Francisco Cal...|     Townsend at 7th| 3748|
|Harry Bridges Pla...|Embarcadero at Sa...| 3145|
...
|     Townsend at 7th|San Francisco Cal...| 2192|
|Temporary Transba...|San Francisco Cal...| 2184|
+--------------------+--------------------+-----+

# Filtering by any valid DF Expression
stationGraph.edges\
  .where("src = 'Townsend at 7th' OR dst = 'Townsend at 7th'")\
  .groupBy("src", "dst").count()\
  .orderBy(desc("count"))\
  .show(10)

+--------------------+--------------------+-----+
|                 src|                 dst|count|
+--------------------+--------------------+-----+
|San Francisco Cal...|     Townsend at 7th| 3748|
|     Townsend at 7th|San Francisco Cal...| 2734|
...
|   Steuart at Market|     Townsend at 7th|  746|
|     Townsend at 7th|Temporary Transba...|  740|
+--------------------+--------------------+-----+
````

### Subgraphs

*Subgraphs* are just smaller graphs within the larger one. We saw in the last section how we can query a given set of edges and vertices.

````python
townAnd7thEdges = stationGraph.edges\
  .where("src = 'Townsend at 7th' OR dst = 'Townsend at 7th'")
subgraph = GraphFrame(stationGraph.vertices, townAnd7thEdges)
````

## Motif Finding

*Motifs* are a way of expresssing structural patterns in a graph. When we specify a  motif, we are querying for patterns in the data instead of actual data. In GraphFrames, we specify our query in a domain-specific language  similar to Neo4J’s Cypher language. This language lets us specify  combinations of vertices and edges and assign then names.

For example, if we want to specify that a given vertex `a` connects to another vertex `b` through an edge `ab`, we would specify `(a)-[ab]->(b)`. The names inside parentheses or brackets do not signify values but  instead what the columns for matching vertices and edges should be named in the resulting DataFrame. We can omit the names (e.g., `(a)-[]->()`) if we do not intend to query the resulting values.

````python
motifs = stationGraph.find("(a)-[ab]->(b); (b)-[bc]->(c); (c)-[ca]->(a)")
````

````python
from pyspark.sql.functions import expr
motifs.selectExpr("*",
    "to_timestamp(ab.`Start Date`, 'MM/dd/yyyy HH:mm') as abStart",
    "to_timestamp(bc.`Start Date`, 'MM/dd/yyyy HH:mm') as bcStart",
    "to_timestamp(ca.`Start Date`, 'MM/dd/yyyy HH:mm') as caStart")\
  .where("ca.`Bike #` = bc.`Bike #`").where("ab.`Bike #` = bc.`Bike #`")\
  .where("a.id != b.id").where("b.id != c.id")\
  .where("abStart < bcStart").where("bcStart < caStart")\
  .orderBy(expr("cast(caStart as long) - cast(abStart as long)"))\
  .selectExpr("a.id", "b.id", "c.id", "ab.`Start Date`", "ca.`End Date`")
  .limit(1).show(1, False)
````

## Graph Algorithms

### PageRank

````python
from pyspark.sql.functions import desc
ranks = stationGraph.pageRank(resetProbability=0.15, maxIter=10)
ranks.vertices.orderBy(desc("pagerank")).select("id", "pagerank").show(10)

+--------------------+------------------+
|                  id|          pagerank|
+--------------------+------------------+
|San Jose Diridon ...| 4.051504835989922|
|San Francisco Cal...|3.3511832964279518|
...
|     Townsend at 7th| 1.568456580534273|
|Embarcadero at Sa...|1.5414242087749768|
+--------------------+------------------+
````

### In-Degree and Out-Degree Metric

- used in context of social networking, follow and followers

````python
inDeg = stationGraph.inDegrees
inDeg.orderBy(desc("inDegree")).show(5, False)

+----------------------------------------+--------+
|id                                      |inDegree|
+----------------------------------------+--------+
|San Francisco Caltrain (Townsend at 4th)|34810   |
|San Francisco Caltrain 2 (330 Townsend) |22523   |
|Harry Bridges Plaza (Ferry Building)    |17810   |
|2nd at Townsend                         |15463   |
|Townsend at 7th                         |15422   |
+----------------------------------------+--------+

# outdegree
outDeg = stationGraph.outDegrees
outDeg.orderBy(desc("outDegree")).show(5, False)

+---------------------------------------------+---------+
|id                                           |outDegree|
+---------------------------------------------+---------+
|San Francisco Caltrain (Townsend at 4th)     |26304    |
|San Francisco Caltrain 2 (330 Townsend)      |21758    |
|Harry Bridges Plaza (Ferry Building)         |17255    |
|Temporary Transbay Terminal (Howard at Beale)|14436    |
|Embarcadero at Sansome                       |14158    |
+---------------------------------------------+---------+
````

The ratio of these two values is an interesting metric to look at. A  higher ratio value will tell us where a large number of trips end (but  rarely begin), while a lower value tells us where trips often begin (but infrequently end):

````python
degreeRatio = inDeg.join(outDeg, "id")\
  .selectExpr("id", "double(inDegree)/double(outDegree) as degreeRatio")
degreeRatio.orderBy(desc("degreeRatio")).show(10, False)
degreeRatio.orderBy("degreeRatio").show(10, False)
````

### BFS

We can specify the maximum of edges to follow with the `maxPathLength`, and we can also specify an `edgeFilter` to filter out edges that do not meet a requirement, like trips during nonbusiness hours.

````python
stationGraph.bfs(fromExpr="id = 'Townsend at 7th'",
  toExpr="id = 'Spear at Folsom'", maxPathLength=2).show(10)

+--------------------+--------------------+--------------------+
|                from|                  e0|                  to|
+--------------------+--------------------+--------------------+
|[65,Townsend at 7...|[913371,663,8/31/...|[49,Spear at Fols...|
|[65,Townsend at 7...|[913265,658,8/31/...|[49,Spear at Fols...|
...
|[65,Townsend at 7...|[903375,850,8/24/...|[49,Spear at Fols...|
|[65,Townsend at 7...|[899944,910,8/21/...|[49,Spear at Fols...|
+--------------------+--------------------+--------------------+
````

### Connected Components

- A *connected component* defines an (undirected) subgraph that has connections to itself but does not connect to the greater graph

````python
spark.sparkContext.setCheckpointDir("/tmp/checkpoints")

minGraph = GraphFrame(stationVertices, tripEdges.sample(False, 0.1))
cc = minGraph.connectedComponents()

cc.where("component != 0").show()

+----------+------------------+---------+-----------+---------+------------+-----
|station_id|                id|      lat|       long|dockcount|    landmark|in...
+----------+------------------+---------+-----------+---------+------------+-----
|        47|   Post at Kearney|37.788975|-122.403452|       19|San Franc...|  ...
|        46|Washington at K...|37.795425|-122.404767|       15|San Franc...|  ...
+----------+------------------+---------+-----------+---------+------------+-----
````

### Strongly Connected Components

- A strongly connected component is a subgraph that has paths between all pairs of vertices inside it.
- NOTE: takes directionality into account

````python
scc = minGraph.stronglyConnectedComponents(maxIter=3)
scc.groupBy("component").count().show()
````

### Advanced Tasks

This is just a short selection of some of the features of GraphFrames.  The GraphFrames library also includes features such as writing your own  algorithms via a message-passing interface, triangle counting, and  converting to and from GraphX. You can find more information in the  GraphFrames documentation.

---

## File: pyspark/notes/ch31.md

# Deep Learning

- Because deep learning is still a new field, many of the newest tools are implemented in external libraries. 

## What is Deep Learning ?

- A neural network is a graph of nodes with weights and activation functions.
- Nodes are organized into layers that are stacked on top of one another, each layer is connected, either partially or completely, to previous layer in the network.
- The goal is to train the network to associate certain inputs with  certain outputs by tuning the weights associated with each connection  and the values of each node in the network.

![Image Classification with Convolutional Neural Networks | by ...](./ch31.assets/1*3fA77_mLNiJTSgZFhYnU0Q@2x.png)

- *Deep Learning* or *deep neural networks*, stack many of these layers together into various different architectures. This concept has existed for decades and have waxed and waned in terms of popularity for various machine learning problems.
- Typical machine learning techniques typically cannot continue to perform well as more data is added; their performance hits a ceiling. Deep learning can benefit from enormous amounts of data and information.
- The most popular tools are TensorFlow, MXNet, Keras, and PyTorch.

## Ways of Using Deep Learning in Spark

- Inference : The simplest way to use deep learning is to take a pretrained model and apply it to large datasets in parallel using Spark. Using pyspark we could simply call a framework such as TensorFlow or PyTorch in a map function to get distributed inference.
- Featurization and transfer Learning : The next level of complexity is to use an existing model as a *featurizer* instead of taking its final output. Many deep learning models learn  useful feature representations in their lower layers as they get trained for an end-to-end task.
  - This method is called *transfer learning*, and generally involves the last few layers of a pretrained model and retraining them with the  data of interest. Transfer learning is also especially useful if you do  not have a large amount of training data: training a full-blown network  from scratch requires a dataset of hundreds of thousands of images, like ImageNet, to avoid overfitting, which
- Model Training : Spark can also be used to train a new deep learning model from scratch. There are two common methods here. 
  - First, you can use a Spark cluster to  parallelize the training of a *single* model over multiple servers, communicating updates between them. 
  - Alternatively, some libraries let the user train *multiple* instances of similar models in parallel to try various model  architectures and hyperparameters, accelerating the model search and  tuning process.

## Deep Learning Libraries

### MLlib Neural Network Support

Spark’s MLlib currently has native support for a single deep learning algorithm: the `ml.classification.MultilayerPerceptronClassifier` class’s multilayer perceptron classifier. This class is limited to training relatively shallow networks containing fully connected layers  with the sigmoid activation function and an output layer with a softmax  activation function. 

This class is most useful for training the last few layers of a classification model when using transfer learning on top of an existing deep learning–based featurizer.

### TensorFrames

[TensorFrames](https://github.com/databricks/tensorframes) is an inference and transfer learning-oriented library that makes it easy to pass data between Spark DataFrames and TensorFlow.

### BigDL

[BigDL](https://github.com/intel-analytics/BigDL) is a distributed deep learning framework for Apache Spark primarily  developed by Intel. It aims to support distributed training of large  models as well as fast applications of these models using inference.

### TensorFlowOnSpark

[TensorFlowOnSpark](https://github.com/yahoo/TensorFlowOnSpark) is a widely used library that can train TensorFlow models in a parallel  fashion on Spark clusters. TensorFlow includes some foundations to do  distributed training, but it still needs to rely on a cluster manager  for managing the hardware and data communications. It does not come with a cluster manager or a distributed I/O layer out of the box.  TensorFlowOnSpark launches TensorFlow’s existing distributed mode inside a Spark job, and automatically feeds data from Spark RDDs or DataFrames into the TensorFlow job.

### DeepLearning4J

[DeepLearning4j](https://deeplearning4j.org/spark) is an open-source, distributed deep learning project in Java and Scala that  provides both single-node and distributed training options.

### Deep Learning Pipelines

[Deep Learning Pipelines](https://github.com/databricks/spark-deep-learning) is an open source package from Databricks that integrates deep learning  functionality into Spark’s ML Pipelines API. The package existing deep  learning frameworks (TensorFlow and Keras at the time of writing), but  focuses on two goals:

- Incorporating these frameworks into standard Spark APIs (such as ML Pipelines and Spark SQL) to make them very easy to use
- Distributing all computation by default

## A simple example with Deep Learning Pipelines





---

## File: pyspark/notes/ch32.md

# Language Specifics : Python (Pyspark) and R (SparkR and sparklyr)

NOTE: Here I only write about Pyspark as It is scope of my requirements, probably try to Read Book for more on R.

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_0202.png)

## Pyspark

### Fundamental PySpark Differences

- While using Structured APIs, Python runs as fast as Scala except when using UDFs due to serialization costs.
- The fundamental idea is that Spark is going to have to work a lot  harder converting information from something that Spark and the JVM can  understand to Python and back again. This includes both functions as  well as data and is a process known as *serialization*.

## Pandas Integration

- PySpark works across programming models.
- A common pattern is to perform very-large scale ETL work with Spark and then collect the result to driver and use Pandas to manipulate it further

```python
import pandas as pd
df = pd.DataFrame({"first":range(200), "second":range(50,250)})
sparkDF = spark.createDataFrame(df)
newPDF = sparkDF.toPandas()
newPDF.head()
```



... NOTE Part on R is left out ...

---

## File: pyspark/notes/ch33.md

# Ecosystem and Community

## Spark Packages 

Spark has a package repository for packages specific to Spark: [Spark Packages](https://spark-packages.org/). packages are libraries for Spark applications that can easily be shared with the community. [GraphFrames](http://graphframes.github.io/) is a perfect example; it makes graph analysis available on Spark’s  structured APIs in ways much easier to use than the lower-level (GraphX) API built into Spark

Healthcare and genomics have seen a surge in opportunity for big data applications. For example, the [ADAM Project](http://bdgenomics.org/) leverages unique, internal optimizations to Spark’s Catalyst engine to provide a scalable API & CLI for genome processing.

Another package, [Hail](https://hail.is/), is an open source, scalable framework for exploring and analyzing  genomic data. Starting from sequencing or microarray data in VCF and  other formats, Hail provides scalable algorithms to enable statistical  analysis of gigabyte-scale data on a laptop or terabyte-scale data on  cluster.

### Popular Spark Packages

- [Spark Cassandra Connector](https://github.com/datastax/spark-cassandra-connector/) : This connector helps you get data in and out of the Cassandra database.
- [Spark Redshift Connector](https://github.com/databricks/spark-redshift) : This connector helps you get data in and out of the Redshift database.
- [Spark bigquery](https://github.com/spotify/spark-bigquery): This connector helps you get data in and out of Google’s BigQuery.
- [Spark Avro](https://github.com/databricks/spark-avro): This package allows you to read and write Avro files.
- [Elasticsearch](https://github.com/elastic/elasticsearch-hadoop): This package allows you to get data into and out of Elasticsearch.
- [Magellan](https://github.com/harsha2010/magellan): Allows you to perform geo-spatial data analytics on top of Spark.
- [GraphFrames](http://graphframes.github.io/): Allows you to perform graph analysis with DataFrames.
- [Spark Deep Learning](https://github.com/databricks/spark-deep-learning): Allows you to leverage Deep Learning and Spark together.

## Community

### Spark Summit

- Event that occurs across globe at various times a year.
- People attend to learn about cutting edge in Spark and Uses Cases
- There are hundreds of videos on such events are available

### Local Meetups

- Use meeting.com to find groups near you!

---

## File: pyspark/notes/ch4.md

# Structured API Overview

- The Structured APIs allows manipulation of all sorts of data from CSV(semi-structured) or Parquet(highly structured because schema validation happens at the write time)
- APIs refer to three core types of distributed collection APIs
  - Datasets
  - DataFrames
  - SQL tables and views

## DataFrames and Datasets

Spark has two notions of structured collections : DataFrames and Datasets.

- Both are (distributed) table like collections with rows and columns
  - Each column must have same number of rows as all other columns
  - Each column type has type information that must be consistent in every row in collection.
- To spark both represent immutable, lazily evaluated plans that specify what operations to apply to data residing at a location to generate some output.

## Schemas

- Schema defines the *column names* and *types* of a Dataframe
- Can be defined or read from data source (*schema on read*)

## Overview of Structured Spark Types

- Spark is effectively a programming languages that uses a engine *Catalyst* that maintains its own type information through the planning and processing of the work.
- Even if we use dynamically typed language most of these operation still operate strictly on Spark Types, not python.

### DataFrames vs DataSets

Within structured APIs, there are two more APIs

- *untyped* DataFrames : slight inaccurate representation, they have types but they are managed by Spark and only checks whether those types line up to those specified in the schema at runtime.

- *typed* Datasets : checks whether types conform to specifications at runtime. Only available in JVM based languages like Scala and Java.

Usages in Languages

- To spark(in Scala) DataFrames are simply Datasets of Type `Row`. Making it highly specialized and optimized rather than using JVM types and causing high garbage-collection and object instantiation costs.
- To spark(in Python or R), there is no such thing as Datasets, everything is a DataFrame and therefore we always operate on that optimized format.

-  NOTE : The `Row` type is Spark’s internal representation of its optimized in-memory format for computation

### Columns

- represent a simple type like an integer or a string, a complex type like an air or map or *null* value.

### Rows

- A row is nothing more than a record of data. Each record in a DataFrame must be of type `Row`. e.g. `spark.range(2).collect()`

### Spark Types

- How to declare a column to be of a specific type.

````python
from pyspark.sql.types import *
b = ByteType()
````

- python types at times have certain requirements. Refer this : http://bit.ly/2EdflXW


| Data type     | Value type in Python                                                                                                                                                    | API to access or create a data type                                                                                          |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| ByteType      | int or long. Note: Numbers will be converted to 1-byte signed integer numbers at runtime. Ensure that numbers are within the range of –128 to 127.                      | ByteType()                                                                                                                   |
| ShortType     | int or long. Note: Numbers will be converted to 2-byte signed integer numbers at runtime. Ensure that numbers are within the range of –32768 to 32767.                  | ShortType()                                                                                                                  |
| IntegerType   | int or long. Note: Python has a lenient definition of “integer.” Numbers that are too large will be rejected by Spark SQL if you use the IntegerType(). It’s best practice to use LongType. | IntegerType()                                                                                                                |
| LongType      | long. Note: Numbers will be converted to 8-byte signed integer numbers at runtime. Ensure that numbers are within the range of –9223372036854775808 to 9223372036854775807. Otherwise, convert data to decimal.Decimal and use DecimalType. | LongType()                                                                                                                   |
| FloatType     | float. Note: Numbers will be converted to 4-byte single-precision floating-point numbers at runtime.                                                                   | FloatType()                                                                                                                  |
| DoubleType    | float                                                                                                                                                                   | DoubleType()                                                                                                                 |
| DecimalType   | decimal.Decimal                                                                                                                                                         | DecimalType()                                                                                                                |
| StringType    | string                                                                                                                                                                  | StringType()                                                                                                                 |
| BinaryType    | bytearray                                                                                                                                                               | BinaryType()                                                                                                                 |
| BooleanType   | bool                                                                                                                                                                    | BooleanType()                                                                                                                |
| TimestampType | datetime.datetime                                                                                                                                                       | TimestampType()                                                                                                              |
| DateType      | datetime.date                                                                                                                                                           | DateType()                                                                                                                   |
| ArrayType     | list, tuple, or array                                                                                                                                                   | ArrayType(elementType, [containsNull]). Note: The default value of containsNull is True.                                     |
| MapType       | dict                                                                                                                                                                    | MapType(keyType, valueType, [valueContainsNull]). Note: The default value of valueContainsNull is True.                      |
| StructType    | list or tuple                                                                                                                                                           | StructType(fields). Note: fields is a list of StructFields. Also, fields with the same name are not allowed.                 |
| StructField   | The value type in Python of the data type of this field (for example, Int for a StructField with the data type IntegerType)                                             | StructField(name, dataType, [nullable]). Note: The default value of nullable is True.                                        |

## Overview of Structured API Executions

- Execution of a single structured API query from user code to executed code.
  1. Write DataFrame/Dataset/SQL Code
  2. If valid code, spark converts this to a *Logical Plan*
  3. Spark transforms this *Logical Plan* to a *Physical Plan*, checking for optimizations along the way.
  4. Spark then executes this *Physical Plan* (RDD manipulations) on the cluster.

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_0401.png)

### Logical Planning

- Represents a set of abstract transformations that do not refer to executors or drivers, it’s purely to convert the user’s set of expressions into most optimized versions
- It does this by converting user code into a *unresolved logical plan* (valid code still needs to be checked for unknown column references etc.)
- Spark uses the *catalog*, a repository of all table and DataFrame information, to *resolve* columns and tables in the *analyzer*

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_0402.png)

### Physical Planning (Spark Plan)

- specifies how the logical plan will execute on the cluster by generating different physical execution strategies and comparing them through a cost model
- Physical planning results in a series of RDDs and transformations. This result  is why you might have heard Spark referred to as a compiler—it takes  queries in DataFrames, Datasets, and SQL and compiles them into RDD  transformations for you.

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_0403.png)

### Execution

- Spark runs all of this code over RDDs
- Spark performs further optimizations at runtime, generating native Java  bytecode that can remove entire tasks or stages during execution. Finally the result is returned to the user.


---

## File: pyspark/notes/ch5.md

# Basic Structured Operations

Dataframe:

- consists of series of records that are of type `Row`
- columns representing a computation expression to be performed on rows
- *Schema* representing type of data in each column
- *Partitioning* of DataFrame defines the layout of the DataFrame or Dataset’s physical distribution across clusters.

## Schemas

- schema defines the column names and types of DataFrame.
- schema is a `StructType` made up of a number of fields, `StructField`s that have name, type and a Boolean representing nullability of the column.

````python
spark.read.format("json").load("/data/flight-data/json/2015-summary.json").schema

# Output
StructType(List(StructField(DEST_COUNTRY_NAME,StringType,true),
StructField(ORIGIN_COUNTRY_NAME,StringType,true),
StructField(count,LongType,true)))
````

- NOTE: Schema’s can contain other StructTypes as well.
- If the types in the data (at runtime) do not match the schema, Spark will throw an error.

````python
# Manual Schema on Read

myManualSchema = StructType([
  StructField("DEST_COUNTRY_NAME", StringType(), True),
  StructField("ORIGIN_COUNTRY_NAME", StringType(), True),
  StructField("count", LongType(), False, metadata={"hello":"world"})
])
df = spark.read.format("json").schema(myManualSchema)\
  .load("/data/flight-data/json/2015-summary.json")
````

## Columns and Expressions

- we can select, manipulate, and remove columns from DataFrames and these operations are called as *expressions*

### Columns

````python
# There are multiple ways to construct and refer to columns
from pyspark.sql.functions import col, column
col("someColumnName")
column("someColumnName")
````

- Columns are not *resolved* until we compare the column names with those we are maintaining in the *catalog*.Column and table resolution happens in the *analyzer* phase

````python
# referencing a column of a df explicitly
df.col("count")
````

### Expressions

An *expression* is a set of transformations on one or more values in a record in a DataFrame

- simplest case is an expression created via the `expr` function, is just a DataFrame column reference. `expr("someCol")` is equivalent to `col("someCol")`

#### **Columns as expression**

- Columns provide a subset of expression functionality. If you use `col()` and want to perform transformations on that column, you must perform those on that column reference. When using an expression, the `expr` function can actually parse transformations and column references from a string and can subsequently be passed into further transformations

- `expr("someCol - 5")` is the same transformation as performing `col("someCol") - 5`, or even `expr("someCol") - 5`

- Example : `(((col("someCol") + 5) * 200) - 6) < col("otherCol")`

#### **Accessing a DataFrame’s columns**

````python
# you could always use printSchema but a more programatic approach is below
spark.read.format("json").load("/data/flight-data/json/2015-summary.json")
  .columns
````

## Records and Rows

- each row in a DataFrame is a single record. e.g. use `df.first()` to get one Row
- `Row` objects internally represent arrays of bytes. The byte  array interface is never shown to users because we only use column expressions to manipulate them.

#### Creating Rows

- You can create rows by manually instantiating a `Row` object with the values that belong in each column.

````python
from pyspark.sql import Row
myRow = Row("Hello", None, 1, False)

myRow[0]
myRow[2]
````

## DataFrame Transformations

### Creating DataFrames

- loading from a file

````python
# load the df up
df = spark.read.format("json").load("/data/flight-data/json/2015-summary.json")
df.createOrReplaceTempView("dfTable")
````

- creating DataFrames on the fly

````python
from pyspark.sql import Row
from pyspark.sql.types import StructField, StructType, StringType, LongType
myManualSchema = StructType([
  StructField("some", StringType(), True),
  StructField("col", StringType(), True),
  StructField("names", LongType(), False)
])
myRow = Row("Hello", None, 1)
myDf = spark.createDataFrame([myRow], myManualSchema)
myDf.show()
````

### select and selectExpr

SQL Equivalents for

````sql
SELECT * FROM dataFrameTable
SELECT columnName FROM dataFrameTable
SELECT columnName * 10, otherColumn, someOtherCol as c FROM dataFrameTable
````

For Dataframes

```python
# selecting one column
df.select("DEST_COUNTRY_NAME").show(2)
# selecting multiple columns
df.select("DEST_COUNTRY_NAME", "ORIGIN_COUNTRY_NAME").show(2)
# using column expressions
from pyspark.sql.functions import expr, col, column
df.select(
    expr("DEST_COUNTRY_NAME"),	# most flexible reference
    col("DEST_COUNTRY_NAME"),
    column("DEST_COUNTRY_NAME"))\
  .show(2)
```

One common error is attempting to mix `Column` objects and strings. For e.g.

````python
# wrong, will result in error
df.select(col("DEST_COUNTRY_NAME"), "DEST_COUNTRY_NAME")
````

````python
# contd..
# flexibilty of using expr
df.select(expr("DEST_COUNTRY_NAME AS destination")).show(2)

# using alias
df.select(expr("DEST_COUNTRY_NAME as destination").alias("DEST_COUNTRY_NAME"))\
  .show(2)

# since select is followed by a series of expr is common there is a shorthand selectExpr
df.selectExpr("DEST_COUNTRY_NAME as newColumnName", "DEST_COUNTRY_NAME").show(2)
````

- `selectExpr` is very powerful allowing complext expressions that create new DataFrames
- we can add any valid non-aggregating SQL statement, as long as the columns resolve.

````python
df.selectExpr(
  "*", # all original columns
  "(DEST_COUNTRY_NAME = ORIGIN_COUNTRY_NAME) as withinCountry")\
  .show(2)
#  equivalent sql code
# SELECT *, (DEST_COUNTRY_NAME = ORIGIN_COUNTRY_NAME) as withinCountry
# FROM dfTable
# LIMIT 2
````

- we can specify aggregation over entire DataFrames as well

````python
df.selectExpr("avg(count)", "count(distinct(DEST_COUNTRY_NAME))").show(2)
#
SELECT avg(count), count(distinct(DEST_COUNTRY_NAME)) FROM dfTable LIMIT 2
````

### Converting to Spark Types (Literals)

- sometimes we need to pass explicit values in Spark that are just a value (rather a new column). This maybe constant or something we compare on later.

````python
from pyspark.sql.functions import lit
df.select(expr("*"), lit(1).alias("One")).show(2)

# SQL
# SELECT *, 1 as One FROM dfTable LIMIT 2
````

### Adding Columns

````python
# more formal way to add column
df.withColumn("numberOne", lit(1)).show(2)
# lets make it as an expression
df.withColumn("withinCountry", expr("ORIGIN_COUNTRY_NAME == DEST_COUNTRY_NAME"))\
  .show(2)
````

### Renaming Columns

````python
df.withColumnRenamed("DEST_COUNTRY_NAME", "dest").columns
# you could rename multiple columns using
df.withColumnsRenamed(column_map)
````

### Reserved Characters and Keywords

- you could encounter reserved characters like spaces or dashes in column names. To escape these columns properly use “`” (backtick)

````python
# withColum expects first arg to string, thats why it works
dfWithLongColName = df.withColumn(
    "This Long Column-Name",
    expr("ORIGIN_COUNTRY_NAME"))

# for selectExpr this is not the case
dfWithLongColName.selectExpr(
    "`This Long Column-Name`",
    "`This Long Column-Name` as `new col`")\
  .show(2)
````

### Case Sensitivity

- by default Spark is case insensitive, but can made that way using

```sql
set spark.sql.caseSensitive true
```

### Removing Columns

````python
# remove single column
df.drop("ORIGIN_COUNTRY_NAME").columns
# deleting multiple columns
dfWithLongColName.drop("ORIGIN_COUNTRY_NAME", "DEST_COUNTRY_NAME")
````

### Changing a Column’s Type (cast)

````python
df.withColumn("count2", col("count").cast("long"))
````

### Filtering Rows

````python
# both where and filter are equivalent
df.filter(col("count") < 2).show(2)	# expressions
df.where("count < 2").show(2)	# its easy to write
````

if you want to specify multiple AND filters, just chain them sequentially

````python
df.where(col("count") < 2).where(col("ORIGIN_COUNTRY_NAME") != "Croatia")\
  .show(2)
````

### Getting Unique Rows

````python
df.select("ORIGIN_COUNTRY_NAME", "DEST_COUNTRY_NAME").distinct().count()
````

### Random Samples

````python
seed = 5
withReplacement = False
fraction = 0.5 # fraction of rows to extract
df.sample(withReplacement, fraction, seed).count()
````

### Random Splits

````python
dataFrames = df.randomSplit([0.25, 0.75], seed)	# two dfs
dataFrames[0].count() > dataFrames[1].count() # False
````

### Concatenating and Appending Rows (Union)

- even tho DataFrames are immutable. we can use `union` to append to a DataFrame concatenating two DFs.
- NOTE: both DF should have same schema and number of columns for union

````python
from pyspark.sql import Row
schema = df.schema
newRows = [
  Row("New Country", "Other Country", 5L),
  Row("New Country 2", "Other Country 3", 1L)
]
parallelizedRows = spark.sparkContext.parallelize(newRows)
newDF = spark.createDataFrame(parallelizedRows, schema)

# Union
# in Python
df.union(newDF)\
  .where("count = 1")\
  .where(col("ORIGIN_COUNTRY_NAME") != "United States")\
  .show()
````

### Sorting Rows

````python
# sort
df.sort("count").show(5)
df.orderBy("count", "DEST_COUNTRY_NAME").show(5)
df.orderBy(col("count"), col("DEST_COUNTRY_NAME")).show(5)

# direction of sort using asc and desc functions
from pyspark.sql.functions import desc, asc
df.orderBy(expr("count desc")).show(2)
df.orderBy(col("count").desc(), col("DEST_COUNTRY_NAME").asc()).show(2)
````

- An advanced tip is to use `asc_nulls_first`, `desc_nulls_first`, `asc_nulls_last`, or `desc_nulls_last` to specify where you would like your null values to appear in an ordered DataFrame.

### Limit

````python
df.limit(5).show()
df.orderBy(expr("count desc")).limit(6).show()
````

### Repartition and Coalesce

- Another important optimization opportunity is to partition the data according  to some frequently filtered columns, which control the physical layout  of data across the cluster including the partitioning scheme and the  number of partitions.
- Repartition will incur a full shuffle of the data, regardless of whether one is necessary. This means that you should typically only repartition when the future number of partitions is greater than your current  number of partitions or when you are looking to partition by a set of  columns

````python
df.repartition(5)
# we filter on this column often
df.repartition(col("DEST_COUNTRY_NAME"))
````

- Coalesce, on the other hand, will not incur a full shuffle and will try to combine partitions

````python
df.repartition(5, col("DEST_COUNTRY_NAME")).coalesce(2)
````

### Collecting Rows to the Driver

- Spark maintains the state of the cluster in the driver, there are times when we could collect some of the data to the driver in order to manipudate it on your local machine.
- `collect` gets all data from entire DataFrame, `take` select the first N rows, and `show` prints out a number of rows nicely.

````python
collectDF = df.limit(10)
collectDF.take(5) # take works with an Integer count
collectDF.show() # this prints it out nicely
collectDF.show(5, False)
collectDF.collect()
````

- We can also using local iterator to iterate over entire dataset partition-by-partition in a serial manner.

````python
collectDF.toLocalIterator()
````

---

## File: pyspark/notes/ch6.md

# Working with Different Types of Data

Where to look for APIs and find functions to transform your data.

- DataFrame (Dataset) Methods
- Column Methods

`org.apache.spark.sql.functions` contains a variety of functions for a range of different data types.

````python
df = spark.read.format("csv")\
  .option("header", "true")\
  .option("inferSchema", "true")\
  .load("/data/retail-data/by-day/2010-12-01.csv")
df.printSchema()
df.createOrReplaceTempView("dfTable")
````

## Converting to Spark Types

- very common operation where we convert native types to Spark Types

````python
from pyspark.sql.functions import lit
df.select(lit(5), lit("five"), lit(5.0))
````

## Working with Booleans

- 4 types of Boolean Statements : `and` , `or`, `true` and `false`

````python
from pyspark.sql.functions import col
df.where(col("InvoiceNo") != 536365)\
  .select("InvoiceNo", "Description")\
  .show(5, False)

# more cleaner approach is to specify predicate as expression string
df.where("InvoiceNo = 536365")
  .show(5, false)
````

- In Spark, you should always chain together `and` filters as a sequential filter. Because even if they are expressed serially, spark will flatten all of these filters into one statement and perform the filter at a time.

````python
from pyspark.sql.functions import instr
priceFilter = col("UnitPrice") > 600
descripFilter = instr(df.Description, "POSTAGE") >= 1
df.where(df.StockCode.isin("DOT")).where(priceFilter | descripFilter).show()
````

- we can use Boolean Columns to filter a `DataFrame`

````python
# we here don't have to chain filters
from pyspark.sql.functions import instr
DOTCodeFilter = col("StockCode") == "DOT"
priceFilter = col("UnitPrice") > 600
descripFilter = instr(col("Description"), "POSTAGE") >= 1
df.withColumn("isExpensive", DOTCodeFilter & (priceFilter | descripFilter))\
  .where("isExpensive")\
  .select("unitPrice", "isExpensive").show(5)
````

````python
# in Python
from pyspark.sql.functions import expr
df.withColumn("isExpensive", expr("NOT UnitPrice <= 250"))\
  .where("isExpensive")\
  .select("Description", "UnitPrice").show(5)
````

NOTE: be carefull with null data and use following expression `df.where(col("Description").eqNullSafe("hello")).show()`

## Working with Numbers

#### Power Function

````python
from pyspark.sql.functions import expr, pow
# power function
fabricatedQuantity = pow(col("Quantity") * col("UnitPrice"), 2) + 5
df.select(expr("CustomerId"), fabricatedQuantity.alias("realQuantity")).show(2)
````

- Note we can multiply columns together both were numerical.

````python
# sparksql
df.selectExpr(
  "CustomerId",
  "(POWER((Quantity * UnitPrice), 2.0) + 5) as realQuantity").show(2)
````

#### Rounding Off

````python
from pyspark.sql.functions import lit, round, bround

df.select(round(lit("2.5")), bround(lit("2.5"))).show(2) # round off only if in between both numbers

# Output
+-------------+--------------+
|round(2.5, 0)|bround(2.5, 0)|
+-------------+--------------+
|          3.0|           2.0|
|          3.0|           2.0|
+-------------+--------------+
````

#### Correlation of two Columns

````python
from pyspark.sql.functions import corr
df.stat.corr("Quantity", "UnitPrice")
df.select(corr("Quantity", "UnitPrice")).show()
````

#### Summary Statistics

````python
# in Python
df.describe().show()

+-------+------------------+------------------+------------------+
|summary|          Quantity|         UnitPrice|        CustomerID|
+-------+------------------+------------------+------------------+
|  count|              3108|              3108|              1968|
|   mean| 8.627413127413128| 4.151946589446603|15661.388719512195|
| stddev|26.371821677029203|15.638659854603892|1854.4496996893627|
|    min|               -24|               0.0|           12431.0|
|    max|               600|            607.49|           18229.0|
+-------+------------------+------------------+------------------+
````

````python
# Manually doing above operations
from pyspark.sql.functions import count, mean, stddev_pop, min, max

# approxQuantile
colName = "UnitPrice"
quantileProbs = [0.5]
relError = 0.05
df.stat.approxQuantile("UnitPrice", quantileProbs, relError) # 2.51

# Cross Tabulation
df.stat.crosstab("StockCode", "Quantity").show()

# Freq Items
df.stat.freqItems(["StockCode", "Quantity"]).show()

# add a unique ID to each row by using the function monotonically_increasing_id
from pyspark.sql.functions import monotonically_increasing_id
df.select(monotonically_increasing_id()).show(2)
````

## Working with Strings

#### `initcap`

- Capitalize every word in a given string

````python
from pyspark.sql.functions import initcap
df.select(initcap(col("Description"))).show()
````

#### `upper/lower`

````python
from pyspark.sql.functions import lower, upper
df.select(col("Description"),
    lower(col("Description")),
    upper(lower(col("Description")))).show(2)
````

#### Cleaning up Strings

````python
from pyspark.sql.functions import lit, ltrim, rtrim, rpad, lpad, trim
df.select(
    ltrim(lit("    HELLO    ")).alias("ltrim"),
    rtrim(lit("    HELLO    ")).alias("rtrim"),
    trim(lit("    HELLO    ")).alias("trim"),
    lpad(lit("HELLO"), 3, " ").alias("lp"),
    rpad(lit("HELLO"), 10, " ").alias("rp")).show(2)

+---------+---------+-----+---+----------+
|    ltrim|    rtrim| trim| lp|        rp|
+---------+---------+-----+---+----------+
|HELLO    |    HELLO|HELLO| HE|HELLO     |
|HELLO    |    HELLO|HELLO| HE|HELLO     |
+---------+---------+-----+---+----------+
````

### Regular Expressions

- Spark takes advantage of the complete power of Java regular expressions. The Java regular expression syntax departs slightly from other  programming languages, so it is worth reviewing before putting anything  into production. 
- Two important functions `regexp_extract` and `regexp_replace`

````python
from pyspark.sql.functions import regexp_replace
regex_string = "BLACK|WHITE|RED|GREEN|BLUE"
df.select(
  regexp_replace(col("Description"), regex_string, "COLOR").alias("color_clean"),
  col("Description")).show(2)

+--------------------+--------------------+
|         color_clean|         Description|
+--------------------+--------------------+
|COLOR HANGING HEA...|WHITE HANGING HEA...|
| COLOR METAL LANTERN| WHITE METAL LANTERN|
+--------------------+--------------------+
````

````python
# Simple Replace

from pyspark.sql.functions import translate
df.select(translate(col("Description"), "LEET", "1337"),col("Description"))\
  .show(2)

+----------------------------------+--------------------+
|translate(Description, LEET, 1337)|         Description|
+----------------------------------+--------------------+
|              WHI73 HANGING H3A...|WHITE HANGING HEA...|
|               WHI73 M37A1 1AN73RN| WHITE METAL LANTERN|
+----------------------------------+--------------------+
````

````python
# grep first color
from pyspark.sql.functions import regexp_extract
extract_str = "(BLACK|WHITE|RED|GREEN|BLUE)"
df.select(
     regexp_extract(col("Description"), extract_str, 1).alias("color_clean"),
     col("Description")).show(2)
````

````python
# check if key exists
from pyspark.sql.functions import instr
containsBlack = instr(col("Description"), "BLACK") >= 1
containsWhite = instr(col("Description"), "WHITE") >= 1
df.withColumn("hasSimpleColor", containsBlack | containsWhite)\
  .where("hasSimpleColor")\
  .select("Description").show(3, False)
````

````python
# how to take in a list of colors and take advantage of spark varargs
from pyspark.sql.functions import expr, locate
simpleColors = ["black", "white", "red", "green", "blue"]
def color_locator(column, color_string):
  return locate(color_string.upper(), column)\
          .cast("boolean")\
          .alias("is_" + c)
selectedColumns = [color_locator(df.Description, c) for c in simpleColors]
selectedColumns.append(expr("*")) # has to a be Column type

df.select(*selectedColumns).where(expr("is_white OR is_red"))\
  .select("Description").show(3, False)
````

## Working with Dates and Timestamps

Dates and times are a constant challenge in programming languages and  databases. It’s always necessary to keep track of timezones and ensure  that formats are correct and valid.

Spark has two kinds of time-related information

- Date
- Timestamps (both time and date)

- working with dates and timestamps closely relates to working with strings because we often store our timestamps or dates as strings and convert them into date types at runtime.This is less common when working with databases and structured data but much more common when we are working with text and CSV files.

Another gotcha with spark is `TimestampType` class only supports seconds-level precision which means that if you are going to be working with milliseconds & microseconds, you are own your own probably using `longs`.

````python
from pyspark.sql.functions import current_date, current_timestamp
dateDF = spark.range(10)\
  .withColumn("today", current_date())\
  .withColumn("now", current_timestamp())
dateDF.createOrReplaceTempView("dateTable")

# subtract/add 5 days in column for date
from pyspark.sql.functions import date_add, date_sub
dateDF.select(date_sub(col("today"), 5), date_add(col("today"), 5)).show(1)

# checking different between two dates
# NOTE: returns number of days
from pyspark.sql.functions import datediff, months_between, to_date
dateDF.withColumn("week_ago", date_sub(col("today"), 7))\
  .select(datediff(col("week_ago"), col("today"))).show(1)

dateDF.select(
    to_date(lit("2016-01-01")).alias("start"),
    to_date(lit("2017-05-22")).alias("end"))\
  .select(months_between(col("start"), col("end"))).show(1)
````

````python
# string to date
from pyspark.sql.functions import to_date, lit
spark.range(5).withColumn("date", lit("2017-01-01"))\
  .select(to_date(col("date"))).show(1)

# NOTE: I faced this issue once in production :)
# Spark will not throw an error if it cannot parse the date; rather, it will just return null

dateDF.select(to_date(lit("2016-20-12")),to_date(lit("2017-12-11"))).show(1)
+-------------------+-------------------+
|to_date(2016-20-12)|to_date(2017-12-11)|
+-------------------+-------------------+
|               null|         2017-12-11|
+-------------------+-------------------+

# Specifying date format to avoid above issues
from pyspark.sql.functions import to_date
dateFormat = "yyyy-dd-MM"
cleanDateDF = spark.range(1).select(
    to_date(lit("2017-12-11"), dateFormat).alias("date"),
    to_date(lit("2017-20-12"), dateFormat).alias("date2"))
cleanDateDF.createOrReplaceTempView("dateTable2")
````

- NOTE: `to_timestamp` always requires a format

````python
from pyspark.sql.functions import to_timestamp
cleanDateDF.select(to_timestamp(col("date"), dateFormat)).show()
+----------------------------------+
|to_timestamp(`date`, 'yyyy-dd-MM')|
+----------------------------------+
|               2017-11-12 00:00:00|
+----------------------------------+
````

## Working with Nulls in Data

- As a best practice always use nulls to represent missing or empty data in DF
- Spark can optimize working with null values more than it can if you use empty strings or placeholders

- Usually we can do following operations with null values

#### Coalesce

````python
# allows to select first non-null value from a set of columns
# note : if there are no null values, returns first column
from pyspark.sql.functions import coalesce
df.select(coalesce(col("Description"), col("CustomerId"))).show()
````

#### ifnull, nullIf, nvl, and nvl2

````sql
# sparksql
SELECT
  ifnull(null, 'return_value'),
  nullif('value', 'value'),
  nvl(null, 'return_value'),
  nvl2('not_null', 'return_value', "else_value")
FROM dfTable LIMIT 1

+------------+----+------------+------------+
|           a|   b|           c|           d|
+------------+----+------------+------------+
|return_value|null|return_value|return_value|
+------------+----+------------+------------+
````

#### drop

````python
df.na.drop()	# drops rows if any value is null
df.na.drop("any")	# drops rows if any value is null

# above two are same
df.na.drop("all") # drops rows only if all values are null or NaN
df.na.drop("all", subset=["StockCode", "InvoiceNo"]) # if all of these columns is null
````

#### fill

````python
# fill all null values in columns of type String
df.na.fill("All Null values become this string")

# filling only specific columns
df.na.fill("all", subset=["StockCode", "InvoiceNo"])
fill_cols_vals = {"StockCode": 5, "Description" : "No Value"}
df.na.fill(fill_cols_vals)
````

#### replace

````python
df.na.replace([""], ["UNKNOWN"], "Description")
````

## Ordering

you can use `asc_nulls_first`, `desc_nulls_first`, `asc_nulls_last`, or `desc_nulls_last` to specify where you would like your null values to appear in an ordered DataFrame.

Check previous chapter for more details.

## Working with Complex Types

### Structs

- structs are like DataFrame within DataFrame.

````python
df.selectExpr("(Description, InvoiceNo) as complex", "*")
df.selectExpr("struct(Description, InvoiceNo) as complex", "*")
````

````python
from pyspark.sql.functions import struct
complexDF = df.select(struct("Description", "InvoiceNo").alias("complex"))
complexDF.createOrReplaceTempView("complexDF")
````

Now we can query all values in struct using `*.` notation

````python
complexDF.select("complex.*")
````

### Arrays

- let’s break every word in description and put it into a row in our DF (Explode)

#### split

````python
# SELECT split(Description, ' ') FROM dfTable

from pyspark.sql.functions import split
df.select(split(col("Description"), " ")).show(2)
+---------------------+
|split(Description,  )|
+---------------------+
| [WHITE, HANGING, ...|
| [WHITE, METAL, LA...|
+---------------------+
   
# NOTE: we can also query this complex type
df.select(split(col("Description"), " ").alias("array_col"))\
  .selectExpr("array_col[0]").show(2)
````

#### Array Length

````python
from pyspark.sql.functions import size
df.select(size(split(col("Description"), " "))).show(2) # shows 5 and 3
````

#### array_contains

````python
from pyspark.sql.functions import array_contains
df.select(array_contains(split(col("Description"), " "), "WHITE")).show(2)
````

### explode

- takes a column that consists of arrays and creates one row (with rest of values duplicated) per value in the array

````python
from pyspark.sql.functions import split, explode

df.withColumn("splitted", split(col("Description"), " "))\
  .withColumn("exploded", explode(col("splitted")))\
  .select("Description", "InvoiceNo", "exploded").show(2)

+--------------------+---------+--------+
|         Description|InvoiceNo|exploded|
+--------------------+---------+--------+
|WHITE HANGING HEA...|   536365|   WHITE|
|WHITE HANGING HEA...|   536365| HANGING|
+--------------------+---------+--------+

````

### maps

- Maps are created using the `map` function and key-value pairs of columns.

````python
from pyspark.sql.functions import create_map
df.select(create_map(col("Description"), col("InvoiceNo")).alias("complex_map"))\
  .show(2)
+--------------------+
|         complex_map|
+--------------------+
|Map(WHITE HANGING...|
|Map(WHITE METAL L...|
+--------------------+
````

- We can query map by using a proper key. A missing key return `null`

````python
df.select(map(col("Description"), col("InvoiceNo")).alias("complex_map"))\
  .selectExpr("complex_map['WHITE METAL LANTERN']").show(2)
````

- We can explode map types into columns

````python
df.select(map(col("Description"), col("InvoiceNo")).alias("complex_map"))\
  .selectExpr("explode(complex_map)").show(2)

+--------------------+------+
|                 key| value|
+--------------------+------+
|WHITE HANGING HEA...|536365|
| WHITE METAL LANTERN|536365|
+--------------------+------+
````

## Working with JSON

- spark supports direct operations on strings of JSON.

````python
jsonDF = spark.range(1).selectExpr("""
  '{"myJSONKey" : {"myJSONValue" : [1, 2, 3]}}' as jsonString""")
````

- we can use `get_json_object` to inline query a JSON Object be it a dictionary or array. Or we can use `json_tuple` if this object has only one level of nesting.

````python
jsonDF.select(
    get_json_object(col("jsonString"), "$.myJSONKey.myJSONValue[1]") as "column",
    json_tuple(col("jsonString"), "myJSONKey")).show(2)

+------+--------------------+
|column|                  c0|
+------+--------------------+
|     2|{"myJSONValue":[1...|
+------+--------------------+
````

- converting structType into a JSON string by using `to_json` function

````python
from pyspark.sql.functions import to_json
df.selectExpr("(InvoiceNo, Description) as myStruct")\
  .select(to_json(col("myStruct")))

# This function also accepts a dictionary (map) of parameters that are the same as the JSON # data source. You can use the from_json function to parse this (or other JSON data) back in.
# This naturally requires you to specify a schema, and optionally you can specify a map of options, as well:

from pyspark.sql.functions import from_json
from pyspark.sql.types import *
parseSchema = StructType((
  StructField("InvoiceNo",StringType(),True),
  StructField("Description",StringType(),True)))
df.selectExpr("(InvoiceNo, Description) as myStruct")\
  .select(to_json(col("myStruct")).alias("newJSON"))\
  .select(from_json(col("newJSON"), parseSchema), col("newJSON")).show(2)


+----------------------+--------------------+
|jsontostructs(newJSON)|             newJSON|
+----------------------+--------------------+
|  [536365,WHITE HAN...|{"InvoiceNo":"536...|
|  [536365,WHITE MET...|{"InvoiceNo":"536...|
+----------------------+--------------------+
````

## User-Defined Functions

- UDFs make it possible for us to write our own custom transformations using Python and even use external libraries.
- UDFs can take and return one or more columns as input. Spark UDFs are very powerful because we can write them in several different programming languages; you do not need to create them in an esoteric format or domain-specific language
- They are just function that operate on data record by record. By default these are registered as temporary functions to be used in taht specific Spark Session or Context.

````python
udfExampleDF = spark.range(5).toDF("num")
def power3(double_value):
  return double_value ** 3
power3(2.0)

# register the function
from pyspark.sql.functions import udf
power3udf = udf(power3)

# usage
from pyspark.sql.functions import col
udfExampleDF.select(power3udf(col("num"))).show(2)

# registering this UDF as Spark SQL Function
from pyspark.sql.types import IntegerType, DoubleType
spark.udf.register("power3py", power3, DoubleType())

udfExampleDF.selectExpr("power3py(num)").show(2)
````

- When you want to optionally return a value from a UDF, you should return `None` in Python
-  NOTE: UDFs written in Java or Scala are little faster than those written in python, in Case of Java/Scala, we can use it within JVM.This means that there will be little performance penalty aside from the  fact that you can’t take advantage of code generation capabilities that  Spark has for built-in functions. There can be performance issues if you create or use a lot of objects
- But in case of Python. Spark starts a Python process on the worker, serializes all of the data to a format that Python can understand (remember, it was in the JVM  earlier), executes the function row by row on that data in the Python process, and then finally returns the results of the row operations to the JVM and Spark
- Starting this Python process is expensive, but the real cost is in serializing the data to Python. This is costly for two reasons: it is an expensive computation, but also, after the data enters Python, Spark cannot manage the memory of the worker. This means that you could potentially cause a worker to fail if it becomes resource constrained.

Conclusion : Whenever possible write UDFs in Scala or Java because you can use them in Python as well.

---

## File: pyspark/notes/ch7.md

# Aggregations

Aggregating is the act of collecting something together. Usually we define aggregations one or more columns. This function must produce one result for each group, given multiple input values.

````python
df = spark.read.format("csv")\
  .option("header", "true")\
  .option("inferSchema", "true")\
  .load("/data/retail-data/all/*.csv")\
  .coalesce(5)
df.cache()
df.createOrReplaceTempView("dfTable")

+---------+---------+--------------------+--------+--------------+---------+-----
|InvoiceNo|StockCode|         Description|Quantity|   InvoiceDate|UnitPrice|Cu...
+---------+---------+--------------------+--------+--------------+---------+-----
|   536365|   85123A|WHITE HANGING...    |       6|12/1/2010 8:26|     2.55|  ...
|   536365|    71053|WHITE METAL...      |       6|12/1/2010 8:26|     3.39|  ...
...
|   536367|    21755|LOVE BUILDING BLO...|       3|12/1/2010 8:34|     5.95|  ...
|   536367|    21777|RECIPE BOX WITH M...|       4|12/1/2010 8:34|     7.95|  ...
+---------+---------+--------------------+--------+--------------+---------+-----
````

Basic Aggregations apply to an entire DataFrame. Simplest example is `count` method.

````python
df.count() == 541909
````

- remember count is actually an action as compared to transformation and so it returns immediately.
- We can use `count` to get an idea of the total size of your dataset but another common pattern is to use it to cache an entire DataFrame in memory.

## Aggregation Functions

All aggregations are available as functions, in addition to the special cases that can appear on DataFrames or via `.stat`

### count

````python
from pyspark.sql.functions import count
df.select(count("StockCode")).show() # 541909
````

Warning : when you run `count(*)` Spark counts null values, including rows with all nulls. However when run a column it will not count null values

### countDistinct

````python
from pyspark.sql.functions import countDistinct
df.select(countDistinct("StockCode")).show() # 4070
````

### approx_count_distinct

````python
from pyspark.sql.functions import approx_count_distinct
df.select(approx_count_distinct("StockCode", 0.1)).show() # 3364
````

### first and last

get the first and last values from a DataFrame

````python
from pyspark.sql.functions import first, last
df.select(first("StockCode"), last("StockCode")).show()
````

### min and max

````python
from pyspark.sql.functions import min, max
df.select(min("Quantity"), max("Quantity")).show()
````

### sum

````python
from pyspark.sql.functions import sum
df.select(sum("Quantity")).show() # 5176450
````

### sumDistinct

````python
from pyspark.sql.functions import sumDistinct
df.select(sumDistinct("Quantity")).show() # 29310
````

### avg

````python
from pyspark.sql.functions import sum, count, avg, expr

df.select(
    count("Quantity").alias("total_transactions"),
    sum("Quantity").alias("total_purchases"),
    avg("Quantity").alias("avg_purchases"),
    expr("mean(Quantity)").alias("mean_purchases"))\
  .selectExpr(
    "total_purchases/total_transactions",
    "avg_purchases",
    "mean_purchases").show()
````

### Variance and Standard Deviation

````python
from pyspark.sql.functions import var_pop, stddev_pop
from pyspark.sql.functions import var_samp, stddev_samp
df.select(var_pop("Quantity"), var_samp("Quantity"),
  stddev_pop("Quantity"), stddev_samp("Quantity")).show()
````

### skewness and kurtosis

- both are measures of extreme points in data
- skewness measures the asymmetry of the values in your data around the mean
- kurtosis is a measure of the tail of the data.

````python
from pyspark.sql.functions import skewness, kurtosis
df.select(skewness("Quantity"), kurtosis("Quantity")).show()
````

### Covariance and Correlation

````python
from pyspark.sql.functions import corr, covar_pop, covar_samp
df.select(corr("InvoiceNo", "Quantity"), covar_samp("InvoiceNo", "Quantity"),
    covar_pop("InvoiceNo", "Quantity")).show()
````

### Aggregating to Complex Types

````python
from pyspark.sql.functions import collect_set, collect_list
df.agg(collect_set("Country"), collect_list("Country")).show()

+--------------------+---------------------+
|collect_set(Country)|collect_list(Country)|
+--------------------+---------------------+
|[Portugal, Italy,...| [United Kingdom, ...|
+--------------------+---------------------+
````

## Grouping

- usually group operations are done on categorical data for which we group our data on one column and perform some calculations on the other columns that end up in that group
- Its a two phase process : first grouping and then declaring aggregations on it.

````python
df.groupBy("InvoiceNo", "CustomerId").count().show()
````

### Grouping with Expressions

- counting is a bit of a special case because it exists as a method. For this, usually we prefer to use the `count` function.
- Rather than passing that function as an expression into a `select` statement, we specify it as within `agg`. This makes it possible for you to pass-in arbitrary expressions that just need to have some aggregation specified.

````python
from pyspark.sql.functions import count

df.groupBy("InvoiceNo").agg(
    count("Quantity").alias("quan"),
    expr("count(Quantity)")).show()

+---------+----+---------------+
|InvoiceNo|quan|count(Quantity)|
+---------+----+---------------+
|   536596|   6|              6|
...
|  C542604|   8|              8|
+---------+----+---------------+
````

### Grouping with Maps

- Sometimes, it can be easier to specify your transformations as a series of `Maps` for which the key is the column, and the value is the aggregation function (as a string) that you would like to perform.

````python
df.groupBy("InvoiceNo").agg(expr("avg(Quantity)"),expr("stddev_pop(Quantity)")).show()

+---------+------------------+--------------------+
|InvoiceNo|     avg(Quantity)|stddev_pop(Quantity)|
+---------+------------------+--------------------+
|   536596|               1.5|  1.1180339887498947|
...
|  C542604|              -8.0|  15.173990905493518|
+---------+------------------+--------------------+
````

## Window Functions

- window functions are used to carry out unique aggregations by either computing some aggregation on the `window` of data, which you define by using a reference to the current data.
- Window specification determines which rows will be passed in to this function.
- Difference : *group-by* takes data, and every row can go only into one grouping. A window function calculates a return value for every input row of a table based on a group of rows, called a frame.Each row can fall into one or more frames.
- A common use case is to take a look at a rolling average of some value  for which each row represents one day. If you were to do this, each row  would end up in seven different frames.

![image](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781491912201/files/assets/spdg_0701.png)

````python
from pyspark.sql.functions import col, to_date
dfWithDate = df.withColumn("date", to_date(col("InvoiceDate"), "MM/d/yyyy H:mm"))
dfWithDate.createOrReplaceTempView("dfWithDate")
````

First step is to create a window specification. Note that the `partition by` is an unnrelated to partitioning scheme concept from earlier. It here just defines how we will be breaking up our group.

````python
from pyspark.sql.window import Window
from pyspark.sql.functions import desc
windowSpec = Window\
  .partitionBy("CustomerId", "date")\
  .orderBy(desc("Quantity"))\
  .rowsBetween(Window.unboundedPreceding, Window.currentRow)
````

Now we can use aggregation function to learn more about each specific customer. An example might be establishing the max purchase quantity over all time.

````python
from pyspark.sql.functions import max
maxPurchaseQuantity = max(col("Quantity")).over(windowSpec)
````

NOTE: this return a column (or expressions). We can now use this in a DataFrame select statement. Before doing so, though, we will create the purchase quantity rank. To do that we use the `dense_rank` function to determine which date had the maximum purchase quantity for every customer.

````python
from pyspark.sql.functions import dense_rank, rank
purchaseDenseRank = dense_rank().over(windowSpec)
purchaseRank = rank().over(windowSpec)
````

````python
# This also returns a column that we can use in select statements. Now we can 
# perform a select to view the calculated window
dfWithDate.where("CustomerId IS NOT NULL").orderBy("CustomerId")\
  .select(
    col("CustomerId"),
    col("date"),
    col("Quantity"),
    purchaseRank.alias("quantityRank"),
    purchaseDenseRank.alias("quantityDenseRank"),
    maxPurchaseQuantity.alias("maxPurchaseQuantity")).show()


+----------+----------+--------+------------+-----------------+---------------+
|CustomerId|      date|Quantity|quantityRank|quantityDenseRank|maxP...Quantity|
+----------+----------+--------+------------+-----------------+---------------+
|     12346|2011-01-18|   74215|           1|                1|          74215|
|     12346|2011-01-18|  -74215|           2|                2|          74215|
|     12347|2010-12-07|      36|           1|                1|             36|
|     12347|2010-12-07|      30|           2|                2|             36|
...
|     12347|2010-12-07|      12|           4|                4|             36|
|     12347|2010-12-07|       6|          17|                5|             36|
|     12347|2010-12-07|       6|          17|                5|             36|
+----------+----------+--------+------------+-----------------+---------------+
````

Another Example :

````python
window_spec = Window.partitionBy("Department").orderBy("Salary")
ranked_employees = employees.withColumn("Rank", row_number().over(window_spec))
ranked_employees.show()

+----------+--------+------+----+
|Department|Employee|Salary|Rank|
+----------+--------+------+----+
|       HR |     Eva|  5500|   1|
|       HR |   David|  6000|   2|
|    Sales |     Bob|  4000|   1|
|    Sales | Charlie|  4500|   2|
|    Sales |   Alice|  5000|   3|
+----------+--------+------+----+

# two row moving average in a within each department

window_spec_avg = Window.partitionBy("Department").orderBy("Salary").rowsBetween(-1, 1)
moving_avg_employees = employees.withColumn("MovingAvg", avg("Salary").over(window_spec_avg))
moving_avg_employees.show()

+----------+--------+------+------------------+
|Department|Employee|Salary|         MovingAvg|
+----------+--------+------+------------------+
|       HR |     Eva|  5500|             5750.0|
|       HR |   David|  6000|             5750.0|
|    Sales |     Bob|  4000| 4250.0|
|    Sales | Charlie|  4500| 4500.0|
|    Sales |   Alice|  5000| 4750.0|
+----------+--------+------+------------------+
````

## Grouping Sets

- powerful feature used for aggregating data across multiple dimensions and combinations in a single query.
- Grouping sets are a low-level tool for combining sets of aggregations  together. They give you the ability to create arbitrary aggregation in  their group-by statements.

Example : we would like to get the total quantity of all stock codes and customers.

````python
dfNoNull = dfWithDate.drop()
dfNoNull.createOrReplaceTempView("dfNoNull")
````

````sql
-- in SQL
SELECT CustomerId, stockCode, sum(Quantity) FROM dfNoNull
GROUP BY customerId, stockCode
ORDER BY CustomerId DESC, stockCode DESC

+----------+---------+-------------+
|CustomerId|stockCode|sum(Quantity)|
+----------+---------+-------------+
|     18287|    85173|           48|
|     18287|   85040A|           48|
|     18287|   85039B|          120|
...
|     18287|    23269|           36|
+----------+---------+-------------+

-- above problem using GROUPING SETS
SELECT CustomerId, stockCode, sum(Quantity) FROM dfNoNull
GROUP BY customerId, stockCode GROUPING SETS((customerId, stockCode))
ORDER BY CustomerId DESC, stockCode DESC

-- but what if you also want to include the total number of items, regardless of customer or stock code
SELECT CustomerId, stockCode, sum(Quantity) FROM dfNoNull
GROUP BY customerId, stockCode GROUPING SETS((customerId, stockCode),())
ORDER BY CustomerId DESC, stockCode DESC
````

NOTE: GROUPING SETS are available in SQL only. For DataFrames we will need to use `rollups` and `cube`.

Another Example

````python
+-------+--------+-----+
|Country| Product|Sales|
+-------+--------+-----+
|    USA|ProductA|  100|
|    USA|ProductB|  150|
| Canada|ProductA|  200|
| Canada|ProductB|  250|
| Mexico|ProductA|  300|
+-------+--------+-----+
df.createOrReplaceTempView("sales")
result = spark.sql("""
SELECT Country, Product, SUM(Sales) as TotalSales
FROM sales
GROUP BY
    GROUPING SETS (
        (Country),
        (Product),
        (Country, Product),
        ()
    )
ORDER BY Country, Product
""")
result.show()
+-------+--------+-----------+
|Country| Product| TotalSales|
+-------+--------+-----------+
| Canada|    null|        450|
| Canada|ProductA|        200|
| Canada|ProductB|        250|
| Mexico|    null|        300|
| Mexico|ProductA|        300|
|    USA|    null|        250|
|    USA|ProductA|        100|
|    USA|ProductB|        150|
|   null|    null|       1000|
|   null|ProductA|        600|
|   null|ProductB|        400|
+-------+--------+-----------+
````

### Rollups

- A rollup is a multidimensional aggregation that performs a variety of group-by style calculations for us.
- create a rollup that looks across time (with our new `Date` column) and space (with the `Country` column) and creates a new DataFrame that includes the grand total over  all dates, the grand total for each date in the DataFrame, and the  subtotal for each country on each date in the DataFrame

````python
rolledUpDF = dfNoNull.rollup("Date", "Country").agg(sum("Quantity"))\
  .selectExpr("Date", "Country", "`sum(Quantity)` as total_quantity")\
  .orderBy("Date")
rolledUpDF.show()

+----------+--------------+--------------+
|      Date|       Country|total_quantity|
+----------+--------------+--------------+
|      null|          null|       5176450|
|2010-12-01|United Kingdom|         23949|
|2010-12-01|       Germany|           117|
|2010-12-01|        France|           449|
...
|2010-12-03|        France|           239|
|2010-12-03|         Italy|           164|
|2010-12-03|       Belgium|           528|
+----------+--------------+--------------+

# A null in both rollup columns specifies the grand total across both of those columns
````

### Cube

- A cube takes the rollup to a level deeper. Rather than treating elements  hierarchically, a cube does the same thing across all dimensions. This  means that it won’t just go by date over the entire time period, but  also the country.

- To put in question : 

  - The total across all dates and countries
  - The total for each date across all countries
  - The total for each country on each date
  - The total for each country across all dates

  ````python
  from pyspark.sql.functions import sum
  
  dfNoNull.cube("Date", "Country").agg(sum(col("Quantity")))\
    .select("Date", "Country", "sum(Quantity)").orderBy("Date").show()
  
  +----+--------------------+-------------+
  |Date|             Country|sum(Quantity)|
  +----+--------------------+-------------+
  |null|               Japan|        25218|
  |null|            Portugal|        16180|
  |null|         Unspecified|         3300|
  |null|                null|      5176450|
  |null|           Australia|        83653|
  ...
  |null|              Norway|        19247|
  |null|           Hong Kong|         4769|
  |null|               Spain|        26824|
  |null|      Czech Republic|          592|
  +----+--------------------+-------------+
  ````

### Grouping Metadata

Sometimes when using cubes and rollups, you want to be able to query the  aggregation levels so that you can easily filter them down accordingly.  We can do this by using the `grouping_id`, which gives us a column specifying the level of aggregation that we have in our result set.

| Grouping ID | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| 3           | This will appear for the highest-level aggregation, which will gives us the total quantity regardless of `customerId` and `stockCode`. |
| 2           | This will appear for all aggregations of individual stock codes. This gives  us the total quantity per stock code, regardless of customer. |
| 1           | This will give us the total quantity on a per-customer basis, regardless of item purchased. |
| 0           | This will give us the total quantity for individual `customerId` and `stockCode` combinations. |

### Pivot

- pivots makes it possible for you to convert a row into a column. We can then aggregate according to some function for each of those given countries and then display them

````python
Original DataFrame:
+-------+--------+-----+
|Country| Product|Sales|
+-------+--------+-----+
|    USA|ProductA|  100|
|    USA|ProductB|  150|
| Canada|ProductA|  200|
| Canada|ProductB|  250|
| Mexico|ProductA|  300|
|    USA|ProductA|  200|
| Canada|ProductA|  300|
+-------+--------+-----+

pivot_df = df.groupBy("Country").pivot("Product").agg(sum("Sales"))

Pivoted DataFrame:
+-------+--------+--------+
|Country|ProductA|ProductB|
+-------+--------+--------+
| Canada|     500|     250|
|    USA|     300|     150|
| Mexico|     300|    null|
+-------+--------+--------+
````

## User-Defined Aggregation Functions

- UDAFs are a way for users to define their own aggregation functions based on custom formulae or business rules.
- Spark maintains a single `AggregationBuffer` to store intermediate results for every group of input data.
- To create a UDAF, you must inherit from the `UserDefinedAggregateFunction` base class and implement the following methods:
  - `inputSchema` represents input arguments as a `StructType`
  - `bufferSchema` represents intermediate UDAF results as a `StructType`
  - `dataType` represents the return `DataType`
  - `deterministic` is a Boolean value that specifies whether this UDAF will return the same result for a given input
  - `initialize` allows you to initialize values of an aggregation buffer
  - `update` describes how you should update the internal buffer based on a given row
  - `merge` describes how two aggregation buffers should be merged
  - `evaluate` will generate the final result of the aggregation
- Currently only available in Scala or Java

---

## File: pyspark/notes/ch8.md

# Joins

A *join* brings together two sets of data, the left and right, by comparing the values of one or more keys of the left and right and evaluaating the result of a *join expression* that determines whether Spark should bring together the left side of data with right side of data.

- The most common join expression, an `equi-join`, compares  whether the specified keys in your left and right datasets are equal. If they are equal, Spark will combine the left and right datasets.

## Join Types

- join expression define two rows should join or not
- join type determines what should be in result set

Types of Join

- Inner joins (keep rows with keys that exist in the left and right datasets)
- Outer joins (keep rows with keys in either the left or right datasets)
- Left outer joins (keep rows with keys in the left dataset)
- Right outer joins (keep rows with keys in the right dataset)
- Left semi joins (keep the rows in the left, and only the left, dataset where the key appears in the right dataset)
- Left anti joins (keep the rows in the left, and only the left, dataset where they do not appear in the right dataset)
- Natural joins (perform a join by implicitly matching the columns between the two datasets with the same names)
- Cross (or Cartesian) joins (match every row in the left dataset with every row in the right dataset)

````python
person = spark.createDataFrame([
    (0, "Bill Chambers", 0, [100]),
    (1, "Matei Zaharia", 1, [500, 250, 100]),
    (2, "Michael Armbrust", 1, [250, 100])])\
  .toDF("id", "name", "graduate_program", "spark_status")
graduateProgram = spark.createDataFrame([
    (0, "Masters", "School of Information", "UC Berkeley"),
    (2, "Masters", "EECS", "UC Berkeley"),
    (1, "Ph.D.", "EECS", "UC Berkeley")])\
  .toDF("id", "degree", "department", "school")
sparkStatus = spark.createDataFrame([
    (500, "Vice President"),
    (250, "PMC Member"),
    (100, "Contributor")])\
  .toDF("id", "status")

person.createOrReplaceTempView("person")
graduateProgram.createOrReplaceTempView("graduateProgram")
sparkStatus.createOrReplaceTempView("sparkStatus")
````

````python
Person DataFrame:
+---+----------------+----------------+-------------+
| id|            name|graduate_program| spark_status|
+---+----------------+----------------+-------------+
|  0|   Bill Chambers|               0|        [100]|
|  1|   Matei Zaharia|               1|[500, 250, 100]|
|  2|Michael Armbrust|               1|    [250, 100]|
+---+----------------+----------------+-------------+
Graduate Program DataFrame:
+---+-------+--------------------+-----------+
| id| degree|          department|     school|
+---+-------+--------------------+-----------+
|  0|Masters|School of Informa...|UC Berkeley|
|  2|Masters|                EECS|UC Berkeley|
|  1|  Ph.D.|                EECS|UC Berkeley|
+---+-------+--------------------+-----------+
Spark Status DataFrame:
+---+--------------+
| id|        status|
+---+--------------+
|500|Vice President|
|250|    PMC Member|
|100|    Contributor|
+---+--------------+
````

## Inner Joins

````python
joinExpression = person["graduate_program"] == graduateProgram['id']

# Keys that do not exist in both DataFrames will not show in the resulting DataFrame.
wrongJoinExpression = person["name"] == graduateProgram["school"]

# default join - inner join
person.join(graduateProgram, joinExpression).show()
+---+----------------+----------------+---------------+---+-------+----------+---
| id|            name|graduate_program|   spark_status| id| degree|department|...
+---+----------------+----------------+---------------+---+-------+----------+---
|  0|   Bill Chambers|               0|          [100]|  0|Masters| School...|...
|  1|   Matei Zaharia|               1|[500, 250, 100]|  1|  Ph.D.|      EECS|...
|  2|Michael Armbrust|               1|     [250, 100]|  1|  Ph.D.|      EECS|...
+---+----------------+----------------+---------------+---+-------+----------+---

joinType = "inner"
person.join(graduateProgram, joinExpression, joinType).show()
````

## Outer Joins

- evaluate keys in both of the DataFrames or tables and includes (and joins together) the rows that evaluate to true or false. If there is no equivalent row in either left or right data frame, Spark will insert `null`.

````python
joinType = "outer"
person.join(graduateProgram, joinExpression, joinType).show()

+----+----------------+----------------+---------------+---+-------+-------------
|  id|            name|graduate_program|   spark_status| id| degree| departmen...
+----+----------------+----------------+---------------+---+-------+-------------
|   1|   Matei Zaharia|               1|[500, 250, 100]|  1|  Ph.D.|       EEC...
|   2|Michael Armbrust|               1|     [250, 100]|  1|  Ph.D.|       EEC...
|null|            null|            null|           null|  2|Masters|       EEC...
|   0|   Bill Chambers|               0|          [100]|  0|Masters|    School...
+----+----------------+----------------+---------------+---+-------+-------------
````

## Left Outer Joins

Left outer joins evaluate the keys in both of the DataFrames or tables and includes all rows from the left DataFrame as well as any rows in the right DataFrame that have a match in the left DataFrame. If there is no  equivalent row in the right DataFrame, Spark will insert `null`

````python
joinType = "left_outer"
graduateProgram.join(person, joinExpression, joinType).show()

+---+-------+----------+-----------+----+----------------+----------------+---
| id| degree|department|     school|  id|            name|graduate_program|...
+---+-------+----------+-----------+----+----------------+----------------+---
|  0|Masters| School...|UC Berkeley|   0|   Bill Chambers|               0|...
|  2|Masters|      EECS|UC Berkeley|null|            null|            null|...
|  1|  Ph.D.|      EECS|UC Berkeley|   2|Michael Armbrust|               1|...
|  1|  Ph.D.|      EECS|UC Berkeley|   1|   Matei Zaharia|               1|...
+---+-------+----------+-----------+----+----------------+----------------+---
````

## Right Outer Joins

Right outer joins evaluate the keys in both of the DataFrames or tables and  includes all rows from the right DataFrame as well as any rows in the  left DataFrame that have a match in the right DataFrame. If there is no  equivalent row in the left DataFrame, Spark will insert `null`

````python
joinType = "right_outer"
person.join(graduateProgram, joinExpression, joinType).show()

+----+----------------+----------------+---------------+---+-------+------------+
|  id|            name|graduate_program|   spark_status| id| degree|  department|
+----+----------------+----------------+---------------+---+-------+------------+
|   0|   Bill Chambers|               0|          [100]|  0|Masters|School of...|
|null|            null|            null|           null|  2|Masters|        EECS|
|   2|Michael Armbrust|               1|     [250, 100]|  1|  Ph.D.|        EECS|
|   1|   Matei Zaharia|               1|[500, 250, 100]|  1|  Ph.D.|        EECS|
+----+----------------+----------------+---------------+---+-------+------------+
````

## Left Semi Joins

- left semi joins do not actually include any values from the right DataFrame.
- They only compare to see if values exist in second DataFrame. If values does exist, those rows will be kept in result, even if there are duplicate keys in the left DataFrame.

````python
joinType = "left_semi"
graduateProgram.join(person, joinExpression, joinType).show()

+---+-------+--------------------+-----------+
| id| degree|          department|     school|
+---+-------+--------------------+-----------+
|  0|Masters|School of Informa...|UC Berkeley|
|  1|  Ph.D.|                EECS|UC Berkeley|
+---+-------+--------------------+-----------+
````

````python
gradProgram2 = graduateProgram.union(spark.createDataFrame([
    (0, "Masters", "Duplicated Row", "Duplicated School")]))

gradProgram2.createOrReplaceTempView("gradProgram2")
gradProgram2.join(person, joinExpression, joinType).show()

+---+-------+--------------------+-----------------+
| id| degree|          department|           school|
+---+-------+--------------------+-----------------+
|  0|Masters|School of Informa...|      UC Berkeley|
|  1|  Ph.D.|                EECS|      UC Berkeley|
|  0|Masters|      Duplicated Row|Duplicated School|
+---+-------+--------------------+-----------------+
````

## Left Anti Joins

- opposite of left semi joins, like left semi joins they do not include any values from the right Dataframe.
- They only compare values to see if the value exists in the second  DataFrame. However, rather than keeping the values that exist in the  second DataFrame, they keep only the values that *do not* have a corresponding key in the second DataFrame.

````python
joinType = "left_anti"
graduateProgram.join(person, joinExpression, joinType).show()

+---+-------+----------+-----------+
| id| degree|department|     school|
+---+-------+----------+-----------+
|  2|Masters|      EECS|UC Berkeley|
+---+-------+----------+-----------+
````

## Natural Joins

Natural joins make implicit guesses at the columns on which you would like to  join. It finds matching columns and returns the results. Left, right,  and outer natural joins are all supported.

## Cross (Catesian) Joins

- The last of our joins are cross-joins or *cartesian products*. Cross-joins in simplest terms are inner joins that do not specify a predicate. Cross joins will join every single row in the left DataFrame to ever single row in the right DataFrame.
- This will cause an absolute explosion in the number of rows contained in the resulting DataFrame. If you have 1,000 rows in each DataFrame, the  cross-join of these will result in 1,000,000 (1,000 x 1,000) rows.

````python
joinType = "cross"
graduateProgram.join(person, joinExpression, joinType).show()

+---+-------+----------+-----------+---+----------------+----------------+-------
| id| degree|department|     school| id|            name|graduate_program|spar...
+---+-------+----------+-----------+---+----------------+----------------+-------
|  0|Masters| School...|UC Berkeley|  0|   Bill Chambers|               0|    ...
|  1|  Ph.D.|      EECS|UC Berkeley|  2|Michael Armbrust|               1|  [2...
|  1|  Ph.D.|      EECS|UC Berkeley|  1|   Matei Zaharia|               1|[500...
+---+-------+----------+-----------+---+----------------+----------------+-------
````

## Challanges When Using Joins

### Join on Complex Types

Even though this might seem like a challenge, it’s actually not. Any  expression is a valid join expression, assuming that it returns a  Boolean:

````python
from pyspark.sql.functions import expr

person.withColumnRenamed("id", "personId")\
  .join(sparkStatus, expr("array_contains(spark_status, id)")).show()

+--------+----------------+----------------+---------------+---+--------------+
|personId|            name|graduate_program|   spark_status| id|        status|
+--------+----------------+----------------+---------------+---+--------------+
|       0|   Bill Chambers|               0|          [100]|100|   Contributor|
|       1|   Matei Zaharia|               1|[500, 250, 100]|500|Vice President|
|       1|   Matei Zaharia|               1|[500, 250, 100]|250|    PMC Member|
|       1|   Matei Zaharia|               1|[500, 250, 100]|100|   Contributor|
|       2|Michael Armbrust|               1|     [250, 100]|250|    PMC Member|
|       2|Michael Armbrust|               1|     [250, 100]|100|   Contributor|
+--------+----------------+----------------+---------------+---+--------------+
````

### Handling Duplicate Column Names

One of the tricky things that come up in joins is dealing with duplicate column names in your results DataFrame.

In a DataFrame, each column has a unique ID within Spark’s SQL Engine,  Catalyst. This unique ID is purely internal and not something that you  can directly reference. This makes it quite difficult to refer to a  specific column when you have a DataFrame with duplicate column names.

This can occur in two distinct situations:

- The join expression that you specify does not remove one key from one of the input DataFrames and the keys have the same column name
- Two columns on which you are not performing the join have the same name

````python
gradProgramDupe = graduateProgram.withColumnRenamed("id", "graduate_program")
joinExpr = gradProgramDupe.col("graduate_program") == person.col(
  "graduate_program")

person.join(gradProgramDupe, joinExpr).show()
person.join(gradProgramDupe, joinExpr).select("graduate_program").show()

# we will get following error
org.apache.spark.sql.AnalysisException: Reference 'graduate_program' is
ambiguous, could be: graduate_program#40, graduate_program#1079.
````

#### Approach 1: Different Join Expression

When you have two keys that have the same name, probably the easiest fix is to change the join expression from a Boolean expression to a string or sequence. This automatically removes one of the columns for you during the join:

````python
person.join(gradProgramDupe,"graduate_program").select("graduate_program").show()
````

#### Approach 2: Dropping the column after the join

Another approach is to drop the offending column after the join.

````python
person.join(gradProgramDupe, joinExpr).drop(person.col("graduate_program"))
  .select("graduate_program").show()
````

#### Approach 3: Renaming a column before the join

````python
val gradProgram3 = graduateProgram.withColumnRenamed("id", "grad_id")
val joinExpr = person.col("graduate_program") === gradProgram3.col("grad_id")
person.join(gradProgram3, joinExpr).show()
````

## How Spark Performs Joins

To understand how Spark performs joins, you need to understand the two core resources at play: the *node-to-node communication strategy* and *per node computation strategy*.

### Communication Strategies

Spark approaches cluster communication in two different ways during joins. It either incurs a *shuffle join*, which results in an all-to-all communication or a *broadcast join*

The core foundation of our simplified view of joins is that in Spark you will have either a big table or a small table. Although this is  obviously a spectrum (and things do happen differently if you have a  “medium-sized table”), it can help to be binary about the distinction  for the sake of this explanation.

#### Big table-to-big table

When you join a big table to another big table, you end up with a shuffle join. In a shuffle join, every node talks to every other node and they share  data according to which node has a certain key or set of keys (on which  you are joining). These joins are expensive because the network can  become congested with traffic, especially if your data is not partitioned well.

#### Big table-to-small table

When the table is small enough to fit into the memory of a single worker node, with some breathing room of course, we can optimize our join.  Although we can use a big table–to–big table communication strategy, it  can often be more efficient to use a broadcast join.

What this means is that we will replicate our small DataFrame onto every worker node in the cluster. Even tho it sounds expensive it save communication overhead during entire join. Which is performed once in the beginning and then let each individual worker node perform the work without having to wait or communicate with any other worker node.

#### Little table–to–little table

When performing joins with small tables, it’s usually best to let  Spark decide how to join them. You can always force a broadcast join if  you’re noticing strange behavior.

---

## File: pyspark/notes/ch9.md

# Data Sources

- goal here is to give ability to read and write from Spark’s core data sources and know enough to understand what you should look for when integrating third-party data sources like Cassandra, Hbase, MongoDB, AWS Redshift, XML, etc.


## The Structure of the Data Sources API

#### Read API Structure

````python
DataFrameReader.format(...).option("key", "value").schema(...).load()
````

- NOTE: `format` is optional because by default Spark will use the Parquet format. `schema` is also optional and by default its inferred.

### Basics of Reading Data

- foundation of reading data in spark is `DataFrameReader`. We can access this through `SparkSession` via the `read` attribute.

````python
spark.read
````

````python
# Example of overall read layout
spark.read.format("csv")
  .option("mode", "FAILFAST")
  .option("inferSchema", "true")
  .option("path", "path/to/file(s)")
  .schema(someSchema)
  .load()
````

#### Read Modes

| Read mode       | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `permissive`    | Sets all fields to `null` when it encounters a corrupted record and places all corrupted records in a string column called `_corrupt_record` |
| `dropMalformed` | Drops the row that contains malformed records                |
| `failFast`      | Fails immediately upon encountering malformed records        |

#### Write API Structure

````python
DataFrameWriter.format(...).option(...).partitionBy(...).bucketBy(...).sortBy(
  ...).save()
````

### Basics of Writing Data

````python
dataFrame.write
# 
dataframe.write.format("csv")
  .option("mode", "OVERWRITE")
  .option("dateFormat", "yyyy-MM-dd")
  .option("path", "path/to/file(s)")
  .save()
````

#### Save Modes

| `append`        | Appends the output files to the list of files that already exist at that location |
| --------------- | ------------------------------------------------------------ |
| `overwrite`     | Will completely overwrite any data that already exists there |
| `errorIfExists` | Throws an error and fails the write if data or files already exist at the specified location (default) |
| `ignore`        | If data or files exist at the location, do nothing with the current DataFrame |

## CSV Files

CSV stands for comma-separated values. Each line represents a single record, and commas separate each field within a record.

### CSV Options

| Read/write | Key                           | Potential values                                             | Default                     | Description                                                  |
| ---------- | ----------------------------- | ------------------------------------------------------------ | --------------------------- | ------------------------------------------------------------ |
| Both       | `sep`                         | Any single string character                                  | ,                           | The single character that is used as separator for each field and value. |
| Both       | `header`                      | `true`, `false`                                              | `false`                     | A Boolean flag that declares whether the first line in the file(s) are the names of the columns. |
| Read       | `escape`                      | Any string character                                         | \                           | The character Spark should use to escape other characters in the file. |
| Read       | `inferSchema`                 | `true`, `false`                                              | `false`                     | Specifies whether Spark should infer column types when reading the file. |
| Read       | `ignoreLeadingWhiteSpace`     | `true`, `false`                                              | `false`                     | Declares whether leading spaces from values being read should be skipped. |
| Read       | `ignoreTrailingWhiteSpace`    | `true`, `false`                                              | `false`                     | Declares whether trailing spaces from values being read should be skipped. |
| Both       | `nullValue`                   | Any string character                                         | “”                          | Declares what character represents a `null` value in the file. |
| Both       | `nanValue`                    | Any string character                                         | NaN                         | Declares what character represents a NaN or missing character in the CSV file. |
| Both       | `positiveInf`                 | Any string or character                                      | Inf                         | Declares what character(s) represent a positive infinite value. |
| Both       | `negativeInf`                 | Any string or character                                      | -Inf                        | Declares what character(s) represent a negative infinite value. |
| Both       | `compression` or `codec`      | None, `uncompressed`, `bzip2`, `deflate`, `gzip`, `lz4`, or `snappy` | none                        | Declares what compression codec Spark should use to read or write the file. |
| Both       | `dateFormat`                  | Any string or character that conforms to java’s `SimpleDataFormat`. | yyyy-MM-dd                  | Declares the date format for any columns that are date type. |
| Both       | `timestampFormat`             | Any string or character that conforms to java’s `SimpleDataFormat`. | yyyy-MM-dd’T’HH:mm:ss.SSSZZ | Declares the timestamp format for any columns that are timestamp type. |
| Read       | `maxColumns`                  | Any integer                                                  | 20480                       | Declares the maximum number of columns in the file.          |
| Read       | `maxCharsPerColumn`           | Any integer                                                  | 1000000                     | Declares the maximum number of characters in a column.       |
| Read       | `escapeQuotes`                | `true`, `false`                                              | `true`                      | Declares whether Spark should escape quotes that are found in lines. |
| Read       | `maxMalformedLogPerPartition` | Any integer                                                  | 10                          | Sets the maximum number of malformed rows Spark will log for each partition. Malformed records beyond this number will be ignored. |
| Write      | `quoteAll`                    | `true`, `false`                                              | `false`                     | Specifies whether all values should be enclosed in quotes, as opposed to just escaping values that have a quote character. |
| Read       | `multiLine`                   | `true`, `false`                                              | `false`                     | This option allows you to read multiline CSV files where each logical row in the CSV file might span multiple rows in the file itself. |

### Reading/Writing CSV Files

````python
# Reading
csvFile = spark.read.format("csv")\
  .option("header", "true")\
  .option("mode", "FAILFAST")\
  .option("inferSchema", "true")\
  .load("/data/flight-data/csv/2010-summary.csv")

# writing
csvFile.write.format("csv").mode("overwrite").option("sep", "\t")\
  .save("/tmp/my-tsv-file.tsv")
````

## JSON Files

- JSON stands for JavaScript Object Notation
- In Spark, when we refer to JSON files, we refer to *line-delimited* JSON files. This contrasts with files that have a large JSON object or array per file.
- The line-delimited versus multiline trade-off is controlled by a single option: `multiLine`. When you set this option to `true`, you can read an entire file as one `json` object and Spark will go through the work of parsing that into a  DataFrame. Line-delimited JSON is actually a much more stable format  because it allows you to append to a file with a new record (rather than having to read in an entire file and then write it out), which is what  we recommend that you use.

| Read/write | Key                                  | Potential values                                             | Default                                         | Description                                                  |
| ---------- | ------------------------------------ | ------------------------------------------------------------ | ----------------------------------------------- | ------------------------------------------------------------ |
| Both       | `compression` or `codec`             | None, `uncompressed`, `bzip2`, `deflate`, `gzip`, `lz4`, or `snappy` | none                                            | Declares what compression codec Spark should use to read or write the file. |
| Both       | `dateFormat`                         | Any string or character that conforms to Java’s `SimpleDataFormat`. | yyyy-MM-dd                                      | Declares the date format for any columns that are date type. |
| Both       | `timestampFormat`                    | Any string or character that conforms to Java’s `SimpleDataFormat`. | yyyy-MM-dd’T’HH:mm:ss.SSSZZ                     | Declares the timestamp format for any columns that are timestamp type. |
| Read       | `primitiveAsString`                  | `true`, `false`                                              | `false`                                         | Infers all primitive values as string type.                  |
| Read       | `allowComments`                      | `true`, `false`                                              | `false`                                         | Ignores Java/C++ style comment in JSON records.              |
| Read       | `allowUnquotedFieldNames`            | `true`, `false`                                              | `false`                                         | Allows unquoted JSON field names.                            |
| Read       | `allowSingleQuotes`                  | `true`, `false`                                              | `true`                                          | Allows single quotes in addition to double quotes.           |
| Read       | `allowNumericLeadingZeros`           | `true`, `false`                                              | `false`                                         | Allows leading zeroes in numbers (e.g., 00012).              |
| Read       | `allowBackslashEscapingAnyCharacter` | `true`, `false`                                              | `false`                                         | Allows accepting quoting of all characters using backslash quoting mechanism. |
| Read       | `columnNameOfCorruptRecord`          | Any string                                                   | Value of `spark.sql.column&NameOfCorruptRecord` | Allows renaming the new field having a malformed string created by `permissive` mode. This will override the configuration value. |
| Read       | `multiLine`                          | `true`, `false`                                              | `false`                                         | Allows for reading in non-line-delimited JSON files.         |

````python
spark.read.format("json").option("mode", "FAILFAST")\
  .option("inferSchema", "true")\
  .load("/data/flight-data/json/2010-summary.json").show(5)

csvFile.write.format("json").mode("overwrite").save("/tmp/my-json-file.json")
````

## Parquet Files

- Parquet is an open source column-oriented data store that provides a variety of storage optimizations, especially for analytics workloads. It provides columnar compression, which saves storage space and allows for reading individual columns instead of entire files
- It is a file format that works exceptionally well with Apache Spark and  is in fact the default file format. It is recommended writing data out to Parquet for long-term storage because reading from a Parquet file will always be more efficient than JSON or CSV.
- Another advantage of Parquet is that it supports complex types

| Read/Write | Key                      | Potential Values                                             | Default                                                    | Description                                                  |
| ---------- | ------------------------ | ------------------------------------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------------ |
| Write      | `compression` or `codec` | None, `uncompressed`, `bzip2`, `deflate`, `gzip`, `lz4`, or `snappy` | None                                                       | Declares what compression codec Spark should use to read or write the file. |
| Read       | `mergeSchema`            | `true`, `false`                                              | Value of the configuration `spark.sql.parquet.mergeSchema` | You can incrementally add columns to newly written Parquet files in the  same table/folder. Use this option to enable or disable this feature. |

````python
spark.read.format("parquet")\
  .load("/data/flight-data/parquet/2010-summary.parquet").show(5)

csvFile.write.format("parquet").mode("overwrite")\
  .save("/tmp/my-parquet-file.parquet")
````

## ORC Files

ORC is self-describing, type-aware columnar file format designed for Hadoop workloads. It is optmized for large streaming reads but with integrated support for finding rows quickly.

ORC actually has no options for reading in data because Spark understands the file format quite well.

````python
spark.read.format("orc").load("/data/flight-data/orc/2010-summary.orc").show(5)

csvFile.write.format("orc").mode("overwrite").save("/tmp/my-json-file.orc")
````

## SQL Databases

- SQL datasources are one of the more powerful connectors because there are variety of systems to which we can connect to.
- We can even connect to SQLite
- To read and write from these databases, you need to do two things: include the Java Database Connectivity (JDBC) driver for you particular  database on the spark classpath, and provide the proper JAR for the  driver itself. For example, to be able to read and write from  PostgreSQL, you might run something like this:

````bash
./bin/spark-shell \
--driver-class-path postgresql-9.4.1207.jar \
--jars postgresql-9.4.1207.jar
````

| Property Name                                 | Meaning                                                      |
| --------------------------------------------- | ------------------------------------------------------------ |
| `url`                                         | The JDBC URL to which to connect. The source-specific connection properties can be specified in the URL; for example, *jdbc:postgresql://localhost/test?user=fred&password=secret*. |
| `dbtable`                                     | The JDBC table to read. Note that anything that is valid in a FROM clause  of a SQL query can be used. For example, instead of a full table you  could also use a subquery in parentheses. |
| `driver`                                      | The class name of the JDBC driver to use to connect to this URL. |
| `partitionColumn`, `lowerBound`, `upperBound` | If any one of these options is specified, then all others must be set as well. In addition, `numPartitions` must be specified. These properties describe how to partition the table when reading in parallel from multiple workers. `partitionColumn` must be a numeric column from the table in question. Notice that `lowerBound` and `upperBound` are used only to decide the partition stride, not for filtering the  rows in the table. Thus, all rows in the table will be partitioned and  returned. This option applies only to reading. |
| `numPartitions`                               | The maximum number of partitions that can be used for parallelism in table  reading and writing. This also determines the maximum number of  concurrent JDBC connections. If the number of partitions to write  exceeds this limit, we decrease it to this limit by calling `coalesce(numPartitions)` before writing. |
| `fetchsize`                                   | The JDBC fetch size, which determines how many rows to fetch per round  trip. This can help performance on JDBC drivers, which default to low  fetch size (e.g., Oracle with 10 rows). This option applies only to  reading. |
| `batchsize`                                   | The JDBC batch size, which determines how many rows to insert per round  trip. This can help performance on JDBC drivers. This option applies  only to writing. The default is 1000. |
| `isolationLevel`                              | The transaction isolation level, which applies to current connection. It can be one of `NONE`, `READ_COMMITTED`, `READ_UNCOMMITTED`, `REPEATABLE_READ`, or `SERIALIZABLE`, corresponding to standard transaction isolation levels defined by JDBC’s `Connection` object. The default is `READ_UNCOMMITTED`. This option applies only to writing. For more information, refer to the documentation in java.sql.Connection. |
| `truncate`                                    | This is a JDBC writer-related option. When `SaveMode.Overwrite` is enabled, Spark truncates an existing table instead of dropping and  re-creating it. This can be more efficient, and it prevents the table  metadata (e.g., indices) from being removed. However, it will not work  in some cases, such as when the new data has a different schema. The  default is `false`. This option applies only to writing. |
| `createTableOptions`                          | This is a JDBC writer-related option. If specified, this option allows  setting of database-specific table and partition options when creating a table (e.g., CREATE TABLE t (*name string*) ENGINE=InnoDB). This option applies only to writing. |
| `createTableColumnTypes`                      | The database column data types to use instead of the defaults, when  creating the table. Data type information should be specified in the  same format as CREATE TABLE columns syntax (e.g., “name CHAR(64),  comments VARCHAR(1024)”). The specified types should be valid Spark SQL  data types. This option applies only to writing. |

### Reading from SQL Database

````python
driver = "org.sqlite.JDBC"
path = "/data/flight-data/jdbc/my-sqlite.db"
url = "jdbc:sqlite:" + path
tablename = "flight_info"
````

After defining connection property we can test database connection.

````python
import java.sql.DriverManager
val connection = DriverManager.getConnection(url)
connection.isClosed()
connection.close()
````

````python
# SQLite
dbDataFrame = spark.read.format("jdbc").option("url", url)\
  .option("dbtable", tablename).option("driver",  driver).load()

# Postgres
pgDF = spark.read.format("jdbc")\
  .option("driver", "org.postgresql.Driver")\
  .option("url", "jdbc:postgresql://database_server")\
  .option("dbtable", "schema.tablename")\
  .option("user", "username").option("password", "my-secret-password").load()
````

### Query Pushdown

- Spark makes a best-effort attempt to filter data in the database itself before creating the DataFrame

```python
dbDataFrame.select("DEST_COUNTRY_NAME").distinct().explain
== Physical Plan ==
*HashAggregate(keys=[DEST_COUNTRY_NAME#8108], functions=[])
+- Exchange hashpartitioning(DEST_COUNTRY_NAME#8108, 200)
   +- *HashAggregate(keys=[DEST_COUNTRY_NAME#8108], functions=[])
      +- *Scan JDBCRelation(flight_info) [numPartitions=1] ...
```

- Spark can do better than this on certain queries. if we specify a filter on out DF, Spark will push that filter down into database

```python
dbDataFrame.filter("DEST_COUNTRY_NAME in ('Anguilla', 'Sweden')").explain()

== Physical Plan ==
*Scan JDBCRel... PushedFilters: [*In(DEST_COUNTRY_NAME, [Anguilla,Sweden])],
...
```

Spark can’t translate all of its own functions into the functions available in the SQL database in which you’re working. Therefore, sometimes you’re going to want to pass an entire query into your SQL that will return the results as a DataFrame.

````python
# in Python
pushdownQuery = """(SELECT DISTINCT(DEST_COUNTRY_NAME) FROM flight_info)
  AS flight_info"""
dbDataFrame = spark.read.format("jdbc")\
  .option("url", url).option("dbtable", pushdownQuery).option("driver",  driver)\
  .load()
````

#### Reading from databases in parallel

- spark has an underlying algorithm that can read multiple files into one partition or conversly depending onthe file size and splittability of file type and compression.
- same flexibility exists with files, SQL databases, defining partition numbers allows you to limit read/write parallel capacity.

````python
dbDataFrame = spark.read.format("jdbc")\
  .option("url", url).option("dbtable", tablename).option("driver",  driver)\
  .option("numPartitions", 10).load()

# this will still be 1 partition as there is not enough data
dbDataFrame.select("DEST_COUNTRY_NAME").distinct().show()
````

- We can explicitly push predicates down into SQL databases through the  connection itself. This optimization allows you to control the physical  location of certain data in certain partitions by specifying predicates

````python
props = {"driver":"org.sqlite.JDBC"}
predicates = [
  "DEST_COUNTRY_NAME = 'Sweden' OR ORIGIN_COUNTRY_NAME = 'Sweden'",
  "DEST_COUNTRY_NAME = 'Anguilla' OR ORIGIN_COUNTRY_NAME = 'Anguilla'"]
spark.read.jdbc(url, tablename, predicates=predicates, properties=props).show()
spark.read.jdbc(url,tablename,predicates=predicates,properties=props)\
  .rdd.getNumPartitions() # 2
````

If you specify predicates that are not disjoint, you can end up with lots of duplicate rows.

#### Partitioning based on a sliding window

- partition based on predicates

````python
colName = "count"
lowerBound = 0L
upperBound = 348113L # this is the max count in our database
numPartitions = 10

spark.read.jdbc(url, tablename, column=colName, properties=props,
                lowerBound=lowerBound, upperBound=upperBound,
                numPartitions=numPartitions).count() # 255
````

### Writing to SQL Databases

````python
newPath = "jdbc:sqlite://tmp/my-sqlite.db"
csvFile.write.jdbc(newPath, tablename, mode="overwrite", properties=props)
````

## Text Files

- each line becomes a record in the DataFrame.
- suppose that you need to parse some Apache log files to some more  structured format, or perhaps you want to parse some plain text for  natural-language processing. Text files make a great argument for the  Dataset API due to its ability to take advantage of the flexibility of  native types.

````python
spark.read.textFile("/data/flight-data/csv/2010-summary.csv")
  .selectExpr("split(value, ',') as rows").show()

csvFile.select("DEST_COUNTRY_NAME").write.text("/tmp/simple-text-file.txt")

# if we are performing some partitioning when performing write, we can write more columns,
# However, those columns will manifest as directories in the folder to which you’re writing out to, instead of columns on every single file

csvFile.limit(10).select("DEST_COUNTRY_NAME", "count")\
  .write.partitionBy("count").text("/tmp/five-csv-files2py.csv")
````

## Advanced I/O Concepts

we can control the parallelism of files that we write by controlling the partitions prior to writing.

### Splittable File Types and Compression

- certain file formats are fundamentally splittable. Improves performance as Spark can avoid reading whole file and access the required parts of the file necessary for query.
- In conjuction with this is a need to manage compression. Not all compression schemes are splittable.
- Recommended is Parquet with gzip compression.

### Reading Data in Parallel

- multiple executors cannot read from same file at same time necessary but can read different files at the same time. When you read from a folder with multiple files in it, each of those files become partition in your dataFrame and be read in available executors in parallel.

### Writing Data in Parallel

- Number of files or data written is dependent on the number of partitions the DataFrame has at the time you write out the data.
- By default , one file is written per partition of the data.

````
csvFile.repartition(5).write.format("csv").save("/tmp/multiple.csv")

ls /tmp/multiple.csv

/tmp/multiple.csv/part-00000-767df509-ec97-4740-8e15-4e173d365a8b.csv
/tmp/multiple.csv/part-00001-767df509-ec97-4740-8e15-4e173d365a8b.csv
/tmp/multiple.csv/part-00002-767df509-ec97-4740-8e15-4e173d365a8b.csv
/tmp/multiple.csv/part-00003-767df509-ec97-4740-8e15-4e173d365a8b.csv
/tmp/multiple.csv/part-00004-767df509-ec97-4740-8e15-4e173d365a8b.csv
````

### Partition

Partitioning is a tool that allows you to control what data is stored as you write it. When you write a file to a partitioned directory (table), you basically encode a column as a folder.

This allows skip lots of data when we read it in later, allowing to read in only the data relevant to your problem instead of having to scan entire dataset.

````python
csvFile.limit(10).write.mode("overwrite").partitionBy("DEST_COUNTRY_NAME")\
  .save("/tmp/partitioned-files.parquet")

$ ls /tmp/partitioned-files.parquet

...
DEST_COUNTRY_NAME=Costa Rica/
DEST_COUNTRY_NAME=Egypt/
DEST_COUNTRY_NAME=Equatorial Guinea/
DEST_COUNTRY_NAME=Senegal/
DEST_COUNTRY_NAME=United States/
````

This is probably the lowest-hanging optimization that you can use when  you have a table that readers frequently filter by before manipulating.  For instance, date is particularly common for a partition because,  downstream, often we want to look at only the previous week’s data  (instead of scanning the entire list of records). This can provide  massive speedups for readers.

### Bucketing

- we can control the data that is specifically written to each file.
- This can avoid shuffles later when we read the data because data with the same bucket ID will be grouped together in one physical partition.
- This means that the data is prepartitioned according to how you expect  to use that data later on, meaning you can avoid expensive shuffles when joining or aggregating.
- Rather than partitioning on a specific column (which might write out a  ton of directories), it’s probably worthwhile to explore bucketing the  data instead. This will create a certain number of files and organize  our data into those “buckets”

`````scala
val numberBuckets = 10
val columnToBucketBy = "count"
csvFile.write.format("parquet").mode("overwrite")
  .bucketBy(numberBuckets, columnToBucketBy).saveAsTable("bucketedFiles")
  
  
$ ls /user/hive/warehouse/bucketedfiles/

part-00000-tid-1020575097626332666-8....parquet
part-00000-tid-1020575097626332666-8....parquet
part-00000-tid-1020575097626332666-8....parquet
...
`````

### Writing Complex Types

Although Spark can work with all of these types, not every single type  works well with every data file format. For instance, CSV files do not  support complex types, whereas Parquet and ORC do.

### Managing File Size

- Managing file sizes is an important factor not so much for writing data but reading it later on
- due to *small file problem* Spark, HDFS etc doesn’t do well. If file are too large then also things become inefficient
- we can use `maxRecordsPerFile` to optimize file sizes based on records size. `df.write.option("maxRecordsPerFile", 5000)` 

---

