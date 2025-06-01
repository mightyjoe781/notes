# Python Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: python
This is part 1 of 1 parts

---

## File: python/ch1.md

## Chapter 1: Getting Started

Python is a cross-platform programming language, which means it runs on all major OS.

#### Installing Python

- Windows : Visit [Link](https://python.org/downloads)
- MacOS: `brew install python3`
- Linux: `sudo apt install python3`

Checking python version : Execute `python` or `python3` and notice its version. Now you are in `>>>` prompt where you can start executing Python commands. To exit type `exit()` or `ctrl+D`. Alternatively you could execute `python3 --version` on terminal.

In case you have python version 2.x then try again installing latest verision.

#### Running hello_world.py

Create a empty file `hello_world.py` with contents.

```python
print("Hello Python world!")
```

Execute : `python3 hello_world.py`

## Chapter 2: Variables and Simple Data Types

#### Variables

Now modify `hello_world.py` with following content and run program again.

```python
message = "Hello Python world!"
print(message)
```

#### Naming and Using Variables

Rules and General Ideas to name variables.

- Variable names can only contain `letters`, `numbers`, and `underscores` and cannot start with numbers.
- Spaces are not allowed in variable names.
- Avoid using keywords and function names as variable names, they are reserved for particular programmatic purpose.
- Variable names should be short but descriptive.
- Be careful when using lowercase letter `l` and uppercase `O`, because they can be confused with number 1 or 0.
- Avoid Name errors when using variables.



---

## File: python/ch1_1.md

## Python Data Model

- Python Data Model is an API that we use to make our objects play well with the most idiomatic language features
- Its more like a description of Python as a framework which formalizes the interfaces of the building blocks of the language itself like sequences, functions, iterators, coroutines etc
- Example : `obj[key]` this syntax is supported by a special dunder method `__getitem__`.
- These functions are meant to be called by python interpretor. for e.g. `len(obj)` is used to get length not `obj.__len__()`.

NOTE: sometimes python interpretor takes shortcut when dealing with builtin types like `list`, `str`, `bytearray` using `PyVarObject` which has `ob_size` field holding number of items in collections.

- `for i in x:` invokes `iter(x)` which in turn calls `x.__iter__()` if its available
- Users should not call these unless they are doing Metaprogramming.

#### Important uses of special methods:

- Emulating Numeric Types

Implementing Vector Class

````python
import math

class Vector:
  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y
  
  # string representation of class
  # !r calls standard representation of attributes to be displayed
  # it shows difference b/w Vector(1, 2) and Vector('1', '2')
  def __repr__(self):
    return f"Vector({self.x!r}, {self.y!r})"
  
  def __abs__(self):
    return math.hypot(self.x, self.y)
  
  def __bool__(self):
    return bool(abs(self))
  
  # implements + operator
  def __add__(self, other):
    x = self.x + other.x
    y = self.y + other.y
    return Vector(x, y)
  
  # implements * operator
  def __mul__(self, scalar):
    return Vector(self.x * scalar, self.y * scalar)
````

- String Representation of objects

`__str__` is called by `str()` built-in and implicitly used by `print` functions.

NOTE: `__repr__` is fallback for `__str__`. But as a practice implement former always. https://fpy.li/1-5

- Boolean Value of an Object

Although `bool` type is supported in python but accepts any object in a Boolean context. To find whether `x` is truthy or falsy, python applies `bool(x)` which return True or False.

By default instances of user-defined classes are truthy, unless `__bool__` or `__len__` is implemented.

- Implementing Collection

![UML class diagram with all superclasses and some subclasses of `abc.Collection`](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_0102.png)

All of these classes are ABCs (abstract base classes).

Each of the top ABCs has a single special method

- `Iterable` to support `for`, `unpacking` and other forms of iteration
- `Sized` to support the `len` built-in function
- `Container` to support the `in` operator

There is no need for a class to inherit from any of these ABCs, any class that implements `__len__` satisfies `Sized` interface.



---

## File: python/ch1_2.md

## An Array of Sequences

There are two types of Sequences

- Container Sequences : `list`, `tuple`, and `collections.deque` : holds references to object it contains (of any type)
- Flat Sequences : `str`, `bytes`, and `array.array` : stores the value of its contents in its own memory space (space efficient but can only hold primitive types)

Another way of grouping sequence is by mutability

- Mutable Sequence (changed) : `list`, `bytearray`, `array.array` and `collections.deque`
- Immutable Sequence : `tuple`, `str` and `bytes`

NOTE:  mutable sequences inherit all methods from immutable sequences and implement several additional methods.

### List Comprehension

Example : build a list of unicode characters

````python
symbols = 'abcde'
codes = [ord(symbol) for symbol in symbols]
print(codes)

# using a loop
# codes = []
# for symbol in symbols:
#		codes.append(ord(symbol))
````

NOTE : use list comprehension when you are building a list but doing a lot of more than that always use for loops as they are more readible.

**Local Scope in List Comprehension**

If we use `:=` (walrus operator) while assigning value then its accesible even after list comprehension or generator expression.

````python
x = 'ABC'
codes = [last := ord(c) for c in x]
print(codes) 	# [65, 66, 67]
print(last)		# 67
````

*NOTE: listcomps are as fast as map/filter/reduce operation sometimes outperforming them*.

#### Catersian Products

````python
colors = ['black', 'white']
size = ['S', 'M', 'L']

tshirts = [(color, size) for color in colors for size in sizes]
# it does cartesion product of colors x size
# ouptut : [('black', 'S'), ('black', 'M'), ('black', 'L'), ('white', 'S'),
# ('white', 'M'), ('white', 'L')]
````

### Generator Expressions (genexp)

you could always use listcomp, but genexp saves memory because it yields items one by one using the iterator protocol instead of building a whole list just to feed to another constructor.

````python
symbols = 'lion'
tuple(ord(symbol) for symbol in symbols)	# notice now its not [] instead ()
import array
array.array('I', ord(symbol) for symbol in symbols)

# in previous catesian product lets say if we had 1000 records then its would be very memory heavy to generate all those lists
for tshirts in (f'{c}{s}' for c in colors for s in sizes):
	print(tshirt)
````

### Tuples

Tuples are not just `immutable list` they can be used for two purpose, immutable list and records with no field names.

````python
lax_coordinates = (33.9425, -118.408056)
# tuple unpacking
city, year, pop, chg, area = ('Tokyo', 2003, 32_450, 0.66, 8014)

# slots based tuple unpacking
traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567')]
for passport in sorted(traveler_ids):
  print('%s/%s' % passport)
  
# nested unpacking 
name, _, _, (lat, lon) = ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
````

#### Tuple as Immutable Lists

Python interpretor and standard library makes extensive use of tuple as immutable list. It has 2 benefits

- Clarity (length never changes)
- Performance (uses less memory than a list of same length)

NOTE: `tuple` immutability applies only to references contained in it but if references are mutable objects then they can be modified but not their reference.

Ex : `a = (10, 'alpha', [1,2])` , this is a bad practice as list can be modified in this tuple effectively changing tuple.

*An object is only hashable if its value cannot ever change, as a result we can’t use unhashable tuple as a dict key or a set element.*

````python
# handy function to quickly check if an object is hashable
def fixed(obj):
  try:
    hash(obj)
  except TypeError:
    return False
  return True
````

[Are Tuples more efficient than list in Python](https://fpy.li/2-3)

```python
a, b = b, a # unpacking based swapping trick
# another use is argument unpacking
t = (20, 8)
# q, r = divmod(20,8)
q, r = divmod(*t)
```

#### Using `*` to Grab Excess Items

`````python
a, b, *rest = range(5)	# (1, 2, [3,4,5])
a, *mid, c = range(5)		# (1, [2, 3, 4], 5)
*s , b, c = range(5)		# ([1, 2, 3, 4, 5])
`````

#### Unpacking with `*` in Function Calls and Sequence Literals

````python
def fun(a, b, c, d, *rest):
  	return a, b, c, d, rest
  
fun(*[1,2], 3, *range(4,7)) # (1, 2, 3, 4, (5, 6))

tupl = *range(4), 4		# (1,2,3,4)
lst = [*range(4), 4]	# [1,2,3,4]
st = {*range(4), 4, *(5,6,7)} # {1, 2, 3, 4, 5, 6, 7}
````

### Pattern Matching with Sequences

Matching commands like `BEEPER 440 3`

````python
def handle_command(self, message):
  match message:
    case ['BEEPER', frequency, times]:
      self.beep(times, frequency)
    case ['NECK', angle]:
      self.rotate_neck(angle)
    case ['LED', ident, intensity]:
      self.leds[ident].set_color(ident, red, green, blue)
    case _:
      raise InvalidCommand(message)
````

It looks like simple C match-case but its supports `destructuring` (commonly used in Scala and Elixir).

````python
# note how [] can be multiline
metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
]
def func():
  for record in metro_ares:
    match record:
      case [name, _, _, (lat, lon)] if lon <= 0:
        print(f"{name:15} | {lat:9.4f} | {lon:9.4f}")
````

Here sequence pattern matches only if

- subject is a sequence
- subject and pattern have same number of items (could be avoided by variable unpacking but should not use it due to unexpected bugs)
- each corresponding items matches, including nested ones

In standard library these types are compatible with sequence patterns : `list, memoryview, array.array, tuple, range, collection.deque`. Unlike unpacking patterns don’t destructure iterables that are not sequences like iterators.

We could also use `as` keyword in case : `case [name, _, _, (lat, lon) as coord]`.

We could make patterns more specific using types : `case [str(name), _, _, (float(lat), float(lon))]` or this also works `case[str(name), *_, (float(lat), float(lon))]` (ignore all variables in between)

**Interesting Example :** [Link](https://github.com/fluentpython/lispy/blob/main/original/norvig/lis.py) Peter Norvig wrote `lis.py` : an interpretor for a subset of Scheme dialect of List Programming language in 132 lines of code. Notice how he move his code commits from elif to match-case as python 3.10 progresses

#### Alternative patterns for lambda

Syntax of lambda in Scheme : `(lambda(params ...) body1 body2)`, this could be written as `case ['lambda', [*params], *body] if body`

#### Shortcut syntax for function definition

syntax : `define (name param ...) body1 body2 ...)`

````python
case ['define', [Symbol() as name, *params], *body] if body:
  env[name] = Procedure(param, body, env)
````

### Slicing

A common feature of `list`, `tuple`, `str` and all sequence types in Python is support of slicing operation.

NOTE: slices and ranges exclude the last element (following 0 indexing of C)

```python
# slice = arr[start:stop:step]
```

NOTE: length of slice = stop-start, slicing an array into two equal part at x is `arr[:x]` and `arr[x:]`

NOTE: notation `a:b:c` is only valid within `[]`, it produces a slice object: `slice(a, b, c)` which is evaluated usinng `seq.__getitem__(slice(a,b,c))`.

#### Multidimensional Slicing and Ellipsis

`[]` operator can take multiple indexes or slices separated by commas. Python calls `a.__getitem__((i,j))` to evaluate `a[i,j]`. Notice how (i,j) is a tuple. Its used NumPy packages a lot, where we can fetch items of 2D `numpy.ndarray` like this : `a[m:n, k:l]`

Except for `memoryview`, the built-in sequence types in python are one-dimensional.

The ellipsis (`...`) is recognized as a token by the Python parser. It is an alias to `Ellipsis` object. It can be passed as an argument to functions and as part of a slice specification, as in `f(a, ..., z)` or `a[i:...]`.Numpy uses `...` as a shortcut for multidimensional slicing. for e.g. 4 dimensional array, `x[i, ...]` is evaluated as `x[i, :, :, :]`

#### Assigning to slicing

Mutable objects can be grafted, excised or modified in place using slicing

````python
l = list(range(10))
l[2:5] = [20,30] # modifying
del l[5:7]	# removing items
````

#### Using + and * with Sequences

`+` concatenates the two same type of sequences while `*` concatenates the same sequence to itself. (as many times scalar is specified: `[1]*4] = [1, 1, 1, 1]`)

NOTE: take note of `a*n` expressions as if you do `mylist = [[] * 3]` it will create a list with three references to same list, causing weird behaviour.

### Augmented Assignment with Sequences

`+=` and `*=` behave quite differently depending on first operand. `+=` internally calls `__iadd__` (in-place addition). In case of mutable sequences (`list`, `bytearray`, `array.array`) `a` will be changed in-place more like `a.extend(b)`. However if `__iadd__` is not implemented then expression will have same effect as `a = a + b` , evalute addition and assign to `a`.

````python
l = [1,2,3]
id(l)	# prints object id
l *= 2
id(l) # should be same as before

# tuple
t = (1,2,3)
id(t)
t *= 2
id(t)	# should be differnt id (object is augmented)
````

### list.sort v/s sorted Built-in

`list.sort` method sorts list in-place, without making copy. It return `None` to remind that it changes the receiver and doesn’t create a new list. (IMPORTANT API Convention in python).

`sorted` creates a new list and return it. It accepts any iterable object as argument, including immutable sequences and generators. Regardless of type sorted always returns sorted **list**!

Both function accept two optional, keyword only arguments:

`reverse` : If true items are in descending order

`key`: A one-argument function that applied to each item to produce its sorting key. default is the item itself but commonly used ones are `key=str.lower` or `key=len`.

Once sorted you can efficiently search using binary search using `bisect` module of python. you can use `bisect.insort` to keep your sorted sequences sorted. [link](https://www.fluentpython.com/extra/ordered-sequences-with-bisect/)

### When a List is not the Answer

`list` is flexible and easy to use, but depending on specific requirements there are better options like `array` which save lots of memory when you need to handle millions of floating-point values. If you are constantly removing items from opposite ends of a list use `collections.deque`

#### Array

`array.array` is more efficient for storing same type of data. it supports all mutable sepquence operations as well as additional methods for fast loading and saving like `.frombytes` and `.tofile`

````python
from array import array
from random import random
floats = array('d', (random() for i in range(10**7)))
print(floats[-1])
# should use context-manager for this
fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()

# with open('floats.bin', 'wb') as fp:
#   floats.tofile(fp)
floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close()
floats2[-1]
````

NOTE: `array` doesn’t support in-place sort method like `list.sort()`, we will need to use built-in `sorted` function to rebuild array

`a = array.array(a.typecode, sorted(a))`

#### Memory Views

The built-in `memoryview` class is a shared memory sequence type that lets you handles slices of arrays without copying bytes.

*A memoryview is essentially a generalized NumPy array structure in Python itself (without the math). It allows you to share memory between data-structures (things like PIL images, SQLite databases, NumPy arrays, etc.) without first copying. This is very important for large data sets.*

````python
from array import array
octets array('B', range(6))
m1 = memoryview(octets)
m1.tolist()	# [0, 1, 2, 3, 4, 5]
m2 = m1.cast('B', [2,3])
m2.tolist() # [[0, 1, 2], [3, 4, 5]]
m3 = m1.case('B', [3,2])
m3.tolist() # [[0,1],[2,3],[4,5]]
````

You can use it to create batches from array.

#### Brief introduction to Numpy

For advanced array and matrix operation, Numpy is used. Numpy implements multi-dimensional, homogenous arrays and matrix types that hold not only numbers but also use-defined records and provides efficient element-wise operations.

````python
import numpy as np
a = np.arange(12)
type(a)
print(a.shape)
a.shape = 3, 4
print(a) # 	[[0,1,2,3],[4,5,6,7],[8,9,10,11]]
print(a[:, 1]) # [1, 5, 9]
a.transpose() # [[0,4,8], [1,5,9], [2,6,10], [3,7,11]]
# trick used in ml to get features and labels
X = a[:,:-1]
y = a[:, -1]
````

#### Deques and Other Queues

`.append` and `.pop` methods make a `list` usable as a stack or a queue. But inserting and removing from head of a list is costly because the entire list is shifted in memory.

`collections.deque` is a thread-safe double ended queue designed for fast inserting and removing from both ends. Its is also the way to keep list of last seen items or something because it can be bounded(fixed size).

when you try to insert in a full bounded deque, it discards item from opposite end and inserts the item

Besides deque there are some other Python standard library implementations of queues

````python
from collection import deque
dq = deque(range(10), maxlen = 10)
print(dq)
dq.rotate(3)
print(dq)
dq.rotate(-4)
print(dq) # deque is restored
dq.appendleft(-1)
dq.extend([11,12,13]) # notice how lenght is fixed
dq.extendleft([10,20,30]) # notice how items on other end are discarded
````



- `queue` : This provides the synchronized(thread-safe) classes `SimpleQueue`, `Queue`, `LifoQueue` and `PriorityQueue`. These can be used for safe communication between threads. All except `SimpleQueue` can be bounded by providing a `maxsize` argument greater than 0 to the constructor. However they don’t discard items to make room as `deque` does. Instead it blocks the inserts of a new item until some thread makes room in the queue for items by taking from queue. It is usefull for implement n-worker threads models etc.
- `multiprocessing` : Implements its own `SimpleQueue` and bounded `Queue` but designed for interprocess communication. A specialized `multiprocessing.JoinableQueue` is provided for task management.
- `asyncio` : Provides `Queue`, `LifoQueue`, `PriorityQueue` and `JoinableQueue` with APIs inspired by the class in `queue` and `multiprocessing` modules but adapted for asynchronous programming.
- `headpq` : doesn’t implement queue class instead provide functions like `heappush` and `heappop` that lets you use mutable sequence as heap queue or priority queue.

---

## File: python/ch1_3.md

# Dictionaries and Sets

- `dict` type is a fundamental part of python’s implementation.
- Highly optimized using hash tables, other built-in types based on hash-tables are `set` and `frozenset` offering richer APIs and operators.

## Modern dict Syntax

### dict Comprehensions (`dictcomp`)

````python
dial_codes = [(91, 'India'), (1, 'United States')]
country_dial = {country: code for code, country in dial_codes}
country_dial["India"] # 91
country_codes = {code: country.upper() for country, code in sorted(country_dial.items()) if code < 70}
````

### Unpacking Mappings

- We can apply `**` to more than one argument in function calls. This works when keys are all strings and unique across all arguments (**NOTE: Duplicate keyword arguments are forbidden**)

````python
def dump(**kwargs):
  return kwargs

# dump(**{'x':1, y = 2, **{'z':3}})
# {'x':1, 'y':2, 'z':3}

# example 2
# {'a': 0, **{'x': 1}, 'y': 2, **{'z': 3, 'x': 4}}
# {'a': 0, 'x': 4, 'y': 2, 'z': 3}
````

NOTE: in case of duplicate args are overwritten by later occurances.

### Merge Mappings with |

````python
d1 = {'a':1, 'b':3}
d2 = {'a':2, 'b':4, 'c':6}
# notice overwritten keys by later set
d1|d2	# {'a': 2, 'b': 4, 'c': 6}
````

## Pattern Matching with Mappings

- Similar to sequence based pattern matching

````python
def get_creators(record: dict)->list:
  match record:
    case {'type':'book', 'api':2, 'authors':[*names]}:
      return names
    case {'type':'book', 'api':1, 'author': name}:
      return [name]
    case {'type':'book'}:
      raise ValueError(f"Invalid 'book' record:{record!r}")
    case {'type': 'movie', 'director':name}:
      return [name]
    case _:
      raise ValueError(f"Invalid Record: {record!r}")  
````

- We can handle semi-structured data like JSON records

````python
from collection import OrderedDict
b1 = dict(api=1, author'Temp Book', type='book', title='unknown')
get_creators(b1)	# ['unknown']
b2 = OrderedDict(api=2, type='book', title='Mystery of Python', authors:'smk hmk vib'.split())	
get_creators(b2) # ['smk', 'hmk', 'vib']

# notice how order doesn't matter, only keys need to be present correctly

````

## Standard API of Mapping Types

![UML class diagram for `Mapping` and `MutableMapping`](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_0301.png)

- To implement a custom mapping, its easier to exten `collections.UserDict`, or to wrap a `dict` by composition, instead of subclassing these ABCs.
- Note : only limitation to this is Keys must be Hashable

### What is Hashable

- An object is hashable if it has a hash code which never changes during its lifetime and can be compared to other objects.
- Implements : `__hash__()` and `__eq__()`

### Common Mapping Methods

| Method                   | Description                                         | dict           | defaultdict    | OrderedDict     |
|--------------------------|-----------------------------------------------------|----------------|----------------|-----------------|
| `d.clear()`              | Remove all items                                   | ●              | ●              | ●               |
| `d.__contains__(k)`      | k in d                                             | ●              | ●              | ●               |
| `d.copy()`               | Shallow copy                                       | ●              | ●              | ●               |
| `d.__copy__()`           | Support for `copy.copy(d)`                         |                |                | ●               |
| `d.default_factory`      | Callable invoked by `__missing__` to set missing values |                |                |                 |
| `d.__delitem__(k)`       | `del d[k]`—remove item with key k                  | ●              | ●              | ●               |
| `d.fromkeys(it, [initial])` | New mapping from keys in iterable, with optional initial value (defaults to None) | ●              | ●              | ●               |
| `d.get(k, [default])`    | Get item with key k, return default or None if missing | ●              | ●              | ●               |
| `d.__getitem__(k)`       | `d[k]`—get item with key k                        | ●              | ●              | ●               |
| `d.items()`              | Get view over items—(key, value) pairs            | ●              | ●              | ●               |
| `d.__iter__()`           | Get iterator over keys                            | ●              | ●              | ●               |
| `d.keys()`               | Get view over keys                                | ●              | ●              | ●               |
| `d.__len__()`            | `len(d)`—number of items                         | ●              | ●              | ●               |
| `d.__missing__(k)`       | Called when `__getitem__` cannot find the key     |                |                |                 |
| `d.move_to_end(k, [last])` | Move k first or last position (last is True by default) |                |                |                 |
| `d.__or__(other)`        | Support for `d1 | d2` to create new dict merging d1 and d2 (Python ≥ 3.9) | ●              | ●              | ●               |
| `d.__ior__(other)`       | Support for `d1 |= d2` to update d1 with d2 (Python ≥ 3.9) | ●              | ●              | ●               |
| `d.pop(k, [default])`    | Remove and return value at k, or default or None if missing | ●              | ●              | ●               |
| `d.popitem()`            | Remove and return the last inserted item as (key, value) | ●              | ●              | ●               |
| `d.__reversed__()`       | Support for `reverse(d)`—returns iterator for keys from last to first inserted |                |                | ●               |
| `d.__ror__(other)`       | Support for `other | dd`—reversed union operator (Python ≥ 3.9) | ●              | ●              | ●               |
| `d.setdefault(k, [default])` | If k in d, return d[k]; else set d[k] = default and return it | ●              | ●              | ●               |
| `d.__setitem__(k, v)`    | `d[k] = v`—put v at k                              | ●              | ●              | ●               |
| `d.update(m, [**kwargs])` | Update d with items from mapping or iterable of (key, value) pairs | ●              | ●              | ●               |
| `d.values()`             | Get view over values                              | ●              | ●              | ●               |

### Inserting or Updating Mutable Values

- following python’s *fail-fast* policy, `dict` access with `d[k]` raises an error when `k` doesn’t exist. Many folks know to use `d.get(k, default)` instead of handling `KeyError`. However to retrieve mutable value and update it, there is a better way.

````python
# example from zen of python
# we calculate occurances of a word and store it in dict (k,v) : (string, List[int])
# skipped irrelevant code
occ = index.get(word, [])	# search dict if the word exists or not
occ.append(location)	# update the list
index[word] = occ		# reassigned the dict key

# A better approach to this is using one line
index.setdefault(word, []).append(location)	# get the key or set the default empty then append

# basically we improved the code
if key not in my_dict:
  my_dict[key] = []
my_dict[key].append(new_value)
# to
my_dict.setdefault(key, []).append(new_value)
````

## Automatic Handling of Missing Keys

- If we want our `dict` to handle missing keys and return some specific value then we can either use `defaultdict` or subclass `dict` or any other mapping and populate `__missing__` method.

````python
# above code can be fixed now as
index = collections.defaultdict(list)	# calls list() function for deafult value
# now code doesn't need to check for missing keys
````

- Another example : `StrKeyDict0` class that converts nonstring keys to `str` on lookup

````python
class StrKeyDict0(dict):
  def __missing__(self, key):
    if isinstance(key, str):	# if key is already a string, return KeyError (imp as prevents recursion)
      raise KeyError(key)
    return self[str(key)]			# build key into string and search (prevent recursion here)
  def get(self, key, default=None):
    try:
      return self[key]	# --> calls `__getitem__` -> calls __missing__
    except KeyError:
      return default
  def __contains__(self, key):
    return key in self.keys() or str(key) in self.keys()	# search unmodified key or its string representation, requires because vanilla contains doesn't falls back to __missing__
````

NOTE: its much better to subclass `UserDict` than `dict`. Above example is bad :)

## Variation of Dict

#### collections.OrderedDict

- NOTE: built-in `dict` also keeps keys ordered, mostly its used due to backward compatibility. Some reasons for using it from python documentation
- The equality operation for `OrderedDict` check for matching order
- `popitem()` method for `OrderedDict` has a different signature and accepts optional argument to specify which item is popped.
- `move_to_end()` method to efficiently reposition element to endpoint
- `OrderedDict` can handle frequent reordering operation better than `dict`. Suitable for tracking recent accesses (LRU Cache)

NOTE: dict was designed primarily for fast access, maintaing order is secondary while Ordered dict was designed for reordering operations.

#### collections.ChainMap

`ChainMap` instance holds a list of mappings that can be searched as one. The lookup is performed on each input mapping in the order it appears in constructor call. returns as soon as key is found in one of those mappings.

````python
d1 = dict(a=1, b= 3)
d2 = dict(a=2, b= 4, c=6)
from collection import ChainMap
chain = ChainMap(d1, d2)
chain['a']	# output 1
chain['a']	# output 6
````

- ChainMap instance doesn’t copy input mapping but holds references to them. Updates or insertions affect first input mapping only.

````python
chain['a'] = -1		# changes on d1
````

NOTE: Its mostly used for implementing interpreters for languages with nested scopes, where each mapping represents a scope context.

````python
import builtins
pylookup = ChainMap(locals(), globals(), vars(builtins))
````

#### collections.Counter

A mapping that holds an integer for each key. Updating an existing key adds to its count. This is used for count instances of hashable objects or as a multiset/ `Counter` implements `+` and `-` operators to combine tallies and provides useful methods such as `most_common[n]` return most commonly updated items and their count.

````python
ct = collections.Counter('abracadabra')
ct	 	# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
ct.update('aaaaazzz')
ct		# Counter({'a': 10, 'z': 3, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
ct.most_common(3)	# [('a', 10), ('z', 3), ('b', 2)]
````

#### shelve.Shelf

`shelve` module in the standard library provides persistent storage for a mapping of string keys to Python Objects serialized in the pickle binary format.

The `shelve.open` module-level fucntion returns a `sheve.Shelf` instance - a simple key-value DBM Database backed by `dbm` module, with following properties

- `shelve.Shelf` subclasses `abc.MutableMapping`, so it provides the essential methods we expect of a mapping type.
- In addition, `shelve.Shelf` provides a few other I/O management methods, like `sync` and `close`.
- A `Shelf` instance is a context manager, so you can use a `with` block to make sure it is closed after use.
- Keys and values are saved whenever a new value is assigned to a key.
- The keys must be strings.
- The values must be objects that the `pickle` module can serialize.

### Subclassing UserDict instead of dict

- built-in has implementation shortcuts that end up forcing us to override methods that we can just inherit from `UserDict` with no problems.
- NOTE: `UserDict` doesn’t inherit from `dict` but uses composition : internal `dict` instance called `data` which holds the actual items. This avoids undesired recursion when coding special methods like `__setitem__` and simplifies the coding of `__contains__`

````python
import collections
class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item
````

## Immutable Mappings

- All standard library mappings are mutable, but we may need to prevent users from changing mapping by accident.
- Use cases in hardware programming library (Pingo) the board.pins maps represent physical GPIO ings on device, requires that user don’t change them
- `types` module provides a wrapper class called `MappingProxyType` which, given a mapping returns a `mappingproxy` instance that is read only but `dynamic proxy` for the original mapping. Meaning we can update dynamicproxy and see changes in mapping proxy but we can’t update mapping proxy.

````python
from types import MappingProxyType
d = {1: 'A'}
d_proxy = MappingProxyType(d)	# mappingproxy({1: 'A'})
d_proxy[1] 	# output : 'A'
d_proxy[2] = 'x'	# doesn't support assignment error
d[2] = 'B'
d_proxy # mappingproxy({1: 'A', 2: 'B'})
d_proxy[2]	# output : 'B'
````

## Dictionary Views

The `dict` instance methods `.keys()`, `.values()` and `.items()` return instances of classes called `dict_keys`, `dict_values` and `dict_items`. These dictionary views are read-only projection of internal data structures used in `dict` implementation.

- Avoids memory overhead or equivalent python2 methods that returned lists duplicating data already in the target `dict` and they also replace old methods that returned iterators.

````python
d = dict(a=10, b=20, c=30)
values = d.values()
values # dict_values([10, 20, 30])  1
len(values)  # 3
list(values) # convert into list, as views are iterable [10, 20, 30]
reversed(values) # <dict_reversevalueiterator object at 0x10e9e7310>
values[0]	# we cannot update these views
# Traceback (most recent call last):
  # File "<stdin>", line 1, in <module>
# TypeError: 'dict_values' object is not subscriptable
````

- A view object is a dynamic proxy. If source `dict` is updated you can immidediately see changes through an existing views.

## Practical Consequences of How dict Works

The hash table implementation of Python’s `dict` is very efficient, but it’s important to understand the practical effects of this design:

- Keys must be hashable objects. They must implement proper `__hash__` and `__eq__` methods.
- Item access by key is very fast. A `dict` may have  millions of keys, but Python can locate a key directly by computing the  hash code of the key and deriving an index offset into the hash table,  with the possible overhead of a small number of tries to find a matching entry.
- Key ordering is preserved as a side effect of a more compact memory layout for `dict` in CPython 3.6, which became an official language feature in 3.7.
- Despite its new compact layout, dicts inevitably have a significant  memory overhead. The most compact internal data structure for a  container would be an array of pointers to the items.[8](https://learning.oreilly.com/library/view/fluent-python-2nd/9781492056348/ch03.html#idm46582498236432) Compared to that, a hash table needs to store more data per entry, and  Python needs to keep at least one-third of the hash table rows empty to  remain efficient.
- To save memory, avoid creating instance attributes outside of the `__init__` method.

## Set Theory

NOTE: `set` is mutable while its sibling `frozenset` is immutable

- A set is a collection of unique objects
- set elements must be hashable. The `set` type is not hashable, so you can’t build a `set` with nested `set`. But `frozenset` is hashable so we can have it inside `set`
- set supports multiple infix operators like
  - `a | b` union
  - `a & b` intersection
  - `a - b` difference
  - `a^b` symmetric difference

````python
l = ['spam', 'spam', 'bacon', 'eggs', 'eggs']
set(l) # {'spam', 'bacon', 'eggs'}
list(set(l))	# remove duplicates from a list
````

````python
# NOTE : unrelated
# remove duplicates but also preserve order of first occurence of each items, we can use plain dict
dict.fromkeys(l).keys()
# dict_keys(['spam','eggs', 'bacon'])
list(dict.fromkeys(l).keys())
````

````python
# count occurrences of needles in a haystack, both of type set
found = len(needles & haystack)
````

### Set Literals

- NOTE: there is no representation for empty set : use `set()` because `{}` already declares an empty dict
- NOTE: `st = {1, 2, 3}` is much faster than `st = set([1, 2, 3])`.
- There is no syntax to represent `frozenset` so we have to use constructor like this `frozenset(range(10))`

### Set Comprehensions

````python
from unicodedata import name
# set of Latin-1 characters that have sign in their unicode names
{chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')}
````

## Practical Consequences of How set Works

`set` and `frozenset` are both implemented with a hash table with following effects.

- set elements must be hashable. They must implement proper `__hash__` and `__eq__` methods.
- Membership testing is very efficient
- sets have significant memory overhead compared to low-level array pointers to its elements
- element ordering depends on insertion order but not in a useful or reliable way.
- adding elements to a set ma change order of existing elements. Because algorithm becomes less efficient if the hash table is more than two-thirds full, so python may need to move and resize table as it grows.

## Set Operations on dict Views
| Method               | frozenset | dict_keys | dict_items | Description                                  |
|----------------------|-----------|-----------|------------|----------------------------------------------|
| s.\_\_and\_\_(z)     |     ●     |     ●     |     ●      | s & z (intersection of s and z)             |
| s.__rand\_\_(z)    |     ●     |     ●     |     ●      | Reversed & operator                         |
| s.__contains\_\_()  |     ●     |     ●     |     ●      | e in s                                       |
| s.copy()             |     ●     |           |            | Shallow copy of s                            |
| s.difference(it, …)  |     ●     |           |            | Difference between s and iterables it, etc. |
| s.intersection(it, …)|     ●     |           |            | Intersection of s and iterables it, etc.    |
| s.isdisjoint(z)      |     ●     |     ●     |     ●      | s and z are disjoint (no elements in common)|
| s.issubset(it)       |     ●     |           |            | s is a subset of iterable it                |
| s.issuperset(it)     |     ●     |           |            | s is a superset of iterable it              |
| s.__iter\_\_\()      |     ●     |     ●     |     ●      | Get iterator over s                          |
| s.__len\_\_()       |     ●     |     ●     |     ●      | len(s)                                       |
| s.__or\_\_(z)        |     ●     |     ●     |     ●      | s |
| s.__ror\_\_()        |     ●     |     ●     |     ●      | Reversed |
| s.__reversed\_\_()  |           |     ●     |     ●      | Get iterator over s in reverse order        |
| s.__rsub\_\_(z)      |     ●     |     ●     |     ●      | Reversed - operator                         |
| s.__sub\_\_(z)       |     ●     |     ●     |     ●      | s - z (difference between s and z)         |
| s.symmetric_difference(it)|   ●   |           |            | Complement of s & set(it)                   |
| s.union(it, …)       |     ●     |           |            | Union of s and iterables it, etc.           |
| s.\_\_xor__()        |     ●     |     ●     |     ●      | s ^ z (symmetric difference of s and z)    |
| s.\_\_rxor__()       |     ●     |     ●     |     ●      | Reversed ^ operator                         |



---

## File: python/ch1_4.md

# Unicode Text Versus Bytes

Python3 introduced a sharp disctinction between string of human text and sequences of raw bytes.

## Character Issues

Concept of “string” is simple : a string is a sequence of characters. The problem lies in the definition of character.

Items that we get out of Python3 `str` is Unicode characters, just like the `unicode` obj in python2.

Unicode standard explicitly separates identity or character from specific byte representation

- The identity of character - its *code point* - is a number from 0 to 1,114,111 (base10) shown as 4 to 6 hex digits with `U+` prefix. Ranges from : `U+0000` to `U+10FFFF`

- The actual byte that represent a character depends on *encoding* in use. An Encoding algorithm converts code points to byte sequences & vice-versa. The code point for the letter A (`U++0041`) is encodd as single byte `\x41` in UTF-8 encoding or bytes `\x41\x00` in UTF-16LE Encoding.

````python
s = 'café'
len(s)	# 4
b = s.encode('utf8')
len(b)	# 5
````

## Byte Essentials

- There are two basic built-in types for binary sequences
  - immutable `byte` type (python3+)
  - mutable `bytearray` (python2.6+)
- python docs uses generic term to refer to these as “byte strings”

````python
cafe = bytes('café', encoding='utf8')
cafe	# b'caf\xc3\xa9' # notice 3 (caf) are printable but not the last one
cafe[0]	# 99 return int
cafe[:1]	# b'c'	wait isn't this should be same as above ? returns byte
cafe_arr = bytearray(cafe)	# bytearray(b'caf\xc3\xa9')
cafe_arr[-1:]	# bytearray(b'\xa9')
````

4 different types of display used to represent binary sequences

- for bytes with decimal codes 32-126 (space to tilde) Ascii character itself is used
- for bytes corresponding to tab, newline, carriage return, and `\` the escape sequences are `\t`, `\n`, `\r` and `\\` are used
- If both string delimiters `‘`, `“”` appear in byte sequence then whole sequence is delimited by `‘` and any `‘` inside are escaped using `\'`
- for other byte values a hexadecimal escape sequence is used. `\x00` is null byte

Both `byte` and `bytearray` support every `str` method except those that do fomatting and those that depend on Unicode data, including `casefold`, `isdecimal`, `isidentifier`, `isnumeric`, `isprintable` and `encode`.

All other functions and even `re` works fine on byte sequences.

Binary sequences have a class method that `str` doesn’t have, called from hex which builds a binary sequence by parsing pairs of hex digits optionally separated by spaces.

```python
bytes.fromhex('31 4B CE A9') # b'1K\xce\xa9'
```

## Basic Encoders/Decorders

Python distribution bundles more than 100 codecs (encoder/decoder) for text to byte conversion & vice-versa.

````python
for codec in ['latin_1', 'utf_8', 'utf_16']:
	print(codec, 'El Niño'.encode(codec), sep='\t')
  
latin_1 b'El Ni\xf1o'
utf_8   b'El Ni\xc3\xb1o'
utf_16  b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'
````

| Encoding  | Description                                                                       |
|-----------|-----------------------------------------------------------------------------------|
| latin1    | Basis for other encodings, such as cp1252 and Unicode; widely used in Western Europe. |
| cp1252    | Latin1 superset created by Microsoft, adding useful symbols like curly quotes and € (euro). |
| cp437     | Original character set of the IBM PC, with box drawing characters. Incompatible with latin1. |
| gb2312    | Legacy standard to encode simplified Chinese ideographs used in mainland China.      |
| utf-8     | Most common 8-bit encoding on the web, supporting a wide range of characters.         |
| utf-16le  | One form of the UTF 16-bit encoding scheme, supporting code points beyond U+FFFF.     |

## Understanding Encode/Decode Problems

Although there is generic `UnicodeError` exception, the error reported by Python is more specific, either `UnicodeEncodeError` or a `UnicodeDecodeError`.

### Coping with UnicodeEncodeError

Most non-UTF codecs handle only a small subset of Unicode characters. When converting text to bytes, if a character is not defined in target encoding `UnicodeEncodeError` is raised, unless special handling is provided by passing an `errors` args to the encoding method or function.

````python
city = 'São Paulo'
city.encode('utf_8')	# works
city.encode('cp437')	# raises error
city.encode('cp437', errors = 'ignore')	# we could pass option like ignore, replace, xmlcharrefreplace
````

Ascii is common subset of all encodings, so if `str.isascii` is true then your text never raise this error.

### Coping with UnicodeDecodeError

Not every byte holds a valid ASCII character, and not every byte sequence is valid UTF-8 or UTF-16; therefore, when you assume one of these encodings while converting a binary sequence to text, you will get a `UnicodeDecodeError` if unexpected bytes are found.

Note: many 8 bit legacy encoding silently convert without reporting errors so output maybe garbled.

### SyntaxError When Loading Modules with Unexpected Encoding

UTF-8 is the default source encoding for python3, just as ascii was for python2. If you load `a.py` module containing non-UTF-8 data and no encoding declaration you get a message like this :

```python
SyntaxError: Non-UTF-8 code starting with '\xe1' in file ola.py on line
```

Fix is very easy magic `coding` comment.

```python
# coding: cp1252

print('Olá, Mundo!')
```

### How to Discover the Encoding of a Byte Sequence

How do you find the encoding of a byte sequence? Short answer: you can’t. You must be told.

Some communication protocols and file formats, like HTTP and XML, contain headers that explicitly tell us how the content is encoded.

However, considering that human languages also have their rules and restrictions, once you assume that a stream of bytes is human *plain text*, it may be possible to sniff out its encoding using heuristics and statistics.

### BOM: A Useful Gremlin

you may have noticed a couple of extra bytes at the beginning of a UTF-16 encoded sequence.

````python
u16 = 'El Niño'.encode('utf_16')
u16
b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'
````

The bytes `b'\xff\xfe`. That is a BOM-byte-order-mark denoting the “little-endian”(least significant byte comes first) byte ordering of the intel CPU where the encoding was performed.

## Handling Text Files

![https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_0402.png](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_0402.png)

As a thumb rule, `bytes` should be decoded to `str` as early as possible and then all operation should be done on `str` and then converted to `bytes` as late as possible.

Python3 makes it easier because `open()` built-in does the necessary decoding when reading and encoding when writing files in text mode. 

````python
open('cafe.txt', 'w', encoding='utf_8').write('café')
open('cafe.txt').read()	# notice how last char is garbled (default encoding error, windows use codepage 1252) (on linux/unix it should be fine)
````

### Beware of Encoding Defaults

several settings affect the encoding defaults for I/O in Python. NOTE its different in windows but on mac/linux/unix its same (utf_8) everywhere.

## Normalizing Unicode for Reliable Comparisons

String comparisions are complicated by the fact that Unicode has combining characters: diacritics and other marks that attach to the preceding characters, appearing as one when printed.

````python
# two ways to compose café word
s1 = 'café'	# len 4
s2 = 'cafe\N{COMBINING ACUTE ACCENT}'	# len 5
s1 == s2 # False
# In the Unicode standard, sequences like 'é' and 'e\u0301' are called “canonical equivalents,”
````

The solution is to use `unicodedata.normalize()`. Keyboard drivers usually generate composed characters, so text typed by users will be in NFC by default. However, to be safe, it may be good to normalize strings with `normalize('NFC', user_text)` before saving.

````python
from unicodedata import normalize, name
ohm = '\u2126'
name(ohm) # 'OHM SIGN'
ohm_c = normalize('NFC', ohm)
name(ohm_c)	# 'GREEK CAPITAL LETTER OMEGA'
ohm == ohm_c # False
normalize('NFC', ohm) == normalize('NFC', ohm_c) # True
````

### Case Folding

Case folding is essentially converting all text to lowercase, with some additional transformations. It is supported by the `str.casefold()` method.

For any string `s` containing only `latin1` characters, `s.casefold()` produces the same result as `s.lower()`, with only two exceptions—the micro sign `'µ'` is changed to the Greek lowercase mu (which looks the same in most fonts) and the German Eszett or “sharp s” (ß) becomes “ss”

There are nearly 300 code points for which `str.casefold()` and `str.lower()` return different results.

### Extreme “Normalization”: Taking Out Diacritics

The Google Search secret sauce involves many tricks, but one of them  apparently is ignoring diacritics (e.g., accents, cedillas, etc.), at  least in some contexts. Removing diacritics is not a proper form of  normalization because it often changes the meaning of words and may  produce false positives when searching. But it helps coping with some  facts of life: people sometimes are lazy or ignorant about the correct  use of diacritics, and spelling rules change over time, meaning that  accents come and go in living languages.

## Sorting Unicode Text

````python
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted(fruits) # ['acerola', 'atemoia', 'açaí', 'caju', 'cajá']
# but it should be ['açaí', 'acerola', 'atemoia', 'cajá', 'caju']
````

The standard way to sort non-ASCII text in Python is to use the `locale.strxfrm` function which, according to the `locale` module docs, “transforms a string to one that can be used in locale-aware comparisons.”

To enable `locale.strxfrm`, you must first set a suitable locale for your application, and pray that the OS supports it.

````python
import locale
my_locale = locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
print(my_locale)
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=locale.strxfrm)
print(sorted_fruits)
````

- since locale settings are global, calling `setlocale` in a library is not recommended
- the locale must be installed on OS
- you must know how to spell the locale name
- locale must be implemented correctly by makes of the OS.

### Sorting with the Unicode Collation Algorithm

James Tauber, prolific Django contributor, must have felt the pain and created pyuca, a pure-Python implementation of the Unicode Collation Algorithm (UCA).

````python
import pyuca
coll = pyuca.Collator()
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=coll.sort_key)
sorted_fruits  # ['açaí', 'acerola', 'atemoia', 'cajá', 'caju']
````

## The Unicode Database

The `unicodedata` module has functions to retrieve character metadata, including `unicodedata.name()`, which returns a character’s official name in the standard.

| ![image-20240502001002209](./ch1_4.assets/image-20240502001002209.png) |
| ------------------------------------------------------------ |

## Dual-Mode str and bytes APIs

Python’s standard library has functions that accept `str` or `bytes` arguments and behave differently depending on the type.

### str Versus bytes in Regular Expressions

Regular expressions built with bytes patterns (\d and \w) only match  ASCII characters, while patterns built with str match Unicode digits or letters beyond ASCII. 

Additionally, the re module  offers the re.ASCII flag for str regular expressions, enabling  ASCII-only matching for certain patterns.

### str Versus bytes in os Functions

In the real world of GNU/Linux systems, filenames can contain byte  sequences that are not valid in any sensible encoding scheme, causing  issues with decoding to `str`. To handle this, functions in the `os` module accept filenames or pathnames as either `str` or `bytes`. When called with a `str` argument, they are automatically converted using the codec specified by `sys.getfilesystemencoding()`

However, if dealing with filenames that cannot be handled this way, passing `bytes` arguments to these functions returns `bytes` values, allowing handling of any file or pathname. The `os` module provides `os.fsencode()` and `os.fsdecode()` functions to assist in manual handling of `str` or `bytes` sequences as filenames or pathnames.

---

## File: python/ch1_5.md

# Data Class Builders

Python offers a few ways to build a simple class that is just a collection of fields, with little or no extra functionality.

That pattern is known as a “data class”—and `dataclasses` is one of the packages that supports this pattern.

We will cover 3 different class builders

- `collection.namedtuple`
- `typing.NamedTuple`
- `@dataclasses.dataclass`

## Overview of Data Class Builders

Conider example of this class

````python
class Coordinate:
  def __init__(self, lat, lon):
    self.lat = lat
    self.lon = lon
````

- This representation is very verbose and doesn’t implement functions like `__eq__` and `__repr__`.

````python
from collections import namedtuple
Coordinate = namedtuple('Coordinate', 'lat lon')
issubclass(Coordinate, tuple)	# true
moscow = Coordinate(55.756, 37.617)	# Coordinate(lat=55.756, lon=37.617)
moscow == Coordinate(lat=55.756, lon=37.617)	# returns true
````

- we achieved both `__repr__` and `__eq__` using namedtuple

Newer `typing.NamedTuple` provides similar functionality but adds type annotation to each field

````python
Coordinate = typing.NamedTuple('Coordinate', [('lat', float), ('lon', float)])
# we could also use key word arguments
Coordinate = typing.NamedTuple('Coordinate', lat=float, lon=float)
````

for python3.6, NamedTuple can also be used in a class statement

````python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'
````

- Note although here NamedTuple appears as superclass but it is not (tuple is) (Python metaprogramming magic).

`typing.NamedTuple` uses the advanced functionality of a metaclass[2](https://learning.oreilly.com/library/view/fluent-python-2nd/9781492056348/ch05.html#idm46582456097616) to customize the creation of the user’s class.

similar to NamedTuple `dataclass` decorator support to declare instance attributes.

````python
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float
````

- Note `@dataclass` decorator doesn’t depend on inheritance or a metaclass, so it should not interfere with your own use of these mechanisms. Here its subclass of object.

### Features:

#### Mutable Instances

- `collections.namedtuple` and `typing.NamedTuple` build `tuple` classed which are immutable, while `@dataclass` produces mutable classes. You can pass `frozen=True` kwarg to make it immutable.

#### Class statement syntax

- Only `typing.NamedTuple` and `@dataclass` support regular `class` statement syntax.

#### Construct dict

- Both named tuple variants provide an instance method `._asdict` to construct a `dict` object from the fields in a dataclass instance. The `dataclass` module provides a function : `dataclass.asdict`

#### Get field names and default values

- All three class builders let you get the field names and default values that may be configured. In named tuple classes its `._fields` and `._fields_defaults` class attributes. for dataclass we use `fields` functions from `dataclasses` module. It returns a tuple of `Field` objects.

#### New instance with changes

given a named tuple instance `x`, the call `x._replace(**kwargs)` returns a new instance with some attribute values replaced according to the keyword args given. The `dataclasses.replace(x, **kwargs)` module-level function does same for dataclasses

#### New class at runtime.

Although the `class` statement syntax is more readable, it is hardcoded. A framework may need to build data classes on the fly for that we can use `collections.namedtuple`, which is supported by NamedTuple as well. The dataclasses module provides a `make_dataclass` fucntion for the same purpose.

## Classic Named Tuples

````python
from collections import namedtuple
import json

City = namedtuple('City', ['name', 'country', 'population', 'location'])
Coordinate = namedtuple('Coordinate', ['lat', 'lon'])

delhi_data = ('Delhi NCR', 'IN', 21.935, Coordinate(28.613889, 77.208889))
delhi = City._make(delhi_data)

delhi_dict = delhi._asdict()
delhi_json = json.dumps(delhi_dict)

print(delhi_dict)
print(delhi_json)
````

## Typed Named Tuples

A typed Named Tuple with defaults

````python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    reference: str = 'WGS84'
````

## Type Hints 101

- Python bytecode compiler and interpreter doesn’t enforce type hints at all.

### No Runtime Effect

- Python type hints are more for documentation purpose and IDE type checkers

````python
import typing

class Coordinate(typing.NamedTuple):
    lat: float
    lon: float

trash = Coordinate('Ni!', None)
print(trash)
````

Above code works fine and throws no errors

### Variable Annotation Syntax

Both `typing.NamedTuple` and `@dataclass` use the syntax of variable annotations.

```python
var_name: some_type
```

These are more likely to be useful:

- A concrete class, for example `str`\
- A parameterized collection type, like `list[int]`, `tuple[str, float]`
- `typing.Optional`, for example, `Optional[str]` - to declare a field that can be a `str` or `None`

### Meaning of Variable Annotation

- There is no runtime effect that type hints have, but at import time when a module is loaded Python does read them to build `__annotation__` dictionary that `typingNameTuple` and `@dataclass` then use to enhance class.

````python
class DemoPlainClass:
  a : int	# becomes an entry in __annotation__	 (not an attribute as its not declared a value)
  b: float = 1.1 # saved as annotation
  c = 'spam'	# normal field
  
# we can check 
from demo_ import DemoPlainClass
DemoPlainClass.__annotation__	# should show two entries
````

Making similar class with Named Tuple

````python
import typing
class DemoNTClass(typing.NamedTuple):
  a : int
  b: float = 1.1
  c = 'spam'
````

````python
from demo_nt import DemoNTClass
DemoNTClass.__annotations__ # {'a': <class 'int'>, 'b': <class 'float'>}
DemoNTClass.a # <_collections._tuplegetter object at 0x101f0f940>
DemoNTClass.b # <_collections._tuplegetter object at 0x101f0f8b0>
DemoNTClass.c # 'spam'
````

NOTE: `DemoNTClass.a` doesn’t throw `AtrtibuteError` anymore (its an attribute) as it has become a class descriptors (kind of like getters and setters). `c` becomes normal old class attribute. similar with @dataclass.

NOTE: now because of annotation we can have `__doc__` docstring as well for `(a, b)`

````python
from dataclasses import dataclass

@dataclass
class DemoDataClass:
  a : int
  b: float = 1.1
  c = 'spam'
````

## More About @dataclass

`@dataclass` accepts several keyword args.

````python
@dataclass(*, init=True, repr=True, eq=True, order=False,
              unsafe_hash=False, frozen=False)
````
| Option      | Meaning                                        | Default | Notes                                                        |
| ----------- | ---------------------------------------------- | ------- | ------------------------------------------------------------ |
| init        | Generate `__init__`                            | True    | Ignored if `__init__` is implemented by user.                |
| repr        | Generate `__repr__`                            | True    | Ignored if `__repr__` is implemented by user.                |
| eq          | Generate `__eq__`                              | True    | Ignored if `__eq__` is implemented by user.                  |
| order       | Generate `__lt__`, `__le__`,`__gt__`, `__ge__` | False   | If True, raises exceptions if `eq=False`, or if any of the comparison methods that would be generated are defined or inherited. |
| unsafe_hash | Generate `__hash__`                            | False   | Complex semantics and several caveats—see: dataclass documentation. |
| frozen      | Make instances “immutable”                     | False   | Instances will be reasonably safe from accidental change, but not really immutable. |

### Field Options

Python does not allow parameters without defaults after parameters with defaults, therefore after you declare a field with a default value, all remaining fields must also have default values.

Mutable defaults are biggest source of bugs for beginners. In function definitions, a mutable default value is easily corrupted when one invocation of the function mutates the default, changing the behaviour of further invocation

````python
@dataclass
class ClubMember:
    name: str
    guests: list = []
````

- dataclasses are smart to avoid this pitfalls.
- import raises a suggestion to use default_factory

````python
from dataclasses import dataclass, field

@dataclass
class ClubMember:
    name: str
    guests: list = field(default_factory=list)
````

The `default_factory` parameter lets you provide a function,  class, or any other callable, which will be invoked with zero arguments  to build a default value each time an instance of the data class is  created. This way, each instance of `ClubMember` will have its own `list`—instead of all instances sharing the same `list` from the class, which is rarely what we want and is often a bug.

### Post-init Processing

The `__init__` method generated by `@dataclass` only takes the arguments passed and assigns them—or their default values, if missing—to the instance attributes that are instance fields. But you may need to do more than that to initialize the instance. If that’s the case, you can provide a `__post_init__` method.

Common use cases for `__post_init__` are validation and computing field values based on other fields.

### Initialization Variables That are not Fields

Sometimes you may need to pass arguments to `__init__` that are not instance fields. Such arguments are called *init-only variables*

To declare an argument like that, the `dataclasses` module provides the pseudotype `InitVar`, which uses the same syntax of `typing.ClassVar`

````python
@dataclass
class C:
    i: int
    j: int = None
    database: InitVar[DatabaseType] = None

    def __post_init__(self, database):
        if self.j is None and database is not None:
            self.j = database.lookup('j')

c = C(10, database=my_database)
````

### @dataclass Example: Dublin Core Resource Record

Often, classes built with `@dataclass` will have more fields than the very short examples presented so far.

````python
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum, auto
from datetime import date

# enums provide type-safe values for Resource.type field
class ResourceType(Enum):
    BOOK = auto()
    EBOOK = auto()
    VIDEO = auto()


@dataclass
class Resource:
    """Media resource description."""
    identifier: str				# required field
    title: str = '<untitled>'	# first default field, rest all should be default
    creators: list[str] = field(default_factory=list)
    date: Optional[date] = None	# value could be datetime.date instance or None
    type: ResourceType = ResourceType.BOOK 	# default is BOOK
    description: str = ''
    language: str = ''
    subjects: list[str] = field(default_factory=list)
````

## Data Class as a Code Smell

Whether you implement a data class by writing all the code yourself or leveraging one of the class builders described in this chapter, be aware that it may signal a problem in your design.

In [*Refactoring: Improving the Design of Existing Code*, 2nd ed.](https://martinfowler.com/books/refactoring.html) (Addison-Wesley), Martin Fowler and Kent Beck present a catalog of  “code smells”—patterns in code that may indicate the need for  refactoring. The entry titled “Data Class” starts like this:

> These are classes that have fields, getting and setting methods for fields, and nothing else. Such classes are dumb data holders and are often being manipulated in far too much detail by other classes.

In Fowler’s personal website, there’s an illuminating post titled [“Code Smell”](https://martinfowler.com/bliki/CodeSmell.html). The post is very relevant to our discussion because he uses *data class* as one example of a code smell and suggests how to deal with it. Here is the post, reproduced in full.

### Data Class as Scaffolding

In this scenario, the data class is an initial, simplistic  implementation of a class to jump-start a new project or module. With  time, the class should get its own methods, instead of relying on  methods of other classes to operate on its instances. Scaffolding is  temporary; eventually your custom class may become fully independent  from the builder you used to start it.

### Data Class as Intermediate Representation

- versatility of data classes in serving as an intermediary representation during data export and import processes, facilitating conversion to  JSON-compatible dictionaries. 
- It is important to treating  data class instances as immutable objects to preserve data integrity.  
- Implement custom builder methods for  scenarios requiring data modification during import/export operations
- exploring pattern matching for arbitrary class  instances to enhance code flexibility.

## Pattern Matching Class Instances

### Simple Class Patterns

syntax for class patterns looks like this

````python
    match x:
        case float():	# matches float values without binding a variable(case can refer to x directly)
            do_something_with(x)
````

NOTE: this is gonna be a bug

````python
    match x:
        case float:  # DANGER!!!	# matches any subject, because its seen as a var which is bound to subject
            do_something_with(x)
````

### Keyword Class Patterns

````python
import typing

class City(typing.NamedTuple):
    continent: str
    name: str
    country: str


cities = [
    City('Asia', 'Tokyo', 'JP'),
    City('Asia', 'Delhi', 'IN'),
    City('North America', 'Mexico City', 'MX'),
    City('North America', 'New York', 'US'),
    City('South America', 'São Paulo', 'BR'),
]


# using the class
def match_asian_cities():
    results = []
    for city in cities:
        match city:
            case City(continent='Asia'):
                results.append(city)
    return results
  
# collecting country variable
def match_asian_countries():
    results = []
    for city in cities:
        match city:
            case City(continent='Asia', country=cc):
                results.append(cc)
    return results
````



---

## File: python/ch1_6.md

# Object References, Mutability and Recycling

## Variables are not Boxes

- python variables are like reference variables in Java
- a better metaphor to think of variables as labels with names attached to objects rather than a box

````python
a = [1, 2, 3]
b = a
a.append(4)
print(b)	# [1, 2, 3, 4]
````

- `b=a` doesn’t copy contents of array instead attaches `b` as a antoher label to array
- objects are created before assignment

````python
class Gizmo:
  def __init__(self):
    print(f"Gizmo id: {id(self)}")

# 
x = Gizmo()	# Gizmo id: 4301489152
y = Gizmo() * 10 
# Gizmo id: 4301489432 # <--- this is printed means object is created first
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: unsupported operand type(s) for *: 'Gizmo' and 'int'

# Notice how Gizmo is created even before the assignment of its multiplication with 10
````

## Identity, Equality and Aliases

````python
charles = {'name':'Charles L Dodgson', 'born':1832}
lewis = charles	# alias
lewis is charles	# true
id(lewis) == id(charles)	# ture
lewis['balance'] = 950
charles	# updated

alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}
alex == charles # true ( Note: how this actually compared objects due to __eq__)
alex is charles # false
````

*An object’s identity never changes once it has been created, more like an address in memory.* The `is` operator compares identity of two objects, and `id` returns an integer representing its identity.

### Choosing Between `==` and `is`

If you are comparing a variable to a singleton then it makes sense to use `is`, most common case is checking whether a variable is bound to `None`, `x is None`, rather than `==`

We can compare sentinel objects using `is` as well.

````python
END_OF_DATA = object()
# ... many lines
def traverse(...):
    # ... more lines
    if node is END_OF_DATA:
        return
    # etc.
````

- is operator is faster than ==, because it can’t be overloaded, so python directly executes it without any checks & comparison of ids is simple

### The Relative Immutability of Tuples

- tuples are containers, they hold references to objects. If referenced objects are mutable they may change even if the tuple itself doesn’t.
- So immutability of tuple only extends to actuals contents of tuple not the objects that are referenced in it.

## Copies are Shallow by Default

- easies way to copy a list(or most built-in mutable collections) is to use built-in constructor for the type itself.

````python
l1 = [3, [55,44], (7,8,9)]
l2 = list(l1) 
l1 == l2	# true
l1 is l2	# false
````

- Note we could also use `l2=l1[:]` to make a shallow copy
- **remember that only outermost container will be duplicated, but the copy is filled with references to the same items held by original container. This saves memory and causes no problem if all items are immutable. For mutable items don’t do this !!**

### Deep and Shallow Copies of Arbitrary Objects

- to create deep copy use `copy` module to get `deepcopy` (deep) and `copy` (shallow) copy functions
- Note: making deep copies is not simple matter in general case. Objects may have cyclic references that would cause naive alogithm to go in  infinite loop. But `deepcopy` function remebers the objects already copied to handle cyclic references gracefully.

## Function Parameters as References

The only mode of parameter passing in Python is *call by sharing*. That is the same mode used in most OOPs languages and JS, Ruby and Java(reference types). 

- Call by sharing refers to that each functions receives the copy of each reference in the arguments. In other words parameters inside function become aliasees of the actual arguments.
- Result is that a function may change a mutable objects passed as parameter, but it cannot change identity of those objects.

````python
def f(a, b):
  a += b
  return a

x = 1
y = 2
f(x, y)	# 3
x,y	# (1,2)

# now
a = [1, 2]
b = [3, 4]
f(a,b)	# [1,2,3,4]
a,b		# ([1,2,3,4], [3,4])

t = (10, 20)
u = (30, 40)
f(t, u)	# (10, 20, 30, 40)
t,u	# ((10, 20), (30, 40))
````

### Mutable Types as Parameter Defaults: Bad Idea

````python
class HauntedBus:
    """A bus model haunted by ghost passengers"""

    def __init__(self, passengers=[]):
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)
        
# Output
bus1 = HauntedBus(['Alice', 'Bill'])
bus1.passengers  # ['Alice', 'Bill']
bus1.pick('Charlie')
bus1.drop('Alice')
bus1.passengers  # ['Bill', 'Charlie']

# horror begin when default invoked
bus2 = HauntedBus()
bus2.pick('Carrie')
bus2.passengers  # ['Carrie']
bus3 = HauntedBus()
bus3.passengers  # ['Carrie']
bus3.pick('Dave')
bus2.passengers  # ['Carrie', 'Dave']
bus2.passengers is bus3.passengers  # True
bus1.passengers  # ['Bill', 'Charlie']
````

### Defensive Programming with Mutable Parameters

When you are coding a function that receives a mutable parameter, you should carefully consider whether the caller expects the argument  passed to be changed.

For example, if your function receives a `dict` and needs  to modify it while processing it, should this side effect be visible  outside of the function or not? Actually it depends on the context. It’s really a matter of aligning the expectation of the coder of the  function and that of the caller.

````python
basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
bus = TwilightBus(basketball_team)
bus.drop('Tina')
bus.drop('Pat')
basketball_team  # ['Sue', 'Maya', 'Diana']
````

Above class violates the *Principle of least Astonishment*, a best practice of interface design.

````python
class TwilightBus:
    """A bus model that makes passengers vanish"""

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers	# this reference is set at class internally

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)
````

- when drop is called its actually run on the object referenced by paramters which in turn is actual list.
- correct way is to make a copy of the list passed.

````python
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)
````

- this makes copy of the list, and extends that our passengers now maybe a tuple or any other iterable type

## del and Garbage Collection

The first strange fact about `del` is that it’s not a function, it’s a statement. We write `del x` and not `del(x)`—although the latter also works, but only because the expressions `x` and `(x)` usually mean the same thing in Python.

The second surprising fact is that `del` deletes references, not objects. Python’s garbage collector may discard an object from memory as an indirect result of `del`, if the deleted variable was the last reference to the object.

````python
a = [1, 2]	# bind to a
b = a	# label b to a
del a	# [1,2] still remains because b references it
b # [1,2]
b = [3]	# [1,2] is now collected becuase it available for garbage collection.
````

In cpython primary algorithm for garbage collection is reference counting. Essentially, each object keeps count of how many reference points to it. As `refcount` reaches zero, the object is immediately destroyed.

You can use `weakref.finalize` register a callback function to be called when an object is destroyed

## Tricks Python Plays with immmutables

- tuple `t`, `t[:]` doesn’t make copy, but returns a reference to same object, you may also get reference even if you write `tuple(t)`
- same behaviour can be observed with instances of `str`, `bytes` and `frozenset` (note: `fs[:]` doesn’t exist, we meant to use `fs.copy()`)
- The sharing of string literals is an optimization technique called *interning*. CPython uses a similar technique with small integers to avoid  unnecessary duplication of numbers that appear frequently in programs  like 0, 1, –1, etc. Note that CPython does not intern all strings or integers, and the criteria it uses to do so is an undocumented implementation  detail.
- The tricks discussed in this section, including the behavior of `frozenset.copy()`, are harmless “lies” that save memory and make the interpreter faster. Do not worry about them, they should not give you any trouble because they only apply to immutable types.

---

## File: python/ch2_10.md

# Design Patterns with First-Class Functions

- In software engineering, a design pattern is a general recipe for solving a common design problem.

- The use of design is popularized by landmark book Design Patterns: Elements of Reusable Object Oriented Software by Gang of Four. Catalog of 23 patterns consisting of arrangements of classes exemplified with code in C++.

- Although designs are language independent, that does not mean every pattern applied to every language, python already implements iterator pattern using generators which don’t need class or anything work.

## Case Study: Refactoring Strategy

Strategy is a good example of a design pattern that can be simpler in Python if you leverage functions as first-class objects. 

### Classic Strategy

![Order discount calculations as strategies](./ch2_10.assets/flpy_1001.png)

Strategy pattern in summarized like this in Designed Patterns:

- Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.
- Here in an online order, discount be based on any strategy

````python
from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple, Optional


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity


class Order(NamedTuple):  # the Context
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional['Promotion'] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


class Promotion(ABC):  # the Strategy: an abstract base class
    @abstractmethod
    def discount(self, order: Order) -> Decimal:
        """Return discount as a positive dollar amount"""


class FidelityPromo(Promotion):  # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""

    def discount(self, order: Order) -> Decimal:
        rate = Decimal('0.05')
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)


