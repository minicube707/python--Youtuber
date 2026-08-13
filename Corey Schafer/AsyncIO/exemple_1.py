import time


# Simulates a data-fetching operation.
# The function waits for the number of seconds given by "param".
def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


# Main function that executes the data-fetching operations sequentially.
def main():
    # First operation: waits for 1 second.
    result1 = fetch_data(1)
    print("Fetch 1 fully completed")

    # Second operation: waits for 2 seconds.
    result2 = fetch_data(2)
    print("Fetch 2 fully completed")

    # Returns the results of both operations.
    return [result1, result2]


# Start the timer to measure the total execution time.
t1 = time.perf_counter()


# Run the main function.
results = main()
print(results)


# Stop the timer.
t2 = time.perf_counter()

# Display the total execution time with two decimal places.
print(f"Finished in {t2 - t1:.2f} seconds")


# --------------------------------------------
# Explanation
# fetch_data(1)  →  wait 1 second  →  completed
#                                       ↓
# fetch_data(2)  →  wait 2 seconds  →  completed

# Total ≈ 3 seconds