import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options for headless execution (Docker-friendly)
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  # Required in Docker/Linux environments
chrome_options.add_argument("--headless")  # Run Chrome without UI
chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues (/dev/shm -> /tmp)

# Path to the ChromeDriver executable installed in the system
service = Service("/usr/bin/chromedriver")

# Initialize the Selenium WebDriver with Chrome
driver = webdriver.Chrome(service=service, options=chrome_options)

# -------------------------
# Test API (IP information)
# -------------------------
print("Info Proxy:")
url_test = "https://ipinfo.io/json"

# Open the URL in the browser
driver.get(url_test)

# Print raw JSON response from the page body
print(driver.find_element("tag name", "body").text)

print("")

# -------------------------
# Web scraping section
# -------------------------
print("Info scraping:")
url = "http://www.neuralnine.com/books"

# Open target website
driver.get(url)

# Parse the page source with BeautifulSoup using lxml parser
soup = BeautifulSoup(driver.page_source, features='lxml')

# Extract all elements matching the target CSS class
headings = soup.find_all(attrs={'class': 'elementor-image-box-title'})

# Print extracted text content
for heading in headings:
    print(heading.getText())

# Keep browser open for debugging purposes (optional delay)
time.sleep(10)

# Close the browser and free resources
driver.quit()