class BulkItemPromo(Promotion):  # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""

    def discount(self, order: Order) -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal('0.1')
        return discount


class LargeOrderPromo(Promotion):  # third Concrete Strategy
    """7% discount for orders with 10 or more distinct items"""

    def discount(self, order: Order) -> Decimal:
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * Decimal('0.07')
        return Decimal(0)
````

- Notice how strategy instances are more like single method, as they have no attributes

````python
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Callable, NamedTuple


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self):
        return self.price * self.quantity

@dataclass(frozen=True)
class Order:  # the Context
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[['Order'], Decimal]] = None # typehints for callable

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'

def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)
````

### Choosing the Best Strategy: Simple Approach

Assume scenario where your best_promo finds you maximum discount you can avail.

````python
Order(joe, long_cart, best_promo)
````

````python
promos = [fidelity_promo, bulk_item_promo, large_order_promo]


def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)
````

- Now to add a new promotion strategy, we must make sure to add it to this list to avail discount correctly. 

### Finding Strategies in a Module

Modules in Python are also first-class objects, and the standard library provides several functions to handle them.

- `globals()` : Returns a dictionary representing the current global symbol table. This is always the dictionary of the current module (inside a function or method, this is the module where it is defined, not the module from its called)

````python
from decimal import Decimal
from strategy import Order
from strategy import (
    fidelity_promo, bulk_item_promo, large_order_promo
)

promos = [promo for name, promo in globals().items()
                if name.endswith('_promo') and
                   name != 'best_promo'
]


def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)
````

Another way of collecting the available promotions would be to create a  module and put all the  strategy functions there, except for `best_promo`.

```python
from decimal import Decimal
import inspect

from strategy import Order
import promotions


promos = [func for _, func in inspect.getmembers(promotions, inspect.isfunction)]


def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)
```

## Decorator-Enhanced Strategy Pattern

- we had problem where each strategy need to be added in `best_promo` function to actually be used or else it will be a subtle bug.
- we can use Registration decorators to avoid these issues.

````python
Promotion = Callable[[Order], Decimal]

promos: list[Promotion] = []


def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)
    return promo


def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)


@promotion
def fidelity(order: Order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)


@promotion
def bulk_item(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


@promotion
def large_order(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)
````

## The Command Pattern

![Command pattern application to text editor](./ch2_10.assets/flpy_1002.png)

The goal of Command is to decouple an object that invokes an operation  (the invoker) from the provider object that implements it (the  receiver). In the example from *Design Patterns*, each invoker is a menu item in a graphical application, and the receivers are the  document being edited or the application itself.

The idea is to put a `Command` object between the two, implementing an interface with a single method, `execute`, which calls some method in the receiver to perform the desired operation.

That way the invoker does not need to know the interface of the  receiver, and different receivers can be adapted through different `Command` subclasses.

Instead of giving the invoker a `Command` instance, we can simply give it a function. Instead of calling `command.execute()`, the invoker can just call `command()`. The `MacroCommand` can be implemented with a class implementing `__call__`.

---

## File: python/ch2_7.md

# Functions as First-Class Objects

First-class-objects is a program entity.

- created at runtime
- assigned a variable or element in a data structure
- passed as an argument to a function
- returned as the result of a function

## Treating a Function Like an Object

````python
def factorial(n):
  """return n!"""
  return 1 if n < 2 else n * factorial(n-1)
factorial(42) # 140500...
factorial.__doc__	# returns doc string
type(factorial)	# <class 'function'>

fact = factorial	# <function factorial at 0x..>
fact(5)	# 120
map(factorial, range(11))	# <map object at 0x..>
list(map(factorial, range(11)))	# [1, 1, 2, 6, ....]
````

## Higher Order Functions

A function that takes a function as an argument or returns a function as the result is a *higher-order function*. One example is `map`, another is `sorted` the optional `key` argument lets you provide a function to be applied to each item for sorting. `sorted(fruits, key = len)`

Some of the best know higher-order functions are `map`, `filter`, `reduce` and `apply`. `apply` was deprecated in python2.3 and removed in python3. As we can do `fn(*args, **kwargs)` instead or `apply(fn, args, kwargs)`

### Modern Replacements for map, filter and reduce

- `map` and `filter` functions are still built-ins in python3 but since introduction of listcomp and genexp they are not as important.

````python
list(map(factorial, range(6)))
[factorial(n) for n in range(6)]
# another
list(map(factorial, filter(lambda n : n%2, range(6))))
[ factorial(n) for n in range(6) if n%2 ]
````

- `reduce` was demoted from built-in in python2 to `functools` module in python3. Its most common use case, summation is better server by `sum` built-in

````python
from functools import reduce
from operator import add
reduce(add, range(100))
sum(range(100))
````

- Other reducing built-ins are `all` or `any`
  - `all(iterable)` : return `True` if there are no falsy elements in iterable
  - `any(iterable)` : returns `True` if any element of the `iterable` is truthy.

## Anonymous Functions

The `lambda` keyword creates an anonymous function within a Python expression.

However, the simple syntax of Python limits the body of `lambda` functions to be pure expressions. In other words, the body cannot contain other Python statements such as `while`, `try`, etc. Assignment with `=` is also a statement, so it cannot occur in a `lambda`.

The new assignment expression syntax using `:=` can be used—but if you need it, your `lambda` is probably too complicated and hard to read, and it should be refactored into a regular function using `def`.



````python
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
sorted(fruits, key=lambda word: word[::-1])
````

## The Nine Flavors of Callable Types

- User-defined functions
  - created with `def` statements or `lambda` expressions
- Built-in functions
  - A function implemented in C(for CPython), like `len` or `time.strftime`
- Built-in methods
  - Methods implemented in C, like `dict.get`
- Methods
  - Functions defined in the body of a class
- Classes
  - when invoked ad class runs its `__new__` method to create an instance then `__init__` to initialize it, and finally instance is returned to caller. There is no `new` operator in python
- Class instances
  - If a class defines `__call__` method, then its instances may be invoked as functions

- Generator Functions
  - Functions or methods that use the `yield` keyword in their body. When called, they return a generator object.
- Native coroutine functions
  - Functions or methods defined with `async def`. When called, they return a coroutine object. Added in Python 3.5.
- Asynchronous generator functions
  - Functions or methods defined with `async def` that have `yield` in their body. When called, they return an asynchronous generator for use with `async for`. Added in Python 3.6.

Given the variety of existing callable types in Python, the safest way to determine whether an object is callable is to use the `callable()`

## User Defined Callable Types

````python
import random

class BingoCage:

    def __init__(self, items):
        self._items = list(items)	# build local copy to avoid mutating items
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):	# shortcut to bingo.pick() : bingo()
        return self.pick()
````

## From Positional to Keyword-only Parameters

One of the best features of Python functions is the extremely flexible parameter handling mechanism. Closely related are the use of `*` and `**` to unpack iterables and mappings into separate arguments when we call a function.

````python
def tag(name, *content, class_=None, **attrs):
    """Generate one or more HTML tags"""
    if class_ is not None:
        attrs['class'] = class_
    attr_pairs = (f' {attr}="{value}"' for attr, value
                    in sorted(attrs.items()))
    attr_str = ''.join(attr_pairs)
    if content:
        elements = (f'<{name}{attr_str}>{c}</{name}>'
                    for c in content)
        return '\n'.join(elements)
    else:
        return f'<{name}{attr_str} />'
      
# we can invoke it in multiple ways
tag('br') # '<br />'
tag('p', 'hello') # '<p>hello</p>'
print(tag('p', 'hello', 'world'))
# <p>hello</p>
# <p>world</p>
tag('p', 'hello', id=33)  # <p id="33">hello</p>'
print(tag('p', 'hello', 'world', class_='sidebar'))  4
# <p class="sidebar">hello</p>
# <p class="sidebar">world</p>
tag(content='testing', name="img")  # '<img content="testing" />'
my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'class': 'framed'}
tag(**my_tag) #'<img class="framed" src="sunset.jpg" title="Sunset Boulevard" />'
````

Keyword-only arguments are a feature of Python 3. In Example above, the class_ parameter can only be given as a keyword argument—it will never capture **unnamed positional arguments**. To specify keyword-only arguments when defining a function, name them after the argument prefixed with *. If you don’t want to support variable positional arguments but still want keyword-only arguments, put a * by itself in the signature, like this:

````python
def f(a, *, b):
  return a, b

