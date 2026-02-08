# Structural Patterns

* Adapter ⭐ 
* Bridge
* Composite
* Decorator ⭐
* Facade
* Flyweight
* Proxy ⭐

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

* **decouples an abstraction from its implementation**, allowing them to evolve **independently**
* When to Use
    * **When you want to avoid a rigid class hierarchy** - Prevents class explosion due to multiple variations.
    * **When you need to support multiple implementations** - Example: Different platforms (Windows, Linux, macOS).
    * **When abstraction and implementation should vary independently** - Example: Devices and their remote controls.

* Key Components
    * **Abstraction** - Defines a high-level interface (e.g., RemoteControl).
    * **Refined Abstraction** - Extends abstraction with additional behavior.
    * **Implementation Interface** - Defines the low-level details (e.g., Device).
    * **Concrete Implementations** - Provide specific implementations.

```python
from abc import ABC, abstractmethod

# Implementation Interface (Device)
class Device(ABC):
    """Defines a common interface for all devices."""
    
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

# Concrete Implementations (TV & Radio)
class TV(Device):
    def turn_on(self):
        print("📺 TV is now ON")

    def turn_off(self):
        print("📺 TV is now OFF")

class Radio(Device):
    def turn_on(self):
        print("📻 Radio is now ON")

    def turn_off(self):
        print("📻 Radio is now OFF")

# Abstraction (Remote Control)
class RemoteControl:
    """Bridge between the abstraction (Remote) and implementation (Device)."""
    
    def __init__(self, device: Device):
        self.device = device

    def toggle_power(self):
        print("🔘 Toggling Power...")
        self.device.turn_on() if isinstance(self.device, TV) else self.device.turn_off()

# Client Code
tv_remote = RemoteControl(TV())
radio_remote = RemoteControl(Radio())

tv_remote.toggle_power()   # 📺 TV is now ON
radio_remote.toggle_power() # 📻 Radio is now OFF
```
### Composite

**Composite** is a structural design pattern that lets you compose objects into tree structures and then work with these structures as if they were individual objects.

Read up about AST (Abstract Syntax Tree)
### Decorator ⭐

* lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.
* Usage : logging, security, caching & UI improvements
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

# Adding features by modifying the class (Not scalable)
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

- Flexible & Scalable
- Combinable - decorators can be combines
- **Follows SOLID principles** - No unnecessary subclasses or modifications.
### Facade

**Facade** is a structural design pattern that provides a simplified interface to a library, a framework, or any other complex set of classes.
### Flyweight

**Flyweight** is a structural design pattern that reduces memory usage by **sharing common (intrinsic) state across many objects**, while keeping only the **unique (extrinsic) state per object**.

```python

class BulletType:
    def __init__(self, sprite, damage):
        self.sprite = sprite      # shared
        self.damage = damage      # shared
        
class BulletFactory:
    _types = {}

    @classmethod
    def get_bullet_type(cls, sprite, damage):
        key = (sprite, damage)
        if key not in cls._types:
            cls._types[key] = BulletType(sprite, damage)
        return cls._types[key]
        
class Bullet:
    def __init__(self, x, y, velocity, bullet_type):
        self.x = x                # unique
        self.y = y                # unique
        self.velocity = velocity # unique
        self.bullet_type = bullet_type  # shared
        
# Shared flyweight 
fast_bullet = BulletFactory.get_bullet_type("bullet.png", 10)

# Thousands of bullets share the same BulletType
b1 = Bullet(10, 20, 5, fast_bullet)
b2 = Bullet(15, 25, 6, fast_bullet)
b3 = Bullet(30, 40, 7, fast_bullet)

print(b1.bullet_type is b2.bullet_type)  # True

```
### Proxy ⭐

* lets you provide a substitute or placeholder for another object. A proxy controls access to the original object, allowing you to perform something either before or after the request gets through to the original object.
* Advantages
    * Lazy Initialization - Virtual Proxy
    * Access Proxy (Control) - Restriction to access original object
    * Logging/monitoring Proxy - record requests for analytics and debugging
    * Caching Proxy - store results to avoid recomputation
    * Remote Proxy - Interface for calling methods on a remote object

Virtual Proxy

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

Logging Proxy

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

