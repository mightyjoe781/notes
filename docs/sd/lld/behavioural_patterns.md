# Behavioural Patterns

* Chain of Responsibility ⭐
* Command ⭐
* Iterator ⭐
* Mediator
* Memento
* Observer ⭐
* Stage
* Strategy Pattern ⭐
* Template Method
* Visitor

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

Without the Iterator, lets say there is a repository returning all the users.

•	Client doesn’t care about LIMIT / OFFSET.
•	Repository provides a clean, Pythonic iteration interface.
•	If DB changes from SQL → API → cache, client code stays the same.

Without Iterator (client handles the pagination ❌) 

```python
class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_users(self, limit, offset):
        # Imagine this queries the DB
        return self.db.query(f"SELECT * FROM users LIMIT {limit} OFFSET {offset}")

# Client code needs to handle pagination manually
repo = UserRepository(db=...)
limit, offset = 2, 0

while True:
    users = repo.get_users(limit, offset)
    if not users:
        break
    for user in users:
        print("👤", user)
    offset += limit
```

Problem : Client code is tied to limit/offset and pagination logic

With Iterator Pattern. Encapsulate the pagination details inside an iterator.

```python
class UserIterator:
    """Iterator that hides pagination logic."""
    def __init__(self, repo, batch_size=2):
        self.repo = repo
        self.batch_size = batch_size
        self.offset = 0
        self.current_batch = []
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Load next batch if needed
        if self.index >= len(self.current_batch):
            self.current_batch = self.repo.get_users(self.batch_size, self.offset)
            if not self.current_batch:
                raise StopIteration
            self.offset += self.batch_size
            self.index = 0

        user = self.current_batch[self.index]
        self.index += 1
        return user


class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_users(self, limit, offset):
        # Mock DB fetch
        data = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
        return data[offset: offset + limit]

    def __iter__(self):
        return UserIterator(self)
```

```python
repo = UserRepository(db=None)  # Mock DB
for user in repo:   # Client just iterates, no offsets/limits
    print(user)
```

### Mediator

### Memento

* lets you save and restore the previous state of an object without revealing the details of its implementation
* When to use
    * *Undo/Redo operations** – Text editors, games, drawing applications.
    * **State recovery** – Crash recovery in software.
    * **Checkpointing** – Saving progress in a game.
* Key Components
    * **Memento** – Stores the state of an object.
    * **Originator** – Creates and restores mementos.
    * **Caretaker** – Manages mementos and handles state restoration.

```python
class Memento:
    """Memento stores the state of an object."""
    def __init__(self, state):
        self._state = state

    def get_saved_state(self):
        return self._state

class TextEditor:
    """Originator - Creates and restores mementos."""
    def __init__(self):
        self._text = ""

    def write(self, text):
        self._text = text

    def save(self):
        return Memento(self._text)

    def restore(self, memento):
        self._text = memento.get_saved_state()

    def show(self):
        print(f"Current Text: {self._text}")

class Caretaker:
    """Caretaker - Manages saved states."""
    def __init__(self):
        self._history = []

    def save_state(self, memento):
        self._history.append(memento)

    def restore_state(self):
        if self._history:
            return self._history.pop()
        return None

# Client Code
editor = TextEditor()
caretaker = Caretaker()

editor.write("Hello, World!")
caretaker.save_state(editor.save())  # Save state

editor.show()  # Output: Current Text: Hello, World!

editor.write("New Text")
editor.show()  # Output: Current Text: New Text

# Restore previous state
editor.restore(caretaker.restore_state())
editor.show()  # Output: Current Text: Hello, World!
```

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

* models an **object’s behavior as a finite set of states**, with **each state defining its own behavior**.
* When to Use
    * When an object has different modes or stages** – Traffic lights, vending machines.
    * **State-dependent behavior** – Objects act differently in different states.
    * **Reducing complex if-else logic** – Avoids conditionals in methods.
* Key Components
    * **State Interface** – Defines behavior for all states.
    * **Concrete States** – Implement specific behavior for each state.
    * **Context (Object)** – Maintains current state & delegates actions.

```python
from abc import ABC, abstractmethod

class TrafficLightState(ABC):
    """Abstract state class defining state-specific behavior."""
    
    @abstractmethod
    def handle(self, light):
        pass

class RedLight(TrafficLightState):
    def handle(self, light):
        print("🚦 Red Light - Stop!")
        light.state = GreenLight()

class GreenLight(TrafficLightState):
    def handle(self, light):
        print("🚦 Green Light - Go!")
        light.state = YellowLight()

class YellowLight(TrafficLightState):
    def handle(self, light):
        print("🚦 Yellow Light - Slow Down!")
        light.state = RedLight()

class TrafficLight:
    """Context class maintaining the current state."""
    
    def __init__(self):
        self.state = RedLight()  # Initial state

    def change(self):
        self.state.handle(self)

# Client Code
traffic_light = TrafficLight()

for _ in range(4):
    traffic_light.change()
```