# now we cannot call b without keyword args
f(1, b = 2) # (1, 2)
f(1, 2)	# raises exception
````

### Positional Only Parameters

Since **Python 3.8**, user-defined function signatures may specify positional-only parameters. This feature always existed for built-in functions, such as `divmod(a, b)`, which can only be called with positional parameters, and not as `divmod(a=10, b=4)`.

To define a function requiring positional-only parameters, use `/` in the parameter list.

````python
def divmod(a, b, /):
  return (a // b, a%b)
````

## Packages for Functional Programming

### The operator Module

Often in functional programming it is convenient to use an arithmetic  operator as a function. For example, suppose you want to multiply a  sequence of numbers to calculate factorials without using recursion. To  perform summation, you can use `sum`, but there is no equivalent function for multiplication.

````python
from functools import reduce

def factorial(n):
    return reduce(lambda a, b: a*b, range(1, n+1))
````

````python
from functools import reduce
from operator import mul

def factorial(n):
    return reduce(mul, range(1, n+1))
````

````python
# itemgetter
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

from operator import itemgetter

for city in sorted(metro_data, key=itemgetter(1)):
    print(city)
````

Partial list of functions defined in operator:

````python
>>> [name for name in dir(operator) if not name.startswith('_')]
['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains',
'countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt',
'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imatmul',
'imod', 'imul', 'index', 'indexOf', 'inv', 'invert', 'ior',
'ipow', 'irshift', 'is_', 'is_not', 'isub', 'itemgetter',
'itruediv', 'ixor', 'le', 'length_hint', 'lshift', 'lt', 'matmul',
'methodcaller', 'mod', 'mul', 'ne', 'neg', 'not_', 'or_', 'pos',
'pow', 'rshift', 'setitem', 'sub', 'truediv', 'truth', 'xor']
````

#### Method caller

````python
from operator import methodcaller

s = 'The time has come'

upcase = methodcaller('upper')
print(upcase(s))  # Output: 'THE TIME HAS COME'

hyphenate = methodcaller('replace', ' ', '-')
print(hyphenate(s))  # Output: 'The-time-has-come'

````

### Freezing Arguments with functools.partial

`partial`: given a callable, it produces a new callable with  some of the arguments of the original callable bound to predetermined  values. This is useful to adapt a function that takes one or more arguments to an API that requires a callback with fewer arguments.

````python
from operator import mul
from functools import partial
triple = partial(mul, 3)	# how 3 is bound as first positional argument
triple(7)  # 21
list(map(triple, range(1, 10)))  # [3, 6, 9, 12, 15, 18, 21, 24, 27]
````



---

## File: python/ch2_8.md

# Type Hints in Functions

Type hints are the biggest change in the history of Python since the unification of types and classes in Python 2.2, released in 2001. However, type hints do not benefit all Python users equally. That’s why they should always be optional.

Goal for introduction is to help dev tools find bugs in python codebases via static analysis, i.e. without actually running the code through tests.

## About Gradual Typing

PEP 484 introduced *gradual type system* to Python. The Mypy type checker itself started as a language: a gradually typed dialect of Python with its own interpreter. Guido van Rossum convinced the creator of Mypy, Jukka Lehtosalo, to make it a tool for checking annotated Python code.

A gradual type system:

- Is optional
  - By default, the type checker should not emit warnings for code that has no type hints. Instead, type checker assumes the `Any` type when it cannot determine the type of an object. The `Any` type is considered compatibly with all other types.
- Does not catch type errors at runtime
  - Type hints are used by static type checkers, linters and IDEs to raise warnings. THey do not prevent incosistent values from being passed to function at runtime
- Does not enhance performance
  - provide data that could, in theory, allow optimizations in the generated byte code

The best usability feature of gradual typing is that annotation are always optional.

## Gradual Typing in Practice

````python
def show_count(count, word):
  if count == 1:
    return f'1{word}'
  count_str = str(count) if count else 'no'
  return f'{count_str}{word}s'
````

`pip install mypy` Installing mypy

Now writing `mypy file.py` gives no error for untyped defs. To make it strict use `--disallow-untyped-defs`

For the first steps with gradual typing, use another option : `--disallow-incomplete-defs`.

````python
def show_count(count: int, word: str)->str:
````

Allowing user to provide optional `plural` parameters.

````python
def show_count(count: int, singular: str, plural: str = '') -> str:
    if count == 1:
        return f'1 {singular}'
    count_str = str(count) if count else 'no'
    if not plural:
        plural = singular + 's'
    return f'{count_str} {plural}'
````

### Using None as a Default

If the optional parmeter expects a mutable type, then `None` is the only sensible default.

````python
from typing import Optional

def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
````

## Types are defined by supported operations

In practice, it’s more useful to consider the set of supported operations as the defining characteristic of a type.

```
def double(x):
    return x * 2
```

The `x` parameter type may be numeric (`int`, `complex`, `Fraction`, `numpy.uint32`, etc.) but it may also be a sequence (`str`, `tuple`, `list`, `array`), an N-dimensional `numpy.array`, or any other type that implements or inherits a `__mul__` method that accepts an `int` argument.

However consider this annotated `double`

````python
from collections import abc

def double(x: abc.Sequence):
    return x * 2
````

Type Checker will reject this code since `__mul__` is not implemented by abc.Sequence but at runtime this code works fine with concrete sequences such as str, tuple, list, array, etc.. as well numbers.

In a gradual type system, we have the interplay of two different views of types:

- Duck Typing
  - object have type but variables are untyped. In practice, it doesn’t matter what the declared type is, only what operations it supports. If I can invoke `birdie.quack()` then `birdie` is a duck in this context.
  - view adopted by Smalltalk, Javascript, and Ruby
- Nominal Typing
  - Objects and variables have types but objects only exist at runtime and type checker only the source code where variables are annotated with type hints.
  - If `Duck` is a subclass of `Bird`, you can assign a `Duck` instance to a parameter annotated as `birdie: Bird`. But in the body of the function, the type checker considers the call `birdie.quack()` illegal, because `birdie` is nominally a `Bird`, and that class does not provide the `.quack()` method. It doesn’t matter if the actual argument at runtime is a `Duck`, because nominal typing is enforced statically.
  - The view adopted by C++, Java, and C#, supported by annotated Python.

## Types Usable in Annotations

### The Any Type

- Aka `dynamic type`
- when type checker sees an untyped function like above assumes following

````python
def double(x: Any) -> Any:
  return x * 2
````

Contrast `Any` with `object`

```python
def double(x: object) -> object:
```

This function accepts arguments of every type, because every type is subtype of object

However type checker rejects this because `object`doesn’t implement `__mul__`

### Simple Types and Classes

Simple types like `int`, `float`, `str`, and `bytes` maybe used directly in type hints. concrete classes from the standard library, can also be used in type hints.

Abstract base classes are also useful in type hints.

Among classes, *consistent-with* is defined like *subtype-of*: a subclass is *consistent-with* all its superclasses.

However, “practicality beats purity,” so there is an important exception, which I discuss in the following tip.

### Optional and Union Types

The construct `Optional[str]` is actually a shortcut for `Union[str, None]`, which means the type of `plural` may be `str` or `None`.

We can write `str | bytes` instead of `Union[str, bytes]` since Python 3.10.

````python
plural: Optional[str] = None    # before
plural: str | None = None       # after
````

`Union[]` requires at least two types. Nested `Union` types have the same effect as a flattened `Union`. So this type hint:

```
Union[A, B, Union[C, D, E]]
```

is the same as:

```
Union[A, B, C, D, E]
```

### Generic Collections

- Most Python collections are heterogeneous.
- Generic types can be declared with type parameters to specify the type of the items they can handle.

````python
def tokenize(text: str) -> list[str]:
    return text.upper().split()
````

- Introduce from __future__ import annotations in Python 3.7 to enable the use of standard library classes as generics with list[str] notation.

- Make that behavior the default in Python 3.9: list[str] now works without the future import.

- Deprecate all the redundant generic types from the typing module. Deprecation warnings will not be issued by the Python interpreter because type checkers should flag the deprecated types when the checked program targets Python 3.9 or newer.

- Remove those redundant generic types in the first version of Python released five years after Python 3.9. At the current cadence, that could be Python 3.14, a.k.a Python Pi.

### Tuple Types

Three way to annotate tuple types : 

- Tuples as records
  - If you’re using a `tuple` as a record, use the `tuple` built-in and declare the types of the fields within `[]`.
  - e.g. `tuple[str, float, str]`
- Tuples as recrods with named fields
  - To annotate a tuple with many fields, or specific types of tuple your code uses in many places, use NamedTuple

````python
from typing import NamedTuple

from geolib import geohash as gh  # type: ignore

PRECISION = 9

class Coordinate(NamedTuple):
    lat: float
    lon: float

def geohash(lat_lon: Coordinate) -> str:
    return gh.encode(*lat_lon, PRECISION)
````

- Tuples as immutable sequences
  - To annotate tuples of unspecified length that are used as immutable lists, you must specify a single type, followed by a comma and `...`
  - The ellipsis indicates that any number of elements >= 1 is acceptable. There is no way to specify fields of different types for tuples of arbitrary length.
  - The annotations `stuff: tuple[Any, ...]` and `stuff: tuple` mean the same thing: `stuff` is a tuple of unspecified length with objects of any type.

### Generic Mappings

Generic mapping types are annotated as `MappingType[KeyType, ValueType]`. The built-in `dict` and the mapping types in `collections` and `collections.abc` accept that notation in Python ≥ 3.9.

- `dict[str, set[str]]`

### Abstract Base Classes

Be conservative in what you send, be liberal in what you accept. Postel’s law, a.k.a. the Robustness Principle.

````python
from collections.abc import Mapping

def name2hex(name: str, color_map: Mapping[str, int]) -> str:
````

- Above allows the caller to provide instance of `dict`, `defaultdict`, `ChainMap`, a `UserDict` subclass, or any other type that is a *subtype-of* `Mapping`.

````python
def name2hex(name: str, color_map: dict[str, int]) -> str:
````

- This one limits to only dict type
- therefore, in general it’s better to use `abc.Mapping` or `abc.MutableMapping` in parameter type hints, instead of `dict`

Postel’s law also tells us to be conservative in what we send. The return value of a function is always a concrete object, so the return type hint should be a concrete type

#### The fall of numeric tower

The `numbers` package defines the so-called numeric tower in order linear hierarchy of ABCs

- `Number`
- `Complex`
- `Real`
- `Rational`
- `Integral`

The “Numeric Tower” section of PEP 484 rejects the numbers ABCs and dictates that the built-in types `complex`, `float`, and `int` should be treated as special cases

### Iterable

The `typing.List` documentation I just quoted recommends `Sequence` and `Iterable` for function parameter type hints.

````python
from collections.abc import Iterable

FromTo = tuple[str, str]	# type alias

def zip_replace(text: str, changes: Iterable[FromTo]) -> str:	# Iterable[tuple[str, str]]
    for from_, to in changes:
        text = text.replace(from_, to)
    return text
````

from python 3.10 we should use this for type aliases

````python
from typing import TypeAlias

FromTo: TypeAlias = tuple[str, str]
````

#### abc.Iterable versus abc.Sequence

Both `math.fsum` and `replacer.zip_replace` must iterate over the entire `Iterable` arguments to return a result. Given an endless iterable such as the `itertools.cycle` generator as input, these functions would consume all memory and crash the Python process. Despite this potential danger, it is fairly common in modern Python to offer functions that accept an `Iterable` input even if they must process it completely to return a result. That gives the caller the option of providing input data as a generator instead of a prebuilt sequence, potentially saving a lot of memory if the number of input items is large.

### Parameterized Generics and TypeVar

- A parameterized generic is a generic type, written as `list[T]`, where `T` is a type variable that will be bound to a specific type with each usage. This allows a parameter type to be reflected on the result type.

Example Illustration for mode

````python
from collections import Counter
from collections.abc import Iterable

def mode(data: Iterable[float]) -> float:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]
````

- Many uses of mode involve `float` or `int` values but python has other numerical types so its desirable to have return type similar to `iterable` used.

````python
from collections.abc import Iterable
from typing import TypeVar

T = TypeVar('T')

def mode(data: Iterable[T]) -> T:
````

- When it first appears in the signature, the type parameter `T` can be any type. The second time it appears, it will mean the same type as the first.

#### Restricted TypeVar

`TypeVar` accepts extra positional arguments to restrict the type parameter. We can improve the signature of `mode` to accept specific number types, like this:

````python
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction
from typing import TypeVar

NumberT = TypeVar('NumberT', float, Decimal, Fraction)

def mode(data: Iterable[NumberT]) -> NumberT:
````

#### Bounded TypeVar

````python
from collections.abc import Iterable, Hashable

def mode(data: Iterable[Hashable]) -> Hashable:
````

- A restricted type variable will be set to one of the types named in the `TypeVar` declaration.

- A bounded type variable will be set to the inferred type of the expression—as long as the inferred type is *consistent-with* the boundary declared in the `bound=` keyword argument of `TypeVar`.

- The `typing` module includes a predefined `TypeVar` named `AnyStr`. It’s defined like this:

  ```
  AnyStr = TypeVar('AnyStr', bytes, str)
  ```

### Static Protocols

In OOPs, the concept of a `protocol` as an info

### Callable

- to annotate callback parameters or callable objects returned by higher-order-functions, `collections.abc` module provides `Callable` type, available in `typing` module for < 3.9

```py
Callable[[ParamType1, ParamType2], ReturnType]
```

```py
def repl(input_fn: Callable[[Any], str] = input]) -> None:
```

- during normal usage, the `repl` function uses Python’s `input` built-in to read expression from user. However for automated testing with other input sources, `repl` accepts an optional `input_fn` parameter (Callable) with same parameter and return types as input

#### Variance in Callable types

- it’s OK to provide a callback that returns an `int` when the code expects a callback that returns a `float`, because an `int` value can always be used where a `float` is expected.
- we say that `Callable[[], int]` is *subtype-of* `Callable[[], float]`—as `int` is *subtype-of* `float`. This means that `Callable` is ***covariant*** on the return type because the *subtype-of* relationship of the types `int` and `float` is in the same direction as the relationship of the `Callable` types that use them as return types.
- But, it’s a type error to provide a callback that takes a `int` argument when a callback that handles a `float` is required.
- `Callable[[int], None]` is not a *subtype-of* `Callable[[float], None]`. Although `int` is *subtype-of* `float`, in the parameterized `Callable` type the relationship is reversed: `Callable[[float], None]` is *subtype-of* `Callable[[int], None]`. Therefore we say that `Callable` is ***contravariant*** on the declared parameter types.

### NoReturn

- special type used to annotate return type of functions that never return
- they exist to raise exceptions
- e.g. `sys.exit()` raises `SystemExit` to terminate python process

````python
def exit(__status: object = ...) -> NoReturn: ...
````

- `__status` parameter is positional only, and it has a default value
- Stub files don’t spell out the default values, they use ... instead.

## Annotating Positional Only and Variadic Parameters

In previous tag example we saw the signature was:

````python
def tag(name, /, *content, class_=None, **attrs):
````

Here is `tag` fully annotated, written in several lines - a common convention for long signatures.

````python
from typing import Optional
def tag(
	name: str,
  /,
  *content: str,	# for arbitrary positional parameters, type in local `content` var => tuple[str, ...]
  class_: Optional[str] = None,
  **attrs: str,	# type hint : dict[str, str], for floats its dict[str, float], for different types you will need to use a Union or Any
) -> str
````

## Imperfect Typing and Strong Testing

Maintainers of large corporate codebases report that many bugs are found by static type checkers and fixed more cheaply than if the bugs were discovered only after the code is running in production. However, it’s essential to note that automated testing was standard practice and widely adopted long before static typing was introduced in the companies.

Even in the contexts where they are most beneficial, static typing cannot be trusted as the ultimate arbiter of correctness. It’s not hard to find:

- False positives

  Tools report type errors on code that is correct.

- False negatives

  Tools don’t report type errors on code that is incorrect.

Also, if we are forced to type check everything, we lose some of the expressive power of Python:

- Some handy features can’t be statically checked; for example, argument unpacking like `config(**settings)`.
- Advanced features like properties, descriptors, metaclasses, and  metaprogramming in general are poorly supported or beyond comprehension  for type  checkers.
- Type checkers lag behind Python releases, rejecting or even crashing  while analyzing code with new language features—for more than a year in  some cases.

Common data constraints cannot be expressed in the type system—even simple ones.

---

## File: python/ch2_9.md

# Decorators and Closures

Function decorators let us `mark` functions in the source code tto enhance their behaviour in some way.

The most obscure reserved keyword in Python is `nonlocal`, introduced in Python 3.0. You can have a profitable life as a Python programmer without ever using it if you adhere to a strict regimen of class-centered object orientation. However, if you want to implement your own function decorators, you must understand closures, and then the need for `nonlocal` becomes obvious.

## Decorators 101

A decorator is a callable that takes another function as an argument (the decorated function)

````python
@decorate
def target():
  print('running target')
````

Its similar to

````python
def target():
  print('running target')
target = decorate(target)	# note how its bound to same function name
````

Another example to prove above point how we modify the function.

````python
def deco(func):
  def inner():
    print('running inner')
  return inner

@deco
def target():
  print('running target')
  
target()
# running inner
````

Strictly speaking, decorators are just syntactic sugar.

Three essential facts make a good summary of decorators:

- A decorator is a function or another callable.
- A decorator may replace the decorated function with a different one.
- Decorators are executed immediately when a module is loaded.

## When Python Executes Decorators

A key features of decorators is that they run right after the decorated function is defined. That is usually at import time.

````python
registry = []

def register(func):
    print(f'Registering function: {func.__name__}')
    registry.append(func)
    return func

@register
def f1():
    print('Running f1()')

@register
def f2():
    print('Running f2()')

def f3():
    print('Running f3()')

def main():
    print('Running main()')
    print('Registry:', registry)
    f1()
    f2()
    f3()

if __name__ == '__main__':
    main()
````

Output of above program

````python
running register(<function f1 at 0x100631bf8>)
running register(<function f2 at 0x100631c80>)
running main()
registry -> [<function f1 at 0x100631bf8>, <function f2 at 0x100631c80>]
running f1()
running f2()
running f3()
````

## Registration Decorators

There are two ways decorators are used in real-code

- The decorator function is defined in the same module as the decorated functions. A real decorator is usually defined in one module and  applied to functions in other modules.
- The `register` decorator returns the same function passed as an argument. In practice, most decorators define an inner function and return it.

## Variable Scope Rules

we define and test a function that reads two variables: a local variable `a`—defined as function parameter—and variable `b` that is not defined anywhere in the function.

````python
def f1(a):
  print(a)
  print(b)	# not defined error
````

Interesting example

````python
b = 6
def f1(a):
  print(a)
  print(b)
  b = 9
# this raises different error, UnboundLocalError, b referenced before assignment
````

- Awkward behaviour of above function is due to Python compiling body of the function first and deciding that `b` is a local variable.
- This is not a bug, but a design choice

f we want the interpreter to treat `b` as a global variable and still assign a new value to it within the function, we use the `global` declaration:

````python
b = 6
def f1(a):
  global b
  print(a)
  print(b)
  b = 9
````

We see two scopes in action :

- The module global scope
  - Made of names assigned to values outside of any class or function block.
- The f3 function local scope
  - Made of names assigned to values as parameters, or directly in the body of the function.

There is one other scope where variables can come from, which we call *nonlocal* and is fundamental for closures

## Closures

In the blogosphere, closures are sometimes confused with anonymous functions. Many confuse them because of the parallel history of those features: defining functions inside functions is not so common or convenient, until you have anonymous functions. And closures only matter when you have nested functions.

- a closure is a function—let’s call it `f`—with an extended scope that encompasses variables referenced in the body of `f` that are not global variables or local variables of `f`. Such variables must come from the local scope of an outer function that encompasses `f`.

It does not matter whether the function is anonymous or not; what matters is that it can access nonglobal variables that are defined outside of its body.

Consider an `avg` function to compute the mean of ever-growing series of values.

````python
avg(10)	# 10
avg(11) # 10.5
avg(12) # 11
````

NOTE: how average function seems to have memory, let’s implement using a class.

````python
class Averager():

    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)
````

````python
avg = Average()
avg(10)
avg(11)
avg(12)
````

We can emulate similar behaviour using high-order functions

````python
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager
````

````python
avg = make_average()
avg(10)
avg(11)
avg(12)
````

- How does the make_averager keep track of the history ?
- `series` is a local variable of make_averager, because its assigned inside body of it. its local scope should be gone with each call but it somehow persists.
- Within `make_average`, we call `series` is a *free variable*. This is a technical term meaning its not bound in the local scope anymore.

![Closure diagram](./ch2_9.assets/flpy_0901.png)

We can inspect by using following commands

````python
>>> avg.__code__.co_varnames
('new_value', 'total')
>>> avg.__code__.co_freevars
('series',)
````

## The nonlocal Declaration

Our previous `make_averager` was not efficient. We stored all values in the historical series and computed their `sum` every time averager was called. Let’s implement much better version

````python
def make_averager():
  cnt = 0
  total = 0
  
  def averager(new_value):
    cnt += 1
    total += new_value
    return total/cnt
  return averager
````

```python
# when executed you get : UnboundLocalError: local variable 'count' referenced before assignment
```

- wait why ? because statement `count += 1` actually means the same as `count = count+1` when `count` is a number or any immutable type. So we are actually assigning to `count` in the body of averager, and that makes its scope local.
- This worked fine with our mutable list, and we only used `append` and `len` method, but how to deal with immutable types ? (newly created always)
- To work around this we use `nonlocal` keyword

````python
def make_averager():
  cnt = 0
  total = 0
  
  def averager(new_value):
    nonlocal count, total
    cnt += 1
    total += new_value
    return total/cnt
  return averager
````

When a function is defined, the Python bytecode compiler determines how to fetch a variable `x` that appears in it, based on these rules:

- If there is a `global x` declaration, `x` comes from and is assigned to the `x` global variable module.
- If there is a `nonlocal x` declaration, `x` comes from and is assigned to the `x` local variable of the nearest surrounding function where `x` is defined.
- If `x` is a parameter or is assigned a value in the function body, then `x` is the local  variable.
- If `x` is referenced but is not assigned and is not a parameter:
  - `x` will be looked up in the local scopes of the surrounding function bodies (nonlocal scopes).
  - If not found in surrounding scopes, it will be read from the module global scope.
  - If not found in the global scope, it will be read from `__builtins__.__dict__`.

## Implementing a Simple Decorators

````python
import time

def clock(func):
  def clocked(*args):
    t0 = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter()-t0
    name = func.__name__
    arg_str = ','.join(repr(arg) for arg in args)
    print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
    return result
  return clocked
````

````python
@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)
  
# internally : factorial = clock(factorial)
# even if you do __name__ for it, output will be `clocked`
````

A more improved clocker that supports keyword arguments and doesn’t mask original functions `__doc__`, `__name__`

````python
import time
import functools


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
        arg_str = ', '.join(arg_lst)
        print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')
        return result
    return clocked
````

## Decorators in Standard Library

### Memoization with functools.cache

- The `functools.cache` decorator implements `memoization`

````python
from clockdeco import clock
import functools

@functools.cache
@clock
def fib(n):
  if n < 2:
    return n
  return fib(n-1) + fib(n-2)
````

````python
# NOTE:
@alpha
@beta
def my_func():
  ...
  
# above syntax resolves to : my_func = alpha(beta(my_func))
````

`functools.cache` can consume all available memory if there is a very large number of cache entries. Consider it more suitable for use in short-lived command-line scripts. In long-running processes, It is recommended using `functools.lru_cache` with a suitable `maxsize` parameter, as explained in the next section.

### Using lru_cache

The `functools.cache` decorator is actually a simple wrapper around the older `functools.lru_cache` function, which is more flexible and compatible with Python 3.8 and earlier versions.

The main advantage of `@lru_cache` is that its memory usage is bounded by the  `maxsize` parameter, which has a rather conservative default value of 128—which means the cache will hold at most 128 entries at any time.

````python
@lru_cache
def my_costly_func(a,b):
  ...
````

- Accepts two params
  - `maxsize=128` : maximum entries in lru
  - `typed=False` : determines whether to store different arg types separately.

### Single Dispatch Generic Functions

Consider this function to htmlize a python obj, but it depends on `repr` of object which may not be useful for all objects.

````python
import html

def htmlize(obj):
    content = html.escape(repr(obj))
    return f'<pre>{content}</pre>'
````

- since we don’t have method overloading in python, we can create either variation of the `htmlize` with different name suffixed/prefixed with its type or we can use long `if/elif/..` or `match/case/..`
- so alternative way to do this is to use singledispatch and then register our overloading function on top of it.

````python
from functools import singledispatch
from collections import abc
import fractions
import decimal
import html
import numbers

@singledispatch
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f'<pre>{content}</pre>'

@htmlize.register
def _(text: str) -> str:
    content = html.escape(text).replace('\n', '<br/>\n')
    return f'<p>{content}</p>'

@htmlize.register
def _(seq: abc.Sequence) -> str:
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'

@htmlize.register
def _(n: numbers.Integral) -> str:
    return f'<pre>{n} (0x{n:x})</pre>'

@htmlize.register
def _(n: bool) -> str:
    return f'<pre>{n}</pre>'

@htmlize.register(fractions.Fraction)
def _(x) -> str:
    frac = fractions.Fraction(x)
    return f'<pre>{frac.numerator}/{frac.denominator}</pre>'

@htmlize.register(decimal.Decimal)
@htmlize.register(float)
def _(x) -> str:
    frac = fractions.Fraction(x).limit_denominator()
    return f'<pre>{x} ({frac.numerator}/{frac.denominator})</pre>'
````

## Parameterized Decorators

- when parsing a decorator source code, python takes decorated function and passes it as the first argument to decorator functions.
- we use decorator factory that takes arguments and return decorator which is then applied to the function

````python
registry = set()

def register(active=True):
  def decorate(func):
    print('running register'f'(active={active})->decorate({func})')
   	if active:
      registry.add(func)
    else:
      registry.discard(func)
    return func
  return decorate

@register(active=False)
def f1():
  print('running f1()')
  
@register()
def f2():
  print('running f2()')

def f3()
	print('running f3()')
  
# Output
# running register(active=False)->decorate(<function f1 at 0x10063c1e0>)
# running register(active=True)->decorate(<function f2 at 0x10063c268>)
# >>> registration_param.registry
# [<function f2 at 0x10063c268>]
````



---

## File: python/ch3_11.md

# A Pythonic Object

Thanks to the Python Data Model, your user-defined types can behave as  naturally as the built-in types. And this can be accomplished without  inheritance, in the spirit of *duck typing*: you just implement the methods needed for your objects to behave as expected.

But if you are writing a library or a framework, the programmers who will use your classes may expect them to behave like the classes that Python provides. Fulfilling that expectation is one way of being “Pythonic.”

## Object Representation

Every object-oriented language has at least one standard way of getting a string representation from any object. Python has 2

- `repr()` : return a string representing the object as the developer want to see it. Its what we get using python console or debugger.
- `str()` : returns a string representing the object as user want to see it. `print()` calls it.

There are two additional special methods to support alternative representations of objects: `__bytes__` and `__format__`.

## Vector Class Redux

````python
from array import array
import math


class Vector2d:
    typecode = 'd'	# Class Attribute

    def __init__(self, x, y):
        self.x = float(x)	# early conversion to prevent bugs
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))	# makes vector iterable

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self) # builds string

    def __str__(self):
        return str(tuple(self))	# tuple for display

    def __bytes__(self): # to generate `bytes` we convert typecode to bytes and concatenate
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))	

    def __eq__(self, other):
        return tuple(self) == tuple(other) # comparison

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))
````

## An Alternative Contructor

Since we can export a `Vector2d` as bytes, naturally we need a method that imports a `Vector2d` from a binary sequence. Looking at the standard library for inspiration, we find that `array.array` has a class method named `.frombytes` that suits our purpose

````python
    @classmethod # modifies method to be directly callable on a class
    def frombytes(cls, octets): # note we pass cls args rather than self.
        typecode = chr(octets[0]) # read typecode from first byte
        memv = memoryview(octets[1:]).cast(typecode) # create a memory view
        return cls(*memv) # unpack memory view resulting from the cast
````

## classmethod v/s staticmethod

The `classmethod` decorator is not mentioned in the Python tutorial, and neither is `staticmethod`. Anyone who has learned OO in Java may wonder why Python has both of these decorators and not just one of them.

- `classmethod` : to define a method that operates on the class and not on instances.
- `classmethod` changes the way the method is called, so it  receives the class itself as the first argument, instead of an instance. Its most common use is for alternative constructors
- the `staticmethod` decorator changes a method so that it  receives no special first argument. In essence, a static method is just  like a plain function that happens to live in a class body, instead of  being defined at the module level.

````python
class Demo:
  @classmethod
  def Klassmeth(*args):
    return args
  @staticmethod
  def statmeth(*args):
    return args
  
Demo.klassmeth()	# (<class '__main__.Demo'>,)
Demo.klassmeth('spam') # (<class '__main__.Demo'>, 'spam')

Demo.statmeth() # ()
Demo.statmeth('spam') # ('spam',)
````

The `classmethod` decorator is clearly useful, but good use cases for `staticmethod` are very rare in my experience.

## Formatted Displays

The f-strings, the `format()` built-in function, and the `str.format()` method delegate the actual formatting to each type by calling their `.__format__(format_spec)` method.

The `format_spec` is a formatting specifier, which is either:

- The second argument in `format(my_obj, format_spec)`, or
- Whatever appears after the colon in a replacement field delimited with `{}` inside an f-string or the `fmt` in `fmt.str.format()`

````python
brl = 1/4.82
brl	# 0.20746887966804978
format(brl, '0.4f')	# 0.2075
"1 BRL = {rate:0.2f} USD".format(rate=brl)
f"1 USD = {1/brl:0.2f} BRL"	# f string syntax
````

The notation used in the formatting specifier is called the Format Specification Mini-Language.

The Format Specification Mini-Language is extensible because each class gets to interpret the `format_spec` argument as it likes. For instance, the classes in the `datetime` module use the same format codes in the `strftime()` functions and in their `__format__` methods.

````python
from datetime import datetime
now = datetime.now()
format(now, "%H%M:%s")
"It's now {:%I:%M %p}".format(now)
````

````python
  # inside the Vector2d class

    def __format__(self, fmt_spec=''):
        components = (format(c, fmt_spec) for c in self) # apply spec to each component
        return '({}, {})'.format(*components) # plug formatted string in (x,y)
      

# more improved version that support polar co-ordinates using p
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)
      
      
# output
format(Vector2d(1, 1), 'p')
format(Vector2d(1, 1), '.3ep')
format(Vector2d(1, 1), '0.5fp')
````

## A Hashable Vector2d

So far `Vector2d` instances are not hashable so we can’t put them in a `set`

To make it hashable we need to implement `__hash__` and `__eq__` (already done) and make vector instances immutable. Because anyone can change them right now using v1.x = 0 and there is nothing in code to prevent that.

````python
class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)	# use __ to make attribute private
        self.__y = float(y)

    @property # marks the getter method of a property
    def x(self): # getter must be named after the public property it exposes
        return self.__x	 # just return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))
    
    def __hash__(self):
        return hash((self.x, self.y))	# hashed the tuple of co-ordinates

    # remaining methods: same as previous Vector2d
````

## Supporting Positional Pattern Matching

So far, Vector2d instances are compatible with keyword class patterns—covered in “Keyword Class Patterns”.

````python
def keyword_pattern_demo(v: Vector2d) -> None:
    match v:
        case Vector2d(x=0, y=0):
            print(f'{v!r} is null')
        case Vector2d(x=0):
            print(f'{v!r} is vertical')
        case Vector2d(y=0):
            print(f'{v!r} is horizontal')
        case Vector2d(x=x, y=y) if x==y:
            print(f'{v!r} is diagonal')
        case _:
            print(f'{v!r} is awesome')
````

However if try to use a position pattern like this: it fails

````python
 				case Vector2d(_, 0):
            print(f'{v!r} is horizontal')
````

```python
TypeError: Vector2d() accepts 0 positional sub-patterns (1 given)
```

To make `Vector2d` work with positional patterns, we need to add a class attribute named `__match_args__` , listing the instance attributes in the order they will be used for positional pattern matching:

````python
class Vector2d:
    __match_args__ = ('x', 'y')
````

Now we can use positional patterns

````python
def positional_pattern_demo(v: Vector2d) -> None:
    match v:
        case Vector2d(0, 0):
            print(f'{v!r} is null')
        case Vector2d(0):
            print(f'{v!r} is vertical')
        case Vector2d(_, 0):
            print(f'{v!r} is horizontal')
        case Vector2d(x, y) if x==y:
            print(f'{v!r} is diagonal')
        case _:
            print(f'{v!r} is awesome')
````

## Complete Listing of Vector2d, version3

````python
from array import array
import math

class Vector2d:
    __match_args__ = ('x', 'y')

    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
````

## Private and “Protected” Attributes in Python

In Python, there is no way to create private variables like there is with the `private` modifier in Java. What we have in Python is a simple mechanism to  prevent accidental overwriting of a “private” attribute in a subclass.

Consider this scenario: someone wrote a class named `Dog` that uses a `mood` instance attribute internally, without exposing it. You need to subclass `Dog` as `Beagle`. If you create your own `mood` instance attribute without being aware of the name clash, you will clobber the `mood` attribute used by the methods inherited from `Dog`. This would be a pain to debug.

To prevent this, if you name an instance attribute in the form `__mood` (two leading underscores and zero or at most one trailing underscore), Python stores the name in the instance `__dict__` prefixed with a leading underscore and the class name, so in the `Dog` class, `__mood` becomes `_Dog__mood`, and in `Beagle` it’s `_Beagle__mood`. This language feature goes by the lovely name of *name mangling*.

The name mangling functionality is not loved by all Pythonistas, and neither is the skewed look of names written as `self.__x`. Some prefer to avoid this syntax and use just one underscore prefix to “protect” attributes by convention (e.g., `self._x`)

The single underscore prefix has no special meaning to the Python  interpreter when used in attribute names, but it’s a very strong  convention among Python programmers that you should not access such  attributes from outside the class.

## Saving Memory with `__slots__`

By default, Python stores the attributes of each instance in a `dict` named `__dict__`. A `dict` has a significant memory overhead - even with the optimizations implemented.

- if you define a class attribute named `__slots__` holding a sequence of attribute names, Python uses an alternative storage model for the instance attributes: the attributes named in `__slots__` are stored in a hidden array or references that use less memory than a `dict`

````python
class Pixel:
  __slots__ = ('x', 'y')

p = Pixel()
p.__dict__	# throws attribute error
p.x = 10
p.y = 20
p.color = 'Red' # throws attribute error

# slots are not inherited
class OpenPixel(Pixel):
  pass
op = OpenPixel()
op.__dict__	# works
op.color = 'green'	# works
````

````python
class ColorPixel(Pixel):
  __slots__ = ('color',)

cp = ColorPixel()
cp.__dict__	# raises attribute error
cp.x = 10
cp.color = 'red'
cp.flavor = 'banana'	# raises attribute error
````

### Issues with `__slots__`

- you must remember to redeclare `__slots__` in each subclass to prevent their instance having `__dict__`
- instances will only be able to have attributes listed in `__slots__`, unless we include `__dict__` in slots.
- Classes using `__slots__` can’t use `@chached_property` decorator, unless they explicitly name `__dict__` in `__slots__`
- Instances can’t be targets of weak references unles you add `__weakref__` in `__slots__`



## Overriding Class Attributes

- class attributes can be used as default values for instance attributes
- we can access them as `self.attribute_name`
- if we declare a instance attribute then the class attribute is left untouched and `self.attribute_name` will always reference to instance attribute.
- If you want to change a class attribute, you must set it on the class directly, not through an instance.
- In python more idiomatic way to achieve it how Django does it. Create subclasses which change class attributes.

````python
from vector2d_v3 import Vector2d
class ShortVector2d(Vector2d)
	typecode = 'f'
````

- Another thing to note is following function which doesn’t hardcodes class name in its representation

````python
    # inside class Vector2d:

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)
````

This way `f` typecodes work fine in representation as well.

---

## File: python/ch3_12.md

# Special Methods for Sequences

## Vector: A User-Defined Sequence Type

Our strategy to implement `Vector` will be use composition, not inheritance. We’ll store the components in an `array` of floats, and will implement the methods needed for out `Vector` to behave like an immutable flat sequence.

## Vector Take #1: Vector2d Compatible

The first version of `Vector` should be compatible as possible with our `Vector2d` class.

````python
from array import array
import reprlib
import math


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components) # hold an array with Vector components

    def __iter__(self):
        return iter(self._components) # to allow iteration return iter 

    def __repr__(self):
        components = reprlib.repr(self._components)	# get limited lenght representation of array : array('d', [0.0, 1.0, 2.0, 3.0, 4.0, ...])
        components = components[components.find('['):-1] # remove the array('d' part from above representation
        return f'Vector({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(*self)	# n dimesional points

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
````

