# Predeclared Types and Declaration

## Predeclared Types

### The Zero Value

- any variable that is declared but not assigned a value defaults to zero

### Literals

- Go literal is an explicitly defined number, character, or string
- Types of literal
    - Integer Literal is sequence of numbers. Defaults to base 10, but we can use prefixes for other bases. e.g. `0b` for binary, `0o` for octal, `0x` for hexadecimal.
        - Go allows you to put `_` in integer literals to make reading longer integers easier. e.g. `1_234`
    - floating-point literal has a decimal point to indicate the fractional portion of the value. We can also define exponents using `e` : `6.03e23`. We can use `_` to format these literals as well.
    - A *rune* literal represents a character and is surrounded by single quotes. NOTE: Single and Double Quotes are not interchangeable.
    - Rune Literals can be : Unicode Characters (`a`), 8-bit octal numbers (`\141`), 8-bit hexadecimal numbers `\x61`, 16-bit hexadecimal numbers (`u0061`), or 32-bit unicode.
    - Two ways indicate string literals. Most of the time we use double quotes to create interpreted string literal. The only characters that cannot appear in an interpreted string literal are unescaped backslashes, unescaped  newlines, and unescaped double quotes.
    - If you need to include backslashes, double quotes, or newlines in your string, using a *raw string literal* is easier. These are delimited with backquotes (```) and can contain any character except a backquote.

````go
`Greetings and
"Salutation"`
````

- Literals are considered untyped.

### Boolean

- `bool` types represent Boolean variables. Two possible values `true` or `false`

````go
var flag bool	// defaults to false
var isAwesome = true
````

### Numeric Types

- Integer Types: `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`
- Special Integers types: `byte` is alias for `uint8`, `int` (varies platform to platform `int32` and `int64`). Integer literals default to `int` type. `uint` similar to `int` except values are `0` or positive.
- Integer Operators: `+`, `-`, `*`, `/` and `%` (Arithmetic Operators), `+=` ... (Assignment Operators), `==`, `!=`, `>`, `<=`, `<`, and `<=` (Comparison Operators), `&`, `|`, `^`, `&^`, `>>`, `<<` are also supported
- Floating point types: `float32` and `float64` (default 0)
- NOTE: A floating-point number cannot represent a decimal value exactly. Do not use them to represent money or any other value that must have an exact  decimal representation!
- Dividing a nonzero floating point var by 0 return `+Inf` or `-Inf`, Dividing a floating point var set to 0 by 0 return `Nan`. Don’t use `==` and `!=` to compare floats. Instead use epsilon difference to comapre them.
- Complex Types: `complex64` (uses `float32` under the hood) and `complex128` (uses `float64`). Supports functions like `real`, `imag`, `cmplx.Abs`

### String and Runes

- Strings can be compared for equality using `==`, difference with `!=`, or ordering with `>`, `>=`, `<`, or `<=`. Concatenated by using `+` operator.
- NOTE: Strings are immutable, we can reassign the value of string value but can’t change value of string that is assigned to it.

````go
var myFirstInitial rune = 'J' // good - the type name matches the usage
var myLastInitial int32 = 'B' // bad - legal but confusing
````

### Explicit Type Conversion

- Many languages support `automatic type promotion` but it sometimes might have pitfalls. Go doesn’t allow automatic type promotion. You must have to perform them.

````go
var x int = 10
var y float64 = 30.2
var sum1 float64 = float64(x) + y
var sum2 int = x + int(y)
fmt.Println(sum1, sum2)
````

NOTE: but go allows integer multiplication on floats

````go
var x float64 = 10
var y float64 = 200.3 * 5
````

## var v/s `:=`

````go
// verbose
var x int = 10
// if right side is expected to be int, we can leave off type
var x = 10
// to declare a var with zero val
var x int
// single line declaration for multiple var
var x, y int = 10, 20
var x, y int // default 0,0
var x, y = 10, "hello"

// declaration list
var (
	x int
  y	= 20
  z int = 30
  d, e = 40, "hello"
  f, g string
)
````

- Go supports `:=` assignment which is short and useful to use but cannot be used on a package level.

````go
var x = 10
x := 10
// ---
var x, y = 10, "hello"
x, y := 10, "hello"

// NOTE: it allows reassignment of variables as well
x := 10
x, y := 20, "hello"
````

## Using const

- `const` is immutable in Go

````go
const x int64 = 10
const(
	idKey = "id"
  nameKey = "name"
)
const z = 20 * 10
````

NOTE: Constants in Go are a way to give names to literals. There is *no* way in Go to declare that a variable is immutable.

````go
// Go doesn’t provide a way to specify that a value calculated at runtime is immutable.
x := 5
y := 10
const z = x + y // compilation fail
````

## Typed and Untyped Constants

- Constants can be typed or untyped. Untyped constants works exactly like a literal, doesn’t have type of intself but does have a default type that is used when no other type can be inferred
- Whether to make a constant typed depends on why the constant was  declared. If you are giving a name to a mathematical constant that could be used with multiple numeric types, keep the constant untyped. In  general, leaving a constant untyped gives you more flexibility.

## Unused Variables

- Go requires *every declared local variable must be read*. It is a *compile-time error* to declare and not use local variables.

````go
func main() {
    x := 10 // this assignment isn't read!
    x = 20
    fmt.Println(x)
    x = 30 // this assignment isn't read!
}
````

- note : `go vet` can’t catch above unread assignments but third-party tools are there which can.

## Naming Variables and Constants

- Identifier names to start with letter or underscore, and name can contain numbers, underscore, and letters.
- Even tho snake case is is valid its rarely used, people use CamelCase
- Within a function, favor short variable names. *The smaller the scope for a variable, the shorter the name that’s used for it*.

