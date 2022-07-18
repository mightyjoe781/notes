## Chapter 1: Getting Started

Python is a cross-platform programming language, which means it runs on all major OS.

#### Installing Python

- Windows : Visit [Link](https://python.org/downloads)
- MacOS: `brew install python3`
- Linux: `sudo apt install python3`

Checking python version : Execute `python` or `python3` and notice its version. Now you are in `>>>` prompt where you can start executing Python commands. To exit type `exit()` or `ctrl+D`. Alternatively you could execute `python3 --version` on terminal.

In case you have python version 2.x then try again installing latest verision.

#### Running hello_world.py

Create a empty file `hello_world.py` with contents.

```python
print("Hello Python world!")
```

Execute : `python3 hello_world.py`

## Chapter 2: Variables and Simple Data Types

#### Variables

Now modify `hello_world.py` with following content and run program again.

```python
message = "Hello Python world!"
print(message)
```

#### Naming and Using Variables

Rules and General Ideas to name variables.

- Variable names can only contain `letters`, `numbers`, and `underscores` and cannot start with numbers.
- Spaces are not allowed in variable names.
- Avoid using keywords and function names as variable names, they are reserved for particular programmatic purpose.
- Variable names should be short but descriptive.
- Be careful when using lowercase letter `l` and uppercase `O`, because they can be confused with number 1 or 0.
- Avoid Name errors when using variables.

