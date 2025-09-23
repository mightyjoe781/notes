# Design Patterns

* Design Pattern serves as typical solution to common problems in software design
* All patterns can be categorised by their *intent*
   	* Creational Pattern - deals with object creation
   	* Structural Pattern - deals organisation of objects/classes
   	* Behavioural Patterns - deals with object/classes communications

## Creational Pattern
* Factory ⭐
* Abstract Factory ⭐
* Builder ⭐
* Prototype
* Singleton ⭐

### Factory Method ⭐

* also known as virtual constructor
* provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created

```python
from abc import ABC, abstractmethod

# Step 1: Define an abstract product
class Vehicle(ABC):
    @abstractmethod
    def create(self):
        pass

# Step 2: Implement concrete products
class Car(Vehicle):
    def create(self):
        return "Car is created 🚗"

class Bike(Vehicle):
    def create(self):
        return "Bike is created 🏍️"

# Step 3: Define a factory class with a factory method
class VehicleFactory(ABC):
    @abstractmethod
    def get_vehicle(self) -> Vehicle:
        pass

# Step 4: Implement concrete factories for each vehicle type
class CarFactory(VehicleFactory):
    def get_vehicle(self) -> Vehicle:
        return Car()

class BikeFactory(VehicleFactory):
    def get_vehicle(self) -> Vehicle:
        return Bike()

# Step 5: Client code
def client_code(factory: VehicleFactory):
    vehicle = factory.get_vehicle()
    print(vehicle.create())

# Example Usage
if __name__ == "__main__":
    car_factory = CarFactory()
    bike_factory = BikeFactory()

    client_code(car_factory)  # Output: Car is created 🚗
    client_code(bike_factory)  # Output: Bike is created 🏍️

```


NOTES : 

- Decouples Object Creation - Client Classes don't need to know how objects are created
- Encapsulation - Factory class has the logic to create objects
- Extensionability - Adding a new Vehicle requires just adding a new subclass, without modifying client code


Why you don't want user to create objects directly ??

- Client codes should not be affected with changes in the code. Let's say your process to create object becomes complicated(db calls, using different configurations), then client has no need to know about object creations.
- Easier Dependency Injection & Testing
    - If you create Car() directly, testing requires changing the entire class.
    - With a factory, you can **inject dependencies**, making testing more modular.



### Abstract Factory
### Builder ⭐

* lets you construct complex objects step by step
* The pattern allows you to produce different types and representations of an object using the same construction code.

Why Use Builder PatternTest

* Better Readability – Instead of a constructor with too many parameters, we build the object step by step.
* Flexibility – Can construct different variations of an object (e.g., Car, SportsCar, SUV).
* Encapsulation – The construction logic is separate from the object representation.

```python
# without builder pattern
class Car:
    def __init__(self, brand, engine, seats, sunroof):
        self.brand = brand
        self.engine = engine
        self.seats = seats
        self.sunroof = sunroof

    def __str__(self):
        return f"Car({self.brand}, {self.engine}, {self.seats} seats, Sunroof: {self.sunroof})"

# Creating a car object with a long constructor
car = Car("Tesla", "Electric", 5, True)
print(car)
```

Above Implementation has following issues
- Long Constructor
- Optional Parameter
- Hard to Extend

````python
#using builder pattern
class Car:
    def __init__(self, brand=None, engine=None, seats=None, sunroof=None):
        self.brand = brand
        self.engine = engine
        self.seats = seats
        self.sunroof = sunroof

    def __str__(self):
        return f"Car({self.brand}, {self.engine}, {self.seats} seats, Sunroof: {self.sunroof})"

class CarBuilder:
    def __init__(self):
        self.car = Car()

    def set_brand(self, brand):
        self.car.brand = brand
        return self  # Enables method chaining

    def set_engine(self, engine):
        self.car.engine = engine
        return self

    def set_seats(self, seats):
        self.car.seats = seats
        return self

    def set_sunroof(self, sunroof):
        self.car.sunroof = sunroof
        return self

    def build(self):
        return self.car

# Using the builder pattern
car = CarBuilder().set_brand("Tesla").set_engine("Electric").set_seats(5).set_sunroof(True).build()
print(car)  # ✅ Car(Tesla, Electric, 5 seats, Sunroof: True)
````


- **Readable & Flexible**: No need to remember constructor parameters.
- **Handles Optional Parameters**: Can omit sunroof, engine, etc.
- **Method Chaining**: Allows easy, fluent object creation.
- **Scalability**: Easily add new features without modifying existing code.
### Prototype

