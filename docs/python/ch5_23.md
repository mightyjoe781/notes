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