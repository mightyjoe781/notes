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

