from locator import *
from element import BasePageElement

class SearchTextElement(BasePageElement):
    
    # Locator name for the search input field
    locator = "q"


class BasePage(object):

    def __init__(self, driver):
        
        # Store the WebDriver instance for use by page objects
        self.driver = driver


class MainPage(BasePage):

    # Descriptor used to interact with the search input field
    search_text_element = SearchTextElement()

    def is_title_matches(self):
        
        # Check that the page title contains "Python"
        return "Python" in self.driver.title

    def click_go_button(self):
        
        # Locate and click the search submit button
        element = self.driver.find_element(*MainPageLocators.GO_BUTTON)
        element.click()


class SearchResultPage(BasePage):

    def is_result_found(self):
        
        # Verify that the search returned at least one result
        return "No results found." not in self.driver.page_source