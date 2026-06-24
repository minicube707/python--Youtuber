from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from utils import get_env

# Get the ChromeDriver path from the .env file
CHROMEDRIVER_PATH = get_env()

# Create Chrome options
options = Options()

# Keep the browser open after the script finishes
options.add_experimental_option("detach", True)

# Create a ChromeDriver service using the specified path
service = Service(CHROMEDRIVER_PATH)

# Launch a new Chrome browser instance
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the target website
driver.get("https://www.techwithtim.net/")

# Print the title of the current page
print(driver.title)