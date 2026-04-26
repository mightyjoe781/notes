# Data Wrangling: Join, Combine And Reshape

## Hierarchical Indexing

Hierarchical Indexing allows to have multiple (two or more) index levels on an axis.

```python
import pandas as pd
import numpy as np

data = pd.Series(np.random.uniform(size=9),
                 index=[["a", "a", "a", "b", "b", "c", "c", "d", "d"],
                        [1, 2, 3, 1, 3, 1, 2, 2, 3]])

data

## ----
a  1    0.191687
   2    0.538137
   3    0.690694
b  1    0.373462
   3    0.584537
c  1    0.129612
   2    0.431979
d  2    0.004920
   3    0.916431
dtype: float64
```

Here we can see Series with *MultiIndex* as its index.

```python
data.index
## ----
MultiIndex([('a', 1),
            ('a', 2),
            ('a', 3),
            ('b', 1),
            ('b', 3),
            ('c', 1),
            ('c', 2),
            ('d', 2),
            ('d', 3)],
           )
           
# partial indexing..
data["b"]

# ----
1    0.503164
3    0.493336
dtype: float64

## similar selections
data["b":"c"]
data.loc[["b", "d"]]
```

Inner level selection.

```python
data[:, 2]

# value 2 on second-index level
# ----
a    0.258494
c    0.152593
d    0.398022
dtype: float64
```

Converting into DataFrame.

```python
data.unstack()
# ------
1	2	3
a	0.956538	0.106071	0.123455
b	0.549255	NaN	0.031701
c	0.496406	0.926585	NaN
d	NaN	0.037208	0.597208
```

Hierarchical Levels can have names (as string or any other Python objects), so they show up in console output

```python
frame.index.names = ["key1", "key2"]
frame.columns.names = ["state", "color"]
```

```python
frame.index.nlevels # prints levels
```

### Reordering and Sorting Levels

`swaplevel` method takes two level numbers or names and returns a new object with the levels interchanged.

```python
frame.swaplevel("key1", "key2")
# --------
state      Ohio     Colorado
color     Green Red    Green
key2 key1                   
1    a        0   1        2
2    a        3   4        5
1    b        6   7        8
2    b        9  10       11
```

```python
# `sort_index` by default sorts using all index levels
# but we can specify specific level or subset of levels

frame.sort_index(level=1)
frame.swaplevel(0, 1).sort_index(level=0)

```
### Summary Statistics by Level

Many descriptive and summary statistics on DataFrame and Series have level options

```python
frame.groupby(level="key2").sum()

frame.groupby(level="color", axis="columns").sum()
```

### Indexing with a DataFrame's Columns

```python
frame = pd.DataFrame({"a": range(7), "b": range(7, 0, -1),
                      "c": ["one", "one", "one", "two", "two",
                            "two", "two"],
                      "d": [0, 1, 2, 0, 1, 2, 3]})

frame
# ------
	a	b	c	d
0	0	7	one	0
1	1	6	one	1
2	2	5	one	2
3	3	4	two	0
4	4	3	two	1
5	5	2	two	2
6	6	1	two	3
# -----

frame2 = frame.set_index(["c", "d"])

		a	b
c	d		
one	0	0	7
1	1	6
2	2	5
two	0	3	4
1	4	3
2	5	2
3	6	1

## ---- by default c, d columns are dropped, it can avoided 
frame2 = frame.set_index(["c", "d"], drop=False)

## -- opposite operation is reset_index, which converts hierarchical data into
## --- columns
```

## Combining and Merging Datasets

Data contained in pandas objects can be combined in a number of ways

- `pandas.merge`
- `pandas.concat`
- `combine_first`

### Database Style DataFrame Joins

```python
df1 = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "a", "b"],
                    "data1": pd.Series(range(7), dtype="Int64")})
## ----
key	data1
0	b	0
1	b	1
2	a	2
3	c	3
4	a	4
5	a	5
6	b	6

df2 = pd.DataFrame({"key": ["a", "b", "d"],
                    "data2": pd.Series(range(3), dtype="Int64")})
## -----
	key	data2
0	a	0
1	b	1
2	d	2

pd.merge(df1, df2) # many-to-one join

	key	data1	data2
0	b	0	1
1	b	1	1
2	a	2	0
3	a	4	0
4	a	5	0
5	b	6	1

# NOTE: we didn't pass join column, pandas infers same column in both df for join
pd.merge(df1, df2, on="key")
```

In general order of columns output in `pandas.merge` operations is unspecified. 

