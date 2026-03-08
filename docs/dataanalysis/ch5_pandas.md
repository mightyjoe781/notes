# Introduction to Pandas

*Pandas* has abstraction which allow to make data cleaning and analysis fast and convenient in Python. 

*Pandas* is designed for working with tabular or heterogenous data. NumPy by contrast, is best suited with working with homogeneously typed numerical data.
### Series

A series is a one-dimensional array-like object containing a sequence of values of the same type and an associated array of data labels called its *index*

```python
import pandas as pd

obj = pd.Series([4, 7, -5, 3])

obj

# output
0    4
1    7
2   -5
3    3
dtype: int64
```

If index is not passed, then default index of 0, ... N-1 is assigned.

```python
obj.array 
# <PandasArray>
# [4, 7, -5, 3]
# Length: 4, dtype: int64

obj.index
# RangeIndex(start=0, stop=4, step=1)
```

```python
# object with custom index
obj2 = pd.Series([4, 7, -5, 3], index=["d", "b", "a", "c"])

# compared with numpy, access using labels is allowed

obj2["a"] # -5
```

Using NumPy-like operations, such as filtering with Boolean array, scalar multiplication, or applying math functions preserve the index-value link.

```python
obj2[obj2 > 0]

# output
d    4
b    7
c    3
dtype: int64

obj2 * 2

import numpy as np
np.exp(obj2) # this alwso works
```

Simple dictionary like operations also work

```python
"b" in obj2 # True
"e" in obj2 # False

# python dictionary can be converted into Series
sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
obj3 = pd.Series(sdata)

# converting back to dictionary
obj3.to_dict()

## generally when creating series, dictionary order (keys in insertion order) is preserved, to reorder the dictionary, pass custom index
states = ["California", "Ohio", "Oregon", "Texas"]
obj4 = pd.Series(sdata, index=states)

California        NaN
Ohio          35000.0
Oregon        16000.0
Texas         71000.0
dtype: float64
```

Notice how California didn't map to any of the values, NaN (Not a Number)

```python
pd.isna(obj4)
pd.isnotna(obj4)
```


Both series and index have a `name` attribute

```python
obj4.name = "population"
obj4.index.name = "state"

state
California        NaN
Ohio          35000.0
Oregon        16000.0
Texas         71000.0
Name: population, dtype: float64
```

Index can be altered in place by assignment

```python
obj

0    4
1    7
2   -5
3    3
dtype: int64

obj.index = ["Bob", "Steve", "Jeff", "Ryan"]

Bob      4
Steve    7
Jeff    -5
Ryan     3
dtype: int64
```
### DataFrame

A DataFrame represents a rectangular table of data and contains an ordered, named collection of columns, each of which can have different value type (*numeric, string, Boolean, etc.*).

The DataFrame has both a row and column index; it can be thought of as a dictionary of series all sharing same index.

```python
data = {"state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada"],
        "year": [2000, 2001, 2002, 2001, 2002],
        "pop": [1.5, 1.7, 3.6, 2.4, 2.9]}
frame = pd.DataFrame(data)
frame

	state	year	pop
0	Ohio	2000	1.5
1	Ohio	2001	1.7
2	Ohio	2002	3.6
3	Nevada	2001	2.4
4	Nevada	2002	2.9
```

For large DataFrames, the `head` method selects only first five rows.

```python
frame.head()
frame.tail() # return last 5 rows
```

If you specify the sequence of columns, DFs columns will be arranged in that order

```python
pd.DataFrame(data, columns=["year", "state", "pop"])
```

If a column is passed and doesn't exists will appear as NaN.

```python
frame2 = pd.DataFrame(data, columns=["year", "state", "pop", "debt"],)


	year	state	pop	debt
0	2000	Ohio	1.5	NaN
1	2001	Ohio	1.7	NaN
2	2002	Ohio	3.6	NaN
3	2001	Nevada	2.4	NaN
4	2002	Nevada	2.9	NaN

frame2.columns
# Index(['year', 'state', 'pop', 'debt'], dtype='str')
```

A column in a DataFrame can be retrieved as a Series either by dictionary like notation of using dot attribute

