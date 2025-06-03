import threading
import time

class ThreadCounter:

    def __init__(self) -> None:
        self.counter = 0
        self.lock = threading.Lock()

    def count(self, thread_num):
        while True:
            self.lock.acquire()
            self.counter +=1
            print(f"{thread_num}: Just increased counter to {self.counter}")
            time.sleep(1)
            print(f"{thread_num}: Done some work, now value is {self.counter}")
            self.lock.release()
            
tc = ThreadCounter()

for i in range(10):
    t = threading.Thread(target=tc.count, args=(i,))
    t.start()