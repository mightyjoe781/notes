---
title: Concurrency & Multi-Threading Concepts
description: Python threading primitives - locks, semaphores, conditions, events, barriers, and thread/process pool executors - with classic synchronization problems solved.
tags:
  - reference
---

# Concurrency & Multi-Threading Concepts

## Python Concepts

- `threading.Thread` ~ OS-level thread wrapper
- `GIL` ~ Global Interpreter Lock
    - Only one thread runs Python byte-code at a time.
    - Still needs locks ~ Gil doesn't protect your own shared data invariants
    - Threads are useful for I/O bound tasks (CPU bound tasks should generally use *multi-processing* )

### Lock & RLock

- `threading.Lock`
    - Binary Mutex : `.acquire()` or `.release()`
    - Non-reentrant: If the same thread acquires twice -> deadlock

```python
import threading

lock = threading.Lock()
counter = 0

def worker():
    global counter
    for _ in range(100000):
        with lock:  # similar to lock.acquire()
            counter += 1
```

- If we call `.release()` without acquiring the lock : *RuntimeError*
- What if we forget finally: `lock.release()` ? Lock may never get released and threads hang forever.

`threading.RLock`

- Reentrant Lock : same thread can be acquired multiple times, (must release same number of times).
- Use in recursive code or when a function holding a lock calls another that also uses the same lock

```python
rlock = threading.RLock()

def f():
    with rlock:
        g()

def g():
    with rlock:
        ...

```

### Semaphore/Bounded Semaphore

`threading.Semaphore`

- Counting lock : allows up to n concurrent acquisitions
- Typical use : limit concurrency, resource pools.

```python
import threading, time

sem = threading.Semaphore(3)

def worker(i):
    with sem:
        print(f"worker {i} in")
        time.sleep(1)
        print(f"worker {i} out")

```


`threading.BoundedSemaphore`

- Like Semaphore, but checks that `.release()` is not called more than `.acquire()`

### Condition, Event, Barrier

`threading.Condition`

- Combines a lock + wait/notify
- Pattern : shared state + condition variable used to signal *state changed*

```python

cond = threading.Condition()
items = []

def producer():
    with cond:
        items.append(1)
        cond.notify() # wake one waiting consumer
        
def consumer():
    with cond:
        while not items: # Always while, not if -> spurious wakeups
            cond.wait()
        items.pop()
```

- NOTE: always use while around `wait()` to re-check the condition

`threading.Event`

- One-bit flag with `set()`, `clear()`, `is_set()`, `wait()`
- great for `start/stop` , or `ready` signals

```python

start_event = threading.Event()

def worker():
    print("waiting ...")
    start_event.wait()
    print("go!")
    
# later
start_event.set()

```

`threading.Barrier`

- N threads call barrier.wait(); all block until `N` have arrived, then all continue.
- Used to sync phases.

```python

barrier = threading.Barrier(3)

def worker():
    print("before barrier")
    barrier.wait()
    print("after barrier")
```

### Solution to classic problems

#### Rendezvous/Turnstile Problem

Goal : Two threads, A & B each must reach a point before either proceeds.
Idea : Each thread signals its arrival and waits for other. Simplest solution is using two semaphores

```python

import threading

a_arrived = threading.Semaphore(0)
b_arrived = threading.Semaphore(0)

def a():
    # phase 1
    print("A: before rendezvous")
    a_arrived.release() # signal A is here
    b_arrived.wait() # wait for B
    # phase 2
    print("A: after rendezvous")

def b():
    # phase 1
    print("B: before rendezvous")
    b_arrived.release() # signal B is here
    a_arrived.wait() # wait for A
    # phase 2
    print("B: after rendezvous")

threading.Thread(target=a).start()
threading.Thread(target=b).start()

```

#### Alternate Printing Odd/Even Numbers

Goal : Two threads, one prints odd, one prints even, in order 1 2 3 4 ...

```python
import threading
cond = threading.Condition()
n = 10
turn = "odd" # shared state

def print_odd():
    global turn
    for i in range(1, n+1, 2):
        with cond:
            while turn != "odd":
                cond.wait()
            print(i)
            turn = "even"
            cond.notify()
            
def print_even():
    global turn
    for i in range(2, n+1, 2):
        with cond:
            while turn != "even":
                cond.wait()
            print(i)
            turn = "odd"
            cond.notify()
            
t1 = threading.Thread(target=print_odd)
t2 = threading.Thread(target=print_even)

t1.start()
t2.start()

t1.join()
t2.join()

```

