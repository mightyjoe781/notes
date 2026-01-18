# Sliding Window

All sliding window problems share a basic concept: slide a sub-array (window) linearly from left to right over the original array of \(n\) elements.
## Common Problem Types

1. **find the smallest sub-array size**(smallest window length) such that sum of the sub-array is greater or equal to a certain constant S in O(n).
2. **find the smallest sub-array size**(smallest window length) such that elements inside the sub-array contains all integers in range `[1..K]`.
3. **find the maximum sum** of a certain sub-arry with static size K.
4. **Find the minimum element** in every sub-array of size \(K\) — a classic problem solved efficiently using a deque.

## Solutions

- **Variable Size Window with Sum Constraint**
    - Maintain a window that **grows** by adding elements at the back (right pointer) and **shrinks** by removing elements from the front (left pointer) as long as the running sum meets or exceeds the target \(S\).
    - Continuously update the smallest window length satisfying the condition like `running sum >= S`

- **Variable Size Window with Frequency Constraints**
    - Expand the window until it contains **all required elements** (e.g., all integers in `[1..K]`).
    - Use a frequency map to track counts of elements inside the window.
    - Shrink the window from the left while maintaining the constraint to find the minimal window.

- **Fixed Size Window for Maximum Sum**
    - Initialize the window with the first \(K\) elements and compute their sum.
    - Slide the window forward by removing the element at the front and adding the next element at the back.
    - Keep track of the maximum sum encountered.

- **Fixed Size Window for Minimum Element (Using Deque)**
    - Use a **deque** to maintain elements in ascending order within the current window.
    - For each new element:
    - Pop elements from the back of the deque while they are larger than the current element to maintain sorting.
    - Add the current element along with its index.
    - Remove elements from the front if they fall outside the current window.
    - The front of the deque always contains the minimum element for the current window.

- this is challenging especially if n is quite large. To get O(n) solution use deque to model the window. this time we maintain that the window is sorted in ascending order, that is front element of deque is minimum. However this changes ordering of elements in the array. To keep track of whether an element is in window or not, we need to remember index of each element too. See example below

````c++
// Type-1
// finding windows with sum == target
int subarraySum(vector<int>& nums, int k) {
    int res = 0, sum = 0;
  	// growing window
    for(int l = 0, r = 0; r < nums.size(); r++) {
        sum += nums[r];
      	// shrinking window
        while(sum > k && l < nums.size()) {
            sum-=nums[l];
            l++;
        }
      	// assess the condition to answer
        if(sum == k)
            res++;
    }
    return res;
}
````

````c++
// Type-4: Minimum in every subarray of size K using deque
void SlidingWindow(int A[], int n, int K) {
    // pair<int,int> represents (value, index)
    deque<pair<int, int>> window;  // maintain ascending order in window
    
    for (int i = 0; i < n; i++) {
        // Remove elements larger than current from the back
        while (!window.empty() && window.back().first >= A[i])
            window.pop_back();
        
        window.push_back({A[i], i});
        
        // Remove elements out of current window from front
        while (window.front().second <= i - K)
            window.pop_front();
        
        // Output minimum for windows starting from index K-1
        if (i + 1 >= K)
            printf("%d\\n", window.front().first);
    }
}
````

## Problems

* [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)
* [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)
* [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)


### Longest Substring Without Repeating Characters

Constraint here is that the window should be unique characters.

```python

def lengthOfLongestSubstring(s: str) -> int:

    mp = {}

    l = 0
    ans = 0
    for r in range(len(s)):

        # shrink the window,
        while s[r] in mp:
            del mp[s[l]]
            l += 1

        # expand window
        mp[s[r]] = r
        ans = max(ans, r - l + 1)
    
    return ans

```

### Longest Substring with At Most K repeating Characters

**Problem Statement:** Given a string s and an integer k.Find the length of the longest substring with at most k distinct characters

```
Input :s = "aababbcaacc" , k = 2
Output :6
Explanation :The longest substring with at most two distinct characters is "aababb".
The length of the string 6
```


