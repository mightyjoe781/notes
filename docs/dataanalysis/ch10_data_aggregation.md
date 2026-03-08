# Data Aggregation and Group Operations

## How to Think About Group Operations

*Hadley Wickham* (well known figure in R community), coined the term *split-apply-combine* for describing group operations.

split into groups (based on groups of keys) on a particular axis -> apply function to each group to receive a value --> combine all values into *combined* result.

Grouping keys could be

- A list or array of values that is same length as axis being grouped
- A value indicating a column name in DataFrame
- A dictionary or Series giving a correspondence between the value on the axis being grouped and group names.
- A function to be invoked on the axis or the individual labels in the index.

![](assets/Pasted%20image%2020260307105350.png)

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({"key1" : ["a", "a", None, "b", "b", "a", None],
                   "key2" : pd.Series([1, 2, 1, 2, 1, None, 1], dtype="Int64"),
                   "data1" : np.random.standard_normal(7),
                   "data2" : np.random.standard_normal(7)})

df

### -------
  key1	key2	data1	data2
0	a	1	1.018953	1.226504
1	a	2	-1.204039	1.479200
2	NaN	1	-0.020466	-1.070601
3	b	2	0.278867	2.343852
4	b	1	-0.294904	0.017379
5	a	<NA>	0.113810	-1.449101
6	NaN	1	0.335964	1.424791

grouped = df["data1"].groupby(df["key1"]) # --> special grouped object
grouped.mean()

key1
a   -1.319973
b   -0.195054
Name: data1, dtype: float64

### --------- grouping by multiple keys

means = df["data1"].groupby([df["key1"], df["key2"]]).mean()

key1  key2
a     1       0.136874
      2       0.277189
b     1      -0.921064
      2       2.004003
Name: data1, dtype: float64

means.unstack()

key2	1	2
key1		
a	1.547456	0.870079
b	0.070886	0.151864

```


```python
# since grouping information is also in index
means = df.groupby("key1").mean()
means

# -----
	key2	data1	data2
key1			
a	1.5	1.059267	0.701249
b	1.5	0.111375	-0.206672

# -----
# NOTE: by default all numeric columns are aggreagted
df.groupby("key2").mean()

## Errors out ~ Mean Operation is not supported for strings, key1 is string

df.groupby(["key1", "key2"]).mean()

         data1	  data2
key1 key2		
a	  1	   1.547456	0.502745
    2	   0.870079	1.309820
b	  1	   0.070886	0.621810
    2	   0.151864	-1.035155


## ---
# discrepence in size is due to grouby ignoring NA numbers
df.groupby(["key1", "key2"]).size()

key1  key2
a     1       1
      2       1
b     1       1
      2       1
dtype: int64

df.groupby(["key1", "key2"], dropna=False).size()

key1  key2
a     1       1
      2       1
      <NA>    1
b     1       1
      2       1
NaN   1       2
dtype: int64

```

### Iterating over Groups

```python
for name, group in df.groupby("key1"):
    print(name)
    print(group)
    
    
# unpacking multiple keys
for (k1, k2), group in df.groupby(["key1", "key2"]):
    print((k1, k2))
    print(group)
    
# computing dicitonary of data pieces
pieces = {name: group for name, group in df.groupby("key1")}

pieces["b"] # returns all record for key1 = "b"

# we can pass axis as well
grouped = df.groupby({"key1": "key", "key2": "key", "data1": "data", "data2": "data"}, axis="columns") # ~ note axis is deprecated use df.T.groupby


```


### Selecting a Column or Subset of Columns

*Indexing* a groupby object created from dataframe with a column name or array of column names has the effect of subsetting for aggregation.

```python
df.groupby("key1")["data1"]
df.groupby("key1")[["data2"]]

# -- same as

df["data1"].groupby(df["key1"])
df[["data2"]].groupby(df["key1"])
```

On large dataset we often take subset of columns, 

```python
df.groupby(["key1", "key2"])[["data2"]].mean()
```

### Grouping with Dictionaries and Series

```python
people = pd.DataFrame(np.random.standard_normal((5, 5)),
                      columns=["a", "b", "c", "d", "e"],
                      index=["Joe", "Steve", "Wanda", "Jill", "Trey"])

