# Setting up Go Environment

Download and Install from here : https://go.dev/dl/

For mac we can use brew as well : `brew install go` or for windows `choco install go`.

Check if installed correctly : `go version`

## Hello World in Go

### Making a Go Module

````bash
mkdir ch1
cd ch1
# marking the dir as go module
go mod init hello_world
cat go.mod
````

- above command creates a go module file : `go.mod` which is exact specification of dependencies of code within the module.

### Building the Go File

- create a `hello.go` file with following content (ignore the indentation)

````go
package main

import "fmt"

func main() {
fmt.Println("Hello, world!")
}
````

- first line is a package declaration, the `main` package in a Go module contains code that starts a Go program.
- Next is import of formatting library in go that is used to print to console.
- all go programs start from `main` function in the `main` package

````bash
go build
# this creates a binary : hello_world (same as module declaration)
./hello_world	# Hello, World!
# building binary with different name
go build -o hello
./hello
````

- `go fmt` is a important tool and language designers spent time considering the code formatting. Go doesn’t give a lot of flexibility in terms of formatting.
- Go enforces to use tabs to indents and if opening brace is not in same line as declaration or command that begins the block.
- fixing the whitespaces in your code to made go standards : `go fmt ./...` (applies to all files)

NOTE:

- go fmt doesn’t fix braces on wrong line because of semicolon insertion rule (look it up)

### go vet

`go vet` detects is whether a value exists for every placeholder in a formatting template. Example : template (`"Hello, %s!\n"`) with a `%s` placeholder, but no value assigned to it

### Using Makefiles to Automate builds

- each possible operation is called a target, `.DEFAULT_GOAL` defines default target to run.
- `.PHONY` keeps `make` from getting confused if a directory or file has same name as one of the listed targets.

````makefile
.DEFAULT_GOAL := build

.PHONY:fmt vet build
fmt:
	go fmt ./...

vet: fmt
	go vet ./...

build: vet
	go build
````

- Now running one command `make` does all three tasks for us
- Great Tutorial on Makefile : https://makefiletutorial.com/

## Go Compatibility Promise

- go development tools are periodically updated roughly every 6 months, go team commits for backward compatibility.
- See 
  - https://go.dev/doc/go1compat
  - https://www.youtube.com/watch?v=v24wrd3RwGo

## Staying up to Date

- `brew upgrade go`