from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class BasePageElement(object):

    def __set__(self, obj, value):
        
        # Get the WebDriver instance from the page object
        driver = obj.driver

        # Wait until the element identified by its name attribute is present
        WebDriverWait(driver, 100).until(
            lambda d: d.find_element(By.NAME, self.locator)
        )

        # Clear any existing text from the input field
        driver.find_element(By.NAME, self.locator).clear()

        # Enter the provided value into the input field
        driver.find_element(By.NAME, self.locator).send_keys(value)

    def __get__(self, obj, owner):
        
        # Get the WebDriver instance from the page object
        driver = obj.driver

        # Wait until the element identified by its name attribute is present
        WebDriverWait(driver, 100).until(
            lambda d: d.find_element(By.NAME, self.locator)
        )

        # Retrieve the element
        element = driver.find_element(By.NAME, self.locator)

        # Return the current value of the input field
        return element.get_attribute("value")