# add few NaN
people.iloc[2:3, [1, 2]] = np.nan

### ----- people df -----
    	a	b	c	d	e
Joe	1.109297	-2.127755	1.950342	-0.262804	-0.342623
Steve	-0.221454	-0.568802	-0.473534	1.902090	1.094954
Wanda	-0.213540	NaN	NaN	-1.076884	0.338169
Jill	1.228075	-0.628660	-2.241994	0.330386	1.602260
Trey	0.670479	0.030333	0.758995	1.854681	-0.419009

mapping = {"a": "red", "b": "red", "c": "blue", "d": "blue", "e": "red", "f" : "orange"}

mapping = {"a": "red", "b": "red", "c": "blue", "d": "blue", "e": "red", "f" : "orange"}
by_column = people.T.groupby(mapping)
by_column.sum()

### ----
    	Joe	Steve	Wanda	Jill	Trey
blue	1.687538	1.428556	-1.076884	-1.911609	2.613677
red	-1.361082	0.304698	0.124629	2.201675	0.281803

```

### Groupby Functions

```python
people.groupby(len).sum()

### -----

a	b	c	d	e
3	1.109297	-2.127755	1.950342	-0.262804	-0.342623
4	1.898554	-0.598326	-1.482999	2.185067	1.183251
5	-0.434994	-0.568802	-0.473534	0.825206	1.433123

```

### Group by Index levels

A final convenience for hierarchically indexed datasets is the ability to aggregate using one of the levels of an axis index

NOTE: don't use `groupby` and `levels` arguments together,


```python
columns = pd.MultiIndex.from_arrays([["US", "US", "US", "JP", "JP"],
                                    [1, 3, 5, 1, 3]], names=["cty", "tenor"])
hier_df = pd.DataFrame(np.random.standard_normal((4, 5)), columns=columns)
```

![](assets/Pasted%20image%2020260307112954.png)

```python
# hier_df.groupby(level="cty", axis="columns").count() ~ old syntax
hier_df.T.groupby(level="cty").count().T
## -------
cty  JP  US
0     2   3
1     2   3
2     2   3
3     2   3
```

## Data Aggregations

Aggregation refers to any data transformation that produces scalar values from arrays. Examples : `any`, `all`, `count`, `cummin`, `cummax`, `cumsum`, `cumprod`, `mean`, `median`, `max`, `min`, `nth`, `ohlc`, `prod`, `quantile`, `rank`, `size`, `sum`, `std, var`

```python
df

grouped = df.groupby("key1")
grouped["data"].nsmallest(2)

### defining custom aggregation function
def peak_to_peak(arr):
    return arr.max - arr.min
    
grouped.agg(peak_to_peak)
grouped.described() # not an aggregation
```

### Column-Wise and Multiple Function Application

```python
tips = pd.read_csv("examples/tips.csv")
tips["tip_pct"] = tips["tip"] / tips["total_bill"]
tips.head()

## =======
   total_bill   tip smoker  day    time  size   tip_pct
0       16.99  1.01     No  Sun  Dinner     2  0.059447
1       10.34  1.66     No  Sun  Dinner     3  0.160542
2       21.01  3.50     No  Sun  Dinner     3  0.166587
3       23.68  3.31     No  Sun  Dinner     2  0.139780
4       24.59  3.61     No  Sun  Dinner     4  0.146808

grouped = tips.groupby(["day", "smoker"])

grouped_pct = grouped["tip_pct"]
grouped_pct.agg("mean")

day   smoker
Fri   No        0.151650
      Yes       0.174783
Sat   No        0.158048
      Yes       0.147906
Sun   No        0.160113
      Yes       0.187250
Thur  No        0.160298
      Yes       0.163863
Name: tip_pct, dtype: float64

grouped_pct.agg(["mean", "std", peak_to_peak])

                 mean       std  peak_to_peak
day  smoker                                  
Fri  No      0.151650  0.028123      0.067349
     Yes     0.174783  0.051293      0.159925
Sat  No      0.158048  0.039767      0.235193
     Yes     0.147906  0.061375      0.290095
Sun  No      0.160113  0.042347      0.193226
     Yes     0.187250  0.154134      0.644685
Thur No      0.160298  0.038774      0.193350
     Yes     0.163863  0.039389      0.151240
