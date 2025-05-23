# Number Theory

## GCD, LCM & Primes

### Euclidean Algorithm

- GCD (Greatest Common Divisor) : largest number that divides both `a` and `b`
- Approach : `gcd(a, b) = gcd(b, a % b)`
- Time: $O(\log \min(a, b))$

````c++
# recursive
int gcd(int a, int b) {
  return b == 0 ? a : gcd(b, a % b);
}

# iterative
int gcd(int a, int b) {
  while(b)
    a %= b, swap(a, b);
 	return a;
}
````

* Properties
  * $\gcd({a,0}) = a$
  * $\gcd(a, b) = \gcd(b, a\%b)$
  * $\gcd (a, b, c) = \gcd(\gcd(a, b), c)$
  * $\gcd(a, b) * lcm(a, b) = a * b$


### Extended Euclidean Algorithm

- Goal : Find $x, y$ such that $ax + by = gcd(a, b)$
- Useful for:
  - Finding modular inverse when $\gcd (a, m) = 1$
  - Solving Linear Diophantine Equations

````python
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1
````

### Applications of GCD (e.g., LCM tricks, reductions)

- LCM : smallest number that is a multiple of both a and b
- Approach : `LCM(a, b) = (a * b) // gcd(a, b)`
- Reduce $\frac{a}{b}$ to lowest terms, divide both by gcd(a, b)
- Problems
  - Rope cutting into equal parts
  - Synchronizing Cycles (LCM)

### Prime Numbers

* A prime number is a number greater than 1 that has no positive divisors other than 1 and itself.
* 2 is the only prime-even number
* If n is not prime, then it has a factor $ \lt= \sqrt{n}$
* There are infinitely many prime numbers
* Naive Implementation take $O(n\sqrt n)$ time

````python
def prime_factors(n):
    i = 2
    while i*i <= n:
        while n % i == 0:
            print(i, end=' ')
            n //= i
        i += 1
    if n > 1:
        print(n)
````

* Applications

  * Cryptography (RSA, etc)

  * Number theory Problems

  * Factorization, divisibility problems

### Count & Sum of Divisors

Let $n = p_1^{e_1} *p_2^{e_2} * ... *p_k^{e_k}$

- #Divisors = $(e_1 + 1) * (e_2 + 1)* ... *(e_k + 1)$
- Sum of Divisors = $((p_1^{(e_1 + 1)}-1)*(p_2^{(e_2 + 1)}-1))*...$

````python
def count_divisors(n):
    cnt = 1
    i = 2
    while i * i <= n:
        power = 0
        while n % i == 0:
            power += 1
            n //= i
        cnt *= (power + 1)
        i += 1
    if n > 1:
        cnt *= 2
    return cnt
````

### Square-Free Numbers

A number is square-free if no prime appears more than once in its factorization.

- 10 : (2, 5) - square free number
- 18 : (3, 3, 2) - not a square free number

Calculate using spf (implemented below) or trial division

## Sieve Techniques

### Sieve of Eratosthenes

* Sieve of Eratosthenes generates primes in $O(n \log \log n)$ 

````c++
// sieve implmentation to generate primes
vector<int> sieve(int N) {
		int i, a[N];
  	for(i = 2; i < N; i++) a[i] = 1;	// set entire array
    for(i=2;i<N;i++) 
        if(a[i])	//takes jumps of j to remove every multiple
            for(int j=i;j*i<N;j++) a[i*j]=0;
    return a;
}
````

### Segmented Sieve

- Used to find primes $[L, R]$ where $R$ is large ( <= 1e12)
- Steps
  - Precompute all primes up to $\sqrt R$ using simple sieve
  - Create a boolean array of size $R-L+1$
  - Mark all multiples of precomputed primes in the range

### Sieve for Smallest/Largest Prime Factors

Useful for fast factorization

````python
N = 10**6
spf = [0] * (N+1)

def compute_spf():
    for i in range(2, N+1):
        if spf[i] == 0:
            for j in range(i, N+1, i):
                if spf[j] == 0:
                    spf[j] = i
````

### Prime Distribution & Number Theorems

- $\pi (n)$ = number of primes $\le n \approx n / \log(n)$ Prime Number Theorem
- There are infinite primes (proved by contradiction - Euclid)

## Diophantine Equations

### Linear Diophantine Equations

**Form:** $ax + by = c$

**Solution exists if:** $\gcd(a, b)$ divides $c$

Find one solution using extended Euclid, then use:

````python
x = x0 + (b/g)*t  
y = y0 - (a/g)*t
````

### Integer Solution using GCD

- If g = gcd(a, b) divides c, then solutions exist.

- Scale extended Euclid’s output to match c/g.

### Application in Modular Inverse

- $a^{(-1)} \mod m$ exists if and only if $\gcd(a, m) == 1$
- Use extended Euclidean algorithm to find it.

````python
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None  # No inverse
    return x % m
````

