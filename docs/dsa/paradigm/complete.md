# Complete Search

- aka brute force or recursive backtracking
- in this method we traverse entire search space to obtain solution and during search we are allowed to prune
- Develop this solution only if
- - clearly no other algorithm available
  - better algorithms are overkill for input size
- Remember *‘KISS’* - Keep it Short and Simple
- If there exists a better solution you will get a TLE
- This method can be used as a verifier for small instances

## Iterative Complete Search

- Problem UVa 725 - Division (Two Nested Loops)
- Problem UVa 441 - Lotto (Many Nested Loops)
- Problem UVa 11565 - Simple Equations ( Loops + Pruning)
- Problem UVa 11742 - Social Constraints( Permutations)
- Problem UVa 12455 - Bars (Subsets)

## Recursive Complete Search

- UVa 750 8 Queens Chess Problem
- This code basically checks for all different possibilities of proper non conflicting solution and checks whether given pair is part of the  placement or not. It recursively does backtracking to save time.

````c++
#include <cstdlib>
#include <cstdio>
#include <cstrings>
using namespace std;

int row[8] , TC , a , b, lineCounter;

bool place(int r,int c){
    for (int prev=0; prev<c ; prev++)
        if(row[prev] == r || (abs(row[prev]-r) == abs(prev - c)))
            return false;
    return true;
}
void backtrack(int c){
    if(c==8 && row[b] == a){
        printf("%2d		%d", ++lineCounter , row[0]+1);
        for(int j=1;j<8; j++) printf(" %d",row[j] +1);
        printf("\n");     }
    for (int r =0; r< 8 ; r++)
        if(place(r,c)){
            row[c] = r; backtrack(c+1);
        }
}

int main(){
    scanf("%d",&TC);
    while(TC--){
        scanf("%d %d", &a,&b); a--;b--; //switching to zero basesd indexing
        memset(row,0,sizeof row); lineCounter = 0;
        printf("SOLN		COLUMN\n");
        printf(" # 		1 2 3 4 5 6 7 8\n\n");
        backtrack(0);	//generates all possible 8! candidates
        if (TC) 
          printf("\n");            
    } 
}
````

### Tips:

- Filtering v/s Generating
- Prune Infeasible Search Space Early
- Utilize Symmetries
- Pre-Computation
- Try solving problem backwards
- Optimize your Source Code
- Use Better Data Structures & Algorithms

### Problems

-  [Subsets - Generate all subsets of a set](https://leetcode.com/problems/subsets/) - recursive backtracking to explore include/exclude choices  
-  [Permutations - Generate all permutations of a list](https://leetcode.com/problems/permutations/) - recursive swapping to generate permutations  
-  [Permutations II - Permutations with duplicates](https://leetcode.com/problems/permutations-ii/) - recursive backtracking with sorting and pruning duplicates  
-  [Combination Sum - Find combinations summing to target](https://leetcode.com/problems/combination-sum/) - recursive backtracking allowing repeated elements  
-  [Combination Sum II - Combinations without duplicates](https://leetcode.com/problems/combination-sum-ii/) - recursive backtracking with sorting and skipping duplicates  
-  [Letter Combinations of a Phone Number - Phone digit to letter combos](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) - recursive backtracking building combinations digit by digit  
-  [Generate Parentheses - All valid parentheses combinations](https://leetcode.com/problems/generate-parentheses/) - recursive backtracking tracking counts of open/close parentheses  
-  [Word Search - Search word in 2D board](https://leetcode.com/problems/word-search/) - DFS with backtracking and visited tracking  
-  [N-Queens - Place N queens without conflicts](https://leetcode.com/problems/n-queens/) - recursive backtracking with conflict checks on columns and diagonals  
-  [N-Queens II - Count distinct N-Queens solutions](https://leetcode.com/problems/n-queens-ii/) - recursive backtracking counting solutions  
-  [Palindrome Partitioning - Partition string into palindromes](https://leetcode.com/problems/palindrome-partitioning/) - recursive backtracking with palindrome checks  
-  [Restore IP Addresses - Generate valid IP address combinations](https://leetcode.com/problems/restore-ip-addresses/) - recursive backtracking choosing valid segments  
-  [Combination Sum III - Combination sum with fixed number of elements](https://leetcode.com/problems/combination-sum-iii/) - recursive backtracking with pruning on sum and count  
-  [Subsets II - Subsets with duplicates](https://leetcode.com/problems/subsets-ii/) - recursive backtracking with sorting and duplicate skipping  
-  [All Paths From Source to Target - List all paths in DAG](https://leetcode.com/problems/all-paths-from-source-to-target/) - DFS with path tracking and backtracking  
-  [Find All Anagrams in a String - Find all anagram start indices](https://leetcode.com/problems/find-all-anagrams-in-a-string/) - sliding window with frequency counting  
-  [Permutations (Iterative) - Generate permutations without recursion](https://leetcode.com/problems/permutations/) (variant) - iterative backtracking using explicit stack or loops  