```python

def lengthOfLongestSubstring(s: str, k) -> int:

    mp = {}

    l = 0
    ans = 0
    for r in range(len(s)):
        mp[s[r]] = mp.get(s[r], 0) + 1
        # shrink the window,
        while len(mp) > k:
            mp[s[l]] -= 1
            if mp[s[l]] == 0:
                del mp[s[l]]
            l += 1
        
        ans = max(ans, r - l + 1)
    
    return ans

```

### Subarray with K Different Integers

[Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/)

This problem ask for exactly K different Integers, We can get that using the following formulae.

```
Exactly K = Atmost(K) - Atmost(K-1)
```

Also notice its count of subarray's, not the longest.

```python

def subarraysWithKDistinct(nums: List[int], k: int) -> int:

    def atmost(target):

        mp = {}

        l = 0
        ans = 0
        for r in range(len(nums)):
            mp[nums[r]] = mp.get(nums[r], 0) + 1
            # shrink the window,
            while len(mp) > target:
                mp[nums[l]] -= 1
                if mp[nums[l]] == 0:
                    del mp[nums[l]]
                l += 1
            
            ans += (r - l + 1) # this is counting problem !!!
        
        return ans

    return atmost(k) - atmost(k-1)

```


### Maximum Consecutive Ones II

Given a binary array `nums` and an integer `k`, return _the maximum number of consecutive_ `1`_'s in the array if you can flip at most_ `k` `0`'s.

```
Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
```

This problem translates to : Longest Subarray with at most `K` zeroes.

### Fruits in the Basket

**Problem Statement:** There is only one row of fruit trees on the farm, oriented left to right. An integer array called fruits represents the trees, where `fruits[i]` denotes the kind of fruit produced by the `ith` tree.  
The goal is to gather as much fruit as possible, adhering to the owner's stringent rules :

- There are two baskets available, and each basket can only contain one kind of fruit. The quantity of fruit each basket can contain is unlimited.
- Start at any tree, but as you proceed to the right, select exactly one fruit from each tree, including the starting tree. One of the baskets must hold the harvested fruits.
- Once reaching a tree with fruit that cannot fit into any basket, stop.

Return the maximum number of fruits that can be picked.

```
Input :fruits = [1, 2, 1]
Output :3
Explanation : We will start from first tree.
The first tree produces the fruit of kind '1' and we will put that in the first basket.
The second tree produces the fruit of kind '2' and we will put that in the second basket.
The third tree produces the fruit of kind '1' and we have first basket that is already holding fruit of kind '1'. So we will put it in first basket.
Hence we were able to collect total of 3 fruits.
```

So we can collect fruits of at most 2 types, there is a brute force solution where we start collection from each index, and take max of that.

We can scan using sliding window for longest subarray containing 2 unique fruits at max.

```python

from collections import defaultdict
def totalFruit(fruits):
    
    basket = defaultdict(int)
    n = len(fruits)
    
    # Initialize pointers and result
    l = 0
    ans = 0

    # Traverse the fruits array using right pointer
    for r in range(n):
        # Add current fruit to basket
        basket[fruits[r]] += 1

        # If more than 2 types, shrink window from left
        while len(basket) > 2:
            basket[fruits[l]] -= 1
            if basket[fruits[l]] == 0:
                del basket[fruits[l]]
            l += 1

        ans = max(ans, r - l + 1)

    return ans
    
```

### Longest Repeating Character Replacement

You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times.

Return _the length of the longest substring containing the same letter you can get after performing the above operations_.

```
Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace the two 'A's with two 'B's or vice versa.
```

For any substring, Let `len` = length of the substring, `maxFreq` = freq. of the most common character in that substring. We are allowed to replace `k` characters in that substring, so to make all characters equal, `k >= len - maxFreq`

This is the window constraint : `k >= len - maxFreq`

```python

from collections import Counter

def characterReplacement(s: str, k: int) -> int:

    mp = Counter()

    n = len(s)
    l, ans = 0, 0
    maxCnt = 0

    for r in range(n):
        mp[s[r]] += 1
        maxCnt = max(maxCnt, mp[s[r]])

        # shrink window
        if r - l + 1 > maxCnt + k:
            # notice how counter removes element automatically when they become zero
            mp[s[l]] -= 1
            l += 1

    return len(s) - l

```

