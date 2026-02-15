import functools
import time

def fibonacci(n):
    #Basic recursive Fibonacci function.
    #This implementation is very slow for large n
    #because it recomputes the same values many times.
    #Time complexity: exponential (O(2^n)).

    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@functools.cache
def fibonacci_cache(n):
    #Optimized recursive Fibonacci function using caching.

    #@functools.cache stores (memoizes) previously computed results.
    #If the function is called again with the same argument,
    #the stored result is returned instantly instead of recomputing it.
    #Time complexity becomes linear (O(n)).

    if n < 2:
        return n
    return fibonacci_cache(n - 1) + fibonacci_cache(n - 2)


num_fibo = 35

# Measure execution time for the simple recursive version
start_time = time.time()
print(fibonacci(num_fibo))
end_time = time.time()
print(f"Simple method Finish: {end_time - start_time:.4f} sec")

# Measure execution time for the cached version
start_time = time.time()
print(fibonacci_cache(num_fibo))
end_time = time.time()
print(f"Cache method Finish: {end_time - start_time:.4f} sec")