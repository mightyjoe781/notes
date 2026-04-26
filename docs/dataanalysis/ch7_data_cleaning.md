# Data Cleaning and Preparation

## Handling Missing Data

For data with `float64` dtype, pandas uses the floating value `NaN` to represent missing data.

```python
float_data = pd.Series([1.2, -3.4, np.nan, 0])
float_data.isna() # [False, False, True, False]

# NOTE: None values are also treated as NA (not available), either data doesn't exist or could not be observed.
```


| Methods  | Description                                                                                                                                 |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `dropna` | Filter axis labels based on whether values for each label have missing data, with varying thresholds for how much missing data to tolerate. |
| `fillna` | fill in missing data with some value or using interpolation methods such as `ffill` or `bfill`                                              |
| `isna`   | Return Boolean values indicating which values are missing/NA                                                                                |
| `notna`  | Negative of `isna`                                                                                                                          |

### Filtering Out Missing Data

```python

import pandas as pd
import numpy as np

data = pd.Series([1, np.nan, 3.5, np.nan, 7])
data.dropna() # or data[data.notna()]

## -------
0    1.0
2    3.5
4    7.0
dtype: float64
```

With DataFrame there are many ways to remove missing data.

```python
data = pd.DataFrame([[1., 6.5, 3.], [1., np.nan, np.nan],[np.nan, np.nan, np.nan], [np.nan, 6.5, 3.]])

# ---------
	0	1	2
0	1.0	6.5	3.0
1	1.0	NaN	NaN
2	NaN	NaN	NaN
3	NaN	6.5	3.0
# ---------
# remove any rows containing NaN
data.dropna() # same as data.dropna(how="any")
# ---------
	0	1	2
0	1.0	6.5	3.0
# ---------
# remove only rows with all columns as NaN
data.dropna(how="all")
# ---------
  0	1	2
0	1.0	6.5	3.0
1	1.0	NaN	NaN
3	NaN	6.5	3.0
# ---------

```

NOTE: Above functions always return new objects, they do not modify the original. Pass `axis="columns"` to operate in the columnar direction.

To set custom threshold (tolerance) of NaN values in the row/column use following.

```python
# keep only rows containing at most 2 missing observation
df.dropna(thresh=2)
```
### Filling Out Missing Data

```python
# fill missing data with default values
df.fillna(0)

# define different values for different columns by defining dict
df.fillna({1: 0.5, 2: 0})

# you can use interpolation like ffill (forward-fill) with threshold as well
df.fillna(method="ffill")
df.fillna(method="ffill", limit=2)

# commonly we usually fill missing data with mean
df.fillna(df.mean())
```

NOTE: you can define `axis` as well for above function.
## Data Transformation

### Removing Duplicates

```python
data = pd.DataFrame({"k1": ["one", "two"] * 3 + ["two"], "k2": [1, 1, 2, 3, 3, 4, 4]})

data.duplicated() # Return Boolean Array for duplicated data set as True

data.drop_duplicates() # drops/filters True values from above duplicated function

# by default all columns are used to detect duplicates
data.drop_duplicates(subset=["k1"])

# by default both above function consider first entry as original, preserved
# for last entry
data.drop_duplicates(["k1", "k2"], keep="last")
```

### Transforming Data Using a Function or Mapping

Mapping to add distinct types using `map`

```python
data = pd.DataFrame({"food": ["bacon", "pulled pork", "bacon","pastrami", "corned beef", "bacon","pastrami", "honey ham", "nova lox"],"ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})

### ------

food	ounces
0	bacon	4.0
1	pulled pork	3.0
2	bacon	12.0
3	pastrami	6.0
4	corned beef	7.5
5	bacon	8.0
6	pastrami	3.0
7	honey ham	5.0
8	nova lox	6.0

### --------

meat_to_animal = {"bacon": "pig", "pulled pork": "pig", "pastrami": "cow", "corned beef": "cow", "honey ham": "pig", "nova lox": "salmon"}

data["animal"] = data["food"].map(meat_to_animal)
data


food	ounces	animal
0	bacon	4.0	pig
1	pulled pork	3.0	pig
2	bacon	12.0	pig
3	pastrami	6.0	cow
4	corned beef	7.5	cow
5	bacon	8.0	pig
6	pastrami	3.0	cow
7	honey ham	5.0	pig
8	nova lox	6.0	salmon
```

### Replacing Values

```python
# assume -999, -1000 were placeholders(sentinals) for NA data
data = pd.Series([1., -999., 2., -999., -1000., 3.])

# we can replace them using replace function
data.replace(-999, np.nan)

# replacing multiple values
data.replace([-999, -1000], np.nan)

# passing substitution lists or dictionary
data.replace([-999, -1000], [np.nan, 0])
data.replace({-999: np.nan, -1000:0})

```

