# Errors

## How to Handle Errors: The Basics

- Go handles errors by returning a value of type `error`. If fuction executes as expected, `nil` is returned for error parameter. If something goes wrong, error value is returned.
- Calling function checks the error return value by comparing it to `nil`, handling the error or returning another error of its own.

````go
func calcRemainderAndMod(numerator, denominator int) (int, int, error) {
    if denominator == 0 {
        return 0, 0, errors.New("denominator is 0")
    }
    return numerator / denominator, numerator % denominator, nil
}
````

- NOTE: Error messages should not be capitalized nor should they end with punctuations. In most cases set return value to their zero values (except in case of sentinel errors).

````go
// example of checking error
num := 20
den := 3
rem, mod, err := calcRemaindereAndMod(num, den)
if err != nil {
  fmt.Println(err)
  os.Exit(1)
}
fmt.Println(remainder, mod)
````

- `error` is a built-in interface that defines a single method.

````go
type error interface {
    Error() string
}
````

- Anything that implements this interface is considered an error. The reason you return `nil` from a function to indicate that no error occurred is that `nil` is zero value of any interface type.

#### Why go uses returned error instead of thrown exception ?

- exception add at least one new code path through code. These paths are sometimes unclear.This produces code that crashes in surprising ways when exception is not handled correctly.
- Go compiler requires all variables to be read. Making returned values forces devs to either check and handle error condition or make it explicit that they are ignoring errors by using `_`

## Use Strings for Simple Errors

- Go standard library has two ways to create error from string
    - `errors.New` function takes string and returns `error`. String you provide will be returned when you call `Error` method on returned error instance. `fmt.Println` automatically calls `Error` method.
    - `fmt.Errorf` function allows to include runtime information in the error message by using `fmt.Printf` verbs to format an error string.

## Sentinel Errors

- some errors signal that processing cannot continue due to problem with current state.

- sentinel errors are few variables that are declared at package level. By convention, their names start with `Err` (except `io.EOF`) They should be treated as read-only.
- Example: `ErrFormat` is raised when `archive/zip` encounters data which doesn’t have zip data.

````go
data := []byte("This is not a zip file")
notAZipFile := bytes.NewReader(data)
_, err := zip.NewReader(notAZipFile, int64(len(data)))
if err == zip.ErrFormat {
    fmt.Println("Told you so")
}
````

## Errors are values

- Since `error` is an interface, you can define your own errors that include additional information for logging  or error handling. For example implementing error codes.

````go
// enumeration to represent status codes
type Status int

const (
    InvalidLogin Status = iota + 1
    NotFound
)

// define StatusErr to hold this value
type StatusErr struct {
    Status    Status
    Message   string
}

func (se StatusErr) Error() string {
    return se.Message
}

````

````go
// usage
token, err := login(uid, pwd)
if err != nil {
    return nil, StatusErr{
        Status:    InvalidLogin,
        Message: fmt.Sprintf("invalid credentials for user %s", uid),
    }
}

````

NOTE: When using custom errors, never define a variable to be of the type of your custom error. Either explicitly return `nil` when no error occurs or define the variable to be of type `error`.

## Wrapping Errors

- Preserving an error and adding information to it is called as wrapping an error.
- A series of wrapped errors, it is called an *error tree*
- Ex - The `fmt.Errorf` function has special verb, `%w`. Its used to create an error whose formatted string includes the formatted string of another error.
- Standard library has a function for unwrapping functions in `errors` package.

````go
func fileChecker(name string) error {
    f, err := os.Open(name)
    if err != nil {
        return fmt.Errorf("in fileChecker: %w", err)
    }
    f.Close()
    return nil
}

func main() {
    err := fileChecker("not_here.txt")
    if err != nil {
        fmt.Println(err)
        if wrappedErr := errors.Unwrap(err); wrappedErr != nil {
            fmt.Println(wrappedErr)
        }
    }
}
````

- If you want to wrap an error with your custom error type, your error type needs to implement the method `Unwrap`
- NOTE: You don’t usually call `errors.Unwrap` directly. Instead, you use `errors.Is` and `errors.As` to find a specific wrapped error. I’ll talk about these two functions in the next section.

- It is not necessary to wrap all errors, there could be implementation details which are not relevant for the current context. You could use `fmt.Errorf` with the `%v` verb instead of `%w`

## Wrapping Multiple Errors

- Ex- in case of fieldValidator we need to validate and return a single error containing all invalid fields.
- Since standard function returns an `error` rather than an array of error, we can merge multiple errors into single error using `errors.Join` function.

````go
type Person struct {
    FirstName string
    LastName  string
    Age       int
}

