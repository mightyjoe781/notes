# Blocks, Shadows and Control Structure

## Blocks

- Go variables can be declared outside of functions, as parameters to functions, and as local variables within functions
- Each place where declaration happens is called as a block. Variables, constants, types and functions declared outside of any function are placed in package block.

## Shadowing Variables

````go
func main() {
    x := 10
    if x > 5 {
        fmt.Println(x)
        x := 5
        fmt.Println(x)
    }
    fmt.Println(x)
}

// guess the output ?
// A) Nothing
// B) 10 line one, 5 line two, 5 line three
// C) 10 line one, 5 line two, 10 line three
````

- Option C is correct
- A *shadowing variable* is a variable that has same name as a variable in a containing blocks, it blocks to the shadowed variable.
- Any modern IDE will be able to detect this and alert you with warning
- Be careful to use `:=` because it creates and assigns value, so you can mistakenly shadow variables.
- Never shadow a package import!

NOTE: There is a universe block in Golang, which actually have definition of 25 keywords used in go like `true` and `false` or `int` and `string` etc.

## if

Example :

````go
n := rand.Intn(10)
if n == 0 {
    fmt.Println("That's too low")
} else if n > 5 {
    fmt.Println("That's too big:", n)
} else {
    fmt.Println("That's a good number:", n)
}
````

- Notice how brackets are not used for enclosing conditional
- variables declared inside `if` or `else` statement exists only within that block. What Go adds is declaring variables which is scoped to both `if` and `else`

````go
if n := rand.Intn(10); n == 0 {
    fmt.Println("That's too low")
} else if n > 5 {
    fmt.Println("That's too big:", n)
} else {
    fmt.Println("That's a good number:", n)
}
````

## for (4 Ways)

### Complete for Statement

````go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
````

- you can leave any part of the for declaration namely : initialisation, comparison and update

````go
i := 0
for ; i < 10; i++ {
    fmt.Println(i)
}
````

### Condition-only for statement

- equivalent to `while` loop in other languages

````go
i := 1
for i < 100 {
        fmt.Println(i)
        i = i * 2
}
````

### Infinite Loop

````go
package main

import "fmt"

func main() {
  for {
    fmt.Println("Hello")
  }
}
````

### break and continue

NOTE: go doesn’t have `do` while loop. Best you could do to run your loop at once is use infinite loop with a break condition.

- Go practices recommend not nesting too many level in if condition, it much better have validation type of code that uses continue to early terminate the loop

````go
// Bad Version
for i := 1; i <= 100; i++ {
    if i%3 == 0 {
        if i%5 == 0 {
            fmt.Println("FizzBuzz")
        } else {
            fmt.Println("Fizz")
        }
    } else if i%5 == 0 {
        fmt.Println("Buzz")
    } else {
        fmt.Println(i)
    }
}

// Improved Version
for i := 1; i <= 100; i++ {
    if i%3 == 0 && i%5 == 0 {
        fmt.Println("FizzBuzz")
        continue
    }
    if i%3 == 0 {
        fmt.Println("Fizz")
        continue
    }
    if i%5 == 0 {
        fmt.Println("Buzz")
        continue
    }
    fmt.Println(i)
}
````

### for-range statement

````go
evenVals := []int{2, 4, 6, 8, 10, 12}
for i, v := range evenVals {
    fmt.Println(i, v)
}
// or equivalent, index is optional
for v := range evenVals {
    fmt.Println(v)
}
````

- note while unpacking range, `i` var is optional

````go
// map iteration
m := map[string]int{
    "a": 1,
    "c": 3,
    "b": 2,
}

for i := 0; i < 3; i++ {
    fmt.Println("Loop", i)
    for k, v := range m {
        fmt.Println(k, v)
    }
}

// string iteration
samples := []string{"hello", "apple_π!"}
for _, sample := range samples {
    for i, r := range sample {
        fmt.Println(i, r, string(r))
    }
    fmt.Println()
}
````

- Notice something unusuall in output : index - 7 is left out because default iteration is on runes not the bytes
- NOTE: for-range (i, v) is a copy of original array so any update to them doesn’t affect array unless assigned to array back

### Labeling for statements

- by default `break` and `continue` keywords apply to `for` loop that directly contains them. You can label loops to provide context to break and continue

````go
func main() {
    samples := []string{"hello", "apple_π!"}
outer:
    for _, sample := range samples {
        for i, r := range sample {
            fmt.Println(i, r, string(r))
            if r == 'l' {
                continue outer	// notice how this resolve and continues the outer loop
            }
        }
        fmt.Println()
    }
}
````

## switch

````go
words := []string{"a", "cow", "smile", "gopher",
    "octopus", "anthropologist"}
for _, word := range words {
    switch size := len(word); size {
    case 1, 2, 3, 4:
        fmt.Println(word, "is a short word!")
    case 5:
        wordLen := len(word)
        fmt.Println(word, "is exactly the right length:", wordLen)
    case 6, 7, 8, 9:
    default:
        fmt.Println(word, "is a long word!")
    }
}

// a is a short word!
// cow is a short word!
// smile is exactly the right length: 5
// anthropologist is a long word!
````

- switch in Go are special, Similar to `if` if a variable is declared in switch declaration then it is accessible to all branches from `case`
- By default case doesn’t fall through in Go as compared to other languages, so there is no use of `break` after every case.
- Since fall-through is not supported we should pass comma separated values for multiple matchings

### Blank Switches

````go
words := []string{"hi", "salutations", "hello"}
for _, word := range words {	// we can leave parts from a for statement
    switch wordLen := len(word); {	// this is blank switch because we didn't specify what value to compare, instead each case defines this comparison
    case wordLen < 5:
        fmt.Println(word, "is a short word!")
    case wordLen > 10:
        fmt.Println(word, "is a long word!")
    default:
        fmt.Println(word, "is exactly the right length.")
    }
}
````

## goto (yes :)

Ever since Edsger Dijkstra wrote  [“Go To Statement Considered Harmful”](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) in 1968, the `goto` statement has been the black sheep of the coding family.

- Most programming languages don’t support `goto`

- in Go, `goto` statemnt specifies a labeled line of code, and execution jumps to it. However Go stricts jumps that skip over variable declaration and jumps that go into inner or parallel block

````go
func main() {
    a := rand.Intn(10)
    for a < 100 {
        if a%5 == 0 {
            goto done
        }
        a = a*2 + 1
    }
    fmt.Println("do something when the loop completes normally")
done:
    fmt.Println("do complicated stuff no matter why we left the loop")
    fmt.Println(a)
}
````

NOTE: You should try very hard to avoid using `goto`. But in the rare situations where it makes your code more readable, it is an option.
