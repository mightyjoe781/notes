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