```python
frame2["state"]

# Or
frame2.year
```

Rows can also be retrieved by position or name with the special `iloc` or `loc` attributes

```python
frame2.loc[1]

year     2002
state    Ohio
pop       3.6
debt      NaN
Name: 2, dtype: object
```

Column can be modified by assignment, empty column `debt` could be assigned a scalar value or an array of values.

```python
frame2["debt"] = 16.5 # all values 16.5

frame2["debt"] = np.arange(6.)

# NOTE when assinging lists or arrays to a column, the value's length must match length of DataFrame.

frame2["eastern"] = frame2["state"] == "Ohio" # adds a new column
# NOTE: frame2.eastern can't be used to create a new column.

del frame2["eastern"] # removes the column

```

Column returned from indexing a DataFrame is a *view* on the underlying data, not a copy. Thus, any in-place modifications to the Series will be reflected in the DataFrame.

Another common form of data is nested dictionary of dictionaries.

```python
population = {"Nevada": {2001: 2.4, 2002: 2.9},
              "Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6}}
frame3 = pd.DataFrame(population)
frame3

	Nevada	Ohio
2001	2.4	1.7
2002	2.9	3.6
2000	NaN	1.5

# transpose of above frame
frame3.T

# NOTE : transpose discrad the column data types if the columns do not all have same data type, so transposing twice may not return original array.

# explicit index
pd.DataFrame(population, index=[2001, 2002, 2003])


Nevada	Ohio
2001	2.4	1.7
2002	2.9	3.6
2003	NaN	NaN
```

Dictionaries of Series are treated similarly

```python
pdata = {"Ohio": frame3["Ohio"][:-1],
         "Nevada": frame3["Nevada"][:2] 
         }

pd.DataFrame(pdata)

	Ohio	Nevada
2001	1.7	2.4
2002	3.6	2.9
```

Similar to Series, if a DataFrame's index and columns have their `name` attributes set, these will also be displayed

```python
frame3.index.name = "year"
frame3.columns.name = "state"

state	Nevada	Ohio
year		
2001	2.4	1.7
2002	2.9	3.6
2000	NaN	1.5
```

DataFrame's `to_numpy` method returns the data contained in the DataFrame as a 2D ndarray

```python
frame3.to_numpy()

array([[2.4, 1.7],
       [2.9, 3.6],
       [nan, 1.5]])
```
### Index Objects

panda's index objects are responsible for holding the axis labels (including DataFrames's column names) and other metadata (axis name or names).

```python
obj = pd.Series(np.arange(3), index=["a", "b", "c"])
idx = obj.index
idx

# Index(['a', 'b', 'c'], dtype='str')
```

*index* objects are immutable and thus can't be modified by the user. Immutability makes it safer to share index objects among data structures

```python
label = pd.Index(np.arange(3))

labels # Int64Index([0, 1, 2], dtype="int64")

obj2 = pd.Series([1.4, 5.2, 0], index=labels)

obj2

obj2.index is labels # True
```

In addition to being array-like, an Index also behaves like a fixed-size set. Unlike Python sets, a pandas Index can contain duplicate labels.

Selection with duplicate labels will select all occurrences of that label. Each index has a number of methods and properties for set logic, which answers common questions about the data it contains. Ex - `append(), differnce(), intersections(), union(), isin(), delete(), drop(), insert(), is_monotonic(), is_unique(), unique()`
## Essential Functionality

### Reindexing

`reindex` on a Series rearranges the data according to a new windex, introducing missing values if any index values were not already present.

```python
obj = pd.Series(range(3), index=["b", "c", "a"])
obj2 = obj.reindex(["a", "b", "c", "d"])
obj2

### ==== OUTPUT ==== ###
a    2.0
b    0.0
c    1.0
d    NaN
dtype: float64
```

Use Case : during interpolation or filling of values when reindexing, `ffill` can hep forward-fill values.

```python
obj3 = pd.Series(["blue", "purple", "yellow"], index=[0, 2, 4])
obj3.reindex(range(6), method="ffill")

### ==== OUTPUT ==== ###
0      blue
1      blue
2    purple
3    purple
4    yellow
5    yellow
dtype: str
```

