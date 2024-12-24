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

- 
- 



## Interfaces Are Type-Safe Duck Typing





## Embedding and Interfaces





## Accept Interfaces Return Structs

## Interfaces and nil

## Interfaces are comparable

## The Empty Interface Says Nothing

## Types Assertions and Type Switches

## Use Type Assertions and Type Switches Sparingly

## Function Types are a Bridge to Interfaces

## Implicit Interfaces Make Dependency Injection Easier

## Wire

## Go isn’t Particularly Object-Oriented (and That’s Great)