#### Producer/Consumer (Bounded Buffer)

**Goal:** Multiple producers/consumers share buffer; no overruns/underruns.
**Python-idiomatic solution:** use queue.Queue which is already thread-safe and uses locks/conditions internally.

```python
import threading, queue, time

q = queue.Queue(maxsize=5)

def producer():
    for i in range(10):
        q.put(i)                 # blocks if full
        print("produced", i)

def consumer():
    while True:
        item = q.get()           # blocks if empty
        if item is None: # graceful shutdown
            break
        print("consumed", item)
        q.task_done()

threading.Thread(target=producer).start()
threading.Thread(target=consumer, daemon=True).start()
```

- NOTE: `daemon=True` -> thread runs in background; if the main program exits, daemon threads are killed immediately (no cleanup).
- Non-daemon thread (default) -> Python waits for it to finish before the program can exit.

#### One-time Initialization (call once)

Goal: Only one thread should execute initialization code; others wait or skip.

```python
init_lock = threading.Lock()
initialized = False

def init():
    global initialized
    with init_lock:
        if not initialized:
            # heavy setup here
            initialized = True
```

Improved version is useful for singleton classes, to avoid allowing multiple creators to acquire lock.

```python
init_lock = threading.Lock()
initialized = False

def init():
    global initialized
    if initialized:
        return

    with init_lock:
        if not initialized:
            print("Heavy initialization")
            initialized = True
```

#### Avoiding Deadlock with Multiple Locks

Classic Trap : Two locks acquired in different orders -> deadlock

```python
lock_a = threading.Lock()
lock_b = threading.Lock()

# BAD
def t1():
    with lock_a:
        with lock_b:
            ...

def t2():
    with lock_b:
        with lock_a:  # can deadlock with t1
            ...
```

Fix : enforce a global lock ordering.

```python
def t1():
    first, second = sorted((lock_a, lock_b), key=id)
    with first:
        with second:
            ...
```

```python

def acquire_locks(*locks):
    for lock in sorted(locks, key=id):
        lock.acquire()

def release_locks(*locks):
    for lock in sorted(locks, key=id, reverse=True):
        lock.release()
        
```

NOTE: "How do you avoid deadlocks when you must hold multiple locks?” -> fixed order, timeouts, lock hierarchy.

### ThreadPool Executor

- From `concurrent.futures`
- Manages a pool of worker threads.
- Best for I/O-bound tasks, many small tasks.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch(url):
    ...

urls = [...]
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch, u) for u in urls]
    for fut in as_completed(futures):
        try:
            result = fut.result()
            print(result)
        except Exception as e:
            print("Task failed:", e)
```

- `max_workers`
    - Too low -> underutilization.
    - Too high -> context-switch overhead, possible resource problems.
- Difference:
    - `submit(fn, *args)` -> returns a single `Future`; combine with `as_completed()` to process results as they finish.
    - `map(fn, iter)` -> returns an iterator of results in **input order** (not completion order); blocks on the slowest-so-far result.
- Exceptions in task:
    - Raised when you call `future.result()` (for `submit`) or while iterating the results (for `map`)

```python
with ThreadPoolExecutor(max_workers=10) as executor:
    for result in executor.map(fetch, urls):  # blocks until each result is ready, in order
        print(result)
```

### ProcessPoolExecutor

- From `concurrent.futures`, same interface as `ThreadPoolExecutor` (`submit`, `map`, `as_completed`)
- Manages a pool of worker **processes** -> sidesteps the GIL
- Best for CPU-bound tasks (number crunching, image/data processing)
- Args/return values are pickled to move across process boundaries -> avoid large/unpicklable objects

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor(max_workers=4) as executor:
    for result in executor.map(cpu_heavy, [10**6, 10**6, 10**6]):
        print(result)
```

- `max_workers` defaults to number of CPU cores (`os.cpu_count()`)
- Higher overhead than threads (process startup, IPC/pickling) -> not worth it for small/short tasks

