import asyncio  # NEW: Used to handle asynchronous operations.
import time


# CHANGED: The function is now asynchronous.
async def fetch_data(param):
    print(f"Do something with {param}...")

    # CHANGED: asyncio.sleep() does not block the event loop.
    # While waiting, other asynchronous tasks can run.
    await asyncio.sleep(param)

    print(f"Done with {param}")
    return f"Result of {param}"


# CHANGED: main() is now an asynchronous function.
async def main():

    # NEW: Calling an async function creates coroutine objects.
    # They do not start executing immediately.
    task1 = fetch_data(1)  # Could be awaited directly
    task2 = fetch_data(2)  # Could be awaited directly

    # CHANGED: We now await the first coroutine.
    result1 = await task1
    print("Task 1 fully completed")

    # The second coroutine is awaited only after the first one finishes.
    result2 = await task2

    print("Task 2 fully completed")

    return [result1, result2]


# The execution timer remains unchanged.
t1 = time.perf_counter()


# CHANGED: asyncio.run() is used to start the asynchronous main() function.
results = asyncio.run(main())
print(results)


# The execution timer remains unchanged.
t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")


# --------------------------------------------
# Explanation
# Task 1:  ──────── wait 1s ──────── DONE
# Task 2:                           ──────── wait 2s ──────── DONE

# Total ≈ 3 seconds