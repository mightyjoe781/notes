# Functions

## Declaring and Calling Functions

- Every Go program starts from `main` function

````go
func div(num int, denom int) int {
  if denom == 0 {
    return 0
  }
  return num/denom
}
````

- `return` is optional for function which do not return any value e.g. `main` function

````go
// no input params or return values
func main() {
    result := div(5, 2)
    fmt.Println(result)
}
````

````go
// NOTE if both params are of same type this also works
func div(num, denom int) int {
````

### Simulating Named and Optional Parameters

- Go doesn’t have : named and optional input parameters!
- Below example shows an exception to above rule as structs get their default zero values.

````go
type MyFuncOpts struct {
  FirstName string
  LastName string
  Age int
}

func MyFunc(opts MyFuncOpts) error {
  // do something
}

func main() {
  MyFunc(MyFuncOpts{
    LastName: 'patel',
    Age: 50,
  })
  MyFunc(MyFuncOpts{
    FirstName: 'Joe',
    LastName: 'Smith',
  })
}
````

### Variadic Input Parameters and Slices

- Go supports *variadic* parameters but they must be last (or only) parameter in the input parameter list.
- We indicate it as `...` before the type

````go
func addTo(base int, vals ...int) []int {
  out := make([]int, 0, len(vals))
  for _, v := range vals {
    out = append(out, base + v)
  }
  return out
}
````

````go
func main() {
    fmt.Println(addTo(3))
    fmt.Println(addTo(3, 2))
    fmt.Println(addTo(3, 2, 4, 6, 8))
    a := []int{4, 3}
    fmt.Println(addTo(3, a...))
    fmt.Println(addTo(3, []int{1, 2, 3, 4, 5}...))
}
````

### Multiple Return Values

````go
func divMod(num, denom int) (int, int, error) {
  if denom == 0 {
    return 0, 0, errors.New("cannot divide by zero")
  }
  return num/denom, num % denom, nil
}

func main() {
  result, remainder, err := divAndRemainder(5, 2)
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
  fmt.Println(result, remainder)
}
````

### Multiple Return Values are Multiple Values

- In language like python return value is a tuple out of which it is optional unpack as many required values
- If you assign multiple value to one variable in Go, it will give runtime-error

````python
q, r = divmod(5, 2)
# q, r both will have values (ints)
v = divmod(5, 2)  # v->tuple of values
````

### Ignoring Returned Values

- you can use `_` to ignore returned values if not referenced/used anywhere
- `result, _, err := divAndRemainder(5, 2)`
- NOTE: but Go does implicitly allows dropping all return values : `divAndRemainder(5, 2)`

### Named Return Values

- Go allows you name the return values

````go
func divAndRemainder(num, denom int) (result int, remainder int, err error) {
    if denom == 0 {
        err = errors.New("cannot divide by zero")
        return result, remainder, err
    }
    result, remainder = num/denom, num%denom
    return result, remainder, err
}
````

- Named Return values give a way to declare *intent* to use and hold values, but they don’t require you to use them i.e. I can return `0, 0, nil` and function will work totally fine.

### Blank Returns - Never Use These!

- If you use named return values, you need to be aware of one severe misfeature in Go: blank (naked) returns. If you do use `return` then it will return last assigned values to the named return values

````go
func divAndRemainder(num, denom int) (result int, remainder int, err error) {
    if denom == 0 {
        err = errors.New("cannot divide by zero")
        return
    }
    result, remainder = num/denom, num%denom
    return
}
````

## Functions are Values

- type of function is built out of keyword `func` and the types of parameters and return values. This combination is called *signature* of the function

````go
var myFuncVariable func(string) int
````

````go
func f1(a string) int {
    return len(a)
}

func f2(a string) int {
    total := 0
    for _, v := range a {
        total += int(v)
    }
    return total
}

func main() {
    var myFuncVariable func(string) int
    myFuncVariable = f1
    result := myFuncVariable("Hello")
    fmt.Println(result)

    myFuncVariable = f2
    result = myFuncVariable("Hello")
    fmt.Println(result)
}
````

Another Interesting Piece of Code

````go
func add(i int, j int) int { return i + j }
func sub(i int, j int) int { return i - j }
func mul(i int, j int) int { return i * j }
func div(i int, j int) int { return i / j }

// operator factory
var opMap = map[string]func(int, int) int{
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
}

func main() {
    expressions := [][]string{
        {"2", "+", "3"},
        {"2", "-", "3"},
        {"2", "*", "3"},
        {"2", "/", "3"},
        {"2", "%", "3"},
        {"two", "+", "three"},
        {"5"},
    }
    for _, expression := range expressions {
        if len(expression) != 3 {
            fmt.Println("invalid expression:", expression)
            continue
        }
        p1, err := strconv.Atoi(expression[0]) // Atoi -> converts string to number
        if err != nil {
            fmt.Println(err)
            continue
        }
        op := expression[1]
        opFunc, ok := opMap[op]	 // pick up function based of operator
        if !ok {
            fmt.Println("unsupported operator:", op)
            continue
        }
        p2, err := strconv.Atoi(expression[2])
        if err != nil {
            fmt.Println(err)
            continue
        }
        result := opFunc(p1, p2)
        fmt.Println(result)
    }
}
````

### Functions Type Declaration

- just as `struct` we can use `type` keyword to define a function type too

````go
type opFuncType func(int, int) int

// then we can rewrite
var opMap = map[string] opFuncType {
  // define map of operators
}
````

### Anonymous Functions

````go
// inner functions are anonymous
func main() {
  f := func(j int) {
    fmt.Println("printing",j,"from inside of an anonymous function")
  }
  for i:= 0; i < 5; i++ {
    f(i)
  }
}

// there is no need to assign anonymous function as well, normally we don't prefer this
func main() {
  for i := 0; i < 5; i++ {
    func(j int) {
      fmt.Println("printing", j, "from inside of an anonymous function")
    } (i)
  }
}
````

- usually we don’t do anonymous function without declaring because you are well off removing them completely and call the code.
- Assigning anonymous function to variables is useful in two scenarios
  - `defer` statements
  - launching goroutines
- Since we declare variables at package scope, we can also declare package scope variables that are assigned anonymous functions

````go
var (
    add = func(i, j int) int { return i + j }
    sub = func(i, j int) int { return i - j }
    mul = func(i, j int) int { return i * j }
    div = func(i, j int) int { return i / j }
)

func main() {
    x := add(2, 3)
    fmt.Println(x)
}
// later on we can monkey patch the add variables by redefining it if we require
````

## Closures

- function declared inside are special and are called as *closures*, as they are able to access and modify declared variables outside their scope.

````go
func main() {
    a := 20
    f := func() {
        fmt.Println(a)
        a = 30
    }
    f()
    fmt.Println(a)
}
// outputs
// 20
// 30

// ---- Now 
func main() {
    a := 20
    f := func() {
        fmt.Println(a)
        a := 30 // this is shadowing not closure -> this creates new a which shadows previous a
        fmt.Println(a)
    }
    f()
    fmt.Println(a)
}

````

- Use of Closure Example : https://github.com/jonbodner/my_lisp/blob/master/scanner/scanner.go

### Passing Functions as Parameters

- since functions are values and we can specify the type of function using its parameter and return types, you can pass functions as parameters into functions.
- Famous example would be a sort function that takes comparator function as input and uses that to compare.

````go
type Person struct {
    FirstName string
    LastName  string
    Age       int
}

people := []Person{
    {"Pat", "Patterson", 37},
    {"Tracy", "Bobdaughter", 23},
    {"Fred", "Fredson", 18},
}
fmt.Println(people)

// sort by last name
// example of closure being passed to sort
sort.Slice(people, func(i, j int) bool {
    return people[i].LastName < people[j].LastName
})
fmt.Println(people)
````

### Returning Functions as Parameters

- we can also return a closure from a function as well

````go
func makeMult(base int) func(int) int {
    return func(factor int) int {
        return base * factor
    }
}

func main() {
    twoBase := makeMult(2)
    threeBase := makeMult(3)
    for i := 0; i < 3; i++ {
        fmt.Println(twoBase(i), threeBase(i))
    }
}
````

## defer

- programs often create temporary resources, like files or network connections, that need to be cleaned up. This cleanup has to happen, no matter how many exit point a function has or whether it exited successfully or not.
- Python has Context Manager that are useful to do above task, or `else` block in `try-catch` or `__enter__`/`__exit__` dunder methods in objects

````go
func main() {
    if len(os.Args) < 2 {
        log.Fatal("no file specified")
    }
    f, err := os.Open(os.Args[1])
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()	// always close file no matter what!
    data := make([]byte, 2048)
    for {
        count, err := f.Read(data)
        os.Stdout.Write(data[:count])
        if err != nil {
            if err != io.EOF {
                log.Fatal(err)
            }
            break
        }
    }
}
````

- we can use a function, closure or a method with `defer`
- we can defer multiple functions in a Go functions, They run in `LIFO` order.

````go
func DoSomeInserts(ctx context.Context, db *sql.DB, value1, value2 string)
                  (err error) {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer func() {
        if err == nil {
            err = tx.Commit()
        }
        if err != nil {
            tx.Rollback()
        }
    }()
    _, err = tx.ExecContext(ctx, "INSERT INTO FOO (val) values $1", value1)
    if err != nil {
        return err
    }
    // use tx to do more database inserts here
    return nil
}
````

Another Common Pattern in Go is

````go
func getFile(name string) (*os.File, func(), error) {
    file, err := os.Open(name)
    if err != nil {
        return nil, nil, err
    }
    return file, func() {
        file.Close()
    }, nil
}


// inside main now
f, closer, err := getFile(os.Args[1])
if err != nil {
    log.Fatal(err)
}
defer closer()
````

## Go is call by value

- Go *always* makes a copy of value of variable passed as parameter to function
- But for maps and slices passed changes are reflected except slices can’t be lengthened.
- This behaviour difference is due to how maps and slices are implemented as a pointer.