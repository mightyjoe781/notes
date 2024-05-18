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
