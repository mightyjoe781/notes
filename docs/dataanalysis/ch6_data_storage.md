# Data Loading, Storage, and File-Formats

## Reading and Writing Data in Text Format

| Functions        | Description                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------ |
| `read_csv`       | Load delimited data from a file, URL, or file-like objects, use comma as default delimiter |
| `read_fwf`       | Read data in fixed-width column format (i.e. no delimiters)                                |
| `read_clipboard` | Read from clipboard                                                                        |
| `read_hdf`       | Read HDF5 files written by pandas                                                          |
| `read_html`      | Read all table from a HTML page                                                            |
| `read_json`      | Read data from JSON                                                                        |
| `read_parquet`   | Read apache parquet binary file format                                                     |
| `read_pickle`    | Read an object stored by pandas using Python pickle format`                                |
| `read_sql`       | Read results of a SQL Query                                                                |
| `read_sql_query` | Read a whole SQL table using SQL Alchemy                                                   |
| `read_xml`       | Read data from XML file                                                                    |
Other important functions are : `read_stata` , `read_sas`, `read_spss`, `read_orc`, `read_feather`, etc.

Optional arguments for these fall in following catagories

- Indexing : Can treat one or more columns as the returned DataFrame, and whether to get column names from the file, arguments you provide, or not at all.
- Type inference and data conversion : Includes the user-defined value conversions and custom list of missing value markers
- Date and time parsing: Includes a combining capability, including combining date and time information spread over multiple columns into a single column in the result.
- Iterating: Support for iterating over chunks of very large files.
- Unclean data issues: Includes skipping rows or a footer, comments, or other minor things like numeric data with thousands separated by commas.

```bash
cat examples/ex1.csv

a,b,c,d,message
1,2,3,4,hello
5,6,7,8,world
9,10,11,12,foo
```

```python
df = pd.read_csv("ex1.csv")

## recreate above file without header and name ex2

# if header is not present in file
df = pd.read_csv("ex2.csv", header=None)

# adding custom header
df = pd.read_csv("ex2.csv", names=["a", "b", "c", "d", "message"])

## assigning message column as index of the df
names=["a", "b", "c", "d", "message"]
df = pd.read_csv("ex2.csv", names=names, index_col="message")
```

Hierarchical Indexing

```python
!cat examples/csv_mindex.csv
key1,key2,value1,value2
one,a,1,2
one,b,3,4
one,c,5,6
one,d,7,8
two,a,9,10
two,b,11,12
two,c,13,14
two,d,15,16

parsed = pd.read_csv("examples/csv_mindex.csv",
                     index_col=["key1", "key2"])


# --------------------------
           value1  value2
key1 key2                
one  a          1       2
     b          3       4
     c          5       6
     d          7       8
two  a          9      10
     b         11      12
     c         13      14
     d         15      16
```

If file is using some other delimiter

```python
!cat ex3.csv

A         B         C
aaa -0.264438 -1.026059 -0.619500
bbb  0.927272  0.302904 -0.032399
ccc -0.264273 -0.386314 -0.217601
ddd -0.871858 -0.348382  1.100491

# while space delimiter
df = pd.read_csv("examples/ex3.txt", sep="\s+")

# NOTE: as header contains 3 entries, pandas will treat first column as index

# skipping rows while reading files
pd.read_csv("examples/ex4.csv", skiprows=[0, 2, 3])


```

Handling Null values

```python
!cat ex5.csv
something,a,b,c,d,message
one,1,2,3,4,NA
two,5,6,,8,world
three,9,10,11,12,foo

# NOTE: By default pandas uses NAN for missing values while reading a file

# but to add additional strings for treated as NaN, use na_values
pd.read_csv("examples/ex5.csv", na_values=["NULL"])


# to disable default
pd.read_csv("examples/ex5.csv", keep_default_na=False)

## different sentinals can be defined for each column

sentinels = {"message": ["foo", "NA"], "something": ["two"]}

pd.read_csv("examples/ex5.csv", na_values=sentinels,
            keep_default_na=False)

