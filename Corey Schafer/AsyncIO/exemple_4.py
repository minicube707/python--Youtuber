import asyncio
import time


# Asynchronous function that simulates a data-fetching operation.
async def fetch_data(param):
    print(f"Do something with {param}...")

    # Non-blocking wait: other tasks can continue running during this time.
    await asyncio.sleep(param)

    print(f"Done with {param}")
    return f"Result of {param}"


async def main():

    # These two tasks are still created and scheduled concurrently.
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    # CHANGED from Version 3:
    # We now wait for Task 2 first.
    result2 = await task2
    print("Task 2 fully completed")

    # Task 1 has been running concurrently in the background.
    # Since Task 1 only takes 1 second, it will normally already
    # be completed by the time we reach this line.
    result1 = await task1
    print("Task 1 fully completed")

    # The results are returned in the desired order.
    return [result1, result2]


# Start measuring the total execution time.
t1 = time.perf_counter()


# Start the asynchronous program.
results = asyncio.run(main())
print(results)


# Stop measuring the execution time.
t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")


# --------------------------------------------
# Explanation  

# Time:    0s        1s                 2s
#          |---------|------------------|
# Task 1:  ██████████ DONE
# Task 2:  █████████████████████████████ DONE
#          ↑
#          Both tasks start here

# # Total ≈ 2s