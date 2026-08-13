import asyncio
import time


# Asynchronous function that simulates a data-fetching operation.
async def fetch_data(param):
    print(f"Do something with {param}...")

    # CHANGED from Version 1:
    # asyncio.sleep() is non-blocking, allowing other tasks
    # to run while this task is waiting.
    await asyncio.sleep(param)

    print(f"Done with {param}")
    return f"Result of {param}"


async def main():

    # CHANGED from Version 2:
    # create_task() immediately schedules both coroutines
    # to run concurrently on the event loop.
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    # We wait for task 1 to finish.
    # However, task 2 is already running in the background.
    result1 = await task1
    print("Task 1 fully completed")

    # Task 2 has been running concurrently while task 1 was executing.
    result2 = await task2
    print("Task 2 fully completed")

    return [result1, result2]


# Start measuring the execution time.
t1 = time.perf_counter()


# Run the asynchronous main() function.
results = asyncio.run(main())
print(results)


# Stop measuring the execution time.
t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")


# --------------------------------------------
# Explanation   
# Task 1: ██████████ 1s
# Task 2: ████████████████████ 2s
#          └────────── running concurrently ──────────┘

# Total ≈ 2s