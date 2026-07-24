import os
import time
import threading
import concurrent.futures


# **Threading** is a concurrency technique that allows a program to execute multiple tasks at the same time within a single process.
# In Python, threads are particularly useful for **I/O-bound operations**, such as reading files, making network requests,
# or waiting for external resources, because other threads can continue running while one thread is waiting.
# The `threading` module lets you create and manage threads manually,
# while `concurrent.futures.ThreadPoolExecutor` provides a simpler and
# more scalable way to execute tasks concurrently using a pool of worker threads.

# --------------------------------------------
# Simple function that simulates an I/O task.
# --------------------------------------------
def do_something():
    print("Sleeping 1 second...")
    time.sleep(1)
    print("Done Sleeping...")


# --------------------------------------------
# Same as above but accepts a duration.
# Used to demonstrate passing arguments
# to a thread.
# --------------------------------------------
def sleep_for(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    print("Done Sleeping...")


# --------------------------------------------
# Simulates work and returns a value.
# Useful for demonstrating ThreadPoolExecutor.
# --------------------------------------------
def return_value(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    print(f"Done Sleeping in {seconds} second(s)...")
    return "hello_world"


# ============================================================
# Thread Information
# Displays CPU information and the number of active threads.
# Useful for understanding the threading environment.
# ============================================================

"""Display information about CPUs and active threads."""
print("Thread Information")
print(f"Logical CPUs : {os.cpu_count()}")
print(f"Physical CPUs: {os.process_cpu_count()}")
print(f"Active threads: {threading.active_count()}")
    

# ============================================================
# Example 1: Sequential execution (single thread)
# Both function calls are executed one after another.
# Expected execution time: ~2 seconds.
# ============================================================

print("\n")
print("=" * 60)
print("Run on single thread")

start = time.perf_counter()

do_something()
do_something()

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} second(s)")


# ============================================================
# Example 2: Two manually created threads
# Both tasks run concurrently.
# Expected execution time: ~1 second.
# ============================================================

print("\n")
print("=" * 60)
print("Run on two threads")

start = time.perf_counter()

t1 = threading.Thread(target=do_something)
t2 = threading.Thread(target=do_something)

# Start both threads
t1.start()
t2.start()

# Wait until both threads finish
t1.join()
t2.join()

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} second(s)")


# ============================================================
# Example 3: Multiple manually created threads
# Launch 10 concurrent tasks.
# ============================================================

print("\n")
print("=" * 60)
print("Run on multiple threads")

start = time.perf_counter()

threads = []

for _ in range(10):
    t = threading.Thread(target=do_something)
    t.start()
    threads.append(t)

# Wait for every thread to complete
for thread in threads:
    thread.join()

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} second(s)")


# ============================================================
# Example 4: Passing arguments to threads
# The args parameter must be an iterable.
# ============================================================

print("\n")
print("=" * 60)
print("Run on multiple threads with arguments")

start = time.perf_counter()

threads = []

for _ in range(10):
    t = threading.Thread(target=sleep_for, args=[1.5])
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} second(s)")


# ============================================================
# Example 5: ThreadPoolExecutor with submit()
# submit() returns a Future object.
# Calling result() blocks until the task completes.
# ============================================================

print("\n")
print("=" * 60)
print("Run on 2 threads with ThreadPoolExecutor")

start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executor:

    f1 = executor.submit(return_value, 1)
    f2 = executor.submit(return_value, 1)

    print(f1.result())
    print(f2.result())

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} second(s)")


# ============================================================
# Example 6: Multiple tasks with submit()
# as_completed() returns futures as soon as they finish,
# regardless of the submission order.
# ============================================================

print("\n")
print("=" * 60)
print("Run on multiple threads with ThreadPoolExecutor")

start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executor:

    futures = [executor.submit(return_value, 1) for _ in range(10)]

    for future in concurrent.futures.as_completed(futures):
        print(future.result())

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} second(s)")


# ============================================================
# Example 7: Tasks with different execution times
# Results are printed in completion order.
# Fastest tasks appear first.
# ============================================================

print("\n")
print("=" * 60)
print("Run on multiple threads with different durations")

start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executor:

    durations = [5, 4, 3, 2, 1]
    futures = [executor.submit(return_value, duration) for duration in durations]

    for future in concurrent.futures.as_completed(futures):
        print(future.result())

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} second(s)")


# ============================================================
# Example 8: Using executor.map()
# Unlike as_completed(), map() preserves the input order.
# Even if shorter tasks finish first, results are yielded
# following the order of the input iterable.
# ============================================================

print("\n")
print("=" * 60)
print("Run on multiple threads using executor.map()")

start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executor:

    durations = [5, 4, 3, 2, 1]

    results = executor.map(return_value, durations)

    for result in results:
        print(result)

finish = time.perf_counter()

print(f"Finished in {round(finish - start, 2)} second(s)")