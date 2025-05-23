# Modular Arithmetic & Exponentiation

## Core Concepts

$$
\frac{A}{B} = Q\text{ remainder }R
$$

Here, A : dividend, B : divisor, Q : quotient, R : remainder. Sometimes we only wish to calculate the remainder only. For that purpose we use modulo operator. (%)

$A \mod{B} = R$

A *modulo* B is *equal* to R. Here B is referred as the **modulus**.
$$
A \mod{B} = (A + K.B) \mod{B} \text{ for any integer } K
$$

### Congruence Modulo

$$
A \equiv B \mod {C}
$$

Above expression says A is **congruent** to B modulo C.
A common way of expressing two values are in the same **equivalence class**.

e.g. 26 $\equiv$ 11 (mod 5).

- 26 mod 5 = 1
- 11 mod 5 = 1

Both 26 and 11 belong to equivalence class for 1.

### Equivalence Relations

Note following relations.

- $A \equiv B (mod\ C) \\$
- $A \ mod \ C = B \ mod \ C \\$
- C | (A - B)  : ( The | symbol means divide, or is a factor of)
- A  = B + K. C (where K is some integer)

Congruence Modulo is an Equivalence Relation. Follows equivalence property.

- A $\equiv$ A (mod C) (Reflexive)
- if A $\equiv$ B (mod C) then B $\equiv$ A (mod C) (Symmetric)
- if A $\equiv$ B (mod C) and B $\equiv$ D (mod C) then A $\equiv$ D (mod C) (Transitive)

### Quotient Remainder Theorem

Given any integer A, and a positive integer B, there exist unique integers Q and R such that
$$
A = B * Q + R \text{ where } 0 \le R < B
$$
From this form actually imerges **A mod B = R**.

### Modular Properties

- Modular Addition
  - (A + B) mod C = (A mod C + B mod C) mod C
- Modular Subtraction
  - (A - B) mod C = (A mod C - B mod C) mod C
- Modular Multiplication
  - (A * B) mod C = (A mod C * B mod C) mod C
- Modular Exponentiation
  - $A^{B}$ mod C = $(A \mod C)^{B}$ mod C
- Extension of Product property above
  - $(A * B * C)$ mod D = ( ( A mod D) (B mod D) (C mod D) ) mod D

### Modular Exponentiation (Binary Exponentiation)

- How can we calculate $A^B$ mod C quickly when B is a power of 2.
- We can utilize : $A^2$ mod C = ((A mod C) (A mod C))mod C

How about when B is not perfect power of 2 ? i.e. $5^{117}$ mod 19.

- divide B into powers of 2 by writing it in binary
  - 117 : 1110101 in binary = $2^0 + 2^2 + 2^4 + 2^5 + 2^6$ = (1 + 4 + 16 + 32 + 64)
  - $5^{117}$ mod 19 = $(5*5^4*5^{16}*5^{32}*5^{64})$ mod 19


- Calculate mod C of powers of two $\le$ B

- Use modular multiplication properties to combine the calculated mod C values

````python
def mod_exp(a, b, m):
    result = 1
    a %= m
    while b:
        if b & 1:
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1
    return result
````

- RSA, Diffie Hellman
- Competitive Programming Constraints $(1e9+7)$

### Modular Inverse

Inverse : A number multiplied by its inverse gives 1

- Modular Inverse of A (mod C) is A ^ -1.
- (A * A^-1) $\equiv$ 1 (mod C) or equivalent (A * A^-1) mod C = 1.
- Only the numbers coprime to C (numbers that share no prime factors with C) have a modular inverse. (mod C)

Implementation

Find x such that (a * x) % m == 1

1. If m is prime: use **Fermat’s Little Theorem**

   ⇒ a^(m-2) % m

2. If gcd(a, m) == 1: use **Extended Euclidean Algorithm**

````python
def modinv(a, m):
    g, x, _ = extended_gcd(a, m)
    return x % m if g == 1 else None
````

### Modular Division

- To compute: (a / b) % m, use inverse: `(a / b) % m = (a * b^(-1)) % m`
- b must be coprime with m

### Fast Exponentiation Techniques 

Variants:

- **Recursive**: cleaner but risk of stack overflow
- **Iterative**: preferred for tight loops
- **Matrix Exponentiation**: for Fibonacci/DP transitions in O(log n)
- **Modular Exponentiation**: use when modulus is large (1e9+7)



## Theorems & Advanced Techniques

### Fermat’s Little Theorem

If p is prime and a not divisible by p, then:

````python
a^(p−1) ≡ 1 (mod p)
⇒ a^(p−2) ≡ a^(-1) (mod p)
````

Usage:

- Modular inverse when mod is prime
- Simplifying power expressions in mod

### Euler’s Theorem

If a and m are coprime:

````python
a^φ(m) ≡ 1 (mod m)
⇒ a^(φ(m)-1) ≡ a^(-1) (mod m)
````

Works for non-prime m, using **Euler’s Totient $\phi(m)$**

### Wilson’s Theorem

For prime p: `(p−1)! ≡ −1 (mod p)`

Theoretical Interests, rarely used in implementation directly

### Euler’s Totient Function ($\phi (n)$)

$\phi(n)$ = Number of integers <= n that are coprime with n

If $n = p_1^{e_1} *p_2^{e_2} * ... *p_k^{e_k}$ (prime factorization)

````python
φ(n) = n * (1 - 1/p1) * (1 - 1/p2) * ... * (1 - 1/pk)
````

Efficient Implementation

````python
def phi(n):
    res = n
    i = 2
    while i*i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            res -= res // i
        i += 1
    if n > 1:
        res -= res // n
    return res
````

### Chinese Remainder Theorem (CRT)

Solve

````python
x ≡ a1 mod m1  
x ≡ a2 mod m2  
...  
````

Where m1, m2, ... are **pairwise coprime**

- Solution exists & is unique modulo M = m1*m2*...
- Combine equations step by step using extended Euclid

### Modular Arithmetic in Primes vs Non-Primes

| **Feature**         | **Prime Modulus**         | **Non-Prime Modulus**    |
| ------------------- | ------------------------- | ------------------------ |
| Inverses Exist      | If gcd(a, p) = 1 → always | Only if gcd(a, m) = 1    |
| Fermat’s Theorem    | ✅                         | ❌                        |
| Use Euler’s Theorem | ❌                         | ✅                        |
| Simplifications     | Easier (unique fields)    | Harder, may lack inverse |

- Prefer Primes like $1e9+7$ or $998244353$ for programming