### Binary Subarray with Sum

Given a binary array `nums` and an integer `goal`, return _the number of non-empty **subarrays** with a sum_ `goal`.

A **subarray** is a contiguous part of the array.

```
Input: nums = [1,0,1,0,1], goal = 2
Output: 4
```

Solution is straightforward : Count Subarrays where `sum == 0`

```python

def numSubarraysWithSum(nums: List[int], goal: int) -> int:
    
    def atmost(target):
        # important check, as goal = 0, fails due goal - 1 < 0
        if target < 0:
            return 0

        n = len(nums)
        mp = collections.Counter()

        l, ans = 0, 0
        for r in range(n):
            mp[nums[r]] += 1

            while mp[1] > target:
                mp[nums[l]] -= 1
                l += 1

            ans += (r - l + 1)
        
        return ans

    return atmost(goal) - atmost(goal - 1)

```

### Count Number of Nice Subarray

Given an array of integers `nums` and an integer `k`. A continuous subarray is called **nice** if there are `k` odd numbers on it.

Return _the number of **nice** sub-arrays_.

Input: `nums = [1,1,2,1,1]`, k = 3
Output: 2
Explanation: The only sub-arrays with 3 odd numbers are `[1,1,2,1]` and `[1,2,1,1]`.

Similar Question : `Exactly K odd numbers = Atmost K odd numbers - Atmost (K-1) odd numbers`
Try not to use map this time, and use `oddCnt` variable only.

### Number of Substrings Containing All Three Characters

Given a string s consisting only of characters a, b and c.

Return the number of substrings containing at least one occurrence of all these characters a, b and c.

```
Input: s = "abcabc"
Output: 10
Explanation: The substrings containing at least one occurrence of the characters a, b and c are "abc", "abca", "abcab", "abcabc", "bca", "bcab", "bcabc", "cab", "cabc" and "abc" (again). 
```

Solution :

```python

from collections import Counter

def numberOfSubstrings(s: str) -> int:
    count = Counter()
    l = 0
    ans = 0
    n = len(s)

    for r in range(n):
        count[s[r]] += 1

        while count['a'] > 0 and count['b'] > 0 and count['c'] > 0:
            ans += n - r
            count[s[l]] -= 1
            l += 1

    return ans

```

### Maximum Points You can Obtain from Cards

There are several cards arranged in a row, and each card has an associated number of points. The points are given in the integer array cardPoints.

In one step, you can take one card from the beginning or from the end of the row. You have to take exactly k cards.

Your score is the sum of the points of the cards you have taken.

Given the integer array cardPoints and the integer k, return the maximum score you can obtain.

```
Input: cardPoints = [1,2,3,4,5,6,1], k = 3
Output: 12
Explanation: After the first step, your score will always be 1. However, choosing the rightmost card first will maximize your total score. The optimal strategy is to take the three cards on the right, giving a final score of 1 + 6 + 5 = 12.
```

This looks more like greedy, or two-pointer problem, but we can think of this sliding window problem.

So taking cards from front/back, leaves us with a window of `(n-k) size` and it should be minimum to maximize the other taken cards.

Find minimum in the fixed size window and then subtract from total sum.

```python
def maxScore(self, cardPoints: List[int], k: int) -> int:
    n = len(cardPoints)
    w = n - k # reset window size
    win_sum = sum(cardPoints[:w])
    res = win_sum
    for i in range(w, n):
        win_sum += (cardPoints[i] - cardPoints[i-w])
        res = min(res, win_sum)
    return sum(cardPoints) - res
```


### Minimum Window Substring ⭐

Given two strings s and t of lengths m and n respectively, return the minimum window of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

```
Example 1:
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
```

We use a sliding window. Expand the right pointer until the window contains all required characters of t.
Then shrink from the left to make it minimal.
Track the smallest valid window seen.

```python

from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not t or not s:
        return ""

    need = Counter(t)      # required character counts
    missing = len(t)       # how many characters still needed

    left = 0
    best_len = float("inf")
    best_start = 0

    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1

        # window is valid
        while missing == 0:
            window_len = right - left + 1
            if window_len < best_len:
                best_len = window_len
                best_start = left

            # shrink from left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1

    return "" if best_len == float("inf") else s[best_start:best_start + best_len]

```

