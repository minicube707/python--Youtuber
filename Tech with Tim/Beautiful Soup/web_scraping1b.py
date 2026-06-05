from bs4 import BeautifulSoup
import requests

# URL of the product page to scrape
url = "https://www.newegg.ca/gigabyte-geforce-rtx-3080-ti-gv-n308tgaming-oc-12gd/p/N82E16814932436?Description=3080&cm_re=3080-_-14-932-436-_-Product"

# Send an HTTP GET request to the webpage
result = requests.get(url)

# Print the raw HTML content returned by the server
print("\nRaw text")
print(result.text)


# Parse the HTML content using BeautifulSoup
doc = BeautifulSoup(result.text, "html.parser")

print("\Beatiful text")
print(doc.prettify())

# Find all text nodes containing the "$" symbol
prices = doc.find_all(string="$")

# Get the parent element of the first "$" text node
if len(prices) > 0:
    parent = prices[0].parent

    # Find the <strong> tag inside the parent element
    strong = parent.find("strong")

    # Print the price value stored in the <strong> tag
    print(strong.string)