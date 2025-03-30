# Generics

DRY(Do not repeat yourself) is common practice among programmers primarily due to easier maintainability later on.

Generics are like type parameters which allow us to practice DRY more effectively.

## Generics Reduce Repetitive Code and Increase Type Safety

* Go is a statically typed language which means types and parameters are validated when code is compiled. Built-in types (maps, channels, slices) and functions like (`len`, `cap` or `make`) are able to work with different types of data.
* Only after 1.18, user-defined Go types and funnctions could  not work with different types of data.
* Without generics only way to avoid duplicate code would be to use interface.
* Example of a Tree implementation using Orderable Interface

````go
type Orderable interface {
    // Order returns:
    // a value < 0 when the Orderable is less than the supplied value,
    // a value > 0 when the Orderable is greater than the supplied value,
    // and 0 when the two values are equal.
    Order(any) int
}
````

```go
type Tree struct {
    val         Orderable
    left, right *Tree
}

func (t *Tree) Insert(val Orderable) *Tree {
    if t == nil {
        return &Tree{val: val}
    }

    switch comp := val.Order(t.val); {
    case comp < 0:
        t.left = t.left.Insert(val)
    case comp > 0:
        t.right = t.right.Insert(val)
    }
    return t
}
```

- Now with an `OrderableInt` type we can insert `int` values.

````go
type OrderableInt int

func (oi OrderableInt) Order(val any) int {
    return int(oi - val.(OrderableInt))
}

func main() {
    var it *Tree
    it = it.Insert(OrderableInt(5))
    it = it.Insert(OrderableInt(3))
    // etc...
}
````

- Above code does not allow compiler to validate inserted values into data structure are same or not :). So you can insert another instance like `OrderableString`

````go
type OrderableString string

func (os OrderableString) Order(val any) int {
    return strings.Compare(string(os), val.(string))
}

// inside main
var it *Tree
it = it.Insert(OrderableInt(5))
it = it.Insert(OrderableString("nope"))
````

- Above code compiles but will panic during runtime :

````go
panic: interface conversion: interface {} is main.OrderableInt, not string
````

- With generics, there’s a way to implement a data structure once for multiple types and detect incompatible data at compile time.

## Introducing Generics in Go

