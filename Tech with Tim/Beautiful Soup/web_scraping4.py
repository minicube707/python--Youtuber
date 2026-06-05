from bs4 import BeautifulSoup
import requests
import re

# Ask the user what product they want to search for
search_term = input("What product do you want to search for? ")

# Build the initial search URL
url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"

# Download the first search results page
page = requests.get(url).text

# Parse the HTML document
doc = BeautifulSoup(page, "html.parser")

# Find the pagination element that contains the total number of pages
page_text = doc.find(class_="list-tool-pagination-text").strong

# Extract the total number of pages from the pagination text
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

print(f"\nFound {pages} pages of results.\n")

# Dictionary to store product information
items_found = {}

# Loop through every page of search results
for page_num in range(1, pages + 1):

    print(f"Scanning page {page_num}/{pages}...")

    # Build the URL for the current page
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page_num}"

    # Download the page
    page = requests.get(url).text

    # Parse the HTML
    doc = BeautifulSoup(page, "html.parser")

    # Search for text matching the search term
    items = doc.find_all(string=re.compile(search_term))

    print(f"  Found {len(items)} potential matches")

    # Process each matching item
    for item in items:

        parent = item.parent

        # Ignore matches that are not product links
        if parent.name != "a":
            continue

        # Get the product URL
        link = parent["href"]

        # Find the product container
        next_parent = item.find_parent(class_="item-container")

        try:
            # Extract the product price
            price = (next_parent.find(class_="price-current").find("strong").string)

            # Store the result
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}

            print(f"    Added: {item}")
            print(f"    Price: ${price}")

        except Exception as e:
            print(f"    Could not extract price for: {item}")
            print(f"    Error: {e}")

print("\nSorting products by price...\n")

# Sort products from cheapest to most expensive
sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])

print("=== SEARCH RESULTS ===\n")

# Display the sorted results
for item in sorted_items:
    print(f"Product: {item[0]}")
    print(f"Price: ${item[1]['price']}")
    print(f"Link: {item[1]['link']}")
    print("-" * 40)