---
title: Asynchronous Programming
description: Explains Python's asyncio model - event loop, coroutines, tasks, and sync primitives - and contrasts it with goroutines and threads.
tags:
  - concept
---

# Asynchronous Programming

## Why do we need it?

- Synchronous code is a straight line: each step blocks until the previous one finishes.
- Most "waiting" (network call, disk read, DB query) doesn't use the CPU - the thread just sits idle until the OS/IO-controller wakes it up.
- In a single-threaded program, that idle thread blocks *everything else* too (e.g. a UI thread can't repaint a button while waiting on a request).
- Multi-threading "solves" this by giving the OS more threads to schedule, but threads share process memory -> need locks/mutexes -> race conditions, deadlocks, hard to get right ("multi-threading is evil" - many experienced devs avoid it, e.g. SQLite).
- Async IO is a middle ground: **single thread, non-blocking IO**. When a task starts an IO operation, it hands control back to an event loop ("here's a callback, call me when you're done") and the thread moves on to other work instead of sitting idle.
- NOTE: async doesn't make a single task faster - it improves *throughput/responsiveness* by keeping the CPU busy with other tasks while one is waiting.

## When to use what

- **Async IO** -> many tasks that *wait a lot* (network requests, file IO). Cheap concurrency, low CPU usage.
- **Threads** -> IO-bound tasks that also need to *share data* / run in parallel within the same app.
- **Processes** -> CPU-bound / heavy-compute tasks. Each process has its own memory, runs on its own core, communicate via IPC (sockets, Redis, queues). e.g. brute-forcing a hash: split the search space across processes, each runs independently.

## Event Loop

- Core of `asyncio` - a central hub that schedules and runs tasks.
- Each task runs until it hits an `await` on something it doesn't control (network, sleep, etc), then steps aside so another task can run.
- Once the awaited operation completes, the task resumes. The loop keeps the thread always doing *something* useful.

```python
import asyncio

async def main():
    print("start")

asyncio.run(main())   # creates event loop, runs `main`, closes loop
```

## Coroutines & `await`

- `async def f(): ...` defines a **coroutine function**. Calling it (`f()`) doesn't run the body - it returns a **coroutine object**.
- A coroutine object only starts executing once it's **awaited** (or wrapped in a Task).
- `await` can only be used inside a coroutine (or async context).

```python
async def fetch_data():
    print("fetching...")
    await asyncio.sleep(2)   # simulate IO wait
    print("fetched")
    return {"data": 1}

async def main():
    result = await fetch_data()   # blocks here until fetch_data finishes
    print(result)

asyncio.run(main())
```

- NOTE: `await`ing coroutines back-to-back is still **sequential** - `await a(); await b()` runs `b` only after `a` fully finishes. No concurrency gain by itself; that's what Tasks are for.

## Tasks

- A **Task** schedules a coroutine to start running ASAP and lets multiple coroutines run concurrently.
- As soon as one task hits an `await` (idle/blocked), the loop switches to another ready task. (Concurrency, not parallelism - one thread, no extra CPU cores.)

```python
async def main():
    t1 = asyncio.create_task(fetch_data(1, delay=2))
    t2 = asyncio.create_task(fetch_data(2, delay=3))
    t3 = asyncio.create_task(fetch_data(3, delay=1))

    results = [await t1, await t2, await t3]   # total ~3s, not 2+3+1=6s
```

- **`asyncio.gather(*coros)`** -> shortcut to schedule + run multiple coroutines concurrently and collect results in input order.
    - Weak error handling: if one fails, the others are *not* automatically cancelled.
- **`asyncio.TaskGroup`** (3.11+) -> preferred way to group tasks; if any task fails, the rest are cancelled automatically (structured concurrency, cleaner error handling).

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch_data(1))
        t2 = tg.create_task(fetch_data(2))
    # both tasks are guaranteed done here
    print(t1.result(), t2.result())
