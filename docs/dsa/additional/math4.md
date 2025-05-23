# Advanced Math Topics

## Pell’s Equation (Basic Form)

Form:
$$
x^2 - D y^2 = 1
$$

- A special type of Diophantine Equation
- Has integer solution only for non-square D

Approach:

- Use a continued fraction to find its minimal solution
- Once smalled solution $(x_1, y_1)$ is known rest can be generated using

$$
x_{k+1} + y_{k+1}\sqrt D = (x_1 + y_1\sqrt D)^{k+1}
$$

- Used in Number theory problems, math olympiads etc.

## Mobius Function & Inversion Principle

Definition: For integer $n$ define
$$
\mu(n) = \begin{cases}
1 & \text{if } n = 1 \\
(-1)^k & \text{if n is a product of k distinct prime} \\
0 & \text{If n has squared prime factors}
\end{cases}
$$
Properties:

- Used in **inclusion-exclusion**, number-theoretic transforms.
- Appears in **Dirichlet convolution**:

$$
f(n) = \Sigma_{d|n} g(d) \implies g(n) = \Sigma_{d|n} \mu(d) f(\frac{n}{d})
$$

- **Use Case**: Inverting divisor sums, e.g., recovering $\phi(n)$ from sum over divisors.

## Integer Partitions (Combinatorial DP)

Number of ways to write n as sum of positive numbers (order doesn’t matter)

$P(n)$ = partition function

Example

- 4 has 5 partition : 4, 3+1, 2+2, 2+1+1, 1+1+1+1

````python
def partition_count(n):
    dp = [1] + [0] * n
    for i in range(1, n+1):
        for j in range(i, n+1):
            dp[j] += dp[j - i]
    return dp[n]
````

- Used in: DP optimization, partition-related number theory problems.

## Base Conversions & Number Representations

- **Binary**: base 2
- **Octal**: base 8
- **Decimal**: base 10
- **Hexadecimal**: base 16

Conversion Technique

- Decimal → base b: repeated division by b
- Base b → decimal: weighted sum by powers of b

Two’s Complement: Signed binary representation

## Continued Fractions (Optional, for theory-heavy contests)

$$
\text{Definition} = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 + \dots}}
$$

Used in :

- Solving Pell’s Equation
- Approximating Irrational with rational
- Analyzing number properties (e.g. irrationality of $e, \pi$)

Application

- Minimal Solution for Pell’s Equation
- Rational Approximation of $\sqrt D, \pi, e$