from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import get_env

import time

# Retrieve ChromeDriver path from environment configuration
CHROMEDRIVER_PATH = get_env()

# Configure Chrome options
options = Options()

# Keep the browser window open after script execution
options.add_experimental_option("detach", True)

# Initialize ChromeDriver service
service = Service(CHROMEDRIVER_PATH)

# Start a new Chrome browser session
driver = webdriver.Chrome(service=service, options=options)

# Open the target website
driver.get("https://www.techwithtim.net/")

# Locate the "Tutorials" link by its visible text and click it
link = driver.find_element(By.LINK_TEXT, "Tutorials")
link.click()

try:
    # Wait until the first tutorial card is present in the DOM, then click it
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "kiZnIX")))
    element.click()

    # Wait until the next element is available, then click it
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hZeIKp")))
    element.click()

    # Small delay to allow page content to load
    time.sleep(2)

    # Navigate back in browser history (step by step)
    driver.back()
    driver.back()
    driver.back()

    # Allow time for the page to load after navigation
    time.sleep(2)

    # Move forward in browser history
    driver.forward()

except Exception as e:
    # Close the browser if any error occurs
    driver.quit()