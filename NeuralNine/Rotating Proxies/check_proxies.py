import threading
import queue
import requests

# Create a queue to store all proxies
q = queue.Queue()

# List that can be used to store valid proxies
valides_proxies = []

# Load proxies from the file and add them to the queue
with open("proxy_list.txt") as f:
    proxies = f.read().split("\n")

    for p in proxies:
        q.put(p)

# Function executed by each thread
def check_proxies():
    global q

    # Keep checking proxies until the queue is empty
    while not q.empty():
        proxy = q.get()

        try:
            # Send a request through the proxy
            res = requests.get("https://ipinfo.io/json", proxies={"http": proxy, "https": proxy}, timeout=5)

        # Skip the proxy if the request fails
        except:
            continue

        # Print the proxy if it returns a successful response
        if res.status_code == 200:
            print(proxy)

# Start 10 threads to check proxies concurrently
for _ in range(10):
    threading.Thread(target=check_proxies).start()