```

```python
functions = ["count", "mean", "max"]
result = grouped[["tip_pct", "total_bill"]].agg(functions)

            tip_pct                     total_bill                  
              count      mean       max      count       mean    max
day  smoker                                                         
Fri  No           4  0.151650  0.187735          4  18.420000  22.75
     Yes         15  0.174783  0.263480         15  16.813333  40.17
Sat  No          45  0.158048  0.291990         45  19.661778  48.33
     Yes         42  0.147906  0.325733         42  21.276667  50.81
Sun  No          57  0.160113  0.252672         57  20.506667  48.17
     Yes         19  0.187250  0.710345         19  24.120000  45.35
Thur No          45  0.160298  0.266312         45  17.113111  41.19
     Yes         17  0.163863  0.241255         17  19.190588  43.11
     
# to apply different operation to different hierarchical index
grouped.agg({"tip_pct" : ["min", "max", "mean", "std"], "size" : "sum"})

              tip_pct                               size
                  min       max      mean       std  sum
day  smoker                                             
Fri  No      0.120385  0.187735  0.151650  0.028123    9
     Yes     0.103555  0.263480  0.174783  0.051293   31
Sat  No      0.056797  0.291990  0.158048  0.039767  115
     Yes     0.035638  0.325733  0.147906  0.061375  104
Sun  No      0.059447  0.252672  0.160113  0.042347  167
     Yes     0.065660  0.710345  0.187250  0.154134   49
Thur No      0.072961  0.266312  0.160298  0.038774  112
     Yes     0.090014  0.241255  0.163863  0.039389   40
```

### Returning Aggregated Data Without Row Indexes

```python
tips.groupby(["day", "smoker"], as_index=False).mean()

# -------
    day smoker  total_bill       tip      size   tip_pct
0   Fri     No   18.420000  2.812500  2.250000  0.151650
1   Fri    Yes   16.813333  2.714000  2.066667  0.174783
2   Sat     No   19.661778  3.102889  2.555556  0.158048
3   Sat    Yes   21.276667  2.875476  2.476190  0.147906
4   Sun     No   20.506667  3.167895  2.929825  0.160113
5   Sun    Yes   24.120000  3.516842  2.578947  0.187250
6  Thur     No   17.113111  2.673778  2.488889  0.160298
7  Thur    Yes   19.190588  3.030000  2.352941  0.163863

```

## Apply : Generic split-apply-combine

```python
def top(df, n=5, column="tip_pct"):
    return df.sort_values(column, ascending=False)[:n]
    
top(tips, n=6)


# now if we group by smokers
tips.groupby("smoker").apply(top)
# -------
            total_bill   tip smoker   day    time  size   tip_pct
smoker                                                           
No     232       11.61  3.39     No   Sat  Dinner     2  0.291990
       149        7.51  2.00     No  Thur   Lunch     2  0.266312
       51        10.29  2.60     No   Sun  Dinner     2  0.252672
       185       20.69  5.00     No   Sun  Dinner     5  0.241663
       88        24.71  5.85     No  Thur   Lunch     2  0.236746
Yes    172        7.25  5.15    Yes   Sun  Dinner     2  0.710345
       178        9.60  4.00    Yes   Sun  Dinner     2  0.416667
       67         3.07  1.00    Yes   Sat  Dinner     1  0.325733
       183       23.17  6.50    Yes   Sun  Dinner     4  0.280535
       109       14.31  4.00    Yes   Sat  Dinner     2  0.279525
```

`tips` DF is split into groups based on Smoker Values, Then top function is called on each of those groups, and results are concatenated using `pandas.concat`, labelling pieces by group names.

```python
# passing extra params to function
tips.groupby(["smoker", "day"]).apply(top, n=1, column="total_bill")
```

Special case example is 

```python
result = tips.groupby("smoker")["tip_pct"].describe()

# internally its shortcut to
def f(group):
    return group.describe()
    
grouped.apply(f)

```

### Suppressing Group Keys

```python
tips.groupby("smoker", group_keys=False).apply(top)

### ------
    total_bill   tip  smoker   day    time  size   tip_pct