With a DataFrame `reindex` can alter the `row` index, columns, or both. There are multiple important arguments for reindex function like : `labels`, `index`, `columns`, `axis`, `method`, `fill_value`, `limit`, `tolerance`, `level`, `copy`, etc.

```python
frame = pd.DataFrame(np.arange(9).reshape((3, 3)),
                        index=["a", "c", "d"],
                        columns=["Ohio", "Texas", "California"])

frame2 = frame.reindex(["a", "b", "c", "d"])
frame2

# columns can be reindexed with `columns` or `reindex` keyword
frame3 = frame.reindex(columns=["Texas", "Utah", "California"])
frame3

# we can pass axis similar to NumPy
# frame3 = frame.reindex(["Texas", "Utah", "California"], axis="columns")
```
### Dropping Entries from an Axis

Dropping Entries (one or more) from an axis is simple if you already have an index array or list without those entries, since you can use `reindex` method or `.loc-` based indexing.

```python
obj = pd.Series(np.arange(5.), index=["a", "b", "c", "d", "e"])
new_obj = obj.drop("c")
# or
new_obj = obj.drop(["d", "c"])
```

With DataFrame, index values can be deleted from either axis.

```python
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
                    index=["Ohio", "Colorado", "Utah", "New York"],
                    columns=["one", "two", "three", "four"])

data.drop(index=["Colorado", "Ohio"]) # deletes selection of rows
data.drop(columns=["two", "four"]) # deletes selection of columns

# passing axis = 1 or axis = "columns" will delete columns instead of rows
data.drop(["two", "four"], axis="columns")
```

### Indexing, Selection, and Filtering

Series indexing works analogously to NumPy, except you can use Series's index values instead of the integers.

```python

obj = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
obj

obj["b"] # 1
obj[1] # 1
obj[2:4] # c 2, d 3
obj[["b", "a", "d"]] # b 1, a 0, d 3
obj[1,3] # b 1, d 3
obj[obj < 2] # a 0, b 1
```

`loc` is preferred over `[]` for label-based selection because `[]` behaves inconsistently with integer indexes, treating them as labels rather than positions.

```python
obj = pd.Series([1, 2, 3], index=["a", "b", "c"])

obj[[0, 1, 2]]

# returns

a 1
b 2
c 3

# while
obj.loc([0, 1]) # errors out, as `loc` processes with labels exclusively
```

NOTE: *Slicing with labels is inclusive as contrast to Python slicing*

Assigning values to slices modifies corresponding Series Selection

```python
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
                    index=["Ohio", "Colorado", "Utah", "New York"],
                    columns=["one", "two", "three", "four"])
data

```

With DataFrames

```python
data = pd.DataFrame(np.arange(16).reshape((4, 4)),
                    index=["Ohio", "Colorado", "Utah", "New York"],
                    columns=["one", "two", "three", "four"])
data

# ------------------
	one	two	three	four
Ohio	0	1	2	3
Colorado	4	5	6	7
Utah	8	9	10	11
New York	12	13	14	15
# ------------------

data["two"]
data[["three", "one"]]

data[:2]

data[data["three"] > 5]

# ------------------
data < 5 # scalar comparison, returns Boolean DataFrame
	one	two	three	four
Ohio	True	True	True	True
Colorado	True	False	False	False
Utah	False	False	False	False
New York	False	False	False	False
# ------------------
# We can empty out the data as well

data[data < 5] = 0 # sets True selection values to zero
```

`loc` : Label Based Indexing,

`iloc` : Integer Based Indexing

Since DF is 2D, you can select a subset of rows and columns with NumPy-like notation, using either axis labels(`loc`) or integers (`iloc`)

```python
# data
	one	two	three	four
Ohio	0	0	0	0
Colorado	0	5	6	7
Utah	8	9	10	11
New York	12	13	14	15
# ----------
data.loc["Colarado"] # column selection
data.loc[["Colarado", "New York"]]

# -- row and column selection
data.loc["Colorado", ["two", "three"]]

# above operations using iloc
data.iloc[2]
data.iloc[[2, 1]]

data.iloc[2, [3, 0, 1]]
data.iloc[[1, 2], [3, 0, 1]]

# using range operations
data.loc[:"Utah", "two"]

data.iloc[:, :3][data.three > 5]
data.loc[data.three >= 2]

```