NOTE: By default pandas does an `inner` join.

```python
pd.merge(df1, df2, how="outer")

	key	data1	data2
0	a	2	0
1	a	4	0
2	a	5	0
3	b	0	1
4	b	1	1
5	b	6	1
6	c	3	<NA>
7	d	<NA>	2

# in outer join keys which didn't join will appear in the result
```


| Option  | Behavior                                                  |
| ------- | --------------------------------------------------------- |
| `inner` | Use only the key combinations observed in both tables     |
| `outer` | Use all key combinations observed in both tables together |
| `left`  | Use all key combinations found in the left table          |
| `right` | Use all key combinations found in the right table         |

To merge on multiple columns use

```python
pd.merge(left, right, on=["key1", "key2"], how="outer")
```

To deal with duplicate names from both df we can use *suffix*.

```python
pd.merge(left, right, on="key1", suffixes=("_left", "_right"))
```
### Merging on Index

In some cases merge keys in a DF will be found in its index (row labels), you can pass `left_index=True` or `right_index=True` (or both) to indicate that the index should be used as the merge key

```python
left1 = pd.DataFrame({"key": ["a", "b", "a", "a", "b", "c"],
                      "value": pd.Series(range(6), dtype="Int64")})
# ------
key	value
0	a	0
1	b	1
2	a	2
3	a	3
4	b	4
5	c	5

right1 = pd.DataFrame({"group_val": [3.5, 7]}, index=["a", "b"])
# ------
group_val
a	3.5
b	7.0

## 
pd.merge(left1, right1, left_on="key", right_index=True)
key	value	group_val
0	a	0	3.5
1	b	1	7.0
2	a	2	3.5
3	a	3	3.5
4	b	4	7.0

# NOTICE : how c is dropped, because default behaviour is inner
pd.merge(left1, right1, left_on="key", right_index=True, how="outer")

key	value	group_val
0	a	0	3.5
2	a	2	3.5
3	a	3	3.5
1	b	1	7.0
4	b	4	7.0
5	c	5	NaN

# we can preserve both indices as well using left_index=True

left.join([right, another_df], how="outer")
```

### Concatenating Along Axis

Another kind of data combination operation is referred to interchangeably as _concatenation_ or _stacking_.

```python
arr = np.arange(12).reshape((3, 4))

# ---
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])

np.concatenate([arr, arr], axis=1)

# ---
array([[ 0,  1,  2,  3,  0,  1,  2,  3],
       [ 4,  5,  6,  7,  4,  5,  6,  7],
       [ 8,  9, 10, 11,  8,  9, 10, 11]])
```

In context of Pandas Series and DataFrames we have labelled axes further generalizing the concatenation.

```python
s1 = pd.Series([0, 1], index=["a", "b"], dtype="Int64")
s2 = pd.Series([2, 3, 4], index=["c", "d", "e"], dtype="Int64")
s3 = pd.Series([5, 6], index=["f", "g"], dtype="Int64")

pd.concat([s1, s2, s3])

## ------
a    0
b    1
c    2
d    3
e    4
f    5
g    6
dtype: Int64

# default concat axis is "index"
pd.concat([s1, s2, s3], axis="column")

	0	1	2
a	0	<NA>	<NA>
b	1	<NA>	<NA>
c	<NA>	2	<NA>
d	<NA>	3	<NA>
e	<NA>	4	<NA>
f	<NA>	<NA>	5
g	<NA>	<NA>	6

# default intersection above is outer

s4 = pd.concat([s1, s3])
pd.concat([s1, s4], axis="columns", join="inner") # remove NA joins

# ----
	0	1
a	0	0
b	1	1

# ------- CREATING Hiearchical Index using concat, by passing keys arg
result = pd.concat([s1, s1, s3], keys=["one", "two", "three"])
result.unstack() # gives DataFrame result of join (outer)

```
### Combining Data with Overlap

*deals with dataset where indexes overlap in full or in part*,

```python
a = pd.Series([np.nan, 2.5, 0.0, 3.5, 4.5, np.nan],
              index=["f", "e", "d", "c", "b", "a"])

b = pd.Series([0., np.nan, 2., np.nan, np.nan, 5.],
              index=["a", "b", "c", "d", "e", "f"])

np.where(pd.isnull(a), b, a) # array([0. , 2.5, 0. , 3.5, 4.5, 5. ])
# fills values from b where ever a is null or else take from a

# using numpy doesn't check the index labels are aligned or not, to line up values using index.
a.combine_first(b)

# -----
a    0.0
b    4.5
c    3.5
d    0.0
e    2.5
f    5.0
dtype: float64
```

