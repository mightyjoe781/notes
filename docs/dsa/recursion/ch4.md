# Backtracking

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

````c++
bool existsInCol(vector<string>& mat, int col, int n){
    for(int i = 0; i <n ; i++){
        if(mat[i][col] == 'Q')
            return true;
    }
    return false;
}
bool existsInDiag(vector<string>& mat, int curr_row, int curr_col, int type, int n){
    //type == 1 principal diagonal (positive slope)
    //type == 2 secondary diagonal (negative slope)

    //Go up
    int factor = (type == 1)? 1 : -1;

    int i = curr_row, j = curr_col;
    while( i>=0 && j<n && j >= 0){
        if(mat[i][j] == 'Q')
            return true;
        i--;
        j+=factor;
    }
    //Go down
    return false;
}
void f(vector<string>& mat, int  rem, vector<string>& contri, vector<vector<string>>& res,int n){

    // Base step
    if(rem == 0)
    { res.push_back(contri); return;}
    //recursive step
    //c1 to c_N
    //try n-rem row
    int i;
    for(i = 0; i < n; i++){
        //check if this is a valid position
        // check if possible in curr col
        if(!existsInCol(mat,i,n) &&
           !existsInDiag(mat,n-rem,i,1,n)&&
           !existsInDiag(mat,n-rem,i,2,n)){
            mat[n-rem][i] = 'Q';
            contri[n-rem][i] = 'Q';
            f(mat,rem-1,contri,res,n);
            mat[n-rem][i] = '.';
            contri[n-rem][i] ='.';

        }
    }

}
vector<vector<string>> solveNQueens(int n) {
    vector<vector<string>> res;
    vector<string> mat(n, string(n,'.'));
    vector<string> contri(n,string(n,'.'));
    f(mat,n,contri,res,n);
    return res;

}
````

Python Solution for above problem:

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