```

Some important functions of read_csv : *delimiter, names, skip_rows, na_values, parse_dates, date_parser, chunk_size, skip_footer, etc.*

### Reading Text Files in Pieces

Panda's default display setting can be modified as 

```python
pd.options.display.max_rows = 10 # top5 and last5

# to avoid reading full file and few entries use nrows
pd.read_csv("examples/ex6.csv", nrows=5)

# to read in chunks using chunker
pd.read_csv("examples/ex6.csv", nrows=5)


```

### Writing Data to Text Format

```python
data.to_csv("examples/out.csv")

# using other delimiter but prints result to console rather than a file
import sys
data.to_csv(sys.stdout, sep="|")

# missing value representation
data.to_csv(sys.stdout, na_rep="NULL")

# by default both row and column labels are written to avoid that
data.to_csv(sys.stdout, index=False, header=False)

## writing a portion of df
data.to_csv(sys.stdout, index=False, columns=["a", "b", "c"])
```

### Working with Other Delimited Formats

Many a times a small preprocessing is required before using `read_csv`

Example file

```csv
"a","b","c"
"1","2","3"
"1","2","3"
```

```python
with open("ex7.csv") as f:
    lines = list(csv.reader(f))
    
    header, values = lines[0], lines[1:]
    
    data_dict = {h: v for h,v zip(*values)}
    
```

### JSON Data

- `json.loads` : convert json string to Python form
- `json.dumps` : converts Python object to JSON

```python
pd.read_json("examples/example.json")

```

## Binary Data Formats

Some of the most simple ways to store (*serialize*) data in binary format is using Python's built-in `pickle` module. Pandas objects all have a `to_pickle` method which writes all data to disk.

```python
frame = pd.read_csv("examples/ex1.csv")

frame.to_pickle("examples/pickle1")

df = pd.read_pickle("examples/pickle1")
```

If you install `pyarrow`, you can read Parquet files using `pandas.read_parquet` method.
### Reading Excel

To read Excel install following : `openpyxl` and `xlrd`

```python

xlsx = pd.ExcelFile("example/ex1.xlsx")

xlsx.sheet_names

# reading the Sheet1
xlsx.parse(sheet_name = "Sheet1")

# this excel table already has Unnamed index, which should be index
xlsx.parse(sheet_name = "Sheet1", index_col=0)

# alernative way
frame = pd.read_excel("example/ex1.xlsx", sheet_name="Sheet1")

# writing
writer = pd.ExcelWriter("examples/ex2.xlsx")
frame.to_excel(writer, "Sheet1")
writer.save()

# or just use following
frame.to_excel("examples/ex2.xlsx")
```

### Using HDF5 Format

HDF, *Hierarchical Data Format*

Compared with simpler formats, HDF5 supports on-the-fly compression with a variety of compression modes, enabling data with repeated patterns to be stored more efficiently.

This requires following package : `pytables`

```python
frame = pd.DataFrame({"a": np.random.standard_normal(100)})
store = frame.HDFStore("examples/mydata.h5")

store["obj1"] = frame
store["obj1_col"] = frame["a"]

store
store.put("obj2", frame, format="table")
store.close()
```

```python
# much simpler
frame.to_hdf("examples/mydata.h5", "obj3", format="table")
pd.read_hdf("examples/mydata.h5", "obj3", where=["index < 5"])

```

HDF5 is _not_ a database. It is best suited for write-once, read-many datasets.
## Interacting with Database

```python
import sqlite3

query = "CREATE TABLE cities (name VARCHAR(50), state VARCHAR(20), population FLOAT)"
con = sqlite3.connect("mydata.sqlite")

con.execute(query)
con.commit()

data = [("Atlanta", "Georgia", 1.25), ("Tallahassee", "Florida", 2.6), ("Sacramento", "California", 1.7)]
stmt = "INSERT INTO cities VALUES (%s, %s, %s)"
con.executemany(stmt, data)

cursor = con.execute("SELECT * FROM cities")
rows = cursor.fetchall()

pd.DataFrame(rows, columns=[x[0] for x in cursor.description])

```

Using SQLAlchemy

```python
import sqlalchemy as sqla

db = sqla.create_engine("sqlite:///mydata.sqlite")
pd.read_sql("SELECT * FROM cities", db)
```