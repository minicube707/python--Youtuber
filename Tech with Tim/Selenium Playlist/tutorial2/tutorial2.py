from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import get_env

# Retrieve the ChromeDriver executable path from environment variables (.env file)
CHROMEDRIVER_PATH = get_env()

# Configure Chrome browser options
options = Options()

# Keep the browser open after the script finishes execution
options.add_experimental_option("detach", True)

# Create a ChromeDriver service using the specified executable path
service = Service(CHROMEDRIVER_PATH)

# Initialize a new Chrome WebDriver instance with the given service and options
driver = webdriver.Chrome(service=service, options=options)

# Maximize the browser window to full screen size
driver.maximize_window()

# Navigate to the French Wikipedia main page
driver.get("https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal")

# Print current page information (URL and title)
print("\nCurrent Website")
print(driver.current_url)
print(driver.title)


# Wait until the search input field is clickable, then interact with it
search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "cdx-text-input__input")))

# Type the search query into the search bar
search.send_keys("Python_(langage)")

# Simulate pressing ENTER to launch the search
search.send_keys(Keys.ENTER)


# Wait until the page title contains "Python" (indicating navigation is complete)
WebDriverWait(driver, 10).until(lambda d: "Python" in d.title)

# Print updated page information after navigation
print("\nNew Website")
print(driver.current_url)
print(driver.title)


# Wait until the main content of the article is loaded in the DOM
main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mw-content-text")))

# Print the extracted text content of the article
print("content")
print(main.text)