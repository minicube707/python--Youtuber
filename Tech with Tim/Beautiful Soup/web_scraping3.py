from bs4 import BeautifulSoup
import requests

# Download the HTML content from CoinMarketCap
url = "https://coinmarketcap.com/"
result = requests.get(url).text

# Parse the HTML document
doc = BeautifulSoup(result, "html.parser")

# Get the first table body (<tbody>)
tbody = doc.tbody

print("=== TABLE BODY (tbody) ===")
print(tbody)

# Get all direct children of the tbody element
trs = tbody.contents

print("\n=== NUMBER OF ROWS FOUND ===")
print(len(trs))

# Display the next sibling of the first row
print("\n=== NEXT SIBLING OF FIRST ROW ===")
print(trs[0].next_sibling)

# Display the previous sibling of the second row
print("\n=== PREVIOUS SIBLING OF SECOND ROW ===")
print(trs[1].previous_sibling)

# Display the list next sibling of the first row
print("\n=== LIST NEXT SIBLING OF FIRST ROW ===")
print(list(trs[0].next_sibling))

# Display the parent tag name of the first row
print("\n=== PARENT TAG OF FIRST ROW ===")
print(trs[0].parent.name)

# Display all descendants of the first row
print("\n=== DESCENDANTS OF FIRST ROW ===")
print(list(trs[0].descendants))

# Dictionary that will store cryptocurrency names and prices
prices = {}

print("\n=== TOP 10 CRYPTOCURRENCIES ===")

# Loop through the first 10 rows
for index, tr in enumerate(trs[:10], start=1):

    # Extract the columns containing the coin name and price
    name, price = tr.contents[2:4]

    # Extract the cryptocurrency name
    fixed_name = name.p.string

    # Display the raw HTML of the price cell
    print(f"\n--- Coin #{index} ---")
    print("Price cell:")
    print(price)

    # Display the <a> tag that contains the price
    print("\nPrice link:")
    print(price.text)

    # Extract the actual price text
    fixed_price = price.text.strip()

    print(f"\nName : {fixed_name}")
    print(f"Price: {fixed_price}")

    # Store the result in the dictionary
    prices[fixed_name] = fixed_price

# Display the final dictionary
print("\n=== FINAL PRICE DICTIONARY ===")
for coin, price in prices.items():
    print(f"{coin}: {price}")