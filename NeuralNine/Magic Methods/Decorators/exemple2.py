# Pratical Exemple #2 - Timing

import time
import sys

sys.set_int_max_str_digits(1_000_000)

def timed(function):
    def wrapper(*args, **kwargs):
        before = time.time()
        value = function(*args, **kwargs)
        after = time.time()
        fname = function.__name__
        print(f"{fname} took {after - before} seconds to execute!")
        return value
    
    return wrapper

@timed
def myfunction(x):
    result = 1
    for i in range(1, x):
        result *= i
    return result

myfunction(100_000)
# print(myfunction(100_000))