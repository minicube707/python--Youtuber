import asyncio
import time


# Asynchronous function that simulates a data-fetching operation.
async def fetch_data(param):
    print(f"Do something with {param}...")

    # CHANGED from Version 4:
    # time.sleep() is a BLOCKING operation.
    # It blocks the entire event loop and prevents other
    # asynchronous tasks from running.
    time.sleep(param)

    print(f"Done with {param}")
    return f"Result of {param}"


async def main():

    # The tasks are still created concurrently.
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    # Wait for Task 1 to complete.
    result1 = await task1
    print("Task 1 fully completed")

    # Wait for Task 2 to complete.
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

# Time:    0s        1s                 3s
#          |---------|------------------|
# Task 1:  ██████████ DONE
# Task 2:            ████████████████████ DONE
#          ↑
#          Task 2 cannot run during Task 1's blocking sleep

# # Total ≈ 3s