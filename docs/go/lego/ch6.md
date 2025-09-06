# Pointers

## A Quick Pointer Primer

- A *pointer* is a variable that holds the location in memory where a value is stored.
- different types of variables will take up different amounts of memory. e.g. `32-bit int` is `4 bytes` and `boolean` is stored in only `1 byte` (smallest memory that can be addressed)

````go
var x int32 = 10
var y bool = true
pointerX := &x
pointerY := &y
var pointerZ *string
````

- zero value for a pointer is `nil`. NOTE: Unlike `NULL` in C, `nil` is not another name for 0. you can’t covert it back and forth
- Most of Go’s pointer syntax is borrowed from C and C++. Go has its own garbage collecter so most of the memory management is handled, furthermore many memory *pointer arithmetic* is not allowed in Go.
- `&` : address operator, `*` is called as *dereferences*

````go
x := 10
pointer := &x
fmt.Println(pointer) // print address
fmt.Println(*pointer) // dereference the address : print 10
````

- before dereferencing make sure pointer is not nil (otherwise program will panic)
- pointer type starts with `*`

````go
x := 10
var pointer *int
pointer = &x

// we use `new` creates a pointer variable

var x = new(int)
fmt.Println(x == nil)	// prints false
fmt.Println(*x)			// prints 0
````

- for structs we can use `&` before a struct literal to create a pointer instance
- we can’t use `&` before constanst or primitive literal because they don’t have memory addresses. 
- There are two ways around this, introducing a variable to hold constant values or create a generic helper function as shown below

````go
func makePointer[T any](t T) *T {
  return &t
}
````

## Don’t Fear the Pointers

- Behaviour of function parameters in Java, Python, JS and Ruby
    - If we pass instance of class to a function, and change a field the change is reflected in variable passed in
    - If we try reassign that variable, change will not be reflected
    - If we pass `nil/null/None` for a parameter value, setting the parameter itself to a new value doesn’t modify the variable in calling function

````python
class Foo:
    def __init__(self, x):
        self.x = x


def outer():
    f = Foo(10)
    inner1(f)
    print(f.x)	# output 20 : instance fields are changed
    inner2(f)
    print(f.x)	# output 20 : no change to instance
    g = None
    inner2(g)
    print(g is None)	# True


def inner1(f):
    f.x = 20


def inner2(f):
    f = Foo(30)


outer()
````

- Another interesting point in Java/Javascript, ther is a difference in behaviour betweeen primitive types and classes (python/ruby doesn’t have primitive values but use immutable instances to simulate them)

## Pointers Indicate Mutable Parameters

- Go constants provide names for literal expressions that can be calculated at compile time. There is no mechanism to declare other kinds of values as immutable.
- The lack of immutable declarations in Go might seem problematic, but the choice between value and pointer parameter types addresses the issue. Mutable objects are fine if used entirely locally within a method and with only one reference to the object. Instead of declaring variables and parameters as immutable, Go developers use pointers to indicate that a parameter is mutable.
- When passing a nil pointer to a function, you cannot make the value non-nil. You can reassign the value only if there was a value already assigned to the pointer.

````go
func failedUpdate(g *int) {
  x := 10
  g = &x
}
func main() {
  var f *int // f is nil pointer
  failedUpdate(f)
  fmt.Println(f)	// prints nil
}
````

- If you want the value assigned to a pointer parameter to persist after the function exits, you must dereference the pointer and set the value. Changing the pointer affects only the copy, not the original. Dereferencing puts the new value in the memory location pointed to by both the original and the copy.

````go
func updateValue(g *int) {
    // Dereferencing the pointer to update the value it points to
    *g = 42
}

func main() {
    var f int = 10
    fmt.Println("Before update:", f) // prints: Before update: 10
    
    // Passing the address of f to the function
    updateValue(&f) 
    fmt.Println("After update:", f) // prints: After update: 42
}
````

## Pointers are a Last Resort

- pointer make program harder to understand, can create additional work for garbage collector
- rather than populating struct by passign a pointer to it into a function, have the function instantiate and return the struct

````go
// don't do this
func MakeFoo(f *Foo) error {
  f.Field1 = 'val'
  f.Field2 = 20
  return nil
}

func MakeFoo() (Foo, error) {
  f := Foo {
    Field1: "val",
    Field2: 20
  }
  return f, nil
}
````

- only use pointers paramters to modify a variable when function expects an interface (exmaples while working with JSON)

## Pointers Passing Performance

- when a struct is very large to be passed as copy or return value is too large, we can use pointers to improve performance.
- Behaviour to return pointer vs value is very interesting, for data structures smaller than 10 megabytes, it is actually slower to return a pointer type than a value type. This behaviour flips as size of DS increases
- To run performance test : `go test ./... -bench=.`

## The Zero Value v/s No Value

- Go pointers are useful to distinguish between zero value and no value. If this distinction is required, its better to use a pointer set to `nil`
- If a `nil` pointer is passed into function via a parameter or a field on a parameter, you cannot set the value within the function, as there’s nowhere to store the values. If a non-nil value is passed in for the pointer, do not modify it unless you document the behaviour.
- JSON conversions are exception to above rules due to its marshalling and unmarshalling usages of it.

## Difference Between Maps and Slices

- Any modifications made to a map that’s passed to a function are reflected in original variable because maps are implemented as a pointer to a struct. Be careful on using maps for input parameters or return values especially on public APIs.

