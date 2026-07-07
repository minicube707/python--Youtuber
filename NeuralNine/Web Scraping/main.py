from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

url = "https://webscraper.io/test-sites/tables"

# Download the HTML source code of the page
html_code = urlopen(url).read().decode("utf-8")

# Basic method
# print(html_code)
# start = html_code.find("<h1>") + len("<h1>")
# end = html_code.find("</h1>")
# print(html_code[start:end])

# ----------------------------------------
# Parse the HTML document with BeautifulSoup
# ----------------------------------------

soup = BeautifulSoup(html_code, 'lxml')

# Find all <h2> headings
heading2 = soup.find_all("h2")
print(f"Heading: {heading2}")

# Extract image information
images = soup.find_all("img")
print(f"\nImages: {images}")
print(f"Source: {images[0]['src']}")
print(f"Alt text: {images[0]['alt']}")

# Extract the last names from the first table
first_table = soup.find("table")
rows = first_table.find_all("tr")[1:]
last_name = []

for row in rows:
    last_name.append(row.find_all('td')[2].get_text())
    
print(f"\nLast names: {last_name}")


# ----------------------------------------
# Scrape data from a Wikipedia page
# ----------------------------------------

url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

# Add a User-Agent to avoid HTTP 403 errors
req = Request(url, headers={"User-Agent": "Mozilla/5.0"})

html_code = urlopen(req).read().decode("utf-8")

soup = BeautifulSoup(html_code, 'lxml')

# Locate the table containing Python's built-in types
type_table = soup.find(class_="wikitable")
body = type_table.find("tbody")
rows = body.find_all("tr")[1:]

mutable_type = []
immutable_type = []

# Separate mutable and immutable types
for row in rows:
    data = row.find_all("td")
    
    if data[1].get_text() == "mutable\n":
        mutable_type.append(data[0].get_text().strip("\n"))
        
    else:
        immutable_type.append(data[0].get_text().strip("\n"))
    
print("\nPython Types:")   
print(f"Mutable Types: {mutable_type}")
print(f"Immutable Types: {immutable_type}")

# Get the URL of the Python logo
thumb_box = soup.find(class_="mw-file-description")
thumb_img_src = thumb_box.find("img")["src"]
print(f"\nImage URL:\n{thumb_img_src}")

# Extract the table of contents
toc = soup.find(class_="vector-toc vector-pinnable-element")
toc_text = [a.get_text(" ", strip=True) for a in toc.find_all("a")]

print(f"\nContents:\n {toc_text}")