### Renaming Axis Indices

Axis indices can be renamed as well, Capitalize or UpperCase.

```python
def transform(x):
    return x[:4].upper()
    
data.index.map(transform) # modifies original dataframe
data.rename(index=str.title, columns=str.upper) # modifies a copy
```

### Discretization and Binning

```python

ages = [12, 15, 20, 21, 21, 40, 41, 32, 30, 25, 28, 32, 31, 30, 29, 30, 31]

bins = [0, 18, 25, 35, 60, 100]
cats = pd.cut(ages, bins) # special Categorical Object
cats

### -----
[(0, 18], (0, 18], (18, 25], (18, 25], (18, 25], ..., (25, 35], (25, 35], (25, 35], (25, 35], (25, 35]]
Length: 17
Categories (5, interval[int64, right]): [(0, 18] < (18, 25] < (25, 35] < (35, 60] < (60, 100]]

### ------
cats.codes
# array([0, 0, 1, 1, 1, 3, 3, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2], dtype=int8)

cats.categories
# IntervalIndex([(0, 18], (18, 25], (25, 35], (35, 60], (60, 100]], dtype='interval[int64, right]')

## ---- custom labeling cuts
group_names = ["Youth", "YoungAdult", "MiddleAged", "Senior", "Old"]
cats = pd.cut(ages, bins, labels=group_names)
cats

# ['Youth', 'Youth', 'YoungAdult', 'YoungAdult', 'YoungAdult', ..., 'MiddleAged', 'MiddleAged', 'MiddleAged', 'MiddleAged', 'MiddleAged']
# Length: 17
# Categories (5, str): ['Youth' < 'YoungAdult' < 'MiddleAged' < 'Senior' < 'Old']

```

Note if we don't pass bins, `cut` can categorize using min, max values in data.

```python
data = np.random.uniform(size=20)
pd.cut(data, 4, precision=2)

## ----
# [(0.51, 0.75], (0.27, 0.51], (0.034, 0.27], (0.27, 0.51], (0.75, 0.98], ..., (0.51, 0.75], (0.75, 0.98], (0.51, 0.75], (0.034, 0.27], (0.034, 0.27]] Length: 20 Categories (4, interval[float64, right]): [(0.034, 0.27] < (0.27, 0.51] < (0.51, 0.75] < (0.75, 0.98]]
```

NOTE: `qcut` can categories data based on sample quantiles, resulting in roughly similar distribution as compared to `cut` uniform binning.
### Detecting and Filtering Outliers

```python
data = pd.DataFrame(np.random.standard_normal((1000, 4)))
data.describe()

# finding values in any column exceeding 3
col = data[2]
col[col.abs() > 3] # outliers

# for dataframe we can use any method as well on Boolean DataFrame
data[(data.abs() > 3).any(axis="column")]

# to restrict data in range -3, 3
data[data.abs() > 3] = np.sign(data) * 3

# to print frame data +1/-1 based on sign of data
np.sign(data).head()

```
### Permutation and Random Sampling

```python
df = pd.DataFrame(np.arange(5 * 7).reshape((5, 7)))

sampler = np.random.permutation(5) # array([3, 1, 4, 2, 0]) ~ indices

df.take(sampler) # or df.take(sampler, axis="columns")
df.iloc[sampler]

# to select random subset without replacement
df.sample(n = 3) # select any 3 rows

# generate sample with replacement
choices = pd.Series([5, 7, -1, 6 ,4])
choices.sample(n=10, replace=True)
```

### Computing Indicator/Dummy Variables

If a column in DataFrame has `k` distinct values, you would derive a matrix or DataFrame with `k` columns contains all `1` and `0`.

Its pretty common in data science, **One-Hot Encoding** (or **One-Hot Vectorization**).

```python
df = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"], "data1": range(6)})

# -----
	key	data1
0	b	0
1	b	1
2	a	2
3	c	3
4	a	4
5	b	5
# -----
pd.get_dummies(df["key"])

	a	b	c
0	False	True	False
1	False	True	False
2	True	False	False
3	False	False	True
4	True	False	False
5	False	True	False

## --- prefixing column with some text
pd.get_dummies(df["key"], prefix="key")

	key_a	key_b	key_c
0	False	True	False
...

```

Quite often we combine `pandas.cut` with `pandas.get_dummies` to discretize the interval and then do One Hot Encoding on a range of numbers divided by bins (helps to avoid having too many `k` features)
## Extension Data Types

Earlier Pandas was developed as an extension to NumPy, because of which is deals with uncanny typecasting issues which is mostly unchanged due to legacy reasons.

