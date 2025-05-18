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

## Generate valid Parenthesis
