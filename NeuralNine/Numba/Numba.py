
from numba import jit
import math
import random
import time

#jiy Just It Time

@jit(nopython=True)
def some_function(n):
    z = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        z += math.sqrt(x**2 + y**2)

    return z

start = time.time()
some_function(10_000_000)
end = time.time()

print(end - start)


start = time.time()
some_function(10_000_000)
end = time.time()

print(end - start)

#In python vannilla 7s
#In python with numba and compilation time 1.2s
#In python with numba without compilation time 0.2s