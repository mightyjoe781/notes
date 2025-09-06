# Composite Types

## Arrays

- Arrays are little too rigid in Go and are not used directly.

````go
// all elements are zero
var x [3]int
// initialize with some variables
var x = [3]int{10, 20, 30}
// for sparse array (most elements are zero)
var x = [12]int{1, 5:4, 6, 10:100, 15}
// x = {1, 0, 0, 0, 0, 0, 4, 6, 0, 0, 0, 100, 15}

// we can use array literal for initialisation as well
var x = [...]int{10, 20, 30}
````

- Go only supports 1D array but we can simulate multidimensional arrays as

````go
var x [2][3]int
// this sounds weird, but some languages have true matrix support like Julia or Fortran
````

- Array elements can be accessed using bracket syntax: `x[2]`
- Length of array can be determined using builtin `len`

## Slices

- slices are useful as they can grow in size when needed. Length is not part of its type

````go
var x = []int{10, 20, 30}
// note: [...] makes an array not slices

var x = []int{1, 5:4, 6, 10:100, 15}

// simulating multidimensional slices
var x [][]int
````

- Builtins which are useful to be used with slice
    - `len` : `var size = len(x)`
    - `append` : `x = append(x, 10, 11, 12)` or appending other slice : `x = append(x, y...)`
    - `capacity`: number of consecutive memory locations reserved, its increased dynamically when length of slice reaches capacity. `var c = cap(x)`
    - `make` : create fixed size slices(can be resized) for initialization. `x := make([]int, 5)` or intialize with capacity 10. `x := make([]int, 5, 10)`
    - emptying slices: `clear(s)`
- declaring slices : usual way is to create a nil slice and then add data to it.

````go
var data[] int // a nil slice
// var x = []int{} : this is slice with zero length and capacity (not a nil slice). It is used in converting slice to JSON :)

data := []int{2,4,6,8}
````

- there are three possibilities while using slices
    - for using as a buffer, specify a nonzero length
    - if you want exact size, specify length and index into slice to set the values
    - other situations use `make` with a zero length and specified capacity. Allows appending to add items to slice as required
- slice expression : NOTE: slices are not copy but share the memory of the variables, so modification to other references will reflect in original slice

````go
x := []string{"a", "b", "c", "d"}
y := x[:2]
z := x[1:]
d := x[1:3]
e := x[:]	// THIS IS NOT A COPY, but a reference to memory
fmt.Println("x:", x) // x: [a b c d]
fmt.Println("y:", y) // y: [a b]
fmt.Println("z:", z) // z: [b c d]
fmt.Println("d:", d) // d: [b c]
fmt.Println("e:", e) // e: [a b c d]
````

- confusing slices

````go
x := []string{"a", "b", "c", "d"}
y := x[:2]
fmt.Println(cap(x), cap(y))
y = append(y, "z")
fmt.Println("x:", x)
fmt.Println("y:", y)

// Output
4 4	// both have same capacity, but when z is inserted capacity didn't change
// for y and instead c is overwritten
x: [a b z d]
y: [a b z]
````

- To avoid confusion with slices : either never use `append` with subslice or make sure `append` doesn’t cause an overwrite by using full slice expression (see example below)

````go
// full slice protects against append
x := make([]string, 0, 5) // 0 size and 5 capacity
x = append(x, "a", "b", "c", "d")
y := x[:2:2]
z := x[2:4:4]
````

- To create a `copy` of the slice

````go
x := []int{1, 2, 3, 4}
y := make([]int, 4)
num := copy(y, x) // (dst, src) format, returns size of the y
fmt.Println(y, num)
````

- convertin arrays to slices

````go
xArray := [4]int{5, 6, 7, 8}
xSlice := xArray[:]

// creating a slice from subset of array
// NOTE: they will have memory sharing properties as earlier
x := [4]int{5, 6, 7, 8}
y := x[:2]
z := x[2:]
````

- converting slices to arrays : data is always copied
- NOTE: size must be declared or else it will be compile-time error

````go
xSlice := []int{1, 2, 3, 4}
xArray := [4]int(xSlice)
smallArray := [2]int(xSlice)
xSlice[0] = 10
````

## Strings and Runes and Bytes

- Go Strings are not made up of runes instead they are a sequence of bytes (default formatting is based on UTF-8 unless changed)

````go
var s string = "Hello there"
// indexing
var b byte = s[6]
````

- strings support slicing and are zero-indexed but be careful while using slicing notation because strings are immutable and they don’t have modification problem as slices. Problem is a string is composed of sequence of bytes, while a code point in UTF-8 can be anywhere from one to four bytes long, so creates problem while dealing with languages other English or emojis
- Strings provide built-in `len`
- A single rune or byte can be converted to string
- A string can be converted back and forth to a slice of bytes a slice or runes

````go
var a rune = 'x'
var s string = string(a)
var b byte = 'y'
var s2 string = string(b)