232       11.61  3.39     No   Sat  Dinner     2  0.291990
149        7.51  2.00     No  Thur   Lunch     2  0.266312
51        10.29  2.60     No   Sun  Dinner     2  0.252672
185       20.69  5.00     No   Sun  Dinner     5  0.241663
88        24.71  5.85     No  Thur   Lunch     2  0.236746
172        7.25  5.15    Yes   Sun  Dinner     2  0.710345
178        9.60  4.00    Yes   Sun  Dinner     2  0.416667
67         3.07  1.00    Yes   Sat  Dinner     1  0.325733
183       23.17  6.50    Yes   Sun  Dinner     4  0.280535
109       14.31  4.00    Yes   Sat  Dinner     2  0.279525
```

### Quantile and Bucket Analysis

We studied `cut` and `qcut` before.

```python
frame = pd.DataFrame({"data1": np.random.standard_normal(1000),
                      "data2": np.random.standard_normal(1000)})
                      
frame.head()

## ----
      data1     data2
0 -0.660524 -0.612905
1  0.862580  0.316447
2 -0.010032  0.838295
3  0.050009 -1.034423
4  0.670216  0.434304

### ----
quartiles = pd.cut(frame["data1"], 4)

# -----
0     (-1.23, 0.489]
1     (0.489, 2.208]
2     (-1.23, 0.489]
3     (-1.23, 0.489]
4     (0.489, 2.208]
5     (0.489, 2.208]
6     (-1.23, 0.489]
7     (-1.23, 0.489]
8    (-2.956, -1.23]
9     (-1.23, 0.489]
Name: data1, dtype: category
Categories (4, interval[float64, right]): [(-2.956, -1.23] < (-1.23, 0.489] < (0.
489, 2.208] < (2.208, 3.928]]

# this categorical object can be passed to groupby

def get_stats(group):
    return pd.DataFrame(
        {"min": group.min(), "max": group.max(),
        "count": group.count(), "mean": group.mean()}
    )


grouped = frame.groupby(quartiles)
grouped.apply(get_stats)

                            min       max  count      mean
data1                                                     
(-2.956, -1.23] data1 -2.949343 -1.230179     94 -1.658818
                data2 -3.399312  1.670835     94 -0.033333
(-1.23, 0.489]  data1 -1.228918  0.488675    598 -0.329524
                data2 -2.989741  3.260383    598 -0.002622
(0.489, 2.208]  data1  0.489965  2.200997    298  1.065727
                data2 -3.745356  2.954439    298  0.078249
(2.208, 3.928]  data1  2.212303  3.927528     10  2.644253
                data2 -1.929776  1.765640     10  0.024750
                

grouped.agg(["min", "max", "count", "mean"])

quartiles_samp = pd.qcut(frame["data1"], 4, labels=False)
grouped = frame.groupby(quartiles_samp)
grouped.apply(get_stats)

```

### Example Missing Values with Group Specific Values

```python
s = pd.Series(np.random.standard_normal(6))
s[::2] = np.nan # sets odd places with nan

s.fillna(s.mean()) # fills nan value with mean
```

```python
states = ["Ohio", "New York", "Vermont", "Florida",
          "Oregon", "Nevada", "California", "Idaho"]

group_key = ["East", "East", "East", "East",
             "West", "West", "West", "West"]

data = pd.Series(np.random.standard_normal(8), index=states)

data[["Vermont", "Nevada", "Idaho"]] = np.nan # mark some data missing
data.groupby(group_key).size()
# ------
East    4
West    4
dtype: int64
# ------
data.groupby(group_key).count() # counts non-null rows
# ------
East    3
West    2
dtype: int64
# ------
data.groupby(group_key).mean()
# ------
East   -0.100594
West    0.960416
dtype: float64
# ------

def fill_mean(group):
    return group.fillna(group.mean())
    
data.groupby(group_key).apply(fill_mean)

### -----
Ohio          0.329939
New York      0.981994
Vermont      -0.100594
Florida      -1.613716
Oregon        1.561587
Nevada        0.960416
California    0.359244
Idaho         0.960416
dtype: float64

## ---- predefining fill values
fill_values = {"East": 0.5, "West": -1}

def fill_func(group):
    return group.fillna(fill_values[group.name])

