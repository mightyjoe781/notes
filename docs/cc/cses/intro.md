## Introductory Problems







### Chessboard and Queens

````c++
#include <bits/stdc++.h>
using namespace std;
 
bool existsInCol(vector<string>& mat, int col, int n) {
    for(int i = 0; i <n; i++) {
        if(mat[i][col] == 'Q')
            return true;
    }
    return false;
}
 
bool existsInDiag(vector<string>& mat, int curr_row, int curr_col, int type, int n) {
    int factor = (type == 1) ? 1 : -1;
    int i = curr_row, j = curr_col;
    while(i >= 0 && j < n && j >= 0) {
        if(mat[i][j] == 'Q')
            return true;
        i--;
        j+= factor;
    }
    return false;
}
 
void solve(vector<vector<string> >& res, int rem, vector<string> &board,
        vector<string>& contri, int n) {
    if(rem == 0) {
        res.push_back(contri);
    }
 
    for(int i = 0; i < n; i++) {
        if(!existsInCol(board,i,n) &&
           !existsInDiag(board,n-rem,i,1,n) &&
           !existsInDiag(board,n-rem,i,2,n) &&
            board[n-rem][i] != '*'){
            // --> solve
            board[n-rem][i] = 'Q';
            contri[n-rem][i] = 'Q';
            solve(res, rem-1, board, contri, n);
            board[n-rem][i] = '.';
            contri[n-rem][i] = '.';
        }
    }
}
 
int main() {
    int n = 8;
    vector<string> board(n);
    for(int i = 0; i < n; i++)
        cin >> board[i];
    vector<string> contri(n,string(n,'.'));
    vector<vector<string> > res;
    solve(res,n,board,contri,n);
    cout << res.size() << endl;
    return 0;
}
````

### Towers of Hanoi

- Minimal Numbers of moves required to solve Tower of Hanoi is $2^{n}-1$, where $n$ is the number of disks. This is precisely $n^{th}$ Mersenne number without primality requirements.
- Todo : Implement Iterative Solution.

````c++
#include <iostream>
#include <vector>
using namespace std;
// three pegs, from peg, to_rod peg and auxilary peg
vector<pair<int, int> > res;

void solve(int n, int from, int to, int aux) {
    if(n == 0)
        return;

    solve(n-1, from, aux, to);
    res.push_back(make_pair(from,to));
    solve(n-1, aux, to, from);
}

int main() {
    int n; cin >> n;
    solve(n,1,3,2);
    cout << res.size() << endl;
    for(auto t : res) {
        cout << t.first << " " << t.second << endl;
    }
    return 0;
}
````

### Trailing Zeros

- Calculating prime and then counting zeros will not work because above 20! there will be overflow.
- A simple strategy is to calculate prime factors and find out how many pairs of 2s and 5s can be made, because each one of then adds one zero. We can observe number of 2s in prime factors of a number is 