[Interesting Read](https://research.swtch.com/generic)

Example of Stack Implementation using Generic

````go
type Stack[T any] struct {
    vals []T
}

func (s *Stack[T]) Push(val T) { // note: how reciever is not Stack instead Stack[T]
    s.vals = append(s.vals, val)
}

func (s *Stack[T]) Pop() (T, bool) {
    if len(s.vals) == 0 {
        var zero T				// easiest way to fetch zero value of a type
        return zero, false
    }
    top := s.vals[len(s.vals)-1]
    s.vals = s.vals[:len(s.vals)-1]
    return top, true
}
````

- Now if you try to compile a code with something like this you will get compile errror

````go
func main() {
    var intStack Stack[int]
    intStack.Push(10)
    intStack.Push(20)
    intStack.Push(30)
    v, ok := intStack.Pop()
    fmt.Println(v, ok)
  
  	intStack.Push("nope")
}

// compile error
// cannot use "nope" (untyped string constant) as int value
//   in argument to intStack.Push
````

- Now add another method to check if a value exists in stack

````go
func (s Stack[T]) Contains(val T) bool {
    for _, v := range s.vals {
        if v == val {
            return true
        }
    }
    return false
}
````

- But above operation with fail with : `invalid operation: v == val (type parameter T is not comparable with ==)`
- This fails because any doesn’t define anything so can’t be compared. You need to use a built in comparable interface in universe block while defining Stack

````go
type Stack[T comparable] struct {
    vals []T
}
````

Full Code: [Playground](https://go.dev/play/p/Ep2_6Zftl5r)

## Generic Abstract Algorithms

Now we can implement generic algorithms for map, reduce and filter from type proposal

````go
// Map turns a []T1 to a []T2 using a mapping function.
// This function has two type parameters, T1 and T2.
// This works with slices of any type.
func Map[T1, T2 any](s []T1, f func(T1) T2) []T2 {
    r := make([]T2, len(s))
    for i, v := range s {
        r[i] = f(v)
    }
    return r
}

// Reduce reduces a []T1 to a single value using a reduction function.
func Reduce[T1, T2 any](s []T1, initializer T2, f func(T2, T1) T2) T2 {
    r := initializer
    for _, v := range s {
        r = f(r, v)
    }
    return r
}

// Filter filters values from a slice using a filter function.
// It returns a new slice with only the elements of s
// for which f returned true.
func Filter[T any](s []T, f func(T) bool) []T {
    var r []T
    for _, v := range s {
        if f(v) {
            r = append(r, v)
        }
    }
    return r
}
````

[Example](https://go.dev/play/p/MYYW3e7cpkX)

## Generics and Interfaces

- Any Interface can used as a Type Constraint, not just `any` or `comparable`

````go
// type thats holds two values of any type as long as those implement fmt.Stringer
type Pair[T fmt.Stringer] struct {
    Val1 T
    Val2 T
}
````

````go
// Interface with type parameter
type Differ[T any] interface {
    fmt.Stringer
    Diff(T) float64
}
// now we can use above interface to create a comparison function
func FindCloser[T Differ[T]](pair1, pair2 Pair[T]) Pair[T] {
    d1 := pair1.Val1.Diff(pair1.Val2)
    d2 := pair2.Val1.Diff(pair2.Val2)
    if d1 < d2 {
        return pair1
    }
    return pair2
}

// writing couple of types that meet differ interface
type Point2D struct {
    X, Y int
}

func (p2 Point2D) String() string {
    return fmt.Sprintf("{%d,%d}", p2.X, p2.Y)
}

func (p2 Point2D) Diff(from Point2D) float64 {
    x := p2.X - from.X
    y := p2.Y - from.Y
    return math.Sqrt(float64(x*x) + float64(y*y))
}

type Point3D struct {
    X, Y, Z int
}

func (p3 Point3D) String() string {
    return fmt.Sprintf("{%d,%d,%d}", p3.X, p3.Y, p3.Z)
}

func (p3 Point3D) Diff(from Point3D) float64 {
    x := p3.X - from.X
    y := p3.Y - from.Y
    z := p3.Z - from.Z
    return math.Sqrt(float64(x*x) + float64(y*y) + float64(z*z))
}
````

- Example Usage of above types

````go
func main() {
    pair2Da := Pair[Point2D]{Point2D{1, 1}, Point2D{5, 5}}
    pair2Db := Pair[Point2D]{Point2D{10, 10}, Point2D{15, 5}}
    closer := FindCloser(pair2Da, pair2Db)
    fmt.Println(closer)

    pair3Da := Pair[Point3D]{Point3D{1, 1, 10}, Point3D{5, 5, 0}}
    pair3Db := Pair[Point3D]{Point3D{10, 10, 10}, Point3D{11, 5, 0}}
    closer2 := FindCloser(pair3Da, pair3Db)
    fmt.Println(closer2)
}
````

## Use Type Terms to Specify Operators

* Go generics require specifying valid operators for a type

- **Type Elements & Operators:**

* Type elements define which types a parameter can accept and which operators are allowed.
* Example: This allows only integer types to use / and %.

```go
type Integer interface {
	int | int8 | int16 | int32 | int64 |
	uint | uint8 | uint16 | uint32 | uint64 | uintptr
}
```

- Generic divAndRemainder Function
	- Works for all integer types in Integer
````go
func divAndRemainder[T Integer](num, denom T) (T, T, error) {
    if denom == 0 {
        return 0, 0, errors.New("cannot divide by zero")
    }
    return num / denom, num % denom, nil
}
````

- **Handling User-Defined Types:**
  - By default, divAndRemainder(MyInt, MyInt) fails because MyInt is a custom type.
  - Fix this using ~ to allow underlying types:

````go
type Integer interface {
    ~int | ~uint | ~int64 | ~uint64
}
````

- Ordered Types for Comparisons: Define an Ordered interface for ==, !=, <, >, <=, >= operators:
  - NOTE: Go 1.21 includes the `cmp` package, while provides built-in comparison functions

````go
type Ordered interface {
    ~int | ~uint | ~float64 | ~string
}
````

- **Mixing Type Terms & Methods**: 
  - Example: Ensure a type has an int underlying type and a String() method:

````go
type PrintableInt interface {
    ~int
    String() string
}
````

- Compiler Enforcement

  - Declaring an impossible interface (e.g., int requiring a method) compiles but fails on use. Example.

    ````go
    type ImpossiblePrintableInt interface {
        int
        String() string
    }
    ````

  - This results in compile-time error when instantiated

- Beyond Primitives
  - Type terms can also be **slices, maps, arrays, channels, structs, or functions** to enforce specific types and methods.

## Type Inference and Generics

- Go supports **type inference** in generic function calls, similar to how := infers types. However, inference **fails when a type parameter is only used as a return type**, requiring explicit type arguments.
- **Example: When Type Inference Fails**

````go
type Integer interface {
    int | int8 | int16 | int32 | int64 | uint | uint8 | uint16 | uint32 | uint64
}

func Convert[T1, T2 Integer](in T1) T2 {
    return T2(in)
}

func main() {
    var a int = 10
    b := Convert[int, int64](a) // Explicit type arguments needed
    fmt.Println(b)
}
````

## Type Elements Limit Constants
* type elements limit which constants can be assigned to variables of generic type.
* Constants must be valid for all types in the constraint.
```go
func PlusOneThousand[T Integer](in T) T {
    return in + 1_000 // INVALID for 8-bit integers
}
```

## Combining Generic Functions with Generic Data Structures
* How to write a single tree function that works for every concrete type
* Write a generic function that compared two values and tells their order
```go
type OrderableFunc [T any] func(t1, t2 T) int
```
* With this `OrderableFunc` we can modify tree implementation into two types, `Tree` and `Node`
```go
type Tree[T any] struct {
	f OrderableFunc[T]
	root *Node[T]
}

type Node[T any] struct {
	val T
	left, right *Node[T]
}

// Tree constructor function
func NewTree[T any](f OrderableFunc[T]) *Tree[T] {
	return &Tree[T] {
		f: f,
		}
}

// Tree's methods use Node to do all the real work
func (t *Tree[T]) Add(v T) {
	t.root = t.root.Add(t.f, v)
}
func (t *Tree[T]) Contains(v T) {
	return t.root.Contains(t.f, v)
}
```

`Add` & `Contains` methods on `Node` are very similar to what we have seen.
```go
func (n *Node[T]) Add(f OrderableFunc[T], v T) *Node[T] {
    if n == nil {
        return &Node[T]{val: v}
    }
    switch r := f(v, n.val); {
    case r <= -1:
        n.left = n.left.Add(f, v)
    case r >= 1:
        n.right = n.right.Add(f, v)
    }
    return n
}

func (n *Node[T]) Contains(f OrderableFunc[T], v T) bool {
    if n == nil {
        return false
    }
    switch r := f(v, n.val); {
    case r <= -1:
        return n.left.Contains(f, v)
    case r >= 1:
        return n.right.Contains(f, v)
    }
    return true
}
```
* Now we need a function that matches `OrderableFunc` definition.
* Use `Compare` in the `cmp` package
```go
t1 := NewTree(cmp.Compare[int])
t1.Add(10)
t1.Add(30)
t1.Add(15)
fmt.Println(t1.Contains(15))
fmt.Println(t1.Contains(40))
```

For structs
* Either write a function that compares two items of struct and then pass that in `NewTree`
```go
type Person struct {
    Name string
    Age int
}

func OrderPeople(p1, p2 Person) int {
    out := cmp.Compare(p1.Name, p2.Name)
    if out == 0 {
        out = cmp.Compare(p1.Age, p2.Age)
    }
    return out
}

// usage
t2 := NewTree(OrderPeople)
t2.Add(Person{"Bob", 30})
t2.Add(Person{"Maria", 35})
t2.Add(Person{"Bob", 50})
fmt.Println(t2.Contains(Person{"Bob", 30}))
fmt.Println(t2.Contains(Person{"Fred", 25}))
```
* or, use a method expression to treat a method like a function.
```go
// method expression
func (p Person) Order(other Person) int {
    out := cmp.Compare(p.Name, other.Name)
    if out == 0 {
        out = cmp.Compare(p.Age, other.Age)
    }
    return out
}

// usage
t3 := NewTree(Person.Order)
t3.Add(Person{"Bob", 30})
t3.Add(Person{"Maria", 35})
t3.Add(Person{"Bob", 50})
fmt.Println(t3.Contains(Person{"Bob", 30}))
fmt.Println(t3.Contains(Person{"Fred", 25}))
```
## More on comparable
* Comparable Interfaces in Go
	- In Go, interfaces are comparable types.
	- Be cautious when using `==` and `!=` with interface types.
	- If an interface's underlying type is not comparable, it causes a runtime panic.
- Comparable Interface with Generics
	- Consider the example where `Thinger` is an interface with two implementations:
	    - `ThingerInt` (comparable)
	    - `ThingerSlice` (not comparable)
	- A generic function `Comparer[T comparable]` is defined to compare values.
	- Works fine with `int` and `ThingerInt`, but fails at compile-time with `ThingerSlice`.
	- However, `ThingerSlice` assigned to `Thinger` compiles but panics at runtime
- Why this Happens
	- The compiler only enforces `comparable` constraints at compile-time.
	- Once assigned to an interface, the underlying type’s comparability is not checked.
	- Results in runtime panic when comparing non-comparable underlying types
## Things that are left Out
1. **Operator Overloading**
    - Unlike Python, Ruby, or C++, Go does not support operator overloading.
    - Prevents misuse and maintains readability.
    - No way to overload `range` or indexing (`[]`) for custom types.
2. **Parameterized Methods**
    - Methods cannot have additional type parameters.
    - Example: `Map` and `Reduce` cannot be method chains on generic types.
    - Requires explicit function calls instead of fluent API chaining.
        
3. **Variadic Type Parameters** 
    - No support for variadic generic parameters.
    - Example: Cannot specify alternating types like `(string, int, string, int, ...)`.
    - All variadic parameters must match a single declared type.
4. **Other Missing Features**
    - **Specialization**: No type-specific versions of a function in addition to a generic version.
    - **Currying**: Cannot partially instantiate functions or types with some type parameters.
    - **Metaprogramming**: No code execution at compile-time to generate runtime code.
## Idiomatic Go and Generics
- Generics introduce new idiomatic Go practices but do not replace existing code.
- **Changes in Best Practices:**
    - Use `any` instead of `interface{}` for unspecified types.
    - Generics improve handling of different slice types in a single function.

- **Performance Considerations:**    
    - Switching an interface-based function to a generic function may not improve performance.
    - Example: `doubleAge(Ager)` vs. `doubleAgeGeneric[T Ager]` may slow execution by ~30% in Go 1.20.
    - Go generates unique functions only for different underlying types.
    - Pointer types share a single generated function, leading to runtime lookups.
- **Future Performance Improvements:**
    - Future Go versions may optimize generic runtime performance.
    - Always use benchmarks to measure impact.
## Adding Generics to Standard Library
- Go 1.18 introduced generics but made no API changes in the standard library.
- Go 1.21 added generic functions for common operations:
    - `Equal` and `EqualFunc` for comparing slices and maps.
    - `Insert`, `Delete`, and `DeleteFunc` for slice manipulation.
    - `maps.Clone` for efficiently copying maps.
    - `sync.OnceValue` and `sync.OnceValues` for executing functions once with generics.
- Future versions will likely expand generic usage in the standard library.
## Future Features Unlocked
- Generics may lead to **sum types** (a bounded set of possible types for a variable).
- Could improve handling of JSON fields that contain either a single value or a list.
- Allows type-safe handling of multiple types in a variable.
- Could enhance Go’s enum capabilities (similar to Rust and Swift).
- Requires further evaluation before adoption into Go.