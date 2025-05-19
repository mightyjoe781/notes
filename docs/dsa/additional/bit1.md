# Bit Manipulation

Bit manipulation enables direct work with the binary representation of numbers. It optimizes performance and solves problems involving sets, parity, power-of-two checks, and other applications.

## XOR

XORs have 2 important property other than commutative & associativity

- Identity Element: $A \oplus 0 = A$
- Self - Inverse : $A \oplus A = 0$
- XOR is monotonic in absolute difference between numbers

[All about XOR](https://accu.org/journals/overload/20/109/lewin_1915/)

## Basic Bit Operations

* Check if `ith` bit is set

````c++
if (n * (1 << i)) {
  // i-th bit is set
}
````

- set the `ith` bit : `n |= (1 << i)`
- clear the `ith` bit : `n |= ~(1 << i)`
- toggle the `ith` bit : `n ^= (1 << i)`
- Count total set Bits (Hamming Weight)

````c++
int count = 0;
for (int i = 0; i < 32; ++i)
    if (n & (1 << i)) ++count;
````

````c++
int count = __builtin_popcount(n);        // GCC / Clang
int countll = __builtin_popcountll(n);    // For long long
````

- count trailing zeroes (rightmost 0s) : `int tz = __builtin_ctz(n);`
- count leading zeroes : `int lz = __builtin_clz(n);`

- Get Rightmost set bit : `int r = n & ~n`
  - Used for iterating over subsets
- Remove Rightmost set bit : `n = n & (n-1)`
  - Useful for counter number of set bits : (Kernighan’s Algorithm)
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

- XOR Trick : Detect Single Number
  - Find the number that appears odd number of times

````c++
int xor_all = 0;
for (int a : arr) xor_all ^= a;
````

- Swap without temporary variable
  - avoid in production, not readable, not safe with references to same memory

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

## Problems on Bit Manipulation

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