// ---
var s string = "Hello, :)"
var bs []byte = []byte(s)
var rs []rune = []rune(s)
````

NOTE:

````go
// when int is converted to string it converts it to char
var x int = 65
var y = string(x)		// 'A' -- prints
````

## Maps

- maps are formatted as : `map[keyType]valueType`

````go
var nilMap map[string]int
// zero value for map is nil here and its of size 0.
// attempting to read nil map always returns zero value for value type's
// attempt to write nil map causes a panic
````

- using map literal : `totalWins := map[string]int{}` (NOTE: this is empty map literal not nil, it will allow writing and reading)

````go
teams := map[string][]string {
    "Orcas": []string{"Fred", "Ralph", "Bijou"},
    "Lions": []string{"Sarah", "Peter", "Billie"},
    "Kittens": []string{"Waldo", "Raul", "Ze"},
}
````

- Creating map with some default size: `ages := make(map[int][]string, 10)` (this map is still 10 length but can grow beyond specified size)
- Similarity in maps and slices
    - grows in size as more key-value pairs are added
    - we specify size of map druing declaration as well
    - passing `len` function a map provides its size
    - zero value of map is `nil`
    - maps are not comparable, but you can check nullability
- key of the map can be any comparable type not a slice or another map

### Reading/Writing a Map

````go
totalWins := map[string]int{}
totalWins["Orcas"] = 1
totalWins["Lions"] = 2
fmt.Println(totalWins["Orcas"])
fmt.Println(totalWins["Kittens"])
totalWins["Kittens"]++
fmt.Println(totalWins["Kittens"])
totalWins["Lions"] = 3
fmt.Println(totalWins["Lions"])
````

### Comma OK Idiom

````go
// map returns zero value of valuetype in case key is not there
// we can use comma ok idiom to check if key is not in map
m := map[string]int{
    "hello": 5,
    "world": 0,
}
v, ok := m["hello"]
fmt.Println(v, ok)

v, ok = m["world"]
fmt.Println(v, ok)

v, ok = m["goodbye"]
fmt.Println(v, ok)
````

### Deleting from Maps

````go
m := map[string]int{
    "hello": 5,
    "world": 10,
}
delete(m, "hello")
````

### Emptying a Map

```go
m := map[string]int{
    "hello": 5,
    "world": 10,
}
fmt.Println(m, len(m))
clear(m)
fmt.Println(m, len(m))
```

### Comparing Maps

```go
m := map[string]int{
    "hello": 5,
    "world": 10,
}
n := map[string]int{
    "world": 10,
    "hello": 5,
}
fmt.Println(maps.Equal(m, n)) // prints true
```

### Using Maps as Sets

````go
// Go doesn't have sets
intSet := map[int]bool{}
vals := []int{5, 10, 2, 5, 8, 7, 3, 9, 1, 2, 10}
for _, v := range vals {
    intSet[v] = true
}
fmt.Println(len(vals), len(intSet))
fmt.Println(intSet[5])
fmt.Println(intSet[500])
if intSet[100] {
    fmt.Println("100 is in the set")
}
````

## Structs

- Go syntax for structs

````go
type person struct {
    name string
    age  int
    pet  string
}
````

- It is defined by keyword `type`, the name of struct, and `struct` keyword with a pair of braces `{}`
- NOTE: no comma separated field unlike map declarations

````go
// declaring variables out of struct

var fred person	// gets zero value of struct i.e. zero value of each field
bob := person{}	// struct literal to assign to the variables
// note unlike maps, there is no difference if no-value is assigned to fred or zero value assigned to bob
julia := person{
    "Julia",
    40,
    "cat",
}
// NOTE: every field must be specified in struct declaration in above format
````

- another style to declare structs

````go
beth := person{
    age:  30,
    name: "Beth",
}
// no order restriction in this format
// unassigned variables get their zero values
````

- Struct is accessed as `bob.name = "Bob"`

### Anonymous Structs

```go
// this notation assigns struct to a variable
var person struct {
    name string
    age  int
    pet  string
}

person.name = "bob"
person.age = 50
person.pet = "dog"

// another way
pet := struct {
    name string
    kind string
}{
    name: "Fido",
    kind: "dog",
}
```

- Anonymous Structs are useful in two situation, translating external data to a struct or a struct into external data (JSON/Protocol Buffers, also known as *unmarshling* and *marshling* data. Second is writing tests where this is used.

### Comparing and Converting Structs

- Struct is comparable depends on its fields (without slice or map fields)
- Unlike Python there is no magic method that we can override to implement or redefine `==` or `!=`
- Go does allow you to perform a type conversion from one struct type to another *if the fields of both structs have the same names, order, and types*
- Anonymous structs add a small twist: if two struct variables are being compared and at least one has a type  that’s an anonymous struct, you can compare them without a type  conversion if the fields of both structs have the same names, order, and types.