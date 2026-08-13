# Concurrency and Parallelism in Python: async, multithreading, multiprocessing, subprocess

Python offers several ways to handle concurrency and parallelism, each suited to specific use cases. This document explains how each approach works, its ideal use cases, and its limitations.

## 1. `async` (asyncio) — cooperative concurrency

`asyncio` allows code to run **concurrently** (but not in parallel) on a **single thread**. The principle relies on an event loop that manages multiple tasks (`coroutines`) by switching between them. When a task hits a blocking operation (like a network request), it "yields control" (`await`) back to the event loop, which can then run another task while the first one waits. This is **cooperative** concurrency: the code must explicitly yield control with `await`, unlike threading where the operating system can interrupt a thread at any time. There is **no real parallelism** here: a single thread, a single CPU core used, but excellent efficiency for handling thousands of simultaneous waiting tasks with very little overhead (no thread or process creation).

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = ["https://example.com"] * 5
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results

asyncio.run(main())
```

**When to use it**: ideal for **I/O bound** tasks with a very large number of concurrent operations (web servers, HTTP clients, websockets, async databases). Requires the libraries used to be `async`-compatible (e.g., `aiohttp`, `asyncpg`), otherwise you lose all the benefit.

---

## 2. `threading` (multithreading) — multiple threads, one process

Multithreading creates multiple threads within a **single process**, sharing the same memory. In theory, these threads could run in parallel across multiple CPU cores. But in Python (in the standard CPython implementation), the **GIL** (*Global Interpreter Lock*) prevents multiple threads from executing Python bytecode **at the same time**. Only one thread can hold the GIL at any given moment. However, the GIL is **automatically released** during I/O operations (file reading, network requests, etc.), which allows other threads to run during that time. Threading is therefore useful for waiting, but provides no gain for pure computation.

```python
import threading
import requests

def fetch(url, results, index):
    response = requests.get(url)
    results[index] = response.status_code

urls = ["https://example.com"] * 5
results = [None] * len(urls)
threads = []

for i, url in enumerate(urls):
    t = threading.Thread(target=fetch, args=(url, results, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(results)
```

**When to use it**: good for **I/O bound** tasks when working with **blocking** (non-async) libraries, like `requests`. Less efficient than `asyncio` for thousands of simultaneous tasks (each thread has a memory and context-switching cost), but simpler to integrate into existing synchronous code. **Useless or even counterproductive for CPU bound** work because of the GIL.

---

## 3. `multiprocessing` — multiple processes, true parallelism

The `multiprocessing` module creates **actual separate processes**, each with its own Python interpreter and its own memory space. Since each process has its own GIL, they can **truly run in parallel** across multiple CPU cores. This is the only native way in Python to work around the GIL limitation. The trade-off: processes don't share memory, so exchanging data between them requires serialization (`pickle`) via mechanisms like `Queue`, `Pipe`, or shared memory, which adds overhead. Starting a process is also more expensive than starting a thread.

```python
from multiprocessing import Pool
import math

def heavy_computation(n):
    return sum(math.sqrt(i) for i in range(n))

if __name__ == "__main__":
    values = [10_000_000] * 4
    with Pool(processes=4) as pool:
        results = pool.map(heavy_computation, values)
    print(results)
```

**When to use it**: ideal for **CPU bound** tasks (scientific computing, image processing, compression, machine learning) that you want to spread across multiple cores to fully leverage the hardware. Avoid for lightweight or very numerous tasks due to the cost of process creation and data serialization.

---

## 4. `subprocess` — launching external programs

`subprocess` isn't about concurrency within your own Python program, but rather about **launching and controlling other programs** (executables, shell scripts, other languages) from Python, as independent child processes. Unlike `multiprocessing`, which launches other Python instances running Python code, `subprocess` can run **any program** on the system (`ls`, `ffmpeg`, a bash script, a compiled C binary, etc.). You can capture its standard output, send it input, check its return code, and either wait for it to finish or let it run in the background.

```python
import subprocess

result = subprocess.run(
    ["ffmpeg", "-i", "video.mp4", "-vn", "audio.mp3"],
    capture_output=True,
    text=True
)

print(result.stdout)
print("Return code:", result.returncode)
```

**When to use it**: whenever you need to interact with an **external, non-Python program** (system tools, specialized binaries, shell scripts, other runtimes like Node.js). It's not a tool for parallelizing your Python logic, but a tool for **system integration**.

---

## Summary: what's the difference between the four?

| Approach | Mechanism | Real parallelism? | Ideal use case |
|---|---|---|---|
| **asyncio** | Single thread, cooperative coroutines | No | I/O bound, very many concurrent tasks (network, APIs) |
| **threading** | Multiple threads, one process, limited by the GIL | No (except during I/O) | I/O bound with blocking (non-async) libraries |
| **multiprocessing** | Multiple independent processes | Yes | CPU bound, heavy computations spread across cores |
| **subprocess** | Launching external programs | Yes (separate process) | Running a non-Python program from your script |

In short, ask yourself two questions:
1. **Does the Python code I'm writing wait (I/O) or compute (CPU)?**
   - I/O bound → `asyncio` (if the libraries support it) or `threading` (otherwise).
   - CPU bound → `multiprocessing`.
2. **Do I need to run my own Python code in parallel, or an external program?**
   - Python code → `multiprocessing` / `threading` / `asyncio`.
   - External program → `subprocess`.

`asyncio` and `threading` solve the same type of problem (I/O bound) with different philosophies (cooperative vs. preemptive), while `multiprocessing` is the only option for true CPU parallelism by working around the GIL, and `subprocess` falls entirely outside the scope of "internal" concurrency to instead control external processes.
