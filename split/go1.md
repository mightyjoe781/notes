# Go Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: go
This is part 1 of 1 parts

---

## File: go/index.md

# GO

Go is a statically typed, compiled programming language designed at Google by Robert Griesemer, Rob Pike, and Ken Thompson. Go is syntactically similar to C, but with memory safety, garbage collection, structural typing, and CSP-style concurrency.



[NOTE] : Generics finally arrive in 1.18 :)

- [Learning Go (2nd Edition)](lego/index.md)

- [Notes: website tracker project](notes/index.md)

### Resources :

- [Official Documentation](https://go.dev/doc/)
- [Go Blogs](https://go.dev/doc/)
- [Go: The Complete Developer’s Guide](https://www.udemy.com/course/go-the-complete-developers-guide) : Aimed at Newbies with some familiarity with Go syntax.
- [Shichao’s Notes GOPL](https://notes.shichao.io/gopl/) : Complete Go notes available on web.

---

## File: go/lego/ch1.md

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

---

## File: go/lego/ch10.md

# Modules, Packages and Imports

## Repositories, Modules, and Packages

- Repository: place in VCS where source code for a project is stored.
- Module: bundle of Go source code that’s distributed and versioned as a single unit. Modules are stored in Repo and contain one-or-more packages.
- Packages: directory of source code which give a module organisation and structure.
- Every module have unique identifier called as *module-path*. It is usually based on repository where module is stored.
- Example: https://github.com/jonbodner/proteus has module-path of : *github.com/jonbodner/proteus*

## Using go.mod

- A directory of Go source code becomes a module when there is a valid `go.mod` file in it.
- It should be created using `go mod` command to manage the module.
- `go mod init MODULE_PATH` creates `go.mod` file that makes current directory root of the module. `MODULE_PATH` should be globally unique name that identifies your module.

````go
// structure of go.mod file

module github.com/mightyjoe781/exmaple // module declaration

go 1.21	// go version determined by toolchain

require (	// dependencies in your build
    github.com/learning-go-book-2e/formatter v0.0.0-20220918024742-18...
    github.com/shopspring/decimal v1.3.1
)

// note: indirect word doesn't have any special meaning here, it just signifies overrides or third-party code
require (
    github.com/fatih/color v1.13.0 // indirect
    github.com/mattn/go-colorable v0.1.9 // indirect 
)
````

- reading : [Go Toolchains](https://go.dev/doc/toolchain)

## Building Packages

### Importing and Exporting

- Go’s `import` statement allows you to access the exported constants, variables, functions and types in another package.
- Go uses *capitalization* to determine whether a package-level identifier must be visible outside the package where it is declared. Identifier which starts with lowercase letter or underscore is accessible within the package where it is declared.
- Anything that is exported becomes part of packages API.

### Creating and Accessing a Package

- [Code](https://github.com/learning-go-book-2e/package_example)

Inside math directory: `math.go`

````go
package math

func Double(a int) int {
  return a * 2
}
````

Inside do-format directory: `formatter.go`

````go
package format

import "fmt"

func Number(num int) string {
  return fmt.Sprintf("The number is %d", num)
}
````

Now `main.go`

````go
package main

import (
    "fmt"

    "github.com/learning-go-book-2e/package_example/do-format"
    "github.com/learning-go-book-2e/package_example/math"
)

func main() {
    num := math.Double(2)
    output := format.Number(num) // notice package name determines package name, not dir
    fmt.Println(output)
}
````

- Sometimes its common for directory names to not match the package name for the sake of versioning.

### Naming Packages

- Package names should be descriptive. Rather than `util`, create a package that describes the functionality. Ex - `names.Extract` or `names.Format`
- Avoid repeating the name of package in the names of functions and types. Ex- `ExtractName` or `FormatName` in `names` package is not suitable.

### Overriding a Package’s Name

- Sometimes its possible you might end up using two libraries with conflicting package names. Ex- `crypto/rand` and `math/rand`
- while importing you can redefine package names as follows

````go
import (
	crand "crypto/rand"
  "fmt"
  "math/rand"
)
````

### Documenting Your Code with Go Doc Comments

- *Go Doc* format comments are automatically converted into documentation
- There are rules for this
  - place comments directly above the item being documented.
  - start each line with double slashes, followed by a space
  - the first word in the comment for a symbol should be name of the symbol (function, type, constant, variables)
  - use a blank comment line to break your comment into multiple paragraphs.
- To put headers use `#` and a space after it.
- To link to exported symbol : `[pkgName.SymbolName]`
- To include text that links to a web page use : `[TEXT]: URL` format

To display these docs use `go doc <pkg_name>`. To view the documentation’s HTML formatting before publishing on web use `pkgsite` (use for `pkg.go.dev` site)

### Using the internal Package

- Sometimes we want to share a function, type or constant among packages in the module but don’t want to make it part of API. We can do this via `internal` package name.
- When a package is created with name `internal` the exported identifiers in that package will be available to direct parent packages and siblings of `internal`

### Avoiding Cicular Dependencies

Two of the goals of Go are a fast compiler and easy-to-understand source code. To support this, Go does not allow you to have a *circular dependency*between packages. If package A imports package B, directly or indirectly, package B cannot import package A, directly or indirectly.

### Organizing Your Module

recommended guidelines for organizing the modules

- If module is small keep all the code in the single package.
- If module grows and to make some order and making your code more readable, start diving it in two broad categories, main application code and the code which is generic and can be used by the different parts of application.
- If you want your module to be used as a library, the root of your module should have same name as repository.
- Its common for library modules to have one or more appication included with them as utilities, in that case create a directory name `cmd`
- when developing a library take advantage of internal package. If you create multiple packages within a module and they are outside an internal package, exporting a symbol so it can be used by another package in your module means, it can be used by anyone who uses your module.
- Problem with above use case is with sufficient users of your API, it doesn’t not matter what you promise in contract, all observable behaviour of your system will be depended on by somebody. once that is part of API it should be supported as long there are new version which are not backwards compatible. Read up Hyrum’s Law [Link](https://www.hyrumslaw.com)

[Simple Go project Layout with Modules](https://eli.thegreenplace.net/2019/simple-go-project-layout-with-modules/)

[How do you structure your go Apps](https://www.youtube.com/watch?v=oL6JBUk6tj0)

### Gracefully Renaming and Reorganizing Your API

- To avoid backward-breaking change, don’t remove original identifiers; provide an alternate name instead.
- This is easy with a function or method. If you want to rename or move an exported type, you use an alias. Quite simply, an *alias* is a new name for a type. `type Bar = Foo`

### Avoiding the init Function if Possible

- Why Go avoids Complex Calls
  - Go does not support method overriding or function overloading to keep code clear and predictable.
- What is `init`
  - A special function that runs automatically when a package is imported.
  - It does not take arguments or return values.
  - Used to set up package-level state.
- Problems with init
  - Some packages use init for automatic setup, like registering a database driver.
  - Blank imports (_ "package") trigger init without exposing any package functions.
  - This method is now **discouraged** as it hides important details.

````go
import (
    "database/sql"

    _ "github.com/lib/pq"
)
````

- **Best Practices**
  - Use init **only** for initializing package-level variables that don’t change.
  - If a variable needs to change during runtime, use a struct instead.
- Documentation is Important
  - Since init runs automatically, document its behavior, especially if it performs tasks like file loading or network access.

## Working with Modules

### Importing Third-Party Code

- Go always builds application from source code into a single binary file. This include your source code and source code that a module depends on.
- We should never use floating-point numbers when we need an exact representation of decimal number. Good option for this is `decimal` library from shopspring

````go
package main

import (
	"fmt"
  "log"
  "github.com/learning-go-book-2e/formatter"
  "github.com/shopspring/decimal"
)
````

- First use `go get` to get the modules(automatically updates `go.mod` file) and then build the application.
- Inspect the `go.mod` file notice, how formatter library has a *pseudoversion* to `formatter` package and `decimal` has a proper version. These both will direct dependencies, rest all will be indirect.
- For each dependency while updating `go.mod` file, another `go.sum` file is created containing checksum of each dependency.
- To download a specific library instead of scanning your source code, you can use `go get <module_path/url>`, in this case all your such dependencies will be in the indirect block. To fix this use `go mod tidy`

### Working with Versions

````bash
// go get ./...
go: downloading github.com/learning-go-book-2e/simpletax v1.1.0
go: added github.com/learning-go-book-2e/simpletax v1.1.0
go: added github.com/shopspring/decimal v1.3.1

go build
````

Now your go.mod file would be

````go
module github.com/learning-go-book-2e/region_tax

go 1.20

require (
    github.com/learning-go-book-2e/simpletax v1.1.0
    github.com/shopspring/decimal v1.3.1
)
````

- by default go picks latest version of module, to check use `go list -m -versions <module_path>`
- Now use `go get github.com/learning-go-book-2e/simpletax@v1.0.0` update module version and check `go.mod` file now. You will notice now `go.sum` will contain both version, which is not an issue.
- The version numbers attached to Go modules follow rules of *semantic versioning* (*SemVer*) [SemVer Specs](https://semver.org)

### Minimal Version Selection

- In case of multiple modules depending on the different version of same module, Go’s module system relies on the principle of minimal version selection.
- It always selects minimum version that would work with all the dependent modules.

### Updating to Compatible Versions

- Assume that there is a package `simpletax` with `v1.1.0` version which has a bug patched in `v1.1.1` then it was updated with a new feature `v1.2.0`.
- to explicitly upgrade a depedency, to upgrade to a bug patch release for current minor version use `go get -u=patch github.com/learning-go-book-2e/simpletax`
- Assume you are on `v1.0.0` and run above patch command, then it doesn’t fetch anythings, but on `v1.1.0` it fetches the latest patch.
- To get the latest version of `simpletax` use `go get -u github.com/learning-go-book-2e/simpletax`

### Updating to Incompatible Versions

- Assume that now `simpletax` features a cross country calculations but API has changed significantly, causing us to use `v2.0.0` as per semantic versioning.
- To handle this incompatibility, Go module follow the semantic import versioning rules
  - The major version of the module must be incremented
  - for all major version besides 0 and 1, the path to the module must end with `vN` where N is major version
- The path changes because an import path uniquely identifies a package. By definition, incompatible versions of a package are not the same package.
- Import becomes : `"github.com/learning-go-book-2e/simpletax/v2"`

### Vendoring

- It refers to practice of keeping the builds consistent  with identical dependencies, we keep copies of dependencies inside the module. It could be enable using `go mod vendor`.
- It creates a vendor directory on top level containing all dependencies

### Using pkg.go.dev

- it is a single service that gathers documentation on Go modules.
- It automatically indexes open source Go modules.
- Visit [pkg.go.dev](https://pkg.go.dev/)

## Publishing your Modules

- whenever a module is released as open source on a public VCS like Github or privately hosted version control, it is published.
- There is no need to explicitly upload your module to some central library repo, as for maven/npm we do.
- When releasing an open source module, make sure to include LICENSCE in the root of your repo. [Choosing a Good Licensce](https://itsfoss.com/open-source-licenses-explained/)

## Versioning Your Module

- always properly version your modules whether they are public or private to avoid issues with Go’s module systems.
- Always follow proper semantic versioning
- Go supports concept of pre-releases. Let’s assume that the curretn version of your module is tagged `v1.3.4`. You are working on version 1.4.0, which is not quite done, but to test it you need to publish it. Just add `v1.4.0-beta1` to indictate is not quite done or `v1.4.0-rc2`
- Only when breaking backward compatibility we need to bump the major version number.
- There are two ways to store new version, create a subdirectory within your module named nN, where N is the major version of your module or create a branch in VCS, you can put either the old code or new code on the new branch. Name the branch `vN`
- Its a good idea to tag the repo in case you are using the same subdirectory system or keeping the code in the main branch only.
- [Go Modules: v2 and Beyond](https://go.dev/blog/v2-go-modules) and [Developing a major version update](https://go.dev/doc/modules/major-version)

### Overriding Dependencies

- whenever a project is unmaintained, people often create fork of that project and you would like to get the community driven updates to fork by overriding the default package.

- ```go
  replace github.com/jonbodner/proteus => github.com/someone/my_proteus v1.0.0
  ```

- NOTE: A `replace` directive can also refer to a path in your local file system as well (in this case version must be omitted).

- To block a specific version of a module from being used.

- ```go
  exclude github.com/jonbodner/proteus v0.10.1
  ```

### Retracting a Version of your Module

- If you accidentally published some buggy or wrong version of your code, you can retract your version by using `retract` directive in go.

````go
retract v1.5.0 // not fully tested
retract [v1.7.0, v.1.8.5] // posts your cat photos to LinkedIn w/o permission
````

- these directive in `go.mod` requires to create a new version of your module.
- When a version is retracted, existing builds that specified the version will continue to work, but `go get` and `go mod tidy` will not upgrade to them. They will no longer appear as options when you use the `go list`command. If the most recent version of a module is retracted, it will no longer be matched with `@latest`; the highest unretracted version will match instead.

### Using Workspaces to Modify Modules Simultaneously

- Go *workspaces* allows users to have multiple module downloads and references between those modules will automatically resolve to local source code instead of the code hosted in your repository.

````go
go work init ./workspace_app  // creating workspace
go work use ./workspace_lib	// use local copy of workspace_lib package
````

- above creates, `go.work` file. This file is supposed for local development only, do not commit to repo

````go
// go.work

go 1.20

use (
    ./workspace_app
    ./workspace_lib
)
````

````go
cd workspace_app
go build
./workspace_app // works as expected.
````

````bash
// since workspace_lib works as expected, it can be pushed to github.

git init
git add .
git commit -m "first commit"
git remote add origin git@github.com:learning-go-book-2e/workspace_lib.git
git branch -M main
git push -u origin main
````

- Now all your previously not working commands like `go get ./...` etc will start working

## Module Proxy Servers

- Every module is stored in a source code repo, like Github or GitLab. But by default `go get` doesn’t ffetch code directly instead sends request to a `proxy server` run by Google which server as a cache store.
- Google also maintains the *checksum database* storing information about every module ever cached by thier server.

### Specifying a Proxy Server

- you can disable proxying by setting `GOPROXY=direct` in environment variables.
- you can run your own proxy server as well. Both Artifactory and Sonatype have their own Go proxy server support built-in in their enterprise plans.

### Using Private Repositories

- To use private repositories you have to run your private proxy server, so that you don’t request it from Google or disable proxy.
- If using a public proxy server we can set `GOPRIVATE=*.example.com, company.com/repo`



[Complete Go Modules Guide](https://go.dev/ref/mod)



---

## File: go/lego/ch11.md

# Go Tooling

## Using go run to Try out Small Programs
* Go is a compiled language, but go run allows executing source code directly without creating a binary.
* It compiles the program into a temporary directory, runs it, and deletes the binary afterward.
* Useful for testing small programs or treating Go like a scripting language.
## Adding Third-Party Tools with go install
* Installs Go programs from source repositories by downloading, compiling, and placing them in the Go binary directory.
* Requires specifying the package path with @version or @latest to avoid unintended behaviour.
* Default installation location is `$HOME/go/bin`, which should be added to the system’s PATH.
* Default installation location is `$HOME/go/bin`, which should be added to the system’s PATH.

#### Environment Variables in Go
* GOROOT (Go installation directory) and GOPATH (workspace for Go code) are automatically managed; manual configuration is usually unnecessary.
* GOBIN can be set to customise where installed binaries are stored.
* go help environment lists all available environment variables.

#### Updating Installed Tools
* Running go install with @latest updates an installed tool to the newest version.
* Example: go install github.com/rakyll/hey@latest updates hey.

#### Distribution of Go Programs
* go install is the preferred method for installing developer tools but is not mandatory for distribution.
* Binaries built using go build can be shared separately.

## Improving Import Formatting with goimports
* `goimports` also cleans up import statements, puts them in alphabetical order, removes unused imports and tries to guess any unspecified imports.
* `go install golang.org/x/tools/cmd/goimports@latest`
* `goimports -l -w .`

## Using Code-Quality Scanners
* `go vet` is a built-in tool that scans for common programming errors.
* Third-party linters help check code style and detect potential bugs missed by `go vet`
* Linters enforce idiomatic Go practices, such as
	* Properly naming variables
	* Formatting error messages correctly.
	* Adding comments to public methods and types.
* While linting suggestions aren't always mandatory, following them helps maintain readable and consistent code.

### Best Practices When Using Linters
* Linters may produce *false positives* or *false negatives* - review their suggestions before applying changes
* If ignoring a linter warning, add a comment explaining why for future reference
* Each linter provides a different format for disabling specific warnings - check the documentation
### staticcheck
* One of the best third-party scanners with over *150 checks*
* Minimizes false positives and is widely supported
* `go install honnef.co/go/tools/cmd/staticcheck@latest`\
* `staticcheck ./...`
* Example issue detected by `staticcheck` but not by `go vet`:
```go
s := fmt.Sprintf("Hello")
fmt.Println(s)

// staticcheck ./...
// main.go:6:7: unnecessary use of fmt.Sprintf (S1039)
```
* Another example: Detecting unused assignments to `err`.
### revive
* successor to `golint`, providing style and quality checks
* Installation: `go install github.com/mgechev/revive@latest`
* Default Checks include
	* Missing comments on exported identifiers.
	* Improper naming conventions.
	* Incorrect ordering of return values.
* Customizable via configuration files (`.toml`). Example:
```toml
[rule.redefines-builtin-id]
```
* Example issue detected by `revive`:
```go
true := false
fmt.Println(true)

// revive -config built_in.toml ./...
// main.go:6:2: assignment creates a shadow of built-in identifier true
```
### golangcli-lint
* **Aggregates multiple linters** into a single tool (includes `go vet`, `staticcheck`, `revive`, etc.).
* Efficient and configurable.
* Installation (recommended via binary download): Follow instructions on the official site.
* `golangci-lint run`
* Example Issue Detection
```go
x := 10
x = 30
// golangci-lint run
// main.go:6:2: ineffectual assignment to x (ineffassign)
```
* Supports advanced shadowing checks with `.golangci.yml`
```yaml
linters:
  enable:
    - govet
    - predeclared
linters-settings:
  govet:
    check-shadowing: true
    settings:
      shadow:
        strict: true
    enable-all: true
```

#### Choosing a Right Linter for Your Team

| Tool            | Best For                                            |
| --------------- | --------------------------------------------------- |
| `go vet`        | Basic, built-in checks                              |
| `staticcheck`   | Comprehensive analysis with minimal false positives |
| `revive`        | Style and naming conventions with configurability   |
| `golangci-lint` | Running multiple linters efficiently                |
|                 |                                                     |

### Recommendations
* Start with `go vet` in your automated builds
* Add `staticcheck` for deeper analysis with fewer false positives
* Use `revive` if you need customizable rules for code quality
* Adopt `golangci-lint` once you're comfortable managing multiple linters
* Standardize configuration and commit them to source control to maintain consistency across developers
## Using govulncheck to Scan for Vulnerable Dependencies
* `govulncheck` scans through dependencies and finds known vulnerabilities in both the standard library and in third-party libraries imported modules.
* Installation: `go install golang.org/x/vuln/cmd/govulncheck@latest`
* To fix vulnerability : `go get -u=patch gopkg.in/yaml.v2`
* `govulncheck ./...`
* Ideally should be randomly changed or updated as it may break compatibility for your package.
## Embedding Content in Your Program
* Ideally all required files might be put in a directory and binary that go compiles can read from the directory.
* In some scenarios you may want to embed those files for distribution in the binary using `go:embed`
* Example: embedding list of most common 1000 passwords,
	* import `embed` package
	* magic comment `//go:embed <file_name>` embeds the content of a file in the variables
```go
package main

import (
    _ "embed"
    "fmt"
    "os"
    "strings"
)

//go:embed passwords.txt
var passwords string

func main() {
    pwds := strings.Split(passwords, "\n")
    if len(os.Args) > 1 {
        for _, v := range pwds {
            if v == os.Args[1] {
                fmt.Println("true")
                os.Exit(0)
            }
        }
        fmt.Println("false")
    }
}
```
* To embed one or more directories of files into your program, use a variable of type `embed.FS` which implements three interfaces defined in `io/fs` package : `FS`, `ReadDirFS` and `ReadFileFS`.
* `embed.FS` can represent a virtual file system this way.
* In additional to exact file and directory names, we can use wildcards and ranges as well in embed
```go
// Example of hel based on the file present
package main

import (
    "embed"
    "fmt"
    "io/fs"
    "os"
    "strings"
)

//go:embed help
var helpInfo embed.FS

func main() {
    if len(os.Args) == 1 {
        printHelpFiles()
        os.Exit(0)
    }
    data, err := helpInfo.ReadFile("help/" + os.Args[1])
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    fmt.Println(string(data))
}
```

```txt
$ **go build**
$ **./help_system**
contents:
advanced/topic1.txt
advanced/topic2.txt
info.txt

$ **./help_system advanced/topic1.txt**
This is advanced topic 1.

$ **./help_system advanced/topic3.txt**
open help/advanced/topic3.txt: file does not exist
```
## Embedding Hidden Files
* hidden files in directory tree that start with `.` or `_` are difficult to embed. Default Embedding ignores them.
* This behaviour can be override by 2 methods
	* put `/*` after the name of a directory you want to embed (does not include hidden files in subdirectory)
	* `all:` includes all files
```go
//go:embed parent_dir
var noHidden embed.FS

//go:embed parent_dir/*
var parentHiddenOnly embed.FS

//go:embed all:parent_dir
var allHidden embed.FS
```

## Using go generate
* `go generate` scans Go source files for special comments (`//go:generate ...) and executes the specified commands
* Typically used for **code generation** tasks, such as creating Go source files from schemas or definitions
* **Example: Generating Go Code from Protobuf**
	* Protobuf (Protocol Buffers) is a binary format used for data serialization.
	* Define a schema (.proto file), then use protoc and protoc-gen-go to generate Go code.
	* `//go:generate protoc -I=. --go_out=. --go_opt=module=github.com/learning-go/proto_generate person.proto`
	* Run with $ go generate ./..., which generates a .pb.go file with the necessary structs and methods.
* Using stringer for Enums
	* Go’s iota does not provide automatic string representations for enums.
	* stringer generates a .go file that implements String() for enum values.
	* Example command: `//go:generate stringer -type=Direction`
	* Running $ go generate ./... creates direction_string.go, allowing enums to be printed as strings.
* **Other Use Cases for go generate**
	* Generating mocks for testing.
	* Embedding assets or templates.
	* Automating repetitive code transformations.
* [Blog Post](https://arjunmahishi.com/posts/golang-stringer)
## Working with go generate and Makefiles
* go generate is used to mechanically create source code (e.g., for protobufs, stringer).
* It should be included in version control for transparency and easier builds.
* Best practice: Automate go generate in the Makefile to avoid forgetting to update generated code.
* Avoid automating it if it generates different outputs for identical inputs or takes too long.
## Reading the Build Info Inside a Go Binary
* go build embeds build info in the binary, including module versions and Git revision.
* Use `go version -m <binary>` to inspect this metadata.
* govulncheck can scan Go binaries for known vulnerabilities.
* This helps in tracking software versions and dependencies in production environments.
## Building Go Binary for Other Platforms
* Go supports cross-compilation using GOOS and GOARCH environment variables.
* Example: GOOS=linux GOARCH=amd64 go build builds a Linux binary on macOS.
* Supported OS/architecture combinations can be found in Go’s documentation.
## Using Build Tags
* Used for conditional compilation based on OS, architecture, Go version, or custom flags.
* Two methods:
	* **Filename convention** (e.g., file_linux.go for Linux-specific code).
	* **Build tags** (`//go:build <condition>` before package declaration).
* Custom build tags allow selective compilation with -tags flag (e.g., `go build -tags customtag`).
## Testing Version of Go
* Use `go install golang.org/dl/go<version>@latest` to install different Go versions.
* Run `go<version>` download and use `go<version> build` to test compatibility. Ex : `go1.19.2 build`
* Uninstall by deleting the Go version from the sdk directory.

## Using go help to Learn more about Go Tooling
* you can get information on import path syntax by typing `go help importpath`
* you can get information about any tooling using `go help`

---

## File: go/lego/ch12.md

# Concurrency in Go

- Concurrency means breaking a process into independent components that safely share data.
- Most languages use OS-level threads with locks for concurrency.
- Go uses **Communicating Sequential Processes (CSP)**, introduced by Tony Hoare in 1978.
- CSP patterns make concurrency simpler and easier to understand.

## When to Use Concurrency

- Concurrency should be used only when necessary; it does not always improve speed.
- New Go developers often misuse goroutines, leading to deadlocks and inefficiencies.
- **Concurrency ≠ Parallelism**: More concurrency doesn’t always mean faster execution.
- **Amdahl’s Law**: Only the parallel portion of a task benefits from concurrency.
- Use concurrency when:
  - Multiple independent operations need to be combined.
  - Tasks involve I/O (disk, network) since they are much slower than memory operations.
  - Code must meet strict time constraints (e.g., web service calls under 50ms)
- Always benchmark to determine if concurrency actually improves performance.

## Goroutines

- **Goroutines** are lightweight threads managed by the Go runtime.
- The Go scheduler assigns goroutines to OS threads efficiently.
- Benefits:
  - Faster than creating OS threads.
  - Uses less memory with smaller, dynamically growing stacks.
  - Faster context switching since it avoids OS-level scheduling.
  - Works with the garbage collector and network poller for better optimization.
- Can launch thousands of goroutines without performance issues.
- **How to Use Goroutines**
  - Use go before a function call to launch it as a goroutine.
  - `go someFunc()`
- Unlike JavaScript’s async functions, any function in Go can be a goroutine.
- Prefer launching goroutines inside closures for better structure.

**Example: Concurrent Processing with Goroutines**

- Uses **channels** to pass values between goroutines.
- Keeps business logic (process()) separate from concurrency logic.
- Ensures modularity and testability.

````go
func process(val int) int {
    return val * 2 // Example: Doubling the value
}

func processConcurrently(inVals []int) []int {
    in := make(chan int, 5)
    out := make(chan int, 5)

    // Launch 5 worker goroutines
    for i := 0; i < 5; i++ {
        go func() {
            for val := range in {
                out <- process(val)
            }
        }()
    }

    // Load data into the in channel
    go func() {
        for _, val := range inVals {
            in <- val
        }
        close(in) // Close in channel to signal no more data
    }()

    // Read processed data
    results := make([]int, 0, len(inVals))
    for i := 0; i < len(inVals); i++ {
        results = append(results, <-out)
    }

    return results
}

func main() {
    input := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    output := processConcurrently(input)
    fmt.Println(output) // Example output: [2 4 6 8 10 12 14 16 18 20]
}
````

**Key Takeaways**

- **Use concurrency wisely**—not all tasks benefit from it.
- **Goroutines are cheap**, but improper use can lead to complexity.
- **Benchmark first**, then decide if concurrency helps.
- **Use channels for communication** and avoid shared memory when possible.

## Channels

- Channels are used in communication by goroutine.
- Channels are a built-in type.

```go
ch := make(chan int)
```

- Like Maps, channels are reference types.
- Zero value of Channels: `nil`

### Reading, Writing, and Buffering

#### Channel Interaction (`<-`)

- Read from a channel: `a := <-ch`
- Write to a channel: `ch <- b`
- Each value written to channel is ***consumed*** only once.
- If multiple goroutines read from the same channel, **only one will receive each value**.

#### Directional Channels

- Read-only channel: `ch <-chan int` (goroutine can only read)
- Write-only channel: `ch chan<- int` (goroutine can only write)
- Helps the **Go Compiler enforce proper channel usage**

#### Unbuffered Channel

- Blocking Behaviour
  - A write *pauses* until another goroutine reads.
  - A *read* pauses until another goroutine writes.
- Requires atleast two concurrently running goroutines.

#### Buffered Channel

- Created with fixed buffer size: `ch := make(chan int, 10)`
- Can hold values temporarily before being read.
- Blocking Behaviour
  - Writing blocks when the buffer is full
  - Reading blocks when the buffer is empty

#### Channel Properties

- `len(ch)`: Number of elements in the buffer
- `cap(ch)`: Maximum Buffer Size
- Unbuffered Channels return 0 for both length and capacity

#### General Recommendation

- Prefer unbuffered channels in most cases.
- Buffered channels are useful when *handling bursts of data* without immediate consumers.

### Using for-range and Channels

````go
for v:= range ch {
  fmt.Println(v)
}
````

- The loop *extracts* values from channel until it is closed.
- Blocking Behaviour
  - If no value is available, goroutine *pauses* until a value is sent or channel is closed.
- Loop Termination
  - The loop stops when the channel is closed.
  - Can also be manually stopped using break or return.
- **Unlike other for-range loops**, only a **single variable** (value) is used, since channels do not have keys.

#### Closing a Channel

- Use `close(ch)` to close a channel when no more data is will be sent.
- Writing to a closed channel causes *panic*
- Closing an already closed channel also causes *panic*

#### Reading from a Closed Channel

- Always succeeds (does not panic)
- If the channel is **buffered**, remaining values are read **in order**.
- If the channel is **empty**, the **zero value** of the channel’s type is returned.

#### Detecting a Closed Channel

````go
v, ok := <-ch
````

- `ok == true` : channel is open, v contains a valid value
- `ok == false` : channel is closed, v contains a zero value
- Always use this when reading from a potentially closed channel

#### Who closes the Channel ?

- The **sending** goroutine is responsible for closing the channel.
- **Closing is necessary** only if a receiver is waiting for the channel to close (e.g., a for-range loop).
- Otherwise, Go **garbage collects** unused channels automatically.

#### Why Channels Matter in Go?

- Go **avoids shared mutable state** (unlike other languages using global shared memory for concurrency).
- Channels **clarify data dependencies**, making concurrent code **easier to reason about**.
- They encourage a **staged pipeline** approach to processing data.

#### Understanding How Channels Behave

| State                  | Read Behaviour                                  | Write Behaviour               | Close Behaviour |
| ---------------------- | ----------------------------------------------- | ----------------------------- | --------------- |
| **Unbuffered**, Open   | Waits until something is written                | Waits until something is read | Works           |
| **Unbuffered**, Closed | Returns **zero value** (use comma ok to check)  | PANIC                         | PANIC           |
| **Buffered**, Open     | Waits if buffer is empty                        | Wait if buffer is full        | Works           |
| **Buffered**, Closed   | Reads remaining values, then returns zero value | PANIC                         | PANIC           |
| Nil Channel            | Hangs Forever                                   | Hangs Forever                 | PANIC           |

#### Closing a Channel Properly

- The **writing goroutine** should close the channel when no more data is sent.
- **Multiple writers?** → Use sync.WaitGroup to prevent multiple close() calls.

#### **Nil Channels**

- Reads and writes **hang forever**.
- Useful in some cases (e.g., turning off a select case).

## select

- **Purpose**
  - select lets a goroutine **read from or write to multiple channels** at once.
  - Prevents **starvation** (all cases are considered randomly, ensuring fairness).

````go
select {
case v := <-ch1:
    fmt.Println(v)
case v := <-ch2:
    fmt.Println(v)
case ch3 <- x:
    fmt.Println("Wrote", x)
case <-ch4:
    fmt.Println("Received from ch4, but ignored")
}
````

- Each case **must** involve a channel operation (<-ch for read, ch <- x for write).
- If **multiple cases are ready**, one is chosen **randomly**.
- If **no cases are ready**, select **blocks** until one can proceed.

#### Avoiding Deadlocks with select

- A **deadlock occurs** when all goroutines are waiting indefinitely.
- Example of **deadlock** (caused by circular waiting):

````go
func main() {
    ch1 := make(chan int)  // Unbuffered channel ch1
    ch2 := make(chan int)  // Unbuffered channel ch2

    go func() { // Goroutine starts
        ch1 <- 1          // Step 1: Sends 1 to ch1 (blocks until read)
        fmt.Println(<-ch2) // Step 3: Reads from ch2 (waits indefinitely)
    }()

    ch2 <- 2              // Step 2: Sends 2 to ch2 (blocks until read)
    fmt.Println(<-ch1)    // Step 4: Reads from ch1 (waits indefinitely)
}
````

- **Error:** fatal error: all goroutines are asleep - deadlock!
- ch1 and ch2 are **waiting on each other** to proceed.
- **Fix using select to avoid deadlock:**

````go
select {
case ch2 <- inMain:
case fromGoroutine = <-ch1:
}
````

- Ensures **at least one** operation can proceed, breaking deadlock.

#### **Using select in Loops (for-select Loop)**

Common Pattern

````go
for {
    select {
    case <-done:
        return // Exit the loop
    case v := <-ch:
        fmt.Println(v)
    }
}
````

- **Exiting condition is required** (done channel in this case).

- **Using default in select**

````go
select {
case v := <-ch:
    fmt.Println("Read:", v)
default:
    fmt.Println("No value available")
}
````

- **Non-blocking behavior** (does not wait if ch has no value).
- **Caution:** Avoid using default inside for-select, as it **wastes CPU** by looping infinitely.

## Concurrency Practices and Patterns

### Keep Your APIs Concurrency-Free]

- Concurrency should be hidden as an implementation detail in the APIs
- Avoid exposing *channels* or *mutexes* in API Types, functions and methods.
- User should not have to manage channels(e.g. buffering, closing)
- Exception: Concurrency helper libraries may expose channels

### Goroutines, for Loops and Varying Variables

- **Before Go 1.22:** Loops reused the same variable, causing goroutines to capture the **final value** instead of different values.
- **Go 1.22 Fix:** Each iteration now gets a **new copy** of the loop variable.
- Workarounds for older versions:
  - **Shadow the variable:** v := v inside the loop.
  - **Pass as a function parameter:** go func(val int) { ch <- val * 2 }(v).
- **Rule of Thumb:** Always pass **copies** of changing variables into closures.

### Always Clean up your Goroutines

- Goroutines must **eventually exit**, or they cause **memory leaks**.
- Example issue: A **blocked goroutine** waiting for channel input may never exit. Consider a case where you call a generator to generate 10 numbers, but the for loop that called the generator exits on 5 numbers. Then the generator coroutine will be blocked.

### Use the Context to Terminate Goroutines

- `context.Context` is used to signal goroutines to exit.
- Modify loops in goroutines.

````go
// passing Context helps clean up goroutines
select {
  case <-ctx.Done(): return  // Gracefully exit
  case ch <- i: // Continue sending data
}
````

### Know when to use Buffered and Unbuffered Channels

- Buffered Channels are useful to limit number of goroutine that will be launched limiting number of amount of work that is queued up.

### Implement Backpressure

- Systems perform better overall when their components limit the amount of work they are willing to perform.
- Buffered Channel and `select` statements can limit number of subsequent requests in a system.

````go
type PressureGauge struct {
    ch chan struct{}
}

func New(limit int) *PressureGauge {
    return &PressureGauge{
        ch: make(chan struct{}, limit),
    }
}

func (pg *PressureGauge) Process(f func()) error {
    select {
    case pg.ch <- struct{}{}:
        f()
        <-pg.ch
        return nil
    default:
        return errors.New("no more capacity")
    }
}
````

````go
// example: ratelimiter in golang

func doThingThatShouldBeLimited() string {
    time.Sleep(2 * time.Second)
    return "done"
}

func main() {
    pg := New(10)
    http.HandleFunc("/request", func(w http.ResponseWriter, r *http.Request) {
        err := pg.Process(func() {
            w.Write([]byte(doThingThatShouldBeLimited()))
        })
        if err != nil {
            w.WriteHeader(http.StatusTooManyRequests)
            w.Write([]byte("Too many requests"))
        }
    })
    http.ListenAndServe(":8080", nil)
}
````

### Turn Off a case in a select

**Handling Closed Channels**

- select helps combine data from multiple sources but requires proper handling of closed channels.
- Reading from a closed channel always succeeds, returning the zero value.
- If not handled, your program may waste time processing junk values.

**Using nil Channels to Disable Cases**

- Reading from or writing to a nil channel causes the program to block indefinitely.
- You can use this behavior to disable a case in select by setting a closed channel to nil.
- This prevents the case from being randomly selected and stops unnecessary reads.

**Example Implementation**

- Use a counter to track how many channels are closed.
- When a read operation detects a closed channel (ok == false), set the channel variable to nil.
- This ensures the case never runs again, preventing unnecessary processing.

### Use WaitGroups

- **Purpose of sync.WaitGroup**
  - Used when one goroutine needs to wait for multiple goroutines to complete.
  - Unlike context cancellation (which works for a single goroutine), WaitGroup manages multiple concurrent tasks.
- **Key Methods in sync.WaitGroup**
  - Add(n): Increments the counter by n, indicating n goroutines will be waited on.
  - Done(): Decrements the counter, called via defer in each goroutine.
  - Wait(): Blocks execution until the counter reaches zero.
- Implementation Details
  - sync.WaitGroup does not require initialization; its zero value is ready to use.
  - Ensure all goroutines share the same WaitGroup instance (use closures instead of passing by value).
  - Helps manage closing channels when multiple goroutines write to the same channel.
- **Example: Processing Data with WaitGroup**
  - Uses multiple worker goroutines to process data from an input channel.
  - A monitoring goroutine waits for all workers to finish before closing the output channel.
  - Ensures out is closed only once, preventing data race issues.

````go
func main() {
    var wg sync.WaitGroup
    wg.Add(3)
    go func() {
        defer wg.Done()
        doThing1()
    }()
    go func() {
        defer wg.Done()
        doThing2()
    }()
    go func() {
        defer wg.Done()
        doThing3()
    }()
    wg.Wait()
}
````

````go
func processAndGather[T, R any](in <-chan T, processor func(T) R, num int) []R {
    out := make(chan R, num)
    var wg sync.WaitGroup
    wg.Add(num)
    for i := 0; i < num; i++ {
        go func() {
            defer wg.Done()
            for v := range in {
                out <- processor(v)
            }
        }()
    }
    go func() {
        wg.Wait()
        close(out)
    }()
    var result []R
    for v := range out {
        result = append(result, v)
    }
    return result
}
````



- **Best Practices**
  - Use WaitGroup only when necessary (e.g., closing shared resources like channels).
  - Prefer higher-level concurrency patterns when applicable.
- **Alternative: errgroup.Group**
  - Found in golang.org/x/sync/errgroup.
  - Extends WaitGroup by allowing goroutines to return errors.
  - Stops all processing if any goroutine encounters an error.

### Run Code Exactly Once

- `init` should be reserved for initialization of effectively immutable package-level state.
- Use sync.Once to ensure a function executes only once, even if called multiple times.

````go
var once sync.Once	// note it should be global
once.Do(func() { parser = initParser() })
````

- Go 1.21 introduced sync.OnceFunc, sync.OnceValue, and sync.OnceValues to simplify this.

### Put Your Concurrent Tools Together

- Example pipeline: Call services A & B in parallel → Combine results → Call service C.
- Uses context.Context to enforce a 50ms timeout.
- Uses goroutines and channels for concurrency.

````go
func GatherAndProcess(ctx context.Context, data Input) (COut, error) {
    ctx, cancel := context.WithTimeout(ctx, 50*time.Millisecond)
    defer cancel()

    ab := newABProcessor()
    ab.start(ctx, data)
    inputC, err := ab.wait(ctx)
    if err != nil {
        return COut{}, err
    }

    c := newCProcessor()
    c.start(ctx, inputC)
    out, err := c.wait(ctx)
    return out, err
}
// notice how ab API doesn't expose concurrency to driver program
````

````go
type abProcessor struct {
    outA chan aOut
    outB chan bOut
    errs chan error
}

func newABProcessor() *abProcessor {
    return &abProcessor{
        outA: make(chan aOut, 1),
        outB: make(chan bOut, 1),
        errs: make(chan error, 2),
    }
}
````

- abProcessor handles concurrent calls to services A & B:
  - abProcessor handles concurrent calls to services A & B:
  - Implements start (launch goroutines) and wait (aggregate results).
- cProcessor is a simpler version handling service C.

````go
func (p *abProcessor) start(ctx context.Context, data Input) {
    go func() {
        aOut, err := getResultA(ctx, data.A)
        if err != nil {
            p.errs <- err
            return
        }
        p.outA <- aOut
    }()
    go func() {
        bOut, err := getResultB(ctx, data.B)
        if err != nil {
            p.errs <- err
            return
        }
        p.outB <- bOut
    }()
}

func (p *abProcessor) wait(ctx context.Context) (cIn, error) {
    var cData cIn
    for count := 0; count < 2; count++ {
        select {
        case a := <-p.outA:
            cData.a = a
        case b := <-p.outB:
            cData.b = b
        case err := <-p.errs:
            return cIn{}, err
        case <-ctx.Done():
            return cIn{}, ctx.Err()
        }
    }
    return cData, nil
}
````

- C-processor implementation:

````go
type cProcessor struct {
    outC chan COut
    errs chan error
}

func newCProcessor() *cProcessor {
    return &cProcessor{
        outC: make(chan COut, 1),
        errs: make(chan error, 1),
    }
}

func (p *cProcessor) start(ctx context.Context, inputC cIn) {
    go func() {
        cOut, err := getResultC(ctx, inputC)
        if err != nil {
            p.errs <- err
            return
        }
        p.outC <- cOut
    }()
}

func (p *cProcessor) wait(ctx context.Context) (COut, error) {
    select {
    case out := <-p.outC:
        return out, nil
    case err := <-p.errs:
        return COut{}, err
    case <-ctx.Done():
        return COut{}, ctx.Err()
    }
}
````



## When to Use Mutexes Instead of Channels

- Channels are preferred for managing concurrent data flow.
- Mutex (sync.Mutex) is better for shared state like an in-memory scoreboard.
- sync.RWMutex allows multiple readers but only one writer at a time.

````go
var mu sync.RWMutex
mu.Lock()
// Critical section
mu.Unlock()
````

**When to Use Channels vs. Mutexes**

- **Use Channels**: When passing values between goroutines.
- **Use Mutexes**: When managing access to shared fields in structs.
- **Use Mutexes only if performance is an issue with channels.**

## Atomics

- The `sync/atomic` package provides access to the *atomic variable* operations built into modern CPUs to add, swap, load, store, or compare and swap (CAS) a value that fits into a single register.

## More

- Read: *Concurrency in Go* for learning more about this chapter.

---

## File: go/lego/ch13.md

# The Standard Library

- Like Python, Go follows a "batteries included" philosophy, offering a rich standard library that addresses modern programming needs.
- Read : [Go Documentation](https://pkg.go.dev/std)

## io and Friends

- The `io` package is central to Go's I/O operations, defining interfaces like `io.Reader` and `io.Writer`.
- `io.Reader` has the `Read` method, which modifies a provided byte slice and returns the number of bytes read.
- `io.Writer` has the `Write` method, which writes bytes to a destination. It returns number of bytes written and error if something went wrong.
- These interfaces are widely used for working with files, network connections, and streams.

````go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}
````

### Efficient Buffer Usage

````go
func countLetters(r io.Reader) (map[string]int, error) {
    buf := make([]byte, 2048)
    out := map[string]int{}
    for {
        n, err := r.Read(buf)
        for _, b := range buf[:n] {
            if (b >= 'A' && b <= 'Z') || (b >= 'a' && b <= 'z') {
                out[string(b)]++
            }
        }
        if err == io.EOF {
            return out, nil
        }
        if err != nil {
            return nil, err
        }
    }
}
````

- Using a reusable buffer in `Read` prevents excessive memory allocations and garbage collection overhead.

````go
// since io.Reader/io.Writer are very simple interfaces that they can be reimplemented in many ways.
s := "The quick brown fox jumped over the lazy dog"
sr := strings.NewReader(s)
counts, err := countLetters(sr)
if err != nil {
    return err
}
fmt.Println(counts)
````

- Functions like `io.Copy` facilitate easy data transfer between `io.Reader` and `io.Writer` implementations.
- Helper functions include:
  - `io.MultiReader` (reads sequentially from multiple readers)
  - `io.MultiWriter` (writes to multiple writers simultaneously)
  - `io.LimitReader` (restricts the number of bytes read from a reader)

### Working with Files

- The `os` package provides file handling functions like `os.Open`, `os.Create`, and `os.WriteFile`.
- The `bufio` package offers buffered I/O for efficient reading and writing.
- `gzip.NewReader` wraps an `io.Reader` to handle gzip-compressed files.

### Closing Resources Properly

- `io.Closer` interface defines the `Close` method for resource cleanup.
- `defer f.Close()` ensures files are closed after use, preventing resource leaks.
- Avoid deferring `Close` in loops to prevent excessive open file handles.

### Seeking in Streams

- `io.Seeker` provides `Seek(offset int64, whence int) (int64, error)` for random access in files.
- The `whence` parameter should ideally have been a custom type instead of `int` for clarity.

### Combining Interfaces

- Go defines composite interfaces like `io.ReadWriter`, `io.ReadCloser`, and `io.ReadWriteSeeker` to provide combined functionalities.
- These interfaces make functions more reusable and compatible with various implementations.

### Additional Utils

- `io.ReadAll` reads an entire `io.Reader` into a byte slice.
- `io.NopCloser` wraps an `io.Reader` to satisfy the `io.ReadCloser` interface, implementing a no-op `Close` method.
- The `os.ReadFile` and `os.WriteFile` functions handle full-file reads and writes but should be used cautiously with large files.

Go’s `io` package and related utilities exemplify simplicity and flexibility. By leveraging these standard interfaces and functions, developers can write modular, efficient, and idiomatic Go programs that interact seamlessly with different data sources and sinks.

## time

- `time` package provides two main types `time.Duration` and `time.Time`
- `time.Duration` represents a period of time based on `int64`. It can represent nanoseconds, microseconds, milliseconds, seconds, minutes and hour.

````go
d := 2 * time.Hour + 30 * time.Minute // d is of type time.Duration
````

- Go defines a sensible string format, a series of numbers that can be parsed using `time.Duration` with the `time.ParseDuration`. Like `300ms`, `-1.5h` or `2h45m`. [Go Standard Library Documentation](https://pkg.go.dev/time#ParseDuration)
- `time.Time` type represents a moment in time complete with timezone.
- `time.Now` provides a reference to current time returning a `time.Time` instance.
- `time.Parse` function converts from a `string` to a `time.Time`, while the `Format` method converts a `time.Time` to a `string`. [Constants Format](https://pkg.go.dev/time#pkg-constants)

````go
t, err := time.Parse("2006-01-02 15:04:05 -0700", "2023-03-13 00:00:00 +0000")
if err != nil {
    return err
}
fmt.Println(t.Format("January 2, 2006 at 3:04:05PM MST"))

// March 13, 2023 at 12:00:00AM UTC
````

- `time.Time` instances can compared using `After`, `Before`, and `Equal` methods.
- `Sub`/`Add` method returns a `time.Duration` representing elapsed/summing time between two `time.Time` instances.

### Monotonic Time

- OS tracks two types of time tracking
  - the *wall clock* which corresponds to the current time.
  - *monotonic clock* which counts up from time the computer was booted.
- Reason is tracking two times is because *wall clock* is not consistent and changes based on Daylight Savings, Leap Seconds, NTP Updates.
- Go invisibly uses *monotonic* time to track elapsed time whenever a timer is set or `time.Time` instance is created.

### Timers and Timeout

- `time.After` returns a channel that outputs once.
- `time.Tick` returns a new value every time specified with `time.Duration`. NOTE: be careful to use this as underlying `time.Ticker` can not be shut down. Use the `time.NewTicker` instead.
- `time.AfterFunc` triggers a specific function post some `time.Duration`

## encoding/json

- REST APIs have made JSON as standard way to communicate between services.
- *Marshalling* : converting a Go data type to and encoding
- *Unmarshalling* : converting to a Go data type.

### Using Struct Tags to Add Metadata

- Struct tags define how Go struct fields map to JSON fields.
- Syntax: `json:"field_name”`
- If no struct tag is provided, JSON field name default to the Go struct field names.
- JSON field names are case-insensitive when unmarshalling.
- To ignore a field : `json:"-"`
- To omit empty values: `json:"field_name,omitempty"`
- `go vet` can validate struct tags but the compiler does not.

````json
{
    "id":"12345",
    "date_ordered":"2020-05-01T13:01:02Z",
    "customer_id":"3",
    "items":[{"id":"xyz123","name":"Thing 1"},{"id":"abc789","name":"Thing 2"}]
}
````

- To map above data we can create data type as

````go
type Order struct {
    ID            string        `json:"id"`
    DateOrdered   time.Time     `json:"date_ordered"`
    CustomerID    string        `json:"customer_id"`
    Items         []Item        `json:"items"`
}

type Item struct {
    ID   string `json:"id"`
    Name string `json:"name"`
}
````

### Unmarshaling and Marshaling

- Unmarshalling

````go
var o Order
err := json.Unmarshal([]byte(data), &o)
if err != nil {
    return err
}
````

- Marshalling

````go
out, err := json.Marshal(o)
````

- Uses **reflection** to read struct tags dynamically.

### JSON, Readers, and Writers

- `json.Marshal` and `json.Unmarshal` work with byte slices
- Efficient handling via `json.Decoder` (for reading) and `json.Encoder` (for writing), which work with `io.Reader` and `io.Writer`

- Example of encoding JSON to a file

````go
err = json.NewEncoder(tmpFile).Encode(toFile)
````

- Example decoding JSON from a file

````go
err = json.NewDecoder(tmpFile2).Decode(&fromFile)
````

### Encoding and Decoding JSON Streams

- Used for handling multiple JSON objects in a stream
- Decoding JSON streams

````go
var t struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}
dec := json.NewDecoder(strings.NewReader(streamData))
for {
    err := dec.Decode(&t)
    if err != nil {
        if errors.Is(err, io.EOF) {
            break
        }
        panic(err)
    }
}
````

- Encoding multiple JSON objects

````go 
var b bytes.Buffer
enc := json.NewEncoder(&b)
for _, input := range allInputs {
    t := process(input)
    err = enc.Encode(t)
    if err != nil {
        panic(err)
    }
}
````

### Custom JSON Parsing

- Needed when JSON format doesn’t align with Go’s built-in types.
- Example Custom time format handling

````go 
type RFC822ZTime struct {
    time.Time
}

func (rt RFC822ZTime) MarshalJSON() ([]byte, error) {
    out := rt.Time.Format(time.RFC822Z)
    return []byte(`"` + out + `"`), nil
}

func (rt *RFC822ZTime) UnmarshalJSON(b []byte) error {
    if string(b) == "null" {
        return nil
    }
    t, err := time.Parse(`"`+time.RFC822Z+`"`, string(b))
    if err != nil {
        return err
    }
    *rt = RFC822ZTime{t}
    return nil
}
````

- Example Struct embedding to override marshalling behaviour

````go 
type Order struct {
    ID          string    `json:"id"`
    Items       []Item    `json:"items"`
    DateOrdered time.Time `json:"date_ordered"`
    CustomerID  string    `json:"customer_id"`
}

func (o Order) MarshalJSON() ([]byte, error) {
    type Dup Order
    tmp := struct {
        DateOrdered string `json:"date_ordered"`
        Dup
    }{
        Dup: (Dup)(o),
    }
    tmp.DateOrdered = o.DateOrdered.Format(time.RFC822Z)
    return json.Marshal(tmp)
}
````

## net/http

### The Client

- `http.Client` handles HTTP requests and responses.
- Avoid using `http.DefaultClient` in production (no timeout).
- Create a custom `http.Client`

````go
client := &http.Client{
  Timeout: 30 * time.Second
}
````

- Use `http.NewRequestWithContext` to create a request.
- Set request headers using `req.Header.Add()`.
- Use `client.Do(req)` to send the request.
- Read response data with `json.NewDecoder(res.Body).Decode(&data)`

````go
// getting a req instance
req, err := http.NewRequestWithContext(context.Background(),
    http.MethodGet, "https://jsonplaceholder.typicode.com/todos/1", nil)
if err != nil {
    panic(err)
}

// adding headers
req.Header.Add("X-My-Client", "Learning Go")
res, err := client.Do(req)
if err != nil {
    panic(err)
}

// decoding response
defer res.Body.Close()
if res.StatusCode != http.StatusOK {
    panic(fmt.Sprintf("unexpected status: got %v", res.Status))
}
fmt.Println(res.Header.Get("Content-Type"))
var data struct {
    UserID    int    `json:"userId"`
    ID        int    `json:"id"`
    Title     string `json:"title"`
    Completed bool   `json:"completed"`
}
err = json.NewDecoder(res.Body).Decode(&data)
if err != nil {
    panic(err)
}
fmt.Printf("%+v\n", data)
````

### The Server

- `http.Server` handles HTTP requests.
- Implements `http.Handler` interface:

````go
type Handler interface {
    ServeHTTP(http.ResponseWriter, *http.Request)
}
````

````go
s := http.Server{
    Addr:         ":8080",	// default 80
    ReadTimeout:  30 * time.Second,
    WriteTimeout: 90 * time.Second,
    Handler:      HelloHandler{},	// mux can be used
}
err := s.ListenAndServe()
if err != nil {
    if err != http.ErrServerClosed {
        panic(err)
    }
}
````

- `http.ResponseWriter` methods includes (in order):
  - `Header()` `http.Header`
  - `Write([]byte)` `(int, error)`
  - `WriteHeader(statusCode int)`

#### Request Routing 

- `*http.ServeMux` is used for routing requests
- `http.NewServeMux` fuction creates a new instance of `ServeMux` which meets the `http.Handler` interface, so can be assigned to `Handler` field in `http.Server`.

````go                                                                                   
mux.HandleFunc("/hello", func(w http.ResponseWrite, r *http.Request)) {
  w.Write([] byte("Hello!\n"));
}
````

- Go 1.22 extends the path syntax to optionally allow HTTP verbs and path wildcard variables.

````go                        
mux.HandleFunc("GET /hello/{name}", func(w http.ResponseWriter, r *http.Request) {
    name := r.PathValue("name")
    w.Write([]byte(fmt.Sprintf("Hello, %s!\n", name)))
})
````

- `*http.ServeMux` dispatches request to `http.Handler` instances and implements them. We can create `*http.ServeMux` instance with multiple related request and register it with a parent `*http.ServeMux`

````go
person := http.NewServeMux()
person.HandleFunc("/greet", func(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("greetings!\n"))
})
dog := http.NewServeMux()
dog.HandleFunc("/greet", func(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("good puppy!\n"))
})
mux := http.NewServeMux()
mux.Handle("/person/", http.StripPrefix("/person", person))
mux.Handle("/dog/", http.StripPrefix("/dog", dog))
````

- `/person/greet` is handled by handler attached to `person`, while `/dog/greet` is handled by handlers attached to `dog`

### Middleware

- Middleware takes `http.Handler` instance and returns `http.Handler` (usually a closure)
- Its usually used to plugin some transformation or validation in requests.

````go
// example-request timer middleware
func RequestTimer(h http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        h.ServeHTTP(w, r)
        dur := time.Since(start)
        slog.Info("request time",
            "path", r.URL.Path,
            "duration", dur)
    })
}

// using it
mux.Handle("/hello", RequestTimer(
    http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("Hello!\n"))
    })))
````

- Since `*http.ServeMux` implements the `http.Handler` interface, a set of middlewares can be applied to all registered handlers.

````go
terribleSecurity := TerribleSecurityProvider("GOPHER")
wrappedMux := terribleSecurity(RequestTimer(mux))
s := http.Server{
    Addr:    ":8080",
    Handler: wrappedMux,
}
````

- Third Party modules to enhance server
  - `alice` allows function chains for middlewares
  - `gorilla mux` and `chi` both are very good request routers
  - `Echo` and `Gin` web frameworks implements their own handler and middleware patterns

### Response Controller

- Backward Compatibility Challenge:

  - Modifying interfaces breaks backward compatibility in Go
  - New methods cannot be added to existing interfaces without breaking existing implementations

- Tradition Approach - Using Additional Interfaces

  - Example: `http.ResponseWriter` could not be modified directly
  - Instead, optional functionality added through new interfaces like `http.Flusher` and `http.Hijacker`
  - This approach makes hard to discover new interfaces and requires verbose type assertions

- New Approach - Concrete Wrapper Type

  - In Go 1.20, to extend `http.ResponseWriter` without breaking compatibility 
  - `http.NewResponseController(rw)` returns a `http.ResponseController` that wraps `http.ResponseWriter`
  - New optional methods are exposed via this wrapper, avoiding interface modification.

- Checking for Optional Methods using Error Handling

  - Instead of type assertions, optional functionality is checked using error comparison:

  - ````go
    err = rc.Flush()
    if err != nil && !errors.Is(err, http.ErrNotSupported) { /* handle error */ }
    ````

  - If `Flush` is unsupported, program handles it gracefully.

- Advantages of `http.ResponseController`
  - New methods can be added **without breaking existing implementations**.
  - Makes **new functionality discoverable** and easy to use.
  - Provides a **standardized way** to check for optional methods using error handling
- Future Use
  - More optional methods (like SetReadDeadline, SetWriteDeadline) are added via http.ResponseController.
  - This pattern will likely be used for future extensions of http.ResponseWriter.

## Structured Logging

- The Go standard library initially included the log package for simple logging, which lacked support for structured logs.
- Structured logs use a consistent format for each entry, facilitating automated processing and analysis.

#### Challenges with Unstructured Logging

- Modern web services handle millions of users simultaneously, necessitating automated log analysis.
- Unstructured logs complicate pattern recognition and anomaly detection due to inconsistent formatting.

#### Introduction of `log`/`slog` Package

- Go 1.21 introduced the log/slog package to address structured logging needs.
- This addition promotes consistency and interoperability among Go modules.

#### Advantages of Standardized Structured Logging

- Prior to log/slog, various third-party loggers like zap, logrus, and go-kit log offered structured logging, leading to fragmentation.
- A unified standard library logger simplifies integration and control over log outputs and levels.

- Structured logging was introduced as a separate package (log/slog) rather than modifying the existing log package to maintain clear and distinct APIs.
- The API is scalable, starting with simple default loggers and allowing for advanced configurations.

#### Basic Usage of log/slog

- Provides functions like `slog.Debug`, `slog.Info`, `slog.Warn`, and `slog.Error` for logging at various levels.
- Default logger output includes timestamp, log level, and message.
- Supports adding custom key-value pairs to log entries for enhanced context.

````go
userID := "fred"
loginCount := 20
slog.Info("user login", "id", userID, "login_count", loginCount)

// output
2023/04/20 23:36:38 INFO user login id=fred login_count=20
````

#### **Customizing Log Output Formats**:

- Allows switching from text to JSON format for logs.

````go
options := &slog.HandlerOptions{Level: slog.LevelDebug}
handler := slog.NewJSONHandler(os.Stderr, options)
mySlog := slog.New(handler)
lastLogin := time.Date(2023, 01, 01, 11, 50, 00, 00, time.UTC)
mySlog.Debug("debug message", "id", userID, "last_login", lastLogin)

// ouput
{"time":"2023-04-22T23:30:01.170243-04:00","level":"DEBUG","msg":"debug message","id":"fred","last_login":"2023-01-01T11:50:00Z"}
````

#### Performance Consideration

- To optimize performance and reduce allocations, use LogAttrs with predefined attribute types.

````go
mySlog.LogAttrs(ctx, slog.LevelInfo, "faster logging",
            slog.String("id", userID),
            slog.Time("last_login", lastLogin))
````

#### Interoperability with Existing log Package:

- The log package remains supported; log/slog offers enhanced features without deprecating existing functionality.
- Bridging between log and slog is possible using slog.NewLogLogger.

````go
myLog := slog.NewLogLogger(mySlog.Handler(), slog.LevelDebug)
myLog.Println("using the mySlog Handler")

// 
{"time":"2023-04-22T23:30:01.170269-04:00","level":"DEBUG","msg":"using the mySlog Handler"}
````

**Additional Features of log/slog**:

- Supports dynamic logging levels and context integration.
- Offers value grouping and common header creation for logs.
- Detailed API documentation provides further insights into advanced functionalities.

---

## File: go/lego/ch14.md

# The Context
* Server has metadata on individual requests which could be 2 types
	* Metadata related to request processing
	* Metadata related to stop processing the request
* Example: tracking-id in an HTTP Server
## What is the Context?
* A context is an **instance** that meets the `Context` interface defined in `context` package
* Go encourages explicit data passing via function parameters
* Go has convention that context is explicitly passed as first parameter of a function with name `ctx`
```go
func logic(ctx context.Context, info string) (string, err) {
	// do something here
	return "", nil
}
```
* `context` package has several factory functions for creating and wrapping contexts.
* `context.Background`: creates empty initial context
* Each time when metadata is added to a context, its done by *wrapping* the existing context by using one of factory methods in `context`
NOTE: `context` was added much later in Go APIs after `net/http` was released, because of compatibility promise, there is no way to change `http.Handler` interface to add a `context.Context` parameter.

General Pattern with `http.Handler`
* `Context` returns the `context.Context` associated with request
* `WithContext` takes in a `context.Context` and returns a new `http.Request` with old request's state combined with the supplied context.
```go
// this middleware wraps the context with other code
func Middleware(handler http.Handler) http.Handler {
	return http.HandlerFunc(func(rw http.ResponseWriter, req *http.Request) {
		ctx := req.Context()
		// wrap context with stuff --
		req = req.WithContext(ctx)
		handler.ServeHTTP(rw, req)
	})
}
// now in handler function you can extract this context
// ctx := req.Context()
```

* Derived Contexts
	* `context.WithValue(parent, key,  value)`
	* `context.WithDeadline(parent, time)`
	* `context.WithTimeout(parent, duration)`
	* `context.WithCancel(parent)`
## Values
* Data should be passed through explicit parameters
* In some cases like HTTP request handler, we have two parameters : one for request, other for response, passing values explicitly is not possible.
* context is used to make available a value to the handler in middleware
* `context.Withvalue` takes three values
	* context (`context.Context` type)
	* key (any type, must be comparable)
	* value (any type)
```go
ctx := context.Background()
if myVal, ok := ctx.Value(myKey).(int); !ok {
	fmt.Println("no value")
} else {
	fmt.Println("value:", myVal)
}
```
* Two pattern to ensure key is unique and comparable
* First Pattern
	* create unexported type for the key: `type UserKey int` based on `int`
	* declare unexported constant of type

```go
// declaring unexported constant
const(
	_ userKey = iota
	key
)
```
* With Unexported Constant, you can be sure, no other package can modify/add data to your context that would cause collision.
* Build an API to place/read value into context
* Making these functions public/private is user's choice
```go
func ContextWithUser(ctx context.Context, user string) context.Context {
    return context.WithValue(ctx, key, user)
}

func UserFromContext(ctx context.Context) (string, bool) {
    user, ok := ctx.Value(key).(string)
    return user, ok
}
```

* Second Option
	* define unexported key types as empty struct : `type userKey struct{}`
```go
func ContextWithUser(ctx context.Context, user string) context.Context {
    return context.WithValue(ctx, userKey{}, user)
}

func UserFromContext(ctx context.Context) (string, bool) {
    user, ok := ctx.Value(userKey{}).(string)
    return user, ok
}
```

Example : middleware that extracts a user ID from a cookie

```go
// a real implementation would be signed to make sure
// the user didn't spoof their identity
func extractUser(req *http.Request) (string, error) {
    userCookie, err := req.Cookie("identity")
    if err != nil {
        return "", err
    }
    return userCookie.Value, nil
}

func Middleware(h http.Handler) http.Handler {
    return http.HandlerFunc(func(rw http.ResponseWriter, req *http.Request) {
        user, err := extractUser(req)
        if err != nil {
            rw.WriteHeader(http.StatusUnauthorized)
            rw.Write([]byte("unauthorized"))
            return
        }
        ctx := req.Context()
        ctx = ContextWithUser(ctx, user)
        req = req.WithContext(ctx)
        h.ServeHTTP(rw, req)
    })
}
```
* In most cases, you want to extract the value from the context in your request handler and pass it in to your business logic explicitly. Go functions have explicit parameters, and you shouldn’t use the context as a way to sneak values past the API
## Cancellation
* Context also allows to control responsiveness of application and co-ordinate concurrent goroutines
* Scenario: Let's say there are multiple goroutines requesting HTTP resource concurrently, we want to cancel all goroutines if any one of them fails.
* `context.WithCancel` takes `context.Context` and parameter and returns `context.Context` and a `context.CancelFunc`
* cancel function must be called when context exits. Use `defer` to invoke it.
```go
ctx, cancelFunc := context.WithCancel(context.Background())
defer cancelFunc()
```
* how to detect context cancellation ? `context.Context` has a method called `Done`. It returns a channel of type `struct{}` (empty struct uses no memory :). This channel is closed when the `cancel` function is invoked.

* First, create cancellable context, a channel to get data back from your goroutines, and `sync.WaitGroup` to allow wait until goroutines have completed

```go
ctx, cancelFunc := context.WithCancel(context.Background())
defer cancelFunc()
ch := make(chan string)
var wg sync.WaitGroup
wg.add(2)
```
* Next launch 2 goroutines, one calls URL that randomly returns bad status, and other sends a canned JSON response after delay

```go

    go func() {
        defer wg.Done()
        for {
            // return one of these status code at random
            resp, err := makeRequest(ctx,
                "http://httpbin.org/status/200,200,200,500")
            if err != nil {
                fmt.Println("error in status goroutine:", err)
                cancelFunc()
                return
            }
            if resp.StatusCode == http.StatusInternalServerError {
                fmt.Println("bad status, exiting")
                cancelFunc()
                return
            }
            select {
            case ch <- "success from status":
            case <-ctx.Done():
            }
            time.Sleep(1 * time.Second)
        }
    }()

// delay goroutine
    go func() {
        defer wg.Done()
        for {
            // return after a 1 second delay
            resp, err := makeRequest(ctx, "http://httpbin.org/delay/1")
            if err != nil {
                fmt.Println("error in delay goroutine:", err)
                cancelFunc()
                return
            }
            select {
            case ch <- "success from delay: " + resp.Header.Get("date"):
            case <-ctx.Done():
            }
        }
    }()

// finally use for/select pattern to read data from channel writen by goroutines and wait for cancellation

loop:
    for {
        select {
        case s := <-ch:
            fmt.Println("in main:", s)
        case <-ctx.Done():
            fmt.Println("in main: cancelled!")
            break loop
        }
    }
    wg.Wait()
```

* above solution doesn't include the error that caused the cancellation
* `context.WithCancelCause` can be used to report the cause of error.

```go

// changes in main
ctx, cancelFunc := context.WithCancelCause(context.Background())
defer cancelFunc(nil)

// changes in reqeusts coroutine
resp, err := makeRequest(ctx, "http://httpbin.org/status/200,200,200,500")
if err != nil {
    cancelFunc(fmt.Errorf("in status goroutine: %w", err))
    return
}
if resp.StatusCode == http.StatusInternalServerError {
    cancelFunc(errors.New("bad status"))
    return
}
ch <- "success from status"
time.Sleep(1 * time.Second)


// changes in delay function
resp, err := makeRequest(ctx, "http://httpbin.org/delay/1")
if err != nil {
    fmt.Println("in delay goroutine:", err)
    cancelFunc(fmt.Errorf("in delay goroutine: %w", err))
    return
}
ch <- "success from delay: " + resp.Header.Get("date")


// changes to for/select
loop:
    for {
        select {
        case s := <-ch:
            fmt.Println("in main:", s)
        case <-ctx.Done():
            fmt.Println("in main: cancelled with error", context.Cause(ctx))
            break loop
        }
    }
    wg.Wait()
    fmt.Println("context cause:", context.Cause(ctx))


```
## Contexts with Deadlines

* server cannot serve infinite request, to scale and handle load servers can
	* limit simultaneous requests
	* limit number of queued requests waiting to run
	* limit the amt of time a request can run
	* limit the resources per request can use (memory/disk)
* Go provides tools to handle first 3 causes
* Context provides limit on how long a code runs
* Two functions that can be used to create time-limited context
	* `context.WithTimeout` : triggers cancellation after specified amount of time has elapsed
	* `context.WithDeadline` : triggers cancellation after specific time has elapsed

```go
ctx := context.Background()
parent, cancel := context.WithTimeout(ctx, 2*time.Second)
defer cancel()
child, cancel2 := context.WithTimeout(parent, 3*time.Second)
defer cancel2()
start := time.Now()
<-child.Done()   // wait for child context to finish
end := time.Now()
fmt.Println(end.Sub(start).Truncate(time.Second))

// output will be 2seconds, since child is derived from parent which should be cancelled in 2 seconds
```

* in above example parent has 2 seconds timeout, child has 3 seconds of timeout.
* The `Err` method returns `nil` if context is still active or it returns one of two sentinel errors : `context.Cancelled` or `context.DeadlineExceeded`
## Context Cancellation in Your Own Code

* When to handle Context Cancellation ?
	* Usually not needed if your code runs quickly
	* Required when calling external services (e.g., HTTP requests, database queries) to **propagate context** for proper cancellation handling.
	* Important in **long-running functions** or **channel-based communication** in goroutines.
* Key Situation to Handle Context Cancellations
	* **When using select with channels**
		* Always include a case for <-ctx.Done() to exit early.
	* **When writing long-running code**
		* Periodically check context.Cause(ctx), which returns an error if the context is canceled.
* **Cancellation Pattern in Long-Running Code**
	* Ensures the function can **gracefully exit** if the context is canceled.
	* Can return **partial results** if needed
```go
func longRunningComputation(ctx context.Context, data string) (string, error) {
    for {
        // Check for cancellation periodically
        if err := context.Cause(ctx); err != nil {
            return "", err // Exit early if canceled
        }
        // Continue processing
    }
}
```

* **Example: Calculating π with Cancellation**
```go
i := 0
for {
    if err := context.Cause(ctx); err != nil {
        fmt.Println("Cancelled after", i, "iterations")
        return sum.Text('g', 100), err
    }
    var diff big.Float
    diff.SetInt64(4)
    diff.Quo(&diff, &d)
    if i%2 == 0 {
        sum.Add(&sum, &diff)
    } else {
        sum.Sub(&sum, &diff)
    }
    d.Add(&d, two)
    i++
}
```

* Uses the **Leibniz algorithm** to compute π.
* The loop checks context.Cause(ctx) to **stop when canceled**.
* Allows control over **how long** the computation runs.

---

## File: go/lego/ch15.md

# Writing Tests

* Automated Testing improves code quality significantly.
## Understanding the Basics of Testing

* Go's testing support has two parts : libraries & tooling
* `testing` package in standard library provides the types & functions to write tests
* `go test` tool bundled with Go runs your tests and generates reports
* `tests` in go are placed in the same directory as your package so as to access unexported variables and functions.

```go
// sample_code/adder/adder.go
func addNumbers(x, y int) int {
	return x + x
}
```

```go
// adder_test.go
func Test_addNumbers(t *testing.T) {
	res := addNumbers(2, 3)
	if res != 5 {
		t.Error("incorrect result: expected 5, got", res)
	}
	// notice nothing is returned in tests
}
```

* for writing tests for `foo.go` , create `foo_test.go` to write test.
* Test Functions start with word `Test` and take single parameter of type `*testing.T`
* for testing unexported function use `Test_<func_name>`
* `got test` runs the test functions in current directory
### Reporting Test Failures
* There are multiple methods on `*testing.T` for reporting test failures
	* `Error` : builds an error out of description string
	* `Errorf` : adds support for `Printf` style formatting
	* `Fatal` & `Fatalf` : halts entire test run when it is encountered

### Setting Up and Tearing Down
```go
var testTime time.Time

// this is used to setup the state
func TestMain(m *testing.M) {
    fmt.Println("Set up stuff for tests here")
    testTime = time.Now()
    exitVal := m.Run()
    fmt.Println("Clean up stuff after tests here")
    os.Exit(exitVal)
}

func TestFirst(t *testing.T) {
    fmt.Println("TestFirst uses stuff set up in TestMain", testTime)
}

func TestSecond(t *testing.T) {
    fmt.Println("TestSecond also uses stuff set up in TestMain", testTime)
}
```
* `TestMain` is useful in two common scenarios
	* setup data in external repository such as database
	* code being tested depends on package-level variables initialization
* `Cleanup` method cleans up temporary resources created for a single test, for simple test cases you could use `defer`
```go
// createFile is a helper function called from multiple tests
func createFile(t *testing.T) (_ string, err error) {
    f, err := os.Create("tempFile")
    if err != nil {
        return "", err
    }
    defer func() {
        err = errors.Join(err, f.Close())
    }()
    // write some data to f
    t.Cleanup(func() {
        os.Remove(f.Name())
    })
    return f.Name(), nil
}

func TestFileProcessing(t *testing.T) {
    fName, err := createFile(t)
    if err != nil {
        t.Fatal(err)
    }
    // do testing, don't worry about cleanup
}
```
* for temporary files correct method is to use `TempDir` method in `*testing.T`, which register cleanup itself.

### Testing with Environment Variables
* env variables are used configure application
* `t.Setenv()` can register a value for an environment variable for test, NOTE: It exits when test ends by calling cleanup.
```go
// assume ProcessEnvVars is a function that processes environment variables
// and returns a struct with an OutputFormat field
func TestEnvVarProcess(t *testing.T) {
    t.Setenv("OUTPUT_FORMAT", "JSON")
    cfg := ProcessEnvVars()
    if cfg.OutputFormat != "JSON" {
        t.Error("OutputFormat not set correctly")
    }
    // value of OUTPUT_FORMAT is reset when the test function exits
}
```

#### Storing Sample Test Data
* create a subdirectory name `testdata` to hold files
* while reading files from this directory, use a relative file reference and Go reserves this dir for this purpose.

#### Caching Test Results
* NOTE: Go caches test results by default, go runs tests only if there is any change in package or the `testdata` directory
* To enable running tests always use `-count=1` flag in `go test`

### Testing Your Public API

 * By default since tests are included in package, allowing testing exported and unexported function.
 * To write tests just for public API of your package, Go suggests using `packagename_test` for the package name.

```go
// file sample_code/pubadder/adder.go
func AddNumbers(x, y int) int {
    return x + y
}

// file : adder_public_test.go
package pubadder_test

import (
    "github.com/learning-go-book-2e/ch15/sample_code/pubadder"
    "testing"
)

func TestAddNumbers(t *testing.T) {
    result := pubadder.AddNumbers(2, 3)
    if result != 5 {
        t.Error("incorrect result: expected 5, got", result)
    }
}
```

### Using go-cmp to Compare Test Results
* `reflect.DeepEqual` has already been used to compare structs, maps, and slices.
* Google released a third-party module called `go-cmp` for performing comparisons and return detailed description of what doesn't match.
* import `github.com/google/go-cmp/cmp` in your codebase, then u can use `cmp.Diff` function to compare results

```go
result := CreatePerson("Dennis", 37)
if diff := cmp.Diff(expected, result); diff != "" {
	t.Error(diff)
}
```

* To use custom comparator you can do following
```go
comparer := cmp.Comparer(func(x, y Person) bool {
    return x.Name == y.Name && x.Age == y.Age
})

// then pass it in Diff
if diff := cmp.Diff(expected, result, comparer); diff != "" {
    t.Error(diff)
}
```
## Running Table Tests

* lot of testing logic is repetitive like, setting up functions and data
* *table tests* is provided by Go for this purpose explicitly
```go
func TestDoMath(t *testing.T) {
    result, err := DoMath(2, 2, "+")
    if result != 4 {
        t.Error("Should have been 4, got", result)
    }
    if err != nil {
        t.Error("Should have been nil error, got", err)
    }
    result2, err2 := DoMath(2, 2, "-")
    if result2 != 0 {
        t.Error("Should have been 0, got", result2)
    }
    if err2 != nil {
        t.Error("Should have been nil error, got", err2)
    }
    // and so on...
}
```
* Above can simplified using test tables
```go
data := []struct {
    name     string
    num1     int
    num2     int
    op       string
    expected int
    errMsg   string
}{
    {"addition", 2, 2, "+", 4, ""},
    {"subtraction", 2, 2, "-", 0, ""},
    {"multiplication", 2, 2, "*", 4, ""},
    {"division", 2, 2, "/", 1, ""},
    {"bad_division", 2, 0, "/", 0, `division by zero`},
}

for _, d := range data {
    t.Run(d.name, func(t *testing.T) {
        result, err := DoMath(d.num1, d.num2, d.op)
        if result != d.expected {
            t.Errorf("Expected %d, got %d", d.expected, result)
        }
        var errMsg string
        if err != nil {
            errMsg = err.Error()
        }
        if errMsg != d.errMsg {
            t.Errorf("Expected error message `%s`, got `%s`",
                d.errMsg, errMsg)
        }
    })
}
```
## Running Tests Concurrently
* By default, unit tests are run sequentially
* Since test cases are independent from each other they can be run concurrently.
```go
func TestMyCode(t *testing.T) {
	t.Parallel()
	// rest of test goes here
}
```

* NOTE: Be careful because before Go 1.21 or earlier version, a reference to the variable `d` is shared by all parallel tests, so they all see the same value. `go vet` is able detect such scenarios by indicating `loop variable d captured by func literal` on each line where `d` is captured.
```go
func TestParallelTable(t *testing.T) {
    data := []struct {
        name   string
        input  int
        output int
    }{
        {"a", 10, 20},
        {"b", 30, 40},
        {"c", 50, 60},
    }
    for _, d := range data {
	    // fix for older version
		// d := d  // shadow
        t.Run(d.name, func(t *testing.T) {
            t.Parallel()
            fmt.Println(d.input, d.output)
            out := toTest(d.input)
            if out != d.output {
                t.Error("didn't match", out, d.output)
            }
        })
    }
}
```
## Checking Your Code Coverage

* although code coverage eliminates obvious problems, 100% coverage doesn't guarantee that there is no bug in your code.
* Adding the `-cover` flag to `go test` calculates coverage information and includes a summary in test output
* `-coverprofile` : used to save coverage information to a file
* `go test -v -cover -coverprofile=c.out`
* for html report : `go tool cover -html=c.out`

## Fuzzing

* one of the most important lessons that every dev learns eventually, is all data is suspect. No matter how well specified a data format is, you will eventually have to process input that doesn't match what you expect
* Even when test cases are 100% coverage and written in good manner, its impossible to think of everything. To supplement test cases with generated data helps you catch unexpected errors.
* Fuzzing : technique for generating random data and submitting it to code to see whether it properly handles unexpected input.
* Devs can provide *seed corpus* which serves as the initial input for *fuzzer* for generating bad input.
* [Example Code](https://github.com/learning-go-book-2e/file_parser)
```go
func ParseData(r io.Reader) ([]string, error) {
    s := bufio.NewScanner(r)
    if !s.Scan() {
        return nil, errors.New("empty")
    }
    countStr := s.Text()
    count, err := strconv.Atoi(countStr)
    if err != nil {
        return nil, err
    }
    out := make([]string, 0, count)
    for i := 0; i < count; i++ {
        hasLine := s.Scan()
        if !hasLine {
            return nil, errors.New("too few lines")
        }
        line := s.Text()
        out = append(out, line)
    }
    return out, nil
}
```

* Unit Tests for above function cover 100%
```go
func TestParseData(t *testing.T) {
    data := []struct {
        name   string
        in     []byte
        out    []string
        errMsg string
    }{
        {
            name:   "simple",
            in:     []byte("3\nhello\ngoodbye\ngreetings\n"),
            out:    []string{"hello", "goodbye", "greetings"},
            errMsg: "",
        },
        {
            name:   "empty_error",
            in:     []byte(""),
            out:    nil,
            errMsg: "empty",
        },
        {
            name:   "zero",
            in:     []byte("0\n"),
            out:    []string{},
            errMsg: "",
        },
        {
            name:   "number_error",
            in:     []byte("asdf\nhello\ngoodbye\ngreetings\n"),
            out:    nil,
            errMsg: `strconv.Atoi: parsing "asdf": invalid syntax`,
        },
        {
            name:   "line_count_error",
            in:     []byte("4\nhello\ngoodbye\ngreetings\n"),
            out:    nil,
            errMsg: "too few lines",
        },
    }
    for _, d := range data {
        t.Run(d.name, func(t *testing.T) {
            r := bytes.NewReader(d.in)
            out, err := ParseData(r)
            var errMsg string
            if err != nil {
                errMsg = err.Error()
            }
            if diff := cmp.Diff(d.out, out); diff != "" {
                t.Error(diff)
            }
            if diff := cmp.Diff(d.errMsg, errMsg); diff != "" {
                t.Error(diff)
            }
        })
    }
}
```

* Writing a fuzz test
```go
func FuzzParseData(f *testing.F) {
    testcases := [][]byte{
        []byte("3\nhello\ngoodbye\ngreetings\n"),
        []byte("0\n"),
    }
    for _, tc := range testcases {
		f.Add(tc)  // seed corpus
    }
    f.Fuzz(func(t *testing.T, in []byte) {
        r := bytes.NewReader(in)
        out, err := ParseData(r)
        if err != nil {
            t.Skip("handled error")
        }
        roundTrip := ToData(out)
        rtr := bytes.NewReader(roundTrip)
        out2, err := ParseData(rtr)
        if diff := cmp.Diff(out, out2); diff != "" {
            t.Error(diff)
        }
    })
}
```

* `go test -fuzz=FuzzParseData`
* to find out where your fuzz test has failed, fuzzer writes failed testcases to *testdata/fuzz/TESTNAME*, adding a new entry to seed corpus.
* The new seed corpus entry in file now becomes a new unit test, one the was automatically generated by the fuzzer. It is run anytime `go test` runs the `FuzzParsedData` function, and acts as a regression test once you fix your bug.
* 
## Using Benchmarks
* Go has built-in support for benchmarking
```go
func FileLen(f string, bufsize int) (int, error) {
    file, err := os.Open(f)
    if err != nil {
        return 0, err
    }
    defer file.Close()
    count := 0
    for {
        buf := make([]byte, bufsize)
        num, err := file.Read(buf)
        count += num
        if err != nil {
            break
        }
    }
    return count, nil
}
```
* Above function counts number of characters in a file.
* `*testing.B` includes all benchmarking functionality, This type includes all functionality of a `*testing.T` as well additional support for benchmarking.
* Every Go benchmark has a loop that iterates from 0 to `b.N`
```go
var blackhole int // interesting usage to stop compiler from becoming too clever to optimize the FileLen, ruining Benchmark

func BenchmarkFileLen1(b *testing.B) {
    for i := 0; i < b.N; i++ {
        result, err := FileLen("testdata/data.txt", 1)
        if err != nil {
            b.Fatal(err)
        }
        blackhole = result
    }
}
```
* Running Test Cases: `go test -bench=.` or you can use `-benchmen` to test memory allocation information in the benchmark output
```go
func BenchmarkFileLen(b *testing.B) {
    for _, v := range []int{1, 10, 100, 1000, 10000, 100000} {
        b.Run(fmt.Sprintf("FileLen-%d", v), func(b *testing.B) {
            for i := 0; i < b.N; i++ {
                result, err := FileLen("testdata/data.txt", v)
                if err != nil {
                    b.Fatal(err)
                }
                blackhole = result
            }
        })
    }
}
```

```text
BenchmarkFileLen/FileLen-1-12          25  47828842 ns/op   65342 B/op  65208 allocs/op
BenchmarkFileLen/FileLen-10-12        230   5136839 ns/op  104488 B/op   6525 allocs/op
BenchmarkFileLen/FileLen-100-12      2246    509619 ns/op   73384 B/op    657 allocs/op
BenchmarkFileLen/FileLen-1000-12    16491     71281 ns/op   68744 B/op     70 allocs/op
BenchmarkFileLen/FileLen-10000-12   42468     26600 ns/op   82056 B/op     11 allocs/op
BenchmarkFileLen/FileLen-100000-12  36700     30473 ns/op  213128 B/op      5 allocs/op
```

## Using Stubs in Go
* Go allows you to abstract function calls in two ways, defining a function type and defining an interface.
* These abstractions help you write not only modular production code but also unit tests.
```go
// struct 
type Processor struct {
	Solver MathSolver
}
type MathSolver interface {
	REsolve(ctx context.Context, expression string) (float64, error)
}

// Processor has an expression from an io.reader and returns calculated value
func (p Processor) ProcessExpression(ctx context.Context, r io.Reader)
                                    (float64, error) {
    curExpression, err := readToNewLine(r)
    if err != nil {
        return 0, err
    }
    if len(curExpression) == 0 {
        return 0, errors.New("no expression to read")
    }
    answer, err := p.Solver.Resolve(ctx, curExpression)
    return answer, err
}

```
* Running Test cases for above Code
```go
type MathSolverStub struct{}

func (ms MathSolverStub) Resolve(ctx context.Context, expr string)
                                (float64, error) {
    switch expr {
    case "2 + 2 * 10":
        return 22, nil
    case "( 2 + 2 ) * 10":
        return 40, nil
    case "( 2 + 2 * 10":
        return 0, errors.New("invalid expression: ( 2 + 2 * 10")
    }
    return 0, nil
}

func TestProcessorProcessExpression(t *testing.T) {
    p := Processor{MathSolverStub{}}
    in := strings.NewReader(`2 + 2 * 10
( 2 + 2 ) * 10
( 2 + 2 * 10`)
    data := []float64{22, 40, 0}
    hasErr := []bool{false, false, true}
    for i, d := range data {
        result, err := p.ProcessExpression(context.Background(), in)
        if err != nil && !hasErr[i] {
            t.Error(err)
        }
        if result != d {
            t.Errorf("Expected result %f, got %f", d, result)
        }
    }
}
```

* If interface is too large and you have to stub multiple interfaces then just implement the Stubs which are request in the context of current test
* In scenario where you have to implement multiple methods, better solution is to create a Stub Struct that proxies method calls to function fields.
## Using httptest

* It can be difficult to write tests for functions that call an HTTP service.
* Traditionally, this became integration by bringing up a mock instance of service that the function calls.
* `net/http/httptest` package makes it easier to stub HTTP services
```go
type RemoteSolver struct {
    MathServerURL string
    Client        *http.Client
}

func (rs RemoteSolver) Resolve(ctx context.Context, expression string)
                              (float64, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodGet,
        rs.MathServerURL+"?expression="+url.QueryEscape(expression),
        nil)
    if err != nil {
        return 0, err
    }
    resp, err := rs.Client.Do(req)
    if err != nil {
        return 0, err
    }
    defer resp.Body.Close()
    contents, err := io.ReadAll(resp.Body)
    if err != nil {
        return 0, err
    }
    if resp.StatusCode != http.StatusOK {
        return 0, errors.New(string(contents))
    }
    result, err := strconv.ParseFloat(string(contents), 64)
    if err != nil {
        return 0, err
    }
    return result, nil
}
```

* Writing test case for this
```go
// stores io data for server
type info struct {
    expression string
    code       int
    body       string
}
var io info

// setup fake remote server
server := httptest.NewServer(
    http.HandlerFunc(func(rw http.ResponseWriter, req *http.Request) {
        expression := req.URL.Query().Get("expression")
        if expression != io.expression {
            rw.WriteHeader(http.StatusBadRequest)
            fmt.Fprintf(rw, "expected expression '%s', got '%s'",
                io.expression, expression)
            return
        }
        rw.WriteHeader(io.code)
        rw.Write([]byte(io.body))
    }))
defer server.Close()
rs := RemoteSolver{
    MathServerURL: server.URL,
    Client:        server.Client(),
}

// writing actual test cases
data := []struct {
    name   string
    io     info
    result float64
}{
    {"case1", info{"2 + 2 * 10", http.StatusOK, "22"}, 22},
    // remaining cases
}
for _, d := range data {
    t.Run(d.name, func(t *testing.T) {
        io = d.io
        result, err := rs.Resolve(context.Background(), d.io.expression)
        if result != d.result {
            t.Errorf("io `%f`, got `%f`", d.result, result)
        }
        var errMsg string
        if err != nil {
            errMsg = err.Error()
        }
        if errMsg != d.errMsg {
            t.Errorf("io error `%s`, got `%s`", d.errMsg, errMsg)
        }
    })
}
```
## Using Integration Tests and Build Tags

* **Integration Tests and Build Tags**
	* **Integration tests** validate the interaction between your application and external services.
	* They are run **less frequently** than unit tests due to dependency on external systems and execution time.
	* **Build tags** (e.g., //go:build integration) control when certain test files are compiled and run.
	* Run integration tests using: `go test -tags integration -v ./...`
	* Some developers prefer **environment variables** over build tags for better discoverability (t.Skip with an explanation).
* **Using the -short Flag**
	* The -short flag is used to **skip slow tests** when running go test.
	* Example usage:
```go
if testing.Short() {
    t.Skip("skipping test in short mode.")
}
```
* Limitation: It only differentiates between “short” and “all” tests, whereas build tags allow **grouping tests by dependencies**.
## Finding Concurrency Problems with the Data Race Detector
* **Data races** occur when multiple goroutines access the same variable without proper synchronization.
* Go’s **race detector** can identify such issues using:
```go
go test -race
```

* Example of a race condition
```go
var counter int
go func() { counter++ }()
```

* **Avoid “fixing” races** with arbitrary sleep calls; use proper **mutexes** or **channels** instead.
* Race detection **slows execution (~10×)**, so it’s not enabled by default in production.


---

## File: go/lego/ch16.md

# Here Be Dragons: Reflect, Unsafe, and Go
* when the type of the data can’t be determined at compile time, you can use the reflection support in the `reflect` package to interact with and even construct data. 
* When you need to take advantage of the memory layout of data types in Go, you can use the `unsafe` package. 
* if there is functionality that can be provided only by libraries written in C, you can call into C code with `cgo`.
## Reflections Lets You work with Types at Runtime
* **Definition**: Reflection allows working with types and variables dynamically at runtime.
* It provides the ability to examine, modify, and create variables, functions, and structs at runtime.
* Reflection are often encountered at boundary of your program and external world.
* **Use Cases**:
	* Database operations (database/sql)
	* Templating (text/template, html/template)
	* Formatting (fmt package)
	* Error handling (errors.Is, errors.As)
	* Sorting (sort.Slice, etc.)
	* Data serialization (encoding/json, encoding/xml)
* **Performance Impact**
	* Slower than normal type-based operations.
	* More complex and fragile; can lead to panics if misused.
	* Should be used only when necessary.
* **Risks**
	* Can cause crashes if misused.
	* Code using unsafe may break in future Go versions.
### Types, Kinds, and Values
* reflection is built around three core concepts : types, kinds, values
#### Types and kinds
* **Type**: Defines a variable’s properties, what it can hold, and how it behaves.
	* Obtained using reflect.TypeOf(v).
	* Name() gives the type’s name (e.g., "int", "Foo")
* **Kind**: Represents the underlying nature of the type (e.g., reflect.Int, reflect.Struct, reflect.Pointer).
	* Obtained using Kind().
	* Important for determining valid reflection operations to avoid panics.
* Inspecting Types
	* `Elem()`: Used to get the element type of a pointer, slice, map, or array.
	* `NumField()`: Returns the number of fields in a struct.
	* `Field(i)`: Retrieves details of a struct field, including name, type, and tags.
* working with values
	* reflect.ValueOf(v): Creates a reflect.Value instance representing a variable’s value.
	* Interface(): Retrieves the value as any, requiring type assertion to use it.
	* Type-specific methods: Int(), String(), Bool(), etc., retrieve primitive values
	* CanSet(): Checks if a value can be modified.
* modifying values
	* Requires passing a pointer to reflect.ValueOf(&v)
	* Elem(): Gets the actual value from a pointer.
	* SetInt(), SetString(), Set(): Modify values if CanSet() is true.
* Creating New Values
	* reflect.New(t): Creates a new instance of a type (reflect.Value)
	* MakeChan(), MakeMap(), MakeSlice(): Create respective Go data structures
	* Append(): Adds elements to a slice
* checking Nil interfaces
	* IsValid(): Checks if a reflect.Value holds anything (false for nil).
	* IsNil(): Checks if the value is nil (only for pointer, slice, map, func, or interface kinds).
### Use Reflection to Write a Data Marshaler
* Using Reflection to Write a Data Marshaler
	* The Go standard library lacks automatic CSV-to-struct mapping.
	* **Goal:** Create a CSV marshaler/unmarshaler using reflection.
* **Defining the Struct API**
	* Struct fields are annotated with csv tags.
	* Marshal and Unmarshal functions map between CSV slices and struct slices
* Implement Marshal
	* Ensures input is a slice of structs.
	* Extracts headers from struct field tags.
	* Iterates over struct values, converts fields to strings using reflection.
* Helper Functions for Marshaling
	* marshalHeader(vt reflect.Type): Extracts CSV tags as column names.
	* marshalOne(vv reflect.Value): Converts struct fields to strings using reflect.Kind.
* Implement Unmarshal
	* Ensures input is a pointer to a slice of structs.
	* Uses the first row as a header for field mapping.
	* Iterates over CSV rows, converts strings to the correct types, and appends structs to the slice.
* Helper Functions for Unmarshalling
	* unmarshalOne(row []string, namePos map[string]int, vv reflect.Value): Converts CSV values to struct fields based on their types.
* Integration with csv Package
	* Uses csv.NewReader and csv.NewWriter for reading/writing CSV files.
	* Calls Unmarshal to parse CSV data into structs and Marshal to convert structs back into CSV.
### Build Function with Reflection to Automate Repetitive Tasks

* **Creating a Function Wrapper with Reflection**
	* MakeTimedFunction(f any): Wraps any function to measure execution time
	* Uses `reflect.MakeFunc` to generate a new function.
	* Calls the original function using `reflect.Value.Call`.
```go
func timeMe(a int) int {
    time.Sleep(time.Duration(a) * time.Second)
    return a * 2
}
timed := MakeTimedFunction(timeMe).(func(int) int)
fmt.Println(timed(2))
```
* Caveats
	* Generated functions can obscure program flow
	* Reflection slows execution - use it only when necessary

### Use Reflection Only if it's Worthwhile
**Struct Creation and Reflection Limitations**
* **Dynamically Creating Structs**
	* reflect.StructOf allows creating new struct types at runtime.
	* Rarely useful outside of advanced use cases (e.g., memoization).
* **Reflection Cannot Create Methods**
	* No way to add methods to a type via reflection.
	* Cannot dynamically implement an interface.
* **When to Avoid Reflection**
	* Reflection is powerful but slow.
	* Use only when interacting with external data formats (e.g., JSON, CSV, databases).
	* Prefer generics or standard type assertions when possible.

## unsafe is Unsafe
* **Why Use unsafe?**
	* The unsafe package allows direct memory manipulation, bypassing Go’s safety features.
	* Commonly used for **system interoperability** and **performance optimization**.
	* A study found **24%** of Go projects use unsafe, mostly for OS and C integration.
* **Key Features of unsafe**
	* **unsafe.Pointer**: Can be cast between any pointer types.
	* **uintptr**: An integer type that can be used for pointer arithmetic.
* **Common Patterns in unsafe Code**
	* **Type Conversion**: Converting between types not normally compatible.
	* **Memory Manipulation**: Directly modifying memory using pointers.

### Memory Layout Insights
* **Sizeof**: Returns the size (in bytes) of a type.
* **Offsetof**: Returns the memory offset of a field in a struct.
* **Field Alignment**:
	* P**adding** is added for proper alignment.
	* Reordering struct fields can optimize memory usage.
```go
type BoolInt struct { b bool; i int64 } // 16 bytes
type IntBool struct { i int64; b bool } // 16 bytes
```
* **Optimized ordering** reduces padding and memory usage.
### Using unsafe for Binary Data Conversion
* **For efficiency**, unsafe.Pointer can map binary data to Go structs.
* **Example: Network Packet Parsing**
```go
type Data struct {
    Value  uint32
    Label  [10]byte
    Active bool
}
```
* Reading binary data safely
```go
func DataFromBytes(b [16]byte) Data {
    d := Data{}
    d.Value = binary.BigEndian.Uint32(b[:4])
    copy(d.Label[:], b[4:14])
    d.Active = b[14] != 0
    return d
}
```
* Using unsafe for efficiency
```go
func DataFromBytesUnsafe(b [16]byte) Data {
    return *(*Data)(unsafe.Pointer(&b))
}
```

Handling Endianness
* CPUs store data in **little-endian** or **big-endian** formats.\
* Check system endianness
```go
var isLE = (*(*[2]byte)(unsafe.Pointer(new(uint16))))[0] == 0x00
```
* Reverse bytes if Needed
```go
if isLE {
    data.Value = bits.ReverseBytes32(data.Value)
}
```


### Unsafe Slices
* Convert struct to a slice
```go
func BytesFromDataUnsafeSlice(d Data) []byte {
    return unsafe.Slice((*byte)(unsafe.Pointer(&d)), unsafe.Sizeof(d))
}
```
* Convert slice to struct
```go
func DataFromBytesUnsafeSlice(b []byte) Data {
    return *(*Data)(unsafe.Pointer(unsafe.SliceData(b)))
}
```

### Performance Comparison
* **Using unsafe can significantly reduce execution time**.
* Example benchmarks on Apple Silicon M1:
	* BenchmarkBytesFromData: **2.185 ns/op**
	* BenchmarkBytesFromDataUnsafe: **0.8418 ns/op**
## Cgo is for Integration, Not Performance
* what is cgo ?
	* cgo is Go’s **Foreign Function Interface (FFI) for C**, used to call C libraries.
	* **Not meant for performance optimizations**, only for integration.
* why use cgo ?
	* **Interoperability**: Used when no Go equivalent library exists.
	* **Access to OS APIs and C libraries**: Many system-level libraries are written in C.
* How cgo works
	* Go can call C functions by embedding C code inside special comments:
```go
/*
    #cgo LDFLAGS: -lm
    #include <math.h>
*/
import "C"
fmt.Println(C.sqrt(100))
```
* The **C pseudopackage** (C.int, C.char) allows type compatibility.

### Calling Go from C
* Use //export before a Go function to expose it to C:
```go
//export doubler
func doubler(i int) int {
    return i * 2
}
```

* Requires _cgo_export.h in C code:
```C
#include "_cgo_export.h"
```

Memory Management Challenges
* Go has garbage collection, C does not.
* Cannot pass Go structs with pointers directly to C.
* Go pointers cannot be stored in C after the function returns.

**Solution: Using cgo.Handle**
* Used to wrap Go objects containing pointers before passing to C.
```go
p := Person{Name: "Jon", Age: 21}
C.in_c(C.uintptr_t(cgo.NewHandle(p)))
```
* In C, the handle is passed back to a Go function for safe use.

**cgo Performance Issues**
* **Calling C from Go is 29x slower** than a direct C-to-C call.
* **Go 1.21 benchmark**: cgo call overhead is **~40ns** on Intel Core i7-12700H.
* cgo has **processing and memory model mismatches** that prevent performance improvements.

When to use cgo
✅ Use cgo **only when necessary**, like:
* No equivalent Go library exists.
* A third-party cgo wrapper is unavailable.

❌ Avoid cgo for:
* *Performance optimizations (native Go is faster).
* **Simple tasks** that can be written in Go.

More
* [The cost and complexity of Cgo](https://www.cockroachlabs.com/blog/the-cost-and-complexity-of-cgo/)


---

## File: go/lego/ch2.md

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



---

## File: go/lego/ch3.md

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

---

## File: go/lego/ch4.md

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


---

## File: go/lego/ch5.md

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

---

## File: go/lego/ch6.md

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



---

## File: go/lego/ch7.md

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

---

## File: go/lego/ch8.md

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

---

## File: go/lego/ch9.md

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



---

## File: go/lego/index.md

# Learning Go (2nd Edition)



###   Content  

1. [Setting up Go Environment](ch1.md)
2. [Predeclared Types and Declaration](ch2.md)
3. [Composite Types](ch3.md)
4. [Blocks, Shadows and Control Structure](ch4.md)
5. [Functions](ch5.md)
6. [Pointers](ch6.md)
7. [Types, Methods, And Interfaces](ch7.md)
8. [Generics](ch8.md)
9. [Errors](ch9.md)
10. [Modules, Packages, And Imports](ch10.md)
11. [Go Tooling](ch11.md)
12. [Concurrency in Go](ch12.md)
13. [The Standard Library](ch13.md)
14. [The Context](ch14.md)
15. [Writing Tests](ch15.md)
16. [Here be Dragons: Reflect, Unsafe, And Cgo](ch16.md)

---

## File: go/notes/index.md

### Notes on Golang

- [Status Tracker Application](stat_trackr.md)

---

## File: go/notes/stat_trackr.md

### Website Status Tracker Application

This is an example of channels and parallelism in go.

Consider this code which goes through a list of websites and prints their status.

````go
package main

import (
	"fmt"
	"net/http"
)

func main() {

	links := []string{
		"http://google.com",
		"http://facebook.com",
		"http://stackoverflow.com",
		"http://golang.org",
		"http://amazon.com",
		"http://books.minetest.in",
	}
	for _, link := range links {
		checkLink(link)
	}
}

func checkLink(link string) {
	_, err := http.Get(link)  // <-- Blocking Call
	if err != nil {
		fmt.Println(link, "might be down!")
		return
	}
	fmt.Println(link, "is up!")
}
````

If we execute above program you will notice a delay in processing of each of links. Delay is present because go program waits for response from each of the website.

If we had 1000 such links, checking a website status might take a lot of time and to again check google.com might end up taking 1 hour. A website might go down and be back up in that timespace. We will fix program such that rather than serial checking of website it happens in parallel. Once a website is checked it keeps checking on.

#### Goroutine

Whenever we execute a program we basically execute a *main* goroutine. Main program executes line by line until it hits blocking function call and execution gets paused and waits for response to come back. We can create additional goroutines that will handle the blocking call so the main goroutine can keep on processing instead of getting blocked.

`go checkLink(link)` : go keyword is used to create a goroutine.

Go scheduler runs one routine until it finishes or makes a blocking call. It starts executing other goroutines in queue pausing the blocked goroutine. So its not actually parallelism instead Go scheduler smartly optimizing queues and running them Concurrently. By default go uses only one core.

In case of multiple CPU cores Go scheduler can easily spawn goroutines parallely. 

*Concurrency is not Parallelism :P*

Concurrency : Multiple threads executing code. If one thread blocks, another is picked up and worked on. Smart scheduling.

Parallelism : (Only in case of multiple CPU cores) Multiple threads executed at the exact same time. Requires multiple CPU’s.

Try adding go keyword to function and execute. Wait it doesn’t output anything :) ??? What happened is that multiple child goroutines were spawned by main goroutine but those all couldn’t complete but main goroutines reached the end and exited killing child goroutines. So we will need to make main goroutine to wait for response to come back from child goroutines.

#### Channels

Only way to communicate between goroutines. We can send messages to channels which becomes automatically gets sent to all the running goroutines that are running on machine and have access to that channel.

Channels are typed and the data shared by channel must be of same type.

```go
c := make(chan string)
```

Note we will need to pass in the channel to all the goroutines that we want to have to access to channel.

#### Sending Data through Channels

- channel<-5 : sends value 5 into the channel
- myNumber <- channel : wait for a value to be sent into the channel. When we get one, assign the value to `myNumber`
- fmt.Println(<-channel) : wait for a value to be sent into the channel. When we get one, we immediately log it out.

We will need for this application purpose all the goroutines to exit, so we will need to wait for all n channels for n websites.

Current Solution :

````go
package main

import (
	"fmt"
	"net/http"
)

func main() {

	links := []string{
		"http://google.com",
		"http://facebook.com",
		"http://stackoverflow.com",
		"http://golang.org",
		"http://amazon.com",
		"http://books.minetest.in",
	}

	c := make(chan string)

	for _, link := range links {
		go checkLink(link, c)
	}

	for i := 0; i < len(links); i++ {
		fmt.Println(<-c) // Note this stops and waits on first execution
	}

}

func checkLink(link string, c chan string) {
	_, err := http.Get(link)
	if err != nil {
		fmt.Println(link, "might be down!")
		c <- "might be down"
		return
	}
	fmt.Println(link, "is up!")
	c <- "It is up"
}
````

#### Modification

Now we are going to design Website Tracker to track website continuously. We can do easily that by sending `c<-link` in checkLink. And change line 26 to `go checkLink(<-c,c)`. This makes channel loop infinitely.

````go
for {
  go checkLink(<-c,c)
}
````

It may look like infinite loop but there is may be some delay and notice how sites go out of order because of different latency. But pinging a site so many times continously might be bad, lets fix this issue.

We will also fix above for loop with a stylistic fix, exactly same as above code.

````go
for l := range c { // waits for channel to return a val and assign to l
  go checkLink(l,c)
}
````

Time fix : Try :P

````go
for l := range c {
  time.Sleep(5 * time.Second) // This is wrong it blocks each channel by 5 sec, they are not lost but gets queued up !!
  go checkLink(l,c)
}
````

Actual fix using function literal. Attempt2 : why it keeps printing same website :P

````go
for l := range c {
  go func() {
    time.Sleep(5 * time.Second)
    go checkLink(l,c)
  }()
}
````

Complete Fixed and patched

````go
for l := range c {
  go func(link string) {
    time.Sleep(5 * time.Second)
    go checkLink(link,c)
  }(l) // always pass a copy of l to function literal, if not then l might changed by the time it gets picked up by checkLink(l,c) :P
}
````



---

