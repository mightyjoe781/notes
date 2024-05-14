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