### Absolute Diff less than or Equal to Limit ⭐

Given an array of integers `nums` and an integer `limit`, return the size of the longest **non-empty** subarray such that the absolute difference between any two elements of this subarray is less than or equal to `limit`

```

Input: nums = [8,2,4,7], limit = 4
Output: 2 
Explanation: All subarrays are: 
[8] with maximum absolute diff |8-8| = 0 <= 4.
[8,2] with maximum absolute diff |8-2| = 6 > 4. 
[8,2,4] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4,7] with maximum absolute diff |8-2| = 6 > 4.
[2] with maximum absolute diff |2-2| = 0 <= 4.
[2,4] with maximum absolute diff |2-4| = 2 <= 4.
[2,4,7] with maximum absolute diff |2-7| = 5 > 4.
[4] with maximum absolute diff |4-4| = 0 <= 4.
[4,7] with maximum absolute diff |4-7| = 3 <= 4.
[7] with maximum absolute diff |7-7| = 0 <= 4. 
Therefore, the size of the longest subarray is 2.

```

A simple brute force solution will be to generate all subarrays, which will be quadratic time.
A simpler solution is to run a sliding window over the array keeping track of the minimum and maximum numbers in this window.

A Simpler solution using Priority Queue (Heaps) : Time : $O(n\log n)$

```python

import heapq
def longestSubarray(nums: List[int], limit: int):
    maxq, minq = [], []
    res = i = 0

    for j, a in enumerate(nums):
        heapq.heappush(maxq, [-a, j])
        heapq.heappush(minq, [a, j])

        # shrink the window
        while -maxq[0][0] - minq[0][0] > limit:
            i = min(maxq[0][1], minq[0][1]) + 1
            while maxq[0][1] < i: heapq.heappop(maxq)
            while minq[0][1] < i: heapq.heappop(minq)
        
        res = max(res, j - i + 1)
    
    return res

```

A more simpler optimization is to use Monotonic Queue & Sliding Window to keep track of the Maximum and Minimum both in the same window.

```python

from collections import deque

def longestSubarray(nums: List[int], limit: int):
    maxd, mind = deque(), deque()
    l = 0

    for r in range(len(nums)):
        v = nums[r]

        # maintain decreasing max deque
        while maxd and v > maxd[-1]:
            maxd.pop()

        # maintain increasing min deque
        while mind and v < mind[-1]:
            mind.pop()

        maxd.append(v)
        mind.append(v)

        # shrink window if invalid
        if maxd[0] - mind[0] > limit:
            if maxd[0] == nums[l]:
                maxd.popleft()
            if mind[0] == nums[l]:
                mind.popleft()
            l += 1

    return len(nums) - l

```


### Minimum Window Subsequence ⭐

Given strings s and t, find the shortest substring of s such that t is a subsequence of that substring.

- Characters of t must appear in order
- They do not have to be contiguous

```
s = "abcdebdde"
t = "bde"
Output = "bcde"

```

- We **cannot shrink greedily from the left** like substring problems
- Order matters, counts don’t

Two-Phase Scan

- Forward Scan : find a valid window
- Backward Scan : minimize that window

```python

def minWindowSubsequence(s: str, t: str) -> str:
    n, m = len(s), len(t)
    min_len = float("inf")
    start = -1

    i = 0
    while i < n:
        j = 0

        # Step 1: forward scan
        while i < n:
            if s[i] == t[j]:
                j += 1
                if j == m:
                    break
            i += 1

        if j < m:
            break  # no more valid windows

        # Step 2: backward scan
        end = i
        j -= 1
        while i >= 0:
            if s[i] == t[j]:
                j -= 1
                if j < 0:
                    break
            i -= 1

        # update answer
        window_len = end - i + 1
        if window_len < min_len:
            min_len = window_len
            start = i

        # Step 3: move forward
        i = i + 1

    return "" if start == -1 else s[start:start + min_len]

```


