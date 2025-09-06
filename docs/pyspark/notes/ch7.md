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