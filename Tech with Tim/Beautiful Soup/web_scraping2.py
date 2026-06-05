from bs4 import BeautifulSoup
import re

# Open the HTML file in read mode
with open("index2.html", "r") as f:
    # Parse the HTML content using BeautifulSoup
    doc = BeautifulSoup(f, "html.parser")

# Find the first <option> element
tag = doc.find("option")

# Modify existing attributes and add a new one
tag['value'] = 'new value'
tag['color'] = "blue"

# Print all attributes of the tag as a dictionary
print("Print all attributes of the tag as a dictionary")
print(tag.attrs)

# Print the updated HTML tag
print("\nPrint the updated HTML tag")
print(tag)

# Find all <p>, <div>, and <li> elements
tags = doc.find_all(["p", "div", "li"])
print("\nPrint all <p>, <div>, and <li> elements")
print(tags)

# Find <option> elements matching specific text and value attributes
tags = doc.find_all(
    ["option"],
    string="Undergraduate",
    value="undergraduate"
)
print("\nPrint  <option> elements matching specific text and value attributes")
print(tags)

# Find all elements with the CSS class "btn-item"
tags = doc.find_all(class_="btn-item")
print("\nPrint all elements with the CSS class 'btn-item'")
print(tags)

# Find strings matching a regular expression (prices starting with '$')
# Limit the result to the first match found
tags = doc.find_all(string=re.compile(r"\$.*"), limit=1)
print("\nPrint strings matching a regular expression (prices starting with '$')")
print(tags)

# Remove extra whitespace and print the matched text
print("\nPrint matched text without extra whitespace")
for tag in tags:
    print(tag.strip())

# Find all text input fields
tags = doc.find_all("input", type="text")

# Update the placeholder attribute of each text input
for tag in tags:
    tag['placeholder'] = "I changed you !"

# Save the modified HTML document to a new file
with open("changed.html", "w") as file:
    file.write(str(doc))