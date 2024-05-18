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