- Passing a slice to a function has more complicated behaviour
    - any modifications to the slice’s contents is reflected in original variable but using `append` to change the length isn’t reflected in the original variables, even if capacity greater than its length
    - A slice is implemented as with three fields
        - `int` : length
        - `int` : capacity
        - `pointer` : block of memory
    - when slice is passed to function a copy of len, capacity is passed but when changes made to copy and some items are appended to the the copy array but those variables (capacity) are not reflected in original. But notice because of pointer values of original arrays get updated due to pointer.

## Slices as Buffer

In Many languages while reading data from external source we have this syntax

````go
r = open_resource() // could be network or a file
while r.has_data() {
  data_chunk = r.next_chunk()
  process(data_chunk)
}
close(r)
````

- Problem with above code reallocating `data_chunk` every time, even tho each one is used once in process. Garbage collected languages handle those allocations automatically, but the work still needs to be done to clean them up when you are done processing
- writing idiomatic Go means avoiding unneeded allocations, we can use slice of bytes as buffer to read data from the data source.

````go
file, err := os.Open(fileName)
if err != nil {
  return err
}
defer file.Close()
data := make([]byte, 100)

for {
  count, err := file.Read(data)
  process(data[:count])
  if err != nil {
    if errors.ls(err, io.EOF) {
      return nil
    }
    return err
  }
}
````



## Reducing the Garbage Collector’s Workload

- Using buffers is one way to reduce the garbage collector's workload. Garbage refers to *data without any pointers pointing to it*.
- Memory in Go is of two types: *heap* and *stack*. The *stack* is a consecutive block of memory shared by function calls in a thread, with fast and simple allocation tracked by a *stack pointer*. When a function is called, a new *stack frame* is created for its data, storing local variables and parameters.
- To store data on the stack, its size must be known at compile time. Go's value types (primitives, arrays, structs) have fixed sizes and can be allocated on the stack. Pointer sizes are also known and stored on the stack.
- Data on the heap remains valid as long as it can be traced back to a pointer on the stack. Once no stack variables point to the data, it becomes *garbage*, and the garbage collector clears it.
- Go's *escape analysis* isn't perfect; sometimes, data that could be on the stack escapes to the heap. The compiler errs on the side of caution to avoid memory corruption by not leaving potentially needed heap data on the stack. Newer Go releases improve escape analysis.
- There are many garbage collection algorithms which can be broadly categorized as :
    - those designed for higher throughput
    - lower latency
- Computer hardware reads memory fastest sequentially. A slice of structs in Go has data laid out sequentially in memory, making it fast to load and process. In contrast, a slice of pointers to structs scatters data across RAM, making access much slower.
- This approach of writing hardware-aware software is called mechanical sympathy. Martin Thompson applied this term to software development, emphasizing the importance of understanding hardware for optimal performance.
- In Go, following best practices naturally aligns with mechanical sympathy. Unlike Go, Java stores objects as pointers, allocating data on the heap, which burdens the garbage collector. Java's List interface and sequential data types in Python, Ruby, and JavaScript also suffer from inefficient memory access due to pointer-based implementations.
- Go encourages sparing use of pointers to reduce the garbage collector's workload by storing as much data on the stack as possible. Slices of structs or primitive types have their data aligned for rapid access. Go's garbage collector is optimized for quick returns rather than gathering the most garbage, and the key is to create less garbage initially.
- For more on heap vs. stack allocation and escape analysis in Go, refer to blog posts by Bill Kennedy of Ardan Labs and Achille Roussel and Rick Branson of Segment.
- https://research.google/pubs/the-tail-at-scale/
- https://www.forrestthewoods.com/blog/memory-bandwidth-napkin-math/
- https://www.ardanlabs.com/blog/2017/05/language-mechanics-on-stacks-and-pointers.html
- https://segment.com/blog/allocation-efficiency-in-high-performance-go-services/

## Tuning the Garbage Collector

- **Garbage Collection Timing**: The Go garbage collector doesn’t reclaim memory immediately but allows garbage to accumulate for better performance. The heap typically contains both live and unneeded memory. 

- **GOGC Setting**: Users can control heap size with the GOGC environment variable. It uses the formula `CURRENT_HEAP_SIZE + CURRENT_HEAP_SIZE*GOGC/100` to determine when the next garbage collection cycle occurs. By default, GOGC is set to 100, meaning the heap size roughly doubles before the next collection. Adjusting GOGC changes the target heap size and CPU time spent on garbage collection. Setting GOGC to off disables garbage collection, speeding up programs but risking excessive memory usage in long-running processes.

- **GOMEMLIMIT Setting**: This sets a limit on total memory usage, similar to Java's -Xmx argument. It is specified in bytes or with suffixes (e.g., GiB). By default, it’s effectively unlimited. Limiting memory prevents the heap from growing too large, avoiding swapping to disk and potential crashes. 

- **Thrashing Prevention**: GOMEMLIMIT is a soft limit that can be exceeded to prevent thrashing, where the garbage collector runs continuously. Set GOMEMLIMIT below the maximum available memory to avoid this issue.

- **Combined Use**: The best practice is to use both GOGC and GOMEMLIMIT together to balance garbage collection pace and memory limits, ensuring consistent performance. More details are available in “A Guide to the Go Garbage Collector” by Go’s development team.

- https://go.dev/doc/gc-guide

