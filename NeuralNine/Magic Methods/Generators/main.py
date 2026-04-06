# Seq 1 to 9,000,000

# yield is a keyword in Python used to create a generator function.
# Unlike return, which terminates a function and sends back a single value,
# yield pauses the function’s execution and returns a value while preserving its state.
# This means the function can resume exactly where it left off the next time it is called.

# Generators are memory-efficient because they produce values on demand instead of storing an entire sequence in memory.
# This makes yield especially useful when working with large datasets or infinite sequences.

# Each time a generator is iterated (for example, with a for loop or next()), execution continues until the next yield statement is reached.
# When the function finishes, it raises a StopIteration exception automatically.

# In short, yield allows you to iterate over data lazily,
# making your code more efficient and often easier to read when dealing with streams or large computations.

import sys

def mygenerator(n):
    for x in range(n):
        yield x**3

# Test 1 : utilisation avec next()
values = mygenerator(9_000_000)

for _ in range(6):
    print(next(values))

print("\n--- Complete iteration ---")
values = mygenerator(100)
for x in values:
    print(x)

print("\n--- Memory usage ---")
gen = mygenerator(9_000_000)
lst = [x ** 3 for x in range(9_000_000)]

print(f"Generator size: {sys.getsizeof(gen)} bytes")
print(f"List size: {sys.getsizeof(lst)} bytes")
