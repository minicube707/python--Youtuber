from time import time, sleep
from contextlib import contextmanager

# The @contextmanager decorator allows you to create a context manager
# using a generator function instead of a class. The code before `yield`
# runs when entering the `with` block, and the code after `yield` runs
# when exiting it (even if an exception occurs).

# Global dictionary for storing cumulative durations
timings: dict[str, float] = {}

@contextmanager
def measure_time(name: str):
    """
    Context manager for measuring the execution time of a block.
    Durations are cumulative by name.
    """
    start = time()
    try:
        # Executing the "with" block
        yield 


    finally:
        # Ensures that the timing is recorded even in case of error
        duration = time() - start
        print(f"{name} exécuté en {duration:.4f}s")
        timings[name] = timings.get(name, 0) + duration


def display_timings():
    print("\n--- Result ---")
    for name, total in timings.items():
        print(f"{name}: {total:.4f} secondes")


def main():
    for i in range(3):
        print(f"\nIteration {i}")

        with measure_time("convolution"):
            sleep(0.5)

        with measure_time("relu"):
            sleep(1)

        with measure_time("softmax"):
            sleep(2)

    display_timings()


if __name__ == "__main__":
    main()