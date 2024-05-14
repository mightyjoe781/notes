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



