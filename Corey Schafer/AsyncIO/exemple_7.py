import asyncio
import time


# CHANGED from Version 6:
# fetch_data() is asynchronous again.
# Instead of using blocking time.sleep(), we use asyncio.sleep().
async def fetch_data(param):
    # asyncio.sleep() is non-blocking.
    # The event loop can run other tasks while waiting.
    await asyncio.sleep(param)

    return f"Result of {param}"


async def main():

    # ==================================================
    # 1. CREATE TASKS MANUALLY
    # ==================================================

    # Same approach introduced in Version 3.
    # create_task() schedules both coroutines immediately.
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    # Wait for both tasks to complete.
    result1 = await task1
    result2 = await task2

    print(f"Task 1 and 2 awaited results: {[result1, result2]}")


    # ==================================================
    # 2. GATHER COROUTINES
    # ==================================================

    # NEW:
    # Instead of creating tasks manually, we create a list
    # of coroutine objects.
    coroutines = [fetch_data(i) for i in range(1, 3)]

    # NEW:
    # asyncio.gather() schedules the coroutines concurrently
    # and waits for all of them to finish.
    #
    # return_exceptions=True means that exceptions are returned
    # as results instead of immediately being raised.
    results = await asyncio.gather(
        *coroutines,
        return_exceptions=True
    )

    print(f"Coroutine Results: {results}")


    # ==================================================
    # 3. GATHER TASKS
    # ==================================================

    # NEW:
    # We can also create Tasks manually and pass them to gather().
    tasks = [
        asyncio.create_task(fetch_data(i))
        for i in range(1, 3)
    ]

    # gather() waits for all tasks to finish.
    results = await asyncio.gather(*tasks)

    print(f"Task Results: {results}")


    # ==================================================
    # 4. TASK GROUP
    # ==================================================

    # NEW in modern Python:
    # TaskGroup provides a structured way to manage
    # multiple asynchronous tasks.
    async with asyncio.TaskGroup() as tg:

        # Create multiple tasks inside the TaskGroup.
        results = [
            tg.create_task(fetch_data(i))
            for i in range(1, 3)
        ]

        # All tasks are automatically awaited when
        # the TaskGroup context manager exits.

    # Task.result() retrieves the result of each completed task.
    print(
        f"Task Group Results: "
        f"{[result.result() for result in results]}"
    )


    return "Main Coroutine Done"


# Start measuring the total execution time.
t1 = time.perf_counter()


# Run the asynchronous main() function.
results = asyncio.run(main())
print(results)


# Stop measuring the total execution time.
t2 = time.perf_counter()

print(f"Finished in {t2 - t1:.2f} seconds")


# --------------------------------------------
# Explanation


# Gather()
# fetch_data(1) ──────────┐
#                         ├──→ gather() → results
# fetch_data(2) ─────────────────┘


# TaskGroup
# │
# ├── Task 1
# ├── Task 2
# │
# └── exit context
#        ↓
#    tasks completed