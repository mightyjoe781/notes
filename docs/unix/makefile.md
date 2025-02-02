# Makefile/Taskfile

 [:octicons-arrow-left-24:{ .icon } Back](index.md)

Task automation tools

### Taskfile

A modern, YAML-based task runner designed to simplify Tasks

1. Create a Taskfile

   ````yaml
   version: '3'
   tasks:
     build:
       cmds:
         - echo "Building..."
   ````

2. Run a Task

   ````bash
   task build
   ````

#### Taskfile Syntax

````yaml
version: '3'  # Taskfile version  

tasks:  
  <task-name>:  
    desc: "Description of the task"  
    cmds:  
      - <command-1>  
      - <command-2>  
    deps:  
      - <dependent-task>  
    vars:  
      <var-name>: <value>  
````

#### Example Taskfile

````yaml
version: '3'  

tasks:  
  greet:  
    desc: "Greet the user"  
    vars:  
      NAME: "World"  
    cmds:  
      - echo "Hello, {{.NAME}}!"  
  clean:  
    desc: "Clean build artifacts"  
    cmds:  
      - echo "Cleaning..."  
  build:  
    desc: "Build the project"  
    deps: [clean]  
    cmds:  
      - echo "Building..."  
````

#### Taskfile Example Go

```yaml
version: '3'  

tasks:  
  fmt:  
    desc: "Format Go code"  
    cmds:  
      - go fmt ./...  
  vet:  
    desc: "Vet Go code"  
    cmds:  
      - go vet ./...  
  build:
    desc: "Build the project"  
    deps: [fmt, vet]
    env:  
      GO_VERSION: "1.20"
    cmds:  
      - go build -o bin/app . 
```

#### Including Other Taskfiles

````yaml
version: '3'  

includes:  
  dev: ./tasks/dev.yml  
  prod: ./tasks/prod.yml  
````

### Makefile

1. Create a Makefile

   ````makefile
   build:
   		echo "Building..."
   ````

2. Run a Make Target

   ````bash
   make build
   ````

#### Makefile Syntax

````makefile
targets: prerequisites
	command
	command
	command
````

#### Makefile Example C

````makefile
blah: blah.c	# build target only if blah.c changes
	cc blah.c -o blah
````

#### Makefile Example Go

````bash
.DEFAULT_GOAL := build

.PHONY:fmt vet build
fmt:
	go fmt ./...

vet: fmt
	go vet ./...

build: vet
	go build
````

### Resources

* [Make File Tutorial](https://makefiletutorial.com/)
* [Taskfile Documentation](https://taskfile.dev)