# Complete Search

- aka brute force or recursive backtracking
- in this method we traverse entire search space to obtain solution and during search we are allowed to prune
- Develop this solution only if
    - clearly no other algorithm available
    - better algorithms are overkill for input size
- Remember *‘KISS’* - Keep it Short and Simple
- If there exists a better solution you will get a TLE
- This method can be used as a verifier for small instances

## Iterative Complete Search

- Problem UVa 725 - Division (Two Nested Loops) - find pairs (fghij / abcde = N) where all 10 digits are distinct
- Problem UVa 441 - Lotto (Many Nested Loops) - print all size-6 combinations from a chosen set of numbers
- Problem UVa 11565 - Simple Equations (Loops + Pruning) - find x, y, z satisfying A = x+y+z, B = x*y*z, C = x²+y²+z²
- Problem UVa 11742 - Social Constraints (Permutations) - count seating arrangements satisfying given min/max distance constraints
- Problem UVa 12455 - Bars (Subsets) - determine if any subset of bars sums to a target length

## Recursive Complete Search

- UVa 750 8 Queens Chess Problem
- This code basically checks for all different possibilities of proper non-conflicting solutions and checks whether a given pair is part of the placement or not. It recursively does backtracking to save time.

````python
row = [0] * 8
line_counter = 0

def place(r, c):
    for prev in range(c):
        if row[prev] == r or abs(row[prev] - r) == abs(prev - c):
            return False
    return True

def backtrack(c, a, b):
    global line_counter
    if c == 8 and row[b] == a:
        line_counter += 1
        cols = ' '.join(str(row[j] + 1) for j in range(8))
        print(f"{line_counter:2d}      {cols}")
        return
    for r in range(8):
        if place(r, c):
            row[c] = r
            backtrack(c + 1, a, b)

TC = int(input())
for t in range(TC):
    a, b = map(int, input().split())
    a -= 1; b -= 1  # switch to zero-based indexing
    row[:] = [0] * 8
    line_counter = 0
    print("SOLN      COLUMN")
    print(" #        1 2 3 4 5 6 7 8\n")
    backtrack(0, a, b)
    if t < TC - 1:
        print()
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
