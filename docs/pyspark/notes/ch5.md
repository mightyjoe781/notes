# Basic Structured Operations

DataFrame:

- consists of series of records that are of type `Row`
- columns represents a computation expression to be performed on rows
- *Schema* representing type of data in each column
- *Partitioning* of DataFrame defines the layout of the DataFrame or Dataset’s physical distribution across clusters.

## Schemas

- schema defines the column names and types of DataFrame.
- schema is a `StructType` made up of a number of fields, `StructFields` that have name, type and a Boolean representing nullability of the column.

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

- Columns are not *resolved* until we compare the column names with those we are maintaining in the *catalog*. Column and table resolution happens in the *analyzer* phase

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