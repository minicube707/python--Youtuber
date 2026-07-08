from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from utils import get_env

# Useful links:
# https://books.toscrape.com/
# https://xpather.com/

# Retrieve the ChromeDriver executable path from the .env file
CHROMEDRIVER_PATH = get_env()

# Target website
url = "https://books.toscrape.com/"

# Configure Chrome browser options
options = Options()

# Keep the browser window open after the script finishes
options.add_experimental_option("detach", True)

# Create a ChromeDriver service using the executable path
service = Service(CHROMEDRIVER_PATH)

# Launch a new Chrome browser instance
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the target website
driver.get(url)

# Maximize the browser window for better visibility
driver.maximize_window()

# XPath expression:
# - Select all book titles (<a> inside <h3>)
# - Select all prices
# - Only for books with a one-star rating
xpath_query = (
    "//article[p[@class='star-rating One']]//h3/a | "
    "//article[p[@class='star-rating One']]//p[@class='price_color']"
)

# Find all elements matching the XPath expression
results = driver.find_elements("xpath", xpath_query)

# Iterate through each matching element
for result in results:

    # If the element is a link (<a>), print its title attribute
    if result.tag_name == "a":
        print(result.get_attribute("title"))

    # Otherwise, print the element's HTML content (the book price)
    else:
        print(result.get_attribute("innerHTML"))