## Protocols and Duck Typing

In the context of object-oriented programming, a protocol is an informal interface, defined only in documentation and not in code. For example,  the sequence protocol in Python entails just the `__len__` and `__getitem__` methods.

````python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
````

An experienced Python coder will look at it and understand that it *is* a sequence, even if it subclasses `object`. We say it *is* a sequence because it *behaves* like one, and that is what matters.

This became known as *duck typing*, after Alex Martelli’s post quoted at the beginning of this chapter.

>Don’t check whether it *is*-a duck: check whether it *quacks*-like-a duck, *walks*-like-a duck, etc., etc., depending on exactly what subset of duck-like behavior you need to play your language-games with. (`comp.lang.python`, Jul. 26, 2000)

Because protocols are informal and unenforced, you can often get away  with implementing just part of a protocol, if you know the specific  context where a class will be used. 

## Vector Take #2: A Sliceable Sequence

- supporting sequence protocol is really easy if you can delegate to a sequence attribute in your objects. `__len__` and `__getitem__` are good start.

````python
class Vector:
    # many lines omitted
    # ...

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        return self._components[index]
      
# we can now use indexing and slicing works
v1 = Vector([3, 4, 5])
len(v1)
v1[0], v1[-1]
v7 = Vector(range(7))
v7[1:4]
````

### How slicing works

Notation : `nums[a:b:c]` internally becomes `slice(a,b,c)` and then `__getitem__` recieve this tuple

### A Slice-Aware `getitem`

````python
    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)	# calls __index__
        return self._components[index]
````

## Vector Take #3: Dynamic Attribute

In the evolution from `Vector2d` to `Vector`, we lost the ability to access vector components by name (e.g., `v.x`, `v.y`). We are now dealing with vectors that may have a large number of  components. Still, it may be convenient to access the first few  components with shortcut letters such as `x`, `y`, `z` instead of `v[0]`, `v[1]`, and `v[2]`.

````python
    __match_args__ = ('x', 'y', 'z', 't') # set this to allow positional pattern matching on dynamic attributes

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name) # try to get position of name in __match_args
        except ValueError: # value error if name doesn't exits
            pos = -1
        if 0 <= pos < len(self._components): # return component in valid range
            return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'  6
        raise AttributeError(msg)
````

````python
v = Vector(range(5))
v # Vector([0.0, 1.0, 2.0, 3.0, 4.0])
v.x # 0.0
v.x = 10 # 
v.x # returns 10 
v # Vector([0.0, 1.0, 2.0, 3.0, 4.0]) # wait why this is not updated, because first time we were calling v.x to get the attribute
````

- because of the way `__getattr__` works: Python only calls  that method as a fallback, when the object does not have the named  attribute. However, after we assign `v.x = 10`, the `v` object now has an `x` attribute, so `__getattr__` will no longer be called to retrieve `v.x`: the interpreter will just return the value `10` that is bound to `v.x`. On the other hand, our implementation of `__getattr__` pays no attention to instance attributes other than `self._components`, from where it retrieves the values of the “virtual attributes” listed in `__match_args__`.

````python
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)
````



## Vector Take #4: Hashing and a Faster `==`

- we will implement xor of every component in succession for hashing

````python
from array import array
import reprlib
import math
import functools
import operator


class Vector:
    typecode = 'd'

    # many lines omitted in book listing...

    def __eq__(self, other):  3
        return tuple(self) == tuple(other)

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    # more lines omitted...
````

- NOTE: we may have a problem when using `__eq__`, as it may return Vector([1,2]) equal to (1,2) which maybe a problem.
- vector instances may have thousand of components, its inefficient

````python
    def __eq__(self, other):
        if len(self) != len(other): # different length then return false
            return False
        for a, b in zip(self, other): # zip produces generator of tuples made from items in each iterable argument
            if a != b:	# as soon as two component are different return
                return False
        return True
````

## Vector Take #5: Formatting

`Vector` will use spherical coordinates—also known as “hyperspherical” coordinates, because now we support *n* dimensions, and spheres are “hyperspheres” in 4D and beyond.[6](https://learning.oreilly.com/library/view/fluent-python-2nd/9781492056348/ch12.html#idm46582425554624) Accordingly, we’ll change the custom format suffix from `'p'` to `'h'`.

````python
from array import array
import reprlib
import math
import functools
import operator
import itertools


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]

    __match_args__ = ('x', 'y', 'z', 't')

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'
        raise AttributeError(msg)

    def angle(self, n):
        r = math.hypot(*self[n:])
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):  # hyperspherical coordinates
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)],
                                     self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)  7
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
````





---

## File: python/ch3_13.md

# Interfaces, Protocols and ABCs

*Program to an interface, not an implementation*. First principle of Object-Oriented Design.

Depending on the programming language, we have one or more ways of defining and using interfaces.

1. Duck Typing : python’s default approach from beginning
2. Goose Typing : approach supported by ABCs since python2.6, relies on runtime checks of objects against ABCs
3. Static Typing: traditional approch of statically-typed language like C and Java, supported since Python3.5 by `typing` module and enforced by external type checkers compliant with PEP484
4. Static Duck Typing: An approach made popular by `Go` language, supported by subclasses of `typing.Protocol` new in python 3.8, enforce by external type checkers.

## The Typing Map

![Four approaches to type checking](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_1301.png)

Each of these four approaches rely on interfaces to work, but static typing can be done—poorly—using only concrete types instead of interface abstractions like protocols and abstract base classes.

## Two Kinds of Protocols

The word `protocol` has different meanings in computer science.

- A network protocol specifies commands that a client can send to server, `GET`, `POST`, and `HEAD`.

An object protocol specifies methods which an object must provide to fulfill a role. sequence protocol : methods which allow python object to behave as a sequences.

Implementing protocol requires bunch of methods but we can go by implementing few of them. Implementing `__getitem__` is enough to retrieve items by index, and support iteration and the `in` operator.

Protocol is a *informal interface*

earlier most of documentation refer to these as protocols (<3.8) but after PEP 544, Static Protocols allows us to create subclasses of `typing.Protocol` to define one or more methods that a class must implement (or inherit) to satisfy a static type checker.

- Dynamic Protocol : Informal protocols python always had
- Static Protocols : protocols defined by PEP 544 standard.

## Programming Ducks

### Python Digs Sequences

philosophy of Python Data Model is to cooperate with essential dynamic protocols as much as possible. When it comes to sequences, python tries hard to work with even simplest implementation.

![UML class diagram for `Sequence`](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_1302.png)

- Note: How sequence interface is formalized as an ABC. NOTE: python interpretor and built-ins like `list` , `str` do not rely on ABC at all.

- Most ABCs in the `collections.abc` module exist to formalize interfaces that are implemented by built-in objects and are implicitly supported by the interpreter—both of which predate the ABCs themselves. The ABCs are useful as starting points for new classes, and to support explicit type checking at runtime (a.k.a. *goose typing*) as well as type hints for static type checkers.

`Vowels` class didn’t have any `__iter__` method and neither it inherited `abc.Sequence` and only implemented `__getitem__` but still it was iterable because of python fallback to `__getitem__` method for iteration. `in` method also works without any implementations of `__contains__`.

### Monkey Patching : Implementing a Protocol at Runtime

Monkey patching is dynamically changing a module, class or function at runtime to add feature or fix bugs. For e.g. the gevent library monkey patches parts of Python’s standard library to allow lightweight concurrency without threads or `async`/`await`

````python
# from our deck example there is no shuffle method

# we need something like this :
from random import shuffle
l = list(range(10))
shuffle(l)
l	@ [1, 3, 4, 9, 7, 8, 2, 5, 6]

# but if we try to shuffle FrenchDeck class it fails
shuffle(deck)
FrenchDeck' object does not support item assignment
````

Mutable sequences must also provide a `__setitem__` method.

````python
def set_card(deck, position, card):			# self, key, value
  deck._cards[position] = card
FrenchDeck.__setitem__ = set_card		# monkey patching
shuffle(deck)
# works
````

Monkey patching is powerful, but the code that does the actual patching is very tightly coupled with the program to be patched, often handling private and undocumented attributes.

Besides being an example of monkey patching, Example 13-4 highlights the dynamic nature of protocols in dynamic duck typing: random.shuffle doesn’t care about the class of the argument, it only needs the object to implement methods from the mutable sequence protocol. It doesn’t even matter if the object was “born” with the necessary methods or if they were somehow acquired later.

### Defensive Programming and Fail Fast

Defensive programming is like defensive driving: a set of practices to enhance safety even when faced with careless programmers—or drivers.

Many bugs cannot be caught except at runtime—even in mainstream statically typed languages. In a dynamically typed language, “fail fast” is excellent advice for safer and easier-to-maintain programs. 

Failing fast means raising runtime errors as soon as possible, for example, rejecting invalid arguments right a the beginning of a function body.

````python
    def __init__(self, iterable):
        self._balls = list(iterable)

# here no need to check if iterable is list or not, immidiatedly build a list out of it
# not it might be bad if data shouldn't be copied (large data). In that case use isinstance(x, abc.MutableSequence)
````

If you are afraid to get an infinite generator—not a common issue—you can begin by calling `len()` on the argument. This would reject iterators, while safely dealing with tuples, arrays, and other existing or future classes that fully implement the `Sequence` interface. Calling `len()` is usually very cheap, and an invalid argument will raise an error immediately.

- Defensive code leveraging duck types can also include logic to handle different types without using `isinstance()` or `hasattr()` tests.

````python
# Duck typing to handle a string or an iterable of strings
		try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        pass
    field_names = tuple(field_names)
    if not all(s.isidentifier() for s in field_names):
        raise ValueError('field_names must all be valid identifiers')
````

- sometimes duck typing is more expressive than static type hints

````python
    def namedtuple(
        typename: str,
        field_names: Union[str, Iterable[str]],		# duck typing is more expressive for this
        *,
        # rest of signature omitted
````

## Goose Typing

*An abstract class represents an interface.* -Bjarne Stroustrup, creator of C++.

Python doesn’t have an `interface` keyword. We use abstract base classes (ABCs) to define interfaces for explicit type checking at runtime - also supported by static type checkers.

Abstract base classes complement duck typing by providing a way to define interfaces when other techniques like `hasattr()` would be clumsy or subtly wrong (for example, with magic methods). ABCs introduce virtual subclasses, which are classes that don’t inherit from a class but are still recognized by `isinstance()` and `issubclass()`; see the `abc` module documentation.

### Waterfowl and ABCs - An Essay by Alex Martelli

In Python, this mostly boils down to avoiding the use of `isinstance` to check obejct’s type, not to mention worst way of checking `type(foo) is bar`.

The overall *duck typing* approach remains quite useful in many contexts - yet it many other and often preferable one has evolved over time.

````python
class Artist:
    def draw(self): ...

class Gunslinger:
    def draw(self): ...

class Lottery:
    def draw(self): ...
````

- mere existence of a method named draw, called without args, ensures x.draw() and y.draw() can be called, and any way exchangeable or abstractly equivalent - nothing about the simlarity of semantics resulting from such calls can be inferred.

- Rather, we need a knowledgeable programmer to somehow positively *assert* that such an equivalence holds at some level!
- In biology (and other disciplines), this issue has led to the emergence  (and, on many facets, the dominance) of an approach that’s an  alternative to phenetics, known as *cladistics*—focusing taxonomical choices on characteristics that are inherited from common  ancestors, rather than ones that are independently evolved.
- For example, sheldgeese (once classified as being closer to other geese) and shelducks (once classified as being closer to other ducks) are now  grouped together within  the subfamily Tadornidae (implying they’re closer to each other than to any other Anatidae, as they share a closer common ancestor)
- What *goose typing* means is: `isinstance(obj, cls)` is now just fine…as long as `cls` is an abstract base class—in other words, `cls`’s metaclass is `abc.ABCMeta`.
- Among the many conceptual advantages of ABCs over concrete classes (e.g., Scott Meyer’s “all non-leaf classes should be abstract”; see Item 33 in his book, More Effective C++, Addison-Wesley), Python’s ABCs add one major practical advantage: the register class method, which lets end-user code “declare” that a certain class becomes a “virtual” subclass of an ABC (for this purpose, the registered class must meet the ABC’s method name and signature requirements, and more importantly, the underlying semantic contract—but it need not have been developed with any awareness of the ABC, and in particular need not inherit from it!).
- Sometimes you don’t even need to register a class for an ABC to recognize it as a  subclass!

````python
class Struggle:
  def __len__(self): return 23

from collections import abc
isinstance(Struggle(), abc.Sized)	# true
````

- `abc.Sized` recorgnizes `Struggle` as a ‘subclass’, with no need for registration, as implemnenting special method `__len__` is all required.

- So, here’s my valediction: whenever you’re implementing a class embodying any of the concepts represented in the ABCs in `numbers`, `collections.abc`, or other framework you may be using, be sure (if needed) to subclass it from, or register it into, the corresponding ABC. At the start of your  programs using some library or framework defining classes which have  omitted to do that, perform the registrations yourself; then, when you  must check for (most typically) an argument being, e.g, “a sequence,”  check whether:

  ```
  isinstance(the_arg, collections.abc.Sequence)
  ```

- And, *don’t* define custom ABCs (or metaclasses) in production code. If you feel the urge to do so, I’d bet it’s likely to be a case  of the “all problems look like a nail”–syndrome for somebody who just  got a shiny new hammer—you (and future maintainers of your code) will be much happier sticking with straightforward and simple code, eschewing such depths. *Valē!*

- To summarize, *goose typing* entails:

  - Subclassing from ABCs to make it explict that you are implementing a previously defined interface.
  - Runtime type checking using ABCs instead of concrete classes as the second argument for `isinstance` and `issubclass`.

- If `isinstance` and `issubclass` is used with concrete classes, type checks limit polymorphism—an essential feature of object-oriented programming.

- However, even with ABCs, you should beware that excessive use of `isinstance` checks may be a *code smell*—a symptom of bad OO design.

- On the other hand, it’s OK to perform an `isinstance` check against an ABC if you must enforce an API contract: “Dude, you have to implement this if you want to call me,” as technical reviewer Lennart Regebro put it. That’s particularly useful in systems that have a plug-in architecture.

### Subclassing an ABC

````python
from collections import namedtuple, abc

Card = namedtuple('Card', ['rank', 'suit'])

class FrenchDeck2(abc.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value):	# for enabling shuffling
        self._cards[position] = value

    def __delitem__(self, position):	# mutable sequence interface forces to implement this.
        del self._cards[position]

    def insert(self, position, value): # its third import abstract method of MutableSequence
        self._cards.insert(position, value)
````

![UML class diagram for `Sequence` and `MutableSequence`](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_1303.png)

### ABCs in the Standard Library

Since Python 2.6, the standard library provides several ABCs. Most are defined in the `collections.abc` module, but there are others. You can find ABCs in the `io` and `numbers` packages, for example. But the most widely used are in `collections.abc`.

![UML for collections.abc](./ch3_13.assets/flpy_1304.png)

### Defining and Using an ABC

This warning appeared in the “Interfaces” chapter of the first edition of *Fluent Python*:

> ABCs, like descriptors and metaclasses, are tools for building frameworks. Therefore, only a small minority of Python developers can create ABCs without imposing unreasonable limitations and needless work on fellow programmers.

To justify creating an ABC, we need to come up with a context for using it as an extension point in a framework. So here is our context:

Imagine you need to display advertisements on a website or a mobile app in random order, but without repeating an ad before the full inventory of ads is shown. Now let’s assume we are building an ad management framework called `ADAM`. One of its requirements is to support **user-provided nonrepeating random-picking classes**.

The ABC will be named `Tombola`, after the Italian name of bingo and the tumbling container that mixes the numbers. It could be used anywhere Bingo Cages, Lottery Blowers machines etc. It will have 4 methods

Abstract Methods

- `.load()` : put items in container
- `.pick()` : remove one item at random from container, return it

Concrete Methods

- `loaded()` : returns True, if there is at least on item in container
- `.inspect()` returns tuple build from items currently in container, without changing its content

````python
import abc

class Tombola(abc.ABC):# subclass ABC

    @abc.abstractmethod
    def load(self, iterable): # abstract method
        """Add items from an iterable."""

    @abc.abstractmethod
    def pick(self): # docstring instructing implementers to raise LookupError
        """Remove item at random, returning it.

        This method should raise `LookupError` when the instance is empty.
        """

    def loaded(self): # abc's may include concrete methods
        """Return `True` if there's at least 1 item, `False` otherwise."""
        return bool(self.inspect())	# we don't how to check if class will implement bool or not, but we know inspect will give us the items

    def inspect(self):
        """Return a sorted tuple with the items currently inside."""
        items = []
        while True:	# we don't know implementation detail of storage scheme but we can repetedily `.pick` to get all items
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items) # put back all items back to the container
        return tuple(items)
````

- Being aware of their internal data structures, concrete subclasses of `Tombola` may always override `.inspect()` with a smarter implementation, but they don’t have to.

### ABC Syntax Details

````python
class MyABC(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def an_abstract_classmethod(cls, ...):
        pass
````

- NOTE: @abstractclassmethod and @abstractstaticmmethod were removed in python 3.3
- The order of stacked function decorators matters

### Subclassing an ABC

````python
import random

from tombola import Tombola


class BingoCage(Tombola): # extends Tombola

    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        self.pick()
````

### A Virtual Subclass of ABC

An essential characteristic of goose typing—and one reason why it deserves a waterfowl name—is the ability to register a class as a *virtual subclass* of an ABC, even if it does not inherit from it. When doing so, we promise that the class faithfully implements the interface defined in the ABC—and Python will believe us without checking. If we lie, we’ll be caught by the usual runtime exceptions.

This is done by calling a `register` class method on the ABC. The registered class then becomes a virtual subclass of the ABC, and will be recognized as such by `issubclass`, but it does not inherit any methods or attributes from the ABC.

````python
from random import randrange

from tombola import Tombola

@Tombola.register # register method in ABC
class TomboList(list): # this class becomes virtual subclass of ABC

    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)  4
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(self)
      
# Tombola.register(TomboList)	# we can register using this syntax also, if we don't maintain the class we want to register
````

- Note that because of the registration, the functions `issubclass` and `isinstance` act as if `TomboList` is a subclass of `Tombola`

- However, inheritance is guided by a special class attribute named `__mro__`—the Method Resolution Order. It basically lists the class and its superclasses in the order Python uses to search for methods. If you inspect the `__mro__` of `TomboList`, you’ll see that it lists only the “real” superclasses—`list` and `object`:
- `Tombola` is not in `Tombolist.__mro__`, so `Tombolist` does not inherit any methods from `Tombola`.

## Structural Typing with ABCs

- ABCs are mostly used with nominal typing. When a class `Sub` explicitly inherits from `AnABC`, or is registered with `AnABC`, the name of `AnABC` is linked to the `Sub` class—and that’s how at runtime, `issubclass(AnABC, Sub)` returns `True`.
- In contrast, structural typing is about looking at the structure of an object’s public interface to determine its type: an object is consistent-with a type if it implements the methods defined in the type. Dynamic and static duck typing are two approaches to structural typing.

````python
class Struggle:
    def __len__(self): return 23

from collections import abc
isinstance(Struggle(), abc.Sized) # True
issubclass(Struggle, abc.Sized) # True
````

- Class `Struggle` is considered a subclass of `abc.Sized` by the `issubclass` function (and, consequently, by `isinstance` as well) because `abc.Sized` implements a special class method named `__subclasshook__`.
- The `__subclasshook__` for `Sized` checks whether the class argument has an attribute named `__len__`. If it does, then it is considered a virtual subclass of `Sized`.

## Static Protocols

### The typed double Function

````python
def double(x):
  return x * 2

double(1.5)	# 3
double('A') # 'AA'
double([10,20,30])	# [10, 20, 30, 10, 20, 30]

from fractions import Fraction
double(Fraction(2, 5)) # Fraction(4,5)
````

- before static protocols were introduced, there was no way to add type hints to `double` without limiting its uses
- thanks to duck typing, `double` works even with types from the future, such as enhanced `Vector` class
- The initial implementation of type hints in Python was a nominal type  system: the name of a type in an annotation had to match the name of the type of the actual arguments—or the name of one of its superclasses.

````python
from typing import TypeVar, Protocol

T = TypeVar('T')

class Reapeatable(Protocol):
  def __mul__(self, T, repeat_count: int) -> T: ... # self is not annotated, assumed to be of type class.
  
RT = TypeVar('RT', bound = Repeatable)->RT:
  
def double(x: RT) -> RT:	# Now type checker can verify x can be multiplied by scalar, return value of same type
  return x * 2
````

### Runtime Checkable Static Protocols

`typing.Protocol` appears in the statick checking area - bottom half of the diagram. However, when defining a `typing.Protocol` subclass, we can use `@runtime_checkable` decorator to make protocol support `isinstance`/`issubclass` checks at runtime. This works because `typing.Protocol` is an ABC, therefore support `__subclasshook__` 

````python
@runtime_checkable
class SupportsComplex(Protocol):
    """An ABC with one abstract method __complex__."""
  	__slots__ = ()
  
  	@abstractmethod
  	def __complex__(self) -> complex:
    		pass
````

- During static type checking, an object will considered consistent-with `SupprotsComplex` protocol if it implements a `__complex__` method that takes only `self` and returns a `complex`
- Thanks to the `@runtime_checkable` class decorator applied to `SupportsComplex`, that protocol can also be used with `isinstance` checks

````python
from typing import SupportsComplex
import numpy as np
c64 = np.complex64(3+4j)
isinstance(c64, complex)	# False
isinstance(c64, SupportsComplex)	# True
c = complex(c64)	# (3+4j)
isinstance(c, SupportsComplex)	# False
complex(c)	# (3+4j)
````

As a result of that last point, if you want to test whether an object `c` is a `complex` or `SupportsComplex`, you can provide a tuple of types as the second argument to  `isinstance`, like this:

````python
isinstance(c, (complex, SupportsComplex))
````

An alternative would be to use the `Complex` ABC, defined in the `numbers` module. The built-in `complex` type and the NumPy `complex64` and `complex128` types are all registered as virtual subclasses of `numbers.Complex`, therefore this works:

````python
import numbers
isinstance(c, numbers.Complex) # True
isinstance(c64, numbers.Complex) # True
````

It was recommended to use the `numbers` ABCs in the first edition of *Fluent Python*, but now that’s no longer good advice, because those ABCs are not recognized by the static type checkers

Very often at runtime, duck typing is the best approach for type checking: instead of calling `isinstance` or `hasattr`, just try the operations you need to do on the object, and handle exceptions as needed. Here is a concrete example.

Example : given an object `o` that I need to use as a complex number, this would be one approach:

````python
# Approach
if isinstance(o, (complex, SupportsComplex)):
    # do something that requires `o` to be convertible to complex
else:
    raise TypeError('o must be convertible to complex')
    
    
# Goose Typing Approach	# use numbers.Complex ABC
if isinstance(o, numbers.Complex):
    # do something with `o`, an instance of `Complex`
else:
    raise TypeError('o must be an instance of Complex')
    
# duck typing, EAFP Principle, Its easier to ask forgiveness than permission
try:
    c = complex(o)
except TypeError as exc:
    raise TypeError('o must be convertible to complex') from exc
````

### Limitations of Runtime Protocol Checks

We’ve seen that type hints are generally ignored at runtime, and this also affects the use of `isinstance` or `issubclass` checks against static protocols.

For example, any class with a `__float__` method is considered—at runtime—a virtual subclass of `SupportsFloat`, even if the `__float__` method does not return a `float`.

### Supporting a Static Protocol

Given that a `complex` number and `Vector2d` instance both consists of a pair of floats, it makes sense to support conversion from `Vector2d` to `complex`

````python
def __complex__(self):
  return complex(self.x, self.y)

@classmethod
def fromcomplex(cls, datum):
	return cls(datum.real, datum.imag)
````

````python
from typing import SupportsComplex, SupportsAbs
from vector2d_v4 import Vector2d

v = Vector2d(3,4)
isinstance(v, SupportsComplex)	# True
isinstance(v, SupportsAbs)	# True
complex(v)	# (3+4j)
abs(v)		# 5
````

### Dynamic a Static Protocol

While studying goose typing, we saw `Tombola` ABC. Here we’ll see how to define a similar interface using a static protocol.

The `Tombola` ABC specifies two methods: `pick` and `load`. We could define a static protocol with these two methods as well, but Go community recommends that single-method protcols make static duck typing more useful and flexible.

The Go standard library has several interface like `Reader`, an interface for I/O that requires just a `read` method. After a while, if you realize a more complete protocol is required, you can combine two or more protcols to define a new one.

````python
from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class RandomPicker(Protocol):
    def pick(self) -> Any: ...
````

````python
import random
from typing import Any, Iterable, TYPE_CHECKING

from randompick import RandomPicker	# its not necessary to import static protocol to define a class implements it

class SimplePicker: # SimplePicker implements RandomPicker but doesn't subclasses, static duck typing in action
    def __init__(self, items: Iterable) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) -> Any:	# Any is default return type
        return self._items.pop()

def test_isinstance() -> None:	# for test cases only, so Mypy knows it
    popper: RandomPicker = SimplePicker([1])
    assert isinstance(popper, RandomPicker)

def test_item_type() -> None:
    items = [1, 2]
    popper = SimplePicker(items)
    item = popper.pick()
    assert item in items
    if TYPE_CHECKING:
        reveal_type(item)
    assert isinstance(item, int)
````

### Best Practices for Protocol Design