- lets you copy existing objects without making your code dependent on their classes
- creates new objects by cloning existing instances rather than creating from scratch
- useful when object creation is expensive or complex
- example : email markups are expensive if same email is sent to multiple people, templates are used and only variables are replaced for that text. e.g. replacing `{{username}}` in the template

````python
import copy
from abc import ABC, abstractmethod

# Step 1: Define abstract prototype
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

# Step 2: Implement concrete prototypes
class Document(Prototype):
    def __init__(self, title, content, formatting):
        self.title = title
        self.content = content
        self.formatting = formatting  # Complex formatting object
        
    def clone(self):
        # Deep copy to ensure formatting object is also cloned
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"Document(title='{self.title}', content='{self.content[:20]}...', formatting={self.formatting})"

class Report(Document):
    def __init__(self, title, content, formatting, charts):
        super().__init__(title, content, formatting)
        self.charts = charts  # List of chart objects
        
    def clone(self):
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"Report(title='{self.title}', content='{self.content[:20]}...', charts={len(self.charts)} charts)"

# Step 3: Prototype manager/registry
class DocumentRegistry:
    def __init__(self):
        self._prototypes = {}
    
    def register_prototype(self, name, prototype):
        self._prototypes[name] = prototype
    
    def create_document(self, name):
        prototype = self._prototypes.get(name)
        if prototype:
            return prototype.clone()
        return None

# Example Usage
if __name__ == "__main__":
    # Create complex formatting object (expensive to create)
    complex_formatting = {"font": "Arial", "size": 12, "styles": ["bold", "italic"]}
    
    # Create prototype documents
    template_doc = Document("Template", "Default content", complex_formatting)
    template_report = Report("Report Template", "Report content", complex_formatting, ["chart1", "chart2"])
    
    # Register prototypes
    registry = DocumentRegistry()
    registry.register_prototype("standard_doc", template_doc)
    registry.register_prototype("standard_report", template_report)
    
    # Clone documents instead of creating from scratch
    doc1 = registry.create_document("standard_doc")
    doc1.title = "My Document"
    doc1.content = "Custom content for doc1"
    
    doc2 = registry.create_document("standard_doc")
    doc2.title = "Another Document"
    doc2.content = "Different content for doc2"
    
    print(doc1)  # ✅ Document with custom content but same formatting
    print(doc2)  # ✅ Another document with different content
    print(template_doc)  # ✅ Original template unchanged
````

Notes:

* **Performance Optimisation** - Avoids expensive object creation when you need similar objects
- **Flexible Object Creation** - Create objects without knowing their exact classes
- **Preserves Object State** - Clones maintain the internal state of prototype
- **Reduces Subclassing** - Instead of creating many subclasses, clone and modify existing objects

When to Use Prototype Pattern ??

- Object creation is **expensive** (database calls, file I/O, complex calculations)
- Need **similar objects** with slight variations
- Want to avoid **tight coupling** between client and concrete classes
- **Runtime object composition** - decide which objects to clone at runtime

### Singleton ⭐

* lets you ensure that a class has only one instance, while providing a global access point to this instance
* Advantages
    * **Prevents multiple instances** of a resource-heavy class.
    * **Centralized access** to a shared instance across the application.
    * **Ensures consistency** when only one instance should exist (e.g., one DB connection)
* Examples Use Cases are one-root logger or one spark context, because spark initialization is costly.

```python
class Singleton:
    _instance = None  # Holds the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
        # The __new__ method ensures only one instance is created
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

# Usage
obj1 = Singleton()
obj2 = Singleton()
print(obj1 is obj2)  # ✅ True (Same instance)
```

Other Interesting ways to create Singleton Classes in Python
```python
# using decorator
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Logger:
    def log(self, msg):
        print(f"[LOG]: {msg}")

# Usage
logger1 = Logger()
logger2 = Logger()
print(logger1 is logger2)  # ✅ True (Same instance)

# using metaclasses
# Ensures **any subclass** automatically follows the Singleton pattern.
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def connect(self):
        return "Connected to database"

# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # ✅ True (Same instance)

```

| **Approach** | **Pros**             | **Cons**         |
| ------------ | -------------------- | ---------------- |
| `__new__`    | Simple, widely used  | Not extendable   |
| Decorator    | Clean, reusable      | Harder debugging |
| Metaclass    | Works for subclasses | Complex          |
