# 20. Concurrent Executors

- 99% of use cases application programmer is likely to run into, the following pattern
- chapter focuses on the `concurrent.futures.Executor` classes that encapsulate the pattern of *spawning a bunch of independent threads and collecting results in a queue*
- mostly systems programmer utilize other features of python quite heavily

## Concurrent Web Downloads

- concurrency is essential for efficient network I/O: instead of waiting of response application should work on something else.
- Following codes fetches 20 country flags from web. There are 4 version of it, Sequential being slowest wihle other concurrent implementation being faster.

### A Sequential Download Script

````python
import time
from pathlib import Path
from typing import Callable

import httpx # not part of standard library/actually its convention to leave one blank line

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split() # List of ISO 3166 country codes

BASE_URL = 'https://www.fluentpython.com/data/flags' # dir with flag img
DEST_DIR = Path('downloaded')                        # local dir

def save_flag(img: bytes, filename: str) -> None: # save img, bytes to file
    (DEST_DIR / filename).write_bytes(img)

def get_flag(cc: str) -> bytes: # return binary contents
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1, # for network calls always add timeout
                     follow_redirects=True) # by default doesn't follow redirectly
    resp.raise_for_status() # there is no error handling but this method raises exception
    return resp.content

def download_many(cc_list: list[str]) -> int: # this will be used for comparisons
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image, f'{cc}.gif')
        print(cc, end=' ', flush=True) # display one country code at a time
    return len(cc_list)

def main(downloader: Callable[[list[str]], int]) -> None: # main called with downloading fn
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many) # call many with download function
````

### Downloading with concurrent.futures

- Main feature of `concurrent.futures` packages are `ThreadPoolExecutor` and `ProcessPoolExecutor` classes which implement an API to submit callables for execution in different threads or processes, respectively.

````python
from concurrent import futures

from flags import save_flag, get_flag, main # reuse old functions

def download_one(cc: str): # this is what each worker will execute
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor: # context manage ThreadPoolExecutor
        res = executor.map(download_one, sorted(cc_list)) # map method is similar to built-in map, returns a generator that we can iterate to retrieve the value returned by each function call.

    return len(list(res))
    # Return the number of results obtained. If any of the threaded calls raises an exception, that exception is raised here when the implicit next() call inside the list constructor tries to retrieve the corresponding return value from the iterator returned by executor.map.
    
if __name__ == '__main__':
    main(download_many) # return number of results obtained.
````

- the computed default for `max_workers` is sensible, and `ThreadPoolExecutor` avoids starting new workers unnecessarily. Understanding the logic behind `max_workers` may help you decide when and how to set it yourself.

### Where are the Futures ?

- there are two classed name `Future` in standard library : `concurrent.futures.Future` and `asyncio.Future`. They server same purpose : an instance of either `Future` class represents a deferred computaion that may or may not have completed.
- Futures encapsulate pending operation so that we can put them in queues, check whether they are done and retrieve results (exception) when they become available.
- We should not create futures: they are meant to created by concurrency framework. a `Future` represent something that will run eventually, therefore it must be schedules to run, and that the job of framework.
- Application code is not supposed to change the state of a future: the concurrency framework changes the state of a future when the computation it represents is done, and we can’t control when that happens.
- Both types of `Future` have a `.done()` method that is nonblocking and returns a Boolean that tells you whether the callable wrapped by that future has executed or not. However, instead of repeatedly asking whether a future is done, client code usually asks to be notified. That’s why both `Future` classes have an `.add_done_callback()` method: you give it a callable, and the callable will be invoked with the future as the single argument when the future is done. Be aware that the callback callable will run in the same worker thread or process that ran the function wrapped in the future.
- There is also a `.result()` method, which works the same in both classes when the future is done: it returns the result of the callable, or re-raises whatever exception might have been thrown when the callable was executed.
- However, when the future is not done, the behavior of the `result` method is very different between the two flavors of `Future`. In a `concurrency.futures.Future` instance, invoking `f.result()` will block the caller’s thread until the result is ready. An optional `timeout` argument can be passed, and if the future is not done in the specified time, the `result` method raises `TimeoutError`. The `asyncio.Future.result` method does not support timeout, and `await` is the preferred way to get the result of futures in `asyncio`—but `await` doesn’t work with `concurrency.futures.Future` instances.

````python
def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5] # take only 5 entries
    with futures.ThreadPoolExecutor(max_workers=3) as executor: # max worker to 3 so see future pending in the otuput
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):	# call in order, result will not be in order
            future = executor.submit(download_one, cc) # submit the callable
            to_do.append(future) # add that future to list
            print(f'Scheduled for {cc}: {future}')

        for count, future in enumerate(futures.as_completed(to_do), 1): # as_completed yields futures as they are completed
            res: str = future.result()
            print(f'{future} result: {res!r}')

    return count
````

## Launching Processes with concurrent.futures

- `concurrent.futures` supportes parallel computation on multicore machines because it supports distributing work among multiple python processes using `ProcessPoolExecutor`.
- In our program there is no advantage of a process pool executor or any I/O bound job. We will get same performance.
- Its useful for CPU-Intensive jobs