- narrow protocols are more useful - often such protocols have single method, rarely more than a couple of methods. [See This](https://martinfowler.com/bliki/RoleInterface.html)
- sometimes protocols are defined near the function that uses it (“client code”) instead of a library, making it easy to create new types to call that function
- Both above practices : narrow protocols and client-code protocols both avoid unecessary tight coupling i.e. Clients should not be forced to depend upon interfaces that they do not use.
- The page Contribution to typeshed recommentds this naming convention for static protocols.
  - Use plain names for protocols that represent a clear concept (e.g., `Iterator`,  `Container`).
  - Use `SupportsX` for protocols that provide callable methods (e.g., `SupportsInt`, `SupportsRead`, `SupportsReadSeek`).
  - Use `HasX` for protocols that have readable and/or writable attributes or getter/setter methods (e.g., `HasItems`, `HasFileno`).
- Another advantage of narrow protocols is that they are easily extendible

### Extending a Protocol

- When practice suggest a protocol with more methods is desired, instead of adding methods to original Protocols, it’s better to derive a new protocol from it.
- In python extending protocols come with caveats

````python
from typing import Protocol, runtime_checkable
from randompick import RandomPicker

@runtime_checkable	# derived Protocol to be runtime checkable
class LoadableRandomPicker(RandomPicker, Protocol):	# Every protocol must explicitly name typing.Protocol as one of its base classes in addition to the protocol we are extending.
    def load(self, Iterable) -> None: ...
````

### The numbers ABCs and Numeric Protocols

- The `numbers` ABCs are fine for runtime type checking, but unsuitale for static typing
- The numeric static protocols `SupportsComplex`, `SupportFloat`, etc. work well for static typing, but are unreliable for runtime type checking when complex numbers are involved.



---

## File: python/ch3_14.md

# Inheritance: For Better of for Worse

- multiple inheritance is supported in C++, Java but not C#. After percieved abuse in early C++ codebases, Java left it out.
- there is significant backlash against overuse of inheritance, multiple inheritance (worse), because superclasses and subclasses are tightly coupled.
- after all this bad name, its(multiple inheritance) still usefull in many practical scenarios, like in standard library, Django, Tkinter GUI toolkit.

## The super() Function

- consistent use of the `super()` built-in function is essential for maintainable object-oriented Python programs.
- when subclass method overrides a method of a superclass, the overriding method usually needs to call the corresponding method of superclass.

````python
class LastUpdatedOrderedDict(OrderedDict):
    """Store items in the order they were last updated"""

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
````

````python
def __init__(self, a, b):
  super().__init__(a,b)
  ... # more init code
````

- there are few examples where overriding method doesn’t use `super()` but instead call method directly as `OrderedDict.__setitem__(self, key, value)`. This is not recommended for reasons
  - hardcoding base class name
  - `super` implements logic to handle class hierarchies with multiple inheritance.

### Subclassing Built-In Types Is Tricky

- earlier versions of python didn’t support subclassing built-ins (most are implemented in C) usually doesn’t call methods overridden by user-defined classes.
- From official documentation:
  - CPython has no rule at all for when exactly overridden method of subclasses of built-in types get implicitly called or not. As an approximation, these methods are never called by other built-in methods of the same object. For example, an overridden `__getitem__()` in a subclass of `dict` will not be called by e.g. the built-in `get()` method.

````python
class DoppelDict(dict):
  def __setitem__(self, key, value):
    super().__setitem__(key, [value] * 2)		# duplicate values when storing

dd = DoppelDict(one = 1)	# constructor ignores __setitem__
dd	# {'one': 1}
dd['two'] = 2	# [] operator works
dd  # {'one': 1, 'two': [2,2]}
dd.update(three = 3)	# update doesn't work expected
dd	# {'three': 3, 'one' : 1, 'two':[2,2]}
````

- The built-in behaviour is a violation of a basic rule of OOP: the search for methods should always start from class of the receiver(`self`), even when the call happens inside a method implemented in a superclass. This is what is called `late binding` which is a key feature of OOP. In any call of form `x.method()` the exact method to be called must be determined at runtime, based on class of receiver `x`.
- The problem is not limited to calls within an instance—whether `self.get()` calls `self.__getitem__()`—but also happens with overridden methods of other classes that should be called by the built-in methods.

````python
class AnswerDict(dict):
  def __getitem__(self, key):	# always return 42
    return 42
  
ad = AnswerDict(a = 'foo')	# loaded with (a='foo')
ad['a']	# 42	# expected
d = {}
d.update(ad)	# update normal dict d, updated with ad
d['a']	# 'foo'	# but our `dict.update` ignored our original AnswerDict method
d			# {'a':'foo'}
````

Subclassing built-in types like `dict` or `list` or `str` directly is error-prone because the built-in methods mostly ignore  user-defined overrides. Instead of subclassing the built-ins, derive  your classes from the [`collections`](https://fpy.li/14-6) module using `UserDict`, `UserList`, and `UserString`, which are designed to be easily  extended.

## Multiple Inheritance and Method Resolution Order

- Any language which implements multiple inheritance has to deal with naming conflicts when superclass implement a method by the same name, commonly known as diamond problem.

![UML for diamond problem](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_1401.png)

Assume following implementation

````python
class Root:
  	def ping(self):
        print(f'{self}.ping() in Root')

    def pong(self):
        print(f'{self}.pong() in Root')

    def __repr__(self):
        cls_name = type(self).__name__
        return f'<instance of {cls_name}>'

class A(Root):
    def ping(self):
        print(f'{self}.ping() in A')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in A')
        super().pong()

class B(Root):
    def ping(self):
        print(f'{self}.ping() in B')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in B')

class Leaf(A, B):
    def ping(self):
        print(f'{self}.ping() in Leaf')
        super().ping()
````

````python
leaf1 = Leaf()
leaf1.ping()

#
#    <instance of Leaf>.ping() in Leaf
#    <instance of Leaf>.ping() in A
#    <instance of Leaf>.ping() in B
#    <instance of Leaf>.ping() in Root

leaf1.pong()

#    <instance of Leaf>.pong() in A
#    <instance of Leaf>.pong() in B
````

Lets take a look at MRO of the class to find references to its superclasses

````python
Leaf.__mro__  # doctest:+NORMALIZE_WHITESPACE
    (<class 'diamond1.Leaf'>, <class 'diamond1.A'>, <class 'diamond1.B'>,
     <class 'diamond1.Root'>, <class 'object'>)
````

- MRO only determines activation order, but when particular method will be activated in each of the classes depend on whether each implementation calls `super()` or not.

- In `pong` method. The `Leaf` doesn’t override it, therefore activated implementation of next class `Leaf.__mro__` : the A class. Since method `A.pong` calls `super().pong()`. The `B` class is next in MRO, therefore `B.pong` is activated but method doesn’t calls `super.pong()` so activation stops.
- NOTE: declaration `Leaf(A,B)` and `Leaf(B, A)` are separate and determine relative order in MRO.
- when a method calls `super()`, it is a cooperative method. Cooperative methods enable *cooperative multiple inheritance*. These terms are intension in order to work, multiple inheritance in Python requires cooperation of the methods involved. In the `B` class, `ping` cooperates but `pong` doesn’t.
- Python is a dynamic language, so the interaction of `super()` with the MRO is also dynamic.

````python
from diamond import A
class U():
  def ping(self):
    print(f'{self}.ping() in U')
    super().ping()
    
class LeafUA(U, A):
  def ping(self):
    print(f'{self}.ping() in LeafUA')
    super().ping()

````

````python
u = U()
u.ping()
# AttributeError: 'super' object has no attribute 'ping'
# because notice U doesn't inherit any class except object, which doesn't implement ping

leaf2 = LeafUA()	# this works as MRO works fine, last Root class doesn't call super ending MRO traversal
````

- Classes like U are called as mixin class. Its a class intended to be used together with other cleasses in multiple inheritance, to provide additional functionality.

## Mixin Classes

A mixin class is designed to be subclassed together with at least one other class in a multiple inheritance arrangement. 

- A mixin is not supposed to be only base class of a concrete class, because it doesn’t provide all the functionality for a concrete class.
- only add/customizes the behaviour of child or sibling class.

### Case-Insesitive Mappings

````python
import collections

def _upper(key):	# helper function
    try:
        return key.upper()
    except AttributeError:
        return key

class UpperCaseMixin: # mixin implement 4 essential methods of mappings, always calling `super()` with the `key` uppercased
    def __setitem__(self, key, item):
        super().__setitem__(_upper(key), item)

    def __getitem__(self, key):
        return super().__getitem__(_upper(key))

    def get(self, key, default=None):
        return super().get(_upper(key), default)

    def __contains__(self, key):
        return super().__contains__(_upper(key))
````

````python
# Concrete Classes using above Mixin
class UpperDict(UpperCaseMixin, collections.UserDict): # UserDict
    pass

class UpperCounter(UpperCaseMixin, collections.Counter): # Counter
    """Specialized 'Counter' that uppercases string keys"""
````

````python
d = UpperDict([('a', 'letter A'), (2, 'digit two')])
list(d.keys()) # ['A', 2]
d['b'] = 'letter B'
'b' in d	# true
list(d.keys())	# ['A', 2, 'B']
````

## Multiple Inheritance in the Real World

- In Design Patterns book, almost all code is in C++, but the only example of multiple inheritance is the Adapter Pattern, In python, multiple inhertance is not the norm either but there are important examples.

### ABCs Are Mixins Too

- documentation of `collection.abc` uses the term *mixin method* for the concrete methods implemented in many of the collection ABCs.
- The ABCs that provide mixin methods play two roles
  - Interface definitions
  - Mixin Classes

### ThreadingMixIn and ForkingMixIn

The `http.server` package provides `HTTPServer` and `ThreadingHTTPServer`. Latter was added in 3.7+, is identical to `HTTPServer` but uses threads to handle requests by using the `ThreadingMixIn`. This is useful to handle web browsers pre-opening sockets, on which `HTTPServer` would wait indefinitely

Complete Source Code for it is

````python
class ThreadingHTTPServer(socketserver.ThreadingMixin, HTTPServer)
	daemon_threads = True
````

### Django Generic Views Mixins

- In Django, a view is a callable object that takes a `request` argument—an object representing an HTTP request—and returns an object representing an HTTP response.

- `View` is the base class of all views (it could be an ABC), and it provides core functionality like the `dispatch` method, which delegates to “handler” methods like `get`, `head`, `post`, etc., implemented by concrete subclasses to handle the different HTTP verbs. The `RedirectView` class inherits only from `View`, and you can see that it implements `get`, `head`, `post`, etc.

### Multiple Inheritance in Tkinter

- Extreme example of multiple inheritance is Python’s standard library, Tkinter GUI Toolkit.
- By current standards, the class hierarchy of Tkinter is very deep. Few parts of the Python standard library have more than three or four levels of concrete classes, and the same can be said of the Java class library. However, it is interesting to note that the some of the deepest hierarchies in the Java class library are precisely in  the packages related to GUI programming:

## Coping with Inheritance

What Alan Kay wrote in the epigraph remains true: there’s still no general theory about inheritance that can guide practicing programmers. What we have are rules of thumb, design patterns, “best practices,” clever acronyms, taboos, etc. Some of these provide useful guidelines, but none of them are universally accepted or always  applicable.

here are a few tips to avoid spaghetti class graphs.

### Favor Object Composition over Class Inheritance

- second principle of object-oriented design from the *Design Patterns* book
- Favoring composition leads to more flexible designs.
- Composition and delegation can replace the use of mixins to make behaviors available to different classes, but cannot replace the use of interface inheritance to define a hierarchy of types.

### Understand Why Inheritance is Used in Each Case

- When dealing with multiple inheritance, it’s useful to keep straight  the reasons why subclassing is done in each particular case. The main reasons are:
  - Inheritance of interface creates a subtype, implying an “is-a” relationship. This is best done with ABCs.
    - **Example**: Consider a scenario where you have a base class `Shape`, and you want to create specific shapes like `Circle` and `Rectangle`. Each shape must implement certain methods like `area()` and `perimeter()`. In this case, `Shape` can be an abstract base class defining these methods, and `Circle` and `Rectangle` can be concrete subclasses implementing these methods.
  - Inheritance of implementation avoids code duplication by reuse. Mixins can help with this.
    - Suppose you have multiple classes (`A`, `B`, `C`) that need logging functionality. Instead of duplicating logging code in each class, you can create a mixin class `LogMixin` that contains the logging functionality. Then, you can inherit from `LogMixin` in each class that needs logging capabilities.

### Make Interface Explicit with ABCs

In modern Python, if a class is intended to define an interface, it should be an explicit ABC or a `typing.Protocol` subclass. An ABC should subclass only `abc.ABC` or other ABCs. Multiple inheritance of ABCs is not problematic.

### Use Explicit Mixins for Code Reuse

If a class is designed to provide method implementations for reuse by multiple unrelated subclasses, without implying an “is-a” relationship, it should be an explicit *mixin class*. Conceptually, a mixin does not define a new type; it merely bundles methods for reuse. A mixin should never be instantiated, and concrete classes should not inherit only from a mixin. Each mixin should provide a single specific behavior, implementing few and very closely related methods. Mixins should avoid keeping any internal state; i.e., a mixin class should not have instance attributes.

- There is no formal way in Python to state that a class is a mixin, so it is highly recommended that they are named with a `Mixin` suffix.

### Provide Aggregate Classes to Users

A class that is constructed primarily by inheriting from mixins and does not add its own structure or behavior is called an *aggregate class*.

If some combination of ABCs or mixins is particularly useful to client code, provide a class that brings them together in a sensible way.

### Subclass Only Classes Designed for Subclassing

Subclassing any complex class and overriding its methods is error-prone because the superclass methods may ignore the subclass overrides in unexpected ways. As much as possible, avoid overriding methods, or at least restrain yourself to subclassing classes which are designed to be easily extended, and only in the ways in which they were designed to be extended.



he PEP introduces a [`@final`](https://fpy.li/14-34) decorator that can be applied to classes or individual methods, so that IDEs or type checkers can report misguided attempts to subclass those classes or override those methods.

### Avoid Subclassing from Concrete Classes

Subclassing concrete classes is more dangerous than subclassing ABCs and mixins, because instances of concrete classes usually have internal state that can easily be corrupted when you override methods that depend on that state. Even if your methods cooperate by calling `super()`, and the internal state is held in private attributes using the `__x` syntax, there are still countless ways a method override can introduce bugs.

### Tkinter: The Good, the Bad, and the Ugly

Most advice in the previous section is not followed by Tkinter, with the notable exception of “Provide Aggregate Classes to Users”.

Keep in mind that Tkinter has been part of the standard library since Python 1.1 was released in 1994. Tkinter is a layer on top of the excellent Tk GUI toolkit of the Tcl language. The Tcl/Tk combo is not originally object-oriented, so the Tk API is basically a vast catalog of functions. However, the toolkit is object-oriented in its design, if not in its original Tcl implementation.

To be fair, as a Tkinter user, you don’t need to know or use multiple  inheritance at all. It’s an implementation detail hidden behind the  widget classes that you will instantiate or subclass in your own code.  But you will suffer the consequences of excessive multiple inheritance  when you type `dir(tkinter.Button)` and try to find the method you need among the 214 attributes listed. And you’ll need to face the complexity if you decide to implement a new Tk widget.


---

## File: python/ch3_15.md

# More About Type Hints

## Overloaded Signatures

- python functions may accept different combination of arguments. The `@typing.overload` decorator allows annotating those different combination.
- this is particularly important when the return type of the function depends on the type of two or more parameters.
- The `sum` built-in is written in C, but *typeshed* has overload type hints for it, in `builtins.py`

````python
@overload
def sum(__iterable: Iterable[_T]) -> Union[_T, int]: ...
@overload
def sum(__iterable: Iterable[_T], start: _S) -> Union[_T, _S]: ...
````

First let’s look at syntax of overload. Thats all the code about the `sum` you will find in the stub file(.pyi). The implementation would be in a different file. The ellipsis(`...`) has no function other than to fulfill the syntactic requirement for a function body, similar to `pass`. So .pyi files are valid Python files.

- As mentioned in “Annotating Positional Only and Variadic Parameters”, the two leading underscores in __iterable are a PEP 484 convention for positional-only arguments that is enforced by Mypy. It means you can call sum(my_list), but not sum(__iterable = my_list).
- The type checker tries to match the given arguments with each overloaded signature, in order. The call `sum(range(100), 1000)` doesn’t match the first overload, because that signature has only one parameter. But it matches the second.

Using `@overload` in the same file

````python
import functools
import operator
from collections.abc import Iterable
from typing import overload, Union, TypeVar

T = TypeVar('T')
S = TypeVar('S') # use in second overload

@overload
def sum(it: Iterable[T]) -> Union[T, int]: ...
@overload
def sum(it: Iterable[T], /, start: S) -> Union[T, S]: ...
def sum(it, /, start=0):
    return functools.reduce(operator.add, it, start)
````

Example files : [Link](https://github.com/python/typeshed/blob/a8834fcd46339e17fc8add82b5803a1ce53d3d60/stdlib/2and3/builtins.pyi)

Aiming for 100% of annotated code may lead to type hints that add lots of noise but little value. Refactoring to simplify type hinting can lead to cumbersome APIs. Sometimes it’s better to be pragmatic and leave a piece of code without type hints.

## TypedDict

Python dictionaries are sometimes used as records, with the keys used as field names and field values of different types.

Example : simple book record

````python
{"isbn": "0134757599",
 "title": "Refactoring, 2e",
 "authors": ["Martin Fowler", "Kent Beck"],
 "pagecount": 478}
````

Before Python 3.8, there was no good way to annotate a record like that, because the mapping types we saw in Generic Mappings limit all values to have the same type.

Here are two lame attempts to annotate a record like the preceding JSON object:

- `Dict[str, Any]` : The values may be of any type
- `Dict[str, Union[str, int, List[str]]]` : hard to read and doesn’t preserve relation between field names and their field types.

````python
from typing import TypedDict

class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int
````

At first glance, `typing.TypedDict` may seem like a data class builder, simialr to `typing.NamedTuple`.

The syntactic similarity is misleading. `TypedDict` is very different. It exists only for benefit of type checker and doesn’t has runtime effect.

`TypedDict` provides two things:

- Class-like syntax to annotate a `dict` with type hints for the value of each “field”
- A constructor that tells the type checker to expect a `dict` with the keys and values as specified.

At runtime a `TypedDict` constructor such as `BookDict` is a placebo: it has same effect as calling the `dict` constructor with same arguments.

- The `fields` in the pseudoclass definition don’t create instance attributes
- you can’t write initializers with default values for the fields
- method definition are not allowed.

Without a type checker, TypedDict is as useful as comments: it may help people read the code, but that’s it. In contrast, the class builders from Chapter 5 are useful even if you don’t use a type checker, because at runtime they generate or enhance a custom class that you can instantiate.

## Type Casting

No type system is perfect, and neither are the static type checkers, the type hints in the *typeshed* project, or the type hints in the third-party packages that have them.

The `typing.cast()` special function provides one way to handle type checking malfunctions or incorrect type hints in code we can’t fix.

Casts are used to silence spurious type checker warnings and give the  type checker a little help when it can’t quite understand what is going  on.

````python
def cast(typ, val):
    """Cast a value to a type.
    This returns the value unchanged.  To the type checker this
    signals that the return value has the designated type, but at
    runtime we intentionally don't check anything (we want this
    to be as fast as possible).
    """
    return val
````



## Reading Type Hints at Runtime

## Implementing a Generic Class

We implemented Tombola ABC. The LottoBlower class was concrete implementation of it. Let’s study generic version of it.

````python
from generic_lotto import LottoBlower

machine = LottoBlower[int](range(1, 11)) # instantiate generic class

first = machine.pick()	# mypy will correctly infer that `first` is and int
remain = machine.inspect() # and that remain is a tuple of integers
````



## Variance

## Implementing a Generic Static Protocol

---

## File: python/ch3_16.md

# Operator Overloading

Operator overloading is necessary to support infix operator notation with user-defined or extension types, such as NumPy arrays. Having operator overloading in a high-level, easy-to-use language was probably a key reason for the huge success of Python in data science, including financial and scientific applications.

## Operator Overloading 101

- allows user-defined objects to interoperate with infix operator like `+` and `|` or unary operators like `-` and `~`. More generally function invocation (`()`), attribute access (`.`), and items-access/slicing `[]` are also operators in python.
- This chapter deals with unary and infix operators
- Python strikes a good balance among flexibility, usability, and safety by imposing some limitations:
  - We cannot change the meaning of the operators for the built-in types.
  - We cannot create new operators, only overload existing ones.
  - A few operators can’t be overloaded: `is`, `and`, `or`, `not` (but the bitwise `&`, `|`, `~`, can).

## Unary Operators

- `-`, implemented by `__neg__`
- `+`, implemented by `__add__`
- `~`, implemented by `__invert__`

The “Data Model” chapter of The Python Language Reference also lists the `abs()` built-in function as a unary operator. The associated special method is `__abs__`, as we’ve seen before.

- its simple to support Unary Operators just implement the supporting function
- Follow only one rule, always return a new objects of suitable types, don’t modify the receiver `self`.

For `+`/`-` usually returned object would be of same type but for `~` its depends on context. `abs` will return scalar always.

````python
    def __abs__(self):
        return math.hypot(*self)

    def __neg__(self):
        return Vector(-x for x in self)

    def __pos__(self):
        return Vector(self)
````

Everybody expects that `x == +x`, and that is true almost all the time in Python, but there are two cases in the standard library where `x != +x`.

The first case involves the `decimal.Decimal` class. You can have `x != +x` if `x` is a `Decimal` instance created in an arithmetic context and `+x` is then evaluated in a context with different settings.

You can find the second case where x != +x in the `collections.Counter` documentation. The `Counter` class implements several arithmetic operators, including infix `+` to add the tallies from two `Counter` instances.

However, for practical reasons, `Counter` addition discards from the result any item with a negative or zero count. And the prefix `+` is a shortcut for adding an empty `Counter`, therefore it produces a new `Counter`, preserving only the tallies that are greater than zero.

````python
ct = Counter('abracadabra')
ct # Counter({'a': 5, 'r': 2, 'b': 2, 'd': 1, 'c': 1})
ct['r'] = -3
ct['d'] = 0
ct # Counter({'a': 5, 'b': 2, 'c': 1, 'd': 0, 'r': -3})
+ct # Counter({'a': 5, 'b': 2, 'c': 1})
````

## Overloading + for Vector Addition

Adding two Euclidean vectors results in a new vector in which the components are the pairwise additions of the components of the operands.

What happens if we try to add two `Vector` instances of  different lengths? We could raise an error, but considering practical  applications (such as information retrieval), it’s better to fill out  the shortest `Vector` with zeros.

````python
    # inside the Vector class

    def __add__(self, other):
        pairs = itertools.zip_longest(self, other, fillvalue=0.0) # generator that produces tuples (a, b) where a is from self, and b. If self and other has different lenghts, fillvalue supplies the missing values for the shortes iterable.
        return Vector(a + b for a, b in pairs)	# built from a generator expression, producing one addition for each (a,b) from pairs
````

````python
v1 = Vector([3, 4, 5])
v1 + (10, 20, 30)	# works because zip_longest consumes any iterable
(10,20, 30) + v1	# fails because tuple doesn't implement our __add__ implementation
````

Python implements a special dispatching mechanism for the infix operator special methods. Given an expression `a + b`, the interpreter will perform these steps

- If `a` has `__add__`, call `a.__add__(b)` and return result unless it’s `NotImplemented`.
- If `a` doesn’t have `__add__`, or calling it returns `NotImplemented`, check if `b` has `__radd__`, then call `b.__radd__(a)` and return result unless it’s `NotImplemented`.
- If `b` doesn’t have `__radd__`, or calling it returns `NotImplemented`, raise `TypeError` with an *unsupported operand types* message.

> Do not confuse `NotImplemented` with `NotImplementedError`. The first, `NotImplemented`, is a special singleton value that an infix operator special method should `return` to tell the interpreter it cannot handle a given operand. In contrast, `NotImplementedError` is an exception that stub methods in abstract classes may `raise` to warn that subclasses must implement them.

````python
    # inside the Vector class

    def __add__(self, other):
        pairs = itertools.zip_longest(self, other, fillvalue=0.0)
        return Vector(a + b for a, b in pairs)

    def __radd__(self, other): # more simple implementation
        return self + other
````

Often, `__radd__` can be as simple as that: just invoke the proper operator, therefore delegating to `__add__` in this case. This applies to any commutative operator; `+` is commutative when dealing with numbers or our vectors, but it’s not commutative when concatenating sequences in Python.

````python
    def __add__(self, other):
        pairs = itertools.zip_longest(self, other, fillvalue=0.0)
        return Vector(a + b for a, b in pairs)

    __radd__ = __add__
````

if an operator special method cannot return a valid result because of type incompatibility, it should return `NotImplemented` and not raise `TypeError`. By returning `NotImplemented`, you leave the door open for the implementer of the other operand type  to perform the operation when Python tries the reversed method call.

In the spirit of duck typing, we will refrain from testing the type of the `other` operand, or the type of its elements. We’ll catch the exceptions and return `NotImplemented`. If the interpreter has not yet reversed the operands, it will try that. If the reverse method call returns `NotImplemented`, then Python will raise `TypeError` with a standard error message like “unsupported operand type(s) for +: *Vector* and *str*.”

````python
    def __add__(self, other):
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        return self + other
````

## Overloading * for Scalar Multiplication

What does `Vector([1, 2, 3]) * x` mean? If `x` is a number, that would be a scalar product, and the result would be a new `Vector` with each component multiplied by `x`—also known as an elementwise multiplication:

Back to our scalar product, again we start with the simplest `__mul__` and `__rmul__` methods that could possibly work:

````python
    # inside the Vector class

    def __mul__(self, scalar):
        return Vector(n * scalar for n in self)

    def __rmul__(self, scalar):
        return self * scalar
````

Those methods do work, except when provided with incompatible operands. The `scalar` argument has to be a number that when multiplied by a `float` produces another `float` (because our `Vector` class uses an `array` of floats internally). So a `complex` number will not do, but the scalar can be an `int`, a `bool` (because `bool` is a subclass of `int`), or even a `fractions.Fraction` instance.

````python
class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    # many methods omitted in book listing, see vector_v7.py
    # in https://github.com/fluentpython/example-code-2e

    def __mul__(self, scalar):
        try:
            factor = float(scalar)
        except TypeError: # scalar can't be converted to float
            return NotImplemented
        return Vector(n * factor for n in self)

    def __rmul__(self, scalar):
        return self * scalar
````

## Using @ as an Infix Operator

The `@` sign is well-known as the prefix of function decorators, but since 2015, it can also be used as an infix operator. For years, the dot product was written as `numpy.dot(a, b)` in NumPy.(3.5+)

Today, you can write `a @ b` to compute the dot product of two NumPy arrays.

The `@` operator is supported by the special methods `__matmul__`, `__rmatmul__`, and `__imatmul__`, named for “matrix multiplication.” These methods are not used anywhere in the standard library at this time, but are recognized by the interpreter since Python 3.5, so the NumPy team—and the rest of us—can support the `@` operator in user-defined types. The parser was also changed to handle the new operator (`a @ b` was a syntax error in Python 3.4).

````python
class Vector:
    # many methods omitted in book listing

    def __matmul__(self, other):
        if (isinstance(other, abc.Sized) and # both should implement __len__ & __iter__
            isinstance(other, abc.Iterable)):
            if len(self) == len(other): # have same length to allow
                return sum(a * b for a, b in zip(self, other)) # using zip and sum operations
            else:
                raise ValueError('@ requires vectors of equal length.')
        else:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other
````

The `zip` built-in accepts a `strict` keyword-only optional argument since Python 3.10. When `strict=True`, the function raises `ValueError` when the iterables have different lengths. The default is `False`. This new strict behavior is in line with Python’s [*fail fast*](https://fpy.li/16-8) philosophy.

## Wrapping-Up Arithmetic Operators

| Operator | Forward      | Reverse     | In-place    | Description                     |
|----------|--------------|-------------|-------------|---------------------------------|
| +        | `__add__`    | `__radd__`  | `__iadd__`  | Addition or concatenation       |
| -        | `__sub__`    | `__rsub__`  | `__isub__`  | Subtraction                     |
| *        | `__mul__`    | `__rmul__`  | `__imul__`  | Multiplication or repetition   |
| /        | `__truediv__`| `__rtruediv__` | `__itruediv__` | True division            |
| //       | `__floordiv__` | `__rfloordiv__` | `__ifloordiv__` | Floor division  |
| %        | `__mod__`    | `__rmod__`  | `__imod__`  | Modulo                          |
| divmod()| `__divmod__` | `__rdivmod__` | `__idivmod__` | Returns tuple of floor division quotient and modulo |
| **, pow()| `__pow__`   | `__rpow__`  | `__ipow__`  | Exponentiation                    |
| @        | `__matmul__`| `__rmatmul__` | `__imatmul__` | Matrix multiplication     |
| &        | `__and__`    | `__rand__`  | `__iand__`  | Bitwise and                      |
| \|       | `__or__`     | `__ror__`   | `__ior__`   | Bitwise or                       |
| ^        | `__xor__`    | `__rxor__`  | `__ixor__`  | Bitwise xor                      |
| <<       | `__lshift__` | `__rlshift__` | `__ilshift__` | Bitwise shift left      |
| >>       | `__rshift__` | `__rrshift__` | `__irshift__` | Bitwise shift right     |

## Rich Comparison Operators

| Group     | Infix operator | Forward method call | Reverse method call | Fallback             |
|-----------|----------------|---------------------|---------------------|----------------------|
| Equality  | `a == b`       | `a.__eq__(b)`       | `b.__eq__(a)`       | `Return id(a) == id(b)` |
|           | `a != b`       | `a.__ne__(b)`       | `b.__ne__(a)`       | `Return not (a == b)`  |
| Ordering  | `a > b`        | `a.__gt__(b)`       | `b.__lt__(a)`       | `Raise TypeError`      |
|           | `a < b`        | `a.__lt__(b)`       | `b.__gt__(a)`       | `Raise TypeError`      |
|           | `a >= b`       | `a.__ge__(b)`       | `b.__le__(a)`       | `Raise TypeError`      |
|           | `a <= b`       | `a.__le__(b)`       | `b.__ge__(a)`       | `Raise TypeError`      |

````python
class Vector:
    # many lines omitted

    def __eq__(self, other):
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))
````

*In the face of ambiguity, refuse the temptation to guess.*

````python
    def __eq__(self, other):
        if isinstance(other, Vector):
            return (len(self) == len(other) and
                    all(a == b for a, b in zip(self, other)))
        else:
            return NotImplemented
````

## Augmented Assignment Operators

Our `Vector` class already supports the augmented assignment operators `+=` and `*=`. That’s because augmented assignment works with immutable receivers by  creating new instances and rebinding the lefthand variable.

the augmented assignment operators work as syntactic sugar: `a += b` is evaluated exactly as `a = a + b`. That’s the expected behavior for immutable types, and if you have `__add__`, then `+=` will work with no additional code.

However, if you do implement an in-place operator method such as `__iadd__`, that method is called to compute the result of `a += b`. As the name says, those operators are expected to change the lefthand  operand in place, and not create a new object as the result.

We can summarize the whole idea of in-place operators by contrasting the return statements that produce results in __add__ and __iadd__ in Example 16-19:

- `__add__` : The result is produced by calling the constructor AddableBingoCage to build a new instance.
- `__iadd__` : The result is produced by returning self, after it has been modified.

---

## File: python/ch4_17.md

# Iterators, Generators, and Classic Coroutines

## A Sequence of Words

- we implement `Sentence` class in `Sequence` Protocol thats why its iterable

````python
import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
  
  def __init__(self, text):
    self.text = text
    self.words = RE_WORD.findall(text)
  
  def __getitem__(self, index):
    return self.words[index]
  
  def __len__(self):
    return len(self.words)
  
  def __repr__(self):
    return "Sequence(%s)" % reprlib.repr(self.text)
````

## Why Sequence Are Iterable: The `iter` Function

whenever python needs to iterate over an object `x` it calls `iter(x)`

- Calls `__iter__` on the object `x`
- if `__iter__` is not implemented but `__get__` is, then `iter()` creates an iterator that tries to fetch items by index, from `0`
- if above all fails python raises `TypeError`, saying `C Object is not iterable`, where `C` is a class or target object.

all python sequences are iterable by definition since they all implement `__getitem__`. This is an extreme form of duck typing. An object is considered iterable not only when it implements the special method `__iter__`, but also when it implements `__getitem__`

NOTE : classes which implement `__getitem__`, works fine when passed to `iter(x)` and return iterator, but when checked with `collections.abc.Iterable` for `isInstance` check they fail.

In goose-typing approach, the definition for an iterable is simpler but not as flexible : an object is considered iterable if it implements the `__iter__` method. No subclassing or registration is required because `abc.Iterable` implements `__subclasshook__` so your class will pass `issubclass` and `isinstance` checks on `abc.Iterable`

### Using iter with Callable

````python
iter_obj = iter(func, sentinel)
````

NOTE: Here `func` should be a callable, sentinel raises `StopIteration` instead of yielding the sentinel

````python
def d6():
  return randint(1, 6)

d6_iter = iter(d6, 1)
for roll in d6_iter:
  print(roll)	 # prints till 1 hits and exits # note doesn't print 1
````

## Iterables v/s Iterators

- Iterable : Any object from which the `iter` built-in obtains iterator. Objects implementing an `__iter__` method returning an iterator are iterable.
- Python obtains iterator from Iterables

````python
s = "ABC"
for c in s:
  print(c)
````

- In above example `str` `ABC` is iterable, but there is a iterator behind the scene we use the same in `for` loop.

Python’s standard interface for an iterator has two methods

- `__next__` : Returns the next item in series, raising `StopIteration` if there are no more.
- `__iter__` : Returns `self`; this allows iterators to be used where an iterable is expected

````python
# Lib/types.py module source code in python3.9

# Iterators in Python aren't a matter of type but of protocol.  A large
# and changing number of builtin types implement *some* flavor of
# iterator.  Don't check the type!  Use hasattr to check for both
# "__iter__" and "__next__" attributes instead.
````

- the best way to check if an object `x` is an iterator is to call `isinstance(x, abc.Iterator)`. Thanks to `Iterator.__subclasshook__`, this test works even if the class of `x` is not a real or virtual subclass of `Iterator`.

## Sentence Classes with `__iter__`

### Sentence Take#2 : A Classic Iterator

````python
# implementation follows the blueprint of the classic Iterator design pattern from the Design Patterns book.

import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self): # isinstance check passes now
        return SentenceIterator(self.words) # returns iterator


class SentenceIterator:

    def __init__(self, words):
        self.words = words # hold reference to word
        self.index = 0 # starting index

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self
````

### Don’t Make the Iterable an Iterator for Itself

- Iterables have an `__iter__` method that instantiates a new iterator every time.
- Iterator implement a `__next` method that returns individual items, and an `__iter__` method that returns self.
- Therefore iterators are also iterable, but iterables are not interators
- NOTE: defining `__next__` in addition to `__iter__` in the Sentence class, makes each Sentence instance at the same time an iterable and iterators over itself. But its a common anti-pattern. An Iterator pattern is supposed to support multiple traversals of aggregate objects. that is why each iterator should maintain its internal state.

### Sentence Take#3 : A Generator Function

````python
import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        for word in self.words:
            yield word # yield current word
		# explicit return in not required
````

### How a generator Works

Any python function with `yield` keyword in its body is a generator function. So it returns generator object.

A generator function builds a generator object that wraps the body of the function. When we invoke `next()` on the generator object, execution advances to the next `yield` in the function body, and the `next()` call evaluates to the value yielded when the function body is suspended. Finally, the enclosing generator object created by Python raises `StopIteration` when the function body returns, in accordance with the `Iterator` protocol.

## Lazy Sentence

### Sentence Take #4 : Lazy Generator

The `Iterator` interface is designed to be lazy : `next(my_iterator)` yields one item at a time.

Our Implementation till now is not lazy because the `__init__` eagerly builds a list of all words in the text, binding it to the `self.words` attribute. This could take as much space as list.

Using an generator function that does regex matching

````python
import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:

    def __init__(self, text):
        self.text = text # no need to have words array

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        for match in RE_WORD.finditer(self.text): # builds iter over mathces of RE_WORD
            yield match.group() # extract matched text from the MatchObject instance
````

### Sentence Take#5 : Lazy Generator Expression

As a list comprehension builds lists, a generator expression builds generator objects.

````python
def gen_AB():
  print('start')
  yield 'A'
  print('continue')
  yield 'B'
  print('end.')
  
res1 = [x*3 for x in gen_AB()]	# list comprehension immideatily evaluates
# start
# continue
# end
for i in res1:
  print('-->', i)
# ---> AAA
# ---> BBB

res2 = (x*3 for x in gen_AB())	# its not consumed instead gets evaluated as called
res2	# generator object <genexp> at 0x...
for i in res2:
  print('-->', i)

start
---> AAA
continue
---> BBB
end.
````

````python
import re
import reprlib
RE_WORD = re.compile(r'\w+')
class Sentence:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))	# generator expression
````

## When to Use Generator Expressions

- generator expressions are just syntactic sugar on top generator functions
- generator expression are short hand and don’t require calling function while gnerator functions are more flexible allowing coding up complex logic.

When a generator expression is passed as the single argument to a function or constructor, you don’t need to write a set of parentheses for the function call and another to enclose the generator expression. A single pair will do, like in the Vector call from the `__mul__` method, reproduced here:

````python
def __mul__(self, scalar):
    if isinstance(scalar, numbers.Real):
        return Vector(n * scalar for n in self)
    else:
        return NotImplemented
````

- However if there are more args, you need to enclose it in parenthesis to avoid a `SyntaxError`

## An Arithmetic Progression Generator

`range` built-in generates a bounded arithmetic progression of integers.

````python
class ArithmeticProgression:

    def __init__(self, begin, step, end=None): 
        self.begin = begin
        self.step = step
        self.end = end  # None -> "infinite" series

    def __iter__(self):
        result_type = type(self.begin + self.step) # get type of their sum
        result = result_type(self.begin) # final type
        forever = self.end is None # infinity check
        index = 0
        while forever or result < self.end: # termination
            yield result
            index += 1
            result = self.begin + self.step * index
````

````python
# same thing using generator function
def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index
````

### Arithmetic Progression using itertools

- `itertools` has over 20 generator function that can be combine to make interesting functions
- Example : `itertools.count` which return a number yielding generator.
- NOTE: above function is unbound when no args are passed. Optinally you should pass `(start, step)`. don’t try to cast it in list `list(itertools.count())` : this will overflow memory.

````python
import itertools

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is None:
        return ap_gen
    return itertools.takewhile(lambda n: n < end, ap_gen)	# notice we return a generator
````

## Generator Functions in the Standard Library

| Module     | Function           | Description                                                                                                                                                            |
|------------|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| itertools  | compress           | Consumes two iterables in parallel; yields items from `it` whenever the corresponding item in `selector_it` is truthy                                                |
| itertools  | dropwhile          | Consumes `it`, skipping items while `predicate` computes truthy, then yields every remaining item (no further checks are made)                                       |
| built-in   | filter             | Applies `predicate` to each item of iterable, yielding the item if `predicate(item)` is truthy; if `predicate` is None, only truthy items are yielded                  |
| itertools  | filterfalse        | Same as `filter`, with the predicate logic negated: yields items whenever `predicate` computes falsy                                                                   |
| itertools  | islice             | Yields items from a slice of `it`, similar to `s[:stop]` or `s[start:stop:step]` except `it` can be any iterable, and the operation is lazy                          |
| itertools  | takewhile          | Yields items while `predicate` computes truthy, then stops and no further checks are made                                                                              |

````python
def vowel(c):
	return c.lower() in 'aeiou'

list(filter(vowel, 'Aardvark'))
# ['A', 'a', 'a']
list(itertools.filterfalse(vowel, 'Aardvark'))
# ['r', 'd', 'v', 'r', 'k']
list(itertools.dropwhile(vowel, 'Aardvardk')
# ['r', 'd', 'v', 'a', 'r', 'k']
list(itertools.takewhile(vowel, 'Aardvark'))
# ['A', 'a']
list(itertools.compress('Aardvark', (1, 0, 1, 1, 0, 1)))
# ['A', 'r', 'd', 'a']
list(itertools.islice('Aardvark', 4))
# ['A', 'a', 'r', 'd']
````

Here's the information converted into a markdown table with the source included:

| Module    | Function                      | Description                                                  | Source     |
| --------- | ----------------------------- | ------------------------------------------------------------ | ---------- |
| itertools | accumulate(it, [func])        | Yields accumulated sums; if func is provided, yields the result of applying it to the first pair of items, then to the first result and next item, etc. | (built-in) |
| built-in  | enumerate(iterable, start=0)  | Yields 2-tuples of the form (index, item), where index is counted from start, and item is taken from the iterable | (built-in) |
| built-in  | map(func, it1, [it2, …, itN]) | Applies func to each item of it, yielding the result; if N iterables are given, func must take N arguments and the iterables will be consumed in parallel | (built-in) |
| itertools | starmap(func, it)             | Applies func to each item of it, yielding the result; the input iterable should yield iterable items iit, and func is applied as func(\*iit) | itertools  |

````python
sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]

import itertools

result1 = list(itertools.accumulate(sample))
# Output: [5, 9, 11, 19, 26, 32, 35, 35, 44, 45]

result2 = list(itertools.accumulate(sample, min))
# Output: [5, 4, 2, 2, 2, 2, 2, 0, 0, 0]

result3 = list(itertools.accumulate(sample, max))
# Output: [5, 5, 5, 8, 8, 8, 8, 8, 9, 9]

import operator

result4 = list(itertools.accumulate(sample, operator.mul))
# Output: [5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]

result5 = list(itertools.accumulate(range(1, 11), operator.mul))
# Output: [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
````

````python
# Example 1
result1 = list(enumerate('albatroz', 1))
# Output: [(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]

import operator

result2 = list(map(operator.mul, range(11), range(11)))
# Output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

result3 = list(map(operator.mul, range(11), [2, 4, 8]))
# Output: [0, 4, 16]

result4 = list(map(lambda a, b: (a, b), range(11), [2, 4, 8]))
# Output: [(0, 2), (1, 4), (2, 8)]

import itertools

result5 = list(itertools.starmap(operator.mul, enumerate('albatroz', 1)))
# Output: ['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']

sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]

result6 = list(itertools.starmap(lambda a, b: b / a, enumerate(itertools.accumulate(sample), 1)))
# Output: [5.0, 4.5, 3.6666666666666665, 4.75, 5.2, 5.333333333333333, 5.0, 4.375, 4.888888888888889, 4.5]
````

| Module | Function | Description |
|--------|----------|-------------|
| itertools | chain(it1, …, itN) | Yields all items from it1, then from it2, etc., seamlessly |
| itertools | chain.from_iterable(it) | Yields all items from each iterable produced by it, one after the other, seamlessly; it will be an iterable where the items are also iterables, for example, a list of tuples |
| itertools | product(it1, …, itN, repeat=1) | Cartesian product: yields N-tuples made by combining items from each input iterable, like nested for loops could produce; repeat allows the input iterables to be consumed more than once |
| built-in | zip(it1, …, itN, strict=False) | Yields N-tuples built from items taken from the iterables in parallel, silently stopping when the first iterable is exhausted, unless strict=True is given |
| itertools | zip_longest(it1, …, itN, fillvalue=None) | Yields N-tuples built from items taken from the iterables in parallel, stopping only when the last iterable is exhausted, filling the blanks with the fillvalue |

| Module | Function | Description |
|--------|----------|-------------|
| itertools | combinations(it, out_len) | Yields combinations of out_len items from the items yielded by it |
| itertools | combinations_with_replacement(it, out_len) | Yields combinations of out_len items from the items yielded by it, including combinations with repeated items |
| itertools | count(start=0, step=1) | Yields numbers starting at start, incremented by step, indefinitely |
| itertools | cycle(it) | Yields items from it, storing a copy of each, then yields the entire sequence repeatedly, indefinitely |
| itertools | pairwise(it) | Yields successive overlapping pairs taken from the input iterable |
| itertools | permutations(it, out_len=None) | Yields permutations of out_len items from the items yielded by it; by default, out_len is len(list(it)) |
| itertools | repeat(item, [times]) | Yields the given item repeatedly, indefinitely unless a number o

| Module | Function | Description |
|--------|----------|-------------|
| itertools | groupby(it, key=None) | Yields 2-tuples of the form (key, group), where key is the grouping criterion and group is a generator yielding the items in the group |
| built-in | reversed(seq) | Yields items from seq in reverse order, from last to first; seq must be a sequence or implement the __reversed__ special method |
| itertools | tee(it, n=2) | Yields a tuple of n generators, each yielding the items of the input iterable independently |

### Iterable Reducing Function

| Module | Function | Description |
|--------|----------|-------------|
| built-in | all(it) | Returns True if all items in it are truthy, otherwise False; all([]) returns True |
| built-in | any(it) | Returns True if any item in it is truthy, otherwise False; any([]) returns False |
| built-in | max(it, [key=,] [default=]) | Returns the maximum value of the items in it; a key is an ordering function, as in sorted; default is returned if the iterable is empty |
| built-in | min(it, [key=,] [default=]) | Returns the minimum value of the items in it; a key is an ordering function, as in sorted; default is returned if the iterable is empty |
| functools | reduce(func, it, [initial]) | Returns the result of applying func to the first pair of items, then to that result and the third item, and so on; if given, initial forms the initial pair with the first item |
| built-in | sum(it, start=0) | The sum of all items in it, with the optional start value added (use math.fsum for better precision when adding floats) |

## Subgenerators with yield from

- Before `yield from` keyword was introduced, subgenerators were declared as

````python
def sub_gen():
  yield 1.1
  yield 1.2
  
def gen():
  yield 1
  for i in sub_gen():
    yield i
  yield 2
````

- Now after python3.3

````python
def gen():
  yield 1
  yield from sub_gen()
  yield 2
````

NOTE: 

````python
def sub_gen():
  yield 1.1
  yield 1.2
  return "DONE"
  
def gen():
  yield 1
  result = yield from sub_gen()	# gen delegates yielding to sub_gen, and it yields till its finished.
  print("<--", result)
  yield 2
  
for x in gen():
  print(x)
# Output :
1
1.1
1.2
<-- Done!
2
````

### Reinventing Chain

````python
def chain(*iterables):
	for it in iterables:
    for i in it:
      yield i
````

### Traversing a Tree (Printing python’s Exception Hierarchy)

````python
def tree(cls, lvl = 0):
    yield cls.__name__, lvl  # yield class and its level
    for sub_cls in cls.__subclasses__(): # for each subclass yield subclass and its level
        yield from tree(sub_cls, lvl + 1)

def display(cls):
    for cls_name, level in tree(cls):
        indent = ' ' * 4 * level  # some indentation
        print(f'{indent}{cls_name}')

if __name__ == '__main__':
    display(BaseException)
````

## Generic Iterable Types

- we can annotate functions which accept iterable arguments using `collection.abc.Iterable`  or `typing.Iterable`

````python
from collections.abc import Iterable

FromTo = tuple[str, str]

def zip_replace(text: str, changes: Iterable[FromTo])-> str:
  for from_, to in changes:
    text = text.replace(from_, to)
	return text
````

````python
from collections.abc import Iterator

def fib() -> Iterator[int]	# return type for generators coded as functions with yield
	a, b = 0, 1
  while True:
    yield a
    a, b = b, a+b
````

- Note for generators there is a `collections.abc.Generator` type.
- `Iterator[T]` is a shortcut for `Generator[T, None, None]` : a generator with no args and no return value.

## Classic Coroutines

- generators are commonly used as iterators, but they are also used for coroutines

- A coroutine is really a generator function, created with `yield` keyword in its body. And a coroutines object is physically a generator object.

