# Digit DP

Digit DP is used to count or optimize over **numbers within a range** that satisfy certain properties.

### State Parameters

| **Parameter** | **Meaning**                                |
| ------------- | ------------------------------------------ |
| pos           | Current digit index                        |
| tight         | Whether we’re restricted by upper bound    |
| leading_zero  | Are we still skipping leading 0s           |
| sum / mask    | Any custom condition (sum of digits, etc.) |



### DP Template

````c++
int dp[20][2][2];  // pos, tight, leading_zero

int dfs(int pos, bool tight, bool leading_zero, string &num) {
    if (pos == num.size()) return /* base case */;
    
    if (dp[pos][tight][leading_zero] != -1) return dp[pos][tight][leading_zero];

    int res = 0;
    int limit = tight ? (num[pos] - '0') : 9;

    for (int d = 0; d <= limit; d++) {
        bool new_tight = (tight && d == limit);
        bool new_leading = (leading_zero && d == 0);
        res += dfs(pos + 1, new_tight, new_leading, num);
    }

    return dp[pos][tight][leading_zero] = res;
}
````

**Example: Count numbers with digit sum divisible by k**

````c++
int k;

int dfs(int pos, int sum, bool tight, string &num) {
    if (pos == num.size()) return (sum % k == 0);

    if (dp[pos][sum][tight] != -1) return dp[pos][sum][tight];

    int res = 0;
    int limit = tight ? (num[pos] - '0') : 9;

    for (int d = 0; d <= limit; d++) {
        res += dfs(pos + 1, (sum + d) % k, tight && (d == limit), num);
    }

    return dp[pos][sum][tight] = res;
}
````

To count in range `[L, R]`

````c++
int count(string x) {
    memset(dp, -1, sizeof dp);
    return dfs(0, 0, true, x);
}

int answer = count(R) - count(L - 1);
````

### Common Use Cases

- Count numbers with no repeated digits
- Count numbers with alternating digits
- Count palindromes in a range
- Sum of digits of all numbers in a range

### Problems

Digit DP is often implicit in “count how many numbers” problems involving digit constraints.

**Easy to Medium**

- [**902. Numbers At Most N Given Digit Set**](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/) - Classic Digit DP, counting numbers ≤ N from a set of digits.
- [**233. Number of Digit One**](https://leetcode.com/problems/number-of-digit-one/) - Count number of ‘1’s from 1 to N.
- [**357. Count Numbers with Unique Digits**](https://leetcode.com/problems/count-numbers-with-unique-digits/) - Use bitmask to ensure digit uniqueness.
- [**600. Non-negative Integers without Consecutive Ones**](https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/) - Count integers with no two consecutive 1s in binary representation.

**Medium to Hard**

- [**1012. Numbers With Repeated Digits**](https://leetcode.com/problems/numbers-with-repeated-digits/) - Complement count of numbers with all unique digits using digit DP.
- [**1397. Find All Good Strings**](https://leetcode.com/problems/find-all-good-strings/) - Hard variant combining digit DP and KMP automaton.
- [**6285. Count Beautiful Substrings I**](https://leetcode.com/problems/count-beautiful-substrings-i/) - Newer problem involving constraints on digit patterns.