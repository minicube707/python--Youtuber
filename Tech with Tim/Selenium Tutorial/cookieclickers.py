# Selenium imports for browser automation
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Custom utility to load environment variables (ChromeDriver path)
from utils import get_env

# Used to resolve local file paths
from pathlib import Path

# Retrieve the ChromeDriver executable path from environment variables (.env file)
CHROMEDRIVER_PATH = get_env()

# Create a ChromeDriver service instance using the provided path
service = Service(CHROMEDRIVER_PATH)

# Configure Chrome options (can be extended with headless mode, arguments, etc.)
options = Options()

# Launch a new Chrome browser session
driver = webdriver.Chrome(service=service, options=options)

# Open the target local website (Cookie Clicker game)
path = Path("cookie-clicker-master/index.html").resolve()
driver.get(path.as_uri())

# Define DOM element identifiers used in the game
cookie_id = "bigCookie"            # Main clickable cookie element
cookies_id = "cookies"             # Element displaying total number of cookies
product_price_prefix = "price"     # Class name prefix for product price elements
product_prefix = "product"         # ID prefix for purchasable upgrades/products

# Wait until the main cookie element is loaded in the DOM
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, cookie_id)))

# Locate the main cookie element and perform an initial click
cookie = driver.find_element(By.ID, cookie_id)
cookie.click()

# Locate the products container and store its initial HTML state
products_div = driver.find_element(By.ID, "products")
previous_html = products_div.get_attribute("innerHTML")

# Infinite loop to continuously click the cookie and purchase upgrades
while True:
    
    # Click the cookie to generate resources
    cookie.click()

    # Retrieve the current number of cookies displayed in the UI
    cookies_count = driver.find_element(By.ID, cookies_id).text.split(" ")[0]

    # Clean the value (remove commas) and convert it to an integer
    cookies_count = int(cookies_count.replace(",", ""))

    # Skip iteration if the products section has not changed
    if products_div.get_attribute("innerHTML") == previous_html:
        continue

    # Attempt to buy upgrades multiple times per loop iteration
    for i in range(4):

        # Ensure product price elements are present in the DOM
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, product_price_prefix))
        )

        # Collect all product prices currently displayed
        list_product_price = []
        
        for element in driver.find_elements(By.CLASS_NAME, product_price_prefix):
            
            try:
                # Clean price text (remove commas for numeric comparison)
                list_product_price.append(element.text.replace(",", ""))
                
            except:
                # Skip elements that cannot be read properly
                continue

        # Iterate through available product prices
        for product_price in list_product_price:

            # Ignore invalid or non-numeric price values
            if not product_price.isdigit():
                continue

            # If we can afford the product, purchase it
            if cookies_count >= int(product_price):

                # Locate the corresponding product by its dynamic ID and click it
                product = driver.find_element(By.ID, product_prefix + str(i))
                product.click()

                # Update the products container state after purchase
                products_div = driver.find_element(By.ID, "products")
                previous_html = products_div.get_attribute("innerHTML")

                break