- The typing documentation describes the formal type parameters of Generator like this:

  `Generator[YieldType, SendType, ReturnType]`

  The `SendType` is only relevent in case of using it as a coroutine, return type is only relevant for coroutine, because iterators don’t return values like regular function.

- Generator type has the same tyupe parameters as `typing.Coroutine` : `Coroutine[YieldType, SendType, ReturnType]`

David Beazley created some of the best talks and most comprehensive workshops about classic coroutines. In his [PyCon 2009 course handout](https://fpy.li/17-18), he has a slide titled “Keeping It Straight,” which reads:

- Generators produce data for iteration
- Coroutines are consumers of data
- To keep your brain from exploding, don’t mix the two concepts together
- Coroutines are not related to iteration
- Note: There is a use of having `yield` produce a value in a coroutine, but it’s not tied to iteration.

### Coroutine to Compute a Running Average

````python
from collections.abc import Generator

def averager() -> Generator[float, float, None]: # return type is none, args is float
    total = 0.0
    count = 0
    average = 0.0
    while True: # infinite
        term = yield average # yield average
        total += term
        count += 1
        average = total/count
        
coro_avg = averager()
next(coro_avg)	# 0.0	# initial value of average 0
coro_avg.send(10) # 10	# each call to send yield avg
coro_avg.send(30) # 20
coro_avg.send(5) # 15
````

### Returning a Value from a coroutine

````python
from collections.abc import Generator
from typing import Union, NamedTuple

class Result(NamedTuple): # subclass of tupe
    count: int  # type: ignore
    average: float

class Sentinel:
    def __repr__(self): # readable
        return f'<Sentinel>'

STOP = Sentinel()

SendType = Union[float, Sentinel]	# SendType: TypeAlias = float | Sentinel

def averager2(verbose: bool = False) -> Generator[None, SendType, Result]: # yield type is none, it recieved data and returns the result
    total = 0.0
    count = 0
    average = 0.0
    while True:
        term = yield # this yields None, but recieves from send(item)
        if verbose:
            print('received:', term)
        if isinstance(term, Sentinel): # term is a sentinel break from the loop
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)

  
  
coro_avg = averager2()
next(coro_avg)
coro_avg.send(10) # no results
coro_avg.send(30)
coro_avg.send(6.5)
coro_avg.close() # close stops but doesn't return result


coro_avg = averager2()
next(coro_avg)
coro_avg.send(10)
coro_avg.send(30)
coro_avg.send(6.5)
try:
    coro_avg.send(STOP)  # makes sentinel break
except StopIteration as exc:
    result = exc.value # notice value attached to exc

result
Result(count=3, average=15.5)
````

### Generic Type Hints for Classic Coroutines

````python
# typing.py definition of generator
T_co = TypeVar('T_co', covariant=True)
V_co = TypeVar('V_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

# many lines omitted

class Generator(Iterator[T_co], Generic[T_co, T_contra, V_co],
                extra=_G_base):
````

That generic type declaration means that a `Generator` type hint requires those three type parameters we’ve seen before:

```
my_coro : Generator[YieldType, SendType, ReturnType]
```

Using the notation introduced in “Covariant types”, the covariance of the first and third parameters is expressed by the :> symbols pointing in the same direction:

                       float :> int
    Generator[float, Any, float] :> Generator[int, Any, int]
    # --------------------------------------------------------
                         float :> int
    Generator[Any, float, Any] <: Generator[Any, int, Any]

Variance rules of thumb

1. If a formal type parameter defines a type for data that comes out of the object, it can be covariant.
2. If a formal type parameter defines a type for data that goes into the object after its initial construction, it can be contravariant.

---

## File: python/ch4_18.md

# With, match and else Block

- The `with` statement sets up a temporary context and reliably tears it down, under the control of a context manager object.

## Context Managers and with Blocks

- Conext Manager objects exist to control a `with` statement, just like iterators exist to control a `for` statement.
- `with` statement simplifies common use cases of `try/finally`, which guarantees taht some operation is performed after a block of code, even if the block is terminated by `return`, and exception or a `sys.exit()` call. The code in `finally` cause usually releases a critical resource or restores some previous state that was temporarily changed.
- Other application
  - Managing transactions in the `sqlite3` module
  - Safely handling locks, conditions, and semaphores
  - Setting up custom environments for arithmetic operations in `Decimal` objects
  - Patching object for testing
- Context manger interface consists of the `__enter__`(usually returns `self`) and `__exit__` methods.

````python
with open('mirror.py') as fp:
  src = fp.read(60)

len(src)	# 60
````

- Here `open()` function returns an instance of `TextIOWrapper`, and its `__enter__` method returns `self`.
- NOTE: when control exits the `with` block in any way, the `__exit__` method is invoked on the context manager object not on the whatever returned by `__enter__`
- NOTE: `as` clause of the `with` is optional. In case of `open` we get reference to file, many context manager will return `None` which is not useful.

````python
from mirror import LookingGlass
with LookingGlass() as what:	# context manager is an instance of LookingGlass
  print("Alice, Kitty and Snowdrop")	# this print is rigged to print reverse
  print(what)
````

````python
import sys

class LookingGlass:

    def __enter__(self): # no args
        self.original_write = sys.stdout.write # monkey_patch
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY' # return assigned to variable that uses as

    def reverse_write(self, text): # reverse function
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback): # tear down call
        sys.stdout.write = self.original_write # on exit restore monkey patched func
        if exc_type is ZeroDivisionError: # error handle
            print('Please DO NOT divide by zero!')
            return True  9
        10
````

- `__exit__` is called with `None`, `None`, `None` if all goes well. These are `exc_type` (Exception Class), `exc_value` (Exception instance) and `traceback` object

### The contextlib Utilities

- Before creating your own context manager classes take a look at `contextlib`, maybe you can find something already implemented.
- The `contextlib` package also includes : 
  - `closing` : A function to build context managers out of objects that provide `close()` method but don’t implement `__enter__/__exit__` interface.
  - `suppress`: A context manager to temporarily ignore exceptions given as arguments.
  - `nullcontext` : A context manager that does nothing to simplify conditional logic around object tthat may not implement context manager. It serves as a stand-in when conditional code before `with` block may or may not provide a context manager for the `with` statements.
- The `contextlib` module provides classes and a decorator that are more widely applicable than `decorator`
  - `@contextmanager` : A simple decorater that lets you build context manager from a simple generator functions.
  - `AbstractContextManager` : An ABC that formalizes the context manager interface, and makes it but easier to create context manager classes by subclassing.
  - `ContextDecorator` : A base class for defining class-based context manager that can also be used as function decorators, running the entire function within a managed context.
  - `ExitStack` : A context manager that lets you enter a variable number of context managers. When the `with` block ends, `ExitStack` calls the stacked context manager’ `__exit__` methods in LIFO order.

### Using @contextmanger

The `@contextmanager` decorator is an elegant and practical tools that brings three distinctive python features ; a function decorator, a generator, and the `with` Statement.

````python
# mirror.py
import contextlib
import sys

@contextlib.contextmanager # contextmanager decorator
def looking_glass():
    original_write = sys.stdout.write # preserve original method

    def reverse_write(text): # reverse function
        original_write(text[::-1])
		
    # note error handling is skipped ! Its full implementation is in book.
    sys.stdout.write = reverse_write # monkey patch
    yield 'JABBERWOCKY' # yield the value bound to target var of as clause
    sys.stdout.write = original_write # undo monkey patch
    
# A feature of @contextmanager is the generators decorated can also be used as decorators
@looking_glass():
  def verse():
    print("The time has come")
    
# Output
verse()
# emoc sah emit ehT
print('back to normal')
# back to normal
````

## Pattern Matching in lis.py: A case study

Read in Book!

## Do This, then That: else Blocks Beyond if

`else` blocks can be used not only with `if` construct but with `for` , `while` and `try`

- `for` : The `else` block will run only if and when the `for` loop runs to completed. (i.e. not if the `for` is aborted with a break)
- `while`: The `else` block will run only if and when the `while` loop exits because the condition became *falsy* (i.e., not if the `while` is aborted with a `break`).
- `try`: The else block will run only if no exception is raised in the try block. The official docs also state: “Exceptions in the else clause are not handled by the preceding except clauses.”

In Python, try/except is commonly used for control flow, and not just for error handling. There’s even an acronym/slogan for that documented in the official Python glossary:

    EAFP
    
        Easier to ask for forgiveness than permission. This common Python coding style assumes the existence of valid keys or attributes and catches exceptions if the assumption proves false. This clean and fast style is characterized by the presence of many try and except statements. The technique contrasts with the LBYL style common to many other languages such as C.

The glossary then defines LBYL:

    LBYL
    
        Look before you leap. This coding style explicitly tests for pre-conditions before making calls or lookups. This style contrasts with the EAFP approach and is characterized by the presence of many if statements. In a multi-threaded environment, the LBYL approach can risk introducing a race condition between “the looking” and “the leaping.” For example, the code, if key in mapping: return mapping[key] can fail if another thread removes key from mapping after the test, but before the lookup. This issue can be solved with locks or by using the EAFP approach.

Given the EAFP style, it makes even more sense to know and use else blocks well in try/except statements.

---

## File: python/ch4_19.md

# Concurrency Models in Python

- Rob Pike (Co-inventor of the Go language) explains concurrency as dealing with lots of things at once, while parallelism is all about doing lots of things at once.
- Concurrency provides a way to structure a solution to solve a problem that may (but not necessarily) be parallelizable.

## The Big Picture

- concurrent programming is hard, mostly its very easy to start threads or processes but keeping track of them is very difficult.
- starting a thread or a process is not cheap, so you don’t want to start one of them just to perform a single computation and quit. Often you want to amortize the startup cost by making each thread or process into a “worker” that enters a loop and stands by for inputs to work on further complicating communications.
- A couroutine is cheap to start. If you start a coroutine using `await` keyword, its eas to get a value returned by it, it can be safely cancelled, and you have a clear site to catch exception. But coroutines are often started by asynchronous framework making them hard to monitor.
- Finally, Python coroutines and threads are not suitable for CPU-intensive tasks, as we’ll see.

## A bit of Jargon

- Concurrency: ability of handle multiple tasks at once, make progress parallely or one at a time.
- Parallelism: ability to execute computation at the same time. Requires multicore CPU, multiple CPUs, GPU, clusters.
- Execution Unit: general term for objects that execute code concurrently, each with independent state and call stack. e.g. processes, threads, and coroutines.
- Process: An instance of computer program while it is running uses memory and slice of CPU Time. Processes communicate via pipes, sockets or memory mapped files all of which can only carry raw bytes. Python objects must be serialized into raw bytes to pass from one process to antoher. This is costly and not all python objects are serializable, A process can spawn subprocess called as child process. Processes allow preemptive multitasking i.e. OS Scheduler can suspend processes to allow running other processes.
- Thread: An execution unit within single process. When a process starts it uses a single thread (main). A process can create more threads to operate concurrently by calling operating system APIs. Threads within a process share same memory space allowing easy data sharing between threads but beware it can also cause corrupting when threads update same memory space. Threads are also enable preemptive multitasking
- Coroutine: A fucntion that can suspend itself and resume later. In python classic couroutine are build from generator functions, and antive coroutines are defined with `async def`.
- Queue: A data structure that lets us put and get items in FIFO order. Queues allow separate execution units to exchange application data and control messages such as error codes and signals to terminate. Implementation of queue varies according to underlying concurrency model. The `queue` in standard library provides queue classes to support thread, while multiprocessing and asyncio packages have their own queue classes.
- Lock: AN object that execution units can use to synchronize their execution and avoid data corruption.The implementation of a lock depends on the underlying concurrency model.
- Contention: Dispute over a limited asset. Resource contention happens when multiple execution units try to access a shared resource such as a lock or storage. There’s also CPU contention when compute intensive processes or threads must wait for the OS scheduler to give them a share of the CPU Time.

### Processes, Threads and Python’s Infamous GIL

- Each instance of Python interpreter is a process, we can use *multiprocessing* or `concurrent.futures` libraries to start additional process. Subprocess is desinged to launch processes to run external programs.
- The python interpreter uses a single thread to run the user’s program and memory garbage collector. We can use threading library to create additonal threads.
- Access to object reference counts and other internal interpreter state is controlled by a lock, the Global Interpreter Lock (GIL). Only one python thread can hold the GIL at any time. This means that only one thread can execute Python code at any time, regardless of the number of CPU cores
- To prevent a Pyhton thread from holding the GIL indefinitely, Python bytecode interpreter pauses the current python thread every 5ms by default releasing the GIL.
- When we write python code, we have no control over the GIL. But a built-in function or an extension written in C- or any language that interface at the Python/C API level can release the GIL while running time-consuming tasks.
- Every python standard library function that makes a syscall releases the GIL. This includes all functions that perform disk I/O, network I/O, and `time.sleep()`.
- Extension that integrate at the Python/C API level can also launch other non Python threads that are not affected by GIL. Such GIL-free threads generally can’t change python objects but they can read from and write to memory underlying objects that support the buffer protocol, such as `bytearray`, `array.array` and NumPy arrays.
- The effect of the GIL on network programming with Python threads is relatively small, because I/O function release the GIL, and reading or writing to the network always implies high latency compared to reading and writing to memory.
- Contention over the GIL slows down the compute intensive Python threads. Sequential, single-threaded code is simpler and faster for such tasks.
- To run CPU intensive Python code on multiple cores you must use multiple Python processes

## A Concurrent Hello World

### Spinner with Threads

start a function that blocks for 3 seconds whiel animating characters in the terminal to let user know that the program is “thinking” and not stalled.

````python
import itertools
import time
from threading import Thread, Event

def spin(msg: str, done: Event) -> None:	# will run in a separate thread. done argument is thread Event to synchronize threads
    for char in itertools.cycle(r'\|/-'):	# infinite chars yielding one at a time
        status = f'\r{char} {msg}'	# trick to move cursor back to start of the line
        print(status, end ='', flush=True)	# flush and clean the line
        if done.wait(.1):	# returns True when event is set by another thread. if the timeout elapses, it runs False. # effectively sets frame rate
            break
    blanks = '' * len(status)
    print(f'\r{blanks}\r', end = '')


def slow()->int:
    time.sleep(3)
    return 42

# supervisor and # main function
def supervisor() -> int:	# will return result of slow
    done = Event()	# Event object that co-ordinates the activities of main thread and spinner thread
    spinner = Thread(target=spin, args = ('thinking!', done))	# target is spin
    print(f'spinner object: {spinner}')
    spinner.start()	# start the spinner, keeps on running animation
    result = slow()	# slow function called, blocking main thread
    done.set()	# update the event status to True, useful to get out of for loop in spin
    spinner.join()	# wait until spinner finishes
    return result

def main()->None:
    result = supervisor()
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()

````

Lets implement same with processes

### Spinner with Processes

- `multiprocessing` pacakge supports running concurrent tasks in separate Python processes instead of threads. When you create `multiprocessing.Process` instance, a whole new Python interpretor is started as a child process in background.
- Since each Python process has its own GIL, this allows your program to  use all available CPU cores—but that ultimately depends on the operating system scheduler.

````python
import itertools
import time
from multiprocessing import Process, Event
from multiprocessing import synchronize

def spin(msg: str, done: synchronize.Event) -> None:
# [same code as previous]

def supervisor() -> int:
    done = Event()
    spinner = Process(target=spin, args = ('thinking!', done))
    print(f'spinner object: {spinner}')
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

# [same code as previous]
````

- `<Process name='Process-1' parent=14868 initial>`, where `14868` is the process ID of the Python instance running  *spinner_proc.py*
- The basic API of `threading` and `multiprocessing` are similar, but their implementation is very different, and `multiprocessing` has a much larger API to handle the added complexity of multiprocess  programming. 
- For example, one challenge when converting from threads to processes is  how to communicate between processes that are isolated by the operating  system and can’t share Python objects. This means that objects crossing process boundaries have to be  serialized and deserialized, which creates overhead.

### Spinner with Coroutines

- read in this order, supervisor, main, spin, slow

````python
import itertools
import asyncio

async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end ='', flush=True)
        try:
            await asyncio.sleep(.1)	# sleep without blocking other coroutines.
        except asyncio.CancelledError:
            break
    blanks = '' * len(status)
    print(f'\r{blanks}\r', end = '')


async def slow()->int:
    await asyncio.sleep(3)
    return 42

async def supervisor() -> int:	# native couroutines are async def
    spinner = asyncio.create_task(spin('thinking!'))	# schedules eventual execution of spin, immediately return instance of asyncio.Task
    print(f'spinner object: {spinner}')
    result = await slow()	# calls slow blocking supervisor till it returns
    spinner.cancel()	# raises CancelledError
    return result

def main()->None:
    result = asyncio.run(supervisor())	# starts the event loop to drive the coroutines that will set other coroutines in motion. Main will be blocker till supervisor returns
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()
````

- Interesting experiment, using this spinner never appears ? Why

````python
async def slow() -> int:
    time.sleep(3)
    return 42
````

- To understand what is happening, recall that Python code using `asyncio` has only one flow of execution, unless you’ve explicitly started additional threads or processes. That means only one coroutine executes at any point in time. Concurrency is achieved by control passing from one coroutine to another.
- when `await` transfers control to `slow` coroutine, sleep block for 3 seconds, nothing else can happen in program as main thread is blocked and its the only thread.
- Right after `slow` returns, the `spinner` task is cancelled. The flow of control never reached the body of the `spin` coroutine.

### Supervisor Side-by-Side

- An `asyncio.Task` is roughly the equivalent of a `threading.Thread`.
- A `Task` drives a coroutine object, and a `Thread` invokes a callable.
- A coroutine yields control explicitly with the `await` keyword.
- You don’t instantiate `Task` objects yourself, you get them by passing a coroutine to `asyncio.create_task(…)`.
- When `asyncio.create_task(…)` returns a `Task` object, it is already scheduled to run, but a `Thread` instance must be explicitly told to run by calling its `start` method.
- In the threaded `supervisor`, `slow` is a plain function and is directly invoked by the main thread. In the asynchronous `supervisor`, `slow` is a coroutine driven by `await`.
- There’s no API to terminate a thread from the outside; instead, you must send a signal—like setting the `done` `Event` object. For tasks, there is the `Task.cancel()` instance method, which raises `CancelledError` at the `await` expression where the coroutine body is currently suspended.
- The `supervisor` coroutine must be started with `asyncio.run` in the `main`  function.

## The Real Impact of GIL

- In all the implementation of `slow` function we can replace it with any well designed asynchronous network library call and spinner will wait till that request completes. Because such libraries provide coroutines that yield control back to the event loop while waiting for network.
- NOTE: but for CPU-intensive code, story is different because it will be busy calculating that task. Take example of calculating prime number function
  - In spinner_proc.py, replacing `time.sleep(3)` with `is_prime(n)` : since spinner is controlled by child process so it keeps spinning while primality test is computed by parent process.
  - In spinner_thread.py : spinner is controlled by secondary thread, so it continues spinning while the primality test is computed by main thread. In this example spinner runs because Python suspends thread every 5ms, making GIL available to other pending threads. This doesn’t have visible impact on running time of this specific example, because quickly iterates once and releases the GIL as it waits for `done` event, so there is not much contention. Because there are two thread, one is CPU intensive while other is not.
  - In spinner_asycnio.py, replacing `await asyncio.sleep(3)` with a call to `is_prime(n)` : spinner never appears, similar to replacing it with `sleep(3)`. The flow of control will pass from supervisor to slow and then to `is_prime`. When `is_prime` return, slow return, `supervisor` resumes, cancelling spinner task even before its executes. One way to keep `spinner` alive is writing it as coroutine and periodically call `asyncio.sleep(0)` in an await expression to yield control back to even loop. However that ends up slowing `is_prime` because of passing of control here and there.

## A Homegrown Process Pool

Lets write a program to check primality of a sample of 20 integers, from 2 to 10^16 - 1

In serial case its approxmately the sum of times for each check but it is computed separately

````python
# primes.py
import math

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True


NUMBERS = [
            2,
            3333333333333333,
            4444444444444444,
            5555555555555555,
            6666666666666666,
            142702110479723,
            7777777777777777,
            299593572317531,
            9999999999999999,
            3333333333333301,
            3333335652092209,
            4444444488888889,
            4444444444444423,
            5555553133149889,
            5555555555555503,
            6666666666666719,
            6666667141414921,
            7777777536340681,
            7777777777777753,
            9999999999999917,
        ]
````

````python
#!/usr/bin/env python3

"""
sequential.py: baseline for comparing sequential, multiprocessing,
and threading code for CPU-intensive work.
"""

from time import perf_counter
from typing import NamedTuple

from primes import is_prime, NUMBERS

class Result(NamedTuple):
    prime: bool
    elapsed: float

def check(n: int) -> Result:
    t0 = perf_counter()
    prime = is_prime(n)
    return Result(prime, perf_counter() - t0)

def main() -> None:
    print(f'Checking {len(NUMBERS)} numbers sequentially:')
    t0 = perf_counter()
    for n in NUMBERS:
        prime, elapsed = check(n)
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')

    elapsed = perf_counter() - t0
    print(f'Total time: {elapsed:.2f}s')

if __name__ == '__main__':
    main()
````

- benchmark takes 14s on my laptop

### Process-Based Solution

Let’s distribute primality across cores : Lets create a number of worker process equal to number of CPU cores

````python
# procs.py
import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count	 # emulating threading using multiprocessing.
from multiprocessing import queues # multiprocessing.queue has SimpleQueue class for type hints

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple): # tuple representing Result
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int] # TypeAlias
ResultQueue = queues.SimpleQueue[PrimeResult] # TypeAlias

def check(n: int) -> PrimeResult:	# similar to sequential.py
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:	# worker gets a queue with numbers, and another to put results
    while n := jobs.get(): # 0 is like poison pill: signal for worker to finish
        results.put(check(n))  # put items in queue for checking
    results.put(PrimeResult(0, False, 0.0))	# send back to main loop to indicate end of worker

def start_jobs(
    procs: int, jobs: JobQueue, results: ResultQueue	# procs is number of prime check in parallel
) -> None:
    for n in NUMBERS:
        jobs.put(n)	# enqueue the numbers to be checked in jobs
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs, results)) # fork child process for each worker
        proc.start() # start child process
        jobs.put(0) # poison pill
````

````python
# main of above program
def main() -> None:
    if len(sys.argv) < 2: # either pass cpu count or takes from library
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()	# create job queue
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results) # start jobs
    checked = report(procs, results) # retrieve result and display
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s') # display all numbers checked

def report(procs: int, results: ResultQueue) -> int: # args are the number of procs queue to post the result
    checked = 0
    procs_done = 0
    while procs_done < procs: # loop till all process completes
        n, prime, elapsed = results.get() # get one PrimeResult
        if n == 0: # if n is zero, process exited
            procs_done += 1
        else:
            checked += 1 
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')
    return checked

if __name__ == '__main__':
    main()
````

- Notice how time is reduce to 4.13s

## Python in Multicore World

Herb Sutter commented : The major processor manufacturers and architectures, from Intel and AMD to Sparc and PowerPC, have run out of room with most of their traditional approaches to boosting CPU performance. Instead of driving clock speeds and straight-line instruction throughput ever higher, they are instead turning en masse to hyper-threading and multicore architectures.

What Sutter calls the “free lunch” was the trend of software getting faster with no additional developer effort because CPUs were executing sequential code faster, year after year. Since 2004, that is no longer true: clock speeds and execution optimizations reached a plateau, and now any significant increase in performance must come from leveraging multiple cores or hyperthreading, advances that only benefit code that is written for concurrent execution.

Python’s story started in the early 1990s, when CPUs were still getting exponentially faster at sequential code execution. There was no talk about multicore CPUs except in supercomputers back then. At the time, the decision to have a GIL was a no-brainer. The GIL makes the interpreter faster when running on a single core, and its implementation simpler. The GIL also makes it easier to write simple extensions through the Python/C API.

Despite the GIL, Python is thriving in applications that require concurrent or parallel execution, thanks to libraries and software architectures that work around the limitations of CPython.

### System Administration

Python is widely used to manage large fleets of servers, routers, load balancers, and network-attached storage (NAS). It’s also a leading option in software-defined networking (SDN) and ethical hacking. Major cloud service providers support Python through libraries and tutorials authored by the providers themselves or by their large communities of Python users.

In this domain, Python scripts automate configuration tasks by issuing  commands to be carried out by the remote machines, so rarely there are  CPU-bound operations to be done. Threads or coroutines are well suited for such jobs.

Beyond the standard library, there are popular Python-based projects to manage server clusters: tools like Ansible and Salt, as well as libraries like Fabric.

### Data Science

Data science—including artificial intelligence—and scientific computing are very well served by Python. Applications in these fields are compute-intensive, but Python users benefit from a vast ecosystem of numeric computing libraries written in C,  C++, Fortran, Cython, etc.—many of which are able to leverage multicore machines, GPUs, and/or distributed parallel computing in heterogeneous clusters.

- Project Jupyter : Two browser-based interfaces—Jupyter Notebook and JupyterLab—that allow users to run and document analytics code potentially running across the network on remote machines.
- TensorFlow and Pytorch: top two deep learning frameworks. Both are written in C++ and are able to leverage multiple cores, GPUs and clusters.
- Dask: parallel computing library that can farm out work to local processes or cluster of machines.

### Server-Side Web/Mobile Development

ython is widely used in web applications and for the backend APIs supporting  mobile applications. How is it that Google, YouTube, Dropbox, Instagram, Quora, and  Reddit—among others—managed to build Python server-side applications  serving hundreds of millions of users 24x7

- At *web scale*, the key is an architecture that allows horizontal scaling. At that point, all systems are distributed systems, and no single programming language is likely to be the right choice for every part of the solution.
- Distributed systems is a field of academic research, but fortunately some practitioners have written accessible books anchored on solid research and practical experience. One of them is Martin Kleppmann, the author of *Designing Data-Intensive Applications* (O’Reilly).

Consider figure, the first of many architecture diagrams in Kleppmann’s book. Here are some components I’ve seen in Python engagements:

- Application caches:*memcached*, *Redis*, *Varnish*
- Relational databases: *PostgreSQL*, *MySQL*
- Document databases: *Apache CouchDB*, *MongoDB*
- Full-text indexes: *Elasticsearch*, *Apache Solr*
- Message queues: *RabbitMQ*, *Redis*

![Architecture for data system that combining several components](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_1903.png)

### WSGI Application Servers

WSGI—the Web Server Gateway Interface—is a standard API for a Python framework or application to receive requests from an HTTP server and send responses to it. WSGI application servers manage one or more processes running your application, maximizing the use of the available CPUs.

best-know application servers in python web projects are 

- mod_wsgi
- uWSGI24
- Gunicorn
- NGINX Unit

### Distributed Task Queues

When the application server delivers a request to one of the Python processes running your code, your app needs to respond quickly: you want the process to be available to handle the next request as soon as possible. However, some requests demand actions that may take longer—for example, sending email or generating a PDF. That’s the problem that distributed task queues are designed to solve.

Celery and RQ are the best known open source task queues with Python APIs. Cloud providers also offer their own proprietary task queues.

These products wrap a message queue and offer a high-level API for delegating tasks to workers, possibly running on different machines.

Quoting directly from Celery’s FAQ, here are some typical use cases:

- Running something in the background. For example, to finish the web  request as soon as possible, then update the users page incrementally.  This gives the user the impression of good performance and “snappiness,” even though the real work might actually take some time.
- Running something after the web request has finished.
- Making sure something is done, by executing it asynchronously and using retries.
- Scheduling periodic work.

Besides solving these immediate problems, task queues support horizontal scalability. Producers and consumers are decoupled: a producer doesn’t call a  consumer, it puts a request in a queue. Consumers don’t need to know  anything about the producers (but the request may include information  about the producer, if an acknowledgment is required). Crucially, you can easily add more workers to consume tasks as demand  grows. That’s why *Celery* and *RQ* are called distributed task queues.

---

## File: python/ch4_20.md

# 20. Concurrent Executors

- 99% of use cases application programmer is likely to run into, the following pattern
- chapter focuses on the `concurrent.futures.Executor` classes that encapsulate the pattern of *spawning a bunch of independent threads and collecting results in a queue*
- mostly systems programmer utilize other features of python quite heavily

## Concurrent Web Downloads

- concurrency is essential for efficient network I/O: instead of waiting of response application should work on something else.
- Following codes fetches 20 country flags from web. There are 4 version of it, Sequential being slowest wihle other concurrent implementation being faster.

### A Sequential Download Script

````python
import time
from pathlib import Path
from typing import Callable

import httpx # not part of standard library/actually its convention to leave one blank line

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split() # List of ISO 3166 country codes

BASE_URL = 'https://www.fluentpython.com/data/flags' # dir with flag img
DEST_DIR = Path('downloaded')                        # local dir

def save_flag(img: bytes, filename: str) -> None: # save img, bytes to file
    (DEST_DIR / filename).write_bytes(img)

def get_flag(cc: str) -> bytes: # return binary contents
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1, # for network calls always add timeout
                     follow_redirects=True) # by default doesn't follow redirectly
    resp.raise_for_status() # there is no error handling but this method raises exception
    return resp.content

def download_many(cc_list: list[str]) -> int: # this will be used for comparisons
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image, f'{cc}.gif')
        print(cc, end=' ', flush=True) # display one country code at a time
    return len(cc_list)

def main(downloader: Callable[[list[str]], int]) -> None: # main called with downloading fn
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many) # call many with download function
````

### Downloading with concurrent.futures

- Main feature of `concurrent.futures` packages are `ThreadPoolExecutor` and `ProcessPoolExecutor` classes which implement an API to submit callables for execution in different threads or processes, respectively.

````python
from concurrent import futures

from flags import save_flag, get_flag, main # reuse old functions

def download_one(cc: str): # this is what each worker will execute
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor: # context manage ThreadPoolExecutor
        res = executor.map(download_one, sorted(cc_list)) # map method is similar to built-in map, returns a generator that we can iterate to retrieve the value returned by each function call.

    return len(list(res))
    # Return the number of results obtained. If any of the threaded calls raises an exception, that exception is raised here when the implicit next() call inside the list constructor tries to retrieve the corresponding return value from the iterator returned by executor.map.
    
if __name__ == '__main__':
    main(download_many) # return number of results obtained.
````

- the computed default for `max_workers` is sensible, and `ThreadPoolExecutor` avoids starting new workers unnecessarily. Understanding the logic behind `max_workers` may help you decide when and how to set it yourself.

### Where are the Futures ?

- there are two classed name `Future` in standard library : `concurrent.futures.Future` and `asyncio.Future`. They server same purpose : an instance of either `Future` class represents a deferred computaion that may or may not have completed.
- Futures encapsulate pending operation so that we can put them in queues, check whether they are done and retrieve results (exception) when they become available.
- We should not create futures: they are meant to created by concurrency framework. a `Future` represent something that will run eventually, therefore it must be schedules to run, and that the job of framework.
- Application code is not supposed to change the state of a future: the concurrency framework changes the state of a future when the computation it represents is done, and we can’t control when that happens.
- Both types of `Future` have a `.done()` method that is nonblocking and returns a Boolean that tells you whether the callable wrapped by that future has executed or not. However, instead of repeatedly asking whether a future is done, client code usually asks to be notified. That’s why both `Future` classes have an `.add_done_callback()` method: you give it a callable, and the callable will be invoked with the future as the single argument when the future is done. Be aware that the callback callable will run in the same worker thread or process that ran the function wrapped in the future.
- There is also a `.result()` method, which works the same in both classes when the future is done: it returns the result of the callable, or re-raises whatever exception might have been thrown when the callable was executed.
- However, when the future is not done, the behavior of the `result` method is very different between the two flavors of `Future`. In a `concurrency.futures.Future` instance, invoking `f.result()` will block the caller’s thread until the result is ready. An optional `timeout` argument can be passed, and if the future is not done in the specified time, the `result` method raises `TimeoutError`. The `asyncio.Future.result` method does not support timeout, and `await` is the preferred way to get the result of futures in `asyncio`—but `await` doesn’t work with `concurrency.futures.Future` instances.

````python
def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5] # take only 5 entries
    with futures.ThreadPoolExecutor(max_workers=3) as executor: # max worker to 3 so see future pending in the otuput
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):	# call in order, result will not be in order
            future = executor.submit(download_one, cc) # submit the callable
            to_do.append(future) # add that future to list
            print(f'Scheduled for {cc}: {future}')

        for count, future in enumerate(futures.as_completed(to_do), 1): # as_completed yields futures as they are completed
            res: str = future.result()
            print(f'{future} result: {res!r}')

    return count
````

## Launching Processes with concurrent.futures

- `concurrent.futures` supportes parallel computation on multicore machines because it supports distributing work among multiple python processes using `ProcessPoolExecutor`.
- In our program there is no advantage of a process pool executor or any I/O bound job. We will get same performance.
- Its useful for CPU-Intensive jobs

### Multicore Prime Checker Redux

````python
import sys
from concurrent import futures
from time import perf_counter
from typing import NamedTuple

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple):
    n: int
    flag: bool
    elapsed: float

def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def main() -> None:
    if len(sys.argv) < 2:
        workers = None
    else:
        workers = int(sys.argv[1])

    executor = futures.ProcessPoolExecutor(workers)
    actual_workers = executor._max_workers  # type: ignore # undocumented instance attribute of Process pool executor taken to show max_workers, disable typehints using that comment

    print(f'Checking {len(NUMBERS)} numbers with {actual_workers} processes:')

    t0 = perf_counter()

    numbers = sorted(NUMBERS, reverse=True) # sort the numbers to expose difference in behaviour of this code as compared to previous
    with executor:
        for n, prime, elapsed in executor.map(check, numbers):
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')

    time = perf_counter() - t0
    print(f'Total time: {time:.2f}s')

if __name__ == '__main__':
    main()
````

- you’ll see the results appearing in strict descending order. In contrast, the ordering of the output of procs.py (shown in “Process-Based Solution”) is heavily influenced by the difficulty in checking whether each number is a prime.
- `executor.map(check, numbers)` always returns the results in same order as the numbers are given.

## Experimenting with Executor.map

````python
from time import sleep, strftime
from concurrent import futures

def display(*args):# simply print whatever given
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)

def loiter(n): # does nothing except disaply message when it starts
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10 # return so we can see how to collect results

def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)	# only 3 threads
    results = executor.map(loiter, range(5))	# submit 5 taks o executor
    display('results:', results) # immidiatedly shows 3 outputs
    display('Waiting for individual results:')
    for i, result in enumerate(results):
    # The enumerate call in the for loop will implicitly invoke next(results), which in turn will invoke _f.result() on the (internal) _f future representing the first call, loiter(0). The result method will block until the future is done, therefore each iteration in this loop will have to wait for the next result to be ready.
        display(f'result {i}: {result}')

if __name__ == '__main__':
    main()
````

- The `Executor.map` function is easy to use, but often it’s preferable to get the results as they are ready, regardless of the order they were submitted. To do that, we need a combination of the `Executor.submit` method and the `futures.as_completed` function
- The combination of `executor.submit` and `futures.as_completed` is more flexible than `executor.map` because you can `submit`  different callables and arguments, while `executor.map` is designed to run the same callable on the different arguments. In addition,  the set of futures you pass to `futures.as_completed` may come from more than one executor—perhaps some were created by  a `ThreadPoolExecutor` instance, while others are from a  `ProcessPoolExecutor`.

## Downloads with Progress Display and Error Handling

We will implement version of `flags2.py` with animated, text-mode progress bar implemented with tqdm packages.

````python
from collections import Counter
from http import HTTPStatus

import httpx
import tqdm  # type: ignore  1

from flags2_common import main, save_flag, DownloadStatus # import already implemented stuff

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

def get_flag(base_url: str, cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()  # HTTPStatusError, if HTTP code not in range(200,300)
    return resp.content

def download_one(cc: str, base_url: str, verbose: bool = False) -> DownloadStatus:
    try:
        image = get_flag(base_url, cc)
    except httpx.HTTPStatusError as exc: # handle 404 correctly
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND # by setting its local status to DownloadStatus.NOT_FOUND; DownloadStatus is an Enum imported from flags2_common.py.
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        save_flag(image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'OK'

    if verbose:
        print(cc, msg)

    return status
````



### Sequential Implementation

````python
def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  _unused_concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter() # tally different download outcomes
    cc_iter = sorted(cc_list) # list of country codes as args
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter) # if no in -v mode, cc_iter is passed to tqdm, which returns an iterator yielding the items in cc_iter
    for cc in cc_iter:
        try:
            status = download_one(cc, base_url, verbose) # call to download one
        except httpx.HTTPStatusError as exc:
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg = error_msg.format(resp=exc.response)
        except httpx.RequestError as exc:
            error_msg = f'{exc} {type(exc)}'.strip()
        except KeyboardInterrupt:
            break
        else:
            error_msg = ''

        if error_msg:
            status = DownloadStatus.ERROR
        counter[status] += 1
        if verbose and error_msg:
            print(f'{cc} error: {error_msg}')

    return counter
````

### Futures.as_completed

````python
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30 # default concurrent req
MAX_CONCUR_REQ = 1000 # max concurrent req


def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    with ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do_map = {}
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc,
                                     base_url, verbose)
            to_do_map[future] = cc
        done_iter = as_completed(to_do_map)
        if not verbose:
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))
        for future in done_iter:
            try:
                status = future.result()
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
            except KeyboardInterrupt:
                break
            else:
                error_msg = ''

            if error_msg:
                status = DownloadStatus.ERROR
            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future]
                print(f'{cc} error: {error_msg}')
    return counter

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
````



