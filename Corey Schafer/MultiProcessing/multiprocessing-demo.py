import concurrent.futures
import multiprocessing
import os
import time

# Multiprocessing is a technique that allows a Python program to execute multiple processes simultaneously.
# Unlike multithreading, each process has its own Python interpreter and memory space,
# which enables true parallel execution on multiple CPU cores.
# This makes multiprocessing particularly effective for CPU-bound tasks,
# such as mathematical computations, image processing, or data analysis.
# Python provides the multiprocessing module and the concurrent.futures.ProcessPoolExecutor class
# to simplify the creation and management of worker processes.
# By distributing work across several processes, programs can significantly reduce execution time
# and make better use of modern multi-core processors.

# --------------------------------------------
# Simple function that simulates an I/O task.
# --------------------------------------------
def do_something():
    """Simulate a task that takes one second."""
    print("Sleeping for 1 second...")
    time.sleep(1)
    print("Done sleeping.")


# --------------------------------------------
# Same as above but accepts a duration.
# Used to demonstrate passing arguments
# to a thread.
# --------------------------------------------
def sleep_for(seconds):
    """Sleep for the specified number of seconds."""
    print(f"Sleeping for {seconds} second(s)...")
    time.sleep(seconds)
    print("Done sleeping.")


# --------------------------------------------
# Simulates work and returns a value.
# Useful for demonstrating ThreadPoolExecutor.
# --------------------------------------------
def return_value(seconds):
    """Sleep for the specified duration and return a sample value."""
    print(f"Sleeping for {seconds} second(s)...")
    time.sleep(seconds)
    print(f"Done sleeping after {seconds} second(s).")
    return "hello_world"


# ============================================================
# CPU Information
# Displays the number of logical and physical CPUs available,
# along with the recommended number of worker processes.
# ============================================================
def print_cpu_info():
    """Display information about the available CPUs."""
    print("CPU Information")
    print(f"Logical CPUs : {os.cpu_count()}")
    print(f"Physical CPUs: {os.process_cpu_count()}")
    print(f"Recommended worker count: {multiprocessing.cpu_count()}")


# ============================================================
# Example 1: Sequential execution (single process)
# Both function calls are executed sequentially.
# Expected execution time: ~2 seconds.
# ============================================================
def run_sequential():
    """Run two tasks sequentially."""
    print("\n=== Sequential execution ===")
    start = time.perf_counter()

    do_something()
    do_something()

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)")


# ============================================================
# Example 2: Two manually created processes
# Both tasks run in parallel.
# Expected execution time: ~1 second.
# ============================================================
def run_two_processes():
    """Run two processes in parallel."""
    print("\n=== Two processes ===")
    start = time.perf_counter()

    p1 = multiprocessing.Process(target=do_something)
    p2 = multiprocessing.Process(target=do_something)

    # Start both processes
    p1.start()
    p2.start()

    # Wait until both processes finish
    p1.join()
    p2.join()

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)")


# ============================================================
# Example 3: Multiple manually created processes
# Launch 10 parallel tasks.
# ============================================================
def run_multiple_processes():
    """Launch several processes manually."""
    print(f"\n=== {10} manual processes ===")
    start = time.perf_counter()

    processes = []

    for _ in range(10):
        process = multiprocessing.Process(target=do_something)
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)")


# ============================================================
# Example 4: Passing arguments to processes
# The args parameter must be an iterable.
# ============================================================
def run_process_with_args():
    """Launch several processes with arguments."""
    print("\n=== Processes with arguments ===")
    start = time.perf_counter()

    processes = []

    for _ in range(10):
        process = multiprocessing.Process(target=sleep_for, args=[1.5])
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)")

# ============================================================
# Example 5: ThreadPoolExecutor with submit()
# submit() returns a Future object.
# Calling result() blocks until the task completes.
# ============================================================

def run_executor_submit_one_process():
    """Submit tasks individually using ProcessPoolExecutor."""
    print("\n=== ProcessPoolExecutor (submit) ===")
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        f1 = executor.submit(return_value, 1)
        f2 = executor.submit(return_value, 1)

        print(f1.result())
        print(f2.result())
    
    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)")

# ============================================================
# Example 6: Multiple tasks with submit()
# as_completed() returns futures as soon as they finish,
# regardless of the submission order.
# ============================================================
def run_executor_submit_several_processes():
    """Submit tasks individually using ProcessPoolExecutor."""
    print("\n=== ProcessPoolExecutor (submit) ===")
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(return_value, 1.5)
            for _ in range(10)
        ]

        # as_completed() returns futures as soon as they finish
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)")


# ============================================================
# Example 7: Tasks with different execution times
# Results are printed in completion order.
# Fastest tasks appear first.
# ============================================================
def run_executor_submit_different_time():
    """Submit tasks individually using ProcessPoolExecutor."""
    print("\n=== ProcessPoolExecutor (submit) ===")
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        durations = [5, 4, 3, 2, 1]
        futures = [executor.submit(return_value, duration) for duration in durations]

        # as_completed() returns futures as soon as they finish
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)")
    
# ============================================================
# Example 8: Using executor.map()
# Unlike as_completed(), map() preserves the input order.
# Even if shorter tasks finish first, results are yielded
# following the order of the input iterable.
# ============================================================ 
def run_executor_map():
    """Execute tasks using executor.map()."""
    print("\n=== ProcessPoolExecutor (map) ===")
    start = time.perf_counter()

    durations = [5, 4, 3, 2, 1]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # map() preserves the input order
        for result in executor.map(return_value, durations):
            print(result)

    elapsed = time.perf_counter() - start
    print(f"Finished in {elapsed:.2f} second(s)")


def main():
    """Run all multiprocessing examples."""
    print_cpu_info()

    run_sequential()
    run_two_processes()
    run_multiple_processes()
    run_process_with_args()
    run_executor_submit_one_process()
    run_executor_submit_several_processes()
    run_executor_submit_different_time()
    run_executor_map()


if __name__ == "__main__":
    # Required when using multiprocessing on Windows.
    # Prevents child processes from executing the main script recursively.
    main()