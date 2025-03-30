# Types, Methods, And Interfaces

- Go is a statically typed languages with both built-in types and user-defined types.
- Go is designed to encourage best practices advocated by software engineers, avoiding inheritance while encouraging composition.

## Types in Go

- declaring struct is defining a user-defined types

````go
type Person struct {
    FirstName string
    LastName  string
    Age       int
}

type Score int
type Converter func(string)Score
````

- Go allows declaring type at any block level from package block down.

## Methods

- Methods can be defined on user types

````go
func (p Person) String() string {
  return fmt.Sprintf("%s %s, age %d", p.FirstName, p.LastName, p.Age)
}
````

- Method declaration is similar to function declaration with additional *receiver specification*. Reciever appears in b/w of `func` and method name.
- By convention, reciever name is short abbreviation of type’s name, usually its first letter. It is noidiomatic to use `this` or `self`
- Methods can only be defined at package block level, functions can be defined inside any block.
- Methods, functions can’t be overloaded. Same method names for different types are allowed but not two different methods with same name and type.

````go
p := Person{
    FirstName: "Fred",
    LastName:  "Fredson",
    Age:       52,
}
output := p.String()
````

### Pointer Receivers and Value Recievers

- If a method modifies the reciever or needs to handle *nil* instances, you must use a pointer reciever
- If a method doesn’t modify reciever, we can use value receiver.

- In Go, you can call a pointer receiver method on a value because Go automatically takes the address of the value. Similarly, when calling a value receiver method on a pointer, Go automatically dereferences the pointer to call the method.

### Code your Methods for nil instances

- If we call a method on `nil` instance, for value recievers it will raise a panic but for pointer recievers it can work if method is written to handle possibility of a `nil` instance.

````go
type IntTree struct {
    val         int
    left, right *IntTree
}

func (it *IntTree) Insert(val int) *IntTree {
    if it == nil {
        return &IntTree{val: val}
    }
    if val < it.val {
        it.left = it.left.Insert(val)
    } else if val > it.val {
        it.right = it.right.Insert(val)
    }
    return it
}
// declared with pointer reciever to handle nil values and doesn't modify tree
func (it *IntTree) Contains(val int) bool {
    switch {
    case it == nil:
        return false
    case val < it.val:
        return it.left.Contains(val)
    case val > it.val:
        return it.right.Contains(val)
    default:
        return true
    }
}
````

### Methods are Functions Too

- Methods can be used as a replacement for functions anytime the variable or parameter of a function type

````go
type Adder struct {
    start int
}

func (a Adder) AddTo(val int) int {
    return a.start + val
}

myAdder := Adder{start: 10}
fmt.Println(myAdder.AddTo(5)) // prints 15
````

- Usual practice: if program depends only on parameters, it should be functions but if it depends on startup values or changes mid program values, it should be stored in a struct, logic should be implemented as methods

### Type Declarations aren’t Inheritance

- we can declare a user-defined type based on another user-defined type

````go
type HighScore Score
type Employee Person
````

- declaring a type based on another type seems like inheritance but it is not. Even tho both have same underlying types. Types do not have any hierarchy
- In Go, you cannot assign an instance of type `HighScore` to a variable of type `Score` or vice-versa

### Types are Executable Documentation

- User-defined types act as documentation, clarifying code by providing meaningful names for concepts and data expectations. 
- They also help reduce repetition and highlight relationships between types when one is based on another.

## `iota` is for Enumeration - Sometimes

- Enums represent that a type can only have limited set of values. Go doesn’t have Enum type instead it uses `iota`, which lets you assign increasing value to a set of constants.
- when using `iota`, best practice is to first define a type based on `int`

````go
type MailCategory int
````

- Next use a `const` block to define a set of values

````go
const(
    Uncategorized MailCategory = iota		// value - 0
    Personal													// value - 1
    Spam
    Social
    Advertisements
)
````

- following first element all other elements neither the type nor a value assigned to it. When Go compiler works, it assigns and repeats the assignment while incrementing the counter from 0.
- Value of `iota` increments for each const in a `const` block, whether or not `iota` is used to define the value of a constant.