Pandas doesn't support `-1` python indexing.

Chaining `loc` operation sometimes may yield `SettingWithCopyWarning` because of modifying the data in the same expression. Better approach is to chain the `loc` separately

```python
data.loc[data["three"] == 5]["three"] = 3 # warning out

# correct way
data.loc[data.three == 5, "three"] = 6
```
### Arithmetic and Data Alignment

pandas makes it simpler to work with objects with different indices. Putting NaN on indeterministic operations.

```python
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=["a", "c", "d", "e"])
s2 = pd.Series([-2.1, 3.6, -1.5, 4.0], index=["a", "c", "e", "f"])

s1+s2

### ------
a    5.2
c    1.1
d    NaN
e    0.0
f    NaN
dtype: float64

```

Similar filling is observed in DataFrames as well.

Arithmetic methods with fill values, In Arithmetic operations between differently indexed objects, you might want to fill a special value like 0, when an axis label is found in one object but not in the other.

```python
df1 = pd.DataFrame(np.arange(12).reshape((3, 4)), columns=list("abcd"))
df2 = pd.DataFrame(np.arange(20).reshape((4, 5)), columns=list("abcde"))

df2.loc[1, "b"] = np.nan # set (1, "b") to NA

df1.add(df2, fill_value=0) # fixed fill value to 0, rather than NaN
df1.rdiv(1) # fills divide by zero

# during indexing as well we can define the fill values
df1.reindex(columns = df2.columns, fill_value = 0)
```

*Broadcasting operation between DataFrame and Series*

```python
arr = np.arange(12).reshape((3, 4))
arr[0] # Series([0, 1, 2, 3])
arr - arr[0] # broadcast, does subtraction in each row

## ----- RESULT -------

[[ 0, 0, 0, 0],
  [4, 4, 4, 4],
  [8, 8, 8, 8]]
```

By default arithmetic between DataFrame and Series matches the index of Series on the columns of the DataFrame, broadcasting down to rows.

```python
frame - series # ops broadcasted to all rows
```

*Broadcasting over columns example*

```python
series3 = frame["d"]

frame.sub(series3, axis="index")
```

#### Function application and Mapping

*NumPy* ufuncs also work with pandas object

```python
frame = pd.DataFrame(np.random.standard_normal((4, 3)),
                        columns = list("bde"),
                        index=["Utah", "Ohio", "Texas", "Oregon"])
                        
np.abs(fram) # applies on all elements of frame

# ex - one dimensional function applied to each row/col
# returns - series having columns of frame as its index
def f1(x):
    return x.max() - x.min()
    
frame.apply(f1)
frame.apply(f1, axis="columns") # to apply on columns

# NOTE f1(x) --> doesn't need to return scalar, it can return Series with multiple values

def f2(x):
    return pd.Series([x.min(), x.max], index=["min", "max"])
    
frame.apply(f2)

# apply to each element
def my_format(x):
    return f"{x:.2f}"
    
frame.applymap(my_format) # frame
frame["e"].map(my_fromat) # Series has map function
```
### Sorting and Ranking

To sort in lexicographically by row or column label, use `sort_index`, which returns a new sorted object.

```python
obj = pd.Series(np.arange(4), index=list("dabc"))
obj.sort_index()

# with dataframe we can sort by index on either axis
frame.sort_index()
frame.sort_index(axis="columns")
frame.sort_index(axis="columns", ascending=False) # default is ascending

# sorting by values
obj.sort_values() # Note missing values are sorted to end
obj.sort_values(na_position="first") # moves missing entries to first

# for sorting a frame we can use the data in one or more columns as sort keys
frame.sort_values("b")
frame.sort_values(["b", "a"])

# Ranking : assigns from 1-number of vlaid entries from lowest  value
obj = pd.Series([7, -5, 7, 4, 2, 0, 4])
obj.rank()

obj.rank(method="first") # assign based on order its seen in data

```
### Axis indexes with Duplicate Labels

