# Design Patterns

* Design Pattern serves as typical solution to common problems in software design
* All patterns can categorized by their *intent*
	* Creational Pattern - deals with object creation
	* Structural Pattern - deals organisation of objects/classes
	* Behavioural Patterns - deals with object/classes communications
* [Refactoring Guru](https://refactoring.guru/design-patterns)
## Creational Patterns
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

* NOTES
	* Decouples Object Creation - Client Classes don't need to know how objects are created
	* Encapsulation - Factory class has the logic to create objects
	* Extensionability - Adding a new Vehicle requires just adding a new subclass, without modifying client code
* Why you don't want user to create objects directly ??
	* Client codes should not be affected with changes in the code. Let's say your process to create object becomes complicated(db calls, using different configurations), then client has no need to know about object creations.
	* Easier Dependency Injection & Testing
		* If you create Car() directly, testing requires changing the entire class.
		* With a factory, you can **inject dependencies**, making testing more modular.
### Abstract Factory
### Builder ⭐
* lets you construct complex objects step by step
* The pattern allows you to produce different types and representations of an object using the same construction code.
* Why Use Builder Pattern ?
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

* Above Implementation has following issues
	* Long Constructor
	* Optional Parameter
	* Hard to Extend

```python
# using builder pattern
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
```
* **Readable & Flexible**: No need to remember constructor parameters.
* **Handles Optional Parameters**: Can omit sunroof, engine, etc.
* **Method Chaining**: Allows easy, fluent object creation.
* **Scalability**: Easily add new features without modifying existing code.
### Prototype
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
| __new__      | Simple, widely used  | Not extendable   |
| Decorator    | Clean, reusable      | Harder debugging |
| Metaclass    | Works for subclasses | Complex          |

## Structural Patterns
### Adapter ⭐
* allows objects with incompatible interfaces to collaborate
* usecases
	* helps integrate 3rd-party library without modifying their code
	* makes incompatible classes work together
```python
# without adapter
class MP3Player:
    def play_mp3(self, filename):
        print(f"Playing MP3 file: {filename}")

# Client Code
player = MP3Player()
player.play_mp3("song.mp3")  # Works fine ✅
player.play_mp4("video.mp4")  # ❌ AttributeError: 'MP3Player' object has no attribute 'play_mp4'
```
* Using Adapter to modify this class
```python
class MP3Player:
    def play_mp3(self, filename):
        print(f"Playing MP3 file: {filename}")

# Adapter to support other formats
class MediaAdapter:
    def __init__(self, media_type):
        self.media_type = media_type
        self.player = MP3Player()  # Uses existing player

    def play(self, filename):
        if self.media_type == "mp3":
            self.player.play_mp3(filename)
        elif self.media_type == "mp4":
            print(f"Converting {filename} to MP3 format... 🎵")
            self.player.play_mp3(filename.replace(".mp4", ".mp3"))
        else:
            print(f"Error: Unsupported format {self.media_type} ❌")

# Client Code
player = MediaAdapter("mp4")
player.play("video.mp4")  # ✅ Plays after conversion
```
### Bridge
### Composite
### Decorator ⭐
* lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.
* Usage
	* logging, security, caching & UI improvements
* why use it ?
	* **Extends functionality** without modifying the original class.
	* **Follows Open-Closed Principle** (open for extension, closed for modification).
	* **Allows multiple decorators** to be combined flexibly.
```python
# without Decorator, adding milk to coffee is cumbersome
class Coffee:
    def cost(self):
        return 5

    def description(self):
        return "Basic Coffee"

# Adding features by modifying the class (Not scalable ❌)
class CoffeeWithMilk(Coffee):
    def cost(self):
        return super().cost() + 2

    def description(self):
        return super().description() + " + Milk"

coffee = CoffeeWithMilk()
print(coffee.description())  # Basic Coffee + Milk
print(coffee.cost())  # 7
```
* creating an ingredient decorator
```python
# Base Component
class Coffee:
    def cost(self):
        return 5

    def description(self):
        return "Basic Coffee"

# Decorator Base Class
class CoffeeDecorator:
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost()

    def description(self):
        return self._coffee.description()

# Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return super().cost() + 2

    def description(self):
        return super().description() + " + Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return super().cost() + 1

    def description(self):
        return super().description() + " + Sugar"

# Client Code
coffee = Coffee()
print(coffee.description(), "->", coffee.cost())  # Basic Coffee -> 5

coffee = MilkDecorator(coffee)
print(coffee.description(), "->", coffee.cost())  # Basic Coffee + Milk -> 7

coffee = SugarDecorator(coffee)
print(coffee.description(), "->", coffee.cost())  # Basic Coffee + Milk + Sugar -> 8
```

* Flexible & Scalable
* Combinable - decorators can be combines
* **Follows SOLID principles** – No unnecessary subclasses or modifications.

### Facade
### Flyweight
### Proxy ⭐
* lets you provide a substitute or placeholder for another object. A proxy controls access to the original object, allowing you to perform something either before or after the request gets through to the original object.
* Advantages
	* Lazy Initialization - Virtual Proxy
	* Access Proxy (Control) - Restriction to access original object
	* Logging/monitoring Proxy - record requests for analytics and debugging
	* Caching Proxy - store results to avoid recomputation
	* Remote Proxy - Interface for calling methods on a remote object
* Virtual Proxy
```python
class RealImage:
    """Heavy object that loads an image from disk."""
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()

    def load_from_disk(self):
        print(f"Loading image: {self.filename}")

    def display(self):
        print(f"Displaying image: {self.filename}")

class ProxyImage:
    """Proxy that delays the creation of RealImage until display is called."""
    def __init__(self, filename):
        self.filename = filename
        self.real_image = None

    def display(self):
        if self.real_image is None:
            self.real_image = RealImage(self.filename)  # Lazy Initialization
        self.real_image.display()

# Client Code
image = ProxyImage("test_image.jpg")  # Image not loaded yet
image.display()  # Loads image only when needed
image.display()  # Second call does not reload image
```

* logging Proxy
```python
class RealService:
    def operation(self):
        print("Performing an operation in RealService")

class LoggingProxy:
    """Logs requests before calling the actual object."""
    def __init__(self, real_service):
        self.real_service = real_service

    def operation(self):
        print("Logging: Operation is about to be executed")
        self.real_service.operation()
        print("Logging: Operation executed successfully")

# Client Code
service = RealService()
proxy = LoggingProxy(service)
proxy.operation()
```
## Behavioural Patterns
### Chain of Responsibility ⭐
* lets you pass requests along a chain of handlers. Upon receiving a request,
* Each handler decides
	* ✅ **Process the request** OR
	* ✅ **Forward it to the next handler**
* When to Use
	* **Logging and Debugging** – Different loggers (file, console, database) handle messages.
	* **Event Handling** – UI elements process events (buttons, forms, popups).
	* **Request Validation** – Middleware authentication in web frameworks.
	* **Customer Support System** – Requests escalate from agent → supervisor → manager.
* Key Components
	* Handler (abstract class) - Defines the method to handle requests.
	* **Concrete Handlers** – Implement request processing & decide whether to pass it forward.
	* **Client** – Sends requests to the first handler in the chain.
```python
# logging System
class Logger:
    """Base Handler"""
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def log(self, level, message):
        if self.next_handler:
            self.next_handler.log(level, message)

class DebugLogger(Logger):
    def log(self, level, message):
        if level == "DEBUG":
            print(f"[DEBUG] {message}")
        else:
            super().log(level, message)

class WarningLogger(Logger):
    def log(self, level, message):
        if level == "WARNING":
            print(f"[WARNING] {message}")
        else:
            super().log(level, message)

class ErrorLogger(Logger):
    def log(self, level, message):
        if level == "ERROR":
            print(f"[ERROR] {message}")
        else:
            super().log(level, message)

# Setting up the chain
logger_chain = DebugLogger(WarningLogger(ErrorLogger()))

# Client Code
logger_chain.log("DEBUG", "This is a debug message.")
logger_chain.log("WARNING", "This is a warning message.")
logger_chain.log("ERROR", "This is an error message.")
```

```python
# web middleware - auth -> role -> log
class Handler:
    """Base Handler"""
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return "Request reached the end of the chain"

class AuthHandler(Handler):
    """Authentication Middleware"""
    def handle(self, request):
        if not request.get("user"):
            return "Authentication Failed"
        return super().handle(request)

class RoleHandler(Handler):
    """Authorization Middleware"""
    def handle(self, request):
        if request.get("role") != "admin":
            return "Access Denied"
        return super().handle(request)

class LoggingHandler(Handler):
    """Logging Middleware"""
    def handle(self, request):
        print(f"Logging request: {request}")
        return super().handle(request)

# Setting up the chain
middleware_chain = AuthHandler(RoleHandler(LoggingHandler()))

# Client Code
request1 = {"user": "Alice", "role": "admin"}
print(middleware_chain.handle(request1))  # Success

request2 = {"user": "Bob", "role": "guest"}
print(middleware_chain.handle(request2))  # Access Denied

request3 = {"role": "admin"}  # Missing user
print(middleware_chain.handle(request3))  # Authentication Failed
```
### Command ⭐
* encapsulates a request as an object, allowing for **delayed execution, undo/redo functionality, and queuing commands**.
* When to Use
	* **Undo/Redo functionality** – Text editors, Photoshop.
	* **Job Scheduling** – Task execution in threads.
	* **Remote Control Devices** – TV remote buttons, IoT devices.
* Key Components
	* **Command Interface** – Declares an execution method.
	* **Concrete Commands** – Implement specific actions.
	* **Invoker** – Triggers commands.
	* **Receiver** – Performs the actual work.
```python
# tv remote
from abc import ABC, abstractmethod

class Command(ABC):
    """Command Interface"""
    @abstractmethod
    def execute(self):
        pass

class TV:
    """Receiver"""
    def turn_on(self):
        print("TV is ON")

    def turn_off(self):
        print("TV is OFF")

class TurnOnCommand(Command):
    """Concrete Command: Turn ON"""
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self):
        self.tv.turn_on()

class TurnOffCommand(Command):
    """Concrete Command: Turn OFF"""
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self):
        self.tv.turn_off()

class RemoteControl:
    """Invoker"""
    def __init__(self):
        self.command = None

    def set_command(self, command: Command):
        self.command = command

    def press_button(self):
        if self.command:
            self.command.execute()

# Client Code
tv = TV()
remote = RemoteControl()

turn_on = TurnOnCommand(tv)
turn_off = TurnOffCommand(tv)

remote.set_command(turn_on)
remote.press_button()  # TV is ON

remote.set_command(turn_off)
remote.press_button()  # TV is OFF
```
### Iterator
### Mediator
### Memento
### Observer ⭐
* The **Observer Pattern** allows multiple objects (**observers**) to listen to and react to changes in another object (**subject**). When the subject’s state changes, all registered observers are notified automatically.
* When to Use
	* **Event-driven programming** – UI elements react to user actions.
	* **Publish-Subscribe systems** – Notification services, message brokers.
	* **Data Binding** – React.js, Vue.js frameworks.
	* **Stock Market Updates** – Multiple clients get real-time stock prices.
* Key Components
	* **Subject (Publisher)** – Maintains a list of observers and notifies them when state changes.
	* **Observer (Subscriber)** – Listens for updates from the subject.
	* **Concrete Subject** – Implements state changes and observer management.
```python
class StockMarket:
    """Subject (Publisher)"""
    def __init__(self):
        self.observers = []
        self.stock_price = 0

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.stock_price)

    def set_price(self, price):
        self.stock_price = price
        self.notify_observers()

class Investor:
    """Observer (Subscriber)"""
    def __init__(self, name):
        self.name = name

    def update(self, price):
        print(f"{self.name} received stock price update: {price}")

# Client Code
market = StockMarket()
investor1 = Investor("Alice")
investor2 = Investor("Bob")

market.add_observer(investor1)
market.add_observer(investor2)

market.set_price(100)  # Both investors get notified
market.set_price(120)  # Another update is sent
```
### Stage
### Strategy ⭐
 * **define a family of algorithms**, put them in separate classes, and make them **interchangeable** at runtime.
 * When to use
	 * **Multiple algorithms for the same task** – Sorting, Compression.
	 * **Reducing conditional logic (if-else/switch)** – Payment methods, Authentication.
	 * **Behavior modification at runtime** – Game difficulty levels.
 * Key Components
	 * **Context** – Maintains a reference to a strategy object.
	 * **Strategy Interface** – Defines a common interface for all strategies.
	 * **Concrete Strategies** – Implement different algorithms.
```python
# payment strategy
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    """Strategy Interface"""
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    """Concrete Strategy: Credit Card"""
    def pay(self, amount):
        print(f"Paid ${amount} using Credit Card.")

class PayPalPayment(PaymentStrategy):
    """Concrete Strategy: PayPal"""
    def pay(self, amount):
        print(f"Paid ${amount} using PayPal.")

class PaymentContext:
    """Context that uses a strategy"""
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def checkout(self, amount):
        self.strategy.pay(amount)

# Client Code
context = PaymentContext(CreditCardPayment())
context.checkout(100)  # Paid using Credit Card

context.set_strategy(PayPalPayment())  
context.checkout(200)  # Paid using PayPal
```
### Template Method
### Visitor