---

## File: python/ch4_21.md

# Asynchronous Programming

Three main topics to be addressed,

- Python’s `async def`, `await`, `async with` and `async for` constructs
- Objects supporting those constructs : native coroutines and asynchronous variants of context managers, iterables, generators, and comprehensions.
- `asyncio` and other asynchronous libraries

## A Few Definitions

Python offers three kinds of coroutines

- *Native Coroutines*
  - A coroutine function defined with `async def` and can be delegated from a native coroutines to another native coroutine using `await` keyword, similar to how classic coroutines use `yield from`.
  - NOTE: `await` can’t be used outside `async def` function but its not necessary to exist.
- *Classic Coroutines*
  - A generator function that consumes data sent to it via `my_coro.send(data)` calls, and reads that data by using `yield` in an expression. Classic coroutines can delegate to other classic coroutines using `yield from`.
  - Classic coroutines can’t be driven using `await` and are not longer supported by asyncio.
- *Generator Based Coroutines*
  - A generator function decorated with `@types.coroutine`. That decorator makes the generator function compatible with `await` keyword.

*Ansynchronous generator*

- A generator function defined with `async def` and using `yield` in its body. It returns an asynchronous generator object that offers `__anext__` with the new `await` keyword.

## An Asyncio Example : Probing domains

A search for domains for a Python blog

```python
#!/usr/bin/env python3
import asyncio
import socket
from keyword import kwlist

MAX_KEYWORD_LEN = 4


async def probe(domain: str) -> tuple[str, bool]:	# returns tuple with domain name and a boolean, True meaning it resolved
    loop = asyncio.get_running_loop() # get a reference to asyncio event loop
    try:
        await loop.getaddrinfo(domain, None) # gets the five part tuple parameter to connect to given address using socket
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


async def main() -> None: # main must be a coroutine
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN) # generator to yield python words
    domains = (f'{name}.dev'.lower() for name in names) # append .dev suffix
    coros = [probe(domain) for domain in domains] # list of coroutines
    for coro in asyncio.as_completed(coros): # as_completed is a generartor that yields coroutines that reutrn the result to the order they are completed in
        domain, found = await coro  # since this coroutine is completed await doesn't block
        mark = '+' if found else ' '
        print(f'{mark} {domain}')


if __name__ == '__main__':
    asyncio.run(main()) # starts the event loop and returns only when event loop exits
```

### Guido’s Trick to Read Asynchronous Code

- Pretend `async` and `await` keywords are not there, If you do that you will realise that coroutines read like plain old sequential function
- here during execute of `probe('if.dev')` coroutine, a new coroutine object is created by `getaddrinfo`. Awaiting it starts the low-level query and yields control back to event loop. The event loop can then drive other pending coroutine object and when there is a response back, that specific coroutine object resumes and returns control back to `probe('if.dev')` which was suspended at `await` and can now handle possible exceptions and return result tuple
- `asyncio.as_completed` and `await` can be applied to any `awaitable` object

## New Concept : Awaitable

The `for` keyword works with iterables. The `await` keyword works with awaitables.

Usually these awaitables are encountered.

- A native coroutine object, which you get by calling a native coroutine function
- An `asyncio.Task`, which you usually get by passing a coroutine object to `asyncio.create_task()`

However, end-user code does not always need to `await` on a `Task`. We use `asyncio.create_task(one_coro())` to schedule `one_coro` for concurrent execution, without waiting for its return. That’s what we did with the `spinner` coroutine in *spinner_async.py* 

If you don’t expect to cancel the task or wait for it, there is no need to keep the `Task` object returned from `create_task`. Creating the task is enough to schedule the coroutine to run.

When implementing asynchronous libraries or contributing to *asyncio* itself, you may also deal with these lower-level awaitables:

- An object with an `__await__` method that returns an iterator; for example, an `asyncio.Future` instance (`asyncio.Task` is a subclass of `asyncio.Future`)
- Objects written in other languages using the Python/C API with a `tp_as_async.am_await` function, returning an iterator (similar to `__await__` method)

## Downloading with asyncio and HTTPX

As of Python 3.10, asyncio only supports TCP and UDP directly, and there are no asynchronous HTTP client or server packages in the standard library. we will be using HTTPX in all the HTTP client examples.

**flags_asyncio.py : startup functions**

````python
def download_many(cc_list: list[str]) -> int: # needs to be plain function not a coroutine, as it passed to and called by main
    return asyncio.run(supervisor(cc_list)) # execute the event loop driving the supervisor(cc_list) couroutine object until it returns. This will block while even loop runs

async def supervisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client: # asynchronous HTTP client operation in httpx are methods of AsyncClient
        to_do = [download_one(client, cc)
                 for cc in sorted(cc_list)] # list of coroutines
        res = await asyncio.gather(*to_do) # wait for .gather couroutines and waits for all of them to complete

    return len(res) # return lenght of the list returned by asyncio.gather

if __name__ == '__main__':
    main(download_many)
````

**flags_asyncio.py : imports and download functions**

````python
import asyncio

from httpx import AsyncClient # must be installed

from flags import BASE_URL, save_flag, main # reuse code from flags.py

async def download_one(client: AsyncClient, cc: str): # download one must be a native coroutine so it can await on get_flag
    image = await get_flag(client, cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

async def get_flag(client: AsyncClient, cc: str) -> bytes: # needs to recieve the AsyncClient instance returning a ClientResponse object that is also an asychronous context manager
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=6.1,
                                  follow_redirects=True) # network I/O operation are run by default by asynchronous context manager
    return resp.read()
````

### The Secret of Native Coroutines: Humble Generators

![Await channel diagram](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_2101.png)

- A key difference b/w classic coroutines and flags_asyncio.py is that there are no visible `.send()` calls or `yield` expression in latter. You code sits b/w asyncio library and asynchronous libraries you are using, such as HTTPX.
- Under the hood, the `asyncio` event loop makes the `.send` calls that drive your coroutines, and your coroutines `await` on other coroutines, including library coroutines. As mentioned, `await` borrows most of its implementation from `yield from`, which also makes `.send` calls to drive coroutines.
- he `await` chain eventually reaches a low-level awaitable, which returns a generator that the event loop can drive in response to events such as timers or network I/O. The low-level awaitables and generators at the end of these `await` chains are implemented deep into the libraries, are not part of their APIs, and may be Python/C extensions.
- Using functions like `asyncio.gather` and `asyncio.create_task`, you can start multiple concurrent `await` channels, enabling concurrent execution of multiple I/O operations driven by a single event loop, in a single thread.

### The All-or-Nothing Problem

we could not reuse the get_flag function from flags.py. We had to rewrite it as a coroutine to use the asynchronous API of HTTPX. For peak performance with asyncio, we must replace every function that does I/O with an asynchronous version that is activated with await or asyncio.create_task, so that control is given back to the event loop while the function waits for I/O. If you can’t rewrite a blocking function as a coroutine, you should run it in a separate thread or process

## Asynchronous Context Managers 

- a context manager implements `__enter__` and `__exit__` (for graceful cleanup).
- In asynchronous driver like `asyncpg`, the setup and wrap-up need to be coroutines so that other operation can happen concurrently. But classic `with` keyword doesn’t work properly in asynchronous cases that is why `async with` was introduced implementing `__aenter__` and `__aexit__` methods as coroutines.

````python
async with connection.transaction():
    await connection.execute("INSERT INTO mytable VALUES (1, 2, 3)")
````

- Using coroutines to implement `Transaction` as an asynchronous context manager allows *asyncpg* to handle many transactions concurrently.

## Enhancing the asyncio Downloader

- our last implementation of progress displayed and done error handling in `flags2`.

### Using asyncio.as_completed and a Thread

- previous example we use `asyncio.gather` which returned list with result of coroutines in order they were submitted which implied it return when all of them completed.
- however to update a progress bar we need to know results as they are done
- We will use `asyncio` equivalent of `as_completed` generator function that we used in thread pool example

````python
import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path

import httpx
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus, save_flag

# low concurrency default to avoid errors from remote site,
# such as 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

async def get_flag(client: httpx.AsyncClient, # very similar to sequential implementation
                   base_url: str,
                   cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True) # .get AsyncClient method and coroutine by default so we await it
    resp.raise_for_status()
    return resp.content

async def download_one(client: httpx.AsyncClient,
                       cc: str,
                       base_url: str,
                       semaphore: asyncio.Semaphore,
                       verbose: bool) -> DownloadStatus:
    try:
        async with semaphore: # semaphore as async context manager so program as a whole is not blocked only this coroutine is suspended when semaphore is zero
            image = await get_flag(client, base_url, cc)
    except httpx.HTTPStatusError as exc: # error handling as before
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        await asyncio.to_thread(save_flag, image, f'{cc}.gif') # I/O operation, to avoid blocking event loop, run in a thread
        status = DownloadStatus.OK
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return status
````

### Throttling Requests with a Semaphore

- network client should be throttled to avoid doing DDOS on a server accidently
- A semaphore is a synchronization primitive, more flexible than a lock. It can be held by multiple coroutines, with a configurable max number.
- In threadpool implementation of `flags2.py` we use max_workers as number of throttle. In above example supervisor function creates asyncio.Semaphore which is passed as args to download one.
- Computer scientist Edsger W. Dijkstra invented the semaphore in the early 1960s. It’s a simple idea, but it’s so flexible that most other synchronization objects—such as locks and barriers—can be built on top of semaphores. There are three `Semaphore` classes in Python’s standard library: one in `threading`, another in `multiprocessing`, and a third one in `asyncio`.
- An `asyncio.Semaphore` has an internal counter that is decremented whenever we `await` on the `.acquire()` coroutine method, and incremented when we call the `.release()` method

```python
    semaphore = asyncio.Semaphore(concur_req)
```

- Awaiting on `.acquire()` causes no delay when the counter is greater than zero, but if the counter is zero, `.acquire()` suspends the awaiting coroutine until some other coroutine calls `.release()` on the same `Semaphore`, thus incrementing the counter. Instead of using those methods directly, it’s safer to use the `semaphore` as an asynchronous context manager

````python
async with semaphore:
            image = await get_flag(client, base_url, cc)
````

- The `Semaphore.__aenter__` coroutine method awaits for `.acquire()`, and its `__aexit__` coroutine method calls `.release()`. That snippet guarantees that no more than `concur_req` instances of `get_flags` coroutines will be active at any time. Each of the `Semaphore` classes in the standard library has a `BoundedSemaphore`  subclass that enforces an additional constraint

````python
# rest of the code for above asyncio downloader
async def supervisor(cc_list: list[str],
                     base_url: str,
                     verbose: bool,
                     concur_req: int) -> Counter[DownloadStatus]: # same args as download_many
    counter: Counter[DownloadStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req) # semaphore
    async with httpx.AsyncClient() as client:
        to_do = [download_one(client, cc, base_url, semaphore, verbose)
                 for cc in sorted(cc_list)] # create list of coroutine objects
        to_do_iter = asyncio.as_completed(to_do) # iterator that return as coroutines are completed
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list)) # tqdm to display progress
        error: httpx.HTTPError | None = None # exceptions
        for coro in to_do_iter: # iterate over tasks
            try:
                status = await coro # await for result
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
                error = exc # scope of exc limited here, so assign to error
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
                error = exc
            except KeyboardInterrupt:
                break

            if error:
                status = DownloadStatus.ERROR # set a status if failed.
                if verbose:
                    url = str(error.request.url)
                    cc = Path(url).stem.upper()
                    print(f'{cc} error: {error_msg}')
            counter[status] += 1

    return counter

def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[DownloadStatus]:
    coro = supervisor(cc_list, base_url, verbose, concur_req)
    counts = asyncio.run(coro) # instantiate supervisor coroutine object and pass it to the event loop with asyncio.run

    return counts

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
````

### Making Multiple Request for Each Download

- Suppose you want to save each country flag with the name of the country  and the country code, instead of just the country code. Now you need to  make two HTTP requests per flag: one to get the flag image itself, the  other to get the *metadata.json* file in the same directory as the image—that’s where the name of the country is recorded.
- Coordinating multiple requests in the same task is easy in the threaded script: just make one request then the other, blocking the thread twice, and keeping both pieces of data (country code and name) in local variables, ready to use when saving the files. If you needed to do the same in an asynchronous script with callbacks, you needed nested functions so that the country code and name were available in their closures until you could save the file, because each callback runs in a different local scope. The `await` keyword provides relief from that, allowing you to drive the asynchronous requests one after the other, sharing the local scope of the driving coroutine.
- We will implement two more functions : `get_country` and `download_one` again

````python
# get_country
async def get_country(client: httpx.AsyncClient,
                      base_url: str,
                      cc: str) -> str: # string with country name returned
    url = f'{base_url}/{cc}/metadata.json'.lower()
    resp = await client.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    metadata = resp.json() # dict built from json
    return metadata['country'] # return country name
  
  
# download_one
async def download_one(client: httpx.AsyncClient,
                       cc: str,
                       base_url: str,
                       semaphore: asyncio.Semaphore,
                       verbose: bool) -> DownloadStatus:
    try:
        async with semaphore: # hold semaphore
            image = await get_flag(client, base_url, cc)
        async with semaphore: # again hold for get_country
            country = await get_country(client, base_url, cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        filename = country.replace(' ', '_') # country name to create files
        await asyncio.to_thread(save_flag, image, f'{filename}.gif')
        status = DownloadStatus.OK
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return status
````

- We put the calls to `get_flag` and `get_country` in separate `with` blocks controlled by the `semaphore` because it’s good practice to hold semaphores and locks for the shortest possible time.
- We could schedule both `get_flag` and `get_country` in parallel using `asyncio.gather`, but if `get_flag` raises an exception, there is no image to save, so it’s pointless to run `get_country`. But there are cases where it makes sense to use `asyncio.gather` to hit several APIs at the same time instead of waiting for one response before making the next request.

## Delegating Tasks to Executors

One important advantage of Node.js over Python for asynchronous programming is the Node.js standard library, which provides async APIs for all I/O—not just for network I/O. In Python, if you’re not careful, file I/O can seriously degrade the performance of asynchronous applications, because reading and writing to storage in the main thread blocks the event loop.

```python
        await asyncio.to_thread(save_flag, image, f'{cc}.gif')
```

- We used above line to write data in main thread. Instead we can get reference to main event loop and delegate this task to another thread using `asyncio.to_thread`

````python
        loop = asyncio.get_running_loop() # get eventloop
        loop.run_in_executor(None, save_flag, # None defaults to ThreadPoolExecutor
                             image, f'{cc}.gif') # positional args to function to run.
````

A common pattern in asynchronous APIs is to wrap blocking calls that are implementation details in coroutines using `run_in_executor` internally. That way, you provide a consistent interface of coroutines to be driven with `await`, and hide the threads you need to use for pragmatic reasons.

The main reason to pass an explict `Executor` to `loop.run_in_executor` is to employ a `ProcessPoolExecutor` if the function to execute is CPU intensive, so that it runs in a different Python process, avoiding contention for the GIL. Because of the high start-up cost, it would be better to start the `ProcessPoolExecutor` in the `supervisor`, and pass it to the coroutines that need to use it.

## Writing asyncio Server

- We will implement an `echo` server whihc allows unicode serar utilities. First using HTTP with FastAPI, then using plain TCP with `asyncio` only

````python
from pathlib import Path
from unicodedata import name

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from charindex import InvertedIndex

STATIC_PATH = Path(__file__).parent.absolute() / 'static' # overload / operator by pathlib

app = FastAPI( # ASGI app
    title='Mojifinder Web',
    description='Search for Unicode characters by name.',
)

class CharName(BaseModel): # A pydantic schema for JOSN Response with char and name fields
    char: str
    name: str

def init(app): # build the index and load static HTML form
    app.state.index = InvertedIndex()
    app.state.form = (STATIC_PATH / 'form.html').read_text()

init(app) # run init

@app.get('/search', response_model=list[CharName])
async def search(q: str): # fast api assumes that any parameter not in the route path will be passed in the HTTP query string
    chars = sorted(app.state.index.search(q))
    return ({'char': c, 'name': name(c)} for c in chars) # return list of iterables of dicts

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def form(): # regular function can be used to produce responses
    return app.state.form

# no main funcion  10
````

- *FastAPI* is built on the *Starlette* ASGI toolkit, which in turn uses `asyncio`.

### An asyncio TCP Server

````python
async def supervisor(index: InvertedIndex, host: str, port: int) -> None:
    server = await asyncio.start_server( # gets an instance of asyncio.Server (TCP socket server)
        functools.partial(finder, index), # client_connected_cb, a callback to run when a client connects, call back can be function or coroutine that accepts two args asyncio.StreamReader and asyncio.StreamWriter, however our finder coroutine also gets an index, so we use partial to bind that parameter and obtain a callable that takes reader and writer.
        host, port)

    socket_list = cast(tuple[TransportSocket, ...], server.sockets) # cast is needed because typeshed has an outdated type hint for sockets property of Server class
    addr = socket_list[0].getsockname()
    print(f'Serving on {addr}. Hit CTRL-C to stop.')
    await server.serve_forever() # server forever

def main(host: str = '127.0.0.1', port_arg: str = '2323'):
    port = int(port_arg)
    print('Building index.')
    index = InvertedIndex()
    try:
        asyncio.run(supervisor(index, host, port)) # start event loop supervisor
    except KeyboardInterrupt: # interrupt to shut down
        print('\nServer shut down.')

if __name__ == '__main__':
    main(*sys.argv[1:])
````

````python
# rest of the implementation
import asyncio
import functools
import sys
from asyncio.trsock import TransportSocket
from typing import cast

from charindex import InvertedIndex, format_results

CRLF = b'\r\n'
PROMPT = b'?> '

async def finder(index: InvertedIndex,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter) -> None:
    client = writer.get_extra_info('peername') # remote client name
    while True:  4
        writer.write(PROMPT)  # can't await! this line sends ?> prompt
        await writer.drain()  # must await! # its a coroutine so drive using await
        data = await reader.readline() # coroutine that returns bytes
        if not data:
            break
        try:
            query = data.decode().strip()
        except UnicodeDecodeError: # can happend when user hits Ctrl-C and telnet client sends control bytes. replace query with null character
            query = '\x00'
        print(f' From {client}: {query!r}') # log
        if query:
            if ord(query[:1]) < 32:
                break
            results = await search(query, index, writer)
            print(f'   To {client}: {results} results.')

    writer.close() # Close stream
    await writer.wait_closed() # wait for it to close
    print(f'Close {client}.') # log end of client's session to server console
````

````python
# search 
async def search(query: str, # must be coroutine
                 index: InvertedIndex,
                 writer: asyncio.StreamWriter) -> int:
    chars = index.search(query) # query inverted index
    lines = (line.encode() + CRLF for line # generator expression yields byte string encoded in UTF-8 with actual unicode code point
                in format_results(chars))
    writer.writelines(lines) # send the lines
    await writer.drain() # drain
    status_line = f'{"─" * 66} {len(chars)} found' # build status and send
    writer.write(status_line.encode() + CRLF)
    await writer.drain()
    return len(chars)
````

## Asynchronous Iteration and Asynchronous Iterables



## Async Beyond asyncio: Curio

Python’s `async/await` language constructs are not tied to any specific event loop or library. Thanks to the extensible API provided by special methods anyone can write their own asynchronous runtime environment and framework to drive native coroutines, asynchronous generators, etc.

That’s what David Beazily did in his `Curio` project. *Curio* has a cleaner API and a simpler implementation, compared to `asyncio`

````python
#!/usr/bin/env python3
from curio import run, TaskGroup
import curio.socket as socket
from keyword import kwlist

MAX_KEYWORD_LEN = 4


async def probe(domain: str) -> tuple[str, bool]: # no need to get event lop
    try:
        await socket.getaddrinfo(domain, None) # top level function of curio.socket, not a event loop object
    except socket.gaierror:
        return (domain, False)
    return (domain, True)

async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f'{name}.dev'.lower() for name in names)
    async with TaskGroup() as group: # TaskGroup is a core concept in Curio, to monitor and control several coroutines, and to make sure they are all executed and cleaned up
        for domain in domains:
            await group.spawn(probe, domain) # start a coroutines
        async for task in group: # this yields over a TaskGroup yielding Task instance as they are completed
            domain, found = task.result
            mark = '+' if found else ' '
            print(f'{mark} {domain}')

if __name__ == '__main__':
    run(main())
````

## Type Hinting Asynchronous Objects

- return type of a native coroutine describes what you get when you `await` on that coroutine, which is type of the object that appears in the `return` statement in the body of the native coroutine function.

````python
async def probe(domain: str) -> tuple[str, bool]:
    try:
        await socket.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)
````

- If you need to annotate a parameter that takes a coroutine object, then generic type is

````python
class typing.Coroutine(Awaitable[V_co], Generic[T_co, T_contra, V_co]):
  
# python 3.5/3.6+
class typing.AsyncContextManager(Generic[T_co]):
    ...
class typing.AsyncIterable(Generic[T_co]):
    ...
class typing.AsyncIterator(AsyncIterable[T_co]):
    ...
class typing.AsyncGenerator(AsyncIterator[T_co], Generic[T_co, T_contra]):
    ...
class typing.Awaitable(Generic[T_co]):
    ...
````

With python 3.9+, use `collection.abc` equivalents of these. Three important aspect of generics

- If a formal type parameter defines a type for data that comes out of the object, it can be covariant.
- If a formal type parameter defines a type for data that goes into the object after its initial construction, it can be contravariant.
- AsyncGenerator has no return type, in contrast with typing.Generator. Returning a value by raising StopIteration(value) was one of the hacks that enabled generators to operate as coroutines and support yield from, as we saw in “Classic Coroutines”. There is no such overlap among the asynchronous objects: AsyncGenerator objects don’t return values, and are completely separate from native coroutine objects, which are annotated with typing.Coroutine.

## How Async Works and How It doesn’t

### Running Circle Around Blocking Calls

Ryan Dahl (Nodejs), introduces philosophy of his project by saying : We’re doing I/O completely wrong, defining a blocking function as one that does file or network I/O, and argues we can’t treat them as we treat non blocking function.

### The Myth of I/O Bound Systems

A common repeated meme is that asynchronous programming is good for `I/O bound systems`. There are no I/O bound systems. You may have I/O bound functions.

Given that any nontrivial system will have CPU-bound functions, dealing with them is the key to success in asynchronous programming

### Avoiding CPU-Bound Traps

- If you are using Python at scale, you should have some automated tests designed specially to detect performance regression as soon as they appear. This is critically important with asynchronous code, but also relevant to threaded Python code, because of GIL. If you wait until the slowdown starts bothering the development team, it’s too late. The fix will probably require some major makeover.

Here are some options for when you identify a CPU-hogging bottleneck

- Delegate the task to a Python process pool
- Delegate the task to an external task queue
- Rewrite relevant code in Cython, C, Rust or some other language that compiles to machine code and interfaces with Python/C API, preferably, releasing GIL
- Decide taht you can afford the performance hit and do nothing but record the decision to make it easier to revert to it later.

---

## File: python/ch5_22.md

# Dynamic Attributes and Properties

- Data Attributes and methods are collectively called as *attributes* in python. Methods are just callable attributes.
- *Dynamic attributes* present same interface as data attributes but are computed on demand following Bertrand Meyer’s Uniform Access Principle.

## Data Wrangling with Dynamic Attributes

- given following JSON Record

````python
{ "Schedule":
  { "conferences": [{"serial": 115 }],
    "events": [
      { "serial": 34505,
        "name": "Why Schools Don´t Use Open Source to Teach Programming",
        "venue_serial": 1462,
        "description": "Aside from the fact that high school programming...",
        "speakers": [157509],
        "categories": ["Education"] }
    ],
    "speakers": [
      { "serial": 157509,
        "name": "Robert Lefkowitz"
      }
    ],
    "venues": [
      { "serial": 1462,
        "name": "F151",
        "category": "Conference Venues" }
    ]
  }
}
````

````python
import json
with open('data/osconfedd.json') as fp:
  feed = json.load(fp)

sorted(feed['Schedule'].keys())
# Output : ['conferences', 'events', 'speakers', 'venues']
feed['Schedule']['speakers'][-1]['name']	# syntax is bad
# Output : 'Carina C. Zona'
````

- above syntax is cumbersome. In JS, we could get the data using `feed.Schedule.events[40].name`. It’s easy to implement a `dict` like class that does similar in python

- There are many ways to do this, with our `FrozenSet` its quite simple

````python
import json
raw_feed = json.load(open('data/osconfeed.json'))
feed = FrozenJSON(raw_feed)
len(feed.Schedule.speakers)
````

````python
from collections import abc

class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
       using attribute notation
    """

    def __init__(self, mapping):
        self.__data = dict(mapping) # make dict from mapping arg

    def __getattr__(self, name): # its called only when there's no attribute with name
        try:
            return getattr(self.__data, name) # nested search
        except AttributeError:
            return FrozenJSON.build(self.__data[name]) # raise error

    def __dir__(self): # supports dir() built-in, supporting auto-completion
        return self.__data.keys()

    @classmethod
    def build(cls, obj): # alternate constructor
        if isinstance(obj, abc.Mapping): # if obj is mapping build frozenjson
            return cls(obj)	# nested jsons
        elif isinstance(obj, abc.MutableSequence): # it must be a list
            return [cls.build(item) for item in obj]	# recursively pass each item to obj recursively
        else: # not a dict or a list return item
            return obj
````

- NOTE: `FrozenJSON` instance has `__data` private instance attributes stored under `_FrozenJSON__data`. Attempts to access this triggers `__getattr__`

### The Invalid Attribute Name Problem

`FrozenJSON` doesn’t support Python keywords as attributes name.

````python
student = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
student.class # invalid syntax error

# but this words
getattr(student, 'class')
````

- A solution is to check whether key in the mapping given to `FrozenJSON.__init__	` is a keyword, and if so, append `_` to it, so the attribute can be read like `student.class_`

````python
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value
````

### Flexible Object Creation with `__new__`

- `__init__` is referred as constructor because of adopted jargon from other languages. NOTE: how `__init__` is called with `self` meaning it has already been initialised. Also `__init__` cannot return anything, so its really initialiser, not a constructor.
- python actually calls `__new__` to create a new instance. Its a class method but gets special treatment, so the `@classmethod` decorator is not applied to it. Python takes the instance returns by `__new__` and then passes it as the first argument of `self` of `__init__`.
- If necessary, the `__new__` method can also return an instance of a different class when that happends interpretor doesn’t call `__init__`

````python
# pseudocode for object construction
def make(the_class, some_arg):
    new_object = the_class.__new__(some_arg)
    if isinstance(new_object, the_class):
        the_class.__init__(new_object, some_arg)
    return new_object

# the following statements are roughly equivalent
x = Foo('bar')
x = make(Foo, 'bar')
````

````python
from collections import abc
import keyword

class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
       using attribute notation
    """

    def __new__(cls, arg): # passing class here
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls) # default behaviour is to delegate to __new__ of a superclass
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        try:
            return getattr(self.__data, name)
        except AttributeError:
            return FrozenJSON(self.__data[name])

    def __dir__(self):
        return self.__data.keys()
````

## Computed Properties

We have used `@property` decorator used to make attributes read-only.

````python
{ "serial": 33950,	# here this is linked to venue and speakers db
  "name": "There *Will* Be Bugs",
  "event_type": "40-minute conference session",
  "time_start": "2014-07-23 14:30:00",
  "time_stop": "2014-07-23 15:10:00",
  "venue_serial": 1449,
  "description": "If you're pushing the envelope of programming...",
  "website_url": "http://oscon.com/oscon2014/public/schedule/detail/33950",
  "speakers": [3471, 5199],
  "categories": ["Python"] }
````

- We will implement a Event class with `venue` and `speaker` properties to return the linked data automatically. (dereferencing the serial number)

### 1. Data Driven Attribute Creations

- fields from the original JSON can be retrieved as `Record` instance attributes

````python
import json

JSON_PATH = 'data/osconfeed.json'

class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs) # shortcut to build an instance with attributes created from keyword arguments

    def __repr__(self):
        return f'<{self.__class__.__name__} serial={self.serial!r}>' # using serial field to build custom Record Representation

def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp) # parse json
    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1] # list name without last char (remove s from suffixes)
        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}' # Events.some_val
            records[key] = Record(**raw_record) # create record objects
    return records
````

- This is much better than previous recursive FrozenJSON implementation.

### 2. Property to Retrieve Linked Record

- The goal of this next version is: given an `event` record, reading its `venue` property will return a `Record`

````python
event = Record.fetch('event.33950')	# instance of Event class
event	# There will be Bugs
event.venue	# <Record serial=1449> # returns a Record instance
event.venue.name # Portland 251
````

- `Event` is a subclass of `Record` adding a `venue` to retrieve linked records, and a specialized `__repr__` method.

````python
# Record Class
import inspect # used for load
import json

JSON_PATH = 'data/osconfeed.json'

class Record:

    __index = None # private class attribute eventually holding reference to dict returned by load

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

    @staticmethod # static method
    def fetch(key):
        if Record.__index is None: # populate the Record.__index if necessary
            Record.__index = load()
        return Record.__index[key]
````

````python
 # Event Class
class Event(Record): # Event extends Record

    def __repr__(self):
        try:
            return f'<{self.__class__.__name__} {self.name!r}>' # if instance has a name attribute it is used to produce a custom representation or else delegate to `__repr__` from Record
        except AttributeError:
            return super().__repr__()

    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key) # build a key from venue.serial_num
````

````python
# load function
def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)
    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, Record) # search for class based on key name like Event
        if inspect.isclass(cls) and issubclass(cls, Record): # check if subclass of Record
            factory = cls # bind factory name to new class
        else:
            factory = Record # or bind to Record
        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record) # store the record and store in records which is contructed by factory
    return records
````

### 3. Property Overriding an Existing Attribute

````python
    @property
    def speakers(self):
        spkr_serials = self.__dict__['speakers'] # directly retrieve from __dict__
        fetch = self.__class__.fetch
        return [fetch(f'speaker.{key}')
                for key in spkr_serials] # return list of all records with key corresponding to the numbers in spkr_serials
````

### 4. Bespoke Property Cache

- Caching property is a common need because there is an expectation that expression like `event.venue` should be inexpensive.
- The handmade caching is straightforward, but creating an attribute after the instance is initialized defeats the PEP 412—Key-Sharing Dictionary optimization, as explained in “Practical Consequences of How dict Works”. Depending on the size of the dataset, the difference in memory usage may be important.

````python
class Event(Record):

    def __init__(self, **kwargs):
        self.__speaker_objs = None	# code this to quikly check if speakers are there or not
        super().__init__(**kwargs)

# 15 lines omitted...
    @property
    def speakers(self):
        if self.__speaker_objs is None:
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch
            self.__speaker_objs = [fetch(f'speaker.{key}')
                    for key in spkr_serials]
        return self.__speaker_objs
````

### 5. Caching using functools

````python
    @cached_property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)
````

- The `@cached_property` decorator does not create a full-fledged property, it creates a *nonoverriding descriptor*. A descriptor is an object that manages the access to an attribute in another class.
- differences between `cached_property` and `property` from a user’s point of view.
  - The mechanics of `cached_property()` are somewhat different from `property()`. A regular property blocks attribute writes unless a setter is defined. In contrast, a `cached_property` allows writes.
  - The `cached_property` decorator only runs on lookups and only when an attribute of the same name doesn’t exist. When it does run, the `cached_property` writes to the attribute with the same name. Subsequent attribute reads and writes take precedence over the `cached_property` method and it works like a normal attribute.
  - The cached value can be cleared by deleting the attribute. This allows the `cached_property` method to run again

`@cached_property` has some important limitations:

- It cannot be used as a drop-in replacement to `@property` if the decorated method already depends on an instance attribute with the same name.
- It cannot be used in a class that defines `__slots__`.
- It defeats the key-sharing optimization of the instance `__dict__`, because it creates an instance attribute after `__init__`.

Despite this `@cached_property` addresses a common need in a simple way and it is thread-safe. Alternate solution that we can use with speaker is to stack `@property` and `@cache` decorators

````python
  	@property # note this order is important speaker= property(cache(speaker))
    @cache
    def speakers(self):
        spkr_serials = self.__dict__['speakers']
        fetch = self.__class__.fetch
        return [fetch(f'speaker.{key}')
                for key in spkr_serials]
````

## Using a Property for Attribute Validation

- Besides computing attribute values, properties are also used to enforce business rules by changing a public attribute into a protected attribute by getter and setter.

### LineItem Take #1: Class for an Item in an Order

````python
class LineItem:
  def __init__(self, desc, weight, price):
    self.description = desc
    self.weight = weight
    self.price = price
  
  def subtotal(self):
    return self.weight * self.price
````

````python
raisins = LineItem('Golden raisins', 10, 6.95)
raisins.subtotal()
# Output : 69.5
raisins.weight = -20  # garbage in...
raisins.subtotal()    # garbage out...
# Output : -139.0
````

### LineItem Take #2: A Validating Property

````python
class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property  # decorate getter
    def weight(self):
        return self.__weight # actual value stored in __weight

    @weight.setter # setter property
    def weight(self, value):
        if value > 0:
            self.__weight = value # only update property when val > 0
        else:
            raise ValueError('value must be > 0') 
````

## A proper look at Properties

- Although often used as a decorator, the `property` built-in is actually a class.
- In Python, functions and classes are often interchangeable, because both are callable and there is no `new` operator for object instantiation, so invoking a constructor is no  different from invoking a factory function. And both can be used as  decorators, as long as they return a new callable that is a suitable  replacement of the decorated callable.

````python
# property signature
property(fget=None, fset=None, fdel=None, doc=None)
````

- A much simpler approach compared with decorator is creating `set_weight` and `get_weight` functions and then defining class attribute `weight = property(get_weight, set_weight)`

### Properties Override Instance Attributes

- Properties are always class attributes, but they actually manage attribute access in the instance of the class.
- Instance attributes shadow same named class attributes.

````python
class Class:
  data = 'the class data attr'
  
  @property
  def prop(self):
    return 'the prop value'
obj = Class()
vars(obj)	# {}
obj.data	# 'the class data attr'
obj.data = 'bar' # shadow by instance attributes
vars(obj)	# {'data': 'bar'}
obj.data	# Output : 'bar'
Class.data	# 'the class data attr'

# let's try to shadow class property
New class property shadows the existing instance attribute

Class.prop	# <property object ...>
obj.prop	# 'the prop value'
obj.prop = 'foo'	# AttributeError becuase directly executes property getter
# lets modify the object data dict
obj.__dict__['prop'] = 'foo'
vars(obj)	# {'data': 'bar', 'prop':'foo'}	# this prop is instance attribute
obj.prop	# 'the prop value'	# this still runs property getter, so its not shadowed
Class.prop = 'baz'	# class property destroyed, now its class attribute
obj.prop	# 'foo'	# shadow now works, obj.prop retrieves the instance attribute

# New class property shadows the existing instance attribute

obj.data	# 'bar'
Class.data	# the class data attr
Class.data = property(lambda self: 'the data prop value')
obj.data	# property is called, instance attribute is shadowed
del Class.data
obj.data	# 'bar'
````

- The main point of this section is that an expression like `obj.data` does not start the search for `data` in `obj`. The search actually starts at `obj.__class__`, and only if there is no property named `data` in the class, Python looks in the `obj` instance itself.

### Property Documentation

When tools such as the console `help()` function or IDEs need to display the documentation of a property, they extract the information from the `__doc__` attribute of the property.

If used with the classic call syntax, `property` can get the documentation string as the `doc` argument:

```
    weight = property(get_weight, set_weight, doc='weight in kilograms')
```

```python
# Documentation Example
class Foo:

    @property
    def bar(self):
        """The bar attribute"""
        return self.__dict__['bar']

    @bar.setter
    def bar(self, value):
        self.__dict__['bar'] = value
```

## Coding a Property Factory

We will create a factory to create `quantity` properties - so named because the managed attributes represent quantities that can’t be negative or zero in the application.

````python
class LineItem:
    weight = quantity('weight') # factory calls
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight	# here the property works automatically
        self.price = price

    def subtotal(self):
        return self.weight * self.price
````

