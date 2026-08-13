import asyncio
import time

# Asynchronous programming is a technique that allows a Python program to start a task
# without waiting for it to finish before continuing with other tasks.
# Unlike synchronous programming, async code can handle multiple tasks concurrently,
# which makes it particularly useful for I/O-bound operations.
# This includes tasks such as network requests, API calls, file operations, or database queries.
# Python provides the asyncio module and the async and await keywords to simplify asynchronous programming.
# By allowing the program to switch between tasks while waiting for operations to complete,
# asynchronous programming can make applications faster and more responsive.


def sync_function(test_param: str) -> str:
    """
    A synchronous function runs from start to finish before returning.
    While it is running, it blocks the current thread.
    """
    print("[SYNC] Function starts executing immediately.")

    # time.sleep() is blocking:
    # the program cannot do anything else during these 0.1 seconds.
    time.sleep(0.1)

    print("[SYNC] Function finished executing and is returning a result.")

    return f"Sync Result: {test_param}"


# ALSO KNOWN AS A COROUTINE FUNCTION
async def async_function(test_param: str) -> str:
    """
    An asynchronous function is also called a coroutine function.

    Calling this function does NOT execute its body immediately.
    It creates a coroutine object that can later be awaited or scheduled.
    """
    print("[COROUTINE] Coroutine has started executing.")

    # asyncio.sleep() is non-blocking.
    # 'await' temporarily gives control back to the event loop,
    # allowing other asynchronous work to run.
    print("[COROUTINE] Reaching 'await asyncio.sleep()' - control is given back to the event loop.")

    await asyncio.sleep(0.1)

    print("[COROUTINE] Sleep is finished - coroutine resumes execution.")

    return f"Async Result: {test_param}"


async def main():

    # ---------------------------------------------------------
    # 1. SYNCHRONOUS FUNCTION
    # ---------------------------------------------------------

    print("\n========== 1. SYNCHRONOUS FUNCTION ==========")

    print("[MAIN] Calling sync_function().")
    print("[MAIN] The function will execute immediately and block until it finishes.")

    sync_result = sync_function("Test")

    print(f"[MAIN] Received the synchronous result: {sync_result}")


    # ---------------------------------------------------------
    # 2. EVENT LOOP
    # ---------------------------------------------------------

    print("\n========== 2. EVENT LOOP ==========")

    # The event loop is the engine that manages asynchronous operations.
    #
    # It keeps track of coroutines, Tasks, Futures, etc.
    # and decides which piece of asynchronous code should run next.

    print("[MAIN] Getting the currently running event loop.")

    loop = asyncio.get_running_loop()

    print(f"[EVENT LOOP] Running event loop obtained: {loop}")


    # ---------------------------------------------------------
    # 3. FUTURE
    # ---------------------------------------------------------

    print("\n========== 3. FUTURE ==========")

    # A Future is a low-level object representing a result
    # that will be available at some point in the future.
    #
    # It is similar to a "promise" in JavaScript.

    print("[FUTURE] Creating an empty Future.")

    future = loop.create_future()

    print(f"[FUTURE] Future created. It does not have a result yet: {future}")


    # We manually give the Future its result.
    #
    # set_result() changes the Future from:
    #     PENDING -> FINISHED

    print("[FUTURE] Setting the result of the Future.")

    future.set_result("Future Result: Test")

    print("[FUTURE] Future is now completed with a result.")


    # 'await' waits for the Future to be completed
    # and retrieves its result.

    print("[FUTURE] Awaiting the Future to retrieve its result.")

    future_result = await future

    print(f"[FUTURE] Result received from the Future: {future_result}")


    # ---------------------------------------------------------
    # 4. COROUTINE OBJECT
    # ---------------------------------------------------------

    print("\n========== 4. COROUTINE OBJECT ==========")

    # Calling an 'async def' function does NOT execute it immediately.
    #
    # Instead, it returns a COROUTINE OBJECT.

    print("[COROUTINE] Calling async_function().")
    print("[COROUTINE] Important: the function body does NOT execute yet.")

    coroutine_obj = async_function("Test")

    print(f"[COROUTINE] We now have a coroutine object: {coroutine_obj}")


    # By using 'await', we start executing the coroutine
    # and wait for its result.

    print("[COROUTINE] Awaiting the coroutine - execution starts now.")

    coroutine_result = await coroutine_obj

    print(f"[COROUTINE] Coroutine finished. Result received: {coroutine_result}")


    # ---------------------------------------------------------
    # 5. TASK
    # ---------------------------------------------------------

    print("\n========== 5. TASK ==========")

    # A Task wraps a coroutine and schedules it to run
    # on the event loop.
    #
    # Unlike simply creating a coroutine object, create_task()
    # tells asyncio to schedule the coroutine for execution.

    print("[TASK] Creating a Task from async_function().")
    print("[TASK] The coroutine is now scheduled to run on the event loop.")

    task = asyncio.create_task(async_function("Test"))

    print(f"[TASK] Task created: {task}")


    # The Task can run independently while other async work
    # is being executed.
    #
    # 'await task' waits until the Task is finished
    # and retrieves its result.

    print("[TASK] Awaiting the Task to get its final result.")

    task_result = await task

    print(f"[TASK] Task finished. Result received: {task_result}")


# -------------------------------------------------------------
# 6. STARTING THE EVENT LOOP
# -------------------------------------------------------------

if __name__ == "__main__":

    print("========== ASYNCIO PROGRAM START ==========")

    # asyncio.run() creates and manages the event loop,
    # runs the main() coroutine, and closes the loop when finished.

    print("[ASYNCIO] Starting the event loop with asyncio.run(main()).")

    asyncio.run(main())

    print("\n========== ASYNCIO PROGRAM END ==========")