# SAT, SMT and Constraint Solving

## Computational Complexity and Decision Problems

Decision Problem is a computation problem that can be posed as *yes* or *no* problem on a set of inputs.

![](assets/Pasted%20image%2020260215123951.png)
A *decision procedure* for a decision problem is an algorithmic method that answers the yes-no question on all inputs, and a decision problem is called decidable if there is a decision procedure for it.

Example : given two numbers _x_ and _y_, does _x_ evenly divide _y_ ? Yes there is a procedure called as long division.

Given a list of variables and a boolean expression, does that expression evaluate to Yes or No.

Does the given graph contains a cycle ?

Solvers answer existence questions, not constructive algorithms.

### Complexity Classes

- Constant / Log / Polynomial / Exponential
- Tractable vs Intractable
### P Polynomial Time

- Problems solvable in polynomial time by a deterministic algorithm
- Examples : Sorting, shortest path

### NP (Nondeterministic Polynomial Time)

- Solutions can be checked efficiently, but no known efficient method to find solutions in all cases
- e.g. Traveling Salesman Problem, Sudoku, Boolean satisfiability (SAT)

We know $(P \subseteq NP)$ but we do not know whether $P = NP$ or $P \ne NP$ (This is the P vs NP Problem)
## P vs NP, SAT and Limits of Computation

