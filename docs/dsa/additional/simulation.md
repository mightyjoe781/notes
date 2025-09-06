# Simulation & Randomized Algorithms

## Game Simulation Problems

* Simulate step-by-step execution of a game scenario or interaction according to predefined rules.
* Example
    * Grid Based Movement
    * Turn-Based Movement
    * Collision Handling
    * Entity Interaction (e.g. player/enemy/item)
* Common Patterns
    * Discrete Time Steps: Update the game state at each tick/turn. Minetest actually has globalstep timer you can utilise.
    * Grid Representation : models position of player, walls, obstacles
    * Entity Queue
    * State Tracking 
    * Rule Engine
* Techniques
    * BFS/DFS for movement (zombie spread, virus simulation)
    * PriorityQueue for ordering actions
    * Coordinate compression or hashing for large boards
    * Bitmasks or flags for power-ups, abilities

### Problems

- [LC 1275: Find Winner on a Tic Tac Toe Game](https://leetcode.com/problems/find-winner-on-a-tic-tac-toe-game/)
- [LC 794: Valid Tic Tac Toe State](https://leetcode.com/problems/valid-tic-tac-toe-state/)
- [LC 1496: Path Crossing](https://leetcode.com/problems/path-crossing/)
- [LC 847: Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/)

## Event Based Simulation

* Instead of updating the simulation at every time unit, only process **important events** that change the system. This improves efficiency.
* Idea
    * Maintain a priority queue of events
    * Each event is represented as `(timestamp, event_data)`
    * process events in *chronological order*
    * Each event may generate new future events
* Use Cases
    * systems where actions are sparse in time
    * Real-Time Simulations
    * Traffic/Server Processing Simulation
    * Collision Detection
    * Network Models

````python
import heapq

event_queue = []
heapq.heappush(event_queue, (event_time, event_type, data))

while event_queue:
    time, evt_type, evt_data = heapq.heappop(event_queue)
    
    if evt_type == "MOVE":
        # simulate movement, add next move
        heapq.heappush(event_queue, (time + dt, "MOVE", new_data))
    elif evt_type == "COLLISION":
        # resolve collision
        pass
````

- Check simulation Implementation : https://leetcode.com/problems/minimum-time-to-repair-cars/editorial/

## Cellular Automata (e.g Conway’s Game of Life)

- Deterministic grid-based models used to simulate complex systems using simple local rules.
- **Cellular Automaton (CA)**: A discrete model made up of a regular grid of cells, each in a finite state (e.g., alive/dead or 0/1). The state of each cell evolves based on a fixed rule depending on the states of neighboring cells.
- Neighborhood
    - Moore : 8 neighbours
    - Von Neuman : 4 neighbours (no diagonal)

**Conway’s Game of Life**

A famous 2D cellular automaton invented by John Conway

**Rules**

Each cell is either alive (1) or dead(0) and evolves per these rules

- **Underpopulation**: Any live cell with fewer than 2 live neighbors dies.
- **Survival**: Any live cell with 2 or 3 live neighbors lives on.
- **Overpopulation**: Any live cell with more than 3 live neighbors dies.
- **Reproduction**: Any dead cell with exactly 3 live neighbors becomes alive.

````python
import os
import time

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def game_of_life(board):
    rows, cols = len(board), len(board[0])
    
    def count_live_neighbors(r, c):
        directions = [(-1, -1), (-1, 0), (-1, 1), 
                      (0, -1),         (0, 1), 
                      (1, -1), (1, 0), (1, 1)]
        count = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and abs(board[nr][nc]) == 1:
                count += 1
        return count

    # Update in place with markers
    for r in range(rows):
        for c in range(cols):
            live_neighbors = count_live_neighbors(r, c)
            if board[r][c] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                board[r][c] = -1  # alive -> dead
            elif board[r][c] == 0 and live_neighbors == 3:
                board[r][c] = 2   # dead -> alive

    # Final state update
    for r in range(rows):
        for c in range(cols):
            board[r][c] = 1 if board[r][c] > 0 else 0

    return board

start = [
    [0, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 1, 0, 1]
]

for i in range(10):
    clear_console()
    print(f"Generation {i+1}")
    start = game_of_life(start)
    for row in start:
        print(" ".join(map(str, row)))
    time.sleep(2)
````

- Resources : John Conway Interview : [Link](https://www.youtube.com/watch?v=xOCe5HUObD4)

## Random Walks & Probabilistic Modelling

- A **random walk** is a process where an object randomly moves in space (line, grid, graph), often used to model physical or stochastic processes like diffusion, stock prices, or Brownian motion.
- Each step is chosen **randomly** from allowed directions.
- Can be 1D, 2D, or nD.
- Often studied for **expected behavior**, like return-to-origin probability or average distance from start.

**Examples** 

- **1D Random Walk**: Step left or right with equal probability.
- **2D Grid**: Move in 4/8 directions randomly.
- **Markov Chains**: Use transition matrices to describe probabilistic state changes.

**Applications**

- Modeling population movement, chemical diffusion
- Estimating mathematical constants (e.g. Pi)
- Physics (Brownian motion)
- PageRank Algorithm
- Monte Carlo simulations

````python
# Estimate average distance after n steps of a 2D walk.
import random
def random_walk_2D(n):
    x = y = 0
    for _ in range(n):
        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        x += dx
        y += dy
    return (x**2 + y**2) ** 0.5
````

## Monte-Carlo Simulations

- Estimates value using randomness (statistical sampling)
- Use-Cases
    - Pi-estimation using random point in square/circle
    - Probabilistic integral approximation
- Usually steps involved are:
    - Simulate random input based on some distribution
    - Count/Measure successful outcomes
    - Estimate with `success/ total trials`
- Pi-Estimation Using Monte Carlo Method
- The idea is to randomly generate points inside a unit square and count how many fall inside the quarter circle of radius 1. The ratio approximates π/4.

````python
import random

def estimate_pi(num_samples=1_000_000):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x * x + y * y <= 1:
            inside_circle += 1

    return (inside_circle / num_samples) * 4

# Example usage
print("Estimated π:", estimate_pi())
````

- Probabilistic integral approximation
- Estimate definite integrals by sampling random points in the domain.

$$
\int^b_a f(x) dx \sim (b-a).\frac{1}{N} \Sigma^{N}_{i=1} f(x_i)
$$



````python
import random
import math

# Function to integrate
def f(x):
    return math.sin(x)  # ∫₀^π sin(x) dx = 2

def monte_carlo_integral(f, a, b, num_samples=100000):
    total = 0
    for _ in range(num_samples):
        x = random.uniform(a, b)
        total += f(x)
    return (b - a) * (total / num_samples)

# Example usage
result = monte_carlo_integral(f, 0, math.pi)
print("Estimated ∫ sin(x) dx from 0 to π:", result)
````

## Las Vegas Algorithms

- These are dual to Monte-Carlo Simulation
- Las Vegas Algorithm
    - Always give correct answer
    - Runtime is probabilistic
- Examples
    - Randomized Quicksort : Uses randomness to select pivot (Las Vegas — correctness guaranteed)
    - Perfect Hashing : Repeatedly tries seeds to find a collision-free assignment of keys.
- Randomized Quicksort : we randomly choose the pivot each time — the correctness is guaranteed, but performance depends on the pivot quality.

````python
import random

def randomized_quicksort(arr):
    if len(arr) <= 1:
        return arr

    # Las Vegas: randomly choose a pivot
    pivot_index = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_index]

    # Partitioning
    less = [x for i, x in enumerate(arr) if x < pivot and i != pivot_index]
    equal = [x for x in arr if x == pivot]
    greater = [x for i, x in enumerate(arr) if x > pivot and i != pivot_index]

    return randomized_quicksort(less) + equal + randomized_quicksort(greater)

# Example usage
arr = [7, 2, 1, 6, 8, 5, 3, 4]
sorted_arr = randomized_quicksort(arr)
print("Sorted:", sorted_arr)
````

## Random Sampling Algorithm

### Reservoir Sampling

- Randomly pick `k` items from a stream of unknown size
- Time : $O(n)$, Space : $O(k)$
- Formula: Replace element with $i-th$ element with probability $k/i$

````python
import random

def reservoir_sampling(stream, k):
    res = stream[:k]
    for i in range(k, len(stream)):
        j = random.randint(0, i)
        if j < k:
            res[j] = stream[i]
    return res
````

## Randomized Algorithms

- Use randomness to achieve simplicity or performance
- Can be faster or memory efficient
- Las-Vegas & Monte Carlo are two broad types

### Randomized Quicksort/Quickselect

**QuickSort**:

- Pick pivot randomly → reduces chance of worst case

**QuickSelect**:

- Find k-th smallest element with expected O(n) time

### Treaps (Randomized BST)

- Combines BST + Heap
- Each node has a key and random priority
- Maintains BST by key and Heap by priority

**Advantages**:

- Balanced with high probability
- Easy to implement split/merge operations

### Randomized Hashing

- Add randomness to hash functions to reduce collision
- E.g., Polynomial Rolling Hash with random base/mod

**Use Case**:

- Hashing strings in rolling hashes
- Prevent collision attacks in contests

## Hashing & Randomization for Collision Detection

Use **hash functions** (with randomness) to detect collisions efficiently in large datasets or data streams. Randomization helps reduce the chance of adversarial inputs causing worst-case behavior.

### Use Cases

- **Plagiarism detection**: Hash substrings (e.g., Rabin-Karp)
- **Data integrity**: Quick comparison via hashes
- **Hash tables**: Reduce collisions by randomizing the hash function
- **Bloom Filters**: Probabilistic set membership with hash functions

### Randomization

- Randomly select hash seeds or mod values.
- Use **universal hashing**: ensures low collision probability even with bad input.

### Techniques

- Rabin-Karp substring matching
- Zobrist hashing (used in game states)
- Randomly seeded polynomial hashing

````python
# Rabin-Karp
def rabin_karp(text, pattern, base=256, mod=10**9+7):
    n, m = len(text), len(pattern)
    pat_hash = 0
    txt_hash = 0
    h = 1

    for i in range(m-1):
        h = (h * base) % mod

    for i in range(m):
        pat_hash = (base * pat_hash + ord(pattern[i])) % mod
        txt_hash = (base * txt_hash + ord(text[i])) % mod

    for i in range(n - m + 1):
        if pat_hash == txt_hash and text[i:i+m] == pattern:
            return i  # match found
        if i < n - m:
            txt_hash = (base * (txt_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            txt_hash = (txt_hash + mod) % mod  # handle negative values
    return -1
````

## Probabilistic Primality Testing (Miller-Rabin)

Determining whether a number is **prime**, especially large numbers, in an efficient and probabilistic way.

- A **Monte Carlo algorithm**: May give false positives, but with low probability.
- Much faster than deterministic primality tests.
- Based on Fermat’s little theorem.

Concept

* For an odd number n > 2 write : ` n - 1 = 2^s *d`
* Then randomly choose bases `a` and check : `a^d % n == 1 or a^{2^r * d} % n == n-1 for some r in [0, s-1]`. If this fails for any `a`, `n` is composite. If it passes for all `a`, **it’s probably prime**

````python
import random

def is_probably_prime(n, k=5):
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

    # Write n-1 = 2^s * d
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite
    return True  # Probably Prime
````

## State Compression in Simulation

Idea: Encode complex states (grid, position, moves left, etc) into integers or bitmasks

Why ? Reduces memory and improves cache usages

Examples

- `3x3` board can be represented in 9 bits
- Compress states as (x, y, moves_left) into a tuple/int