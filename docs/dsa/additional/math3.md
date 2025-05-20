# Modular Arithmetic

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

### Fast Modular Exponentiation

How can we calculate $A^B$ mod C quickly when B is a power of 2.

We can utilize : A^2 mod C = ((A mod C) (A mod C))mod C

How about when B is not perfect power of 2 ? i.e. $5^{117}$ mod 19.

1. divide B into powers of 2 by writing it in binary
   - 117 : 1110101 in binary = $2^0 + 2^2 + 2^4 + 2^5 + 2^6$ = (1 + 4 + 16 + 32 + 64)
   - $5^{117}$ mod 19 = $(5*5^4*5^{16}*5^{32}*5^{64})$ mod 19
2. Calculate mod C of powers of two $\le$ B
3. Use modular multiplication properties to combine the calculated mod C values

### Modular Inverse

Inverse : A number multiplied by its inverse gives 1

- Modular Inverse of A (mod C) is A ^ -1.
- (A * A^-1) $\equiv$ 1 (mod C) or equivalent (A * A^-1) mod C = 1.
- Only the numbers coprime to C (numbers that share no prime factors with C) have a modular inverse. (mod C)

#### Method to calculate Modular Inverse

Naive Approach : Calculate (A * B) mod C for B values 0 through C-1, such that (A * B) mod C = 1.

Above approach is naive if B is of powers of 10^9. A better approach is extended Euclidean algorithm.

### The Euclidean Algorithm

This algorithm finds gcd (Greatest Common Divisor) of two numbers very quickly.

The Euclidean Algorithm for finding GCD(A,B) is as follows :

- If A = 0, then GCD(A ,B) = B, since GCD(0, B) = B, we can stop
- If B = 0, then GCD(A ,B) = A, since GCD(A, 0) = A, we can stop
- Write A in quotient form ( A = B . Q + R)
- Find GCD (B,R) using the euclidean algorithm since GCD(A, B) = GCD(B, R)

C++ code for above algorithm.

````c++
int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); } 
int lcm(int a, int b) { return a * (b / gcd(a, b)); }
````

Ques  : Calculate 2 ^ n mod C, where n ~ 10^9 and C is 10^9+7. Write a C++ program for the problem.

````
#include <bits/stdc++.h>
using namespace std;

#define MOD 1000000007

int main() {
	int n, ans = 1;
	cin >> n;
	for(int i = 0; i < n; i++) {
		ans *= 2;
		ans %= MOD;
	}
	cout << ans;
}
````

#### Resources

- [Khan Academy](https://www.khanacademy.org/computing/computer-science/cryptography#modarithmetic)

To update

Modular Arithmetic & Exponentiation

Topics:
	•	Modular Properties (add, subtract, multiply)
	•	Modular Exponentiation (Binary Exponentiation)
	•	Modular Inverse
	•	Fermat’s Little Theorem
	•	Extended Euclidean
	•	Modular Combinatorics
	•	Modular Division
	•	Chinese Remainder Theorem
	•	Euler’s Theorem
	•	Wilson’s Theorem
	•	Fast Power Techniques
	•	Modular Arithmetic in Primes vs Non-Primes