### Multicore Prime Checker Redux

````python
import sys
from concurrent import futures
from time import perf_counter
from typing import NamedTuple

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple):
    n: int
    flag: bool
    elapsed: float

def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def main() -> None:
    if len(sys.argv) < 2:
        workers = None
    else:
        workers = int(sys.argv[1])

    executor = futures.ProcessPoolExecutor(workers)
    actual_workers = executor._max_workers  # type: ignore # undocumented instance attribute of Process pool executor taken to show max_workers, disable typehints using that comment

    print(f'Checking {len(NUMBERS)} numbers with {actual_workers} processes:')

    t0 = perf_counter()

    numbers = sorted(NUMBERS, reverse=True) # sort the numbers to expose difference in behaviour of this code as compared to previous
    with executor:
        for n, prime, elapsed in executor.map(check, numbers):
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')

    time = perf_counter() - t0
    print(f'Total time: {time:.2f}s')

if __name__ == '__main__':
    main()
````

- you’ll see the results appearing in strict descending order. In contrast, the ordering of the output of procs.py (shown in “Process-Based Solution”) is heavily influenced by the difficulty in checking whether each number is a prime.
- `executor.map(check, numbers)` always returns the results in same order as the numbers are given.

## Experimenting with Executor.map

````python
from time import sleep, strftime
from concurrent import futures

def display(*args):# simply print whatever given
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)

def loiter(n): # does nothing except disaply message when it starts
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10 # return so we can see how to collect results

def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)	# only 3 threads
    results = executor.map(loiter, range(5))	# submit 5 taks o executor
    display('results:', results) # immidiatedly shows 3 outputs
    display('Waiting for individual results:')
    for i, result in enumerate(results):
    # The enumerate call in the for loop will implicitly invoke next(results), which in turn will invoke _f.result() on the (internal) _f future representing the first call, loiter(0). The result method will block until the future is done, therefore each iteration in this loop will have to wait for the next result to be ready.
        display(f'result {i}: {result}')

if __name__ == '__main__':
    main()
````

- The `Executor.map` function is easy to use, but often it’s preferable to get the results as they are ready, regardless of the order they were submitted. To do that, we need a combination of the `Executor.submit` method and the `futures.as_completed` function
- The combination of `executor.submit` and `futures.as_completed` is more flexible than `executor.map` because you can `submit`  different callables and arguments, while `executor.map` is designed to run the same callable on the different arguments. In addition,  the set of futures you pass to `futures.as_completed` may come from more than one executor—perhaps some were created by  a `ThreadPoolExecutor` instance, while others are from a  `ProcessPoolExecutor`.

## Downloads with Progress Display and Error Handling

We will implement version of `flags2.py` with animated, text-mode progress bar implemented with tqdm packages.

````python
from collections import Counter
from http import HTTPStatus

import httpx
import tqdm  # type: ignore  1

from flags2_common import main, save_flag, DownloadStatus # import already implemented stuff

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

def get_flag(base_url: str, cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()  # HTTPStatusError, if HTTP code not in range(200,300)
    return resp.content

def download_one(cc: str, base_url: str, verbose: bool = False) -> DownloadStatus:
    try:
        image = get_flag(base_url, cc)
    except httpx.HTTPStatusError as exc: # handle 404 correctly
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND # by setting its local status to DownloadStatus.NOT_FOUND; DownloadStatus is an Enum imported from flags2_common.py.
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        save_flag(image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'OK'

    if verbose:
        print(cc, msg)

    return status
````



### Sequential Implementation

````python
def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  _unused_concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter() # tally different download outcomes
    cc_iter = sorted(cc_list) # list of country codes as args
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter) # if no in -v mode, cc_iter is passed to tqdm, which returns an iterator yielding the items in cc_iter
    for cc in cc_iter:
        try:
            status = download_one(cc, base_url, verbose) # call to download one
        except httpx.HTTPStatusError as exc:
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg = error_msg.format(resp=exc.response)
        except httpx.RequestError as exc:
            error_msg = f'{exc} {type(exc)}'.strip()
        except KeyboardInterrupt:
            break
        else:
            error_msg = ''

        if error_msg:
            status = DownloadStatus.ERROR
        counter[status] += 1
        if verbose and error_msg:
            print(f'{cc} error: {error_msg}')

    return counter
````

### Futures.as_completed

````python
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30 # default concurrent req
MAX_CONCUR_REQ = 1000 # max concurrent req


def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    with ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do_map = {}
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc,
                                     base_url, verbose)
            to_do_map[future] = cc
        done_iter = as_completed(to_do_map)
        if not verbose:
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))
        for future in done_iter:
            try:
                status = future.result()
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
            except KeyboardInterrupt:
                break
            else:
                error_msg = ''

            if error_msg:
                status = DownloadStatus.ERROR
            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future]
                print(f'{cc} error: {error_msg}')
    return counter

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
````

