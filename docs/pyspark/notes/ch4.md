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
