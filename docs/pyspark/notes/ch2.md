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