Similar with DataFrame

```python
df1 = pd.DataFrame({"a": [1., np.nan, 5., np.nan],
                    "b": [np.nan, 2., np.nan, 6.],
                    "c": range(2, 18, 4)})

df2 = pd.DataFrame({"a": [5., 4., np.nan, 3., 7.],
                    "b": [np.nan, 3., 4., 6., 8.]})

# fills-out nan values from df2, but matches values based on index               # The output of `combine_first` with DataFrame objects will have the union of all the column names.
df1.combine_first(df2)

	a	b	c
0	1.0	NaN	2.0
1	4.0	2.0	6.0
2	5.0	4.0	10.0
3	3.0	6.0	14.0
4	7.0	8.0	NaN
                 
```
## Reshaping and Pivoting
### Reshaping with Hierarchical Indexing

- `stack` : This “rotates” or pivots from the columns in the data to the rows.
- `unstack` : This pivots from the rows into the columns.


```python
data = pd.DataFrame(np.arange(6).reshape((2, 3)),
                    index=pd.Index(["Ohio", "Colorado"], name="state"),
                    columns=pd.Index(["one", "two", "three"],
                    name="number"))
data

# --------
number	one	two	three
state			
Ohio	0	1	2
Colorado	3	4	5

### stack
data.stack() # stacks the columns into rows,
# -----
state     number
Ohio      one       0
          two       1
          three     2
Colorado  one       3
          two       4
          three     5
dtype: int64

# to convert back into frame from Series
data.unstack() # or data.unstack(level=0)
# similarly ~ use data.unstack(level="state")

```

Stacking by default may introduce missing data.

```python
s1 = pd.Series([0, 1, 2, 3], index=["a", "b", "c", "d"], dtype="Int64")
s2 = pd.Series([4, 5, 6], index=["c", "d", "e"], dtype="Int64")

data2 = pd.concat([s1, s2], keys=["one", "two"])

# -----
one  a    0
     b    1
     c    2
     d    3
two  c    4
     d    5
     e    6
dtype: Int64

# ------
data2.unstack()

    a	b	c	d	e
one	0	1	2	3	<NA>
two	<NA> <NA>	4	5	6

data2.unstack().stack()
# -------
one  a       0
     b       1
     c       2
     d       3
     e    <NA>
two  a    <NA>
     b    <NA>
     c       4
     d       5
     e       6
dtype: Int64

```
### Pivoting Long to Wide Format

A common way to store multiple time series in databases and CSV files is what is sometimes called long or stacked format.

Individual values are represented by a single row in a table rather than multiple values per row.

```python
data = pd.read_csv("examples/macrodata.csv")
data = data.loc[:, ["year", "quarter", "realgdp", "infl", "unemp"]]

data.head()

# -----
   year  quarter   realgdp  infl  unemp
0  1959        1  2710.349  0.00    5.8
1  1959        2  2778.801  2.34    5.1
2  1959        3  2775.488  2.74    5.3
3  1959        4  2785.204  0.27    5.6
4  1960        1  2847.699  2.31    5.2
# ------
```

`pandas.PeriodIndex` represents time intervals rather than points in time.

```python
# set to values at teh end of the quarter

periods = pd.PeriodIndex(year=data.pop("year"),
                         quarter=data.pop("quarter"),
                         name="date")

data.index = periods.to_timestamp("D")

data.head()

# ------
             realgdp  infl  unemp
date                             
1959-01-01  2710.349  0.00    5.8
1959-04-01  2778.801  2.34    5.1
1959-07-01  2775.488  2.74    5.3
1959-10-01  2785.204  0.27    5.6
1960-01-01  2847.699  2.31    5.2
# ------                         

data = data.reindex(columns=["realgdp", "infl", "unemp"])
data.columns.name = "item"

# -------
item         realgdp  infl  unemp
date                             
1959-01-01  2710.349  0.00    5.8
1959-04-01  2778.801  2.34    5.1
1959-07-01  2775.488  2.74    5.3
1959-10-01  2785.204  0.27    5.6
1960-01-01  2847.699  2.31    5.2

# -------

long_data = (data.stack()
             .reset_index()
             .rename(columns={0: "value"}))

# --------
        date     item     value
0 1959-01-01  realgdp  2710.349
1 1959-01-01     infl     0.000
2 1959-01-01    unemp     5.800
3 1959-04-01  realgdp  2778.801
4 1959-04-01     infl     2.340
5 1959-04-01    unemp     5.100
6 1959-07-01  realgdp  2775.488
7 1959-07-01     infl     2.740
8 1959-07-01    unemp     5.300
9 1959-10-01  realgdp  2785.204
# ---------


```

