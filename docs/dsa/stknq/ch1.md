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

### Problems

* Valid Parentheses (20)
* Min Stack (155)
* String Reversal
* Basic Calculator
* Longest Valid Parentheses
* Decode String
* Remove K Digits