````python
def quantity(storage_name): # where data for each property is stored like 'weight' or 'price'

    def qty_getter(instance): # getter
        return instance.__dict__[storage_name] # return the property

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter) # return the property
````

## Handling Attribute Deletion

- We can not only delete variables but attributes as well using `del`
- In practice, deleting attributes is not something we do every day in Python, and the requirement to handle it with a property is even more unusual.

## Essential Attributes and Function for Attributes Handling

### Special Attributes that Affect Attribute Handling

- `__class__` : A reference to the object’s class. Python looks for special methods such as `__getattr__` only in an object’s class and not in the instance themselves.
- `__dict__`: A mapping that stores the writeable attributes of an object or class. An object that has a `__dict__` can have arbitrary new attributes set at any time. If a class has a `__slots__` attribute, then its instances may not have a `__dict__`.
- `__slots__` : An attribute that may be defined in a class to save memory. `__slots__` is a `tuple` of strings naming the allowed attributes

### Built-in Functions for Attribute Handling

- `dir([object])` : lists most attributes of the object. The official docs say dir is intended for interactive use so it does not provide a comprehensive list of attributes, but an “interesting” set of names. dir can inspect objects implemented with or without a __dict__. The __dict__ attribute itself is not listed by dir, but the __dict__ keys are listed. Several special attributes of classes, such as __mro__, __bases__, and __name__, are not listed by dir either.
- `getattr(object, name[, default])` : Gets the attribute identified by the `name` string from the `object`. The main use case is to retrieve attributes (or methods) whose names we don’t know beforehand. This may fetch an attribute from the object’s class or from a superclass.
- `hasattr(object, name)` : Returns `True` if the named attribute exists in the `object`, or can be somehow fetched through it (by inheritance, for example).
- `setattr(object, name, value)` : Assigns the `value` to the named attribute of `object`, if the `object` allows it. This may create a new attribute or overwrite an existing one.
- `vars([object])` : Returns the `__dict__` of `object`; `vars` can’t deal with instances of classes that define `__slots__` and don’t have a `__dict__` (contrast with `dir`, which handles such instances). Without an argument, `vars()` does the same as `locals()`: returns a `dict` representing the local scope.

### Special Methods for Attribute Handling

- `__delattr__(self, name)` : Always called when there is an attempt to delete an attribute using the `del` statement;
- `__dir__(self)` : Called when `dir` is invoked on the object, to provide a listing of attributes; `dir(obj)` triggers `Class.__dir__(obj)`. Also used by tab-completion in all modern Python consoles.
- `__getattr__(self, name)` : Called only when an attempt to retrieve the named attribute fails, after the `obj`, `Class`, and its superclasses are searched. The expressions `obj.no_such_attr`, `getattr(obj, 'no_such_attr')`, and `hasattr(obj, 'no_such_attr')` may trigger `Class.__getattr__(obj, 'no_such_attr')`, but only if an attribute by that name cannot be found in `obj` or in `Class` and its superclasses.
- `__getattribute__(self, name)` : Always called when there is an attempt to retrieve the named attribute  directly from Python code (the interpreter may bypass this in some  cases, for example, to get the `__repr__` method). Dot notation and the `getattr` and `hasattr` built-ins trigger this method.
- `__setattr__(self, name, value)` : Always called when there is an attempt to set the named attribute. Dot notation and the `setattr` built-in trigger this method


---

## File: python/ch5_23.md

# Attribute Descriptors

- Descriptors are a way of reusing the same access logic in multiple attributes. i.e. field types in ORMs, such as Django ORM and SQLAlchemy are descriptors managing flow of data from fields in database record to Python object attributes and vice-versa.
- A descriptor is a class that implements a dynamic protocol consisting of the `__get__`, `__set__`, and `__delete__` methods. The `property` class implements the full descriptor protocol. As usual with dynamic  protocols, partial implementations are OK. In fact, most descriptors we  see in real code implement only `__get__` and `__set__`, and many implement only one of these methods.
- User-defined functions are descriptors. We’ll see how the descriptor  protocol allows methods to operate as bound or unbound methods,  depending on how they are called.

## Descriptor Example: Attribute Validation

- we saw previously how property factory helps us avoid repititive coding of getters and setters by applying funcional programming patterns. A property factory is a higher-order function that creates a parameterized set of accessor function and builds custom property instance from them, with closures to hold settings like `storage_name`
- Let’s code `quantity` property factory into a `Quantity` descriptor class

### LineItem Take #3: A simple descriptor

- a class implementing `__get__`, a `__set__` or a `__delete__` method is a descriptor. We can use it by declaring instances of it as class attributes for another class.

![UML class diagram for `Quantity` and `LineItem`](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_2301.png)

- NOTE: there are two instance of `weight` one is class attribute of `LineItem` and another instance attribute that will exist in each `LineItem` object.
- Important Terms :
  - Descriptor class : A class implementing the descriptor protocol. 
  - Managed Class: class where descriptor isntances are declared as class attributes
  - Descriptor Instance: each instance of descriptor is class attribute of the managed class
  - Managed instance : one of the instance of managed class
  - Storage attribute: an attribute of managed class that holds the value of managed attribute for that particular instance
  - managed attribute: a public attribute in the managed class that is handled by a descriptor instance with values stored in storage attributes.



````python
class Quantity: # its a protocol based feature- no subclassing is needed

    def __init__(self, storage_name):
        self.storage_name = storage_name # each quantity instance will have storage_name attribute

    def __set__(self, instance, value): # instance here is managed instance
        if value > 0:
            instance.__dict__[self.storage_name] = value # update managed instance
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

    def __get__(self, instance, owner):  # need to implement this because name of managed attribute may not be same as storage_name
        return instance.__dict__[self.storage_name]
````

- `__get__` is important to implement as see :

````python
class House:
    rooms = Quantity('number_of_rooms')	# the managed attribute is rooms, but the storage attribute is number_of_rooms
````

````python
class LineItem:
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):  # rest of body is simple and clean as the original code.
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
````

- It’s important to realize that `Quantity` instances are class attributes of `LineItem`

### LineItem Take #4: Automatic Naming of Storage Attributes

- To avoid retyping the attribute name in the descriptor instances, we’ll implement `__set_name__` to set the `storage_name` of each `Quantity` instance. The `__set_name__` special method was added to the descriptor protocol in Python 3.6. The interpreter calls `__set_name__` on each descriptor it finds in a `class` body—if the descriptor implements it.

````python
class Quantity:

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

    # no __get__ needed # because of __set_name__ property both have same name

class LineItem:
    weight = Quantity() # no need to pass managed attribute name to Quantity constructor
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
````

- Following code better represents the typical usage of a descriptor

````python
import model_v4c as model # we import it as model


class LineItem:
    weight = model.Quantity() # Doesn't this looks like Django model fields :)
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
````

### LineItem Take #5: A New Descriptor Type

The imaginary organic food store hits a snag: somehow a line item  instance was created with a blank description, and the order could not  be fulfilled. To prevent that, we’ll create a new descriptor, `NonBlank`. As we design `NonBlank`, we realize it will be very much like the `Quantity` descriptor, except for the validation logic.

This prompts a refactoring, producing `Validated`, an abstract class that overrides the `__set__` method, calling a `validate` method that must be implemented by subclasses.

````python
import abc

class Validated(abc.ABC):

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        value = self.validate(self.storage_name, value)
        instance.__dict__[self.storage_name] = value

    @abc.abstractmethod
    def validate(self, name, value):  3
        """return validated value or raise ValueError"""
      
# Quantity Class
class Quantity(Validated):
    """a number greater than zero"""

    def validate(self, name, value):
        if value <= 0:
            raise ValueError(f'{name} must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validate(self, name, value):
        value = value.strip()
        if not value:
            raise ValueError(f'{name} cannot be blank')
        return value 
````

````python
# usage
class LineItem:
    description = model.NonBlank() # using our new descriptor
    weight = model.Quantity()
    price = model.Quantity()
````

## Overriding Versus Nonoverriding Descriptors

NOTE: there is an important asymmetry in the way python handles attributes : 

- Reading an attribute through an instance normally returns the attribute defined in the instance, but if there is no such attribute in the instance, a class attribute is retrieved.
- Assigning to an attribute in an instance normally creates the attribute in the instance without affecting class at all.

This asymmetry also affects descriptors as well, creating two categories of Descriptors

- Overriding Descriptor : `__set__` is present
- Non-Overriding Descriptor: `__set__` is not present.

Regardless of whether a descriptor is overriding or not, it can be overwritten by assignment to the class. This is a monkey-patching technique

## Methods are Descriptors

A function within a class becomes a bound method when invoked on an instance because all user-defined functions have a `__get__` method, therefore they operate as descriptors when attached to a class. A method is a nonoverriding descriptor.

`obj.spam` and `Managed.spam` retrieve different objects. As usual with descriptors, the `__get__` of a function returns a reference to itself when the access happens  through the managed class. But when the access goes through an instance, the `__get__` of the function returns a bound method object: a callable that wraps the function and binds the managed instance (e.g., `obj`) to the first argument of the function (i.e., `self`), like the `functools.partial` function does

## Descriptor Usage Tips

- Use `property` to keep it simple

  The `property` built-in creates overriding descriptors implementing `__set__` and `__get__` even if you do not define a setter method.

- Read-only descriptors require `__set__`

  If you use a descriptor class to implement a read-only attribute, you must remember to code both `__get__` and `__set__`, otherwise setting a namesake attribute on an instance will shadow the descriptor.

- Validation descriptors can work with `__set__` only

  In a descriptor designed only for validation, the `__set__` method should check the `value` argument it gets, and if valid, set it directly in the instance `__dict__` using the descriptor instance name as key. That way, reading the  attribute with the same name from the instance will be as fast as  possible, because it will not require a `__get__`.

- Caching can be done efficiently with `__get__` only

  If you code just the `__get__` method, you have a  nonoverriding descriptor. These are useful to make some expensive computation and then cache the  result by setting an attribute by the same name on the instance. The namesake instance attribute will shadow the descriptor, so subsequent access to that attribute will fetch it directly from the instance `__dict__` and not trigger the descriptor `__get__` anymore. The `@functools.cached_property` decorator actually produces a nonoverriding descriptor.

- Nonspecial methods can be shadowed by instance attributes

  Because functions and methods only implement `__get__`, they are nonoverriding descriptors. A simple assignment like `my_obj.the_method = 7` means that further access to `the_method` through that instance will retrieve the number `7`—without affecting the class or other instances. However, this issue does not  interfere with special methods. The interpreter only looks for special  methods in the class itself, in other words, `repr(x)` is executed as `x.__class__.__repr__(x)`, so a `__repr__` attribute defined in `x` has no effect on `repr(x)`. For the same reason, the existence of an attribute named `__getattr__` in an instance will not subvert the usual attribute access algorithm.

## Descriptor Docstring and Overriding Deletion

- The docstring of a descriptor class is used to document every instance of the descriptor in the managed class.
- That is somewhat unsatisfactory. In the case of `LineItem`, it would be good to add, for example, the information that `weight` must be in kilograms. That would be trivial with properties, because  each property handles a specific managed attribute. But with  descriptors, the same `Quantity` descriptor class is used for `weight` and `price`
- The second detail we discussed with properties, but have not addressed  with descriptors, is handling attempts to delete a managed attribute. That can be done by implementing a `__delete__` method alongside or instead of the usual `__get__` and/or `__set__` in the descriptor class.

---

## File: python/ch5_24.md

# Class Metaprogramming

Everyone knows that debugging is twice as hard as writing a program in the first place.        So if you’re as clever as you can be when you write it, how will you ever debug it? - Brian W. Kernighan and PJ Plauger, The Elements of Programming Style

- Class metaprogramming is the art of creating or customizing classes at runtime.
- Classes are first-class objects in Python, so a function can be used to create a new class at any time, without `class` keyword.
- Class decorators are functions, but designed to inspect, change and even replace the decorated class with another class.
- Metaclasses are most advanced tool for class metaprogramming : they let you create whole new categories of classes with special traits such as abstract base classes.
- Metaclasses are powerful, but hard to justify and even harder to get right. Class decorators solve many of the same problems and are easier to understand.

## Classes as Objects

- classes are `objects` in python. Every class has a number of attributes defined in the Python Data Model. Three of those attributes appeared several times in this book already : `__class__`, `__name__`, and `__mro__`. Other class attributes are :

- `cls.__bases__` : tuple of base classes of the class

- `cls.__qualname__` : The qualified name of a class or function which is a dotted path from global scope of the module to the class definition.

- `cls.__subclasses__()` : This method returns a list of immediate subclasses of the class. The implementation uses weak references to avoid circular references between the superclass and its subclasses - which hold a strong reference to the superclasses in their `__bases__` attribute.

  NOTE: The method lists subclasses currently in memory. Subclasses in modules not yet imported will not appear in the result.

- `cls.mro()` : The interpreter calls this method when building a class to obtain the tuple of superclasses stored in the `__mro__` attribute of the class. A metaclass can override this method to customize the method resolution order of the class under construction.

*None of the attributes mentioned in this section are listed by the `dir(…)` function.*

## type: The Built-in Class Factory

- We usually think `type` returns the class of the object, because thats what `type(my_object)` does : it returns `my_object.__class__`
- `type` is a class that creates a new class when invoked with three arguments

````python
class MyClass(MySuperClass, MyMixin):
  x = 42
  def x2(self):
    return self.x * 2
````

- Using `type` constructor we can create `MyClass` at runtime with this code:

````python
MyClass = type('MyClass',
               (MySuperClass, MyMixin),
               {'x': 42, 'x2': lambda self: self.x * 2},
          )
````

- when Python read `class` statement it calls, type to build the class object with these parameters. `name` (MyClass), `bases` (tuple of superclasses) and `dict` (mapping of attribute names to values. Callable become methods)
- The `type` class is a metaclass : a class that builds classes. instance of `type` class are classes.

## A Class Factory Function

- Standard library has a class factory function that appears several times in book : `collections.namedtuple`, we also saw `typing.NamedTuple` and `@dataclass`
- a super simple factory for classes of mutable objects - the simplest replacement for `@dataclass`

````python
class Dog:
  def __init__(self, name, weight, owner):
    self.name = name
    self.weight = weight
    self.owner = owner
````

- Above boilplate is repititive (appears 3 times), and that doesn’t even buy us a nice `repr`

````python
rex = Dog('Rex', 30, 'Bob')
rex
# <__main__.Dog object at 0x2865..>
````

- Let’s create a record_factory that simplifies this

````python
Dog = record_factory('Dog','name weight owner')
rex = Dog('Rex', 30, 'Bob')
rex
# Dog(name='Rex', weight=30, owner='Bob')
name, weight, _ = rex
rex.weight = 32
rex
# Dog(name='Rex', weight=32, owner='Bob')
Dog.__mro__
# (<class 'factories.Dog'>, <class 'object'>)
````

The code for `record_factory` :

````python
from typing import Union, Any
from collections.abc import Iterable, Iterator

FieldNames = Union[str, Iterable[str]] # single string or list of string

def record_factory(cls_name: str, field_names: FieldNames) -> type[tuple]: # first two of collections.namedtuple; return a type

    slots = parse_identifiers(field_names) # build a tuple of attribute names

    def __init__(self, *args, **kwargs) -> None: # build tuple from slots and args
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self) -> Iterator[Any]: # return iterators
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self): # representation
        values = ', '.join(f'{name}={value!r}'
            for name, value in zip(self.__slots__, self))
        cls_name = self.__class__.__name__
        return f'{cls_name}({values})'

    cls_attrs = dict(  # assemble a dictionary of class attributes
        __slots__=slots,
        __init__=__init__,
        __iter__=__iter__,
        __repr__=__repr__,
    )

    return type(cls_name, (object,), cls_attrs) # return and build class, type constructor


def parse_identifiers(names: FieldNames) -> tuple[str, ...]:
    if isinstance(names, str):
        names = names.replace(',', ' ').split() # convert names separated by spaces or commas to list of str
    if not all(s.isidentifier() for s in names):
        raise ValueError('names must all be valid identifiers')
    return tuple(names)
````

## Introducing `__init_subclass__`

- Both `__initsubclass__` and `__set_name__` (prev chap) came out in PEP487-Simple customization of class creation. 
- We could use both `typing.NamedTuple` and `@dataclass` to let programmers used class statement to specify attributes for a new class, which is enhanced by the class builder with automatic addition of methods like `__init__`, `__repr__` , `__eq__` etc.
- Both these class builders read type hints in user’s class to enhance class. Those type hints to allow static type checkes to validate code that sets or gets those attributes. However `NamedTuple` and `@dataclass` doesn’t take advantage of type hints for attributes at runtimes. We will implement a Checked class that does

````python
from collections.abc import Callable  # Type hints on callable
from typing import Any, NoReturn, get_type_hints


class Field:	# descriptor
    def __init__(self, name: str, constructor: Callable) -> None: # minimum type hints and return type is Any
        if not callable(constructor) or constructor is type(None): # Minimal callable type hint
            raise TypeError(f'{name!r} type hint must be callable')
        self.name = name
        self.constructor = constructor

    def __set__(self, instance: Any, value: Any) -> None:
        if value is ...: # Checked.__init__ sets value as Ellipses we call the constructor with no arguments.
            value = self.constructor()
        else:
            try:
                value = self.constructor(value) # otherwise call with the value
            except (TypeError, ValueError) as e:
                type_name = self.constructor.__name__
                msg = f'{value!r} is not compatible with {self.name}:{type_name}'
                raise TypeError(msg) from e
        instance.__dict__[self.name] = value # store values in instance dictionary
        
class Checked:
    @classmethod
    def _fields(cls) -> dict[str, type]:
        return get_type_hints(cls)

    def __init_subclass__(subclass) -> None: # is called when subclass of the current class is defined
        super().__init_subclass__() # not strictly necessary but should handle classes that invoke .__init_subclass__()
        for name, constructor in subclass._fields().items(): # for each field name and constructor
            setattr(subclass, name, Field(name, constructor)) # create an attribute on subclass with that name bound to a Field descriptor parameterized with name and constructor

    def __init__(self, **kwargs: Any) -> None:
        for name in self._fields():
            value = kwargs.pop(name, ...) # for each field get value from kwargs and remove from kwargs, ... helps distinguish between arguments given the value None from arguments that wer not given.
            setattr(self, name, value)  # Calls Checked.__setattr__
        if kwargs: # if still items remaining in the kwargs, __init__ fails
            self.__flag_unknown_attrs(*kwargs)
    def __setattr__(self, name: str, value: Any) -> None: # intercepts all attempsts to set and instance attribute
        if name in self._fields(): # if attribute name is konw fetch corresponding descriptor
            cls = self.__class__
            descriptor = getattr(cls, name)
            descriptor.__set__(self, value) # we need it due to above comment
        else: # unknown attribute
            self.__flag_unknown_attrs(name)

    def __flag_unknown_attrs(self, *names: str) -> NoReturn: # rare use of NoReturn type to raise Attribute Error
        plural = 's' if len(names) > 1 else ''
        extra = ', '.join(f'{name!r}' for name in names)
        cls_name = repr(self.__class__.__name__)
        raise AttributeError(f'{cls_name} object has no attribute{plural} {extra}')

    def _asdict(self) -> dict[str, Any]: # create dict from the attributes of a Movie object
        return {
            name: getattr(self, name)
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, Field)
        }

    def __repr__(self) -> str: # implement nice __repr__
        kwargs = ', '.join(
            f'{key}={value!r}' for key, value in self._asdict().items()
        )
        return f'{self.__class__.__name__}({kwargs})'
````

````python
class Movie(Checked):
	title: str
  year: int
  box_office : float
  
  
movie = Movie(title='The Godfather', year=1972, box_office=137)
movie.title # The Godfather
movie # Movie(title='The Godfather', year=1972, box_office=137.0)

Movie(title="Life of Brian")
# Movie(title='Life of Brian', year=0, box_office=0.0)

# NOTE : How defaults are picked up based on type
# int(), float(), bool(), str(), list(), dict(), set()
# (0, 0.0, False, '', [], {}, set())

blockbuster = Movie(title='Avatar', year=2009, box_office='billions')
# TypeError: 'billions' is not compatible with box_office:float
````

### Why `__init_subclass__` Cannot configure `__slots__`

The `__slots__` attribute is only effective if it is one of the entries in the class namespace passed to `type.__new__`. Adding `__slots__` to an existing class has no effect. Python invokes `__init_subclass__` only after the class is built—by then it’s too late to configure `__slots__`. A class decorator can’t configure `__slots__` either, because it is applied even later than `__init_subclass__`.

To configure `__slots__` at runtime, your own code must build the class namespace passed as the last argument of `type.__new__`. To do that, you can write a class factory function, like *record_factory.py*, or you can take the nuclear option and implement a metaclass. We will see how to dynamically configure `__slots__` in “Metaclasses 101”.

## Enhancing Classes with a Class Decorator

A class decorator is a callable that behaves similarly to a function decorator.

Probably the most common reason to choose a class decorator over the simpler `__init_subclass__` is to avoid interfering with other class features, such as inheritance and metaclasses

````python
def checked(cls: type)-> type:
    for name, constructor in _fields(cls).items(): # _fields is a top-level function
        setattr(cls, name, Field(name, constructor)) # replace each attribute by Fields descriptor

    cls._fields = classmethod(_fields)  # type: ignore # build class method from _fields, add to decorated class.

    instance_methods = ( # module level functions that will become instance methods of decorated class.
        __init__,
        __repr__,
        __setattr__,
        _asdict,
        __flag_unknown_attrs,
    )
    for method in instance_methods: # add each instance methods
        setattr(cls, method.__name__, method)

    return cls
````

- Method’s to be injected in decorated class

````python
def _fields(cls: type) -> dict[str, type]:
    return get_type_hints(cls)

def __init__(self: Any, **kwargs: Any) -> None:
    for name in self._fields():
        value = kwargs.pop(name, ...)
        setattr(self, name, value)
    if kwargs:
        self.__flag_unknown_attrs(*kwargs)

def __setattr__(self: Any, name: str, value: Any) -> None:
    if name in self._fields():
        cls = self.__class__
        descriptor = getattr(cls, name)
        descriptor.__set__(self, value)
    else:
        self.__flag_unknown_attrs(name)

def __flag_unknown_attrs(self: Any, *names: str) -> NoReturn:
    plural = 's' if len(names) > 1 else ''
    extra = ', '.join(f'{name!r}' for name in names)
    cls_name = repr(self.__class__.__name__)
    raise AttributeError(f'{cls_name} has no attribute{plural} {extra}')

def _asdict(self: Any) -> dict[str, Any]:
    return {
        name: getattr(self, name)
        for name, attr in self.__class__.__dict__.items()
        if isinstance(attr, Field)
    }

def __repr__(self: Any) -> str:
    kwargs = ', '.join(
        f'{key}={value!r}' for key, value in self._asdict().items()
    )
    return f'{self.__class__.__name__}({kwargs})'
````

## What Happens when : Import Time vs Runtime

- Python programmers talk about `import time` vs `runtime`, but the terms are not strictly defined and there is gray area.
- At import time the interpreter:
  - Parses the source code of a *.py* module in one pass from top to bottom. This is when a `SyntaxError` may occur.
  - Compiles the bytecode to be executed.
  - Executes the top-level code of the compiled module.
- If there is an up-to-date *.pyc* file available in the local `__pycache__`, parsing and compiling are skipped because the bytecode is ready to run.
- parsing and compiling is “import time” activities while executable statements can potentially run and change state of program.
- In particular, the `import` statement is not merely a declaration, but it actually runs all the top-level code of a module when it is imported for the first time in the process. Further imports of same module will use a cache, and then the only effect will be binding the imported objects to names in the client module.
- the `import` statement can trigger all sorts of “runtime” behavior. Conversely, “import time” can also happen deep inside runtime, because the `import` statement and the `__import__()` built-in can be used inside any regular function.

### Evaluation Time Experiments

Consider an *evaldemo.py* script that uses a class decorator, a descriptor, and a class builder based on `__init_subclass__`, all defined in a *builderlib.py* module.

````python
print('@ builderlib module start')

class Builder:
    print('@ Builder body')

    def __init_subclass__(cls):
        print(f'@ Builder.__init_subclass__({cls!r})')

        def inner_0(self):
            print(f'@ SuperA.__init_subclass__:inner_0({self!r})')

        cls.method_a = inner_0

    def __init__(self):
        super().__init__()
        print(f'@ Builder.__init__({self!r})')


def deco(cls): # class decorator
    print(f'@ deco({cls!r})')

    def inner_1(self): # print the class
        print(f'@ deco:inner_1({self!r})')

    cls.method_b = inner_1
    return cls
  
class Descriptor:
    print('@ Descriptor body')

    def __init__(self):
        print(f'@ Descriptor.__init__({self!r})')

    def __set_name__(self, owner, name):
        args = (self, owner, name)
        print(f'@ Descriptor.__set_name__{args!r}')

    def __set__(self, instance, value):
        args = (self, instance, value)
        print(f'@ Descriptor.__set__{args!r}')

    def __repr__(self):
        return '<Descriptor instance>'


print('@ builderlib module end')
````

Now in terminal type `import builderlib`

````python
@ builderlib module start
@ Builder body
@ Descriptor body
@ builderlib module end
````

## Metaclasses 101

[Metaclasses] are deeper magic than 99% of users should ever  worry about. If you wonder whether you need them, you don’t (the people  who actually need them know with certainty that they need them, and  don’t need an explanation about why).    

Tim Peters, inventor of the Timsort algorithm and prolific Python contributor

A Metaclass is a class factory! Metaclass is a class whose instance are classes.

- We know classes are objects therefore each class must be instance of some other class right ?
- Python classes are instances of `type`. In other words `type` is the metaclass for most built-in and user-defined classes.

````python
str.__class__
# <class 'type'>
type.__class__
# <class 'type' >
````

- To avoid infinite regress, the class of `type` is `type`
- NOTE: `str` adn `LineItem` are not subclasses of `type`. Both `str` and `LineItem` are instances of `type`. The all are subclasses of `object`.

![UML class diagrams with `object` and `type` relationships.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492056348/files/assets/flpy_2402.png)

The classes `object` and `type` have a unique relationship: `object` is an instance of `type`, and `type` is a subclass of `object`. This relationship is “magic”: it cannot be expressed in Python because  either class would have to exist before the other could be defined. The  fact that `type` is an instance of itself is also magical.

The next snippet shows that the class of `collections.Iterable` is `abc.ABCMeta`. Note that `Iterable` is an abstract class, but `ABCMeta` is a concrete class—after all, `Iterable` is an instance of `ABCMeta`

````python
>>> from collections.abc import Iterable
>>> Iterable.__class__
<class 'abc.ABCMeta'>
>>> import abc
>>> from abc import ABCMeta
>>> ABCMeta.__class__
<class 'type'>
````

- Ultimately, the class of `ABCMeta` is also `type`. Every class is an instance of `type`, directly or indirectly, but only metaclasses are also subclasses of `type`.

![UML class diagrams with `Iterable` and `ABCMeta` relationships.](./ch5_24.assets/flpy_2403.png)

### How a Metaclass Customizes a Class

- To use a Metaclasses, its crucial to understand how `__new__` works on any class

````python
class Klass(SuperKlass, metaclass=MetaKlass):
    x = 42
    def __init__(self, y):
        self.y = y
````

- To process `class` statement, Python calls `MetaKlass.__new__` with these arguments
  - `meta_cls` : The metaclass itself(`MetaKlass`)
  - `cls_name` : The string `Klass`
  - `bases` : The single-element tuple (`SuperKlass`), with more elements in the case of multiple inheritance
  - `cls_dict` : A mapping like :

````python
{x: 42, `__init__`: <function __init__ at 0x1009c4040>}
````

- When you implement `MetaKlass.__new__`, you can inspect and change those arguments before passing them to `super().__new__`, which will eventually call `type.__new__` to create the new class object.
- After `super().__new__` returns, you can also apply further processing to the newly created class before returning it to Python. Python then calls `SuperKlass.__init_subclass__`, passing the class you created, and then applies a class decorator to it, if one is present. Finally, Python binds the class object to its name in the surrounding namespace—usually the global namespace of a module, if the `class` statement was a top-level statement.
- The most common processing made in a metaclass `__new__` is to add or replace items in the `cls_dict`—the mapping that represents the namespace of the class under construction. For instance, before calling `super().__new__`, you can inject methods in the class under construction by adding functions to `cls_dict`. However, note that adding methods can also be done after the class is built, which is why we were able to do it using `__init_subclass__` or a class decorator.

### A Nice Metaclass Example

This is example form a book Python in a Nutshell (3rd edition) Chapter 4.

````python
class MetaBunch(type): # to create a metaclass inherit from type
    def __new__(meta_cls, cls_name, bases, cls_dict): # new works as classmethod

        defaults = {} # holds mapping of attribute names and their defaults

        def __init__(self, **kwargs): # injected in new class
            for name, default in defaults.items(): # read defaults and inject in dict
                setattr(self, name, kwargs.pop(name, default))
            if kwargs: # it means there are no slots left where we can place them. We believe in failing fast as best practice, so we don’t want to silently ignore extra items. A quick and effective solution is to pop one item from kwargs and try to set it on the instance, triggering an AttributeError on purpose.
                extra = ', '.join(kwargs)
                raise AttributeError(f'No slots left for: {extra!r}')

        def __repr__(self):  # string representation
            rep = ', '.join(f'{name}={value!r}'
                            for name, default in defaults.items()
                            if (value := getattr(self, name)) != default)
            return f'{cls_name}({rep})'

        new_dict = dict(__slots__=[], __init__=__init__, __repr__=__repr__)  # namespace for new class

        for name, value in cls_dict.items(): # iterate over namespace's of user class
            if name.startswith('__') and name.endswith('__'): # dunder name is found, copy the item to the new class namespace unless its already there. This prevents users from overwriting __init__, __repr__, ..etc
                if name in new_dict:
                    raise AttributeError(f"Can't set {name!r} in {cls_name!r}")
                new_dict[name] = value
            else: # not a dunder append to slots
                new_dict['__slots__'].append(name)
                defaults[name] = value
        return super().__new__(meta_cls, cls_name, bases, new_dict)  12


class Bunch(metaclass=MetaBunch):  # provide a base class, so users don’t need to see MetaBunch.
    pass
````



### Metaclass Evaluation Time Experiment

## A Metaclass Solution for Checked

read in book

## Metaclasses in the Real World



### Modern Features Simplify or Replace Metaclasses

Over time, several common use cases of metaclasses were made redundant by new language features:

- Class decorators : Simpler to understand than metaclasses, and less likely to cause conflicts with base classes and metaclasses.

- `__set_name__` : Avoids the need for custom metaclass logic to automatically set the name of a descriptor.

- `__init_subclass__` : Provides a way to customize class creation that is transparent to the end user and even simpler than a decorator—but may introduce conflicts in a complex class hierarchy.

- Built-in `dict` preserving key insertion order

  Eliminated the #1 reason to use `__prepare__`: to provide an `OrderedDict` to store the namespace of the class under construction. Python only calls `__prepare__` on metaclasses, so if you needed to process the class namespace in the order it appears in the source code, you had to use a metaclass before Python 3.6.

I keep advocating these features because I see too much unnecessary complexity in our profession, and metaclasses are a gateway to complexity.

### Metaclasses Are Stable Language Features

Metaclasses were introduced in Python 2.2 in 2002, together with so-called “new-style classes,” descriptors, and properties.

It is remarkable that the `MetaBunch` example, first posted by Alex Martelli in July 2002, still works in Python 3.9—the only change being the way to specify the metaclass to use, which in Python 3 is done with the syntax `class Bunch(metaclass=MetaBunch):`.

### A Class Can Only Have One Metaclass

If your class declaration involves two or more metaclasses, you will see this puzzling error message:

```
TypeError: metaclass conflict: the metaclass of a derived class
must be a (non-strict) subclass of the metaclasses of all its bases
```

This may happen even without multiple inheritance. For example, a declaration like this could trigger that `TypeError`:

```
class Record(abc.ABC, metaclass=PersistentMeta):
    pass
```

We saw that `abc.ABC` is an instance of the `abc.ABCMeta` metaclass. If that `Persistent` metaclass is not itself a subclass of `abc.ABCMeta`, you get a metaclass conflict.

There are two ways of dealing with that error:

- Find some other way of doing what you need to do, while avoiding at least one of the metaclasses involved.
- Write your own `PersistentABCMeta` metaclass as a subclass of both `abc.ABCMeta` and `PersistentMeta`, using multiple inheritance, and use that as the only metaclass for `Record`

### Metaclasses Should Be Implementation Details

Besides `type`, there are only six metaclasses in the entire Python 3.9 standard library. The better known metaclasses are probably `abc.ABCMeta`, `typing.NamedTupleMeta`, and `enum.EnumMeta`. None of them are intended to appear explicitly in user code. We may consider them implementation details.

In recent years, some metaclasses in the Python standard library were replaced by other mechanisms, without breaking the public API of their packages. The simplest way to future-proof such APIs is to offer a regular class that users subclass to access the functionality provided by the metaclass, as we’ve done in our examples.

## Wrapping Up

Metaclasses, as well as class decorators and `__init_subclass__` are useful for:

- Subclass registration
- Subclass structural validation
- Applying decorators to many methods at once
- Object serialization
- Object-relational mapping
- Object-based persistence
- Implementing special methods at the class level
- Implementing class features found in other languages, such as traits and aspect-oriented programming

Class metaprogramming can also help with performance issues in some cases, by performing tasks at import time that otherwise would execute repeatedly at runtime.

To wrap up, let’s recall Alex Martelli’s final advice from his essay “Waterfowl and ABCs”:

> And, *don’t* define custom ABCs (or metaclasses) in production code… if you feel the urge to do so, I’d bet it’s likely to be a case  of “all problems look like a nail”-syndrome for somebody who just got a  shiny new hammer—you (and future maintainers of your code) will be much  happier sticking with straightforward and simple code, eschewing such  depths.

Those powerful tools exist primarily to support library and framework development. Applications naturally should *use* those tools, as provided by the Python standard library or external packages. But *implementing* them in application code is often premature abstraction.

Good frameworks are extracted, not invented. - David Heinemeier Hansson, creator of Ruby on Rails

---

## File: python/index.md

# Python

Python is a high-level, general-purpose programming language. Its design philosophy emphasizes **code readability** with the use of significant indentation.

NOTE: These notes are adaption from following books : *Fluent Python 2nd edition (comprehensive book on python)*

## Topics

1. ### Data Structures

   1. [Python Data Model](ch1_1.md)
   2. [Array](ch1_2.md)
   3. [Dictionary & Sets](ch1_3.md)
   4. [Unicode Text vs Bytes](ch1_4.md)
   5. [Data Class Builders](ch1_5.md)
   6. [Object References, Mutability, and Recycling](ch1_6.md)

2. ### Functions as Objects

   1. [Functions as First Class Objects](ch2_7.md)
   2. [Type Hints in Functions](ch2_8.md)
   3. [Decorators and Closures](ch2_9.md)
   4. [Design Patterns with First Class Functions](ch2_10.md)

3. ### Classes and Protocols

   1. [A Pythonic Object](ch3_11.md)
   2. [Special Methods for Sequences](ch3_12.md)
   3. [Interfaces, Protocols, and ABCs](ch3_13.md)
   4. [Inheritance: For Better or for Worse](ch3_14.md)
   5. [More about Type Hints](ch3_15.md)
   6. [Operator Overloading](ch3_16.md)

4. ### Control Flow

   1. [Iterators, Generators, and Classic Coroutines](ch4_17.md)
   2. [With, Match and Else Blocks](ch4_18.md)
   3. [Concurrency Models in Python](ch4_19.md)
   4. [Concurrent Executors](ch4_20.md)
   5. [Asynchronous Programming](ch4_21.md)

5. ### Metaprogramming

   1. [Dynamic Attributes & Properties](ch5_22.md)
   2. [Attribute Descriptor](ch5_23.md)
   3. [Class Metaprogramming](ch5_24.md)


### Books

- [Python for Data Analysis](../dataanalysis/index.md) by Wes McKinney
- [Python](py/index.md)
- Python Crash Course

### Resources

- Booksite : [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)


---

## File: python/py/ch0.md

### Introduction

- Arithmetic in Python

  - Power : `a**b`

- Division in python :

  - Integer Division : `a//b`
  - Float Division : `a/b`

- Conditionals in Python

- Loop in Python

- given `n` : print `123..n` (don’t use strings)

  ```python
  for i in xrange(10):
  	print i,		# this (due to comma) prints numbers in a single line separated by space
  	
  # there is a print function from __future__ module
  print(*values, sep=' ', end='\n', file=sys.stdout) # *values means array is unpacked : val1, val2, val3..
  
  # solution 
  	print(*range(1,n+1), sep='')
  ```

### Basic Data Types

- List : `[element1, element2, element3, element4, ...]`
- 

---

