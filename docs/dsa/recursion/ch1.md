# Recursion

* A recursion program is one that calls itself with a *termination* condition
* Ex - Trees are defined recursively
* **Definition-** A *recursive algorithm* is one that solves a program by solving one or more smaller instances of the same problem. ~ (Divide & Conquer Rule)
* Its always possible to convert recursive program into a non-recursive-one, sometimes it might not be obvious

***Factorial function (recursive implementation)***

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

A care should be taken while writing programs related to recursion

* they must explicitly solve a basis case
* each recursive call must involve smaller values of the arguments

***A questionable recursive program***

```python
def puzzle(n):
    if n == 1:
        return 1
    if n % 2 == 0:
        return puzzle(n // 2)
    else:
        return puzzle(3 * (n + 1))  # unbounded n
```

***Euclid’s algorithm***

```python
def gcd(m, n):
    if n == 0:
        return m
    return gcd(n, m % n)
```

***Recursive program to evaluate prefix expressions***

```python
def eval_prefix(expr):
    tokens = expr.split()
    i = [0]  # mutable index via list (simulates global state)

    def eval():
        tok = tokens[i[0]]
        i[0] += 1
        if tok == '+':
            return eval() + eval()
        if tok == '*':
            return eval() * eval()
        return int(tok)

    return eval()

eval_prefix("+ * 2 3 4")  # => 10  i.e. (2*3)+4
```

***Examples of recursive functions for linked lists***

- `count` - It counts number of nodes on the list.
- `traverse` - calls `visit` for each node on the list from beginning to end.
- `traverseR` - It calls `visit` for every node but in reverse order.
- `remove` - Removes all nodes from a given item value from the list.

```python
class Node:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def count(node):
    if node is None:
        return 0
    return 1 + count(node.next)

def traverse(node, visit):
    if node is None:
        return
    visit(node)
    traverse(node.next, visit)

def traverse_r(node, visit):
    if node is None:
        return
    traverse_r(node.next, visit)
    visit(node)

def remove(node, val):
    if node is None:
        return None
    if node.val == val:
        return remove(node.next, val)
    node.next = remove(node.next, val)
    return node
```

#### Call by value

Memory Layout

* Stack (local function data : arguments & inside data)
* Heap (dynamic like malloc, new)
* Global (global variable, code)

Flow of execution

* Main
* Stack is allocated for every function

#### Call by Reference

* Change the value at calls
    * Explicit return types (use struct to create a new data type)
    * Implicit Return type
* Space Optimized: don’t need extra memory declaration in memory stack

### Problem Types

Note: This is a broad classification. Some types will be discussed in later sections, while others will be covered in their respective sections due to prerequisite topics.

| **Type**                      | **Keywords / Pattern**                          | **Examples**                                        |
| ----------------------------- | ----------------------------------------------- | --------------------------------------------------- |
| **Basic Recursion**           | Simple function calls, base + recursive step    | Factorial, Fibonacci, Power(x, n)                   |
| **Backtracking**              | Try all possibilities, undo step, constraints   | N-Queens, Sudoku Solver, Permutations               |
| **Combinatorics**             | Generate combinations, subsets, partitions      | Subsets, Combination Sum, Phone Number Letter Comb  |
| **Permutations**              | All orderings, visited flags                    | All permutations of string/array, Anagrams          |
| **Divide & Conquer**          | Split input, solve subproblems, merge result    | Merge Sort, Quick Sort, Binary Search               |
| **Tree Recursion**            | Binary tree traversal, multiple recursive calls | DFS, Tree Diameter, Max Depth of Tree               |
| **Graph Traversal**           | Recursively visit nodes/edges, visited map      | DFS on Graph, Islands Count, Connected Components   |
| **Recursion + Memoization**   | Reuse overlapping subproblems                   | Fibonacci (Top-down), Climbing Stairs               |
| **String Recursion**          | Substring generation, character decisions       | Palindrome Partitioning, Generate Valid Parentheses |
| **Recursion with Return**     | Return values from children, accumulate results | Path Sum in Tree, Sum of Subsets                    |
| **Recursion with Parameters** | Track path, state                               | Subsequence with sum K, Combinations with k size    |
| **Recursion Tree Analysis**   | T(n) = 2T(n/2) + n, or similar                  | Understanding time complexity                       |

## Time Complexity Analysis

* A very straight forward method to solve recursion complexity is using Back Substitution method (write-out recurrence)

$$
\begin{align}
f(n) &= f(n-1) + f(n-2)\\
f(n) &= f(n-2) + f(n-3) + f(n-3) + f(n-4)\\
f(n) &= f(n-2) + 2 f(n-3) + f(n-4) ... f(n)\\
f(n) &= f(1) + O(2^n)
\end{align}
$$

* Tree Method
    * Imagine the tree
    * Sum up the work at each level
* Subsets Problem : $O(2^n)$
* Combination Problem: $O(2^{max(n, k)}) = O(2^n)$

- A recursion Visualizer : https://recursion.vercel.app/

### Another Example : Fast Collapsing Recursion State (Fast Exponentiation Example)

- Implement a `pow(x, n)` function which calculates the following : $x^n$

A naive recursive solution would be :

```python

def pow(x, n):
    if n == 0:
        return 1
    return x * pow(x, n-1)

pow(2, 5) # returns 32
```

Problem with above solution is let's say we have a question like $2^{50000}$ then above solution fails to resolve in most cases within time-limits. (NOTE: In python you may encounter recursion stack limits)

Problem is the rate at which recursion being called, making the solution linear in time at worst case. But here we can prune the solution to obtain a $O(\log n)$ time complexity.

Ex - fast Exponentiation

```python

def fast_pow(x, n):
    if n == 0:
        return 1
        
    # break it into : x^(n/2) and x^(n/2)
    half = fast_pow(x, n//2)
    
    if n % 2:
        return half * half * x
        
    return half * half

fast_pow(2, 5000) # works ~
```

NOTE: we can't represent larger number in python variables, so often problems require calculating this against a mod value.