### Strategy ⭐

**define a family of algorithms**, put them in separate classes, and make them **interchangeable** at runtime.

* When to use
    * **Multiple algorithms for the same task** – Sorting, Compression.
    * **Reducing conditional logic (if-else/switch)** – Payment methods, Authentication.
    * **Behaviour modification at runtime** – Game difficulty levels.

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

### Repository Pattern

It is an architectural pattern, not structural/behaviour. Proxy(introduced in Gang of 4) has intent of structural wrapper, while Repository has architecture abstraction (introduced in DDD).

Another comparison often drawn with mediator, but Mediator deals with preventing dependencies/coupling between objects, while Repository is just database abstraction layer.

Often known as DAO (Data Access Objects).

- **Repository** acts as a **mediator between domain/business logic and data access layer**.
- It hides database queries, providing a **clean abstraction** for data operations.
- Usage:
    - Decouples business logic from persistence logic.
    - Centralizes data access logic (CRUD, queries).
    - Makes switching storage (SQL → NoSQL, in-memory) easier.

```python
from abc import ABC, abstractmethod

# Domain Model
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return f"User(id={self.user_id}, name='{self.name}')"

# Repository Interface
class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def get(self, user_id: int) -> User:
        pass

    @abstractmethod
    def list_all(self):
        pass


# In-memory Repository (Concrete Implementation)
class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {} # private store

    def add(self, user: User):
        self._users[user.user_id] = user.name
        print(f"Added {user}")
        
    def get(self, user_id: int) -> User:
        return self._users[user_id]

    def list_all(self):
        return list(self._users.values())

repo = InMemoryUserRepository()
repo.add(User(1, "Alice"))
repo.add(User(2, "Bob"))

print(repo.get(1))
print(repo.list_all())
```
### Template Method

* defines the **skeleton** of an algorithm in a **base class**, allowing subclasses to **override specific steps** without modifying the structure of the algorithm.
* When to Use
    * **Common workflow with variations** – Report generation, data processing.
    * **Code reuse** – Avoids duplicate code in similar processes.
    * **Standardized behavior** – Ensures steps are executed in a defined order.
* Key Components
    * **Abstract Class (Template)** – Defines the algorithm structure.
    * **Concrete Class** – Implements missing steps of the algorithm.

```python
from abc import ABC, abstractmethod

class ReportGenerator(ABC):
    """Abstract class defining the template method."""
    
    def generate_report(self):
        """Template method defining the report generation process."""
        self.collect_data()
        self.analyze_data()
        self.format_report()
        self.print_report()

    @abstractmethod
    def collect_data(self):
        pass

    @abstractmethod
    def analyze_data(self):
        pass

    def format_report(self):
        """Common implementation."""
        print("Formatting report in PDF format.")

    def print_report(self):
        """Common implementation."""
        print("Printing report...")

class SalesReport(ReportGenerator):
    """Concrete class implementing specific steps."""
    
    def collect_data(self):
        print("Collecting sales data.")

    def analyze_data(self):
        print("Analyzing sales trends.")

# Client Code
report = SalesReport()
report.generate_report()
```

### Visitor

* **add new behaviors to objects** **without modifying their structure**, by **separating the operation from the object itself**.
* When to Use
    * **Extending behavior without modifying existing classes** – Syntax tree traversal.
    * **Applying different operations to a group of objects** – Compilers, AST manipulation
    * **Avoiding clutter in existing classes** – Separates logic from data structures.
* Components
    * **Visitor** – Defines new operations on elements.
    * **Concrete Visitors** – Implement specific behavior.
    * **Element** – Accepts a visitor and allows it to operate on itself.


```python

# We **separate operations (size calculation & compression)** from the **file structure**
from abc import ABC, abstractmethod

class FileElement(ABC):
    """Abstract element accepting visitors."""
    
    @abstractmethod
    def accept(self, visitor):
        pass

class File(FileElement):
    """Concrete file class."""
    
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def accept(self, visitor):
        visitor.visit_file(self)

class Folder(FileElement):
    """Concrete folder class."""
    
    def __init__(self, name, children):
        self.name = name
        self.children = children

    def accept(self, visitor):
        visitor.visit_folder(self)

class Visitor(ABC):
    """Abstract visitor defining operations."""
    
    @abstractmethod
    def visit_file(self, file):
        pass

    @abstractmethod
    def visit_folder(self, folder):
        pass

class SizeCalculator(Visitor):
    """Concrete visitor calculating total size."""
    
    def visit_file(self, file):
        print(f"File: {file.name}, Size: {file.size} KB")
    
    def visit_folder(self, folder):
        print(f"Folder: {folder.name} contains:")
        for child in folder.children:
            child.accept(self)

# Client Code
file1 = File("Document.txt", 120)
file2 = File("Photo.jpg", 450)
folder = Folder("MyFolder", [file1, file2])

size_calculator = SizeCalculator()
folder.accept(size_calculator)
```