pandas by default doesn't put restriction of unique indexes

```python
obj = pd.Series(np.arange(5), index=list(aabbc))

obj.index.is_unique # False

obj["a"] # ---> return Series
obj["c"] # returns Scalar

# similar logic extends to frame

df = pd.DataFrame(np.random.standard_normal((5, 3)),
                            index=list("aabbc"))

df.loc["b"] # ---->> returns frame
df.loc["c"] # ----->> returns Series
```

## Summarizing and Computing Descriptive Statistics

There are two types of statistical methods available in pandas. *Reductions & Summary Statistics*

```python
df = pd.DataFrame([[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]],
                    index=["a", "b", "c", "d"],
                    columns=["one", "two"]
                    )

df.sum() # ---> Series containing column sums
### 
one    9.25
two   -5.80
dtype: float64

### 
df.sum(axis="columns") # across columns --> rows

# by default NaN is ignored
df.sum(axis="index", skipna=False) # returns NaN if any column has NaN

# some aggregation require atleast one non-NA value
df.mean(axis = "columns")

df.idxmax() # max value of index

## ----- ACCUMULATIONS -----

df.cumsum() # -- frame

### ---->
	one	two
a	1.40	NaN
b	8.50	-4.5
c	NaN	NaN
d	9.25	-5.8

# quick statistical summary
df.describe()

# NOTE: on non-numeric data it provides alternative summary
```
### Correlation and Covariance

```python
price = pd.read_pickle("data/prices.pickle")
volume = pd.read_pickle("data/volumes.pickle")

returns = price.pct_change() # compute percentage changes
returns.tail()

# let's calculate the correlation of percentage change between Microsoft and Apple
returns["MSFT"].corr(returns["AAPL"])
returns["MSFT"].cov(returns["AAPL"])

# to get full corr and cov matrix

returns.corr()
returns.cov()

# to get pairwise covariance
returns.corrwith(returns["IBM"])

## passing a DF computes the correlation of matching column names
returns.corrwith(volume)

# passing axis = "column" will does things row-by-row
```

### Unique Values, Value Counts, and Membership

```python
obj = pd.Series(list("cadaabbcc"))

uniques = obj.unique()

obj.value_counts() # return frequency counter, returned in sorted value in descending order

pd.value_counts(obj.to_numpy(), sort=False)

# is-in does vectorized set membership check and useful in filtering
mask = obj.isin(["b", "c"])

## ----
0     True
1    False
2    False
3    False
4    False
5     True
6     True
7     True
8     True
dtype: bool

obj[mask]

0    c
5    b
6    b
7    c
8    c
dtype: str
```

`Index.get_indexer` method gives an index array from an array of possibly non-distinct values into another array of distinct values.

```python
to_match = pd.Series(["c", "a", "b", "b", "c", "a"])
unique_vals = pd.Series(["c", "b", "a"])

indices = pd.Index(unique_vals).get_indexer(to_match)
indices

 # array([0, 2, 1, 1, 0, 2])
```

Histogram Calculation

```python
data = pd.DataFrame({"Qu1": [1, 2, 3, 4], "Qu2": [5, 6, 7, 8], "Qu3": [9, 10, 11, 12]},
                    index=["a", "b", "c", "d"]
                    )

data["Qu1"].value_counts().sort_index()

Qu1
1    1
2    1
3    1
4    1
Name: count, dtype: int64

## applying on all columns
data = pd.DataFrame({"Qu1": [1, 3, 4, 3, 4], "Qu2": [2, 3, 1, 2, 3], "Qu3": [1, 5, 2, 4, 4]},
                    index=["a", "b", "c", "d", "e"]
                    )

data["Qu1"].value_counts().sort_index()

# apply on all columns that contain "Qu"
res = data.apply(data.value_counts).fillna(0)
res
# ------ OUTPUT -----
	Qu1	Qu2	Qu3
1	1.0	1.0	1.0
2	0.0	2.0	1.0
3	2.0	2.0	0.0
4	2.0	0.0	2.0
5	0.0	0.0	1.0
```