import requests

# Load the list of validated proxies from a file
with open("valid_proxies.txt") as f:
    proxies = f.read().split("\n")

# List of websites that will be tested with different proxies
sites_to_check = [
    "https://ipinfo.io/json",
    "https://books.toscrape.com/",
    "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html",
    "https://books.toscrape.com/catalogue/category/books/history_32/index.html"
]

# Keep track of which proxy is being used
counter = 0

# Loop through each website
for site in sites_to_check:

    try:
        # Display the proxy currently being used
        print(f"Using the proxy: {proxies[counter]}")

        # Send the request through the selected proxy
        res = requests.get(
            site,
            proxies={"http": proxies[counter], "https": proxies[counter]}, timeout=5)

        # Print the HTTP status code and response content
        print("")
        print(f"Code: {res.status_code}")

    except Exception:
        # Handle connection or proxy errors
        print("Failed")

    finally:
        # Move to the next proxy for the next request
        counter += 1