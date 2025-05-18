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

## Sudoko Solver