Pandas support defining Data Types treated as First Class Citizens in library and has many newer implementations.

```python
s = pd.Series([1, 2, 3, None])
s

# ---
0 1.0
1 2.0
2 3.0
3 NaN
dtype: float64
```

NOTE: How integers are typecasted into float, and None into NaN by default in Series for backwards compatibility.

```python
s = pd.Series([1, 2, 3, None], dtype=pd.Int64Dtype()) # can use Int64 shorthand

# ---
0 1
1 2
2 3
3 <NA> # special Pandas sentinels
dtype: Int64

```

Pandas also supports specialized for string data without using NumPy objects array (*requires `pyarrow`*)

```python
s = pd.Series(["one", "two", None, "three"], dtype=pd.StringDtype())
```

Another important extension type is `Categorical` discussed above. `astype` is useful to cleanup data types.

```python
df = pd.DataFrame({"A": [1, 2, None, 4],"B": ["one", "two", "three", None],"C": [False, None, False, True]})

df["A"] = df["A"].astype("Int64")
df["B"] = df["B"].astype("string")
df["C"] = df["C"].astype("boolean")
df
```
## String Manipulation

### Python Built-in String Object Methods


| Method                      | Descriptions                                                                                                                                                |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `count`                     |                                                                                                                                                             |
| `endswith`                  |                                                                                                                                                             |
| `startswith`                |                                                                                                                                                             |
| `join`                      |                                                                                                                                                             |
| `index`                     | Return starting index of the first occurrence of passed substring if found in the string; otherwise, raises ValueError if not found                         |
| `find`                      | Return position of first character of first occurrence of substring in the string; like index, but returns –1 if not found                                  |
| `rfind`                     | Return position of first character of last occurrence of substring in the string; returns –1 if not found                                                   |
| `replace`                   |                                                                                                                                                             |
| `strip`, `rstrip`, `lstrip` | Trim whitespace, including newlines on both sides, on the right side, or on the left side, respectively                                                     |
| `split`                     |                                                                                                                                                             |
| `lower`                     |                                                                                                                                                             |
| `upper`                     |                                                                                                                                                             |
| `casefold`                  | Convert characters to lowercase, and convert any region-specific variable character combinations to a common comparable form                                |
| `ljust`, `rjust`            | Left justify or right justify, respectively; pad opposite side of string with spaces (or some other fill character) to return a string with a minimum width |
|                             |                                                                                                                                                             |

### Regular Expressions


| Method        | Description                                                                                                                                                                                  |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `findall`     | Return all nonoverlapping matching patterns in a string as a list                                                                                                                            |
| `finditer`    | Like findall, but returns an iterator                                                                                                                                                        |
| `match`       | Match pattern at start of string and optionally segment pattern components into groups; if the pattern matches, return a match object, and otherwise None                                    |
| `search`      | Scan string for match to pattern, returning a match object if so; unlike match, the match can be anywhere in the string as opposed to only at the beginning                                  |
| `split`       | Break string into pieces at each occurrence of pattern                                                                                                                                       |
| `sub`, `subn` | Replace all (`sub`) or first `n` occurrences (`subn`) of pattern in string with replacement expression; use symbols `\1, \2, ...` to refer to match group elements in the replacement string |
|               |                                                                                                                                                                                              |

### String Functions in Pandas

```python
data = {"Dave": "dave@google.com", "Steve": "steve@gmail.com", "Rob": "rob@gmail.com", "Wes": np.nan}
data = pd.Series(data) # dtype: obj

data.isna() # returns boolean series

# String and regular expression methods can be applied (passing a `lambda` or other function) to each value using `data.map`, but it will fail on the NA (null) values. To cope with this, Series has array-oriented methods for string operations that skip over and propagate NA values. These are accessed through Series’s `str` attribute;

data.str.contains("gmail")

data_as_string_ext = data.astype('string') # dtype: string
data_as_string_ext.str.contains("gmail")

pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"

data.str.findall(pattern, flags=re.IGNORECASE)

## ----
Dave     [(dave, google, com)]
Steve    [(steve, gmail, com)]
Rob        [(rob, gmail, com)]
Wes                        NaN
dtype: object
## ----

matches = data.str.findall(pattern, flags=re.IGNORECASE).str[0] # splits the array
matches.str.get(1) # only first entry

# returns captured groups as df
data.str.extract(pattern, flags=re.IGNORECASE)

# ----
           0       1    2
Dave    dave  google  com
Steve  steve   gmail  com
Rob      rob   gmail  com
Wes      NaN     NaN  NaN
## -----


```

## Categorical Data

### Background and Motivation

### Categorical Extension Type in pandas

### Computations with Categoricals

### Categorical Methods

