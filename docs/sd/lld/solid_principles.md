# SOLID


Key Principle of LLD

- S - Single Responsibility Principle (SRP)
- O - Open Closed Principle (OCP)
- L - Liskov Substitution Principle (LSP)
- I - Interface Segregation Principle (ISP)
- D - Dependency Inversion (DIP)

## Single Responsibility Principle

* A class, module, or function should have only one reason to change, meaning it should perform only one specific task or have one primary responsibility.

* Goal : Separate behaviours so that if bug arise as a result of your change, it won't affect other unrelated behaviours.

Example - 1 Report Generation & Printing
```python
class Report:
    def compile_content(self, data):
        # logic to gather and format report
        return "compiled report"

    def print_report(self, report):
        # logic to print or send to printer
        print("Printing:", report)
        
    def mail_report(self, email, report):
        print("Sending:", email, report)
```

* Above code violates SRP because it tries to do 3 tasks which should be separated (Report Compiler, Printer, Mailer)

```python
class ReportCompiler:
    def compile_content(self, data):
        # only compiles report content
        return "compiled report"

class ReportPrinter:
    def print_report(self, report):
        # only handles output/printing
        print("Printing:", report)

# usage
compiler = ReportCompiler()
printer = ReportPrinter()
mailer = ReportMailer()
user_email = "smk@minetest.in"

report = compiler.compile_content(data={})
printer.print_report(report)
mailer.send_report(user_email, report)
```

Example 2 - Food Delivery App
```python
class FoodDeliveryApp:
    def handle_order(self, order):
        # validate & accept order
        print("Order accepted:", order)

    def calculate_bill(self, order):
        # compute tax, discounts
        return 100  # dummy bill

    def schedule_delivery(self, order):
        # assign delivery agent & time
        print("Delivery scheduled for:", order)
```

```python
class OrderHandler:
    def handle_order(self, order):
        print("Order accepted:", order)

class BillCalculator:
    def calculate_bill(self, order):
        return 100  # dummy bill

class DeliveryScheduler:
    def schedule_delivery(self, order):
        print("Delivery scheduled for:", order)

# usage
order = {"item": "Pizza"}

handler = OrderHandler()
billing = BillCalculator()
scheduler = DeliveryScheduler()

handler.handle_order(order)
print("Bill:", billing.calculate_bill(order))
scheduler.schedule_delivery(order)
```

## Open-Close Principle
* software entities (classes, modules, functions, etc.) should be open for extension but closed for modification
* Goal : extend the current behaviour, avoiding changes to existing behaviour (client using the old instances should not encounter bugs)
* good idea is to depend (coupling) on abstract classes, rather than concrete classes.

Example-1
- Violates OCP
```python
class PaymentProcessor:
    def process(self, method, amount):
        if method == "credit_card":
            print("Processing credit card payment:", amount)
        elif method == "paypal":
            print("Processing PayPal payment:", amount)
        else:
            print("Unknown payment method")
```
* correct way to implement, now we can extent new payment processors by inheriting Abstract Class.
```python
from abc import ABC, abstractmethod

# abstract base (closed for modification)
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# extensions (open for extension)
class CreditCardPayment(PaymentMethod):
    def pay(self, amount):
        print("Processing credit card payment:", amount)

class PayPalPayment(PaymentMethod):
    def pay(self, amount):
        print("Processing PayPal payment:", amount)

class CryptoPayment(PaymentMethod):
    def pay(self, amount):
        print("Processing crypto payment:", amount)

# main processor (no modification needed)
class PaymentProcessor:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def process(self, amount):
        self.payment_method.pay(amount)

# usage
processor = PaymentProcessor(CryptoPayment())
processor.process(200)
```
Example - 2 Area Calculator
```python
class AreaCalculator:
    def calculate(self, shape):
        if shape["type"] == "circle":
            return 3.14 * shape["radius"] ** 2
        elif shape["type"] == "rectangle":
            return shape["width"] * shape["height"]
```

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height

# calculator is closed for modification
class AreaCalculator:
    def calculate(self, shape: Shape):
        return shape.area()

# usage
shapes = [Circle(5), Rectangle(2, 3)]
calc = AreaCalculator()

for s in shapes:
    print(calc.calculate(s))
```

## LSP (Liskov Substitution Principle)

* Objects of a superclass should be replaceable with objects of its subclasses **_without altering the correctness_** of the program

Example - 1
```python
class Bird:
    def fly(self):
        print("Flying high in the sky")

class Penguin(Bird):
    def fly(self):
        # Penguins can’t fly!
        raise Exception("Penguins cannot fly")
```

* Violates A Penguin is-a Bird, but substituting it breaks client code that assumes all Birds can fly. That’s a violation of LSP.

```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

class Sparrow(Bird):
    def move(self):
        print("Flying high in the sky")

class Penguin(Bird):
    def move(self):
        print("Swimming in the water")

# usage
birds = [Sparrow(), Penguin()]

for b in birds:
    b.move()   # works for both sparrow & penguin
```

* So technically design of the previous class was not correct, and design needs to address this. An abstract representation should not force us to implement designs.

## ISP (Interface Segregation Principle)
* Clients should not be forced to depend on interfaces, methods, behaviours they do not use.

Example - 1
```python
from abc import ABC, abstractmethod

# Too broad
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass

    @abstractmethod
    def eat(self):
        pass

class HumanWorker(Worker):
    def work(self):
        print("Human working")
    def eat(self):
        print("Human eating lunch")

class RobotWorker(Worker):
    def work(self):
        print("Robot working")
    def eat(self):
        # Robots don't eat!
        raise Exception("Robots cannot eat")
```

* RobotWorker is forced to implement eat() even though it doesn’t apply

```python
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class HumanWorker(Workable, Eatable):
    def work(self):
        print("Human working")
    def eat(self):
        print("Human eating lunch")

class RobotWorker(Workable):
    def work(self):
        print("Robot working")
```

* Now interfaces are segregated.

## DIP (Dependency Inversion Principle)

* High-level modules should not depend on low-level modules. Both should depend on abstractions.

Example - 1 : Notifications
```python
class EmailService:
    def send_email(self, message):
        print("Sending email:", message)

class Notification:
    def __init__(self):
        self.email_service = EmailService()  # tightly coupled

    def notify(self, message):
        self.email_service.send_email(message)
```
* Problem: Notification is tightly coupled to EmailService. If you want to switch to SMS or Push notifications, you must modify Notification.
```python
from abc import ABC, abstractmethod

# Abstraction
class MessageService(ABC):
    @abstractmethod
    def send(self, message):
        pass

# Low-level implementations
class EmailService(MessageService):
    def send(self, message):
        print("Sending email:", message)

class SMSService(MessageService):
    def send(self, message):
        print("Sending SMS:", message)

# High-level module depends on abstraction
class Notification:
    def __init__(self, service: MessageService):
        self.service = service

    def notify(self, message):
        self.service.send(message)

# usage
notifier = Notification(SMSService())
notifier.notify("Hello via SMS!")

notifier = Notification(EmailService())
notifier.notify("Hello via Email!")
```
