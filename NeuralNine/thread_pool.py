import time
from concurrent.futures import ThreadPoolExecutor

def worker(number):
    print(f"Calculation for the number {number}")
    time.sleep(2)
    return number**2

pool = ThreadPoolExecutor(5)
worker1 = pool.submit(worker, 7)
worker2 = pool.submit(worker, 5)
worker3 = pool.submit(worker, 9)
worker4 = pool.submit(worker, 6)
worker4 = pool.submit(worker, 8)
worker5 = pool.submit(worker, 12)
worker6 = pool.submit(worker, 54)

if worker3.done():
    print("res work3 ",worker3.result())
else:
    print("wait for the result")

#Wait the result
print("")
print("hello world 1")
print(worker1.result())

if worker3.done():
    print("res work3 ",worker3.result())
else:
    print("wait for the result")

print("hello world 2")
print(worker6.result())
print("hello world 3")

pool.shutdown()