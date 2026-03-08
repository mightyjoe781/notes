# NumPy Basics
*Arrays and Vectorized Computations*

*NumPy* is short for *Numerical Python*

Features of NumPy

- `ndarray`, an efficient multi-dimensional array providing fast array-oriented arithmetic operations and flexible *broadcasting* capabilities.
- Mathematical functions for fast operations on entire array of data without having to write loops
- Tools for reading/writing array data to disk and working with memory-mapped files
- Linear Algebra, random number generation, and FFT
- A C API for connecting NumPy with libraries written in C, C++, or FORTRAN

Internals of NumPy

- NumPy internally stores data in a contiguous block memory, independent of other built-in objects, library of C language can operate in this memory very fast without any type checking or other overheads. Takes less memory than a list.
- NumPy can perform complex computation on entire array without the need for Python `for` loops, which could be slow for large sequences.

```python

import numpy as np
import timeit

my_array = np.arange(1_000_000)
my_list = list(range(1_000_000))

def multiply_array():
    return my_array * 2

def multiply_list():
    return [x * 2 for x in my_list]

array_time = timeit.timeit(multiply_array, number=100)
list_time = timeit.timeit(multiply_list, number=100)

print(f"Array multiplication time: {array_time:.4f} seconds")
print(f"List multiplication time: {list_time:.4f} seconds")

# Array multiplication time: 0.0575 seconds 
# List multiplication time: 2.5690 seconds

```

## The NumPy ndarray

`ndarray` : fast, flexible container for large datasets in Python. Arrays enable to perform mathematical operations on whole blocks of data using syntax similar to equivalent operations between scalar elements.

```python

import numpy as np

data = np.array([[1.5, -0.1, 3], [0, -3, 6.5]])
print(data)

print(data * 10)
print(data + data)
```

```
[[ 1.5 -0.1  3. ]
 [ 0.  -3.   6.5]]
[[ 15.  -1.  30.]
 [  0. -30.  65.]]
[[ 3.  -0.2  6. ]
 [ 0.  -6.  13. ]]
```

`ndarray` is a generic multidimensional container for homogeneous data, Every array has a *shape*, a tuple indication size of each dimension, and a *dtype* : an object describing the *data type* of the array.

```python
data.shape # (2, 3)
data.dtype # dtype('float64')

```

Creating `ndarray`

```python

data1 = [1, 2, 3, 4, 5]
arr1 = np.array(data1)

# nested lists are converted into multidimensional array
data2 = [[1, 2, 3, 4], [4, 5, 6, 9]]
arr2 = np.array(data2)
arr2.shape # (2, 4)
arr2.ndim # 2

# by default data types are infered
```

Other than above method there are 4 more methods to create arrays

```python
np.zeroes(10) # array([0., 0., ....])
np.zeroes((3, 6)) # 3x6 array of zeroes

np.empty((2, 3, 2)) # 2 3x2 arrays of uninitialized memory

# NOTE: numpy.empty always doesn't return zero

np.arange(15) # arrays of range(0, 15)
```

### Data Types for ndarrays

*data type* of *dtype* is a special object containing the information (or *metadata*, data about data) the ndarray needs to interpret a chunk of memory as a particular type of data.

```python
arr1.dtype # dtype('float64')
arr2.dtype # dtype('int32')
```

