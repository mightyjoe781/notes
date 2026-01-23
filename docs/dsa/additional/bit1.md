# Bit Manipulation

Bit manipulation enables direct work with the binary representation of numbers. It optimizes performance and solves problems involving sets, parity, power-of-two checks, and other applications.

### XOR Properties

XORs have 2 important property other than commutative & associativity

- Identity Element: $A \oplus 0 = A$
- Self - Inverse : $A \oplus A = 0$

[All about XOR](https://accu.org/journals/overload/20/109/lewin_1915/)

### Basic Bit Operations

````c++
// Correct bit manipulation operations
bool checkBit(int n, int i) { return n & (1 << i); }
int setBit(int n, int i) { return n | (1 << i); }
int clearBit(int n, int i) { return n & ~(1 << i); }
int toggleBit(int n, int i) { return n ^ (1 << i); }
int getRightmostSetBit(int n) { return n & -n; } // used for subset iteration
int clearRightmostSetBit(int n) { return n & (n - 1); }
````

### Counting Bits

- Count total set Bits (Hamming Weight)

````c++
// Loop method
int count = 0;
for (int i = 0; i < 32; ++i)
    if (n & (1 << i)) ++count;

// Built-in (GCC/Clang) : NOTE these are invalid for n = 0
int count = __builtin_popcount(n);
int countll = __builtin_popcountll(n);  // For long long
````

```python
x = 13
set_bits = bin(x).count('1')  # 3
```

- Count trailing zeroes (rightmost 0s)

````cpp
int tz = __builtin_ctz(n);	// Undefined if n == 0
````

```python
tz = len(bin(x)) - len(bin(x).rstrip('0')) - 2 # remove(0b)
```

- Count leading zeroes :


````cpp
int lz = __builtin_clz(n);  // Undefined if n == 0
````

```python
bit_length = x.bit_length()
lz = 32 - bit_length
```

### Bit Tricks

- Get Rightmost set bit : Used for iterating over subsets

````c++
// bit manipulation
int r = n & -n  // Two's complement trick // doesn't work if n=0
// OR
int r = n & (~n + 1)  // Explicit two's complement
````

- Remove Rightmost set bit :

````cpp
// Useful for counter number of set bits : (Kernighan’s Algorithm)
n = n & (n-1)
````

- Reverse Bits (Manually)

````c++
unsigned int reverseBits(unsigned int n) {
    unsigned int rev = 0;
    for (int i = 0; i < 32; ++i)
        rev = (rev << 1) | ((n >> i) & 1);
    return rev;
}
````

- Iterate over all subsets of a Bitmask. Useful in DP on subsets

````c++
int mask = ...;
for (int sub = mask; sub; sub = (sub - 1) & mask) {
    // process sub
}
````

```python

mask = ...  # define your mask value here
sub = mask
while sub:
    # process sub
    sub = (sub - 1) & mask

```

- XOR Trick : Detect Single Number
    - Find the number that appears odd number of times, given there is only one such number.

````c++
int xor_all = 0;
for (int a : arr) xor_all ^= a;
````

- Swap without temporary variable
    - avoid in production, not readable, not safe with references to same memory if `a` and `b` refers to same memory location

````c++
a ^= b;
b ^= a;
a ^= b;
````

- Check power of two

````c++
bool isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
````

- Difference Bits Sum Pairwise
    - Efficiently calculates total XOR difference over all pairs

````c++
// A - array of numbers
long long total = 0;
int n = A.size();
for (int i = 0; i < 32; ++i) {
    int count = 0;
    for (int x : A)
        if (x & (1 << i)) count++;
    total += 2LL * count * (n - count);
}
````

- Binary String Representation

````c++
bitset<32> bs(n);
cout << bs.to_string() << "\n";
````

- Turn Off Last Consectuive Set Bits : `x = x & (x + 1);`
- Turn On Last Zero Bit : `x = x | (x + 1);`
- Log Base 2 : `int highestSetBit = 31 - __builtin_clz(n);  // Position of MSB (0-indexed)`
- Parity (Even or Odd Number of Set Bits) : `bool evenParity = __builtin_parity(n) == 0;`

## Builtins

| **Functionality**                   | **C++ Built-in**          | **Python Equivalent (or Alternative)**                  |
| ----------------------------------- | ------------------------- | ------------------------------------------------------- |
| **Count 1s in binary (popcount)**   | `__builtin_popcount(x)`   | bin(x).count('1') or x.bit_count() (Python 3.10+)       |
| **Count 1s in 64-bit int**          | `__builtin_popcountll(x)` | bin(x).count('1') or x.bit_count() (works for int)      |
| **Count trailing zeroes**           | `__builtin_ctz(x)`        | len(bin(x & -x)) - 3 or use custom function (see below) |
| **Count leading zeroes (32-bit)**   | `__builtin_clz(x)`        | 32 - x.bit_length()                                     |
| **Parity (even/odd 1s)**            | `__builtin_parity(x)`     | bin(x).count('1') % 2                                   |
| **Check if power of 2**             | N/A                       | x > 0 and (x & (x - 1)) == 0                            |
| **Get lowest set bit**              | N/A                       | x & -x                                                  |
| **Remove lowest set bit**           | N/A                       | x & (x - 1)                                             |
| **Reverse bits manually**           | N/A (manual loop)         | Use a loop, or: int('{:032b}'.format(x)[::-1], 2)       |
| **Highest set bit position (log2)** | `31 - __builtin_clz(x)`   | x.bit_length() - 1                                      |

### Python Custom Helper Functions

````c++
def count_trailing_zeroes(x):
    return (x & -x).bit_length() - 1 if x != 0 else 32

def count_leading_zeroes(x, bits=32):
    return bits - x.bit_length() if x != 0 else bits

def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0
````

### Problems on Bit Manipulation

- **Single Number (Leetcode 136)** – XOR trick (A ^ A = 0)
- **Single Number II (Leetcode 137)** – Bit count per position, modulo 3 trick
- **Sum of XOR of all pairs** – Count set bits at each position, pairwise XOR contribution
- **Counting Bits (Leetcode 338)** – DP using n & (n - 1) to count set bits
- **Reverse Bits (Leetcode 190)** – Bit shifting and reconstruction
- **Hamming Distance (Leetcode 461)** – popcount(a ^ b)
- **Number of 1 Bits (Leetcode 191)** – Hamming weight, __builtin_popcount, loop-based
- **Power of Two (Leetcode 231)** – (n > 0 && (n & (n - 1)) == 0)
- **Power of Four (Leetcode 342)** – Power of two + only one bit set at even position
- **Bitwise AND of Numbers Range (Leetcode 201)** – Common prefix by bit shifting
- **Subsets Generation** – Bitmask subset loop: (sub - 1) & mask
- **Maximum XOR of Two Numbers in an Array (Leetcode 421)** – Trie + greedy on MSBs
- **Total Hamming Distance (Leetcode 477)** – Bitwise count at each position
- **Missing Number (Leetcode 268)** – XOR from 0 to n with array
- **Binary Watch (Leetcode 401)** – Count set bits, generate valid times
- **Complement of Base 10 Integer (Leetcode 1009)** – Flip bits up to MSB
- **Find Rightmost Set Bit** – x & -x, used in subset iteration, masks, etc.

## Problems

### Divide Two Integers

Given two integers `dividend` and `divisor`, divide two integers **without** using multiplication, division, and mod operator.

The integer division should truncate toward zero, which means losing its fractional part. For example, `8.345` would be truncated to `8`, and `-2.7335` would be truncated to `-2`.

Return _the **quotient** after dividing_ `dividend` _by_ `divisor`.

Hint : We can subtract using bit operations, and repeated subtraction is nothing but division.

```python

def divide(self, A, B):
    # overflow case !!
    # divide (-2^31/ -1) -> 2^31 (overflows as range is [-2^31, 2^31-1])
    if (A == -2147483648 and B == -1): return 2147483647
    a, b, res = abs(A), abs(B), 0
    for x in range(32)[::-1]:
        # check if current shifted divisor fits
        if (a >> x) - b >= 0:
            res += 1 << x # Adds 2^x to quotient
            a -= b << x # Substract b.2^x from reminder
    # fix final sign
    return res if (A > 0) == (B > 0) else -res

```

### Minimum Bit Flips to Convert Number

A **bit flip** of a number `x` is choosing a bit in the binary representation of `x` and **flipping** it from either `0` to `1` or `1` to `0`.

```python

def minBitFlips(start, goal):
    return bin(start ^ goal).count('1')

```

### Single Number

Given a **non-empty** array of integers `nums`, every element appears _twice_ except for one. Find that single one.

Straightforward XOR application, similar numbers cancel out, leaving only the number occuring once.

```python
def singleNumber(nums):
    return reduce(lambda x, y: x ^ y,nums)
```


### Find Two numbers appearing odd number of times

**Problem Statement:** Given an array nums of length n, every integer in the array appears twice except for two integers. Identify and return the two integers that appear only once in the array. Return the two numbers in **ascending order**.  
  
For example, if `nums = [1, 2, 1, 3, 5, 2]`, the correct answer is `[3, 5]`, not `[5, 3]`.

What is interesting here, is that since both number occurs odd number of times, xor of entire array is just xor of both number.

$$

XOR(0, n) = A \oplus B

$$

Although it looks like we can't restore both numbers, but let's think about both numbers for a bit, Assume both number are like following

```

A : 0b0001001010
B : 0b0010000010
            ~
NOTICE : how tilde bit is the first different bit,

```

So we can divide all numbers into two groups, 1st group with `~` bit as set, and another group as `~` bit set as unset.

Now lets say there are `a0, a1, a2, ...` and `b0, b1, b2, ...` are those groups, and since these numbers appear in group, so total numbers will be.

```
group 1 : {a0, a0, a1, a1, ....., A}
group 2 : {b0, b0, b1, b1, ....., B}

```

If we take xor of both groups separately, then we will be able to restore the numbers.

```python

def main(nums):
    
    xor_xy = reduce(xor, nums)
    # xor set i th bit 0 if different, find that
    i = (~xor_xy) & (xor_xy + 1)

    x, y = 0, 0

    for num in nums:
        # check group membership
        if num & (1 << i):
            x ^= num
        else:
            y ^= num

    return x, y

```