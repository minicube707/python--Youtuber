import asyncio
import time
from concurrent.futures import ProcessPoolExecutor  # NEW: Used to run functions in separate processes.


# CHANGED from Version 5:
# fetch_data() is no longer an async function.
# It is a regular synchronous function because it uses time.sleep().
def fetch_data(param):
    print(f"Do something with {param}...", flush=True)

    # This is still a blocking operation.
    # However, it will now run outside the main asyncio event loop.
    time.sleep(param)

    print(f"Done with {param}", flush=True)
    return f"Result of {param}"


async def main():

    # =========================
    # RUNNING IN THREADS
    # =========================

    # NEW:
    # asyncio.to_thread() moves the blocking function to a separate thread.
    # This prevents time.sleep() from blocking the asyncio event loop.
    task1 = asyncio.create_task(asyncio.to_thread(fetch_data, 1))
    task2 = asyncio.create_task(asyncio.to_thread(fetch_data, 2))

    # Both thread tasks can run concurrently.
    result1 = await task1
    print("Thread 1 fully completed")

    result2 = await task2
    print("Thread 2 fully completed")


    # =========================
    # RUNNING IN A PROCESS POOL
    # =========================

    # NEW:
    # Get the currently running asyncio event loop.
    loop = asyncio.get_running_loop()

    # NEW:
    # Create a pool of worker processes.
    # Each process has its own Python interpreter.
    with ProcessPoolExecutor() as executor:

        # NEW:
        # run_in_executor() sends fetch_data() to separate processes.
        task1 = loop.run_in_executor(executor, fetch_data, 1)
        task2 = loop.run_in_executor(executor, fetch_data, 2)

        # Both processes can execute fetch_data() concurrently.
        result1 = await task1
        print("Process 1 fully completed")

        result2 = await task2
        print("Process 2 fully completed")


    return [result1, result2]


# NEW:
# This condition is especially important when using multiprocessing.
# It prevents the program from recursively creating new processes.
if __name__ == "__main__":

    # Start measuring execution time.
    t1 = time.perf_counter()

    # Run the asynchronous main function.
    results = asyncio.run(main())
    print(results)

    # Stop measuring execution time.
    t2 = time.perf_counter()

    print(f"Finished in {t2 - t1:.2f} seconds")


# --------------------------------------------
# Explanation  

#          asyncio event loop
#                  │
#       ┌──────────┴──────────┐
#       ↓                     ↓
#   Thread 1              Thread 2
# fetch_data(1)          fetch_data(2)
#   sleep(1)               sleep(2)
#       │                     │
#       └──────────┬──────────┘
#                  ↓
#             asyncio


#          asyncio event loop
#                  │
#       ┌──────────┴──────────┐
#       ↓                     ↓
#   Process 1              Process 2
# fetch_data(1)          fetch_data(2)
#   sleep(1)               sleep(2)