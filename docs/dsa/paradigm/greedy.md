# Greedy Algorithms & Strategies

* an algorithm that make the locally optimal choice at each step with the  hope of eventually reaching the globally optimal solution.

* a problem to be solved using greedy must exhibit these two property

    * It has optimal sub structures
    * It has the greedy property (difficult to prove in time -critical environment)

- Proving Greedy Stays Ahead : [Link](https://www.cs.cornell.edu/courses/cs482/2007su/ahead.pdf)

* **Coin Change**

    * Problem Statement:

    Given a target amount $( V )$ cents and a list of $( n )$ coin denominations, represented as `coinValue[i]` (in cents) for coin types $i \in [0..n-1]$, determine the minimum number of coins required to represent the amount (V). Assume an unlimited supply of coins of each type.

    Example: For \( n = 4 \) and coinValue = {25, 10, 5, 1} cents, to represent \( V = 42 \) cents, apply the greedy algorithm by selecting the largest coin denomination not exceeding the remaining amount: \( 42 - 25 = 17 \), \( 17 - 10 = 7 \), \( 7 - 5 = 2 \), \( 2 - 1 = 1 \), \( 1 - 1 = 0 \). This requires a total of 5 coins and is optimal.

    - The Problem has two properties

        - Optimal sub-structures

      These are

            - To represent 17 cents we use 10+5+1+1
            - To represent 7 cents we use 5+1+1

        - Greedy property- Given every amount V, we can greedily subtract the  largest coin denomination which is not greater than this amount V. It  can be proven that using any other strategies will not lead to an  optimal solution, at least for this set of coin denominations.

    - However **this greedy doesn’t always work** for all sets of coin denominations e.g.  cents. To make 6 cents with this set will fail optimal solution.

- **UVa - 11292 Dragon of Loowater (Sort the input first)**
    - This is a bipartite matching problem but still can be solved.
    - we match(pair) certain knights to dragon heads in maximal fashion. However, this problem can be solved greedily
    - Each dragon head must be chopped by a knight with the shortest height  that is at least as tall as the diameter’s of the dragon’s head.
    - However input is arbitrary order. Sorting Cost : $O(n \log n + m \log m)$, then to get answer $O(min(n, m))$

````c++
gold = d = k = 0; // array dragon and knight sorted in non decreasing order
while(d<n && k<m){
    while(dragon[d]> knight[k] && k<m) k++; //find required knight
    if(k==m) break;		//no knight can kill this dragon head,doomed
    gold+= knight[k]; // the king pays this amount of gold
    d++;k++;	//next dragon head and knight please
}

if(d==n) printf("%d\n",gold);		//all dragon heads arer chopped
else printf("Loowater is doomed!\n");
````

* Other classical Examples
    * Kruskal’s (and Prim’s) algorithm for the minimum spanning tree (MST)
    * Dijkstra’s (SSSP)
    * Huffman Code
    * Fractional Knapsacks
    * Job Scheduling Problem
* More on [Greedy](https://algo.minetest.in/CP3_Book/3_Problem_Solving_Paradigms/#greedy)

### Water Sprinkler

You’re given: A line segment to cover: `[0 ... L]`, Sprinklers placed at positions i, Each sprinkler covers an interval: `[i - range[i], i + range[i]]`

Use the minimum number of sprinklers to fully cover `[0 ... L]`. If impossible, return -1

```python

def minSprinklers(arr, n):
    intervals = []
    for i, r in enumerate(arr):
        if r != -1:
            intervals.append((i - r, i + r))

    
    intervals.sort()
    covered = 0  # farthest position covered so far
    i = 0        # interval index
    used = 0     # sprinklers used
    
    while covered < n:
        farthest = covered
        while i < len(intervals) and intervals[i][0] <= covered:
            farthest = max(farthest, intervals[i][1] + 1)
            i += 1
            
        if farthest == covered:
            return -1
        covered = farthest
        used += 1
        
    return used

```

## Simple Problems
### Assign Cookies

Assume you are an awesome parent and want to give your children some cookies. But, you should give each child at most one cookie.

Each child `i` has a greed factor `g[i]`, which is the minimum size of a cookie that the child will be content with; and each cookie `j` has a size `s[j]`. If `s[j] >= g[i]`, we can assign the cookie `j` to the child `i`, and the child `i` will be content. Your goal is to maximize the number of your content children and output the maximum number.

```
Input: g = [1,2,3], s = [1,1]
Output: 1
```

So idea is simple that we try to greedily assign cookies to children, sort both cookies and children and try to assign cookies to children as we wish to maximize number of children which are content.

```python

def findContentChildren(g, s):
    g.sort()
    s.sort()

    content_children = 0
    cookie_index = 0

    while cookie_index < len(s) and content_children < len(g):
        if s[cookie_index] >= g[content_children]:
            content_children += 1
        cookie_index += 1
    
    return content_children

```

### Fractional Knapsack Problem

Often people confuse Fractional Knapsack to be a DP problem, but since value/wt obtained is fractional, we can optimize the collection by collecting more valuable objects first.

**Problem Statement:** The weight of N items and their corresponding values are given. We have to put these items in a knapsack of weight W such that the total value obtained is maximized.

```python

def fractionalKnapsack(W, arr, n):

    # Sort items based on the value/weight ratio in descending order
    arr.sort(key=lambda x: (x.value / x.weight), reverse=True)

    curWeight = 0  # Current weight of knapsack
    finalvalue = 0.0  # Final value we can achieve

    # Iterate through the sorted items
    for i in range(n):

        # take full objects
        if curWeight + arr[i].weight <= W:
            curWeight += arr[i].weight
            finalvalue += arr[i].value  # Add the full value of the item
        else:
            # fill remaining fractional value
            remain = W - curWeight
            finalvalue += (arr[i].value / arr[i].weight) * remain
            break  # Break as we have filled the knapsack

    return finalvalue

```

### Greedy Coin-Change

**Problem Statement:** Given a value V, if we want to make a change for V Rs, and we have an infinite supply of each of the denominations in Indian currency, i.e., we have an infinite supply of { 1, 2, 5, 10, 20, 50, 100, 500, 1000} valued coins/notes, what is the minimum number of coins and/or notes needed to make the change.

```
Input : 70
Output : 2 (#50, #20)
```

To minimize the number of coins, we need the most greater note just less than `70` using bisect_left

```python

from bisect import bisect_right
def main(coins, v):
    cnt, amt = 0, v
    while amt > 0:
        i = bisect_right(coins, amt)
        if i:
            amt -= coins[i - 1]
            cnt += 1
        else:
            # i == 0 ~> all remaining 1s can be used
            cnt += amt
            amt = 0

    return cnt

```

### Lemonade Change

At a lemonade stand, each lemonade costs `$5`. Customers are standing in a queue to buy from you and order one at a time (in the order specified by bills). Each customer will only buy one lemonade and pay with either a `$5`, `$10`, or `$20` bill. You must provide the correct change to each customer so that the net transaction is that the customer pays `$5`.

Note that you do not have any change in hand at first.

Given an integer array `bills` where `bills[i]` is the bill the `ith` customer pays, return `true` _if you can provide every customer with the correct change, or_ `false` _otherwise_.

```python

from collections import defaultdict

class Shop:
    def __init__(self):
        self.balance = 0
        self.notes = defaultdict(lambda: 0)

    # each txn is fixed to earn $5
    def transact(self, amt):
        match amt:
            case 5:
                pass
            case 10:
                if self.notes[5] < 1:
                    return False
                self.notes[5] -= 1
            case 20:
                if self.notes[10] >= 1 and self.notes[5] >= 1:
                    self.notes[10] -= 1
                    self.notes[5] -= 1
                elif self.notes[5] >= 3:
                    self.notes[5] -= 3
                else:
                    return False
            case _:
                return False
            
        self.notes[amt] += 1
        self.balance += 5
        return True

class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        shop = Shop()
        return all(shop.transact(bill) for bill in bills)

```

### Valid Parenthesis Checker

Given a string `s` containing only three types of characters: `'('`, `')'` and `'*'`, return `true` _if_ `s` _is **valid**_.

The following rules define a **valid** string:

- Any left parenthesis `'('` must have a corresponding right parenthesis `')'`.
- Any right parenthesis `')'` must have a corresponding left parenthesis `'('`.
- Left parenthesis `'('` must go before the corresponding right parenthesis `')'`.
- `'*'` could be treated as a single right parenthesis `')'` or a single left parenthesis `'('` or an empty string `""`.

A DP Solution for matching the parenthesis

```python

def checkValidString(self, s: str) -> bool:
    n = len(s)

    @cache
    def solve(i, open):
        if i == n:
            return open == 0
        
        valid = False
        if s[i] == "*":
            # '*' is ')'
            valid |= solve(i+1, open+1)
            # pruning
            if open > 0:
                # better to cast it as '*' is '('
                valid |= solve(i+1, open-1)
            # '*' is none 
            valid |= solve(i+1, open)
        else:
            if s[i] == '(':
                valid |= solve(i+1, open+1)
            elif open > 0:
                valid |= solve(i+1, open-1)

        return valid

    return solve(0, 0)

```

Another Optimal Greedy Solution is to match `*` greedily.

```python

def checkValidString(self, s: str) -> bool:

    # min, max. possible open brackets
    min_open, max_open = 0, 0
    
    for char in s:

        if char == '(':
            min_open += 1
            max_open += 1

        elif char == ')':
            min_open -= 1
            max_open -= 1

        # If current character is '*', it can be '(', ')' or ''
        else:
             # If '*' acts as ')'
            min_open -= 1    
            # If '*' acts as '('
            max_open += 1      

        # If max_open goes below 0, we have too many unmatched ')'
        if max_open < 0:
            return False
        # min_open should not be negative
        if min_open < 0:
            min_open = 0

    # At the end, all opens must be matched for valid string
    return min_open == 0

```

## Medium/Hard Problems

### Jump Game

You are given an integer array `nums`. You are initially positioned at the array's **first index**, and each element in the array represents your maximum jump length at that position.

Return `true` _if you can reach the last index, or_ `false` _otherwise_.

```python

def canJump(nums):
    n = len(nums)

    @cache
    def solve(i):
        # reached or crossed the end
        if i >= n - 1:
            return True

        # dead end
        if nums[i] == 0:
            return False

        for jump in range(1, nums[i] + 1):
            if solve(i + jump):
                return True

        return False

    return solve(0)

```

Converting to tabulation

```python

def canJump(nums):
    n = len(nums)

    dp = [False] * n
    dp[n - 1] = True  # base case

    for i in range(n - 2, -1, -1):
        for j in range(1, nums[i] + 1):
            if i + j < n and dp[i + j]:
                dp[i] = True
                break

    return dp[0]

```

Here we can see are pruning jumps, still this will fail and give TLE.

Instead of asking: “Can I reach the end from here?”

Ask: “What is the farthest index I can reach so far?”

If at any index i:

```
i > farthest
you are stuck, -> return false
```


```python

def canJump(self, nums: List[int]) -> bool:
    farthest = 0

    for i in range(len(nums)):
        if i > farthest:
            return False

        farthest = max(farthest, i + nums[i])

    return True

```

### Jump Game 2

You are given a **0-indexed** array of integers `nums` of length `n`. You are initially positioned at index 0.

Each element `nums[i]` represents the maximum length of a forward jump from index `i`. In other words, if you are at index `i`, you can jump to any index `(i + j)` where:

- `0 <= j <= nums[i]` and
- `i + j < n`

Return _the minimum number of jumps to reach index_ `n - 1`. The test cases are generated such that you can reach index `n - 1`.

A DP Solution that I came up with is following :

```python

def jump(self, nums: List[int]) -> int:

    n = len(nums)

    @cache
    def solve(i):
        if i == n - 1:
            return 0

        # invalid state
        if i >= n:
            return float('inf')

        cost = float('inf')
        for j in range(1, nums[i] + 1):
            cost = min(cost, 1 + solve(i+j))
        
        return cost

    return solve(0)

```

But we can solve it in $O(n)$ using Greedy !

Instead of asking: “From index i, what is the best next jump?”

Ask: “With k jumps, what is the farthest index I can reach?”

This reframes the problem into layers, similar to BFS on an array.

```python

def jump(nums):
    jumps = 0
    curr_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        if i == curr_end:
            jumps += 1
            curr_end = farthest

    return jumps

```


Think of it as BFS:

- All indices reachable within `curr_end` are reachable in jumps moves
- farthest tracks the next layer
- Jumping earlier does not help, because we want the max reach per jump

### Min, Number of Platform Required for a Railway

**Problem Statement:** We are given two arrays that represent the arrival and departure times of trains that stop at the platform. We need to find the minimum number of platforms needed at the railway station so that no train has to wait.

Just create diff array pattern from intervals topic, for each arrival time `+1` and `-1` for departure and take max of that.

### Job Sequencing Problem

**Problem Statement:** You are given a set of N jobs where each job comes with a deadline and profit. The profit can only be earned upon completing the job within its deadline. Find the number of jobs done and the maximum profit that can be obtained. Each job takes a single unit of time and only one job can be performed at a time.

```
N = 4, Jobs = {(1, 4, 20), (2, 1, 10), (3, 1, 40), (4, 1, 30)}  
Output:
 2 60 
```

Greedy Strategy:

- Sort jobs by profit (descending)
- Try to schedule each job in the latest free time slot ≤ its deadline
- If no slot is free → skip the job

```python

def JobScheduling(self, jobs, n):
    # jobs: list of (id, deadline, profit)
    jobs.sort(key=lambda x: x[2], reverse=True)

    max_deadline = max(job[1] for job in jobs)
    slots = [-1] * (max_deadline + 1)

    count = 0
    profit = 0

    for job in jobs:
        deadline = job[1]
        for t in range(deadline, 0, -1):
            if slots[t] == -1:
                slots[t] = job[0]
                count += 1
                profit += job[2]
                break

    return count, profit

```
### Candy

There are `n` children standing in a line. Each child is assigned a rating value given in the integer array `ratings`.

You are giving candies to these children subjected to the following requirements:

- Each child must have at least one candy.
- Children with a higher rating get more candies than their neighbors.

Return _the minimum number of candies you need to have to distribute the candies to the children_.

Its a difficult and unintuitive problem, this requires a technique called 2 phase scan. Reason why one-pass greedy fails, 

```
ratings = [1, 3, 2] ~ greedy works
candies = [1, 2, 1] (3 > 2), works

for take example : [1, 2, 3, 2, 1] one pass breaks
```


Two Pass Approach

- If rating increases, give one more than left neighbor.
- If rating decreases, ensure current has more than right neighbor.


```python

def candy(ratings):
    n = len(ratings)
    candies = [1] * n  # each child gets at least one

    # Left to right
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Right to left
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)

```

#### Scheduling/Interval Problems

Already Covered in Previous Interval Section

- Program for Shortest Job First (or SJF) CPU Scheduling
- Program for Least Recently Used (LRU) Page Replacement Algorithm
- Insert Interval
- Merge Intervals
- Non-overlapping Intervals
