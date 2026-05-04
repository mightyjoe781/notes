# Backtracking

## The Backtracking Template

Backtracking = try a choice → recurse → undo the choice.

```python
def backtrack(state, choices):
    if is_solution(state):
        result.append(copy of state)
        return

    for choice in choices:
        if is_valid(state, choice):
            make_choice(state, choice)    # choose
            backtrack(state, next_choices)  # recurse
            undo_choice(state, choice)    # unchoose
```

Three questions to answer before coding:

1. **What is the state?** (current path, board, remaining target)
2. **What are the choices?** (indices to pick, cells to fill)
3. **What makes a choice invalid?** (constraints to prune)

---

## Combination Sum

[Leetcode 39](https://leetcode.com/problems/combination-sum/)

*Find all combinations of candidates that sum to target. Each number can be reused.*

- **State:** current combination, remaining target, start index (to avoid duplicates)
- **Choices:** candidates from `start` onward
- **Invalid:** candidate > remaining (prune)

```python
def combinationSum(candidates, target):
    res = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remaining:
                break          # prune: candidates sorted, rest are larger too
            path.append(c)
            backtrack(i, path, remaining - c)   # i not i+1, reuse allowed
            path.pop()

    candidates.sort()
    backtrack(0, [], target)
    return res
```

**Combination Sum II** (no reuse, `i+1` instead of `i`, skip duplicates at same level):

```python
def combinationSum2(candidates, target):
    res = []
    candidates.sort()

    def backtrack(start, path, remaining):
        if remaining == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue       # skip duplicate at same recursion level
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return res
```

---

## Word Search

[Leetcode 79](https://leetcode.com/problems/word-search/)

*Find if word exists in grid following adjacent cells (no reuse).*

- **State:** current position `(r, c)`, index into word
- **Choices:** 4 neighbors
- **Invalid:** out of bounds, already visited, wrong character

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    visited = set()

    def backtrack(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx] or (r, c) in visited:
            return False

        visited.add((r, c))
        found = (backtrack(r+1, c, idx+1) or backtrack(r-1, c, idx+1) or
                 backtrack(r, c+1, idx+1) or backtrack(r, c-1, idx+1))
        visited.remove((r, c))
        return found

    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

---

## N-Queens Problem

[Leetcode Link](https://leetcode.com/problems/n-queens/)

Enumeration Problem

Problem can be restated as putting 1 queen into each row such that they don’t conflict.

Split into chunks

* `n` queens can be put in `n` rows
* for each row we have `n` possible columns

$c_1$ : List of valid configuration s.t. first cell is `[0, 0]` and rest of solution is `Mat[1..n-1][0..n-1]`

$c_2$ : List of valid configuration st.t first cell is `[0, 1]`

$c_3$ : List of valid configuration st.t first cell is `[0, 2]`

Subproblem instance

$c_1$ : take `(0, 0)` as occupied and then find out all valid configuration for `n-1` queens and append `(0, 0)` to it

Representation of problem : `f(n*n Matrix, n-1)`

```python
from copy import deepcopy

def solveNQueens(n):
    board = [['.']*(n) for _ in range(n)]
    res = []

    def validate(board, i, j):
        # check if the current column already doesn't have a queen
        for k in range(i):
            if board[k][j] == 'Q':
                return False
        
        # check upper-left diagonal
        r, c = i - 1, j - 1
        while r >= 0 and c >= 0:
            if board[r][c] == 'Q':
                return False
            r -= 1
            c -= 1

        # check upper-right diagonal
        r, c = i - 1, j + 1
        while r >= 0 and c < n:
            if board[r][c] == 'Q':
                return False
            r -= 1
            c += 1

        return True

    def solve(i):

        if i == n:
            # put correctly here
            res.append([ "".join(row) for row in deepcopy(board)])
            return 1

        for j in range(n):
            if validate(board, i, j):
                # place queen
                board[i][j] = 'Q'
                solve(i+1)
                # remove queen
                board[i][j] = '.'

    solve(0)
    return res

```

Above solution tries to fill the board layer by layer.
## Sudoko Solver

Problem Link - 37 : [Link](https://leetcode.com/problems/sudoku-solver/description/)

Write a program to solve a Sudoku puzzle by filling the empty cells.

```python

def solveSudoku(self, board: List[List[str]]) -> None:

    def is_valid(r, c, ch):
        # row
        for j in range(9):
            if board[r][j] == ch:
                return False

        # column
        for i in range(9):
            if board[i][c] == ch:
                return False

        # 3x3 box
        br = (r // 3) * 3
        bc = (c // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if board[i][j] == ch:
                    return False

        return True

    def dfs():
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for ch in "123456789":
                        if is_valid(i, j, ch):
                            board[i][j] = ch
                            if dfs():
                                return True
                            board[i][j] = '.'
                    return False
        return True  # no empty cell left

    dfs()
        
```


## M-Coloring Problem

**Problem Statement:** Given an undirected graph and a number `m`, determine if the graph can be colored with at most m colors such that no two adjacent vertices of the graph are colored with the same color.

Python Solution to problem : 

```python
def main(graph, V, M):
    color = [-1] * V

    def is_safe(u, col):
        for v in graph[u]:
            if color[v] == col:
                return False
        return True

    def dfs(u):
        if u == V:
            return True

        for col in range(M):
            if is_safe(u, col):
                color[u] = col
                if dfs(u + 1):
                    return True
                color[u] = -1  # backtrack

        return False

    possible = dfs(0)
    return possible, color
```


## Expression Add Operators

Problem Link - 282 - [Link](https://leetcode.com/problems/expression-add-operators/description/)

This problem is quite hard, 

At each step:

- Pick the next number chunk `num[pos:i]`
- Insert one of +, -, * before it (except at start)
- Track:
- `value: current evaluated result
- last: last operand (needed for `*`)
- expr: expression string so far

NOTE: `*` is tricky to calculate here, lets say input it `1 + 2 * 3`

It evaluation should be `1 + (2 * 3)` but we might calculate `1+2 = 3` from previous values, so to do correct evaluation we perform following

```
value - last + (last * curr)
```


```python

def addOperators(num, target):
    res = []
    n = len(num)

    def dfs(pos, expr, value, last):

        if pos == n:
            if value == target:
                res.append(expr)
            return

        for i in range(pos, n):
            # avoid numbers with leading zeros
            if i > pos and num[pos] == '0':
                break

            curr_str = num[pos:i+1]
            curr = int(curr_str)

            if pos == 0:
                # first number: no operator
                dfs(i + 1, curr_str, curr, curr)
            else:
                dfs(i + 1, expr + "+" + curr_str, value + curr, curr)
                dfs(i + 1, expr + "-" + curr_str, value - curr, -curr)

                # multiplication (IMPORTANT)
                dfs(i + 1, expr + "*" + curr_str,
                    value - last + last * curr,
                    last * curr)

    dfs(0, "", 0, 0)
    return res
```