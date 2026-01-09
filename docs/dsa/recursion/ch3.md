# String Recursion

## Palindrome Partitioning

[Leetcode Link](https://leetcode.com/problems/palindrome-partitioning/)

* Given a string `s`, partition `s` such that every substring of the partition is a substring, Enumerate all such solutions

Split Strategy

* divide into `n` chunks
* set of solution where first partition `a` : `a | a | b`
* set of solution where first partition `aa` : `a a | b`
* set of solution where first partition `aab` : $\phi$ // prefix is not a palindrome

Subproblem

* $c_i$ : All the palindrome partition of elements of array after $i$ and then append palindrome before $c_i$

* 1 D Subproblem, its a suffix array problem

````c++
bool isPalindrome(string& s){
    int start= 0, end = s.size()-1;
    while(start <= end){
        if(s[start] != s[end])
            return false;
        start++,end--;
    }
    return true;
}
void f(string& s, int start, vector<string>& contri, vector<vector<string>>& res){
    //Base case
    if(start == s.size()){
        res.push_back(contri);
        return;
    }

    //Try all possibilities of putting up the partition
    string part;
    for(int j = start; j < s.size(); j++){
        // s[start .. j] is the first partition
        part = s.substr(start, j-start+1);

        if(!isPalindrome(part))
            continue;
        contri.push_back(part);
        f(s,j+1, contri, res);
        contri.pop_back(); // clear parent call! important
    }
}
vector<vector<string>> partition(string s) {
    vector<vector<string>> res;
    vector<string> contri;
    f(s,0,contri,res);
    return res;
}

````

Python Solution :

```python

def partition(s):

    n = len(s)
    res = []

    def dfs(i, curr):

        if i == n:
            res.append(curr[:])
            return
        
        for j in range(i, n):
            part = s[i:j + 1]
            if part == part[::-1]: # check palindrome
                dfs(j+1, curr + [part])


    dfs(0, [])
    return res

```

## Word Search

[Leetcode Link](https://leetcode.com/problems/word-search/description/)

* Problem based on 2D Matrix DFS, standard pattern

````c++
vector<vector<int>> dirs = {{1,0}, {-1,0} , {0,1} , {0,-1}};
bool f(vector<vector<char>>& board, int start_i, int start_j,vector<vector<bool>>& visited, string& word, int pos){
    // 4 possibilities
    if(pos == word.size())
        return true;
    int m = board.size() , n =board[0].size();
    bool res = false;
    for(int i = 0; i < dirs.size(); i++){
        int x = start_i + dirs[i][0];
        int y = start_j + dirs[i][1];

        //check if its valid
        if(x<0 || x>=m || y <0  || y>=n) continue;
        if(visited[x][y] || board[x][y] != word[pos]) continue;
        visited[x][y] = true;
        res = res||f(board, x, y, visited, word, pos+1);
        visited[x][y] = false;

    }
    return res;
}
bool exist(vector<vector<char>>& board, string word) {
    int m = board.size(), n = board[0].size();
    bool res = false;
    vector<vector<bool>> visited(m,vector<bool>(n,false));
    for(int i = 0; i<m; i++)
        for(int j = 0; j < n ; j++)
            if(board[i][j] == word[0]){
                visited[i][j] = true;
                res = res || f(board,i,j,visited, word, 1);
                visited[i][j] = false;
            }

    return res;
}
````

Python Solution :

```python

def exist(self, board: List[List[str]], word: str) -> bool:

    n, m = len(board), len(board[0])
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    vis = set()

    def dfs(i, j, k):
        # matched full word
        if k == len(word):
            return True

        # bounds + char check
        if i < 0 or i >= n or j < 0 or j >= m:
            return False
        if (i, j) in vis:
            return False
        if board[i][j] != word[k]:
            return False

        vis.add((i, j))

        for dx, dy in dirs:
            if dfs(i + dx, j + dy, k + 1):
                return True

        vis.remove((i, j))
        return False

    # MUST try every starting cell
    for i in range(n):
        for j in range(m):
            if dfs(i, j, 0):
                return True

    return False
```


## Word Break

Problem Link 139 - [Link](https://leetcode.com/problems/word-break/)

Although this a DP problem but shows how recursion can be used to this problem.

Python Solution :

```python
def wordBreak(s, wordDict):

    dt = set(wordDict)
    @cache
    def dfs(i):
        if i == len(s): return True

        word = ""
        ans = False
        for j in range(i, len(s)):
            word += s[j]
            if word in dt:
                ans |= dfs(j+1)
        return ans

    return dfs(0)
```


## Rat in a Maze

**Problem Statement:** Given a grid of dimensions n x n. A rat is placed at coordinates (0, 0) and wants to reach at coordinates (n-1, n-1). Find all possible paths that rat can take to travel from (0, 0) to (n-1, n-1). The directions in which rat can move are 'U' (up) , 'D' (down) , 'L' (left) , 'R' (right).  
The value 0 in grid denotes that the cell is blocked and rat cannot use that cell for traveling, whereas value 1 represents that rat can travel through the cell. If the cell (0, 0) has 0 value, then mouse cannot move to any other cell.

NOTE: instead of using visited array, reused the grid. Generally its bad practice mutate the inputs.

```python

def main(n, grid):
    res = []
    dirs = [(0, 1, "R"), (1, 0, "D"), (-1, 0, "L"), (0, -1, "U")]

    def dfs(i, j, path):
        if i == n - 1 and j == n - 1:
            res.append(path)
            return

        if i < 0 or j < 0 or i >= n or j >= n:
            return

        if grid[i][j] == 0:
            return

        # block back travel
        grid[i][j] = 0

        for dx, dy, name in dirs:
            dfs(i + dx, j + dy, path + name)

        # reset grid
        grid[i][j] = 1

    dfs(0, 0, "")
    return res


```

## Generate valid Parenthesis
