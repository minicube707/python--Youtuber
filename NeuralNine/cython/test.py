import main
import time

print('Running')

start_vanillia = time.time()
main.prime_finder_vanillia(50_000)
end_vanillia = time.time()

start_optimized = time.time()
main.prime_finder_optimized(100_000)
end_optimized = time.time()

print("")
print("Time to vanillia", end_vanillia - start_vanillia)
print("Time to optimized", end_optimized - start_optimized)