func ValidatePerson(p Person) error {
    var errs []error // never use your own err types in declartion, this is fine
    if len(p.FirstName) == 0 {
        errs = append(errs, errors.New("field FirstName cannot be empty"))
    }
    if len(p.LastName) == 0 {
        errs = append(errs, errors.New("field LastName cannot be empty"))
    }
    if p.Age < 0 {
        errs = append(errs, errors.New("field Age cannot be negative"))
    }
    if len(errs) > 0 {
        return errors.Join(errs...)
    }
    return nil // always return nil values.
}
````

- Another way to merge errors is just use `fmt.Errorf` with multiple `%w` verbs.
- You could create your own version of Unwrap that takes   an array of errors `[] error`. But since Go doesn’t support overloading you can’t create single type and provide both implementation :(. But you could do something like this.

````go
var err error
err = funcThatReturnsAnError()
switch err := err.(type) {
case interface {Unwrap() error}:
    // handle single error
    innerErr := err.Unwrap()
    // process innerErr
case interface {Unwrap() []error}:
    //handle multiple wrapped errors
    innerErrs := err.Unwrap()
    for _, innerErr := range innerErrs {
        // process each innerErr
    }
default:
    // handle no wrapped error
}
````

## Is and As

- If sentinel errors are wrapped, we can’t use `==` to compare them. Go provides `Is` and `As` for this.
- `errors.Is`: checks if any error in error tree matches the the provided sentinel

````go
func fileChecker(name string) error {
    f, err := os.Open(name)
    if err != nil {
        return fmt.Errorf("in fileChecker: %w", err)
    }
    f.Close()
    return nil
}

func main() {
    err := fileChecker("not_here.txt")
    if err != nil {
        if errors.Is(err, os.ErrNotExist) {
            fmt.Println("That file doesn't exist")
        }
    }
}
````

- `errors.As`: function allows you to check whether a returned error (on any error it wraps) matches a specific type. It takes two parameters, first the error being examined, second is pointer to variable of type that you are looking for.

````go
err := AFunctionThatReturnsAnError()
var myErr MyErr
if errors.As(err, &myErr) {
    fmt.Println(myErr.Codes)
}
````

- we can even pass pointer to inteface as well instead of the variable.

````go
err := AFunctionThatReturnsAnError()
// anonymous interface
var coder interface {
    CodeVals() []int
}
if errors.As(err, &coder) {
    fmt.Println(coder.CodeVals())
}

````

## Wrapping Errors with defer

Some times we find ourselves wrapping multiple errors with same message, which can be simplified using `defer`

````go
func DoSomeThings(val1 int, val2 string) (string, error) {
    val3, err := doThing1(val1)
    if err != nil {
        return "", fmt.Errorf("in DoSomeThings: %w", err)
    }
    val4, err := doThing2(val2)
    if err != nil {
        return "", fmt.Errorf("in DoSomeThings: %w", err)
    }
    result, err := doThing3(val3, val4)
    if err != nil {
        return "", fmt.Errorf("in DoSomeThings: %w", err)
    }
    return result, nil
}

// using defer
func DoSomeThings(val1 int, val2 string) (_ string, err error) {
  // this clousure checks whether an error was returned. So it reassins wrapping the error
    defer func() {
        if err != nil {
            err = fmt.Errorf("in DoSomeThings: %w", err)
        }
    }()
    val3, err := doThing1(val1)
    if err != nil {
        return "", err
    }
    val4, err := doThing2(val2)
    if err != nil {
        return "", err
    }
    return doThing3(val3, val4)
}
````

## panic and recover

- A *panic* is similar to an `Error` in Java or Python. It is state generated by Go runtime whenever it is not able to figure out what to do next.

- Go runtime panics if it detects bugs in itself, such as GC misbehaving. Or it could be due to user like, accessing slices beyond capacity or declaring negative size slices using `make`. 

- If there is a panic, then most likely runtime is last to blame.

- As soon as a panic happens, the current function exits immediately, and any `defer`s attached to the current function start running. When those `defer`s complete, the `defer`s attached to the calling function run, and so on, until `main` is reached. The program then exits with a message and a stack trace.

- You can create a custom `panic` using built-in which takes input as any type. Usually it is string.
- We can capture a `panic` to provide more graceful shutdown or prevent shutdown at all. The built-in `recover` function is called from within a `defer` to check whether a panic happened. Once a `recover` happens, execution continue normally.

````go
func div60(i int) {
    defer func() {
        if v := recover(); v != nil {
            fmt.Println(v)
        }
    }()
    fmt.Println(60 / i)
}

func main() {
    for _, val := range []int{1, 2, 0, 6} {
        div60(val)
    }
}
````

- Use panic for fatal errors and recover to handle them gracefully, but avoid relying on them for general error handling. Explicitly check for errors instead. If writing a library, use recover to prevent panics from escaping public APIs and convert them into errors.

## Getting a Stack Trace from an Error

- Go doesn’t provide stack traces by default, but you can use error wrapping or third-party libraries like CockroachDB’s to generate them. To print a stack trace, use fmt.Printf with %+v. To hide file paths in errors, compile with the -trimpath flag.

