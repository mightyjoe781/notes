# Prime Numbers, GCD, LCM

## Prime Numbers

* A prime number is a number greater than 1 that has no positive divisors other than 1 and itself.
* 2 is the only prime-even number
* If n is not prime, then it has a factor $ \lt= \sqrt{n}$
* There are infinitely many prime numbers
* Naive Implementation take $O(n\sqrt n)$ time
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

Applications

* Cryptography (RSA, etc)
* Number theory Problems
* Factorization, divisibility problems

## GCD

* largest number that divides both `a` and `b`

Recursive Implementation

````c++
int gcd(int a, int b) {
  return b == 0 ? a : gcd(b, a % b);
}
````

Itertative Implementation

````c++
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

## LCM

* smallest number that is a multiple of both a and b

````c++
ll lcm(int a, int b) {
    return a / gcd(a, b) * 1LL * b; // prevent overflow
}
````

* Properties
  * $lcm(a, b, c) = lcm(lcm(a, b), c)$
  * $\gcd(a, b) * lcm(a, b) = a * b$

* Use cases
  * Scheduling problems
  * synchronizing cycles
  * counting common multiples

To Update

Prime Numbers, GCD, LCM

Topics:
	•	GCD & LCM Basics
	•	Prime Factorization
	•	Sieve of Eratosthenes
	•	Segmented Sieve
	•	Sieve for Smallest/Largest Prime Factors
	•	Count & Sum of Divisors
	•	Prime Number Theorems & Distribution
	•	Applications of GCD (LCM-related problems, reduction techniques)