```

## Future

- A **Future** is a low-level "promise of a result that will arrive eventually" - you typically don't create these yourself; libraries (and Tasks, internally) use them.
- Awaiting a future just waits for *a value* to be set, not for an entire coroutine/task to finish.

## Synchronization Primitives (`asyncio` versions)

Same ideas as `threading`, but designed to cooperate with the event loop (`async with`, non-blocking).

- **`asyncio.Lock`** -> only one coroutine can enter the critical section at a time.
```python
lock = asyncio.Lock()

async def modify():
    async with lock:
        ...   # only one coroutine here at a time
```
- **`asyncio.Semaphore(n)`** -> up to `n` coroutines can access a resource concurrently. Used to throttle (e.g. max 5 concurrent outbound requests).
- **`asyncio.Event`** -> simple boolean flag; coroutines can `await event.wait()` until something calls `event.set()`.
- `asyncio.Condition` also exists (lock + wait/notify), same pattern as `threading.Condition`.

## Goroutines vs Python's `asyncio`

Both give you cheap, massively-concurrent "lightweight tasks" on top of a small number of OS threads, but the model is quite different:

- **Scheduling: cooperative vs preemptive**
    - `asyncio` coroutines are *cooperatively* scheduled - a coroutine only yields control at an explicit `await`. Forget the `await` (or call a blocking function) and you stall the entire event loop.
    - Goroutines are scheduled by the **Go runtime** (M:N scheduler - many goroutines over few OS threads) and can be preempted automatically, even mid-computation. You don't need to mark "yield points" - the runtime handles it.
- **Parallelism**
    - `asyncio` is single-threaded by default - coroutines run *concurrently*, never *in parallel* (GIL also prevents true thread parallelism for CPU-bound Python code).
    - Goroutines run on Go's scheduler which spreads them across `GOMAXPROCS` OS threads -> genuine parallel execution across cores, no GIL.
- **Function coloring**
    - Python distinguishes `async def` vs `def` - async code is "contagious" (an async function can only be awaited from another async function); mixing requires bridges like `run_in_threadpool` / `asyncio.to_thread`.
    - Go has no such split - any function can be run as a goroutine with `go f()`. No separate async/sync universe ("no function coloring").
- **Communication / synchronization**
    - Python: shared memory + locks/semaphores/events (same primitives as threads, just `async`-aware versions).
    - Go: idiomatic style favours **channels** ("don't communicate by sharing memory; share memory by communicating"), though `sync.Mutex` etc. are still available.
- **Cost**: both are cheap compared to OS threads/processes - goroutines start around a few KB of stack (grows dynamically); coroutines are just objects scheduled on the loop, even lighter, but capped to one core's worth of work.

NOTE (interview angle): the headline difference is *cooperative single-threaded concurrency with explicit `await` points* (Python) vs *runtime-managed M:N scheduling with real parallelism and no special syntax* (Go).

## How this plugs into Starlette / FastAPI

- Both run on top of `asyncio` (via an ASGI server like `uvicorn`), which owns **one event loop per worker**.
- `async def` endpoint -> runs directly as a coroutine on the event loop. Any blocking call inside it (without `await`) blocks the *entire* loop -> blocks all other requests on that worker.
- `def` (sync) endpoint -> Starlette automatically runs it in a **thread pool executor** (`run_in_threadpool`, backed by `anyio`'s worker threads) so it doesn't block the event loop. This is why plain blocking code (e.g. sync DB drivers) is "safe" in a sync route but dangerous in an async one.
- Dependencies, middleware, background tasks all follow the same rule: sync callables get offloaded to a thread pool, async callables run on the loop directly.
- NOTE (interview angle): "Why is FastAPI fast?" -> async-first design lets a single worker handle many concurrent IO-bound requests without spawning a thread per request; CPU-bound work should still go to a process pool / background worker (Celery, etc), not the event loop.
