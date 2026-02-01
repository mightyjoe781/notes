# Digit DP

Digit DP is used to count or optimize over **numbers within a range** that satisfy certain properties.

Example Problem : count number of integers $x$ between $a$ and $b$ such that $x$ satisfies some property related to its digit.

$$
G(x) = G(b) - G(a-1)
$$

Typical Constraint

- $R \le 10^{18}$ ~ too large to iterate
- Digit wise dependencies

Core Idea : We build number *digit by digit* from *most significant to least* while tracking following state parameters

| **Parameter** | **Meaning**                                |
| ------------- | ------------------------------------------ |
| pos           | Current digit index                        |
| tight         | Whether we’re restricted by upper bound    |
| leading_zero  | Are we still skipping leading 0s           |
| sum / mask    | Any custom condition (sum of digits, etc.) |

NOTE: Let's say we are not bounded by *tight*, then the digit can be *0-9*.

Example ~ consider limiting integer to 3245 and we need to calculate G(3245)

```
index : 4 3 2 1
digit : 3 2 4 5

# so each of these digits serve as upper bound, so we don't cross the integer

e.g.
index : 4 3 2 1
digits: 3 2 4 5
generate integer: 3 1 _ _
Here index 2 has unrestricted range, since tight is not applicable

generate integer: 3 2 _ _
Here index 2 in tight, and it can't go over 4 [0, 4] range

```

Canonical Digit DP State : `dfs(pos, tight, leading_zero, extra_state)`

NOTE:

- $pos \in [0, len(num)]$
- $tight \in \{0, 1\}$
- $\text{leading\_zero} \in \{0, 1\}$

Transition Rules

- Maximum digits allowed
- For each digit $d \in [0, limit]$

```python
# max digit allowed
limit = digits[pos] if tight else 9

# for d 
new_tight = tight and (d == limit)
new_leading = leading_zero and (d == 0)
```

### Generic Template

````python
from functools import lru_cache

def digit_dp(num):
    digits = list(map(int, num))

    @lru_cache(None)
    def dfs(pos, tight, leading_zero):
        if pos == len(digits):
            return 1  # base case

        res = 0
        limit = digits[pos] if tight else 9

        for d in range(limit + 1):
            res += dfs(
                pos + 1,
                tight and (d == limit),
                leading_zero and (d == 0)
            )

        return res

    return dfs(0, True, True)
    
````

### Count numbers with digit sum divisible by k

First Thing we do is convert the given string digit into an array *digits*, here : "5234" ~ `[5, 2, 3, 4]`

Since here leading zero of no relevance when calculating divisibility.


```
# property
extra = sum_mod_k
```

````python
from functools import lru_cache

def count_sum_divisible(num, k):
    digits = list(map(int, num))

    @lru_cache(None)
    def dfs(pos, sum_mod, tight):
        if pos == len(digits):
            return sum_mod == 0

        res = 0
        limit = digits[pos] if tight else 9

        for d in range(limit + 1):
            res += dfs(
                pos + 1,
                (sum_mod + d) % k,
                tight and (d == limit)
            )

        return res

    return dfs(0, 0, True)

print(count_sum_divisible("5234", 3))

````

To count in range `[L, R]`

````c++
def solve(L, R, k):
    return count_sum_divisible(R, k) - count_sum_divisible(str(int(L) - 1), k)
````

## Common Use Cases

### Count Numbers with no repeated digits

```
mask = used digits (10-bit mask)
```

```python
def count_no_repeat(num):
    digits = list(map(int, num))

    @lru_cache(None)
    def dfs(pos, mask, tight, leading):
        if pos == len(digits):
            return 1

        res = 0
        limit = digits[pos] if tight else 9

        for d in range(limit + 1):
            if leading and d == 0:
                res += dfs(pos + 1, mask, tight and d == limit, True)
            else:
                if mask & (1 << d):
                    continue
                res += dfs(
                    pos + 1,
                    mask | (1 << d),
                    tight and d == limit,
                    False
                )

        return res

    return dfs(0, 0, True, True)
```


### Count Numbers with Alternating Digits

Adjacent digits must be different

```
# extra state
prev_digit
```


```python
def count_alternating(num):
    digits = list(map(int, num))

    @lru_cache(None)
    def dfs(pos, prev, tight, leading):
        if pos == len(digits):
            return 1

        res = 0
        limit = digits[pos] if tight else 9

        for d in range(limit + 1):
            if leading and d == 0:
                res += dfs(pos + 1, -1, tight and d == limit, True)
            else:
                if prev != -1 and d == prev:
                    continue
                res += dfs(pos + 1, d, tight and d == limit, False)

        return res

    return dfs(0, -1, True, True)
```

### Count Palindromes in a Range

Digit DP is hard for palindromes. Instead

- Generate palindrome by first half
- Compare with bounds

```python
def count_palindrome(n):
    s = str(n)
    length = len(s)
    half = (length + 1) // 2
    prefix = int(s[:half])

    pal = str(prefix) + str(prefix[:-1] if length % 2 else prefix)[::-1]
    return prefix - (pal > s)
```

### Sum of Digits of All Numbers in a Range

```
# state
return (count, sum)
```

```python
def digit_sum(num):
    digits = list(map(int, num))

    @lru_cache(None)
    def dfs(pos, tight):
        if pos == len(digits):
            return (1, 0)

        limit = digits[pos] if tight else 9
        total_cnt = total_sum = 0

        for d in range(limit + 1):
            cnt, s = dfs(pos + 1, tight and d == limit)
            total_cnt += cnt
            total_sum += s + d * cnt

        return total_cnt, total_sum

    return dfs(0, True)[1]
```

Range Query

```python
def range_digit_sum(L, R):
    return digit_sum(R) - digit_sum(str(int(L) - 1))
```


NOTE: When to Use Digit DP

- Constraint go up to $10^{18}$
- Condition depends on digits
- Range Queries are involved

## Problems

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