from bs4 import BeautifulSoup

# Open the HTML file in read mode
with open("index.html", "r") as f:
    # Parse the HTML content using BeautifulSoup
    doc = BeautifulSoup(f, "html.parser")

# Display the formatted HTML structure
print(doc.prettify())

# Get the <title> tag
tag = doc.title

# Print the title tag
print("\nThe Title")
print(tag)

# Print only the text inside the title tag
print("\nThe Title without tag")
print(tag.string)

# Modify the text inside the title tag
tag.string = "Hello World"

# Display the updated title tag
print("\nThe updated title tag")
print(tag)

# Display the updated title text only
print("\nThe Title without tag")
print(tag.string)

# Find the first <a> tag in the document
print("\nThe first <a> tag in the document")
first_tag = doc.find("a")
print(first_tag)

# Find all <p> tags and print them as a list
print("\nAll <p> tags and print them as a list")
all_tag = doc.find_all("p")
print(all_tag)

# Access and print only the first <p> tag
print("\nAccess and print only the first <p> tag")
all_tag = doc.find_all("p")[0]
print(all_tag)