Video Explanation : [Link](https://www.youtube.com/watch?v=6OPsH8PK7xM)

*Satisfiability (SAT)*

Given Variables : $a, b, c, d$
Given Constraint : $a \text{ OR } (\text{ NOT } c), \text{ NOT } b, b \text{ OR } (\text{ NOT } c) \text{ OR } (\text{ NOT } d)$

In general Constraint can be anything arbitrarily, but we can consider a simple case *CNF-SAT* (**Conjunctive Normal Form**), Each constraint is a variables and their negation connected by OR.

Task is to set values of variables such that are constraint are true.

Given a large satisfiability problem, solving it or figuring out whether a solution exists or not is a very hard problem.

In general, solving SAT problem can be modeled as a simple circuit where we are given variables as inputs to SAT solver which runs the circuit on inputs, to evaluate the circuit,

Running it backwards is same as given a Constraint, and figuring out the solution which a SAT Solver tries to solve. Verifying the product is easier, but solving it is hard.

![](assets/Pasted%20image%2020260215125806.png)

Example of Factoring a Large Number, Effectively reducing the problem of prime factorization into SAT problem.

Breaking RSA (factoring numbers of size $10^{500}$ ) our reductions Solving SAT with ~ 50M variables.

If we had a solver which could solve the problem in linear or quadratic time, then we could solve RSA.

### General Reductions

Similar to above, 3-coloring problem can be reduced into SAT Problem. Verifying 3-coloring is easy, but solving it is difficult.

![](assets/Pasted%20image%2020260215130354.png)
We can reduce these problems into SAT Problem in Polynomial Time, So solving SAT problem in Polynomial Time effectively solves all these class of problem in Polynomial Time.

A problem is $NP$ complete if

- It is in NP
- Every problem in NP is reducible to it in polynomial time. (= NP Hard) 

Satisfiability is NP Complete was proved by Stephen Cook and Leonid Levin independently.

Richard Karp further proved there are bunch of problems which can be converted into SAT problems using Reductions.
[Link](https://en.wikipedia.org/wiki/Karp%27s_21_NP-complete_problems)

![](assets/Pasted%20image%2020260215130825.png)

So if we cannot say with certainty

- We can verify a potential solution $\implies$ We can solve the problem
- We can compute $f$ $\implies$ We can compute $f^{-1}$

So Famous Is P = NP ? Reduces to whether can we effectively invert algorithms ? Does the polynomial time SAT solver exists ?

Existing SAT solver are no better than brute forcing all the inputs.

An **SMT solver** (Satisfiability Modulo Theories) and a **SAT solver** (Satisfiability Solver) are tools used to determine the satisfiability of logical formulas

SMT Solvers checks satisfiability of formulas over one or more background theories (e.g., integers, real numbers, arrays) extending SAT Solver with formulas involving richer theories (e.g., arithmetic, bit-vectors, arrays), 

A SMT Solver could be more complex than NP Complete, depending on theories involved.
## Z3 - SMT Solver

Z3 is high performance theorem prover solver developed at *Microsoft Research*. Z3 can be used in software/hardware verification and testing, constraint solving, analysis of hybrid systems, security, biology, and geometrical problems.

[Z3 Python API Docs](https://ericpony.github.io/z3py-tutorial/guide-examples.htm)

### Boolean Logic

Z3 supports Boolean operators: And, Or, Not, Implies (implication), If (if-then-else). Bi-implications are represented using equality `==`. The following example shows how to solve a simple set of Boolean constraints.

```python
p = Bool('p')
q = Bool('q')
r = Bool('r')
solve(Implies(p, q), r == Not(q), Or(Not(p), r))


### 
p = Bool('p')
q = Bool('q')
print (And(p, q, True))
print (simplify(And(p, q, True)))
print (simplify(And(p, False)))

# combining polynomial & Boolean Expression
p = Bool('p')
x = Real('x')
solve(Or(x < 5, x > 10), Or(p, x**2 == 2), Not(p))
```
### Solvers

Z3 provides different solvers. The command *solve* is implemented using Z3 solver API.

```python
x = Int('x')
y = Int('y')

s = Solver()
print (s)

s.add(x > 10, y == x + 2)
print (s)
print ("Solving constraints in the solver s ...")
print (s.check())

print ("Create a new scope...")
s.push()
s.add(y < 11)
print (s)
print ("Solving updated set of constraints...")
print (s.check())

print ("Restoring state...")
s.pop()
print (s)
print ("Solving restored set of constraints...")
print (s.check())
```
### Arithmetic & Machine Arithmetic

Refer to Link
### Functions

Function in Z3 have no side-effect and are *total*. That is they are defined on all input values. This includes functions, like division. Z3 is based on *first-order logic*


```python
x = Int('x')
y = Int('y')
f = Function('f', IntSort(), IntSort())
s = Solver()
s.add(f(f(x)) == x, f(x) == y, x != y)
print (s.check())
m = s.model()
print ("f(f(x)) =", m.evaluate(f(f(x))))
print ("f(x)    =", m.evaluate(f(x)))
```

### Satisfiability and Validity

A formula/constraint F is **valid** if F always evaluates to true for any assignment of appropriate values to its uninterpreted symbols.

A formula/constraint F is **satisfiable** if there is some assignment of appropriate values to its uninterpreted symbols under which F evaluates to true.

```python
p, q = Bools('p q')
demorgan = And(p, q) == Not(Or(Not(p), Not(q)))

print(demorgan)

def prove(f):
    s = Solver()
    s.add(Not(f))
    if s.check() == unsat:
        print("proved")
    else:
        print("failed to prove")

print("Proving demogram")
prove(demorgan)
```

### Question using Z3 solver

Question : [Link](https://adventofcode.com/2025/day/10)

For each machine there is a final state given, and we are supposed to provide button presses which would lead us to final state,


```
[button_states] (button_pairs) {joltage requirements}
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

So pressing any button even number of times will not affect the final state, so each button must be pressed or not pressed. (two states)

We could quickly bruteforce the solution for the first part where, joltage requirements are not enforced.

```python
import z3

def main():
    p1 = 0

    with open("10.txt") as f:
        for line in f:
            words = line.split()
            goals = words[0]
            goals = goals[1:-1]
            goals_n = 0
            for i, c in enumerate(goals):
                if c == "#":
                    goals_n += 2**i

            buttons = words[1:-1]
            B = []
            NS = []

            for button in buttons:
                ns = [int(x) for x in button[1:-1].split(",")]
                button_ns = sum(2**x for x in ns)
                B.append(button_ns)
                NS.append(ns)

            # try all possible using bitmask
            score = len(buttons)
            for a in range(2 ** len(buttons)):
                an = 0
                a_score = 0
                for i in range(len(buttons)):
                    if ((a >> i) % 2) == 1:
                        an ^= B[i]
                        a_score += 1
                if an == goals_n:
                    score = min(score, a_score)
            p1 += score
    print(p1)
```

As the order you press the buttons doesn't matter, you can express the amount of times each button was pressed as a single number. When you do this, the joltage you get afterwards is based on the sum of specific buttons. We can model this as a **system of linear equations**.

```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

$$
\begin{align}
x_4 + x_5 &= 3 \\
x_1 + x_5 &= 5 \\
x_2 + x_3 + x_4 &= 4 \\
x_0 + x_1 + x_3 &= 7
\end{align}
$$

Note here : $x_0$ number of times the first button is pressed, $x_1$ : number of times second button is pressed.

$$
\begin{pmatrix}
0 & 0 & 0 & 0 & 1 & 1 \\
0 & 1 & 0 & 0 & 0 & 1 \\
0 & 0 & 1 & 1 & 1 & 0 \\
1 & 1 & 0 & 1 & 0 & 0
\end{pmatrix}
\cdot
\begin{pmatrix}
x_{0}\\
x_{1}\\
x_{2} \\
x_{3} \\
x_{4} \\
x_5
\end{pmatrix}
=
\begin{pmatrix}
3 \\
5 \\
4 \\
7
\end{pmatrix}
$$

More Generalized Form

$$
\begin{pmatrix}
a_{11} & a_{12} & \dots & a_{1n} \\
a_{21} & a_{22} & \dots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \dots & a_{mn}
\end{pmatrix}
\cdot
\begin{pmatrix}
x_{0}\\
x_{1}\\
\vdots\\
x_{n}
\end{pmatrix}
=
\begin{pmatrix}
b_{0}\\
b_{1}\\
\vdots\\
b_{n}
\end{pmatrix}
$$

```python

# solve Ax = B
# where A ~ effect of each button
# x = how many times we press that button
# B = goal state

joltage = words[-1]
joltage_ns = [int(x) for x in joltage[1:-1].split(",")]

V = []
for i in range(len(buttons)):
    V.append(z3.Int(f"B{i}"))
EQ = []
for i in range(len(joltage_ns)):
    terms = []
    for j in range(len(buttons)):
        if i in NS[j]:
            terms.append(V[j])
        eq = sum(terms) == joltage_ns[i]
        EQ.append(eq)

print(NS)
print(V)
print(EQ)
o = z3.Optimize()
o.minimize(sum(V))
for eq in EQ:
    o.add(eq)
for v in V:
    o.add(v >= 0)

assert o.check()
M = o.model()
for d in M.decls():
    p2 += M[d].as_long()

print(p2)
```

Instead of Z3 Solver you can use [Gauss Jordan Elimination](https://en.wikipedia.org/wiki/Gaussian_elimination)
to convert into row echelon form.

$$
\begin{pmatrix}
1 & 0 & 0 & 1 & 0 & -1 \\
0 & 1 & 0 & 0 & 0 & 1 \\
0 & 0 & 1 & 1 & 0 & -1 \\
0 & 0 & 0 & 0 & 1 & 1
\end{pmatrix}
\cdot
\begin{pmatrix}
x_{0}\\
x_{1}\\
x_{2} \\
x_{3} \\
x_{4} \\
x_5
\end{pmatrix}
=
\begin{pmatrix}
2 \\
5 \\
1 \\
3
\end{pmatrix}
$$

Now we can identify free variables from here

$$
\begin{align}
x_0 &= 2 - x_3 + x_5 \\
x_1 &= 5 - x_5 \\
x_2 &= 1 - x_3 + x_5 \\
x_4 &= 3 - x_5
\end{align}
$$

Now $x_3$ and $x_5$ being *free variables* - that is, if you have a value for those variables, you can set the value of the rest exactly.

We can brute force *free variables* (only 2) until we find a solution.
Example of optimal solution : $x_3 = 3, x_5 = 2$
Other optimal solutions : $x_3 = 1, x_5 = 0$, $x_3 = 4, x_5 =3$
