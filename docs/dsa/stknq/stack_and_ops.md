# Stack Operations & Application

*A stack is a linear data structure that follows the Last-In First-Out (LIFO) principle.*

**Basic Stack Operations**

* Push - *Insert and element on top of the stack*
* Pop - *Remove the top element from the stack*
* Peek/Top - *View the top element without removing it*
* isEmpty - *Check whether stack is empty*

## Application of Stack

* Function Call Management
    * Every function call is pushed to the *call* stack and popped when it returns
* Expression Evaluation and Conversion
    * Infix to Postfix/Prefix Conversion
    * Postfix Expression Evaluation
* Undo Mechanisms in Editors and Apps
    * Each operation is pushed onto a stack, `undo` just pops the last action
* Syntax Parsing
    * Used in Compilers to parse Expressions, Match Brackets, and More
* Backtracking
    * Pathfinding, Maze Solving, Puzzle Solving (DFS uses stack)
* Memory Management
    * Stacks are use for **stack frame** in program execution

## STL & Python Usage

Python (`builtin` or `collections.deque`)

| **Operation** | **Using list**  | **Using deque**                                        |
| ------------- | --------------- | ------------------------------------------------------ |
| Create stack  | stack = []      | `from collections import deque` then `stack = deque()` |
| Push          | stack.append(x) | stack.append(x)                                        |
| Pop           | stack.pop()     | stack.pop()                                            |
| Peek          | stack[-1]       | stack[-1]                                              |
| Check empty   | not stack       | not stack                                              |

NOTE: `deque` is faster and preferred for large-scale stack operations

C++ (`std::stack`)

| **Operation** | **Function** | **Notes**                    |
| ------------- | ------------ | ---------------------------- |
| Create stack  | stack<T> s   | T is the data type           |
| Push          | s.push(x)    | Adds x to top                |
| Pop           | s.pop()      | Removes top element          |
| Peek          | s.top()      | Returns top without removing |
| Check empty   | s.empty()    | Returns true if empty        |
| Size          | s.size()     | Returns number of elements   |

- To use a different container: `stack<int, vector<int>> s; or stack<int, deque<int>> s;`

#### Problems

* Basic Calculator
* Longest Valid Parentheses
* Decode String

### Check For Balanced Parenthesis

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

```python

def isValid(s):
    stk = []

    for c in s:
        if c in ('(', '[', '{'):
            stk.append(c)
        else:
            match c:
                case ')':
                    if stk and stk[-1] != '(':
                        return False
                case ']':
                    if stk and stk[-1] != '[':
                        return False
                case '}':
                    if stk and stk[-1] != '{':
                        return False

            if stk:
                stk.pop()
            else:
                return False

    return len(stk) == 0

```

Now complete the longest Valid Parenthesis Problem, just keep track of the longest brackets where stack becomes empty.

### Min-Stack

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

```python

class MinStack:

    def __init__(self):
        self.min_stk = []
        self.normal_stk = []
        

    def push(self, val: int) -> None:
        self.normal_stk.append(val)
        if self.min_stk:
            self.min_stk.append(min(val, self.min_stk[-1]))
        else:
            self.min_stk.append(val)
        

    def pop(self) -> None:
        self.min_stk.pop()
        self.normal_stk.pop()
        

    def top(self) -> int:
        return self.normal_stk[-1]
        

    def getMin(self) -> int:
        return self.min_stk[-1]

```

### Sort a Stack

[Video Explanation](https://www.youtube.com/watch?v=4zx5bM2OcvA&list=PL3edoBgC7ScV9WPytQ2dtso21YrTuUSBd&index=14)