````go
const (
    Field1 = 0
  Field2 = 1 + iota		// 1 + iota(1) = 2
    Field3 = 20
    Field4						// takes value from previous const
    Field5 = iota			// again uses iota value
)

func main() {
    fmt.Println(Field1, Field2, Field3, Field4, Field5)
  // 0 2 20 20 4
}
````

- be careful while using iota and avoid using it as used in above example.
- Since we can assign literal expression to a const.

````go
type BitField int

const (
    Field1 BitField = 1 << iota // assigned 1
    Field2                      // assigned 2
    Field3                      // assigned 4
    Field4                      // assigned 8
)
````

## Use Embeddings for Composition

- From the book Design Patterns : *Favour Object Composition over class inheritance*
- While Go doesn’t have Inheritance we are left to used built-in composition and promotion options.

````go
type Employee struct {
    Name         string
    ID           string
}

func (e Employee) Description() string {
    return fmt.Sprintf("%s (%s)", e.Name, e.ID)
}

type Manager struct {
    Employee				// notice its not assigned. This makes it a embedded field
    Reports []Employee
}

func (m Manager) FindNewEmployees() []Employee {
    // do business logic
}
````

- Any fields or methods declared on embedded field are *promoted* to containing struct and can be invoked directly on it.

````go
m := Manager{
    Employee: Employee{
        Name: "Bob Bobson",
        ID:   "12345",
    },
    Reports: []Employee{},
}
fmt.Println(m.ID)            // prints 12345
fmt.Println(m.Description()) // prints Bob Bobson (12345
````

- If containing struct has fields or methods same as embedded field then you need to use embedded field’s type to refer to the obscured fields or methods

## Embedding is NOT Inheritance

- You can’t assign a variable of type `Manager` to a variable of type `Employee` if `Manager` is not a subtype of `Employee`. If you want to access the `Employee` properties or methods in a `Manager` object, you must do so explicitly. This violates the Liskov Substitution Principle.
- Furthermore, Go has no dynamic dispatch for concrete types. The mthods on embedded field have no idea they are embedded.
- In Go, concrete types don’t support dynamic dispatch, so methods on an embedded field don’t recognize they are embedded. If a method on the embedded field calls another method with the same name as one in the containing struct, the embedded method is invoked. 
- This means that while you can’t treat the outer type as the inner, the methods on the embedded field still count toward the method set of the containing struct, allowing it to implement interfaces.

## A Quick Lessons on Interfaces

- Implicit Interfaces are the only abstract type in Go
- Example: `Stringer` interface in the `fmt` package
```go
type Stringer interface {
	// list of methods that needs to be implemented
	String() string
}
```
* Example: `Counter` struct defined previously
	* method set of a pointer instances contains the methods defined with pointer and value receivers.
	* method set of a value instance contains only methods with value receiver.
```go
type Incrementor interface {
	Increment()
}

var myStringer fmt.Stringer
var myIncrementer Incrementer
pointerCounter := &Counter{}
valueCounter := Counter{}

myStringer = pointerCounter    // ok
myStringer = valueCounter      // ok
myIncrementer = pointerCounter // ok
myIncrementer = valueCounter   // compile-time error
// last-line fails because Counter does not implement Incrementer
```
## Interfaces Are Type-Safe Duck Typing
* Go's interfaces are special because they are implemented implicitly
* A concrete type doesn't declare that it implements an interface. 
* If concrete type has all method sets for an interface, the concrete type implements the interface & can be assigned to a variable or fields declared to be type of interface.
* This enable safety and decoupling, bridging functionality between both static & dynamic language.
* Advice from *Design Patterns*
	* favour composition over inheritance
	* program to an interface, not an interface (allows you to depend on behaviour, not on implementation, allowing to swap implementations)
* Dynamically typed languages like Python, Ruby & JS don't have interfaces, and rely on *duck typing*, which is based on expression. "If it walks like a duck and quacks like a duck, it's a duck"
* In Duck Typing, Concept is that you can pass an instance of a type as a parameter to a function as long as the function can find a method to invoke than it expect :
```python
class Logic:
	def process(self, data):
		# business logic
def program(logic): # doesn't care about type of logic
	# get data from somewhere
	logic.process(data)

logicToUse = Logic()
program(logicToUse)
```

