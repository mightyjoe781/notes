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