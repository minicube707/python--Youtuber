from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from utils import get_env
from pathlib import Path

# Retrieve ChromeDriver path from environment configuration
CHROMEDRIVER_PATH = get_env()

# Initialize ChromeDriver service with the executable path
service = Service(CHROMEDRIVER_PATH)

# Start a new Chrome browser session
driver = webdriver.Chrome(service=service)

# Load the local Cookie Clicker game (HTML file)
path = Path("cookie-clicker-master/index.html").resolve()
driver.get(path.as_uri())

# Implicit wait to allow elements to load before throwing errors
driver.implicitly_wait(5)

# Locate the main cookie button (the big clickable cookie)
cookie = driver.find_element(By.ID, "bigCookie")

# Locate the store container and store its initial HTML state
# This will be used to detect changes when new upgrades appear or are purchased
store_div = driver.find_element(By.ID, "store")
previous_html = store_div.get_attribute("innerHTML")

# Main automation loop (simulates continuous clicking and buying upgrades)
for i in range(5000):

    # Click the big cookie to generate cookies
    cookie.click()

    # Check if the store content has changed (new upgrade unlocked or purchased)
    if store_div.get_attribute("innerHTML") != previous_html:

        # Re-locate the store element to avoid stale references
        store = driver.find_element(By.ID, "store")

        # Find all currently purchasable upgrades (enabled items)
        enabled_items = store.find_elements(By.CLASS_NAME, "enabled")

        # Buy the most expensive available upgrade (last enabled item)
        if enabled_items:
            enabled_items[-1].click()

        # Update stored state after purchase so we can detect future changes
        store_div = driver.find_element(By.ID, "store")
        previous_html = store_div.get_attribute("innerHTML")