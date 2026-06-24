import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import page

from utils import get_env

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        
        # Retrieve the ChromeDriver executable path from environment settings
        CHROMEDRIVER_PATH = get_env()

        # Create a ChromeDriver service using the specified executable path
        service = Service(CHROMEDRIVER_PATH)

        # Initialize the Chrome browser instance
        self.driver = webdriver.Chrome(service=service)

        # Navigate to the Python official website
        self.driver.get("https://www.python.org")

    def test_search_python(self):
        
        # Create an instance of the main page object
        mainPage = page.MainPage(self.driver)

        # Verify that the page title matches the expected value
        assert mainPage.is_title_matches()

        # Enter the search keyword
        mainPage.search_text_element = "pycon"

        # Click the search button
        mainPage.click_go_button()

        # Create an instance of the search results page object
        search_result_page = page.SearchResultPage(self.driver)

        # Verify that search results are displayed
        assert search_result_page.is_result_found()

    def tearDown(self):
        
        # Close the browser after each test execution
        self.driver.close()


if __name__ == "__main__":
    # Run the test suite
    unittest.main()