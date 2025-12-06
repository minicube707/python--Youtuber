import gc
import sys
import time

gc.set_threshold(20_000, 50, 100)
gc.disable()

class Link:

    def __init__(self, next_link, value) -> None:
        self.next_link = next_link
        self.value = value

    def __repr__(self) -> str:
        return self.value
    
l = Link(None, "Main Link")

my_list = []

start = time.perf_counter()
for i in range(5_000_000):
    l_temp = Link(l, "L")
    my_list.append(l_temp)
end = time.perf_counter()

print("Done in ", end - start)