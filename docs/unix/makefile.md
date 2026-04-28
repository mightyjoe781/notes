# Taskfile / Makefile

[:octicons-arrow-left-24:{ .icon } Back](index.md)

Task runners for automating build, test, lint, and deploy workflows.

## Taskfile

YAML-based task runner. Cleaner than Makefile for general-purpose automation.

### Installation

```bash
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
# or
brew install go-task
```

### Basic Taskfile.yaml

```yaml
version: '3'

tasks:
  default:
    cmds:
      - task: build

  build:
    desc: "Build the binary"
    cmds:
      - go build -o bin/app ./cmd/app

  test:
    desc: "Run tests"
    cmds:
      - go test ./...

  lint:
    desc: "Run linter"
    cmds:
      - golangci-lint run

  ci:
    desc: "Full CI pipeline"
    deps: [lint, test, build]
```

```bash
task                                 # run default task
task build
task --list                          # list all tasks with descriptions
task --dry                           # print commands without running
```

### Variables and Environment

```yaml
version: '3'

vars:
  APP: myapp
  VERSION:
    sh: git describe --tags --always  # dynamic variable from command

env:
  GO111MODULE: on

tasks:
  build:
    cmds:
      - go build -ldflags "-X main.version={{.VERSION}}" -o bin/{{.APP}} .
```

### Dependencies and Watch

```yaml
tasks:
  dev:
    desc: "Start dev server"
    deps: [build]
    cmds:
      - ./bin/app serve

  watch:
    desc: "Watch and rebuild"
    watch: true
    sources:
      - "**/*.go"
    cmds:
      - task: build
```

### Multiple Taskfiles

```yaml
includes:
  docker: ./tasks/docker.yaml
  db: ./tasks/db.yaml
```

---

## Makefile

The classic build tool. Widely understood, great for compiled languages.

### Syntax

```makefile
target: prerequisites
	command                          # indented with a TAB, not spaces
```

### Basic Makefile

```makefile
.DEFAULT_GOAL := build
.PHONY: fmt vet test build clean

fmt:
	go fmt ./...

vet: fmt
	go vet ./...

test: vet
	go test ./...

build: test
	go build -o bin/app ./cmd/app

clean:
	rm -rf bin/

run: build
	./bin/app

# Print help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'
```

### Variables

```makefile
APP      = myapp
VERSION  = $(shell git describe --tags --always)
LDFLAGS  = -ldflags "-X main.version=$(VERSION)"
BUILD    = go build $(LDFLAGS) -o bin/$(APP) ./cmd/$(APP)

build:
	$(BUILD)
```

### Pattern Rules

```makefile
# Compile each .c file to .o
%.o: %.c
	$(CC) -c $< -o $@

# $< = first prerequisite, $@ = target, $^ = all prerequisites
```

### Conditional and OS Detection

```makefile
UNAME := $(shell uname)

ifeq ($(UNAME), Darwin)
    OPEN = open
else
    OPEN = xdg-open
endif

docs:
	$(OPEN) http://localhost:6060
```

### Useful Patterns

```makefile
# Silence command echo
build:
	@echo "Building..."
	@go build -o bin/app .

# Phony targets (not real files)
.PHONY: build test clean

# Pass arguments
deploy:
	./deploy.sh $(ENV)
# usage: make deploy ENV=prod

# Run in parallel
ci:
	$(MAKE) -j lint test
```

### Taskfile vs Makefile

| Feature | Taskfile | Makefile |
|---|---|---|
| Syntax | YAML | Custom (TAB-sensitive) |
| Variables | Built-in, easy | Complex, quirky |
| Cross-platform | Yes | Requires GNU make on macOS |
| Learning curve | Low | Medium |
| Language agnostic | Yes | Yes |
| Built-in watch | Yes | No |

### See Also

- [Shell](shell.md) for scripting inside tasks
- Also: just (simpler Makefile alternative), mage (Go-based build tool), bazel (large-scale build system), gradle
