import time
import requests
import asyncio
import httpx


# List of URLs to fetch from the Books to Scrape website
urls = [
    "https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html",
    "https://books.toscrape.com/catalogue/category/books/nonfiction_13/page-2.html",
    "https://books.toscrape.com/catalogue/category/books/nonfiction_13/page-3.html",
    "https://books.toscrape.com/catalogue/category/books/nonfiction_13/page-4.html",
    "https://books.toscrape.com/catalogue/category/books/nonfiction_13/page-5.html",
    "https://books.toscrape.com/catalogue/category/books/nonfiction_13/page-6.html",
    "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html",
    "https://books.toscrape.com/catalogue/category/books/fiction_10/page-2.html",
    "https://books.toscrape.com/catalogue/category/books/fiction_10/page-3.html",
    "https://books.toscrape.com/catalogue/category/books/fiction_10/page-4.html",
    "https://books.toscrape.com/catalogue/category/books/default_15/index.html",
    "https://books.toscrape.com/catalogue/category/books/default_15/page-2.html",
    "https://books.toscrape.com/catalogue/category/books/default_15/page-3.html",
    "https://books.toscrape.com/catalogue/category/books/default_15/page-4.html",
    "https://books.toscrape.com/catalogue/category/books/default_15/page-5.html",
    "https://books.toscrape.com/catalogue/category/books/default_15/page-6.html",
    "https://books.toscrape.com/catalogue/category/books/default_15/page-7.html",
    "https://books.toscrape.com/catalogue/category/books/default_15/page-8.html",
]


# Fetch all URLs sequentially using the requests library
def fetch():

    # Send an HTTP GET request for each URL
    # Each request waits for the previous one to finish
    result = [requests.get(url) for url in urls]

    # Display the list of HTTP responses
    print(result)


# Asynchronous function to fetch URLs using httpx
async def fetch_httpx():

    # Create an asynchronous HTTP client
    async with httpx.AsyncClient() as client:

        # Create multiple asynchronous GET requests
        reqs = [client.get(url) for url in urls]

        # Execute all requests concurrently and wait for their completion
        result = await asyncio.gather(*reqs)

    # Display the list of HTTP responses
    print(result)


# Display a message indicating that requests is being tested
print("\nFetch with requests:")

# Record the starting time
start = time.perf_counter()
fetch()
end = time.perf_counter()

# Calculate and display the total execution time
print(f"Time: {end - start}")


# Display a message indicating that httpx is being tested
print("\nFetch with httpx:")

# Record the starting time
start = time.perf_counter()
asyncio.run(fetch_httpx())
end = time.perf_counter()

# Calculate and display the total execution time
print(f"Time: {end - start}")