This so-called long format for multiple time series, each row in the table represents a single observation.

Data is frequently stored this way in SQL databases, as a fixed schema (column names and types) allow the number of distinct values in the `item` columns to change as data is added to the table.

Both `date` and `item` can be primary keys.

Sometimes its easier to work with data where each unique item is required indexed by `date`

```python
pivoted = long_data.pivot(index="date", columns="item",
                          values="value")
                          
item        infl   realgdp  unemp
date                             
1959-01-01  0.00  2710.349    5.8
1959-04-01  2.34  2778.801    5.1
1959-07-01  2.74  2775.488    5.3
1959-10-01  0.27  2785.204    5.6
1960-01-01  2.31  2847.699    5.2
```

Pivoting multiple-column data

```python
        date     item     value    value2
0 1959-01-01  realgdp  2710.349  0.802926
1 1959-01-01     infl     0.000  0.575721
2 1959-01-01    unemp     5.800  1.381918
3 1959-04-01  realgdp  2778.801  0.000992
4 1959-04-01     infl     2.340 -0.143492
5 1959-04-01    unemp     5.100 -0.206282
6 1959-07-01  realgdp  2775.488 -0.222392
7 1959-07-01     infl     2.740 -1.682403
8 1959-07-01    unemp     5.300  1.811659
9 1959-10-01  realgdp  2785.204 -0.351305

pivoted = long_data.pivot(index="date", columns="item")

           value                    value2                    
item        infl   realgdp unemp      infl   realgdp     unemp
date                                                          
1959-01-01  0.00  2710.349   5.8  0.575721  0.802926  1.381918
1959-04-01  2.34  2778.801   5.1 -0.143492  0.000992 -0.206282
1959-07-01  2.74  2775.488   5.3 -1.682403 -0.222392  1.811659
1959-10-01  0.27  2785.204   5.6  0.128317 -0.351305 -1.313554
1960-01-01  2.31  2847.699   5.2 -0.615939  0.498327  0.174072

# extract a portion of the data
pivoted["value"]

item        infl   realgdp  unemp
date                             
1959-01-01  0.00  2710.349    5.8
1959-04-01  2.34  2778.801    5.1
1959-07-01  2.74  2775.488    5.3
1959-10-01  0.27  2785.204    5.6
1960-01-01  2.31  2847.699    5.2

# NOTE: pivot is same as creating hierarchical index using set_index followed by unstack

long_data.set_index(["date", "item"]).unstack(level="item")

```
### Pivoting Wide to Long Format

An inverse operation of `pivot` for DataFrames is `pandas.melt`.

Rather than transforming one column into many in a new DataFrame, it merges multiple columns into one, producing a DataFrame that is longer than the input.

```python

df = pd.DataFrame({"key": ["foo", "bar", "baz"],
                   "A": [1, 2, 3],
                   "B": [4, 5, 6],
                   "C": [7, 8, 9]})


   key  A  B  C
0  foo  1  4  7
1  bar  2  5  8
2  baz  3  6  9

melted = pd.melt(df, id_vars="key")

   key variable  value
0  foo        A      1
1  bar        A      2
2  baz        A      3
3  foo        B      4
4  bar        B      5
5  baz        B      6
6  foo        C      7
7  bar        C      8
8  baz        C      9

# restore using pivot
reshaped = melted.pivot(index="key", columns="variable", values="value")

variable  A  B  C
key              
bar       2  5  8
baz       3  6  9
foo       1  4  7

## --- reset index to fix index
reshaped.reset_index()
### ----
variable  key  A  B  C
0         bar  2  5  8
1         baz  3  6  9
2         foo  1  4  7

```


You can also specify a subset of columns to use as value columns:

```python
pd.melt(df, id_vars="key", value_vars=["A", "B"])

  variable  value
0        A      1
1        A      2
2        A      3
3        B      4
4        B      5
5        B      6
6        C      7
7        C      8
8        C      9

# group identifiers
pd.melt(df, value_vars=["A", "B", "C"])

  variable value
0      key   foo
1      key   bar
2      key   baz
3        A     1
4        A     2
5        A     3
6        B     4
7        B     5
8        B     6

```