data.groupby(group_key).apply(fill_func)
```

### Random Sampling and Permutation


```python
suits = ["H", "S", "C", "D"]  # Hearts, Spades, Clubs, Diamonds
card_val = (list(range(1, 11)) + [10] * 3) * 4
base_names = ["A"] + list(range(2, 11)) + ["J", "K", "Q"]
cards = []
for suit in suits:
    cards.extend(str(num) + suit for num in base_names)

deck = pd.Series(card_val, index=cards)

def draw(deck, n=5):
    return deck.sample(n)
    
def get_suit(card):
    # last letter is suit
    return card[-1]
    
deck.groupby(get_suit).apply(draw, n=2)
deck.groupby(get_suit, group_keys=False).apply(draw, n=2) # drop outer suit-index in output
```

### Group Weighted Average and Correlation

```python
df = pd.DataFrame({"category": ["a", "a", "a", "a",
                                "b", "b", "b", "b"],
                   "data": np.random.standard_normal(8),
                   "weights": np.random.uniform(size=8)})

grouped = df.groupby("category")

def get_wavg(group):
    return np.average(group["data"], weights=group["weights"])

grouped.apply(get_wavg)

```

###  Group-Wise Linear Regression

We can run Groupby computation using a function as long as it returns pandas object or a scalar value.

```python
import statsmodels.api as sm
def regress(data, yvar=None, xvars=None):
    Y = data[yvar]
    X = data[xvars]
    X["intercept"] = 1.
    result = sm.OLS(Y, X).fit()
    return result.params
    
# run a yearly linear regression of AAPL on SPX returns, execute:

by_year.apply(regress, yvar="AAPL", xvars=["SPX"])

## ------
           SPX  intercept
2003  1.195406   0.000710
2004  1.363463   0.004201
2005  1.766415   0.003246
2006  1.645496   0.000080
2007  1.198761   0.003438
2008  0.968016  -0.001110
2009  0.879103   0.002954
2010  1.052608   0.001261
2011  0.806605   0.001514
```

## Group Transforms and *Unwrapped* GroupBys

Transform is quite similar to `apply` but has few restrictions like

- It can produce a scalar value to be broadcast to the shape of the group
- It can produce object of the same shape as input group
- It must not mutate its input

```python
df = pd.DataFrame({'key': ['a', 'b', 'c'] * 4,
                   'value': np.arange(12.)})

   key  value
0    a    0.0
1    b    1.0
2    c    2.0
3    a    3.0
4    b    4.0
5    c    5.0
6    a    6.0
7    b    7.0
8    c    8.0
9    a    9.0
10   b   10.0
11   c   11.0

g = df.groupby('key')['value']

g.mean()

key
a    4.5
b    5.5
c    6.5
Name: value, dtype: float64

# ---
def get_mean(group):
    return group.mean()
    
g.transform(get_mean)

0     4.5
1     5.5
2     6.5
3     4.5
4     5.5
5     6.5
6     4.5
7     5.5
8     6.5
9     4.5
10    5.5
11    6.5
Name: value, dtype: float64
```

Transform ranks in descending order

```python
def get_ranks(group):
    return group.rank(ascending=False)

g.transform(get_ranks)
```

Normalize input

```python
def normalize(x):
    return (x - x.mean()) / x.std()
    
g.transform(normalize)

0    -1.161895
1    -1.161895
2    -1.161895
3    -0.387298
4    -0.387298
5    -0.387298
6     0.387298
7     0.387298
8     0.387298
9     1.161895
10    1.161895
11    1.161895
Name: value, dtype: float64

g.apply(normalize)

0    -1.161895
1    -1.161895
2    -1.161895
3    -0.387298
4    -0.387298
5    -0.387298
6     0.387298
7     0.387298
8     0.387298
9     1.161895
10    1.161895
11    1.161895
Name: value, dtype: float64

normalized = (df['value'] - g.transform('mean')) / g.transform('std')
# above unwrapped expression is much faster than writing your own function.

```
## Pivot tables and Cross Tabulation

dataframes has `pivot_table` method but Pandas has a top level `pandas.pivot_table` function.

In addition to providing a convenience interface to groupby, pivot_table can add partial totals, also known as margins.

```python

tips.head()

   total_bill   tip smoker  day    time  size   tip_pct
