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