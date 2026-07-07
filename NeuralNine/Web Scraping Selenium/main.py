from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from utils import get_env

# Retrieve the ChromeDriver executable path from the .env file
CHROMEDRIVER_PATH = get_env()

# Create a ChromeDriver service
service = Service(CHROMEDRIVER_PATH)

# Configure Chrome options
options = Options()

# Keep the browser open after the script finishes
options.add_experimental_option("detach", True)

# Launch a new Chrome browser instance
driver = webdriver.Chrome(service=service, options=options)

# Open the NeuralNine homepage
driver.get("http://www.neuralnine.com/")

# Maximize the browser window
driver.maximize_window()

# Find all links on the page
links = driver.find_elements("xpath", "//a[@href]")

# Look for the "Books" link and click it
for link in links:

    if "Books" in link.get_attribute("innerHTML"):

        try:
            link.click()
            break
        
        # Ignore elements that cannot be clicked
        except:
            pass

# Locate the "The Python Bible 7 in 1" book link
link = driver.find_element(By.XPATH, "//div[contains(@class,'elementor-widget-container')][.//h3[contains(.,'7 in 1')]]//h3/a")

# Click the link using JavaScript to avoid click interception issues
driver.execute_script("arguments[0].click();", link)

# Find all price elements associated with the Paperback edition in EUR
buttons = driver.find_elements(By.XPATH, "//a[.//span[text()[contains(., 'Paperback')]]]//span[text()[contains(., 'EUR')]]")

# Print each price while replacing the HTML non-breaking space with a regular space
for button in buttons:
    print(button.get_attribute("innerHTML").replace("&nbsp;", " "))