* Java uses different pattern, They define an interface, create an implementation of the interface, but refer to interface only in client code.
* Dynamic language dev look at explicit interface in Java and don't see how can you refactor your code over time when you have explicit dependencies.
```java
public interface Logic {
    String process(String data);
}

public class LogicImpl implements Logic {
    public String process(String data) {
        // business logic
    }
}

public class Client {
    private final Logic logic; // Dependency on the interface, not the implementation
    // this type is the interface, not the implementation

    public Client(Logic logic) {
        this.logic = logic;
    }

    public void program() {
        // get data from somewhere
        this.logic.process(data);
    }
}

public static void main(String[] args) {
    Logic logic = new LogicImpl();
    Client client = new Client(logic);
    client.program();
}
```

* Go decided both approaches are correct, If program is going to grow and change over time, we should have flexibility to change implementations.
```go
type LogicProvider struct {}

func (lp LogicProvider) Process(data string) string {
    // business logic
}

type Logic interface {
    Process(data string) string
}

type Client struct{
    L Logic
}

func(c Client) Program() {
    // get data from somewhere
    c.L.Process(data)
}

main() {
    c := Client{
        L: LogicProvider{}, // we can swap out implementations
    }
    c.Program()
}
```

* Interfaces can be shared and it can become really powerful. If your code works with `io.Reader` and `io.Writer`, it will function correctly whether it is writing to a file on local disk or a value in memory.
* Furthermore, using standard interfaces encourages the _decorator pattern_. It is common in Go to write factory functions that take in an instance of an interface and return another type that implements the same interface.
```go
// example function declaration
func process(r io.Reader) error

// we can process data from a file with following code
r, err := os.Open(fileName)
if err != nil {
    return err
}
defer r.Close()
return process(r)
```
* `os.Open` returns a type of `os.File` which implements `io.Reader` interface, and can be used in any code that reads data.
* If file is g-zip compressed, you can wrap the `io.Reader` in another `io.Reader` and same code will read from a compressed file as well
```go
r, err := os.Open(fileName)
if err != nil {
    return err
}
defer r.Close()
gz, err := gzip.NewReader(r)
if err != nil {
    return err
}
defer gz.Close()
return process(gz)
```

## Embedding and Interfaces
* Interfaces can embed other interfaces.
```go
type Reader interface {
        Read(p []byte) (n int, err error)
}

type Closer interface {
        Close() error
}

type ReadCloser interface {
        Reader
        Closer
}
```

