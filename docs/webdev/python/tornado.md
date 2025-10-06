# Python ~ Backend (Tornado)

## Python

* CPython Interpreter
    - CPython is most popular Python interpreter that most Python programs run on
    - It's written in C programming language
- Execution Steps
    - Source to Bytecode : Python source code (`.py` files) is converted to bytes
    - Bytecode Caching: The bytecode is cached for efficiency and is more compact than source code
    - Interpretation: The Python interpreter reads bytecode instructions one by one and converts them to corresponding C functions (since CPython in written in C)
        - Example : `print()` becomes `printf()` in C
        - Array operations become C pointer/object operations
- Key Characterstics
    - Step-by-Step Execution
    - Not direct machine code : Bytecode is not machine code that can run directly on CPU
    - Interpreter Layer

### JIT (Just-In-Time)

- Purpose : Optimized executed code by compiling it to native machine code
- Process: Takes interpreted bytecode that runs repeatedly and compiles it directly to machine instructions
- Benefit: Eliminates the interpretation overhead for hot code paths

Python and JIT

- Standard Python limitation: Most Python implementations don't have built-in JIT compilation
- Performance impact: This means Python generally runs slower than compiled languages since it maintains the interpretation layer

### GIL (Global Interpreted Lock)

The GIL exists because Python's interpreter architecture requires sequential processing of bytecode, making true multithreading impossible at the interpreter level. This is a fundamental difference from compiled languages where threads can execute machine code directly and in parallel.

Global Interpreter Lock (GIL) Solution

- Mutex for interpretation: Only one thread can execute Python code at a time
- Lock acquisition: A thread must acquire the GIL before interpreting any bytecode
- Serialization: Threads are essentially serialized during code execution
- Performance impact: Introduces stalling and slowness in multithreaded applications

## Mac Setup

```bash
brew install python3

python -m venv .venv
source .venv/bin/activate

pip3 install tornado

mkdir server && cd server

touch index.py index.html
```


```python

```

```html
<! DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, ini">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>List of Animals</title>
</head>
<body>
    <h1>This is a list of Animals</h1>
    <select>
        <option>Snake</option>
        <option>Horse</option>
        <option>Mouse</option>
        <option>Bird</option>
    </select>
</body>
</html>
```

```python

import tornado.web
import tornado.ioloop

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World")
        
class listRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
        
class queryRequestHandler(tornado.web.RequestHandler):
    def get(self):
        num = self.get_argument("num")
        if (num.isdigit()):
            r = "odd" if int(num) % 2 else "even"
            self.write(f"The integer {num} ir {r}")
        else:
            self.write(f"{num} is not a valid integer")

class resourceParamRequestHandler(tornado.web.RequestHandler):
    def get(self, studentName, courseId):
        self.write(f"Hello {studentName} the course you are viewing is {courseId})")
        
        


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/animals", listRequestHandler),
        (r"/iseven", queryRequestHandler),
        (r"/students/([a-z, A-Z]+)/([0-9]+)", resourceParamRequestHandler), 
        
    ])
    port = 8882
    app.listen(port)
    print(f"Listening on {port} ...")
    
    tornado.ioloop.IOLoop.current().start()
    
```