0       16.99  1.01     No  Sun  Dinner     2  0.059447
1       10.34  1.66     No  Sun  Dinner     3  0.160542
2       21.01  3.50     No  Sun  Dinner     3  0.166587
3       23.68  3.31     No  Sun  Dinner     2  0.139780
4       24.59  3.61     No  Sun  Dinner     4  0.146808

tips.pivot_table(index=["day", "smoker"])

                 size       tip   tip_pct  total_bill
day  smoker                                          
Fri  No      2.250000  2.812500  0.151650   18.420000
     Yes     2.066667  2.714000  0.174783   16.813333
Sat  No      2.555556  3.102889  0.158048   19.661778
     Yes     2.476190  2.875476  0.147906   21.276667
Sun  No      2.929825  3.167895  0.160113   20.506667
     Yes     2.578947  3.516842  0.187250   24.120000
Thur No      2.488889  2.673778  0.160298   17.113111
     Yes     2.352941  3.030000  0.163863   19.190588
     
## above can be replicated using
tips.groupby(["day", "smoker"]).mean()

tips.pivot_table(index=["time", "day"], columns="smoker",
                 values=["tip_pct", "size"])

                 size             tip_pct          
smoker             No       Yes        No       Yes
time   day                                         
Dinner Fri   2.000000  2.222222  0.139622  0.165347
       Sat   2.555556  2.476190  0.158048  0.147906
       Sun   2.929825  2.578947  0.160113  0.187250
       Thur  2.000000       NaN  0.159744       NaN
Lunch  Fri   3.000000  1.833333  0.187735  0.188937
       Thur  2.500000  2.352941  0.160311  0.163863
       
```

We could augment this table to include partial totals by passing `margins=True`. This has the effect of adding All row and column labels, with corresponding values being the group statistics for all the data within a single tier

```python
tips.pivot_table(index=["time", "day"], columns="smoker",
                 values=["tip_pct", "size"], margins=True)

# -----
                 size                       tip_pct                    
smoker             No       Yes       All        No       Yes       All
time   day                                                             
Dinner Fri   2.000000  2.222222  2.166667  0.139622  0.165347  0.158916
       Sat   2.555556  2.476190  2.517241  0.158048  0.147906  0.153152
       Sun   2.929825  2.578947  2.842105  0.160113  0.187250  0.166897
       Thur  2.000000       NaN  2.000000  0.159744       NaN  0.159744
Lunch  Fri   3.000000  1.833333  2.000000  0.187735  0.188937  0.188765
       Thur  2.500000  2.352941  2.459016  0.160311  0.163863  0.161301
All          2.668874  2.408602  2.569672  0.159328  0.163196  0.160803
```

Here, the All values are means without taking into account smoker versus non-smoker (the All columns) or any of the two levels of grouping on the rows (the All row).

To use an aggregation function other than mean, pass it to the `aggfunc` keyword argument.

If some combinations are empty (or otherwise NA), you may wish to pass a `fill_value`

### Cross-Tabulations: Crosstab

```python
from io import StringIO

data = """Sample  Nationality  Handedness
1   USA  Right-handed
2   Japan    Left-handed
3   USA  Right-handed
4   Japan    Right-handed
5   Japan    Left-handed
6   Japan    Right-handed
7   USA  Right-handed
8   USA  Left-handed
9   Japan    Right-handed
10  USA  Right-handed"""

data = pd.read_table(StringIO(data), sep="\s+")

# --------
   Sample Nationality    Handedness
0       1         USA  Right-handed
1       2       Japan   Left-handed
2       3         USA  Right-handed
3       4       Japan  Right-handed
4       5       Japan   Left-handed
5       6       Japan  Right-handed
6       7         USA  Right-handed
7       8         USA   Left-handed
8       9       Japan  Right-handed
9      10         USA  Right-handed

# ------
pd.crosstab(data["Nationality"], data["Handedness"], margins=True)

Handedness   Left-handed  Right-handed  All
Nationality                                
Japan                  2             3    5
USA                    1             4    5
All                    3             7   10

# ----------
pd.crosstab([tips["time"], tips["day"]], tips["smoker"], margins=True)

smoker        No  Yes  All
time   day                
Dinner Fri     3    9   12
       Sat    45   42   87
       Sun    57   19   76
       Thur    1    0    1
Lunch  Fri     1    6    7
       Thur   44   17   61
All          151   93  244

```