[Full Data Types List](https://numpy.org/devdocs/user/basics.types.html#relationship-between-numpy-data-types-and-c-data-types)

Arrays can be *casted* or converted into anther type using `ndarray` `astype` method

```python
arr = np.array([1, 2, 3, 4, 5])
arr.dtype # dtype('int64')

float_arr = arr.astype(np.float64)
float_arr.dtype # dtype('float64')

## example converting strings into numbers
num_strings = np.array(["1.25", "-9.6", "25"])
num_strings.astype(float) # array([1.25, -9.6, 25.]) # notice float is aliased internally to float64
```

We can use other array's `dtype` as well

```python
int_arr = np.arange(10)
flt_arr = np.array([.22, .207, .348], dtype=np.float64)

int_arr.astype(flt_arr.dtype)
```

We can use shorthand as well

```python
zeroes_uint32 = np.zeroes(8, dtype="u4")

zeroes_uint32 # array([0, 0, 0, 0, 0, 0, 0, 0], dtype=uint32)
```

### Arithmetic with NumPy Arrays

Arrays allow to express batch operations on data without writing any `for` loops, NumPy users call this *vectorization*

Any arithmetic operations between equal-size arrays apply the operations element wise.

```python
arr = np.array([[1., 2., 3.], [4., 5., 6.]])
print(arr)
print(arr * arr)
print(arr - arr)
```

```
[[1. 2. 3.]
 [4. 5. 6.]]
[[ 1.  4.  9.]
 [16. 25. 36.]]
[[0. 0. 0.]
 [0. 0. 0.]]
```

Operations involving scalars propagate scalar argument to each element in the array.

```python
print(1/arr)

print(arr ** 2)
```

```
[[1.         0.5        0.33333333]
 [0.25       0.2        0.16666667]]
[[ 1.  4.  9.]
 [16. 25. 36.]]
```

Comparisons between arrays yield same size Boolean Arrays.

```python
arr2 = np.array([[0., 4., 1.], [7., 2., 12.]])
print(arr2)
print(arr2 > arr)
```

```
[[ 0.  4.  1.]
 [ 7.  2. 12.]]
[[False  True False]
 [ True False  True]]
```

### Basic Indexing and Slicing

Evaluating operations between differently sized arrays is called as *broadcasting*

```python

arr = np.arange(10)
print(arr) # [0 1 2 3 4 5 6 7 8 9]
print(arr[5]) # 5
print(arr[5:8]) # [5 6 7]
print(arr[5:8] + arr[0:3]) # [5 6 7] + [0 1 2] = [5 7 9]
arr[5:8] = 12 # arr[5:8] = [12, 12, 12]
print(arr) # [ 0  1  2  3  4 12 12 12  8  9]
```

NOTE: An important first distinction from Python's built-in lists is that array slices are views on the original array. Meaning data is not copies, and changes to view are reflected in original array.

```python
arr_slice = arr[5:8]
print(arr_slice) # [12 12 12]
arr_slice[1] = 12345
print(arr) # [ 0, 1, 2, 3, 4, 12, 12345, 12, 8, 9]

# bare slice assignment
arr_slice[:] = 64
print(arr) # [ 0 1 2 3 4 64 64 64 8 9]
```

To create a copy of the slice rather than view, you should explicitly need to use copy the array. for example, `arr[5:8].copy()`

With multiple dimensional arrays, you have many more options to access nested list elements, each dimensional array is indicated by index.

```python
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print(arr2d[0]) # [1 2 3]
print(arr2d[0][2]) # 3
print(arr2d[0, 2]) # 3
```

In multi-dimensional arrays, if you omit later indices, the returned object will be lower dimensional ndarray consisting of all the data along the higher dimensions. So in the array `arr3d`

```python
arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(arr3d)

print(arr3d[0]) # [[1 2 3] [4 5 6]]
print(arr3d[0][1]) # [4 5 6]

# Both scalar values and arrays can be assigned to arr3d[0]
old_values = arr3d[0].copy()
arr3d[0] = 42
print(arr3d)

# [[42 42 42]
#  [42 42 42]]
# [[ 7  8  9]
#  [10 11 12]]
```

Similarly, `arr3d[1, 0]` gives you all of the values whose indices start with `(1, 0)`, forming 1d-array.

```python
arr3d[1, 0]
# array([7, 8, 9])
```

NOTE: all these subsection of array that have been selected are views in array.

### Indexing with slices

Like one-dimensional objects such as Python lists, `ndarrays` can be slices with the familiar syntax

```python
arr # array([ 0, 1, 2, 3, 4, 12, 12, 12, 8, 9])
arr[1:6] # array([ 1, 2, 3, 4, 12])
```

Consider the two-dimensional array from before `arr2d`, slicing is bit different.

```python
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr2d[:2] # [[1 2 3] [4 5 6]]
```

It has slices along axis 0, the first axis. A slice, therefore, selects a range of elements along an axis. It can be helpful to read the expression `arr2d[:2]` as *select first two rows of `arr2d`*

Passing Multiple slices as multiple indexes.

```python
arr2d[:2, 1:]

# [[2, 3]
#   [5, 6]]
```

Slicing and indexing to get lower dimensional slice.

```python
lower_dim_slice = arr2d[1, :2]

# [4, 5]
lower_dim_slice.shape # (2, )

# selecting third column, but only first two rows
arr2d[:2, 2]

# 
arr2d[:, :1]

# array([[1],
#        [4],
#        [7]])

# we can assign to slices to fill out values
```

### Boolean Indexing

```python
# Assume given

names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14]])

# each name corresponds to a slice

# we want to select data where name is Bob
# Boolean indexing

names == 'Bob' # [ True False False True False False False]
data[names == 'Bob'] # [[1 2] [7 8]]
data[names == 'Bob', 1:] # [[2] [8]]

# to select everything other than Bob
data[names != 'Bob']

```

```python

# using ~ operator
cond = names == "Bob"
data[~cond]
```

```python
# constructing bigger mask
mask = (names == "Bob") | (names == "Will") # [True, False, True, ....]
data[mask]
```

This is quite similar to `itertools.compress`

NOTE: Python keywords like `and` and `or` doesn't work with Boolean Arrays. Use `&` and `|`

```python
# set all negative values to zero
data[data < 0] = 0

# set all rows/columns using 1d Boolean Array
data[names != "Joe"] = 7
```

### Fancy Indexing

```python
# 8x4 zero array
arr = np.zeros((8, 4))

for i in range(8):
    arr[i] = i
    
# [[0. 0. 0. 0.] [1. 1. 1. 1.] [2. 2. 2. 2.] [3. 3. 3. 3.] [4. 4. 4. 4.] [5. 5. 5. 5.] [6. 6. 6. 6.] [7. 7. 7. 7.]]

arr[[4, 3, 0, 6]] # [[4. 4. 4. 4.] [3. 3. 3. 3.] [0. 0. 0. 0.] [6. 6. 6. 6.]]
# we can pass negative indexes to select values from end

```

```python
arr = np.arange(32).reshape((8, 4))

print(arr)
# [[ 0 1 2 3] [ 4 5 6 7] [ 8 9 10 11] [12 13 14 15] [16 17 18 19] [20 21 22 23] [24 25 26 27] [28 29 30 31]]
arr[[1, 5, 7, 2], [0, 3, 1, 2]] # [ 4, 23, 29, 10]
```

### Transposing Arrays and Swapping Axes

```python
arr = np.arange(15).reshape((3, 5))
arr
arr.T
```

Calculating inner matrix product using `numpy.dot`

```python
np.dot(arr.T, arr)

# alternatively use @ operator
arr.T @ arr
```

NOTE: `.T` simple transpose is special case of swapping axes. `ndarray` has the method *swapaxes*, which takes a pair of axis numbers and switches the indicated axes to rearrange data.

```python
arr = np.arange(10).reshape((2, 5)) # [[0 1 2 3 4] [5 6 7 8 9]]
print(arr)
arr.swapaxes(1, 0) # [[0 5] [1 6] [2 7] [3 8] [4 9]]
```
## Pseduorandom Number Generation

The `numpy.random` module supplements the built-in Python `random` module with functions for efficiently generating whole arrays of sample values from many kinds of probability distributions.

```python
samples = np.random.standard_normal(size=(4, 4))
```

In contrast python built-in `random` module samples only one value,

NOTE: These random numbers are *pseudorandom*, generated by configurable random number generator that determines deterministically what values are created.

```python

# explicit generator
rng = np.random.default_rng(seed=12345)
data = rng.standard_normal((2, 3))
```

Other important Python random number generator methods. *permutations*, *shuffle*, *uniform*, *integers*, *standard_normal*, *binomial*, *normal*, *beta*, *chisquare*, *gamma*, *uniform*

## Universal Functions: Fast Element Wise Array Functions

A universal function, or *ufunc* is a function that performs element-wise operations on data in `ndarray`, vectorized wrappers for simple functions that take one or more scalar values and produce one or more scalar results.

Ex - `numpy.sqrt`, `numpy.exp`

```python
arr = np.arange(1)
np.sqrt(arr)
np.exp(arr)
```

Other binary *ufuncs* are `numpy.add`, `numpy.maximum`

```python
x = rng.standard_normal(8)
y = rng.standard_normal(8)
np.maximum(x, y) # computes elementwise maximum of elements in x and y
```

A *ufunc* can return multiple arrays, e.g. `numpy.modf` ~ returns fractional and integral parts of floating point array.

```python
arr = rng.standard_normal(7) * 5
rem, quo = np.modf(arr)
```

`ufunc` supports `out` argument allows them to assign their results into an existing array rather than creating new one.

```python
out = np.zeros_like(arr)
np.add(arr, 1)
np.add(arr, 1, out=out)
```

[Universal Function](https://numpy.org/doc/stable/user/basics.ufuncs.html)
## Array-Oriented Programming with Arrays

Using NumPy enables to think of many data processing tasks as concise array expression, avoiding writing loops.
The practice is often referred as *vectorization*

A simple example to evaluate : `sqrt(x^2 + y^2)` across regular grid of values

```python
points = np.arange(-5, 5, 0.01) # 100 equally spaced points

xs, ys = np.meshgrid(points, points)

z = np.sqrt(xs ** 2 + ys ** 2)
```

### Expressing Conditional Logic as Array Operations

```python
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])

cond = np.array([True, False, True, True, False])

# Pythonic
res = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]

# Numpy
res = np.where(cond, xarr, yarr)
```

Example

```python
arr = rng.standard_normal((4, 4))

np.where(arr > 0, 2, -2) # extract subgrid, assign 2 for positive, -2 for negative

# setting only positive values
np.where(arr > 0, 2, arr)
```


### Mathematical and Statistical Methods

A set of mathematical functions that compute statistics about an entire array or about the data along an axis are accessible as methods of the array class.

You can use aggregation (sum, mea, std) *(reductions)* either by calling array instacne or using top-level NumPy functions.

```python
arr = rng.standard_normal((5, 4))

arr.mean() # or
np.mean(arr)

arr.sum()
```

NOTE: functions like `mean` and `sum` take extra optional axis argument that computes statistics over given axis, resulting in an array with one less dimension

```python
arr.mean(axis = 1)
```

Accumulation functions like `cumsum` return an array of the same size but with partial aggregates computed along the indicated axis according to each lower dimensional slice

```python
arr = np.array([[0, 1. 2], [3, 4, 5], [6, 7, 8]])

arr.cumsum(axis = 0)
arr.cumsum(axis = 1)
```

### Methods for Boolean Arrays

```python

arr = rng.standard_normal(100)

(arr > 0).sum() # number of positive values
(arr <= 0).sum() # number of non-positive values

bools = np.array([False, False, True, False])

bools.any() # True
bools.all() # False
```

### Sorting

```python
arr = rng.standard_normal(6)

arr.sort()

# multi-dimensional sort along axis
arr = rng.standard_normal((5, 3))
arr.sort(axis=0) # sorts values in each column
arr.sort(axis = 1) # sorts across each rows

# np.sort ~ return copy of sorted data
arr2 = np.array([5, -10, 7, 1, 0, -3])
sorted_arr2 = np.sort(arr2)

sorted_arr2 is arr2 # False
```

### Unique and Other Set Logic

```python
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])

np.unique(names) # array(['Bob', 'Joe', 'Will'], dtype='<U4')

# compared with pure python alternative its very fast
sorted(set(names))

# numpy.in1d tests membership very fast
values = np.array([6, 0, 0, 3, 2, 5, 6])
np.in1d(values, [2, 3, 6])
# array([True, False, False, True, True, False, True])
```
## File Input and Output with Arrays

NumPy is able to save and load data to and from disk in some text or binary formats.

```python
arr = np.arange(10)
np.save("some_array", arr) # create some_array.npy file

np.load("some_array.npy")
# arr([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
```

Saving multiple arrays in an uncompressed archive using `numpy.savez`

```python
np.savez("array_archive.npz", a=arr, b=arr)
```

When loading we get dictionary like object

```python
arch = np.load("array_archive.npz")

arch["b"]
# array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
```

If your data compresses well, use `np.savez_compressed`
## Linear Algebra

Linear algebra operations like *matrix multiplication*, *decompositions*, *determinants*, and other square matrix math, are an important part of many array libraries.

```python

x = np.array([[1,2, 3], [4, 5, 6]])
y = np.array([[6, 23.], [-1, 7], [8, 9]])

x.dot(y) # same as np.dot(x, y)

from numpy.linalg import inv, qr # inverse, determinants

x = rng.standard_noarml((5, 5))
mat = X.T @ X 

inv(mat)

mat @ inv(mat) # equals identity matrix

```

## Example : Random Walks

*Simulation Example*

```python
import random
position = 0
walk = [position]

nsteps = 1000
for i in range(nsteps):
    step = 1 if random.randint(0, 1) else -1
    position += step
    walk.append(position)
    
# drawing
from matplotlib import pyplot as plt
plt.plot(walk[:100])
```

Walk is cumulative sum of random steps and could be evaluated using array expression. We perform 1000 coin flips at once, setting them to 1, -1 and compute cumulative sum.

![](assets/Pasted%20image%2020260301170529.png)

```python

nsteps = 1000
rng = np.random.default_rng(seed=12345)

draws = rng.integers(0, 2, size=nsteps)
steps = np.where(draws > 0, 1, -1)
walk = steps.cumsum()

# maximum displacement
walk.max()

# minimum displacement
walk.min()

# first crossing of 10 or -10
(np.abs(walk) >= 10).argmax()
```