## Accept Interfaces Return Structs
* coined by Jack Lindamood in 2016 [Blog Link](https://medium.com/@cep21/preemptive-interface-anti-pattern-in-go-54c18ac0668a)
* Functions should accept interfaces but return concrete types.
* This provides flexibility in function inputs while ensuring stability in function outputs.
* **Why Accept Interfaces?**
	* Makes code more flexible and decoupled.
	* Explicitly declares required functionality.
	* Allows different implementations without modifying existing code.
* **Why Return Structs?**
	* Easier to evolve functions over time without breaking backward compatibility.
	* Adding new fields or methods to a struct does not break existing code.
	* Modifying an interface requires all implementations to be updated, leading to breaking changes.
* Exceptions
	* Some standard libraries (e.g., `database/sql/driver`) return interfaces due to compatibility requirements.
	* Errors (error interface) are an exception since different implementations may be returned.
* **Performance Considerations**:
	* Returning structs avoids heap allocations, improving performance.
	* Passing interfaces as function parameters causes heap allocations.
	* If performance issues arise due to heap allocations, consider switching to concrete type parameters.
* **Generics vs. This Pattern**
	* Developers from C++/Rust may try using generics.
	* In Go (as of v1.21), generics do not necessarily lead to better performance.

## Interfaces and nil
* **Nil as Zero Value**
	* Interfaces in Go can have nil as their zero value.
	* However, checking nil for interfaces is more complex than for concrete types.
* **Interface Representation in Go**
	* Interfaces are internally implemented as a struct with:
		* A **type** pointer (holds type information).
		* A **value** pointer (holds the actual value).
	* An interface is considered **nil only if both pointers are nil**.
* Example Behaviour
	*  Assigning pointerCounter (which is nil) to incrementer makes incrementer non-nil.
	* This happens because incrementer now holds a **non-nil type** with a **nil value**.
```go
var pointerCounter *Counter
fmt.Println(pointerCounter == nil) // true

var incrementer Incrementer
fmt.Println(incrementer == nil) // true

incrementer = pointerCounter
fmt.Println(incrementer == nil) // false
```

* **Method Invocation on nil Interfaces**
	* Calling a method on a nil interface causes a **panic**.
	* However, calling a method on a **non-nil interface** with a nil value may also cause a panic if the method does not handle nil properly.
* **Checking for nil Values Inside an Interface**
	* Since an interface with a non-nil type is not nil, detecting a nil value inside an interface is tricky.
	* **Reflection** must be used to check if the interface’s value is nil.

## Interfaces are comparable
* **Interfaces Can Be Compared**
	* Interfaces can be checked for equality using `==`
	* Two interface instances are equal **only if both their type and value are equal**.
	* An interface is nil only if both its **type** and **value** are nil
* **Comparable vs. Non-Comparable Types**
	* **Comparable**: Pointer types (e.g., *DoubleInt)
	* **Non-Comparable**: Slice types (e.g., DoubleIntSlice)
	* Comparing a *DoubleInt with a DoubleIntSlice results in false due to mismatched types.
```go
var di DoubleInt = 10
var di2 DoubleInt = 10
fmt.Println(&di == &di2) // false (different pointers)
```
* **Panic on Comparing Non-Comparable Types**
	* Slices (and other non-comparable types) **cannot be compared** and cause a **runtime panic**.
```go
var dis = DoubleIntSlice{1, 2, 3}
var dis2 = DoubleIntSlice{1, 2, 3}
fmt.Println(dis == dis2) // Runtime panic!
```
* **Interfaces as Map Keys**
	* Map keys must be **comparable**.
	* Map keys must be **comparable**.
	* If a non-comparable type is used as a key, a **runtime panic** occurs.
```go
m := map[Doubler]int{}
```
* Avoiding Panics
	* Be **cautious** when using == or != with interfaces
	* Future changes may introduce **non-comparable** implementations, leading to unexpected panics.
	* Use **reflection** (`reflect.Value.Comparable()`) to check comparability before comparisons.

## The Empty Interface Says Nothing
* In Go, `interface{}` (or any in Go 1.18+) allows storing values of any type.
```go
var i interface{}
i = 20
i = "hello"
i = struct {
    FirstName string
    LastName string
} {"Fred", "Fredson"}
```
*  It is commonly used for handling unknown types, such as reading JSON data.
```go
data := map[string]any{}
contents, err := os.ReadFile("testdata/sample.json")
if err != nil {
    return err
}
json.Unmarshal(contents, &data)
// the contents are now in the data map
```
* Avoid any when possible, as Go is strongly typed.
* If you see a function that takes in an empty interface, it’s likely using reflection to either populate or read the value.
## Types Assertions and Type Switches
* Type Assertions
	* Extracts a specific type from an interface.
	* Syntax: `value, ok := i.(Type)`, where ok is false if the assertion fails.
	* Direct assertion (`i.(Type)`) causes a panic if the type doesn’t match.
	* Prefer the comma ok idiom to avoid runtime errors.
* **Type Switches**
	* Used to handle multiple possible types.
	* Always include a default case to handle unexpected types.
```go
switch v := i.(type) {
case int:
    fmt.Println("Integer:", v)
case string:
    fmt.Println("String:", v)
default:
    fmt.Println("Unknown type")
}
```
## Use Type Assertions and Type Switches Sparingly
* **Use Type Assertions & Switches Infrequently**
	* Extracting concrete types from interfaces can make code harder to maintain.
	* Functions should declare required types explicitly instead of relying on assertions.
* **Checking for Additional Interface Implementations**
	* Used for optional interfaces, e.g., `io.WriterTo` in `io.Copy`, which optimizes data copying.
```go
if wt, ok := src.(WriterTo); ok {
    return wt.WriteTo(dst)
}
```
* **Evolving APIs with Optional Interfaces**
	* Older Go versions lacked context, so Go 1.8 introduced context-aware interfaces like StmtExecContext.
	* The standard library checks for new interface implementations and falls back if unavailable.
* **Drawbacks of Optional Interfaces**
	* Wrapping interfaces (e.g., `bufio.Reader` over `io.ReaderFrom`) can prevent optimizations.
	* Type assertions and switches don’t detect wrapped errors; use errors.Is or errors.As.
* **Type Switches for Limited Type Variants**
	* Used when an interface has only a few expected concrete implementations
	* Always include a default case to handle new types safely:
```go
switch val := t.val.(type) {
case number:
    return int(val), nil
case operator:
    left, _ := walkTree(t.lchild)
    right, _ := walkTree(t.rchild)
    return val.process(left, right), nil
default:
    return 0, errors.New("unknown node type")
}
```
* **Best Practices**
	* Use unexported interfaces with at least one unexported method to prevent unexpected implementations.
	* Prefer explicit interface contracts over runtime type checks.

## Function Types are a Bridge to Interfaces
 * **Methods on User-Defined Function Types**
	 * Go allows methods on any user-defined type, including function types.
	 * This enables functions to implement interfaces, making them more flexible.
 * **Functions as HTTP Handlers**
	 * The http.Handler interface defines the ServeHTTP method:
	 * A function can be converted into an http.Handler by defining a function type with a method:
	 * This allows simple functions, methods, or closures to serve as HTTP handlers.
```go
type Handler interface {
    ServeHTTP(http.ResponseWriter, *http.Request)
}
type HandlerFunc func(http.ResponseWriter, *http.Request)

func (f HandlerFunc) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    f(w, r)
}
```
* **Functions vs. Interfaces as Parameters**
	* Go encourages small interfaces, often with a single method.
	* A function parameter is good for simple operations (e.g., sort.Slice).
	* An interface should be used when the function needs access to additional dependencies or state.
	* The http.Handler example shows how an interface provides flexibility for complex processing.
* **When to Use Each Approach**
	* **Use a function type** when a simple function is sufficient (e.g., sorting)
	* **Use an interface** when multiple dependencies or behaviors are involved (e.g., HTTP handlers).
## Implicit Interfaces Make Dependency Injection Easier
*  **Importance of Decoupling**
	* Software requires maintenance for bug fixes, new features, and environment changes.
	* Decoupling ensures different parts of a program can change independently.
* **Dependency Injection (DI) in Go**
	* DI specifies dependencies explicitly, making code modular and easier to test.
	* Unlike other languages requiring frameworks, Go achieves DI easily using interfaces.
	* [The Dependency Inversion Principle](https://web.archive.org/web/20110714224327/http://www.objectmentor.com/resources/articles/dip.pdf)
* **Implicit Interfaces and DI**
	* Go’s implicit interfaces enable DI without explicit bindings between dependencies.
	* Example: LoggerAdapter allows functions to satisfy interfaces dynamically.
* **Structuring Code with Interfaces**
	* Define small, focused interfaces for dependencies (DataStore, Logger, Logic).
	* Implement business logic using interfaces rather than concrete types.
* **Testing Benefits**
	* DI makes testing easier by allowing mock implementations of interfaces
	* Example: A test logger can capture log output for validation
* **Go’s Practical Approach**
	* Go isn’t purely object-oriented, procedural, or functional—it is **practical**.
	* Focuses on simplicity, readability, and maintainability for large teams.
## Wire
* **Wire** (by Google) automates dependency injection using code generation.

## Go isn’t Particularly Object-Oriented (and That’s Great)
* From above discussions its clear Go can't categorize Go as a particular style of language
* It isn't strictly procedural language. At the same time lacks methods overriding, inheritance, or, well objects mans that it is also not OOP language.
* Go has function types and closure, but its not functional language either.
* If you had to label Go’s style, the best word to use is _practical_. It borrows concepts from many places with the overriding goal of creating a language that is simple, readable, and maintainable by large teams for many years.