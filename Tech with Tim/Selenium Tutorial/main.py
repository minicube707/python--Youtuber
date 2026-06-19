from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import get_env

import time

# Retrieve the ChromeDriver executable path from environment variables (.env file)
CHROMEDRIVER_PATH = get_env()

# Create a ChromeDriver service instance using the provided path
service = Service(CHROMEDRIVER_PATH)

# Launch a new Chrome browser session
driver = webdriver.Chrome(service=service)

# Open Google homepage
driver.get("https://google.com/")

# Create an explicit wait object (up to 100 seconds max wait time)
wait = WebDriverWait(driver, 100)

# Wait until the "Reject all" cookies/consent button is clickable and click it
btn = wait.until(EC.element_to_be_clickable((By.ID, "W0wltc")))
btn.click()

# Locate the Google search input field by its class name
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")

# Type a search query and simulate pressing ENTER
input_element.send_keys("tech with tim" + Keys.ENTER)

# Wait for results to load / keep browser open for observation
time.sleep(10)

# Close the browser and end the session
driver.quit()